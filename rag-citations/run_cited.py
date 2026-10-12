"""Stage 3: answers every test question with citations, then has a second model call check each citation.

Same search as Stage 2's reference run (400 / 80, top-k 5, flash-lite, temperature 1). What changes:
  1. The chunks are numbered in the prompt, and the model must cite a chunk number for every claim.
  2. A verifier call checks each claim against the chunk(s) it cites: supported, partly, or not supported.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-citations/run_cited.py cited
    rag-chain/.venv/bin/python rag-citations/run_cited.py smoke --only Q01,Q13,Q17   # a few questions only
    rag-chain/.venv/bin/python rag-citations/run_cited.py old --db pharma_db.json   # Stage 2's database instead of the default

Writes three files to rag-citations/results/:
    <run>.md           every answer next to its claim checks and chunks, for reading. Same layout as
                       Stage 2's reports, so rag-eval/grade.py can grade it.
    <run>_grades.csv   one row per question (blank columns for hand grades, as in Stage 2)
    <run>_claims.csv   one row per claim, with the verifier's verdict and a blank column for your hand check
"""
import argparse
import csv
import os
import re
import sys
import time
from typing import Literal

from pydantic import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore

CITATIONS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CITATIONS_DIR, "..", "rag-eval"))
import run_eval  # Stage 2's runner: same settings, search, retry and page-checking code
from run_eval import (CHAT_MODEL, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, TEMPERATURE, DOCS,
                      EVAL_DIR, expected_pages, with_retry)

DEFAULT_DB = "pharma_db_sentences.json"  # since 2026-10-12: reference lists removed, whole-sentence chunks (build_index.py)
VERIFIER_MODEL = "gemini-3.5-flash-lite"  # same family as the answering model: free, but may go easy on its own style


# --- Step 1: the answer, with a source number on every claim ---------------------------------------------

class CitedSentence(BaseModel):
    text: str = Field(description="One short sentence making one claim, without citation numbers in it")
    sources: list[int] = Field(description="The number(s) of the source(s) that state this claim")


class CitedAnswer(BaseModel):
    sentences: list[CitedSentence] = Field(description="The answer, one claim per sentence. Empty if the sources don't answer the question")
    not_in_sources: str = Field(description="What the question asks that the sources don't say. Empty if the answer is complete")


# Stage 1's prompt, with the chunks numbered and the citation rules added
ANSWER_PROMPT = """You are a highly knowledgeable assistant specializing in pharmaceutical sciences.
Answer the question based only on the following numbered sources:

{sources}

Question: {question}

Use the sources to answer the question accurately and concisely.
Don't justify your answers.
Don't give information not mentioned in the sources.
Write the answer as short sentences, each making one claim, and give the number(s) of the source(s) that state it.
Every claim must be stated by the source(s) you cite for it. Don't join facts from different sources into a claim none of them makes.
If the sources don't answer the question, leave the sentences empty and say what's missing in not_in_sources.
If they answer only part of it, answer that part and say what's missing in not_in_sources."""


# --- Step 2: the verifier, a second call that checks each claim against the source(s) it cites ------------

class ClaimCheck(BaseModel):
    claim_number: int
    verdict: Literal["supported", "partly", "not supported"]
    reason: str = Field(description="One sentence: what the cited source says, compared with the claim")


class Verification(BaseModel):
    checks: list[ClaimCheck]


# v2 (2026-10-08): each claim is shown with only the source(s) it cites. v1 listed all five chunks once and
# told the verifier to read only the cited ones; on wrong citations it often found support elsewhere instead.
VERIFIER_PROMPT = """You are checking the citations in an answer written by an AI research assistant.
Each numbered claim below is followed by the text of the source(s) it cites. Using only that text, decide:
- supported: the cited text states this claim. Paraphrasing is fine.
- partly: the cited text states part of the claim, but not all of it.
- not supported: the cited text doesn't state this claim, even if the claim is true.
A claim that combines facts from two sources into a new statement neither source makes is not supported.

{claims}

Return one check per claim."""


def label(doc):
    """'Chen p7': how a chunk is shown to the user, and to the grader."""
    source = os.path.basename(doc.metadata["source"])
    return f"{next(name for name, file in DOCS.items() if file == source)} p{doc.metadata['page'] + 1}"


def claim_rows(answer, results):
    """One row per claim. Claims that cite nothing, or a source number that doesn't exist, fail without a
    model call: a plain code check is free and never wrong, so it runs before the verifier."""
    rows = []
    for number, sentence in enumerate(answer.sentences, 1):
        valid = [s for s in sentence.sources if 1 <= s <= len(results)]
        cited = "; ".join(f"[{s}] {label(results[s - 1][0])}" for s in valid)
        if not valid:
            verdict, reason = "not supported", "cites no source" if not sentence.sources else "cites a source that doesn't exist"
        else:
            verdict, reason = "", ""  # filled in by the verifier
        rows.append({"claim": number, "text": sentence.text, "sources": valid, "cited": cited,
                     "verifier": verdict, "verifier_reason": reason})
    return rows


def verify(verifier, rows, sources_text):
    """One verifier call per question checks all its claims at once (one call per claim would use the
    free-tier quota up 3-4 times faster). Each claim is shown only the chunk(s) it cites."""
    to_check = [r for r in rows if not r["verifier"]]
    if not to_check:
        return
    chunks = dict(re.findall(r"^\[(\d+)\] (.*)$", sources_text, re.M))  # "[2] (Blanco p5) text" -> {"2": "(Blanco p5) text"}
    claims = "\n\n".join(f"Claim {r['claim']}: {r['text']}\n" + "\n".join(f"Cited source {chunks[str(s)]}" for s in r["sources"])
                         for r in to_check)
    result = with_retry(lambda: verifier.invoke(VERIFIER_PROMPT.format(claims=claims)))
    checks = {c.claim_number: c for c in result.checks}
    for r in to_check:
        check = checks.get(r["claim"])
        r["verifier"], r["verifier_reason"] = (check.verdict, check.reason) if check else ("not checked", "verifier skipped it")


def render(answer, results, for_user, rows=None):
    """The answer as text. The grader sees chunk number and paper ([2 Chen p7]): with bare numbers it didn't
    count a citation as saying which paper says what. The user sees only where each claim comes from (Chen p7),
    and, once the verifier has run (rows), a warning on every claim its cited source doesn't fully confirm:
    the claim stays visible for the researcher to accept, edit or reject (decided 2026-10-12, EXPERIMENTS.md).
    Refusals say "I couldn't find": the documents may hold the answer even when search missed it (Q03, Q15)."""
    parts = []
    for i, sentence in enumerate(answer.sentences):
        valid = [s for s in sentence.sources if 1 <= s <= len(results)]
        if for_user:
            labels = list(dict.fromkeys(label(results[s - 1][0]) for s in valid))  # two chunks from one page: show once
            tag = f" ({'; '.join(labels)})" if labels else " (no source)"
            verdict = rows[i]["verifier"] if rows else "supported"
            if verdict != "supported":
                warning = "only partly confirmed" if verdict == "partly" else "not confirmed"
                parts.append(f"⚠ {sentence.text.rstrip()}{tag} [{warning} by the cited source: accept, edit or reject]")
                continue
        else:
            tag = " " + "".join(f"[{s} {label(results[s - 1][0])}]" if s in valid else f"[{s}]"
                                for s in sentence.sources) if sentence.sources else ""
        parts.append(sentence.text.rstrip() + tag)
    text = " ".join(parts)
    missing = answer.not_in_sources.strip()
    if not answer.sentences:
        return f"I couldn't find this in the documents. {missing}".strip()
    return f"{text} Not found in the documents: {missing}" if missing else text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_name")
    parser.add_argument("--only", help="comma-separated question ids, e.g. Q01,Q17, for a quick test")
    parser.add_argument("--test-set", help="questions file (default: rag-eval/test_set.csv), e.g. rag-citations/test_set_nearmiss.csv")
    parser.add_argument("--db", default=DEFAULT_DB, help=f"database file in rag-chain/ (default: {DEFAULT_DB}); see build_index.py")
    args = parser.parse_args()
    api_key = os.getenv("GOOGLE_API_KEY")
    db_file = os.path.join(run_eval.RAG_CHAIN_DIR, args.db)
    db = InMemoryVectorStore.load(db_file,
                                  GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=api_key))
    answerer = ChatGoogleGenerativeAI(model=CHAT_MODEL, api_key=api_key, temperature=TEMPERATURE).with_structured_output(CitedAnswer)
    verifier = ChatGoogleGenerativeAI(model=VERIFIER_MODEL, api_key=api_key, temperature=0).with_structured_output(Verification)

    with open(args.test_set or os.path.join(EVAL_DIR, "test_set.csv")) as f:
        questions = list(csv.DictReader(f))
    if args.only:
        questions = [q for q in questions if q["id"] in args.only.split(",")]

    results_dir = os.path.join(CITATIONS_DIR, "results")
    os.makedirs(results_dir, exist_ok=True)
    report = [f"# Run: {args.run_name}\n",
              f"Settings: model `{CHAT_MODEL}`, chunk size {CHUNK_SIZE} / overlap {CHUNK_OVERLAP}, top-k {TOP_K}, "
              f"temperature {TEMPERATURE}; cited answers checked by `{VERIFIER_MODEL}` (temperature 0); "
              f"database `{os.path.basename(db_file)}`\n"]
    grades, claims = [], []

    for row in questions:
        print(f"{row['id']}: {row['question'][:70]}")
        start, waited_before = time.time(), run_eval.waited_seconds
        results = with_retry(lambda: db.similarity_search_with_score(row["question"], k=TOP_K))
        sources_text = "\n\n".join(f"[{i}] ({label(doc)}) {' '.join(doc.page_content.split())}"
                                   for i, (doc, _) in enumerate(results, 1))
        answer = with_retry(lambda: answerer.invoke(ANSWER_PROMPT.format(sources=sources_text, question=row["question"])))
        answer_seconds = time.time() - start - (run_eval.waited_seconds - waited_before)  # excludes rate-limit waits

        start, waited_before = time.time(), run_eval.waited_seconds
        rows = claim_rows(answer, results)
        verify(verifier, rows, sources_text)
        verify_seconds = time.time() - start - (run_eval.waited_seconds - waited_before)

        wanted = expected_pages(row)
        found = {(os.path.basename(doc.metadata["source"]), doc.metadata["page"] + 1) for doc, _ in results}
        retrieval = f"{len(wanted & found)} of {len(wanted)} expected pages" if wanted else "n/a (unanswerable)"
        verdicts = [r["verifier"] for r in rows]
        supported = f"{verdicts.count('supported')} supported, {verdicts.count('partly')} partly, " \
                    f"{len(verdicts) - verdicts.count('supported') - verdicts.count('partly')} not supported"

        report.append(f"\n---\n\n## {row['id']} ({row['question_type']})\n")
        report.append(f"**Question:** {row['question']}\n")
        report.append(f"**Expected:** {row['correct_answer']}\n")
        report.append(f"**App answered:** {render(answer, results, for_user=False)}\n")
        report.append(f"**Search:** {retrieval} found · {answer_seconds:.1f}s to answer + {verify_seconds:.1f}s to verify\n")
        if row["notes"]:
            report.append(f"**Notes:** {row['notes']}\n")
        report.append(f"**User sees:** {render(answer, results, for_user=True, rows=rows)}\n")
        report.append(f"**Claim checks:** {supported if rows else 'no claims (refused)'}\n")
        for r in rows:
            report.append(f"- Claim {r['claim']} → {r['cited'] or 'no valid source'}: **{r['verifier']}**. "
                          f"{r['text']}  \n  *Verifier:* {r['verifier_reason']}")
        report.append("\n**Retrieved chunks:**\n")
        for rank, (doc, score) in enumerate(results, 1):
            source = os.path.basename(doc.metadata["source"])
            marker = " ✅ expected page" if (source, doc.metadata["page"] + 1) in wanted else ""
            report.append(f"\n{rank}. *{label(doc)}, similarity {score:.3f}*{marker}\n   > {' '.join(doc.page_content.split())}\n")

        grades.append({"id": row["id"], "question_type": row["question_type"], "question": row["question"],
                       "expected": row["correct_answer"], "answer": render(answer, results, for_user=False),
                       "retrieval": retrieval, "refused": "yes" if not answer.sentences else "no",
                       "claims": len(rows), "supported": verdicts.count("supported"), "partly": verdicts.count("partly"),
                       "top_similarity": f"{results[0][1]:.3f}",
                       "answer_seconds": f"{answer_seconds:.1f}", "verify_seconds": f"{verify_seconds:.1f}",
                       "correct (yes/partly/no)": "", "faithful (yes/no)": "", "failure_pattern": "", "my_notes": ""})
        claims += [{"id": row["id"], "question_type": row["question_type"], "claim": r["claim"], "text": r["text"],
                    "cited": r["cited"], "verifier": r["verifier"], "verifier_reason": r["verifier_reason"],
                    "hand (supported/partly/not supported)": "", "my_notes": ""} for r in rows]

    with open(os.path.join(results_dir, f"{args.run_name}.md"), "w") as f:
        f.write("\n".join(report))
    for suffix, table in [("grades", grades), ("claims", claims)]:
        if table:
            with open(os.path.join(results_dir, f"{args.run_name}_{suffix}.csv"), "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(table[0].keys()))
                writer.writeheader()
                writer.writerows(table)
    print(f"\nSaved results/{args.run_name}.md, _grades.csv and _claims.csv in rag-citations/")


if __name__ == "__main__":
    main()
