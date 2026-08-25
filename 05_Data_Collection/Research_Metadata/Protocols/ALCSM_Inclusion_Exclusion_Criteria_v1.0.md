# ALCSM Inclusion and Exclusion Criteria

**Version:** 1.0
**Status:** Final for Step 3 — governance-layer research documentation. Pre-registered; not to be adjusted after collection begins without a dated, documented revision.
**Document type:** Research protocol (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This document consolidates the finalized inclusion and exclusion criteria for both ALCSM datasets. Criteria are stated as objective, observable conditions applied to publicly available profile or posting content; none depends on an assessment of the individual's or organization's actual capability, only on what is publicly presented. Criteria are pre-registered and fixed before collection begins and are not adjusted mid-collection; any future revision is recorded as a new version with a dated rationale, per §5.

Criteria numbering follows: `IC` (inclusion criteria, LinkedIn), `EC` (exclusion criteria, LinkedIn), `IC-J` (inclusion criteria, job postings), `EC-J` (exclusion criteria, job postings).

---

## 2. LinkedIn Profiles

### 2.1 Study Population

AI leadership professionals employed in organizations operating in Germany who publicly present leadership responsibilities related to artificial intelligence, machine learning, advanced analytics, or AI strategy on their LinkedIn profiles. See `ALCSM_LinkedIn_Collection_Protocol_v1.0.md` §3 for the full population statement and its scope conditions.

### 2.2 Inclusion Criteria

| ID | Criterion | Mandatory | Reason |
|---|---|---|---|
| IC-01 | The profile is publicly accessible under LinkedIn's default view settings, without requiring a connection request or account access beyond the permitted logged-out/logged-in-fallback browsing policy. | Yes | Ensures only publicly observable information is collected, consistent with the study's legal basis and the "publicly available information only" principle. |
| IC-02 | The organization associated with the individual's current role has a verifiable operating presence in Germany (headquarters, office, or registered entity), regardless of the organization's global headquarters location. | Yes | Establishes the study's geographic scope as organizational operation in Germany, not organizational nationality. |
| IC-03 | The individual's current job title matches a Tier 1 (Core) entry in `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`. | Yes, unless IC-04 applies | Provides an objective, title-based entry point to the study population that does not depend on subjective assessment. |
| IC-04 | Where the current job title matches a Tier 2 (Conditional) entry in `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`, manual review of the profile's publicly stated content confirms explicit, observable evidence of AI-related leadership responsibility. | Yes, unless IC-03 applies | Extends coverage to plausible but title-ambiguous cases while bounding judgement to a single, documented review step. |
| IC-05 | The profile's publicly stated content evidences leadership, strategic, managerial, or organizational responsibility, as distinct from a purely individual-contributor technical role. | Yes | Operationalizes "leadership" as the population criterion, consistent with the study's focus on leadership credential signal. |
| IC-06 | The leadership responsibility evidenced under IC-05 relates to artificial intelligence, machine learning, advanced analytics, or AI strategy. | Yes | Operationalizes the AI-domain scope of the study population. |
| IC-07 | The profile's content is presented in a language the research team can accurately read and transcribe. | Yes | Ensures transcription fidelity and coding accuracy. |
| IC-08 | The profile represents a unique individual not already represented by another record in the dataset. | Yes | Prevents duplicate representation of the same individual, preserving the integrity of population-level analysis. |

### 2.3 Exclusion Criteria

| ID | Criterion | Mandatory | Reason |
|---|---|---|---|
| EC-01 | The profile is not publicly accessible under default view settings (requires a connection or login access beyond the permitted browsing fallback). | Yes | Mirrors IC-01; a profile that cannot be viewed publicly cannot be collected under the study's legal basis. |
| EC-02 | The organization associated with the individual's current role has no verifiable operating presence in Germany. | Yes | Mirrors IC-02; enforces the geographic scope of the study population. |
| EC-03 | The individual's current job title does not match a Tier 1 entry, and either does not match a Tier 2 entry or fails manual review under IC-04. | Yes | Enforces the title-based population boundary defined by the Title Dictionary. |
| EC-04 | The profile describes an individual-contributor technical role with no evidence of leadership, strategic, managerial, or organizational scope. | Yes | Mirrors IC-05; excludes technical individual contributors regardless of AI-domain relevance. |
| EC-05 | The profile represents a company page, product page, or other non-person entity rather than a natural person. | Yes | The unit of analysis is an individual's presented credential signal; non-person pages cannot present one. |
| EC-06 | The profile is a duplicate of an individual already represented elsewhere in the dataset. | Yes | Mirrors IC-08; prevents double-counting. |
| EC-07 | The profile's content is not available in a language the research team can accurately transcribe and evaluate. | Yes | Mirrors IC-07; protects transcription and coding fidelity. |
| EC-08 | The qualifying title identified is a past or former position rather than the individual's current role. | Yes | Restricts the dataset to present-day presented credential signal, consistent with the study's cross-sectional design. |

---

## 3. Job Postings

### 3.1 Study Population

Publicly available AI leadership job advertisements published by organizations operating in Germany that describe leadership, strategic, managerial, or organizational responsibilities related to artificial intelligence or closely related domains. See `ALCSM_JobPosting_Collection_Protocol_v1.0.md` §3 for the full population statement and its scope conditions.

### 3.2 Inclusion Criteria

| ID | Criterion | Mandatory | Reason |
|---|---|---|---|
| IC-J01 | The posting is publicly accessible without requiring account registration, application submission, or payment to view the full text. | Yes | Ensures only publicly available information is collected. |
| IC-J02 | The posting organization has a verifiable operating presence in Germany, regardless of global headquarters location. | Yes | Establishes the study's geographic scope, mirroring IC-02. |
| IC-J03 | The posting's title or role description matches a Tier 1 entry in `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md`, or a Tier 2 entry confirmed via review of the posting's stated responsibilities. | Yes | Applies the same objective title-based screening used for the LinkedIn dataset, for comparability between corpora. |
| IC-J04 | The posting describes leadership, strategic, managerial, or organizational responsibility for AI, ML, advanced analytics, or a closely related domain, rather than a purely individual-contributor technical role. | Yes | Operationalizes the "leadership" scope of the study population for the posting corpus. |
| IC-J05 | The posting is active (open for application) at the time of collection, or its original posting date and active status are otherwise verifiable. | Yes | Ensures the posting reflects a genuine, dated statement of requirements rather than an unverifiable or archival listing. |
| IC-J06 | The posting's content is presented in a language the research team can accurately read and transcribe. | Yes | Ensures transcription fidelity, mirroring IC-07. |

### 3.3 Exclusion Criteria

| ID | Criterion | Mandatory | Reason |
|---|---|---|---|
| EC-J01 | The posting is not publicly accessible under default view settings. | Yes | Mirrors IC-J01. |
| EC-J02 | The posting organization has no verifiable operating presence in Germany. | Yes | Mirrors IC-J02. |
| EC-J03 | The role described is individual-contributor in scope, with no leadership, strategic, managerial, or organizational responsibility. | Yes | Mirrors IC-J04. |
| EC-J04 | The posting is a duplicate or substantially identical re-post of a posting already represented in the dataset (same organization, same role, materially identical text). | Yes | Prevents double-counting of a single underlying requirement statement. |
| EC-J05 | The posting is expired, withdrawn, or otherwise no longer active at the time of collection, with no independently verifiable original posting date. | Yes | Mirrors IC-J05; prevents inclusion of undated or unverifiable content. |
| EC-J06 | The posting is a general recruitment-agency advertisement not tied to one specific, identifiable employing organization and role. | Yes | The unit of analysis is a specific role's requirements; an agency's general pitch does not represent one. |
| EC-J07 | The posting's content is not available in a language the research team can accurately transcribe and evaluate. | Yes | Mirrors IC-J06. |

---

## 4. Application Notes

- These criteria are applied in the order set out in `ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md` for LinkedIn profiles. An equivalent ordered application applies to job postings, following the same sequence of accessibility → geography → title → leadership scope → uniqueness/verifiability.
- Every exclusion is logged with the specific criterion identifier (e.g. `EC-03`) applied, per `ALCSM_Data_Quality_Guidelines_v1.0.md` §8 (audit trail).
- The Tier 2 manual-review step referenced in IC-04 and IC-J03 is the only point of judgement permitted in the screening process; it is bounded to the review question stated in `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md` §4 and does not extend to any other criterion.

## 5. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Finalized study population statements and full inclusion/exclusion criteria (IC-01–IC-08, EC-01–EC-08, IC-J01–IC-J06, EC-J01–EC-J07) for both datasets, completing the Step 2 structural placeholder. | Samiksha Dhere |

---

*This document defines the finalized eligibility criteria for both ALCSM datasets. It does not alter the frozen ALCSM scoring methodology or database schema.*
