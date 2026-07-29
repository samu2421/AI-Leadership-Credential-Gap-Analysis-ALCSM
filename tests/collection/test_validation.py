"""Pure-logic tests for collection validation — no database required.

Assertions are written against the frozen rules in PROJECT_CONTEXT.md
(§9, §32, §45), not against whatever the implementation currently
does (CLAUDE_CODE_RULES.md rule 6). All fixture data below is
synthetic; nothing here resembles a real person or profile.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from alcsm.collection.helper import (
    ProfileRecord,
    ProfileSection,
    ProfileValidationError,
    validate_profile_record,
)


def _valid_record(**overrides: object) -> ProfileRecord:
    defaults: dict[str, object] = dict(
        profile_id="PRF-00001",
        sampling_batch_id="BATCH-001",
        search_query='"Chief AI Officer"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Chief AI Officer"),
        },
    )
    defaults.update(overrides)
    return ProfileRecord(**defaults)  # type: ignore[arg-type]


def test_valid_record_has_no_problems() -> None:
    assert validate_profile_record(_valid_record()) == []


@pytest.mark.parametrize(
    "bad_id",
    ["", "PRF-1", "PRF-123456", "prf-00001", "00001", "PRF-0000A"],
)
def test_profile_id_must_match_prf_pattern(bad_id: str) -> None:
    errs = validate_profile_record(_valid_record(profile_id=bad_id))
    assert any("PRF-#####" in e for e in errs)


@pytest.mark.parametrize(
    "field_name",
    ["sampling_batch_id", "search_query", "inclusion_reason", "collection_ts"],
)
def test_missing_provenance_field_is_reported(field_name: str) -> None:
    record = _valid_record(**{field_name: None})
    errs = validate_profile_record(record)
    assert any(f"missing provenance field: {field_name}" in e for e in errs)


def test_inclusion_reason_must_be_in_controlled_vocabulary() -> None:
    errs = validate_profile_record(_valid_record(inclusion_reason="i_just_liked_it"))
    assert any("controlled vocabulary" in e for e in errs)


@pytest.mark.parametrize(
    "valid_reason", ["title_match", "title_variant_match", "manual_review_included"]
)
def test_all_controlled_vocabulary_inclusion_reasons_are_accepted(
    valid_reason: str,
) -> None:
    errs = validate_profile_record(_valid_record(inclusion_reason=valid_reason))
    assert not any("controlled vocabulary" in e for e in errs)


@pytest.mark.parametrize("bad_lang", ["ENG", "e", "123", "eng"])
def test_profile_language_must_be_iso_639_1_or_und(bad_lang: str) -> None:
    errs = validate_profile_record(_valid_record(profile_language=bad_lang))
    assert any("ISO 639-1" in e for e in errs)


def test_profile_language_und_is_accepted() -> None:
    assert validate_profile_record(_valid_record(profile_language="und")) == []


def test_profile_language_valid_iso_code_is_accepted() -> None:
    assert validate_profile_record(_valid_record(profile_language="en")) == []


@pytest.mark.parametrize("bad_geo", ["de", "DEU", "1", "D3"])
def test_profile_geography_must_be_iso_3166_1_alpha_2(bad_geo: str) -> None:
    errs = validate_profile_record(_valid_record(profile_geography=bad_geo))
    assert any("ISO 3166-1" in e for e in errs)


def test_profile_geography_none_is_accepted() -> None:
    assert validate_profile_record(_valid_record(profile_geography=None)) == []


def test_unknown_section_name_is_rejected() -> None:
    record = _valid_record(
        sections={"skills": ProfileSection(available=True, text="Python")}
    )
    errs = validate_profile_record(record)
    assert any("unknown section name" in e for e in errs)


def test_unavailable_section_with_text_is_incoherent() -> None:
    """PROJECT_CONTEXT.md §9: a not-retrieved section cannot carry text —
    'unavailable' and 'absent_stated' must never be conflated."""
    record = _valid_record(
        sections={"about": ProfileSection(available=False, text="some leaked text")}
    )
    errs = validate_profile_record(record)
    assert any("available=False but text present" in e for e in errs)


def test_unavailable_section_with_no_text_is_coherent() -> None:
    record = _valid_record(
        sections={"about": ProfileSection(available=False, text=None)}
    )
    assert validate_profile_record(record) == []


def test_available_section_with_no_text_is_permitted() -> None:
    """An available section with no substantive text is not an error in
    itself — only the availability/text *coherence* rule is enforced."""
    record = _valid_record(
        sections={"about": ProfileSection(available=True, text=None)}
    )
    assert validate_profile_record(record) == []


def test_activity_captured_without_ethics_flag_is_rejected() -> None:
    record = _valid_record(
        sections={"activity": ProfileSection(available=True, text="Posted about AI")},
        activity_data_collected=False,
    )
    errs = validate_profile_record(record)
    assert any("activity_data_collected is False" in e for e in errs)


def test_activity_captured_with_ethics_flag_is_accepted() -> None:
    record = _valid_record(
        sections={"activity": ProfileSection(available=True, text="Posted about AI")},
        activity_data_collected=True,
    )
    assert validate_profile_record(record) == []


def test_activity_unavailable_never_needs_the_ethics_flag() -> None:
    record = _valid_record(
        sections={"activity": ProfileSection(available=False, text=None)},
        activity_data_collected=False,
    )
    assert validate_profile_record(record) == []


def test_multiple_problems_are_all_reported_together() -> None:
    """A human data-entry mistake should surface every problem at once,
    not one constraint at a time (PROJECT_CONTEXT.md §32)."""
    record = _valid_record(
        profile_id="bad", inclusion_reason="nonsense", profile_language="ENG"
    )
    errs = validate_profile_record(record)
    assert len(errs) >= 3


class TestFromMapping:
    """The untrusted-input boundary: `ProfileRecord.from_mapping`."""

    def _valid_mapping(self, **overrides: object) -> dict[str, object]:
        base: dict[str, object] = dict(
            profile_id="PRF-00002",
            sampling_batch_id="BATCH-001",
            search_query='"Head of AI"',
            inclusion_reason="title_match",
            collection_ts=datetime.now(UTC),
            sections={"headline": {"available": True, "text": "Head of AI"}},
        )
        base.update(overrides)
        return base

    @pytest.mark.parametrize(
        "forbidden_field",
        ["name", "full_name", "profile_url", "url", "photo", "email", "phone"],
    )
    def test_forbidden_identifier_field_is_rejected(self, forbidden_field: str) -> None:
        data = self._valid_mapping(**{forbidden_field: "some value"})
        with pytest.raises(ProfileValidationError) as exc_info:
            ProfileRecord.from_mapping(data)
        assert any(
            f"forbidden identifier field present: {forbidden_field!r}" in p
            for p in exc_info.value.problems
        )

    def test_missing_required_field_is_rejected(self) -> None:
        data = self._valid_mapping()
        del data["search_query"]
        with pytest.raises(ProfileValidationError) as exc_info:
            ProfileRecord.from_mapping(data)
        assert any("search_query" in p for p in exc_info.value.problems)

    def test_well_formed_mapping_builds_a_record(self) -> None:
        record = ProfileRecord.from_mapping(self._valid_mapping())
        assert record.profile_id == "PRF-00002"
        assert record.sections["headline"] == ProfileSection(
            available=True, text="Head of AI"
        )
        assert validate_profile_record(record) == []

    def test_missing_profile_id_defers_to_validate_profile_record(self) -> None:
        """from_mapping does not itself require profile_id (it is not a
        provenance field); validate_profile_record is the single gate
        that catches its absence or malformed shape."""
        data = self._valid_mapping()
        del data["profile_id"]
        record = ProfileRecord.from_mapping(data)
        assert record.profile_id == ""
        errs = validate_profile_record(record)
        assert any("PRF-#####" in e for e in errs)

    def test_forbidden_and_missing_problems_are_combined(self) -> None:
        data = self._valid_mapping(name="Someone", email="someone@example.com")
        del data["inclusion_reason"]
        with pytest.raises(ProfileValidationError) as exc_info:
            ProfileRecord.from_mapping(data)
        problems = exc_info.value.problems
        assert len(problems) == 3


def test_profile_validation_error_message_lists_all_problems() -> None:
    error = ProfileValidationError(["problem one", "problem two"])
    assert "problem one" in str(error)
    assert "problem two" in str(error)
    assert error.problems == ["problem one", "problem two"]
