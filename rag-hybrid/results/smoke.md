# Run: smoke

Settings: model `gemini-3.5-flash-lite`, chunk size 400 / overlap 80, top-k 5, temperature 1; cited answers checked by `gemini-3.5-flash-lite` (temperature 0); search `hybrid+rerank` (reranker `rerank-v3.5` reads the top 25), database `pharma_db_sentences.json`


---

## Q01 (simple fact)

**Question:** How many review articles met the inclusion criteria in the first search round?

**Expected:** 16 (out of 23 review articles identified)

**App answered:** In the first round of literature search, 16 review articles met the inclusion criteria. [1 Chen p4][2 Chen p4]

**Search:** 1 of 1 expected pages found · 0.8s to search + 0.6s to rerank + 2.0s to answer + 1.3s to verify

**User sees:** In the first round of literature search, 16 review articles met the inclusion criteria. (Chen p4)

**Claim checks:** 1 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p4; [2] Chen p4: **supported**. In the first round of literature search, 16 review articles met the inclusion criteria.  
  *Verifier:* The cited source explicitly states that in the first round of literature search, 16 review articles met the inclusion criteria.

**Retrieved chunks:**


1. *Chen p4, relevance 0.939* ✅ expected page
   > In Figure 1, we summarize the overall search and screening process. Current progress in the literature In the first round of literature search, a total of 23 review articles were identified; among them, 16 met our inclusion criteria.


2. *Chen p4, relevance 0.930* ✅ expected page
   > Current progress in the literature In the first round of literature search, a total of 23 review articles were identified; among them, 16 met our inclusion criteria. Based on these review papers, in Figure 2 Panel 1, we first highlight the key steps in the drug development process and then summarize the identified research topics in each step.


3. *Chen p5, relevance 0.457*
   > Similar to the first round of literature search, we screened all studies on these three topics using keywords related to AI and RWD as detailed in the Methods section. A total of 65 research studies were included after title/abstract and full-text screening. In Table 1, we summarize these studies into subcategories with examples.


4. *Chen p3, relevance 0.375*
   > Following best practice for rapid reviews [18,19], we first restricted our search to identify existing review articles for inclusion. We then manually identified the specific AI and RWD applications described in these reviews.


5. *Chen p3, relevance 0.347*
   > For completeness, we included keywords such as “natural language processing” in the AI keywords, because state-of-the-art models for these NLP tasks are often ML/DL methods. The full search query and the complete list of keywords are in the Supplementary Table S1. Following best practice for rapid reviews [18,19], we first restricted our search to identify existing review articles for inclusion.
