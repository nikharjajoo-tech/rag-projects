# Answer-chunk ranks: w1.5

28 answerable questions, 40 answer pieces. Rank = position of the first chunk holding the piece; the model sees the top 5. Merging: meaning-based search gets 1.5 vote(s), keyword search 1.

## Summary

| Method | Pieces in top 5 | Questions with every piece in top 5 | Pieces at 6–25 | Pieces beyond 25 | Search time |
|---|---|---|---|---|---|
| hybrid | 30 of 40 | 21 of 28 | 6 | 4 | 0.62s |
| hybrid+rerank | 32 of 40 | 23 of 28 | 4 | 4 | 1.41s |

Search time: the real time of the embedding and rerank calls (saved with the cached results) plus local ranking. Rate-limit waits not counted.

## Per piece

| Question | Piece | hybrid | hybrid+rerank |
|---|---|---|---|
| Q01 | 16 of 23 met the criteria | **1** | **1** |
| Q02 | just 6% correct | **1** | **1** |
| Q03 | no studies for preclinical | 21 | **1** |
| Q04 | searched until July 1 2020 | **1** | **1** |
| Q05 | 41 of 55 (74.5%) | **2** | **1** |
| Q06 | trained in 2021 | 10 | 12 |
| Q07 | target trial framework | 18 | 6 |
| Q08 | over 80% free text | 9 | **1** |
| Q09 | OHDSI expanded | **1** | **1** |
| Q10 | BEHRT described | **1** | **1** |
| Q11 | Xu et al. assessed metformin | **1** | **1** |
| Q11 | finding: decreased mortality | **4** | **2** |
| Q12 | BACE1 and Alzheimer's | **1** | **1** |
| Q13 | Chen: XAI interprets decisions | **2** | **1** |
| Q13 | Chen: XAI for drug repurposing | **4** | **4** |
| Q13 | Blanco: XAI explanations | **1** | **2** |
| Q14 | Chen: data quality | **4** | **4** |
| Q14 | Chen: sharing data is hard | 51 | 51 |
| Q14 | Blanco: low quality or inconsistent data | 11 | 7 |
| Q14 | Blanco: biased training data | **5** | 6 |
| Q15 | 55 on adverse events | **4** | **5** |
| Q15 | 2 on drug repurposing | 31 | 31 |
| Q16 | Chen: external validation | 43 | 43 |
| Q16 | Chen: loop back to clinical studies | 167 | 167 |
| Q16 | Blanco: humans validate | **3** | **1** |
| Q16 | Blanco: check reliable sources | 10 | **3** |
| N01 | Zhang et al. statin study | **1** | **1** |
| N03 | T-LSTM adds elapsed time | **1** | **1** |
| N05 | Blanco: bias and unequal access | **4** | **1** |
| N05 | Blanco: job loss | **3** | **1** |
| N05 | Blanco: privacy and security | **3** | **3** |
| N07 | Spasic et al. NLP system | **1** | **1** |
| E01 | journal and year | **1** | **1** |
| E02 | Ramón y Cajal contract | **1** | **1** |
| E03 | VESPA finding | **1** | **1** |
| E04 | CTSA ACT expanded | **1** | **1** |
| E05 | baseline regularization | **1** | **1** |
| E06 | 48 studies | **1** | **1** |
| E07 | IML expanded | **2** | **1** |
| E08 | what the LSTM detected | **1** | **1** |
