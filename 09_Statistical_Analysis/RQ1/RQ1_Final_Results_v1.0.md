# RQ1 Final Results v1.0 — LinkedIn Profile Descriptive Patterns

**RQ1:** What credential patterns exist among self-identified AI leaders, as observable on LinkedIn?
**Status:** Final consolidation for thesis use. **No new computation** — every figure below is reproduced from `RQ1_Analysis_Report_v1.0.md` and its underlying `Tables/`/`Figures/`, regenerable via `15_Scripts/alcsm_rq1_analysis_v1.0.py`. **Only results actually supported by the final 500-profile dataset are included here** — no composite score, no weighting, no inferential/significance test anywhere (none was computed by the underlying analysis; none is added here).
**n = 500 profiles** throughout.
**Author:** Samiksha Dhere (researcher) — consolidated with Claude Code assistance

---

## 1. Dimension score distributions

| Dim | Mean | Median | Std | Range observed |
|---|---|---|---|---|
| D1 — Formal Education | 2.28 | 3 | 1.59 | 0–5 (full range) |
| D2 — Professional Certifications | 0.47 | 0 | 0.50 | 0–1 only |
| D3 — Practical AI Experience | 2.93 | 3 | 1.14 | 0–4 |
| D4 — Technical Contributions | 0.95 | 0 | 1.32 | 0–3 |
| D5 — Leadership & Strategic Responsibility | 2.91 | 3 | 0.49 | 0–4, heavily concentrated at 3 |
| D6 — AI Industry/Application Breadth | 1.77 | 2 | 0.96 | 0–5 (full range) |

D2 and D4 never reach the top of the nominal 0–5 scale in this dataset — a property of the source data (no certification issue/expiry metadata; no technical-contribution verification metadata), not a scoring artifact. D5 is heavily concentrated at score 3 (87.0% of profiles) — this same concentration independently explains D5's low inter-rater reliability alpha in the parallel reliability analysis (`RQ3_Final_Results_Package_v1.0.md` §C), a cross-check between two separate analyses of the same underlying population property.

## 2. Missingness by dimension

| Dim | Present | Unavailable | % Unavailable |
|---|---|---|---|
| D1 | 471 | 29 | 5.8% |
| D2 | 234 | 266 | 53.2% |
| D3 | 497 | 3 | 0.6% |
| D4 | 175 | 325 | 65.0% |
| D5 | 500 | 0 | 0.0% |
| D6 | 497 | 3 | 0.6% |

D4 (technical contributions) and D2 (certifications) are the two dimensions where a majority or near-majority of profiles simply do not state the relevant evidence at all on LinkedIn — a property of what people choose to publish, not a scoring artifact. D3's and D6's three unavailable profiles each are the same three profiles throughout this project (`LP0041`, `LP0170`, `LP0182`), which have zero `Professional_Experience` records.

## 3. Major credential patterns

- **D1 and D3 are the most evenly spread dimensions**, using most or all of the 0–5 range with substantial mass at several points — and are also, independently, the two dimensions with the strongest and weakest human inter-rater reliability results respectively (D1 strong, D3 weak), showing that a well-spread distribution alone does not guarantee reproducible scoring.
- **D5's near-ceiling concentration at score 3** (87% of profiles) means the "Leadership & Strategic Responsibility" dimension, as observed on LinkedIn, mostly distinguishes profiles at a coarse level (has some documented leadership signal vs. not) rather than finely across its full nominal range.
- Among title categories with meaningful sample sizes, **"Lead" shows the lowest D1 and D5 means**, consistent with "Lead" typically denoting a more technical, less strategic-scope role than "Director"/"VP" — an observed association in this sample, not a causal claim.

## 4. Important cross-dimension observations (descriptive only, never combined into one figure)

- D1 (formal education) and D5 (leadership/strategic scope) show different distributional shapes (D1 well-spread, D5 concentrated), consistent with them capturing genuinely different, non-interchangeable credential signals — supporting ALCSM's formative-index design rather than contradicting it.
- D6 (AI industry/application breadth), scored on the profile's own history, is observed on 99.4% of profiles (497/500) — near-universal profile-side coverage, a fact directly relevant to RQ2's finding that the job-posting side almost never states this as a requirement (`RQ2_Final_Results_v1.0.md`).
- No cross-dimension correlation, factor structure, or combined score is computed or reported anywhere in this document, consistent with ALCSM's formative (not reflective) measurement design (`RQ3_Final_Results_Package_v1.0.md` §A).

## What this document does not do

- No composite ALCSM score.
- No weight assigned to any dimension.
- No classification band.
- No inferential statistic (t-test, ANOVA, regression p-value, correlation significance test) — every number above is a count, mean, median, or standard deviation describing this sample only, exactly as in the underlying `RQ1_Analysis_Report_v1.0.md`.

---

*Full demographic breakdowns (country, industry, title category, company size) and the complete cross-tabulation tables remain in `09_Statistical_Analysis/RQ1/Tables/` and `Figures/` — reproduced here only where they support a stated finding, to keep this final document thesis-length. Reproducible via `python 15_Scripts/alcsm_rq1_analysis_v1.0.py`.*
