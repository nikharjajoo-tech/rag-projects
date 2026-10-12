# What I learned adding citations and "I don't know" (Stage 3)

My PM notes from making a research assistant for a pharma research company show its sources: every claim
carries a citation, a second model call checks each claim against the source it cites, and the answer gets
a confidence label. 20 test questions plus 8 near-miss questions, over two research papers.

## 1. Citations don't create trust on their own; they let the researcher check
The idea was that if every claim the LLM makes is backed by a citation, the answer becomes transparent
and the researcher can trust it more. But a citation alone can create *too much* trust: people believe
text with a source attached without opening it. Trust has to come from checking, which is why the
product checks every citation and asks the researcher to view the source before accepting a flagged claim.

**What I predicted vs. what happened:** I expected citations to make answers more faithful. They didn't
(faithful stayed at 95–100%). They made unfaithfulness **visible**: the checker caught claims stitched
together from two chunks that the whole-answer grader had passed.

## 2. Three steps, done by two different things
1. **Search** (no LLM) finds the 5 chunks closest in meaning to the question.
2. **The LLM** writes the answer as claims, each tagged with the chunk it came from.
3. **The verifier** (a second LLM call) checks each claim against *only* the chunk it cites. Each claim
   gets a verdict: supported, partly supported, or not supported.

## 3. What can go wrong, and who catches it

| Case | Caught by the verifier? | What the researcher sees | In our tests |
|---|---|---|---|
| 1. Right chunks, right citation, complete answer | n/a | High | Most answers |
| 2. Right chunks, right citation, incomplete answer | No | Medium if the model admits the gap; **high if it doesn't** | Q14, N05 shown as high |
| 3. Wrong chunks (search missed), right citation | No | Usually "I couldn't find this" | Q03, Q09, Q16: unnecessary refusals |
| 4. Right chunks, wrong citation | **Yes** | Low, claim flagged | Passed 1 of 45 planted wrong citations |

**The verifier only protects against wrong citations.** Incomplete answers and search misses get past
it. They need better search (Stage 4) and the researcher's own review.

## 4. Confidence comes from the checker, not from the model
Models are poorly calibrated about themselves, so the label comes from the verifier's verdicts. For a
medical research product I chose a strict rule (rule C), checked worst first:
- any claim not fully supported → **low**
- the answer admits part of the question isn't covered → **medium**
- otherwise → **high**

"High" was right 100% of the time on the 20 questions, 88% on the near-miss set. The one failure no rule
can catch: an answer that silently leaves facts out.

## 5. Show the doubtful claim, flagged — don't hide it
Should low-confidence claims stay in the answer? Some answers were right even though a claim's citation
was weak. Refusing the whole answer was never better than dropping the claim, and dropping threw away a
true claim (Q12). So the product shows the full answer with the unbacked claim highlighted, and the
researcher can view the source, then accept, edit or reject it. Every accept or reject is a free human
check on the verifier.

## 6. Fix the inputs even when the score doesn't move
Removing reference lists from the papers cut junk chunks in search results from 24 of 100 to 2, and
whole-sentence chunks stopped facts being cut in half. Correct stayed at 80–85% (within noise), because
the freed slots went to on-topic passages that don't hold the answer. Ranking the right passage first
is the next problem.

## 7. What it costs
The verifier doubles the model calls and roughly doubles the wait. No invented answers on any of the
28 questions, but this is 2 papers and 28 questions: it shows direction, not proof.

## Where I set the line: medical vs. shopping assistant
The line depends on what each error costs and who reads the answer.
- **Medical:** a wrong answer is the worst outcome, so be strict: verify every claim, rule C, flag
  unbacked claims. There's an expert behind the screen who can check each claim against its source,
  so flags are worth showing.
- **Shopping:** a wrong answer usually costs less, and an unnecessary refusal is a lost sale, so lean
  towards answering. There's no expert behind the screen: shoppers won't check claims, so flags make no
  sense. Verifying everything doubles cost and wait, so verify only the claims that matter (price,
  allergens, compatibility, return policy), and check a sample of past answers to measure quality.
- **The catch I learned:** rule C is free to run, but its input isn't. Without the verifier there are no
  verdicts, so no confidence label and no flags. The rule is free; the information it depends on costs money.
