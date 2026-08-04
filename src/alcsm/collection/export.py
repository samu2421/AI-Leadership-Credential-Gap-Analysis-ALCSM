"""Export infrastructure for validated collection metadata.

Exports *metadata only* — batch provenance, counts, and per-record
identifiers/provenance fields — never raw profile section text or job-
posting text. This is a hard rule enforced by an explicit column
allow-list below, not left to caller discipline: a later research
phase (NLP, analysis) reads real text through the frozen schema/views
directly when the time comes; this export exists to let *operational*
metadata be reviewed/archived without opening the whole database.

No real dataset is exported during this session — every test exports
constructed, synthetic fixture data to a temporary path (Task 7's
explicit "infrastructure only" boundary).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from psycopg2.extensions import cursor as PGCursor

from alcsm.constants import Corpus

EXPORT_FORMAT_VERSION = "1.0"

# Explicit allow-list: only these columns may ever be exported. Never
# raw_posting_text, raw_requirements_text, or any profile section text.
_PROFILE_METADATA_COLUMNS = (
    "profile_id",
    "sampling_batch_id",
    "search_query",
    "search_rank_position",
    "inclusion_reason",
    "collection_ts",
    "profile_language",
    "profile_geography",
)
_JOB_POSTING_METADATA_COLUMNS = (
    "posting_id",
    "sampling_batch_id",
    "posting_source",
    "search_query",
    "search_rank_position",
    "inclusion_reason",
    "collection_ts",
    "posting_language",
    "posting_geography",
    "posted_date",
)


def _table_id_and_columns(corpus: Corpus) -> tuple[str, str, tuple[str, ...]]:
    if corpus == "profile":
        return "profile", "profile_id", _PROFILE_METADATA_COLUMNS
    return "job_posting", "posting_id", _JOB_POSTING_METADATA_COLUMNS


@dataclass(frozen=True)
class ExportManifest:
    """Describes one export: what was exported, when, and how much."""

    export_format_version: str
    corpus: Corpus
    sampling_batch_id: str
    record_count: int
    generated_ts: datetime
    output_path: str


def export_batch_metadata(
    cur: PGCursor,
    sampling_batch_id: str,
    corpus: Corpus,
    output_path: Path,
) -> ExportManifest:
    """Export one batch's record *metadata* (never raw text) to a
    deterministic, versioned JSON file.

    Deterministic: records are ordered by their id column, so the same
    database state always produces byte-identical output. Versioned:
    every export stamps ``export_format_version`` so a later reader
    knows which shape to expect, mirroring the versioning discipline
    already applied to schema/rulebook/taxonomy artefacts
    (PROJECT_CONTEXT.md §37).
    """
    table, id_column, columns = _table_id_and_columns(corpus)
    column_list = ", ".join(columns)
    cur.execute(
        f"SELECT {column_list} FROM alcsm.{table} "
        f"WHERE sampling_batch_id = %s ORDER BY {id_column}",
        (sampling_batch_id,),
    )
    rows = cur.fetchall()

    records = []
    for row in rows:
        record: dict[str, object] = {}
        for col, value in zip(columns, row, strict=True):
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            record[col] = value
        records.append(record)

    generated_ts = datetime.now(UTC)
    payload = {
        "export_format_version": EXPORT_FORMAT_VERSION,
        "corpus": corpus,
        "sampling_batch_id": sampling_batch_id,
        "generated_ts": generated_ts.isoformat(),
        "record_count": len(records),
        "records": records,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return ExportManifest(
        export_format_version=EXPORT_FORMAT_VERSION,
        corpus=corpus,
        sampling_batch_id=sampling_batch_id,
        record_count=len(records),
        generated_ts=generated_ts,
        output_path=str(output_path),
    )
