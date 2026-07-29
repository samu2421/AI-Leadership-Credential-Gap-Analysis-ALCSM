"""Fixed reference vocabulary shared across the codebase.

These constants mirror the frozen reference tables `dimension_ref` and
`missing_status_ref` (PROJECT_CONTEXT.md §15). They are vocabulary, not
scoring logic: no function in this module computes or implies a score.

FROZEN — do not add, remove, or rename dimensions or missing-status
states here. Any such change is a methodology change and requires
author approval (CLAUDE_CODE_RULES.md rule 1).
"""

from __future__ import annotations

from typing import Literal, NamedTuple

DimensionCode = Literal[
    "d1_education",
    "d2_certifications",
    "d3_experience",
    "d4_contributions",
    "d5_leadership",
    "d6_engagement",
]

MissingStatus = Literal[
    "present",
    "absent_stated",
    "unavailable",
    "not_applicable",
]

SCORE_MIN = 0
SCORE_MAX = 5

# Dimension for which external verification is permitted (confirm/lower
# only, never raise beyond the profile text — PROJECT_CONTEXT.md §10, §17).
EXTERNAL_VERIFICATION_DIMENSION: DimensionCode = "d4_contributions"


class DimensionRef(NamedTuple):
    number: int
    code: DimensionCode
    label: str
    verifiability: str


# Order and content are fixed by ALCSM_Measurement_Specification_v1.0
# (see 02_Framework_Development/). Never reorder, add, or remove rows.
DIMENSIONS: tuple[DimensionRef, ...] = (
    DimensionRef(1, "d1_education", "Formal Education", "high"),
    DimensionRef(2, "d2_certifications", "Professional Certifications", "high"),
    DimensionRef(3, "d3_experience", "Practical AI Experience", "medium"),
    DimensionRef(4, "d4_contributions", "Technical Contributions", "medium-high"),
    DimensionRef(5, "d5_leadership", "Leadership & Strategic Responsibility", "low"),
    DimensionRef(
        6,
        "d6_engagement",
        "Professional Engagement & Continuous Development",
        "low-medium",
    ),
)

# `not_applicable` is valid for job postings only, never for profiles
# (PROJECT_CONTEXT.md §9).
MISSING_STATUSES: tuple[MissingStatus, ...] = (
    "present",
    "absent_stated",
    "unavailable",
    "not_applicable",
)

# The fifteen binding precedent identifiers (PROJECT_CONTEXT.md §12).
# Full ruling text lives only in the `precedent_ref` database table,
# loaded from docs/rulebook — never duplicated here.
PRECEDENT_IDS: tuple[str, ...] = tuple(f"P-{i:02d}" for i in range(1, 16))

# The seven raw profile sections (PROJECT_CONTEXT.md §15), matching the
# `profile_raw_section.section_name` CHECK constraint in
# schema/alcsm_schema_v1.0.1.sql exactly. Long-format storage, one row
# per section, each with an explicit availability flag (PROJECT_CONTEXT.md §9).
ProfileSectionName = Literal[
    "headline",
    "about",
    "experience",
    "education",
    "certifications",
    "contributions",
    "activity",
]

PROFILE_SECTIONS: tuple[ProfileSectionName, ...] = (
    "headline",
    "about",
    "experience",
    "education",
    "certifications",
    "contributions",
    "activity",
)

# Controlled vocabulary for `profile.inclusion_reason`, matching the
# schema's CHECK constraint exactly.
InclusionReason = Literal[
    "title_match",
    "title_variant_match",
    "manual_review_included",
]

INCLUSION_REASONS: tuple[InclusionReason, ...] = (
    "title_match",
    "title_variant_match",
    "manual_review_included",
)
