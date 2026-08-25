"""Reference-data seeding for the two tables the DDL does not pre-populate.

``dimension_ref`` and ``missing_status_ref`` are seeded directly inside
``alcsm_schema_v1.0.1.sql`` (``INSERT INTO ... VALUES`` right in the
DDL). ``rater_ref`` and ``precedent_ref`` are not -- PROJECT_CONTEXT.md
§12 says the fifteen precedent rulings are "load[ed] ... during Phase
P0", but no seed script existed anywhere in the repository before this
module. The P4 annotation write path cannot function without both
(``alcsm_dimension_score.rater_id`` and ``.precedent_applied`` are
foreign keys to them), so seeding them is necessary P4-adjacent
plumbing, not scope creep -- it unblocks the FK, nothing more.

Precedent text is copied verbatim from PROJECT_CONTEXT.md §12 (the
"real text" the guide requires, not a placeholder) -- never
paraphrased and never invented here (PROJECT_CONTEXT.md §12: "Do not
invent new precedents in code; new precedents are a research decision
made by the author through the revision log").
"""

from __future__ import annotations

from psycopg2.extensions import connection as PGConnection

from alcsm.annotation.models import ADJUDICATOR_RATER_ID, RaterRole
from alcsm.logging_config import get_logger

logger = get_logger(__name__)

# rater_id, rater_role, blind_to_hypotheses, notes.
# RATER_A/RATER_B are the two independent raters (P4 pilot, P6 main
# coding); ADJUDICATOR is the literal id the schema's
# ck_adjudication_role_alignment constraint requires whenever
# is_adjudication=TRUE -- not a free choice.
_RATERS: tuple[tuple[str, RaterRole, bool, str], ...] = (
    ("RATER_A", RaterRole.PRIMARY, True, "Primary independent rater."),
    ("RATER_B", RaterRole.SECONDARY, True, "Secondary independent rater."),
    (
        ADJUDICATOR_RATER_ID,
        RaterRole.ADJUDICATOR,
        False,
        "Resolves disagreements per ALCSM_Coding_Rulebook_and_Pilot_Design.md §1.5.",
    ),
)

# precedent_id, situation, binding_ruling -- verbatim from PROJECT_CONTEXT.md §12.
_PRECEDENTS: tuple[tuple[str, str, str], ...] = (
    (
        "P-01",
        "Field on a taxonomy tier boundary",
        "Default-low; flag ambiguity; escalate only if raters differ",
    ),
    (
        "P-02",
        '"Head of X" with no scope language',
        "Score Director-equivalent (Tier 3), not VP (Tier 4)",
    ),
    (
        "P-03",
        "Senior title, nothing substantiating it",
        "Title alone must not push D5 above 2; set contradiction flag",
    ),
    (
        "P-04",
        "Strong tech, low certs/leadership/engagement",
        "Score honestly; no positive halo; keep the lows",
    ),
    (
        "P-05",
        "Substantiated leader, thin technical depth",
        "High D5 with low D4 is legitimate -- not a contradiction",
    ),
    ("P-06", "Certification from an unrecognised issuer", "Low-credibility tier"),
    (
        "P-07",
        "Long career, short AI-specific tenure",
        "Score D3 on AI-relevant experience only",
    ),
    (
        "P-08",
        "Adjacent-field expert (data eng., general SWE)",
        "Adjacent band for D3; resist halo",
    ),
    (
        "P-09",
        "Keyword-stuffed profile, no substance",
        "Ontology locates, never scores; flag contradiction",
    ),
    (
        "P-10",
        "Headline claim contradicts dated experience",
        "Prefer dated evidence; flag contradiction",
    ),
    (
        "P-11",
        "Non-English / untranslatable credential",
        "Map if defensible, else default-low, log verbatim",
    ),
    (
        "P-12",
        "One artefact evidences two dimensions",
        "Each dimension on its own criterion; no double-inflation",
    ),
    (
        "P-13",
        "Stated absence vs missing",
        "absent_stated (score it) vs unavailable (missing)",
    ),
    (
        "P-14",
        "Profile-provided link",
        "Within-profile evidence (any dim); web search is D4-only",
    ),
    (
        "P-15",
        "Verification reveals an overstated claim",
        "May lower (D4 only), never raise above the text",
    ),
)


def seed_rater_ref(conn: PGConnection) -> int:
    """Insert RATER_A/RATER_B/ADJUDICATOR if not already present.

    Idempotent (``ON CONFLICT DO NOTHING``), matching
    ``create_sampling_batch``'s pattern. Returns the number of rows
    actually inserted.
    """
    cur = conn.cursor()
    inserted = 0
    try:
        for rater_id, role, blind, notes in _RATERS:
            cur.execute(
                """
                INSERT INTO alcsm.rater_ref
                  (rater_id, rater_role, blind_to_hypotheses, notes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (rater_id) DO NOTHING;
                """,
                (rater_id, role.value, blind, notes),
            )
            inserted += cur.rowcount
        conn.commit()
        logger.info("rater_ref seed: %d row(s) inserted", inserted)
        return inserted
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()


def seed_precedent_ref(conn: PGConnection) -> int:
    """Insert P-01..P-15 with their real ruling text if not already present.

    Idempotent. Returns the number of rows actually inserted.
    """
    cur = conn.cursor()
    inserted = 0
    try:
        for precedent_id, situation, ruling in _PRECEDENTS:
            cur.execute(
                """
                INSERT INTO alcsm.precedent_ref
                  (precedent_id, situation, binding_ruling, introduced_in_version)
                VALUES (%s, %s, %s, '1.0')
                ON CONFLICT (precedent_id) DO NOTHING;
                """,
                (precedent_id, situation, ruling),
            )
            inserted += cur.rowcount
        conn.commit()
        logger.info("precedent_ref seed: %d row(s) inserted", inserted)
        return inserted
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()


def seed_reference_data(conn: PGConnection) -> None:
    """Seed both reference tables the P4 write path depends on."""
    seed_rater_ref(conn)
    seed_precedent_ref(conn)
