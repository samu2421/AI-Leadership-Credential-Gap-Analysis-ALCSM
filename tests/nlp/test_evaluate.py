"""RQ5 NLP evaluation: confusion matrices, ordinal metrics, error
analysis -- against a tiny fixture with known gold scores
(PROJECT_CONTEXT.md §33), never a trained model."""

from __future__ import annotations

import pandas as pd
import pytest

from alcsm.analysis.config import DataNotFrozenError
from alcsm.nlp.evaluate import (
    confusion_matrix_by_dimension,
    error_analysis,
    evaluate_predictions,
)


class TestConfusionMatrix:
    def test_shape_is_six_by_six(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        matrices = confusion_matrix_by_dimension(synthetic_predictions, synthetic_gold)
        for matrix in matrices.values():
            assert matrix.shape == (6, 6)

    def test_total_count_matches_n_paired(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        matrices = confusion_matrix_by_dimension(synthetic_predictions, synthetic_gold)
        n_per_dim = synthetic_predictions.groupby("dimension_number").size()
        for dim, matrix in matrices.items():
            assert matrix.values.sum() == n_per_dim[dim]

    def test_perfect_prediction_is_diagonal_only(self) -> None:
        predictions = pd.DataFrame(
            [
                {"profile_id": f"P{i}", "dimension_number": 1, "predicted_score": i % 6}
                for i in range(6)
            ]
        )
        gold = pd.DataFrame(
            [
                {"profile_id": f"P{i}", "dimension_number": 1, "score": i % 6}
                for i in range(6)
            ]
        )
        matrix = confusion_matrix_by_dimension(predictions, gold)[1]
        off_diagonal_sum = matrix.values.sum() - sum(
            matrix.iloc[i, i] for i in range(6)
        )
        assert off_diagonal_sum == 0


class TestEvaluatePredictions:
    def test_gated_on_provisional(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            evaluate_predictions(
                synthetic_predictions,
                synthetic_gold,
                "provisional_first_pass",
                "fixture",
            )

    def test_perfect_agreement_metrics(self) -> None:
        predictions = pd.DataFrame(
            [
                {"profile_id": f"P{i}", "dimension_number": n, "predicted_score": 3}
                for i in range(5)
                for n in range(1, 7)
            ]
        )
        gold = pd.DataFrame(
            [
                {"profile_id": f"P{i}", "dimension_number": n, "score": 3}
                for i in range(5)
                for n in range(1, 7)
            ]
        )
        report = evaluate_predictions(predictions, gold, "final_frozen", "fixture")
        for metrics in report.by_dimension.values():
            assert metrics.exact_match_rate == 1.0
            assert metrics.mean_absolute_error == 0.0
            assert metrics.mean_signed_error == 0.0

    def test_never_pooled_across_dimensions(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        report = evaluate_predictions(
            synthetic_predictions, synthetic_gold, "final_frozen", "fixture"
        )
        assert len(report.by_dimension) == 6
        maes = {m.mean_absolute_error for m in report.by_dimension.values()}
        assert len(maes) > 1  # dimensions genuinely differ, not one pooled figure

    def test_weighted_kappa_bounded(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        report = evaluate_predictions(
            synthetic_predictions, synthetic_gold, "final_frozen", "fixture"
        )
        for metrics in report.by_dimension.values():
            if (
                metrics.linear_weighted_kappa == metrics.linear_weighted_kappa
            ):  # not NaN
                assert -1.0 <= metrics.linear_weighted_kappa <= 1.0


class TestErrorAnalysis:
    def test_gated_on_provisional(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        with pytest.raises(DataNotFrozenError):
            error_analysis(
                synthetic_predictions,
                synthetic_gold,
                "provisional_first_pass",
                "fixture",
            )

    def test_largest_errors_sorted_descending(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        report = error_analysis(
            synthetic_predictions, synthetic_gold, "final_frozen", "fixture"
        )
        errors = [c.absolute_error for c in report.largest_errors]
        assert errors == sorted(errors, reverse=True)

    def test_error_cases_never_carry_evidence_text(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        from dataclasses import fields

        from alcsm.nlp.evaluate import ErrorCase

        field_names = {f.name for f in fields(ErrorCase)}
        assert "evidence" not in field_names
        assert "rationale" not in field_names

    def test_respects_top_n(
        self, synthetic_predictions: pd.DataFrame, synthetic_gold: pd.DataFrame
    ) -> None:
        report = error_analysis(
            synthetic_predictions, synthetic_gold, "final_frozen", "fixture", top_n=3
        )
        assert len(report.largest_errors) <= 3


def test_module_never_imports_or_calls_a_training_function() -> None:
    """Structural guard: this task's explicit "do not train final NLP
    models" -- `nlp/evaluate.py` must not import `nlp.classify` or call
    anything with "train" in its name."""
    import ast
    import inspect

    from alcsm.nlp import evaluate as evaluate_module

    tree = ast.parse(inspect.getsource(evaluate_module))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "classify" not in node.module.lower()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert "train" not in node.func.id.lower()
