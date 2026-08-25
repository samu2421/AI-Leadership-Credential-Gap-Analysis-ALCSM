# ALCSM LinkedIn Profile Collection Protocol

**Version:** 1.0
**Status:** Draft — governance-layer research documentation. Study population and eligibility criteria are finalized (§3, §6, §7); search strategy (§5) remains a placeholder. Does not itself authorize data collection.
**Document type:** Research protocol (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This protocol documents how the LinkedIn profile dataset for the ALCSM study is identified, screened, and collected, at a level of detail sufficient for another researcher to understand and reproduce the process independent of the software used to execute it.

## 2. Scope

This protocol covers the collection of publicly visible LinkedIn profile content for individuals presenting a qualifying AI-leadership title. It covers identification, screening, and transcription of profile content into the research dataset. It does not cover annotation or scoring of collected profiles, which is governed by separate documentation.

## 3. Target Population

### 3.1 Study Population Statement

The study population comprises AI leadership professionals employed in organizations operating in Germany who publicly present leadership responsibilities related to artificial intelligence, machine learning, advanced analytics, or AI strategy on their LinkedIn profiles.

This population is deliberately narrower than "all individuals in AI leadership roles" — the frame is defined by what a profile publicly states, not by an independent assessment of the individual's actual role or capability.

### 3.2 Scope Conditions

- **Geographic scope.** Germany is the geographic scope of the study population. Geographic scope is defined by organizational operation, not by the individual's personal location or nationality.
- **Organizational scope.** An organization need not be headquartered in Germany to qualify; it is sufficient that the organization operates in Germany (e.g. through a German office, subsidiary, or registered entity). An individual employed by a non-German-headquartered organization's German operations is within scope on the same basis as an individual employed by a German-headquartered organization.
- **Publicity requirement.** Only information that is publicly available on the individual's LinkedIn profile, without requiring a connection or login beyond the permitted browsing fallback, is collected. No private, connection-gated, or otherwise access-restricted content is used to establish eligibility or to populate the dataset.
- **Title and responsibility basis.** Eligibility is established through the individual's presented job title and publicly stated responsibilities, per the finalized eligibility criteria (§6) and the AI Leadership Title Dictionary (§6.1). It is not established through any assessment of the individual's underlying competence.

## 4. Sampling Strategy

Purposive, title-based sampling. Profiles enter the dataset by matching a pre-registered set of qualifying title strings, not through random or probability-based selection. The sampling strategy, including target sample size and batch structure, is documented in full in the collection protocol governing the software implementation of this process.

## 5. Search Strategy

*[PLACEHOLDER — to be finalized during Step 3]*

The exact search platforms, query strings, filters, and per-query quotas used to identify candidate profiles are not yet finalized. This section will record, once fixed:

- The platform surface(s) used for search.
- The exact, pre-registered query strings.
- Any filters applied (e.g. geography, language).
- The per-query target count.
- The collection window during which searches were run.

## 6. Inclusion Criteria

The finalized inclusion criteria (IC-01–IC-08) are defined in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` §2.2, and are referenced here rather than duplicated. Criteria are pre-registered and fixed before collection begins and are not adjusted mid-collection; any future revision is recorded there as a new version.

### 6.1 Supporting Reference Documents

- **`ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`** — the finalized Tier 1/Tier 2/Tier 3 title vocabulary applied under IC-03 and IC-04.
- **`ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md`** — the ordered screening procedure applying these criteria to each candidate profile.

## 7. Exclusion Criteria

The finalized exclusion criteria (EC-01–EC-08) are defined in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` §2.3, and are referenced here rather than duplicated.

## 8. Data Collection Workflow

At a research-process level, collection proceeds as follows:

1. A candidate profile is identified through the search strategy (§5).
2. The profile is screened against the inclusion and exclusion criteria (§§6–7).
3. If included, the profile is assigned a pseudonymous identifier at the point of capture. No name, profile URL, photograph, or contact detail is recorded at any stage.
4. Defined profile sections are transcribed verbatim by a human collector. A section that is not retrievable is recorded as such, distinct from a section the profile owner has left empty — this distinction is preserved rather than collapsed.
5. Provenance information (search query, result position, inclusion reason, collection timestamp) is recorded alongside the transcribed content.
6. The record is validated against the dataset's structural and completeness requirements before being finalized as part of the dataset.

Collection is manual and human-driven throughout. No automated retrieval, scraping, or browser automation is used at any step.

## 9. Quality Assurance

- Every collected record is checked for structural completeness (required provenance fields present) before being finalized.
- A sample of each collection batch is independently re-checked against the source profile for transcription fidelity.
- See `ALCSM_Data_Quality_Guidelines_v1.0.md` for the full set of data quality principles applied to this dataset.

## 10. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial draft of the LinkedIn profile collection protocol, with search strategy and eligibility criteria left as placeholders pending finalization. | Samiksha Dhere |
| 1.0 (Step 3 update) | 2026-08-02 | Finalized the study population statement (§3) and replaced the inclusion/exclusion criteria placeholders (§6, §7) with references to the finalized `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md`, `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`, and `ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md`. Search strategy (§5) remains a placeholder. | Samiksha Dhere |

---

*This document is a research protocol. It does not define or alter any software implementation, database schema, or ALCSM scoring methodology.*
