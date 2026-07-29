"""P0 skeleton test. Real coverage is added in Phase P8."""

from __future__ import annotations

import pytest

from alcsm.analysis.gap import credential_gap_by_dimension


def test_credential_gap_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        credential_gap_by_dimension()
