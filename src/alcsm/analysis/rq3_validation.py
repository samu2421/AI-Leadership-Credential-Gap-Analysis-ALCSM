"""RQ3 — How can ALCSM be constructed and validated?

Four structurally distinct pieces of evidence, kept in separate
functions and separate result types so none can be mistaken for
another:

1. **Content validity** (`content_validity_summary`) — expert-survey
   ratings of relevance/clarity/distinctiveness per dimension.
2. **Inter-rater reliability** (`inter_rater_reliability`) — Krippendorff's
   alpha, per dimension, computed ONLY over genuine independent human
   raters (`RATER_A`/`RATER_B`/`ADJUDICATOR`, per `alcsm.annotation.
   seed`). **This function refuses to run if any rater id it is given
   is not on that allow-list** — the explicit purpose of that check is
   this task's own instruction: "Do not calculate reliability against
   the current AI first-pass dataset as if it were human gold
   standard." No real inter-rater data exists yet (the P4 pilot has
   not run); this function is ready and tested against synthetic
   fixtures.
3. **Researcher review-change concordance** (`researcher_review_changes_
   summary`) — how often, and in what direction, the researcher's
   final score differs from the AI-assisted first pass. This is
   deliberately NOT called "reliability" or "agreement" anywhere in
   its name, docstring, or fields, and it never touches Krippendorff's
   alpha — it is a process-transparency metric about one reviewer's
   revisions to a machine-generated draft, not a statement about
   inter-rater reliability between two independent human coders.
4. **Missingness** (`dimension_missingness`, reused directly from
   `rq1_descriptive` — RQ3's missingness question is the same
   question RQ1 already answers, not a second implementation of it).

`ALCSM_Measurement_Model_and_Validation_Note.md` §2 is the underlying
frame: content validity and (once real pilot data exists) reliability
are the two principal validation routes for this formative index —
never Cronbach's alpha, never pooled across dimensions.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import pandas as pd

from alcsm.analysis.config import (
    KRIPPENDORFF_MINIMUM_ACCEPTABLE,
    KRIPPENDORFF_TARGET,
    AnalysisRunMetadata,
    make_metadata,
)
from alcsm.analysis.survey import ReshapedSurvey
from alcsm.constants import DIMENSIONS
from alcsm.reliability.krippendorff import (
    InsufficientDataError,
    KrippendorffResult,
    Ratings,
    compute_reliability_result,
)

# The only rater ids this module will accept as genuine independent
# human raters (alcsm.annotation.seed._RATERS). Anything else --
# including any id containing "first", "pass", "ai", "draft" -- is
# refused, which is exactly the guard this task's explicit
# instruction requires.
_ALLOWED_HUMAN_RATER_IDS = {"RATER_A", "RATER_B"}


class NotAHumanRaterError(ValueError):
    """Raised when `inter_rater_reliability` is given a rater id that is
    not a registered independent human rater -- most importantly, this
    catches an AI-assisted first-pass id being mistaken for a second
    "rater", which this task explicitly forbids."""


# ---------------------------------------------------------------------
# 1. Content validity (expert survey)
# ---------------------------------------------------------------------


@dataclass(frozen=True)
class ContentValiditySummary:
    metadata: AnalysisRunMetadata
    n_consented_respondents: int
    relevance_by_dimension: pd.DataFrame  # index=D1..D6, columns=[mean, median, n]
    clarity_by_dimension: pd.DataFrame
    distinctiveness_by_dimension: pd.DataFrame
    overall_appropriateness: pd.Series  # descriptive stats: mean/median/n
    most_important_dimension_counts: pd.Series
    n_respondents_with_missing_signal_comment: int


def _ratings_summary_table(ratings: list, item_type: str) -> pd.DataFrame:
    rows = []
    for d in DIMENSIONS:
        values = [
            r.value
            for r in ratings
            if r.dimension_number == d.number
            and r.item_type == item_type
            and r.value is not None
        ]
        n_answered = sum(
            1
            for r in ratings
            if r.dimension_number == d.number and r.item_type == item_type
        )
        series = pd.Series(values, dtype=float)
        rows.append(
            {
                "dimension": f"D{d.number}",
                "mean": series.mean() if len(series) else float("nan"),
                "median": series.median() if len(series) else float("nan"),
                "n_answered": len(values),
                "n_total": n_answered,
            }
        )
    return pd.DataFrame(rows).set_index("dimension")


def content_validity_summary(
    survey: ReshapedSurvey,
    source_description: str = "Expert survey (Google Forms export)",
) -> ContentValiditySummary:
    """Per-dimension relevance/clarity/distinctiveness ratings, overall
    framework-appropriateness, and most-important-dimension picks.

    Free text is not part of this summary at all -- only the count of
    respondents who left a missing-signal comment
    (`n_respondents_with_missing_signal_comment`), never its content.
    """
    appropriateness_values = [
        r.overall_appropriateness
        for r in survey.respondents
        if r.overall_appropriateness is not None
    ]
    most_important_counts = pd.Series(
        [
            r.most_important_dimension
            for r in survey.respondents
            if r.most_important_dimension
        ]
    ).value_counts()
    return ContentValiditySummary(
        metadata=make_metadata("final_frozen", source_description),
        n_consented_respondents=survey.n_consented,
        relevance_by_dimension=_ratings_summary_table(survey.ratings, "relevance"),
        clarity_by_dimension=_ratings_summary_table(survey.ratings, "clarity"),
        distinctiveness_by_dimension=_ratings_summary_table(
            survey.ratings, "distinctiveness"
        ),
        overall_appropriateness=pd.Series(
            {
                "mean": (
                    pd.Series(appropriateness_values, dtype=float).mean()
                    if appropriateness_values
                    else float("nan")
                ),
                "median": (
                    pd.Series(appropriateness_values, dtype=float).median()
                    if appropriateness_values
                    else float("nan")
                ),
                "n_answered": len(appropriateness_values),
                "n_total": survey.n_consented,
            }
        ),
        most_important_dimension_counts=most_important_counts,
        n_respondents_with_missing_signal_comment=sum(
            1 for ft in survey.free_text_presence if ft.has_missing_signal_comment
        ),
    )


# ---------------------------------------------------------------------
# 2. Inter-rater reliability (human raters only)
# ---------------------------------------------------------------------


@dataclass(frozen=True)
class ReliabilityVerdict:
    """One dimension's Krippendorff's alpha plus the frozen decision-rule
    interpretation (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §16 item 9)."""

    result: KrippendorffResult
    verdict: str  # 'proceed' | 'acceptable_with_review' | 'revise_rulebook_wording'


def _interpret_alpha(alpha: float) -> str:
    if alpha != alpha:  # NaN
        return "undefined"
    if alpha >= KRIPPENDORFF_TARGET:
        return "proceed"
    if alpha >= KRIPPENDORFF_MINIMUM_ACCEPTABLE:
        return "acceptable_with_review"
    return "revise_rulebook_wording"


@dataclass(frozen=True)
class InterRaterReliabilityReport:
    metadata: AnalysisRunMetadata
    by_dimension: dict[int, ReliabilityVerdict]


def inter_rater_reliability(
    ratings_by_dimension: dict[int, Ratings],
    analysis_stage: str,
    corpus: str,
    rulebook_version: str,
    source_description: str,
) -> InterRaterReliabilityReport:
    """Krippendorff's alpha per dimension, over independent human raters
    only, each dimension interpreted against the frozen decision rule.

    Raises :class:`NotAHumanRaterError` if any rater id appearing
    anywhere in ``ratings_by_dimension`` is not in the registered
    human-rater allow-list (`RATER_A`, `RATER_B`) -- this is the
    concrete mechanism behind "do not calculate reliability against
    the current AI first-pass dataset as if it were human gold
    standard": an AI-assisted first-pass id (or any id not explicitly
    registered as a human rater) cannot pass this check no matter what
    it is named.
    """
    for dimension_number, ratings in ratings_by_dimension.items():
        for unit_ratings in ratings.values():
            for rater_id in unit_ratings:
                if rater_id not in _ALLOWED_HUMAN_RATER_IDS:
                    allowed = sorted(_ALLOWED_HUMAN_RATER_IDS)
                    raise NotAHumanRaterError(
                        f"rater id {rater_id!r} (dimension {dimension_number}) "
                        f"is not a registered independent human rater "
                        f"({allowed}). Inter-rater reliability must never be "
                        "computed against the AI-assisted first pass or any "
                        "other non-human source."
                    )

    by_dimension: dict[int, ReliabilityVerdict] = {}
    for d in DIMENSIONS:
        ratings = ratings_by_dimension.get(d.number, {})
        try:
            result = compute_reliability_result(
                ratings, d.number, analysis_stage, corpus, rulebook_version  # type: ignore[arg-type]
            )
        except InsufficientDataError:
            continue
        by_dimension[d.number] = ReliabilityVerdict(
            result=result, verdict=_interpret_alpha(result.krippendorff_alpha)
        )
    return InterRaterReliabilityReport(
        metadata=make_metadata("synthetic_fixture", source_description),
        by_dimension=by_dimension,
    )


# ---------------------------------------------------------------------
# 3. Researcher review-change concordance (NOT a reliability statistic)
# ---------------------------------------------------------------------


@dataclass(frozen=True)
class ReviewChangeConcordance:
    """Deliberately not named "agreement" or "reliability" anywhere --
    see module docstring item 3. `n_changes` may legitimately be 0 if
    the researcher has not yet recorded any change (an empty
    `Review_Changes` sheet is a valid, expected state early in
    review, not an error)."""

    metadata: AnalysisRunMetadata
    n_changes_by_dimension: pd.Series  # index=D1..D6
    mean_absolute_change_by_dimension: pd.Series
    direction_counts: (
        pd.DataFrame
    )  # index=D1..D6, columns=[increased, decreased, unchanged]
    precedent_usage_counts: pd.Series


def researcher_review_changes_summary(
    review_changes: pd.DataFrame, source_description: str = "Review_Changes sheet"
) -> ReviewChangeConcordance:
    """Summarize what the researcher actually changed relative to the
    AI-assisted first pass: counts per dimension, mean absolute score
    change, direction of change, and which precedents were cited.

    Reads `Review_Changes` exactly as-is; an empty sheet produces an
    all-zero summary, not an error (Human_Annotation_Review_Protocol_
    v1.1.md §9: populated only once changes actually occur).
    """
    dims = [f"D{d.number}" for d in DIMENSIONS]
    if review_changes.empty:
        empty_counts = pd.Series(0, index=dims)
        empty_direction = pd.DataFrame(
            0, index=dims, columns=["increased", "decreased", "unchanged"]
        )
        return ReviewChangeConcordance(
            metadata=make_metadata("provisional_first_pass", source_description),
            n_changes_by_dimension=empty_counts,
            mean_absolute_change_by_dimension=pd.Series(float("nan"), index=dims),
            direction_counts=empty_direction,
            precedent_usage_counts=pd.Series(dtype=int),
        )

    rc = review_changes.copy()
    rc["dimension_label"] = rc["Dimension"].apply(
        lambda x: x if str(x).startswith("D") else f"D{x}"
    )
    rc["delta"] = rc["Final_Score"] - rc["FirstPass_Score"]

    n_changes = rc.groupby("dimension_label").size().reindex(dims, fill_value=0)
    mean_abs_change = rc.groupby("dimension_label")["delta"].apply(
        lambda s: s.abs().mean()
    )
    mean_abs_change = mean_abs_change.reindex(dims)

    direction = pd.DataFrame(
        0, index=dims, columns=["increased", "decreased", "unchanged"]
    )
    for dim, group in rc.groupby("dimension_label"):
        direction.loc[dim, "increased"] = int((group["delta"] > 0).sum())
        direction.loc[dim, "decreased"] = int((group["delta"] < 0).sum())
        direction.loc[dim, "unchanged"] = int((group["delta"] == 0).sum())

    precedent_counts = rc["Precedent"].dropna().value_counts()

    return ReviewChangeConcordance(
        metadata=make_metadata("provisional_first_pass", source_description),
        n_changes_by_dimension=n_changes,
        mean_absolute_change_by_dimension=mean_abs_change,
        direction_counts=direction,
        precedent_usage_counts=precedent_counts,
    )


def ratings_from_dimension_evidence(
    dimension_evidence_by_rater: dict[str, pd.DataFrame],
) -> dict[int, Ratings]:
    """Build the `{dimension_number: {unit_id: {rater_id: value}}}` shape
    `inter_rater_reliability` expects, from one Dimension_Evidence-shaped
    DataFrame per rater (columns: `Profile_ID`, `Dimension`, `Score`).

    A convenience adapter for pilot data shaped like the P4 annotation
    interface's export (`alcsm.annotation.reliability_export`), so a
    caller does not have to hand-build the nested dict.
    """
    by_dimension: dict[int, dict[str, dict[str, float]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for rater_id, df in dimension_evidence_by_rater.items():
        for row in df.itertuples(index=False):
            dim_number = int(str(row.Dimension).lstrip("D"))
            by_dimension[dim_number][row.Profile_ID][rater_id] = float(row.Score)
    return {k: dict(v) for k, v in by_dimension.items()}
