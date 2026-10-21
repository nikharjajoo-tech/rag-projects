# Breaking meaning-based search with near-identical codes

14 made-up chunks added to the 232 real ones: 8 trial entries that differ only in the trial ID's last digit and the patient count, and 6 compounds whose codes reuse the same four digits. Rank = position of the chunk for the code the question names; the model sees the top 5. A wrong chunk in the top 5 is worse than a miss: it holds a plausible, wrong number.

## Summary

| Method | Right chunk ranked 1st | Right chunk in top 5 |
|---|---|---|
| vector | 7 of 7 | 7 of 7 |
| bm25 | 7 of 7 | 7 of 7 |
| hybrid | 7 of 7 | 7 of 7 |
| vector+rerank | 7 of 7 | 7 of 7 |
| hybrid+rerank | 7 of 7 | 7 of 7 |

## Per question

| Code asked about | vector | bm25 | hybrid | vector+rerank | hybrid+rerank |
|---|---|---|---|---|---|
| NCT04512343 | **1** | **1** | **1** | **1** | **1** |
| NCT04512346 | **1** | **1** | **1** | **1** | **1** |
| NCT04512348 | **1** | **1** | **1** | **1** | **1** |
| NCT04512341 | **1** | **1** | **1** | **1** | **1** |
| RX-2014 | **1** | **1** | **1** | **1** | **1** |
| RX-2401 | **1** | **1** | **1** | **1** | **1** |
| RX-4021 | **1** | **1** | **1** | **1** | **1** |
