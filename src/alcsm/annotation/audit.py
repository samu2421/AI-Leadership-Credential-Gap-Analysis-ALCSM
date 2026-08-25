"""Append-only audit logging for every annotation-workflow action.

Structured, never contains profile text, evidence, rationale, or any
other free-text content that could carry personal data -- only
pseudonymous IDs and controlled-vocabulary action names (CLAUDE_CODE_
IMPLEMENTATION_GUIDE.md §13: "never log profile text or any personal
data at INFO or above; scrub identifiers from error messages"). The
audit log is a metadata trail of WHO did WHAT to WHICH (pseudonymous)
record WHEN, not a second copy of the data itself.

Writes JSON Lines to a local file so every entry is independently
parseable and a partial/interrupted write never corrupts prior
entries. The audit directory is git-ignored (real rater_ids and
profile_ids will appear here once used for real annotation), mirroring
this project's standing rule that anything touching real records never
enters version control.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import TextIO


class AuditAction(StrEnum):
    SCORE_SUBMITTED = "SCORE_SUBMITTED"
    SCORE_CHANGED = "SCORE_CHANGED"
    SCORE_DEFERRED = "SCORE_DEFERRED"
    ADJUDICATION_SUBMITTED = "ADJUDICATION_SUBMITTED"
    PILOT_SELECTED = "PILOT_SELECTED"
    EXPORT_PRODUCED = "EXPORT_PRODUCED"
    VALIDATION_REJECTED = "VALIDATION_REJECTED"
    DUPLICATE_REJECTED = "DUPLICATE_REJECTED"


@dataclass(frozen=True)
class AuditEntry:
    """One audit-log line. ``detail`` must never carry evidence/rationale
    text -- callers pass only short, structural strings (e.g. a
    validation-rule name), never a quoted profile excerpt.
    """

    timestamp: datetime
    actor: str  # rater_id, or a tool/process name for automated actions
    action: AuditAction
    profile_id: str | None
    dimension_number: int | None
    detail: str | None = None

    def to_json_line(self) -> str:
        record = asdict(self)
        record["timestamp"] = self.timestamp.isoformat()
        record["action"] = self.action.value
        return json.dumps(record, sort_keys=True)


_FORBIDDEN_DETAIL_MARKERS = ("linkedin.com", "http://", "https://", "@")


class AuditDetailUnsafeError(ValueError):
    """Raised when a caller's ``detail`` string looks like it might carry
    a URL or email -- a defensive check, not a full PII scanner (the
    real guarantee is the *caller* convention of only ever passing
    structural strings, per this module's docstring)."""


class AuditLogger:
    """Append-only writer over one audit-log file."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: AuditEntry) -> None:
        if entry.detail:
            lowered = entry.detail.lower()
            if any(marker in lowered for marker in _FORBIDDEN_DETAIL_MARKERS):
                raise AuditDetailUnsafeError(
                    f"audit detail rejected, looks like it may contain a "
                    f"URL/email: {entry.detail!r}"
                )
        handle: TextIO
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(entry.to_json_line())
            handle.write("\n")

    def record(
        self,
        actor: str,
        action: AuditAction,
        profile_id: str | None = None,
        dimension_number: int | None = None,
        detail: str | None = None,
    ) -> AuditEntry:
        """Convenience wrapper: build and log an :class:`AuditEntry` in one call."""
        entry = AuditEntry(
            timestamp=datetime.now(),
            actor=actor,
            action=action,
            profile_id=profile_id,
            dimension_number=dimension_number,
            detail=detail,
        )
        self.log(entry)
        return entry

    def read_all(self) -> list[AuditEntry]:
        """Read every entry back, oldest first. For tests and review, not
        the hot path."""
        if not self._path.exists():
            return []
        entries: list[AuditEntry] = []
        with self._path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                entries.append(
                    AuditEntry(
                        timestamp=datetime.fromisoformat(record["timestamp"]),
                        actor=record["actor"],
                        action=AuditAction(record["action"]),
                        profile_id=record["profile_id"],
                        dimension_number=record["dimension_number"],
                        detail=record["detail"],
                    )
                )
        return entries


def default_audit_log_path() -> Path:
    """The default audit-log location: git-ignored, under 06_Annotation/."""
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "06_Annotation" / "audit_log" / "annotation_audit.jsonl"
