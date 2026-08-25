# Canonical Analysis Outputs Register v1.0

**Purpose:** one authoritative pointer per RQ — which report and dataset a thesis writer (or any future session) should cite, with no ambiguity. Resolves the survey-filename inconsistency raised in this task.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## Survey filename resolution (read this first)

**`Survey_Analysis_Final_v1.1.xlsx` does not exist anywhere in this repository and never has** — confirmed by repository-wide search. It appears only inside this project's own documents as a flagged non-existent reference (first raised in `RQ3_Final_Results_Package_v1.0.md`, prior session).

**The actual authoritative N=24 source is two files, serving two distinct purposes, neither superseding the other:**

| File | Role |
|---|---|
| `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` | **Canonical raw source.** 24 consented Google-Forms responses, one row per respondent. This is where "N=24" comes from. |
| `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` | **Canonical processed/analysis-ready file**, reproducibly derived from the raw file above via `15_Scripts/alcsm_survey_analysis_v1.0.py` — never hand-edited, never a second raw source. **This is the file to cite for every survey statistic used in thesis writing** (relevance/clarity means, appropriateness, most-important-dimension counts). |

No new dataset was invented to resolve this — the fix is a documentation correction (`Document_Version_Policy.md`, updated this session) pointing forward references at the file that actually exists, not a re-derivation or new file.

---

## Canonical register, per RQ

| RQ | Canonical report | Canonical dataset | Sample size | Primary analysis | Main result | Main limitation |
|---|---|---|---|---|---|---|
| **RQ1** | `09_Statistical_Analysis/RQ1/RQ1_Final_Results_v1.0.md` | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` + `05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` | 500 profiles, 3,000 profile×dimension labels | Descriptive statistics: score distributions, missingness, cross-tabulations | D1/D3/D6 span the full 0–5 range; D2/D4 range-restricted; D5 concentrated at score 3 (87%) | Descriptive only — no inferential statistics, no causal claims |
| **RQ2** | `09_Statistical_Analysis/RQ2/RQ2_Final_Results_v1.0.md` | `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` + frozen annotation | 201 postings, 1,558 requirement records | Aggregate dimension-level demand-vs-supply comparison (no numeric gap) | 51.3% of requirements NOT_DIRECTLY_MAPPED; D5 dominates demand; D6 shows the sharpest profile/posting asymmetry (99.4% vs. 0.06%) | No per-requirement numeric required-level score exists; no one-to-one candidate/posting matching |
| **RQ3** | `09_Statistical_Analysis/RQ3/RQ3_Final_Results_Package_v1.0.md` | `07_Reliability/Reliability_Results_v1.1.xlsx` (75-profile subset) + `ALCSM_Survey_Analysis_Processed_v1.0.xlsx` (N=24) | 75 profiles (reliability); N=24 (survey) | Krippendorff's alpha (ordinal, per dimension, never pooled) + descriptive survey statistics | D1/D6 strong reproducibility; D2/D4 perfect but degenerate; D3 limited (α=.102, systematic calibration disagreement); D5 limited (α=.246, range restriction) | One subset, one second rater; N=24 self-selected respondents; content-assessment evidence, not proof of validity |
| **RQ4** | `09_Statistical_Analysis/RQ4/RQ4_Final_Status_v1.0.md` | None — not conducted | 0 | Not conducted | None — documented limitation, not an empirical finding | External criterion data (network reach, engagement, recognition, seniority progression) was never collected |
| **RQ5** | `09_Statistical_Analysis/RQ5/RQ5_NLP_Final_Results_v1.0.md` | `08_NLP_Development/NLP_Baseline_Results_v1.0.xlsx` | 500 profiles, per-dimension train/test splits (seed=42) | TF-IDF + Ridge regression, six independent per-dimension models | D3 strongest signal (52.0% exact, κ=.399); D1 modest signal; D2/D5 tie degenerate/imbalanced baselines; D4/D6 below baseline | Proof-of-concept baseline, not production-ready; linear bag-of-words model cannot represent cross-field aggregation |

## Cross-RQ index

`09_Statistical_Analysis/ALCSM_Final_Results_Summary_v1.0.xlsx` — one sheet per RQ plus a summary sheet, all numbers traceable to the reports above.

`11_Implementation_Governance/Reviews/Final_Thesis_Evidence_Audit_v1.0.md` — full source/denominator/method trace for every number appearing in thesis-ready prose.

---

*No canonical source file modified. This register introduces no new statistic — it is a pointer/index document only.*
