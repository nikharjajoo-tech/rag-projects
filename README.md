# Document Retrieval System (RAG Chain)

Ask questions about your own PDFs. The app finds the most relevant passages and has Gemini
answer using only those passages. This is the basic **Retrieval-Augmented Generation (RAG)** pattern
behind tools like NotebookLM and "chat with your files" features.

This is stage 1 of my [RAG learning series](../README.md).

## How it works

```
PDF → extract text → split into chunks → embed each chunk (Gemini) → store vectors
                                                                        │
Question → embed question → find 5 most similar chunks ─────────────────┘
         → put chunks + question into a prompt → Gemini writes the answer
```

| Step | Setting in `app.py` | Tradeoff it controls |
|---|---|---|
| Chunking | `chunk_size=400`, `chunk_overlap=200` (characters) | Precise small chunks vs. context-rich large ones; more chunks = more embedding cost |
| Retrieval | `k=5` | More chunks = better chance of including the answer, but more tokens and more noise |
| Generation | `PROMPT_TEMPLATE`, `temperature=1` | How strictly the model sticks to the retrieved text |

## What I changed from the original tutorial (and why)

Adapted from [`rag_tutorials/rag_chain`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/rag_tutorials/rag_chain)
in Shubham Saboo's [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
(original app by Charan).

- **Runs on an Intel Mac with Python 3.14.** There are no builds of `onnxruntime` or PyTorch for that combination, so
  ChromaDB was replaced with LangChain's `InMemoryVectorStore` (saved to `pharma_db.json`), and the
  SentenceTransformers splitter was replaced with `RecursiveCharacterTextSplitter`.
- **Current models.** The retired `gemini-1.5-pro` / `embedding-001` were replaced with `gemini-3.8-flash` /
  `gemini-embedding-001`.
- **Bug fix.** The sidebar API key never reached the embedding model. The app now uses it, falling back to `.env`.
- **Works on the free tier.** Gemini's free tier allows 100 embedding requests per minute, so a normal PDF
  (about 200–300 chunks) used to crash the upload. Uploads now go in batches, wait out the limit with a
  countdown, save progress after each batch, and stop cleanly when the daily limit is hit. I deliberately did *not*
  increase chunk size to avoid the limit, because chunk size is a quality setting I want to experiment with.
- **Generalised** from pharma-only to any document.

## Run it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "GOOGLE_API_KEY=your-key-here" > .env     # free key: https://aistudio.google.com/apikey
.venv/bin/streamlit run app.py
```

Upload a PDF in the sidebar → **Submit & Process** → ask a question.

## Test document

`test_docs/` contains two open-access arXiv papers. Start with
`Role_of_AI_in_Drug_Discovery_2212.08104.pdf` (11 pages, about 187 chunks, about 2 minutes to upload on the free tier).
Good questions to check against it:

1. Who developed AlphaFold and what does it do?
2. What does the successful use of AI in drug discovery depend on?
3. How was this article written? (It was co-written with ChatGPT as an experiment.)
4. What drug did Insilico Medicine take to clinical trials? (**Not in the paper.** A good app should say it
   doesn't know. A confident answer here is a hallucination.)

## Known limitations (fixed in later stages)

- It doesn't show *which* chunks the answer came from, so you can't tell a retrieval miss from a hallucination.
- It doesn't refuse when the document doesn't contain the answer.
- Meaning-based search can miss exact terms (drug names, codes).
- Tables, charts and scanned pages lose their content when the text is extracted.
