"""Stage 4: Stage 3's pipeline (cited answer + verifier) with a different search in front of it.

Only the search changes; prompt, model, verifier and reports are Stage 3's (run_cited.py), so scores compare
directly. --search picks one of search.py's MODES.

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-hybrid/run_hybrid.py vector --search vector              # Stage 3's search, re-timed
    rag-chain/.venv/bin/python rag-hybrid/run_hybrid.py hybrid_rerank --search hybrid+rerank
    rag-chain/.venv/bin/python rag-hybrid/run_hybrid.py smoke --search hybrid --only Q01,Q09
    rag-chain/.venv/bin/python rag-eval/grade.py rag-hybrid/results/hybrid_rerank gemini-3.5-flash-lite
    python3 rag-citations/score_cited.py rag-hybrid/results/hybrid_rerank

Writes the same three files as run_cited.py to rag-hybrid/results/. Latency is split into search, rerank,
answer and verify; "answer" no longer includes the search, as it did in Stage 3.
"""
import os

from search import HYBRID_DIR, MODES, SCORE_NAMES, POOL, RERANK_MODEL, Searcher
import run_cited


def make_search(args):
    searcher = Searcher(args.db)
    reranker = f" (reranker `{RERANK_MODEL}` reads the top {POOL})" if args.search.endswith("+rerank") else ""
    note = f"search `{args.search}`{reranker}, database `{args.db}`"
    return (lambda question: searcher.search(question, args.search)), note, SCORE_NAMES[args.search]


if __name__ == "__main__":
    run_cited.main(make_search=make_search, results_dir=os.path.join(HYBRID_DIR, "results"),
                   extra_args=lambda parser: parser.add_argument("--search", choices=MODES, default="hybrid+rerank"))
