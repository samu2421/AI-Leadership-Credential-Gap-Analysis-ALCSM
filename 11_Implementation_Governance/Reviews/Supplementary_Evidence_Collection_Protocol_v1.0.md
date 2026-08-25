# Supplementary Evidence Collection Protocol

**Version:** 1.0
**Status:** Operational protocol, approved for use. Governs manual use of `ALCSM_Supplementary_Evidence_Collection_v1.0.xlsx`. Does not itself constitute P4 annotation and assigns no ALCSM score.
**Purpose:** document how the researcher performs the one combined manual supplementary evidence review per profile, so the process is transparent, reproducible, and auditable independent of the workbook itself.
**Last Updated:** 2026-08-17
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

---

## 1. Purpose

This protocol governs the manual, researcher-performed step between data preparation (complete, per `Pre_P4_Data_Readiness_Status.md`) and P4 annotation (not yet begun): collecting the specific supplementary evidence the approved triage (`ALCSM_Supplementary_Evidence_Triage_v1.0.xlsx`) identified as missing, for the 500 included profiles, using the operational workbook `ALCSM_Supplementary_Evidence_Collection_v1.0.xlsx`.

## 2. Scope

**In scope:** manually reading a profile's public page and recording evidence for the specific dimensions the triage flagged for that profile; recording D6 activity observations for all 500 profiles under the finalized 12-month rule. **Out of scope:** assigning any ALCSM 0–5 score (no scoring field exists anywhere in the collection workbook); modifying `01_Raw/` or `02_Processed/`; annotating under the frozen Coding Rulebook/Annotation Handbook (that is P4); external web research beyond the profile's own public LinkedIn page, except where D4 verification is explicitly used (D4-only, confirm-or-lower only, per the frozen rule — and moot for the current triage, since 0 profiles are D4-flagged).

## 3. One-visit-per-profile principle

`Profile_Evidence_Collection` gives every profile exactly one row, carrying all six dimensions' required-flags and evidence fields together. The researcher opens a flagged profile's public page **once** and records everything relevant — whichever of D1–D5 the triage flagged for that profile, plus the D6 observation every profile needs — in that single visit, rather than revisiting the same profile once per dimension. This mirrors the same principle the Annotation Handbook already applies at P4 ("show one profile's six dimensions together") and reduces both researcher effort and the chance of drifting standards across repeated partial visits to the same profile.

## 4. D1–D5 targeted-review rule

Only the profiles the approved triage marked `additional_review_needed = Yes` require action for that dimension:

| Dimension | Profiles flagged | Basis |
|---|---|---|
| D1 — Formal Education | 17 | Missing/unknown degree level or field where the applicable band can materially change |
| D2 — Professional Certifications | 64 | Issue/renewal/expiry date needed for date-sensitive certifications |
| D3 — Practical AI Experience | 9 | Missing AI-role duration or current-role timing at a boundary case |
| D4 — Technical Contributions | 0 | No mandatory supplementary evidence identified in this triage pass |
| D5 — Leadership & Strategic Responsibility | 2 | Title/substance or positional-scope cases not resolvable conservatively from existing structured data |

For every other profile, that dimension's field is pre-marked "No" in `Profile_Evidence_Collection` and requires no reviewer action. This is a deliberate, MSc-appropriate scope decision, not an oversight: it targets effort at cases where the existing structured evidence genuinely cannot distinguish the applicable rubric band, rather than re-verifying every profile on every dimension.

## 5. D6 12-month rule

Per `DECISION_LOG.md` D-0037, applied to all 500 profiles:

- **Window:** 12 months immediately preceding the profile's `collection_ts` (pre-computed in both `Profile_Evidence_Collection` and `D6_Observation_Log`).
- **Qualifies:** publicly visible original posts; publicly visible reshares/reposts; visible professional commentary; publicly stated community/professional roles; continuing-development signals where publicly stated and presented as engagement.
- **Excluded:** follower counts, connection counts, reach metrics, inferred engagement, private/connection-only content, non-LinkedIn activity not presented on LinkedIn.

## 6. Observed absence vs. unavailable

`D6_Observation_Log.Missing_Status` takes exactly one of two values, and they are never collapsed into each other:

- **`present`** — the activity surface **was** viewable and assessed within the window, and a genuine finding was made (whether or not any qualifying activity was actually present). An empty-but-observed feed is `present`, not `unavailable` — it is confirmed information, not a data gap.
- **`unavailable`** — the activity surface itself **could not be viewed** under the approved public-access method. This is a data gap, distinct from a confirmed absence, and must never be read as "this person doesn't engage."

This is the same distinction established in `D6_Observation_Rule_Decision_Proposal.md` §5, applying the existing four-state missing-data framework to activity observation — restated here for the reviewer's direct operational use.

## 7. Evidence recording conventions

- Quote or closely paraphrase what is actually observed on the profile; never invent, infer, or assume evidence.
- Cite where the evidence was found (`*_Source_Note` fields, or `Evidence_Note` in the D6 log) — which processed field, or which part of the observed activity surface.
- Leave a field blank rather than guess. A blank field is honest; a guessed one is not.
- For D2 recency specifically: if the certification's date genuinely cannot be observed, record the literal marker `RECENCY_NOT_AVAILABLE` rather than leaving an ambiguous blank — this keeps "checked, not found" distinguishable from "not yet checked."
- For D4 (not currently triggered by any profile in this triage, but documented for completeness): external verification may only **confirm or lower** what the profile text already supports, never raise a score above it — the frozen D4-only verification rule, unchanged here.
- D6 counts (`Original_Posts_Count`, `Reshares_Count`, `Visible_Comments_Count`) are counted manually by the reviewer within the fixed window. Nothing in the workbook auto-populates or infers a count.

## 8. Researcher responsibilities

- Work only from the profiles/dimensions the approved triage flagged; do not "reopen" an unflagged dimension on a whim (consistent with the "do not reopen profiles unnecessarily" scoping principle).
- Update `Review_Status` (`Not Started` / `In Progress` / `Completed` / `Unable to Verify`) and `Review_Date` as work proceeds, so `Progress_Dashboard` reflects real state when recalculated.
- Never copy a name, profile URL, email, or phone number into any field of this workbook, consistent with the frozen no-direct-identifier rule already enforced structurally throughout this project.
- Never modify `01_Raw/` (archival, permanently read-only) or `02_Processed/` (the analytical source; this workbook reads from it but does not write back to it).
- If a profile cannot be accessed at all (deleted, made fully private, etc.), record `Review_Status = Unable to Verify` with a note — never fabricate a substitute observation.

## 9. No-score-during-evidence-collection rule

`ALCSM_Supplementary_Evidence_Collection_v1.0.xlsx` contains **no scoring field of any kind**, for any dimension, on any sheet. Evidence collection and rubric scoring are deliberately separate stages: this workbook exists to gather the raw material an annotator will later judge under the frozen Coding Rulebook and Annotation Handbook at P4 — it does not pre-empt that judgement. No 0–5 value, band label, or scoring inference is to be written anywhere in this workbook by the researcher, regardless of how obvious a score might seem while reading a profile.

## 10. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-17 | Initial protocol, governing the operational collection workbook built from the approved triage. | Samiksha Dhere |

---

*This protocol governs manual evidence-collection operations only. It does not alter `ALCSM_Measurement_Specification_v1.0.md`, `ALCSM_Coding_Rulebook_and_Pilot_Design.md`, `ALCSM_Annotation_Handbook.md`, the frozen schema, or any other historical methodology document.*
