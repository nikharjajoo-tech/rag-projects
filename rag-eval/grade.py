"""Has a Gemini model grade a run using RUBRIC.md, then compares its grades with the hand grades.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-eval/grade.py baseline gemini-3.5-flash-lite
    rag-chain/.venv/bin/python rag-eval/grade.py baseline gemini-3.5-flash-lite repeat2   # grade again, separately

Reads   results/<run>.md                       (written by run_eval.py)
Writes  results/<run>_model_grades_<model>.csv (same columns as the hand-grading sheet)
Saves after every question, so a rerun after a quota stop picks up where it left off.
"""
import csv
import os
import re
import sys
from typing import Literal

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from run_eval import EVAL_DIR, with_retry

GRADE_COLUMNS = ["correct (yes/partly/no)", "faithful (yes/no)", "failure_pattern", "my_notes"]


class Grade(BaseModel):
    key_facts: list[str] = Field(description="The 1-4 key facts of the expected answer (empty for unanswerable questions)")
    search_check: str = Field(description="For each key fact, which retrieved chunk contains it, or 'not in chunks'")
    claims_check: str = Field(description="Each claim in the app's answer and whether a chunk supports it")
    correct: Literal["yes", "partly", "no"]
    faithful: Literal["yes", "no"]
    failure_pattern: Literal["none", "search-miss", "P01", "P02", "P03", "model-miss"]
    reason: str = Field(description="One sentence explaining the grade")


GRADER_PROMPT = """You are grading one answer from a retrieval-augmented question-answering system.
Apply this rubric exactly:

<rubric>
{rubric}
</rubric>

Question type: {question_type}
Question: {question}
Expected answer: {expected}
Notes from the test-set author: {notes}

Retrieved chunks (what the system was given):
{chunks}

The system's answer:
<answer>
{answer}
</answer>

Follow the rubric's routine in order: key facts, then search check, then claims check, then the grades."""


def parse_run(markdown):
    """Splits a run report from run_eval.py into one dict per question."""
    questions = []
    for block in markdown.split("\n---\n\n## ")[1:]:
        field = lambda name: re.search(rf"\*\*{name}:\*\* (.*?)\n\n?(?=\*\*|\n\*\*|$)", block, re.S)
        chunks = re.findall(r"\n\d+\. \*(\w+ p\d+), similarity [\d.]+\*.*?\n   > (.*)", block)
        notes = field("Notes")
        questions.append({
            "id": block.split()[0],
            "question_type": re.search(r"\((.*?)\)", block).group(1),
            "question": field("Question").group(1).strip(),
            "expected": field("Expected").group(1).strip(),
            "answer": re.search(r"\*\*App answered:\*\* (.*?)\n\*\*Search:\*\*", block, re.S).group(1).strip(),
            "notes": notes.group(1).strip() if notes else "none",
            "chunks": "\n\n".join(f"[{i}] ({where}) {text}" for i, (where, text) in enumerate(chunks, 1)),
        })
    return questions


def compare(hand_path, model_path):
    """Prints how often the model grader agrees with the hand grades."""
    hand = {r["id"]: r for r in csv.DictReader(open(hand_path))}
    model = {r["id"]: r for r in csv.DictReader(open(model_path))}
    ids = sorted(hand.keys() & model.keys())
    print(f"\nAgreement with hand grades ({len(ids)} questions):")
    for column, label in [("correct (yes/partly/no)", "correct"), ("faithful (yes/no)", "faithful"),
                          ("failure_pattern", "failure pattern")]:
        same = [i for i in ids if (hand[i][column] or "none") == (model[i][column] or "none")]
        print(f"  {label:<16} {len(same)} of {len(ids)} ({len(same) / len(ids):.0%})")
    print("\nDisagreements (hand -> model):")
    for i in ids:
        diffs = [f"{label}: {hand[i][c] or 'none'} -> {model[i][c] or 'none'}"
                 for c, label in [("correct (yes/partly/no)", "correct"), ("faithful (yes/no)", "faithful"),
                                  ("failure_pattern", "pattern")]
                 if (hand[i][c] or "none") != (model[i][c] or "none")]
        if diffs:
            print(f"  {i}: {'; '.join(diffs)}\n       model's reason: {model[i]['my_notes']}")


def main():
    run_name, grader_model = sys.argv[1], sys.argv[2]
    label = f"_{sys.argv[3]}" if len(sys.argv) > 3 else ""  # lets the same run be graded again into a new file
    results_dir = os.path.join(EVAL_DIR, "results")
    out_path = os.path.join(results_dir, f"{run_name}_model_grades_{grader_model}{label}.csv")
    # The rubric cites test questions as examples, e.g. "(Q05)"; strip them so the grader isn't taught the answers
    rubric = re.sub(r" ?\((?:see )?Q\d{2}[^)]*\)", "", open(os.path.join(EVAL_DIR, "RUBRIC.md")).read())
    questions = parse_run(open(os.path.join(results_dir, f"{run_name}.md")).read())

    done = {r["id"]: r for r in csv.DictReader(open(out_path))} if os.path.exists(out_path) else {}
    grader = ChatGoogleGenerativeAI(model=grader_model, api_key=os.getenv("GOOGLE_API_KEY")).with_structured_output(Grade)

    for q in questions:
        if q["id"] in done:
            continue
        print(f"Grading {q['id']}...")
        grade = with_retry(lambda: grader.invoke(GRADER_PROMPT.format(rubric=rubric, **q)))
        done[q["id"]] = {"id": q["id"], "question_type": q["question_type"], "question": q["question"],
                         "expected": q["expected"], "answer": q["answer"],
                         "correct (yes/partly/no)": grade.correct, "faithful (yes/no)": grade.faithful,
                         "failure_pattern": "" if grade.failure_pattern == "none" else grade.failure_pattern,
                         "my_notes": grade.reason}
        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(done[q["id"]].keys()))
            writer.writeheader()
            writer.writerows(done[i] for i in sorted(done))

    print(f"Saved {os.path.relpath(out_path, EVAL_DIR)}")
    hand_path = os.path.join(results_dir, f"{run_name}_grades.csv")
    if os.path.exists(hand_path):
        compare(hand_path, out_path)


if __name__ == "__main__":
    main()
