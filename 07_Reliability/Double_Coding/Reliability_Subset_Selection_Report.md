# Reliability Subset Selection Report

**Status:** Selection complete. **No second-rater scores exist yet** — this document records how the 75-profile double-coding subset was chosen, not any reliability result.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## 1. Method

- **Selection mechanism:** `alcsm.annotation.pilot.select_pilot_subset()` — an existing, already-tested module built in an earlier phase (P4) specifically to implement the frozen double-coding policy ("100% double coding if feasible; otherwise a pre-registered random subset of at least 15%"). Not rewritten for this task; reused as-is.
- **Method:** `random_subset`.
- **Fraction:** `0.15` (the frozen policy minimum, used exactly — not exceeded, not reduced).
- **Seed:** `20260824`, fixed and pre-registered here. Chosen prospectively (the date this reliability package was prepared), never tuned, never resampled to change the outcome.
- **Candidate pool:** all 500 `Profile_ID`s from the frozen `Profile_Scores` sheet of `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` (SHA-256 `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f`), in the row order that sheet already has.
- **Mechanics:** `random.Random(20260824).sample(pool, k=75)` over the 500-element candidate list. This is Python's standard-library sampling, deterministic for a fixed seed and fixed input order.
- **Result:** 75 profiles selected out of 500 candidates — **exactly 15.00%**, no rounding drift.
- **Reproducibility:** anyone with the same frozen annotation file and this script (`15_Scripts/alcsm_reliability_subset_build_v1.0.py`) gets the identical 75 profiles. No manual selection or cherry-picking occurred at any step.

## 2. Exclusions applied — and *not* applied

- **Duplicate Profile_IDs:** not a concern — the candidate pool is already known to contain 0 duplicates (`Final_Annotation_Audit_v1.1.md`).
- **Incomplete records:** not filtered out. The candidate pool is the full 500-profile `Profile_Scores` sheet; every profile in it has a complete 6-dimension record (verified in the same audit), so no profile qualifies as "incomplete" in the first place.
- **Known data-integrity profiles (`LP0041`, `LP0170`, `LP0182`):** **not excluded a priori.** The task instructed against silently distorting the subset by cherry-picking only "easy" profiles, and against excluding known-hard cases without documentation. The correct application of that instruction is to leave these three profiles in the candidate pool exactly like any other profile and let the random draw decide — which is what was done. **As it happens, none of the three was drawn by this seed** (checked explicitly: `{LP0041, LP0170, LP0182} ∩ selected = ∅`). No special handling was therefore required in the resulting workbook. Had one or more been drawn, this report would name it and note that its D3/D6 dimensions carry `unavailable` status for both raters by definition (the second rater would independently confirm unavailability, not invent a score) — the general rule is stated here for completeness even though it wasn't triggered this time.

## 3. Representativeness check

The subset is compared against the full 500-profile population on every field available on `Profile_Scores`, to confirm the sample was not accidentally skewed:

| Dimension | Population mean score | Subset mean score | Population % unavailable | Subset % unavailable |
|---|---|---|---|---|
| D1 | 2.282 | 2.320 | 5.8% | 4.0% |
| D2 | 0.468 | 0.360 | 53.2% | 64.0% |
| D3 | 2.928 | 3.000 | 0.6% | 0.0% |
| D4 | 0.946 | 0.907 | 65.0% | 65.3% |
| D5 | 2.914 | 2.907 | 0.0% | 0.0% |
| D6 | 1.774 | 1.867 | 0.6% | 0.0% |

| Field | Population | Subset (n=75) |
|---|---|---|
| `Overall_Review_Status = CARRIED_FORWARD_REVIEWED` | 93.2% | 96.0% |
| `Overall_Review_Status = FINAL_TARGET_REVIEW_ACCEPTED` | 6.2% | 4.0% |
| `Overall_Review_Status = FINAL_REVIEWED_UNAVAILABLE_RESOLVED` | 0.6% | 0.0% |
| `Researcher_Confidence = MEDIUM` | 71.4% | 76.0% |
| `Researcher_Confidence = LOW` | 28.4% | 24.0% |
| `Researcher_Confidence = HIGH` | 0.2% | 0.0% |
| `Completeness_Index` (mean) | 0.791 | 0.778 |

All deviations are within the range expected for a random draw of n=75 from N=500 (the largest gap is D2's unavailability rate, 53.2% vs. 64.0%, which is ordinary sampling variability for a dimension where unavailability is itself the majority state — not a sign of a biased draw). No dimension, review-status category, or confidence band is over- or under-represented in a way that would distort a reliability estimate. No manual adjustment was made to these proportions; they are reported, not engineered.

## 4. Deliverables produced

| File | Contents | Purpose |
|---|---|---|
| `ALCSM_Reliability_Subset_75_v1.1.xlsx` | `Subset_Roster` (75 Profile_IDs + missing-status flags + data-integrity flag), `Existing_Scores_REFERENCE_ONLY` (the 75 profiles' existing frozen D1–D6 final scores — the primary researcher's own final judgment, i.e. "Rater A" in the two-rater sense described in `Second_Rater_Annotation_Instructions_v1.1.md`), `Selection_Metadata` (this section's method/seed/fraction, machine-readable) | Reference and audit trail. **The second rater must not open the `Existing_Scores_REFERENCE_ONLY` sheet before or during independent coding** — doing so would defeat the purpose of independent double coding. |
| `Rater_A_Blank_Template.xlsx` | Sheet `Independent_Coding`: exactly `Profile_ID, D1, D2, D3, D4, D5, D6`, all score cells blank | The blank instrument to be filled in independently. Despite the filename, it is not pre-populated with the primary researcher's scores — see §5. Duplicate this file (rename appropriately, e.g. `Rater_B_Blank_Template.xlsx`) for each additional independent coder; the structure is identical for any rater. |

## 5. Blank-template column convention (important — also stated in the instructions document)

Per the task's literal specification, the blank template's `Independent_Coding` sheet has **exactly** seven columns: `Profile_ID, D1, D2, D3, D4, D5, D6`. No extra status column was added, to respect that constraint precisely. Instead, the present-vs-unavailable distinction (required by Part 5 of this task) is carried by cell content itself:

- A **blank/empty cell** for a dimension means the rater found **no observable evidence** to score that dimension — i.e., `unavailable`.
- A **written integer 0–5** means the rater scored that dimension from observable evidence, including a genuine, observed score of `0`.

This convention is deliberately simple (no second column to misalign), matches the "leave it blank if you can't observe it" instinct most raters already have, and is exactly what the Part 4 reliability adapter (`src/alcsm/reliability/subset_workflow.py`) expects when it reads a filled-in template — see `Second_Rater_Annotation_Instructions_v1.1.md` §"Recording your scores" for the rater-facing statement of this same rule.

## 6. What this report does not do

- It does not contain any second-rater score — none exists yet.
- It does not compute Krippendorff's alpha, agreement, or any other reliability statistic.
- It does not modify `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` in any way (read-only access only).
- It does not decide who the second rater will be — that is the researcher's decision, outside the scope of this preparatory package.

---

*Next step: hand `Rater_A_Blank_Template.xlsx` (duplicated per rater) and `Second_Rater_Annotation_Instructions_v1.1.md` to each independent coder. Reliability statistics can be computed only once at least one genuinely independent, filled-in template exists.*
