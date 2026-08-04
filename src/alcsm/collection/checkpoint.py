"""Checkpoint and resume support for interrupted collection sessions.

A checkpoint records only pseudonymous record ids and counts — never
raw collected text — so it carries no personal data itself
(PROJECT_CONTEXT.md §45) and, like the collection log it complements,
is meant to live outside the database and outside Git in real
operation (Task5_P3_Sampling_Framework_Design.md §13). This module
builds and tests the checkpoint *mechanism*; where a real checkpoint
file lives during real collection is an operational decision for that
later, ethics-gated phase, not something this session hard-codes.

No real collection occurs here — every test uses constructed,
synthetic ids against a temporary file path.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from psycopg2.extensions import cursor as PGCursor

from alcsm.constants import Corpus

CHECKPOINT_FORMAT_VERSION = "1.0"


class CheckpointError(ValueError):
    """A checkpoint file or its content violates the checkpoint contract."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("Validation failed:\n  - " + "\n  - ".join(problems))


@dataclass(frozen=True)
class CollectionCheckpoint:
    """A point-in-time snapshot of one batch's collection progress.

    ``processed_ids`` and ``failed_ids`` are disjoint by construction
    (enforced by :func:`validate_checkpoint`) — a record is either
    successfully captured or it failed, never both, matching the
    atomic, all-or-nothing insert contract in ``collection/helper.py``.
    """

    sampling_batch_id: str
    corpus: Corpus
    processed_ids: tuple[str, ...] = ()
    failed_ids: tuple[str, ...] = ()
    last_checkpoint_ts: datetime = field(default_factory=datetime.now)
    checkpoint_format_version: str = CHECKPOINT_FORMAT_VERSION


def validate_checkpoint_shape(checkpoint: CollectionCheckpoint) -> list[str]:
    """Return every structural problem found (empty if valid).

    Checks only what can be known from the checkpoint object itself —
    no database access. See :func:`validate_checkpoint_against_database`
    for the restart-safety cross-check.
    """
    errs: list[str] = []
    if not checkpoint.sampling_batch_id:
        errs.append("missing field: sampling_batch_id")
    overlap = set(checkpoint.processed_ids) & set(checkpoint.failed_ids)
    if overlap:
        errs.append(
            f"processed_ids and failed_ids overlap (a record cannot be both): "
            f"{sorted(overlap)}"
        )
    if len(checkpoint.processed_ids) != len(set(checkpoint.processed_ids)):
        errs.append("processed_ids contains duplicate entries")
    if len(checkpoint.failed_ids) != len(set(checkpoint.failed_ids)):
        errs.append("failed_ids contains duplicate entries")
    if checkpoint.checkpoint_format_version != CHECKPOINT_FORMAT_VERSION:
        errs.append(
            f"unsupported checkpoint_format_version "
            f"{checkpoint.checkpoint_format_version!r} "
            f"(expected {CHECKPOINT_FORMAT_VERSION!r})"
        )
    return errs


def save_checkpoint(checkpoint: CollectionCheckpoint, path: Path) -> None:
    """Write ``checkpoint`` to ``path`` as deterministic JSON.

    Validates shape first — an invalid checkpoint is never written.
    Overwrites any existing file at ``path`` atomically (write to a
    temp file, then replace), so a crash mid-write cannot corrupt a
    previously-good checkpoint (restart safety, Task 2).
    """
    problems = validate_checkpoint_shape(checkpoint)
    if problems:
        raise CheckpointError(problems)

    payload = {
        "sampling_batch_id": checkpoint.sampling_batch_id,
        "corpus": checkpoint.corpus,
        "processed_ids": sorted(checkpoint.processed_ids),
        "failed_ids": sorted(checkpoint.failed_ids),
        "last_checkpoint_ts": checkpoint.last_checkpoint_ts.isoformat(),
        "checkpoint_format_version": checkpoint.checkpoint_format_version,
    }
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    tmp_path.replace(path)


def load_checkpoint(path: Path) -> CollectionCheckpoint:
    """Read a :class:`CollectionCheckpoint` previously written by
    :func:`save_checkpoint`. Re-validates shape on load, so a
    corrupted or hand-edited file is caught immediately.
    """
    data = json.loads(path.read_text())
    checkpoint = CollectionCheckpoint(
        sampling_batch_id=data["sampling_batch_id"],
        corpus=data["corpus"],
        processed_ids=tuple(data["processed_ids"]),
        failed_ids=tuple(data["failed_ids"]),
        last_checkpoint_ts=datetime.fromisoformat(data["last_checkpoint_ts"]),
        checkpoint_format_version=data["checkpoint_format_version"],
    )
    problems = validate_checkpoint_shape(checkpoint)
    if problems:
        raise CheckpointError(problems)
    return checkpoint


def validate_checkpoint_against_database(
    checkpoint: CollectionCheckpoint, cur: PGCursor
) -> list[str]:
    """Cross-check a checkpoint's claims against the live database.

    Restart safety (Task 2): a checkpoint claiming a record was
    processed must correspond to a real row in the database — if it
    does not, the checkpoint is stale or corrupt, and resuming from it
    without this check could silently skip a record that was never
    actually captured.
    """
    errs = validate_checkpoint_shape(checkpoint)

    table = "profile" if checkpoint.corpus == "profile" else "job_posting"
    id_column = "profile_id" if checkpoint.corpus == "profile" else "posting_id"

    for record_id in checkpoint.processed_ids:
        cur.execute(
            f"SELECT 1 FROM alcsm.{table} WHERE {id_column} = %s AND "
            "sampling_batch_id = %s",
            (record_id, checkpoint.sampling_batch_id),
        )
        if cur.fetchone() is None:
            errs.append(
                f"checkpoint claims {record_id!r} was processed, but no such row "
                f"exists in alcsm.{table} for batch {checkpoint.sampling_batch_id!r}"
            )

    return errs
