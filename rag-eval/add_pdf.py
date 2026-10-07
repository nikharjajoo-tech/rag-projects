"""Adds a PDF to the stage-1 database, chunked exactly the way the rag-chain app does it.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-eval/add_pdf.py rag-chain/test_docs/<file>.pdf
    rag-chain/.venv/bin/python rag-eval/add_pdf.py rag-chain/test_docs/<file>.pdf --overlap 80   # experiment database
"""
import argparse
import os
import re
import sys
import time

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from run_eval import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, db_path

EMBED_BATCH_SIZE = 50

parser = argparse.ArgumentParser()
parser.add_argument("pdf_path")
parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)  # defaults match rag-chain/app.py
parser.add_argument("--overlap", type=int, default=CHUNK_OVERLAP)
args = parser.parse_args()
pdf_path = args.pdf_path
file_name = os.path.basename(pdf_path)
DB_PATH = db_path(args.chunk_size, args.overlap)

embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
db = InMemoryVectorStore.load(DB_PATH, embedding_model) if os.path.exists(DB_PATH) else InMemoryVectorStore(embedding_model)

# Refuse to add the same PDF twice: duplicate chunks would crowd out other results in the top-k
if any(doc["metadata"].get("source", "").endswith(file_name) for doc in db.store.values()):
    sys.exit(f"{file_name} is already in the database; nothing to do.")

pages = PyPDFLoader(pdf_path).load()
for page in pages:
    page.metadata["source"] = f"./temp/{file_name}"  # same source format the app writes
splitter = RecursiveCharacterTextSplitter(chunk_size=args.chunk_size, chunk_overlap=args.overlap)
chunks = splitter.split_documents(pages)
print(f"{file_name}: {len(pages)} pages -> {len(chunks)} chunks ({args.chunk_size} / {args.overlap}) -> {os.path.basename(DB_PATH)}")

# Embed in batches, waiting out the free-tier per-minute limit (100 chunks/minute)
done = 0
while done < len(chunks):
    batch = chunks[done:done + EMBED_BATCH_SIZE]
    try:
        db.add_documents(batch)
    except Exception as e:
        if "RESOURCE_EXHAUSTED" not in str(e) and "429" not in str(e):
            raise
        if "PerDay" in str(e):
            sys.exit(f"Daily free-tier embedding limit reached after {done} of {len(chunks)} chunks.")
        match = re.search(r"retry in ([\d.]+)s", str(e))
        wait_seconds = int(float(match.group(1))) + 2 if match else 60
        print(f"Hit the per-minute limit; waiting {wait_seconds}s...")
        time.sleep(wait_seconds)
        continue
    done += len(batch)
    db.dump(DB_PATH)
    print(f"Embedded {done} of {len(chunks)} chunks")

print(f"Done. Database now holds {len(db.store)} chunks.")
