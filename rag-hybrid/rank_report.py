"""Where does the chunk holding each answer rank, for each search method? No chat-model calls.

Each answerable question has one or more answer pieces in answer_chunks.csv: a phrase that only the chunk(s)
holding that piece contain. A piece's rank is the position of the first chunk containing its phrase.
    rank 1-5    the model sees it
    rank 6-25   missed, but inside the reranker's pool: reranking could rescue it
    rank > 25   only a better first stage can find it

Usage (from the rag-projects folder):
    rag-chain/.venv/bin/python rag-hybrid/rank_report.py baseline --modes vector
    rag-chain/.venv/bin/python rag-hybrid/rank_report.py all                    # all five methods
    rag-chain/.venv/bin/python rag-hybrid/rank_report.py w2 --modes hybrid --vector-weight 2
    rag-chain/.venv/bin/python rag-hybrid/rank_report.py pool50 --modes vector+rerank,hybrid+rerank --pool 50

The first run of a question embeds it (1 Gemini embedding call); reranking costs 1 Cohere call per question
per rerank method. Both are cached in rag-hybrid/cache/. Writes results/ranks_<name>.md and .csv.
"""
import argparse
import csv
import os
from collections import defaultdict

from search import HYBRID_DIR, MODES, Searcher
from run_eval import EVAL_DIR, TOP_K

TEST_SETS = [os.path.join(EVAL_DIR, "test_set.csv"), os.path.join(HYBRID_DIR, "..", "rag-citations", "test_set_nearmiss.csv"),
             os.path.join(HYBRID_DIR, "test_set_exact.csv")]


def squash(text):
    return " ".join(text.split())


def bucket(rank, pool):
    return "top 5" if rank <= TOP_K else f"6-{pool}" if rank <= pool else f">{pool}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--modes", default=",".join(MODES), help=f"comma-separated, from: {', '.join(MODES)}")
    parser.add_argument("--only", help="comma-separated question ids")
    parser.add_argument("--pool", type=int, help="candidates the reranker reads (default: search.py's POOL)")
    parser.add_argument("--vector-weight", type=float, help="votes for meaning-based search when merging (default: search.py's VECTOR_WEIGHT)")
    args = parser.parse_args()
    modes = args.modes.split(",")

    questions = {row["id"]: row for path in TEST_SETS for row in csv.DictReader(open(path))}
    pieces = defaultdict(list)
    for row in csv.DictReader(open(os.path.join(HYBRID_DIR, "answer_chunks.csv"))):
        pieces[row["id"]].append(row)
    if args.only:
        pieces = {q: p for q, p in pieces.items() if q in args.only.split(",")}

    searcher = Searcher()
    if args.vector_weight is not None:
        searcher.vector_weight = args.vector_weight
    if args.pool is not None:
        searcher.pool = args.pool
    pool = searcher.pool
    texts = [squash(d.page_content) for d in searcher.docs]
    for rows in pieces.values():  # every phrase must find its chunk, or the ranks below mean nothing
        for p in rows:
            if not any(p["phrase"] in t for t in texts):
                raise SystemExit(f"{p['id']}: no chunk contains {p['phrase']!r}")

    table, seconds = [], defaultdict(list)
    for qid, rows in pieces.items():
        question = questions[qid]
        for mode in modes:
            ranking, timings = searcher.ranking(question["question"], mode)
            seconds[mode].append(sum(timings.values()))
            order = [texts[i] for i, _ in ranking]
            for p in rows:
                rank = next(r for r, t in enumerate(order, 1) if p["phrase"] in t)
                table.append({"id": qid, "question_type": question["question_type"], "piece": p["piece"],
                              "mode": mode, "rank": rank, "bucket": bucket(rank, pool)})
        print(f"{qid}: " + "  ".join(f"{m} " + ",".join(str(t["rank"]) for t in table if t["id"] == qid and t["mode"] == m)
                                     for m in modes))

    report = [f"# Answer-chunk ranks: {args.name}\n",
              f"{len(pieces)} answerable questions, {sum(len(r) for r in pieces.values())} answer pieces. "
              f"Rank = position of the first chunk holding the piece; the model sees the top {TOP_K}. "
              f"Merging: meaning-based search gets {searcher.vector_weight:g} vote(s), keyword search 1. "
              f"The reranker reads the top {pool}.\n",
              "## Summary\n",
              f"| Method | Pieces in top {TOP_K} | Questions with every piece in top {TOP_K} | Pieces at 6–{pool} | Pieces beyond {pool} | Search time |",
              "|---|---|---|---|---|---|"]
    for mode in modes:
        rows = [t for t in table if t["mode"] == mode]
        whole = sum(all(t["rank"] <= TOP_K for t in rows if t["id"] == q) for q in pieces)
        count = lambda b: sum(t["bucket"] == b for t in rows)
        report.append(f"| {mode} | {count('top 5')} of {len(rows)} | {whole} of {len(pieces)} | {count(f'6-{pool}')} | "
                      f"{count(f'>{pool}')} | {sum(seconds[mode]) / len(seconds[mode]):.2f}s |")
    report += ["\nSearch time: the real time of the embedding and rerank calls (saved with the cached results) plus "
               "local ranking. Rate-limit waits not counted.\n", "## Per piece\n",
               "| Question | Piece | " + " | ".join(modes) + " |", "|---|---|" + "---|" * len(modes)]
    for qid, rows in pieces.items():
        for p in rows:
            ranks = [next(t["rank"] for t in table if t["id"] == qid and t["mode"] == m and t["piece"] == p["piece"]) for m in modes]
            report.append(f"| {qid} | {p['piece']} | " + " | ".join(f"**{r}**" if r <= TOP_K else str(r) for r in ranks) + " |")

    results_dir = os.path.join(HYBRID_DIR, "results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, f"ranks_{args.name}.md"), "w") as f:
        f.write("\n".join(report) + "\n")
    with open(os.path.join(results_dir, f"ranks_{args.name}.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        writer.writeheader()
        writer.writerows(table)
    print(f"\nSaved results/ranks_{args.name}.md and .csv in rag-hybrid/")


if __name__ == "__main__":
    main()
