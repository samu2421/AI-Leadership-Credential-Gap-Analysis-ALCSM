"""P0 skeleton test. Real coverage (constructed fixtures only, never
real personal data) is added in Phase P1 when the helper is ported.
"""

from __future__ import annotations

import pytest

from alcsm.collection.helper import insert_profile


def test_insert_profile_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        insert_profile()
