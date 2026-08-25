"""Versioned dimension display/rubric configuration for the P4 UI.

Two things must never be confused with each other:

- ``alcsm.constants.DIMENSIONS`` is the FROZEN, DB-aligned vocabulary
  (``dimension_code``, matching ``dimension_ref.dimension_code`` and
  the schema's CHECK constraints exactly). It is not touched by this
  module and must never be edited to reflect a proposed rubric change
  — doing so would silently rewrite frozen vocabulary
  (CLAUDE_CODE_RULES.md rule 1).
- This module is the DISPLAY/rubric-text layer the annotation UI reads
  from. It is deliberately versioned so a proposed dimension revision
  (D6 v1.1, see ``02_Framework_Development/ALCSM_D6_Industry_Breadth_
  v1.1.md`` and ``DECISION_LOG.md`` D-0038, status PROPOSED/PILOT_
  REQUIRED) can be shown to a reviewer without editing the frozen
  vocabulary or any other UI code, and can be swapped back to v1.0 or
  forward to a future v1.2 by changing one setting.

D1-D5 are identical across every version below (`ALCSM_v1.1_Scoring_
Framework.md` restates them unchanged). Only D6 differs between "v1_0"
and "v1_1". No rubric text here is invented — every criterion string
is copied from the frozen/proposed source documents, never
paraphrased or summarised into a different meaning.
"""

from __future__ import annotations

from dataclasses import dataclass

from alcsm.constants import DimensionCode

RUBRIC_CRITERIA = tuple[str, str, str, str, str, str]  # scores 0..5, as text


@dataclass(frozen=True)
class DimensionDefinition:
    """Display-facing definition of one dimension, for one config version.

    ``dimension_code`` still matches the frozen DB vocabulary
    (``alcsm.constants.DIMENSIONS``) even when the *label*/*definition*
    describe a proposed revision — the underlying database row
    (``dimension_ref``) is not changed until the author formally
    freezes a revision (DECISION_LOG.md D-0038 §"Consequences").
    """

    number: int
    code: DimensionCode
    label: str
    definition: str
    verifiability: str
    criteria: RUBRIC_CRITERIA
    is_proposed: bool
    source_doc: str


# ---------------------------------------------------------------------
# v1.0 — frozen (ALCSM_Measurement_Specification_v1.0.md,
# ALCSM_v1.0_Scoring_Framework_Task3.md §1). D1-D5 criteria are shared
# verbatim by every config version below.
# ---------------------------------------------------------------------

_D1 = DimensionDefinition(
    1,
    "d1_education",
    "Formal Education",
    "Credentialed foundational AI/quantitative literacy.",
    "high",
    (
        "No higher education, or unrelated field",
        "Bachelor's, adjacent field, no AI coursework",
        "Bachelor's CS/quant, no AI specialization",
        "Bachelor's + AI specialization, or Master's adjacent",
        "Master's AI/ML/DS, or PhD adjacent quant",
        "PhD CS/AI/ML with AI-specific research",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md",
)
_D2 = DimensionDefinition(
    2,
    "d2_certifications",
    "Professional Certifications",
    "Renewable, lower-cost competence signals.",
    "high",
    (
        "None listed",
        "One expired/low-credibility cert",
        "One current recognized-vendor cert",
        "2+ current general certs",
        "Multiple current AI/ML-specific certs",
        "Multiple AI/ML certs + actively maintained professional body credential",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md",
)
_D3 = DimensionDefinition(
    3,
    "d3_experience",
    "Practical AI Experience",
    "Self-described applied AI/ML role history (depth/tenure, not breadth).",
    "medium",
    (
        "No AI/ML roles",
        "AI-adjacent role only",
        "1-2 yrs explicit AI/ML role, IC scope",
        "3+ yrs AI/ML, or 1-2 yrs with ownership language",
        "Multi-yr, multi-role, ownership escalation",
        "Sustained multi-yr AI/ML leadership, deployed systems at scale",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md",
)
_D4 = DimensionDefinition(
    4,
    "d4_contributions",
    "Technical Contributions",
    "Visible, partly verifiable technical output.",
    "medium-high",
    (
        "None discoverable",
        "Non-technical public content only",
        "One verifiable technical artifact",
        "Multiple artifacts, unverified",
        "Multiple artifacts, >=1 externally verifiable",
        "Sustained, externally verifiable output (pubs/patents/high-engagement OSS)",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md",
)
_D5 = DimensionDefinition(
    5,
    "d5_leadership",
    "Leadership & Strategic Responsibility",
    "Positional + strategic-framing leadership signal.",
    "low",
    (
        "Individual contributor, no leadership language",
        "Team lead/informal only",
        "Manager-level, team-scope",
        "Director/Head, some strategic language",
        "VP/senior, explicit enterprise-strategy scope",
        "C-level/CAIO-equivalent, strategic AND augmentation-aware framing",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md",
)

_D6_V1_0 = DimensionDefinition(
    6,
    "d6_engagement",
    "Professional Engagement & Continuous Development",
    "Ongoing reputational/engagement activity (post-level activity evidence).",
    "low-medium",
    (
        "No visible engagement",
        "Passive engagement (likes/shares) only",
        "Regular passive engagement, no original content",
        "Occasional original commentary",
        "Regular original commentary + community membership",
        "Sustained thought leadership, community leadership role",
    ),
    False,
    "ALCSM_Measurement_Specification_v1.0.md §2.6 (retired for pilot; "
    "see DECISION_LOG.md D-0038)",
)

# ---------------------------------------------------------------------
# v1.1 — proposed, D6 only (ALCSM_D6_Industry_Breadth_v1.1.md,
# ALCSM_v1.1_Scoring_Framework.md §1). Status PROPOSED/PILOT_REQUIRED
# (DECISION_LOG.md D-0038) -- shown as such by `is_proposed=True`, and
# the UI must surface that flag, never present it as final.
# ---------------------------------------------------------------------

_D6_V1_1 = DimensionDefinition(
    6,
    "d6_engagement",  # DB code unchanged -- see module docstring
    "AI Industry/Application Breadth",
    "The breadth of distinct industries or application domains in which an "
    "individual has observable AI-related professional experience. Not a "
    "measure of competence or leadership effectiveness -- an observable "
    "credential signal only.",
    "medium",
    (
        "No AI-related experience with identifiable industry context",
        "Exactly one distinct industry/application domain",
        "Exactly two distinct industries/application domains",
        "Exactly three distinct industries/application domains",
        "Exactly four distinct industries/application domains",
        "Five or more distinct industries/application domains",
    ),
    True,
    "ALCSM_D6_Industry_Breadth_v1.1.md §3, §7 (PROPOSED/PILOT_REQUIRED, "
    "DECISION_LOG.md D-0038)",
)

_CONFIG_V1_0: tuple[DimensionDefinition, ...] = (_D1, _D2, _D3, _D4, _D5, _D6_V1_0)
_CONFIG_V1_1: tuple[DimensionDefinition, ...] = (_D1, _D2, _D3, _D4, _D5, _D6_V1_1)

_VERSIONS: dict[str, tuple[DimensionDefinition, ...]] = {
    "v1_0": _CONFIG_V1_0,
    "v1_1": _CONFIG_V1_1,
}

# The version the annotation UI loads unless a caller explicitly asks
# for another one. Changing this line is how a future proposed
# revision becomes the UI's default *display* — it never touches
# `alcsm.constants` or the database. Currently v1_1 because that is
# what the first-pass annotation and researcher-review layer already
# use (`ALCSM_Full_FirstPass_Annotation_v1.1.xlsx`, `ALCSM_Final_Human_
# Annotation_v1.1_REVIEW.xlsx`).
DEFAULT_VERSION = "v1_1"


def available_versions() -> tuple[str, ...]:
    """Every dimension-config version this module knows about."""
    return tuple(_VERSIONS.keys())


def get_dimension_config(
    version: str = DEFAULT_VERSION,
) -> tuple[DimensionDefinition, ...]:
    """Return the six dimension definitions for ``version``, in order 1-6.

    Raises ``KeyError`` with the available versions listed if
    ``version`` is not recognised, rather than silently falling back
    -- a typo in a version string must never quietly serve the wrong
    rubric to a reviewer.
    """
    try:
        return _VERSIONS[version]
    except KeyError as exc:
        raise KeyError(
            f"unknown dimension-config version {version!r}; "
            f"available: {sorted(_VERSIONS)}"
        ) from exc


def get_dimension(number: int, version: str = DEFAULT_VERSION) -> DimensionDefinition:
    """Return one dimension's definition (1-6) for ``version``."""
    for d in get_dimension_config(version):
        if d.number == number:
            return d
    raise KeyError(f"no dimension numbered {number!r} (must be 1-6)")
