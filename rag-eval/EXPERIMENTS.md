# Experiment log

Every change is predicted *before* it runs, then scored on the same 20 questions (`test_set.csv`) with
the same rubric (`RUBRIC.md`). With 20 questions, one question = 5 points: treat differences under
~10 points as noise.

| Run | Settings | Correct | Faithful | Spread out | Notes |
|---|---|---|---|---|---|
| `baseline` | flash-lite, chunk 400 / overlap 200, top-k 5, temp 1 | 78% | 90% | 40% | Graded by hand. 24 of 100 retrieved slots were near-copies of each other. |

## Experiment 1: chunk overlap

**Question:** does cutting overlap from 50% help, now that a quarter of search results are near-copies?

**Variants:**
- A. 400 / 200 (baseline)
- B. 400 / 80 (20% overlap): needs re-chunking and re-embedding (~270 chunks)
- C. 400 / 200, retrieve 8 and drop near-copies to keep 5: no re-embedding

**My prediction (2026-10-07):** B gives the best answers. With overlap down to 20%, the 5 retrieved
chunks repeat less of each other, so more distinct information reaches the model.

(Note: the model receives the same ~2,000 characters either way; what should change is how much of it is unique.)

**Result:** _pending; to be scored with the model grader once it's checked against my baseline grades._
