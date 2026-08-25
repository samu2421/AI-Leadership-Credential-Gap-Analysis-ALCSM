"""alcsm.analysis.data_sources: loader error handling.

Does not read the real files (they may not exist in this checkout,
and must never be required for the test suite to pass -- CLAUDE_CODE_
RULES.md rule 6). Only exercises the "file not found" path and the
`AnalysisPaths` plumbing with a `tmp_path`-based override.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from alcsm.analysis.config import AnalysisPaths
from alcsm.analysis.data_sources import (
    SourceFileNotFoundError,
    load_dimension_evidence,
    load_job_postings_processed,
    load_linkedin_processed,
    load_profile_scores,
    load_review_changes,
    load_survey_raw,
)


@pytest.fixture()
def missing_paths(tmp_path: Path) -> AnalysisPaths:
    return AnalysisPaths(
        repo_root=tmp_path,
        review_workbook=tmp_path / "does_not_exist_review.xlsx",
        linkedin_processed=tmp_path / "does_not_exist_linkedin.xlsx",
        job_postings_processed=tmp_path / "does_not_exist_jobs.xlsx",
        survey_responses=tmp_path / "does_not_exist_survey.xlsx",
    )


def test_load_profile_scores_missing_file_raises(missing_paths: AnalysisPaths) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_profile_scores(missing_paths)


def test_load_dimension_evidence_missing_file_raises(
    missing_paths: AnalysisPaths,
) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_dimension_evidence(missing_paths)


def test_load_review_changes_missing_file_raises(missing_paths: AnalysisPaths) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_review_changes(missing_paths)


def test_load_linkedin_processed_missing_file_raises(
    missing_paths: AnalysisPaths,
) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_linkedin_processed(missing_paths)


def test_load_job_postings_missing_file_raises(missing_paths: AnalysisPaths) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_job_postings_processed(missing_paths)


def test_load_survey_raw_missing_file_raises(missing_paths: AnalysisPaths) -> None:
    with pytest.raises(SourceFileNotFoundError):
        load_survey_raw(missing_paths)


def test_load_profile_scores_infers_status_from_a_real_looking_file(
    tmp_path: Path,
) -> None:
    """A constructed, non-personal .xlsx round-trip, proving the loader
    + status inference work together end to end without touching any
    real data file."""
    path = tmp_path / "constructed_review.xlsx"
    df = pd.DataFrame(
        [
            {"Profile_ID": "PRF-90001", "Overall_Review_Status": "Pending Review"},
            {"Profile_ID": "PRF-90002", "Overall_Review_Status": "Reviewed"},
        ]
    )
    df.to_excel(path, sheet_name="Profile_Scores", index=False)
    paths = AnalysisPaths(
        repo_root=tmp_path,
        review_workbook=path,
        linkedin_processed=tmp_path / "x.xlsx",
        job_postings_processed=tmp_path / "y.xlsx",
        survey_responses=tmp_path / "z.xlsx",
    )
    bundle = load_profile_scores(paths)
    assert bundle.data_status == "provisional_first_pass"
    assert len(bundle.scores) == 2
