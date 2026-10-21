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

## Experiment 2 (open thread A): give meaning-based search more votes (2026-10-15)

**Setup:** same rank report, same questions. When the two lists are merged, meaning-based search's votes are
multiplied by a weight (`VECTOR_WEIGHT` in `search.py`, or `--vector-weight`); keyword search keeps 1. Weight 1 =
Experiment 1 (checked: identical ranks). Main run: weight 2. Also 1.5 and 3, to see the trend.

**My predictions** (2026-10-15, before any weighted run):
1. 2-to-1 hybrid: **26 or more** of 32 pieces in the top 5 (equal votes: 21; meaning-based alone: 25).
2. Q03's answer is **pushed beyond 25** after merging, so the reranker never sees it.
3. 2-to-1 hybrid + rerank **beats 25** of 32.

**Result** (`results/ranks_w1.5.md`, `ranks_w2.md`, `ranks_w3.md`). Pieces in the top 5, of the 32 original +
near-miss pieces. The 8 exact-term pieces stay 8 of 8 under every setting.

| Meaning-based votes | hybrid | hybrid + rerank | Q03 after merging (needs ≤ 25 for the reranker) |
|---|---|---|---|
| meaning-based alone | **25** | 24 (vector + rerank) | 47 |
| 1 (Experiment 1) | 21 | 24 | 18 |
| 1.5 | 22 | 24 | 21 |
| 2 | 22 | 23 | 27 |
| 3 | 24 | 23 | 30 |

**What happened**
- **More weight on meaning helps hybrid, slowly, and never passes meaning-based alone.** Each step up returns
  pieces keyword search had pushed out (Q06 13 → 5, Q07 27 → 8, Q08 11 → 4, Q14 Blanco 15 → 5). At weight 3
  hybrid is almost meaning-based search again: 24 vs 25.
- **The Q03 win and the losses pull in opposite directions.** Q03's answer is 47th by meaning, so it only gets
  into the reranker's 25 if keyword search has a strong vote. That same strong vote is what pushes out Q06, Q07
  and Q08. Somewhere between 1.5 and 2, Q03 drops out of the pool (21 → 27) and the reranker loses its one win.
  No single weight keeps both.
- **The reranker is now the bottleneck, not the merge.** At every weight it makes the same two mistakes: Q06's
  answer falls to 11–13 (it prefers passages about the authors testing ChatGPT), and Q14's "low quality or
  inconsistent data" falls to 6–7. It also leaves Q07 at 6, one place short. What it fixes, it fixes at every
  weight too (Q08 → 1, Q16 Blanco → 3).
- Search time is unchanged: merging with weights is arithmetic on two lists (0.62s, all of it the embedding call).
- Cohere calls used so far: about 140 of 1,000.

**Predictions vs. result**
1. 2-to-1 hybrid 26+ → **22**. Wrong: weighting reduces the damage but doesn't add new finds.
2. Q03 pushed beyond 25 → **right** (27).
3. 2-to-1 hybrid + rerank beats 25 → **23**. Wrong: the reranker's own mistakes cap it.

**So what (for a PM):** a weight is a dial between two products, not a free lunch. Turned towards keywords, it
rescues the one question worded like the paper (Q03) and breaks the ones worded differently. Turned towards
meaning, it becomes the system we already had. On this test set, the best hybrid setting is "don't".

**Still open:** add keyword search only when the question has a rare term (the other half of thread A); pool
size; the reranker's score as an "unsure" signal.

## Experiment 3 (open thread B): the reranker reads 50 candidates instead of 25 (2026-10-15)

**Setup:** same rank report and questions, `--pool 50` (`POOL` in `search.py`), equal votes when merging (weight 1,
the only weight that keeps Q03 inside 25). Both reranked methods: meaning-based + rerank and hybrid + rerank.

**My predictions** (2026-10-15, before seeing any pool-50 result):
1. Hybrid + rerank: **26 or more** of 32 (pool 25: 24; meaning-based alone: 25): it rescues Q07 and Q15.
2. Meaning-based + rerank: the reranker lifts **both** Q03's answer (47th by meaning) and Q15's missing piece (43rd)
   into the top 5.
3. Reranker latency: **about the same** as with 25 (0.6–1.6s).

**Result** (`results/ranks_pool50.md`). Pieces in the top 5, of 32 (the 8 exact-term pieces: 8 of 8 throughout).

| Method | Reranker reads 25 | Reranker reads 50 |
|---|---|---|
| meaning-based alone (no reranker) | 25 | 25 |
| meaning-based + rerank | 24 | 24 |
| hybrid + rerank | 24 | 24 |
| Reranker call, median (range) | 0.64s (0.55–12.9s, 140 calls) | 0.93s (0.63–2.2s, 56 calls) |

**What happened**
- **Same score, different questions.** Each method gains one piece and loses one.
- **Q03 no longer needs keyword search.** Its answer is 47th by meaning, now inside the 50, and the reranker puts
  it 1st. Meaning-based + rerank with 50 fixes Q03 with no keyword search at all.
- **More candidates, more distractors.** Under meaning-based + rerank, Q07's answer slips from 4th to 7th: the extra
  25 chunks include passages the reranker likes better. Under hybrid + rerank, Q07 is finally in the pool (27th)
  and climbs to 9th, still short.
- **The reranker sees the hard pieces and still doesn't pick them.** Q15's "two articles on drug repurposing" is now
  in the pool and lands 30th–31st. Q16's Chen "external validation" climbs from 34th to 14th under hybrid. Q14's
  "sharing data is hard" rises from 41st to 13th by meaning. All better, none in the top 5. Q16's other Chen piece
  (112th–171st) is still out of reach.
- **Its two steady mistakes don't move:** Q06 (11th–14th) and Q14 "low quality or inconsistent data" (7th).
- **Latency:** the median call rose by 0.3s (about 1.5x) for twice the text. The worst case is a network
  outlier, not size: the slowest call, 12.9s, was at 25.
- Cohere calls used: 196 of 1,000.

**Predictions vs. result**
1. Hybrid + rerank 26+ → **24**. Wrong: rescues and new misses cancel out.
2. The reranker lifts both Q03 and Q15 → **one**: Q03 to 1st; Q15's piece to 30th–31st.
3. Latency about the same → **about 1.5x** (0.64 → 0.93s median). Wrong, but small in absolute terms.

**So what (for a PM):** three dials turned (keyword search, weight, pool), and the score never moved off 24–25. On
this test set the limit isn't what search can *find* any more; it's what the reranker *judges* relevant. A wider
funnel only helps if the judge at the bottom is good. Rank in the top 5 is still not a correct answer, though: the
answer runs decide whether moving answers to rank 1 (Q03, Q08) helps the model more than the misses (Q06, Q14) hurt.

## Experiment 4: answer runs, end to end (2026-10-15)

**Setup:** Stage 3's pipeline (cited answer + fact-checker, `gemini-3.5-flash-lite`), only the search changed, on the
20 original questions. Graded by `rag-eval/grade.py` (flash-lite), scored by `rag-citations/score_cited.py`.
Three settings, two runs each (the model ignores temperature, so answers vary run to run):
`answers_vrr50_*` (meaning-based + rerank, reads 50), `answers_hrr25_*` (hybrid + rerank, reads 25),
`answers_vector_*` (meaning-based only: Stage 3's search, re-run as the control).

**My predictions** (2026-10-15, before any answer run finished):
1. Meaning-based + rerank (50): **above 80%** correct (Stage 3: 80%).
2. Q06 with the reranker: the model **refuses** (its answer chunk is ranked ~14th).
3. End to end, the reranker adds **0.5–1.5s** per question.

**Result** (`results/answers_*.md`; scores from `score_cited.py`, model-graded):

| Search | Correct (run a / b) | Wrong answers | Shown as high confidence but wrong or partly right | Extra wait from the reranker |
|---|---|---|---|---|
| Stage 3 `sentences` (reference) | 80% | 1 | 0 | — |
| meaning-based only (control) | **80% / 80%** | 0 / 1 | **0 / 0** | — |
| hybrid + rerank, reads 25 | 78% / 75% | 1 / 1 | 1 / 2 | 0.94s |
| meaning-based + rerank, reads 50 | 72% / 72% | 2 / 2 | 2 / 2 | 1.01s |

Full wait per question (search + rerank + answer + fact-check): meaning-based 6.0 / 6.5s, the reranked runs
6.0–7.4s. The reranker's ~1s is real, but Gemini's own answer time swings by as much between runs (1.6–4.3s).

**What changed, by question** (4 reranked runs vs the 2 control runs)
- **Won: Q03** (preclinical): right in 3 of 4 reranked runs, refused in both controls. In the 4th the model misread
  the same sentence ("the stage *after* preclinical testing").
- **Lost: Q06** (trained in 2021): refused in all 4 reranked runs, right in both controls. Exactly as the rank report said.
- **Lost: Q14** (data obstacles, two papers): partly right in all 4 (Blanco's pieces pushed out), right in both controls.
- **Lost, dangerously: Q07** (target trial): wrong in 2 of 4. The reranker surfaced a nearby passage about a "trial
  simulation framework"; the model answered from it, and the fact-checker passed it, because the citation *is*
  accurate. A correct citation for the wrong answer: the fact-checker checks faithfulness, not correctness.
- Unchanged: Q09, Q16 refused everywhere; Q15 wrong or refused everywhere.

**Q09 is not randomness (correcting Stage 3's note).** Refused in all 6 runs here and in Stage 3's `sentences`, 7 of 7,
even with the answer chunk at rank 1. The sentence lists three networks: "...(PCORnet) [51], Observational Health
Data Sciences and Informatics (OHDSI) consortium [52], and ..." and the model won't read the name-then-acronym
pattern as a definition. It answered correctly in Stage 3's `cited` and `norefs` runs, which used the older,
larger chunks. A prompt or chunking problem, not a search problem.

**Free bonus, open thread C (no new calls): the reranker's top score as an "unsure" signal.** Top relevance per
question in `answers_vrr50_a`: every reranker-caused failure scored lowest (Q14 0.13, Q16 0.18, Q06 0.28, Q07 0.33),
along with three of the unanswerable questions (Q19 0.33, Q18 0.35, Q17 0.40; Q20 scored 0.62). Every correct
answer to an answerable question scored 0.55 or above. It doesn't flag failures where the right chunk was found and
the model misread it (Q15 0.57, Q09 0.71, Q03 in run b 0.76): it catches search misses, not reading mistakes. Meaning-based similarity can't do this: all 20 questions sit between 0.65 and 0.83, and Q03, refused,
has the highest. A promising lead, not a finding: 20 questions, and the cut-off was picked after seeing the scores.

**Predictions vs. result**
1. Meaning-based + rerank (50) above 80% → **72%** (both runs). Wrong.
2. Q06: the model refuses → **right**, 4 of 4.
3. The reranker adds 0.5–1.5s → **right**: ~1.0s.

**So what (for a PM):** on this library and test set, the reranker costs about 1s and 2–8 points of correctness, and
it introduces the worst kind of error: confident, well-cited, wrong (0 in the control runs, 1–2 per reranked run).
**Ship meaning-based search alone.** Revisit when the library grows or users start searching for near-identical codes.
The reranker's score is a lead worth keeping: it may be more useful as a "not sure" alarm than as a ranker.
- Calls: ~300 Gemini chat calls (answers, fact-checks, grades); 8 new Cohere calls (204 of 1,000 used).
