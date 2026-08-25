"""Pre-database validation for annotation scores.

Every rule here mirrors a CHECK constraint already in
``alcsm_schema_v1.0.1.sql`` (``alcsm_dimension_score``) -- this module
exists so a reviewer gets a readable message in the interface instead
of a raw ``psycopg2.errors.CheckViolation`` traceback (CLAUDE_CODE_
IMPLEMENTATION_GUIDE.md §13: "Surface readable messages, not raw
tracebacks, to end users"). The database constraints remain the final
authority; this module is a friendlier first gate, not a replacement.

Mirrors the "never write test assertions against the implementation"
caution (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §11): every check below
cites the exact schema constraint it mirrors, so a schema change is
the only thing that can silently invalidate a check here.
"""

from __future__ import annotations

from alcsm.annotation.models import AnnotationScore
from alcsm.constants import MISSING_STATUSES, SCORE_MAX, SCORE_MIN

_EXTERNAL_VERIFICATION_DIMENSION_NUMBER = (
    4  # d4_contributions, PROJECT_CONTEXT.md §10, §17
)

_VALID_VERIFICATION_OUTCOMES = ("confirmed", "contradicted", "not_confirmable")


class AnnotationValidationError(ValueError):
    """Raised with every rule violation found, never just the first one."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("; ".join(problems))


def validate_annotation_score(record: AnnotationScore) -> list[str]:
    """Return every rule violation found in ``record`` (empty if valid).

    Mirrors, in order, these ``alcsm_dimension_score`` CHECK constraints:
    ``score BETWEEN 0 AND 5``; ``missing_status`` FK to
    ``missing_status_ref``; ``ck_evidence_when_present``;
    ``ck_unavailable_scores_zero``; ``ck_unavailable_has_no_evidence``;
    ``ck_absent_stated_needs_evidence``; ``ck_profile_not_applicable``;
    ``ck_verification_d4_only``; ``ck_verification_metadata``;
    ``ck_ambiguity_metadata``; ``ck_ambiguity_brackets_score``;
    ``ck_contradiction_metadata``;
    ``ck_adjudication_role_alignment``/``ADJUDICATOR_RATER_ID``;
    ``dimension_number BETWEEN 1 AND 6``.
    """
    errs: list[str] = []

    if not (SCORE_MIN <= record.score <= SCORE_MAX):
        errs.append(
            f"score must be between {SCORE_MIN} and {SCORE_MAX}, got {record.score}"
        )

    if not (1 <= record.dimension_number <= 6):
        errs.append(
            f"dimension_number must be between 1 and 6, got {record.dimension_number}"
        )

    if record.missing_status not in MISSING_STATUSES:
        errs.append(
            f"missing_status {record.missing_status!r} not in controlled "
            f"vocabulary {MISSING_STATUSES}"
        )

    # not_applicable is a posting-side state only (ck_profile_not_applicable).
    if record.missing_status == "not_applicable":
        errs.append(
            "missing_status='not_applicable' is never valid for a profile "
            "score (posting-side state only, ck_profile_not_applicable)"
        )

    # A 'present' score must cite evidence (ck_evidence_when_present).
    if record.missing_status == "present" and not record.evidence_text:
        errs.append(
            "missing_status='present' requires evidence_text "
            "(ck_evidence_when_present -- no span, no score)"
        )

    # 'absent_stated' is a positive textual claim: must be evidenced too
    # (ck_absent_stated_needs_evidence, P-13).
    if record.missing_status == "absent_stated" and not record.evidence_text:
        errs.append(
            "missing_status='absent_stated' requires evidence_text "
            "(ck_absent_stated_needs_evidence -- P-13: stated absence is "
            "evidenced, unlike a genuine gap)"
        )

    # 'unavailable' means no evidence found: none may be stored, and the
    # frozen convention is score=0 (ck_unavailable_has_no_evidence,
    # ck_unavailable_scores_zero).
    if record.missing_status == "unavailable":
        if record.evidence_text:
            errs.append(
                "missing_status='unavailable' must not carry evidence_text "
                "(ck_unavailable_has_no_evidence)"
            )
        if record.score != 0:
            errs.append(
                "missing_status='unavailable' requires score=0 "
                "(ck_unavailable_scores_zero)"
            )

    # External verification permitted for D4 only (ck_verification_d4_only).
    if (
        record.verification_used
        and record.dimension_number != _EXTERNAL_VERIFICATION_DIMENSION_NUMBER
    ):
        errs.append(
            "verification_used=True is only permitted for dimension 4 "
            "(d4_contributions, ck_verification_d4_only)"
        )

    # Verification metadata required exactly when verification_used=True
    # (ck_verification_metadata).
    verification_fields = (
        record.verification_source,
        record.verification_ts,
        record.verification_outcome,
    )
    if record.verification_used:
        if any(f is None for f in verification_fields):
            errs.append(
                "verification_used=True requires verification_source, "
                "verification_ts, and verification_outcome all set "
                "(ck_verification_metadata)"
            )
        if (
            record.verification_outcome is not None
            and record.verification_outcome not in _VALID_VERIFICATION_OUTCOMES
        ):
            errs.append(
                f"verification_outcome must be one of {_VALID_VERIFICATION_OUTCOMES}"
            )
    elif any(f is not None for f in verification_fields):
        errs.append(
            "verification_used=False requires verification_source, "
            "verification_ts, and verification_outcome all unset "
            "(ck_verification_metadata)"
        )

    # Ambiguity candidates required exactly when ambiguity_flag=True, and
    # low <= high (ck_ambiguity_metadata, ck_ambiguity_brackets_score).
    if record.ambiguity_flag:
        if (
            record.ambiguity_candidate_low is None
            or record.ambiguity_candidate_high is None
        ):
            errs.append(
                "ambiguity_flag=True requires both ambiguity_candidate_low "
                "and ambiguity_candidate_high (ck_ambiguity_metadata)"
            )
        elif record.ambiguity_candidate_low > record.ambiguity_candidate_high:
            errs.append("ambiguity_candidate_low must be <= ambiguity_candidate_high")
        elif not (
            record.ambiguity_candidate_low
            <= record.score
            <= record.ambiguity_candidate_high
        ):
            errs.append(
                "score must lie within [ambiguity_candidate_low, "
                "ambiguity_candidate_high] when ambiguity_flag=True "
                "(ck_ambiguity_brackets_score)"
            )
    elif (
        record.ambiguity_candidate_low is not None
        or record.ambiguity_candidate_high is not None
    ):
        errs.append(
            "ambiguity_flag=False requires ambiguity_candidate_low/high "
            "both unset (ck_ambiguity_metadata)"
        )

    # Contradiction text required exactly when contradiction_flag=True
    # (ck_contradiction_metadata).
    if record.contradiction_flag and not record.contradiction_text:
        errs.append(
            "contradiction_flag=True requires contradiction_text "
            "(ck_contradiction_metadata)"
        )
    if not record.contradiction_flag and record.contradiction_text:
        errs.append(
            "contradiction_flag=False requires contradiction_text unset "
            "(ck_contradiction_metadata)"
        )

    # Adjudicator rater_id/is_adjudication alignment
    # (ck_adjudication_role_alignment).
    if record.is_adjudication and record.rater_id != "ADJUDICATOR":
        errs.append(
            "is_adjudication=True requires rater_id='ADJUDICATOR' "
            "(ck_adjudication_role_alignment)"
        )
    if not record.is_adjudication and record.rater_id == "ADJUDICATOR":
        errs.append(
            "rater_id='ADJUDICATOR' requires is_adjudication=True "
            "(ck_adjudication_role_alignment)"
        )

    if not record.profile_id:
        errs.append("profile_id is required")
    if not record.rater_id:
        errs.append("rater_id is required")
    if not record.rulebook_version:
        errs.append("rulebook_version is required")
    if not record.coding_ts:
        errs.append("coding_ts is required")

    return errs


def validate_evidence_is_supported(
    evidence_text: str | None, source_section_text: str | None
) -> list[str]:
    """Reject an evidence claim that is not a substring of its cited source.

    Enforces "no unsupported evidence claims" (this task's explicit
    workflow rule) and the rulebook's "quote, don't paraphrase"
    principle (PROJECT_CONTEXT.md §10) at the structural level this
    module can check: the quoted text must actually appear in the
    section it is claimed to come from. This cannot verify semantic
    accuracy (that a quote genuinely supports the assigned score) --
    that judgement remains the reviewer's, per the annotation
    handbook. ``source_section_text=None`` means "not checked against
    a source" (e.g. a D6 breadth summary derived from structured
    fields, not a raw text span) and is not itself an error.
    """
    if evidence_text is None or source_section_text is None:
        return []
    if evidence_text.strip() and evidence_text not in source_section_text:
        return [
            "evidence_text is not a verbatim substring of the cited source "
            "section (quote, don't paraphrase -- PROJECT_CONTEXT.md §10)"
        ]
    return []
