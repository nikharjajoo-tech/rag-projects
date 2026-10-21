# Stage 4: Hybrid search and reranking

Adds the two standard upgrades to RAG search: **keyword search (BM25) alongside meaning-based search**, merged
into one list, and a **reranker** that reads the top candidates together with the question and reorders them.
The question this stage answers: **is extra quality worth the extra waiting?** On this library, the answer was
that there was no extra quality to buy.

Builds on Stage 3 ([`../rag-citations/`](../rag-citations/)): same 20 questions, cited answers, fact-checker,
grader and whole-sentence database (`pharma_db_sentences.json`). Only the search in front of it changes.

## What's here

| File | What it does |
|---|---|
| `search.py` | Keyword search (BM25, written by hand), meaning-based search, reciprocal rank fusion, Cohere reranker. Five modes; API results cached with their real latency |
| `rank_report.py` | For each answer, the rank of the chunk that holds it, under each search method. No chat-model calls |
| `answer_chunks.csv` | A phrase marking each answer piece: 20 answerable questions, 32 pieces, plus 8 exact-term questions |
| `test_set_exact.csv` | 8 exact-term questions: a PMID, a grant code, acronyms, author names |
| `run_hybrid.py` | Stage 3's pipeline (cited answer + fact-checker) with a pluggable search |
| `EXPERIMENTS.md` | Every run: prediction first, then result |
| `results/` | Rank reports (`ranks_*`) and answer runs (`answers_*`) |

## How it works

1. **Meaning-based search** (Stages 1–3): every chunk ranked by how close its embedding is to the question's.
2. **Keyword search (BM25):** every chunk scored on the question's words it contains, rare words counting far
   more than common ones. Runs locally in milliseconds, with no API call.
3. **Merging (reciprocal rank fusion):** each list votes `weight / (60 + rank)` for every chunk. It uses ranks,
   not scores, because a similarity of 0.68 and a BM25 score of 12.4 aren't on the same scale.
4. **Reranker:** the top 25 (or 50) candidates go to Cohere `rerank-v3.5`, which reads the question and each
   chunk together and scores how well the chunk answers it. The top 5 go to the model.

The settings are at the top of `search.py`: `BM25_K1`, `BM25_B`, `RRF_K`, `VECTOR_WEIGHT`, `POOL`.

## How to run (from the `rag-projects` folder)

```
rag-chain/.venv/bin/python rag-hybrid/rank_report.py all                     # ranks, all 5 methods, no chat calls
rag-chain/.venv/bin/python rag-hybrid/rank_report.py w2 --modes hybrid --vector-weight 2
rag-chain/.venv/bin/python rag-hybrid/rank_report.py pool50 --modes vector+rerank,hybrid+rerank --pool 50
rag-chain/.venv/bin/python rag-hybrid/run_hybrid.py my_run --search vector+rerank --pool 50   # answers
rag-chain/.venv/bin/python rag-eval/grade.py rag-hybrid/results/my_run gemini-3.5-flash-lite
python3 rag-citations/score_cited.py rag-hybrid/results/my_run
```

Uses `rag-chain`'s virtual environment and `.env`. The reranker needs `COHERE_API_KEY` there (a free trial key:
1,000 calls a month, 10 a minute). One rerank call per question; results are cached in `cache/` (not in git), so
reruns cost nothing.

## Results

**Where the answer ranks** (32 answer pieces; the model sees the top 5):

| Search | Pieces in top 5 | Search time |
|---|---|---|
| Meaning-based (Stages 1–3) | **25** | 0.6s |
| Keyword only | 15 | ~0s |
| Hybrid, equal votes | 21 | 0.6s |
| Hybrid, meaning-based counts 1.5 / 2 / 3 times | 22 / 22 / 24 | 0.6s |
| Meaning-based + reranker (reads 25 / 50) | 24 / 24 | +0.6 / +0.9s |
| Hybrid + reranker (reads 25 / 50) | 24 / 24 | +0.6 / +0.9s |

On the 8 exact-term questions, every method except keyword-only already finds all 8.

**End to end** (cited answers + fact-checker, 2 runs each):

| Search | Correct | Confident but wrong or partly right | Extra wait |
|---|---|---|---|
| Meaning-based only | **80% / 80%** | **0 / 0** | none |
| Hybrid + reranker (reads 25) | 78% / 75% | 1 / 2 | +0.9s |
| Meaning-based + reranker (reads 50) | 72% / 72% | 2 / 2 | +1.0s |

- **Embeddings didn't miss exact terms here.** With 232 chunks, a rare code or acronym makes its chunk the
  nearest anyway. The textbook failure needs near-identical codes or a far bigger library.
- **Merging gave a weak list an equal vote.** Most questions are worded differently from the papers, so keyword
  search alone is weak (15 of 32), and merging pushed out answers meaning-based search had found. Weighting it
  down just moves the result back towards meaning-based search alone.
- **The reranker fixed one question and broke three.** It found Q03 (answer 47th by meaning, 1st after
  reranking). It lost Q06 and Q14, and in two runs it surfaced a nearby passage for Q07 that the model answered
  from. The fact-checker passed that answer, because the citation was accurate: **a correct citation for the
  wrong answer.**
- **Wider funnel, same judge.** Reading 50 candidates instead of 25 rescued and lost one piece each. What limits
  this system now is what the reranker judges relevant, not what search can find.
- **A lead: the reranker's score as an "unsure" alarm.** Every failure the reranker caused had a top score below
  0.35; every correct answer to an answerable question scored 0.55 or more. Similarity scores can't separate them
  (all 0.65–0.83). Unproven: 20 questions, and the cut-off was picked after seeing the scores.
- **Correction to Stage 3:** Q09 (OHDSI) isn't randomness. It was refused 7 of 7 times with whole-sentence chunks,
  even with the answer at rank 1. The model won't read "Observational Health Data Sciences and Informatics
  (OHDSI) consortium", in a list of three networks, as a definition.

**Decision:** ship meaning-based search alone for this library. Revisit when the library grows or users search
for near-identical codes (trial IDs, batch numbers, gene variants).

**Limits of this evidence:** 20 questions over 2 papers. One question moves a score 5 points, and the model
ignores temperature, so answers vary run to run (hence 2 runs per setting, and the rank report, which has no
randomness). Details in `EXPERIMENTS.md`.

## What I learned (PM note)

See [LEARNINGS.md](LEARNINGS.md).
