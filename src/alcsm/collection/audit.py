"""GDPR-safe, structured audit logging for collection operations.

Distinct from (and built on top of) the plain ``logging`` calls already
inside ``collection/helper.py``: this module provides a structured,
replayable event record — batch creation/completion, validation
failures, duplicate detections, checkpoint events, recovery events —
suitable for the operational reports built in ``collection/reporting.py``.

The GDPR requirement ("never log personal information",
PROJECT_CONTEXT.md §31, §45) is enforced here, not just followed by
convention: :func:`validate_audit_event` rejects an event whose
``entity_id`` is not pseudonymous-shaped, whose ``details`` use a
known free-text field name, or whose ``details`` values contain a
machine-detectable personal-identifier pattern (reusing
``collection.helper.detect_recruiter_identifiers`` rather than
duplicating that logic).
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal

from alcsm.collection.helper import detect_recruiter_identifiers
from alcsm.logging_config import get_logger

logger = get_logger(__name__)

AuditEventType = Literal[
    "batch_created",
    "batch_completed",
    "batch_failed",
    "record_inserted",
    "record_validation_failed",
    "duplicate_detected",
    "checkpoint_saved",
    "checkpoint_loaded",
    "checkpoint_validation_failed",
    "recovery_started",
    "recovery_completed",
]

AUDIT_EVENT_TYPES: tuple[AuditEventType, ...] = (
    "batch_created",
    "batch_completed",
    "batch_failed",
    "record_inserted",
    "record_validation_failed",
    "duplicate_detected",
    "checkpoint_saved",
    "checkpoint_loaded",
    "checkpoint_validation_failed",
    "recovery_started",
    "recovery_completed",
)

# Pseudonymous-identifier shapes an `entity_id` is allowed to take
# (profile, job posting, sampling batch, taxonomy version) — anything
# else is refused rather than logged.
_ENTITY_ID_PATTERN = re.compile(r"^(PRF-\d{5}|JOB-\d{5}|BATCH-\d{3}|TAX-[\w-]+)$")


def is_pseudonymous_id(value: str | None) -> bool:
    """Whether ``value`` is shaped like a recognised pseudonymous id.

    Exposed for callers (e.g. ``collection.manager``) that need to
    decide *before* constructing an :class:`AuditEvent` whether a
    candidate identifier is safe to use as ``entity_id`` — most
    importantly, a record that failed validation *because* its own id
    is malformed must not have that malformed id passed straight
    through as ``entity_id``, or recording the failure would itself
    raise :class:`AuditLogError` and mask the original error.
    """
    return value is not None and bool(_ENTITY_ID_PATTERN.fullmatch(value))


# Detail keys that would only ever hold free text long enough to carry
# an identifier — refused outright regardless of content, in addition
# to the content scan below.
_FORBIDDEN_DETAIL_KEYS = (
    "raw_posting_text",
    "raw_requirements_text",
    "section_text",
    "name",
    "email",
    "phone",
    "profile_url",
    "url",
)

DetailValue = str | int | float | bool | None


class AuditLogError(ValueError):
    """An audit event violates the GDPR-safe logging contract."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("Validation failed:\n  - " + "\n  - ".join(problems))


@dataclass(frozen=True)
class AuditEvent:
    """One structured, GDPR-safe audit record.

    ``entity_id`` is a pseudonymous identifier or None (e.g. a
    corpus-wide event with no single record). ``details`` carries only
    small, non-personal operational metadata (counts, booleans,
    short codes) — never raw collected text.
    """

    event_type: AuditEventType
    entity_id: str | None
    timestamp: datetime
    details: Mapping[str, DetailValue] = field(default_factory=dict)


def validate_audit_event(event: AuditEvent) -> list[str]:
    """Return every rule violation found in ``event`` (empty if valid).

    Enforces: ``event_type`` is in the controlled vocabulary;
    ``entity_id`` (if set) is pseudonymous-shaped; no ``details`` key
    is a known free-text field name; no string ``details`` value
    contains a machine-detectable personal-identifier pattern.
    """
    errs: list[str] = []

    if event.event_type not in AUDIT_EVENT_TYPES:
        errs.append(f"event_type {event.event_type!r} is not a recognised audit event")

    if event.entity_id is not None and not is_pseudonymous_id(event.entity_id):
        errs.append(
            f"entity_id {event.entity_id!r} is not a recognised pseudonymous id "
            "(expected PRF-/JOB-/BATCH-/TAX- shape)"
        )

    for key, value in event.details.items():
        if key in _FORBIDDEN_DETAIL_KEYS:
            errs.append(f"details key {key!r} must never appear in an audit event")
        if isinstance(value, str):
            for finding in detect_recruiter_identifiers(value):
                errs.append(f"details[{key!r}]: {finding}")

    return errs


class AuditLog:
    """An append-only, in-memory audit trail, optionally persisted.

    Every :meth:`record` call validates first (rejecting personal
    data before it is ever appended, not after); nothing is added to
    the trail on a validation failure.
    """

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        problems = validate_audit_event(event)
        if problems:
            raise AuditLogError(problems)
        self._events.append(event)
        logger.info("audit: %s entity=%s", event.event_type, event.entity_id)

    def events(self) -> tuple[AuditEvent, ...]:
        """All recorded events, in the order they were recorded."""
        return tuple(self._events)

    def events_of_type(self, event_type: AuditEventType) -> tuple[AuditEvent, ...]:
        return tuple(e for e in self._events if e.event_type == event_type)

    def count_of_type(self, event_type: AuditEventType) -> int:
        return len(self.events_of_type(event_type))

    def save(self, path: Path) -> None:
        """Append every recorded event to ``path`` as JSON Lines.

        Deterministic, human-readable, and diffable — one JSON object
        per line, matching the "collection log" pattern already
        specified in Task5_P3_Sampling_Framework_Design.md §13 (kept
        outside the database and outside Git in real operation).
        """
        with path.open("a", encoding="utf-8") as f:
            for event in self._events:
                f.write(
                    json.dumps(
                        {
                            "event_type": event.event_type,
                            "entity_id": event.entity_id,
                            "timestamp": event.timestamp.isoformat(),
                            "details": dict(event.details),
                        },
                        sort_keys=True,
                    )
                )
                f.write("\n")

    @classmethod
    def load(cls, path: Path) -> AuditLog:
        """Reconstruct an :class:`AuditLog` from a JSON Lines file
        written by :meth:`save`. Re-validates every event on load, so
        a hand-edited or corrupted file is caught immediately rather
        than silently trusted.
        """
        log = cls()
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                event = AuditEvent(
                    event_type=data["event_type"],
                    entity_id=data["entity_id"],
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                    details=data["details"],
                )
                log.record(event)
        return log
