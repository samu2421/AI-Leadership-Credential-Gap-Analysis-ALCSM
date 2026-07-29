"""Tests for alcsm.constants — assertions taken from the frozen spec
(PROJECT_CONTEXT.md §6-§9), not from the implementation
(CLAUDE_CODE_RULES.md rule 6).
"""

from __future__ import annotations

from alcsm.constants import (
    DIMENSIONS,
    EXTERNAL_VERIFICATION_DIMENSION,
    MISSING_STATUSES,
    PRECEDENT_IDS,
    SCORE_MAX,
    SCORE_MIN,
)


def test_exactly_six_dimensions_in_fixed_order() -> None:
    codes = tuple(d.code for d in DIMENSIONS)
    assert codes == (
        "d1_education",
        "d2_certifications",
        "d3_experience",
        "d4_contributions",
        "d5_leadership",
        "d6_engagement",
    )


def test_dimension_numbers_are_1_to_6_in_order() -> None:
    assert tuple(d.number for d in DIMENSIONS) == (1, 2, 3, 4, 5, 6)


def test_exactly_four_missing_statuses() -> None:
    assert MISSING_STATUSES == (
        "present",
        "absent_stated",
        "unavailable",
        "not_applicable",
    )


def test_score_range_is_0_to_5() -> None:
    assert (SCORE_MIN, SCORE_MAX) == (0, 5)


def test_external_verification_is_d4_only() -> None:
    assert EXTERNAL_VERIFICATION_DIMENSION == "d4_contributions"


def test_fifteen_precedents_p01_to_p15() -> None:
    assert PRECEDENT_IDS == tuple(f"P-{i:02d}" for i in range(1, 16))
    assert len(PRECEDENT_IDS) == 15
