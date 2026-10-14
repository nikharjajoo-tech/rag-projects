# Answer-chunk ranks: exact

8 answerable questions, 8 answer pieces. Rank = position of the first chunk holding the piece; the model sees the top 5.

## Summary

| Method | Pieces in top 5 | Questions with every piece in top 5 | Pieces at 6–25 | Pieces beyond 25 | Search time |
|---|---|---|---|---|---|
| vector | 8 of 8 | 8 of 8 | 0 | 0 | 0.73s |
| bm25 | 7 of 8 | 7 of 8 | 1 | 0 | 0.00s |
| hybrid | 8 of 8 | 8 of 8 | 0 | 0 | 0.73s |
| vector+rerank | 8 of 8 | 8 of 8 | 0 | 0 | 1.46s |
| hybrid+rerank | 8 of 8 | 8 of 8 | 0 | 0 | 1.36s |

Search time: the real time of the embedding and rerank calls (saved with the cached results) plus local ranking. Rate-limit waits not counted.

## Per piece

| Question | Piece | vector | bm25 | hybrid | vector+rerank | hybrid+rerank |
|---|---|---|---|---|---|---|
| E01 | journal and year | **1** | **1** | **1** | **1** | **1** |
| E02 | Ramón y Cajal contract | **1** | **1** | **1** | **1** | **1** |
| E03 | VESPA finding | **1** | **1** | **1** | **1** | **1** |
| E04 | CTSA ACT expanded | **1** | **1** | **1** | **1** | **1** |
| E05 | baseline regularization | **1** | **1** | **1** | **1** | **1** |
| E06 | 48 studies | **1** | **1** | **1** | **1** | **1** |
| E07 | IML expanded | **3** | 6 | **2** | **1** | **1** |
| E08 | what the LSTM detected | **1** | **1** | **1** | **1** | **1** |
