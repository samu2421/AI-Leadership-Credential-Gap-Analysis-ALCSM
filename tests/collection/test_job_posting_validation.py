"""Pure-logic tests for job-posting validation — no database required.

Assertions are written against the frozen rules in PROJECT_CONTEXT.md
(§9, §32, §45) and Task5_P3_JobPosting_Collection_Plan.md (§3-§6), not
against whatever the implementation currently does
(CLAUDE_CODE_RULES.md rule 6). All fixture data below is synthetic;
nothing here resembles a real posting.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from alcsm.collection.helper import (
    JobPostingRecord,
    JobPostingValidationError,
    detect_recruiter_identifiers,
    validate_job_posting_record,
)


def _valid_record(**overrides: object) -> JobPostingRecord:
    defaults: dict[str, object] = dict(
        posting_id="JOB-00001",
        sampling_batch_id="BATCH-101",
        posting_source="example_job_board",
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI to lead a 12-person applied-ML "
        "team. TensorFlow and Kubernetes experience preferred.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


def test_valid_record_has_no_problems() -> None:
    assert validate_job_posting_record(_valid_record()) == []


@pytest.mark.parametrize(
    "bad_id",
    ["", "JOB-1", "JOB-123456", "job-00001", "00001", "JOB-0000A"],
)
def test_posting_id_must_match_job_pattern(bad_id: str) -> None:
    errs = validate_job_posting_record(_valid_record(posting_id=bad_id))
    assert any("JOB-#####" in e for e in errs)


@pytest.mark.parametrize(
    "field_name",
    [
        "sampling_batch_id",
        "search_query",
        "inclusion_reason",
        "collection_ts",
        "posting_source",
    ],
)
def test_missing_provenance_field_is_reported(field_name: str) -> None:
    record = _valid_record(**{field_name: None})
    errs = validate_job_posting_record(record)
    assert any(f"missing provenance field: {field_name}" in e for e in errs)


def test_inclusion_reason_must_be_in_controlled_vocabulary() -> None:
    errs = validate_job_posting_record(
        _valid_record(inclusion_reason="i_just_liked_it")
    )
    assert any("controlled vocabulary" in e for e in errs)


@pytest.mark.parametrize(
    "valid_reason", ["title_match", "title_variant_match", "manual_review_included"]
)
def test_all_controlled_vocabulary_inclusion_reasons_are_accepted(
    valid_reason: str,
) -> None:
    errs = validate_job_posting_record(_valid_record(inclusion_reason=valid_reason))
    assert not any("controlled vocabulary" in e for e in errs)


@pytest.mark.parametrize("bad_lang", ["ENG", "e", "123", "eng"])
def test_posting_language_must_be_iso_639_1_or_und(bad_lang: str) -> None:
    errs = validate_job_posting_record(_valid_record(posting_language=bad_lang))
    assert any("ISO 639-1" in e for e in errs)


def test_posting_language_und_is_accepted() -> None:
    assert validate_job_posting_record(_valid_record(posting_language="und")) == []


@pytest.mark.parametrize("bad_geo", ["de", "DEU", "1", "D3"])
def test_posting_geography_must_be_iso_3166_1_alpha_2(bad_geo: str) -> None:
    errs = validate_job_posting_record(_valid_record(posting_geography=bad_geo))
    assert any("ISO 3166-1" in e for e in errs)


def test_posting_geography_none_is_accepted() -> None:
    assert validate_job_posting_record(_valid_record(posting_geography=None)) == []


@pytest.mark.parametrize("empty_text", ["", "   ", "\n\t"])
def test_raw_posting_text_must_be_non_empty(empty_text: str) -> None:
    errs = validate_job_posting_record(_valid_record(raw_posting_text=empty_text))
    assert any("raw_posting_text must be non-empty" in e for e in errs)


def test_multiple_problems_are_all_reported_together() -> None:
    record = _valid_record(
        posting_id="bad", inclusion_reason="nonsense", posting_language="ENG"
    )
    errs = validate_job_posting_record(record)
    assert len(errs) >= 3


class TestRecruiterPrivacyDetection:
    """CLAUDE_CODE_RULES.md rule 8; Task5_P3_JobPosting_Collection_Plan.md §6:
    the unit of analysis is the posting's requirements, never the
    poster. `detect_recruiter_identifiers` is deterministic and
    content-based — it never uses NLP/NER, so bare recruiter *names*
    in free text are explicitly not something it can catch (see the
    function's own docstring); only machine-detectable patterns are.
    """

    @pytest.mark.parametrize(
        "text",
        [
            "Contact jane.doe@example.com for more information.",
            "Apply by emailing recruiting.team@acme-corp.io",
        ],
    )
    def test_email_pattern_is_detected(self, text: str) -> None:
        findings = detect_recruiter_identifiers(text)
        assert any("email" in f for f in findings)

    @pytest.mark.parametrize(
        "text",
        [
            "Call our recruiter at +1 415-555-0173 to discuss.",
            "Reach us on 030-1234-5678 during business hours.",
        ],
    )
    def test_phone_pattern_is_detected(self, text: str) -> None:
        findings = detect_recruiter_identifiers(text)
        assert any("phone" in f for f in findings)

    def test_linkedin_profile_link_is_detected(self) -> None:
        text = "Reach out to our recruiter: linkedin.com/in/jane-doe-12345"
        findings = detect_recruiter_identifiers(text)
        assert any("LinkedIn" in f for f in findings)

    @pytest.mark.parametrize(
        "clean_text",
        [
            "Seeking a Head of AI with 10-15 years of experience.",
            "Salary range: $120,000 - $150,000 depending on experience.",
            "Team of 5-10 engineers reporting to the VP of Engineering.",
            "TensorFlow, PyTorch, and Kubernetes experience required.",
        ],
    )
    def test_ordinary_posting_text_has_no_false_positives(
        self, clean_text: str
    ) -> None:
        assert detect_recruiter_identifiers(clean_text) == []

    def test_raw_posting_text_with_recruiter_email_is_rejected(self) -> None:
        record = _valid_record(
            raw_posting_text="Great AI leadership role. Apply to jane@acme.com."
        )
        errs = validate_job_posting_record(record)
        assert any("recruiter-identifying content" in e for e in errs)

    def test_raw_requirements_text_is_also_scanned(self) -> None:
        record = _valid_record(
            raw_requirements_text="Must have 5+ years AI experience. "
            "Contact +1 415-555-0173."
        )
        errs = validate_job_posting_record(record)
        assert any(
            "raw_requirements_text" in e and "recruiter-identifying content" in e
            for e in errs
        )

    def test_clean_posting_has_no_recruiter_identifier_problems(self) -> None:
        assert validate_job_posting_record(_valid_record()) == []


class TestFromMapping:
    """The untrusted-input boundary: `JobPostingRecord.from_mapping`."""

    def _valid_mapping(self, **overrides: object) -> dict[str, object]:
        base: dict[str, object] = dict(
            posting_id="JOB-00002",
            sampling_batch_id="BATCH-101",
            posting_source="example_job_board",
            search_query='"VP of AI"',
            inclusion_reason="title_match",
            collection_ts=datetime.now(UTC),
            raw_posting_text="Seeking a VP of AI. ML platform experience required.",
        )
        base.update(overrides)
        return base

    @pytest.mark.parametrize(
        "forbidden_field",
        ["name", "email", "phone", "url"],
    )
    def test_general_forbidden_identifier_field_is_rejected(
        self, forbidden_field: str
    ) -> None:
        data = self._valid_mapping(**{forbidden_field: "some value"})
        with pytest.raises(JobPostingValidationError) as exc_info:
            JobPostingRecord.from_mapping(data)
        assert any(
            f"forbidden identifier field present: {forbidden_field!r}" in p
            for p in exc_info.value.problems
        )

    @pytest.mark.parametrize(
        "forbidden_field",
        [
            "recruiter_name",
            "recruiter_email",
            "recruiter_phone",
            "recruiter_profile_url",
            "contact_name",
            "contact_email",
            "contact_phone",
            "contact_profile_url",
        ],
    )
    def test_recruiter_forbidden_field_is_rejected(self, forbidden_field: str) -> None:
        data = self._valid_mapping(**{forbidden_field: "some value"})
        with pytest.raises(JobPostingValidationError) as exc_info:
            JobPostingRecord.from_mapping(data)
        assert any(
            f"forbidden identifier field present: {forbidden_field!r}" in p
            for p in exc_info.value.problems
        )

    def test_missing_required_field_is_rejected(self) -> None:
        data = self._valid_mapping()
        del data["posting_source"]
        with pytest.raises(JobPostingValidationError) as exc_info:
            JobPostingRecord.from_mapping(data)
        assert any("posting_source" in p for p in exc_info.value.problems)

    def test_well_formed_mapping_builds_a_record(self) -> None:
        record = JobPostingRecord.from_mapping(self._valid_mapping())
        assert record.posting_id == "JOB-00002"
        assert record.posting_source == "example_job_board"
        assert validate_job_posting_record(record) == []

    def test_missing_posting_id_defers_to_validate_job_posting_record(self) -> None:
        data = self._valid_mapping()
        del data["posting_id"]
        record = JobPostingRecord.from_mapping(data)
        assert record.posting_id == ""
        errs = validate_job_posting_record(record)
        assert any("JOB-#####" in e for e in errs)


def test_job_posting_validation_error_message_lists_all_problems() -> None:
    error = JobPostingValidationError(["problem one", "problem two"])
    assert "problem one" in str(error)
    assert "problem two" in str(error)
    assert error.problems == ["problem one", "problem two"]
