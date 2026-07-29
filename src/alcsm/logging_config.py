"""Centralised logging configuration.

Configured once and reused everywhere (PROJECT_CONTEXT.md §31).

Hard rule: never log personal data. Profile text, evidence spans, and
any identifier must not appear at INFO level or above. If a log
message must reference a record, log only its pseudonymous id
(e.g. "PRF-00042") — never raw profile content. This module does not
enforce that at runtime (it cannot know what a caller passes); callers
are responsible for keeping personal data out of log calls.
"""

from __future__ import annotations

import logging

_CONFIGURED = False

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure the root logger once. Subsequent calls are no-ops."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    logging.basicConfig(level=level.upper(), format=_LOG_FORMAT)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module logger. Configures logging on first use."""
    if not _CONFIGURED:
        configure_logging()
    return logging.getLogger(name)
