# Run: nearmiss_sentences

Settings: model `gemini-3.5-flash-lite`, chunk size 400 / overlap 80, top-k 5, temperature 1; cited answers checked by `gemini-3.5-flash-lite` (temperature 0); database `pharma_db_sentences.json`


---

## N01 (near-miss)

**Question:** What did Zhang et al. do with NLP, and what did they then examine?

**Expected:** They used NLP to identify patients who had adverse events related to statin therapy, then examined the relationship between continuing statin therapy and death and cardiovascular events among these patients

**App answered:** Zhang et al. first used NLP to identify patients who had adverse events related to statin therapy. [1 Chen p5] They then examined the relationship between the continuation of statin therapy and the incidence of death and cardiovascular events among these patients. [1 Chen p5]

**Search:** 1 of 1 expected pages found · 22.0s to answer + 18.2s to verify

**Notes:** Trap: two other Zhangs appear only in the reference list (costs of pivotal trials; time-aware LSTM)

**User sees:** Zhang et al. first used NLP to identify patients who had adverse events related to statin therapy. (Chen p5) They then examined the relationship between the continuation of statin therapy and the incidence of death and cardiovascular events among these patients. (Chen p5)

**Claim checks:** 2 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p5: **supported**. Zhang et al. first used NLP to identify patients who had adverse events related to statin therapy.  
  *Verifier:* The cited text explicitly states that Zhang et al. first used NLP to identify patients who had AE (adverse events) related to statin therapy.
- Claim 2 → [1] Chen p5: **supported**. They then examined the relationship between the continuation of statin therapy and the incidence of death and cardiovascular events among these patients.  
  *Verifier:* The cited text confirms that they then examined the relationship between continuation of statin therapy and incidence of death and cardiovascular events among these patients.

**Retrieved chunks:**


1. *Chen p5, similarity 0.739* ✅ expected page
   > For example, Zhang et al. first used NLP to identify patients who had AE related to statin therapy, and then examined the relationship between continuation of statin therapy and incidence of death and cardiovascular events among these patients [27].


2. *Chen p5, similarity 0.724* ✅ expected page
   > For example, Spasic et al. used an NLP system that combined rule-based knowledge infusion and machine learning algorithms to analyze longitudinal patient records to determine if the corresponding patients met given eligibility criteria for clinical trials [28]. Finally, for the two articles on clinical drug repurposing [29,30], one of them used NLP methods.


3. *Chen p5, similarity 0.712* ✅ expected page
   > Finally, for the two articles on clinical drug repurposing [29,30], one of them used NLP methods. In work by Xu et al., automated informatics methods including NLP were used on EHR data to identify patient cohorts and medication information[29], and they then assessed whether metformin is a potential drug that can be repurposed to cancer treatment.


4. *Chen p5, similarity 0.702* ✅ expected page
   > Overall, we observed a steady increase in the total number of studies. In particular, the number of studies focusing on adverse event detection has exploded and many focused on using NLP methods to extract adverse events from free-text narratives, likely because of advances in DL-based NLP methods that achieved state-of-the-art performance[24].


5. *Chen p4, similarity 0.702*
   > These studies showed that text-mining techniques, ranging from simple free-text searching to more advanced ML/DL-based natural language processing (NLP) methods, can be powerful in adverse events detection, given that adverse events are more extensively documented in EHR narratives.


---

## N02 (unanswerable)

**Question:** What is the average cost in US dollars of bringing one new drug to market?

**Expected:** Not in the documents. Chen says only that a new drug typically costs billions of U.S. dollars and more than 10 years of work.

**App answered:** It is estimated that bringing a new drug to the market typically costs billions of U.S. Dollars. [1 Chen p2] Not in the documents: The sources do not provide a specific average numerical cost in U.S. dollars.

**Search:** n/a (unanswerable) found · 45.3s to answer + 18.4s to verify

**Notes:** Trap: a vague 'billions of dollars' answer is acceptable; any specific figure is made up

**User sees:** It is estimated that bringing a new drug to the market typically costs billions of U.S. Dollars. (Chen p2) Not in the documents: The sources do not provide a specific average numerical cost in U.S. dollars.

**Claim checks:** 1 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p2: **supported**. It is estimated that bringing a new drug to the market typically costs billions of U.S. Dollars.  
  *Verifier:* The cited source explicitly states that bringing every new drug to the market typically costs billions of U.S. Dollars.

**Retrieved chunks:**


1. *Chen p2, similarity 0.758*
   > During the drug development process, chemical entities that have the potential to become therapeutic agents will have to be identified and thoroughly tested, and the entire process is lengthy and costly. It is estimated that for every new drug brought to the market, it typically costs billions of U.S. Dollars and more than 10 years of work [3,4].


2. *Chen p2, similarity 0.750*
   > Dollars and more than 10 years of work [3,4]. Therefore, strategies that can facilitate and accelerate the drug development process are of high interest. Recently, the FDA has been actively promoting the use of real-world data (RWD) for drug development [5,6].


3. *Chen p2, similarity 0.703*
   > We discussed current research gaps and future opportunities. Introduction Drug development is the process of bringing a new drug molecule into clinical practice; in its broadest definition, it includes all stages from the basic research of finding a suitable molecular target to large- scale Phase III clinical studies that support the commercial launch of the drug to post-market pharmacosurveillance and drug repurposing studies [1,2].


4. *Chen p4, similarity 0.681*
   > There are three phases of clinical studies before the drug can be submitted for marketing approval. The key issue that needs to be addressed in this step is to evaluate both the safety and efficacy of the new agents in the target human population [20].


5. *Blanco p2, similarity 0.679*
   > Drug discovery, the process of identifying and developing new medications, is a complex and time - consuming endeavor that traditionally relies on labor -intensive techniques such as trial -and- error experimentation and high-throughput screening.


---

## N03 (near-miss)

**Question:** What does time-aware LSTM (T-LSTM) add to a standard LSTM, and why?

**Expected:** It incorporates elapsed time information into the standard LSTM architecture, to handle irregular time intervals in longitudinal EHR data (to learn disease subphenotypes)

**App answered:** Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture. [1 Chen p7] This addition is used to handle irregular time intervals in longitudinal electronic health record (EHR) data. [1 Chen p7] T-LSTM handles these irregular time intervals in order to learn disease subphenotypes. [1 Chen p7]

**Search:** 1 of 1 expected pages found · 21.7s to answer + 17.6s to verify

**Notes:** Trap: the next sentence describes BEHRT; claims stitched across the two are wrong

**User sees:** Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture. (Chen p7) This addition is used to handle irregular time intervals in longitudinal electronic health record (EHR) data. (Chen p7) T-LSTM handles these irregular time intervals in order to learn disease subphenotypes. (Chen p7)

**Claim checks:** 3 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p7: **supported**. Time-aware LSTM (T-LSTM) incorporates elapsed time information into the standard LSTM architecture.  
  *Verifier:* The cited text explicitly states that time-aware LSTM incorporates elapsed time information into the standard LSTM architecture.
- Claim 2 → [1] Chen p7: **supported**. This addition is used to handle irregular time intervals in longitudinal electronic health record (EHR) data.  
  *Verifier:* The cited text confirms that this architecture is used to handle irregular time intervals in longitudinal EHR data.
- Claim 3 → [1] Chen p7: **supported**. T-LSTM handles these irregular time intervals in order to learn disease subphenotypes.  
  *Verifier:* The cited text directly states that handling these irregular time intervals is done to learn disease subphenotypes.

**Retrieved chunks:**


1. *Chen p7, similarity 0.788* ✅ expected page
   > For example, time-aware LSTM (T-LSTM) incorporate elapsed time information into the standard LSTM architecture to handle irregular time intervals in longitudinal EHR data [42] to learn disease subphenotypes.


2. *Chen p7, similarity 0.695* ✅ expected page
   > Other developments in deep learning include the ability to handle not only the temporal order of clinical events but also the long- term dependencies among the event as well as the time-varying effects of the covariates.


3. *Chen p7, similarity 0.651* ✅ expected page
   > Li et al. developed a deep learning model based on recurrent neural networks to learn representation and temporal dynamics of longitudinal cognitive measures of individual subjects and combined them with baseline hippocampal Magnetic Resonance Imaging (MRI) measures to build a prognostic model of Alzheimer’s disease dementia progression [41].


4. *Chen p7, similarity 0.645* ✅ expected page
   > BEHRT, a new deep neural sequence transduction model for prediction of interpretable personalized risk using EHR data, models the temporal evolution of EHR data through utilizing various forms of sequential concepts and enabled the ability of incorporating multiple heterogeneous concepts (e.g., diagnosis, medication, measurements, and more) to further improve the accuracy of its predictions [43].


5. *Chen p5, similarity 0.645*
   > For example, Yang et al. developed a Long Short-Term Memory (LSTM)-based DL model to detect medication, AEs, and their relations from clinical text[26]. In other studies, the AEs and associated attributes (such as severity) extracted from the NLP pipeline were further fed into a downstream model to assess association between AEs and other health outcomes.


---

## N04 (unanswerable)

**Question:** By what percentage did AI shorten the time to find COVID-19 drug candidates?

**Expected:** Not in the documents. Blanco says only that AI found promising candidates in a fraction of the time traditional methods take.

**App answered:** The documents don't answer this. The sources do not mention the exact percentage by which AI shortened the time to find COVID-19 drug candidates.

**Search:** n/a (unanswerable) found · 15.0s to answer + 0.0s to verify

**Notes:** Trap: 'a fraction of the time' is acceptable; any percentage is made up

**User sees:** The documents don't answer this. The sources do not mention the exact percentage by which AI shortened the time to find COVID-19 drug candidates.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Blanco p4, similarity 0.807*
   > In some cases, these AI -powered approaches have been able to identify promising drug candidates in a fraction of the time it would take traditional methods26–31. Many more examples are available 3,32–37, showing that AI -based methods can accelerate the drug discovery process and enable the development of more effective medications. 6.


2. *Blanco p4, similarity 0.791*
   > ML algorithms have been used to analyze large datasets of potential compounds and identify those with the most potential for treating the virus. In some cases, these AI -powered approaches have been able to identify promising drug candidates in a fraction of the time it would take traditional methods26–31.


3. *Blanco p2, similarity 0.778*
   > However, AI techniques such as machine learning (ML) and natural language processing offer the potential to accelerate and improve this process by enabling more efficient and accurate analysis of large amounts of dat a4. The successful use of deep learning (DL) to predict the efficacy of drug compounds with high accuracy has been recently describe d5.


4. *Blanco p2, similarity 0.768*
   > The successful use of deep learning (DL) to predict the efficacy of drug compounds with high accuracy has been recently describe d5. AI-based methods have also been able to predict the toxicity of drug candidates6. These and other research efforts have highlighted the capacity of AI to improve the efficiency and effectiveness of drug discovery processes.


5. *Blanco p4, similarity 0.765*
   > The use of AI in the discovery of drugs to combat COVID -19 has been a promising area of research during the last two years . ML algorithms have been used to analyze large datasets of potential compounds and identify those with the most potential for treating the virus.


---

## N05 (near-miss)

**Question:** What ethical concerns does the Blanco paper raise about AI in the pharmaceutical industry?

**Expected:** AI making decisions that affect people's health (which drugs to develop, which trials to run, how to market drugs); bias in algorithms leading to unequal access and unfair treatment; job loss from automation; data privacy and security of sensitive medical data

**App answered:** The use of AI raises concerns about potential bias in algorithms. [2 Blanco p6] Algorithm bias could cause unequal access to medical treatment and unfair treatment of certain groups. [2 Blanco p6] The automation of AI in the pharmaceutical industry raises concerns about job loss. [2 Blanco p6] The use of AI raises questions regarding data privacy and security. [3 Blanco p6] Sensitive personal information risks being accessed or misused due to reliance on large amounts of data. [3 Blanco p6]

**Search:** 1 of 1 expected pages found · 20.2s to answer + 31.2s to verify

**Notes:** Trap: Chen p6 mentions ethical and legal issues of data sharing, which is the wrong paper. Blanco p5 also mentions fairness and bias

**User sees:** The use of AI raises concerns about potential bias in algorithms. (Blanco p6) Algorithm bias could cause unequal access to medical treatment and unfair treatment of certain groups. (Blanco p6) The automation of AI in the pharmaceutical industry raises concerns about job loss. (Blanco p6) The use of AI raises questions regarding data privacy and security. (Blanco p6) Sensitive personal information risks being accessed or misused due to reliance on large amounts of data. (Blanco p6)

**Claim checks:** 5 supported, 0 partly, 0 not supported

- Claim 1 → [2] Blanco p6: **supported**. The use of AI raises concerns about potential bias in algorithms.  
  *Verifier:* The cited text explicitly states that a key concern is the potential for bias in AI algorithms.
- Claim 2 → [2] Blanco p6: **supported**. Algorithm bias could cause unequal access to medical treatment and unfair treatment of certain groups.  
  *Verifier:* The cited text states that bias in AI algorithms could result in unequal access to medical treatment and unfair treatment of certain groups of people.
- Claim 3 → [2] Blanco p6: **supported**. The automation of AI in the pharmaceutical industry raises concerns about job loss.  
  *Verifier:* The cited text states that the use of AI in the pharmaceutical industry raises concerns about job loss due to automation.
- Claim 4 → [3] Blanco p6: **supported**. The use of AI raises questions regarding data privacy and security.  
  *Verifier:* The cited text states that the use of AI in the pharmaceutical industry raises questions about data privacy and security.
- Claim 5 → [3] Blanco p6: **supported**. Sensitive personal information risks being accessed or misused due to reliance on large amounts of data.  
  *Verifier:* The cited text states that because AI systems rely on large amounts of data, there is a risk that sensitive personal information could be accessed or misused.

**Retrieved chunks:**


1. *Blanco p6, similarity 0.810* ✅ expected page
   > Overall, the ethical use of AI in the pharmaceutical industry requires careful consideration and thoughtful approaches to addressing these concerns. This can include measures such as ensuring that AI systems are trained on diverse and representative data, regularly reviewing and auditing AI systems for bias, and implementing strong data privacy and security protocols.


2. *Blanco p6, similarity 0.806* ✅ expected page
   > Another key concern is the potential for bias in AI algorithms, which could result in unequal access to medical treatment and unfair treatment of certain groups of people. This could undermine the principles of equality and justice. The use of AI in the pharmaceutical industry also raises concerns about job loss due to automation.


3. *Blanco p6, similarity 0.796* ✅ expected page
   > Additionally, the use of AI in the pharmaceutical industry raises questions about data privacy and security. As AI systems rely on large amounts of data to function, there is a risk that sensitive personal information could be accessed or misused. This could have serious consequences for individuals, as well as for the reputation of the companies involved.


4. *Blanco p6, similarity 0.791* ✅ expected page
   > The collection and use of sensitive medical data must be done in a way that respects individuals' privacy and complies with relevant regulations. Overall, the ethical use of AI in the pharmaceutical industry requires careful consideration and thoughtful approaches to addressing these concerns.


5. *Blanco p6, similarity 0.790* ✅ expected page
   > By addressing these issues, the pharmaceutical industry can use AI in a respons ible and ethical manner. 9.


---

## N06 (unanswerable)

**Question:** What is the name of the broad-spectrum antibiotic the ML approach discovered?

**Expected:** Not in the documents. Blanco says an ML approach found powerful antibiotics in over 100 million molecules, including one that works against a wide range of bacteria, but doesn't name it.

**App answered:** The documents don't answer this. The sources do not mention the specific name of the broad-spectrum antibiotic discovered by the ML approach.

**Search:** n/a (unanswerable) found · 15.1s to answer + 0.0s to verify

**Notes:** Trap: the model may know the real name (halicin) from its training; naming it is not from the documents

**User sees:** The documents don't answer this. The sources do not mention the specific name of the broad-spectrum antibiotic discovered by the ML approach.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Blanco p4, similarity 0.781*
   > AI has also been successfully applied in the discovery of new antibiotics 24. A pioneering ML approach has identified powerful types of antibiotic from a pool of more than 100 million molecules, including one that works against a wide range of bacteria, such as tuberculosis and untreatable strains25.


2. *Blanco p4, similarity 0.757*
   > Another example is the identification of novel inhibitors of beta-secretase (BACE1), a protein involved in the development of Alzheimer's disease 23 by using a ML algorithm. AI has also been successfully applied in the discovery of new antibiotics 24.


3. *Blanco p3, similarity 0.737*
   > AI techniques such as ML are able to overcome these limitations. Based on the analysis of a large amount of information, ML algorithms can identify patterns and trends that may not be apparent to human researchers. This can enable the proposal of new bioactive compounds with minimum side effects much faster than using classical protocols.


4. *Blanco p2, similarity 0.729*
   > However, AI techniques such as machine learning (ML) and natural language processing offer the potential to accelerate and improve this process by enabling more efficient and accurate analysis of large amounts of dat a4. The successful use of deep learning (DL) to predict the efficacy of drug compounds with high accuracy has been recently describe d5.


5. *Blanco p4, similarity 0.729*
   > As an output, novel compounds with high potential for cancer treatment were obtained, demonstrating the ability of this method to discover new therapeutic candidates. The use of ML to identify small molecule inhibitors of the protein MEK 22 has been recently described . MEK is also a target for the treatment of cancer, but the development of effective inhibitors has been challenging.


---

## N07 (near-miss)

**Question:** How did Spasic et al. determine whether patients met trial eligibility criteria?

**Expected:** An NLP system combining rule-based knowledge infusion and machine learning algorithms analyzed longitudinal patient records

**App answered:** Spasic et al. used an NLP system to analyze longitudinal patient records. [1 Chen p5] The NLP system combined rule-based knowledge infusion and machine learning algorithms. [1 Chen p5] This system was used to determine if patients met given eligibility criteria for clinical trials. [1 Chen p5]

**Search:** 1 of 1 expected pages found · 13.8s to answer + 23.1s to verify

**Notes:** Reference 28 (p12) gives the title only: 'Text Mining Approach'

**User sees:** Spasic et al. used an NLP system to analyze longitudinal patient records. (Chen p5) The NLP system combined rule-based knowledge infusion and machine learning algorithms. (Chen p5) This system was used to determine if patients met given eligibility criteria for clinical trials. (Chen p5)

**Claim checks:** 3 supported, 0 partly, 0 not supported

- Claim 1 → [1] Chen p5: **supported**. Spasic et al. used an NLP system to analyze longitudinal patient records.  
  *Verifier:* The cited source states that Spasic et al. used an NLP system to analyze longitudinal patient records.
- Claim 2 → [1] Chen p5: **supported**. The NLP system combined rule-based knowledge infusion and machine learning algorithms.  
  *Verifier:* The cited source explicitly mentions that the NLP system combined rule-based knowledge infusion and machine learning algorithms.
- Claim 3 → [1] Chen p5: **supported**. This system was used to determine if patients met given eligibility criteria for clinical trials.  
  *Verifier:* The cited source confirms the system was used to determine if patients met given eligibility criteria for clinical trials.

**Retrieved chunks:**


1. *Chen p5, similarity 0.708* ✅ expected page
   > For example, Spasic et al. used an NLP system that combined rule-based knowledge infusion and machine learning algorithms to analyze longitudinal patient records to determine if the corresponding patients met given eligibility criteria for clinical trials [28]. Finally, for the two articles on clinical drug repurposing [29,30], one of them used NLP methods.


2. *Chen p5, similarity 0.675* ✅ expected page
   > Meanwhile, the majority of studies (75% of studies included) on recruitment optimization also utilized clinical notes from EHR data, and attempted to identify eligible populations for trials using information extracted from NLP.


3. *Chen p23, similarity 0.675*
   > into EHR workflow that sends electronic messages to recruit eligible patients [26,27] Eligible population identification/pre- screening Automated review of EHR to identify eligible population using NLP [28] Clinical drug repurposing Comparison between diabetic and non- diabetic cancer patients showed that the use of metformin was associated with decreased mortality after cancer diagnosis [29] NLP: natural language process; EHR: electronic health record


4. *Chen p4, similarity 0.663*
   > They found that the automation in screening and patient identification could contribute to higher recruitment yield and reduced workload. After a drug is available on the market, the drug developers are required to submit regular reports detailing adverse events (AEs) associated with the drug [14].


5. *Chen p4, similarity 0.657*
   > For example, Lai et al. examined the impact of using EHRs for clinical research recruitment in a review of 13 research articles [21]. They found that the automation in screening and patient identification could contribute to higher recruitment yield and reduced workload.


---

## N08 (unanswerable)

**Question:** Up to what date did the second-round search for individual research studies run?

**Expected:** Not in the documents. Chen gives a date (July 1, 2020) only for the first-round search for review articles.

**App answered:** The documents don't answer this. The sources do not mention up to what date the second-round search for individual research studies ran.

**Search:** n/a (unanswerable) found · 20.5s to answer + 0.0s to verify

**Notes:** Trap: reusing July 1, 2020, the first-round date

**User sees:** The documents don't answer this. The sources do not mention up to what date the second-round search for individual research studies ran.

**Claim checks:** no claims (refused)


**Retrieved chunks:**


1. *Chen p5, similarity 0.741*
   > Therefore, we conducted a second round of literature search focusing on individual research studies of these three main applications as shown in Figure 1. Similar to the first round of literature search, we screened all studies on these three topics using keywords related to AI and RWD as detailed in the Methods section.


2. *Chen p4, similarity 0.703*
   > In Figure 1, we summarize the overall search and screening process. Current progress in the literature In the first round of literature search, a total of 23 review articles were identified; among them, 16 met our inclusion criteria.


3. *Chen p5, similarity 0.699*
   > Three main types of study used AI on RWD (Figure 2 Panel 3): trial recruitment optimization, adverse events detection, and drug repurposing. Therefore, we conducted a second round of literature search focusing on individual research studies of these three main applications as shown in Figure 1.


4. *Chen p3, similarity 0.678*
   > As a rapid review, we first focused on identifying existing review articles. Search strategy and study selection We performed a literature search through PubMed to identify relevant review articles published until July 1, 2020. In our search strategy, we considered different combinations of search keywords dictated by the definitions of RWD, AI, and drug development that we chose to focus on.


5. *Chen p4, similarity 0.677*
   > In a more recent review conducted by Luo et al. in 2017 on the same topic, a total of 48 studies were identified [23].
