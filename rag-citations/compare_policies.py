"""What should the app do with a claim the verifier can't back? Compares three policies on saved runs.

    show:   keep every claim; the answer is labelled "low" (rule C). The researcher sees the unbacked claim.
    drop:   remove claims that aren't fully supported and show the rest. Nothing left = a refusal.
    refuse: if any claim isn't fully supported, refuse the whole answer.

Usage (from the rag-projects folder):
    python3 rag-citations/compare_policies.py cited norefs sentences nearmiss_stage2 nearmiss_sentences

No API calls: uses each run's saved verifier verdicts and model grades. An answer that only loses some of
its claims ("trimmed") would need regrading to know its new score; those are listed for a hand check.
"""
import csv
import os
import sys
from collections import defaultdict

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def load(run):
    questions = list(csv.DictReader(open(os.path.join(RESULTS, f"{run}_grades.csv"))))
    grades = {r["id"]: r["correct (yes/partly/no)"]
              for r in csv.DictReader(open(os.path.join(RESULTS, f"{run}_model_grades_gemini-3.5-flash-lite.csv")))}
    verdicts = defaultdict(list)
    for c in csv.DictReader(open(os.path.join(RESULTS, f"{run}_claims.csv"))):
        verdicts[c["id"]].append(c["verifier"])
    return questions, grades, verdicts


def outcome(policy, q, grade, verdicts):
    """What the researcher gets for one question under one policy."""
    unbacked = sum(v != "supported" for v in verdicts)
    if q["refused"] == "yes":
        return "refused", 0
    if unbacked == 0 or policy == "show":
        return "answered", unbacked
    if policy == "refuse" or unbacked == len(verdicts):
        return "refused", 0
    return "trimmed", 0  # drop, with some claims left


def main():
    for run in sys.argv[1:]:
        questions, grades, verdicts = load(run)
        unbacked_total = sum(v != "supported" for vs in verdicts.values() for v in vs)
        claims_total = sum(len(vs) for vs in verdicts.values())
        print(f"\n{run}: {len(questions)} questions, {unbacked_total} of {claims_total} claims not fully supported")
        print(f"  {'policy':<7} {'unbacked claims shown':>22} {'unnecessary refusals':>21} {'right answers lost':>19}   trimmed (regrade by hand)")
        for policy in ["show", "drop", "refuse"]:
            shown = needless = lost = 0
            trimmed = []
            for q in questions:
                result, unbacked = outcome(policy, q, grades[q["id"]], verdicts[q["id"]])
                shown += unbacked
                if result == "refused" and q["question_type"] != "unanswerable":
                    needless += 1
                    if q["refused"] == "no" and grades[q["id"]] != "no":
                        lost += 1  # this policy turned an answer that was at least partly right into a refusal
                if result == "trimmed":
                    trimmed.append(q["id"])
            print(f"  {policy:<7} {shown:>22} {needless:>21} {lost:>19}   {', '.join(trimmed) or '-'}")


if __name__ == "__main__":
    main()
