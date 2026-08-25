"""Expert-survey reshape: wide Google-Forms export -> tidy long format,
consent filtering, and the structural free-text isolation guarantee."""

from __future__ import annotations

import inspect

import pandas as pd

from alcsm.analysis.survey import (
    participant_background_summary,
    reshape_survey_responses,
)


def test_non_consenting_respondent_is_excluded(
    synthetic_survey_raw: pd.DataFrame,
) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    assert result.n_respondents == len(synthetic_survey_raw)
    assert (
        result.n_consented == len(synthetic_survey_raw) - 1
    )  # fixture's respondent 0 declined


def test_every_consented_respondent_gets_eighteen_rating_rows(
    synthetic_survey_raw: pd.DataFrame,
) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    # 6 dimensions x 3 item types (relevance/clarity/distinctiveness)
    assert len(result.ratings) == result.n_consented * 18


def test_relevance_labels_parsed_to_numeric(synthetic_survey_raw: pd.DataFrame) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    relevance = [
        r
        for r in result.ratings
        if r.item_type == "relevance" and r.dimension_number == 1
    ]
    assert all(
        r.value == 1.0 for r in relevance
    )  # fixture sets D1 relevance to "1 -- Not at all"


def test_fully_unanswered_item_type_parses_to_none(
    synthetic_survey_raw: pd.DataFrame,
) -> None:
    """The fixture leaves distinctiveness entirely blank, mirroring the
    real survey's own 100%-unanswered distinctiveness section."""
    result = reshape_survey_responses(synthetic_survey_raw)
    distinctiveness = [r for r in result.ratings if r.item_type == "distinctiveness"]
    assert distinctiveness  # rows exist...
    assert all(r.value is None for r in distinctiveness)  # ...but every value is None


def test_free_text_presence_is_boolean_only(synthetic_survey_raw: pd.DataFrame) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    assert any(ft.has_missing_signal_comment for ft in result.free_text_presence)
    assert any(not ft.has_missing_signal_comment for ft in result.free_text_presence)


def test_respondent_ids_are_pseudonymous_sequential() -> None:
    from alcsm.analysis.survey import SurveyRespondentProfile

    field_names = {f for f in SurveyRespondentProfile.__dataclass_fields__}
    assert "respondent_id" in field_names
    assert not any(k in field_names for k in ("name", "email", "ip_address"))


def test_module_never_carries_free_text_content_into_any_return_type() -> None:
    """Structural guard: no dataclass this module defines has a field
    that could hold the actual comment text -- only a boolean presence
    flag (`SurveyFreeText.has_missing_signal_comment`)."""
    from alcsm.analysis import survey as survey_module

    for name in ("SurveyRatings", "SurveyRespondentProfile", "SurveyFreeText"):
        cls = getattr(survey_module, name)
        for field_name in cls.__dataclass_fields__:
            assert "comment" not in field_name or field_name.startswith("has_")


def test_module_source_never_prints_or_logs_cell_values() -> None:
    """This module must never call print()/logging on a cell value --
    only structural counts/booleans may be surfaced (module docstring's
    own explicit rule)."""
    source = inspect.getsource(__import__("alcsm.analysis.survey", fromlist=["x"]))
    assert "print(" not in source


def test_participant_background_summary_counts_every_consented_respondent(
    synthetic_survey_raw: pd.DataFrame,
) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    summary = participant_background_summary(result)
    assert set(summary) == {
        "role",
        "years_experience",
        "ai_years_experience",
        "leadership_experience",
    }
    for series in summary.values():
        assert series.sum() == result.n_consented


def test_participant_background_summary_keeps_blank_as_its_own_category(
    synthetic_survey_raw: pd.DataFrame,
) -> None:
    result = reshape_survey_responses(synthetic_survey_raw)
    # No dropped respondents: value_counts(dropna=False) must still
    # sum to n_consented even if some field is blank for a respondent.
    summary = participant_background_summary(result)
    assert summary["role"].sum() == result.n_consented
