# Experiment log

Same rules as Stage 2 (`../rag-eval/EXPERIMENTS.md`): prediction written *before* the run, same 20
questions, same rubric. One question = 5 points; differences under ~10 points are noise.

Reference point: `overlap80` (Stage 2): model-graded 82% correct, 100% faithful, 50% on spread-out
questions; 0 wrong answers, 2 unnecessary refusals (Q03, Q15), plus Q16 refused.

## Smoke test (2026-10-07): Q01, Q10, Q13, Q17

Checked that the pipeline works before spending a full run's quota. Not a score: 4 questions.

- **Q10: the verifier caught what the grader missed.** The answer said BEHRT "learns disease subphenotypes
  and handles irregular time intervals". The chunk says that about a *different* model (reference 42), in
  the sentence before BEHRT's. The verifier marked the claim not supported (checked by hand: correct).
  The grader again called the whole answer faithful, the same miss as in Stage 2. Checking one claim
  against one chunk is a narrower, easier task than judging a whole answer against five chunks.
- **Q13: rubric question to settle.** The answer gives each paper's role, tagged "(Blanco p5)" and
  "(Chen p7)", but never names the papers in the text. The grader gave *partly*: the rubric says
  both-paper answers must say which paper says what. Does a citation count as saying it?
- Q17 refused correctly. Q01 correct, one supported claim.
- Latency: ~2.5s to answer + ~1.5s to verify per question.

## Experiment 1: citations + verifier vs. the Stage 2 reference

**My prediction (written 2026-10-07, before building):** citations plus a second model checking each
citation against the retrieved chunks will increase faithfulness, but correctness will stay the same.

**Result (2026-10-07), run `cited`, graded by gemini-3.5-flash-lite, failures hand-checked:**

| Run | Correct | Faithful | Wrong answers | Unnecessary refusals | Citation accuracy | Latency per question |
|---|---|---|---|---|---|---|
| `overlap80` (Stage 2) | 82% | 100% | 0 | 2 (Q03, Q15) + Q16 refused | not measurable | ~2.5s |
| `cited` | 85% | 100% | 0 | 2 (Q03, Q15) | 27 of 28 claims (96%) | 2.4s + 3.0s to verify |

Confidence shown to the user (default rule: all claims supported = high, at least half = medium, else low):

| Level | Questions | Correct |
|---|---|---|
| high | 13 | 92%: Q14 and Q16 only partly right |
| low | 1 | Q12, correct answer, unsupported citation |
| refused | 6 | 4 correct refusals (Q17–Q20), 2 unnecessary (Q03, Q15) |

- **Prediction half right.** Correctness stayed the same (82% → 85% is within noise). Faithfulness
  couldn't rise: it was already 100%. But that 100% was over-scored: the grader passes claims stitched
  across chunks. **Citations didn't make answers more faithful; they made unfaithfulness visible**,
  one claim at a time.
- **Q12: right answer, wrong evidence.** "BACE1 is a protein involved in Alzheimer's disease": correct, but
  it cites two reference-list chunks that mention BACE1 and Alzheimer's separately. The chunk that says it
  (Blanco p4) is cut mid-sentence: "…BACE1, a protein involved". The verifier marked it not supported
  (correct, checked by hand); the grader called it faithful. A researcher who clicks the citation can't
  confirm the claim, so low confidence is the honest label, even though the answer is right.
- **The verifier checks that each claim is supported, not that the answer is complete.** Both dangerous
  cases (partly right, shown as high) are *missing* facts, not wrong ones. Q16 says so itself ("Not in
  the documents: …"), so the confidence rule can catch it. Q14 doesn't, and nothing in this design
  catches it: completeness needs better search (Stages 4, 6–7), not checking.
- **Citations don't fix search misses.** Q03 and Q15 are refused as in Stage 2. Q16 went from a refusal
  to a half answer with honest "missing" text: one fewer refusal.
- **Product copy:** "The documents don't answer this" is wrong for Q03 and Q15. The documents do; the search
  didn't find it. "I couldn't find this in the documents" is honest about which one failed.
- **Cost:** the verifier doubles the chat calls and more than doubles the wait (2.4s → 5.4s per question).
- **Evaluation fix:** with bare `[2]` tags the grader didn't credit citations as saying which paper says
  what, even after the rubric rule was added (Q13 graded partly). Showing it `[2 Blanco p5]` fixed it
  (Q13 → yes); Q13, Q14 and Q16 regraded, answers unchanged. First grades kept in
  `results/archive_cited_model_grades_bare_tags.csv`. Lesson: grade what the user sees.
- **Verifier hand check (2026-10-08): agrees on 28 of 28 claims.** I looked up each claim in the PDFs
  and noted the page; it matched the cited page on 27, and the odd one out is Q12 (found on Blanco p4,
  cited p9 and p10): not supported, as the verifier said. Q09 cites reference 52 on p16, whose title
  spells out OHDSI: supported, though a body-text citation (p7) would be better for a researcher.
- **But 100% agreement proves little about catching errors.** 27 of 28 claims were supported, so a
  verifier that always said "supported" would also agree 96% of the time. It has caught 2 bad claims
  so far (Q12; Q10 in the smoke test) and missed none we know of, which is too few to trust it on the
  rare case that matters. Also, a page match is a slightly weaker check than reading the cited chunk:
  a page holds 5–6 chunks. Next: break it on purpose, feeding it wrong citations to see how many it catches.

## Experiment 2: break the verifier on purpose (2026-10-08)

**Question:** when a citation does *not* support its claim, how often does the verifier catch it?

**Design:** the 27 supported claims from `cited`, each re-pointed at a wrong chunk from the same search:
- easy: the chunk sharing the fewest words with the claim (clearly unrelated)
- hard: the other chunk sharing the most words with the claim (same topic: a near-miss like Q12)

Same verifier, same one-call-per-question batching as the app. Every "supported" verdict is hand-checked,
because a near-miss chunk can turn out to state the claim too (overlapping neighbours, repeated facts).

**Prediction:** none written by me before the run. Claude's expectation, logged before running: it
catches nearly all easy ones and misses a few hard ones, mostly where the wrong chunk repeats key terms.

**Result (2026-10-08).** Hand check first: in the hard version, 4 of the "wrong" chunks turned out to
state the claim too (Q09, Q11 ×2, Q13 claim 6), and 4 more state part of it. So results are counted
against what each planted chunk actually says. Files: `results/cited_break_v1.csv`, `cited_break_v2.csv`.

**v1** (the verifier used in `cited`: all five chunks listed once, "read only the cited one"):

| Planted chunk... | Claims | Rejected | Marked partly | Passed as supported |
|---|---|---|---|---|
| doesn't state the claim (easy) | 26 | 26 | 0 | 0 |
| doesn't state the claim (hard) | 19 | 17 | 0 | **2** (Q07 ×2) |
| does state it (hard) | 4 | **4** | 0 | 0 |

- **Both misses came from reading the wrong chunk.** For Q07 the verifier's own reason quotes the real
  source ("Source [5] states…"), not the planted reference-list entry. Telling it to "read only the
  cited source" while showing it all five didn't work.
- **It rejected all 4 valid alternative citations.** It wasn't checking what the cited chunk says, but
  whether the cited number matched where it had seen the fact. Its 98% catch rate was partly that shortcut.

**Fix, v2:** each claim is shown only the text of the chunk it cites (still one call per question).
Rerun with a control: the 27 real citations.

| Planted chunk... | Claims | Rejected | Marked partly | Passed as supported |
|---|---|---|---|---|
| the real citation (control) | 27 | 0 | 0 | 27 ✅ |
| doesn't state the claim (easy) | 26 | 25 | 1 | 0 |
| doesn't state the claim (hard) | 19 | 16 | 2 | **1** (Q14 claim 3) |
| does state it (hard) | 4 | 0 | 0 | 4 ✅ |

- **v2 judges the text, not the number:** it accepts all 31 valid citations (27 real, 4 alternative) and
  fully passes 1 of 45 wrong ones. v1 rejected 4 of 31 valid ones and fully passed 2 of 45 wrong ones.
- **What still fools it:**
  - **Shared phrases:** Q14 claim 3 ("limited, low-quality data… affects accuracy and reliability")
    passed against a chunk on data augmentation "improving the accuracy and reliability".
  - **Claims mixed up within one call:** Q14 claim 1's reason describes claim 2's chunk. Both v2
    problems are in the questions with the most claims per call (Q13: 6, Q14: 4).
  - "Partly" is generous: 3 of the 45 wrong citations got it.
- **Tradeoff:** one call per claim would stop the mix-ups but use 1.4× the calls on this test set (28
  claims vs. 20 questions), and 3–6× on questions with many claims. Not done: one wrong citation in 45
  passed, against roughly one real bad citation in 28 claims.
- **Decision:** v2 is now the verifier in `run_cited.py`. The `cited` run's verdicts are from v1; the
  control shows its 27 supported claims stay supported under v2. Q12 hasn't been rechecked with v2.
- **What it means for the product:** a near-miss citation (same topic, doesn't state the claim) gets
  through about 1 time in 20 at most, and is marked "partly" 2 more times. "High confidence" is a strong
  signal, not proof, which is why the source must stay one click away.

## Experiment 3: clean what goes into the index (2026-10-08)

**Question:** search returned wrong or useless chunks (a third of `cited`'s 100 retrieved chunks were
reference-list entries; Q12's fact was cut mid-sentence). Does cleaning the index fix that?

**Variants** (built with `build_index.py`, same questions, same answer prompt, verifier v2):
- `cited`: Stage 2 database, 268 chunks (reference: run above, verifier v1)
- `norefs`: fix 1, reference lists removed (Chen p9–18, Blanco p8–11; Chen's figures and Table 1 kept),
  same 400 / 80 splitter: 182 chunks
- `sentences`: fix 1 + fix 2, whole-sentence chunks of up to ~400 characters, each starting with the
  previous chunk's last sentence: 232 chunks

**Prediction:** none written by me before the run. Claude's expectation, logged before running: reference
entries in the top 5 drop to ~0; Q12 gets a real citation; Q03/Q15/Q16 may improve if real passages take
the freed slots; overall correctness within noise. Q08, Q09, Q10 and Q11 used reference entries before
(Q09 cited one), so a loss there is possible.

**Result (2026-10-08), graded by gemini-3.5-flash-lite, changed questions read by hand:**

| Run | Chunks | Junk reference chunks in top 5 (of 100) | Expected pages found | Correct | Unnecessary refusals | Claims supported |
|---|---|---|---|---|---|---|
| `cited` | 268 | 24 | 21 of 25 | 85% | 2 (Q03, Q15) | 96% (v1) |
| `norefs` | 182 | 2 | 21 of 25 | 80% | 3 (Q03, Q12, Q15) | 100% |
| `sentences` | 232 | 2 | 20 of 25 | 80% | 3 (Q03, Q09, Q16) | 100% |

(Earlier "a third of chunks were references" used a looser pattern that also counted "et al." in body
text; the stricter count is 24 of 100.)

- **The cleaning worked on the inputs:** junk in the top 5 fell from 24 slots to 2, and every claim's
  citation was supported in both new runs.
- **The score didn't move** (85 → 80 → 80, within noise). The freed slots went to other passages on the
  same topic, not to the passages with the answer. Q03, Q15 and Q16 still fail on search, now for one
  reason only: the right chunk ranks below five on-topic ones. That's what reranking fixes (Stage 4).
- **Q12 shows why both fixes were needed.** In `cited` the right answer came from reference-list titles
  (the bad citation found in Experiment 1). Removing them (`norefs`) made the app refuse honestly: the
  only real passage was cut before "...in the development of Alzheimer's disease". Whole-sentence chunks
  (`sentences`) fixed it: correct, with a supported citation to Blanco p4. Right answer, right reason.
- **Q14 improved** (partly → yes) with sentence chunks: each paper's obstacles came back whole.
- **Q09 is noise, not search:** the OHDSI sentence was retrieved, and the model still said "not
  mentioned". Answer randomness (temperature 1) flips a question or two per run.
- **Q16 got worse:** one fewer expected page, and the model refused outright instead of giving
  Blanco's half. Graded unfaithful: Blanco's half was in the chunks.
- **Q15 is counted as a "wrong answer" by `score_cited.py`, but it isn't one:** a single true claim (55
  adverse-event studies) plus "the rest isn't in the documents". Nothing invented. The confidence rule's
  `says_missing` would move it off "high".
- **Recommendation (my decision pending):** make `sentences` the default database for later stages: same
  score, a fact can no longer be split in half, no junk slots, 13% fewer chunks than Stage 2's database.

## Choosing the confidence rule (2026-10-08)

Three candidate rules, scored on the saved verdicts of all three runs (no new API calls):

| Rule | "High" answers right | Not fully right, but "high" |
|---|---|---|
| A. all claims supported = high, at least half = medium, else low | 92% | Q14, Q16 (Q15 in `sentences`) |
| B. A, plus "answer admits something is missing" = medium | 96–100% | Q14 |
| C. strict: any claim not fully supported = low; admits missing = medium; else high | 96–100% | Q14 |

- B and C give identical results here: nearly every claim was fully supported, so strictness on
  citations cost nothing. They'll differ on the near-miss questions, where partly-supported claims appear.
- No rule catches Q14: every claim it makes is true and correctly cited; it just leaves facts out and
  doesn't say so. Completeness is a search problem (Stages 4, 6), not a labelling one.
- **Decision: rule C**, for a medical research product: strict on citations, and an answer that admits a
  gap is never "high". Show the reason with the label ("part of your question isn't covered"), not just
  the level. Check on the near-miss questions whether C pushes too many answers to "low".

## Experiment 4: near-miss questions (2026-10-08)

8 new questions I wrote (`test_set_nearmiss.csv`), kept apart from the original 20 so Stage 2 scores stay
comparable: 4 answerable with a trap nearby (N01, N03, N05, N07) and 4 not answerable but nearly
(N02, N04, N06, N08). Answer key checked against the PDFs. Run on the Stage 2 database and on
`sentences`, verifier v2, scored with rule C.

**Prediction:** none written by me. Claude's expectation, logged before running: the unanswerable ones
are refused or answered vaguely (the app hasn't invented a figure yet); N06 is the riskiest, since the
model may name the antibiotic from its own training; rule C puts at least one answer on "low" or "medium".

**Result (2026-10-08), graded by gemini-3.5-flash-lite, all 16 answers read by hand:**

| Database | Correct (model) | Correct (hand) | Invented answers | Unnecessary refusals | Claims supported | "High" answers right |
|---|---|---|---|---|---|---|
| Stage 2 (`pharma_db.json`) | 88% | 81% | 0 | 0 | 8 of 9, 1 partly | 75% (N05 partly) |
| `sentences` | 94% | 94% | 0 | 0 | 14 of 14 | 88% (N05 partly) |

- **No traps sprang:** all 4 unanswerable questions were refused or answered vaguely in both runs. N06
  didn't name the antibiotic from the model's own memory; N08 didn't reuse the first-round date; N02 said
  "billions" with no made-up figure.
- **Both Stage 2 database failures were chunks cut mid-fact**, and whole-sentence chunks fixed both:
  - N01: the chunk ends at "...continuation of statin therapy and incidence". The answer repeated the
    fragment ("...and incidence."). The verifier marked it partly; rule C showed **low**. The grader said
    *yes*; by hand it's *partly* (death and cardiovascular events missing). The verifier was right, the grader wasn't.
  - N03: the chunk ends right before the "why" (irregular time intervals); the model then said the reason
    wasn't in the sources, though another chunk had it. Rule C showed **medium**.
- **Rule C vs B:** they differed only on N01 (C: low, B: medium). Low was fair: the claim was literally a
  fragment. C didn't wrongly demote any fully correct answer.
- **N05 is the third incomplete-but-"high" answer** (after Q14): every claim is true and cited, but one of
  Blanco's four ethical concerns is missing, and the answer doesn't say so. On `sentences` the missing
  concern wasn't retrieved at all (search miss). This is the main risk left, and no label rule catches it.
- **More evidence for `sentences` as the default database:** 94% vs 81% by hand on these questions.

## Experiment 5: what to do with a claim the verifier can't back (2026-10-12)

`compare_policies.py`, on the saved verdicts of all runs (no API calls). Only **3 of 115 claims** were not
fully supported, and **none** on the `sentences` database: a clean index makes this decision rare.

| Case | The unbacked claim | Show | Drop the claim | Refuse the answer |
|---|---|---|---|---|
| Q10 (smoke) | wrong: another model's features credited to BEHRT | wrong claim shown, labelled low | wrong claim gone, correct half kept | mostly right answer lost |
| Q12 (`cited`) | true, but the citation doesn't back it | right answer, labelled low | becomes a refusal | becomes a refusal |
| N01 (`nearmiss_stage2`) | a fragment ("...and incidence.") | fragment shown, labelled low | partly right half kept | partly right answer lost |

(Trimmed answers checked by hand: Q10 without its wrong claim is mostly correct; N01 without the
fragment is partly correct.)

- **Refusing is never better than dropping:** it threw away something useful in all three cases.
- Too few cases for the planned chart of wrong answers vs. unnecessary refusals; the cases decide it.
- **Decision (mine): show the claim, flagged, and let the researcher decide.** Dropping loses true
  claims with a bad citation (Q12); showing unflagged hides wrong ones (Q10). So every claim the verifier
  doesn't fully confirm stays visible, marked "⚠ not confirmed by the cited source", with view source /
  accept / edit / reject. The answer as a whole keeps rule C's "low" label.
  - Each accept or reject is a free human label on the verifier's verdict: the hand check, at scale.
  - Risks to design against: accepting without reading (automation bias: require "view source" before
    accept), and the warning lost when the answer is copied into a report.
- Built: `run_cited.py` marks flagged claims in what the user sees (buttons need a real UI). Also reworded
  refusals: "I couldn't find this in the documents" instead of "The documents don't answer this", since
  the documents often do answer it and search missed (Q03, Q15); partial answers say "Not found in the documents: …".
