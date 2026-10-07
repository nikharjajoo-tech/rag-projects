"""Scores a graded run: overall, by question type, and by failure pattern.

Usage (from the rag-projects folder):
    python3 rag-eval/score.py baseline
"""
import csv
import os
import sys
from collections import Counter, defaultdict

POINTS = {"yes": 1, "partly": 0.5, "no": 0}  # "partly" counts as half a correct answer

run_name = sys.argv[1] if len(sys.argv) > 1 else "baseline"
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", f"{run_name}_grades.csv")
rows = list(csv.DictReader(open(path)))


def score(subset):
    return sum(POINTS[r["correct (yes/partly/no)"]] for r in subset) / len(subset)


print(f"Run: {run_name} ({len(rows)} questions)\n")
print(f"Correctness score: {score(rows):.0%}  (yes = 1, partly = 0.5, no = 0)")
print(f"Correct / partly / wrong: {Counter(r['correct (yes/partly/no)'] for r in rows)['yes']} / "
      f"{Counter(r['correct (yes/partly/no)'] for r in rows)['partly']} / "
      f"{Counter(r['correct (yes/partly/no)'] for r in rows)['no']}")
faithful = sum(r["faithful (yes/no)"] == "yes" for r in rows)
print(f"Faithful: {faithful} of {len(rows)} ({faithful / len(rows):.0%})\n")

print("By question type:")
by_type = defaultdict(list)
for r in rows:
    by_type[r["question_type"]].append(r)
for question_type, subset in by_type.items():
    print(f"  {question_type:<18} {score(subset):>4.0%}  ({len(subset)} questions)")

patterns = Counter(r["failure_pattern"] for r in rows if r["failure_pattern"])
print("\nFailure patterns:")
for pattern, count in patterns.most_common():
    ids = ", ".join(r["id"] for r in rows if r["failure_pattern"] == pattern)
    print(f"  {pattern:<12} {count}  ({ids})")
