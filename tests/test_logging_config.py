"""Tests for alcsm.logging_config — configured once, reused everywhere."""

from __future__ import annotations

import logging

from alcsm import logging_config


def test_get_logger_returns_a_logger() -> None:
    logger = logging_config.get_logger("alcsm.test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "alcsm.test"


def test_configure_logging_is_idempotent() -> None:
    logging_config.configure_logging("DEBUG")
    first_level = logging.getLogger().level
    logging_config.configure_logging("ERROR")
    # Second call is a no-op: level must not change.
    assert logging.getLogger().level == first_level
