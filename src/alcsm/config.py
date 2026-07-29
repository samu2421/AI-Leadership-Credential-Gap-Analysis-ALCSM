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
        """Build a SQLAlchemy-style DSN (used by db/engine.py only)."""
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

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
