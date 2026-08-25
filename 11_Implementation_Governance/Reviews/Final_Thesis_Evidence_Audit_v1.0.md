# Final Thesis Evidence Audit v1.0

**Purpose:** every numerical result appearing anywhere in the thesis-ready prose (`10_Thesis_Writing/Abstract_Draft_v1.0.md`, `Results_Chapter_Draft_v1.0.md`, `Discussion_Chapter_Draft_v1.0.md`, `Conclusion_Draft_v1.0.md`) traced to its exact source file, sheet/table, denominator, and analysis method. Interpretive statements (read from a number, not directly measured) are flagged separately in §6.
**Author:** Samiksha Dhere (researcher) — audited with Claude Code assistance

---

## 1. Dataset overview figures

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| 500 LinkedIn profiles | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` | `Profile_Scores` (row count) | 500 unique `Profile_ID` | Direct count, `Final_Annotation_Audit_v1.1.md` |
| 3,000 profile × dimension labels | same file | `Dimension_Evidence` (row count) | 500 profiles × 6 dimensions | Direct count |
| 201 job postings | `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` | `Job_Master` (row count) | 201 unique `Job_ID` | Direct count |
| 1,558 requirement records | same file | `Requirements` (row count) | 1,558 rows | Direct count |
| N=24 expert survey respondents | `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` | `Form responses 1` | 24 rows, all consent=="Yes, I agree to participate" | Direct count, `alcsm.analysis.survey.reshape_survey_responses` |
| 75-profile reliability subset | `07_Reliability/Double_Coding/ALCSM_Reliability_Subset_75_v1.1.xlsx` | `Subset_Roster` | 75 unique `Profile_ID` | Deterministic seeded selection (seed=20260824), `Reliability_Subset_Verification_v1.2.md` Part A |

## 2. RQ1 — dimension score distributions and missingness

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| D1 mean 2.28, median 3, range 0–5 | `09_Statistical_Analysis/RQ1/Tables/Table1_Dimension_Score_Distribution.csv` | Table 1 | n=500 | `alcsm.analysis.rq1_descriptive.dimension_distribution`, `D1_Final` column, `Missing_Status` not filtered (population-wide) |
| D2 mean 0.47, median 0, range 0–1 | same | same | n=500 | same method |
| D3 mean 2.93, median 3, range 0–4 | same | same | n=500 | same method |
| D4 mean 0.95, median 0, range 0–3 | same | same | n=500 | same method |
| D5 mean 2.91, median 3 | same | same | n=500 | same method |
| D5: 87.0% of profiles at score 3 | derived from Table 1 (435/500) | Table 1, score=3 row | n=500 | Direct division, 435/500 = 0.870 |
| D6 mean 1.77, median 2, range 0–5 | Table 1 | same | n=500 | same method |
| D1 missingness 5.8% (29/500) | `Table2_Missingness_By_Dimension.csv` | Table 2 | n=500 | `alcsm.analysis.rq1_descriptive.dimension_missingness`, `Dimension_Evidence.Missing_Status` |
| D2 missingness 53.2% (266/500) | same | same | n=500 | same |
| D3 missingness 0.6% (3/500) | same | same | n=500 | same |
| D4 missingness 65.0% (325/500) | same | same | n=500 | same |
| D5 missingness 0.0% (0/500) | same | same | n=500 | same |
| D6 missingness 0.6% (3/500) | same | same | n=500 | same |

## 3. RQ2 — requirement volume and gap comparison

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| 51.3% NOT_DIRECTLY_MAPPED (799/1558) | `09_Statistical_Analysis/RQ2/Tables/Table1_Requirement_Counts_By_Dimension.csv` | Table 1 | n=1,558 | `alcsm.analysis.gap.not_directly_mapped_report`, `Requirements.Final_ALCSM_Dimension` |
| D5: 436 requirements (28.0%) | same | same | n=1,558 | `alcsm.analysis.gap.requirement_counts_by_dimension` |
| D3: 185 requirements (11.9%) | same | same | n=1,558 | same |
| D1: 116 requirements (7.4%) | same | same | n=1,558 | same |
| D2: 17 requirements (1.1%) | same | same | n=1,558 | same |
| D4: 4 requirements (0.3%) | same | same | n=1,558 | same |
| D6: 1 requirement (0.06%) | same | same | n=1,558 | same |
| D6 profile-side coverage 99.4% (497/500) | `Table6_D6_Profile_vs_Posting_Asymmetry.csv` | Table 6 | n=500 profiles | `alcsm.analysis.gap.d6_profile_vs_posting_asymmetry` |
| D6 posting-side coverage 0.06% (1/1558) | same | same | n=1,558 requirements | same |
| 48.7% of requirements mapped (Abstract) | derived | — | 100% − 51.3% | Direct arithmetic complement of the NOT_DIRECTLY_MAPPED figure above |

## 4. RQ3 — inter-rater reliability

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| D1 α=.944, n=72, agreement 81.9% | `07_Reliability/Reliability_Results_v1.1.xlsx` | `Per_Dimension_Reliability` | 72 dually-scored, non-unavailable profile pairs (of 75) | `alcsm.reliability.krippendorff.compute_reliability_result` (ordinal), reused via `alcsm.analysis.rq3_validation.inter_rater_reliability` |
| D2 α=1.000, n=27, agreement 100% | same | same | 27 (of 75; 48 unavailable in this subset) | same |
| D3 α=.102, n=75, agreement 54.7% | same | same | 75 (0 unavailable in this subset) | same |
| D4 α=1.000, n=26, agreement 100% | same | same | 26 (of 75; 49 unavailable) | same |
| D5 α=.246, n=75, agreement 85.3% | same | same | 75 (0 unavailable) | same |
| D6 α=1.000, n=75, agreement 100% | same | same | 75 (0 unavailable) | same |
| D3 3→4 boundary = 18 of 34 disagreements (52.9%) | `07_Reliability/D3_D5_Disagreement_Analysis_v1.0.xlsx` | `Profile_Level_Disagreement`, filtered Rater_A=3 & Rater_B=4 | 34 total D3 disagreements | Direct count, `RQ3_Reliability_Final_Interpretation_v1.0.md` §3 |
| D3 disagreement is 100% one-directional (Rater B always higher) | same | same | 34 disagreements, 0 counter-examples | Direct count of `Direction` column |
| D5: Rater A concentrated 68/75 at one score (90.7%) | `Reliability_Results_v1.1.xlsx` | `Per_Dimension_Reliability`, `rater_a_distribution` JSON field | 75 | Direct count from score-distribution JSON `{"2": 7, "3": 68}` |
| D5 exact agreement 85.3% vs. α=.246 | same | same | 75 | Contrast cited to illustrate range-restriction effect, not a separate statistic |

## 5. RQ3 — expert survey

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| N=24 consented respondents | `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` | `Overview` | 24 of 24 raw rows | `alcsm.analysis.survey.reshape_survey_responses` |
| Relevance means (D1–D6: 3.54, 3.25, 4.33, 3.54, 3.63, 3.67) | same | `Relevance` | 24 respondents per dimension | `alcsm.analysis.rq3_validation.content_validity_summary` |
| D3 highest relevance (4.33) | same | same | 24 | Direct comparison across the six means above |
| Overall appropriateness mean 3.42 | same | `Overall_Appropriateness` | 24 | same method |
| Most-important: D3 = 9 of 24 (37.5%) | same | `Most_Important_Dimension` | 24 | Direct count and division |
| Distinctiveness 0% response rate | same | `Distinctiveness` sheet, `n_answered` column = 0 for all D1–D6 | 24 | Direct count |

## 6. RQ4

| Statistic | Source file | Denominator | Method |
|---|---|---|---|
| 0 criterion variables available | `09_Statistical_Analysis/RQ4/RQ4_Limitation_Report_v1.0.md` §2 | n/a | Exhaustive search of every processed data source and the database; none of the four `rq4_impact_indicator` columns found in any form |

## 7. RQ5 — NLP baseline

| Statistic | Source file | Sheet/table | Denominator | Method |
|---|---|---|---|---|
| D1: 29.5% exact, κ=.283, baseline 28.4% | `08_NLP_Development/NLP_Baseline_Results_v1.0.xlsx` | `Per_Dimension_Metrics` | n=95 test profiles | `alcsm.nlp.evaluate.evaluate_predictions` (exact match, linear-weighted Cohen's κ) against `alcsm.nlp.baseline`'s TF-IDF+Ridge predictions, seed=42 |
| D2: 100.0% exact, κ=1.000, baseline 100.0% | same | same | n=47 | same; degenerate — present-only population is 100% score 1 (verified separately against `Dimension_Evidence`, `RQ5_NLP_Final_Results_v1.0.md`) |
| D3: 52.0% exact, κ=.399, baseline 35.0% | same | same | n=100 | same |
| D4: 62.9% exact, κ=−.022, baseline 71.4% | same | same | n=35 | same |
| D5: 87.0% exact, κ=.260, baseline 87.0% | same | same | n=100 | same |
| D6: 44.0% exact, κ=.238, baseline 48.0% | same | same | n=100 | same |
| Fixed random seed 42 | `src/alcsm/nlp/baseline.py`, `RANDOM_SEED` constant | n/a | n/a | Used for every train/test split and the Ridge model itself |
| D1 train=376/test=95; D2 187/47; D3 397/100; D4 140/35; D5 400/100; D6 397/100 | `NLP_Baseline_Results_v1.0.xlsx` | `Model_Configuration` | Per-dimension "present"-only population | `alcsm.nlp.baseline.split_profiles_for_dimension`, 80/20 split |

## 8. Interpretive statements — flagged as interpretation, not direct measurement

The following claims in the thesis-ready prose synthesize or draw an inference from directly measured numbers above; they are not themselves a single measured statistic and are flagged here so they are not mistaken for one in the final thesis text:

| Statement (chapter, section) | Basis | Nature of the interpretive step |
|---|---|---|
| "D3 shows the strongest genuine NLP signal despite the weakest human reliability" (Results §4.6, Discussion §5.3) | RQ3 α=.102 (lowest) + RQ5 D3 κ=.399 (highest margin over baseline) | Cross-analysis comparison between two independently computed results; the juxtaposition itself is an interpretive observation, not a jointly computed statistic. |
| "D6's weak NLP performance plausibly reflects an inability to aggregate distinct-industry counts across experience rows" (Discussion §5.8) | RQ5 D6 confusion matrix (predictions cluster at 1–2) + D6's rubric definition (counts distinct industries) | A plausible mechanistic explanation, not something directly measured — no ablation or feature-attribution analysis was run to confirm this cause. |
| "D5's low alpha is primarily range restriction, not primarily construct ambiguity" (Discussion §5.4) | RQ3 D5 variance (rater A concentrated 68/75) + 85.3% raw agreement | An interpretive weighting of two contributing factors; both underlying numbers are measured, but "primarily" is a qualitative judgment, not a computed proportion of variance explained. |
| "D2 and D4's perfect alpha are not evidence of strong discrimination" (Results §4.4, Discussion §5.2) | RQ3 D2/D4 variance and category counts (near-zero variance) | Interpretive framing applied to a measured statistic (alpha), not a separate measurement. |
| "This convergence... is read as reasonably strong evidence that D1 and D6 can be scored with acceptable reproducibility" (Discussion §5.2) | Combination of RQ1 distribution shape + RQ3 alpha + RQ5 signal for D1/D6 | Explicit synthesis judgment across three separate analyses — flagged with "read as" in the source text precisely because it is interpretive. |
| "ALCSM is not presented as a fully validated instrument" (Conclusion) | Entirety of RQ3 findings | A stated framing/scope decision, not a measured result — included here for completeness, not because it risks being mistaken for a statistic. |
| Future-work recommendations (Discussion §5.10) | Gaps identified across RQ3/RQ4/RQ5 | Forward-looking judgment, not a result. |

## 9. Cross-document consistency check

Every figure in §2–§7 above was checked for consistency across the documents that cite it (RQ-specific final-results documents, the Results/Discussion/Abstract/Conclusion drafts, and `ALCSM_Final_Results_Summary_v1.0.xlsx`). **No numerical contradiction was found** — every repeated citation of a given statistic (e.g., D3's α=.102, or the 51.3% NOT_DIRECTLY_MAPPED figure) uses the identical value everywhere it appears.

---

*This audit is itself descriptive — it does not introduce, adjust, or reinterpret any statistic. No canonical source file was modified in the course of this audit.*
