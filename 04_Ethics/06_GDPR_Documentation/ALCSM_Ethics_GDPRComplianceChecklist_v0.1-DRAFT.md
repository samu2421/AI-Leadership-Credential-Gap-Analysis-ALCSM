# ALCSM GDPR Compliance Checklist (Draft)

**Version:** 0.1-DRAFT
**Status:** Draft — self-assessment checklist, for the researcher's own tracking and for DPO/committee review. A checked box records "drafted/addressed," not "approved" — approval is recorded separately in each source document.
**Purpose:** a single-page, at-a-glance view of GDPR-relevant governance status, consolidating items from the Ethics Application, LIA, DPIA, Privacy Notice, and DMP. This checklist does not replace those documents — it points to them.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

---

## A. Legal basis and transparency

- [ ] Legal basis identified and documented for the LinkedIn strand (legitimate interests, Art 6(1)(f)) — `ALCSM_Ethics_LIA_v0.1-DRAFT.md`
- [ ] Legal basis identified and documented for the survey strand (consent, Art 6(1)(a)) — `ALCSM_Ethics_SurveyConsentForm_v0.1-DRAFT.md`
- [ ] Balancing test completed and reviewed by DPO — `ALCSM_Ethics_LIA_v0.1-DRAFT.md` §3
- [ ] Article 14 position decided and documented (public privacy notice as the transparency safeguard) — `ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`
- [ ] Privacy notice actually published (not just drafted) before collection begins

## B. Data minimisation and special-category data

- [ ] No direct identifiers (name, URL, photo, email, phone) collected — enforced technically by the collection helper, confirmed by test (see `P1_Completion_Summary.md`)
- [ ] No Article 9 special-category data collected, including incidental content — rule documented in the Ethics Application §4 and the LinkedIn Collection Protocol §5
- [ ] RQ4 indicators kept structurally separate from ALCSM dimension scores — enforced by the frozen schema (`rq4_impact_indicator` table isolation)

## C. DPIA

- [ ] DPIA screening completed — `ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md`
- [ ] Full DPIA drafted (screening concluded one is warranted) — `ALCSM_Ethics_DPIAFull_v0.1-DRAFT.md`
- [ ] DPIA reviewed and signed off by the DPO
- [ ] Residual risk determination confirmed by the DPO

## D. Collection method and international transfer

- [ ] Collection method confirmed as manual/human-driven only, no scraping or automation — `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md`
- [ ] Method decision confirmed with supervisor/DPO as ToS-compliant
- [ ] All storage and processing confirmed EEA-resident; no international transfer — `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md` §4
- [ ] NLP pipeline (later phase) confirmed local-models-only, no third-party API processing of profile text — frozen architectural decision, see `DECISION_LOG.md` D-0012

## E. Storage, retention, destruction

- [ ] Controller identified — `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md` §11
- [ ] Secure store provisioned, access-controlled, EEA-resident
- [ ] Backup/restore procedure verified on the real (not just throwaway/dev) environment
- [ ] Retention period/trigger fixed and documented
- [ ] Destruction procedure documented and responsibility assigned
- [ ] Re-identification-mapping decision made and documented — `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md` §4.1

## F. Data-subject rights

- [ ] Process for handling an access/rectification/erasure/objection request documented and assigned to a named responsible person
- [ ] Supervisory authority named for complaints — `ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`

## G. Governance and sign-off

- [ ] Ethics committee approval obtained, reference recorded — `01_Ethics_Approval/`
- [ ] DPO sign-off obtained on the DPIA and the LIA's balancing test
- [ ] Supervisor sign-off on the collection method
- [ ] All of the above cross-checked against what is actually built/planned in `src/alcsm/` and the `Implementation_Phase_Roadmap.md` P3/P4/P6 scope, so approved scope and built scope do not drift apart

---

**This checklist is not itself a gate.** The actual gate is `Implementation_Phase_Roadmap.md`'s Phase P2 exit criteria and the collection-readiness checklist in `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §14 — this document is a quick-reference index into that fuller process, not a replacement for it.

---

*No frozen ALCSM methodology or database schema element is altered by this document.*
