"""Tests for checkpoint save/load/validate and restart-safety checks.

No real collection occurs — every checkpoint below references
constructed, synthetic ids, and file I/O uses pytest's `tmp_path`
(CLAUDE_CODE_RULES.md rule 6).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import psycopg2
import pytest

from alcsm.collection.checkpoint import (
    CHECKPOINT_FORMAT_VERSION,
    CheckpointError,
    CollectionCheckpoint,
    load_checkpoint,
    save_checkpoint,
    validate_checkpoint_against_database,
    validate_checkpoint_shape,
)
from alcsm.collection.helper import JobPostingRecord, insert_job_posting


def _checkpoint(**overrides: object) -> CollectionCheckpoint:
    defaults: dict[str, object] = dict(
        sampling_batch_id="BATCH-101",
        corpus="job_posting",
        processed_ids=("JOB-00001", "JOB-00002"),
        failed_ids=("JOB-00003",),
        last_checkpoint_ts=datetime.now(UTC),
    )
    defaults.update(overrides)
    return CollectionCheckpoint(**defaults)  # type: ignore[arg-type]


class TestValidateCheckpointShape:
    def test_valid_checkpoint_has_no_problems(self) -> None:
        assert validate_checkpoint_shape(_checkpoint()) == []

    def test_missing_sampling_batch_id_is_reported(self) -> None:
        errs = validate_checkpoint_shape(_checkpoint(sampling_batch_id=""))
        assert any("sampling_batch_id" in e for e in errs)

    def test_overlap_between_processed_and_failed_is_reported(self) -> None:
        errs = validate_checkpoint_shape(
            _checkpoint(processed_ids=("JOB-00001",), failed_ids=("JOB-00001",))
        )
        assert any("overlap" in e for e in errs)

    def test_duplicate_processed_ids_are_reported(self) -> None:
        errs = validate_checkpoint_shape(
            _checkpoint(processed_ids=("JOB-00001", "JOB-00001"))
        )
        assert any("processed_ids contains duplicate" in e for e in errs)

    def test_unsupported_format_version_is_reported(self) -> None:
        errs = validate_checkpoint_shape(_checkpoint(checkpoint_format_version="99.0"))
        assert any("unsupported checkpoint_format_version" in e for e in errs)

    def test_default_format_version_matches_module_constant(self) -> None:
        assert _checkpoint().checkpoint_format_version == CHECKPOINT_FORMAT_VERSION


class TestSaveAndLoadCheckpoint:
    def test_save_then_load_round_trips(self, tmp_path: Path) -> None:
        checkpoint = _checkpoint()
        path = tmp_path / "checkpoint.json"
        save_checkpoint(checkpoint, path)
        loaded = load_checkpoint(path)
        assert loaded.sampling_batch_id == checkpoint.sampling_batch_id
        assert set(loaded.processed_ids) == set(checkpoint.processed_ids)
        assert set(loaded.failed_ids) == set(checkpoint.failed_ids)

    def test_invalid_checkpoint_is_never_written(self, tmp_path: Path) -> None:
        path = tmp_path / "checkpoint.json"
        bad = _checkpoint(processed_ids=("JOB-00001",), failed_ids=("JOB-00001",))
        with pytest.raises(CheckpointError):
            save_checkpoint(bad, path)
        assert not path.exists()

    def test_save_overwrites_atomically_leaving_no_temp_file(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "checkpoint.json"
        save_checkpoint(_checkpoint(), path)
        save_checkpoint(
            _checkpoint(processed_ids=("JOB-00001", "JOB-00002", "JOB-00004")), path
        )
        loaded = load_checkpoint(path)
        assert len(loaded.processed_ids) == 3
        assert not path.with_suffix(path.suffix + ".tmp").exists()

    def test_second_save_replaces_rather_than_appends(self, tmp_path: Path) -> None:
        """Unlike the audit log (append-only JSONL), a checkpoint file
        holds one current snapshot — the second save must replace, not
        append to, the first."""
        path = tmp_path / "checkpoint.json"
        save_checkpoint(_checkpoint(), path)
        save_checkpoint(_checkpoint(processed_ids=()), path)
        loaded = load_checkpoint(path)
        assert loaded.processed_ids == ()


class TestValidateCheckpointAgainstDatabase:
    def test_checkpoint_matching_real_rows_has_no_problems(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = JobPostingRecord(
            posting_id=unique_posting_id,
            sampling_batch_id=job_posting_batch_id,
            posting_source="example_job_board",
            search_query='"Head of AI"',
            inclusion_reason="title_match",
            collection_ts=datetime.now(UTC),
            raw_posting_text="Seeking a Head of AI. TensorFlow experience preferred.",
        )
        insert_job_posting(db_connection, record)

        checkpoint = _checkpoint(
            sampling_batch_id=job_posting_batch_id,
            processed_ids=(unique_posting_id,),
            failed_ids=(),
        )
        cur = db_connection.cursor()
        errs = validate_checkpoint_against_database(checkpoint, cur)
        cur.close()
        assert errs == []

    def test_checkpoint_claiming_a_nonexistent_row_is_flagged(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
    ) -> None:
        """Restart safety: a stale/corrupt checkpoint claiming a record
        was processed when it was never actually inserted must be
        caught before resuming, not silently trusted."""
        checkpoint = _checkpoint(
            sampling_batch_id=job_posting_batch_id,
            processed_ids=("JOB-99999",),
            failed_ids=(),
        )
        cur = db_connection.cursor()
        errs = validate_checkpoint_against_database(checkpoint, cur)
        cur.close()
        assert any("JOB-99999" in e for e in errs)

    def test_structurally_invalid_checkpoint_is_flagged_before_any_query(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        checkpoint = _checkpoint(
            processed_ids=("JOB-00001",), failed_ids=("JOB-00001",)
        )
        cur = db_connection.cursor()
        errs = validate_checkpoint_against_database(checkpoint, cur)
        cur.close()
        assert any("overlap" in e for e in errs)
