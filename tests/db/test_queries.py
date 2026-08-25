"""Read queries over the five frozen views.

`fetch_reliability_input`, `fetch_final_profile_scores`, and
`fetch_profile_completeness` were implemented in Phase P4 (the
annotation interface needs progress tracking and reliability-export
scaffolding — see `alcsm.annotation.reliability_export`); tested here
against a real throwaway PostgreSQL cluster with the frozen schema
deployed, per PROJECT_CONTEXT.md §33 ("test against the specification,
not a mock"). `fetch_credential_gap_by_dimension` and
`fetch_nlp_evaluation` remain P7/P8 skeletons (PROJECT_CONTEXT.md §38).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from sqlalchemy.orm import Session

import alcsm.db.engine as engine_module
from alcsm.config import DatabaseSettings, Settings
from alcsm.db import queries
from alcsm.db.engine import get_engine


@pytest.mark.parametrize(
    "func",
    [
        queries.fetch_credential_gap_by_dimension,
        queries.fetch_nlp_evaluation,
    ],
)
def test_still_unimplemented_query_raises_not_implemented(
    func: Callable[[object], object],
) -> None:
    """P7/P8 scope, unrelated to P4 annotation — still a skeleton."""
    with pytest.raises(NotImplementedError):
        func(None)


@pytest.fixture()
def sqlalchemy_session(throwaway_database: DatabaseSettings) -> Iterator[Session]:
    """Mirrors `tests/db/test_engine.py`'s process-wide-singleton reset
    pattern, so this file never picks up a stale engine from another
    test module and never leaves one behind."""
    engine_module._engine = None
    engine_module._session_factory = None
    settings = Settings(database=throwaway_database, log_level="INFO")
    engine = get_engine(settings)
    session = Session(bind=engine, future=True)
    try:
        yield session
    finally:
        session.close()
        engine_module._engine = None
        engine_module._session_factory = None


def test_fetch_reliability_input_reads_the_view_without_error(
    sqlalchemy_session: Session,
) -> None:
    """This file shares one session-scoped throwaway cluster with every
    other test module (`tests/conftest.py`), so other files' rows may
    already be present by the time this runs -- this only proves the
    view is reachable and every returned row is well-typed, never
    asserts a specific row count."""
    rows = queries.fetch_reliability_input(sqlalchemy_session)
    assert isinstance(rows, list)
    for row in rows:
        assert 1 <= row.dimension_number <= 6
        assert row.corpus in ("profile", "job_posting")


def test_fetch_final_profile_scores_reads_the_view_without_error(
    sqlalchemy_session: Session,
) -> None:
    rows = queries.fetch_final_profile_scores(sqlalchemy_session)
    assert isinstance(rows, list)
    for row in rows:
        assert 1 <= row.dimension_number <= 6
        assert 0 <= row.score <= 5


def test_fetch_profile_completeness_reads_the_view_without_error(
    sqlalchemy_session: Session,
) -> None:
    rows = queries.fetch_profile_completeness(sqlalchemy_session)
    assert isinstance(rows, list)
    for row in rows:
        assert 0.0 <= row.completeness_index <= 1.0
        assert 0 <= row.dimensions_scored <= 6
