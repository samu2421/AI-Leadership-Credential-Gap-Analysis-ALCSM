# RQ1–RQ5 Analysis Reproducibility Instructions

**Status:** Describes the analysis-preparation infrastructure as built. Does not itself run a final analysis — see `Analysis_Preparation_Completion_Report.md` for what remains blocked.
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Date:** 2026-08-23

---

## 1. Environment setup

```bash
cd "AI_Leadership_Credential_Gap_Analysis"
python3 -m venv .venv && source .venv/bin/activate   # if not already set up
pip install -e ".[app,reliability,dev]"
```

`pip install -e .` (editable install) is required — without it, `alcsm` is only importable inside `pytest` (which auto-adds `src/` to `sys.path` via `pyproject.toml`'s `pythonpath = ["src"]`), not from a standalone script. This was discovered while building this task's dry-run script; if it is missing, every script under `15_Scripts/` and `05_Data_Collection/Scripts/` fails with `ModuleNotFoundError: No module named 'alcsm'` — a pre-existing environment-setup gap, not specific to this task, now resolved in this project's own `.venv`.

For the reliability-computation and database-backed test suite, PostgreSQL 16 is also needed:

```bash
brew install postgresql@16   # macOS, if not already installed
```

## 2. Run the automated test suite

```bash
python3 -m pytest tests/ -q
```

570 tests, all against constructed fixtures or a throwaway PostgreSQL cluster this suite creates and destroys itself — no real data is ever required for the test suite to pass, and no real data is ever written to by it. Run twice in a row if in doubt about cross-test ordering effects on the shared session-scoped cluster (`tests/conftest.py`); both runs are deterministic and produce the same result.

Quality gates:

```bash
black --check src tests 15_Scripts
ruff check src tests 15_Scripts
mypy src 15_Scripts
```

## 3. Run the RQ1–RQ5 dry run

```bash
python3 15_Scripts/alcsm_analysis_dry_run_v1.0.py
```

Runs every RQ1–RQ5 module end to end. Where real (git-ignored) source files are present in this checkout, it reads them; where they are not (a fresh clone, or CI), the corresponding section prints "Skipped (source not found)" rather than failing. RQ4 and RQ5 always run against small constructed fixtures, since no real `rq4_impact_indicator` data or trained NLP model exists yet. **Every line of output is prefixed with its `data_status`** (`[FINAL_FROZEN]`, `[⚠ PROVISIONAL]`, or `[SYNTHETIC_FIXTURE]`) — nothing printed by this script is a final thesis finding, regardless of how well-formed the output looks.

## 4. Real data locations (git-ignored; present only in a researcher's own checkout)

| Source | Path | Loader |
|---|---|---|
| Researcher-review layer (ALCSM scores) | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx` | `alcsm.analysis.data_sources.load_profile_scores` / `load_dimension_evidence` / `load_review_changes` / `load_d6_quality_review` |
| LinkedIn processed workbook (demographics) | `05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` | `load_linkedin_processed` |
| Job postings processed workbook | `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` | `load_job_postings_processed` |
| Expert survey (raw Google Forms export) | `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` | `load_survey_raw` (then `alcsm.analysis.survey.reshape_survey_responses`) |

All four paths are resolved via `alcsm.analysis.config.default_analysis_paths()` and are covered by `.gitignore` — none has ever been committed. If a path does not exist, every loader raises `alcsm.analysis.data_sources.SourceFileNotFoundError`, never a bare, confusing `FileNotFoundError`.

**A note on the expert-survey file specifically:** it was found at the repository root, outside any git-ignored path, during this task — a real exposure risk, now corrected (moved to the path above, `.gitignore` updated same-session). If you are starting from a state before this fix, check `git status` for anything resembling `ALCSM Expert Survey Responses.xlsx` sitting outside `07_Reliability/Survey_Responses/01_Raw/` before doing anything else.

## 5. Running the real analysis once data is frozen

Every RQ1–RQ5 function that consumes profile-level ALCSM scores requires either `data_status="final_frozen"` or an explicit `acknowledge_provisional=True` (`alcsm.analysis.config.require_frozen_or_acknowledge_provisional`). Once the researcher's review is complete (no `Profile_Scores.Overall_Review_Status` row still reads `Pending Review`), `alcsm.analysis.data_sources.load_profile_scores` will itself infer `data_status="final_frozen"` automatically (`infer_profile_scores_status`) — no code change is needed to "turn on" final-mode analysis, the same functions just stop requiring the acknowledgement flag once the underlying data says so.

**Recommended sequence once frozen:**

1. Re-run `15_Scripts/alcsm_analysis_dry_run_v1.0.py` — every `[⚠ PROVISIONAL]` line for RQ1/RQ2 should now read `[FINAL_FROZEN]` without any code change.
2. For RQ3 reliability: once a P4 pilot has produced real `RATER_A`/`RATER_B` independent scores, shape them via `alcsm.annotation.reliability_export` (already built) into `alcsm.analysis.rq3_validation.inter_rater_reliability`'s expected input, or use the `ratings_from_dimension_evidence` adapter provided for exactly this purpose.
3. For RQ4: once profiles are loaded into the database (blocked on the Profile_ID format issue — see `P4_Implementation_Completion_Report.md` §3.2) and `rq4_impact_indicator` is populated, replace the dry-run's constructed fixture with a real query result shaped the same way.
4. For RQ5: once a gold standard is frozen and a Phase P7 model produces predictions, replace the dry-run's constructed fixture with real `(profile_id, dimension_number, predicted_score)` rows.
5. Only after all of the above: assemble a real thesis findings chapter. This repository's analysis package computes descriptive statistics, correlations, and evaluation metrics — it does not write prose interpretation, and no function in it produces a "finding" on its own authority.

## 6. What must never be done, regardless of how tempting the output looks

- Do not remove the `acknowledge_provisional` requirement from any RQ1/RQ2/RQ5 function to make output print more easily — it exists specifically to prevent silently treating provisional scores as final.
- Do not add a composite/weighted score anywhere in `alcsm.analysis` — none of the five RQ modules compute one, by design (`tests/analysis/test_isolation.py::test_no_analysis_module_computes_a_composite_score` checks this structurally).
- Do not feed the AI-assisted first-pass data into `inter_rater_reliability` as if it were a second human rater — the function's own `_ALLOWED_HUMAN_RATER_IDS` allow-list refuses this by construction.
- Do not call `.to_excel()` (or any other write) from inside `alcsm.analysis` — every loader is read-only (`test_isolation.py::test_no_analysis_module_writes_to_the_review_workbook_or_processed_sources`).

---

*These instructions describe how to run and reproduce the analysis-preparation infrastructure only. They do not authorize a data freeze, real annotation, NLP training, or final thesis findings.*
