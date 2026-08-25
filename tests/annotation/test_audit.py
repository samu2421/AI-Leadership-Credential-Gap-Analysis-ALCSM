"""Audit logging: append-only, structural fields only, unsafe-detail rejection."""

from __future__ import annotations

from pathlib import Path

import pytest

from alcsm.annotation.audit import AuditAction, AuditDetailUnsafeError, AuditLogger


@pytest.fixture()
def audit_logger(tmp_path: Path) -> AuditLogger:
    return AuditLogger(tmp_path / "audit_log" / "test_audit.jsonl")


def test_log_and_read_back_round_trip(audit_logger: AuditLogger) -> None:
    audit_logger.record(
        actor="RATER_A",
        action=AuditAction.SCORE_SUBMITTED,
        profile_id="PRF-00001",
        dimension_number=1,
        detail="ACCEPT",
    )
    entries = audit_logger.read_all()
    assert len(entries) == 1
    assert entries[0].actor == "RATER_A"
    assert entries[0].action == AuditAction.SCORE_SUBMITTED
    assert entries[0].profile_id == "PRF-00001"
    assert entries[0].dimension_number == 1


def test_entries_are_append_only_and_ordered(audit_logger: AuditLogger) -> None:
    audit_logger.record(
        actor="RATER_A",
        action=AuditAction.SCORE_SUBMITTED,
        profile_id="PRF-00001",
        dimension_number=1,
    )
    audit_logger.record(
        actor="RATER_A",
        action=AuditAction.SCORE_SUBMITTED,
        profile_id="PRF-00001",
        dimension_number=2,
    )
    audit_logger.record(
        actor="RATER_B",
        action=AuditAction.SCORE_DEFERRED,
        profile_id="PRF-00001",
        dimension_number=3,
    )
    entries = audit_logger.read_all()
    assert [e.dimension_number for e in entries] == [1, 2, 3]


def test_creates_parent_directory_if_missing(tmp_path: Path) -> None:
    nested = tmp_path / "a" / "b" / "c" / "audit.jsonl"
    logger = AuditLogger(nested)
    logger.record(actor="RATER_A", action=AuditAction.PILOT_SELECTED)
    assert nested.exists()


def test_reading_nonexistent_log_returns_empty_list(tmp_path: Path) -> None:
    logger = AuditLogger(tmp_path / "never_written.jsonl")
    assert logger.read_all() == []


def test_url_like_detail_rejected(audit_logger: AuditLogger) -> None:
    with pytest.raises(AuditDetailUnsafeError):
        audit_logger.record(
            actor="RATER_A",
            action=AuditAction.SCORE_SUBMITTED,
            profile_id="PRF-00001",
            dimension_number=4,
            detail="see https://linkedin.com/in/someone for confirmation",
        )


def test_email_like_detail_rejected(audit_logger: AuditLogger) -> None:
    with pytest.raises(AuditDetailUnsafeError):
        audit_logger.record(
            actor="RATER_A",
            action=AuditAction.SCORE_SUBMITTED,
            detail="contact person@example.com to confirm",
        )


def test_plain_structural_detail_is_accepted(audit_logger: AuditLogger) -> None:
    audit_logger.record(
        actor="RATER_A",
        action=AuditAction.VALIDATION_REJECTED,
        profile_id="PRF-00001",
        dimension_number=2,
        detail="score must be between 0 and 5, got 9",
    )
    assert len(audit_logger.read_all()) == 1


def test_no_evidence_text_field_exists_on_audit_entry() -> None:
    """Structural guard: AuditEntry has no field that invites pasting
    evidence/rationale text (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §13)."""
    from dataclasses import fields

    from alcsm.annotation.audit import AuditEntry

    field_names = {f.name for f in fields(AuditEntry)}
    assert "evidence_text" not in field_names
    assert "rationale" not in field_names
