# Run: nearmiss_stage2

Settings: model `gemini-3.5-flash-lite`, chunk size 400 / overlap 80, top-k 5, temperature 1; cited answers checked by `gemini-3.5-flash-lite` (temperature 0); database `pharma_db.json`


---

## N01 (near-miss)

**Question:** What did Zhang et al. do with NLP, and what did they then examine?

**Expected:** They used NLP to identify patients who had adverse events related to statin therapy, then examined the relationship between continuing statin therapy and death and cardiovascular events among these patients

**App answered:** Zhang et al. used NLP to identify patients who had an adverse event related to statin therapy. [1 Chen p5] They then examined the relationship between the continuation of statin therapy and incidence. [1 Chen p5]

**Search:** 1 of 1 expected pages found · 23.9s to answer + 20.0s to verify

**Notes:** Trap: two other Zhangs appear only in the reference list (costs of pivotal trials; time-aware LSTM)

**User sees:** Zhang et al. used NLP to identify patients who had an adverse event related to statin therapy. (Chen p5) They then examined the relationship between the continuation of statin therapy and incidence. (Chen p5)

**Claim checks:** 1 supported, 1 partly, 0 not supported

- Claim 1 → [1] Chen p5: **supported**. Zhang et al. used NLP to identify patients who had an adverse event related to statin therapy.  
  *Verifier:* The cited source explicitly states that Zhang et al. used NLP to identify patients who had an adverse event related to statin therapy.
- Claim 2 → [1] Chen p5: **partly**. They then examined the relationship between the continuation of statin therapy and incidence.  
  *Verifier:* The cited source states they examined the relationship between continuation of statin therapy and incidence, but does not explicitly mention incidence of what.

**Retrieved chunks:**


1. *Chen p5, similarity 0.766* ✅ expected page
   > NLP pipeline were further fed into a downstream model to assess association between AEs and other health outcomes. For example, Zhang et al. first used NLP to identify patients who had AE related to statin therapy, and then examined the relationship between continuation of statin therapy and incidence


2. *Chen p5, similarity 0.723* ✅ expected page
   > source, especially unstructured clinical notes. Consequently, a large number of studies have focused on developing or using NLP methods. Among the 55 studies on AE detection, 41 (74.5%) of them were NLP-related. Some studies developed a NLP system to extract information from clinical notes to


3. *Chen p5, similarity 0.719* ✅ expected page
   > observed a steady increase in the total number of studies. In particular, the number of studies focusing on adverse event detection has exploded and many focused on using NLP methods to extract adverse events from free-text narratives, likely because of advances in DL-based NLP methods that achieved


4. *Chen p5, similarity 0.718* ✅ expected page
   > one of them used NLP methods. In work by Xu et al., automated informatics methods including NLP were used on EHR data to identify patient cohorts and medication information[29], and they then assessed whether metformin is a potential drug that can be repurposed to cancer treatment. In the other clinical


5. *Chen p4, similarity 0.710*
   > searching to more advanced ML/DL-based natural language processing (NLP) methods, can be powerful in adverse events detection, given that adverse events are more extensively documented in EHR


---

## N02 (unanswerable)

**Question:** What is the average cost in US dollars of bringing one new drug to market?

**Expected:** Not in the documents. Chen says only that a new drug typically costs billions of U.S. dollars and more than 10 years of work.

**App answered:** Bringing every new drug to the market is estimated to typically cost billions of U.S. Dollars. [1 Chen p2] Not in the documents: The sources do not state the exact average cost in numerical figures.

**Search:** n/a (unanswerable) found · 8.2s to answer + 20.3s to verify

**Notes:** Trap: a vague 'billions of dollars' answer is acceptable; any specific figure is made up

**User sees:** Bringing every new drug to the market is estimated to typically cost billions of U.S. Dollars. (Chen p2) Not in the documents: The sources do not state the exact average cost in numerical figures.

**Claim checks:** 1 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p2: **supported**. Bringing every new drug to the market is estimated to typically cost billions of U.S. Dollars.  
  *Verifier:* The cited source states that for every new drug brought to the market, it typically costs billions of U.S. Dollars.

**Retrieved chunks:**


1. *Chen p2, similarity 0.770*
   > thoroughly tested, and the entire process is lengthy and costly. It is estimated that for every new drug brought to the market, it typically costs billions of U.S. Dollars and more than 10 years of work [3,4]. Therefore, strategies that can facilitate and accelerate the drug development process are of high interest.


2. *Chen p9, similarity 0.712*
   > 4. Moore, T. J., Zhang, H., Anderson, G., & Alexander, G. C. (2018). Estimated Costs of Pivotal Trials for Novel Therapeutic Agents Approved by the US Food and Drug Administration, 2015-2016. JAMA Internal Medicine, 178(11), 1451–1457. https://doi.org/10.1001/jamainternmed.2018.3931 5. Health, C. for D. and R. (2019, August 27). Use of Real-World Evidence to Support Regulatory


3. *Chen p9, similarity 0.704*
   > Repository Only! https://doi.org/10.1016/B978-0-323-09138-1.00049-8 3. Paul, S. M., Mytelka, D. S., Dunwiddie, C. T., Persinger, C. C., Munos, B. H., Lindborg, S. R., & Schacht, A. L. (2010). How to improve R&D productivity: The pharmaceutical industry’s grand challenge. Nature Reviews. Drug Discovery, 9(3), 203–214. https://doi.org/10.1038/nrd3078


4. *Chen p2, similarity 0.701*
   > scale Phase III clinical studies that support the commercial launch of the drug to post-market pharmacosurveillance and drug repurposing studies [1,2]. During the drug development process, chemical entities that have the potential to become therapeutic agents will have to be identified and


5. *Chen p18, similarity 0.688*
   > drug development. Supplement Supplement Table S1. Search query and the complete list of keywords of literature search


---

## N03 (near-miss)

**Question:** What does time-aware LSTM (T-LSTM) add to a standard LSTM, and why?

**Expected:** It incorporates elapsed time information into the standard LSTM architecture, to handle irregular time intervals in longitudinal EHR data (to learn disease subphenotypes)

**App answered:** Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture. [1 Chen p7] Not in the documents: The sources do not explain why T-LSTM adds elapsed time information to a standard LSTM.

**Search:** 1 of 1 expected pages found · 20.5s to answer + 18.8s to verify

**Notes:** Trap: the next sentence describes BEHRT; claims stitched across the two are wrong

**User sees:** Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture. (Chen p7) Not in the documents: The sources do not explain why T-LSTM adds elapsed time information to a standard LSTM.

**Claim checks:** 1 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p7: **supported**. Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture.  
  *Verifier:* The cited source explicitly states that time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture.

**Retrieved chunks:**


1. *Chen p7, similarity 0.788* ✅ expected page
   > learning include the ability to handle not only the temporal order of clinical events but also the long- term dependencies among the event as well as the time-varying effects of the covariates. For example, time-aware LSTM (T-LSTM) incorporate elapsed time information into the standard LSTM architecture


2. *Chen p15, similarity 0.675*
   > https://doi.org/10.1109/ISBI.2019.8759397 42. Baytas, I. M., Xiao, C., Zhang, X., Wang, F., Jain, A. K., & Zhou, J. (2017). Patient Subtyping via Time-Aware LSTM Networks. Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 65–74. https://doi.org/10.1145/3097983.3097997


3. *Chen p7, similarity 0.661* ✅ expected page
   > to handle irregular time intervals in longitudinal EHR data [42] to learn disease subphenotypes. BEHRT, a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data, models the temporal evolution of EHR data through utilizing various forms of sequential


4. *Chen p7, similarity 0.645* ✅ expected page
   > 7 coherent model. Li et al. developed a deep learning model based on recurrent neural networks to learn representation and temporal dynamics of longitudinal cognitive measures of individual subjects and combined them with baseline hippocampal Magnetic Resonance Imaging (MRI) measures to build a prognostic model of Alzheimer’s disease dementia progression [41]. Other developments in deep


5. *Chen p7, similarity 0.644* ✅ expected page
   > concepts and enabled the ability of incorporating multiple heterogeneous concepts (e.g., diagnosis, medication, measurements, and more) to further improve the accuracy of its predictions [43]. In NLP, new methods have been developed that can incorporate factual medical knowledge from existing ontologies/knowledge bases (e.g., the Unified Medical Language System) to further improve the


---

## N04 (unanswerable)

**Question:** By what percentage did AI shorten the time to find COVID-19 drug candidates?

**Expected:** Not in the documents. Blanco says only that AI found promising candidates in a fraction of the time traditional methods take.

**App answered:** The documents don't answer this. The sources do not mention the percentage by which AI shortened the time to find COVID-19 drug candidates.

**Search:** n/a (unanswerable) found · 19.5s to answer + 0.0s to verify

**Notes:** Trap: 'a fraction of the time' is acceptable; any percentage is made up

**User sees:** The documents don't answer this. The sources do not mention the percentage by which AI shortened the time to find COVID-19 drug candidates.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Blanco p2, similarity 0.763*
   > successful use of deep learning (DL) to predict the efficacy of drug compounds with high accuracy has been recently describe d5. AI-based methods have also been able to predict the toxicity of drug candidates6. These and other research efforts have highlighted the capacity of AI to improve the efficiency and effectiveness of drug discovery processes. However, the use


2. *Blanco p2, similarity 0.760*
   > consuming endeavor that traditionally relies on labor -intensive techniques such as trial -and- error experimentation and high-throughput screening. However, AI techniques such as machine learning (ML) and natural language processing offer the potential to accelerate and improve this process by enabling more efficient and accurate analysis of large amounts of dat a4. The


3. *Blanco p4, similarity 0.759*
   > of existing compounds, which can be a slow and labor-intensive process. AI-based approaches, on the other hand, can enable the rapid and efficient design of novel compounds with desired properties and activities. For example, a deep learning (DL) algorithm has been recently trained on a dataset of known drug compounds and their corresponding properties to propose new


4. *Blanco p4, similarity 0.755*
   > strains25. The use of AI in the discovery of drugs to combat COVID -19 has been a promising area of research during the last two years . ML algorithms have been used to analyze large datasets of potential compounds and identify those with the most potential for treating the virus. In some cases, these AI -powered approaches have been able to identify promising drug


5. *Blanco p4, similarity 0.755*
   > candidates in a fraction of the time it would take traditional methods26–31.


---

## N05 (near-miss)

**Question:** What ethical concerns does the Blanco paper raise about AI in the pharmaceutical industry?

**Expected:** AI making decisions that affect people's health (which drugs to develop, which trials to run, how to market drugs); bias in algorithms leading to unequal access and unfair treatment; job loss from automation; data privacy and security of sensitive medical data

**App answered:** The use of AI raises concerns about job loss due to automation. [1 Blanco p6] AI may be used to make decisions that affect people's health and well-being, including drug development, clinical trials, and drug marketing and distribution. [3 Blanco p6] There is a potential for bias in AI algorithms that could cause unequal access to medical treatment and unfair treatment of certain groups. [1 Blanco p6][3 Blanco p6]

**Search:** 1 of 1 expected pages found · 14.8s to answer + 19.5s to verify

**Notes:** Trap: Chen p6 mentions ethical and legal issues of data sharing, which is the wrong paper. Blanco p5 also mentions fairness and bias

**User sees:** The use of AI raises concerns about job loss due to automation. (Blanco p6) AI may be used to make decisions that affect people's health and well-being, including drug development, clinical trials, and drug marketing and distribution. (Blanco p6) There is a potential for bias in AI algorithms that could cause unequal access to medical treatment and unfair treatment of certain groups. (Blanco p6)

**Claim checks:** 3 supported, 0 partly, 0 not supported

- Claim 1 → [1] Blanco p6: **supported**. The use of AI raises concerns about job loss due to automation.  
  *Verifier:* The cited source explicitly states that the use of AI in the pharmaceutical industry raises concerns about job loss due to automation.
- Claim 2 → [3] Blanco p6: **supported**. AI may be used to make decisions that affect people's health and well-being, including drug development, clinical trials, and drug marketing and distribution.  
  *Verifier:* The cited source states that AI has the potential to be used to make decisions affecting health and well-being, specifically mentioning drug development, clinical trials, and drug marketing and distribution.
- Claim 3 → [1] Blanco p6; [3] Blanco p6: **supported**. There is a potential for bias in AI algorithms that could cause unequal access to medical treatment and unfair treatment of certain groups.  
  *Verifier:* The cited sources mention both the potential for bias in AI algorithms resulting in unequal access to medical treatment and the unfair treatment of certain groups of people.

**Retrieved chunks:**


1. *Blanco p6, similarity 0.804* ✅ expected page
   > treatment of certain groups of people. This could undermine the principles of equality and justice. The use of AI in the pharmaceutical industry also raises concerns about job loss due to automation. It is important to consider the potential impact on workers and provide support for those who may be affected. Additionally, the use of AI in the pharmaceutical industry raises


2. *Blanco p6, similarity 0.797* ✅ expected page
   > individuals' privacy and complies with relevant regulations. Overall, the ethical use of AI in the pharmaceutical industry requires careful consideration and thoughtful approaches to addressing these concerns. This can include measures such as ensuring that AI systems are trained on diverse and representative data, regularly reviewing and auditing


3. *Blanco p6, similarity 0.778* ✅ expected page
   > in this field55,56. One key issue is the potential for AI to be used to make decisions that affect people's health and well-being, such as decisions about which drugs to develop, which clinical trials to conduct, and how to market and distribute drugs. Another key concern is the potential for bias in AI algorithms, which could result in unequal access to medical treatment and unfair


4. *Blanco p6, similarity 0.753* ✅ expected page
   > expertise and experience of human researchers 53, it is possible to optimize the drug discovery process and accelerate the development of new medications54. 8. Ethical considerations in the use of AI in the pharmaceutical industry As said in the previous section, i t is important to consider the ethical implications of using AI


5. *Blanco p1, similarity 0.747*
   > The Role of AI in Drug Discovery: Challenges, Opportunities, and Strategies Alexandre Blanco-González1,2,3, Alfonso Cabezón1,2, Alejandro Seco-González1,2, Daniel Conde-Torres1,2, Paula Antelo-Riveiro1,2, Ángel Piñeiro2*, Rebeca Garcia-Fandino1* 1Department of Organic Chemistry, Center for Research in Biological Chemistry and Molecular


---

## N06 (unanswerable)

**Question:** What is the name of the broad-spectrum antibiotic the ML approach discovered?

**Expected:** Not in the documents. Blanco says an ML approach found powerful antibiotics in over 100 million molecules, including one that works against a wide range of bacteria, but doesn't name it.

**App answered:** The documents don't answer this. The sources do not mention the specific name of the broad-spectrum antibiotic discovered by the ML approach.

**Search:** n/a (unanswerable) found · 13.6s to answer + 0.0s to verify

**Notes:** Trap: the model may know the real name (halicin) from its training; naming it is not from the documents

**User sees:** The documents don't answer this. The sources do not mention the specific name of the broad-spectrum antibiotic discovered by the ML approach.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Blanco p9, similarity 0.769*
   > Divers. 26, 1501–1517 (2022). 24. Melo, M. C. R., Maasch, J. R. M. A. & de la Fuente-Nunez, C. Accelerating antibiotic discovery through artificial intelligence. Communications Biology vol. 4 1–13 (2021). 25. Marchant, J. Powerful antibiotics discovered using AI. Nature (2020) doi:10.1038/d41586-020-00018-3.


2. *Blanco p4, similarity 0.754*
   > in the development of Alzheimer's disease 23 by using a ML algorithm. AI has also been successfully applied in the discovery of new antibiotics 24. A pioneering ML approach has identified powerful types of antibiotic from a pool of more than 100 million molecules, including one that works against a wide range of bacteria, such as tuberculosis and untreatable


3. *Blanco p4, similarity 0.733*
   > strains25. The use of AI in the discovery of drugs to combat COVID -19 has been a promising area of research during the last two years . ML algorithms have been used to analyze large datasets of potential compounds and identify those with the most potential for treating the virus. In some cases, these AI -powered approaches have been able to identify promising drug


4. *Blanco p4, similarity 0.733*
   > been recently reported by Gupta, R. et al.21. These authors trained a DL algorithm on a large dataset of known cancer-related compounds and their corresponding biological activity. As an output, novel compounds with high potential for cancer treatment were obtained, demonstrating the ability of this method to discover new therapeutic candidates. The use of ML to identify


5. *Blanco p4, similarity 0.731*
   > small molecule inhibitors of the protein MEK 22 has been recently described . MEK is also a target for the treatment of cancer, but the development of effective inhibitors has been challenging. The ML algorithm was able to identify novel inhibitors for this protein. Another example is the identification of novel inhibitors of beta-secretase (BACE1), a protein involved


---

## N07 (near-miss)

**Question:** How did Spasic et al. determine whether patients met trial eligibility criteria?

**Expected:** An NLP system combining rule-based knowledge infusion and machine learning algorithms analyzed longitudinal patient records

**App answered:** Spasic et al. used an NLP system to analyze longitudinal patient records. [1 Chen p5] The NLP system combined rule-based knowledge infusion and machine learning algorithms. [1 Chen p5]

**Search:** 1 of 1 expected pages found · 16.8s to answer + 23.5s to verify

**Notes:** Reference 28 (p12) gives the title only: 'Text Mining Approach'

**User sees:** Spasic et al. used an NLP system to analyze longitudinal patient records. (Chen p5) The NLP system combined rule-based knowledge infusion and machine learning algorithms. (Chen p5)

**Claim checks:** 2 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p5: **supported**. Spasic et al. used an NLP system to analyze longitudinal patient records.  
  *Verifier:* The cited source states that Spasic et al. used an NLP system to analyze longitudinal patient records.
- Claim 2 → [1] Chen p5: **supported**. The NLP system combined rule-based knowledge infusion and machine learning algorithms.  
  *Verifier:* The cited source states that the NLP system combined rule-based knowledge infusion and machine learning algorithms.

**Retrieved chunks:**


1. *Chen p5, similarity 0.742* ✅ expected page
   > Spasic et al. used an NLP system that combined rule-based knowledge infusion and machine learning algorithms to analyze longitudinal patient records to determine if the corresponding patients met given eligibility criteria for clinical trials [28]. Finally, for the two articles on clinical drug repurposing [29,30],


2. *Chen p5, similarity 0.686* ✅ expected page
   > of death and cardiovascular events among these patients [27]. Meanwhile, the majority of studies (75% of studies included) on recruitment optimization also utilized clinical notes from EHR data, and attempted to identify eligible populations for trials using information extracted from NLP. For example,


3. *Chen p23, similarity 0.673*
   > Mining structured EHR data Predictive modeling of structured EHRs for adverse drug event detection [25] Recruitment optimization Electronic recruitment through EHR Electronic recruitment integrated into EHR workflow that sends electronic messages to recruit eligible patients [26,27] Eligible population identification/pre- screening Automated review of EHR to identify


4. *Chen p3, similarity 0.673*
   > Eligibility criteria The inclusion criteria for our review were: (1) studies using RWD as data sources; (2) studies using AI methods for statistical analysis or data mining; and (3) studies focused on the development of drugs. As a rapid review, we first focused on identifying existing review articles. Search strategy and study selection


5. *Chen p4, similarity 0.667*
   > patient identification could contribute to higher recruitment yield and reduced workload. After a drug is available on the market, the drug developers are required to submit regular reports detailing adverse events (AEs) associated with the drug [14]. In addition to AE reporting, observational


---

## N08 (unanswerable)

**Question:** Up to what date did the second-round search for individual research studies run?

**Expected:** Not in the documents. Chen gives a date (July 1, 2020) only for the first-round search for review articles.

**App answered:** The documents don't answer this. The sources do not state the date up to which the second-round search ran.

**Search:** n/a (unanswerable) found · 17.7s to answer + 0.0s to verify

**Notes:** Trap: reusing July 1, 2020, the first-round date

**User sees:** The documents don't answer this. The sources do not state the date up to which the second-round search ran.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Chen p5, similarity 0.747*
   > second round of literature search focusing on individual research studies of these three main applications as shown in Figure 1. Similar to the first round of literature search, we screened all studies on these three topics using keywords related to AI and RWD as detailed in the Methods section. A total of 65


2. *Chen p4, similarity 0.707*
   > 4 articles for inclusion. We then manually identified the specific AI and RWD applications described in these reviews. Next, based on the identified applications, we performed a second round of literature search to look for their detailed approaches, including data source, data type, and analytical methods used. In Figure 1, we summarize the overall search and screening process.


3. *Chen p4, similarity 0.706*
   > used. In Figure 1, we summarize the overall search and screening process. Current progress in the literature In the first round of literature search, a total of 23 review articles were identified; among them, 16 met our inclusion criteria. Based on these review papers, in Figure 2 Panel 1, we first highlight the key


4. *Chen p19, similarity 0.704*
   > 19 Figure 1. The overall search and screening process.


5. *Chen p3, similarity 0.697*
   > Following best practice for rapid reviews [18,19], we first restricted our search to identify existing review
