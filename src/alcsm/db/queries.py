"""Read queries over the five frozen views.

Every function here must read through the named view — never
reconstruct the equivalent logic against base tables
(PROJECT_CONTEXT.md §16).

``fetch_reliability_input``, ``fetch_final_profile_scores``, and
``fetch_profile_completeness`` are implemented as part of Phase P4
(the annotation interface needs progress tracking via
``v_profile_completeness`` and reliability export scaffolding via
``v_reliability_input`` — see ``alcsm.annotation.reliability_export``).
This is read-only plumbing over already-frozen views; it does not
compute or interpret reliability, which remains Phase P5's job
(``alcsm.reliability.krippendorff``, still unimplemented, gated on P4
pilot data existing).

``fetch_credential_gap_by_dimension`` and ``fetch_nlp_evaluation``
remain P7/P8 skeletons, unrelated to annotation.

Views these functions read through, and never bypass:
    v_reliability_input            alcsm.annotation.reliability_export
                                    (P4 export), P5 (alpha)
    v_final_profile_score          gold-standard lookups
                                    (P4+ progress tracking, P5+)
    v_profile_completeness         completeness index
                                    (P4 progress tracking, P5+)
    v_credential_gap_by_dimension  analysis/gap.py (P8)
    v_nlp_evaluation                nlp/evaluate.py (P7)
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class ReliabilityInputRecord:
    """One row of ``v_reliability_input``."""

    unit_id: str
    corpus: str
    dimension_number: int
    rater_id: str
    score: int
    rulebook_version: str


@dataclass(frozen=True)
class FinalProfileScoreRecord:
    """One row of ``v_final_profile_score``."""

    profile_id: str
    dimension_number: int
    score: int
    missing_status: str
    ambiguity_flag: bool
    contradiction_flag: bool
    from_adjudication: bool
    rulebook_version: str
    alcsm_version: str


@dataclass(frozen=True)
class ProfileCompletenessRecord:
    """One row of ``v_profile_completeness``."""

    profile_id: str
    completeness_index: float
    dimensions_scored: int
    coding_complete: bool


def fetch_reliability_input(session: Session) -> list[ReliabilityInputRecord]:
    """Read `v_reliability_input` (pre-adjudication, independent rows only).

    Must query `v_reliability_input` directly — never the base
    `alcsm_dimension_score` table (PROJECT_CONTEXT.md §16, §27). Used
    by :mod:`alcsm.annotation.reliability_export` to shape export rows;
    does not itself compute alpha (Phase P5's job).
    """
    rows = session.execute(
        text(
            "SELECT unit_id, corpus, dimension_number, rater_id, score, "
            "rulebook_version FROM alcsm.v_reliability_input"
        )
    ).all()
    return [
        ReliabilityInputRecord(
            unit_id=r.unit_id,
            corpus=r.corpus,
            dimension_number=r.dimension_number,
            rater_id=r.rater_id,
            score=r.score,
            rulebook_version=r.rulebook_version,
        )
        for r in rows
    ]


def fetch_final_profile_scores(session: Session) -> list[FinalProfileScoreRecord]:
    """Read `v_final_profile_score` (adjudicated value wins where present).

    Used for P4 progress tracking (what has a final score already) and
    as the future P5+ gold-standard source. No composite is computed
    here or anywhere downstream of this function without an explicit,
    labelled aggregation choice (schema comment on the view itself:
    "No composite is produced: aggregation remains OPEN").
    """
    rows = session.execute(
        text(
            "SELECT profile_id, dimension_number, score, missing_status, "
            "ambiguity_flag, contradiction_flag, from_adjudication, "
            "rulebook_version, alcsm_version FROM alcsm.v_final_profile_score"
        )
    ).all()
    return [
        FinalProfileScoreRecord(
            profile_id=r.profile_id,
            dimension_number=r.dimension_number,
            score=r.score,
            missing_status=r.missing_status,
            ambiguity_flag=r.ambiguity_flag,
            contradiction_flag=r.contradiction_flag,
            from_adjudication=r.from_adjudication,
            rulebook_version=r.rulebook_version,
            alcsm_version=r.alcsm_version,
        )
        for r in rows
    ]


def fetch_profile_completeness(session: Session) -> list[ProfileCompletenessRecord]:
    """Read `v_profile_completeness` (informative dimensions / 6).

    Denominator is always 6 — see the F-01 bug this view fixes
    (PROJECT_CONTEXT.md §9, §16). Used by the P4 interface's progress
    tracker.
    """
    rows = session.execute(
        text(
            "SELECT profile_id, completeness_index, dimensions_scored, "
            "coding_complete FROM alcsm.v_profile_completeness"
        )
    ).all()
    return [
        ProfileCompletenessRecord(
            profile_id=r.profile_id,
            completeness_index=float(r.completeness_index),
            dimensions_scored=r.dimensions_scored,
            coding_complete=r.coding_complete,
        )
        for r in rows
    ]


def fetch_credential_gap_by_dimension(session: Session) -> list:
    """Read `v_credential_gap_by_dimension` (mean required - mean held).

    TODO (Phase P8): implement for RQ2. Must exclude
    `not_applicable`/`unavailable`, never treat silence as zero
    (PROJECT_CONTEXT.md §9, §16, §27).
    """
    raise NotImplementedError("Implemented in Phase P8 (analysis/gap.py).")


def fetch_nlp_evaluation(session: Session) -> list:
    """Read `v_nlp_evaluation` (predictions joined to the gold standard).

    TODO (Phase P7): implement for RQ5 evaluation.
    """
    raise NotImplementedError("Implemented in Phase P7 (nlp/evaluate.py).")
