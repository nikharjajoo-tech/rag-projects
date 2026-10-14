# Answer-chunk ranks: baseline

20 answerable questions, 32 answer pieces. Rank = position of the first chunk holding the piece; the model sees the top 5.

## Summary

| Method | Pieces in top 5 | Questions with every piece in top 5 | Pieces at 6–25 | Pieces beyond 25 | Search time |
|---|---|---|---|---|---|
| vector | 25 of 32 | 16 of 20 | 2 | 5 | 0.57s |

Search time: the real time of the embedding and rerank calls (saved with the cached results) plus local ranking. Rate-limit waits not counted.

## Per piece

| Question | Piece | vector |
|---|---|---|
| Q01 | 16 of 23 met the criteria | **1** |
| Q02 | just 6% correct | **1** |
| Q03 | no studies for preclinical | 47 |
| Q04 | searched until July 1 2020 | **2** |
| Q05 | 41 of 55 (74.5%) | **2** |
| Q06 | trained in 2021 | **1** |
| Q07 | target trial framework | **2** |
| Q08 | over 80% free text | **2** |
| Q09 | OHDSI expanded | **2** |
| Q10 | BEHRT described | **1** |
| Q11 | Xu et al. assessed metformin | **1** |
| Q11 | finding: decreased mortality | **5** |
| Q12 | BACE1 and Alzheimer's | **1** |
| Q13 | Chen: XAI interprets decisions | **3** |
| Q13 | Chen: XAI for drug repurposing | **2** |
| Q13 | Blanco: XAI explanations | **1** |
| Q14 | Chen: data quality | 6 |
| Q14 | Chen: sharing data is hard | 41 |
| Q14 | Blanco: low quality or inconsistent data | **1** |
| Q14 | Blanco: biased training data | 10 |
| Q15 | 55 on adverse events | **2** |
| Q15 | 2 on drug repurposing | 43 |
| Q16 | Chen: external validation | 84 |
| Q16 | Chen: loop back to clinical studies | 112 |
| Q16 | Blanco: humans validate | **1** |
| Q16 | Blanco: check reliable sources | **3** |
| N01 | Zhang et al. statin study | **1** |
| N03 | T-LSTM adds elapsed time | **1** |
| N05 | Blanco: bias and unequal access | **2** |
| N05 | Blanco: job loss | **2** |
| N05 | Blanco: privacy and security | **3** |
| N07 | Spasic et al. NLP system | **1** |
