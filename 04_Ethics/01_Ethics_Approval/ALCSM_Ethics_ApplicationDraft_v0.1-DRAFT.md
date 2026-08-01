# ALCSM Ethics Application (Draft)

**Version:** 0.1-DRAFT
**Status:** Draft — not yet submitted, not yet reviewed, not yet approved. No ethics approval has been sought or granted at the time of writing.
**Purpose:** the formal ethics-committee application requesting approval to collect and process the LinkedIn profile and expert-survey data this thesis requires.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher), MSc Applied Data Science & Analytics, SRH University Heidelberg (Campus Hamburg) — drafted with Claude Code assistance
**Supervisor:** [INSERT: supervisor name]
**Submitting to:** [INSERT: name of institutional ethics committee / research ethics board]
**Related documents:** `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` (Annex A), `ALCSM_Ethics_LIA_v0.1-DRAFT.md`, `ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md`, `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md`, `ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`

This document is a preparation draft. All bracketed fields (`[INSERT: ...]`) must be completed with real, institution-specific information before submission — none of them are filled in with assumed or fabricated values.

---

## 1. Study title and summary

**Title:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles.*

**Summary.** This study audits the **credential signal** that individuals publicly present when holding AI-leadership titles (e.g. "Chief AI Officer," "Head of AI") on LinkedIn, and compares that signal against what a matched sample of AI-leadership job postings state they require. It does **not** assess any individual's actual competence, capability, or quality of leadership — only the observable credentials they present. The research delivers (1) a six-dimension scoring framework (ALCSM) applied consistently by trained human coders and cross-checked for inter-rater reliability; (2) a descriptive comparison of required vs. held credentials; (3) a local NLP tool that automates the scoring for comparison against the human results.

## 2. Purpose and public benefit

Job titles implying AI leadership have proliferated faster than any shared, checkable understanding of what such a role should require. This creates a public-interest question: to what degree do publicly presented credentials substantiate publicly presented titles? This study brings a transparent, reproducible, and falsifiable method to that question, rather than anecdote. The output is population-level evidence (patterns across a sample), not a verdict on any named individual, and no individual-level score is ever published or disclosed.

## 3. Data subjects and data collected

**Two distinct data-subject populations, on two different legal bases (see §6):**

1. **LinkedIn profile subjects (~500 individuals).** Working professionals who *publicly* present a qualifying AI-leadership title on LinkedIn. Not a vulnerable population. From each profile, the study records: the ALCSM-relevant section text (headline, about, experience, education, certifications, contributions, activity), search provenance, and a small set of observable engagement/reach indicators (RQ4 impact indicators — see §5). **The study does not collect, and the collection tooling actively rejects, any of the following: full name, profile URL, photograph, email address, phone number.** A profile is pseudonymised at the moment of capture (`PRF-#####`) and is never referred to by any other identifier in the research database.
2. **Expert survey respondents (a separate, smaller group).** Professionals with relevant expertise, invited to complete a short validation survey about the scoring framework's dimensions. This population is **never linked** to the profile-subject population — the database schema deliberately contains no relationship between the two, so the survey cannot be (mis)represented as evaluating the audited individuals.

## 4. Special-category data (Article 9 GDPR)

The study does not seek, and has no methodological need for, any special-category data (health, political opinion, trade-union membership, sexual orientation, etc.). **Rule applied:** if a profile incidentally reveals special-category content not required by the ALCSM framework, that content is not recorded, in any form, at any stage. This is enforced as a data-collection discipline; see the collection protocol (Annex A) for how this is operationalised.

## 5. What is *not* collected: the RQ4/ALCSM separation

A secondary research question (RQ4) asks whether presented credential signal correlates with independent, observable indicators of professional impact (network reach, engagement, third-party recognition, career-progression rate). These indicators are collected into a table that is **physically separate** from the credential scores and **is never shown to the human coders while they score** — this prevents the validation from being circular. This structural separation is enforced by the database design, not left to procedural discipline alone.

## 6. Legal basis and consent position

- **Profile-subject strand:** consent from ~500 individuals is not sought — it is infeasible at this scale and would itself distort the population under study (only self-selected, contactable individuals would remain). The legal basis relied upon is **legitimate interests (Art 6(1)(f) GDPR)**, supported by the scientific-research safeguards (Art 89 GDPR) and documented in full in the accompanying Legitimate Interests Assessment. The Article 14 transparency question (since these individuals are not contacted directly) is addressed via a published public privacy notice — see `ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`.
- **Survey strand:** explicit, informed **consent (Art 6(1)(a) GDPR)** is obtained from every respondent before any response is recorded; see `ALCSM_Ethics_SurveyInfoSheet_v0.1-DRAFT.md` and `ALCSM_Ethics_SurveyConsentForm_v0.1-DRAFT.md`.

## 7. Risk to data subjects and mitigations

**Principal risk:** re-identification of a profile subject, or reputational harm if an individual-level finding (e.g. a "credential inflation" pattern) were ever linked back to a named person.

**Mitigations:**
- Pseudonymisation at the point of capture; no direct identifier is ever stored in the research database (technically enforced, not just a policy).
- No individual-level score, finding, or profile excerpt is published; all reporting is at the aggregate/population level.
- Data stored only in an access-controlled, EEA-resident secure environment (see the Data Management Plan).
- A documented decision on whether any pseudonym-to-person mapping is retained at all, and if so, for how long and under what access control (§4.1 of the DMP) — **[INSERT: this decision — no mapping / temporary mapping / retained mapping — once made with the DPO]**.
- Defined retention and secure-destruction schedule (see DMP).

## 8. Risk to the researcher and institution

Automated collection (scraping) of LinkedIn data would breach LinkedIn's User Agreement — a real, adjudicated legal exposure (the *hiQ Labs v. LinkedIn* litigation ultimately found in LinkedIn's favour on the contract claim, with a financial judgment and injunction against the scraping party). **This study uses manual, human-driven collection only — no scraping, no browser automation, no automated retrieval of any kind.** Full method and rationale: `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` (Annex A).

## 9. Data protection impact assessment

Given the scale (~500 identifiable individuals) and the nature of the processing (systematic scoring/evaluation of individuals from a publicly accessible source), a DPIA screening was conducted; see `ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md`. **Conclusion of that screening: a full DPIA is warranted** — see `ALCSM_Ethics_DPIAFull_v0.1-DRAFT.md`.

## 10. Data storage, access, retention, and destruction

Fully specified in `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md`. In summary: university-approved, EEA-resident, access-controlled storage; access limited to the researcher and supervisor; encrypted backups with a verified restore procedure; a concrete retention period and destruction trigger **[INSERT: institutional policy period]**; no personal data ever committed to the project's version-control repository.

## 11. International data transfer

All storage and processing (including any NLP tooling used later in the project) is confined to EEA-resident, university-approved infrastructure. No profile text is sent to a third-party or hosted API of any kind at any stage.

## 12. Committee questions this application anticipates

- *Why not seek consent from profile subjects?* Addressed in §6 and the LIA — consent is infeasible at scale and would bias the sample toward the contactable/agreeable subset, which is precisely the sampling distortion a signal-audit study cannot tolerate.
- *Why is manual collection acceptable given the scale?* 500 profiles collected by hand over a defined collection window is a deliberately modest, tractable target chosen specifically because it stays within the manual method — not a compromise forced by the method, but the reason the sample size is what it is.
- *What happens if a data subject objects or requests erasure?* The privacy notice states the process; because profiles are pseudonymised at capture, honouring a specific erasure request may require the temporary/retained mapping (if one exists) — this is disclosed honestly, not glossed over, in the DMP.

---

## Annexes referenced by this application

- **Annex A** — `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md`
- **Annex B** — `ALCSM_Ethics_LIA_v0.1-DRAFT.md`
- **Annex C** — `ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md` / `ALCSM_Ethics_DPIAFull_v0.1-DRAFT.md`
- **Annex D** — `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md`
- **Annex E** — `ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`
- **Annex F** — `ALCSM_Ethics_SurveyInfoSheet_v0.1-DRAFT.md`, `ALCSM_Ethics_SurveyConsentForm_v0.1-DRAFT.md`

## Committee decision (to be completed by the committee — do not fill in pre-emptively)

| Field | Value |
|---|---|
| Decision | `[INSERT: Approved / Approved with conditions / Rejected / Deferred]` |
| Reference number | `[INSERT]` |
| Date | `[INSERT]` |
| Conditions (if any) | `[INSERT]` |
| Signed | `[INSERT]` |

---

*Sources: this application consolidates and formalises content already reasoned through in `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §2.1 and `Task5_LinkedIn_Collection_Workflow.md`. No frozen ALCSM methodology or database element is described differently here than in `PROJECT_CONTEXT.md`; see the governance consistency review (`09_Review_Logs/`) for the explicit cross-check.*
