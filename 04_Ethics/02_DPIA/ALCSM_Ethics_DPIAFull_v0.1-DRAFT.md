# ALCSM Data Protection Impact Assessment (Full Draft)

**Version:** 0.1-DRAFT
**Status:** Draft — prepared by the researcher for DPO review. Not yet reviewed, not yet signed off, not a substitute for the DPO's own assessment or the controller's formal sign-off.
**Purpose:** assess, in full, the data-protection risks of the LinkedIn profile-audit strand and the measures taken to address them, per the DPIA Screening's conclusion that a full assessment is warranted.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Triggered by:** `ALCSM_Ethics_DPIAScreening_v0.1-DRAFT.md` (conclusion: full DPIA warranted)
**Structure follows:** GDPR Art 35(7) and WP248 (Article 29 Working Party DPIA guidelines).

---

## Part A — Systematic description of the processing and its purposes

**Nature of processing.** Manual, human-driven collection of publicly visible LinkedIn profile content (text only) for individuals presenting AI-leadership titles; pseudonymisation at capture; structured, rubric-based scoring of six credential dimensions by trained human coders; independent collection of ~200 job-posting texts; a descriptive comparison ("gap") between required and held credential levels per dimension; a later-stage local NLP pipeline that automates the scoring for comparison against the human-coded results; an isolated set of observable professional-impact indicators (RQ4) for a separate correlation analysis.

**Scope.** ~500 pseudonymised LinkedIn profiles; ~200 job postings; a small number of expert survey responses (separate legal basis, see below). No name, profile URL, photograph, email, or phone number is ever collected into the research database.

**Context.** An MSc thesis research project. Data subjects are working professionals who have themselves chosen to present an AI-leadership title publicly; they have a general awareness that public professional-networking content may be viewed and referenced by third parties, though they have not been told specifically that this study exists (addressed via the public privacy notice, not direct contact — see §D.4 below and the LIA).

**Purpose.** Research into the correspondence (or lack of it) between publicly presented AI-leadership credentials and publicly stated AI-leadership job requirements — see the Ethics Application §2 for the full public-benefit rationale. This is **not** an evaluation of any named individual's actual competence; the frozen research framing is explicit that the study measures *presented signal*, never *ability* (`PROJECT_CONTEXT.md` §1).

**Legal basis.** Legitimate interests (Art 6(1)(f)) for the profile-audit strand, detailed in `ALCSM_Ethics_LIA_v0.1-DRAFT.md`; consent (Art 6(1)(a)) for the separate expert-survey strand.

**Controller.** `[INSERT: to be confirmed — typically the university, with the researcher acting on its behalf; this determines who formally owns this DPIA and signs it]`.

## Part B — Assessment of necessity and proportionality

- **Is the processing necessary to achieve the stated purpose?** Yes — the research question is specifically about *publicly presented* credentials, which by definition requires observing what is publicly presented; there is no way to answer it from already-anonymised or synthetic data.
- **Could a less-intrusive approach achieve the same purpose?** A smaller sample would reduce the population processed but would weaken the statistical basis for the population-level claims the study makes; the ~500 figure is set at a level the DMP and LIA both describe as a pragmatic, manually tractable target — not the largest sample the researcher could gather, but a bounded one. No alternative data source (e.g. self-report surveys of AI leaders) would answer the *presented-credential* question, since self-report is exactly the signal-inflation phenomenon under study.
- **Is data minimisation respected?** Yes — only ALCSM-relevant section text, provenance fields, and the RQ4 indicators are recorded; direct identifiers are excluded by design and enforced technically, not just by policy; special-category content is excluded outright regardless of relevance.
- **Is the processing proportionate to the purpose?** The population-level, non-individually-published nature of the output, combined with pseudonymisation and the exclusion of direct identifiers, supports proportionality. This assessment should be revisited if the sample size or data fields expand materially.

## Part C — Assessment of risks to the rights and freedoms of data subjects

| Risk | Likelihood | Severity | Description |
|---|---|---|---|
| Re-identification of a pseudonymised profile | Low–Medium | Medium–High | An unusual combination of role, seniority, and public activity could in principle make a profile recognisable even without a stored name, particularly for high-profile individuals (e.g. a well-known named "Chief AI Officer" of a specific large company). |
| Reputational harm from a "credential inflation" finding | Low | Medium–High | If a specific, de-pseudonymised individual's low-substantiation finding became public or was inferred, it could cause professional harm, notwithstanding that the study's own framing is explicitly about *signal*, not competence. |
| Lack of awareness / inability to exercise data-subject rights | Medium | Medium | Profile subjects are not directly contacted; the public privacy notice is the primary transparency mechanism, and a subject who never encounters it may be unaware their data is processed. |
| Data breach of the research database or backups | Low | Medium–High | Any pseudonymised personal-data breach is a genuine harm and a notifiable event under Art 33/34, regardless of pseudonymisation. |
| Scope creep (data used beyond the stated research purpose) | Low | Medium | Purpose limitation must be actively maintained across a multi-year thesis project with several contributors/reviewers. |
| Requirement–possession commensurability being over-read (a schema-disclosed weakness, W-class) | N/A (methodological, not a data-protection risk) | — | Noted for completeness; addressed in the frozen schema/framework documentation, not a DPIA matter. |

## Part D — Measures to address the identified risks

1. **Pseudonymisation at the earliest possible point** (capture, not after), technically enforced by the collection tooling (direct identifiers cannot be entered into the database at all).
2. **No individual-level publication.** All thesis and any subsequent publication reporting is at the aggregate/population level; no verbatim profile excerpt or individual score is disclosed outside the research team.
3. **Structural separation of RQ4 indicators from ALCSM scores**, preventing the specific circularity risk and limiting what any single view of the data reveals about an individual.
4. **Public Article 14 privacy notice** published as the transparency safeguard in place of infeasible direct notification, stating purpose, legal basis, retention, and how to exercise data-subject rights (`ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`).
5. **Access control.** Only the researcher and supervisor (and, if applicable, a named second coder under confidentiality obligations) have access to the research database; access is not extended casually.
6. **EEA-resident, university-approved storage only**, with encrypted backups and a tested, verified restore procedure (see the Data Management Plan).
7. **Retention limit and destruction trigger**, concretely dated once confirmed with the institution (DMP §Retention).
8. **Re-identification-mapping decision**, made explicitly and documented (DMP §4.1) rather than left as an undocumented default; the recommended default is **no persistent mapping**.
9. **No external-API processing of profile text at any stage** (including the later NLP pipeline), removing the international-transfer risk entirely for this data.
10. **Purpose-limitation discipline** maintained via the governance documents in this repository (`DECISION_LOG.md`, `Implementation_Phase_Roadmap.md`) so that scope changes are visible, dated, and reviewable rather than silent.

## Part E — Residual risk and recommendation

After the measures in Part D, the residual risk is assessed by the researcher as **low**, principally because of the technically enforced pseudonymisation, the structural (not merely procedural) separation of RQ4 from ALCSM scoring, and the exclusively aggregate reporting commitment. **This residual-risk judgement is the researcher's own and must be confirmed or revised by the DPO before collection begins.**

| Field | Value |
|---|---|
| DPO review completed | `[INSERT: yes/no, date]` |
| DPO's residual-risk determination | `[INSERT]` |
| Conditions attached | `[INSERT]` |
| Sign-off | `[INSERT: name, role, date]` |

---

## Part F — Consultation

GDPR Art 35(9) expects the controller to seek the views of data subjects or their representatives on the intended processing "where appropriate." This section addresses that expectation explicitly, rather than leaving it silently unaddressed, and records who is consulted on this DPIA and when.

**Consultation with the University's Data Protection Officer.** The DPO's review of this DPIA is mandatory, not optional, and is the primary consultation this assessment relies on — recorded in Part E above (review completed, residual-risk determination, conditions, sign-off). The DPO's own institutional consultation obligations (e.g. with a wider data-protection function, if the institution has one) are a matter for the DPO's own process, not something this document can specify.

**Consultation with the ethics committee.** The ethics committee reviews this DPIA as an annex to the Ethics Application (`ALCSM_Ethics_ApplicationDraft_v0.1-DRAFT.md`) and may raise its own conditions independently of the DPO's. Both consultations are tracked to closure before collection begins (see the GDPR Compliance Checklist, §C).

**Consultation with data subjects or their representatives.** Not undertaken, and the reason is stated here rather than left implicit: the ~500 profile subjects are not contacted individually (§3.5 of the LIA explains why direct contact is not used), and there is no pre-existing representative body for "individuals who publicly present an AI-leadership title on LinkedIn" that could stand in for them collectively. The public privacy notice (`ALCSM_Ethics_PrivacyNotice_v0.1-DRAFT.md`) is the closest available substitute — it gives any data subject who becomes aware of the study the means to raise a concern or object, after the fact rather than before. **This is a real limitation of this DPIA, disclosed rather than concealed:** the consultation this assessment relies on is institutional (DPO, ethics committee), not from the data subjects whose data is actually processed. **[INSERT: the DPO may determine that a more active data-subject consultation step is required despite the above reasoning — record that determination here if so.]**

**Circumstances that would require re-consultation.** If the processing changes materially after this DPIA is signed off — a larger sample, a new data field, a new storage location, a new sub-population (e.g. extending beyond LinkedIn) — this DPIA must be revisited and the DPO re-consulted before the changed processing begins, not retrofitted afterward.

**Documentation of consultation outcomes.** Every consultation above is recorded in `07_Institutional_Correspondence/` as a dated entry (committee queries and responses, DPO guidance and clarifications), so the consultation trail is auditable independently of this document.

---

*This DPIA draws its factual content from `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §3 and the frozen schema's own structural guarantees (`PROJECT_CONTEXT.md` §13–§17, §45). No frozen ALCSM methodology or database element is altered by this document — the DPIA assesses existing, frozen design decisions; it does not propose new ones.*
