"""Annotation-score storage: insert/read round trip, duplicate prevention,
rater blinding, and adjudication -- against a real throwaway PostgreSQL
cluster with the frozen schema deployed (PROJECT_CONTEXT.md §33: test
against the specification, not a mock).
"""

from __future__ import annotations

from datetime import datetime

import psycopg2
import pytest

from alcsm.annotation.models import AnnotationScore
from alcsm.annotation.store import (
    DuplicateScoreError,
    fetch_adjudication_score,
    fetch_both_rater_scores_for_adjudication,
    fetch_rater_score,
    has_other_rater_submitted,
    insert_adjudication,
    insert_annotation_score,
)
from alcsm.annotation.validation import AnnotationValidationError

_NOW = datetime.now()


def _score(profile_id: str, **overrides: object) -> AnnotationScore:
    defaults: dict[str, object] = dict(
        profile_id=profile_id,
        dimension_number=1,
        rater_id="RATER_A",
        score=3,
        missing_status="present",
        rulebook_version="1.0",
        coding_ts=_NOW,
        evidence_text="fixture evidence text",
    )
    defaults.update(overrides)
    return AnnotationScore(**defaults)  # type: ignore[arg-type]


def test_insert_and_fetch_round_trip(
    db_connection: psycopg2.extensions.connection, inserted_profile_id: str
) -> None:
    record = _score(
        inserted_profile_id, dimension_number=1, rater_id="RATER_A", score=4
    )
    record_id = insert_annotation_score(db_connection, record)
    assert record_id > 0

    fetched = fetch_rater_score(db_connection, inserted_profile_id, 1, "RATER_A")
    assert fetched is not None
    assert fetched.score == 4
    assert fetched.evidence_text == "fixture evidence text"


def test_unsubmitted_dimension_returns_none(
    db_connection: psycopg2.extensions.connection, inserted_profile_id: str
) -> None:
    assert fetch_rater_score(db_connection, inserted_profile_id, 5, "RATER_A") is None


def test_invalid_score_never_reaches_the_database(
    db_connection: psycopg2.extensions.connection, inserted_profile_id: str
) -> None:
    bad = _score(inserted_profile_id, score=9)
    with pytest.raises(AnnotationValidationError):
        insert_annotation_score(db_connection, bad)
    assert fetch_rater_score(db_connection, inserted_profile_id, 1, "RATER_A") is None


class TestDuplicatePrevention:
    def test_second_submission_same_rater_same_dimension_rejected(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        first = _score(inserted_profile_id, dimension_number=2, rater_id="RATER_A")
        insert_annotation_score(db_connection, first)

        second = _score(
            inserted_profile_id, dimension_number=2, rater_id="RATER_A", score=1
        )
        with pytest.raises(DuplicateScoreError):
            insert_annotation_score(db_connection, second)

    def test_original_score_survives_a_rejected_duplicate(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        first = _score(
            inserted_profile_id, dimension_number=3, rater_id="RATER_A", score=4
        )
        insert_annotation_score(db_connection, first)
        try:
            insert_annotation_score(
                db_connection,
                _score(
                    inserted_profile_id, dimension_number=3, rater_id="RATER_A", score=1
                ),
            )
        except DuplicateScoreError:
            pass
        fetched = fetch_rater_score(db_connection, inserted_profile_id, 3, "RATER_A")
        assert fetched is not None
        assert (
            fetched.score == 4
        ), "a rejected duplicate must never overwrite the original"

    def test_different_raters_same_dimension_both_allowed(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection,
            _score(inserted_profile_id, dimension_number=4, rater_id="RATER_A"),
        )
        insert_annotation_score(
            db_connection,
            _score(inserted_profile_id, dimension_number=4, rater_id="RATER_B"),
        )
        assert (
            fetch_rater_score(db_connection, inserted_profile_id, 4, "RATER_A")
            is not None
        )
        assert (
            fetch_rater_score(db_connection, inserted_profile_id, 4, "RATER_B")
            is not None
        )


class TestRaterBlinding:
    def test_has_other_rater_submitted_false_before_any_submission(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        assert (
            has_other_rater_submitted(db_connection, inserted_profile_id, 5, "RATER_A")
            is False
        )

    def test_has_other_rater_submitted_true_after_the_other_rater_submits(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection,
            _score(inserted_profile_id, dimension_number=5, rater_id="RATER_B"),
        )
        assert (
            has_other_rater_submitted(db_connection, inserted_profile_id, 5, "RATER_A")
            is True
        )

    def test_has_other_rater_submitted_is_false_for_ones_own_submission(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        """Submitting your own score must not make has_other_rater_submitted
        report True for yourself -- it answers "has anyone ELSE"."""
        insert_annotation_score(
            db_connection,
            _score(inserted_profile_id, dimension_number=6, rater_id="RATER_A"),
        )
        assert (
            has_other_rater_submitted(db_connection, inserted_profile_id, 6, "RATER_A")
            is False
        )

    def test_blinding_check_returns_boolean_never_a_score(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection,
            _score(
                inserted_profile_id, dimension_number=1, rater_id="RATER_B", score=5
            ),
        )
        result = has_other_rater_submitted(
            db_connection, inserted_profile_id, 1, "RATER_A"
        )
        assert isinstance(result, bool)


class TestAdjudication:
    def test_insert_adjudication_forces_correct_rater_id_and_flag(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        record = _score(
            inserted_profile_id,
            dimension_number=2,
            rater_id="anything-a-caller-might-pass",
            is_adjudication=False,
            score=3,
        )
        insert_adjudication(db_connection, record)
        adjudicated = fetch_adjudication_score(db_connection, inserted_profile_id, 2)
        assert adjudicated is not None
        assert adjudicated.rater_id == "ADJUDICATOR"
        assert adjudicated.is_adjudication is True

    def test_fetch_both_rater_scores_excludes_adjudication(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection,
            _score(
                inserted_profile_id, dimension_number=3, rater_id="RATER_A", score=2
            ),
        )
        insert_annotation_score(
            db_connection,
            _score(
                inserted_profile_id, dimension_number=3, rater_id="RATER_B", score=4
            ),
        )
        insert_adjudication(
            db_connection,
            _score(
                inserted_profile_id, dimension_number=3, rater_id="RATER_A", score=3
            ),
        )
        independent = fetch_both_rater_scores_for_adjudication(
            db_connection, inserted_profile_id, 3
        )
        assert len(independent) == 2
        assert all(not s.is_adjudication for s in independent)

    def test_no_adjudication_returns_none(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        assert fetch_adjudication_score(db_connection, inserted_profile_id, 4) is None
