# RAG Projects — learning series

## Who I am
AI Product Manager / APM aiming for PM roles at Google, Anthropic, OpenAI. Limited coding background —
I'm doing these projects to understand RAG hands-on. Explain things in plain language, tell me *why*
each step matters (especially product tradeoffs: quality vs. cost vs. latency), and don't assume I
know Python conventions. Let me try changes myself where it's educational.

## Repo
GitHub: https://github.com/nikharjajoo-tech/rag-projects (public — portfolio piece, so scan for
secrets before every push; never commit `.env`). One subfolder per project, each with its own
`.venv`, `requirements.txt`, `.env`, README and CLAUDE.md. The root README holds the roadmap table —
update its Status column when a stage is built.

## Approach (decided)
Rebuild each tutorial concept from Shubham Saboo's `awesome-llm-apps/rag_tutorials` on the Gemini
free tier, reusing the same test documents and questions so each technique's effect is measurable.
Skip local-model variants (Ollama/llama.cpp) and model-swap duplicates — same concepts.
Follow `LEARNING_PLAN.md` for each stage: concept first, predict, build, break, measure, explain back.
Stage 1 tuning experiments (chunk size, top-k, temperature) were skipped — I have prior experience with them.

## Machine constraints (apply to every project)
Intel Mac (x86_64), Python 3.14 — no builds of `onnxruntime`, PyTorch, `chromadb`,
`sentence-transformers`, `faiss`, `llama-cpp-python`. Pick pure-Python / API-based alternatives.
Gemini free tier: 100 embedding requests/minute plus a daily cap — design uploads around it.
