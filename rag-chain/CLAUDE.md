# RAG Chain (Document Retrieval System) — stage 1 of the series

(Who I am, repo conventions and machine constraints are in `../CLAUDE.md`.)

## Where this came from
Tutorial `rag_tutorials/rag_chain` from https://github.com/Shubhamsaboo/awesome-llm-apps
(copied in, not cloned).

## Changes from the original tutorial (and why)
This Mac is Intel (x86_64) with Python 3.14, which has no builds of `onnxruntime` or PyTorch. So:
- **Vector DB:** Chroma → LangChain `InMemoryVectorStore`, saved to `pharma_db.json`.
  Do not reintroduce `chromadb`, `sentence-transformers`, `torch`, or `faiss` — they won't install here.
- **Chunking:** SentenceTransformers token splitter → `RecursiveCharacterTextSplitter`
  (`chunk_size=400`, `chunk_overlap=200` characters ≈ the original 100/50 tokens).
- **Models:** `gemini-1.5-pro` / `embedding-001` (retired) → `gemini-3.5-flash-lite` / `models/gemini-embedding-001`.
  Was `gemini-3.8-flash` until 2026-10-06; switched because its free tier allows only 20 requests/day.
  Set via `CHAT_MODEL` / `EMBEDDING_MODEL` constants at the top of `app.py`. Using Gemini free tier.
- **Bug fix:** the sidebar API key never reached the embedding model. Now `get_api_key()` uses the
  sidebar key, falling back to `GOOGLE_API_KEY` in `.env`.
- **Free-tier rate limit:** Gemini free tier allows 100 embedding requests/minute (1 chunk = 1
  request), so normal PDFs failed with 429. Uploads now embed in batches of `EMBED_BATCH_SIZE`,
  wait out the per-minute limit, save after each batch, and stop with a message on the daily limit.
  Chunk size was deliberately NOT changed to work around this — it's an experiment variable.
- **Rebranded:** UI says "Document Retrieval System"; footer credits Nikhar (linkedin.com/in/nikhar-jajoo).
  The answer prompt still says "pharmaceutical sciences" (left as-is, not yet decided).

## How to run (from this `rag-chain/` folder)
```
.venv/bin/streamlit run app.py --server.headless true
```
(`--server.headless true` skips Streamlit's first-run email prompt, which otherwise hangs background runs.)
API key goes in `.env` as `GOOGLE_API_KEY=...` (gitignored — never commit it). Upload a PDF in the
sidebar → "Submit & Process" → ask a question.

## Status / next steps
- [x] Setup done, app launches, API key verified (embeddings + chat both work)
- [ ] First successful question on my own PDF
- [ ] Show the retrieved chunks next to each answer (to see *why* an answer is right/wrong)
- [ ] Experiments: vary `chunk_size`, `chunk_overlap`, `k`, `temperature` (currently 1 — high for a
      grounded Q&A app) and note how answers change
- [ ] Write up learnings as a PM-style note (tradeoffs, failure modes, how I'd evaluate quality)
