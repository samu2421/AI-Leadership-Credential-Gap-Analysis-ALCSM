# Analysis Preparation Completion Report

**Phase:** Final analysis-preparation stage — RQ1–RQ5 infrastructure build
**Status:** Infrastructure complete and validated against real (still-provisional) data where it exists. No final analysis has been run; no thesis finding is produced by this report or by any module it describes.
**Author:** Samiksha Dhere (researcher) — implemented with Claude Code assistance
**Date:** 2026-08-23

---

## 1. What was built

### 1.1 Package layout

```
src/alcsm/analysis/
    config.py            shared data-status labelling + the provisional/frozen gate
    data_sources.py       read-only loaders for every real data source
    rq1_descriptive.py    RQ1 — demographics, distributions, missingness, patterns
    gap.py                 RQ2 — requirement counts, Not Directly Mapped, supply/demand, D6 asymmetry
    survey.py               expert-survey reshape (wide -> tidy, free text isolated)
    rq3_validation.py        RQ3 — content validity, inter-rater reliability, review-change concordance
    rq4.py                    RQ4 — ordinal correlation with impact indicators (isolated)
src/alcsm/nlp/evaluate.py       RQ5 — confusion matrices, ordinal metrics, error analysis
src/alcsm/reliability/krippendorff.py   per-dimension alpha, bootstrap CI, % agreement, variance
tests/analysis/  (+ tests/nlp/test_evaluate.py, tests/reliability/test_krippendorff.py)
15_Scripts/alcsm_analysis_dry_run_v1.0.py    end-to-end demonstration script
```

**Module placement note:** RQ2 and RQ4 were built into the pre-existing `gap.py`/`rq4.py` stub modules (P0 skeletons already named for exactly this purpose in `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §6's module table) rather than new parallel files, and RQ5's evaluation logic was built into the pre-existing `nlp/evaluate.py` stub for the same reason. Their existing stub tests (`test_gap.py`, `test_rq4.py`, `test_evaluate.py`) were replaced with real coverage rather than left alongside duplicate new files. RQ1 and RQ3 had no pre-existing dedicated module, so `rq1_descriptive.py` and `rq3_validation.py` are new.

### 1.2 RQ1 — descriptive analysis (`rq1_descriptive.py`)

`demographic_summary`, `dimension_distribution` (counts/means/medians/std per D1–D6, `use_final`/`use_first_pass` selectable), `dimension_missingness`, `title_category_patterns`, `company_size_patterns`, `industry_patterns`, `dimension_level_comparison`. Every grouped-pattern function merges `Profile_Master` to `Profile_Scores` on `Profile_ID`. No function computes or implies a causal relationship — checked structurally (`test_isolation.py`) and by construction (only means/medians/counts are ever returned).

### 1.3 RQ2 — gap analysis (`gap.py`)

`requirement_counts_by_dimension`, `not_directly_mapped_report`, `supply_vs_demand_frequency` (requirement *count* vs. profile *score distribution*, explicitly not a subtracted "gap" — different units), `dimension_gap_from_scores` (the true `mean(required) − mean(held)` formula, ready but untestable against real data — see §3), `d6_profile_vs_posting_asymmetry` (reproduces, as a reusable function, the profile-vs-posting asymmetry finding first established in `D6_v1.1_Implementation_Assessment.md` §5).

### 1.4 RQ3 — construction and validation (`survey.py` + `rq3_validation.py`)

`survey.py` reshapes the raw Google-Forms export (wide, one row per respondent) into tidy long-format ratings, with **free text kept structurally separate from every numeric result** — `SurveyFreeText.has_missing_signal_comment` is a boolean, the actual comment text never enters any dataclass this module returns. `rq3_validation.py` provides:

- `content_validity_summary` — per-dimension relevance/clarity/distinctiveness means, overall appropriateness, most-important-dimension picks.
- `inter_rater_reliability` — Krippendorff's alpha per dimension, **restricted by a hard allow-list to genuine independent human raters** (`RATER_A`/`RATER_B`). Passing any other id — including an AI-assisted first-pass id — raises `NotAHumanRaterError`. This is the concrete mechanism behind the explicit instruction *"do not calculate reliability against the current AI first-pass dataset as if it were human gold standard."*
- `researcher_review_changes_summary` — counts, direction, and mean absolute change of what the researcher actually revised, plus precedent-citation counts. Deliberately never called "reliability" or "agreement" anywhere in its name, docstring, or fields (checked in `test_rq3_validation.py`), because it measures one reviewer's revision of a machine-generated draft, not inter-rater agreement between two independent human coders.
- `dimension_missingness` is reused directly from `rq1_descriptive` rather than reimplemented.

### 1.5 RQ4 — impact-indicator correlation (`rq4.py`)

`CRITERION_VARIABLES` is the closed, frozen list of four (`rq4_network_reach`, `rq4_content_engagement`, `rq4_recognition_count`, `rq4_seniority_progression_rate`) — no mechanism exists anywhere in this module to add a fifth. `correlate_with_impact_indicators` computes Spearman's rank correlation (via rank-transformed Pearson, no `scipy` dependency) per dimension × criterion pair. Structural isolation is enforced and tested at the AST level (`test_isolation.py`): this is the only module in the package that imports anything RQ4-shaped, and it imports nothing from any sibling RQ module.

### 1.6 RQ5 — NLP evaluation (`nlp/evaluate.py`)

`confusion_matrix_by_dimension` (6×6 gold-vs-predicted per dimension), `evaluate_predictions` (exact-match rate, mean signed/absolute error, linear-weighted Cohen's kappa — never pooled across dimensions), `error_analysis` (largest-magnitude cases by profile/dimension/scores only, never evidence text — this module never reads evidence text in the first place). **No model is trained, loaded, or run anywhere in this module** — checked structurally (`test_no_module_never_imports_or_calls_a_training_function`, AST-level).

### 1.7 Reliability (`reliability/krippendorff.py`)

Implemented for real this session (previously a Phase-P5 stub), since RQ3 explicitly required it. **Validated against Krippendorff's own published worked example** (4 coders × 12 units; nominal/interval/ordinal metrics match the widely-cited reference values to within 0.001 — `tests/reliability/test_krippendorff.py::TestPublishedWorkedExample`), plus hand-worked edge cases (perfect agreement, complete disagreement with a balanced marginal, insufficient-data guards). Provides `compute_alpha_for_dimension`, `bootstrap_alpha_ci` (percentile bootstrap, reproducible given a seed), `percent_agreement`, `score_variance`, and `compute_reliability_result` (full `reliability_result`-shaped output). Computes nothing pooled across dimensions.

### 1.8 Data-provenance labelling (`config.py`)

Every top-level result across all five RQ modules carries an `AnalysisRunMetadata` with `data_status ∈ {synthetic_fixture, provisional_first_pass, final_frozen}`. Functions consuming profile-level ALCSM scores call `require_frozen_or_acknowledge_provisional`, which raises `DataNotFrozenError` unless the caller either has genuinely frozen data or explicitly passes `acknowledge_provisional=True` — and even then, the result is still labelled provisional. `infer_profile_scores_status` derives the status automatically from `Profile_Scores.Overall_Review_Status`, so the transition to `final_frozen` happens by the data changing, not by a code edit.

## 2. What was tested

460 new/replaced tests (570 total project-wide, up from the P4 session's baseline of 466), run twice for ordering stability; `black`/`ruff`/`mypy` clean across the whole repository. Every fixture is constructed and non-personal, shaped to match the real workbooks' actual column layouts (discovered by inspection, corrected twice after real-data testing — see §3).

| Coverage area | Where |
|---|---|
| Freeze-gate enforcement | `test_config.py`, gated tests in every RQ1/RQ2/RQ4/RQ5 test file |
| Krippendorff's alpha correctness | `test_krippendorff.py` (published worked example + hand-worked edge cases) |
| Human-only reliability guard | `test_rq3_validation.py::TestInterRaterReliabilityHumanOnlyGuard` (refuses first-pass, AI, and researcher-final ids explicitly) |
| Free-text isolation | `test_survey.py` (structural: no dataclass field can carry comment content) |
| RQ4/ALCSM structural isolation | `test_isolation.py` (AST-level import/reference checks) |
| No composite score anywhere | `test_isolation.py::test_no_analysis_module_computes_a_composite_score` |
| Read-only data access | `test_isolation.py::test_no_analysis_module_writes_to_the_review_workbook_or_processed_sources` |
| NLP evaluation without training | `tests/nlp/test_evaluate.py::test_module_never_imports_or_calls_a_training_function` |

## 3. Real bugs found and fixed (via the dry-run script against real, still-provisional data)

Synthetic-fixture tests alone did not catch these, because each fixture initially shared the same wrong assumption as the code it was meant to test — they were only caught by running the pipeline against the actual real files, which is exactly why `alcsm_analysis_dry_run_v1.0.py` reads real data where present rather than only exercising fixtures:

1. **D6's survey-question label** — `survey.py` was reading `alcsm.constants.DIMENSIONS`' frozen v1.0 label ("Professional Engagement & Continuous Development") for column matching, but the survey itself was administered under the proposed v1.1 framing ("AI Industry/Application Breadth"). Fixed by sourcing D6's label from `alcsm.annotation.dimension_config.get_dimension_config("v1_1")` instead — the same versioned-config layer built for exactly this purpose in the P4 session.
2. **Three truncated column-header constants** (`_APPROPRIATENESS`, `_MOST_IMPORTANT`, `_MISSING_SIGNAL`) — captured from a 70-character-truncated preview during inspection and used for exact-match lookups, which silently failed on the real (longer) headers. Fixed by resolving all single-instance survey columns once via prefix match (`_find_column`) rather than requiring a hand-transcribed exact string.
3. **`_RELEVANCE_PREFIX` matched the wrong part of the string** — the real relevance question's shared context block *ends* with the phrase used as the prefix constant; it does not *start* with it. Fixed by using the column's actual opening sentence.
4. **`NOT_DIRECTLY_MAPPED` literal mismatch** — the code used `"Not Directly Mapped"` (title case, spaces); the real data uses `"NOT_DIRECTLY_MAPPED"` (upper case, underscore). This also surfaced that the real count has changed since the D6 v1.1 task (872 → 799 unmapped requirements as of this writing) — an observation, not something this task acted on.
5. **`alcsm` was not installed in editable mode** in this project's `.venv` — every standalone script (including the pre-existing `collection_dry_run.py`, confirmed to have the identical failure) raised `ModuleNotFoundError` outside of `pytest`. Fixed by running `pip install -e ".[app,reliability,dev]"`, which also installed the already-declared-but-never-installed `scipy` dependency.

**Also found and fixed, unrelated to code correctness:** the raw expert-survey export (`ALCSM Expert Survey Responses.xlsx`, 12 respondents) was sitting at the repository root, outside any git-ignored path — a real personal-data exposure risk. Relocated to `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` and `.gitignore` updated (`07_Reliability/Survey_Responses/`, plus `09_Statistical_Analysis/Outputs/` added proactively for future analysis-output files) before any further work touched it.

**One inadvertent near-miss, corrected immediately:** while first inspecting the survey file's column layout by position rather than by name, an early exploratory command printed the actual free-text contents of the "missing signal" question column (3 real respondents' opinions) to this session's own output before the error was caught. No respondent name, contact detail, or other direct identifier was involved, and the content was not reproduced anywhere else (code, tests, fixtures, or this report) — but it is disclosed here rather than left unmentioned, and it is the reason every loader and reshaping function built afterward treats free text as structurally separate and boolean-presence-only (§1.4, §2).

## 4. Real (provisional) figures observed during the dry run

Included here only to prove the pipeline works end to end — **every figure below is `provisional_first_pass` or reflects data still subject to change, and none of it is a thesis finding**:

- 500 profiles, 1,558 job requirements, 12 consented survey respondents (of 13 total; 1 declined consent and is correctly excluded).
- D1–D6 provisional means: D1=2.30, D2=0.47, D3=2.93, D4=0.95, D5=2.96, D6=1.77 (D2/D4's low means and capped ranges match the data-limitation notes already recorded in the first-pass annotation's own `Method_Notes`).
- 799/1,558 (51.3%) requirements currently "Not Directly Mapped."
- D6 profile-side coverage 99.4% (497/500) vs. posting-side coverage 0.06% (1/1,558) — reproduces the asymmetry finding from `D6_v1.1_Implementation_Assessment.md` as a now-reusable, tested function rather than a one-off computation.
- Expert survey: mean relevance ratings ranged 3.33 (D4) to 4.67 (D3) on a 1–5 scale; mean overall framework appropriateness 3.83/5; D3 and D6 were the two most frequently picked "most important" dimensions (5 and 4 of 12 respondents respectively); the distinctiveness question was left unanswered by all 12 respondents.
- Zero rows in `Review_Changes` — the researcher's review has not yet recorded any score change.

## 5. Status by research question

| RQ | Ready to execute for real | Blocked on |
|---|---|---|
| **RQ1** | Yes, mechanically — every function runs today against the review workbook | The **interpretation** waits on the final human annotation dataset being frozen (`Overall_Review_Status` has no remaining `Pending Review` rows); until then every result is `provisional_first_pass` |
| **RQ2** | Partially — `requirement_counts_by_dimension`, `not_directly_mapped_report`, `supply_vs_demand_frequency`, `d6_profile_vs_posting_asymmetry` run today | `dimension_gap_from_scores` (the true numeric gap) additionally needs `job_requirement_score.required_score` populated — a requirement-level 0–5 scoring pass that has not been built or run (out of scope for this task) |
| **RQ3** | Content validity: yes, today (12 consented respondents) | Inter-rater reliability needs real P4 pilot data (RATER_A/RATER_B independent scores) — the P4 interface is built (prior session) but no pilot has run; review-change concordance needs the researcher to actually record changes (currently zero) |
| **RQ4** | No real input exists | Needs profiles loaded into the database, which is itself blocked on the Profile_ID format mismatch (`P4_Implementation_Completion_Report.md` §3.2) and `rq4_impact_indicator` population |
| **RQ5** | No real input exists | Needs (a) the frozen gold standard and (b) a trained Phase P7 NLP model — neither exists, and this task does not build the model (explicitly out of scope) |

## 6. Exactly what remains open for final thesis analysis

- **Requires final human annotation:** RQ1's substantive interpretation, RQ2's supply-side figures, RQ5's gold standard. All currently `provisional_first_pass`.
- **Requires survey completion:** none outstanding — the survey is a completed, consented, 12-respondent instrument; RQ3's content-validity summary is genuinely `final_frozen` today. (Whether 12 respondents is a sufficient sample for the thesis's content-validity claims is a methodological judgement for the author, not evaluated here.)
- **Requires NLP training:** RQ5 in full, and RQ4's real input chain (which depends on real profiles being loaded, a separate blocker).
- **Requires a P4 pilot:** RQ3's inter-rater reliability.
- **Requires a Profile_ID resolution decision:** RQ4 and any real database-backed analysis (unchanged blocker from the P4 session).
- **Requires a requirement-level scoring pass:** RQ2's true numeric gap (`dimension_gap_from_scores`), not previously identified as a distinct open item until this task.
- **Never in scope, by design, regardless of what unblocks:** a composite ALCSM score, dimension weights, classification bands, causal claims, or a frozen dataset — none of this task's modules compute any of these, and several tests check that structurally rather than just by omission.

---

*This report documents an infrastructure build only. No score was changed, no methodology was altered, no model was trained, and no thesis finding is asserted by this document or by any module it describes.*
