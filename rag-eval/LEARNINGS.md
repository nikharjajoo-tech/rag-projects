# What I learned measuring RAG quality (Stage 2)

My PM notes from building an evaluation harness for a basic RAG app: 20 test questions over two
research papers, a grading rubric, a model grader checked against my own grades, and a first experiment.

## 1. A quality score is a range, not a number
Our app scores 82%, but with 20 questions each one is worth 5 points, so the honest claim is
"roughly 72–92%". Four things decide how much to trust a score:
- **Sample size:** small test sets can't detect small changes. I treat differences under ~10 points as noise.
- **Representativeness:** I wrote the questions, and half come from one paper. Real user questions
  would be the better test set.
- **Grader error:** the grader agrees with me 95% of the time and has a known blind spot.
- **Randomness:** the same question can get a different answer on a re-run.

A score per question type says more than one headline number: we're at 100% on simple facts and
unanswerable questions, but 40–50% on questions whose answer is spread across a document.

## 2. Grade the search and the answer separately
A RAG answer can fail in two places, and they need different fixes.
- **Correct** compares the answer with the true answer: what the user got.
- **Faithful** compares the answer with the chunks the model was given: whether the model was honest.

They can disagree. When the search missed, the model said "not in the documents". That was *faithful*
(true of what it saw) but *not correct* (the documents did have the answer). Most of our failures were
search failures, not model failures — so the next investment is search quality, not a bigger model.

## 3. A clear rubric matters more than a better grader model
Clarifying two rules in the rubric took the model grader from 80% to 95% agreement with me. Switching to
a stronger model added nothing. Most grader "mistakes" were the rubric being ambiguous — and two careful
humans (Claude and I) disagreed on 5 of 20 for the same reason.

## 4. How I'd adopt an LLM grader
- Build a golden set graded by humans first, and **set the agreement bar before switching** (e.g. 90%).
- Use a grader from a **different model family** than the one answering, to avoid self-preference.
  Ours tended to be lenient towards answers from its own family.
- **Move humans, don't remove them:** people check every failure, borderline cases, and random samples.
  Our grader never caught a claim stitched together from two chunks.
- **Measure consistency** (ours agreed with itself 19 of 20 times) and re-check whenever the grader
  model or rubric changes.
- Keep rubric examples generic so the grader isn't taught the test answers.

## 5. Check what the system actually did, not what you configured
I set chunk overlap to 80 characters, expecting 20%. The PDF text splits into ~91-character lines and
overlap only carries whole lines, so the real overlap was almost zero. The setting isn't the behaviour.

## 6. When quality is equal, choose the cheaper option, and check what you remove
- Cutting overlap kept quality the same (82% vs 80%, within noise) with **37% fewer chunks** to embed
  and store, so it became the default. Before rolling it out widely I'd test each document type, keep
  the old index for rollback, and watch refusal rates and user feedback.
- Dropping "near-duplicate" chunks lost answers: overlapping neighbours each hold text the other doesn't.
  Removing "duplicates" needs a check of what's being thrown away.

## 7. Constraints shape the design
The strongest free model allowed 20 requests a day — less than one test run. Switching to a smaller model
before measuring anything cost nothing in comparability, and kept every later experiment affordable.

## How I answer evaluation questions now
**Number → uncertainty → evidence → decision → risk.** For example: "We're at about 82%, ±10 points
on 20 questions. The failures are mostly search, not the model, concentrated in multi-part questions. So
I'd fund retrieval improvements before a bigger model, and re-test on real user questions first."
