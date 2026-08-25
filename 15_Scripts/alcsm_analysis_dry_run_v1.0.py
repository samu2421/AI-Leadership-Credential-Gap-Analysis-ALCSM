#!/usr/bin/env python3
"""RQ1-RQ5 analysis-infrastructure dry run.

Runs every RQ1-RQ5 module end to end and prints a structured summary,
so the whole analysis pipeline can be proven to work on demand without
ambiguity -- mirrors `05_Data_Collection/Scripts/collection_dry_run.py`'s
role for the collection infrastructure.

Where real (git-ignored) data files are present, this script reads
them -- but every result printed is explicitly labelled with its
`data_status` (`synthetic_fixture` / `provisional_first_pass` /
`final_frozen`), and profile-level ALCSM scores are currently
`provisional_first_pass` (the researcher's review is still in
progress) -- **nothing this script prints is a final thesis finding**.
Where no real data exists yet (RQ4 impact indicators; RQ5 NLP
predictions), it falls back to clearly-labelled constructed fixtures
from `alcsm.annotation.fixtures`-style synthetic data, to prove the
function runs, not to produce a result.

Only aggregate counts/means/tables are ever printed -- no evidence
text, no free-text survey comments, no direct identifiers (the same
discipline this project has followed throughout).

Usage (from the repository root, with the project's virtualenv active):

    python 15_Scripts/alcsm_analysis_dry_run_v1.0.py
"""

from __future__ import annotations

import sys

import pandas as pd

from alcsm.analysis.config import default_analysis_paths
from alcsm.analysis.data_sources import (
    SourceFileNotFoundError,
    load_dimension_evidence,
    load_job_postings_processed,
    load_linkedin_processed,
    load_profile_scores,
    load_review_changes,
    load_survey_raw,
)
from alcsm.analysis.gap import (
    d6_profile_vs_posting_asymmetry,
    not_directly_mapped_report,
    requirement_counts_by_dimension,
    supply_vs_demand_frequency,
)
from alcsm.analysis.rq1_descriptive import (
    company_size_patterns,
    demographic_summary,
    dimension_distribution,
    dimension_level_comparison,
    dimension_missingness,
    industry_patterns,
    title_category_patterns,
)
from alcsm.analysis.rq3_validation import (
    content_validity_summary,
    researcher_review_changes_summary,
)
from alcsm.analysis.rq4 import correlate_with_impact_indicators
from alcsm.analysis.survey import reshape_survey_responses
from alcsm.nlp.evaluate import evaluate_predictions

_SECTION = "=" * 70


def _header(title: str) -> None:
    print(f"\n{_SECTION}\n{title}\n{_SECTION}")


def _status_line(label: str, status: str, extra: str = "") -> None:
    flag = "⚠ PROVISIONAL" if status == "provisional_first_pass" else status.upper()
    print(f"[{flag}] {label}{('  ' + extra) if extra else ''}")


def run_rq1(paths) -> None:
    _header("RQ1 — Credential patterns among AI leaders")
    try:
        linkedin = load_linkedin_processed(paths)
        scores_bundle = load_profile_scores(paths)
        evidence = load_dimension_evidence(paths)
    except SourceFileNotFoundError as exc:
        print(f"Skipped (source not found): {exc}")
        return

    demo = demographic_summary(linkedin.profile_master)
    _status_line("Demographic summary", demo.metadata.data_status)
    print(f"  n_profiles={demo.n_profiles}")
    print(f"  industries observed: {demo.industry_counts.to_dict()}")

    dist = dimension_distribution(
        scores_bundle.scores,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("D1-D6 score distribution", dist.metadata.data_status)
    print(f"  means: {dist.means.round(2).to_dict()}")

    missing = dimension_missingness(
        evidence,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("Missingness by dimension", missing.metadata.data_status)
    print(missing.by_dimension.to_string())

    titles = title_category_patterns(
        linkedin.profile_master,
        scores_bundle.scores,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("Title-category patterns", titles.metadata.data_status)
    print(titles.means.round(2).to_string())

    sizes = company_size_patterns(
        linkedin.profile_master,
        scores_bundle.scores,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("Company-size patterns", sizes.metadata.data_status)
    print(sizes.means.round(2).to_string())

    industries = industry_patterns(
        linkedin.profile_master,
        scores_bundle.scores,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("Industry patterns", industries.metadata.data_status)
    print(industries.means.round(2).to_string())

    comparison = dimension_level_comparison(
        scores_bundle.scores,
        evidence,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line(
        "Dimension-level comparison (not a composite)", comparison.metadata.data_status
    )
    print(comparison.table.round(2).to_string())


def run_rq2(paths) -> None:
    _header("RQ2 — Job requirements vs. held credentials")
    try:
        jobs = load_job_postings_processed(paths)
        scores_bundle = load_profile_scores(paths)
        evidence = load_dimension_evidence(paths)
    except SourceFileNotFoundError as exc:
        print(f"Skipped (source not found): {exc}")
        return

    req_counts = requirement_counts_by_dimension(jobs.requirements)
    _status_line("Requirement counts by dimension", req_counts.metadata.data_status)
    print(f"  n_requirements={req_counts.n_requirements}")

    ndm = not_directly_mapped_report(jobs.requirements)
    _status_line("Not Directly Mapped", ndm.metadata.data_status)
    print(f"  {ndm.n_not_mapped}/{ndm.n_total} ({ndm.fraction_not_mapped:.1%})")

    dist = dimension_distribution(
        scores_bundle.scores,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    freq = supply_vs_demand_frequency(req_counts, dist)
    _status_line(
        "Supply (score) vs. demand (count) frequency", freq.metadata.data_status
    )
    print(freq.table.round(2).to_string())

    d6 = d6_profile_vs_posting_asymmetry(
        scores_bundle.scores,
        evidence,
        jobs.requirements,
        scores_bundle.data_status,
        "review workbook (dry run)",
        acknowledge_provisional=True,
    )
    _status_line("D6 profile-vs-posting asymmetry", d6.metadata.data_status)
    print(
        f"  profile-side coverage: {d6.profile_side_coverage:.1%} "
        f"({d6.n_profiles_with_d6_evidence}/{d6.n_profiles_total})"
    )
    print(
        f"  posting-side coverage: {d6.posting_side_coverage:.1%} "
        f"({d6.n_requirements_d6_mappable}/{d6.n_requirements_total})"
    )

    print(
        "\n  Note: dimension_gap_from_scores() (true mean-required-minus-"
        "mean-held gap) is not run here -- it needs job_requirement_score."
        "required_score data, which does not exist yet. See test_gap.py "
        "for its behaviour against synthetic fixtures."
    )


def run_rq3(paths) -> None:
    _header("RQ3 — ALCSM construction and validation")
    try:
        raw_survey = load_survey_raw(paths)
    except SourceFileNotFoundError as exc:
        print(f"Survey skipped (source not found): {exc}")
    else:
        survey = reshape_survey_responses(raw_survey)
        summary = content_validity_summary(survey)
        _status_line("Content validity summary", summary.metadata.data_status)
        print(f"  n_consented_respondents={summary.n_consented_respondents}")
        print("  relevance means:")
        print(
            summary.relevance_by_dimension[["mean", "n_answered"]].round(2).to_string()
        )
        appropriateness_mean = summary.overall_appropriateness["mean"]
        appropriateness_n = int(summary.overall_appropriateness["n_answered"])
        print(
            f"  overall appropriateness: mean={appropriateness_mean:.2f} "
            f"(n={appropriateness_n})"
        )
        most_important = summary.most_important_dimension_counts.to_dict()
        print(f"  most-important-dimension picks: {most_important}")
        print(
            f"  respondents with a missing-signal comment: "
            f"{summary.n_respondents_with_missing_signal_comment} "
            "(count only -- content is never printed)"
        )

    try:
        review_changes = load_review_changes(paths)
    except SourceFileNotFoundError as exc:
        print(f"Review-changes skipped (source not found): {exc}")
    else:
        rc_summary = researcher_review_changes_summary(review_changes)
        _status_line(
            "Researcher review-change concordance", rc_summary.metadata.data_status
        )
        print(
            f"  n_changes_by_dimension: {rc_summary.n_changes_by_dimension.to_dict()}"
        )
        if rc_summary.n_changes_by_dimension.sum() == 0:
            print("  (no changes recorded yet -- review is still in progress)")

    print(
        "\n  Note: inter_rater_reliability() is not run here -- no real "
        "P4 pilot data exists yet (RATER_A/RATER_B independent scores). "
        "See tests/analysis/test_rq3_validation.py for its behaviour "
        "against synthetic fixtures, including the guard that refuses "
        "to run against the AI-assisted first pass."
    )


def run_rq4() -> None:
    _header("RQ4 — Credential signal vs. observable impact indicators")
    print(
        "No real rq4_impact_indicator data exists yet (no profile has been "
        "loaded into the database -- see P4_Implementation_Completion_"
        "Report.md §3.2). Running against a small constructed fixture to "
        "prove the function works; this is not a finding."
    )
    scores = pd.DataFrame(
        {
            "Profile_ID": [f"PRF-{i:05d}" for i in range(6)],
            **{f"D{n}_Final": [(i + n) % 6 for i in range(6)] for n in range(1, 7)},
        }
    )
    indicators = pd.DataFrame(
        {
            "profile_id": [f"PRF-{i:05d}" for i in range(6)],
            "rq4_network_reach": [10, 20, 30, 40, 50, 60],
            "rq4_content_engagement": [1, 2, 3, 4, 5, 6],
            "rq4_recognition_count": [0, 1, 0, 1, 0, 1],
            "rq4_seniority_progression_rate": [0.1, 0.2, 0.1, 0.3, 0.2, 0.1],
        }
    )
    report = correlate_with_impact_indicators(
        scores, indicators, "synthetic_fixture", "dry-run constructed fixture"
    )
    _status_line("RQ4 correlation (fixture only)", report.metadata.data_status)
    print(report.table.round(2).to_string())


def run_rq5() -> None:
    _header("RQ5 — Human-vs-NLP evaluation")
    print(
        "No trained NLP model exists yet (Phase P7, gated on a frozen "
        "gold standard). Running evaluate_predictions() against a small "
        "constructed fixture to prove the metrics work; this is not a "
        "finding about any real model."
    )
    predictions = pd.DataFrame(
        [
            {
                "profile_id": f"P{i}",
                "dimension_number": n,
                "predicted_score": (i + n) % 6,
            }
            for i in range(6)
            for n in range(1, 7)
        ]
    )
    gold = pd.DataFrame(
        [
            {
                "profile_id": f"P{i}",
                "dimension_number": n,
                "score": (i + n + (1 if i == 0 else 0)) % 6,
            }
            for i in range(6)
            for n in range(1, 7)
        ]
    )
    report = evaluate_predictions(
        predictions, gold, "synthetic_fixture", "dry-run constructed fixture"
    )
    _status_line("NLP evaluation (fixture only)", report.metadata.data_status)
    for dim_n, metrics in report.by_dimension.items():
        print(
            f"  D{dim_n}: exact_match={metrics.exact_match_rate:.2f} "
            f"MAE={metrics.mean_absolute_error:.2f} "
            f"kappa={metrics.linear_weighted_kappa:.2f}"
        )


def main() -> int:
    paths = default_analysis_paths()
    print("ALCSM RQ1-RQ5 analysis infrastructure -- dry run")
    print(f"Repository root: {paths.repo_root}")

    run_rq1(paths)
    run_rq2(paths)
    run_rq3(paths)
    run_rq4()
    run_rq5()

    _header("Done")
    print(
        "Every result above is either a constructed fixture or explicitly "
        "labelled provisional_first_pass. None of it is a final thesis "
        "finding -- see Analysis_Preparation_Completion_Report.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
