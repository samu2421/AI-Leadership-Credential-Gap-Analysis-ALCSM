"""Tests for the P6 double-coding subset reliability workflow.

Everything here runs against small, hand-built synthetic fixtures --
no real second-rater dataset exists yet (none is fabricated here
either). The point of these tests is to verify the *mechanics*: that
unavailable/blank cells are excluded rather than coerced to 0, that
each dimension is scored independently (never pooled), that the
RATER_A/RATER_B guard still fires through this module, and that the
descriptive statistics (distribution, missing counts) are computed
correctly against a known small case.
"""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.rq3_validation import NotAHumanRaterError
from alcsm.reliability.subset_workflow import (
    load_primary_scores_long,
    load_second_rater_scores_long,
    run_subset_reliability_analysis,
)


def _primary_long(rows: list[tuple[str, str, float]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["Profile_ID", "Dimension", "Score"])


def _second_long(rows: list[tuple[str, str, float]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["Profile_ID", "Dimension", "Score"])


class TestPerfectAgreementFixture:
    """Four profiles, two dimensions, both raters agree on everything
    that both scored -- alpha should be 1.0 (or undefined only if
    variance is zero, which D2 below deliberately avoids)."""

    def _ratings(self) -> tuple[pd.DataFrame, pd.DataFrame, set[str]]:
        primary = _primary_long(
            [
                ("P1", "D1", 3),
                ("P2", "D1", 4),
                ("P3", "D1", 2),
                ("P4", "D1", 3),
                ("P1", "D2", 1),
                ("P2", "D2", 0),
                ("P3", "D2", 2),
                ("P4", "D2", 1),
            ]
        )
        second = _second_long(
            [
                ("P1", "D1", 3),
                ("P2", "D1", 4),
                ("P3", "D1", 2),
                ("P4", "D1", 3),
                ("P1", "D2", 1),
                ("P2", "D2", 0),
                ("P3", "D2", 2),
                ("P4", "D2", 1),
            ]
        )
        return primary, second, {"P1", "P2", "P3", "P4"}

    def test_alpha_is_one_for_perfect_agreement(self) -> None:
        primary, second, subset = self._ratings()
        results = run_subset_reliability_analysis(primary, second, subset)
        assert results[1].krippendorff_alpha == pytest.approx(1.0)
        assert results[2].krippendorff_alpha == pytest.approx(1.0)

    def test_percent_agreement_is_one(self) -> None:
        primary, second, subset = self._ratings()
        results = run_subset_reliability_analysis(primary, second, subset)
        assert results[1].percent_agreement == pytest.approx(1.0)

    def test_n_units_counts_only_dually_scored_profiles(self) -> None:
        primary, second, subset = self._ratings()
        results = run_subset_reliability_analysis(primary, second, subset)
        assert results[1].n_units == 4

    def test_dimensions_never_pooled(self) -> None:
        """D1 and D2 are returned as independent summaries -- no
        combined/averaged alpha appears anywhere in the result."""
        primary, second, subset = self._ratings()
        results = run_subset_reliability_analysis(primary, second, subset)
        assert set(results.keys()) == {1, 2}
        assert results[1] is not results[2]
        assert not hasattr(results, "pooled_alpha")


class TestUnavailableHandling:
    """The core Part 5 rule: a unit unavailable for either rater is
    excluded from that dimension's alpha computation entirely -- never
    treated as an observed 0."""

    def test_profile_unavailable_for_one_rater_is_excluded(self) -> None:
        # P3 has no D1 row from the second rater (unavailable) -- it
        # must not silently become a 0 vs 2 disagreement.
        primary = _primary_long(
            [("P1", "D1", 2), ("P2", "D1", 2), ("P3", "D1", 2), ("P4", "D1", 2)]
        )
        second = _second_long([("P1", "D1", 2), ("P2", "D1", 2), ("P4", "D1", 2)])
        subset = {"P1", "P2", "P3", "P4"}

        results = run_subset_reliability_analysis(primary, second, subset)
        # Only P1, P2, P4 are dually scored -> n_units == 3, not 4.
        assert results[1].n_units == 3
        assert results[1].krippendorff_alpha == pytest.approx(1.0)

    def test_unavailable_counts_are_reported_separately(self) -> None:
        # P1 and P4 are dually scored (>=2 comparable units needed for
        # alpha to be defined); P2 is scored by the primary only; P3
        # is scored by neither.
        primary = _primary_long([("P1", "D1", 2), ("P2", "D1", 2), ("P4", "D1", 3)])
        second = _second_long([("P1", "D1", 2), ("P4", "D1", 3)])
        subset = {"P1", "P2", "P3", "P4"}

        results = run_subset_reliability_analysis(primary, second, subset)
        summary = results[1]
        # P3 unavailable for both raters; P2 unavailable for the
        # second rater only.
        assert summary.primary_unavailable_count == 1  # P3
        assert summary.second_rater_unavailable_count == 2  # P2, P3
        assert summary.both_unavailable_count == 1  # P3

    def test_known_data_integrity_profiles_pattern(self) -> None:
        """Mirrors the real LP0041/LP0170/LP0182 case: neither rater
        scores D6 for a profile with no Professional_Experience
        section. That profile must contribute zero rows to either
        rater's long frame for D6 (enforced upstream by the loaders in
        TestLoaders) -- here we confirm the analysis step never
        fabricates a (0, 0) agreement pair for it: with other profiles
        providing real D6 data, LP0041 simply doesn't count toward
        n_units."""
        primary = _primary_long([("LP0002", "D6", 2), ("LP0003", "D6", 2)])
        second = _second_long([("LP0002", "D6", 2), ("LP0003", "D6", 2)])
        subset = {"LP0041", "LP0002", "LP0003"}

        results = run_subset_reliability_analysis(primary, second, subset)
        assert results[6].n_units == 2
        assert results[6].both_unavailable_count == 1  # LP0041 only


class TestTransparentDiagnosticStats:
    """The FINAL RELIABILITY DIAGNOSIS task's Part 2 additions: per-rater
    variance/category counts and the disagreement-magnitude
    distribution, alongside the existing pooled statistics."""

    def _mixed_disagreement_fixture(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame, set[str]]:
        # P1: exact match (0 apart). P2: 1 apart. P3: 2 apart. P4: 1 apart.
        primary = _primary_long(
            [("P1", "D3", 3), ("P2", "D3", 3), ("P3", "D3", 2), ("P4", "D3", 4)]
        )
        second = _second_long(
            [("P1", "D3", 3), ("P2", "D3", 4), ("P3", "D3", 4), ("P4", "D3", 3)]
        )
        return primary, second, {"P1", "P2", "P3", "P4"}

    def test_disagreement_magnitude_distribution(self) -> None:
        primary, second, subset = self._mixed_disagreement_fixture()
        results = run_subset_reliability_analysis(primary, second, subset)
        summary = results[3]
        assert summary.disagreement_magnitude_distribution == {0: 1, 1: 2, 2: 1}

    def test_exact_agreement_count_matches_zero_magnitude_bucket(self) -> None:
        primary, second, subset = self._mixed_disagreement_fixture()
        results = run_subset_reliability_analysis(primary, second, subset)
        summary = results[3]
        assert summary.exact_agreement_count == 1
        assert summary.exact_agreement_count == pytest.approx(
            summary.percent_agreement * summary.n_units
        )

    def test_per_rater_variance_computed_independently(self) -> None:
        primary, second, subset = self._mixed_disagreement_fixture()
        results = run_subset_reliability_analysis(primary, second, subset)
        summary = results[3]
        # Rater A: [3,3,2,4] -> mean 3.0, variance 0.5
        assert summary.rater_a_variance == pytest.approx(0.5)
        # Rater B: [3,4,4,3] -> mean 3.5, variance 0.25
        assert summary.rater_b_variance == pytest.approx(0.25)

    def test_n_categories_counts_distinct_values_used(self) -> None:
        primary, second, subset = self._mixed_disagreement_fixture()
        results = run_subset_reliability_analysis(primary, second, subset)
        summary = results[3]
        assert summary.rater_a_n_categories == 3  # {2,3,4}
        assert summary.rater_b_n_categories == 2  # {3,4}

    def test_zero_variance_when_rater_uses_one_category(self) -> None:
        primary = _primary_long([("P1", "D2", 1), ("P2", "D2", 1), ("P3", "D2", 1)])
        second = _second_long([("P1", "D2", 1), ("P2", "D2", 1), ("P3", "D2", 1)])
        results = run_subset_reliability_analysis(primary, second, {"P1", "P2", "P3"})
        summary = results[2]
        assert summary.rater_a_variance == pytest.approx(0.0)
        assert summary.rater_a_n_categories == 1


class TestLoaders:
    """Loaders operate on the actual wide/long shapes the real files
    use -- exercised here against small in-memory equivalents rather
    than real Excel files, to keep the test fast and dependency-free."""

    def test_second_rater_loader_drops_blank_cells(self, tmp_path) -> None:
        wide = pd.DataFrame(
            {
                "Profile_ID": ["LP0001", "LP0002"],
                "D1": [3, None],
                "D2": [None, 1],
                "D3": [2, 4],
                "D4": [1, 1],
                "D5": [0, 2],
                "D6": [None, None],
            }
        )
        path = tmp_path / "second_rater.xlsx"
        wide.to_excel(path, sheet_name="Independent_Coding", index=False)

        long = load_second_rater_scores_long(path)
        # LP0001/D1 present, LP0002/D1 blank -> dropped.
        assert not (
            (long["Profile_ID"] == "LP0002") & (long["Dimension"] == "D1")
        ).any()
        assert ((long["Profile_ID"] == "LP0001") & (long["Dimension"] == "D1")).any()
        # Both D6 cells blank -> D6 entirely absent from the long frame.
        assert "D6" not in set(long["Dimension"])

    def test_primary_loader_drops_unavailable_rows(self, tmp_path) -> None:
        de = pd.DataFrame(
            {
                "Profile_ID": ["LP0001", "LP0001", "LP0002"],
                "Dimension": ["D1", "D6", "D1"],
                "Final_Score": [3, 0, 2],
                "Missing_Status": ["present", "unavailable", "present"],
            }
        )
        path = tmp_path / "annotation.xlsx"
        with pd.ExcelWriter(path) as writer:
            de.to_excel(writer, sheet_name="Dimension_Evidence", index=False)

        long = load_primary_scores_long(path, {"LP0001", "LP0002"})
        assert len(long) == 2
        assert not (
            (long["Profile_ID"] == "LP0001") & (long["Dimension"] == "D6")
        ).any()


class TestHumanRaterGuard:
    def test_non_human_rater_id_rejected_even_through_this_module(self) -> None:
        from alcsm.analysis.rq3_validation import inter_rater_reliability
        from alcsm.constants import DIMENSIONS

        ratings = {DIMENSIONS[0].number: {"P1": {"AI_FIRST_PASS": 3.0, "RATER_B": 3.0}}}
        with pytest.raises(NotAHumanRaterError):
            inter_rater_reliability(
                ratings,
                analysis_stage="main_double_coded",
                corpus="profile",
                rulebook_version="v1.1",
                source_description="test",
            )


class TestInsufficientData:
    def test_too_few_units_dimension_is_simply_absent(self) -> None:
        primary = _primary_long([("P1", "D1", 3)])
        second = _second_long([("P1", "D1", 3)])
        results = run_subset_reliability_analysis(primary, second, {"P1"})
        assert 1 not in results
