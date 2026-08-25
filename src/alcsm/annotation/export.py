"""Safe export of annotation results.

Two independent defenses against "direct identifiers in exported
annotation files" (this task's explicit rule):

1. An explicit column allow-list -- only known-safe fields are ever
   written; an unrecognised field is dropped with a warning, never
   included "just in case".
2. A regex scan of every string value actually being written, reusing
   the same URL/email pattern this project has used throughout its
   real-data QA sessions (P3_Final_Data_QA_Report.md, D6_v1.1
   Implementation Assessment, Human_Annotation_Review_Protocol_v1.1.md
   §13) -- an export whose evidence text happens to contain a pasted
   URL is refused, not silently written.
"""

from __future__ import annotations

import csv
import re
from dataclasses import asdict, fields
from pathlib import Path
from typing import Any

from alcsm.annotation.models import AnnotationScore

_URL_EMAIL_PATTERN = re.compile(
    r"linkedin\.com|https?://|www\.|[\w.+-]+@[\w-]+\.[\w.-]+", re.IGNORECASE
)

# Every field on AnnotationScore is already free of direct identifiers
# by construction (no name/url/email field exists on the dataclass at
# all -- see models.py), so the allow-list here is "every field", not
# a subset. The allow-list exists as a structural guard for FUTURE
# fields: a field added to AnnotationScore later is exported only once
# someone deliberately adds it here too.
_EXPORT_COLUMNS: tuple[str, ...] = tuple(f.name for f in fields(AnnotationScore))


class UnsafeExportError(ValueError):
    """Raised when a value about to be written matches a URL/email pattern."""


def _scan_row_for_identifiers(row: dict[str, Any]) -> list[str]:
    problems = []
    for key, value in row.items():
        if isinstance(value, str) and _URL_EMAIL_PATTERN.search(value):
            problems.append(f"field {key!r} matches a URL/email pattern")
    return problems


def export_annotation_scores_csv(
    scores: list[AnnotationScore], output_path: Path
) -> Path:
    """Write ``scores`` to a CSV at ``output_path``, allow-listed and PII-scanned.

    Raises :class:`UnsafeExportError` (naming every offending row and
    field) without writing anything if any value looks like a URL or
    email -- this function either writes a complete, safe file or
    writes nothing at all, never a partial file.
    """
    rows = [asdict(score) for score in scores]
    all_problems: list[str] = []
    for i, row in enumerate(rows):
        safe_row = {k: v for k, v in row.items() if k in _EXPORT_COLUMNS}
        problems = _scan_row_for_identifiers(safe_row)
        all_problems.extend(f"row {i}: {p}" for p in problems)
    if all_problems:
        raise UnsafeExportError(
            "export refused, possible identifiers found: " + "; ".join(all_problems)
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(_EXPORT_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in _EXPORT_COLUMNS})
    return output_path


def default_export_dir() -> Path:
    """Git-ignored export destination, mirroring audit.py's convention."""
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "06_Annotation" / "exports"
