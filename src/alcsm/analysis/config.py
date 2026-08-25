"""Shared configuration and data-provenance labeling for RQ1-RQ5 analysis.

Every top-level analysis function in this package returns a result
whose first field is an :class:`AnalysisRunMetadata` carrying a
``data_status``. This is the structural mechanism behind this
project's explicit "use synthetic fixtures or clearly labelled
provisional input data for testing" rule: nothing computed by this
package can be presented without a visible, load-bearing label of
where its input came from and whether that input is final.

This module also defines the one deliberate gate in the whole
package: :func:`require_frozen_or_acknowledge_provisional`. It exists
because the researcher's final human review of the 500-profile
first-pass annotation was still in progress when this package was
built (`06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx`
`Profile_Scores.Overall_Review_Status` still shows `Pending Review`
for a majority of profiles as of this writing) — every RQ1/RQ2/RQ5
function that consumes profile-level ALCSM scores calls this gate
before proceeding, so a caller can never accidentally treat
still-under-review scores as final without explicitly saying so.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

DataStatus = Literal[
    "synthetic_fixture",
    "provisional_first_pass",
    "final_frozen",
]


@dataclass(frozen=True)
class AnalysisRunMetadata:
    """Carried by every RQ1-RQ5 result. Never optional, never inferred
    silently -- the caller states it, or a loader infers it from an
    explicit, checkable signal (e.g. `Overall_Review_Status`), never
    from a guess."""

    data_status: DataStatus
    source_description: str
    run_ts: datetime


def make_metadata(
    data_status: DataStatus, source_description: str
) -> AnalysisRunMetadata:
    return AnalysisRunMetadata(
        data_status=data_status,
        source_description=source_description,
        run_ts=datetime.now(),
    )


class DataNotFrozenError(RuntimeError):
    """Raised by :func:`require_frozen_or_acknowledge_provisional` when
    profile-level scores are still under researcher review and the
    caller has not explicitly acknowledged that."""


def require_frozen_or_acknowledge_provisional(
    data_status: DataStatus, *, acknowledge_provisional: bool
) -> None:
    """The one enforcement point behind "do not freeze current scores"
    and "do not produce final thesis findings".

    Call this at the top of any function that is about to compute a
    result intended for interpretation (not just a unit test). If
    ``data_status`` is ``"provisional_first_pass"`` and the caller has
    not passed ``acknowledge_provisional=True``, raises
    :class:`DataNotFrozenError` with a message naming exactly what is
    missing. ``"final_frozen"`` and ``"synthetic_fixture"`` always pass
    silently -- a fixture is never mistaken for a real finding by this
    gate (that is `AnalysisRunMetadata.data_status` itself doing its
    job when the result is displayed), and "final_frozen" is, by
    definition, an explicit author/researcher decision made elsewhere
    (a `DECISION_LOG.md` entry), not something this function judges.
    """
    if data_status == "provisional_first_pass" and not acknowledge_provisional:
        raise DataNotFrozenError(
            "Profile-level ALCSM scores are still under researcher review "
            "(data_status='provisional_first_pass'). This function requires "
            "acknowledge_provisional=True to run against provisional data, "
            "and the result will be labelled provisional regardless -- it "
            "must never be reported as a final thesis finding."
        )


def infer_profile_scores_status(overall_review_status: Iterable[object]) -> DataStatus:
    """Infer ``data_status`` from a `Profile_Scores.Overall_Review_Status`
    column (or an equivalent Series/iterable of its values).

    Returns ``"provisional_first_pass"`` if any value is still
    ``"Pending Review"`` (the review workbook's own convention, see
    `Human_Annotation_Review_Protocol_v1.1.md` §4), else
    ``"final_frozen"``. This is a structural signal check, not a
    judgement call -- it never consults anything outside the column
    itself, and it does not itself constitute a freeze decision (a
    freeze is an author action recorded in `DECISION_LOG.md`; this
    function only reports what the data currently shows).
    """
    values = list(overall_review_status)
    if any(v == "Pending Review" for v in values):
        return "provisional_first_pass"
    return "final_frozen"


@dataclass(frozen=True)
class AnalysisPaths:
    """File locations every RQ module's loaders read from. All are
    git-ignored, real-data-bearing paths except where noted -- see
    each field's comment for the exact source."""

    repo_root: Path
    review_workbook: Path  # 06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx
    linkedin_processed: Path  # 05_Data_Collection/LinkedIn_Profiles/02_Processed/...
    job_postings_processed: Path  # 05_Data_Collection/Job_Postings/02_Processed/...
    survey_responses: Path  # 07_Reliability/Survey_Responses/01_Raw/...


def default_analysis_paths() -> AnalysisPaths:
    root = Path(__file__).resolve().parents[3]
    return AnalysisPaths(
        repo_root=root,
        review_workbook=root
        / "06_Annotation"
        / "ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx",
        linkedin_processed=root
        / "05_Data_Collection"
        / "LinkedIn_Profiles"
        / "02_Processed"
        / "ALCSM_LinkedIn_Processed_v1.1.xlsx",
        job_postings_processed=root
        / "05_Data_Collection"
        / "Job_Postings"
        / "02_Processed"
        / "ALCSM_JobPosting_Processed_v1.1.xlsx",
        survey_responses=root
        / "07_Reliability"
        / "Survey_Responses"
        / "01_Raw"
        / "ALCSM_Expert_Survey_Responses_v1.0.xlsx",
    )


# Reliability decision thresholds -- frozen (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
# §16 item 9; PROJECT_CONTEXT.md §48). Never redefine these per-call; a
# caller who wants different thresholds is making a methodology
# decision that belongs in a DECISION_LOG entry, not a function
# argument.
KRIPPENDORFF_MINIMUM_ACCEPTABLE = 0.667
KRIPPENDORFF_TARGET = 0.80
