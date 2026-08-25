"""Expert-survey descriptive analysis (Part 6 of the FINAL VALIDATION
AND ANALYSIS STAGE task).

Reuses the existing, already-tested `alcsm.analysis.survey` (reshape)
and `alcsm.analysis.rq3_validation.content_validity_summary` modules
unchanged -- this script only orchestrates them against the real,
current 23-respondent survey export and writes a processed,
analysis-ready copy under `07_Reliability/Survey_Analysis/`.

Read-only against the source: `07_Reliability/Survey_Responses/01_Raw/
ALCSM_Expert_Survey_Responses_v1.0.xlsx` is never modified.

Scope (see `Survey_Analysis_Plan_v1.0.md` for the full statement):
descriptive statistics only. Not predictive validation, not competence
validation, not population inference, not internal consistency, not
factor analysis. No Cronbach's alpha anywhere. No weights derived from
the most-important-dimension question.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from alcsm.analysis.rq3_validation import content_validity_summary
from alcsm.analysis.survey import (
    participant_background_summary,
    reshape_survey_responses,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_SURVEY_PATH = (
    REPO_ROOT
    / "07_Reliability"
    / "Survey_Responses"
    / "01_Raw"
    / "ALCSM_Expert_Survey_Responses_v1.0.xlsx"
)
OUTPUT_DIR = REPO_ROOT / "07_Reliability" / "Survey_Analysis"
OUTPUT_PATH = OUTPUT_DIR / "ALCSM_Survey_Analysis_Processed_v1.0.xlsx"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = pd.read_excel(RAW_SURVEY_PATH, sheet_name="Form responses 1")
    survey = reshape_survey_responses(raw)
    print(f"n_respondents (raw rows): {survey.n_respondents}")
    print(f"n_consented: {survey.n_consented}")

    background = participant_background_summary(survey)
    content = content_validity_summary(
        survey, source_description=str(RAW_SURVEY_PATH.relative_to(REPO_ROOT))
    )

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        pd.DataFrame(
            {
                "Field": ["n_respondents_raw", "n_consented", "data_status"],
                "Value": [
                    survey.n_respondents,
                    survey.n_consented,
                    content.metadata.data_status,
                ],
            }
        ).to_excel(writer, sheet_name="Overview", index=False)

        for field_name, series in background.items():
            series.rename_axis(field_name).reset_index(name="n").to_excel(
                writer, sheet_name=f"Background_{field_name}"[:31], index=False
            )

        content.relevance_by_dimension.to_excel(writer, sheet_name="Relevance")
        content.clarity_by_dimension.to_excel(writer, sheet_name="Clarity")
        content.distinctiveness_by_dimension.to_excel(
            writer, sheet_name="Distinctiveness"
        )
        content.overall_appropriateness.rename("value").to_frame().to_excel(
            writer, sheet_name="Overall_Appropriateness"
        )
        content.most_important_dimension_counts.rename_axis("dimension").reset_index(
            name="n"
        ).to_excel(writer, sheet_name="Most_Important_Dimension", index=False)
        pd.DataFrame(
            {
                "Field": ["n_respondents_with_missing_signal_comment", "n_consented"],
                "Value": [
                    content.n_respondents_with_missing_signal_comment,
                    survey.n_consented,
                ],
            }
        ).to_excel(writer, sheet_name="Missing_Signal_Comment_Count", index=False)

    print(f"Wrote {OUTPUT_PATH}")
    print(
        "\nNOTE: free-text comment CONTENT was never read into this script or its "
        "output -- only the count of respondents who left a missing-signal "
        "comment. Thematic coding of comment content is a separate, manual, "
        "qualitative step for the researcher (see Survey_Analysis_Plan_v1.0.md)."
    )


if __name__ == "__main__":
    main()
