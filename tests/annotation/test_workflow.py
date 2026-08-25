"""Reviewer workflow: accept/change/defer, six-dimensions-together gating,
save+validate, duplicate/validation audit trail, and the blinding-aware
display gate.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import psycopg2
import pytest

from alcsm.annotation.audit import AuditAction, AuditLogger
from alcsm.annotation.models import AnnotationScore, ReviewDecision
from alcsm.annotation.store import insert_annotation_score
from alcsm.annotation.validation import AnnotationValidationError
from alcsm.annotation.workflow import (
    ReviewSession,
    check_blinding_before_display,
    submit_and_save,
)

_NOW = datetime.now()


@pytest.fixture()
def audit_logger(tmp_path: Path) -> AuditLogger:
    return AuditLogger(tmp_path / "audit.jsonl")


def _score(
    profile_id: str, dimension_number: int, rater_id: str, **overrides: object
) -> AnnotationScore:
    defaults: dict[str, object] = dict(
        profile_id=profile_id,
        dimension_number=dimension_number,
        rater_id=rater_id,
        score=3,
        missing_status="present",
        rulebook_version="1.0",
        coding_ts=_NOW,
        evidence_text="fixture evidence",
    )
    defaults.update(overrides)
    return AnnotationScore(**defaults)  # type: ignore[arg-type]


class TestSixDimensionsTogether:
    def test_profile_incomplete_until_all_six_have_a_decision(
        self, audit_logger: AuditLogger
    ) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        assert session.is_profile_complete() is False
        for d in range(1, 6):
            session.record_accept(d, _score("PRF-90001", d, "RATER_A"))
        assert session.is_profile_complete() is False
        session.record_accept(6, _score("PRF-90001", 6, "RATER_A"))
        assert session.is_profile_complete() is True

    def test_defer_counts_toward_completeness(self, audit_logger: AuditLogger) -> None:
        """A profile with all six dimensions DEFERRED is 'complete' in the
        sense of having been visited -- DEFER is a recorded decision, not
        an absence of one."""
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        for d in range(1, 7):
            session.record_defer(d)
        assert session.is_profile_complete() is True


class TestAcceptChangeDefer:
    def test_accept_requires_an_explicit_submission(
        self, audit_logger: AuditLogger
    ) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        session.record_accept(1, _score("PRF-90001", 1, "RATER_A", score=4))
        state = session.dimensions[1]
        assert state.decision == ReviewDecision.ACCEPT
        assert state.submitted_score is not None
        assert state.submitted_score.score == 4

    def test_change_produces_a_review_outcome_audit_row(
        self, audit_logger: AuditLogger
    ) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        session.record_change(
            dimension_number=5,
            score=_score("PRF-90001", 5, "RATER_A", score=2),
            first_pass_score=4,
            change_reason="Title alone does not substantiate strategic scope (P-03)",
            governing_rule="ALCSM_v1.1_Scoring_Framework.md §1, D5 criteria",
            precedent="P-03",
        )
        outcome = session.dimensions[5].change_outcome
        assert outcome is not None
        assert outcome.first_pass_score == 4
        assert outcome.final_score == 2
        assert outcome.precedent == "P-03"

    def test_accept_never_produces_a_review_outcome(
        self, audit_logger: AuditLogger
    ) -> None:
        """Human_Annotation_Review_Protocol_v1.1.md §9: Review_Changes is
        populated only on CHANGE, never on ACCEPT."""
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        session.record_accept(1, _score("PRF-90001", 1, "RATER_A"))
        assert session.dimensions[1].change_outcome is None

    def test_defer_records_no_score(self, audit_logger: AuditLogger) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        session.record_defer(3)
        state = session.dimensions[3]
        assert state.decision == ReviewDecision.DEFER
        assert state.submitted_score is None

    def test_submitting_with_mismatched_rater_id_raises(
        self, audit_logger: AuditLogger
    ) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        with pytest.raises(ValueError, match="does not match"):
            session.record_accept(1, _score("PRF-90001", 1, "RATER_B"))

    def test_every_decision_is_audit_logged(self, audit_logger: AuditLogger) -> None:
        session = ReviewSession("PRF-90001", "RATER_A", "1.0", audit_logger)
        session.record_accept(1, _score("PRF-90001", 1, "RATER_A"))
        session.record_defer(2)
        entries = audit_logger.read_all()
        actions = [e.action for e in entries]
        assert AuditAction.SCORE_SUBMITTED in actions
        assert AuditAction.SCORE_DEFERRED in actions


class TestSubmitAndSave:
    def test_valid_submission_persists_and_returns_record_id(
        self,
        db_connection: psycopg2.extensions.connection,
        inserted_profile_id: str,
        audit_logger: AuditLogger,
    ) -> None:
        session = ReviewSession(inserted_profile_id, "RATER_A", "1.0", audit_logger)
        score = _score(inserted_profile_id, 1, "RATER_A")
        record_id = submit_and_save(db_connection, session, 1, score, audit_logger)
        assert record_id > 0

    def test_invalid_submission_is_audit_logged_and_reraised(
        self,
        db_connection: psycopg2.extensions.connection,
        inserted_profile_id: str,
        audit_logger: AuditLogger,
    ) -> None:
        session = ReviewSession(inserted_profile_id, "RATER_A", "1.0", audit_logger)
        bad_score = _score(inserted_profile_id, 1, "RATER_A", score=99)
        with pytest.raises(AnnotationValidationError):
            submit_and_save(db_connection, session, 1, bad_score, audit_logger)
        entries = audit_logger.read_all()
        assert any(e.action == AuditAction.VALIDATION_REJECTED for e in entries)

    def test_duplicate_submission_is_audit_logged_and_reraised(
        self,
        db_connection: psycopg2.extensions.connection,
        inserted_profile_id: str,
        audit_logger: AuditLogger,
    ) -> None:
        from alcsm.annotation.store import DuplicateScoreError

        session = ReviewSession(inserted_profile_id, "RATER_A", "1.0", audit_logger)
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 2, "RATER_A")
        )
        with pytest.raises(DuplicateScoreError):
            submit_and_save(
                db_connection,
                session,
                2,
                _score(inserted_profile_id, 2, "RATER_A", score=1),
                audit_logger,
            )
        entries = audit_logger.read_all()
        assert any(e.action == AuditAction.DUPLICATE_REJECTED for e in entries)


class TestBlindingGate:
    def test_display_gate_false_before_this_rater_submits(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 1, "RATER_B")
        )
        assert (
            check_blinding_before_display(
                db_connection, inserted_profile_id, 1, "RATER_A"
            )
            is False
        )

    def test_display_gate_false_before_other_rater_submits(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 2, "RATER_A")
        )
        assert (
            check_blinding_before_display(
                db_connection, inserted_profile_id, 2, "RATER_A"
            )
            is False
        )

    def test_display_gate_true_once_both_submitted(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 3, "RATER_A")
        )
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 3, "RATER_B")
        )
        assert (
            check_blinding_before_display(
                db_connection, inserted_profile_id, 3, "RATER_A"
            )
            is True
        )
        assert (
            check_blinding_before_display(
                db_connection, inserted_profile_id, 3, "RATER_B"
            )
            is True
        )
