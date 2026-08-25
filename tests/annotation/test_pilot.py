"""Pilot / double-coding subset selection.

Verifies the mechanism only -- these tests never assert a specific
real profile is "the" pilot (this task's explicit "DO NOT choose the
final pilot sample automatically" rule); every candidate pool here is
constructed fixture IDs.
"""

from __future__ import annotations

import pytest

from alcsm.annotation.pilot import PilotSelectionError, select_pilot_subset

_CANDIDATES = [f"PRF-{i:05d}" for i in range(1, 21)]  # 20 constructed ids


def test_full_selects_every_candidate() -> None:
    selection = select_pilot_subset(_CANDIDATES, method="full")
    assert set(selection.selected_profile_ids) == set(_CANDIDATES)
    assert selection.actual_fraction == 1.0
    assert selection.seed is None


def test_random_subset_respects_minimum_fraction() -> None:
    with pytest.raises(PilotSelectionError, match="below the frozen minimum"):
        select_pilot_subset(_CANDIDATES, method="random_subset", seed=1, fraction=0.10)


def test_random_subset_at_minimum_fraction_accepted() -> None:
    selection = select_pilot_subset(
        _CANDIDATES, method="random_subset", seed=1, fraction=0.15
    )
    assert len(selection.selected_profile_ids) >= round(len(_CANDIDATES) * 0.15)


def test_random_subset_requires_seed() -> None:
    with pytest.raises(PilotSelectionError, match="seed is required"):
        select_pilot_subset(_CANDIDATES, method="random_subset", fraction=0.2)


def test_random_subset_is_reproducible_given_same_seed() -> None:
    a = select_pilot_subset(_CANDIDATES, method="random_subset", seed=42, fraction=0.25)
    b = select_pilot_subset(_CANDIDATES, method="random_subset", seed=42, fraction=0.25)
    assert a.selected_profile_ids == b.selected_profile_ids


def test_random_subset_differs_across_seeds_generally() -> None:
    a = select_pilot_subset(_CANDIDATES, method="random_subset", seed=1, fraction=0.5)
    b = select_pilot_subset(_CANDIDATES, method="random_subset", seed=2, fraction=0.5)
    assert a.selected_profile_ids != b.selected_profile_ids


def test_unknown_method_rejected() -> None:
    with pytest.raises(PilotSelectionError, match="unknown method"):
        select_pilot_subset(_CANDIDATES, method="whatever_i_feel_like")


def test_empty_candidate_pool_rejected() -> None:
    with pytest.raises(PilotSelectionError, match="must not be empty"):
        select_pilot_subset([], method="full")


def test_selection_never_invents_ids_outside_the_candidate_pool() -> None:
    selection = select_pilot_subset(
        _CANDIDATES, method="random_subset", seed=7, fraction=0.3
    )
    assert set(selection.selected_profile_ids) <= set(_CANDIDATES)


def test_this_module_never_hardcodes_a_real_pilot_selection() -> None:
    """Structural guard: no function in pilot.py should read any real
    data source (e.g. the processed LinkedIn workbook) -- every
    function takes candidate_profile_ids as an argument."""
    import inspect

    from alcsm.annotation import pilot

    source = inspect.getsource(pilot)
    assert "ALCSM_LinkedIn_Processed" not in source
    assert "ALCSM_Final_Human_Annotation" not in source
    assert ".xlsx" not in source
