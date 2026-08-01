# Governance Consistency Review — P2 Session 2
### Cross-check of the newly drafted ethics/GDPR documentation set against frozen methodology and existing governance

**Version:** 0.1-DRAFT
**Status:** Draft — an internal review record, not a submission document. Superseded in currency (not in accuracy) by `11_Implementation_Governance/Reviews/P2_Governance_QA_Report.md` (P2 Session 3) and `P2_Final_Governance_Review.md` (P2 Session 4), which reviewed this document's own set alongside everything else.
**Purpose:** cross-check the ten documents drafted in P2 Session 2 against frozen ALCSM methodology and existing governance decisions, before they were handed off for QA review.
**Last Updated:** 2026-07-30 — added this metadata block for consistency with the rest of the package (P2 Session 4); the review content itself (§1–§6) is unchanged from P2 Session 2.
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Scope:** the ten documents drafted in this session (listed in §1) plus the nine new `04_Ethics/` subfolder READMEs, checked against `PROJECT_CONTEXT.md`, `CLAUDE_CODE_RULES.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `DECISION_LOG.md`, and `Implementation_Phase_Roadmap.md`.

---

## 1. Documents reviewed

| Document | Location |
|---|---|
| Ethics Application | `01_Ethics_Approval/ALCSM_Ethics_ApplicationDraft_v0.1-DRAFT.md` |
| LinkedIn Collection Protocol | `01_Ethics_Approval/ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` |
| DPIA Screening | `02_DPIA/ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md` |
| Full DPIA | `02_DPIA/ALCSM_Ethics_DPIAFull_v0.1-DRAFT.md` |
| LIA | `03_LIA/ALCSM_Ethics_LIA_v0.1-DRAFT.md` |
| Privacy Notice | `04_Privacy_Notice/ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md` |
| Survey Info Sheet | `05_Consent_Materials/ALCSM_Ethics_SurveyInfoSheet_v0.1-DRAFT.md` |
| Survey Consent Form | `05_Consent_Materials/ALCSM_Ethics_SurveyConsentForm_v0.1-DRAFT.md` |
| Data Management Plan | `06_GDPR_Documentation/ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md` |
| GDPR Compliance Checklist | `06_GDPR_Documentation/ALCSM_Ethics_GDPRComplianceChecklist_v0.1-DRAFT.md` |

## 2. Frozen-methodology checks

| Check | Result |
|---|---|
| Signal-not-competence framing used consistently (never "measures competence/ability/quality of leadership") | **Pass** — every document states the study measures presented credential *signal*; the Ethics Application §1 and DPIA Part A both state this explicitly. |
| No composite/aggregate ALCSM score implied anywhere in these documents | **Pass** — no document describes or implies a single score; the Ethics Application describes "six-dimension scoring," never a total. |
| RQ4 indicators described as structurally separate from ALCSM scores | **Pass** — stated in the Ethics Application §5, the DPIA Part D item 3, and the DMP/Checklist, consistent with `PROJECT_CONTEXT.md` §5, §15. |
| No special-category (Article 9) data collection implied or permitted | **Pass** — explicit exclusion rule stated in the Ethics Application §4, the Collection Protocol §5, and the DPIA/Checklist. |
| No suggestion of scraping, browser automation, or automated retrieval | **Pass** — every document that touches collection method states manual-only, citing the same *hiQ Labs v. LinkedIn* rationale already established in `Task5_PreCollection_Roadmap.md`. |
| `survey_respondent` treated as a population entirely separate from `profile` (no link implied) | **Pass** — stated explicitly in the Ethics Application §3 and the Survey Info Sheet's applicability note, matching `PROJECT_CONTEXT.md` §14's "deliberately absent" relationship. |
| No frozen precedent, dimension, rubric, or missing-data-state redefined | **Pass** — none of these documents touch ALCSM scoring content at all; they are collection/governance documents, not methodology documents. |
| No schema change proposed or implied | **Pass** — every document that references the schema (DMP §4.1, Consent Form's schema-alignment note, Collection Protocol) describes existing frozen fields (`survey_respondent.consent_confirmed`, `rq4_impact_indicator` isolation, `PRF-#####` format) without proposing any addition or alteration. |

## 3. Cross-reference checks against existing governance documents

| Check | Result |
|---|---|
| Consistent with `DECISION_LOG.md` D-0009 (single write path) | **Pass** — the Collection Protocol describes data entering "the project's access-controlled... database" via the existing validated tooling; it does not describe or imply a second write path. |
| Consistent with `DECISION_LOG.md` D-0011 (no composite score) | **Pass** — see §2 above. |
| Consistent with `DECISION_LOG.md` D-0012 (no external-API processing of profile text) | **Pass** — the DMP §4 and the Checklist §D both restate this as a standing constraint carried into the later NLP phase (P7), not something these documents relax. |
| Consistent with `Implementation_Phase_Roadmap.md`'s definition of Phase P2 | **Pass** — every document produced this session is a governance/document artefact; none contains code, SQL, or an implementation decision. The Roadmap's P2 "Allowed implementation work: None in the software-engineering sense" boundary was respected throughout. |
| Consistent with `CLAUDE_CODE_RULES.md` rule 8 (no real data collection before ethics approval) | **Pass** — every document is explicitly marked DRAFT / NOT YET APPROVED, and the Collection Protocol states collection may not begin under it until approval is obtained. |
| Consistent with the P0-cleanup decision that `05_Data_Collection/Scripts/collection_helper.py` and `05_Data_Collection/Documentation/*` remain the operative technical references | **Pass** — this session's documents cite and formalise those existing documents (`Task5_PreCollection_Roadmap.md`, `Task5_LinkedIn_Collection_Workflow.md`) rather than duplicating or contradicting their content. |

## 4. Internal consistency across this session's new documents

- All ten documents share the version tag `0.1-DRAFT` and an explicit "not yet approved/submitted/published" status statement at the top — no document overstates its own authority.
- Cross-references between documents (e.g. the Ethics Application's Annex list, the DMP's re-identification-mapping section referenced from both the Ethics Application and the Collection Protocol) point to filenames that actually exist in this commit — verified by directory listing at time of writing.
- The Survey Info Sheet and Survey Consent Form both reference "version 0.1-DRAFT" as the synchronised version shown to respondents, per the versioning rule stated in `05_Consent_Materials/README.md`.
- No document asserts a specific ethics-committee decision, DPO sign-off, or approval reference as fact — every such field is a bracketed placeholder (see the companion placeholder summary in this session's closing report).

## 5. Issues found

**None that required a document to be rewritten.** One point is flagged for the author's attention rather than treated as an error:

- The Ethics Application, DPIA, and LIA each independently restate the *hiQ Labs v. LinkedIn* litigation summary and the Article 14/DPIA reasoning already present in `Task5_PreCollection_Roadmap.md`. This is intentional — each document must be legible as a standalone submission artefact to a committee/DPO who may not read the others — but it does mean a future substantive change to that reasoning (e.g. new case law, a revised Article 14 position) must be propagated across four documents by hand. Recommend re-checking all four together if that reasoning ever changes.

## 6. Conclusion

The ten drafted documents and nine new folder READMEs are internally consistent with each other and with every frozen methodology and governance decision checked above. Nothing drafted this session requires a correction before proceeding to author/DPO/committee review.
