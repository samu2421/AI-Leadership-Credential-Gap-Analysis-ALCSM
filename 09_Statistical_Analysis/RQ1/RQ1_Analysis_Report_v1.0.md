# RQ1 Analysis Report v1.0 — LinkedIn Profile Descriptive Patterns

**RQ1:** What credential patterns exist among self-identified AI leaders, as observable on LinkedIn?
**Status:** Purely descriptive. **No composite ALCSM score, no weights, no classification bands, no inferential statistic (no p-value, no effect size, no causal claim) anywhere in this report or the code that produced it.**
**Source (read-only, unmodified):** `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` (`Profile_Scores`, `Dimension_Evidence`), `05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` (`Profile_Master`).
**Script:** `15_Scripts/alcsm_rq1_analysis_v1.0.py`, reusing `alcsm.analysis.rq1_descriptive` (one label fix applied — D6 now displays its frozen v1.1 name, "AI Industry/Application Breadth", instead of the retired v1.0 label; this is a display-string correction, not a change to D6's definition or criteria).
**n = 500 profiles** throughout.

---

## 1. Per-dimension score distribution (Table 1, Figure 1)

| Score | D1 Education | D2 Certs | D3 Experience | D4 Contributions | D5 Leadership | D6 Industry Breadth |
|---|---|---|---|---|---|---|
| 0 | 122 | 266 | 4 | 325 | 3 | 6 |
| 1 | 40 | 234 | 105 | 4 | 12 | 239 |
| 2 | 67 | 0 | 4 | 44 | 30 | 155 |
| 3 | 134 | 0 | 197 | 127 | 435 | 67 |
| 4 | 120 | 0 | 190 | 0 | 20 | 28 |
| 5 | 17 | 0 | 0 | 0 | 0 | 5 |
| **Mean** | 2.28 | 0.47 | 2.93 | 0.95 | 2.91 | 1.77 |
| **Median** | 3 | 0 | 3 | 0 | 3 | 2 |
| **Std** | 1.59 | 0.50 | 1.14 | 1.32 | 0.49 | 0.96 |

`09_Statistical_Analysis/RQ1/Tables/Table1_Dimension_Score_Distribution.csv`; `Figures/Figure1_Dimension_Score_Distributions.png`.

**Reading the shape, not just the mean:**
- **D2 and D3 never reach the top of the 0–5 scale** in this dataset (D2 max observed = 1; D4 max observed = 3). This is a known, previously documented property of the source data (no certification issue/expiry metadata; no technical-contribution verification metadata) — not new to this report, but visible again here in the raw counts.
- **D5 is heavily concentrated at 3** (435 of 500 profiles, 87%) with almost no use of the low end — this concentration is exactly what produced D5's low, range-restricted reliability alpha in `Reliability_Report_v1.1.md` §10, and the two findings corroborate each other from independent angles (population-wide distribution here, subset reliability there).
- **D1 and D3 are the most evenly spread dimensions**, using most or all of the 0–5 range with substantial mass at several points — consistent with D1 also being the dimension with the strongest reliability result (§10 of the reliability report).

## 2. Missingness by dimension (Table 2, Figure 2)

| Dimension | Present | Unavailable | % Unavailable |
|---|---|---|---|
| D1 | 471 | 29 | 5.8% |
| D2 | 234 | 266 | 53.2% |
| D3 | 497 | 3 | 0.6% |
| D4 | 175 | 325 | 65.0% |
| D5 | 500 | 0 | 0.0% |
| D6 | 497 | 3 | 0.6% |

`Tables/Table2_Missingness_By_Dimension.csv`; `Figures/Figure2_Missingness_By_Dimension.png`. D4 (technical contributions) and D2 (certifications) are the two dimensions where a majority or near-majority of profiles simply do not state the relevant evidence at all — this is a property of what people choose to publish on LinkedIn, not a scoring artifact. D3's and D6's 3 unavailable profiles each are the same three profiles throughout this project (`LP0041`, `LP0170`, `LP0182`, zero `Professional_Experience` records — `Final_Annotation_Audit_v1.1.md`).

## 3. Dimension-level comparison (Table 3)

Side-by-side, **never summed or weighted** (`Tables/Table3_Dimension_Level_Comparison.csv`) — included for reference, not as a ranking:

| Dim | Label | Mean | Median | Std | Min | Max | n informative |
|---|---|---|---|---|---|---|---|
| D1 | Formal Education | 2.28 | 3 | 1.59 | 0 | 5 | 471 |
| D2 | Professional Certifications | 0.47 | 0 | 0.50 | 0 | 1 | 234 |
| D3 | Practical AI Experience | 2.93 | 3 | 1.14 | 0 | 4 | 497 |
| D4 | Technical Contributions | 0.95 | 0 | 1.32 | 0 | 3 | 175 |
| D5 | Leadership & Strategic Responsibility | 2.91 | 3 | 0.49 | 0 | 4 | 500 |
| D6 | AI Industry/Application Breadth | 1.77 | 2 | 0.96 | 0 | 5 | 497 |

## 4. Profile-level demographic patterns (Table 4)

Counts by `Country`, `Federal_State`, `Company_Size`, `Industry`, `Title_Category` — five CSVs under `Tables/Table4_Demographics_*.csv`. Not reproduced in full here (they are large categorical breakdowns better read directly from CSV or embedded as thesis appendix tables); `Title_Category` has 17 distinct levels, `Industry` has 20.

## 5. Cross-tabulations (substantively justified — Tables 5–6, Figure 3)

**Table 5 — mean D1–D6 by `Title_Category`.** Justified because RQ1 asks about patterns among self-identified *leaders* specifically — whether formal seniority title tracks with any particular credential dimension is a natural first descriptive question. Selected findings (full table in CSV; top-8-by-n categories plotted in `Figures/Figure3_Mean_Score_By_Title_Category.png`):
- `Director` (n largest among senior titles) and `Head` show broadly similar mean profiles across D1/D3/D5/D6, both close to the population-wide means.
- `Lead` shows the lowest D1 and D5 means among the larger categories — consistent with "Lead" typically denoting a more technical, less strategic-scope role than "Director"/"VP", which is exactly what D5's definition (strategic responsibility, not title alone) would predict.
- These are observed associations in this sample, described as such — not a claim that title category determines credential level.

**Table 6 — mean D1–D6 by current-employer `Industry`.** Justified specifically because D6 measures AI-related industry/application *breadth*, and checking whether D6 (or any other dimension) varies systematically by the profile's own single current-employer industry is a directly relevant, substantively motivated check — distinct from D6 itself, which counts breadth across a person's history, not their current employer's sector (`ALCSM_D6_Industry_Breadth_v1.1.md` §5, already flagged in `rq1_descriptive.py`'s own docstring as a conflation to avoid). 20 industry levels; full table in CSV.

## 6. What this report does not do

- No composite ALCSM score is computed anywhere.
- No weight is assigned to any dimension.
- No classification band (e.g., "high/medium/low AI leader") is created.
- No inferential test (t-test, ANOVA, regression, correlation p-value) is run — every number above is a count, mean, median, or standard deviation, describing this sample only.
- The annotation and LinkedIn source workbooks were opened read-only; neither was modified.

---

*Reproducible via `python 15_Scripts/alcsm_rq1_analysis_v1.0.py`. Tables (CSV) and figures (PNG) regenerate identically from the frozen annotation file on every run.*
