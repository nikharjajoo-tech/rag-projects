# rag-citations — stage 3 of the series (citations and "I don't know")

(Who I am, repo conventions and machine constraints are in `../CLAUDE.md`. The learning loop is in
`../LEARNING_PLAN.md`. Stage 2's evaluation harness is in `../rag-eval/`; read its `CLAUDE.md`, `README.md`
and `EXPERIMENTS.md` before building anything.)

## Status (2026-10-07)
- Learning loop step 1 (concepts) **done** in the previous session: two error types (wrong answer vs.
  unnecessary refusal), three places to decide "I don't know" (search threshold, prompt, verification
  check), citations and citation accuracy.
- Step 2 (predict) **done**: my predictions are below.
- **Next: step 3 (build).** Nothing built yet in this folder.

## Findings carried over from Stage 2
- Reference point to beat: `rag-eval` run `overlap80` (400 / 80, top-k 5, flash-lite, temp 1):
  model-graded 82% correct, 100% faithful, 50% on spread-out questions.
- The app never invented answers to the 4 unanswerable questions, but refused Q03 and Q15, which the
  documents do answer (search misses) — two unnecessary refusals.
- **A similarity threshold can't separate answerable from unanswerable here:** top-chunk similarity was
  0.704–0.793 for unanswerable and 0.713–0.821 for answerable questions (Q17 scored 0.793, higher than 14
  of 16 answerable). Similarity measures "same topic", not "contains the answer".
- The model grader misses claims stitched across two chunks (Q10); citations may make these visible.

## My predictions (written before building)
1. **Citations + a second LLM that checks each citation against the retrieved chunks will increase
   faithfulness, but correctness will stay the same.**
2. **Where the line sits for a pharma research assistant:** there's no room for error, but refusing too
   often would hurt adoption. So answer more often, but every answer must be accurate: use citations,
   a second model to verify citations against the chunks, and **show the user a confidence level**.

## Plan
1. **Citations:** number the chunks in the prompt, have the model tag each claim ([1], [2]), render
   tags as "Chen, p7". New metric: **citation accuracy** (does the cited chunk support the claim?).
2. **Verifier:** a second call checks each cited claim against its chunk. Decide what the product does
   when a claim fails: drop the claim, refuse, or show it with low confidence.
3. **Confidence shown to the user:** derive it from the verifier (share of claims supported), not from
   the model's own self-rating (usually poorly calibrated). Test calibration: when it says "high", is it
   right that often?
4. **Extend the test set:** add ~8 near-miss questions (half answerable, half not) as a separate Stage 3
   extension. Keep the original 20 unchanged so scores stay comparable with Stage 2.
5. **Measure the tradeoff:** wrong answers vs. unnecessary refusals for each design; extend `RUBRIC.md`
   with citation-accuracy rules (keep examples generic).
6. Explain back + PM note, mark Stage 3 built in the root README.

## Open questions to settle in the build
- Is "100% correct" achievable? It isn't — the decision is which error a researcher would rather see,
  and how citations + confidence let them catch the rest.
- Verifier model: same family (flash-lite, free) or different family (less self-preference bias, costs money)?
- Each verification doubles model calls per question; flash-lite free tier hits per-minute limits at ~7
  calls/minute, so a 20-question run with verification takes ~6–8 minutes.
