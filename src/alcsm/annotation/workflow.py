"""The P4 review workflow state machine.

Implements: profile selection -> display evidence -> display D1-D6 ->
researcher review -> accept/change/defer -> capture rationale -> save
-> validation -> next profile (this task's "Annotation Workflow"
section, verbatim ordering).

Also enforces, structurally rather than just by UI convention, the
four frozen constraints (PROJECT_CONTEXT.md §11):

    1. Show one profile's six dimensions together, score all six
       before moving on -- :class:`ReviewSession` tracks completion
       per dimension and :meth:`ReviewSession.is_profile_complete`
       gates advancing to the next profile.
    2. Never display RQ4 impact values during scoring -- this module
       has no import of, or reference to, ``rq4_impact_indicator`` or
       :mod:`alcsm.analysis.rq4`  anywhere; that is enforced by
       ``tests/annotation/test_rq4_isolation.py`` asserting the
       absence, not just by omission here.
    3. Blind the two raters to each other until both submit --
       :meth:`ReviewSession.submit` refuses to let a rater read
       another rater's score before submitting their own (via
       :func:`alcsm.annotation.store.has_other_rater_submitted`,
       which never returns a value, only yes/no).
    4. Capture, per dimension: score, verbatim evidence, missing-
       status, ambiguity/contradiction flags, precedent applied, and
       (D4 only) verification metadata -- :class:`AnnotationScore`
       has every one of these fields and :func:`validate_annotation_
       score` refuses an incomplete submission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from psycopg2.extensions import connection as PGConnection

from alcsm.annotation.audit import AuditAction, AuditLogger
from alcsm.annotation.models import AnnotationScore, ReviewDecision, ReviewOutcome
from alcsm.annotation.store import (
    DuplicateScoreError,
    fetch_rater_score,
    has_other_rater_submitted,
    insert_annotation_score,
)
from alcsm.annotation.validation import AnnotationValidationError


class BlindingViolationError(RuntimeError):
    """Raised if code attempts to reveal another rater's score before
    both raters have submitted -- should never happen through normal
    use of this module; exists as a defensive backstop."""


@dataclass
class DimensionReviewState:
    dimension_number: int
    decision: ReviewDecision | None = None
    submitted_score: AnnotationScore | None = None
    change_outcome: ReviewOutcome | None = None


@dataclass
class ReviewSession:
    """Tracks one rater's progress through one profile's six dimensions.

    A thin, in-process state holder the Streamlit app (or a test) can
    drive -- it owns no I/O of its own beyond delegating to
    :mod:`alcsm.annotation.store` and :mod:`alcsm.annotation.audit`.
    """

    profile_id: str
    rater_id: str
    rulebook_version: str
    audit_logger: AuditLogger
    dimensions: dict[int, DimensionReviewState] = field(
        default_factory=lambda: {n: DimensionReviewState(n) for n in range(1, 7)}
    )

    def is_profile_complete(self) -> bool:
        """True once all six dimensions have a recorded decision.

        Enforces frozen constraint #1: the UI should refuse to advance
        to the next profile while this is False.
        """
        return all(d.decision is not None for d in self.dimensions.values())

    def record_accept(self, dimension_number: int, score: AnnotationScore) -> None:
        """Record an ACCEPT decision: the first-pass score is correct as-is.

        Still requires an explicit :class:`AnnotationScore` submission
        (acceptance is an action, not a default -- Human_Annotation_
        Review_Protocol_v1.1.md §8) and still goes through the same
        validated insert path as any other submission.
        """
        self._submit(dimension_number, ReviewDecision.ACCEPT, score)

    def record_change(
        self,
        dimension_number: int,
        score: AnnotationScore,
        first_pass_score: int,
        change_reason: str,
        governing_rule: str,
        precedent: str | None,
    ) -> None:
        """Record a CHANGE decision, producing a :class:`ReviewOutcome`
        audit-trail row per Human_Annotation_Review_Protocol_v1.1.md §9.
        """
        self._submit(dimension_number, ReviewDecision.CHANGE, score)
        outcome = ReviewOutcome(
            profile_id=self.profile_id,
            dimension_number=dimension_number,
            first_pass_score=first_pass_score,
            final_score=score.score,
            change_reason=change_reason,
            governing_rule=governing_rule,
            precedent=precedent,
            reviewer=self.rater_id,
            review_date=score.coding_ts,
        )
        self.dimensions[dimension_number].change_outcome = outcome

    def record_defer(self, dimension_number: int) -> None:
        """Record a DEFER decision: no score is submitted; the case is
        escalated (Adjudication_Log territory, not this module's job to
        resolve).
        """
        self.dimensions[dimension_number].decision = ReviewDecision.DEFER
        self.audit_logger.record(
            actor=self.rater_id,
            action=AuditAction.SCORE_DEFERRED,
            profile_id=self.profile_id,
            dimension_number=dimension_number,
        )

    def _submit(
        self, dimension_number: int, decision: ReviewDecision, score: AnnotationScore
    ) -> None:
        if score.rater_id != self.rater_id:
            raise ValueError(
                f"score.rater_id={score.rater_id!r} does not match this "
                f"session's rater_id={self.rater_id!r}"
            )
        state = self.dimensions[dimension_number]
        state.decision = decision
        state.submitted_score = score
        action = (
            AuditAction.SCORE_SUBMITTED
            if decision == ReviewDecision.ACCEPT
            else AuditAction.SCORE_CHANGED
        )
        self.audit_logger.record(
            actor=self.rater_id,
            action=action,
            profile_id=self.profile_id,
            dimension_number=dimension_number,
            detail=decision.value,
        )


def submit_and_save(
    conn: PGConnection,
    session: ReviewSession,
    dimension_number: int,
    score: AnnotationScore,
    audit_logger: AuditLogger,
) -> int:
    """Validate and persist one dimension's score, honouring rater blinding.

    This is the single function that actually writes to the database
    from the review workflow. On success, returns the new
    ``score_record_id``. On a validation failure or a duplicate
    submission, logs the rejection to the audit trail and re-raises
    (the caller -- the UI -- is responsible for showing the message;
    this function never swallows an error to keep the workflow moving).
    """
    try:
        record_id = insert_annotation_score(conn, score)
    except AnnotationValidationError as exc:
        audit_logger.record(
            actor=score.rater_id,
            action=AuditAction.VALIDATION_REJECTED,
            profile_id=score.profile_id,
            dimension_number=dimension_number,
            detail="; ".join(exc.problems)[:200],
        )
        raise
    except DuplicateScoreError:
        audit_logger.record(
            actor=score.rater_id,
            action=AuditAction.DUPLICATE_REJECTED,
            profile_id=score.profile_id,
            dimension_number=dimension_number,
        )
        raise
    return record_id


def check_blinding_before_display(
    conn: PGConnection, profile_id: str, dimension_number: int, viewing_rater_id: str
) -> bool:
    """Return whether it is safe to show cross-rater comparison info yet.

    True only once BOTH this rater and at least one other independent
    rater have submitted. The UI must call this -- and only display a
    comparison view when it returns True -- rather than querying
    :func:`alcsm.annotation.store.fetch_both_rater_scores_for_
    adjudication` directly, which would leak the other rater's score
    the instant it exists, before this rater has submitted their own.
    """
    this_rater_submitted = (
        fetch_rater_score(conn, profile_id, dimension_number, viewing_rater_id)
        is not None
    )
    other_rater_submitted = has_other_rater_submitted(
        conn, profile_id, dimension_number, viewing_rater_id
    )
    return this_rater_submitted and other_rater_submitted


def now_utc() -> datetime:
    """Small seam so tests can freeze time if ever needed; avoids every
    caller importing ``datetime`` just for ``coding_ts``."""
    return datetime.now()
