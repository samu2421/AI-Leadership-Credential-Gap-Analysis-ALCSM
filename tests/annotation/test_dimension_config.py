"""Versioned dimension configuration: D1-D6 display, D6 v1.0 vs v1.1."""

from __future__ import annotations

import pytest

from alcsm.annotation.dimension_config import (
    DEFAULT_VERSION,
    available_versions,
    get_dimension,
    get_dimension_config,
)
from alcsm.constants import DIMENSIONS


def test_default_version_is_v1_1() -> None:
    assert DEFAULT_VERSION == "v1_1"


def test_available_versions_includes_both() -> None:
    assert set(available_versions()) == {"v1_0", "v1_1"}


@pytest.mark.parametrize("version", ["v1_0", "v1_1"])
def test_config_has_all_six_dimensions_in_order(version: str) -> None:
    dims = get_dimension_config(version)
    assert [d.number for d in dims] == [1, 2, 3, 4, 5, 6]


@pytest.mark.parametrize("version", ["v1_0", "v1_1"])
def test_every_dimension_has_six_criteria(version: str) -> None:
    for dim in get_dimension_config(version):
        assert len(dim.criteria) == 6


@pytest.mark.parametrize("version", ["v1_0", "v1_1"])
def test_dimension_codes_match_frozen_constants(version: str) -> None:
    """The DB-aligned code never changes across versions -- only display
    text does (dimension_config.py's central design rule)."""
    frozen_codes = [d.code for d in DIMENSIONS]
    config_codes = [d.code for d in get_dimension_config(version)]
    assert config_codes == frozen_codes


def test_d1_through_d5_identical_across_versions() -> None:
    v1_0 = get_dimension_config("v1_0")
    v1_1 = get_dimension_config("v1_1")
    for i in range(5):  # D1-D5, zero-indexed
        assert v1_0[i] == v1_1[i]


def test_d6_differs_between_versions() -> None:
    d6_v1_0 = get_dimension(6, "v1_0")
    d6_v1_1 = get_dimension(6, "v1_1")
    assert d6_v1_0.label == "Professional Engagement & Continuous Development"
    assert d6_v1_1.label == "AI Industry/Application Breadth"
    assert d6_v1_0.criteria != d6_v1_1.criteria


def test_d6_v1_1_is_flagged_as_proposed() -> None:
    assert get_dimension(6, "v1_1").is_proposed is True


def test_d6_v1_0_is_not_flagged_as_proposed() -> None:
    assert get_dimension(6, "v1_0").is_proposed is False


def test_no_other_dimension_is_flagged_as_proposed() -> None:
    for version in ("v1_0", "v1_1"):
        for dim in get_dimension_config(version):
            if dim.number != 6:
                assert dim.is_proposed is False


def test_unknown_version_raises_with_available_versions_listed() -> None:
    with pytest.raises(KeyError, match="v9_9"):
        get_dimension_config("v9_9")


def test_unknown_dimension_number_raises() -> None:
    with pytest.raises(KeyError):
        get_dimension(7)
    with pytest.raises(KeyError):
        get_dimension(0)


def test_d6_v1_1_never_uses_competence_or_effectiveness_language() -> None:
    """The proposed D6's definition must preserve the signal-not-competence
    framing (this document's own explicit requirement, ALCSM_D6_
    Industry_Breadth_v1.1.md §3)."""
    definition = get_dimension(6, "v1_1").definition.lower()
    assert "competence" not in definition or "not a measure of competence" in definition
    assert "leadership effectiveness" not in definition or (
        "not a measure of" in definition
    )
