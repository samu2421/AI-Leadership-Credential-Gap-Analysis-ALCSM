# ALCSM AI Leadership Title Dictionary

**Version:** 1.0
**Status:** Final for Step 3 — governance-layer research documentation.
**Document type:** Reference document (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This dictionary defines the job-title vocabulary used to identify candidate LinkedIn profiles and job postings for the ALCSM study population. It is a sampling-frame instrument: it determines which title strings bring a candidate record into the eligibility-screening process. It governs collection only.

**Relationship to the ALCSM scoring framework.** This dictionary is structurally and conceptually distinct from the frozen ALCSM leadership-level taxonomy that governs Dimension 5 (Leadership & Strategic Responsibility) scoring. The scoring taxonomy assigns a leadership-seniority score to an already-collected profile; this dictionary determines whether a profile is collected at all. Using this dictionary to inform how a profile is later scored would introduce circularity between sampling and measurement and is expressly out of scope. The two vocabularies are maintained independently.

## 2. Tier Structure

Titles are organized into three tiers, corresponding to the confidence with which a title alone indicates membership in the study population.

| Tier | Purpose |
|---|---|
| **Tier 1 — Core** | Titles that unambiguously indicate AI-related leadership responsibility on their face. A Tier 1 title match is sufficient, on its own, to proceed to the remaining eligibility criteria (organizational and geographic scope, public accessibility). No review of profile content is required to establish title-based eligibility. |
| **Tier 2 — Conditional** | Titles that plausibly indicate AI-related leadership responsibility but are ambiguous without further evidence — either because the title is generic (e.g. spans domains beyond AI) or because seniority/scope cannot be determined from the title string alone. A Tier 2 title match requires manual review of the profile's publicly stated responsibilities (headline, about, or experience section) before an inclusion decision is made, per `ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md`. |
| **Tier 3 — Excluded** | Titles that do not, on their own or through reasonable extension, indicate AI-related leadership responsibility. A Tier 3 title match does not proceed to manual review and is excluded at the title-screening step. |

A title not listed in any tier is treated as Tier 3 (excluded) by default, consistent with the principle that inclusion requires positive, observable evidence rather than the absence of a disqualifying signal.

## 3. Tier 1 — Core AI Leadership Titles

| Title |
|---|
| Chief AI Officer |
| Chief Data Officer |
| Chief Data Scientist |
| Chief Analytics Officer |
| Chief Machine Learning Officer |
| VP of Artificial Intelligence |
| VP of Machine Learning |
| VP of Data Science |
| VP of AI / VP of AI & ML |
| VP of Data & Analytics |
| Head of Artificial Intelligence |
| Head of Machine Learning |
| Head of Data Science |
| Head of AI Strategy |
| Head of Advanced Analytics |
| Director of Artificial Intelligence |
| Director of Machine Learning |
| Director of Data Science |
| Director of AI Strategy |
| Director of Advanced Analytics |
| Global Head of AI |
| Senior Director of Artificial Intelligence |

German-language equivalents encountered during collection (e.g. "Leiter/-in Künstliche Intelligenz," "Direktor/-in Data Science") are treated as Tier 1 where they are direct translations of a listed title; the translation mapping applied is recorded in the collection log at the time of use, per `ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md`.

## 4. Tier 2 — Conditional Titles Requiring Manual Review

| Title | Basis for Conditional Status |
|---|---|
| Chief Technology Officer (CTO) | Broad title; AI-specific responsibility must be evidenced in profile content. |
| Chief Executive Officer (CEO) | Broad title; applies only where the organization's AI focus and the individual's AI-strategy responsibility are both evidenced. |
| Director of Data | Generic; AI/ML-specific scope must be evidenced. |
| Head of Analytics | Generic; "advanced analytics" scope per the study population definition must be evidenced. |
| Director of Digital Transformation | AI-specific component of the transformation mandate must be evidenced. |
| Head of Innovation | AI-specific component of the innovation mandate must be evidenced. |
| Director of Technology | Generic; AI/ML-specific leadership scope must be evidenced. |
| VP of Engineering | AI/ML-specific engineering scope must be evidenced, as distinct from general software engineering leadership. |
| AI Lead / ML Lead | Title does not by itself establish leadership (as opposed to individual-contributor "lead") scope; must be evidenced. |
| Principal Data Scientist | Seniority label is IC-oriented by convention; leadership/managerial scope must be evidenced. |
| Head of Product (AI) | AI-specific product leadership scope must be evidenced, as distinct from general product management. |

Manual review under Tier 2 is limited strictly to the profile's own publicly stated content. It does not extend to external verification, inference from the employing organization's general business activity, or any judgement about the individual's actual competence. The review question is narrow and observable: *does the profile's own text state AI-, ML-, advanced-analytics-, or AI-strategy-related leadership responsibility?*

## 5. Tier 3 — Excluded Titles

| Title | Basis for Exclusion |
|---|---|
| Data Analyst | Individual-contributor scope; no leadership indication. |
| Machine Learning Engineer | Individual-contributor technical role. |
| AI Researcher (no leadership qualifier) | Individual-contributor technical/research role. |
| Software Engineer | Not AI-domain-specific; individual-contributor scope. |
| Data Engineer | Individual-contributor technical role. |
| Business Analyst | Not AI-domain-specific. |
| HR Director | Not AI-domain-specific. |
| Marketing Director | Not AI-domain-specific. |
| Sales Director | Not AI-domain-specific. |
| Operations Director (general) | Not AI-domain-specific absent an explicit AI qualifier. |
| Student / Intern (any AI-related title) | Not a professional leadership role. |

This list is illustrative, not exhaustive; any title not listed in Tier 1 or Tier 2 is treated as Tier 3 by the default rule stated in §2.

## 6. Application

The tier assigned to a candidate title determines the `inclusion_reason` recorded for that record: a Tier 1 match is recorded as a direct title match; a confirmed Tier 2 match is recorded as a manually reviewed inclusion; a Tier 3 match results in exclusion prior to further screening. See `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` for the full eligibility criteria and `ALCSM_Profile_Eligibility_Decision_Tree_v1.0.md` for the sequencing of the screening process.

## 7. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial finalized title dictionary (Tier 1–3), completing the Step 3 title-list placeholder previously carried in the sampling framework design. | Samiksha Dhere |

---

*This dictionary governs sampling-frame title matching only. It does not define, alter, or substitute for the frozen ALCSM leadership-level scoring taxonomy.*
