"""Synthetic fixtures for the RQ1-RQ5 analysis test suite.

Every fixture here is constructed, non-personal data (CLAUDE_CODE_
RULES.md rule 6) shaped to match the real workbooks' column layouts
exactly, discovered by inspection during this task (see
`Analysis_Preparation_Completion_Report.md`). No fixture is derived
from, or resembles, any real profile, job posting, or survey
respondent.
"""

from __future__ import annotations

import pandas as pd
import pytest

_PROFILE_IDS = [f"PRF-{i:05d}" for i in range(1, 13)]


@pytest.fixture()
def synthetic_profile_master() -> pd.DataFrame:
    titles = [
        "Head of AI",
        "VP AI",
        "ML Engineer",
        "Data Scientist",
        "CAIO",
        "AI Consultant",
    ]
    industries = ["Technology", "Automotive", "Healthcare", "Financial Services"]
    sizes = ["1-50", "51-200", "201-1000", "1000+"]
    rows = []
    for i, pid in enumerate(_PROFILE_IDS):
        rows.append(
            {
                "Profile_ID": pid,
                "Country": "Germany",
                "Federal_State": ["Bavaria", "Berlin", "Hamburg"][i % 3],
                "City": ["Munich", "Berlin", "Hamburg"][i % 3],
                "Current_Company": f"Company {i}",
                "Industry": industries[i % len(industries)],
                "Company_Size": sizes[i % len(sizes)],
                "Current_Title": titles[i % len(titles)],
                "Current_Role_Start_Date": pd.Timestamp("2022-01-01"),
                "Current_Role_Duration_Months": 12 + i,
                "Title_Category": ["Leadership", "Technical", "Hybrid"][i % 3],
            }
        )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_profile_scores_final() -> pd.DataFrame:
    """All rows reviewed (`Overall_Review_Status != 'Pending Review'`) --
    represents a hypothetically frozen state for testing "final" code paths."""
    rows = []
    for i, pid in enumerate(_PROFILE_IDS):
        scores = [(i + n) % 6 for n in range(6)]
        rows.append(
            {
                "Profile_ID": pid,
                **{f"D{n + 1}_FirstPass": scores[n] for n in range(6)},
                **{f"D{n + 1}_Final": scores[n] for n in range(6)},
                "Completeness_Index": 1.0,
                "Overall_Review_Status": "Reviewed",
                "Reviewer": "TEST_RESEARCHER",
                "Review_Date": pd.Timestamp("2026-08-20"),
                "General_Notes": None,
            }
        )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_profile_scores_provisional(
    synthetic_profile_scores_final: pd.DataFrame,
) -> pd.DataFrame:
    """Same data, but half the rows still show 'Pending Review' -- the
    realistic current state of the real review workbook."""
    df = synthetic_profile_scores_final.copy()
    df.loc[: len(df) // 2, "Overall_Review_Status"] = "Pending Review"
    return df


@pytest.fixture()
def synthetic_dimension_evidence() -> pd.DataFrame:
    rows = []
    statuses = ["present", "present", "present", "unavailable", "absent_stated"]
    for i, pid in enumerate(_PROFILE_IDS):
        for dim_n in range(1, 7):
            rows.append(
                {
                    "Profile_ID": pid,
                    "Dimension": f"D{dim_n}",
                    "FirstPass_Score": (i + dim_n) % 6,
                    "Final_Score": (i + dim_n) % 6,
                    "Evidence": (
                        "fixture evidence text"
                        if statuses[i % 5] != "unavailable"
                        else None
                    ),
                    "Rationale": "fixture rationale",
                    "Missing_Status": statuses[i % 5],
                    "Confidence": ["HIGH", "MEDIUM", "LOW"][i % 3],
                    "Review_Required": "NO",
                    "Reviewer_Decision": None,
                    "Reviewer_Notes": None,
                    "Reviewer": None,
                    "Review_Date": None,
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_review_changes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Profile_ID": "PRF-00001",
                "Dimension": "D5",
                "FirstPass_Score": 4,
                "Final_Score": 2,
                "Change_Reason": "Title alone does not substantiate strategic scope",
                "Governing_Rule": "D5 criteria",
                "Precedent": "P-03",
                "Reviewer": "TEST_RESEARCHER",
                "Review_Date": pd.Timestamp("2026-08-20"),
            },
            {
                "Profile_ID": "PRF-00002",
                "Dimension": "D2",
                "FirstPass_Score": 1,
                "Final_Score": 2,
                "Change_Reason": "Certification confirmed current",
                "Governing_Rule": "D2 recency",
                "Precedent": None,
                "Reviewer": "TEST_RESEARCHER",
                "Review_Date": pd.Timestamp("2026-08-20"),
            },
            {
                "Profile_ID": "PRF-00003",
                "Dimension": "D5",
                "FirstPass_Score": 3,
                "Final_Score": 3,
                "Change_Reason": "Confirmed correct on review",
                "Governing_Rule": "D5 criteria",
                "Precedent": "P-02",
                "Reviewer": "TEST_RESEARCHER",
                "Review_Date": pd.Timestamp("2026-08-20"),
            },
        ]
    )


@pytest.fixture()
def empty_review_changes() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "Profile_ID",
            "Dimension",
            "FirstPass_Score",
            "Final_Score",
            "Change_Reason",
            "Governing_Rule",
            "Precedent",
            "Reviewer",
            "Review_Date",
        ]
    )


@pytest.fixture()
def synthetic_job_master() -> pd.DataFrame:
    rows = []
    for i in range(1, 9):
        rows.append(
            {
                "Job_ID": f"JOB-{i:05d}",
                "Company_Name": f"Employer {i}",
                "Industry": ["Technology", "Automotive"][i % 2],
                "Company_Size": ["1-50", "1000+"][i % 2],
                "Federal_State": "Bavaria",
                "City": "Munich",
                "Job_Title": "Head of AI",
                "Job_Title_Category": "Leadership",
                "Seniority_Level": "Senior",
                "Employment_Type": "Full-time",
                "Remote_Status": "Hybrid",
                "AI_Leadership_Role": "Yes",
                "Requirement_Info_Available": "Yes",
                "Requires_Education": "Yes",
                "Requires_Certification": "No",
                "Requires_AI_Experience": "Yes",
                "Requires_Technical_Skills": "Yes",
                "Requires_Business_Strategy": "Yes",
                "Requires_Governance_Knowledge": "No",
            }
        )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_requirements() -> pd.DataFrame:
    dims = [
        "D1 - Formal Education",
        "D2 - Professional Certifications",
        "D3 - Practical AI Experience",
        "D4 - Technical Contributions",
        "D5 - Leadership & Strategic Responsibility",
        "D6 - AI Industry/Application Breadth",
        "NOT_DIRECTLY_MAPPED",
    ]
    rows = []
    rid = 1
    for job_i in range(1, 9):
        for dim_i, dim in enumerate(dims):
            # skew so "NOT_DIRECTLY_MAPPED" and D5 dominate, D6 is rare --
            # mirrors the real corpus's actual shape.
            n_reqs = (
                3
                if dim == "NOT_DIRECTLY_MAPPED"
                else (2 if dim_i == 4 else (1 if dim_i != 5 else 0))
            )
            for _ in range(n_reqs):
                rows.append(
                    {
                        "Requirement_ID": f"JR{rid:04d}",
                        "Job_ID": f"JOB-{job_i:05d}",
                        "Requirement_Text": "Fixture requirement text",
                        "Requirement_Category": "Leadership Experience",
                        "Mandatory_or_Preferred": "Mandatory",
                        "Final_ALCSM_Dimension": dim,
                    }
                )
                rid += 1
    # add exactly one D6-mapped requirement so D6 asymmetry has a nonzero
    # posting-side numerator to test against.
    rows.append(
        {
            "Requirement_ID": f"JR{rid:04d}",
            "Job_ID": "JOB-00001",
            "Requirement_Text": "Experience across multiple industries",
            "Requirement_Category": "Leadership Experience",
            "Mandatory_or_Preferred": "Preferred",
            "Final_ALCSM_Dimension": "D6 - AI Industry/Application Breadth",
        }
    )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_required_scores() -> pd.DataFrame:
    """Shaped like `job_requirement_score` -- does not exist for real yet."""
    rows = []
    for dim_n in range(1, 7):
        for i in range(5):
            rows.append(
                {
                    "dimension_number": dim_n,
                    "required_score": (dim_n + i) % 6,
                    "missing_status": "present",
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_held_scores() -> pd.DataFrame:
    """Shaped like `v_final_profile_score` -- does not exist for real yet."""
    rows = []
    for dim_n in range(1, 7):
        for i in range(10):
            rows.append(
                {
                    "dimension_number": dim_n,
                    "score": (dim_n + i + 1) % 6,
                    "missing_status": "present",
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_impact_indicators() -> pd.DataFrame:
    rows = []
    for i, pid in enumerate(_PROFILE_IDS):
        rows.append(
            {
                "profile_id": pid,
                "rq4_network_reach": 100 * (i + 1),
                "rq4_content_engagement": 2.5 * (i + 1),
                "rq4_recognition_count": i % 4,
                "rq4_seniority_progression_rate": 0.1 * (i + 1),
            }
        )
    return pd.DataFrame(rows)


# `synthetic_predictions`/`synthetic_gold` (needed by both
# `tests/analysis/` and `tests/nlp/test_evaluate.py`) now live in the
# root `tests/conftest.py`, since a directory-local `conftest.py`'s
# fixtures are not visible outside that directory's subtree.

# ---------------------------------------------------------------------
# Expert survey -- constructed to match the raw Google Forms export's
# exact column headers (see alcsm.analysis.survey's module constants),
# never resembling the real respondents' data.
# ---------------------------------------------------------------------

_DIM_LABELS = {
    1: "D1 — Formal Education",
    2: "D2 — Professional Certifications",
    3: "D3 — Practical AI Experience",
    4: "D4 — Technical Contributions",
    5: "D5 — Leadership & Strategic Responsibility",
    6: "D6 — AI Industry/Application Breadth",
}


@pytest.fixture()
def synthetic_survey_raw() -> pd.DataFrame:
    # Matches the real export's structure: the relevance question's
    # actual column text STARTS with this framing sentence, not with
    # "Please rate..." (that phrase appears only at the very end, right
    # before the "[Dn -- Label]" bracket) -- see
    # `Analysis_Preparation_Completion_Report.md` for the exact real
    # column text this fixture was corrected to match.
    relevance_prefix = (
        "For each dimension, please rate how relevant it is as an "
        "observable credential signal when assessing AI leadership."
    )
    clarity_prefix = (
        "How clear and distinct is this dimension as a component of the "
        "AI leadership credential-signal framework?"
    )
    distinctiveness_prefix = (
        "How distinct is this dimension from the other dimensions in the framework?"
    )

    relevance_labels = {
        1: "1 — Not at all relevant",
        2: "5 — Extremely relevant",
        3: "3 — Moderately relevant",
        4: "2 — Slightly relevant",
        5: "4 — Very relevant",
        6: "5 — Extremely relevant",
    }
    clarity_labels = {
        1: "Clear / clearly distinct",
        2: "Very clear / highly distinct",
        3: "Moderately clear / moderately distinct",
        4: "Somewhat unclear / weakly distinct",
        5: "Clear / clearly distinct",
        6: "Very clear / highly distinct",
    }

    columns: dict[str, list] = {
        "Timestamp": [],
        "I have read the information above and I voluntarily agree to participate.": [],
        "Which best describes your primary professional role?": [],
        "How many years of professional work experience do you have?": [],
        (
            "How many years of experience do you have specifically in AI, "
            "data, or related technology fields?"
        ): [],
        (
            "Do you have experience leading, managing, or hiring for "
            "AI/technology roles or teams?"
        ): [],
    }
    for n in range(1, 7):
        columns[f"{relevance_prefix} [{_DIM_LABELS[n]}]"] = []
    for n in range(1, 7):
        columns[f"{clarity_prefix} [{_DIM_LABELS[n]}]"] = []
    columns[
        "Overall, how appropriate is the six-dimensional ALCSM framework "
        "for assessing observable AI leadership credential signals?"
    ] = []
    columns[
        "Which of the six dimensions do you consider MOST important when "
        "assessing AI leadership credential signals?"
    ] = []
    columns[
        "Is there any important credential signal associated with AI "
        "leadership that you believe is missing from the current "
        "six-dimensional framework?"
    ] = []
    for n in range(1, 7):
        columns[f"{distinctiveness_prefix} [{_DIM_LABELS[n]}]"] = []

    n_respondents = 6
    appropriateness_choices = [
        "3 — Moderately appropriate",
        "4 — Very appropriate",
        "5 — Extremely appropriate",
    ]
    most_important_choices = [_DIM_LABELS[3], _DIM_LABELS[6], _DIM_LABELS[5]]

    for i in range(n_respondents):
        columns["Timestamp"].append(pd.Timestamp("2026-08-01") + pd.Timedelta(days=i))
        # Respondent 0 did not consent -- must be excluded downstream.
        columns[
            "I have read the information above and I voluntarily agree to participate."
        ].append("No" if i == 0 else "Yes, I agree to participate")
        columns["Which best describes your primary professional role?"].append(
            "AI/ML practitioner or engineer"
        )
        columns["How many years of professional work experience do you have?"].append(
            "3–5 years"
        )
        columns[
            "How many years of experience do you have specifically in AI, "
            "data, or related technology fields?"
        ].append("1–3 years")
        columns[
            "Do you have experience leading, managing, or hiring for "
            "AI/technology roles or teams?"
        ].append("Some experience")
        for n in range(1, 7):
            columns[f"{relevance_prefix} [{_DIM_LABELS[n]}]"].append(
                relevance_labels[n]
            )
            columns[f"{clarity_prefix} [{_DIM_LABELS[n]}]"].append(clarity_labels[n])
            columns[f"{distinctiveness_prefix} [{_DIM_LABELS[n]}]"].append(None)
        columns[
            "Overall, how appropriate is the six-dimensional ALCSM framework "
            "for assessing observable AI leadership credential signals?"
        ].append(appropriateness_choices[i % 3])
        columns[
            "Which of the six dimensions do you consider MOST important "
            "when assessing AI leadership credential signals?"
        ].append(most_important_choices[i % 3])
        columns[
            "Is there any important credential signal associated with AI "
            "leadership that you believe is missing from the current "
            "six-dimensional framework?"
        ].append("Fixture comment text." if i == 1 else None)

    return pd.DataFrame(columns)
