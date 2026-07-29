"""P0 skeleton test. Real coverage is added in Phase P9."""

from __future__ import annotations

import pytest

from alcsm.app.streamlit_app import main


def test_main_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        main()
