"""Scores a cited run: citation accuracy, the confidence shown to the user, and the two error types.

Usage (from the rag-projects folder), after grading the run with rag-eval/grade.py:
    python3 rag-citations/score_cited.py cited
    python3 rag-citations/score_cited.py cited gemini-3.5-flash-lite    # which model's grades to use for "correct"

Reads results/<run>_grades.csv and results/<run>_claims.csv (from run_cited.py), and
results/<run>_model_grades_<model>.csv (from grade.py) if it exists. Makes no API calls, so changing the
confidence rule below and rescoring is free and instant.
"""
import csv
import os
import sys
from collections import Counter, defaultdict

POINTS = {"yes": 1, "partly": 0.5, "no": 0}  # same as rag-eval/score.py


def confidence(refused, verdicts, says_missing):
    """The confidence label the user sees next to an answer, worked out from the verifier's verdicts.

    Rule C (my decision, 2026-10-08, for a medical research product; see EXPERIMENTS.md): strict on citations,
    and an answer that admits a gap is never "high". Checked worst to best: the first match wins.
    refused: True when the answer has no claims ("The documents don't answer this").
    verdicts: one per claim, each "supported", "partly", "not supported" or "not checked".
    says_missing: True when the answer gives some claims but admits part of the question isn't covered.
    """
    if refused:
        return "refused"
    if not all(v == "supported" for v in verdicts):
        return "low"
    if says_missing:
        return "medium"
    return "high"


def main():
    run_name = sys.argv[1]
    grader_model = sys.argv[2] if len(sys.argv) > 2 else "gemini-3.5-flash-lite"
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    questions = list(csv.DictReader(open(os.path.join(results_dir, f"{run_name}_grades.csv"))))
    claims_path = os.path.join(results_dir, f"{run_name}_claims.csv")
    claims = list(csv.DictReader(open(claims_path))) if os.path.exists(claims_path) else []
    grades_path = os.path.join(results_dir, f"{run_name}_model_grades_{grader_model}.csv")
    graded = {r["id"]: r for r in csv.DictReader(open(grades_path))} if os.path.exists(grades_path) else {}

    print(f"Run: {run_name} ({len(questions)} questions, {len(claims)} claims)")

    # 1. Citation accuracy: of all the claims, how many does the cited chunk actually support?
    verdicts = Counter(c["verifier"] for c in claims)
    print("\nCitation accuracy (verifier):")
    for verdict in ["supported", "partly", "not supported", "not checked"]:
        if verdicts[verdict]:
            print(f"  {verdict:<14} {verdicts[verdict]:>3}  ({verdicts[verdict] / len(claims):.0%})")
    hand_key = "hand (supported/partly/not supported)"
    checked = [c for c in claims if c[hand_key]]
    if checked:
        # The verifier is part of the product; your hand check measures how far it can be trusted
        same = sum(c[hand_key] == c["verifier"] for c in checked)
        hand = Counter(c[hand_key] for c in checked)
        print(f"  Hand-checked {len(checked)} claims: {hand['supported']} supported by hand; "
              f"verifier agrees on {same} of {len(checked)} ({same / len(checked):.0%})")
        for c in checked:
            if c[hand_key] != c["verifier"]:
                print(f"    {c['id']} claim {c['claim']}: you {c[hand_key]}, verifier {c['verifier']}")

    # 2. Confidence per question, and whether it's calibrated: is "high" right more often than "low"?
    by_question = defaultdict(list)
    for c in claims:
        by_question[c["id"]].append(c["verifier"])
    levels = {q["id"]: confidence(q["refused"] == "yes", by_question[q["id"]], any(m in q["answer"] for m in ("Not in the documents:", "Not found in the documents:")))
              for q in questions}
    print("\nConfidence shown to the user:")
    print(f"  {'level':<9} {'questions':>9}   {'correct':>7}   ids")
    for level in ["high", "medium", "low", "refused"]:
        ids = [q["id"] for q in questions if levels[q["id"]] == level]
        if not ids:
            continue
        scored = [POINTS[graded[i]["correct (yes/partly/no)"]] for i in ids if i in graded]
        correct = f"{sum(scored) / len(scored):.0%}" if scored else "–"
        print(f"  {level:<9} {len(ids):>9}   {correct:>7}   {', '.join(ids)}")
    if not graded:
        print("  (no model grades yet: run rag-eval/grade.py on this run to fill the 'correct' column)")

    # 3. The two errors a researcher can suffer
    if graded:
        answerable = [q for q in questions if q["question_type"] != "unanswerable"]
        refusals = [q["id"] for q in answerable if q["refused"] == "yes"]
        wrong = [q["id"] for q in questions if q["refused"] == "no" and graded[q["id"]]["correct (yes/partly/no)"] == "no"]
        partly = [q["id"] for q in questions if q["refused"] == "no" and graded[q["id"]]["correct (yes/partly/no)"] == "partly"]
        score = sum(POINTS[graded[q["id"]]["correct (yes/partly/no)"]] for q in questions) / len(questions)
        faithful = sum(graded[q["id"]]["faithful (yes/no)"] == "yes" for q in questions)
        print(f"\nCorrect: {score:.0%}   Faithful: {faithful} of {len(questions)} ({faithful / len(questions):.0%})")
        print(f"Wrong answers (answered, but wrong): {len(wrong)}  {', '.join(wrong)}")
        print(f"Partly right answers:                {len(partly)}  {', '.join(partly)}")
        print(f"Unnecessary refusals (answerable):   {len(refusals)}  {', '.join(refusals)}")
        shown = [q["id"] for q in questions if q["id"] in wrong + partly and levels[q["id"]] == "high"]
        print(f"Wrong or partly right, shown as high confidence: {len(shown)}  {', '.join(shown)}  <- the dangerous ones")

    # 4. Cost of the check: how much waiting the verifier adds
    answer_s = [float(q["answer_seconds"]) for q in questions]
    verify_s = [float(q["verify_seconds"]) for q in questions]
    print(f"\nLatency per question: {sum(answer_s) / len(answer_s):.1f}s to answer + "
          f"{sum(verify_s) / len(verify_s):.1f}s to verify (rate-limit waits excluded)")


if __name__ == "__main__":
    main()
