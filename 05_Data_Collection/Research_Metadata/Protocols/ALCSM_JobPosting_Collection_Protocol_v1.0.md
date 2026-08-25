# ALCSM Job Posting Collection Protocol

**Version:** 1.0
**Status:** Draft — governance-layer research documentation. Study population and eligibility criteria are finalized (§3, §6, §7). Does not itself authorize data collection.
**Document type:** Research protocol (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This protocol documents how the job posting dataset for the ALCSM study is identified, screened, and collected, at a level of detail sufficient for another researcher to understand and reproduce the process independent of the software used to execute it.

## 2. Scope

This protocol covers the collection of publicly accessible AI-leadership job postings. It covers identification, screening, and transcription of posting content into the research dataset. It does not cover the use of that content to anchor taxonomy term lists, which is governed by separate documentation.

## 3. Target Population

### 3.1 Study Population Statement

The study population comprises publicly available AI leadership job advertisements published by organizations operating in Germany that describe leadership, strategic, managerial, or organizational responsibilities related to artificial intelligence or closely related domains.

The unit of analysis is the posting's stated requirements, not the identity of the posting organization or any individual associated with it.

### 3.2 Scope Conditions

- **Geographic scope.** Germany is the geographic scope of the study population. Geographic scope is defined by organizational operation, not by the organization's headquarters location.
- **Organizational scope.** An organization need not be headquartered in Germany to qualify; it is sufficient that the organization operates in Germany. A posting for a German operation of a non-German-headquartered organization is within scope on the same basis as a posting from a German-headquartered organization.
- **Publicity requirement.** Only postings that are publicly accessible without requiring account registration, application submission, or payment are collected. No content gated behind an application step is used to establish eligibility or to populate the dataset.
- **Role and responsibility basis.** Eligibility is established through the posting's stated title and responsibilities, per the finalized eligibility criteria (§6) and the AI Leadership Title Dictionary (§6.1), mirroring the basis applied to the LinkedIn dataset (see `ALCSM_Relationships_v1.0.md` for the independence of the two datasets during collection).

## 4. Sampling Frame

Purposive, title-based sampling, structurally mirroring the LinkedIn profile dataset's sampling approach so that the two datasets remain comparable at the level of role/title, while being collected independently (see `ALCSM_Relationships_v1.0.md`). The frame is the set of postings returned by a pre-registered set of searches across pre-registered source platforms.

## 5. Collection Workflow

At a research-process level, collection proceeds as follows:

1. A candidate posting is identified through a pre-registered search on a pre-registered source platform.
2. The posting is screened against the inclusion and exclusion criteria (§§6–7).
3. If included, the posting is assigned an identifier at the point of capture, and its full text is transcribed verbatim, including a separately identifiable requirements section where the posting structure allows it.
4. Provenance information (source, search query, result position, posting date where available, collection timestamp) is recorded alongside the transcribed content.
5. Any incidentally identifying information about an individual recruiter (name, contact details) is not transcribed. The unit of analysis is the posting's requirements, not the poster.
6. The record is validated against the dataset's structural and completeness requirements before being finalized as part of the dataset.

Collection is manual and human-driven throughout. No automated retrieval, scraping, or browser automation is used at any step.

## 6. Inclusion Criteria

The finalized inclusion criteria (IC-J01–IC-J06) are defined in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` §3.2, and are referenced here rather than duplicated. Criteria are pre-registered and fixed before collection begins and are not adjusted mid-collection; any future revision is recorded there as a new version.

### 6.1 Supporting Reference Documents

- **`ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`** — the finalized Tier 1/Tier 2/Tier 3 title vocabulary applied under IC-J03, shared with the LinkedIn dataset for comparability between corpora.
- **`ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md`** — the ordered screening procedure formalized for LinkedIn profiles. The equivalent sequence (accessibility → geography → title → leadership scope → uniqueness/verifiability) applies to job postings using the IC-J/EC-J criteria in §3.2–3.3 above; a posting-specific decision tree has not been separately formalized in this version.

## 7. Exclusion Criteria

The finalized exclusion criteria (EC-J01–EC-J07) are defined in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` §3.3, and are referenced here rather than duplicated.

## 8. Quality Control

- Every collected posting is checked for structural completeness (non-empty verbatim text, required provenance fields present) before being finalized.
- A sample of each collection batch is independently re-checked against the source posting for transcription fidelity.
- Postings are screened for incidental recruiter-identifying content before finalization.
- See `ALCSM_Data_Quality_Guidelines_v1.0.md` for the full set of data quality principles applied to this dataset.

## 9. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial draft of the job posting collection protocol, with eligibility criteria left as placeholders pending finalization. | Samiksha Dhere |
| 1.0 (Step 3 update) | 2026-08-02 | Finalized the study population statement (§3) and replaced the inclusion/exclusion criteria placeholders (§6, §7) with references to the finalized `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` and `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`. | Samiksha Dhere |

---

*This document is a research protocol. It does not define or alter any software implementation, database schema, or ALCSM scoring methodology.*
