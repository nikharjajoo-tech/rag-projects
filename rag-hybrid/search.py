"""Stage 4's search pieces: keyword search (BM25), meaning-based search, merging the two, and a reranker.

Five ways to pick the 5 chunks the model answers from (`MODES`):
    vector          meaning-based search, as in Stages 1-3
    bm25            keyword search only
    hybrid          both, merged with reciprocal rank fusion
    vector+rerank   the top 25 by meaning, reordered by Cohere's reranker
    hybrid+rerank   the top 25 of hybrid, reordered by Cohere's reranker

Used by run_hybrid.py (answers) and rank_report.py (where the answer chunk ranks). Question embeddings and
rerank results are saved in cache/ with the time the first call took: reruns spend no quota, and latency is
still the real one.
"""
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter

import httpx
import numpy as np
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

HYBRID_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HYBRID_DIR, "..", "rag-eval"))
sys.path.insert(0, os.path.join(HYBRID_DIR, "..", "rag-citations"))
from run_eval import RAG_CHAIN_DIR, EMBEDDING_MODEL, TOP_K, with_retry  # importing run_eval loads rag-chain/.env
from run_cited import DEFAULT_DB

MODES = ["vector", "bm25", "hybrid", "vector+rerank", "hybrid+rerank"]
SCORE_NAMES = {"vector": "similarity", "bm25": "bm25", "hybrid": "rrf",
               "vector+rerank": "relevance", "hybrid+rerank": "relevance"}

# The knobs. Each one changes which chunks come back; try them.
BM25_K1 = 1.5    # how fast repeats of a word stop counting (0 = once is enough, higher = repeats keep adding)
BM25_B = 0.75    # how much long chunks are penalised (0 = not at all, 1 = fully)
RRF_K = 60       # fusion: higher = the two lists' top ranks matter less (60 is the usual default)
POOL = 25        # candidates the reranker reads: wider finds more, but costs more tokens and time
RERANK_MODEL = "rerank-v3.5"
RERANK_GAP_SECONDS = 6.5  # Cohere's trial allows 10 rerank calls a minute

CACHE_DIR = os.path.join(HYBRID_DIR, "cache")


def tokenize(text):
    """How keyword search splits text into words: lower case, letters and digits only.
    'BACE1' -> 'bace1', 'AI/RWD' -> 'ai', 'rwd', 'COVID-19' -> 'covid', '19'.
    No stemming, so 'study' and 'studies' don't match, and no stop-word list ('the', 'what'):
    BM25 already gives words found in most chunks almost no weight."""
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    """Keyword search. A chunk scores for each question word it contains, weighted by how rare the word
    is across all chunks (OHDSI, in 1 of 232 chunks, counts far more than 'drug', in most of them)."""

    def __init__(self, texts):
        self.word_counts = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(c.values()) for c in self.word_counts]
        self.average_length = sum(self.lengths) / len(self.lengths)
        chunks_with = Counter(word for counts in self.word_counts for word in counts)
        n = len(texts)
        self.rarity = {word: math.log((n - k + 0.5) / (k + 0.5) + 1) for word, k in chunks_with.items()}

    def scores(self, question):
        words = tokenize(question)
        scores = []
        for counts, length in zip(self.word_counts, self.lengths):
            score = 0.0
            for word in words:
                if word in counts:
                    repeats = counts[word]
                    score += self.rarity[word] * repeats * (BM25_K1 + 1) / (
                        repeats + BM25_K1 * (1 - BM25_B + BM25_B * length / self.average_length))
            scores.append(score)
        return scores


def fuse(*rankings):
    """Reciprocal rank fusion: each list votes 1 / (RRF_K + rank) for every chunk in it. Uses positions,
    not scores, because a similarity of 0.68 and a BM25 score of 12.4 aren't on the same scale."""
    votes = Counter()
    for ranking in rankings:
        for rank, (i, _) in enumerate(ranking, 1):
            votes[i] += 1 / (RRF_K + rank)
    return votes.most_common()


class Cache:
    """A JSON file of saved API results."""

    def __init__(self, name):
        self.path = os.path.join(CACHE_DIR, name)
        self.data = json.load(open(self.path)) if os.path.exists(self.path) else {}

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value):
        self.data[key] = value
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f)


class Searcher:
    def __init__(self, db_name=DEFAULT_DB):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
        store = InMemoryVectorStore.load(os.path.join(RAG_CHAIN_DIR, db_name), self.embeddings).store
        self.docs = [Document(id=i, page_content=c["text"], metadata=c["metadata"]) for i, c in store.items()]
        vectors = np.array([c["vector"] for c in store.values()])
        self.vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        self.bm25 = BM25([d.page_content for d in self.docs])
        self.embedding_cache = Cache(f"question_embeddings_{db_name}")
        self.rerank_cache = Cache("rerank.json")
        self.last_rerank = 0.0

    # --- the first stage: rank every chunk ------------------------------------------------------------------

    def vector_ranking(self, question):
        """Every chunk, by cosine similarity to the question (what InMemoryVectorStore does)."""
        saved = self.embedding_cache.get(question)
        if not saved:
            start = time.time()
            vector = with_retry(lambda: self.embeddings.embed_query(question))
            saved = {"vector": vector, "seconds": time.time() - start}
            self.embedding_cache.put(question, saved)
        query = np.array(saved["vector"]) / np.linalg.norm(saved["vector"])
        similarity = self.vectors @ query
        return [(int(i), float(similarity[i])) for i in np.argsort(-similarity)], saved["seconds"]

    def bm25_ranking(self, question):
        scores = self.bm25.scores(question)
        return sorted(enumerate(scores), key=lambda x: -x[1]), 0.0  # runs locally: no API call to time

    def first_stage(self, question, method):
        """(ranking, seconds): every chunk index with its score, best first. Seconds = the embedding call's
        real time (saved with it) plus the time spent ranking here."""
        if method == "bm25":
            start = time.time()
            return self.bm25_ranking(question)[0], time.time() - start
        by_meaning, embed_seconds = self.vector_ranking(question)
        start = time.time()  # after the embedding call, which may have come from the cache
        ranking = by_meaning if method == "vector" else fuse(by_meaning, self.bm25_ranking(question)[0])
        return ranking, embed_seconds + time.time() - start

    # --- the second stage: the reranker ---------------------------------------------------------------------

    def rerank(self, question, ranking):
        """Sends the top POOL chunks to Cohere, which reads the question and each chunk together and scores
        how well the chunk answers it. Returns (the pool, reordered, with relevance scores; seconds)."""
        pool = [i for i, _ in ranking[:POOL]]
        texts = [self.docs[i].page_content for i in pool]
        key = hashlib.sha1("\n".join([RERANK_MODEL, question] + texts).encode()).hexdigest()
        saved = self.rerank_cache.get(key)
        if not saved:
            saved = self._call_cohere(question, texts)
            self.rerank_cache.put(key, saved)
        return [(pool[r["index"]], r["relevance_score"]) for r in saved["results"]], saved["seconds"]

    def _call_cohere(self, question, texts):
        while True:
            pause = RERANK_GAP_SECONDS - (time.time() - self.last_rerank)
            if pause > 0:
                time.sleep(pause)  # rate-limit wait: not counted as latency
            start = time.time()
            response = httpx.post("https://api.cohere.com/v2/rerank", timeout=60,
                                  headers={"Authorization": f"Bearer {os.environ['COHERE_API_KEY']}"},
                                  json={"model": RERANK_MODEL, "query": question, "documents": texts})
            seconds, self.last_rerank = time.time() - start, time.time()
            if response.status_code == 429:
                print("  Cohere per-minute limit; waiting 60s...")
                time.sleep(60)
                continue
            response.raise_for_status()
            return {"results": response.json()["results"], "seconds": seconds}

    # --- what the runner and the rank report call ------------------------------------------------------------

    def ranking(self, question, mode):
        """(every chunk index with its score, best first; timings). With a reranker, the reordered pool
        comes first and the rest of the first stage after it: a chunk ranked beyond POOL can't be rescued."""
        first, search_seconds = self.first_stage(question, mode.removesuffix("+rerank"))
        timings = {"search_seconds": search_seconds}
        if mode.endswith("+rerank"):
            reranked, timings["rerank_seconds"] = self.rerank(question, first)
            first = reranked + first[POOL:]
        return first, timings

    def search(self, question, mode, k=TOP_K):
        """The k chunks the model sees, as (Document, score) pairs, plus timings."""
        ranking, timings = self.ranking(question, mode)
        return [(self.docs[i], score) for i, score in ranking[:k]], timings
