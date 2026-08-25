"""Sanity checks on the constructed synthetic fixtures themselves.

If these fail, every other test that depends on fixtures.py is
suspect -- catch a bad fixture here, not as a confusing failure three
layers away.
"""

from __future__ import annotations

import re

from alcsm.annotation.fixtures import (
    FIXTURE_EVIDENCE,
    FIXTURE_SCORES,
    SYNTHETIC_PROFILES,
    all_fixture_profile_ids,
)
from alcsm.constants import MISSING_STATUSES, SCORE_MAX, SCORE_MIN

_PRF_PATTERN = re.compile(r"^PRF-\d{5}$")


def test_every_fixture_profile_id_matches_schema_format() -> None:
    for profile_id in all_fixture_profile_ids():
        assert _PRF_PATTERN.fullmatch(profile_id), profile_id


def test_fixture_ids_use_a_reserved_high_block() -> None:
    """PRF-9#### is used precisely so a fixture id is visually
    distinguishable from anything a real ~500-profile collection would
    plausibly produce."""
    for profile_id in all_fixture_profile_ids():
        assert profile_id.startswith("PRF-9")


def test_every_profile_has_scores_for_all_six_dimensions() -> None:
    for profile_id in all_fixture_profile_ids():
        assert set(FIXTURE_SCORES[profile_id].keys()) == {1, 2, 3, 4, 5, 6}


def test_every_fixture_score_is_in_range() -> None:
    for dims in FIXTURE_SCORES.values():
        for score, _missing_status in dims.values():
            assert SCORE_MIN <= score <= SCORE_MAX


def test_every_fixture_missing_status_is_valid() -> None:
    for dims in FIXTURE_SCORES.values():
        for _score, missing_status in dims.values():
            assert missing_status in MISSING_STATUSES


def test_unavailable_fixture_scores_are_zero() -> None:
    """Mirrors the schema's ck_unavailable_scores_zero constraint --
    a fixture that violated this would make every test built on it
    misleading."""
    for dims in FIXTURE_SCORES.values():
        for score, missing_status in dims.values():
            if missing_status == "unavailable":
                assert score == 0


def test_profile_e_reaches_high_d6_breadth() -> None:
    """None of A-D reach the D6=4/5 bands; E exists specifically to
    exercise them."""
    assert FIXTURE_SCORES["PRF-90005"][6][0] == 5


def test_no_profile_id_collides_with_the_reserved_adjudicator_rater_id() -> None:
    assert "ADJUDICATOR" not in all_fixture_profile_ids()


def test_no_fixture_text_contains_a_url_or_email() -> None:
    url_email = re.compile(r"https?://|linkedin\.com/in/|[\w.+-]+@[\w-]+\.\w+")
    for profile in SYNTHETIC_PROFILES:
        for section in profile.sections.values():
            if section.text:
                assert not url_email.search(section.text), section.text
    for evidence in FIXTURE_EVIDENCE.values():
        assert not url_email.search(evidence)
