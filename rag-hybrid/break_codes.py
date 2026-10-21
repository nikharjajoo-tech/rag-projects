"""Break meaning-based search on purpose: near-identical codes (learning-loop step 4, "break it").

Adds 14 made-up chunks to an in-memory copy of the library (the database file is never changed):
    8 trial registry entries, identical except the last digit of the trial ID and the patient count
    6 compound records whose codes use the same four digits in a different order, each with its own potency
Then asks 7 questions that name one ID or code, and reports where the matching chunk ranks under each method.
Everything here is fictional: no real trial or compound.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-hybrid/break_codes.py

Costs 1 Gemini embedding call for the 14 chunks, 7 for the questions, and 14 Cohere calls (all cached in cache/).
Writes results/break_codes.md.
"""
import os

import numpy as np
from langchain_core.documents import Document

from search import HYBRID_DIR, MODES, BM25, Cache, Searcher
from run_eval import TOP_K, with_retry

ENROLLED = [212, 348, 156, 420, 275, 190, 305, 238]
TRIALS = {f"NCT0451234{n}": (f"Registry entry NCT0451234{n}: a phase 2 trial of an oral BACE1 inhibitor in early "
                             f"Alzheimer's disease, which enrolled {patients} patients and reported its primary "
                             f"outcome at 52 weeks.")
          for n, patients in enumerate(ENROLLED, 1)}
POTENCY = {"RX-2041": 12, "RX-2014": 85, "RX-2401": 7, "RX-2104": 140, "RX-4021": 33, "RX-2410": 61}
COMPOUNDS = {code: f"Compound {code} inhibited BACE1 with an IC50 of {nm} nM in cell assays and was taken forward "
                   f"for further testing."
             for code, nm in POTENCY.items()}
QUESTIONS = [("How many patients did trial NCT04512343 enroll?", "NCT04512343"),
             ("How many patients did trial NCT04512346 enroll?", "NCT04512346"),
             ("How many patients did trial NCT04512348 enroll?", "NCT04512348"),
             ("How many patients did trial NCT04512341 enroll?", "NCT04512341"),
             ("What IC50 did compound RX-2014 show against BACE1?", "RX-2014"),
             ("What IC50 did compound RX-2401 show against BACE1?", "RX-2401"),
             ("What IC50 did compound RX-4021 show against BACE1?", "RX-4021")]


def add_synthetic_chunks(searcher):
    """Appends the made-up chunks to the searcher's chunks, embeddings and keyword index. Returns {code: index}."""
    texts = {**TRIALS, **COMPOUNDS}
    cache = Cache("synthetic_codes.json")
    missing = [t for t in texts.values() if not cache.get(t)]
    if missing:
        for text, vector in zip(missing, with_retry(lambda: searcher.embeddings.embed_documents(missing))):
            cache.put(text, vector)
    start = len(searcher.docs)
    searcher.docs += [Document(id=f"synthetic-{code}", page_content=text, metadata={"source": "synthetic", "page": 0})
                      for code, text in texts.items()]
    vectors = np.array([cache.get(t) for t in texts.values()])
    searcher.vectors = np.vstack([searcher.vectors, vectors / np.linalg.norm(vectors, axis=1, keepdims=True)])
    searcher.bm25 = BM25([d.page_content for d in searcher.docs])
    return {code: start + i for i, code in enumerate(texts)}


def main():
    searcher = Searcher()
    where = add_synthetic_chunks(searcher)
    rows = []
    for question, code in QUESTIONS:
        ranks = {}
        for mode in MODES:
            ranking, _ = searcher.ranking(question, mode)
            ranks[mode] = next(r for r, (i, _) in enumerate(ranking, 1) if i == where[code])
        rows.append((code, ranks))
        print(f"{code}: " + "  ".join(f"{m} {r}" for m, r in ranks.items()))

    report = ["# Breaking meaning-based search with near-identical codes\n",
              f"{len(TRIALS) + len(COMPOUNDS)} made-up chunks added to the {len(searcher.docs) - len(TRIALS) - len(COMPOUNDS)}"
              f" real ones: {len(TRIALS)} trial entries that differ only in the trial ID's last digit and the patient "
              f"count, and {len(COMPOUNDS)} compounds whose codes reuse the same four digits. Rank = position of the "
              f"chunk for the code the question names; the model sees the top {TOP_K}. A wrong chunk in the top "
              f"{TOP_K} is worse than a miss: it holds a plausible, wrong number.\n",
              "## Summary\n", "| Method | Right chunk ranked 1st | Right chunk in top 5 |", "|---|---|---|"]
    for mode in MODES:
        report.append(f"| {mode} | {sum(r[mode] == 1 for _, r in rows)} of {len(rows)} | "
                      f"{sum(r[mode] <= TOP_K for _, r in rows)} of {len(rows)} |")
    report += ["\n## Per question\n", "| Code asked about | " + " | ".join(MODES) + " |", "|---|" + "---|" * len(MODES)]
    for code, ranks in rows:
        report.append(f"| {code} | " + " | ".join(f"**{r}**" if r == 1 else str(r) for r in ranks.values()) + " |")
    path = os.path.join(HYBRID_DIR, "results", "break_codes.md")
    with open(path, "w") as f:
        f.write("\n".join(report) + "\n")
    print("\nSaved results/break_codes.md in rag-hybrid/")


if __name__ == "__main__":
    main()
