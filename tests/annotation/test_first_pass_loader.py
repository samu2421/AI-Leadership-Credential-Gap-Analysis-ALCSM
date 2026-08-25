"""First-pass reference loader: reads a review workbook's shape, never
real data. A small constructed workbook, matching `Dimension_Evidence`'s
real column layout, is built fresh in a tmp_path for every test.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from alcsm.annotation.first_pass_loader import (
    FirstPassWorkbookNotFoundError,
    load_first_pass_for_profile,
    load_first_pass_references,
)


def _write_constructed_workbook(path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                "Profile_ID": "PRF-90001",
                "Dimension": "D1",
                "FirstPass_Score": 4,
                "Final_Score": 4,
                "Evidence": "fixture evidence D1",
                "Rationale": "fixture rationale",
                "Missing_Status": "present",
                "Confidence": "HIGH",
                "Review_Required": "NO",
            },
            {
                "Profile_ID": "PRF-90001",
                "Dimension": "D6",
                "FirstPass_Score": 3,
                "Final_Score": 3,
                "Evidence": "3 distinct industries",
                "Rationale": "D6 v1.1 breadth",
                "Missing_Status": "present",
                "Confidence": "MEDIUM",
                "Review_Required": "YES",
            },
            {
                "Profile_ID": "PRF-90002",
                "Dimension": "D4",
                "FirstPass_Score": 0,
                "Final_Score": None,
                "Evidence": None,
                "Rationale": None,
                "Missing_Status": "unavailable",
                "Confidence": "HIGH",
                "Review_Required": "NO",
            },
        ]
    )
    df.to_excel(path, sheet_name="Dimension_Evidence", index=False)


def test_missing_workbook_raises_clear_error(tmp_path: Path) -> None:
    with pytest.raises(FirstPassWorkbookNotFoundError):
        load_first_pass_references(tmp_path / "does_not_exist.xlsx")


def test_loads_all_rows_grouped_by_profile_and_dimension(tmp_path: Path) -> None:
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    refs = load_first_pass_references(path)
    assert set(refs.keys()) == {"PRF-90001", "PRF-90002"}
    assert set(refs["PRF-90001"].keys()) == {1, 6}


def test_first_pass_score_and_final_reviewed_score_are_distinct_fields(
    tmp_path: Path,
) -> None:
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    refs = load_first_pass_references(path)
    d1 = refs["PRF-90001"][1]
    assert d1.first_pass_score == 4
    assert d1.final_reviewed_score == 4


def test_unreviewed_final_score_is_none_not_zero(tmp_path: Path) -> None:
    """A NaN Final_Score in the workbook (not yet reviewed) must load as
    None, never silently coerced to 0 -- 0 is a real, distinct score."""
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    refs = load_first_pass_references(path)
    d4 = refs["PRF-90002"][4]
    assert d4.final_reviewed_score is None
    assert d4.first_pass_score == 0


def test_review_required_parsed_as_bool(tmp_path: Path) -> None:
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    refs = load_first_pass_references(path)
    assert refs["PRF-90001"][6].review_required is True
    assert refs["PRF-90001"][1].review_required is False


def test_load_first_pass_for_profile_convenience_wrapper(tmp_path: Path) -> None:
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    dims = load_first_pass_for_profile("PRF-90002", path)
    assert set(dims.keys()) == {4}


def test_unknown_profile_returns_empty_dict(tmp_path: Path) -> None:
    path = tmp_path / "constructed_review.xlsx"
    _write_constructed_workbook(path)
    assert load_first_pass_for_profile("PRF-99999", path) == {}
