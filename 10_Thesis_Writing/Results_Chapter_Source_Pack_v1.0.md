# Results Chapter Source Pack v1.0

**Purpose:** every numerical statement available for Chapter 4 (Results), with exact value, denominator, source report, and source table. **No interpretation is added here** — this is raw sourced material only; synthesis and interpretation belong in the Discussion chapter (`Discussion_Chapter_Source_Pack_v1.0.md`) and the Results chapter's own connecting prose (`Results_Chapter_Draft_v1.0.md`), not in this pack.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## 4.1 Dataset overview

| Statement | Exact value | Denominator | Source report | Source table |
|---|---|---|---|---|
| LinkedIn profiles | 500 | — | `Final_Annotation_Audit_v1.1.md` | `Profile_Scores` sheet, `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` |
| Profile × dimension labels | 3,000 | 500 profiles × 6 dimensions | `Final_Annotation_Audit_v1.1.md` | `Dimension_Evidence` sheet, same file |
| Job postings | 201 | — | `RQ2_Final_Results_v1.0.md` §1 | `Job_Master`, `ALCSM_JobPosting_Processed_v1.1.xlsx` |
| Requirement records | 1,558 | — | `RQ2_Final_Results_v1.0.md` §1 | `Requirements`, same file |
| Expert survey respondents (consented) | 24 | 24 of 24 raw rows | `Survey_Status_Report_v1.0.md` | `Overview`, `ALCSM_Survey_Analysis_Processed_v1.0.xlsx` |
| Reliability subset size | 75 | 15% of 500 | `Reliability_Subset_Verification_v1.2.md` Part A | `Subset_Roster`, `ALCSM_Reliability_Subset_75_v1.1.xlsx` |
| Reliability subset selection seed | 20260824 | — | `Reliability_Subset_Selection_Report.md` | `Selection_Metadata` sheet, same file |

## 4.2 RQ1

**Score distribution** (source: `RQ1_Final_Results_v1.0.md` §1; source table: `Table1_Dimension_Score_Distribution.csv`; denominator n=500 throughout):

| Dim | Mean | Median | Std | Range observed |
|---|---|---|---|---|
| D1 | 2.28 | 3 | 1.59 | 0–5 |
| D2 | 0.47 | 0 | 0.50 | 0–1 |
| D3 | 2.93 | 3 | 1.14 | 0–4 |
| D4 | 0.95 | 0 | 1.32 | 0–3 |
| D5 | 2.91 | 3 | 0.49 | 0–4 |
| D6 | 1.77 | 2 | 0.96 | 0–5 |

- D5 profiles scored exactly 3: 435 of 500 (87.0%). Source: `Table1_Dimension_Score_Distribution.csv`, score=3 row, direct division 435/500.

**Missingness** (source: `RQ1_Final_Results_v1.0.md` §2; source table: `Table2_Missingness_By_Dimension.csv`; denominator n=500):

| Dim | Present | Unavailable | % Unavailable |
|---|---|---|---|
| D1 | 471 | 29 | 5.8% |
| D2 | 234 | 266 | 53.2% |
| D3 | 497 | 3 | 0.6% |
| D4 | 175 | 325 | 65.0% |
| D5 | 500 | 0 | 0.0% |
| D6 | 497 | 3 | 0.6% |

- Three profiles (LP0041, LP0170, LP0182) account for all D3/D6 unavailable cases. Source: `Final_Annotation_Audit_v1.1.md`; `Data_Integrity` sheet, frozen annotation workbook.

**Cross-tabulation** (source: `RQ1_Final_Results_v1.0.md` §3; source table: `Table5_Mean_Dimension_By_Title_Category.csv`): mean D1–D6 scores broken out by 17 `Title_Category` levels — exact per-category values are in the source table; not reproduced in full here (large categorical table, better read directly from CSV for the thesis appendix).

## 4.3 RQ2

**Requirement volume by dimension** (source: `RQ2_Final_Results_v1.0.md` §1; source table: `Table1_Requirement_Counts_By_Dimension.csv`; denominator n=1,558):

| Category | n requirements | % of total |
|---|---|---|
| NOT_DIRECTLY_MAPPED | 799 | 51.3% |
| D5 | 436 | 28.0% |
| D3 | 185 | 11.9% |
| D1 | 116 | 7.4% |
| D2 | 17 | 1.1% |
| D4 | 4 | 0.3% |
| D6 | 1 | 0.06% |

- Requirements mapped to any dimension (complement of NOT_DIRECTLY_MAPPED): 48.7% (759/1,558). Derived by direct arithmetic (100% − 51.3%); not a separately-computed statistic.

**Held level (supply side)** (source: `RQ2_Final_Results_v1.0.md` §2; source table: `Table3_Mean_Median_Held_Level_By_Dimension.csv`; denominator n=500): identical to the RQ1 §4.2 mean/median table above — same underlying `Profile_Scores` computation, reused not recomputed.

**D6 asymmetry** (source: `RQ2_Final_Results_v1.0.md` §4; source table: `Table6_D6_Profile_vs_Posting_Asymmetry.csv`):

| Side | Coverage | Denominator |
|---|---|---|
| Profile side (D6 evidence present) | 99.4% | 497/500 |
| Posting side (requirements mappable to D6) | 0.06% | 1/1,558 |

- Requirement intensity (Mandatory/Preferred/Not Specified counts per dimension): source table `Table5_Requirement_Intensity_By_Dimension.csv` — exact per-cell counts in that table, not reproduced here.

## 4.4 RQ3

**Inter-rater reliability** (source: `RQ3_Final_Results_Package_v1.0.md` §C, `Reliability_Report_v1.1.md`; source table: `Per_Dimension_Reliability` sheet, `Reliability_Results_v1.1.xlsx`):

| Dim | Krippendorff's α (ordinal) | n (dually-scored) | Observed agreement | Unavailable (of 75) |
|---|---|---|---|---|
| D1 | .944 | 72 | 81.9% | 3 |
| D2 | 1.000 | 27 | 100.0% | 48 |
| D3 | .102 | 75 | 54.7% | 0 |
| D4 | 1.000 | 26 | 100.0% | 49 |
| D5 | .246 | 75 | 85.3% | 0 |
| D6 | 1.000 | 75 | 100.0% | 0 |

- D3 disagreement pairs at score (3→4): 18 of 34 total D3 disagreements (52.9%). Source: `D3_D5_Disagreement_Analysis_v1.0.xlsx`, `Profile_Level_Disagreement` sheet, filtered `Rater_A=3 & Rater_B=4`.
- D3 disagreement directionality: 34 of 34 disagreements have Rater B scoring higher than Rater A (0 counter-examples). Source: same sheet, `Direction` column.
- D5 Rater A score concentration: 68 of 75 (90.7%) scored exactly 3. Source: `Reliability_Results_v1.1.xlsx`, `Per_Dimension_Reliability`, `rater_a_distribution` field (`{"2": 7, "3": 68}`).

**Expert survey** (source: `RQ3_Final_Results_Package_v1.0.md` §B; source table: sheets of `ALCSM_Survey_Analysis_Processed_v1.0.xlsx`; denominator N=24 throughout):

| Dim | Relevance mean (/5) |
|---|---|
| D1 | 3.54 |
| D2 | 3.25 |
| D3 | 4.33 |
| D4 | 3.54 |
| D5 | 3.63 |
| D6 | 3.67 |

- Overall framework appropriateness: mean 3.42/5. Source table: `Overall_Appropriateness` sheet.
- Most-important-dimension: D3 = 9/24 (37.5%), D4 = 5/24, D2 = 4/24, D6 = 4/24, D5 = 2/24. Source table: `Most_Important_Dimension` sheet.
- Distinctiveness item: 0/24 answered, all six dimensions. Source table: `Distinctiveness` sheet, `n_answered` column.

## 4.5 RQ4

| Statement | Exact value | Source report |
|---|---|---|
| Criterion variables available (network reach, content engagement, recognition count, seniority progression rate) | 0 of 4 | `RQ4_Final_Status_v1.0.md`, `RQ4_Limitation_Report_v1.0.md` §2 |

No further numerical content exists for RQ4 — the analysis was not conducted.

## 4.6 RQ5

**Per-dimension NLP baseline performance** (source: `RQ5_NLP_Final_Results_v1.0.md`; source table: `Per_Dimension_Metrics` sheet, `NLP_Baseline_Results_v1.0.xlsx`):

| Dim | n (test) | Exact agreement | Weighted κ | Majority-class baseline |
|---|---|---|---|---|
| D1 | 95 | 29.5% | .283 | 28.4% |
| D2 | 47 | 100.0% | 1.000 | 100.0% |
| D3 | 100 | 52.0% | .399 | 35.0% |
| D4 | 35 | 62.9% | −.022 | 71.4% |
| D5 | 100 | 87.0% | .260 | 87.0% |
| D6 | 100 | 44.0% | .238 | 48.0% |

**Train/test split sizes** (source table: `Model_Configuration` sheet, same file):

| Dim | n train | n test |
|---|---|---|
| D1 | 376 | 95 |
| D2 | 187 | 47 |
| D3 | 397 | 100 |
| D4 | 140 | 35 |
| D5 | 400 | 100 |
| D6 | 397 | 100 |

- Random seed: 42, fixed. Source: `src/alcsm/nlp/baseline.py`, `RANDOM_SEED` constant.
- Confusion matrices: `Confusion_D1` through `Confusion_D6` sheets, same workbook — exact per-cell counts there, not reproduced here.

---

*No canonical source file modified in the preparation of this pack. Every figure above is cross-checked against `Final_Thesis_Evidence_Audit_v1.0.md` (Task 7 of this session repeats this check).*
