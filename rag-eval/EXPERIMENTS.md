# Experiment log

Every change is predicted *before* it runs, then scored on the same 20 questions (`test_set.csv`) with
the same rubric (`RUBRIC.md`). With 20 questions, one question = 5 points: treat differences under
~10 points as noise.

| Run | Settings | Correct | Faithful | Spread out | Notes |
|---|---|---|---|---|---|
| `baseline` | flash-lite, chunk 400 / overlap 200, top-k 5, temp 1 | 78% | 90% | 40% | Graded by hand. 24 of 100 retrieved slots were near-copies of each other. |
| `overlap80` | as baseline, overlap 80 | 82% | 100% | 50% | Model-graded (baseline model-graded: 80%). 0 near-copy slots. |
| `dedupe` | as baseline, near-copies dropped | 75% | 90% | 40% | Model-graded. Lost Q04: dropped neighbour held the answer. |

## Choosing a model grader (2026-10-07)

Graded the baseline with a model, using `RUBRIC.md` as the prompt, and compared with my hand grades.
Agreement on correct / faithful / failure pattern:

| Grader | Rubric | Correct | Faithful | Pattern |
|---|---|---|---|---|
| gemini-3.5-flash-lite | v1 | 80% | 95% | 85% |
| gemini-3.5-flash-lite | v2 (two clarifications) | 95% | 95% | 90% |
| gemini-3.5-flash | v2 | 95% | 95% | 80% |
| gemini-3.8-flash | — | not run: timing out on Google's side | | |

- v1 → v2 was the biggest gain: the grader's errors were mostly the rubric's ambiguity, not the model's.
- Both graders still miss Q10 (a claim stitched across two chunks), so faithfulness may be over-scored.
- Caveat: the rubric was clarified using these same 20 questions, so 95% is an optimistic estimate.
- **Decision:** use gemini-3.5-flash-lite for experiments (same agreement, more free quota); hand-check
  every failure and any answer built from several chunks.

**Consistency check:** graded the baseline a second time with gemini-3.5-flash-lite (rubric v2).
The grader agreed with itself on 19 of 20 for correct, 20 of 20 for faithful, 19 of 20 for pattern.
The one flip (Q05: yes → partly) broke the "counts are a bonus" rule, and moved the score 80% → 78%.
So the grader alone adds about ±1 question (±5 points) of noise; with answer randomness on top, the
10-point threshold stands.

## Experiment 1: chunk overlap

**Question:** does cutting overlap from 50% help, now that a quarter of search results are near-copies?

**Variants:**
- A. 400 / 200 (baseline)
- B. 400 / 80 (20% overlap): needs re-chunking and re-embedding (~270 chunks)
- C. 400 / 200, retrieve 8 and drop near-copies to keep 5: no re-embedding

**My prediction (2026-10-07):** B gives the best answers. With overlap down to 20%, the 5 retrieved
chunks repeat less of each other, so more distinct information reaches the model.

(Note: the model receives the same ~2,000 characters either way; what should change is how much of it is unique.)

**Result (2026-10-07), all graded by gemini-3.5-flash-lite:**

| Variant | Correct | Faithful | Spread out | Near-copy slots | Chunks embedded |
|---|---|---|---|---|---|
| A. 400 / 200 (baseline) | 80% | 95% | 40% | 24 of 100 | 425 |
| B. 400 / 80 | 82% | 100% | 50% | 0 of 100 | 268 |
| C. 400 / 200 + drop near-copies | 75% | 90% | 40% | 0 of 100 | 425 |

- **No variant is clearly better on quality**: all differences are within the ~10-point noise band.
  Prediction (B best) points the right way, but 1–2 questions isn't evidence.
- **B is the better product choice anyway**: same quality for **37% fewer chunks** to embed and store,
  and no wasted search slots.
- **C was a flawed design**: overlapping neighbours aren't duplicates — each holds ~200 characters the
  other doesn't. Dropping one lost Q04's answer ("July 1, 2020" was in the dropped neighbour).
  Merging neighbours instead of dropping them would keep that text.
- Q03, Q15 and Q16 fail in every variant: overlap isn't their problem.
- **Decision (2026-10-07): 400 / 80 is the new default** in the app and the runner. Future stages compare
  against the `overlap80` run (model-graded 82%), not the 400 / 200 hand-graded baseline.
- **Correction:** B was effectively *no* overlap, not 20%. The splitter cuts the PDF text into lines
  (~91 characters each) and only carries whole lines over as overlap. A line doesn't fit in 80
  characters, so 102 of 136 neighbouring pairs shared nothing (average 11 characters shared). The 200
  setting really shares ~144 characters. So this experiment compared ~36% overlap against ~0%.
