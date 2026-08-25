"""RQ3 validation: content validity, inter-rater reliability (human-only),
researcher review-change concordance."""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.rq3_validation import (
    NotAHumanRaterError,
    content_validity_summary,
    inter_rater_reliability,
    ratings_from_dimension_evidence,
    researcher_review_changes_summary,
)
from alcsm.analysis.survey import reshape_survey_responses


class TestContentValiditySummary:
    def test_covers_all_six_dimensions(
        self, synthetic_survey_raw: pd.DataFrame
    ) -> None:
        survey = reshape_survey_responses(synthetic_survey_raw)
        result = content_validity_summary(survey)
        assert len(result.relevance_by_dimension) == 6
        assert len(result.clarity_by_dimension) == 6

    def test_distinctiveness_shows_zero_answered(
        self, synthetic_survey_raw: pd.DataFrame
    ) -> None:
        survey = reshape_survey_responses(synthetic_survey_raw)
        result = content_validity_summary(survey)
        assert (result.distinctiveness_by_dimension["n_answered"] == 0).all()

    def test_missing_signal_comment_count_not_content(
        self, synthetic_survey_raw: pd.DataFrame
    ) -> None:
        survey = reshape_survey_responses(synthetic_survey_raw)
        result = content_validity_summary(survey)
        assert isinstance(result.n_respondents_with_missing_signal_comment, int)
        assert result.n_respondents_with_missing_signal_comment >= 1

    def test_most_important_dimension_counts_sum_to_answered(
        self, synthetic_survey_raw: pd.DataFrame
    ) -> None:
        survey = reshape_survey_responses(synthetic_survey_raw)
        result = content_validity_summary(survey)
        n_answered = sum(
            1 for r in survey.respondents if r.most_important_dimension is not None
        )
        assert result.most_important_dimension_counts.sum() == n_answered


class TestInterRaterReliabilityHumanOnlyGuard:
    def test_refuses_a_first_pass_rater_id(self) -> None:
        ratings = {1: {"U0": {"RATER_A": 3.0, "FIRST_PASS": 4.0}}}
        with pytest.raises(NotAHumanRaterError):
            inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")

    def test_refuses_an_ai_rater_id(self) -> None:
        ratings = {1: {"U0": {"RATER_A": 3.0, "AI_ASSISTED": 4.0}}}
        with pytest.raises(NotAHumanRaterError):
            inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")

    def test_refuses_researcher_final_disguised_as_rater(self) -> None:
        """The precise scenario this task's explicit instruction forbids:
        treating the AI-assisted first pass and the researcher's final
        review as if they were two independent human raters."""
        ratings = {1: {"U0": {"RATER_A": 3.0, "RESEARCHER_FINAL": 4.0}}}
        with pytest.raises(NotAHumanRaterError):
            inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")

    def test_accepts_genuine_human_raters(self) -> None:
        ratings = {
            n: {
                f"U{i}": {"RATER_A": float((i + n) % 6), "RATER_B": float((i + n) % 6)}
                for i in range(5)
            }
            for n in range(1, 7)
        }
        report = inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")
        assert len(report.by_dimension) == 6
        for verdict in report.by_dimension.values():
            assert verdict.verdict == "proceed"  # perfect agreement fixture

    def test_verdict_thresholds(self) -> None:
        # Alpha near zero (near-chance agreement) -> revise_rulebook_wording
        ratings = {
            1: {
                "U0": {"RATER_A": 0.0, "RATER_B": 5.0},
                "U1": {"RATER_A": 5.0, "RATER_B": 0.0},
                "U2": {"RATER_A": 0.0, "RATER_B": 5.0},
                "U3": {"RATER_A": 5.0, "RATER_B": 0.0},
            }
        }
        report = inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")
        assert report.by_dimension[1].verdict in {
            "revise_rulebook_wording",
            "acceptable_with_review",
        }

    def test_never_pooled_across_dimensions(self) -> None:
        ratings = {
            1: {
                "U0": {"RATER_A": 5.0, "RATER_B": 5.0},
                "U1": {"RATER_A": 5.0, "RATER_B": 5.0},
            },
            2: {
                "U0": {"RATER_A": 0.0, "RATER_B": 5.0},
                "U1": {"RATER_A": 5.0, "RATER_B": 0.0},
            },
        }
        report = inter_rater_reliability(ratings, "pilot", "profile", "1.0", "fixture")
        assert (
            report.by_dimension[1].result.krippendorff_alpha
            != report.by_dimension[2].result.krippendorff_alpha
        )


class TestRatingsFromDimensionEvidenceAdapter:
    def test_builds_expected_nested_shape(self) -> None:
        rater_a = pd.DataFrame(
            [{"Profile_ID": "PRF-00001", "Dimension": "D1", "Score": 3}]
        )
        rater_b = pd.DataFrame(
            [{"Profile_ID": "PRF-00001", "Dimension": "D1", "Score": 4}]
        )
        result = ratings_from_dimension_evidence(
            {"RATER_A": rater_a, "RATER_B": rater_b}
        )
        assert result[1]["PRF-00001"] == {"RATER_A": 3.0, "RATER_B": 4.0}


class TestResearcherReviewChangesSummary:
    def test_empty_sheet_produces_all_zero_summary(
        self, empty_review_changes: pd.DataFrame
    ) -> None:
        result = researcher_review_changes_summary(empty_review_changes)
        assert (result.n_changes_by_dimension == 0).all()

    def test_never_uses_reliability_language(self) -> None:
        from dataclasses import fields

        from alcsm.analysis.rq3_validation import ReviewChangeConcordance

        field_names = {f.name for f in fields(ReviewChangeConcordance)}
        assert not any(
            "alpha" in f.lower() or "reliability" in f.lower() for f in field_names
        )

    def test_counts_and_direction_match_fixture(
        self, synthetic_review_changes: pd.DataFrame
    ) -> None:
        result = researcher_review_changes_summary(synthetic_review_changes)
        assert result.n_changes_by_dimension["D5"] == 2
        assert result.n_changes_by_dimension["D2"] == 1
        assert result.direction_counts.loc["D5", "decreased"] == 1
        assert result.direction_counts.loc["D5", "unchanged"] == 1
        assert result.direction_counts.loc["D2", "increased"] == 1

    def test_precedent_usage_counted(
        self, synthetic_review_changes: pd.DataFrame
    ) -> None:
        result = researcher_review_changes_summary(synthetic_review_changes)
        assert result.precedent_usage_counts["P-03"] == 1
        assert result.precedent_usage_counts["P-02"] == 1

    def test_mean_absolute_change_computed_correctly(
        self, synthetic_review_changes: pd.DataFrame
    ) -> None:
        result = researcher_review_changes_summary(synthetic_review_changes)
        assert result.mean_absolute_change_by_dimension["D5"] == pytest.approx(1.0)


def test_review_changes_never_calls_into_krippendorff_module() -> None:
    """Structural guard: `researcher_review_changes_summary` must never
    call into `alcsm.reliability.krippendorff` -- it is a different
    kind of statistic entirely (module docstring item 3)."""
    import ast
    import inspect

    from alcsm.analysis import rq3_validation

    tree = ast.parse(
        inspect.getsource(rq3_validation.researcher_review_changes_summary)
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert "alpha" not in node.func.id.lower()
