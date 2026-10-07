# Grading rubric

The rules for grading every run by hand. The model grader's prompt will be built from this file, so a
rule change here should be followed by regrading. Agreed during the stage-1 baseline (2026-10-07); clarified after the first model-grader run.

## Routine for each question
1. **Key facts first.** Split the expected answer into 1–4 key facts *before* reading the app's answer.
   Key facts are what the **question asks for**. Extra detail in the expected answer is optional: e.g. when
   the question asks for a percentage, the percentage is enough and the counts behind it are a bonus (Q05).
2. **Search.** Find each key fact in the retrieved chunks. The ✅ marks only mean "chunk from the right
   page" — the right page doesn't guarantee the right chunk (see Q15 in the baseline).
3. **Grade** correct and faithful (below).
4. **Diagnose** any failure with one pattern.

## Correct — answer vs. expected answer
- **yes:** every key fact, nothing wrong.
- **partly:** some key facts missing, or the core is right but a detail is wrong.
- **no:** the main fact is wrong or missing.
- **A refusal on an answerable question is always no**, even when it's faithful because the chunks lacked
  the answer (Q03, Q15). Correct measures what the user got; faithful measures the model's honesty.
- Extra information beyond the expected answer is fine if it's faithful.
- Questions about both papers must say **which paper says what**; otherwise at most *partly*.
- Unanswerable questions: "not in the documents" = yes. Any invented figure = no.

## Faithful — answer vs. retrieved chunks (ignore the expected answer)
- Check **claims, not words**: each claim must be supported by the chunks. Words stitched together from
  two different chunks into a new claim = not faithful (Q10 in the baseline).
- A refusal is faithful when the chunks really don't contain the answer, even if the documents do (Q03).

## Failure patterns
| Label | Meaning |
|---|---|
| `search-miss` | The fact isn't in any retrieved chunk |
| `P03` | Not in the chunks, and irrelevant chunks (e.g. reference lists) took the slots |
| `P02` | The fact or claim is cut across a chunk boundary |
| `P01` | The answer states something the chunks don't support |
| `model-miss` | The fact was in the chunks, but the model missed it, refused, or contradicted it |
