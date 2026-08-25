"""Per-dimension Krippendorff's alpha, bootstrap CI, % agreement, variance.

Implements Phase P5's reliability computation, now explicitly
requested as part of the RQ3 analysis-preparation build
(`alcsm.analysis.rq3_validation`). Must:

- compute alpha separately per dimension, never pooled across the six
  dimensions (PROJECT_CONTEXT.md §27, §41 — formative index, dimensions
  are not expected to correlate);
- be called only on pre-adjudication, independent rows (i.e. exactly
  the shape `alcsm.annotation.reliability_export`/`db.queries.
  fetch_reliability_input` already produce via `v_reliability_input`,
  which already excludes adjudicated rows) — this module does not
  itself know or care where its input came from, it only computes the
  statistic on whatever ratings it is given, so the caller carries
  the responsibility of not feeding it adjudicated rows;
- never compute or report Cronbach's alpha across dimensions
  (PROJECT_CONTEXT.md §3, §41 — wrong statistic for a formative index)
  — nothing in this module sums or pools scores across dimensions;
- match `reliability_result`'s column shape (alpha, bootstrap CI
  bounds, % agreement, n_units, variance), tagged with the thresholds
  from `alcsm.analysis.config` (KRIPPENDORFF_MINIMUM_ACCEPTABLE=.667,
  KRIPPENDORFF_TARGET=.80).

Reference: Krippendorff (2004), *Content Analysis: An Introduction to
Its Methodology*; Hayes & Krippendorff (2007), *Answering the Call for
a Standard Reliability Measure for Coding Data*, Communication Methods
and Measures.

Tested against hand-worked small cases with a known alpha
(CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §11).
"""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations
from typing import Literal

DistanceMetric = Literal["nominal", "ordinal", "interval"]

# A unit (profile x dimension) keyed by an opaque id, mapping rater_id
# to its numeric rating. Units with fewer than 2 raters are excluded
# from the coincidence matrix (standard Krippendorff's alpha
# treatment: disagreement is undefined for a single rating).
Ratings = Mapping[str, Mapping[str, float]]


class InsufficientDataError(ValueError):
    """Raised when fewer than 2 units have >=2 ratings each -- alpha is
    undefined (there is nothing to compare)."""


def _distance_squared(
    a: float, b: float, metric: DistanceMetric, all_values: Sequence[float]
) -> float:
    if metric == "nominal":
        return 0.0 if a == b else 1.0
    if metric == "interval":
        return (a - b) ** 2
    if metric == "ordinal":
        # Krippendorff's ordinal difference function: build marginal
        # frequency counts over the observed value scale, then
        # delta^2(c,k) = (sum of frequencies for ranks between c and k,
        # inclusive, minus half of each endpoint's own frequency) ^ 2.
        if a == b:
            return 0.0
        lo, hi = sorted((a, b))
        freq: dict[float, int] = defaultdict(int)
        for v in all_values:
            freq[v] += 1
        distinct_sorted = sorted(freq)
        total_between = 0.0
        for v in distinct_sorted:
            if lo <= v <= hi:
                total_between += freq[v]
        total_between -= (freq[lo] + freq[hi]) / 2.0
        return total_between**2
    raise ValueError(f"unknown metric: {metric}")


def _coincidence_matrix(
    ratings: Ratings, metric: DistanceMetric
) -> tuple[dict[tuple[float, float], float], dict[float, float], float, list[float]]:
    """Build the coincidence matrix, marginal totals, grand total n,
    and the flat list of every pairable value (for the ordinal metric's
    marginal-frequency computation)."""
    o: dict[tuple[float, float], float] = defaultdict(float)
    all_values: list[float] = []
    usable_units = 0
    for unit_ratings in ratings.values():
        values = list(unit_ratings.values())
        m_u = len(values)
        if m_u < 2:
            continue
        usable_units += 1
        all_values.extend(values)
        weight = 1.0 / (m_u - 1)
        for a, b in permutations(values, 2):
            o[(a, b)] += weight
    if usable_units < 2:
        raise InsufficientDataError(
            f"only {usable_units} unit(s) have >=2 ratings; need at least 2 "
            "comparable units to compute Krippendorff's alpha"
        )
    n_c: dict[float, float] = defaultdict(float)
    for (a, _b), w in o.items():
        n_c[a] += w
    n = sum(n_c.values())
    return dict(o), dict(n_c), n, all_values


def compute_alpha_for_dimension(
    ratings: Ratings, metric: DistanceMetric = "ordinal"
) -> float:
    """Krippendorff's alpha for one dimension's ratings.

    ``ratings`` is ``{unit_id: {rater_id: value}}`` — exactly the shape
    a group-by over `alcsm.annotation.reliability_export.
    ReliabilityInputRow` filtered to one `dimension_number` produces.
    Units with only one rater contribute nothing (standard treatment).
    Raises :class:`InsufficientDataError` if fewer than two comparable
    units exist.
    """
    o, n_c, n, all_values = _coincidence_matrix(ratings, metric)
    do = 0.0
    for (a, b), weight in o.items():
        if a != b:
            do += weight * _distance_squared(a, b, metric, all_values)
    do /= n

    de = 0.0
    values = list(n_c.keys())
    for a in values:
        for b in values:
            if a != b:
                de += n_c[a] * n_c[b] * _distance_squared(a, b, metric, all_values)
    de /= n * (n - 1)

    if de == 0:
        # Zero expected disagreement: either everyone agrees on
        # everything (alpha=1, no discrimination needed) or there is
        # only one distinct value across all raters. Krippendorff's
        # convention: alpha is undefined in the zero-variance case;
        # this project's own schema comment flags exactly this risk
        # ("low variance can deflate alpha despite high raw agreement").
        return 1.0 if do == 0 else float("nan")
    return 1.0 - do / de


def percent_agreement(ratings: Ratings) -> float:
    """Fraction of >=2-rater units where every rater gave the same value.

    A simple, literature-standard companion statistic to alpha —
    reported alongside it, never instead of it (alpha corrects for
    chance agreement; percent agreement does not).
    """
    usable = [list(u.values()) for u in ratings.values() if len(u) >= 2]
    if not usable:
        raise InsufficientDataError("no unit has >=2 ratings")
    agreements = sum(1 for values in usable if len(set(values)) == 1)
    return agreements / len(usable)


def score_variance(ratings: Ratings) -> float:
    """Population variance of every individual rating across all units
    and raters (not a per-unit variance) — reported alongside alpha
    per the schema's own comment on `reliability_result.score_variance`:
    low variance can deflate alpha even when raw agreement is high, so
    both figures must always be read together."""
    all_values = [v for unit in ratings.values() for v in unit.values()]
    if len(all_values) < 2:
        raise InsufficientDataError("need at least 2 individual ratings")
    mean = sum(all_values) / len(all_values)
    return sum((v - mean) ** 2 for v in all_values) / len(all_values)


@dataclass(frozen=True)
class KrippendorffResult:
    """Mirrors `reliability_result`'s column shape exactly (minus the
    server-assigned `reliability_id`), so a future write path (not
    built here) needs no reshaping."""

    dimension_number: int
    analysis_stage: Literal["pilot", "main_double_coded"]
    corpus: Literal["profile", "job_posting"]
    n_units: int
    krippendorff_alpha: float
    alpha_ci_lower: float | None
    alpha_ci_upper: float | None
    percent_agreement: float
    score_variance: float
    rulebook_version: str
    notes: str | None = None


def bootstrap_alpha_ci(
    ratings: Ratings,
    metric: DistanceMetric = "ordinal",
    n_resamples: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> tuple[float, float]:
    """Percentile bootstrap CI for Krippendorff's alpha.

    Resamples UNITS with replacement (not individual ratings —
    resampling ratings would break the within-unit pairing structure
    alpha depends on), recomputes alpha on each resample, and returns
    the ``confidence``-level percentile interval. Deterministic given
    the same ``seed`` (reproducibility, CLAUDE_CODE_IMPLEMENTATION_
    GUIDE.md §11/§25). Resamples that happen to contain fewer than two
    usable units are skipped rather than raising, since a bootstrap
    over a small pilot can occasionally produce a degenerate sample.
    """
    unit_ids = list(ratings.keys())
    rng = random.Random(seed)
    alphas: list[float] = []
    for _ in range(n_resamples):
        sample_ids = [rng.choice(unit_ids) for _ in unit_ids]
        sample = {f"{uid}#{i}": ratings[uid] for i, uid in enumerate(sample_ids)}
        try:
            a = compute_alpha_for_dimension(sample, metric)
        except InsufficientDataError:
            continue
        if a == a:  # exclude NaN (undefined zero-variance resamples)
            alphas.append(a)
    if not alphas:
        return (float("nan"), float("nan"))
    alphas.sort()
    lower_q = (1 - confidence) / 2
    upper_q = 1 - lower_q
    lower_idx = max(0, int(lower_q * len(alphas)))
    upper_idx = min(len(alphas) - 1, int(upper_q * len(alphas)))
    return (alphas[lower_idx], alphas[upper_idx])


def compute_reliability_result(
    ratings: Ratings,
    dimension_number: int,
    analysis_stage: Literal["pilot", "main_double_coded"],
    corpus: Literal["profile", "job_posting"],
    rulebook_version: str,
    metric: DistanceMetric = "ordinal",
    bootstrap: bool = True,
    seed: int = 42,
) -> KrippendorffResult:
    """One-call convenience wrapper producing a full `KrippendorffResult`
    (alpha, CI, percent agreement, variance) for one dimension.

    Does not interpret the result against the frozen decision
    thresholds (`alcsm.analysis.config.KRIPPENDORFF_MINIMUM_ACCEPTABLE`
    / `_TARGET`) — that interpretation belongs to the caller
    (`alcsm.analysis.rq3_validation`), keeping "compute the statistic"
    and "decide what it means for the rulebook" as separate steps.
    """
    alpha = compute_alpha_for_dimension(ratings, metric)
    ci = bootstrap_alpha_ci(ratings, metric, seed=seed) if bootstrap else (None, None)
    n_units = sum(1 for u in ratings.values() if len(u) >= 2)
    return KrippendorffResult(
        dimension_number=dimension_number,
        analysis_stage=analysis_stage,
        corpus=corpus,
        n_units=n_units,
        krippendorff_alpha=alpha,
        alpha_ci_lower=ci[0],
        alpha_ci_upper=ci[1],
        percent_agreement=percent_agreement(ratings),
        score_variance=score_variance(ratings),
        rulebook_version=rulebook_version,
    )
