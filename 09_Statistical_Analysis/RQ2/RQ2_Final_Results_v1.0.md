# RQ2 Final Results v1.0 — Job Posting Requirements vs. Profile Credential Signals

**RQ2:** How do stated job-posting requirements compare to the credential signals held by AI leaders on LinkedIn?
**Status:** Final consolidation for thesis use. **No new computation** — every figure below is reproduced from `RQ2_Gap_Analysis_Report_v1.0.md` and its underlying `Tables/`/`Figures/`, regenerable via `15_Scripts/alcsm_rq2_analysis_v1.0.py`.
**Data:** 201 job postings, 1,558 requirement records, final six-dimensional mapping (`Final_ALCSM_Dimension`).
**Author:** Samiksha Dhere (researcher) — consolidated with Claude Code assistance

---

## Demand-side vs. supply-side — kept explicitly distinct throughout

This document distinguishes two signals that are **not the same thing and are never combined into one number**:

- **Demand-side requirement signal**: how often, and how insistently, job postings *state* a requirement mappable to a dimension. This describes what employers say they want.
- **Supply-side observed credential signal**: the *held* score profiles display on that same dimension, from the frozen annotation. This describes what LinkedIn profiles show.

**A stated requirement is not the same as possession of the corresponding credential**, and this document never treats it as such. No individual profile is matched against an individual job posting anywhere in this analysis — every comparison below is an aggregate, dimension-level statistic across the whole corpus.

## 1. Requirement volume (demand-side)

| Category | n requirements | % of total |
|---|---|---|
| **NOT_DIRECTLY_MAPPED** | **799** | **51.3%** |
| D5 — Leadership & Strategic Responsibility | 436 | 28.0% |
| D3 — Practical AI Experience | 185 | 11.9% |
| D1 — Formal Education | 116 | 7.4% |
| D2 — Professional Certifications | 17 | 1.1% |
| D4 — Technical Contributions | 4 | 0.3% |
| D6 — AI Industry/Application Breadth | 1 | 0.06% |

**More than half of all requirement records (51.3%) do not map to any ALCSM dimension and are preserved as `NOT_DIRECTLY_MAPPED` — never forced into D1–D6.** The largest unmapped categories are generic technical-skill and communication requirements, which ALCSM's six credential-signal dimensions are not designed to capture.

## 2. Held level (supply-side, from the frozen annotation)

| Dim | Mean held | Median held |
|---|---|---|
| D1 | 2.28 | 3.0 |
| D2 | 0.47 | 0.0 |
| D3 | 2.93 | 3.0 |
| D4 | 0.95 | 0.0 |
| D5 | 2.91 | 3.0 |
| D6 | 1.77 | 2.0 |

## 3. Qualitative comparison (never a numeric gap — no `required_score` data exists)

| Dim | Demand volume | Held level | Reading |
|---|---|---|---|
| D5 | Highest (436 requirements, 285 stated as `Required`) | High (mean 2.91) | Demand and supply point the same direction — D5 is the most actively recruited-for signal and profiles also tend to display it. |
| D3 | High (185 requirements) | High (mean 2.93) | Same pattern as D5, smaller scale. |
| D2 | Low (17 requirements) | Lowest (mean 0.47) | Both sides agree D2 is a minor signal in this corpus. |
| D6 | Almost absent (1 requirement, 0.06%) | Present (mean 1.77, 99.4% profile coverage) | **The sharpest asymmetry in the dataset** — postings essentially never state AI industry/application breadth as a requirement, even though nearly every profile carries some observable signal for it. |

**No numeric "gap value" is computed anywhere in this document.** `job_requirement_score.required_score` — a per-requirement 0–5 numeric scoring pass — has never been built or populated; the comparison above is deliberately qualitative and stated as such, per the same discipline as the underlying `RQ2_Gap_Analysis_Report_v1.0.md`.

## 4. D6 profile-vs-posting asymmetry (headline finding)

| Side | Coverage |
|---|---|
| Profile side (profiles with D6 evidence) | 497 / 500 = **99.4%** |
| Posting side (requirements mappable to D6) | 1 / 1,558 = **0.06%** |

This reproduces, from the current real data, the asymmetry finding already documented in the D6 v1.1 construct design work. It is a property of how job postings are conventionally written (industry breadth is rarely phrased as a discrete stated requirement, unlike a degree or certification), not evidence for or against D6's validity as a construct — that question belongs to the reliability and content-validity evidence in RQ3, not to this gap analysis.

## What this document does not do

- No individual profile is matched against an individual job posting anywhere.
- No `NOT_DIRECTLY_MAPPED` requirement is forced into a dimension.
- No claim that a stated requirement equals possession of the corresponding credential.
- No numeric gap value, composite score, weight, or classification band is computed anywhere.

---

*Reproducible via `python 15_Scripts/alcsm_rq2_analysis_v1.0.py`. Full tables (requirement intensity, demographic cross-tabs) remain in `09_Statistical_Analysis/RQ2/Tables/`; reproduced here only where they support a stated finding.*
