"""RQ1 descriptive analysis: demographics, distributions, missingness,
grouped patterns, dimension-level comparison."""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.config import DataNotFrozenError
from alcsm.analysis.rq1_descriptive import (
    company_size_patterns,
    demographic_summary,
    dimension_distribution,
    dimension_level_comparison,
    dimension_missingness,
    industry_patterns,
    title_category_patterns,
)


def test_demographic_summary_counts(synthetic_profile_master: pd.DataFrame) -> None:
    result = demographic_summary(synthetic_profile_master)
    assert result.n_profiles == len(synthetic_profile_master)
    assert result.metadata.data_status == "final_frozen"
    assert result.industry_counts.sum() == len(synthetic_profile_master)
    assert result.company_size_counts.sum() == len(synthetic_profile_master)


class TestDimensionDistribution:
    def test_provisional_without_acknowledgement_raises(
        self, synthetic_profile_scores_provisional: pd.DataFrame
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            dimension_distribution(
                synthetic_profile_scores_provisional,
                "provisional_first_pass",
                "fixture",
            )

    def test_provisional_with_acknowledgement_runs(
        self, synthetic_profile_scores_provisional: pd.DataFrame
    ) -> None:
        result = dimension_distribution(
            synthetic_profile_scores_provisional,
            "provisional_first_pass",
            "fixture",
            acknowledge_provisional=True,
        )
        assert result.metadata.data_status == "provisional_first_pass"

    def test_counts_sum_to_n_profiles_per_dimension(
        self, synthetic_profile_scores_final: pd.DataFrame
    ) -> None:
        result = dimension_distribution(
            synthetic_profile_scores_final, "final_frozen", "fixture"
        )
        for col in result.counts.columns:
            assert result.counts[col].sum() == len(synthetic_profile_scores_final)

    def test_means_within_score_range(
        self, synthetic_profile_scores_final: pd.DataFrame
    ) -> None:
        result = dimension_distribution(
            synthetic_profile_scores_final, "final_frozen", "fixture"
        )
        assert (result.means >= 0).all()
        assert (result.means <= 5).all()

    def test_first_pass_vs_final_are_independently_selectable(
        self, synthetic_profile_scores_final: pd.DataFrame
    ) -> None:
        df = synthetic_profile_scores_final.copy()
        df["D1_Final"] = 5  # diverge Final from FirstPass
        final_result = dimension_distribution(
            df, "final_frozen", "fixture", use_final=True
        )
        first_pass_result = dimension_distribution(
            df, "final_frozen", "fixture", use_final=False
        )
        assert final_result.means["D1"] == 5.0
        assert first_pass_result.means["D1"] != 5.0


class TestMissingness:
    def test_by_dimension_covers_all_six(
        self, synthetic_dimension_evidence: pd.DataFrame
    ) -> None:
        result = dimension_missingness(
            synthetic_dimension_evidence, "final_frozen", "fixture"
        )
        assert list(result.by_dimension.index) == [f"D{n}" for n in range(1, 7)]

    def test_counts_sum_to_row_count_per_dimension(
        self, synthetic_dimension_evidence: pd.DataFrame
    ) -> None:
        result = dimension_missingness(
            synthetic_dimension_evidence, "final_frozen", "fixture"
        )
        n_profiles = synthetic_dimension_evidence["Profile_ID"].nunique()
        assert (result.by_dimension.sum(axis=1) == n_profiles).all()


class TestGroupedPatterns:
    def test_title_category_patterns_covers_every_present_category(
        self,
        synthetic_profile_master: pd.DataFrame,
        synthetic_profile_scores_final: pd.DataFrame,
    ) -> None:
        result = title_category_patterns(
            synthetic_profile_master,
            synthetic_profile_scores_final,
            "final_frozen",
            "fixture",
        )
        assert set(result.means.index) == set(
            synthetic_profile_master["Title_Category"].unique()
        )

    def test_company_size_patterns_n_per_group_sums_correctly(
        self,
        synthetic_profile_master: pd.DataFrame,
        synthetic_profile_scores_final: pd.DataFrame,
    ) -> None:
        result = company_size_patterns(
            synthetic_profile_master,
            synthetic_profile_scores_final,
            "final_frozen",
            "fixture",
        )
        assert result.n_per_group.sum() == len(synthetic_profile_master)

    def test_industry_patterns_gated_on_provisional(
        self,
        synthetic_profile_master: pd.DataFrame,
        synthetic_profile_scores_provisional: pd.DataFrame,
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            industry_patterns(
                synthetic_profile_master,
                synthetic_profile_scores_provisional,
                "provisional_first_pass",
                "fixture",
            )


class TestDimensionLevelComparison:
    def test_table_has_one_row_per_dimension(
        self,
        synthetic_profile_scores_final: pd.DataFrame,
        synthetic_dimension_evidence: pd.DataFrame,
    ) -> None:
        result = dimension_level_comparison(
            synthetic_profile_scores_final,
            synthetic_dimension_evidence,
            "final_frozen",
            "fixture",
        )
        assert len(result.table) == 6

    def test_never_produces_a_composite_column(
        self,
        synthetic_profile_scores_final: pd.DataFrame,
        synthetic_dimension_evidence: pd.DataFrame,
    ) -> None:
        result = dimension_level_comparison(
            synthetic_profile_scores_final,
            synthetic_dimension_evidence,
            "final_frozen",
            "fixture",
        )
        forbidden = {"composite", "total", "sum", "alcsm_total", "weighted"}
        assert not forbidden & set(c.lower() for c in result.table.columns)
