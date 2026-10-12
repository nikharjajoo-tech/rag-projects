# Run: smoke

Settings: model `gemini-3.5-flash-lite`, chunk size 400 / overlap 80, top-k 5, temperature 1; cited answers checked by `gemini-3.5-flash-lite` (temperature 0)


---

## Q01 (simple fact)

**Question:** How many review articles met the inclusion criteria in the first search round?

**Expected:** 16 (out of 23 review articles identified)

**App answered:** A total of 16 review articles met the inclusion criteria in the first round of literature search. [1]

**Search:** 1 of 1 expected pages found · 3.2s to answer + 1.9s to verify

**User sees:** A total of 16 review articles met the inclusion criteria in the first round of literature search. (Chen p4)

**Claim checks:** 1 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p4: **supported**. A total of 16 review articles met the inclusion criteria in the first round of literature search.  
  *Verifier:* The cited source states that among the 23 review articles identified in the first round, 16 met the inclusion criteria.

**Retrieved chunks:**


1. *Chen p4, similarity 0.762* ✅ expected page
   > used. In Figure 1, we summarize the overall search and screening process. Current progress in the literature In the first round of literature search, a total of 23 review articles were identified; among them, 16 met our inclusion criteria. Based on these review papers, in Figure 2 Panel 1, we first highlight the key


2. *Chen p5, similarity 0.746*
   > second round of literature search focusing on individual research studies of these three main applications as shown in Figure 1. Similar to the first round of literature search, we screened all studies on these three topics using keywords related to AI and RWD as detailed in the Methods section. A total of 65


3. *Chen p19, similarity 0.740*
   > 19 Figure 1. The overall search and screening process.


4. *Chen p4, similarity 0.739* ✅ expected page
   > 4 articles for inclusion. We then manually identified the specific AI and RWD applications described in these reviews. Next, based on the identified applications, we performed a second round of literature search to look for their detailed approaches, including data source, data type, and analytical methods used. In Figure 1, we summarize the overall search and screening process.


5. *Chen p3, similarity 0.736*
   > Following best practice for rapid reviews [18,19], we first restricted our search to identify existing review


---

## Q10 (exact term)

**Question:** What is BEHRT and what does it do?

**Expected:** A deep neural sequence transduction model (a Transformer for EHRs) that predicts interpretable personalized risk from EHR data, modelling how records change over time and combining diagnoses, medications and measurements

**App answered:** BEHRT is a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data. [1] BEHRT models the temporal evolution of EHR data through utilizing various forms of sequential data to learn disease subphenotypes and handle irregular time intervals. [1]

**Search:** 1 of 1 expected pages found · 2.2s to answer + 1.8s to verify

**Notes:** Name expanded only in reference 43 on page 15

**User sees:** BEHRT is a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data. (Chen p7) BEHRT models the temporal evolution of EHR data through utilizing various forms of sequential data to learn disease subphenotypes and handle irregular time intervals. (Chen p7)

**Claim checks:** 1 supported, 0 partly, 1 not supported

- Claim 1 → [1] Chen p7: **supported**. BEHRT is a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data.  
  *Verifier:* The cited source states that BEHRT is a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data.
- Claim 2 → [1] Chen p7: **not supported**. BEHRT models the temporal evolution of EHR data through utilizing various forms of sequential data to learn disease subphenotypes and handle irregular time intervals.  
  *Verifier:* The cited source mentions handling irregular time intervals and learning disease subphenotypes separately with reference [42], but does not state that BEHRT itself uses sequential data to learn disease subphenotypes and handle irregular time intervals.

**Retrieved chunks:**


1. *Chen p7, similarity 0.729* ✅ expected page
   > to handle irregular time intervals in longitudinal EHR data [42] to learn disease subphenotypes. BEHRT, a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data, models the temporal evolution of EHR data through utilizing various forms of sequential


2. *Chen p4, similarity 0.651*
   > become an important data source for RCTs to understand how the developed treatments are being used in real-world settings. For example, Lai et al. examined the impact of using EHRs for clinical research recruitment in a review of 13 research articles [21]. They found that the automation in screening and


3. *Chen p15, similarity 0.649*
   > 43. Li, Y., Rao, S., Solares, J. R. A., Hassaine, A., Ramakrishnan, R., Canoy, D., Zhu, Y., Rahimi, K., & Salimi-Khorshidi, G. (2020). BEHRT: Transformer for Electronic Health Records. Scientific Reports, 10(1), 7155. https://doi.org/10.1038/s41598-020-62922-y 44. Wu, Y., Yang, X., Bian, J., Guo, Y., Xu, H., & Hogan, W. (2018). Combine Factual Medical


4. *Chen p23, similarity 0.648*
   > Mining structured EHR data Predictive modeling of structured EHRs for adverse drug event detection [25] Recruitment optimization Electronic recruitment through EHR Electronic recruitment integrated into EHR workflow that sends electronic messages to recruit eligible patients [26,27] Eligible population identification/pre- screening Automated review of EHR to identify


5. *Chen p6, similarity 0.646*
   > in NLP methods, especially those new deep learning-based models with state-of-the-art performance. In fact, over 80% of the clinical information in EHR is documented in free-text [37], which makes text mining an ideal tool. EHRs have been particularly useful for investigating AEs and other therapeutic


---

## Q13 (spread out)

**Question:** Both papers discuss explainable AI (XAI). What role does each assign to it?

**Expected:** Chen: helps interpret why an AI model made a decision (e.g. variable ranking); especially useful for drug repurposing, where hypotheses need plausible explanations. Blanco: a strategy to overcome AI's obstacles: transparent explanations that address bias and fairness concerns and reveal the mechanisms behind predictions

**App answered:** Explainable AI methods aim to provide interpretable and transparent explanations for predictions made by machine learning algorithms. [2] Explainable AI can address concerns about bias and fairness in artificial intelligence-based approaches. [2] Explainable AI provides a better understanding of the underlying mechanisms and assumptions behind predictions. [2] Explainable AI models help us understand why an artificial intelligence system makes a certain decision. [4] Explainable AI models are particularly useful for tasks like drug repurposing where plausible explanations are crucial for generating hypotheses. [4] Explainable artificial intelligence could help to interpret and understand artificial intelligence decisions. [5]

**Search:** 2 of 2 expected pages found · 2.6s to answer + 1.8s to verify

**User sees:** Explainable AI methods aim to provide interpretable and transparent explanations for predictions made by machine learning algorithms. (Blanco p5) Explainable AI can address concerns about bias and fairness in artificial intelligence-based approaches. (Blanco p5) Explainable AI provides a better understanding of the underlying mechanisms and assumptions behind predictions. (Blanco p5) Explainable AI models help us understand why an artificial intelligence system makes a certain decision. (Chen p7) Explainable AI models are particularly useful for tasks like drug repurposing where plausible explanations are crucial for generating hypotheses. (Chen p7) Explainable artificial intelligence could help to interpret and understand artificial intelligence decisions. (Chen p7)

**Claim checks:** 6 supported, 0 partly, 0 not supported

- Claim 1 → [2] Blanco p5: **supported**. Explainable AI methods aim to provide interpretable and transparent explanations for predictions made by machine learning algorithms.  
  *Verifier:* Source [2] states that XAI methods aim to provide interpretable and transparent explanations for predictions made by ML algorithms.
- Claim 2 → [2] Blanco p5: **supported**. Explainable AI can address concerns about bias and fairness in artificial intelligence-based approaches.  
  *Verifier:* Source [2] states that this can help to address concerns about bias and fairness in AI-based approaches.
- Claim 3 → [2] Blanco p5: **supported**. Explainable AI provides a better understanding of the underlying mechanisms and assumptions behind predictions.  
  *Verifier:* Source [2] states that XAI methods provide a better understanding of the underlying mechanisms and assumptions behind the predictions.
- Claim 4 → [4] Chen p7: **supported**. Explainable AI models help us understand why an artificial intelligence system makes a certain decision.  
  *Verifier:* Source [4] states that these methods ultimately help us understand why an AI system makes a certain decision.
- Claim 5 → [4] Chen p7: **supported**. Explainable AI models are particularly useful for tasks like drug repurposing where plausible explanations are crucial for generating hypotheses.  
  *Verifier:* Source [4] states that XAI models are particularly useful for tasks such as drug repurposing because these tasks are generating hypotheses where plausible explanations are crucial.
- Claim 6 → [5] Chen p7: **supported**. Explainable artificial intelligence could help to interpret and understand artificial intelligence decisions.  
  *Verifier:* Source [5] states that the emerging of explainable AI (XAI) could help to interpret and understand AI decisions.

**Retrieved chunks:**


1. *Blanco p10, similarity 0.771*
   > SSCI 2018 1542–1547 (Institute of Electrical and Electronics Engineers Inc., 2019). doi:10.1109/SSCI.2018.8628742. 48. Minh, D., Wang, H. X., Li, Y. F. & Nguyen, T. N. Explainable artificial intelligence: a comprehensive review. Artif. Intell. Rev. 55, 3503–3568 (2022). 49. Barredo Arrieta, A. et al. Explainable Artificial Intelligence (XAI): Concepts,


2. *Blanco p5, similarity 0.757* ✅ expected page
   > explainable AI (XAI) methods 48, which aim to provide interpretable and transparent explanations for the pred ictions made by ML algorithms. This can help to address concerns about bias and fairness in AI -based approaches 43, and provide a better understanding of the underlying mechanisms and assumptions behind the predictions49.


3. *Blanco p10, similarity 0.756*
   > Expertise and Artificial Intelligence. in Expertise at Work 149–175 (Palgrave Macmillan, Cham, 2021). doi:10.1007/978-3-030-64371-3_8. 52. Gilpin, L. H. et al. Explaining explanations: An overview of interpretability of machine learning. in Proceedings - 2018 IEEE 5th International Conference on Data Science and Advanced Analytics, DSAA 2018 80–89 (Institute of Electrical and Electronics


4. *Chen p7, similarity 0.749* ✅ expected page
   > distillation, and rule extraction) on top of ML/DL models to generate interpretable outputs such as variable ranking [50], which ultimately help us understand why an AI system makes a certain decision. XAI models are particular useful for tasks such as drug repurposing because these tasks are generating hypotheses where plausible explanations are crucial.


5. *Chen p7, similarity 0.738* ✅ expected page
   > trial”[49] framework aiming to establish causal treatment effects using RWD without conducting RCTs. Additionally, the emerging of explainable AI (XAI) could help to interpret and understand AI decisions. The XAI models use different mechanisms (e.g., feature interaction and importance, knowledge


---

## Q17 (unanswerable)

**Question:** What F1-score did the best deep-learning NLP model for adverse event detection reach?

**Expected:** Not in the documents. Chen says only that deep-learning NLP reached state-of-the-art performance.

**App answered:** The documents don't answer this. The F1-score reached by the best deep-learning NLP model for adverse event detection is not mentioned in the sources.

**Search:** n/a (unanswerable) found · 2.1s to answer + 0.0s to verify

**Notes:** Expected behaviour: say it doesn't know

**User sees:** The documents don't answer this. The F1-score reached by the best deep-learning NLP model for adverse event detection is not mentioned in the sources.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Chen p5, similarity 0.793*
   > observed a steady increase in the total number of studies. In particular, the number of studies focusing on adverse event detection has exploded and many focused on using NLP methods to extract adverse events from free-text narratives, likely because of advances in DL-based NLP methods that achieved


2. *Chen p4, similarity 0.790*
   > searching to more advanced ML/DL-based natural language processing (NLP) methods, can be powerful in adverse events detection, given that adverse events are more extensively documented in EHR


3. *Chen p5, similarity 0.783*
   > NLP pipeline were further fed into a downstream model to assess association between AEs and other health outcomes. For example, Zhang et al. first used NLP to identify patients who had AE related to statin therapy, and then examined the relationship between continuation of statin therapy and incidence


4. *Chen p6, similarity 0.776*
   > in NLP methods, especially those new deep learning-based models with state-of-the-art performance. In fact, over 80% of the clinical information in EHR is documented in free-text [37], which makes text mining an ideal tool. EHRs have been particularly useful for investigating AEs and other therapeutic


5. *Chen p5, similarity 0.775*
   > identify AEs related to the administration of medication. For example, Yang et al. developed a Long Short-Term Memory (LSTM)-based DL model to detect medication, AEs, and their relations from clinical text[26]. In other studies, the AEs and associated attributes (such as severity) extracted from the
