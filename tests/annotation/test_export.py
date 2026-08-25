"""Export safety: allow-listed columns, no partial writes, PII-scan refusal."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pytest

from alcsm.annotation.export import UnsafeExportError, export_annotation_scores_csv
from alcsm.annotation.models import AnnotationScore

_NOW = datetime.now()


def _score(**overrides: object) -> AnnotationScore:
    defaults: dict[str, object] = dict(
        profile_id="PRF-00001",
        dimension_number=1,
        rater_id="RATER_A",
        score=3,
        missing_status="present",
        rulebook_version="1.0",
        coding_ts=_NOW,
        evidence_text="fixture evidence text",
    )
    defaults.update(overrides)
    return AnnotationScore(**defaults)  # type: ignore[arg-type]


def test_safe_export_writes_all_rows(tmp_path: Path) -> None:
    scores = [_score(dimension_number=d) for d in range(1, 7)]
    out = export_annotation_scores_csv(scores, tmp_path / "export.csv")
    with out.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6


def test_export_refuses_url_in_evidence_text(tmp_path: Path) -> None:
    scores = [_score(evidence_text="see https://linkedin.com/in/someone")]
    out_path = tmp_path / "export.csv"
    with pytest.raises(UnsafeExportError):
        export_annotation_scores_csv(scores, out_path)
    assert not out_path.exists(), "unsafe export must write nothing, not a partial file"


def test_export_refuses_email_in_notes(tmp_path: Path) -> None:
    scores = [_score(notes="contact person@example.com")]
    out_path = tmp_path / "export.csv"
    with pytest.raises(UnsafeExportError):
        export_annotation_scores_csv(scores, out_path)
    assert not out_path.exists()


def test_export_all_or_nothing_across_rows(tmp_path: Path) -> None:
    """One unsafe row among many safe ones still blocks the whole export
    -- never a partial file with the unsafe row silently dropped."""
    scores = [
        _score(dimension_number=1),
        _score(dimension_number=2, evidence_text="www.example.com"),
    ]
    out_path = tmp_path / "export.csv"
    with pytest.raises(UnsafeExportError):
        export_annotation_scores_csv(scores, out_path)
    assert not out_path.exists()


def test_export_creates_parent_directories(tmp_path: Path) -> None:
    out_path = tmp_path / "nested" / "dir" / "export.csv"
    export_annotation_scores_csv([_score()], out_path)
    assert out_path.exists()


def test_exported_columns_match_annotation_score_fields(tmp_path: Path) -> None:
    from dataclasses import fields

    out = export_annotation_scores_csv([_score()], tmp_path / "export.csv")
    with out.open(encoding="utf-8") as handle:
        header = next(csv.reader(handle))
    expected = {f.name for f in fields(AnnotationScore)}
    assert set(header) == expected
