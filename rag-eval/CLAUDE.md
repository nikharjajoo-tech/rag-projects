# rag-eval — stage 2 of the series (measurement)

(Who I am, repo conventions and machine constraints are in `../CLAUDE.md`.)

- The evaluation harness every later stage reuses: same `test_set.csv`, same `RUBRIC.md`, scored with
  `score.py`. Log every experiment in `EXPERIMENTS.md` with the prediction written *before* the run.
- No own `.venv`: uses `../rag-chain/.venv` and `../rag-chain/.env`. Databases live in `../rag-chain/`
  (`pharma_db.json` = app default 400 / 80; other settings are `pharma_db_<size>_<overlap>.json`).
- Grader: `gemini-3.5-flash-lite` (agrees 95% with hand grades). Hand-check every failure and any answer
  built from several chunks — the grader misses claims stitched across chunk boundaries.
- The grader's copy of the rubric has "(Qxx …)" references stripped; keep rubric examples generic so
  they don't give away test answers.
- Never re-chunk by uploading in the Streamlit app twice — it doesn't check for duplicates. Use `add_pdf.py`.
