# Reliability Subset Verification v1.1

**Status:** Verification of the double-coding subset's integrity, performed at the start of the FINAL RELIABILITY AND ANALYSIS session, before any reliability computation. Documents both the subset-selection check (Part A) and the second-rater data recovery (Part B).
**Author:** Samiksha Dhere (researcher) — verified with Claude Code assistance

---

## Part A — Subset selection integrity

**Workbook state before touching anything:** `07_Reliability/Double_Coding/ALCSM_Reliability_Subset_75_v1.1.xlsx` was open and locked in Excel (`lsof` confirmed, PID 2096) at the start of this session, same as reported at the end of the prior session. It was read-only inspected (never written to) while in this state.

**Prior-session anomaly status:** the prior session reported the `Subset_Roster` sheet had dropped to 50 rows while the file was open in Excel. On inspection this session, the sheet was back to **75 rows** — the researcher had continued working in the file between sessions.

**Verification performed:**

| Check | Result |
|---|---|
| Unique profiles in `Subset_Roster` | **75** (`Profile_ID.nunique() == 75`) |
| Duplicate `Profile_ID` rows | **0** |
| Matches deterministic seed-20260824 selection | **Yes — exact match.** Re-ran `select_pilot_subset(candidate_ids, method="random_subset", seed=20260824, fraction=0.15)` against the 500 `Profile_ID`s in `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`'s `Profile_Scores` sheet (unchanged, same SHA-256 as every prior check). The resulting 75-ID set is byte-for-byte identical to the `Subset_Roster` sheet's `Profile_ID` column — 0 IDs in one set and not the other, in both directions. |
| Fixed seed | `20260824`, unchanged from the prior session, still hard-coded in `15_Scripts/alcsm_reliability_subset_build_v1.0.py`. |
| Reproducibility | Confirmed by the exact re-match above — no manual edit to the selected IDs occurred. |
| Known data-integrity profiles (`LP0041`, `LP0170`, `LP0182`) | **Not present in the subset** — consistent with the original selection (the deterministic draw simply did not select them; this was already reported in `Reliability_Subset_Selection_Report.md` §2 and is unchanged since no re-selection occurred). |

**Conclusion: no regeneration was necessary.** The 75-profile roster is exactly the deterministic, reproducible, seed-20260824 selection. **No profile ID was manually changed.**

**What was found altered instead:** the six `D{n}_Missing_Status` columns on the same `Subset_Roster` sheet no longer contain their original `present`/`unavailable` text — see Part B below.

---

## Part B — Locating and verifying the friend's second-rater scores

**Search performed:** repository-wide (`find . -iname "*rater*" -o -iname "*second*" -o -iname "*friend*" -o -iname "*reliability*subset*"`, excluding `.git`/`.venv`), plus `~/Downloads`, `~/Desktop`, and `~/Documents` (shallow). No file with a name suggesting a dedicated second-rater or "friend" export was found anywhere. `Downloads` contains only files already known from prior sessions (old annotation drafts, survey export, job-requirement-mapping drafts) — none new, none matching a completed second-rater shape.

**`Rater_A_Blank_Template.xlsx`** (the file this project's own instructions actually direct a second rater to fill in) was checked directly: still **completely blank** (0 non-null values in any of D1–D6, across all 75 rows).

**The only candidate found:** `ALCSM_Reliability_Subset_75_v1.1.xlsx`'s `Subset_Roster` sheet. Its six columns headed `D1_Missing_Status` … `D6_Missing_Status` — which should hold the text values `present`/`unavailable` — instead hold plain integers in the 0–5 range (dtype `int64`, zero nulls in any column). This is genuinely ambiguous on its face: it could be the friend's scores typed into the wrong sheet/columns, or unrelated corruption.

**Evidence considered before asking:**

1. **Not a copy of the researcher's own scores.** Compared cell-by-cell against `Existing_Scores_REFERENCE_ONLY` (this workbook's own untouched copy of the researcher's frozen scores for these 75 profiles, itself re-verified as 0 mismatches against the canonical annotation file). Result: **93 of 450 cells differ** — D1: 16 differ, D2: 0 differ, D3: 61 differ, D4: 0 differ, D5: 16 differ, D6: 0 differ. Not identical, so not a simple duplicate.
2. **Pattern consistent with independent rating, not random corruption.** All 450 values fall within each dimension's valid 0–5 range (no out-of-range or nonsensical values); the split between dimensions with zero disagreement (D2, D4 — narrow, low-ambiguity dimensions in this project's own rubric) and dimensions with substantial disagreement (D1, D3, D5 — broader or more judgment-dependent dimensions) is exactly the shape genuine second-rater data is expected to take, not the shape of a random paste error.

**This was still reported as an ambiguity rather than assumed** — the researcher was asked directly whether this is the friend's independent scoring. **Confirmed: yes.** Proceeding on that basis.

### The missing-data problem this recovery creates, and how it was resolved

The friend's data, as recovered, has **no way to represent "unavailable" separately from an observed score of 0** — every one of the 450 cells is a plain integer, no blanks, no sentinel value. This directly collides with this project's standing rule (documented since the prior session's Part 5, restated in this session's Part C) that unavailable cases must never be coerced into a disguised 0.

**Resolution, verified empirically before being applied:** for every profile × dimension cell where the **primary researcher's own, independently recorded** `Missing_Status` is `unavailable`, the friend's corresponding entry is **exactly `0`, with zero exceptions**:

| Dimension | Rater A `unavailable` count in subset | Friend's value for those same cells |
|---|---|---|
| D1 | 3 | `0` — 3/3 |
| D2 | 48 | `0` — 48/48 |
| D4 | 49 | `0` — 49/49 |
| D3, D5, D6 | 0 (no unavailable cases in this subset for these dimensions) | n/a |

This 100%-coincidence pattern, together with the fact that "unavailable" in this project's rubric is defined as a structural property of the source profile (e.g., no `Professional_Experience` section exists at all) rather than a subjective per-rater judgment, supports treating these coinciding cells as the friend's unavailable cases too. **This is an explicit, disclosed interpretive decision, not fabricated data** — every excluded cell is excluded strictly because the primary researcher's own independently made determination says so.

**Stated limitation (carried into `Reliability_Report_v1.1.md`):** any case where the friend privately regarded a dimension as unobservable but wrote `0` anyway, *without* that coinciding with Rater A's own unavailable flag, cannot be detected from this recovered file and would be silently counted as an observed score of 0. Given the 100% coincidence found on every dimension where the primary researcher recorded any unavailable case at all, this residual risk is assessed as low but is not zero, and is reported as a limitation rather than dismissed.

**Implementation:** `15_Scripts/alcsm_reliability_real_run_v1.0.py`, fully commented with the same reasoning as this document.

---

*Both parts verified; no manual edit was made to any Profile_ID or score value. Part C's reliability computation proceeds on the data as recovered and documented here.*
