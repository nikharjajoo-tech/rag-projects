# Stage 4 experiments

Every run: prediction first, then result. Reference point: Stage 3 run `sentences` (80% correct, 3 unnecessary
refusals: Q03, Q09, Q16).

## Experiment 1: where does the answer chunk rank? (2026-10-14)

**Setup:** `rank_report.py`, no chat calls. For every answerable question, the position of the first chunk
holding each answer piece (`answer_chunks.csv`), under five search methods. 20 questions / 32 pieces from the
original and near-miss sets, plus 8 new exact-term questions (`test_set_exact.csv`, written before any method
was run on them). Reranker: Cohere `rerank-v3.5`, reading the top 25.

**My predictions** (from `CLAUDE.md`): hybrid brings 4 or more of the 7 missed pieces into the top 5;
hybrid + rerank answers Q15 and Q16, and Q03 stays refused; acceptable wait: depends on the gain.

**Result: original + near-miss questions** (`results/ranks_all.md`)

| Method | Pieces in top 5 | Questions with every piece in top 5 | Pieces beyond the reranker's 25 | Search time |
|---|---|---|---|---|
| vector (Stage 3) | **25 of 32** | **16 of 20** | 5 | 0.6s |
| bm25 | 15 of 32 | 10 of 20 | 9 | 0.0s |
| hybrid | 21 of 32 | 13 of 20 | 5 | 0.6s |
| vector + rerank | 24 of 32 | 15 of 20 | 5 | 2.2s |
| hybrid + rerank | 24 of 32 | 15 of 20 | 5 | 1.4s |

**Result: exact-term questions** (`results/ranks_exact.md`): every method except BM25 alone puts all 8 answers
in the top 5 (vector: 7 at rank 1, IML at 3). Nothing to fix.

**What happened**
- **Hybrid made search worse, not better** (25 → 21 pieces). It rescued 1 of the 7 missed pieces (Q14 data
  quality, 6 → 4) and pushed out 5 that meaning-based search had found (Q06, Q07, Q08, Q14 Blanco, Q16
  Blanco). Fusion gives both lists an equal vote, and keyword search alone is much weaker here (15 of 32):
  most questions are worded differently from the papers, by design.
- **Embeddings didn't miss exact terms.** PMID, grant code, acronyms, author names: all rank 1–3 by
  meaning. With 232 chunks a rare token makes its chunk the nearest anyway. The failure the textbook warns
  about needs near-duplicates (NCT01234567 vs NCT01234568) or a far bigger library.
- **Q03 is the textbook funnel, working:** keyword search ranks the answer 1st (it shares "no studies
  identified … stage … reviews" with the question), meaning-based 47th. Hybrid lifts it to 18, inside the
  reranker's 25, and the reranker puts it 1st. Neither piece alone fixes it.
- **The reranker breaks Q06 and Q07.** Q06 ("according to the authors who tested it"): the reranker
  promoted passages about the authors *testing ChatGPT*; the answer fell 1 → 13. Its top score was only
  0.28 (Q01: 0.94): it was unsure. Q07: hybrid put the answer at 27, just outside the pool, so the reranker
  never saw it.
- **Just outside the pool:** Q15's "two articles on drug repurposing" (28) and Q07's answer (27) under
  hybrid. A pool of 30–50 would include them. Q16's Chen pieces (34, 171) and Q14's "sharing data" (41–103)
  are out of reach.
- **Latency:** the reranker adds 0.6–1.6s per question (Cohere call, varies by call).

**Predictions vs. result**
1. Hybrid rescues 4+ of 7 → **1 of 7**, and loses 5. Wrong.
2. Hybrid + rerank fixes Q15 and Q16, not Q03 → by rank, the **reverse**: Q03's answer is 1st; Q15's missing
   piece stays at 28 and Q16's Chen pieces at 34 and 171. To confirm with answer runs (the model may still
   answer Q15 partly).
3. Depends on the gain → so far, hybrid + rerank costs ~1s for **no net gain** in pieces found (fixes Q03,
   breaks Q06 and Q07).

**Open threads**
- Weight the lists instead of equal votes (e.g. meaning-based counts double), or add keyword search only
  when the question has a rare term.
- Pool size 25 → 50: rescues Q07 and Q15 under hybrid? Costs more reranker time per call.
- The reranker's top score as an "I'm not sure" signal: Q06 0.28 vs Q01 0.94. Stage 3 found similarity
  can't separate answerable from unanswerable questions; can relevance?
- Break exact-term search on purpose: near-duplicate codes, where embeddings should fail and keywords win.
