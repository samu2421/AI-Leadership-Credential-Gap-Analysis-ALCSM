"""In-memory types for the P4 annotation workflow.

These mirror ``alcsm_dimension_score`` and ``rater_ref`` closely enough
that :mod:`alcsm.annotation.store` can insert them directly, but they
are plain dataclasses, not ORM models -- the schema still owns
structure (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §8).

FIRST_PASS_SCORE vs FINAL_HUMAN_SCORE (critical rule, this phase):
    :class:`FirstPassReference` carries a read-only score produced by
    the AI-assisted first pass (``ALCSM_Full_FirstPass_Annotation_v1.1
    .xlsx`` / the researcher-review layer built on top of it). It is
    never written to ``alcsm_dimension_score`` and is not a
    ``rater_ref`` row -- the reliability framework (Krippendorff's
    alpha) is defined over independent HUMAN raters only, and mixing
    an AI-assisted draft into that pool would corrupt what the
    statistic means, not just violate a naming convention.

    :class:`AnnotationScore` is what a human rater submits through the
    P4 interface and is the only thing this module ever writes to the
    database, under a real ``rater_id`` (RATER_A / RATER_B /
    ADJUDICATOR -- see :mod:`alcsm.annotation.seed`).

    The two are never merged into one record type: a
    :class:`FirstPassReference` cannot be adjudicated, cannot carry a
    ``rater_id`` from ``rater_ref``, and is never accepted directly by
    :func:`alcsm.annotation.store.insert_annotation_score` without
    first being wrapped in a genuine :class:`AnnotationScore` that a
    human reviewer explicitly submitted (an ACCEPT decision still
    requires the reviewer to submit the score, per Human_Annotation_
    Review_Protocol_v1.1.md §5 -- acceptance is an action, not a
    default).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from alcsm.constants import DimensionCode, MissingStatus


class ReviewDecision(StrEnum):
    """The three outcomes Human_Annotation_Review_Protocol_v1.1.md §8 defines."""

    ACCEPT = "ACCEPT"
    CHANGE = "CHANGE"
    DEFER = "DEFER"


class RaterRole(StrEnum):
    """Matches ``rater_ref.rater_role``'s CHECK constraint exactly."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    ADJUDICATOR = "adjudicator"


# The literal rater_id the schema's ck_adjudication_role_alignment
# constraint requires whenever is_adjudication=TRUE (alcsm_schema_v1.0.1
# .sql, alcsm_dimension_score). Any other adjudicator rater_id is
# rejected by the database, not just discouraged.
ADJUDICATOR_RATER_ID = "ADJUDICATOR"


@dataclass(frozen=True)
class FirstPassReference:
    """A read-only AI-assisted first-pass score, shown for context only.

    Sourced from the researcher-review workbook
    (``06_Annotation/ALCSM_Final_Human_Annotation_v1.1_REVIEW.xlsx``),
    never from the database. Field names deliberately echo that
    workbook's ``Dimension_Evidence`` columns so the loader in
    :mod:`alcsm.annotation.first_pass_loader` can build one of these
    per profile x dimension with no renaming ambiguity.
    """

    profile_id: str
    dimension_number: int
    first_pass_score: int
    final_reviewed_score: int | None  # None if the researcher hasn't reviewed it yet
    evidence: str | None
    rationale: str | None
    missing_status: MissingStatus
    confidence: str  # "HIGH" / "MEDIUM" / "LOW", as recorded by the first pass
    review_required: bool


@dataclass(frozen=True)
class AnnotationScore:
    """One human rater's submitted score for one profile x dimension.

    The only type :func:`alcsm.annotation.store.insert_annotation_score`
    accepts. Field set mirrors ``alcsm_dimension_score`` (schema §"5.
    CORPUS 1"), minus server-assigned columns (``score_record_id``,
    ``created_ts``).
    """

    profile_id: str
    dimension_number: int
    rater_id: str
    score: int
    missing_status: MissingStatus
    rulebook_version: str
    coding_ts: datetime
    evidence_text: str | None = None
    ambiguity_flag: bool = False
    ambiguity_candidate_low: int | None = None
    ambiguity_candidate_high: int | None = None
    contradiction_flag: bool = False
    contradiction_text: str | None = None
    verification_used: bool = False
    verification_source: str | None = None
    verification_ts: datetime | None = None
    verification_outcome: str | None = (
        None  # 'confirmed'/'contradicted'/'not_confirmable'
    )
    precedent_applied: str | None = None
    alcsm_version: str = "1.0"
    taxonomy_version_id: str | None = None
    is_adjudication: bool = False
    notes: str | None = None


@dataclass(frozen=True)
class ReviewOutcome:
    """One row of Human_Annotation_Review_Protocol_v1.1.md's Review_Changes sheet.

    Produced only when a reviewer's decision is CHANGE -- an ACCEPT or
    DEFER never creates one of these (matches the review workbook's
    "Review_Changes ... populated only ... when the researcher changes
    the first-pass score" rule exactly).
    """

    profile_id: str
    dimension_number: int
    first_pass_score: int
    final_score: int
    change_reason: str
    governing_rule: str
    precedent: str | None
    reviewer: str
    review_date: datetime


@dataclass(frozen=True)
class D6IndustryBreadthDetail:
    """Structured D6 v1.1 evidence, mirroring D6_Quality_Review's columns.

    Kept separate from the generic :class:`AnnotationScore.evidence_text`
    so the annotation UI can render the industry list distinctly, per
    the task's "D6 breadth handling" requirement -- this is a display
    convenience, not a new database column (the schema stores D6 like
    every other dimension, in ``alcsm_dimension_score.evidence_text``;
    this dataclass is rendered into that text field, never stored
    separately).
    """

    profile_id: str
    ai_related_industry_count: int
    normalized_industries: tuple[str, ...]
    zero_ai_industries: bool
    missing_industry_partial: bool
    ambiguous_industry_label: bool
    duplicate_normalization_collapsed: bool
    potential_d3_d6_overlap: bool
    unusually_high_breadth: bool

    def as_evidence_text(self) -> str:
        """Render a verbatim-style evidence string for ``evidence_text``.

        Matches the wording pattern ``ALCSM_Full_FirstPass_Annotation_
        v1.1.xlsx``'s ``D6_Industry_Detail.D6_Rationale`` already uses,
        so a human reviewer sees a familiar shape.
        """
        industries = "; ".join(self.normalized_industries) or "none"
        return (
            f"{self.ai_related_industry_count} distinct normalized industry/"
            f"application domain(s) among AI_Related=Yes records: {industries}. "
            "D6 score = min(count, 5)."
        )


@dataclass(frozen=True)
class ProfileForAnnotation:
    """Everything the annotation UI needs to render one profile's six dimensions.

    Assembled by the caller (fixtures for a dry run; a real loader once
    P2/P3 clear) -- this module does not know where the data came from.
    """

    profile_id: str
    dimension_codes: dict[int, DimensionCode]
    first_pass: dict[int, FirstPassReference] = field(default_factory=dict)
    d6_detail: D6IndustryBreadthDetail | None = None
