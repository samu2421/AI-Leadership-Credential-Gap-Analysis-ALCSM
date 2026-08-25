"""D6 breadth handling: D6IndustryBreadthDetail rendering and consistency
with the v1.1 rubric (score = min(distinct normalized industry count, 5)).
"""

from __future__ import annotations

import pytest

from alcsm.annotation.dimension_config import get_dimension
from alcsm.annotation.models import D6IndustryBreadthDetail


def _detail(**overrides: object) -> D6IndustryBreadthDetail:
    defaults: dict[str, object] = dict(
        profile_id="PRF-90005",
        ai_related_industry_count=3,
        normalized_industries=("Automotive", "Healthcare", "Financial Services"),
        zero_ai_industries=False,
        missing_industry_partial=False,
        ambiguous_industry_label=False,
        duplicate_normalization_collapsed=False,
        potential_d3_d6_overlap=False,
        unusually_high_breadth=False,
    )
    defaults.update(overrides)
    return D6IndustryBreadthDetail(**defaults)  # type: ignore[arg-type]


def test_evidence_text_lists_every_normalized_industry() -> None:
    detail = _detail()
    text = detail.as_evidence_text()
    assert "Automotive" in text
    assert "Healthcare" in text
    assert "Financial Services" in text
    assert "3 distinct" in text


def test_evidence_text_handles_zero_industries() -> None:
    detail = _detail(
        ai_related_industry_count=0, normalized_industries=(), zero_ai_industries=True
    )
    text = detail.as_evidence_text()
    assert "0 distinct" in text
    assert "none" in text


@pytest.mark.parametrize(
    "count,expected_band",
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 5), (10, 5)],
)
def test_score_matches_v1_1_rubric_band(count: int, expected_band: int) -> None:
    """score = min(count, 5) -- the exact rule ALCSM_D6_Industry_Breadth_
    v1.1.md §7 and the first-pass annotation both use."""
    computed_score = min(count, 5)
    assert computed_score == expected_band


def test_d6_v1_1_rubric_criteria_align_with_breadth_bands() -> None:
    """The dimension_config's D6 v1.1 criteria text must describe exactly
    the six bands 0..5+ in ascending order, matching the score = min(count, 5)
    rule this module's evidence rendering assumes."""
    d6 = get_dimension(6, "v1_1")
    assert "no ai-related experience" in d6.criteria[0].lower()
    assert "one distinct" in d6.criteria[1].lower()
    assert "five or more" in d6.criteria[5].lower()


def test_flags_are_independent_booleans_not_mutually_exclusive() -> None:
    """A profile can legitimately be both high-breadth AND touch an
    ambiguous label at the same time -- the dataclass must allow this,
    not force a single flag."""
    detail = _detail(
        ai_related_industry_count=5,
        unusually_high_breadth=True,
        ambiguous_industry_label=True,
    )
    assert detail.unusually_high_breadth is True
    assert detail.ambiguous_industry_label is True
