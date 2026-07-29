"""SQLAlchemy engine and session lifecycle.

Provides the engine/session only. Must never define or migrate schema
(PROJECT_CONTEXT.md §23, §27): no `declarative_base()` table
definitions and no `metadata.create_all()` against the research
database, and no Alembic wiring. `schema/alcsm_schema_v1.0.1.sql` is
deployed independently of this module.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from alcsm.config import Settings, load_settings

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def get_engine(settings: Settings | None = None) -> Engine:
    """Return the process-wide SQLAlchemy engine, creating it once."""
    global _engine
    if _engine is None:
        settings = settings or load_settings()
        _engine = create_engine(settings.database.to_dsn(), future=True)
    return _engine


@contextmanager
def session_scope(settings: Settings | None = None) -> Iterator[Session]:
    """Yield a Session; commit on success, roll back on any error.

    Mirrors the atomic, fail-loud pattern required by
    PROJECT_CONTEXT.md §32 (validate, transact, roll back whole on
    error — no partial writes).
    """
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(settings), future=True)
    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
