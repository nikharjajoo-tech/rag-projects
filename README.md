# RAG Projects: learning Retrieval-Augmented Generation from basic to advanced

I'm an AI Product Manager building RAG systems hands-on to understand the quality, cost and latency
tradeoffs behind products like NotebookLM, Perplexity and enterprise support assistants.

Each project builds on the one before it and fixes a failure mode of the previous stage. I use the same
documents and test questions throughout, so the effect of each technique can be measured instead of guessed.
The projects are adapted from [Shubham Saboo's awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/rag_tutorials)
and rebuilt to run on the Gemini free tier.

## Roadmap

| # | Stage | What it adds | Product question it answers | Status |
|---|---|---|---|---|
| 1 | [**Basic RAG**](rag-chain/) | Retrieve relevant chunks, then answer from them | What's the simplest thing that works, and where does it fail? | ✅ Built |
| 2 | [**Measure it**](rag-eval/) | Test question set, grading rubric, checked model grader | Did a change actually help? | ✅ Built |
| 3 | Citations and "I don't know" | Source quotes, confidence, refusal threshold | Wrong answers vs. unanswered questions: where's the line? | Planned |
| 4 | Hybrid search and reranking | Keyword + meaning-based search, reranker | Is extra quality worth the extra latency? | Planned |
| 5 | Routing | Send each question to the right knowledge base | How do you scale to many document sets? | Planned |
| 6 | Corrective RAG | Grade retrieved chunks, rewrite the query, fall back to web search | Is 3–5× the model calls worth it? | Planned |
| 7 | Agentic RAG | The model decides when and what to search | Flexibility vs. predictability | Planned |
| 8 | Beyond text | Images, tables, knowledge graphs | When does plain text chunking stop working? | Planned |
| 9 | Build vs. buy | Managed RAG platforms, guardrails, user feedback | Speed of shipping vs. control | Planned |

What I aim to understand at each stage, the experiments and time estimates are in the [learning plan](LEARNING_PLAN.md).

## Repo layout

Each folder is a self-contained project with its own README, `requirements.txt` and virtual environment.
API keys go in a per-project `.env` file, which git ignores.

---
Built by [Nikhar Jajoo](https://www.linkedin.com/in/nikhar-jajoo/)
