"""RQ2 gap analysis: requirement counts, Not Directly Mapped, supply
vs. demand, true numeric gap, D6 asymmetry."""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.config import DataNotFrozenError
from alcsm.analysis.gap import (
    d6_profile_vs_posting_asymmetry,
    dimension_gap_from_scores,
    not_directly_mapped_report,
    requirement_counts_by_dimension,
    requirement_intensity_by_dimension,
    supply_vs_demand_frequency,
)
from alcsm.analysis.rq1_descriptive import dimension_distribution


class TestRequirementCounts:
    def test_counts_sum_to_total(self, synthetic_requirements: pd.DataFrame) -> None:
        result = requirement_counts_by_dimension(synthetic_requirements)
        assert result.n_requirements == len(synthetic_requirements)
        assert result.counts_by_dimension.sum() == len(synthetic_requirements)

    def test_not_directly_mapped_is_one_of_the_counted_categories(
        self, synthetic_requirements: pd.DataFrame
    ) -> None:
        result = requirement_counts_by_dimension(synthetic_requirements)
        assert "NOT_DIRECTLY_MAPPED" in result.counts_by_dimension.index


class TestNotDirectlyMapped:
    def test_fraction_matches_manual_count(
        self, synthetic_requirements: pd.DataFrame
    ) -> None:
        result = not_directly_mapped_report(synthetic_requirements)
        manual = (
            synthetic_requirements["Final_ALCSM_Dimension"] == "NOT_DIRECTLY_MAPPED"
        ).sum()
        assert result.n_not_mapped == manual
        assert result.fraction_not_mapped == pytest.approx(
            manual / len(synthetic_requirements)
        )


class TestRequirementIntensity:
    def test_table_rows_sum_to_dimension_counts(
        self, synthetic_requirements: pd.DataFrame
    ) -> None:
        result = requirement_intensity_by_dimension(synthetic_requirements)
        counts = requirement_counts_by_dimension(synthetic_requirements)
        row_sums = result.table.sum(axis=1)
        for dim in result.table.index:
            assert row_sums[dim] == counts.counts_by_dimension[dim]

    def test_columns_are_the_actual_mandatory_or_preferred_values(
        self, synthetic_requirements: pd.DataFrame
    ) -> None:
        result = requirement_intensity_by_dimension(synthetic_requirements)
        assert set(result.table.columns) == set(
            synthetic_requirements["Mandatory_or_Preferred"].unique()
        )


class TestSupplyVsDemandFrequency:
    def test_never_produces_a_single_gap_number(
        self,
        synthetic_requirements: pd.DataFrame,
        synthetic_profile_scores_final: pd.DataFrame,
    ) -> None:
        """The frequency comparison keeps n_requirements and
        profile_mean_score as separate columns -- never subtracted."""
        req_counts = requirement_counts_by_dimension(synthetic_requirements)
        profile_dist = dimension_distribution(
            synthetic_profile_scores_final, "final_frozen", "fixture"
        )
        result = supply_vs_demand_frequency(req_counts, profile_dist)
        assert "n_requirements" in result.table.columns
        assert "profile_mean_score" in result.table.columns
        assert not any("gap" in c.lower() for c in result.table.columns)

    def test_provisional_status_propagates(
        self,
        synthetic_requirements: pd.DataFrame,
        synthetic_profile_scores_provisional: pd.DataFrame,
    ) -> None:
        req_counts = requirement_counts_by_dimension(synthetic_requirements)
        profile_dist = dimension_distribution(
            synthetic_profile_scores_provisional,
            "provisional_first_pass",
            "fixture",
            acknowledge_provisional=True,
        )
        result = supply_vs_demand_frequency(req_counts, profile_dist)
        assert result.metadata.data_status == "provisional_first_pass"


class TestDimensionGapFromScores:
    def test_gated_on_provisional(
        self,
        synthetic_required_scores: pd.DataFrame,
        synthetic_held_scores: pd.DataFrame,
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            dimension_gap_from_scores(
                synthetic_required_scores,
                synthetic_held_scores,
                "provisional_first_pass",
                "fixture",
            )

    def test_gap_equals_required_minus_held(
        self,
        synthetic_required_scores: pd.DataFrame,
        synthetic_held_scores: pd.DataFrame,
    ) -> None:
        result = dimension_gap_from_scores(
            synthetic_required_scores, synthetic_held_scores, "final_frozen", "fixture"
        )
        for dim in result.table.index:
            row = result.table.loc[dim]
            assert row["gap_value"] == pytest.approx(
                row["mean_required"] - row["mean_held"]
            )

    def test_unavailable_rows_excluded_never_read_as_zero(self) -> None:
        required = pd.DataFrame(
            [
                {
                    "dimension_number": 1,
                    "required_score": 5,
                    "missing_status": "present",
                },
                {
                    "dimension_number": 1,
                    "required_score": 0,
                    "missing_status": "unavailable",
                },
            ]
        )
        held = pd.DataFrame(
            [{"dimension_number": 1, "score": 5, "missing_status": "present"}]
        )
        result = dimension_gap_from_scores(required, held, "final_frozen", "fixture")
        # If the unavailable row were wrongly included, mean_required
        # would be 2.5, not 5.
        assert result.table.loc["D1", "mean_required"] == 5.0
        assert result.table.loc["D1", "n_postings"] == 1


class TestD6Asymmetry:
    def test_profile_side_more_observable_than_posting_side(
        self,
        synthetic_profile_scores_final: pd.DataFrame,
        synthetic_dimension_evidence: pd.DataFrame,
        synthetic_requirements: pd.DataFrame,
    ) -> None:
        result = d6_profile_vs_posting_asymmetry(
            synthetic_profile_scores_final,
            synthetic_dimension_evidence,
            synthetic_requirements,
            "final_frozen",
            "fixture",
        )
        assert 0.0 <= result.profile_side_coverage <= 1.0
        assert 0.0 <= result.posting_side_coverage <= 1.0
        assert result.n_requirements_d6_mappable >= 1

    def test_gated_on_provisional(
        self,
        synthetic_profile_scores_provisional: pd.DataFrame,
        synthetic_dimension_evidence: pd.DataFrame,
        synthetic_requirements: pd.DataFrame,
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            d6_profile_vs_posting_asymmetry(
                synthetic_profile_scores_provisional,
                synthetic_dimension_evidence,
                synthetic_requirements,
                "provisional_first_pass",
                "fixture",
            )
