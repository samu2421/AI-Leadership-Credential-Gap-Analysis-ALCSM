# Abstract (Draft v1.0)

*Draft. Every figure below is reproduced from the final RQ results documents; no new computation.*

---

This thesis investigates observable credential signals of AI leadership through an NLP-assisted audit of 500 LinkedIn profiles, evaluated against 201 job postings and 1,558 extracted requirement records. Credential signals were operationalized through the AI Leadership Credential Scoring Model (ALCSM), a six-dimensional formative index (D1: Formal Education, D2: Professional Certifications, D3: Practical AI Experience, D4: Technical Contributions, D5: Leadership & Strategic Responsibility, D6: AI Industry/Application Breadth) applied to each profile as six independent, non-interchangeable 0–5 ordinal scores rather than a single composite score.

ALCSM's measurement properties were assessed through two complementary lines of evidence: content-assessment feedback from 24 consented domain-expert survey respondents, and inter-rater reliability (Krippendorff's alpha, ordinal) from an independently double-coded 75-profile subset. Results were dimension-dependent rather than uniform: D1 and D6 showed strong, non-degenerate reproducibility (α = .944 and α = 1.000); D2 and D4 reached perfect agreement on degenerate, near-zero-variance samples; D3 showed limited reliability (α = .102) traced to a systematic rater-calibration disagreement around cumulative AI-experience duration; and D5 showed limited reliability (α = .246) attributable primarily to range restriction in the scored population, with a residual, identifiable disagreement around seniority-title versus explicit strategic-scope language.

A gap analysis comparing job-posting requirements against profile-held credential signals found that just under half of extracted requirement text (48.7%) mapped to an ALCSM dimension, with demand concentrated in D5 and D3, and a marked profile-supply-versus-posting-demand asymmetry for D6 (99.4% profile-side coverage versus 0.06% posting-side coverage). A planned criterion-validity analysis against external professional-impact indicators (RQ4) could not be conducted, as the necessary criterion data were not collected within this project's scope, and is reported as an open limitation rather than an estimated result.

Finally, a minimal, fully local, reproducible NLP baseline (TF-IDF features with ridge regression, six independently trained per-dimension models) was evaluated against the human-coded gold standard as a proof-of-concept for automated ALCSM scoring, not a production system. Performance varied by dimension: D3 showed the strongest genuine signal (52.0% exact agreement, weighted κ = .399) despite having the weakest human inter-rater reliability, while D4 and D6 underperformed a majority-class baseline.

This thesis does not claim ALCSM is fully validated. It reports content-assessment evidence, inter-rater reliability evidence, and measurement-reproducibility findings as complementary, dimension-specific evidence for a formative credential-signal framework, together with the main limitations bounding that evidence: a single reliability subset and second rater, a self-selected expert-survey sample, the absence of external criterion data for RQ4, and a deliberately minimal NLP baseline rather than a state-of-the-art model.

---

*Sources: `RQ1_Final_Results_v1.0.md` through `RQ5_NLP_Final_Results_v1.0.md`, `ALCSM_Final_Results_Summary_v1.0.xlsx`.*
