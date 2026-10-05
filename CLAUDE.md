# RAG Chain (PharmaQuery) — learning project

## Who I am
AI Product Manager / APM aiming for PM roles at Google, Anthropic, OpenAI. Limited coding background —
I'm doing this project to understand RAG hands-on. Explain things in plain language, tell me *why*
each step matters (especially product tradeoffs: quality vs. cost vs. latency), and don't assume I
know Python conventions. Let me try changes myself where it's educational.

## Where this came from
Tutorial `rag_tutorials/rag_chain` from https://github.com/Shubhamsaboo/awesome-llm-apps
(copied in, not cloned — this repo has its own local git history, no remote yet).

## Changes from the original tutorial (and why)
This Mac is Intel (x86_64) with Python 3.14, which has no builds of `onnxruntime` or PyTorch. So:
- **Vector DB:** Chroma → LangChain `InMemoryVectorStore`, saved to `pharma_db.json`.
  Do not reintroduce `chromadb`, `sentence-transformers`, `torch`, or `faiss` — they won't install here.
- **Chunking:** SentenceTransformers token splitter → `RecursiveCharacterTextSplitter`
  (`chunk_size=400`, `chunk_overlap=200` characters ≈ the original 100/50 tokens).
- **Models:** `gemini-1.5-pro` / `embedding-001` (retired) → `gemini-3.8-flash` / `models/gemini-embedding-001`.
  Set via `CHAT_MODEL` / `EMBEDDING_MODEL` constants at the top of `app.py`. Using Gemini free tier.
- **Bug fix:** the sidebar API key never reached the embedding model. Now `get_api_key()` uses the
  sidebar key, falling back to `GOOGLE_API_KEY` in `.env`.

## How to run
```
.venv/bin/streamlit run app.py
```
API key goes in `.env` as `GOOGLE_API_KEY=...` (gitignored — never commit it). Upload a PDF in the
sidebar → "Submit & Process" → ask a question.

## The pipeline (where to look in app.py)
PDF → `PyPDFLoader` → split into chunks → embed with Gemini → store in vector DB →
on a question, retrieve top `k=5` similar chunks → stuff into prompt → Gemini answers.

## Status / next steps
- [x] Setup done, app launches (not yet tested end-to-end with a real API key)
- [ ] First successful question on my own PDF
- [ ] Show the retrieved chunks next to each answer (to see *why* an answer is right/wrong)
- [ ] Experiments: vary `chunk_size`, `chunk_overlap`, `k`, `temperature` (currently 1 — high for a
      grounded Q&A app) and note how answers change
- [ ] Write up learnings as a PM-style note (tradeoffs, failure modes, how I'd evaluate quality)
