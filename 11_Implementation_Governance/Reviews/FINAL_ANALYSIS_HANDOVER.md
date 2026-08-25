# FINAL ANALYSIS HANDOVER

**Status:** Repository cleaned, consolidated, and handed over. This is the single reference point for beginning analysis work. Nothing past this document has been started.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance
**Date:** 2026-08-24

---

## Canonical sources

| Corpus | Canonical path | Status |
|---|---|---|
| **Annotation (scoring baseline)** | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` | **Frozen.** SHA-256 `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f`. See `Final_Annotation_v1.1_Freeze_Report.md`. |
| **LinkedIn profiles (processed)** | `05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` | Active. Currently open in Excel on the researcher's machine — re-verify before any batch read if working live. |
| **Job postings (processed)** | `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` | Active. Requirement-mapping revision already merged (799/1,558 `NOT_DIRECTLY_MAPPED`, down from 872 at the time of the D6 v1.1 task). |
| **Expert survey (raw)** | `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` | Active. 23 consented respondents (updated this session from 12 — see `Repository_Cleanup_Report.md` §3). |

All four are git-ignored; none has ever been committed. Full canonical register, including framework and database files: `Document_Version_Policy.md`.

## Current versions

| Component | Version | Notes |
|---|---|---|
| ALCSM framework | **v1.1** | D1–D5 unchanged from frozen v1.0 (`ALCSM_v1.0_Scoring_Framework_Task3.md` remains the historical predecessor for those five). No weights, aggregation function, or classification bands chosen — deliberately open. |
| D6 | **v1.1 — "AI Industry/Application Breadth"** | Status **PROPOSED / PILOT_REQUIRED** (`DECISION_LOG.md` D-0038). Not yet frozen — the pilot design in `D6_v1.1_Implementation_Assessment.md` §Pilot Design has not been run. The retired v1.0 D6 ("Professional Engagement & Continuous Development") is superseded, its observation-rule proposal archived at `16_Archive/Superseded_D6_Professional_Engagement/`. |
| Database schema | **v1.0.1** | Frozen DDL, deployed to the live local `alcsm_dev` PostgreSQL 16 database (22 tables, 5 views). **`alcsm.profile` currently has zero rows** — no real profile has been loaded, because of the Profile_ID incompatibility below. No DDL change has been made. |

## Known missingness cases

- **`LP0041`, `LP0170`, `LP0182`** — zero `Professional_Experience` records in the processed LinkedIn workbook; D3 and D6 are marked `unavailable` (a data gap, not a genuine zero finding) for all three, confirmed directly in the frozen annotation file's `Data_Integrity` sheet and `Missing_Status` columns.
- Only `present`/`unavailable` missing-status values appear in the frozen annotation dataset — `absent_stated`/`not_applicable` are valid states in the frozen four-state framework but were never triggered on the profile side.
- D2 and D4 scores never reach the top of the 0–5 range in the frozen dataset (D2 max observed = 1; D4 max observed = 3) — a consequence of the source data's own limitations (no certification issue/expiry dates; no technical-contribution verification metadata), already documented in the first-pass annotation's own `Method_Notes` and re-verified against the frozen file's `Score_Distribution` sheet in `Final_Annotation_v1.1_Freeze_Report.md` §4.
- D6 is asymmetrically observable: ~99% profile-side coverage vs. 0.06% (1 of 1,558) posting-side requirement mappability, per `D6_v1.1_Implementation_Assessment.md` §5 and reconfirmed via `alcsm.analysis.gap.d6_profile_vs_posting_asymmetry`.

## Known methodological limitations (carried forward, not resolved by this session)

1. **D6 v1.1 is not yet frozen.** It is the researcher-reviewed scoring baseline for the 500 profiles, but its pilot (independent human raters, Krippendorff's alpha) has not been run. Treat D6 results as provisional relative to that pilot until it completes.
2. **No real profile can currently enter the database.** Blocks any analysis path that requires `alcsm_dimension_score`, `rq4_impact_indicator`, or other DB-resident tables to hold real data — see `PostgreSQL_ProfileID_Compatibility_Audit.md`.
3. **RQ2's true numeric credential gap is not computable yet.** `dimension_gap_from_scores` exists and is tested against fixtures, but needs `job_requirement_score.required_score` populated — a requirement-level 0–5 scoring pass that has not been built or run (identified during the RQ1–RQ5 preparation session, `DECISION_LOG.md` D-0040 open items).
4. **RQ4's real input chain is blocked** on the same database-loading issue as (2), plus `rq4_impact_indicator` population.
5. **RQ5 has no gold-standard-vs-prediction data** — the frozen annotation is now the gold standard, but no NLP model has been trained (Phase P7, not started).
6. **Inter-rater reliability has no real input yet** — the P4 annotation interface is built and tested (prior session), but no pilot with independent human raters (`RATER_A`/`RATER_B`) has been run against real profiles.
7. **General ethics/DPO approval status remains undocumented** in this repository (`DECISION_LOG.md` §8, Finding GOV-01, still open) — unaffected by this session, still a standing blocker for any further real-data collection.

## Do-not-change constraints (unchanged, restated for this handover)

- Do not redesign ALCSM; do not change D1–D6; do not introduce a new dimension; do not change scoring criteria; do not change D6's definition.
- Do not rescore any profile. Do not modify `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` — it is frozen.
- Do not compute a composite score, weighting scheme, or classification band anywhere.
- Do not rename the 500 analytical Profile_IDs (`LP####`) — any database compatibility fix must preserve them as the external analytical identifier (`PostgreSQL_ProfileID_Compatibility_Audit.md` §E).
- Do not treat the AI-assisted first-pass dataset as a second independent human rater in any reliability computation.

## Immediate next tasks (not started; sequencing only, per this session's brief)

1. Inter-rater reliability (needs a real P4 pilot to run first).
2. Descriptive RQ1 analysis, against the now-frozen annotation dataset.
3. Job-requirement gap analysis (RQ2) — descriptive parts are runnable now; the true numeric gap needs the requirement-scoring pass in limitation (3) above.
4. Survey / expert validation analysis (RQ3) — content-validity summary is runnable now against the 23-respondent dataset.
5. RQ4 analysis — blocked on database loading (limitation 4).
6. NLP implementation / evaluation (RQ5) — blocked on Phase P7 model training.
7. Figures / tables.
8. Thesis writing.

**None of these were begun in this session.** The infrastructure for 1–6 (analysis modules, reliability computation, dry-run script) was built and tested in the prior RQ1–RQ5 preparation session against fixtures and provisional data; this session's job was only to establish the frozen dataset those modules should now run against and clear repository/database obstacles in the way.

---

## Companion documents from this session

- `Final_Annotation_v1.1_Freeze_Report.md` — full verification of the frozen annotation dataset (Part A).
- `Repository_Cleanup_Report.md` — every file moved, archived, or removed, and why; final repository tree (Parts B, C, F).
- `PostgreSQL_ProfileID_Compatibility_Audit.md` — full A–E investigation of the database incompatibility; no fix applied, awaiting a decision (Part D).
- `Document_Version_Policy.md` — updated canonical-file register (Part E).

---

*This document hands over a cleaned, consolidated, verified repository with one clearly frozen annotation baseline. It authorizes no analysis, no scoring, and no schema change on its own — each remains a separate, later, explicitly-approved step.*
