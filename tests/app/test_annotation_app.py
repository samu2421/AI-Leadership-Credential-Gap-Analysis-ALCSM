"""P4 annotation interface — Streamlit app-level smoke tests.

Uses Streamlit's own `AppTest` runner (streamlit>=1.28) to actually
execute the app against constructed fixtures, not just import it.
Never touches a real database or real profile data -- the app's
default state is fixtures-only, matching how it is meant to be run
before P2/P3 clear.
"""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

_APP_PATH = str(
    Path(__file__).resolve().parents[2] / "src" / "alcsm" / "app" / "annotation_app.py"
)


def _run() -> AppTest:
    at = AppTest.from_file(_APP_PATH)
    at.run(timeout=30)
    return at


def test_app_runs_without_error() -> None:
    at = _run()
    assert not at.exception


def test_app_shows_all_six_dimensions() -> None:
    at = _run()
    body = " ".join(md.value for md in at.markdown)
    for n in range(1, 7):
        assert f"D{n} —" in body


def test_app_shows_d6_as_proposed() -> None:
    at = _run()
    body = " ".join(md.value for md in at.markdown)
    assert "AI Industry/Application Breadth" in body
    assert "PROPOSED/PILOT_REQUIRED" in body


def test_app_never_renders_rq4_labels() -> None:
    at = _run()
    all_text = " ".join(md.value for md in at.markdown) + " ".join(
        c.value for c in at.caption
    )
    lowered = all_text.lower()
    assert "rq4_network_reach" not in lowered
    assert "rq4_content_engagement" not in lowered
    assert "rq4_recognition_count" not in lowered


def test_app_states_rq4_isolation_explicitly() -> None:
    """Frozen constraint #2 -- the app should say plainly that RQ4 is not
    shown here, not just happen to omit it silently."""
    at = _run()
    info_text = " ".join(i.value for i in at.info)
    assert "RQ4" in info_text


def test_app_shows_first_pass_and_final_as_distinct_concepts() -> None:
    at = _run()
    body = " ".join(md.value for md in at.markdown)
    assert "FIRST_PASS_SCORE" in body
    assert "FINAL_HUMAN_SCORE" in body


def test_switching_to_v1_0_shows_the_retired_d6_label() -> None:
    at = _run()
    version_selector = [s for s in at.selectbox if "version" in (s.label or "").lower()]
    assert version_selector, "expected a dimension-config version selector"
    version_selector[0].set_value("v1_0").run(timeout=30)
    body = " ".join(md.value for md in at.markdown)
    assert "Professional Engagement" in body
