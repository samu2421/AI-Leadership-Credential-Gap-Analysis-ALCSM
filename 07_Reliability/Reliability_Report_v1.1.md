# ALCSM v1.1 Inter-Rater Reliability Report

**Status:** Real reliability results, computed from genuinely independent human double coding. **Not a pilot, not a simulation, not an AI-vs-human comparison.**
**Rater A:** primary researcher (frozen final annotation, `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`).
**Rater B:** independent human second rater (a friend of the researcher), recovered from `07_Reliability/Double_Coding/ALCSM_Reliability_Subset_75_v1.1.xlsx` — see `Reliability_Subset_Verification_v1.1.md` for the full data-recovery and missing-data-inference trail.
**Results workbook:** `Reliability_Results_v1.1.xlsx` (git-ignored, real data).
**Author:** Samiksha Dhere (researcher) — analyzed with Claude Code assistance

---

## 1. Sample design

75 of the 500 frozen profiles (exactly 15%), selected by `alcsm.annotation.pilot.select_pilot_subset(method="random_subset", seed=20260824, fraction=0.15)` — a deterministic, seeded random draw over all 500 `Profile_ID`s in their `Profile_Scores` row order. Verified this session to be exactly reproducible and unaltered (`Reliability_Subset_Verification_v1.1.md` Part A). No profile was manually added, removed, or swapped.

## 2. Why 75 profiles were double-coded

This project's frozen double-coding policy (`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §15) requires "100% double coding if feasible; otherwise a pre-registered random subset of at least 15%." 100% double coding of 500 profiles was not feasible within the available time and personnel; 75 profiles (exactly the 15% minimum, not less) was pre-registered and drawn before any second-rater coding began (`Reliability_Subset_Selection_Report.md`, prior session). Sampling was not restricted to "easy" profiles — the subset's dimension-score and missingness proportions were checked against the full 500-profile population and found unbiased (`Reliability_Subset_Selection_Report.md` §3).

## 3. Independent-rater procedure

Rater A's scores are the researcher's own final judgment already on record in the frozen annotation (not the AI-assisted first pass — see §4 for the explicit distinction). Rater B is a second, independent human coder (the researcher's friend) who scored the same 75 profiles using the frozen v1.1 framework and instructions (`Second_Rater_Annotation_Instructions_v1.1.md`), without access to Rater A's scores during coding. Rater B's completed scores were entered directly into the roster workbook rather than the intended blank template — a filing deviation, not a procedural one; the coding itself was independent.

**On the AI-vs-human question:** this reliability result compares two independent *human* coders (the researcher and her friend). It is not, and is never described anywhere in this codebase as, a comparison between the AI-assisted first pass and a human — `alcsm.analysis.rq3_validation.inter_rater_reliability`'s `_ALLOWED_HUMAN_RATER_IDS` guard structurally rejects any non-`RATER_A`/`RATER_B` id, and both raters used here are exactly those two ids.

## 4. Missing-data handling (explicit, per this session's Part C requirement)

If **either** rater's value for a profile × dimension cell is unavailable, that cell is excluded from that dimension's alpha computation entirely — never coerced to a 0 (`alcsm.reliability.subset_workflow.run_subset_reliability_analysis`, tested in `tests/reliability/test_subset_workflow.py::TestUnavailableHandling`).

Rater A's unavailable status comes directly from the frozen annotation's own `Missing_Status` column. Rater B's raw file has no structural way to record "unavailable" separately from an observed 0 (see `Reliability_Subset_Verification_v1.1.md` Part B for the full explanation) — so Rater B's unavailable cases were **inferred** from Rater A's own unavailable flag for the same cell, justified by every one of Rater B's `0` entries coinciding exactly (100%, no exceptions) with a cell Rater A independently marked unavailable, for every dimension where Rater A recorded any unavailable case at all (D1: 3/3, D2: 48/48, D4: 49/49). D3, D5, D6 have zero Rater-A-unavailable cases in this subset, so no exclusion was needed or applied there. This is disclosed as an interpretive decision with a stated residual limitation, not treated as certain.

## 5–9. Per-dimension results

Ordinal Krippendorff's alpha, percent agreement, n (dually-scored, non-unavailable units), 95% bootstrap CI (2,000 resamples, seed 42), and score variance — **each dimension computed and reported entirely separately; no pooled or averaged alpha is computed or reported anywhere in this document or its underlying code.**

| Dim | n | Alpha (ordinal) | 95% CI | % Agreement | Score variance | Rater A unavail. | Rater B unavail. (inferred) |
|---|---|---|---|---|---|---|---|
| D1 — Formal Education | 72 | **0.944** | [0.884, 0.980] | 81.9% | 2.609 | 3 | 3 |
| D2 — Certifications | 27 | **1.000** | [1.000, 1.000] | 100.0% | 0.000 | 48 | 48 |
| D3 — Practical AI Experience | 75 | **0.102** | [−0.136, 0.333] | 54.7% | 1.015 | 0 | 0 |
| D4 — Technical Contributions | 26 | **1.000** | [1.000, 1.000] | 100.0% | 0.391 | 49 | 49 |
| D5 — Leadership & Strategic Responsibility | 75 | **0.246** | [−0.072, 0.584] | 85.3% | 0.222 | 0 | 0 |
| D6 — AI Industry/Application Breadth | 75 | **1.000** | [1.000, 1.000] | 100.0% | 0.889 | 0 | 0 |

Full score distributions for both raters, per dimension, are in `Reliability_Results_v1.1.xlsx` (`Per_Dimension_Reliability` sheet) and the raw long-format rating tables (`Rater_A_Long`, `Rater_B_Long` sheets).

## 10. Interpretation, dimension by dimension

**No dimension is declared invalid here on alpha alone** — per this task's own instruction, low alpha is a starting point for discussion, not an automatic verdict, and this section discusses variance, distribution shape, and missingness alongside the number itself.

**D1 (α = 0.944, "proceed").** High agreement across a genuinely wide score range (0–5, all six values represented, variance 2.61 — the highest of any dimension here). This is the cleanest evidence of reliable independent scoring in this subset: both raters are discriminating across the full scale and mostly landing in the same place.

**D2 (α = 1.000, "proceed" — read with caution).** Perfect agreement, but on a **restricted, low-variance sample**: 48 of 75 profiles are unavailable for D2 in this subset, and of the remaining 27, every single rating from both raters was exactly `1` (variance = 0.000). Krippendorff's alpha is mathematically defined as 1.0 when there is zero expected disagreement and zero observed disagreement — technically correct, but this reflects a **range-restricted, low-discrimination case**, not strong evidence that D2 reliably separates different credential levels. The real population-wide D2 range is only 0–1 in the frozen annotation to begin with (`Final_Annotation_v1.1_Freeze_Report.md` §4), so this ceiling is a known property of the source data, not new to this reliability check. Treat this alpha as "no disagreement observed," not "high discriminating reliability."

**D3 (α = 0.102, "revise rulebook wording").** The weakest result. Percent agreement is only 54.7% and the two raters' score distributions diverge sharply: Rater A spreads across 0–4 with real mass at 1 and 3 (`{0:1, 1:15, 2:1, 3:24, 4:34}`), while Rater B concentrates almost entirely at 3–4 (`{0:1, 3:10, 4:64}`) — Rater B rarely used the low end of the scale at all. This looks like a genuine **rulebook-application difference** (how strictly "practical AI experience" evidence is read) rather than a fluke: D3 is documented as "medium" verifiability in the dimension config, and unlike D2/D4/D6 it has no unavailable cases in this subset to narrow the comparison — the full 75-profile range is in play, so this is not a low-variance artifact (variance = 1.015, comparable to D1's). This dimension is the strongest candidate for rulebook wording review before any further double coding, per this task's own guidance not to change the scoring criteria but to consider clarifying wording.

**D4 (α = 1.000, "proceed" — read with the same caution as D2).** Perfect agreement again, again on a restricted sample (49 of 75 unavailable, only 26 comparable units, variance 0.391 — low but not zero, since three distinct values (1, 2, 3) do appear and both raters matched on all of them). Somewhat more informative than D2's ceiling case since more than one value is actually being discriminated, but still a small, high-missingness subsample — read as encouraging, not conclusive.

**D5 (α = 0.246, "revise rulebook wording" — this is the difficult dimension the task specifically asks to be discussed carefully).** Percent agreement is actually fairly high (85.3%) — most of the time the two raters land on the same score. But alpha is low, because **variance is extremely low** (0.222, the lowest of any dimension after D2): Rater A scored 68 of 75 profiles as exactly `3` and the other 7 as `2` — an extremely narrow effective range for this subset. Krippendorff's alpha corrects for chance agreement relative to the observed variance, so when almost everyone gets the same score, even a few real disagreements (Rater B additionally used `0` once and `1` five times) are enough to pull a chance-corrected statistic down sharply despite the high raw agreement. This is exactly the "low variance can deflate alpha despite high raw agreement" case this project's own reliability code has flagged as a known risk since it was first built (`krippendorff.py`'s own docstring). **This does not mean D5 is unreliable in the way D3 appears to be** — the raw agreement rate argues against that — but it does mean this particular 75-profile draw did not give D5 enough score variation to produce a trustworthy alpha, and this is compounded by D5 being documented as "low" verifiability in the dimension config (a leadership/strategic-responsibility judgment call is inherently harder to pin to observable text than, say, a listed academic degree). D5's low alpha should be read as *inconclusive due to restricted range*, not as evidence the dimension fails.

**D6 (α = 1.000, "proceed").** Perfect agreement across the full 75-profile subset (no unavailable cases), with real variance (0.889, five of six possible score values represented in Rater A's distribution). Unlike D2/D4, this is not a restricted-sample ceiling case — this is the strongest "proceed" result in the set alongside D1.

## Summary judgment (not a composite, not a ranking — a plain-language recap)

Two dimensions show genuinely strong, well-supported reliability evidence in this subset (**D1, D6**). Two show perfect agreement but on small, low-variance subsamples that should be read cautiously rather than as strong evidence (**D2, D4**). Two show low alpha for different reasons that both fall short of "the dimension doesn't work": **D3** looks like a real rulebook-wording disagreement worth revisiting, and **D5** looks like a range-restriction artifact on top of an inherently harder-to-observe construct. None of this is used to compute, and should never be used to compute, a single reliability figure for ALCSM as a whole — the six results are reported and must remain six separate results.

## What this does not establish

This is one 75-profile subset, one second rater, computed once. It does not establish population-level reliability, does not validate ALCSM's construct validity on its own (that is a separate, content-assessment question — see `07_Reliability/Survey_Analysis/`), and does not justify a composite score, weighting scheme, or classification bands — none of which exist anywhere in this codebase.

---

*Reproducible via `15_Scripts/alcsm_reliability_real_run_v1.0.py`. No canonical source file was modified to produce this report.*
