"""Breaks the verifier on purpose: gives it good claims with a wrong citation, and counts how many it catches.

The hand check agreed with the verifier on 28 of 28 claims, but 27 of them were supported, so a verifier
that always says "supported" would score almost as well. This test measures the case that matters: a
citation that does NOT support its claim.

Each supported claim from a run is checked three ways:
    real: its real citation, as a control: a stricter verifier must not start rejecting good citations
and re-pointed at a different chunk from the same search results:
    easy: the chunk sharing the fewest words with the claim (clearly unrelated)
    hard: the chunk sharing the most words with the claim, other than the real one (same topic, the
          kind of near-miss citation the app really made in Q12)
Then the verifier checks each question's claims in one call, exactly as in run_cited.py.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-citations/break_verifier.py cited v2    # v2 = label for this verifier version

Writes results/<run>_break_<label>.csv: one row per planted wrong citation, with the verdict and a blank hand column.
In the "hard" version the wrong chunk can turn out to state the claim too, so check every
"supported" verdict by hand before counting it as a miss.
"""
import csv
import os
import re
import sys
from collections import defaultdict

from langchain_google_genai import ChatGoogleGenerativeAI

from run_cited import CITATIONS_DIR, VERIFIER_MODEL, Verification, verify
from grade import parse_run  # rag-eval/grade.py, on the path via run_cited

STOPWORDS = {"that", "this", "with", "from", "were", "have", "which", "their", "about", "these", "they", "there"}


def words(text):
    return {w for w in re.findall(r"[a-z0-9%.]+", text.lower()) if len(w) >= 4 and w not in STOPWORDS}


def main():
    run_name, label = sys.argv[1], sys.argv[2]
    results_dir = os.path.join(CITATIONS_DIR, "results")
    reports = {q["id"]: q for q in parse_run(open(os.path.join(results_dir, f"{run_name}.md")).read())}
    claims = [c for c in csv.DictReader(open(os.path.join(results_dir, f"{run_name}_claims.csv")))
              if c["verifier"] == "supported"]
    verifier = ChatGoogleGenerativeAI(model=VERIFIER_MODEL, api_key=os.getenv("GOOGLE_API_KEY"),
                                      temperature=0).with_structured_output(Verification)

    by_question = defaultdict(list)
    for c in claims:
        by_question[c["id"]].append(c)

    out = []
    for qid, question_claims in by_question.items():
        sources_text = reports[qid]["chunks"]  # "[1] (Chen p4) text...", the same text the verifier saw in the run
        chunks = dict(re.findall(r"^\[(\d+)\] (.*)$", sources_text, re.M))
        for version in ["real", "easy", "hard"]:
            rows = []
            for c in question_claims:
                real = {int(n) for n in re.findall(r"\[(\d+)\]", c["cited"])}
                others = [int(n) for n in chunks if int(n) not in real]
                overlap = {n: len(words(c["text"]) & words(chunks[str(n)])) for n in others}
                if version == "real":
                    wrong = min(real)  # all real citations in this run cite a single chunk
                    overlap[wrong] = len(words(c["text"]) & words(chunks[str(wrong)]))
                else:
                    wrong = (min if version == "easy" else max)(others, key=lambda n: overlap[n])
                rows.append({"claim": int(c["claim"]), "text": c["text"], "sources": [wrong], "verifier": "",
                             "verifier_reason": "", "real": c["cited"], "wrong": f"[{wrong}] {re.match(r'\((\w+ p\d+)\)', chunks[str(wrong)]).group(1)}",
                             "shared_words": overlap[wrong]})
            print(f"{qid} ({version}): checking {len(rows)} claims with wrong citations")
            verify(verifier, rows, sources_text)
            out += [{"id": qid, "version": version, "claim": r["claim"], "text": r["text"], "real citation": r["real"],
                     "planted citation": r["wrong"], "shared_words": r["shared_words"], "verifier": r["verifier"],
                     "verifier_reason": r["verifier_reason"], "hand: does the planted chunk state it? (yes/no)": ""}
                    for r in rows]

    path = os.path.join(results_dir, f"{run_name}_break_{label}.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        writer.writeheader()
        writer.writerows(out)

    print(f"\nSaved results/{run_name}_break_{label}.csv\n")
    for version in ["real", "easy", "hard"]:
        rows = [r for r in out if r["version"] == version]
        verdicts = [r["verifier"] for r in rows]
        print(f"{version:<5} ({len(rows)} claims): {verdicts.count('supported')} supported, "
              f"{verdicts.count('partly')} partly, {verdicts.count('not supported')} not supported")


if __name__ == "__main__":
    main()
