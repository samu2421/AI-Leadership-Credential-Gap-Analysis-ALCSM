# Human Annotation Review Protocol v1.1

**Version:** 1.1
**Status:** Operational protocol, describing how to work in `ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx`. Does not itself constitute annotation, adjudication, or dataset freeze.
**Governs:** the researcher-review layer converting `ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` (AI-assisted first pass, 500 profiles, 3,000 profile×dimension records, unmodified and permanently read-only) into the final human-reviewed ALCSM dataset.
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Date:** 2026-08-17

---

## 1. Purpose and scope

The first-pass workbook applies the frozen v1.0 rubric (D1–D5) and the proposed v1.1 rubric (D6, `ALCSM_D6_Industry_Breadth_v1.1.md`, status PROPOSED/PILOT_REQUIRED) mechanically and conservatively against `ALCSM_LinkedIn_Processed_v1.1.xlsx`. It is a disciplined starting point, not a human gold standard: no LinkedIn browsing, no web research, no prestige assumptions, default-low under uncertainty throughout (its own `Method_Notes` sheet documents this in full).

This protocol governs the single remaining step before any score can be treated as final: **researcher review of every flagged case**, producing an audit trail of what was accepted as-is, what was changed and why, and what remains deferred. It does not redesign any dimension, does not change scoring criteria, does not calculate a composite score, and does not modify the source workbook.

## 2. The two workbooks and their relationship

| Workbook | Role | Mutability |
|---|---|---|
| `06_Annotation/ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` | Baseline first-pass annotation | **Permanently read-only.** Never opened for editing during review. Verified byte-identical (SHA-256) to the file as received, both before this review workbook was built and as an ongoing check any time it is reason to suspect drift. |
| `06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` | Researcher-review layer | The only file the researcher edits during review. |

Both are git-ignored (`06_Annotation/*.xlsx`), consistent with this project's standing rule that workbooks containing real profile-derived data are never tracked in version control.

## 3. Workbook structure (8 sheets)

`ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` contains:

1. **Profile_Scores** (500 rows) — one row per profile, First-Pass and Final columns side by side for all six dimensions.
2. **Dimension_Evidence** (3,000 rows) — one row per profile×dimension, carrying the first-pass evidence/rationale forward alongside a Final_Score and a reviewer decision.
3. **Review_Queue** (685 rows / 425 profiles) — the working triage list of everything requiring researcher attention, prioritized HIGH/MEDIUM.
4. **Review_Changes** (0 rows, header only) — populated only as the researcher actually changes scores; the permanent audit trail.
5. **Adjudication_Log** (0 rows, header only) — for cases escalated beyond the primary researcher's own review (see §8).
6. **D6_Quality_Review** (500 rows) — a dedicated D6 diagnostic table, added beyond the six sheets named in the original task list because Task 8's required columns and flag conditions do not fit inside Dimension_Evidence's fixed structure without overloading it; this addition is documented, not silent.
7. **Score_Distribution** — first-pass score counts and percentages per dimension, descriptive only.
8. **Method_Notes** — the rules and constraints this workbook was built under, and the specific evidentiary basis for each.

## 4. Profile_Scores and Dimension_Evidence: the Final-value convention

Every `D1_Final`…`D6_Final` value in `Profile_Scores`, and every `Final_Score` in `Dimension_Evidence`, is **initialized equal to the first-pass value**. This is a starting point, not an acceptance: a score is *not* final because it appears in the `_Final` column, it is final once the researcher has reviewed it (directly, or by virtue of not being flagged — see §5) and no `Review_Changes` row exists changing it. A researcher who changes a `_Final` value must add a corresponding row to `Review_Changes` (§7) in the same sitting — the two must never drift apart.

## 5. Review_Queue: population logic

Not every one of the 3,000 profile×dimension records needs researcher attention — most first-pass scores are confidently and correctly resolved by the rubric alone. The queue is built from the union of five conditions, each checked directly against the first-pass data rather than assumed:

| # | Condition | Rows contributed | Note |
|---|---|---|---|
| (a) | First-pass `Review_Required = YES` | 675 | The annotator's own flag, already covering precedent-governed boundary cases (P-02/P-03 title/scope calls), date-sensitive certifications, degree-tier boundaries, and ambiguous-record cases. |
| (b) | `Confidence = LOW` | 0 new | Strict subset of (a) in this dataset — verified directly, not assumed: every LOW-confidence row is already `Review_Required = YES`. |
| (c) | `Missing_Status = unavailable` **and** genuinely uncertain (`Confidence != HIGH`) | 0 new | Also a strict subset of (a) — verified: of 626 `unavailable` rows, 591 are HIGH-confidence with `Review_Required = NO` (a genuinely resolved zero-evidence case, e.g. "no certifications listed" → confidently 0) and the remaining 35 are LOW-confidence and already in (a). See §6 for why the 591 are deliberately excluded. |
| (d) | D6 industry classification touches a deliberately-unmerged ambiguous industry label (`ALCSM_D6_Industry_Breadth_v1.1.md` §6) | 1 new | LP0037's D6 row — the only case where a label-level ambiguity exists but the annotator's confidence was high enough that (a)/(b)/(c) didn't already catch it. |
| (e) | Profile is one of the three Professional_Experience-missing profiles (§7 below) | 9 new | All six dimension rows for LP0041, LP0170, LP0182 are surfaced together, not only the three-per-profile the automated flag individually caught. |

**Total: 685 rows across 425 unique profiles.**

Each row carries `Priority` (HIGH/MEDIUM), `Review_Reason` (concatenated from the data-integrity flag, the D6-ambiguity flag, and/or the first-pass annotator's own reason text where applicable), `Data_Integrity_Issue` (TRUE/FALSE), and blank `Reviewer_Decision`/`Reviewer_Notes`/`Reviewer`/`Review_Date` fields for the researcher to complete.

## 6. Why the queue does not include all "unavailable" rows

A literal reading of "missingness affects the score" could be taken to mean every row where `Missing_Status = unavailable` (626 rows) belongs in the queue. This was deliberately not done. Of those 626 rows, 591 are cases where the annotator found no evidence at all — most commonly D2 (no certifications listed, 266 rows) and D4 (no discoverable technical output, 325 rows) — and recorded HIGH confidence in the resulting score of 0, because there genuinely is nothing ambiguous about "no evidence found → score 0" in those cases. Queuing all 591 would directly contradict the explicit "do not create unnecessary review work" instruction while adding no real decision for the researcher to make. The queue instead includes only the 35 `unavailable` rows where the annotator's own confidence was not HIGH — i.e., where missingness plausibly *does* affect whether the recorded score is right — and these were already present via condition (a).

## 7. The three Professional_Experience-missing profiles

**LP0041, LP0170, LP0182** have zero `Professional_Experience` rows in `ALCSM_LinkedIn_Processed_v1.1.xlsx` — verified directly against the processed workbook for this protocol, not taken on the first-pass annotation's own word (though its `Method_Notes` independently flagged the same finding). All 18 Dimension_Evidence rows for these three profiles (6 dimensions × 3 profiles) are placed in `Review_Queue` at **HIGH priority** with `Data_Integrity_Issue = TRUE`, regardless of whether the individual dimension row had already tripped a first-pass flag.

**The issue, stated precisely:** it cannot be determined from the processed dataset alone whether a profile with zero experience rows reflects (a) a genuine finding — the person's LinkedIn profile listed no professional experience — or (b) a collection gap — the Professional_Experience section was not successfully retrieved for that profile at collection time. This is exactly the open question `ALCSM_Coding_Rulebook_v1.1_Addendum.md` §5 already flags for D6 specifically, now confirmed to affect D3 as well (both dimensions read from the same section). The first-pass annotation defaulted these profiles' D3 and D6 (and D1/D5 for two of the three) to `unavailable`, which is a defensible conservative choice but not a settled one. **No score for these three profiles has been changed by this workbook.** Resolving the ambiguity (checking the raw collection record, or the original LinkedIn profile if still accessible) is a researcher decision, to be recorded in `Review_Changes` if it results in a score change, or in `Reviewer_Notes` if the `unavailable` status is confirmed and retained.

## 8. Reviewer_Decision values and workflow

Each queued row's `Reviewer_Decision` (a dropdown in both `Dimension_Evidence` and `Review_Queue`) takes exactly one of:

- **ACCEPT** — the first-pass score is correct as-is. No change to `_Final`; no `Review_Changes` row.
- **CHANGE** — the first-pass score is wrong or needs adjustment. The researcher updates the corresponding `_Final` field(s) in `Profile_Scores`/`Dimension_Evidence` **and** adds a row to `Review_Changes` (§9) in the same sitting.
- **DEFER** — the researcher cannot resolve the case alone (e.g., it requires supervisor input, or a pilot-stage rubric clarification). The score is left at its first-pass value and the case is logged in `Adjudication_Log` (§10) rather than closed.

Reviewing a profile's six dimensions together (rather than one dimension across many profiles) is recommended, consistent with `ALCSM_Coding_Rulebook_and_Pilot_Design.md` §1.2's sequential-context-bias caution and this project's established "one profile visit, all relevant dimensions" principle from `Supplementary_Evidence_Collection_Protocol_v1.0.md` §3.

## 9. Review_Changes: the audit trail

Populated **only** when a `_Final` value is actually changed from its first-pass value. Every row must cite:

- `Change_Reason` — what evidence or reasoning justifies the change, in the reviewer's own words.
- `Governing_Rule` — the specific frozen rubric clause (`ALCSM_v1.1_Scoring_Framework.md` §1) or D6 v1.1 addendum clause (`ALCSM_Coding_Rulebook_v1.1_Addendum.md`) the change applies.
- `Precedent` — a precedent ID (P-01…P-15) if one governs the case, or "none."

This mirrors the revision-log discipline already established in `ALCSM_Coding_Rulebook_and_Pilot_Design.md` §2.6: a defensible audit trail an examiner can follow from any changed score back to the specific rule that changed it. A score changed without a corresponding `Review_Changes` row is a protocol violation, not a shortcut.

## 10. Adjudication_Log: escalated cases

Used only for **DEFER** cases the researcher cannot resolve alone — for example, a genuinely novel D5/D6 boundary situation not covered by the existing tie-breaking rule (`ALCSM_Coding_Rulebook_v1.1_Addendum.md` §9), or a case requiring supervisor input before the researcher will commit to a score. Fields (`Issue_Type`, `Escalated_By`, `Adjudicator`, `Adjudicated_Score`, `Adjudication_Reasoning`, `Precedent_Applied`) mirror the escalation structure already established in `ALCSM_Coding_Rulebook_and_Pilot_Design.md` §1.5 Rule 3, adapted from a two-rater pilot context to this single-pass researcher-review context. An adjudicated case that results in a score change still requires a corresponding `Review_Changes` row — the two logs are not substitutes for each other.

## 11. D6_Quality_Review: dimension-specific diagnostics

One row per profile (500 total), carrying `AI_Related_Industry_Count`, `Normalized_Industry_List`, `D6_FirstPass`, and `D6_Review_Required`, plus seven independently-computed flags: zero AI-related industries (6 profiles), partial industry missingness (31 profiles — has usable AI-related industry evidence but at least one AI-related row's industry is unusable), ambiguous industry label (4 profiles — LP0036/37/38/40, touching a deliberately-unmerged label per `ALCSM_D6_Industry_Breadth_v1.1.md` §6), duplicate-normalization collapse (1 profile — LP0038, where two raw industry strings for the same profile were merged into one by the normalization table), potential D3/D6 overlap (22 profiles with both D3≥4 and D6≥4 — a prompt to double-check depth and breadth aren't being conflated, not evidence of an actual error), unusually high breadth (5 profiles at the D6=5 ceiling), and rubric inconsistency (verified FALSE for all 500 profiles — every `D6_FirstPass` value was recomputed and confirmed to equal `min(distinct normalized AI-related industry count, 5)`). No score is changed by this sheet; it exists to focus the researcher's D6-specific attention efficiently rather than requiring a manual re-derivation of these patterns.

## 12. Score_Distribution

Descriptive only — first-pass score counts and percentages per dimension, unmodified from what the first-pass annotation actually produced. No weights, no `ALCSM_Total`, no classification bands. **This table must never be used as a target.** A score is changed because the evidence and the governing rule justify it, never because the resulting distribution looks more even, more expected, or more publishable. Any researcher tempted to adjust a borderline case "to balance the distribution" should treat that impulse itself as a signal to stop and re-read the evidence, not act on it.

## 13. Data safety

Verified for this workbook specifically (not assumed from prior sessions):

- No LinkedIn URL, name, or email pattern found in any Evidence/Rationale/D6_Rationale text field across all 3,000 Dimension_Evidence rows and 500 D6_Industry_Detail rows (regex-scanned).
- No column in either workbook is named or contains direct identifiers; `Profile_ID` (`LP####`) is the only per-individual key, consistent with this project's pseudonymization convention throughout.
- `ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` confirmed byte-identical (SHA-256) to the file as originally provided; this review workbook's creation did not alter it.
- Both workbooks are git-ignored (`06_Annotation/*.xlsx`, confirmed via `git check-ignore -v`); neither has ever been staged or committed.

## 14. What this protocol does not authorize

- No dimension is redesigned, and no scoring criterion is changed automatically — every change flows through §9's `Review_Changes` audit trail, tied to an existing governing rule.
- No composite score, weight, or classification band is calculated anywhere in this workbook.
- No NLP work is started.
- No statistical relationship (correlation, reliability statistic, etc.) is calculated as part of this review layer.
- The dataset is not frozen by this protocol or by completing a review pass through the queue — freezing is a separate, later, explicitly-authorized step.
- D6 remains PROPOSED/PILOT_REQUIRED (`DECISION_LOG.md` D-0038) throughout this review; researcher review of D6 first-pass scores does not itself constitute the pilot or a freeze decision for the v1.1 rubric.

---

*This protocol governs the researcher-review workflow only. It does not alter `ALCSM_Measurement_Specification_v1.0.md`, `ALCSM_v1.1_Scoring_Framework.md`, `ALCSM_Coding_Rulebook_and_Pilot_Design.md`, `ALCSM_Coding_Rulebook_v1.1_Addendum.md`, the frozen schema, or any other historical methodology document.*
