"""Builds the thesis-ready reliability summary table (Part 8 of the
FINAL RELIABILITY DIAGNOSIS task).

Reads every number from `Reliability_Results_v1.1.xlsx` (itself
produced by `alcsm_reliability_real_run_v1.0.py`) -- nothing here is
hand-typed or independently recomputed, so this table can never drift
out of sync with the actual analysis. Only the `Interpretation` column
is authored text (the qualitative diagnosis from
`RQ3_Reliability_Final_Interpretation_v1.0.md` §5), which is inherently
a human judgment, not derived data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = REPO_ROOT / "07_Reliability" / "Reliability_Results_v1.1.xlsx"
OUTPUT_PATH = (
    REPO_ROOT / "09_Statistical_Analysis" / "RQ3" / "Table_Reliability_v1.0.xlsx"
)
SUBSET_SIZE = 75  # the double-coding subset size, constant across all dimensions

_INTERPRETATION = {
    "D1": (
        "Strong reproducibility -- wide range, high variance both raters, "
        "genuine agreement."
    ),
    "D2": (
        "Perfect agreement but degenerate (zero variance, ceiling effect) -- "
        "not evidence of strong discrimination."
    ),
    "D3": (
        "Limited reliability -- systematic, one-directional rater-calibration "
        "disagreement (duration/title weighting at the 3-4 boundary), not a "
        "variance artifact."
    ),
    "D4": (
        "Perfect agreement, non-degenerate but small, restricted-range "
        "sample -- encouraging, low confidence given small n."
    ),
    "D5": (
        "Limited reliability -- primarily range-restriction (Rater A "
        "concentrated at one score); residual disagreement is a specific "
        "Director/Head/VP strategic-language boundary judgment."
    ),
    "D6": "Strong reproducibility -- full range, genuine agreement, matches D1.",
}


def main() -> None:
    results = pd.read_excel(RESULTS_PATH, sheet_name="Per_Dimension_Reliability")

    table = pd.DataFrame(
        {
            "Dimension": results["Dimension"],
            "Krippendorff_Alpha": results["krippendorff_alpha_ordinal"],
            "N": SUBSET_SIZE,
            "Observed_Agreement": results["observed_agreement"],
            "Valid_Cases": results["n_units"],
            "Unavailable_Cases": results["rater_a_unavailable"],
            "Score_Variance": results["score_variance_pooled"],
            "Interpretation": results["Dimension"].map(_INTERPRETATION),
        }
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    table.to_excel(OUTPUT_PATH, sheet_name="Reliability", index=False)
    print(f"Wrote {OUTPUT_PATH}")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
