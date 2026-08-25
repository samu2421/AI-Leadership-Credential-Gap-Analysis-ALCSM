# PostgreSQL Profile_ID Compatibility — Status (Thesis-Deadline-Focused)

**Status:** Re-verified against the live database. **No schema, application, or data change made.** This is a focused status update against four specific questions, not a repeat of the full investigation already recorded in `PostgreSQL_ProfileID_Compatibility_Audit.md` (2026-08-24) — that document remains the fuller reference; this one exists to give a direct, deadline-relevant answer.
**Author:** Samiksha Dhere (researcher) — investigated with Claude Code assistance

---

## Q1. Does the live schema still reject `LP####`?

**Yes, confirmed again just now**, by direct rolled-back test against the live `alcsm_dev` database:

```
BEGIN;
INSERT INTO alcsm.profile (profile_id, sampling_batch_id, search_query, inclusion_reason, collection_ts)
VALUES ('LP0041', 'BATCH-TEST', 'test', 'title_match', now());
ROLLBACK;
-- ERROR: new row for relation "profile" violates check constraint "profile_profile_id_check"
```

`profile_profile_id_check: CHECK (profile_id ~ '^PRF-[0-9]{5}$')` is unchanged since the prior audit. `alcsm.profile` still has **0 rows**. Nothing about this incompatibility has changed.

## Q2. Can the analysis proceed directly from Excel without DB loading?

**Yes — and it already has, throughout this session.** Every deliverable prepared today (annotation audit, reliability subset selection, reliability analysis workflow, survey analysis) read the canonical Excel workbooks directly with `pandas` and never touched the database:

- `Final_Annotation_Audit_v1.1.md` — read `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` directly.
- `15_Scripts/alcsm_reliability_subset_build_v1.0.py` and `alcsm_reliability_subset_analysis_v1.0.py` — read the same file plus the subset workbook, no DB connection anywhere in either script.
- `15_Scripts/alcsm_survey_analysis_v1.0.py` — read the survey Excel export directly.

None of the analysis modules exercised this session (`alcsm.analysis.rq3_validation`, `alcsm.analysis.survey`, `alcsm.reliability.krippendorff`, `alcsm.reliability.subset_workflow`) import or call anything from `alcsm.db`. The database path exists in this codebase (`src/alcsm/db/`) as a separate, optional layer for RQ4 (`rq4_impact_indicator`) and any future querying need — it is not on the path of any RQ1–RQ3 descriptive or reliability work.

## Q3. Is a DB migration actually required for the thesis?

**No, not for the work in scope through this session.** The only real-data path that structurally requires the database at all is **RQ4** (observable professional impact indicators, `rq4_impact_indicator`) — and RQ4 is additionally blocked on a separate, unfinished data-collection step (no impact-indicator data has been collected for any profile yet, DB-loadable or not). RQ1, RQ2 (descriptive side), and RQ3 (both content-validity and reliability) run entirely off Excel. RQ5 (NLP evaluation) compares model predictions against the frozen annotation, also Excel-based, once a model exists (Phase P7, not started, explicitly out of scope this session).

**Conclusion: a Profile_ID schema fix is not a blocker for finishing the statistical analysis this thesis needs in the next three days.** It only matters if/when RQ4 work begins.

## Q4. Least-invasive future fix (unchanged from the prior audit — restated, not re-decided)

Two candidate fixes were identified in `PostgreSQL_ProfileID_Compatibility_Audit.md` §E and remain valid:

1. **Widen the CHECK constraint** to accept `LP[0-9]{4,5}` alongside `PRF-[0-9]{5}` — smallest schema footprint (one constraint's regex text), requires a `v1.0.1` → `v1.0.2` version bump and a matching `collection/helper.py` validator update. Still the leading recommendation on the same grounds as before.
2. **Add an ID-mapping layer** (new `external_profile_id` column, generate a `PRF-#####` primary key at load time) — larger footprint, leaves the original constraint untouched.

**No decision is made here, on the same grounds as before:** this is a schema/methodology choice for the author to make explicitly, not an implementation default. Given Q3's answer, there is no deadline pressure to force that decision now — it can be made whenever RQ4 work actually begins, with no cost to the work completed this session.

## What was checked, and what wasn't touched

- Checked: live constraint text, row count, a rolled-back test insert. Nothing else was re-run (the `db/models.py` reflection bug and `config.py` empty-password issue documented in the prior audit were not re-tested here — no new information changes their status, and neither affects Q1–Q3 above).
- Not touched: no `ALTER TABLE`, no version bump, no code change, no row inserted or left behind (`alcsm.profile` is still 0 rows).

---

**Bottom line for the next three days: proceed with Excel-based analysis. The database is not on the critical path.**
