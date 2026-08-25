"""Run the P6 double-coding reliability analysis (Part 4/5 of the
FINAL VALIDATION AND ANALYSIS STAGE task).

Usage (once a genuinely independent second-rater file exists):

    python 15_Scripts/alcsm_reliability_subset_analysis_v1.0.py \\
        --second-rater-file path/to/filled_in_rater_b_template.xlsx

Reads the primary researcher's scores directly from the frozen
`06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`, restricted to
the 75-profile subset roster in
`07_Reliability/Double_Coding/ALCSM_Reliability_Subset_75_v1.1.xlsx`,
and compares them against the given second-rater file using
`alcsm.reliability.subset_workflow`. Prints per-dimension (never
pooled) Krippendorff's alpha, 95% bootstrap CI, percent agreement, n,
score distribution, score variance, and unavailable counts.

This script has never been run against real second-rater data in this
repository -- no genuinely independent second rater has coded the
subset yet. Running it with no `--second-rater-file` argument runs it
against the blank template instead, which will correctly report
"insufficient data" for every dimension (a blank template contributes
zero observed scores) -- this is a smoke test of the pipeline itself,
not a reliability result, and is labeled as such in the output.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from alcsm.reliability.subset_workflow import (
    DimensionReliabilitySummary,
    load_primary_scores_long,
    load_second_rater_scores_long,
    run_subset_reliability_analysis,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
SUBSET_ROSTER_PATH = (
    REPO_ROOT
    / "07_Reliability"
    / "Double_Coding"
    / "ALCSM_Reliability_Subset_75_v1.1.xlsx"
)
DEFAULT_BLANK_TEMPLATE = (
    REPO_ROOT / "07_Reliability" / "Double_Coding" / "Rater_A_Blank_Template.xlsx"
)


def _print_summary(summary: DimensionReliabilitySummary) -> None:
    print(f"\n--- D{summary.dimension_number} ---")
    print(f"n_units (dually scored): {summary.n_units}")
    print(f"Krippendorff's alpha (ordinal): {summary.krippendorff_alpha:.4f}")
    if summary.alpha_ci_lower is not None:
        print(
            f"95% bootstrap CI: [{summary.alpha_ci_lower:.4f}, "
            f"{summary.alpha_ci_upper:.4f}]"
        )
    print(f"Percent agreement: {summary.percent_agreement:.4f}")
    print(
        f"Score variance (pooled across both raters' ratings): "
        f"{summary.score_variance:.4f}"
    )
    print(f"Verdict: {summary.verdict}")
    print(f"Primary (RATER_A) score distribution: {summary.primary_score_distribution}")
    print(
        f"Second rater (RATER_B) score distribution: "
        f"{summary.second_rater_score_distribution}"
    )
    print(f"Unavailable (primary): {summary.primary_unavailable_count}")
    print(f"Unavailable (second rater): {summary.second_rater_unavailable_count}")
    print(f"Unavailable (both): {summary.both_unavailable_count}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--second-rater-file",
        type=Path,
        default=DEFAULT_BLANK_TEMPLATE,
        help=(
            "Path to a filled-in Rater_A_Blank_Template.xlsx-shaped file. "
            "Defaults to the still-blank template (pipeline smoke test "
            "only, not a real reliability result)."
        ),
    )
    args = parser.parse_args()

    subset_roster = pd.read_excel(SUBSET_ROSTER_PATH, sheet_name="Subset_Roster")
    subset_profile_ids = set(subset_roster["Profile_ID"])
    assert (
        len(subset_profile_ids) == 75
    ), f"expected the frozen 75-profile subset, found {len(subset_profile_ids)}"

    primary_long = load_primary_scores_long(ANNOTATION_PATH, subset_profile_ids)
    second_rater_long = load_second_rater_scores_long(args.second_rater_file)

    is_blank_run = args.second_rater_file == DEFAULT_BLANK_TEMPLATE
    if is_blank_run:
        print(
            "WARNING: running against the still-blank template. This is a "
            "pipeline smoke test, NOT a reliability result -- no genuine "
            "second-rater data exists yet. Every dimension below is "
            "expected to show 0 dually-scored units."
        )

    results = run_subset_reliability_analysis(
        primary_long,
        second_rater_long,
        subset_profile_ids,
        rulebook_version="v1.1",
        source_description=(
            "P6 double-coding subset (75/500, seed=20260824) -- "
            f"second rater file: {args.second_rater_file.name}"
        ),
    )

    if not results:
        print(
            "\nNo dimension had >=2 dually-scored profiles -- no alpha "
            "could be computed for any dimension. Expected if run against "
            "the blank template; unexpected once a real second-rater file "
            "is supplied."
        )
        return

    for dimension_number in sorted(results):
        _print_summary(results[dimension_number])


if __name__ == "__main__":
    main()
