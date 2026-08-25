# P4 Implementation Completion Report

**Phase:** P4 — Annotation interface (software build only; pilot coding remains gated)
**Status:** Interface build complete and tested against constructed fixtures. Real pilot coding not started and not authorized by this report.
**Author:** Samiksha Dhere (researcher) — implemented with Claude Code assistance
**Date:** 2026-08-19

---

## 1. What was implemented

### 1.1 New package: `src/alcsm/annotation/`

| Module | Responsibility |
|---|---|
| `dimension_config.py` | Versioned dimension display/rubric configuration (`v1_0`, `v1_1`). D1–D5 identical across versions; D6 v1.1 shows the proposed "AI Industry/Application Breadth" definition, flagged `is_proposed=True`. Reads nothing from, and writes nothing to, the frozen `alcsm.constants.DIMENSIONS` vocabulary — the two are deliberately decoupled (§1.4 explains why). |
| `models.py` | `FirstPassReference` (read-only AI-assisted first-pass display data) and `AnnotationScore` (what a human rater submits) as two structurally distinct dataclasses — see §1.3. Also `ReviewDecision` (ACCEPT/CHANGE/DEFER), `RaterRole`, `ReviewOutcome`, `D6IndustryBreadthDetail`, `ProfileForAnnotation`. |
| `validation.py` | `validate_annotation_score` — mirrors every relevant `alcsm_dimension_score` CHECK constraint in Python (score range, evidence-required, missing-status coherence, D4-only verification, ambiguity/contradiction metadata, adjudicator-role alignment) so the interface can show a readable message instead of a raw `psycopg2` error. |
| `seed.py` | Seeds `rater_ref` (RATER_A/RATER_B/ADJUDICATOR) and `precedent_ref` (P-01…P-15, real ruling text from `PROJECT_CONTEXT.md` §12) — neither table is pre-populated by the DDL itself, and no seed script existed anywhere in the repository before this task (§3.3). |
| `store.py` | The validated, atomic, single-purpose write/read path for `alcsm_dimension_score` — mirrors `collection/helper.py`'s pattern (validate → one transaction → commit or full rollback). Duplicate submissions are refused (`DuplicateScoreError`), never silently overwritten. Rater-blinding reads (`has_other_rater_submitted`) return a boolean only, never a score. |
| `workflow.py` | `ReviewSession` state machine (profile selection → six dimensions together → accept/change/defer → save → validate → next) and `submit_and_save`/`check_blinding_before_display`, which wire validation, storage, and audit logging together for the interface to call. |
| `pilot.py` | `select_pilot_subset` — the double-coding-subset *mechanism* (100% or a seeded, reproducible ≥15% random sample, per the frozen policy). Chooses nothing on its own; every call takes the candidate pool as an argument. No real profile ID appears anywhere in this module. |
| `reliability_export.py` | Long-format (`ReliabilityInputRow`, reading `v_reliability_input`) and wide-format (`RaterComparisonRow`, Rater A / Rater B / Adjudicator side by side) export shaping for the future P5 alpha computation. Computes no statistic itself. |
| `audit.py` | Append-only, structured JSONL audit log (`AuditLogger`) — pseudonymous IDs and controlled action names only; a value that looks like a URL or email is refused before it can be written. |
| `export.py` | Allow-listed, PII-scanned CSV export of `AnnotationScore` rows — an export containing a URL/email pattern anywhere is refused whole, never partially written. |
| `fixtures.py` | Five constructed profiles (`PRF-9####`), reusing the same four composites already published and approved in `ALCSM_v1.0_Scoring_Framework_Task3.md` §4 / `ALCSM_v1.1_Scoring_Framework.md` §4, plus one new high-D6-breadth case. |
| `first_pass_loader.py` | Reads `06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx`'s `Dimension_Evidence` sheet into `FirstPassReference` objects, read-only. Raises a clear, catchable error if the (git-ignored) workbook is absent, rather than a bare `FileNotFoundError`. |

### 1.2 New Streamlit app: `src/alcsm/app/annotation_app.py`

A second, separate Streamlit entry point from `app/streamlit_app.py` (the P9 NLP-screening tool). Implements the full workflow this task specified: profile selection → evidence/missing-status/first-pass-reference display → D1–D6 display (versioned config) → accept/change/defer → rationale capture → save → validation → progress tracking. Runs today against fixtures only, with no database required (`P4_Dry_Run_Instructions.md`).

### 1.3 The FIRST_PASS_SCORE / FINAL_HUMAN_SCORE resolution

This was the first substantive design question, not just a naming exercise. The frozen schema's `rater_ref.rater_role` CHECK constraint accepts exactly `'primary'`, `'secondary'`, `'adjudicator'` — there is no role for an AI-assisted first pass, and none was added (that would be a schema change, out of scope and not needed). The resolution: **the AI-assisted first-pass scores are never written to `alcsm_dimension_score` at all.** They stay exactly where the prior session's work already put them — in `06_Annotation/ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` / `ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` — and `first_pass_loader.py` reads them read-only for display. `alcsm_dimension_score` is reserved for genuine human-rater submissions, which is also the methodologically correct reading: Krippendorff's alpha is defined over independent *human* raters, and inserting an AI-assisted draft as if it were a third "rater" would corrupt what the reliability statistic means, not just violate a naming convention. `AnnotationScore` (human, database-bound) and `FirstPassReference` (AI-assisted, read-only, workbook-bound) are consequently two separate dataclasses with no shared base type — see `models.py`'s module docstring for the full reasoning.

### 1.4 The D6 versioned-configuration design

`alcsm.constants.DIMENSIONS` (frozen, DB-aligned: `dimension_code='d6_engagement'`, label "Professional Engagement & Continuous Development") is untouched — editing it would silently rewrite frozen vocabulary (`CLAUDE_CODE_RULES.md` rule 1). `alcsm.annotation.dimension_config` is a new, separate, versioned layer: `get_dimension_config("v1_1")` returns the proposed D6 ("AI Industry/Application Breadth," `is_proposed=True`); `get_dimension_config("v1_0")` returns the original, retired D6. D1–D5 are byte-identical across both. The interface defaults to `v1_1` (matching what the first-pass annotation already used) but can show either side by side with no code change — exercised directly in the dry run (`P4_Dry_Run_Instructions.md` §2).

### 1.5 Two bugs found and fixed in already-existing code

Neither is scope creep — both were latent defects in P0-era code this task was the first to actually exercise for real:

1. **`DatabaseSettings.to_dsn()` (`config.py`) silently corrupted the connection string whenever `host` was a Unix-socket directory path** (e.g. `/tmp/alcsm_pgrun_xxx`, exactly what `alcsm.collection.devcluster.throwaway_database` uses) — the manual f-string URL builder put the socket path into the URL's host segment, where a literal `/` is not valid, and the resulting DSN silently mis-parsed (wrong `dbname`, wrong `user`). This had never been caught because nothing had exercised `db/engine.py`'s SQLAlchemy path against a real throwaway cluster before — `collection/helper.py`'s psycopg2 path uses `as_psycopg2_kwargs()` instead, which was never affected. Fixed using `sqlalchemy.engine.URL.create()`, which also correctly percent-encodes special characters in a password. Covered indirectly by every reliability-export test and directly by `tests/db/test_queries.py`.
2. **`tests/db/test_queries.py` needed updating**, not fixing — it asserted all five `db/queries.py` functions raised `NotImplementedError`, which stopped being true for three of them (`fetch_reliability_input`, `fetch_final_profile_scores`, `fetch_profile_completeness`) once this task implemented them as P4-adjacent read plumbing. Split into "still-unimplemented" (`fetch_credential_gap_by_dimension`, `fetch_nlp_evaluation`, correctly still P7/P8 stubs) and "now-implemented, tested against the real view" groups.

### 1.6 `pyproject.toml` / `.gitignore`

Added `openpyxl>=3.1` as an explicit dependency (was installed ad hoc in a prior session but never declared — `first_pass_loader.py` now formally depends on it via `pandas.read_excel`). Added `06_Annotation/audit_log/` and `06_Annotation/exports/` to `.gitignore`.

## 2. What was tested

466 tests pass project-wide (up from the pre-existing baseline), `black --check`, `ruff check`, and `mypy` all clean across the whole repository, run twice to check for cross-test-file ordering issues on the shared throwaway cluster.

New: `tests/annotation/` (14 files) + `tests/app/test_annotation_app.py` + 3 new tests in `tests/db/test_queries.py`, covering every item this task's "Testing" section named:

| Requirement | Where |
|---|---|
| Score validation | `test_validation.py` (range, dimension bounds, unknown missing-status) |
| Evidence requirements | `test_validation.py::TestEvidenceRequirements` |
| Missing-status handling | `test_validation.py::TestMissingStatusHandling`, `test_d6_breadth.py` |
| Reviewer workflow | `test_workflow.py` (six-together gating, accept/change/defer, save+validate) |
| Adjudication | `test_store.py::TestAdjudication`, `test_reliability_export.py` (adjudicated rows excluded from reliability export, per `v_reliability_input`'s own rule) |
| Duplicate prevention | `test_store.py::TestDuplicatePrevention` (original score survives a rejected duplicate) |
| Audit logging | `test_audit.py`, `test_workflow.py` (every decision produces an entry) |
| Export safety | `test_export.py` (URL/email refusal, all-or-nothing, allow-listed columns) |
| RQ4/annotation access separation | `test_access_separation.py` (AST-level: no import, no live reference, anywhere in the package or the app) |
| D1–D6 display | `test_dimension_config.py`, `tests/app/test_annotation_app.py` (real `AppTest` run) |
| D6 breadth handling | `test_d6_breadth.py` (evidence rendering, rubric-band consistency) |

Also: `test_pilot.py` (reproducibility given the same seed, 15% minimum enforced, never reads real data), `test_seed.py` (idempotent, real precedent text, no placeholders), `test_first_pass_loader.py` (constructed workbook only — never the real one), `test_fixtures.py` (fixtures are internally well-formed).

**Never real data.** Every fixture profile ID is `PRF-9####` (a block no real ~500-profile collection would plausibly reach) or a freshly-generated `PRF-6####` test ID from a counter range checked to be disjoint from every other literal ID already used elsewhere in the test suite (a real, if minor, collision was found and fixed during this task — `tests/collection/test_workflow.py`'s hardcoded `PRF-80001`…`80008` and `tests/collection/test_manager.py`'s hardcoded `BATCH-901` — both pre-existing, neither previously documented anywhere, both now avoided by construction rather than luck).

## 3. What remains blocked until the final human annotation is frozen (and until P2/P3 clear)

1. **Real pilot coding.** Per `Implementation_Phase_Roadmap.md`, pilot coding on real profiles needs P2 (ethics) and P3 (taxonomy anchoring) both to clear — unaffected by anything in this task, and not claimed to be resolved here.
2. **The Profile_ID format mismatch (confirmed, not fixed).** The real collected dataset uses `LP####` (`LP0001`…`LP0611`, confirmed valid by `P3_Final_Data_QA_Report.md`). The frozen schema's `profile` table requires `profile_id ~ '^PRF-[0-9]{5}$'`, and `collection/helper.py`'s own Python-level validator independently enforces the same pattern. **Every one of the 500 real profiles would currently fail both checks if loaded as-is.** This was surfaced incidentally in the prior D6 v1.1 task and is squarely in scope now: no real profile can be inserted into `alcsm.profile` — and therefore no real `alcsm_dimension_score` row can exist for one — until this is resolved. Not fixed here, per the explicit "STOP and report the exact issue" / "do not create migrations without explicit approval" instruction. Resolution options (for the author to choose, not decided here): (a) a load-time ID-mapping layer (`LP####` → a newly-assigned `PRF-#####`, with the mapping itself retained as provenance) that leaves the frozen schema untouched, or (b) a schema-level change to the CHECK constraint's pattern (a DDL edit requiring the same author approval as any other schema change). No schema change has been made or attempted.
3. **D6 v1.1's own pilot.** Independent of the above — `DECISION_LOG.md` D-0038 status remains PROPOSED/PILOT_REQUIRED. The interface displays the proposed D6 (flagged as such) but nothing about running the interface changes that status.
4. **Real reliability computation.** `reliability/krippendorff.py` remains an unimplemented P5 skeleton, correctly untouched by this task — `reliability_export.py` prepares data structures only, as instructed.
5. **Job-requirement-side annotation UI.** Out of scope for this task (which named "the annotation interface" without qualifying corpus, but every example, constraint, and fixture in the task was profile-side); `job_requirement_score` exists in the schema and would need an analogous (not yet built) interface before job-posting-side pilot coding.
6. **Wiring the Streamlit "Save" button to `alcsm.annotation.store`.** The dry run intentionally keeps decisions in Streamlit session state (§4 explains why — no database is required to exercise the interface today); connecting it to a real, credentialed database session is a small, mechanical change but has not been made, since there is no real database session to connect to yet in the current governance state.

## 4. Exactly how the researcher will use the system later

Once P2 and P3 clear and the Profile_ID mismatch (§3.2) is resolved:

1. **Provision the database.** Point `.env` at the real `alcsm_dev` (or production) database with the frozen schema deployed. Run `alcsm.annotation.seed.seed_reference_data(conn)` once (idempotent, safe to re-run) to populate `rater_ref` and `precedent_ref`.
2. **Load real profiles**, via the already-existing, unmodified `collection/helper.py` write path — once §3.2 is resolved, using whatever ID scheme is decided there.
3. **Select the double-coding subset.** Call `alcsm.annotation.pilot.select_pilot_subset(real_profile_ids, method=..., seed=...)`, choosing the method/seed deliberately and recording them (the function's return value already carries both, satisfying the pre-registration requirement) — this is the one substantive research decision this task deliberately left to the researcher, not automated anywhere in this codebase.
4. **Wire the Streamlit "Save" button to the database** (the one remaining mechanical step from §3.6): replace the in-session `decisions` dict with a call to `alcsm.annotation.workflow.submit_and_save`, passing a real `psycopg2` connection instead of none. Every other piece (validation, blinding, audit logging, duplicate prevention) is already wired to that exact function and needs no further change.
5. **Run the interface for real.** Two raters (RATER_A, RATER_B) independently code the pilot subset, never seeing each other's scores until both submit (enforced by `check_blinding_before_display`, tested in `test_workflow.py::TestBlindingGate`). An adjudicator resolves disagreements via `insert_adjudication`.
6. **Export for reliability analysis.** `alcsm.annotation.reliability_export.build_reliability_export_rows` / `build_rater_comparison_view` produce the Rater A/B/Adjudicator data structures P5's (still-unbuilt) Krippendorff's-alpha computation will consume — nothing here computes or interprets a reliability figure.
7. **Freeze or revise.** Per the existing frozen decision rule (α ≥ .80 proceed; .667–.80 acceptable with review; < .667 revise rulebook *wording* only, never criteria, and re-pilot) — unchanged by this task, and not evaluated here since no real pilot data exists yet.

---

*This report documents a software build only. No real profile has been scored, no schema has been changed, and no annotation has been finalized.*
