"""Compare NLP predictions to the human gold standard (RQ5).

Evaluation infrastructure only. **No model is trained, loaded, or run
by this module** — `alcsm.nlp.classify` (the actual predictor) remains
an unimplemented Phase P7 stub, untouched by this task, per the
explicit "do not train final NLP models" instruction. Every function
here takes a ``predictions`` table as plain input data (columns:
`profile_id`, `dimension_number`, `predicted_score`) and compares it
against a gold-standard table shaped like `v_final_profile_score` (via
`db.queries.fetch_final_profile_scores` once real data exists) — where
those predictions came from is not this module's concern.

The gold-standard side of every comparison must be the final,
researcher-reviewed human annotation, never the AI-assisted first pass
(the same "final, not first-pass" discipline as RQ1/RQ2/RQ4) — every
top-level function threads `data_status` through
`require_frozen_or_acknowledge_provisional` exactly as the other RQ
modules do.

Metrics are ordinal-appropriate throughout, using
`db.queries.fetch_nlp_evaluation` (i.e. `v_nlp_evaluation`) as the
target read path once real predictions exist: exact-match rate,
signed/absolute error, and linear-weighted Cohen's kappa (the same
weighted-kappa companion statistic `ALCSM_Coding_Rulebook_and_Pilot_
Design.md` §2.4 already recommends alongside Krippendorff's alpha for
a 0-5 ordinal scale), computed without a hard `scipy`/`sklearn`
dependency (PROJECT_CONTEXT.md §16, §25, §48).
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from alcsm.analysis.config import (
    AnalysisRunMetadata,
    DataStatus,
    make_metadata,
    require_frozen_or_acknowledge_provisional,
)
from alcsm.constants import DIMENSIONS, SCORE_MAX, SCORE_MIN

_SCORE_LEVELS = list(range(SCORE_MIN, SCORE_MAX + 1))


def _merge_predictions_and_gold(
    predictions: pd.DataFrame, gold: pd.DataFrame, dimension_number: int
) -> pd.DataFrame:
    pred_d = predictions[predictions["dimension_number"] == dimension_number]
    gold_d = gold[gold["dimension_number"] == dimension_number]
    return pred_d.merge(gold_d, on="profile_id", suffixes=("_pred", "_gold"))


def confusion_matrix_by_dimension(
    predictions: pd.DataFrame, gold: pd.DataFrame
) -> dict[int, pd.DataFrame]:
    """One 6x6 (0-5 x 0-5) confusion matrix per dimension, rows=gold,
    columns=predicted. Dimensions with no paired observations are
    omitted from the returned dict rather than included as an
    all-zero matrix (an empty matrix is not itself a finding)."""
    result: dict[int, pd.DataFrame] = {}
    for d in DIMENSIONS:
        merged = _merge_predictions_and_gold(predictions, gold, d.number)
        if merged.empty:
            continue
        matrix = pd.crosstab(
            merged["score"], merged["predicted_score"], dropna=False
        ).reindex(index=_SCORE_LEVELS, columns=_SCORE_LEVELS, fill_value=0)
        result[d.number] = matrix
    return result


def _linear_weighted_kappa(confusion: pd.DataFrame) -> float:
    """Linear-weighted Cohen's kappa from a 6x6 gold-x-predicted
    confusion matrix (counts, not proportions)."""
    n = confusion.values.sum()
    if n == 0:
        return float("nan")
    observed = confusion.values / n
    row_marginal = observed.sum(axis=1)
    col_marginal = observed.sum(axis=0)
    expected = pd.DataFrame(
        [[r * c for c in col_marginal] for r in row_marginal],
        index=confusion.index,
        columns=confusion.columns,
    ).values

    max_weight = SCORE_MAX - SCORE_MIN
    weights = pd.DataFrame(
        [[abs(i - j) / max_weight for j in _SCORE_LEVELS] for i in _SCORE_LEVELS],
        index=_SCORE_LEVELS,
        columns=_SCORE_LEVELS,
    ).values

    observed_disagreement = (weights * observed).sum()
    expected_disagreement = (weights * expected).sum()
    if expected_disagreement == 0:
        return 1.0 if observed_disagreement == 0 else float("nan")
    return 1.0 - observed_disagreement / expected_disagreement


@dataclass(frozen=True)
class DimensionEvaluationMetrics:
    dimension: str
    n: int
    exact_match_rate: float
    mean_signed_error: float
    mean_absolute_error: float
    linear_weighted_kappa: float


@dataclass(frozen=True)
class NlpEvaluationReport:
    metadata: AnalysisRunMetadata
    by_dimension: dict[int, DimensionEvaluationMetrics]
    confusion_matrices: dict[int, pd.DataFrame]


def evaluate_predictions(
    predictions: pd.DataFrame,
    gold: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
) -> NlpEvaluationReport:
    """Per-dimension NLP-vs-gold-standard evaluation: exact-match rate,
    signed/absolute error, linear-weighted kappa, and the confusion
    matrix. Never pooled across dimensions (same discipline as
    Krippendorff's alpha reporting, and for the same reason: the six
    dimensions have different verifiability profiles and a pooled
    figure would hide that).

    ``gold`` must be the final, researcher-reviewed annotation --
    `data_status` is threaded through the same freeze-gate every other
    RQ module uses, so a caller cannot silently evaluate against a
    still-provisional gold standard without acknowledging it.
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    confusion_matrices = confusion_matrix_by_dimension(predictions, gold)
    by_dimension: dict[int, DimensionEvaluationMetrics] = {}
    for d in DIMENSIONS:
        merged = _merge_predictions_and_gold(predictions, gold, d.number)
        if merged.empty:
            continue
        signed_error = merged["predicted_score"] - merged["score"]
        by_dimension[d.number] = DimensionEvaluationMetrics(
            dimension=f"D{d.number}",
            n=len(merged),
            exact_match_rate=float((signed_error == 0).mean()),
            mean_signed_error=float(signed_error.mean()),
            mean_absolute_error=float(signed_error.abs().mean()),
            linear_weighted_kappa=_linear_weighted_kappa(confusion_matrices[d.number]),
        )
    return NlpEvaluationReport(
        metadata=make_metadata(data_status, source_description),
        by_dimension=by_dimension,
        confusion_matrices=confusion_matrices,
    )


@dataclass(frozen=True)
class ErrorCase:
    profile_id: str
    dimension: str
    gold_score: int
    predicted_score: int
    absolute_error: int


@dataclass(frozen=True)
class ErrorAnalysisReport:
    metadata: AnalysisRunMetadata
    largest_errors: list[ErrorCase]  # sorted descending by absolute_error
    error_distribution_by_dimension: (
        pd.DataFrame
    )  # index=D1..D6, columns=absolute error 0..5


def error_analysis(
    predictions: pd.DataFrame,
    gold: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    top_n: int = 20,
) -> ErrorAnalysisReport:
    """The ``top_n`` largest-magnitude prediction errors (profile id,
    dimension, gold vs predicted score only -- never evidence text,
    which this module never reads in the first place), plus the full
    per-dimension distribution of absolute error magnitudes.
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    all_cases: list[ErrorCase] = []
    dist_rows = []
    for d in DIMENSIONS:
        merged = _merge_predictions_and_gold(predictions, gold, d.number)
        if merged.empty:
            zero_counts: dict[object, object] = {i: 0 for i in range(6)}
            dist_rows.append({"dimension": f"D{d.number}", **zero_counts})
            continue
        abs_error = (merged["predicted_score"] - merged["score"]).abs()
        for _, row in merged.assign(abs_error=abs_error).iterrows():
            all_cases.append(
                ErrorCase(
                    profile_id=row["profile_id"],
                    dimension=f"D{d.number}",
                    gold_score=int(row["score"]),
                    predicted_score=int(row["predicted_score"]),
                    absolute_error=int(row["abs_error"]),
                )
            )
        counts = abs_error.value_counts().reindex(range(6), fill_value=0)
        dist_rows.append({"dimension": f"D{d.number}", **counts.to_dict()})

    all_cases.sort(key=lambda c: c.absolute_error, reverse=True)
    distribution = pd.DataFrame(dist_rows).set_index("dimension")
    return ErrorAnalysisReport(
        metadata=make_metadata(data_status, source_description),
        largest_errors=all_cases[:top_n],
        error_distribution_by_dimension=distribution,
    )
