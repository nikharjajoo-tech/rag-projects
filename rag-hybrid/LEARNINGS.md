# What I learned adding hybrid search and a reranker (Stage 4)

My PM notes from trying to improve the search behind a research assistant for a pharma research company: keyword
search alongside meaning-based search, and a reranker in front of the model. 20 test questions plus 8 exact-term
questions, over two research papers. Every change was measured twice: where the answer ranks (no randomness), and
end-to-end answers (two runs each).

## 1. Keyword search finds words; meaning-based search finds meaning
Keyword search looks for the question's words in the documents, and rare words count far more than common ones.
Meaning-based search turns text into a "meaning fingerprint", which is why it finds answers worded differently from
the question, and also why it can blur exact terms: to it, `NCT01234567` and `NCT01234568` look almost the same.

**Why keyword search didn't help here:** meaning-based search was already finding the relevant chunks, and keyword
search on its own was much weaker (15 of 32 answer pieces vs. 25), because our questions are worded differently
from the papers. Its one real advantage, exact terms, never showed: in a 232-chunk library with no near-identical
codes, a PMID, grant code or acronym makes its own chunk the closest match anyway (8 of 8 found by meaning).

**What I predicted vs. what happened:** I expected hybrid search to rescue 4 or more of the 7 missed answer
pieces. It rescued 1 and pushed out 5. Merging gives both lists a vote, and a weak list with an equal vote drags
good results down. Giving meaning-based search more votes only moved the result back towards meaning-based search
alone; it never beat it.

## 2. The reranker is a second, slower judge on a shortlist
The first search compares fingerprints made in advance, so it's fast enough to check every chunk. The reranker reads
the question and each chunk *together* and scores how relevant the chunk is, which is smarter but slower, so it only
gets a shortlist (25 or 50). Its top 5 go to the model.

**Why a wider shortlist didn't help:** 50 candidates let it see answers it had missed (Q03 went from 47th to 1st),
but they also brought in more distractors (Q07 slipped from 4th to 7th), and its own misjudgements (Q06, Q14) didn't
change. A wider funnel only helps if the judge at the bottom is good. Here, what limited the system stopped being
what search could *find* and became what the reranker *judged* relevant.

## 3. A correct citation for the wrong answer
On Q07 the reranker surfaced a passage about a *related* method ("trial simulation framework"). The model answered
from it accurately, the fact-checker confirmed the passage says that, and the user saw **high confidence** on a
wrong answer. The fact-checker checks "does the cited chunk say this?", not "does this answer the question?", so
tuning it won't catch this. What would:
- **A "did it answer the question" check:** one extra model call per answer.
- **The reranker's score as an alarm:** Q07's top relevance was 0.33. Every failure the reranker caused scored below
  0.35; every correct answer scored 0.55 or more. Showing "low confidence" below a cut-off costs nothing extra. A
  lead, not proof: 20 questions, and the cut-off was picked after seeing the scores.
- **Fixing the search:** here, by not using the reranker.

Plain meaning-based search produced none of these confident wrong answers; every reranked run produced 1 or 2.

## 4. Is a 10% quality gain worth 800 ms of extra waiting?
- **Pharma research assistant: yes.** A wrong answer can send research the wrong way, and a researcher will wait
  a second for a better one. 800 ms on our 6–7 s answers is about 13% more waiting.
- **Shopping assistant: usually no.** A wrong product answer costs less, and speed affects sales. And 800 ms on a
  1-second search box nearly doubles the wait.
- **What actually happened here:** the trade on offer wasn't +10% for 800 ms. It was **+1 s for a 2–8 point loss**,
  plus a new kind of error that looks trustworthy. Easy no.

## 5. "Best practice" is a hypothesis to test, not a decision
If engineers want hybrid search and a reranker because it's industry best practice, I'd run our golden test set
three ways (meaning-based only, hybrid, hybrid + reranker) and compare. If the results are about the same, there's no
point paying for the extra cost, latency and moving parts. If one is clearly better, ship it. Two things to measure
beyond the score:
- **Latency and cost per question**, end to end.
- **New kinds of error.** The score hid that the reranker added confident, well-cited wrong answers.

**When I'd revisit it for this product:** the library grows to thousands of documents; users start typing trial
IDs, compound codes or batch numbers; or search logs show exact-term questions failing.

## 6. Measure the cheap thing first
The rank report (where does the chunk holding the answer rank?) needs no chat-model calls and has no randomness,
so it tested 4 settings × 28 questions for about 200 reranker calls and no Gemini quota. The full answer runs
(~300 chat calls) came last, only for the settings worth confirming. They agreed with the rank report, and showed
the one thing ranks can't: what the model does with what it's given.

## Corrections to earlier stages
- **Q09 (OHDSI) isn't randomness.** Refused 7 of 7 with whole-sentence chunks, even with its answer ranked 1st: the
  model won't read "Observational Health Data Sciences and Informatics (OHDSI) consortium", in a list of three
  networks, as a definition. A prompt or chunking problem, not search.
- **Temperature was never applied.** `gemini-3.5-flash-lite` ignores it, so Stages 2–3's temperature settings ran on
  the model's defaults. Answers vary run to run; that's why each setting here ran twice.
