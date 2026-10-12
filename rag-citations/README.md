# Stage 3: Citations and "I don't know"

Every claim in an answer carries a source ("Chen p7"), and a second model call checks each claim against
the chunk it cites. The verifier's verdicts set the confidence level shown to the user. The question this
stage answers: **wrong answers vs. unnecessary refusals, where's the line, and how do citations and
confidence help a researcher catch the errors that remain?**

Builds on Stage 2's harness in [`../rag-eval/`](../rag-eval/): same 20 questions, same rubric, same grader,
same search settings as the reference run `overlap80` (400 / 80, top-k 5, flash-lite, temperature 1).

## What's here

| File | What it does |
|---|---|
| `run_cited.py` | Answers each question with a source number on every claim, then runs the verifier over the claims |
| `score_cited.py` | Citation accuracy, confidence vs. correctness (calibration), wrong answers vs. unnecessary refusals, latency. No API calls |
| `build_index.py` | Builds a cleaner database: reference lists removed, optional whole-sentence chunks |
| `compare_policies.py` | What to do with an unbacked claim: show, drop or refuse, compared on saved runs |
| `break_verifier.py` | Feeds the verifier wrong citations on purpose and counts how many it catches |
| `EXPERIMENTS.md` | Every run: prediction first, then result |
| `results/` | Run reports (`.md`), per-question sheets (`*_grades.csv`), per-claim sheets (`*_claims.csv`), model grades |

## How it works

1. **Search:** the same similarity search as Stage 2 (top 5), over a cleaned database (since 2026-10-12):
   reference lists removed and whole-sentence chunks, built by `build_index.py`. Stage 2's database still
   works with `--db pharma_db.json`.
2. **Answer with citations:** the 5 chunks go into the prompt numbered `[1]`–`[5]`. The model returns its
   answer as a list of one-claim sentences, each with the chunk numbers that state it, plus what the
   question asks that the chunks don't say. No sentences means "I couldn't find this in the documents"
   (not "the documents don't answer this": often they do, and search missed it).
3. **Free checks first:** a claim that cites nothing, or a chunk number that doesn't exist, fails at once.
   Plain code is free and never wrong, so it runs before any model call.
4. **Verifier:** one extra call per question checks every claim against *only* the chunks it cites:
   supported, partly, or not supported.
5. **Confidence:** worked out from the share of claims the verifier supports, not from the model rating
   itself. The rule lives in `score_cited.py` (`confidence()`), so it can be changed without new API calls.

## How to run (from the `rag-projects` folder)

```
rag-chain/.venv/bin/python rag-citations/build_index.py pharma_db_sentences.json --drop-references --sentences  # once: databases aren't in git
rag-chain/.venv/bin/python rag-citations/run_cited.py cited                                   # 20 questions
rag-chain/.venv/bin/python rag-eval/grade.py rag-citations/results/cited gemini-3.5-flash-lite  # correct / faithful
python3 rag-citations/score_cited.py cited                                                    # Stage 3 metrics
```

Uses `rag-chain`'s virtual environment and `.env`, like Stage 2. A run is 20 embedding calls plus up to 40
chat calls (answer + verifier), and grading another 20: about 60 chat calls on `gemini-3.5-flash-lite`.

## Results

| Run | Correct | Faithful | Wrong answers | Unnecessary refusals | Citation accuracy | Latency |
|---|---|---|---|---|---|---|
| Stage 2 reference (`overlap80`) | 82% | 100% | 0 | 2 | not measurable | ~2.5s |
| Citations + verifier (`cited`) | 85% | 100% | 0 | 2 | 96% of claims | 2.4s + 3.0s to verify |
| + reference lists removed (`norefs`) | 80% | 100% | 0 | 3 | 100% of claims | 2.4s + 2.6s |
| + whole-sentence chunks (`sentences`) | 80% | 95% | 0 | 3 | 100% of claims | 3.8s + 1.9s |

- **Citations didn't make answers more faithful; they made unfaithfulness visible.** The verifier caught
  claims stitched across chunks that the whole-answer grader passed (Q12 here; Q10 in the smoke test).
- **The verifier checks that each claim is supported, not that the answer is complete.** The two answers
  shown as "high" confidence that were only partly right were missing facts, not wrong ones.
- **Citations don't fix search misses:** the same two answerable questions are refused as in Stage 2.
- **Cost:** twice the chat calls, and more than twice the wait.
- **Can the verifier be trusted?** Fed 45 wrong citations on purpose, it passed 1 as supported and
  marked 3 "partly". It also accepted all 31 valid ones. The first version looked better (2 passed) but
  was rejecting valid citations by number rather than reading them; showing each claim only its cited
  chunk fixed that.
- **Cleaning the index fixed the inputs, not the score.** Removing reference lists cut junk chunks in
  the top 5 from 24 of 100 to 2; whole-sentence chunks stopped a fact being split in two (Q12). Correct
  stayed at 80–85%: the freed slots went to on-topic passages that don't hold the answer. Ranking the
  right passage first is the next problem (Stage 4: reranking).

**Limits of this evidence:** 20 questions over 2 papers. One question moves a score 5 points, so these
results show direction, not statistical proof. At library scale, near-duplicate and conflicting sources
would make citations matter more and search harder; Stage 5 adds a second document set.

**Near-miss questions** (8 more, `test_set_nearmiss.csv`: 4 answerable with a trap nearby, 4 nearly
answerable): no invented answers and no unnecessary refusals on either database. Hand-graded correct: 81% on
Stage 2's database, 94% with whole-sentence chunks (both Stage 2 failures were facts cut mid-chunk).

**Confidence rule** (rule C): any claim not fully supported → low; answer admits a gap → medium; else
high. "High" was right 100% of the time on the 20 questions with whole-sentence chunks, 88% on the
near-miss set. What it can't catch: an answer that silently leaves facts out (Q14, N05).

**Unbacked claims: flag them, let the researcher decide.** Only 3 of 115 claims were unbacked (none
with the cleaned index). Refusing the whole answer was never better than dropping the claim, and dropping
lost a true claim whose citation was weak. So the product shows the claim, flagged:

```
BEHRT is a deep neural sequence transduction model for predicting
personalized risk from EHR data. (Chen p7)

┃ ⚠ BEHRT learns disease subphenotypes and handles irregular time
┃   intervals. (Chen p7)
┃   The cited source doesn't confirm this.
┃   [ View source ]  [ Accept ]  [ Reject ]  [ Edit ]
```

- Every accept or reject is a free human label on the verifier: the hand check, at scale.
- Design against: accepting without reading (require "view source" first), and the warning getting lost
  when the answer is copied into a report.

Details and the hand-checks are in `EXPERIMENTS.md`.

## What I learned (PM note)

See [LEARNINGS.md](LEARNINGS.md).
