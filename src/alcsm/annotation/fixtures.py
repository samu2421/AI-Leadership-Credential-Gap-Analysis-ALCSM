"""Constructed, non-personal profile fixtures for the P4 dry run and tests.

Never real data (CLAUDE_CODE_RULES.md rule 6; CLAUDE_CODE_IMPLEMENTATION
_GUIDE.md §11: "No test may contain real personal data; use
constructed fixtures"). Reuses, rather than reinvents, the four
constructed composites already established and approved in
``ALCSM_v1.0_Scoring_Framework_Task3.md`` §4 and restated for D6 v1.1
in ``ALCSM_v1.1_Scoring_Framework.md`` §4 -- the same "Substantiated AI
Leader" / "Titleholder Without Substantiated Leadership" / "Under-
Signaled Practitioner" / "Sparse/Low-Completeness Profile" composites,
with the exact same D1-D6 values those documents already worked out
and disclosed as fully constructed, never-real illustrations. A fifth
profile is added purely to exercise D6's higher breadth bands (4-5
distinct industries), which none of the original four reach.

``PRF-9####`` is used throughout (a block no real collection would
plausibly reach at this project's ~500-profile scale) so a fixture ID
is visually distinguishable from a real one on sight, in addition to
being synthetic by construction.
"""

from __future__ import annotations

from datetime import UTC, datetime

from alcsm.collection.helper import ProfileRecord, ProfileSection, SamplingBatch

SYNTHETIC_SAMPLING_BATCH = SamplingBatch(
    sampling_batch_id="BATCH-FIXTURE-001",
    search_query='"AI Leader" OR "Head of AI" (constructed fixture, not a real search)',
    platform="linkedin",
    collection_started_ts=datetime(2026, 1, 1, tzinfo=UTC),
    inclusion_protocol_version="fixture-1.0",
    corpus="profile",
    collection_ended_ts=datetime(2026, 1, 1, tzinfo=UTC),
    result_set_size=5,
    records_included=5,
    notes="Synthetic fixture batch for P4 dry runs and tests only.",
)


def _profile(profile_id: str, headline: str, about: str) -> ProfileRecord:
    return ProfileRecord(
        profile_id=profile_id,
        sampling_batch_id=SYNTHETIC_SAMPLING_BATCH.sampling_batch_id,
        search_query=SYNTHETIC_SAMPLING_BATCH.search_query,
        inclusion_reason="title_match",
        collection_ts=datetime(2026, 1, 2, tzinfo=UTC),
        sections={
            "headline": ProfileSection(available=True, text=headline),
            "about": ProfileSection(available=True, text=about),
            "experience": ProfileSection(
                available=True, text="(fixture experience text)"
            ),
            "education": ProfileSection(
                available=True, text="(fixture education text)"
            ),
            "certifications": ProfileSection(
                available=True, text="(fixture certifications text)"
            ),
            "contributions": ProfileSection(available=False, text=None),
            "activity": ProfileSection(available=False, text=None),
        },
        profile_language="en",
        profile_geography="DE",
    )


PROFILE_A_SUBSTANTIATED_LEADER = _profile(
    "PRF-90001",
    "VP of AI, Enterprise Strategy",
    "Leading AI strategy across the enterprise. MSc AI. AWS ML Specialty, "
    "TensorFlow Developer certified. 5+ years building and deploying ML "
    "systems with clear ownership language.",
)
PROFILE_B_TITLEHOLDER = _profile(
    "PRF-90002",
    "Chief AI Officer",
    "Chief AI Officer. General project-management background; no AI-specific "
    "achievements described. BSc Computer Science, no AI specialization. One "
    "expired certification.",
)
PROFILE_C_UNDER_SIGNALED = _profile(
    "PRF-90003",
    "Machine Learning Engineer",
    "Built and deployed several production ML systems over 4 years with "
    "clear ownership language. No certifications listed. Minimal public "
    "posting activity.",
)
PROFILE_D_SPARSE = _profile(
    "PRF-90004",
    "Data Scientist",
    "(minimal profile text; most sections not retrieved at collection)",
)
PROFILE_E_HIGH_BREADTH = _profile(
    "PRF-90005",
    "AI Consultant",
    "AI consulting engagements spanning automotive, healthcare, financial "
    "services, and manufacturing clients over a multi-year career.",
)

SYNTHETIC_PROFILES: tuple[ProfileRecord, ...] = (
    PROFILE_A_SUBSTANTIATED_LEADER,
    PROFILE_B_TITLEHOLDER,
    PROFILE_C_UNDER_SIGNALED,
    PROFILE_D_SPARSE,
    PROFILE_E_HIGH_BREADTH,
)

# D1-D6 first-pass-style scores for each fixture profile, matching
# ALCSM_v1.1_Scoring_Framework.md §4 exactly for A-D; E is a new,
# purpose-built high-D6-breadth case (not in that table).
# missing_status is 'present' unless noted; Profile D uses 'unavailable'
# for its three "(missing)" dimensions per that table's own annotation.
FIXTURE_SCORES: dict[str, dict[int, tuple[int, str]]] = {
    "PRF-90001": {
        1: (4, "present"),
        2: (3, "present"),
        3: (4, "present"),
        4: (4, "present"),
        5: (4, "present"),
        6: (3, "present"),
    },
    "PRF-90002": {
        1: (2, "present"),
        2: (1, "present"),
        3: (1, "present"),
        4: (0, "unavailable"),
        5: (5, "present"),
        6: (1, "present"),
    },
    "PRF-90003": {
        1: (3, "present"),
        2: (0, "unavailable"),
        3: (4, "present"),
        4: (3, "present"),
        5: (1, "present"),
        6: (2, "present"),
    },
    "PRF-90004": {
        1: (0, "unavailable"),
        2: (0, "unavailable"),
        3: (1, "present"),
        4: (0, "unavailable"),
        5: (2, "present"),
        6: (0, "unavailable"),
    },
    "PRF-90005": {
        1: (2, "present"),
        2: (1, "present"),
        3: (3, "present"),
        4: (1, "present"),
        5: (2, "present"),
        6: (5, "present"),
    },
}

FIXTURE_EVIDENCE: dict[int, str] = {
    1: "MSc AI (fixture evidence text)",
    2: "AWS ML Specialty (fixture evidence text)",
    3: "5+ years building and deploying ML systems (fixture evidence text)",
    4: "co-authored paper, linked GitHub (fixture evidence text)",
    5: "VP of AI, enterprise strategy language (fixture evidence text)",
    6: "occasional original commentary (fixture evidence text)",
}


def all_fixture_profile_ids() -> tuple[str, ...]:
    return tuple(p.profile_id for p in SYNTHETIC_PROFILES)
