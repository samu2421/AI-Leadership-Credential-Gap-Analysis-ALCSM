# Final Annotation Audit v1.1

**Status:** Independent re-verification, performed fresh against the live file (not copied from `Final_Annotation_v1.1_Freeze_Report.md`, though results are cross-checked against it below). **No modification made to the annotation workbook.**
**File audited:** `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`
**SHA-256:** `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f` — unchanged since the 2026-08-24 freeze; confirmed identical at the start of this audit.
**File lock status:** confirmed not open in Excel (`lsof` clean) before reading.
**Author:** Samiksha Dhere (researcher) — audited with Claude Code assistance

---

## Checklist result

| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | 500 unique Profile_IDs | **PASS** | `Profile_Scores`: 500 rows, `Profile_ID.nunique() == 500`, 0 duplicates. |
| 2 | 3,000 profile×dimension records | **PASS** | `Dimension_Evidence`: shape (3000, 9) = 500 profiles × 6 dimensions. |
| 3 | Exactly six dimensions | **PASS** | `Dimension_Evidence['Dimension'].unique()` = `{D1, D2, D3, D4, D5, D6}`, each with exactly 500 rows — no extra or missing dimension. |
| 4 | Score range 0–5 | **PASS** | `Final_Score.min() == 0`, `Final_Score.max() == 5`; zero rows outside `[0, 5]`. |
| 5 | Valid missingness states | **PASS** | Only `present` (2,374) and `unavailable` (626) appear — both valid states in the frozen four-state framework (`present`, `absent_stated`, `unavailable`, `not_applicable`); the other two states are simply never triggered on the profile side, consistent with prior sessions. |
| 6 | No direct identifiers | **PASS** | Regex scan for email patterns and URL/`linkedin.com` patterns across every text column in all 7 sheets returned zero matches. |
| 7 | No duplicate dimension rows | **PASS** | `(Profile_ID, Dimension)` pair duplication count in `Dimension_Evidence` = 0. (Not explicitly re-verified in the prior Freeze Report by name — confirmed here.) |
| 8 | No unresolved cases | **PASS** | `Unresolved_Cases` sheet: 0 rows. |
| 9 | 28 retained score changes documented | **PASS** | `Review_Changes`: exactly 28 rows, all `Decision == ACCEPT`. Per-dimension breakdown: D5 = 22, D1 = 4, D3 = 2, D2/D4/D6 = 0. Sum = 28. |
| 10 | LP0041, LP0170, LP0182 marked unavailable for D3/D6 | **PASS** | All three: `D3_Final = 0`, `D3_Missing_Status = unavailable`, `D6_Final = 0`, `D6_Missing_Status = unavailable`. Cross-confirmed in `Data_Integrity` (`Issue_Type = MISSING_PROFESSIONAL_EXPERIENCE_SECTION` for all three). |

## Additional cross-consistency checks (beyond the literal checklist)

Performed because `Profile_Scores` and `Dimension_Evidence` store final scores and missing-status redundantly (wide vs. long form), and the two must agree for the file to be internally trustworthy:

- **Final_Score agreement:** for all 500×6 = 3,000 cells, `Profile_Scores.D{n}_Final` vs. the corresponding `Dimension_Evidence.Final_Score` — **0 mismatches**.
- **Missing_Status agreement:** same comparison for `D{n}_Missing_Status` vs. `Dimension_Evidence.Missing_Status` — **0 mismatches**.
- **`Overall_Review_Status` vocabulary:** `CARRIED_FORWARD_REVIEWED` (466), `FINAL_TARGET_REVIEW_ACCEPTED` (31), `FINAL_REVIEWED_UNAVAILABLE_RESOLVED` (3) — sums to 500, no unexpected value.
- **`Researcher_Confidence` vocabulary:** only `LOW` / `MEDIUM` / `HIGH` present, no blanks.
- **`Completeness_Index`:** takes only the six values expected from "how many of 6 dimensions are `present`" (i.e. k/6 for k = 1..6), consistent with its definition — no out-of-range or non-fractional values.

## Result

**The canonical annotation workbook passes every audit item.** No discrepancy was found against the prior `Final_Annotation_v1.1_Freeze_Report.md` (2026-08-24) — this re-verification, performed independently and against the live file rather than by copying that report's figures, reproduces the same counts. The one previously-unstated-by-name item ("no duplicate dimension rows") is now explicitly confirmed.

**The file was not modified.** No cell was written; only read operations were performed.

## Downstream compatibility note (carried forward, relevant to Part 4 of this task)

`src/alcsm/analysis/data_sources.py`'s loaders and `rq1_descriptive.py` were originally built against an earlier review-workbook column shape that included `D{n}_FirstPass` columns and a `D6_Quality_Review` sheet. **Neither exists in this frozen file** — `Profile_Scores` has only `D{n}_Final` + `D{n}_Missing_Status` pairs, and there is no `D6_Quality_Review` sheet. This audit's own verification queries above read the file directly with `pandas.ExcelFile`/`pandas.DataFrame.pivot`, bypassing those loaders entirely, specifically to avoid depending on that unverified compatibility. This gap is not fixed as part of this audit (out of scope for Part 1) but is flagged again here because Part 4's reliability workflow must read this same file correctly — the new reliability adapter built for Part 4 reads `Profile_Scores` and `Dimension_Evidence` directly by their actual column names, not through the older loaders, to sidestep this risk.

---

*This audit is read-only. It authorizes no scoring change, no composite score, and no schema change.*
