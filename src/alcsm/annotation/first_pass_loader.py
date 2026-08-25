"""Read-only loader for the researcher-review workbook's first-pass data.

Loads ``ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx``'s
``Dimension_Evidence`` sheet into :class:`~alcsm.annotation.models.
FirstPassReference` objects for display in the P4 interface. Never
writes to the workbook, never treats its ``Final_Score`` column as
gold-standard data, and is never used inside a test with the real
file (tests use a small constructed workbook built with the same
column shape -- see ``tests/annotation/conftest.py``).

This module is the concrete implementation of the "first-pass/
reference score display where appropriate" requirement: it supplies
:class:`FirstPassReference` rows for :mod:`alcsm.app.annotation_app`
to render alongside (never instead of) the researcher's own
:class:`~alcsm.annotation.models.AnnotationScore` entry field.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from alcsm.annotation.models import FirstPassReference
from alcsm.constants import MissingStatus

_DIMENSION_LABEL_TO_NUMBER: dict[str, int] = {f"D{i}": i for i in range(1, 7)}


class FirstPassWorkbookNotFoundError(FileNotFoundError):
    """Raised when the review workbook is not present at the given path.

    A normal, expected condition (the workbook is git-ignored and may
    simply not exist in this checkout, e.g. CI or a fresh clone) --
    callers should catch this and render "no first-pass data
    available" rather than letting a bare ``FileNotFoundError``
    surface.
    """


def default_review_workbook_path() -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx"


def load_first_pass_references(
    workbook_path: Path | None = None,
) -> dict[str, dict[int, FirstPassReference]]:
    """Load every profile x dimension row from the review workbook.

    Returns ``{profile_id: {dimension_number: FirstPassReference}}``.
    Raises :class:`FirstPassWorkbookNotFoundError` if ``workbook_path``
    (or the default location) does not exist -- never returns a
    silently-empty result for a missing file, since that would be
    indistinguishable from "the file exists and genuinely has no
    rows".
    """
    path = workbook_path or default_review_workbook_path()
    if not path.exists():
        raise FirstPassWorkbookNotFoundError(str(path))

    df = pd.read_excel(path, sheet_name="Dimension_Evidence")

    out: dict[str, dict[int, FirstPassReference]] = {}
    for row in df.itertuples(index=False):
        profile_id = str(row.Profile_ID)
        dimension_number = _DIMENSION_LABEL_TO_NUMBER.get(str(row.Dimension))
        if dimension_number is None:
            continue
        missing_status: MissingStatus = row.Missing_Status  # type: ignore[assignment]
        final_score = row.Final_Score
        reference = FirstPassReference(
            profile_id=profile_id,
            dimension_number=dimension_number,
            first_pass_score=int(row.FirstPass_Score),
            final_reviewed_score=(int(final_score) if pd.notna(final_score) else None),
            evidence=(row.Evidence if pd.notna(row.Evidence) else None),
            rationale=(row.Rationale if pd.notna(row.Rationale) else None),
            missing_status=missing_status,
            confidence=str(row.Confidence),
            review_required=(str(row.Review_Required).upper() == "YES"),
        )
        out.setdefault(profile_id, {})[dimension_number] = reference
    return out


def load_first_pass_for_profile(
    profile_id: str, workbook_path: Path | None = None
) -> dict[int, FirstPassReference]:
    """Convenience wrapper: first-pass references for one profile only."""
    all_refs = load_first_pass_references(workbook_path)
    return all_refs.get(profile_id, {})
