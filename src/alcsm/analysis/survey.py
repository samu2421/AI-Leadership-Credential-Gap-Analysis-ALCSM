"""Expert-survey reshape: raw Google-Forms export -> tidy, analysis-ready data.

The raw export (`alcsm.analysis.data_sources.load_survey_raw`) is wide
(one row per respondent, one column per question, with a real free-
text opinion column) and must never be printed or logged in bulk. This
module's job is entirely mechanical reshaping and light parsing (text
Likert labels -> numeric codes); the actual content-validity summary
statistics live in `rq3_validation.py`.

**Free text is kept structurally separate from every numeric result.**
`reshape_survey_responses` returns rating data and free-text data as
two different fields on two different objects; nothing downstream of
this module ever needs to touch the free-text field to compute a
statistic, and no function anywhere in this package prints its
contents. Thematic coding of the actual comments (what respondents
said, not how many responded) is a manual qualitative-analysis task
for the researcher, out of scope here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd

from alcsm.annotation.dimension_config import get_dimension_config

# The survey question text uses the PROPOSED v1.1 D6 label ("AI
# Industry/Application Breadth"), not the frozen v1.0 label
# `alcsm.constants.DIMENSIONS` still carries ("Professional Engagement
# & Continuous Development") -- the survey was administered under the
# v1.1 framing. Column matching below must therefore read dimension
# labels from `dimension_config` (versioned display layer), never from
# `alcsm.constants` directly, or D6 column lookup fails outright. D1-D5
# labels are identical across both sources either way.
_SURVEY_DIMENSIONS = get_dimension_config("v1_1")

# The raw export's column order, discovered by inspection (see
# `Analysis_Preparation_Completion_Report.md` for the full mapping and
# the caution about not trusting column *position* blindly -- this
# constant is the single place that encodes it, matched by substring
# rather than raw index wherever this module reads a column).
_TIMESTAMP = "Timestamp"
_CONSENT = "I have read the information above and I voluntarily agree to participate."
_ROLE = "Which best describes your primary professional role?"
_YEARS_EXPERIENCE = "How many years of professional work experience do you have?"
_AI_YEARS_EXPERIENCE = (
    "How many years of experience do you have specifically in AI, data, "
    "or related technology fields?"
)
_LEADERSHIP_EXPERIENCE = (
    "Do you have experience leading, managing, or hiring for "
    "AI/technology roles or teams?"
)
_RELEVANCE_PREFIX = (
    "For each dimension, please rate how relevant it is as an "
    "observable credential signal when assessing AI leadership."
)
_CLARITY_PREFIX = "How clear and distinct is this dimension"
_APPROPRIATENESS = "Overall, how appropriate is the six-dimensional ALCSM framework"
_MOST_IMPORTANT = "Which of the six dimensions do you consider MOST important"
_MISSING_SIGNAL = (
    "Is there any important credential signal associated with AI leadership"
)
_DISTINCTIVENESS_PREFIX = "How distinct is this dimension from the other dimensions"

_CONSENT_YES_VALUE = "Yes, I agree to participate"

_RELEVANCE_SCALE = {
    "1 — Not at all relevant": 1,
    "2 — Slightly relevant": 2,
    "3 — Moderately relevant": 3,
    "4 — Very relevant": 4,
    "5 — Extremely relevant": 5,
}
_CLARITY_SCALE = {
    "Very unclear / not distinct": 1,
    "Somewhat unclear / weakly distinct": 2,
    "Moderately clear / moderately distinct": 3,
    "Clear / clearly distinct": 4,
    "Very clear / highly distinct": 5,
}
_APPROPRIATENESS_SCALE = {
    "1 — Not at all appropriate": 1,
    "2 — Slightly appropriate": 2,
    "3 — Moderately appropriate": 3,
    "4 — Very appropriate": 4,
    "5 — Extremely appropriate": 5,
}
_DISTINCTIVENESS_SCALE = {
    "1 — Not at all distinct": 1,
    "2 — Slightly distinct": 2,
    "3 — Moderately distinct": 3,
    "4 — Very distinct": 4,
    "5 — Extremely distinct": 5,
}

_LEADING_DIGIT = re.compile(r"^\s*(\d+)\s*[—\-–]")


def _parse_ordinal(value: object, scale: dict[str, int]) -> float | None:
    """Map a Likert text label to its numeric code. Tries the explicit
    scale dict first (exact match); falls back to a leading-digit
    regex for any "N — label" format not already in the dict, so a
    label with slightly different wording than the constants above
    still parses rather than silently becoming a missing value."""
    if value is None or (isinstance(value, float) and value != value):  # NaN
        return None
    text = str(value).strip()
    if text in scale:
        return float(scale[text])
    match = _LEADING_DIGIT.match(text)
    if match:
        return float(match.group(1))
    return None


def _find_column(
    columns: list[str], prefix: str, dimension_suffix: str | None = None
) -> str:
    for c in columns:
        if c.startswith(prefix) and (
            dimension_suffix is None or c.endswith(dimension_suffix)
        ):
            return c
    raise KeyError(
        f"no column found starting with {prefix!r} (suffix={dimension_suffix!r})"
    )


@dataclass(frozen=True)
class SurveyRatings:
    """Tidy, long-format numeric ratings: one row per (respondent,
    dimension, item_type)."""

    respondent_id: str
    dimension_number: int
    item_type: str  # 'relevance' | 'clarity' | 'distinctiveness'
    value: float | None  # None = respondent did not answer this item


@dataclass(frozen=True)
class SurveyRespondentProfile:
    respondent_id: str
    role: str | None
    years_experience: str | None
    ai_years_experience: str | None
    leadership_experience: str | None
    overall_appropriateness: float | None
    most_important_dimension: str | None


@dataclass(frozen=True)
class SurveyFreeText:
    """Free-text presence only -- `has_response` is a boolean, the
    actual comment is never carried into this dataclass or anywhere
    else in this package."""

    respondent_id: str
    has_missing_signal_comment: bool


@dataclass(frozen=True)
class ReshapedSurvey:
    n_respondents: int
    n_consented: int
    ratings: list[SurveyRatings]
    respondents: list[SurveyRespondentProfile]
    free_text_presence: list[SurveyFreeText]


def reshape_survey_responses(raw: pd.DataFrame) -> ReshapedSurvey:
    """Reshape the raw wide Google-Forms export into tidy, analysis-ready
    structures. Excludes any respondent row whose consent column is not
    exactly the "yes" value (schema `survey_respondent.consent_confirmed`
    CHECK — only consented records are ever retained/analyzed)."""
    columns = list(raw.columns)

    # Resolved once via prefix match, never assumed to equal a fully
    # hand-transcribed constant -- several of this module's question-
    # text constants were captured from a truncated preview during
    # inspection (see `Analysis_Preparation_Completion_Report.md`) and
    # are deliberately short prefixes, not full text, for exactly this
    # reason: matching the start of a long column header is robust to
    # a constant being shorter than the real text, matching the full
    # text is not.
    consent_col = _find_column(columns, _CONSENT)
    role_col = _find_column(columns, _ROLE)
    years_experience_col = _find_column(columns, _YEARS_EXPERIENCE)
    ai_years_experience_col = _find_column(columns, _AI_YEARS_EXPERIENCE)
    leadership_experience_col = _find_column(columns, _LEADERSHIP_EXPERIENCE)
    appropriateness_col = _find_column(columns, _APPROPRIATENESS)
    most_important_col = _find_column(columns, _MOST_IMPORTANT)
    missing_signal_col = _find_column(columns, _MISSING_SIGNAL)

    consented = raw[raw[consent_col] == _CONSENT_YES_VALUE].reset_index(drop=True)

    relevance_cols = {
        d.number: _find_column(columns, _RELEVANCE_PREFIX, f"[D{d.number} — {d.label}]")
        for d in _SURVEY_DIMENSIONS
    }
    clarity_cols = {
        d.number: _find_column(columns, _CLARITY_PREFIX, f"[D{d.number} — {d.label}]")
        for d in _SURVEY_DIMENSIONS
    }
    distinctiveness_cols = {
        d.number: _find_column(
            columns, _DISTINCTIVENESS_PREFIX, f"[D{d.number} — {d.label}]"
        )
        for d in _SURVEY_DIMENSIONS
    }

    ratings: list[SurveyRatings] = []
    respondents: list[SurveyRespondentProfile] = []
    free_text: list[SurveyFreeText] = []

    for i, row in consented.iterrows():
        respondent_id = (
            f"RSP-{i + 1:04d}"  # assigned at load time; see module docstring caveat
        )
        for d in _SURVEY_DIMENSIONS:
            ratings.append(
                SurveyRatings(
                    respondent_id,
                    d.number,
                    "relevance",
                    _parse_ordinal(row[relevance_cols[d.number]], _RELEVANCE_SCALE),
                )
            )
            ratings.append(
                SurveyRatings(
                    respondent_id,
                    d.number,
                    "clarity",
                    _parse_ordinal(row[clarity_cols[d.number]], _CLARITY_SCALE),
                )
            )
            ratings.append(
                SurveyRatings(
                    respondent_id,
                    d.number,
                    "distinctiveness",
                    _parse_ordinal(
                        row[distinctiveness_cols[d.number]], _DISTINCTIVENESS_SCALE
                    ),
                )
            )
        respondents.append(
            SurveyRespondentProfile(
                respondent_id=respondent_id,
                role=(row[role_col] if pd.notna(row[role_col]) else None),
                years_experience=(
                    row[years_experience_col]
                    if pd.notna(row[years_experience_col])
                    else None
                ),
                ai_years_experience=(
                    row[ai_years_experience_col]
                    if pd.notna(row[ai_years_experience_col])
                    else None
                ),
                leadership_experience=(
                    row[leadership_experience_col]
                    if pd.notna(row[leadership_experience_col])
                    else None
                ),
                overall_appropriateness=_parse_ordinal(
                    row[appropriateness_col], _APPROPRIATENESS_SCALE
                ),
                most_important_dimension=(
                    row[most_important_col]
                    if pd.notna(row[most_important_col])
                    else None
                ),
            )
        )
        free_text.append(
            SurveyFreeText(
                respondent_id=respondent_id,
                has_missing_signal_comment=pd.notna(row[missing_signal_col]),
            )
        )

    return ReshapedSurvey(
        n_respondents=len(raw),
        n_consented=len(consented),
        ratings=ratings,
        respondents=respondents,
        free_text_presence=free_text,
    )


def participant_background_summary(survey: ReshapedSurvey) -> dict[str, pd.Series]:
    """Descriptive counts of who took the survey: professional role,
    years of professional experience, years of AI/tech experience, and
    AI/tech leadership experience -- each as a value-count `pd.Series`
    over the consented respondents.

    Purely descriptive (no inference, no test statistic). A `None`
    value (respondent left the field blank) is counted under its own
    `None` category rather than dropped, so every series still sums to
    `survey.n_consented`.
    """
    fields = {
        "role": [p.role for p in survey.respondents],
        "years_experience": [p.years_experience for p in survey.respondents],
        "ai_years_experience": [p.ai_years_experience for p in survey.respondents],
        "leadership_experience": [p.leadership_experience for p in survey.respondents],
    }
    return {
        name: pd.Series(values, dtype=object).value_counts(dropna=False)
        for name, values in fields.items()
    }
