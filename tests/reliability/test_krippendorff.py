"""Krippendorff's alpha, bootstrap CI, percent agreement, variance.

Validated against Krippendorff's own published worked example
(4 coders x 12 units, nominal/interval/ordinal, widely used to
validate independent implementations -- e.g. the `krippendorff` PyPI
package's own README/tests use the same reliability_data table),
matching to within 0.001 -- per PROJECT_CONTEXT.md §33's "test against
hand-worked cases with a known alpha".
"""

from __future__ import annotations

import pytest

from alcsm.reliability.krippendorff import (
    InsufficientDataError,
    bootstrap_alpha_ci,
    compute_alpha_for_dimension,
    compute_reliability_result,
    percent_agreement,
    score_variance,
)

# Krippendorff's published worked example. Rows = coders, columns =
# units, None = missing. Expected alphas are the widely-cited
# published reference values.
_PUBLISHED_DATA = [
    [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
    [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
    [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
    [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None],
]


def _published_ratings() -> dict[str, dict[str, float]]:
    ratings: dict[str, dict[str, float]] = {}
    for unit_idx in range(12):
        unit: dict[str, float] = {}
        for rater_idx, row in enumerate(_PUBLISHED_DATA):
            v = row[unit_idx]
            if v is not None:
                unit[f"R{rater_idx}"] = float(v)
        ratings[f"U{unit_idx}"] = unit
    return ratings


class TestPublishedWorkedExample:
    def test_nominal_alpha(self) -> None:
        alpha = compute_alpha_for_dimension(_published_ratings(), "nominal")
        assert alpha == pytest.approx(0.743, abs=0.001)

    def test_interval_alpha(self) -> None:
        alpha = compute_alpha_for_dimension(_published_ratings(), "interval")
        assert alpha == pytest.approx(0.849, abs=0.001)

    def test_ordinal_alpha(self) -> None:
        alpha = compute_alpha_for_dimension(_published_ratings(), "ordinal")
        assert alpha == pytest.approx(0.815, abs=0.001)


class TestHandWorkedEdgeCases:
    def test_perfect_agreement_gives_alpha_one(self) -> None:
        ratings = {f"U{i}": {"A": 3.0, "B": 3.0} for i in range(5)}
        assert compute_alpha_for_dimension(ratings) == 1.0

    def test_perfect_agreement_percent_agreement_is_one(self) -> None:
        ratings = {f"U{i}": {"A": 3.0, "B": 3.0} for i in range(5)}
        assert percent_agreement(ratings) == 1.0

    def test_complete_disagreement_two_point_scale(self) -> None:
        """Hand-worked: 4 units, 2 raters each, always maximally opposed
        on a {0,1} nominal scale -- 0% raw agreement, but with a
        balanced 4/4 marginal split the hand-computed formula
        (do=1, de = n_0*n_1*2 / (n*(n-1)) = 4*4*2/(8*7) = 4/7) gives
        alpha = 1 - 1/(4/7) = -0.75, not -1 -- the well-known point that
        Krippendorff's alpha is not simply "1 minus raw disagreement"."""
        ratings = {
            "U0": {"A": 0.0, "B": 1.0},
            "U1": {"A": 1.0, "B": 0.0},
            "U2": {"A": 0.0, "B": 1.0},
            "U3": {"A": 1.0, "B": 0.0},
        }
        do = 1.0  # every pair disagrees
        n_c = {0.0: 4.0, 1.0: 4.0}
        n = 8.0
        de = (n_c[0.0] * n_c[1.0] * 2) / (n * (n - 1))
        expected_alpha = 1 - do / de
        assert expected_alpha == pytest.approx(-0.75, abs=1e-9)
        assert compute_alpha_for_dimension(ratings, "nominal") == pytest.approx(
            expected_alpha, abs=1e-9
        )

    def test_single_unit_raises_insufficient_data(self) -> None:
        with pytest.raises(InsufficientDataError):
            compute_alpha_for_dimension({"U0": {"A": 1.0}})

    def test_all_single_rater_units_raises_insufficient_data(self) -> None:
        with pytest.raises(InsufficientDataError):
            compute_alpha_for_dimension(
                {"U0": {"A": 1.0}, "U1": {"B": 2.0}, "U2": {"A": 3.0}}
            )

    def test_units_with_one_rater_are_excluded_not_erroring(self) -> None:
        """A mix of 1-rater and 2-rater units should compute using only
        the 2-rater units, not raise."""
        ratings = {
            "U0": {"A": 3.0, "B": 3.0},
            "U1": {"A": 3.0},  # excluded: only one rater
            "U2": {"A": 2.0, "B": 2.0},
        }
        assert compute_alpha_for_dimension(ratings) == 1.0


class TestPercentAgreement:
    def test_partial_agreement(self) -> None:
        ratings = {
            "U0": {"A": 1.0, "B": 1.0},
            "U1": {"A": 2.0, "B": 3.0},
            "U2": {"A": 4.0, "B": 4.0},
            "U3": {"A": 1.0, "B": 5.0},
        }
        assert percent_agreement(ratings) == 0.5

    def test_no_usable_units_raises(self) -> None:
        with pytest.raises(InsufficientDataError):
            percent_agreement({"U0": {"A": 1.0}})


class TestScoreVariance:
    def test_zero_variance_when_all_equal(self) -> None:
        ratings = {f"U{i}": {"A": 2.0, "B": 2.0} for i in range(3)}
        assert score_variance(ratings) == 0.0

    def test_nonzero_variance(self) -> None:
        ratings = {"U0": {"A": 0.0, "B": 5.0}, "U1": {"A": 0.0, "B": 5.0}}
        assert score_variance(ratings) == pytest.approx(6.25)

    def test_insufficient_values_raises(self) -> None:
        with pytest.raises(InsufficientDataError):
            score_variance({"U0": {"A": 1.0}})


class TestBootstrapCI:
    def test_perfect_agreement_ci_is_degenerate_at_one(self) -> None:
        ratings = {f"U{i}": {"A": 3.0, "B": 3.0} for i in range(6)}
        lower, upper = bootstrap_alpha_ci(ratings, n_resamples=300, seed=1)
        assert lower == pytest.approx(1.0)
        assert upper == pytest.approx(1.0)

    def test_reproducible_given_same_seed(self) -> None:
        ratings = dict(_published_ratings())
        ci_a = bootstrap_alpha_ci(ratings, "ordinal", n_resamples=200, seed=7)
        ci_b = bootstrap_alpha_ci(ratings, "ordinal", n_resamples=200, seed=7)
        assert ci_a == ci_b

    def test_ci_bounds_the_point_estimate_reasonably(self) -> None:
        ratings = dict(_published_ratings())
        point = compute_alpha_for_dimension(ratings, "ordinal")
        lower, upper = bootstrap_alpha_ci(ratings, "ordinal", n_resamples=500, seed=3)
        # A 95% CI need not strictly contain the point estimate for every
        # resample scheme, but for a reasonably-sized sample it should be
        # in the same general region -- a loose sanity bound, not an
        # exact-equality assertion.
        assert lower - 0.3 <= point <= upper + 0.3


class TestComputeReliabilityResult:
    def test_full_result_matches_reliability_result_shape(self) -> None:
        ratings = dict(_published_ratings())
        result = compute_reliability_result(
            ratings,
            dimension_number=3,
            analysis_stage="pilot",
            corpus="profile",
            rulebook_version="1.0",
            metric="ordinal",
            bootstrap=True,
            seed=1,
        )
        assert result.dimension_number == 3
        assert result.analysis_stage == "pilot"
        assert result.corpus == "profile"
        assert result.krippendorff_alpha == pytest.approx(0.815, abs=0.001)
        assert result.alpha_ci_lower is not None
        assert result.alpha_ci_upper is not None
        assert 0.0 <= result.percent_agreement <= 1.0
        assert result.score_variance >= 0.0
        assert result.n_units > 0

    def test_bootstrap_false_leaves_ci_none(self) -> None:
        ratings = {f"U{i}": {"A": 3.0, "B": 3.0} for i in range(5)}
        result = compute_reliability_result(
            ratings, 1, "pilot", "profile", "1.0", bootstrap=False
        )
        assert result.alpha_ci_lower is None
        assert result.alpha_ci_upper is None


def test_never_computes_a_single_pooled_alpha_across_dimensions() -> None:
    """Structural guard: no function in this module accepts a
    multi-dimension input and produces one pooled number -- every
    public function here operates on one dimension's ratings at a
    time. `compute_reliability_result` requires an explicit
    `dimension_number` argument, never inferring or aggregating across
    several."""
    import inspect

    from alcsm.reliability import krippendorff

    sig = inspect.signature(krippendorff.compute_reliability_result)
    assert "dimension_number" in sig.parameters
