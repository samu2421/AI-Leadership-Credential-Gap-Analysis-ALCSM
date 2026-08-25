# Thesis Analysis Output Inventory v1.0

**Purpose:** exact list of tables/figures available right now for thesis writing, by RQ. Everything below already exists on disk and is reproducible; nothing here is aspirational.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## RQ1 — LinkedIn Profile Descriptive Patterns

| # | Title | Source dataset | Variables | Method | Chapter |
|---|---|---|---|---|---|
| Table 1 | Dimension Score Distribution | Frozen annotation, `Profile_Scores` (n=500) | D1–D6 scores 0–5, counts/mean/median/std | Descriptive frequency table | Results — RQ1 |
| Table 2 | Missingness by Dimension | Frozen annotation, `Dimension_Evidence` (n=500) | Present/unavailable counts per dimension | Descriptive count | Results — RQ1 |
| Table 3 | Dimension-Level Comparison | Frozen annotation | D1–D6 mean/median/std/min/max/n-informative | Descriptive side-by-side (not combined) | Results — RQ1 |
| Table 4 (×5) | Demographics (Country/State/Company Size/Industry/Title Category) | LinkedIn processed, `Profile_Master` (n=500) | Categorical counts | Frequency table | Results — RQ1 / Sample description |
| Table 5 | Mean Dimension Score by Title Category | LinkedIn + annotation, merged on Profile_ID | D1–D6 mean per Title_Category (17 levels) | Descriptive cross-tabulation | Results — RQ1 |
| Table 6 | Mean Dimension Score by Industry | LinkedIn + annotation, merged on Profile_ID | D1–D6 mean per Industry (20 levels) | Descriptive cross-tabulation | Results — RQ1 |
| Figure 1 | Dimension Score Distributions (small multiples) | Table 1 | D1–D6 histograms | Bar chart, 2×3 grid | Results — RQ1 |
| Figure 2 | Missingness by Dimension | Table 2 | Present/unavailable stacked bar | Stacked bar chart | Results — RQ1 |
| Figure 3 | Mean Score by Title Category (top 8 by n) | Table 5 | D1–D6 grouped bar | Grouped bar chart | Results — RQ1 |

**Location:** `09_Statistical_Analysis/RQ1/Tables/`, `Figures/`. **Report:** `RQ1_Analysis_Report_v1.0.md`. **Script:** `15_Scripts/alcsm_rq1_analysis_v1.0.py`.

## RQ2 — Job Posting Requirements vs. Profile Credential Signals

| # | Title | Source dataset | Variables | Method | Chapter |
|---|---|---|---|---|---|
| Table 1 | Requirement Counts by Dimension | Job postings, `Requirements` (n=1,558) | Count per `Final_ALCSM_Dimension` incl. Not Directly Mapped | Frequency table | Results — RQ2 |
| Table 2 | Not Directly Mapped by Category | Job postings, `Requirements` | Count per `Requirement_Category` for unmapped requirements | Frequency table | Results — RQ2 |
| Table 3 | Mean/Median Held Level by Dimension | Frozen annotation | D1–D6 mean/median (profile side) | Descriptive | Results — RQ2 |
| Table 4 | Supply vs. Demand Frequency | Tables 1+3 combined | n requirements vs. mean/median held score, side by side | Descriptive comparison (two units, not subtracted) | Results — RQ2 |
| Table 5 | Requirement Intensity by Dimension | Job postings, `Requirements` | Mandatory/Preferred/Not Specified counts per dimension | Frequency cross-tab | Results — RQ2 |
| Table 6 | D6 Profile-vs-Posting Asymmetry | Frozen annotation + job postings | Profile-side coverage % vs. posting-side coverage % for D6 | Descriptive ratio comparison | Results — RQ2 / Discussion |
| Figure 1 | Requirement Volume by Dimension | Table 1 | Sorted bar chart | Bar chart | Results — RQ2 |
| Figure 2 | Demand Volume vs. Held Level (dual-axis) | Table 4 | Requirement count (bar) + mean held score (line), two axes | Dual-axis chart | Results — RQ2 |
| Figure 3 | Requirement Intensity by Dimension | Table 5 | Stacked bar, Mandatory/Preferred/Not Specified | Stacked bar chart | Results — RQ2 |

**Location:** `09_Statistical_Analysis/RQ2/Tables/`, `Figures/`. **Report:** `RQ2_Gap_Analysis_Report_v1.0.md`. **Script:** `15_Scripts/alcsm_rq2_analysis_v1.0.py`. **No numeric "gap value" table exists** — `job_requirement_score.required_score` is unpopulated (§4 of the RQ2 report).

## RQ3 — ALCSM Construction/Validation

| # | Title | Source dataset | Variables | Method | Chapter |
|---|---|---|---|---|---|
| Table (in Reliability_Results_v1.1.xlsx) | Per-Dimension Reliability | 75-profile double-coded subset | n, Krippendorff's α (ordinal), 95% CI, % agreement, score variance, unavailable counts, per dimension | Krippendorff's alpha, bootstrap CI (2,000 resamples) | Methodology / Results — RQ3 |
| Table (in ALCSM_Survey_Analysis_Processed_v1.0.xlsx) | Relevance/Clarity/Distinctiveness by Dimension | 24-respondent expert survey | Mean/median 1–5 rating per dimension per item type | Descriptive | Results — RQ3 |
| Table (same file) | Participant Background | 24-respondent expert survey | Role, years experience, AI experience, leadership experience counts | Descriptive frequency | Methodology — sample description |
| Table (same file) | Most-Important-Dimension Counts | 24-respondent expert survey | Count per dimension | Descriptive frequency | Results — RQ3 |
| Narrative package | Formative measurement rationale + evidence synthesis + limitations | Reliability results + survey results, combined | — | Qualitative synthesis, explicitly not "proof of validity" | Methodology / Discussion — RQ3 |

**Location:** `07_Reliability/Reliability_Results_v1.1.xlsx`, `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` (both git-ignored, real data — export figures by hand into the thesis document). **Reports:** `07_Reliability/Reliability_Report_v1.1.md`, `07_Reliability/Survey_Analysis/Survey_Analysis_Plan_v1.0.md`, `09_Statistical_Analysis/RQ3/RQ3_Measurement_Evidence_Package_v1.0.md`. **No figures (PNG) generated for RQ3 this session** — the six-dimension alpha table and survey means are better presented as thesis tables directly from the CSV-equivalent data than as charts, but could be added if the thesis format benefits from a visual (not built, flagged as an easy addition if wanted).

## RQ4 — Observable Professional Impact Indicators

**No table or figure available.** Data-collection gap, not a code or analysis gap — see `09_Statistical_Analysis/RQ4/RQ4_Limitation_Report_v1.0.md`. The four criterion variables (`rq4_network_reach`, `rq4_content_engagement`, `rq4_recognition_count`, `rq4_seniority_progression_rate`) do not exist anywhere in the currently collected data.

## RQ5 — NLP Human-vs-Machine Agreement

**No table or figure available — no model has been trained.** Gold-standard readiness is confirmed and documented in `08_NLP_Development/NLP_Readiness_Report_v1.0.md` (label distributions, missingness, class imbalance — reusing RQ1's Table 1/2 rather than a separate computation). If a baseline model is built before submission, `alcsm.nlp.evaluate`'s confusion-matrix/exact-match/MAE/weighted-kappa outputs would populate this section — the evaluation code is ready; no prediction data exists yet to run it on.

---

## Summary count

| RQ | Tables | Figures | Status |
|---|---|---|---|
| RQ1 | 10 (across 6 numbered tables, one multi-file) | 3 | Complete |
| RQ2 | 6 | 3 | Complete (no numeric gap value — documented why) |
| RQ3 | 4 (2 workbooks) | 0 | Complete (evidence package, not proof-of-validity) |
| RQ4 | 0 | 0 | Blocked — data collection gap, documented |
| RQ5 | 0 | 0 | Not started — readiness confirmed, baseline scoped not built |

**19 real, reproducible tables and 6 figures currently exist across RQ1–RQ3**, all regenerable from source with a single script run each, all reading directly from canonical Excel workbooks that were never modified to produce them.
