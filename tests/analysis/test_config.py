"""alcsm.analysis.config: data-status labeling and the freeze gate."""

from __future__ import annotations

import pytest

from alcsm.analysis.config import (
    DataNotFrozenError,
    default_analysis_paths,
    infer_profile_scores_status,
    make_metadata,
    require_frozen_or_acknowledge_provisional,
)


def test_metadata_carries_status_source_and_timestamp() -> None:
    meta = make_metadata("synthetic_fixture", "unit test")
    assert meta.data_status == "synthetic_fixture"
    assert meta.source_description == "unit test"
    assert meta.run_ts is not None


class TestFreezeGate:
    def test_provisional_without_acknowledgement_raises(self) -> None:
        with pytest.raises(DataNotFrozenError, match="acknowledge_provisional=True"):
            require_frozen_or_acknowledge_provisional(
                "provisional_first_pass", acknowledge_provisional=False
            )

    def test_provisional_with_acknowledgement_passes(self) -> None:
        require_frozen_or_acknowledge_provisional(
            "provisional_first_pass", acknowledge_provisional=True
        )

    def test_final_frozen_always_passes(self) -> None:
        require_frozen_or_acknowledge_provisional(
            "final_frozen", acknowledge_provisional=False
        )

    def test_synthetic_fixture_always_passes(self) -> None:
        require_frozen_or_acknowledge_provisional(
            "synthetic_fixture", acknowledge_provisional=False
        )


class TestInferProfileScoresStatus:
    def test_any_pending_review_is_provisional(self) -> None:
        status = infer_profile_scores_status(["Reviewed", "Pending Review", "Reviewed"])
        assert status == "provisional_first_pass"

    def test_no_pending_review_is_final_frozen(self) -> None:
        status = infer_profile_scores_status(["Reviewed", "Reviewed"])
        assert status == "final_frozen"

    def test_empty_is_final_frozen(self) -> None:
        assert infer_profile_scores_status([]) == "final_frozen"


def test_default_analysis_paths_point_inside_repo() -> None:
    paths = default_analysis_paths()
    assert paths.review_workbook.is_relative_to(paths.repo_root)
    assert paths.linkedin_processed.is_relative_to(paths.repo_root)
    assert paths.job_postings_processed.is_relative_to(paths.repo_root)
    assert paths.survey_responses.is_relative_to(paths.repo_root)
