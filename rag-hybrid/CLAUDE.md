# rag-hybrid — stage 4 of the series (hybrid search and reranking)

(Who I am, repo conventions and machine constraints are in `../CLAUDE.md`. The learning loop is in
`../LEARNING_PLAN.md`. Stage 2's evaluation harness is in `../rag-eval/`, Stage 3's cited runner in
`../rag-citations/`; read their `CLAUDE.md`, `README.md` and `EXPERIMENTS.md` before building anything.)

## Status (2026-10-12)
- Learning loop step 1 (concepts) **done**: keyword search (BM25) vs. meaning-based search, why
  embeddings blur exact terms, merging two ranked lists (reciprocal rank fusion), rerankers (retrieve
  wide, rerank narrow), and what each piece costs in latency and money.
- Step 2 (predict) **done 2026-10-14**: my predictions are below, sharpened into checkable outcomes.
- Step 3 (build) **started 2026-10-14**: `search.py` (BM25 by hand, reciprocal rank fusion, Cohere rerank,
  5 modes, cached API results with their real latency), `rank_report.py` (where the answer chunk ranks, no
  chat calls), `answer_chunks.csv` (a phrase marking each answer piece: 20 answerable questions, 32 pieces,
  incl. 4 near-miss), `run_hybrid.py` (Stage 3's pipeline with a pluggable search). Smoke-tested on Q01;
  vector scores match Stage 3 to 3 decimals. Stage 3 files changed only to plug in: `run_cited.main()` takes a
  search hook, `grade.py` reads other score names, `score_cited.py` takes a run path.
- Vector baseline (`results/ranks_baseline.md`, before predictions): 25 of 32 pieces in the top 5; Q03's chunk
  at 47, Q15's at 43, Q16's Chen pieces at 84 and 112, Q14's "sharing data" at 41: beyond the pool of 25.
- **Experiment 1 done 2026-10-14** (ranks, all 5 methods; `EXPERIMENTS.md`): hybrid 21 of 32 (worse than
  vector's 25); hybrid + rerank 24 (fixes Q03, breaks Q06 and Q07); exact-term set: vector already 8 of 8.
  Predictions 1 and 2 wrong. 8 exact-term questions added (`test_set_exact.csv`, written by Claude
  before any run on them; I should still review them).
- **Next:** choose among the open threads in `EXPERIMENTS.md` (weighted fusion, pool size, reranker score as
  "unsure" signal, near-duplicate IDs), then answer runs (2 per setting) for correctness and end-to-end latency.
- Saboo's tutorial uses RAGLite (needs spaCy + Postgres: no builds here). Rebuilt the same three pieces
  in plain Python instead (Saboo also uses Cohere for reranking).
- **`gemini-3.5-flash-lite` ignores temperature** (the library warns: "uses fixed sampling defaults; the
  sampling parameter(s) temperature will be ignored"). So Stages 2–3's "temperature 1" answers and
  "temperature 0" verifier ran on the model's fixed defaults. Randomness can't be switched off: repeat runs.

## Findings carried over from Stage 3 (checked against `../rag-citations/results/sentences.md`)
- Reference point to beat: Stage 3 run `sentences` (whole-sentence chunks, top-k 5, flash-lite, temp 1,
  citations + verifier): model-graded 80% correct, 95% faithful, 0 wrong answers, 3 unnecessary
  refusals (Q03, Q09, Q16). Near-miss set: `nearmiss_sentences` 94%.
- **The 3 "exact term" questions already pass with meaning-based search** on this database (232
  chunks): BEHRT, BACE1 and the OHDSI sentence all reach the top 5. So the current test set can't show
  the problem hybrid search is built for. Needs exact-term questions that actually stress it (plan item 3).
- What each remaining failure is, by cause:
  - **Q03** (preclinical): the answer sentence says "no studies identified for **this stage**"; it never
    names the stage. Its chunk isn't in the top 5: five on-topic chunks from p3–p5 outrank it. A ranking
    problem.
  - **Q15** (65 studies): the chunks with "8 trial recruitment" / "2 drug repurposing" aren't in the top 5.
    The question contains an exact number ("65") that a keyword search could match.
  - **Q16** (validation, both papers): all 5 slots went to Blanco; none to Chen. A one-paper-takes-all
    problem, not an exact-term one.
  - **Q09** (OHDSI): **not a search failure** — the answer chunk was #2 and the model still said "not
    mentioned" (temperature-1 randomness; it passed in `cited` and `norefs`). Hybrid search shouldn't
    get credit if it flips back.

## My predictions (written 2026-10-14, after the vector baseline ranks, before any new method was measured)
1. **Keyword search:** "Adding keyword search will search for the meaning of the query as well as the exact
   keywords to find the answer; this can pull chunks even from different documents which are far apart."
   As a number: hybrid brings **4 or more of the 7** missed answer pieces into the top 5.
2. **Reranker:** "Adding the reranker will give weight to the chunks retrieved during the search, and the
   top-ranked chunks will then be given to the LLM to generate the answer."
   As an outcome: hybrid + rerank answers **Q15 and Q16** correctly; Q03 stays refused.
3. **Latency:** "For a pharma research assistant it is more important to be accurate than to be fast."
   The line: **depends on the gain**: decide after seeing how much quality each extra second buys.

## Plan
1. **Baseline ranks, no model calls:** for every answerable question, at what rank does the chunk holding
   the answer sit under meaning-based search? (Top 5 = hit; 6–30 = a reranker could rescue it; beyond =
   only better first-stage search can.) Needs the answer chunk marked per question.
2. **Keyword search (BM25)**, written by hand so its knobs are visible: how words are split (BACE1,
   AI/RWD, "65"), and how rare words outweigh common ones. Run it alone first: what does it find that
   embeddings miss, and the reverse (Q05's "spotting medication side effects" shares no words with
   "adverse event detection")?
3. **Exact-term extension set** (~8 questions, separate file, like Stage 3's near-miss set): reference
   numbers, acronyms, numbers, names mentioned once. Keep the original 20 unchanged so scores stay
   comparable.
4. **Fusion:** merge the two lists with reciprocal rank fusion (ranks, not scores: similarity 0.68 and a
   BM25 score of 12.4 aren't on the same scale).
5. **Reranker:** fetch ~25 candidates, rerank with Cohere, keep the top 5. Compare with a Gemini
   flash-lite reranker (no new key, but uses chat quota) if time allows.
6. **Measure** each piece on and off: vector only / BM25 only / hybrid / hybrid + rerank, on the 20
   questions and the extension set. Correct, unnecessary refusals, answer-chunk rank, and latency per step.
7. Explain back + PM note (checkpoint: "Is a 10% quality gain worth 800 ms of extra waiting?"), mark
   Stage 4 built in the root README.

## Open questions to settle in the build
- Cohere key: **added and tested 2026-10-14** (`COHERE_API_KEY` in `../rag-chain/.env`; this stage reuses
  rag-chain's `.venv` and `.env`, like Stages 2–3). Call `https://api.cohere.com/v2/rerank` with plain
  `httpx` (already installed), model `rerank-v3.5`. Trial: 1,000 calls/month per account (more keys don't
  add calls), **10 rerank calls/minute**. One call reranks all candidates for a question; cache results to
  disk so answer-step reruns cost no Cohere calls. Budget for the whole stage: ~150–250 calls.
- With 20 questions, one question moves the score 5 points: Q09-style randomness can hide or fake a gain.
  Temperature 0 isn't available (see above), so: two runs per setting, and judge search by the rank report,
  which has no randomness at all.
- Pool size: most missed pieces sit beyond 25. A wider pool (50? all 232 chunks?) costs more Cohere tokens
  and time per call; worth measuring as its own experiment.
- Does reranking help Q16 (one paper takes all five slots), or does that need a different fix
  (e.g. a slot per paper)?
