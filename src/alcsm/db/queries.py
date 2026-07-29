"""Read queries over the five frozen views.

Every function here must read through the named view — never
reconstruct the equivalent logic against base tables
(PROJECT_CONTEXT.md §16). Not implemented yet: these are P0 skeletons
only; filling them in is later-phase work (reliability → P5, analysis
→ P8, NLP evaluation → P7), once real data and a deployed schema
exist.

Views these functions must eventually read through, and never bypass:
    v_reliability_input          reliability/krippendorff.py (P5)
    v_final_profile_score        gold-standard lookups (P5+)
    v_profile_completeness       completeness index (P5+)
    v_credential_gap_by_dimension  analysis/gap.py (P8)
    v_nlp_evaluation              nlp/evaluate.py (P7)
"""

from __future__ import annotations

from sqlalchemy.orm import Session


def fetch_reliability_input(session: Session) -> list:
    """Read `v_reliability_input` (pre-adjudication, independent rows only).

    TODO (Phase P5): implement once reliability computation begins.
    Must query `v_reliability_input` directly — never the base
    `alcsm_dimension_score` table (PROJECT_CONTEXT.md §16, §27).
    """
    raise NotImplementedError("Implemented in Phase P5 (reliability).")


def fetch_final_profile_scores(session: Session) -> list:
    """Read `v_final_profile_score` (adjudicated value wins where present).

    TODO (Phase P5+): implement once a gold standard exists.
    """
    raise NotImplementedError("Implemented in Phase P5+ (gold standard).")


def fetch_profile_completeness(session: Session) -> list:
    """Read `v_profile_completeness` (informative dimensions / 6).

    TODO (Phase P5+): implement. Denominator is always 6 — see the
    F-01 bug this view fixes (PROJECT_CONTEXT.md §9, §16).
    """
    raise NotImplementedError("Implemented in Phase P5+.")


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
