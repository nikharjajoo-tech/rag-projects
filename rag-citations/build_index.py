"""Builds a cleaner database from the two test PDFs: housekeeping fixes for search (2026-10-08).

    fix 1, --drop-references: removes each paper's reference list before chunking. A third of the chunks
           search returned in run `cited` were reference entries, taking slots real passages could use.
    fix 2, --sentences: chunks are built from whole sentences (no fact cut in half, like Q12's
           "BACE1, a protein involved | in ... Alzheimer's"), and each chunk starts with the previous chunk's
           last sentence, so neighbours really overlap. Without it: the app's splitter (400 / 80).

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-citations/build_index.py pharma_db_norefs.json --drop-references
    rag-chain/.venv/bin/python rag-citations/build_index.py pharma_db_sentences.json --drop-references --sentences

The database goes to rag-chain/ next to the others. Chunks whose text is already in rag-chain/pharma_db.json
reuse that embedding instead of being sent to Google again (saves free-tier quota).
"""
import argparse
import os
import re
import sys
import time
import uuid

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CITATIONS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CITATIONS_DIR, "..", "rag-eval"))
from run_eval import RAG_CHAIN_DIR, DOCS, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, db_path

MAX_CARRIED_SENTENCE = 200  # longer last sentences aren't repeated in the next chunk, or chunks would balloon
EMBED_BATCH_SIZE = 50


def read_pages(pdf_path):
    """The text of each page, as PyPDFLoader (used by the app) extracts it."""
    return [page.extract_text() for page in PdfReader(pdf_path).pages]


def drop_references(pages):
    """Removes the reference list: from a line that is just 'Reference(s)' up to the next page that starts with a
    figure or table caption (Chen keeps its figures and Table 1 after the references; Q11 needs Table 1)."""
    kept, in_references = [], False
    for text in pages:
        body = re.sub(r"^\s*\d+\s*\n", "", text)  # page number at the top of the page
        if in_references and re.match(r"\s*(Figure|Table) \d", body):
            in_references = False
        if in_references:
            kept.append("")
            continue
        heading = re.search(r"^\s*References?\s*:?\s*$", text, re.M | re.I)
        if heading:
            text, in_references = text[:heading.start()], True
        kept.append(text)
    return kept


def splitter_chunks(pages, file_name):
    """The app's chunking: each page split on its own with RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    docs = [Document(page_content=text, metadata={"source": f"./temp/{file_name}", "page": i})
            for i, text in enumerate(pages) if text.strip()]
    return splitter.split_documents(docs)


def sentences_of(pages):
    """(page, sentence) pairs in reading order. A sentence that runs over a page break is joined back
    together and belongs to the page where it starts."""
    out = []
    for page, text in enumerate(pages):
        text = re.sub(r"^\s*\d+\s*\n", "", text)  # page number at the top of the page
        text = " ".join(text.split())  # PDF line breaks -> spaces
        if not text:
            continue
        # A sentence ends at . ! or ? followed by a space and a capital letter, digit, quote or bracket
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(\[])", text)
        if out and not re.search(r"[.!?][”\"')\]]?\s*(\d+(,\d+)*)?$", out[-1][1]):
            out[-1] = (out[-1][0], out[-1][1] + " " + parts.pop(0))  # continues from the previous page
        out += [(page, p) for p in parts if p]
    # A "sentence" far longer than a chunk (e.g. a table read as one line) is cut on word boundaries
    split = []
    for page, s in out:
        while len(s) > 1.5 * CHUNK_SIZE:
            cut = s.rfind(" ", 0, CHUNK_SIZE)
            split.append((page, s[:cut]))
            s = s[cut + 1:]
        split.append((page, s))
    return split


def sentence_chunks(pages, file_name):
    """Packs whole sentences into chunks of up to ~400 characters. Each chunk starts with the last sentence
    of the chunk before it (if that sentence is short enough), so a fact near a boundary is whole in one of them."""
    sentences = sentences_of(pages)
    chunks, start, carried = [], 0, None
    while start < len(sentences):
        picked = ([carried] if carried is not None else []) + [start]  # always at least one new sentence
        end = start + 1
        while end < len(sentences) and sum(len(sentences[i][1]) + 1 for i in picked) + len(sentences[end][1]) <= CHUNK_SIZE:
            picked.append(end)
            end += 1
        page = sentences[picked[0]][0]
        chunks.append(Document(page_content=" ".join(sentences[i][1] for i in picked),
                               metadata={"source": f"./temp/{file_name}", "page": page}))
        last = picked[-1]
        carried = last if len(picked) > 1 and len(sentences[last][1]) <= MAX_CARRIED_SENTENCE else None
        start = end
    return chunks


def embed_missing(texts, embedding_model, known):
    """Embeds the texts that have no stored embedding yet, waiting out the per-minute limit."""
    missing = [t for t in dict.fromkeys(texts) if t not in known]
    print(f"{len(texts) - sum(t in missing for t in texts)} chunks reuse a stored embedding; embedding {len(missing)} new ones")
    done = 0
    while done < len(missing):
        batch = missing[done:done + EMBED_BATCH_SIZE]
        try:
            vectors = embedding_model.embed_documents(batch)
        except Exception as e:
            if "RESOURCE_EXHAUSTED" not in str(e) and "429" not in str(e):
                raise
            if "PerDay" in str(e):
                sys.exit(f"Daily free-tier embedding limit reached after {done} of {len(missing)} chunks.")
            match = re.search(r"retry in ([\d.]+)s", str(e))
            wait_seconds = int(float(match.group(1))) + 2 if match else 60
            print(f"  hit the per-minute limit; waiting {wait_seconds}s...")
            time.sleep(wait_seconds)
            continue
        known.update(zip(batch, vectors))
        done += len(batch)
        print(f"  embedded {done} of {len(missing)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_name", help="file name for the new database, e.g. pharma_db_norefs.json")
    parser.add_argument("--drop-references", action="store_true")
    parser.add_argument("--sentences", action="store_true")
    args = parser.parse_args()

    chunks = []
    for file_name in DOCS.values():
        pages = read_pages(os.path.join(RAG_CHAIN_DIR, "test_docs", file_name))
        if args.drop_references:
            before = sum(len(p) for p in pages)
            pages = drop_references(pages)
            print(f"{file_name}: reference list removed ({before - sum(len(p) for p in pages):,} of {before:,} characters)")
        doc_chunks = sentence_chunks(pages, file_name) if args.sentences else splitter_chunks(pages, file_name)
        print(f"  -> {len(doc_chunks)} chunks")
        chunks += doc_chunks

    embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
    old = InMemoryVectorStore.load(db_path(CHUNK_SIZE, CHUNK_OVERLAP), embedding_model)
    known = {d["text"]: d["vector"] for d in old.store.values()}
    embed_missing([c.page_content for c in chunks], embedding_model, known)

    db = InMemoryVectorStore(embedding_model)
    for c in chunks:
        doc_id = str(uuid.uuid4())
        db.store[doc_id] = {"id": doc_id, "vector": known[c.page_content], "text": c.page_content, "metadata": c.metadata}
    path = os.path.join(RAG_CHAIN_DIR, args.db_name)
    db.dump(path)
    sizes = sorted(len(c.page_content) for c in chunks)
    print(f"Saved {len(chunks)} chunks to rag-chain/{args.db_name} "
          f"(length: median {sizes[len(sizes) // 2]}, longest {sizes[-1]} characters)")


if __name__ == "__main__":
    main()
