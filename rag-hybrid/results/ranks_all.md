# Answer-chunk ranks: all

20 answerable questions, 32 answer pieces. Rank = position of the first chunk holding the piece; the model sees the top 5.

## Summary

| Method | Pieces in top 5 | Questions with every piece in top 5 | Pieces at 6–25 | Pieces beyond 25 | Search time |
|---|---|---|---|---|---|
| vector | 25 of 32 | 16 of 20 | 2 | 5 | 0.57s |
| bm25 | 15 of 32 | 10 of 20 | 8 | 9 | 0.00s |
| hybrid | 21 of 32 | 13 of 20 | 6 | 5 | 0.57s |
| vector+rerank | 24 of 32 | 15 of 20 | 3 | 5 | 2.16s |
| hybrid+rerank | 24 of 32 | 15 of 20 | 3 | 5 | 1.44s |

Search time: the real time of the embedding and rerank calls (saved with the cached results) plus local ranking. Rate-limit waits not counted.

## Per piece

| Question | Piece | vector | bm25 | hybrid | vector+rerank | hybrid+rerank |
|---|---|---|---|---|---|---|
| Q01 | 16 of 23 met the criteria | **1** | **1** | **1** | **1** | **1** |
| Q02 | just 6% correct | **1** | **1** | **1** | **1** | **1** |
| Q03 | no studies for preclinical | 47 | **1** | 18 | 47 | **1** |
| Q04 | searched until July 1 2020 | **2** | **1** | **1** | **1** | **1** |
| Q05 | 41 of 55 (74.5%) | **2** | **4** | **2** | **1** | **1** |
| Q06 | trained in 2021 | **1** | 47 | 13 | 13 | 11 |
| Q07 | target trial framework | **2** | 131 | 27 | **4** | 27 |
| Q08 | over 80% free text | **2** | 42 | 11 | **1** | **1** |
| Q09 | OHDSI expanded | **2** | **3** | **1** | **1** | **1** |
| Q10 | BEHRT described | **1** | 6 | **1** | **1** | **1** |
| Q11 | Xu et al. assessed metformin | **1** | **1** | **1** | **1** | **1** |
| Q11 | finding: decreased mortality | **5** | 11 | **4** | **2** | **2** |
| Q12 | BACE1 and Alzheimer's | **1** | **1** | **1** | **1** | **1** |
| Q13 | Chen: XAI interprets decisions | **3** | **1** | **2** | **1** | **1** |
| Q13 | Chen: XAI for drug repurposing | **2** | 12 | **4** | **4** | **4** |
| Q13 | Blanco: XAI explanations | **1** | **2** | **1** | **2** | **2** |
| Q14 | Chen: data quality | 6 | 22 | **4** | **4** | **4** |
| Q14 | Chen: sharing data is hard | 41 | 103 | 63 | 41 | 63 |
| Q14 | Blanco: low quality or inconsistent data | **1** | 86 | 15 | 7 | 7 |
| Q14 | Blanco: biased training data | 10 | 24 | 7 | 6 | 6 |
| Q15 | 55 on adverse events | **2** | 6 | **3** | **5** | **5** |
| Q15 | 2 on drug repurposing | 43 | 28 | 28 | 43 | 28 |
| Q16 | Chen: external validation | 84 | 23 | 34 | 84 | 34 |
| Q16 | Chen: loop back to clinical studies | 112 | 191 | 171 | 112 | 171 |
| Q16 | Blanco: humans validate | **1** | 37 | **5** | **1** | **1** |
| Q16 | Blanco: check reliable sources | **3** | 84 | 14 | **3** | **3** |
| N01 | Zhang et al. statin study | **1** | **1** | **1** | **1** | **1** |
| N03 | T-LSTM adds elapsed time | **1** | **1** | **1** | **1** | **1** |
| N05 | Blanco: bias and unequal access | **2** | 7 | **4** | **1** | **1** |
| N05 | Blanco: job loss | **2** | **1** | **1** | **1** | **1** |
| N05 | Blanco: privacy and security | **3** | **1** | **1** | **3** | **3** |
| N07 | Spasic et al. NLP system | **1** | **1** | **1** | **1** | **1** |
