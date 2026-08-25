"""Typed, environment-driven settings.

Loads configuration from environment variables (and a local `.env` via
python-dotenv). Never hard-codes secrets or a database DSN — see
CLAUDE_CODE_RULES.md rule 8 and PROJECT_CONTEXT.md §27 ("config.py ...
Must never: Hard-code secrets or DSNs").
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


@dataclass(frozen=True)
class DatabaseSettings:
    """Connection parameters for the ALCSM PostgreSQL database.

    The schema itself is defined only in
    ``schema/alcsm_schema_v1.0.1.sql`` (see PROJECT_CONTEXT.md §22);
    this class carries connection parameters only, never structure.
    """

    name: str
    user: str
    host: str
    port: int
    password: str

    def to_dsn(self) -> str:
        """Build a SQLAlchemy-style DSN (used by db/engine.py only).

        Uses ``sqlalchemy.engine.URL.create`` rather than manual
        f-string interpolation for two reasons: it percent-encodes a
        password containing special characters correctly, and it
        handles a Unix-socket-directory ``host`` (e.g.
        ``alcsm.collection.devcluster.throwaway_database``'s socket
        path, which contains ``/``) by passing it as a query
        parameter instead of the URL's host segment -- a literal
        ``/`` in the host segment itself is not valid there and
        silently corrupts the parsed DSN (discovered when Phase P4's
        annotation tests first exercised this path against a real
        throwaway cluster; ``as_psycopg2_kwargs`` never hit this
        because psycopg2's own ``host`` kwarg already accepts a
        socket path directly).
        """
        if self.host.startswith("/"):
            return URL.create(
                "postgresql+psycopg2",
                username=self.user,
                password=self.password or None,
                database=self.name,
                query={"host": self.host, "port": str(self.port)},
            ).render_as_string(hide_password=False)
        return URL.create(
            "postgresql+psycopg2",
            username=self.user,
            password=self.password or None,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)

    def as_psycopg2_kwargs(self) -> dict[str, str | int]:
        """Connection kwargs for a raw ``psycopg2.connect(**kwargs)`` call.

        psycopg2 does not understand the SQLAlchemy ``+psycopg2`` DSN
        dialect suffix, so the collection helper (the single
        psycopg2-based write path, PROJECT_CONTEXT.md §23) uses this
        instead of ``to_dsn()``.
        """
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.name,
            "user": self.user,
            "password": self.password,
        }


@dataclass(frozen=True)
class Settings:
    """Application-wide settings, assembled from the environment."""

    database: DatabaseSettings
    log_level: str


def _require_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {key}. "
            "Copy .env.example to .env and fill in local values."
        )
    return value


def load_settings() -> Settings:
    """Load Settings from the current environment.

    Raises RuntimeError with a readable message if a required variable
    is missing, rather than failing deep inside a connection attempt.
    """
    database = DatabaseSettings(
        name=_require_env("DATABASE_NAME"),
        user=_require_env("DATABASE_USER"),
        host=_require_env("DATABASE_HOST"),
        port=int(os.environ.get("DATABASE_PORT", "5432")),
        password=_require_env("DATABASE_PASSWORD"),
    )
    return Settings(
        database=database,
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
