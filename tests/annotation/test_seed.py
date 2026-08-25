"""Reference-data seeding: rater_ref (3 rows) and precedent_ref (15 rows,
real ruling text), idempotent."""

from __future__ import annotations

import psycopg2

from alcsm.annotation.seed import (
    seed_precedent_ref,
    seed_rater_ref,
    seed_reference_data,
)


def test_seed_rater_ref_inserts_exactly_three_roles(
    db_connection: psycopg2.extensions.connection,
) -> None:
    # seeded_reference_data (autouse, session-scoped) already ran once;
    # re-running here must find 0 new rows (idempotent), not error.
    inserted = seed_rater_ref(db_connection)
    assert inserted == 0

    cur = db_connection.cursor()
    cur.execute("SELECT rater_id, rater_role FROM alcsm.rater_ref ORDER BY rater_id;")
    rows = dict(cur.fetchall())
    cur.close()
    assert rows == {
        "ADJUDICATOR": "adjudicator",
        "RATER_A": "primary",
        "RATER_B": "secondary",
    }


def test_seed_precedent_ref_has_all_fifteen_with_real_text(
    db_connection: psycopg2.extensions.connection,
) -> None:
    inserted = seed_precedent_ref(db_connection)
    assert inserted == 0  # already seeded by the session-scoped autouse fixture

    cur = db_connection.cursor()
    cur.execute(
        "SELECT precedent_id, situation, binding_ruling FROM alcsm.precedent_ref;"
    )
    rows = cur.fetchall()
    cur.close()
    assert len(rows) == 15
    ids = {r[0] for r in rows}
    assert ids == {f"P-{i:02d}" for i in range(1, 16)}
    # None of the "real text, not placeholders" fields are empty/placeholder-like.
    for precedent_id, situation, ruling in rows:
        assert situation.strip()
        assert ruling.strip()
        assert "TODO" not in ruling
        assert "placeholder" not in ruling.lower()


def test_seeding_twice_is_a_no_op_the_second_time(
    db_connection: psycopg2.extensions.connection,
) -> None:
    seed_reference_data(db_connection)  # already seeded once at session start
    second_pass_raters = seed_rater_ref(db_connection)
    second_pass_precedents = seed_precedent_ref(db_connection)
    assert second_pass_raters == 0
    assert second_pass_precedents == 0
