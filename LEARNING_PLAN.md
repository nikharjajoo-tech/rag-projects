# Learning plan

The roadmap in the [README](README.md) says *what* gets built. This file says what I should *understand*
by the end of each stage, and how I'll check that I do. The tutorials are only starting code; the goal
is to be able to explain each technique, its tradeoffs, and when I'd choose it as a PM.

## The loop for every stage

1. **Concept first, no code (20–30 min).** Plain-language explanation, with examples from real products.
2. **Predict.** Write one line on what I expect the change to do, e.g. "bigger chunks will fix question 7".
3. **Build.** Claude sets up the code; I make the small, meaningful edits myself.
4. **Break it on purpose.** Find the cases where the technique fails.
5. **Measure.** Run the Stage 2 test set and compare against the previous stage's score.
6. **Explain it back.** Write a one-page note in the stage's README, then answer interview-style questions.

## Stages

| # | Stage | Saboo tutorial(s) | Concepts to understand | Experiment | Checkpoint question | Est. time |
|---|---|---|---|---|---|---|
| 1 | Basic RAG | `rag_chain` | Embeddings, chunking, similarity search, top-k, temperature | Skipped: covered by prior project experience | "Is a wrong answer caused by the search or by the model?" | ✅ Done |
| 2 | Measure it | `rag_failure_diagnostics_clinic` + our own test set | Golden test sets, retrieval hit rate, faithful vs. correct answers, model-as-grader and its biases, failure patterns | Grade 10 answers myself, then have the model grade them; check how often we agree | "How would you know your RAG product got better after a launch?" | 6–8 hrs |
| 3 | Citations and "I don't know" | Citation ideas from `knowledge_graph_rag_citations`; mostly our own build | Grounding, source attribution, confidence thresholds, wrong answers vs. refusing answerable questions | Move the refusal threshold; chart wrong answers against unnecessary refusals | "Where do you set the line for a medical assistant vs. a shopping assistant?" | 5–7 hrs |
| 4 | Hybrid search + reranking | `hybrid_search_rag` | Keyword vs. meaning-based search, why embeddings miss exact terms (drug names, IDs), merging result lists, rerankers | Exact-term questions; measure quality and latency with and without each piece | "Is a 10% quality gain worth 800 ms of extra waiting?" | 6–8 hrs |
| 5 | Routing | `rag_database_routing` | Question classification, multiple document sets, misrouting, fallbacks | Add a second document set; measure how often questions reach the right one | "How does a company-wide search tool like Glean handle thousands of sources?" | 5–6 hrs |
| 6 | Corrective RAG | `corrective_rag` | Model grading its own search results, query rewriting, web-search fallback, cost multiplication | Count calls, cost and latency vs. how many failed Stage 2 questions get fixed | "When is 3–5× the cost per question worth paying?" | 7–9 hrs |
| 7 | Agentic RAG | `gemini_agentic_rag`, `agentic_rag_with_reasoning`, `autonomous_rag` | Tool calling, the agent loop (think → act → observe), stopping conditions, why agents are hard to test | Questions needing two searches: fixed pipeline vs. agent | "Why might Perplexity use a fixed pipeline for some questions and an agent for others?" | 7–9 hrs |
| 8 | Beyond text | `vision_rag`, `multimodal_agentic_rag`, `knowledge_graph_rag_citations` | PDF parsing, tables, images, multimodal embeddings, knowledge graphs | Questions whose answer sits in a table or figure in the test PDFs | "When does splitting text into chunks stop working?" | 10+ hrs |
| 9 | Build vs. buy | `rag-as-a-service`, `contextualai_rag_agent`, `rag_agent_cohere` | Managed RAG services (e.g. Gemini File Search, Vertex AI Search), guardrails, user-feedback loops | Run the same test set through a managed service; compare score, cost and build time | One-page build-vs-buy memo for a made-up company | 5–7 hrs |
| ★ | Capstone | — | Pulling it together | One chart of quality, cost and latency across all stages | Portfolio write-up I can walk an interviewer through | 3–4 hrs |

**Total: about 50–70 hours** — roughly 2.5–3 months at 5 hrs/week, or 6–7 weeks at 10 hrs/week.

## Risks to the estimates

- **Stage 8** is the riskiest: image and table libraries often have no builds for Intel Mac + Python 3.14.
- **Stages 4, 6 and 9** each need a new free API key (reranker, web search, managed RAG platform).
- **Stages 6–7** use 3–5× more model calls per question, so test runs hit the Gemini daily cap sooner.
  That cost is part of what those stages measure.

## Skipped tutorials (and why)

- Local-model variants — no local model builds on this machine, and the concepts are the same:
  `llama3.1_local_rag`, `qwen_local_rag`, `deepseek_local_rag_agent`, `local_rag_agent`,
  `local_hybrid_search_rag`, `agentic_rag_embedding_gemma`.
- Model or domain swaps of a concept already covered: `agentic_rag_gpt5`, `agentic_typed_rag_pydanticai`,
  `agentic_rag_math_agent`, `ai_blog_search`.
