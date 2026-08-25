# Reliability Subset Verification v1.2 — Second-Rater Data Integrity

**Status:** Fresh, independent re-inspection of the second-rater source, performed for the FINAL RELIABILITY DIAGNOSIS stage. Supersedes nothing in `Reliability_Subset_Verification_v1.1.md` (that document remains accurate for Part A/B of the prior session) — this document goes deeper specifically on the second-rater encoding question, including checks not previously performed (cell comments, fill colors, number formats).
**File inspected:** `07_Reliability/Double_Coding/ALCSM_Reliability_Subset_75_v1.1.xlsx`, `Subset_Roster` sheet. Open/locked in Excel at inspection time (PID 2096, unchanged from prior session) — read-only inspection only, no write attempted.
**Author:** Samiksha Dhere (researcher) — verified with Claude Code assistance

---

## What was checked, and the exact result

| Check | Result |
|---|---|
| Unique Profile_IDs | **75** (`nunique() == 75`) |
| Total rows | **75** |
| Duplicate Profile_ID rows | **0** |
| Six dimensions present | **Yes** — columns `D1_Missing_Status` … `D6_Missing_Status` (one per dimension; column names retain their original, now-inaccurate header text — see below) |
| Impossible scores (outside 0–5) | **None.** Per-column observed value sets: D1 `{0,1,2,3,4,5}`, D2 `{0,1}`, D3 `{0,3,4}`, D4 `{0,1,2,3}`, D5 `{0,1,3}`, D6 `{0,1,2,3,4}` — every value in every column is a valid integer in `[0,5]`. |
| Missing / blank cells | **None.** Every column is `dtype=int64` (not `float64`), which in pandas is only possible when a column has zero `NaN` values — confirmed directly: `isna().sum() == 0` for all six score columns, all 75 rows. |
| Is "unavailable" explicitly encoded anywhere? | **No.** No text value, no sentinel (e.g. `-1`, `99`, empty string) appears anywhere in the six score columns — every cell is a plain in-range integer. |
| Can a numeric 0 be distinguished from "unavailable" *within this file, using only what is encoded*? | **No.** There is no structural, textual, or numeric marker anywhere in the `Subset_Roster` sheet that separates "rater observed evidence and concluded a score of 0" from "rater found no evidence at all." |
| Cell comments (Excel notes) on any score cell | **0 found**, checked directly via `openpyxl` (`data_only=True`), iterating every cell in the sheet's used range (`A1:G76`). |
| Non-default cell fill colors | **0 found** — no color-coding anywhere in the used range. |
| Custom number formats | **None** — every score cell uses Excel's default `General` format; no custom format that could be hiding a display convention (e.g. blank-displays-as-0) was found. |

**Conclusion of Part 1's structural check: the raw second-rater file, as it exists on disk right now, contains no information of any kind that would allow "unavailable" to be recovered from the file itself.** This is stated as an observed fact about the file, not an assumption — every mechanism Excel offers for encoding a distinction (a different value, a blank cell, a comment, a fill color, a custom format) was checked and found absent.

## Column-naming caveat (unchanged from v1.1, restated for completeness)

The six columns are still headed `D{n}_Missing_Status`, a name inherited from this workbook's original template design (where the sheet held `present`/`unavailable` text). They currently hold plain scores instead. This is a labeling artifact, not a data problem — documented already in `Reliability_Subset_Verification_v1.1.md` Part B, restated here because it is directly relevant to why no "unavailable" encoding was found: the column that was *designed* to hold that information was overwritten with scores instead, at the point the friend's data was entered.

## Reproducing the unavailable-inference logic, separately, from scratch

The prior session's reliability computation treated a cell as the second rater's "unavailable" case if and only if the **primary researcher's own, independently recorded** `Missing_Status` for that same profile × dimension was `unavailable` (`Existing_Scores_REFERENCE_ONLY` sheet, itself a verified, unaltered copy of the frozen annotation). That logic is reproduced here independently, not re-used as a given:

```
for each dimension d in {D1..D6}:
    unavailable_ids = { Profile_ID : Rater_A_Missing_Status[Profile_ID, d] == "unavailable" }
    for pid in unavailable_ids:
        check: does the friend's raw value at (pid, d) equal 0?
```

**Result, computed fresh:**

| Dimension | Rater A unavailable (n) | Friend's raw value at those same cells | Coincidence rate |
|---|---|---|---|
| D1 | 3 | `0` for all 3 | 3/3 = 100% |
| D2 | 48 | `0` for all 48 | 48/48 = 100% |
| D3 | 0 | n/a | n/a |
| D4 | 49 | `0` for all 49 | 49/49 = 100% |
| D5 | 0 | n/a | n/a |
| D6 | 0 | n/a | n/a |

**Total cells affected by this inference: 100 out of 450 profile × dimension cells in the subset — 22.2%.** All 100 fall in D1/D2/D4; **D3 and D5 (this diagnosis's primary focus) are entirely unaffected by the inference** — Rater A recorded zero unavailable cases for D3 or D5 anywhere in this 75-profile subset, so no cell in either dimension was excluded or reinterpreted by the inference logic. This is a directly relevant, load-bearing fact for the rest of this diagnosis: **whatever is causing D3's and D5's low alpha, it is not the missing-data/unavailable-inference mechanism** — that mechanism does not touch either dimension at all in this subset.

## What this means for Part D of this diagnosis (below)

Because the inference is 100%-coincident everywhere it applies, and because it does not apply to D3 or D5 at all, this document's finding is: **the second-rater encoding limitation is real and worth stating plainly in the thesis, but it structurally cannot be the explanation for D3's or D5's low reliability.** Any diagnosis of D3/D5 must look elsewhere — see `RQ3_Reliability_Final_Interpretation_v1.0.md` and the disagreement analysis in `D3_D5_Disagreement_Analysis_v1.0.xlsx`.

---

*Read-only inspection. No cell in the second-rater workbook was modified. No unavailable status was silently assumed anywhere in this document — every inference is shown with its exact inputs, outputs, and coverage above.*
