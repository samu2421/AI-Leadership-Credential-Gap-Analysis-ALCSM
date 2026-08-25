"""Score validation: range, evidence requirements, missing-status handling.

Pure-logic tests, no database required — every rule mirrors a CHECK
constraint (see validation.py's docstrings for exactly which one), so
these tests exercise the same logic the DB will enforce a second time.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from alcsm.annotation.models import AnnotationScore
from alcsm.annotation.validation import validate_annotation_score

_NOW = datetime.now()


def _base(**overrides: object) -> AnnotationScore:
    defaults: dict[str, object] = dict(
        profile_id="PRF-00001",
        dimension_number=1,
        rater_id="RATER_A",
        score=3,
        missing_status="present",
        rulebook_version="1.0",
        coding_ts=_NOW,
        evidence_text="fixture evidence",
    )
    defaults.update(overrides)
    return AnnotationScore(**defaults)  # type: ignore[arg-type]


class TestScoreRange:
    @pytest.mark.parametrize("score", [0, 1, 2, 3, 4, 5])
    def test_valid_scores_pass(self, score: int) -> None:
        assert validate_annotation_score(_base(score=score)) == []

    @pytest.mark.parametrize("score", [-1, 6, 10])
    def test_out_of_range_scores_rejected(self, score: int) -> None:
        problems = validate_annotation_score(_base(score=score))
        assert any("between 0 and 5" in p for p in problems)

    @pytest.mark.parametrize("dimension_number", [0, 7, -1])
    def test_out_of_range_dimension_rejected(self, dimension_number: int) -> None:
        problems = validate_annotation_score(_base(dimension_number=dimension_number))
        assert any("dimension_number" in p for p in problems)


class TestEvidenceRequirements:
    def test_present_without_evidence_rejected(self) -> None:
        problems = validate_annotation_score(
            _base(missing_status="present", evidence_text=None)
        )
        assert any("requires evidence_text" in p for p in problems)

    def test_present_with_evidence_accepted(self) -> None:
        assert validate_annotation_score(_base(missing_status="present")) == []

    def test_absent_stated_without_evidence_rejected(self) -> None:
        problems = validate_annotation_score(
            _base(missing_status="absent_stated", score=0, evidence_text=None)
        )
        assert any("absent_stated" in p for p in problems)

    def test_absent_stated_with_evidence_accepted(self) -> None:
        assert (
            validate_annotation_score(
                _base(
                    missing_status="absent_stated",
                    score=0,
                    evidence_text="explicitly states no formal AI education",
                )
            )
            == []
        )


class TestMissingStatusHandling:
    def test_unavailable_requires_score_zero(self) -> None:
        problems = validate_annotation_score(
            _base(missing_status="unavailable", score=2, evidence_text=None)
        )
        assert any("requires score=0" in p for p in problems)

    def test_unavailable_must_not_carry_evidence(self) -> None:
        problems = validate_annotation_score(
            _base(missing_status="unavailable", score=0, evidence_text="some text")
        )
        assert any("must not carry evidence_text" in p for p in problems)

    def test_unavailable_score_zero_no_evidence_accepted(self) -> None:
        assert (
            validate_annotation_score(
                _base(missing_status="unavailable", score=0, evidence_text=None)
            )
            == []
        )

    def test_not_applicable_rejected_for_a_profile_score(self) -> None:
        problems = validate_annotation_score(
            _base(missing_status="not_applicable", score=0, evidence_text=None)
        )
        assert any("never valid for a profile score" in p for p in problems)

    def test_unknown_missing_status_rejected(self) -> None:
        problems = validate_annotation_score(_base(missing_status="bogus"))
        assert any("not in controlled vocabulary" in p for p in problems)


class TestD4OnlyVerification:
    def test_verification_on_d4_with_full_metadata_accepted(self) -> None:
        record = _base(
            dimension_number=4,
            verification_used=True,
            verification_source="https://github.com/example/repo",
            verification_ts=_NOW,
            verification_outcome="confirmed",
        )
        assert validate_annotation_score(record) == []

    @pytest.mark.parametrize("dimension_number", [1, 2, 3, 5, 6])
    def test_verification_on_non_d4_rejected(self, dimension_number: int) -> None:
        record = _base(
            dimension_number=dimension_number,
            verification_used=True,
            verification_source="https://example.com",
            verification_ts=_NOW,
            verification_outcome="confirmed",
        )
        problems = validate_annotation_score(record)
        assert any("only permitted for dimension 4" in p for p in problems)

    def test_verification_used_without_metadata_rejected(self) -> None:
        record = _base(dimension_number=4, verification_used=True)
        problems = validate_annotation_score(record)
        assert any("requires verification_source" in p for p in problems)

    def test_verification_metadata_without_flag_rejected(self) -> None:
        record = _base(
            dimension_number=4,
            verification_used=False,
            verification_source="https://example.com",
            verification_ts=_NOW,
            verification_outcome="confirmed",
        )
        problems = validate_annotation_score(record)
        assert any(
            "requires verification_source" in p or "unset" in p for p in problems
        )

    def test_invalid_verification_outcome_rejected(self) -> None:
        record = _base(
            dimension_number=4,
            verification_used=True,
            verification_source="https://example.com",
            verification_ts=_NOW,
            verification_outcome="probably-fine",
        )
        problems = validate_annotation_score(record)
        assert any("verification_outcome must be one of" in p for p in problems)


class TestAmbiguityMetadata:
    def test_ambiguity_flag_requires_both_candidates(self) -> None:
        record = _base(ambiguity_flag=True)
        problems = validate_annotation_score(record)
        assert any("requires both ambiguity_candidate" in p for p in problems)

    def test_ambiguity_candidates_without_flag_rejected(self) -> None:
        record = _base(ambiguity_candidate_low=2, ambiguity_candidate_high=3)
        problems = validate_annotation_score(record)
        assert any(
            "requires ambiguity_candidate_low/high both unset" in p for p in problems
        )

    def test_score_must_lie_within_ambiguity_range(self) -> None:
        record = _base(
            score=1,
            ambiguity_flag=True,
            ambiguity_candidate_low=2,
            ambiguity_candidate_high=3,
        )
        problems = validate_annotation_score(record)
        assert any("must lie within" in p for p in problems)

    def test_valid_ambiguity_range_accepted(self) -> None:
        record = _base(
            score=2,
            ambiguity_flag=True,
            ambiguity_candidate_low=2,
            ambiguity_candidate_high=3,
        )
        assert validate_annotation_score(record) == []


class TestContradictionMetadata:
    def test_contradiction_flag_requires_text(self) -> None:
        problems = validate_annotation_score(_base(contradiction_flag=True))
        assert any("requires contradiction_text" in p for p in problems)

    def test_contradiction_text_requires_flag(self) -> None:
        problems = validate_annotation_score(
            _base(contradiction_text="title vs substance")
        )
        assert any("requires contradiction_text unset" in p for p in problems)

    def test_valid_contradiction_accepted(self) -> None:
        record = _base(
            contradiction_flag=True, contradiction_text="title vs substance (P-03)"
        )
        assert validate_annotation_score(record) == []


class TestAdjudicatorAlignment:
    def test_adjudication_true_requires_adjudicator_id(self) -> None:
        problems = validate_annotation_score(
            _base(rater_id="RATER_A", is_adjudication=True)
        )
        assert any("requires rater_id='ADJUDICATOR'" in p for p in problems)

    def test_adjudicator_id_requires_adjudication_true(self) -> None:
        problems = validate_annotation_score(
            _base(rater_id="ADJUDICATOR", is_adjudication=False)
        )
        assert any("requires is_adjudication=True" in p for p in problems)

    def test_valid_adjudication_accepted(self) -> None:
        record = _base(rater_id="ADJUDICATOR", is_adjudication=True)
        assert validate_annotation_score(record) == []


def test_multiple_problems_all_reported_together() -> None:
    record = _base(score=9, missing_status="bogus", dimension_number=0)
    problems = validate_annotation_score(record)
    assert len(problems) >= 3
