# Stage 2: Measure it

A fixed test set, a grading rubric and a checked model grader, so every later stage can answer
"did this change actually help?" with a number instead of a feeling.

How the indexing, answering and evaluation flows fit together: see the diagram in [PIPELINE.md](PIPELINE.md).

## What's here

| File | What it does |
|---|---|
| `test_set.csv` | 20 questions over the two test PDFs, with correct answers and pages, in 5 types (below) |
| `RUBRIC.md` | How to grade: key facts, *correct* vs. *faithful*, failure patterns |
| `run_eval.py` | Runs every question through the RAG pipeline and saves each answer next to its retrieved chunks |
| `grade.py` | Has a Gemini model grade a run with the rubric, and compares it with the hand grades |
| `score.py` | Scores a graded run: overall, by question type, by failure pattern |
| `add_pdf.py` | Adds a PDF to a database without duplicates, for any chunk setting |
| `EXPERIMENTS.md` | Every run: prediction first, then result |
| `LEARNINGS.md` | My PM takeaways from this stage |
| `results/` | Run reports (`.md`), hand grades (`*_grades.csv`), model grades (`*_model_grades_*.csv`) |

**Question types**, each aimed at a failure a later stage should fix:
- **simple fact:** does basic RAG work at all?
- **different wording:** does meaning-based search find facts asked about in other words?
- **exact term:** names and acronyms, where meaning-based search is weak (Stage 4).
- **spread out:** answers spread across a paper or both papers (Stages 6–7).
- **unanswerable:** does it admit "not in the documents" or invent an answer (Stage 3)?

## How to run (from the `rag-projects` folder)

```
rag-chain/.venv/bin/python rag-eval/run_eval.py my_run                            # current app settings
rag-chain/.venv/bin/python rag-eval/run_eval.py my_run --overlap 200              # any chunk setting
rag-chain/.venv/bin/python rag-eval/grade.py my_run gemini-3.5-flash-lite         # model grading
python3 rag-eval/score.py my_run_model_grades_gemini-3.5-flash-lite               # scores
```

Uses `rag-chain`'s virtual environment and `.env`. A run is ~20 embedding + 20 chat calls and grading
another 20, all within the free tier on `gemini-3.5-flash-lite` (about 5 minutes with rate-limit waits).

## Results

| Run | Correct | Faithful | Spread out |
|---|---|---|---|
| Baseline, 400 / 200, graded by hand | 78% | 90% | 40% |
| 400 / 80 (new default), model-graded | 82% | 100% | 50% |

- **Search is the weak point, not the model:** most failures are chunks that never came back.
- **Spread-out questions are the gap (40–50%).**
- **The model grader agrees with hand grades 95% of the time**, after the rubric was clarified (80%
  before), and agrees with itself 19 of 20 times. It misses claims stitched across two chunks.
- **With 20 questions, differences under ~10 points are noise.**

Details, including the overlap experiment and what went wrong in it, are in `EXPERIMENTS.md`.

## What I learned (PM note)

See [LEARNINGS.md](LEARNINGS.md).
