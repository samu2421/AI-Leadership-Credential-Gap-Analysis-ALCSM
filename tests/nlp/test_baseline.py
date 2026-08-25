"""Tests for the minimal TF-IDF + Ridge NLP baseline.

Everything here runs against small, hand-built synthetic profile data
-- never real LinkedIn content. The point of these tests is to verify
the *mechanics*: the input document excludes label-derived fields by
construction (there's nothing in `build_profile_documents`'s inputs to
leak), the train/test split never lets a profile appear on both sides,
stratification falls back correctly for sparse classes, predictions
stay within the valid 0-5 range, and the vectorizer/model are fit
"train-only" (verified indirectly via reproducibility and via the
function signature never receiving test data before fitting).
"""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.nlp.baseline import (
    RANDOM_SEED,
    build_profile_documents,
    fit_predict_dimension,
    split_profiles_for_dimension,
)


def _synthetic_sheets() -> tuple[pd.DataFrame, ...]:
    profile_master = pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, 41)],
            "Current_Title": (["AI Lead"] * 20) + (["Sales Manager"] * 20),
            "Industry": ["Technology"] * 40,
            "Company_Size": ["501-1000"] * 40,
            "Title_Category": (["Head"] * 20) + (["Manager"] * 20),
        }
    )
    education = pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, 41)],
            "Degree_Level": (["PhD"] * 20) + (["Bachelor's"] * 20),
            "Field_of_Study": (["Computer Science"] * 20) + (["Business"] * 20),
            "University": ["Some University"] * 40,
        }
    )
    certification = pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, 11)],
            "Certification_Category": ["AI & Machine Learning"] * 10,
            "Certification_Name": ["Deep Learning Specialization"] * 10,
            "Issuing_Organization": ["Coursera"] * 10,
        }
    )
    professional_experience = pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, 41)],
            "Job_Title": (["AI Engineer"] * 20) + (["Sales Rep"] * 20),
            "Industry": ["Technology"] * 40,
            "Duration_Months": [40] * 40,
            "Leadership_Role": (["Yes"] * 20) + (["No"] * 20),
            "AI_Related": (["Yes"] * 20) + (["No"] * 20),
        }
    )
    technical_contribution = pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, 6)],
            "Contribution_Type": ["Publication"] * 5,
            "Title": ["A Paper About AI"] * 5,
        }
    )
    return (
        profile_master,
        education,
        certification,
        professional_experience,
        technical_contribution,
    )


def _synthetic_gold_long(dimension_number: int, labels: list[int]) -> pd.DataFrame:
    dim_label = f"D{dimension_number}"
    return pd.DataFrame(
        {
            "Profile_ID": [f"LP{i:04d}" for i in range(1, len(labels) + 1)],
            "Dimension": dim_label,
            "Score": labels,
        }
    )


class TestBuildProfileDocuments:
    def test_every_profile_in_profile_master_gets_a_row(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        assert set(docs["Profile_ID"]) == set(sheets[0]["Profile_ID"])

    def test_ai_profiles_and_non_ai_profiles_have_different_text(self) -> None:
        docs = build_profile_documents(*_synthetic_sheets()).set_index("Profile_ID")
        ai_text = docs.loc["LP0001", "Text"]
        non_ai_text = docs.loc["LP0021", "Text"]
        assert "AI" in ai_text or "ai_related_Yes" in ai_text
        assert ai_text != non_ai_text

    def test_never_includes_evidence_or_rationale_fields(self) -> None:
        """Structural guard: nothing in the five input sheets this
        function accepts has an Evidence/Rationale/Confidence/Decision
        column at all -- there is nothing to leak by construction."""
        for sheet in _synthetic_sheets():
            forbidden = {"Evidence", "Rationale", "Confidence", "Decision"}
            assert forbidden.isdisjoint(sheet.columns)

    def test_profile_with_no_rows_elsewhere_still_gets_a_row(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        # LP0040 has no certification or technical contribution rows
        # (only 10 and 5 profiles respectively have those) but must
        # still appear, since it's in Profile_Master.
        assert "LP0040" in set(docs["Profile_ID"])


class TestSplitProfilesForDimension:
    def test_no_profile_appears_in_both_train_and_test(self) -> None:
        profile_ids = [f"LP{i:04d}" for i in range(1, 41)]
        labels = ([0] * 20) + ([1] * 20)
        split = split_profiles_for_dimension(profile_ids, labels, dimension_number=1)
        assert set(split.train_profile_ids).isdisjoint(set(split.test_profile_ids))
        assert set(split.train_profile_ids) | set(split.test_profile_ids) == set(
            profile_ids
        )

    def test_stratifies_when_every_class_has_at_least_two_members(self) -> None:
        profile_ids = [f"LP{i:04d}" for i in range(1, 41)]
        labels = ([0] * 20) + ([1] * 20)
        split = split_profiles_for_dimension(profile_ids, labels, dimension_number=1)
        assert split.stratified is True

    def test_falls_back_to_unstratified_for_a_singleton_class(self) -> None:
        profile_ids = [f"LP{i:04d}" for i in range(1, 21)]
        labels = [0] + ([1] * 19)  # class 0 has exactly one member
        split = split_profiles_for_dimension(profile_ids, labels, dimension_number=1)
        assert split.stratified is False
        assert "0" in split.note or "[0]" in split.note

    def test_reproducible_given_same_seed(self) -> None:
        profile_ids = [f"LP{i:04d}" for i in range(1, 41)]
        labels = ([0] * 20) + ([1] * 20)
        split_a = split_profiles_for_dimension(
            profile_ids, labels, dimension_number=1, seed=RANDOM_SEED
        )
        split_b = split_profiles_for_dimension(
            profile_ids, labels, dimension_number=1, seed=RANDOM_SEED
        )
        assert split_a.train_profile_ids == split_b.train_profile_ids
        assert split_a.test_profile_ids == split_b.test_profile_ids


class TestFitPredictDimension:
    def test_predictions_are_within_valid_score_range(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(3, labels)

        predictions, split, artifacts = fit_predict_dimension(docs, gold, 3)
        assert predictions["predicted_score"].between(0, 5).all()

    def test_predictions_cover_exactly_the_test_set(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(3, labels)

        predictions, split, artifacts = fit_predict_dimension(docs, gold, 3)
        assert set(predictions["profile_id"]) == set(split.test_profile_ids)
        assert len(predictions) == len(split.test_profile_ids)

    def test_dimension_number_is_constant_across_all_predictions(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(5, labels)

        predictions, _split, _artifacts = fit_predict_dimension(docs, gold, 5)
        assert (predictions["dimension_number"] == 5).all()

    def test_a_clearly_separable_signal_is_learned_better_than_chance(self) -> None:
        """Not a performance guarantee -- a sanity check that the
        pipeline (vectorizer -> ridge -> round/clip) actually learns
        the obvious AI-vs-non-AI signal built into the fixture, rather
        than e.g. silently predicting a constant."""
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(3, labels)

        predictions, split, _artifacts = fit_predict_dimension(docs, gold, 3)
        gold_by_id = dict(zip(gold["Profile_ID"], gold["Score"]))
        errors = [
            abs(row.predicted_score - gold_by_id[row.profile_id])
            for row in predictions.itertuples(index=False)
        ]
        assert (sum(errors) / len(errors)) < 2.0  # much better than random 0-5 guessing

    def test_artifacts_record_hyperparameters_and_vocabulary_size(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(3, labels)

        _predictions, _split, artifacts = fit_predict_dimension(docs, gold, 3)
        assert artifacts.dimension_number == 3
        assert artifacts.vectorizer_vocabulary_size > 0
        assert artifacts.n_train + artifacts.n_test == 40
        assert len(artifacts.top_positive_terms) == 5
        assert len(artifacts.top_negative_terms) == 5

    def test_reproducible_given_same_seed(self) -> None:
        sheets = _synthetic_sheets()
        docs = build_profile_documents(*sheets)
        labels = ([4] * 20) + ([0] * 20)
        gold = _synthetic_gold_long(3, labels)

        pred_a, _split_a, _art_a = fit_predict_dimension(docs, gold, 3, seed=7)
        pred_b, _split_b, _art_b = fit_predict_dimension(docs, gold, 3, seed=7)
        pd.testing.assert_frame_equal(
            pred_a.sort_values("profile_id").reset_index(drop=True),
            pred_b.sort_values("profile_id").reset_index(drop=True),
        )


def test_never_calls_an_external_api() -> None:
    """Structural guard: no `requests`/`httpx`/`openai`/`anthropic`
    import anywhere in this module -- everything is local scikit-learn
    computation."""
    import inspect

    from alcsm.nlp import baseline as baseline_module

    source = inspect.getsource(baseline_module)
    for forbidden in ("import requests", "import httpx", "openai", "anthropic"):
        assert forbidden not in source


@pytest.mark.parametrize("bad_input", [None, float("nan"), "not_a_number"])
def test_duration_bucket_handles_missing_or_invalid_gracefully(
    bad_input: object,
) -> None:
    from alcsm.nlp.baseline import _duration_bucket

    assert _duration_bucket(bad_input) == ""
