"""P0 skeleton test. Real coverage is added in Phase P8."""

from __future__ import annotations

import pytest

from alcsm.analysis.rq4 import correlate_with_impact_indicators


def test_rq4_correlation_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        correlate_with_impact_indicators()
