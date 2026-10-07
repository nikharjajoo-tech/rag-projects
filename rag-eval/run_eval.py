"""Runs every question in test_set.csv through the stage-1 RAG pipeline and saves the results for grading.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-eval/run_eval.py baseline

Writes two files to rag-eval/results/:
    <run_name>.md          every answer next to the chunks it was based on, for reading
    <run_name>_grades.csv  one row per question, with blank columns for you to grade
"""
import csv
import os
import re
import sys
import time

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_CHAIN_DIR = os.path.join(EVAL_DIR, "..", "rag-chain")
load_dotenv(os.path.join(RAG_CHAIN_DIR, ".env"))

# The settings under test. Keep these identical to rag-chain/app.py for the baseline run.
CHAT_MODEL = "gemini-3.5-flash-lite"
EMBEDDING_MODEL = "models/gemini-embedding-001"
DB_PATH = os.path.join(RAG_CHAIN_DIR, "pharma_db.json")  # built with chunk_size=400, chunk_overlap=200
TOP_K = 5
TEMPERATURE = 1  # Google recommends the default 1.0 for Gemini 3 models

# Copied word for word from rag-chain/app.py
PROMPT_TEMPLATE = """
    You are a highly knowledgeable assistant specializing in pharmaceutical sciences.
    Answer the question based only on the following context:
    {context}

    Answer the question based on the above context:
    {question}

    Use the provided context to answer the user's question accurately and concisely.
    Don't justify your answers.
    Don't give information not mentioned in the CONTEXT INFORMATION.
    Do not say "according to the context" or "mentioned in the context" or similar.
    """

# Short names used in test_set.csv -> PDF file names
DOCS = {
    "Chen": "AI_Drug_Development_Real_World_Data_2101.08904.pdf",
    "Blanco": "Role_of_AI_in_Drug_Discovery_2212.08104.pdf",
}


def expected_pages(row):
    """Turns the source_pdf and page columns into a set of (file name, page) pairs.

    Handles "Chen" + "7; 8", and "Both" + "Chen 7; Blanco 5-6". Pages are 1-based, as printed in the PDF viewer."""
    if not row["page"]:
        return set()
    pairs = set()
    for part in row["page"].split(";"):
        part = part.strip()
        doc = row["source_pdf"]
        for name in DOCS:
            if part.startswith(name):
                doc, part = name, part[len(name):].strip()
        for piece in part.split(","):
            start, _, end = piece.strip().partition("-")
            for page in range(int(start), int(end or start) + 1):
                pairs.add((DOCS[doc], page))
    return pairs


waited_seconds = 0  # time spent waiting on rate limits, excluded from latency


def with_retry(call):
    """Runs an API call, waiting and retrying when we hit the free-tier per-minute limit
    or Google's servers are temporarily overloaded (503)."""
    global waited_seconds
    overloaded_attempts = 0
    while True:
        try:
            return call()
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                overloaded_attempts += 1
                if overloaded_attempts > 6:
                    raise
                wait_seconds = 15 * overloaded_attempts
                print(f"  model overloaded (503); waiting {wait_seconds}s...")
                time.sleep(wait_seconds)
                waited_seconds += wait_seconds
                continue
            if "RESOURCE_EXHAUSTED" not in str(e) and "429" not in str(e):
                raise
            if "PerDay" in str(e):
                sys.exit("Daily free-tier limit reached; run again tomorrow.")
            match = re.search(r"retry in ([\d.]+)s", str(e))
            wait_seconds = int(float(match.group(1))) + 2 if match else 60
            print(f"  hit the per-minute limit; waiting {wait_seconds}s...")
            time.sleep(wait_seconds)
            waited_seconds += wait_seconds


def main():
    run_name = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    api_key = os.getenv("GOOGLE_API_KEY")
    db = InMemoryVectorStore.load(DB_PATH, GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=api_key))
    chain = (ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
             | ChatGoogleGenerativeAI(model=CHAT_MODEL, api_key=api_key, temperature=TEMPERATURE)
             | StrOutputParser())

    with open(os.path.join(EVAL_DIR, "test_set.csv")) as f:
        questions = list(csv.DictReader(f))

    os.makedirs(os.path.join(EVAL_DIR, "results"), exist_ok=True)
    report = [f"# Run: {run_name}\n",
              f"Settings: model `{CHAT_MODEL}`, chunk size 400 / overlap 200, top-k {TOP_K}, temperature {TEMPERATURE}\n"]
    grades = []

    for row in questions:
        print(f"{row['id']}: {row['question'][:70]}")
        start, waited_before = time.time(), waited_seconds
        # Search: the same similarity search the app uses, plus the score of each chunk
        results = with_retry(lambda: db.similarity_search_with_score(row["question"], k=TOP_K))
        search_seconds = time.time() - start - (waited_seconds - waited_before)
        context = "\n\n".join(doc.page_content for doc, _ in results)
        answer = with_retry(lambda: chain.invoke({"context": context, "question": row["question"]}))
        total_seconds = time.time() - start - (waited_seconds - waited_before)  # excludes rate-limit waits

        # Retrieval check: did the search bring back chunks from the page(s) where the answer is?
        wanted = expected_pages(row)
        found = {(os.path.basename(doc.metadata["source"]), doc.metadata["page"] + 1) for doc, _ in results}
        if not wanted:
            retrieval = "n/a (unanswerable)"
        else:
            retrieval = f"{len(wanted & found)} of {len(wanted)} expected pages"

        report.append(f"\n---\n\n## {row['id']} ({row['question_type']})\n")
        report.append(f"**Question:** {row['question']}\n")
        report.append(f"**Expected:** {row['correct_answer']}\n")
        report.append(f"**App answered:** {answer.strip()}\n")
        report.append(f"**Search:** {retrieval} found · {total_seconds:.1f}s total ({search_seconds:.1f}s search)\n")
        if row["notes"]:
            report.append(f"**Notes:** {row['notes']}\n")
        report.append("\n**Retrieved chunks:**\n")
        for rank, (doc, score) in enumerate(results, 1):
            source = os.path.basename(doc.metadata["source"])
            short = next(name for name, file in DOCS.items() if file == source)
            page = doc.metadata["page"] + 1
            marker = " ✅ expected page" if (source, page) in wanted else ""
            text = " ".join(doc.page_content.split())
            report.append(f"\n{rank}. *{short} p{page}, similarity {score:.3f}*{marker}\n   > {text}\n")

        grades.append({"id": row["id"], "question_type": row["question_type"], "question": row["question"],
                       "expected": row["correct_answer"], "answer": answer.strip(), "retrieval": retrieval,
                       "seconds": f"{total_seconds:.1f}",
                       "correct (yes/partly/no)": "", "faithful (yes/no)": "", "failure_pattern": "", "my_notes": ""})

    with open(os.path.join(EVAL_DIR, "results", f"{run_name}.md"), "w") as f:
        f.write("\n".join(report))
    with open(os.path.join(EVAL_DIR, "results", f"{run_name}_grades.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grades[0].keys()))
        writer.writeheader()
        writer.writerows(grades)
    print(f"\nSaved results/{run_name}.md and results/{run_name}_grades.csv")


if __name__ == "__main__":
    main()
