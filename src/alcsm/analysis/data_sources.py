"""Reusable, read-only loaders for every real-data source RQ1-RQ5 read from.

Every loader here is read-only (never writes back to its source file,
matching the same discipline `alcsm.annotation.first_pass_loader`
already established) and raises a clear, specific, catchable error if
its source file is absent, rather than a bare `FileNotFoundError` a
caller has to guess about. None of them print or log cell contents —
callers that need to inspect a loaded DataFrame's actual values are
responsible for following this project's standing rule against
surfacing raw evidence/free-text/PII (see e.g. `P3_Final_Data_QA_
Report.md`'s and `Human_Annotation_Review_Protocol_v1.1.md`'s
"aggregate counts only" discipline, applied here at the loader layer
by simply never calling `print`/`log` on cell values).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from alcsm.analysis.config import (
    AnalysisPaths,
    DataStatus,
    default_analysis_paths,
    infer_profile_scores_status,
)


class SourceFileNotFoundError(FileNotFoundError):
    """Raised when a real-data source file is not present at its expected
    (git-ignored) path. A normal, expected condition in a fresh clone
    or CI -- callers should catch this and fall back to fixtures."""


def _require(path: Path) -> Path:
    if not path.exists():
        raise SourceFileNotFoundError(str(path))
    return path


@dataclass(frozen=True)
class ProfileScoresBundle:
    """`Profile_Scores` plus the inferred data-provenance status."""

    scores: pd.DataFrame
    data_status: DataStatus
    source_path: Path


def load_profile_scores(paths: AnalysisPaths | None = None) -> ProfileScoresBundle:
    """Load `Profile_Scores` from the researcher-review workbook.

    `data_status` is inferred from `Overall_Review_Status`
    (:func:`alcsm.analysis.config.infer_profile_scores_status`) --
    never hardcoded, never assumed "final" by default.
    """
    paths = paths or default_analysis_paths()
    path = _require(paths.review_workbook)
    scores = pd.read_excel(path, sheet_name="Profile_Scores")
    status = infer_profile_scores_status(scores["Overall_Review_Status"])
    return ProfileScoresBundle(scores=scores, data_status=status, source_path=path)


def load_dimension_evidence(paths: AnalysisPaths | None = None) -> pd.DataFrame:
    """Load `Dimension_Evidence` (one row per profile x dimension)."""
    paths = paths or default_analysis_paths()
    path = _require(paths.review_workbook)
    return pd.read_excel(path, sheet_name="Dimension_Evidence")


def load_review_changes(paths: AnalysisPaths | None = None) -> pd.DataFrame:
    """Load `Review_Changes` (populated only once the researcher has
    actually changed a first-pass score; may legitimately be empty)."""
    paths = paths or default_analysis_paths()
    path = _require(paths.review_workbook)
    return pd.read_excel(path, sheet_name="Review_Changes")


def load_d6_quality_review(paths: AnalysisPaths | None = None) -> pd.DataFrame:
    """Load `D6_Quality_Review` (one row per profile, D6-specific flags)."""
    paths = paths or default_analysis_paths()
    path = _require(paths.review_workbook)
    return pd.read_excel(path, sheet_name="D6_Quality_Review")


@dataclass(frozen=True)
class LinkedInProcessedBundle:
    profile_master: pd.DataFrame
    education: pd.DataFrame
    certification: pd.DataFrame
    professional_experience: pd.DataFrame
    technical_contribution: pd.DataFrame


def load_linkedin_processed(
    paths: AnalysisPaths | None = None,
) -> LinkedInProcessedBundle:
    """Load the processed LinkedIn workbook's demographic/structural sheets.

    Deliberately does not load the `ALCSM_Score` sheet also present in
    this workbook: `Profile_Scores` in the researcher-review workbook
    is the canonical, actively-maintained source for ALCSM scores
    (`load_profile_scores`); `ALCSM_Score` here is a separate, static
    mirror that this loader does not assume stays in sync with it once
    the researcher starts recording review changes (see
    `Analysis_Preparation_Completion_Report.md` for this observation).
    """
    paths = paths or default_analysis_paths()
    path = _require(paths.linkedin_processed)
    return LinkedInProcessedBundle(
        profile_master=pd.read_excel(path, sheet_name="Profile_Master"),
        education=pd.read_excel(path, sheet_name="Education"),
        certification=pd.read_excel(path, sheet_name="Certification"),
        professional_experience=pd.read_excel(
            path, sheet_name="Professional_Experience"
        ),
        technical_contribution=pd.read_excel(path, sheet_name="Technical_Contribution"),
    )


@dataclass(frozen=True)
class JobPostingsBundle:
    job_master: pd.DataFrame
    requirements: pd.DataFrame


def load_job_postings_processed(
    paths: AnalysisPaths | None = None,
) -> JobPostingsBundle:
    """Load the processed job-postings workbook (`Job_Master` + `Requirements`)."""
    paths = paths or default_analysis_paths()
    path = _require(paths.job_postings_processed)
    return JobPostingsBundle(
        job_master=pd.read_excel(path, sheet_name="Job_Master"),
        requirements=pd.read_excel(path, sheet_name="Requirements"),
    )


# ---------------------------------------------------------------------
# Expert survey (Google Forms export, wide format -- see
# alcsm.analysis.survey for the reshape into tidy long format and the
# actual content-validity analysis; this loader only reads the raw
# sheet unmodified).
# ---------------------------------------------------------------------


def load_survey_raw(paths: AnalysisPaths | None = None) -> pd.DataFrame:
    """Load the raw expert-survey export exactly as received (wide
    format, one row per respondent, one column per question).

    This is genuinely raw survey data (real respondents, real free-
    text opinions in one column) -- callers must never print or log an
    entire row/column of this DataFrame. Use
    `alcsm.analysis.survey.reshape_survey_responses` for tidy,
    analysis-ready output that keeps free-text separate and clearly
    labelled.
    """
    paths = paths or default_analysis_paths()
    path = _require(paths.survey_responses)
    return pd.read_excel(path, sheet_name="Form responses 1")
