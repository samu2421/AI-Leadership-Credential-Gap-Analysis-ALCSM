# Final Annotation v1.1 — Freeze Report

**Status:** The ALCSM v1.1 researcher-reviewed annotation dataset is frozen as the canonical analytical scoring baseline for all downstream work (reliability, RQ1–RQ5 analysis, NLP evaluation).
**Author:** Samiksha Dhere (researcher) — verified with Claude Code assistance
**Date:** 2026-08-24

---

## 1. Source

| Field | Value |
|---|---|
| Canonical path | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` |
| SHA-256 | `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f` |
| File size | 343,576 bytes |
| Provenance | Placed into the canonical path from two byte-identical copies found in the researcher's `Downloads/` folder (`ALCSM_Final_Human_Annotation_v1.1.xlsx` and `ALCSM_Final_Human_Annotation_v1.1 (1).xlsx` — a duplicate download, same SHA-256, no discrepancy). The stale, incomplete draft previously sitting at this path in the repository (`ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx`, unchanged since 2026-08-17, `Overall_Review_Status` still showing `Pending Review` for most rows) has been superseded and archived — see §7. |
| Git status | Git-ignored (`06_Annotation/*.xlsx`), never committed, never will be — consistent with this project's standing rule that real personal data never enters version control. |

**This file was not modified by this session in any way.** It was copied into place and read-only verification was performed against it; no cell, sheet, or structural element was altered.

## 2. Structure verified

| Sheet | Shape | Role |
|---|---|---|
| `Profile_Scores` | 500 × 17 | One row per profile: `D1_Final`…`D6_Final`, `D1_Missing_Status`…`D6_Missing_Status`, `Completeness_Index`, `Overall_Review_Status`, `Researcher_Confidence`, `Notes` |
| `Dimension_Evidence` | 3,000 × 9 | One row per profile × dimension: `Final_Score`, `Evidence`, `Rationale`, `Missing_Status`, `Confidence`, `Decision`, `Reviewer_Notes` |
| `Review_Changes` | 28 × 11 | Every case where the researcher's final score differs from the AI-assisted first pass (see §5) |
| `Unresolved_Cases` | 0 × 9 | Empty — no case remains unresolved |
| `Data_Integrity` | 6 × 10 | 3 rows for the Professional-Experience-missing profiles (`MISSING_PROFESSIONAL_EXPERIENCE_SECTION`) + 3 `GLOBAL` rows (`STRUCTURAL_QA`, `SOURCE_PRESERVATION`) |
| `Score_Distribution` | 35 × 8 | Descriptive counts/percentages per dimension — no composite, no weighting |
| `Method_Notes` | 16 × 3 | Documented rules/decisions governing the review pass |

**Note on structure:** this workbook's sheet and column layout differs from the intermediate `ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` built during the P4-preparation session (different column names, an added `Unresolved_Cases`/`Data_Integrity` sheet, no separate `Adjudication_Log`/`D6_Quality_Review`/`Review_Queue` sheets). This reflects independent continued development of the review workbook after that session; the file described in this report is treated as authoritative as delivered, not reconciled against the earlier design.

## 3. Verification checklist (all passed)

| Check | Result |
|---|---|
| 500 unique profiles | ✅ `Profile_Scores.Profile_ID.nunique() == 500`, no duplicates |
| 3,000 dimension rows | ✅ `Dimension_Evidence` shape (3000, 9) |
| 6 dimensions per profile | ✅ every `Profile_ID` has exactly 6 distinct `Dimension` values |
| D1–D6 only | ✅ `Dimension_Evidence.Dimension` values are exactly `{D1, D2, D3, D4, D5, D6}` |
| Scores 0–5 | ✅ every `D{n}_Final` column and `Dimension_Evidence.Final_Score` fall within [0, 5] |
| No unresolved cases | ✅ `Unresolved_Cases` sheet is empty (0 rows) |
| No direct identifiers / LinkedIn URLs / emails / names | ✅ regex scan (`linkedin\.com`, `https?://`, `www\.`, email pattern) across every text column in every sheet: **0 matches**; no column header matches a name/url/email/phone pattern |
| Missingness correctly represented | ✅ only `present` and `unavailable` values appear (the four-state framework's other two states, `absent_stated`/`not_applicable`, are legitimately unused — consistent with the first-pass annotation, which never triggered them either) |
| LP0041, LP0170, LP0182 marked unavailable for D3/D6 | ✅ confirmed directly: all three show `D3_Missing_Status = unavailable`, `D6_Missing_Status = unavailable`, `D3_Final = 0`, `D6_Final = 0` |
| No composite score | ✅ no column matching `composite`/`total`/`alcsm_score` anywhere in `Profile_Scores` |
| No weighting | ✅ no weight column or weighted-sum logic anywhere in the workbook |
| No classification band | ✅ no band/threshold column; `Score_Distribution` is raw counts/percentages only |

## 4. Score distributions (D1–D6, final)

| Score | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|
| 0 | 122 | 266 | 4 | 325 | 3 | 6 |
| 1 | 40 | 234 | 105 | 4 | 12 | 239 |
| 2 | 67 | 0 | 4 | 44 | 30 | 155 |
| 3 | 134 | 0 | 197 | 127 | 435 | 67 |
| 4 | 120 | 0 | 190 | 0 | 20 | 28 |
| 5 | 17 | 0 | 0 | 0 | 0 | 5 |

Read as descriptive fact only — no interpretation, no composite, no weighting is derived from this table here. (For comparison against the pre-review first-pass distribution and fuller discussion of the D2/D4 range-capping already documented in the first-pass `Method_Notes`, see `Analysis_Preparation_Completion_Report.md` §4, which used the provisional predecessor of this file.)

## 5. Missingness handling

Two missing-status values are used throughout: `present` (evidence was found and scored on its merits, including a genuine zero finding) and `unavailable` (the underlying data section could not be observed at all). This matches the frozen four-state framework's `present`/`unavailable` states exactly; `absent_stated` and `not_applicable` are valid but unused states for this profile-side dataset, consistent with the first-pass annotation's own behavior.

**The three Professional-Experience-missing profiles** (`LP0041`, `LP0170`, `LP0182`) — first identified in the P4-preparation session and structurally verified again here — are correctly and consistently marked `unavailable` for both D3 and D6, with a corresponding `Data_Integrity` sheet entry for each (`Issue_Type = MISSING_PROFESSIONAL_EXPERIENCE_SECTION`). This is the same open interpretive question flagged in `ALCSM_Coding_Rulebook_v1.1_Addendum.md` §5 (whether zero experience reflects a genuine finding or a collection gap) — the researcher's resolution, as reflected in this frozen file, is to record it as `unavailable` (a data gap), not `present`/score-0 (a genuine finding). This is the researcher's own considered decision, recorded here as fact, not revisited or second-guessed by this report.

## 6. The 28 historical score changes

`Review_Changes` contains exactly 28 rows, each recording a case where the researcher's final judgment differed from the AI-assisted first pass, with `FirstPass_Score`, `Final_Score`, `Decision`, `Evidence`, `Reason`, `Governing_Rule`, `Precedent`, `Confidence`, and `Reviewer_Notes` columns present for every row — a complete audit trail from first-pass to final for every changed case. This report does not reproduce the 28 rows' content (some contain evidence-text fields that this report's own "no raw evidence in governance documents" discipline keeps out of prose reports); the count and structural completeness are verified and recorded here as the auditable fact.

## 7. Superseded predecessor, archived

`ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` (the incomplete intermediate workbook built during the P4-preparation session, `Overall_Review_Status` still `Pending Review` throughout) has been moved to `16_Archive/Superseded_Annotation_Drafts/ALCSM_Final_Human_Annotation_v1.1_REVIEW_incomplete_20260817.xlsx` — preserved for audit continuity, not deleted, and no longer read by any active tooling. A second, structurally distinct precursor draft (`ALCSM_Processed_Reviewed_v1.1.xlsx`, found at the repository root, with per-dimension review sheets `D1_Detailed_Review`/`D2_Review`/`D3_D5_Review`/`D6_Review` not present in the final consolidated file) has likewise been archived alongside it — see `11_Implementation_Governance/Reviews/Repository_Cleanup_Report.md` for the full cleanup record.

## 8. Freeze statement

**The annotation dataset at `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` (SHA-256 `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f`) is frozen as the canonical analytical scoring baseline.** No ALCSM dimension, scoring criterion, or D6 definition was changed to produce this freeze — this report only verifies and records what the researcher's completed review already established. This file must not be modified going forward; any further correction is a new, separately-versioned event, not an edit to this one.

**Not authorized by this report:** any composite score, weighting scheme, or classification band (none exist in this file and none should be added); NLP training or statistical analysis (a separate, later task); any change to D1–D6 or their scoring criteria.

---

*This report records a verification and freeze of existing, already-completed researcher work. It performs no scoring, no methodology change, and no modification to the source file.*
