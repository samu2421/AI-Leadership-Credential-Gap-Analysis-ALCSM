"""Tests for GDPR-safe structured audit logging.

No database required — pure logic plus file save/load round-tripping
via pytest's `tmp_path`. No real personal data anywhere
(CLAUDE_CODE_RULES.md rule 6).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from alcsm.collection.audit import (
    AuditEvent,
    AuditLog,
    AuditLogError,
    validate_audit_event,
)


def _event(**overrides: object) -> AuditEvent:
    defaults: dict[str, object] = dict(
        event_type="record_inserted",
        entity_id="PRF-00001",
        timestamp=datetime.now(UTC),
        details={"corpus": "profile"},
    )
    defaults.update(overrides)
    return AuditEvent(**defaults)  # type: ignore[arg-type]


class TestValidateAuditEvent:
    def test_valid_event_has_no_problems(self) -> None:
        assert validate_audit_event(_event()) == []

    def test_unrecognised_event_type_is_rejected(self) -> None:
        errs = validate_audit_event(_event(event_type="something_else"))
        assert any("not a recognised audit event" in e for e in errs)

    @pytest.mark.parametrize(
        "valid_id", ["PRF-00001", "JOB-00042", "BATCH-001", "TAX-0001"]
    )
    def test_all_pseudonymous_id_shapes_are_accepted(self, valid_id: str) -> None:
        assert validate_audit_event(_event(entity_id=valid_id)) == []

    def test_none_entity_id_is_accepted(self) -> None:
        assert validate_audit_event(_event(entity_id=None)) == []

    @pytest.mark.parametrize("bad_id", ["jane.doe", "12345", "profile-1"])
    def test_non_pseudonymous_entity_id_is_rejected(self, bad_id: str) -> None:
        errs = validate_audit_event(_event(entity_id=bad_id))
        assert any("not a recognised pseudonymous id" in e for e in errs)

    @pytest.mark.parametrize(
        "forbidden_key", ["raw_posting_text", "name", "email", "phone", "url"]
    )
    def test_forbidden_detail_key_is_rejected(self, forbidden_key: str) -> None:
        errs = validate_audit_event(_event(details={forbidden_key: "x"}))
        assert any(f"details key {forbidden_key!r}" in e for e in errs)

    def test_email_in_a_detail_value_is_rejected(self) -> None:
        errs = validate_audit_event(
            _event(details={"note": "contact jane@example.com"})
        )
        assert any("email" in e for e in errs)

    def test_ordinary_operational_detail_values_are_accepted(self) -> None:
        errs = validate_audit_event(
            _event(details={"corpus": "profile", "problem_count": 3, "ok": True})
        )
        assert errs == []


class TestAuditLogRecording:
    def test_valid_event_is_recorded(self) -> None:
        log = AuditLog()
        log.record(_event())
        assert len(log.events()) == 1

    def test_invalid_event_is_rejected_and_not_recorded(self) -> None:
        log = AuditLog()
        with pytest.raises(AuditLogError):
            log.record(_event(entity_id="not-pseudonymous"))
        assert len(log.events()) == 0

    def test_events_of_type_filters_correctly(self) -> None:
        log = AuditLog()
        log.record(_event(event_type="record_inserted"))
        log.record(_event(event_type="duplicate_detected", entity_id=None))
        log.record(_event(event_type="record_inserted"))
        assert log.count_of_type("record_inserted") == 2
        assert log.count_of_type("duplicate_detected") == 1
        assert log.count_of_type("batch_failed") == 0

    def test_events_preserve_recording_order(self) -> None:
        log = AuditLog()
        log.record(_event(event_type="batch_created", entity_id="BATCH-001"))
        log.record(_event(event_type="batch_completed", entity_id="BATCH-001"))
        types = [e.event_type for e in log.events()]
        assert types == ["batch_created", "batch_completed"]


class TestAuditLogSaveAndLoad:
    def test_save_then_load_round_trips(self, tmp_path: Path) -> None:
        log = AuditLog()
        log.record(_event(event_type="batch_created", entity_id="BATCH-001"))
        log.record(_event(event_type="record_inserted", entity_id="PRF-00001"))

        path = tmp_path / "audit.jsonl"
        log.save(path)

        loaded = AuditLog.load(path)
        assert len(loaded.events()) == 2
        assert [e.event_type for e in loaded.events()] == [
            "batch_created",
            "record_inserted",
        ]

    def test_save_appends_across_calls(self, tmp_path: Path) -> None:
        path = tmp_path / "audit.jsonl"
        first = AuditLog()
        first.record(_event(event_type="batch_created", entity_id="BATCH-001"))
        first.save(path)

        second = AuditLog()
        second.record(_event(event_type="batch_completed", entity_id="BATCH-001"))
        second.save(path)

        loaded = AuditLog.load(path)
        assert len(loaded.events()) == 2

    def test_saved_file_contains_no_forbidden_content(self, tmp_path: Path) -> None:
        """Defence in depth: even the serialized file, read as plain
        text, must never contain a forbidden detail key name — since
        every event is validated before being appended, this should
        always hold, and this test guards that invariant directly."""
        log = AuditLog()
        log.record(
            _event(
                event_type="record_inserted",
                details={"corpus": "profile", "sampling_batch_id": "BATCH-001"},
            )
        )
        path = tmp_path / "audit.jsonl"
        log.save(path)
        content = path.read_text()
        assert "raw_posting_text" not in content
        assert "@" not in content
