"""RQ4 correlation: closed criterion-variable list, ordinal correlation,
freeze gate, isolation from ALCSM scoring."""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.config import DataNotFrozenError
from alcsm.analysis.rq4 import CRITERION_VARIABLES, correlate_with_impact_indicators


def test_criterion_variables_is_the_closed_frozen_list() -> None:
    assert set(CRITERION_VARIABLES) == {
        "rq4_network_reach",
        "rq4_content_engagement",
        "rq4_recognition_count",
        "rq4_seniority_progression_rate",
    }


class TestCorrelateWithImpactIndicators:
    def test_gated_on_provisional(
        self,
        synthetic_profile_scores_provisional: pd.DataFrame,
        synthetic_impact_indicators: pd.DataFrame,
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            correlate_with_impact_indicators(
                synthetic_profile_scores_provisional,
                synthetic_impact_indicators,
                "provisional_first_pass",
                "fixture",
            )

    def test_table_covers_all_dimensions_and_criteria(
        self,
        synthetic_profile_scores_final: pd.DataFrame,
        synthetic_impact_indicators: pd.DataFrame,
    ) -> None:
        result = correlate_with_impact_indicators(
            synthetic_profile_scores_final,
            synthetic_impact_indicators,
            "final_frozen",
            "fixture",
        )
        assert list(result.table.index) == [f"D{n}" for n in range(1, 7)]
        assert set(result.table.columns) == set(CRITERION_VARIABLES)

    def test_correlation_bounded(
        self,
        synthetic_profile_scores_final: pd.DataFrame,
        synthetic_impact_indicators: pd.DataFrame,
    ) -> None:
        result = correlate_with_impact_indicators(
            synthetic_profile_scores_final,
            synthetic_impact_indicators,
            "final_frozen",
            "fixture",
        )
        values = result.table.to_numpy(dtype=float)
        valid = values[~pd.isna(values)]
        assert ((valid >= -1.0) & (valid <= 1.0)).all()

    def test_perfect_monotonic_relationship_gives_rho_one(self) -> None:
        scores = pd.DataFrame(
            {
                "Profile_ID": [f"PRF-{i:05d}" for i in range(6)],
                **{f"D{n}_Final": list(range(6)) for n in range(1, 7)},
            }
        )
        indicators = pd.DataFrame(
            {
                "profile_id": [f"PRF-{i:05d}" for i in range(6)],
                "rq4_network_reach": list(range(6)),
                "rq4_content_engagement": [0] * 6,
                "rq4_recognition_count": [0] * 6,
                "rq4_seniority_progression_rate": [0] * 6,
            }
        )
        result = correlate_with_impact_indicators(
            scores, indicators, "final_frozen", "fixture"
        )
        assert result.table.loc["D1", "rq4_network_reach"] == pytest.approx(1.0)

    def test_unmatched_profiles_excluded_via_inner_merge(
        self, synthetic_profile_scores_final: pd.DataFrame
    ) -> None:
        indicators = pd.DataFrame(
            {
                "profile_id": ["PRF-99999"],  # matches no fixture profile
                "rq4_network_reach": [1],
                "rq4_content_engagement": [1],
                "rq4_recognition_count": [1],
                "rq4_seniority_progression_rate": [1],
            }
        )
        result = correlate_with_impact_indicators(
            synthetic_profile_scores_final, indicators, "final_frozen", "fixture"
        )
        assert (result.n_table.to_numpy() == 0).all()


def test_no_causal_language_anywhere_in_module_docstrings_or_field_names() -> None:
    import inspect
    from dataclasses import fields

    from alcsm.analysis import rq4 as rq4_module

    forbidden = ("causes", "effect_of", "impact_of", "drives", "leads_to")
    for name in ("CriterionCorrelation", "RQ4CorrelationReport"):
        cls = getattr(rq4_module, name)
        for f in fields(cls):
            assert not any(term in f.name.lower() for term in forbidden)
    module_doc = inspect.getdoc(rq4_module) or ""
    assert "no function here computes or implies" in module_doc.lower()
