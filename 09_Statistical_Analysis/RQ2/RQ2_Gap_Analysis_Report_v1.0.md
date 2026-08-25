# RQ2 Gap Analysis Report v1.0 — Job Posting Requirements vs. Profile Credential Signals

**RQ2:** How do stated job-posting requirements compare to the credential signals held by AI leaders on LinkedIn?
**Status:** Aggregate, dimension-level comparison only. **No one-to-one candidate-to-posting matching. No numeric "gap value" is computed (no `required_score` data exists — see §4). No composite score, no weights.**
**Source (read-only, unmodified):** `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` (`Requirements`, 1,558 rows / 201 postings), `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` (`Profile_Scores`, `Dimension_Evidence`).
**Script:** `15_Scripts/alcsm_rq2_analysis_v1.0.py`, reusing `alcsm.analysis.gap` (one new function added this session, `requirement_intensity_by_dimension`) and `alcsm.analysis.rq1_descriptive.dimension_distribution`.

---

## 1. Requirement volume by dimension (Table 1, Figure 1)

| Category | n requirements | % of total |
|---|---|---|
| NOT_DIRECTLY_MAPPED | 799 | 51.3% |
| D5 — Leadership & Strategic Responsibility | 436 | 28.0% |
| D3 — Practical AI Experience | 185 | 11.9% |
| D1 — Formal Education | 116 | 7.4% |
| D2 — Professional Certifications | 17 | 1.1% |
| D4 — Technical Contributions | 4 | 0.3% |
| D6 — AI Industry/Application Breadth | 1 | 0.06% |

**More than half of all requirement records (51.3%) do not map to any ALCSM dimension.** This is reported as its own category, exactly as stated, not redistributed or forced into a dimension (Table 2 breaks the 799 down by `Requirement_Category` — `Technical Skill` (170), `Communication` (164), and `Other` (125) are the largest unmapped categories, i.e. postings frequently ask for generic technical/soft skills that ALCSM's six credential-signal dimensions are not designed to capture).

Among mapped requirements, demand is heavily concentrated in **D5** (leadership/strategic language) and **D3** (practical AI experience) — together 78% of all mapped requirements. **D6 is almost entirely absent on the posting side** (1 of 1,558 requirements) — see §5.

## 2. Profile-side held level (Table 3)

| Dim | Mean held | Median held |
|---|---|---|
| D1 | 2.28 | 3.0 |
| D2 | 0.47 | 0.0 |
| D3 | 2.93 | 3.0 |
| D4 | 0.95 | 0.0 |
| D5 | 2.91 | 3.0 |
| D6 | 1.77 | 2.0 |

Identical to RQ1's Table 1 means — reused directly, not recomputed differently, so the two reports stay consistent with each other.

## 3. Supply vs. demand, side by side (Table 4, Figure 2)

**Explicitly two different units, never subtracted into one number:**

| Dim | n requirements (demand volume) | Mean held score (supply level) |
|---|---|---|
| D1 | 116 | 2.28 |
| D2 | 17 | 0.47 |
| D3 | 185 | 2.93 |
| D4 | 4 | 0.95 |
| D5 | 436 | 2.91 |
| D6 | 1 | 1.77 |

**Qualitative gap direction** (descriptive, not a numeric subtraction): D5 is simultaneously the **highest-demand** dimension (436 requirements, 28% of all mapped requirements) and one of the **higher-held** dimensions on the profile side (mean 2.91) — demand and supply point the same direction here, suggesting D5 is a genuinely contested, actively-recruited-for signal that profiles also tend to display. D3 shows a similar pattern (185 requirements, mean held 2.93). By contrast, **D2 has low demand (17 requirements) and the lowest held level (mean 0.47)** — both sides agree this dimension is a minor signal in this corpus, on both the hiring and the profile side. **D6's near-total absence on the posting side (1 requirement) against a moderate, present held level on the profile side (mean 1.77, 99.4% profile coverage) is the sharpest asymmetry in the dataset** — postings essentially never ask for AI industry/application breadth as a stated requirement, even though most profiles carry some observable signal for it. This is examined on its own in §5.

## 4. Why no numeric gap value is reported

`alcsm.analysis.gap.dimension_gap_from_scores` implements the true `mean(required) − mean(held)` formula, but it requires `job_requirement_score.required_score` — a per-requirement 0–5 numeric scoring pass that has never been built or run (a separate, requirement-level annotation exercise, distinct from the D1–D6 mapping already done). That function remains exercised against synthetic fixtures only (`tests/analysis/test_gap.py`); it is not run against real data in this report, and no numeric gap value appears anywhere in this document. What §1–§3 report instead — requirement **volume/intensity** (demand) next to profile **held level** (supply) — is the closest available real-data comparison, and is explicitly labeled as being in different units throughout.

## 5. Requirement intensity (Table 5, Figure 3)

`Mandatory_or_Preferred` breakdown per dimension:

| Dim | Not Specified | Preferred | Required |
|---|---|---|---|
| D1 | 38 | 9 | 69 |
| D2 | 2 | 9 | 6 |
| D3 | 40 | 36 | 109 |
| D4 | 0 | 4 | 0 |
| D5 | 121 | 30 | 285 |
| D6 | 1 | 0 | 0 |

D5 has both the highest volume and the highest count of requirements explicitly stated as `Required` (285) rather than merely `Preferred` — reinforcing §3's reading that D5 is the most insistently demanded credential signal in this corpus. D1 and D3 also skew toward `Required` over `Preferred`. D4's four requirements are all `Preferred`, none `Required` — the weakest-demanded mapped dimension along with D2 and D6.

## 6. D6 profile-vs-posting asymmetry (Table 6)

| Side | Coverage |
|---|---|
| Profile side (profiles with D6 evidence) | 497 / 500 = **99.4%** |
| Posting side (requirements mappable to D6) | 1 / 1,558 = **0.06%** |

This reproduces, from the current real data, the same asymmetry finding already documented in `ALCSM_D6_Industry_Breadth_v1.1.md` §5 and `D6_v1.1_Implementation_Assessment.md` §5: D6 is a dimension almost every profile can be scored on, but one that job postings essentially never state as an explicit requirement. This is a property of how job postings are written (industry breadth is not typically phrased as a discrete "requirement" the way a degree or certification is), not a flaw in D6's construction, and it is not evidence for or against D6's validity — that question belongs to the reliability and content-validity evidence in `07_Reliability/`, not to this gap analysis.

## 7. What this report does not do

- No individual profile is compared against an individual posting anywhere.
- No `NOT_DIRECTLY_MAPPED` requirement is forced into a dimension.
- No numeric gap value, composite score, weight, or classification band is computed.

---

*Reproducible via `python 15_Scripts/alcsm_rq2_analysis_v1.0.py`. Tables (CSV) and figures (PNG) regenerate identically from the frozen source files on every run.*
