# Expert Survey Analysis Plan v1.0

**Status:** Plan + reproducible descriptive analysis complete, run once against the real 23-respondent survey. **No inferential, predictive, or internal-consistency statistic is computed anywhere in this plan or its script.**
**Source (read-only, never modified):** `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` — 23 rows, all 23 consented (`consent == "Yes, I agree to participate"` for every respondent).
**Script:** `15_Scripts/alcsm_survey_analysis_v1.0.py` — reuses `alcsm.analysis.survey.reshape_survey_responses`/`participant_background_summary` and `alcsm.analysis.rq3_validation.content_validity_summary` unchanged; writes `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` (git-ignored, real respondent-derived data).
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## 1. Intended role of this evidence — and what it explicitly is NOT

The 23-respondent expert survey is **content-assessment evidence**: it tells us whether practitioners judge the six ALCSM dimensions relevant, clear, and appropriate as *observable credential signals*. It is explicitly **not** any of the following, and none of the following is computed anywhere in this plan, the underlying modules, or the processed output:

| Not this | Why not |
|---|---|
| Predictive validation | The survey does not test whether ALCSM scores predict any real-world outcome. |
| Competence validation | The survey does not test whether high-ALCSM-scoring individuals are actually more competent. |
| Population inference | n=23 self-selected respondents is not treated as representative of any wider population; no confidence interval, hypothesis test, or generalization claim is made from it. |
| Internal consistency | **No Cronbach's alpha, anywhere.** ALCSM is a formative index (six independent, non-interchangeable credential signals) — internal consistency is the wrong question to ask of it, exactly as already established for the annotation reliability side of this project. |
| Factor analysis | No factor/component analysis of the relevance, clarity, or distinctiveness items is performed. |

## 2. Descriptive statistics produced

All of the following are pure counts, means, and medians over the 23 consented respondents — no test statistic, no p-value, no model fit anywhere:

1. **Participant background** (`participant_background_summary`): value counts of professional role, years of professional experience, years of AI/tech experience, AI/tech leadership experience.
2. **Dimension relevance** (`content_validity_summary.relevance_by_dimension`): mean/median 1–5 relevance rating per dimension (D1–D6), n answered.
3. **Dimension clarity/distinctness** (`clarity_by_dimension`, `distinctiveness_by_dimension`): same, for the "how clear and distinct" and "how distinct from other dimensions" items.
4. **Overall framework appropriateness** (`overall_appropriateness`): mean/median of the single 1–5 appropriateness rating.
5. **Most-important dimension** (`most_important_dimension_counts`): a simple count of how many respondents picked each dimension as most important. **This count is reported as description only — it is never converted into a weight, percentage-of-composite, or ranking used anywhere in scoring.** (See §3.)
6. **Open-comment themes**: only the *count* of respondents who left a "missing signal" free-text comment is computed programmatically (`n_respondents_with_missing_signal_comment = 8` of 23). The comment *content* is never read into any function in `alcsm.analysis.survey` — this is a structural guarantee (`SurveyFreeText` carries only a boolean), verified by `tests/analysis/test_survey.py::test_module_never_carries_free_text_content_into_any_return_type`. Actual thematic coding of what respondents wrote is a manual qualitative step the researcher performs separately, by reading the raw file directly — out of scope for this script by design.

## 3. Explicit guardrails (why these, and how enforced)

- **No weights derived from "most important dimension."** The survey asks respondents to pick one dimension as most important; this plan reports the resulting counts as a descriptive fact about expert opinion, not as an input to any scoring formula. No function in this codebase reads `most_important_dimension_counts` and produces a weight — there is no weight-computation function anywhere in the analysis package at all (consistent with the project-wide rule that ALCSM has no composite score or weighting scheme yet).
- **No Cronbach's alpha.** Not computed by any function called here; the underlying `alcsm.analysis.rq3_validation` module's own docstring states this as a standing rule (shared with the annotation-reliability side, where the same wrong-statistic-for-a-formative-index reasoning applies).
- **Distinctiveness is 100% unanswered** in this survey instrument — confirmed again against the live 23-respondent file (`distinctiveness_by_dimension` shows `n_answered = 0` for all six dimensions). This is not a bug; it is reported as-is. Any future write-up should note this as a limitation of the instrument, not silently omit the column.

## 4. Re-verification against the current (24-respondent) file

**Update, 2026-08-25:** a newer raw response-level export (24 consented respondents, one more than the 23-respondent snapshot this plan was first written against) was found during this session's Part G search (see `Survey_Status_Report_v1.0.md`) and promoted to canonical; the prior 23-respondent file is archived at `16_Archive/Superseded_Survey_Responses/`. The modules that implement this plan (`alcsm.analysis.survey`, `alcsm.analysis.rq3_validation.content_validity_summary`) were re-run directly against the new file (read-only) with no code change required. Headline figures below are from that re-run, superseding the original 23-respondent figures:

| Metric | Value |
|---|---|
| n_respondents (raw rows) | 24 |
| n_consented | 24 |
| Relevance mean, highest dimension | D3 (Practical AI Experience), 4.33 |
| Relevance mean, lowest dimension | D2 (Professional Certifications), 3.25 |
| Overall appropriateness (mean, 1–5) | 3.42 |
| Most-important-dimension top pick | D3 — Practical AI Experience (9 of 24) |
| Respondents with a missing-signal comment | 8 of 24 |
| Distinctiveness items answered | 0 of 24 (instrument-wide, all dimensions) |

Full per-dimension tables are in the processed output workbook, not reproduced in full here to avoid a second place these numbers can drift out of sync.

## 5. Deliverables

| File | Contents |
|---|---|
| `Survey_Analysis_Plan_v1.0.md` | This document. |
| `15_Scripts/alcsm_survey_analysis_v1.0.py` | Reproducible script; read-only against the raw survey; writes the processed workbook below. |
| `ALCSM_Survey_Analysis_Processed_v1.0.xlsx` (git-ignored, real data) | `Overview`, `Background_role`, `Background_years_experience`, `Background_ai_years_experience`, `Background_leadership_experience`, `Relevance`, `Clarity`, `Distinctiveness`, `Overall_Appropriateness`, `Most_Important_Dimension`, `Missing_Signal_Comment_Count` sheets. |

---

*This plan authorizes no composite score, no weighting scheme, and no claim of predictive or population validity. It is descriptive content-assessment evidence only, one of two validation routes for a formative index — the other being inter-rater reliability, prepared separately in `07_Reliability/Double_Coding/`.*
