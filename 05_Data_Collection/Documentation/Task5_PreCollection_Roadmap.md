# Task 5 — Pre-Collection Roadmap
### Ethics, Data Protection, and Operational Readiness Before Any LinkedIn Data Is Collected

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Role for this task:** research methodology reviewer (not database architect). ALCSM v1.0 and Schema v1.0.1 are frozen and are not modified anywhere in this document.

**Convention:** *[Established]* draws on recognised research-methods or data-protection practice; *[Thesis-specific]* is a project decision you must own; **[BLOCKER]** must be resolved before collection begins; **[INSTITUTIONAL]** requires a determination from your supervisor, your university's ethics committee, or its Data Protection Officer (DPO) — not something a methodology reviewer can decide for you.

---

## 0. The reviewer's headline, stated plainly before the templates

Most of this task is routine and I can hand you usable drafts. **One part is not routine, and I would be failing as your methodology reviewer if I buried it in section 2:** *how* you obtain the 500 profiles is the single largest risk in the entire thesis, and it is a legal/ethical question you cannot resolve by yourself. Two facts an examiner (and your DPO) will know, which contradict the assumptions students usually bring to this:

1. **"Publicly visible" does not mean "free to collect."** LinkedIn's User Agreement expressly prohibits scraping and copying profiles by any automated means. In the *hiQ Labs v. LinkedIn* litigation — often cited by students as having *authorised* scraping — the final 2022 outcome was the opposite: after six years, the court found hiQ had **breached LinkedIn's User Agreement** through its scraping, a consent judgment entered **$500,000** against hiQ, and a permanent injunction stopped its scraping. The CFAA ("hacking") claim failed for public data, but the **contract** claim succeeded. So automated scraping of LinkedIn is a live breach-of-contract exposure, independent of whether the data is public. <cite index="2-1,4-1">After six years of litigation the parties reached a settlement including a $500,000 judgment against hiQ and injunctive relief prohibiting its future scraping, following LinkedIn's summary-judgment win on breach of contract based on a finding that hiQ's scraping violated LinkedIn's user agreement.</cite>

2. **"Publicly available personal data" is still fully protected personal data under the GDPR.** There is no public-data exemption. Because you are in Germany, the GDPR and the German BDSG apply directly, and processing 500 identifiable professionals' data engages Articles 6, 9, 13/14, and quite possibly 35 (DPIA). The Article 14 duty to *notify each data subject* applies specifically to data not collected from the person, and the research/"disproportionate effort" exemption is real but **must be argued case-by-case, not assumed** — and the EDPB has signalled it should be read narrowly. <cite index="12-1">When personal data comes from publicly available sources, data subjects must in principle be notified in line with Article 14.</cite> <cite index="11-1">The disproportionate-effort exemption from the Article 14 notice duty must be interpreted narrowly, assessed case by case against factors including the number of data subjects, the age of the data, and the safeguards in place.</cite>

**What this means concretely, and it is a [BLOCKER] [INSTITUTIONAL]:** before you collect a single profile you need (a) ethics committee approval, (b) a documented GDPR legal basis and a decision on the Article 14 notification question, and (c) a supervisor-endorsed decision on collection *method* that does not expose you or the university to a ToS breach. The most defensible method for a master's thesis is almost always **manual, human-driven collection of a modest sample** rather than automated scraping — slower, but it sidesteps the "automated means" prohibition that sank hiQ and keeps the volume proportionate. I develop this in §2 and §5, but I am flagging it here because every other document in this roadmap depends on how these three questions are answered.

I am not your lawyer and this is not legal advice; it is a methodology reviewer telling you where the load-bearing risk is and who must sign it off.

---

## 1. Roadmap overview

Thirteen deliverables, grouped by dependency. Items in **Group A must be approved before anything in Group C begins.**

| Group | Deliverable | Section | Gate |
|---|---|---|---|
| **A. Governance** | Ethics documentation | §2 | [BLOCKER] approval before collection |
| | GDPR/privacy assessment (+ DPIA screening) | §3 | [BLOCKER] |
| | Data Management Plan (DMP) | §4 | Should precede collection |
| **B. Design** | Sampling protocol | §5 | Depends on A |
| | LinkedIn collection protocol | §6 | Depends on A |
| | Job-posting collection protocol | §7 | Depends on A |
| **C. Operations** | File organisation | §8 | — |
| | Version-control strategy | §9 | — |
| | Annotation workflow | §10 | — |
| | Double-coding protocol | §11 | — |
| | Reliability workflow | §12 | — |
| | Data-quality checklist | §13 | — |
| | Collection-readiness checklist | §14 | Final gate |

---

## 2. Ethics Documentation

**[INSTITUTIONAL]** Your university sets the actual form and approval route. This section gives you the *content* an ethics application needs; the *format* must follow SRH's own template and process. Confirm with your supervisor whether your project needs full committee review or a lighter self-assessment — a study collecting identifiable personal data from 500 people will almost certainly need the former.

### 2.1 Ethics application — required content

An examiner-ready application should address, at minimum:

- **Purpose and public benefit.** State the research aim in the frozen signal-audit language (auditing the observable LinkedIn credential *signal*, not judging individuals' competence). Ethics reviewers respond well to a clear, proportionate public-interest rationale.
- **What data, from whom.** Profiles of individuals *publicly presenting AI-leadership titles*; the six ALCSM dimensions' underlying fields; the RQ4 impact indicators. State explicitly that you do **not** collect names, photographs, or contact details into the research database (the schema already enforces pseudonymity).
- **Data subjects and vulnerability.** Working professionals, not a vulnerable population — but note that some profiles may incidentally reveal special-category data (Article 9: e.g. trade-union roles, political affiliations, health advocacy). State your rule for handling incidental special-category content: **do not record it**, since ALCSM does not require it. *[Thesis-specific — recommended]*
- **Consent position and its justification.** You will *not* seek consent from the 500 profile subjects (infeasible at scale and arguably self-defeating for an audit of self-presentation). This must be justified under a GDPR legal basis (§3), and the ethics application must show you have thought about the Article 14 notification duty rather than ignored it.
- **Risk to data subjects and mitigation.** Principal risk: re-identification and reputational harm if raw data or a poorly aggregated "low-credential" label were linked to a named individual. Mitigations: pseudonymisation at capture; no publication of individual-level scores; reporting only in aggregate; secure storage; defined retention/destruction (§4).
- **Risk to the researcher and institution.** The ToS/scraping exposure in §0. State the collection method and why it minimises this.
- **The survey strand** (expert respondents) — consent-based, low-risk, covered by the participant information sheet and consent form in §2.2–2.3.
- **Data storage, access, retention, destruction.** Cross-reference the DMP (§4).

### 2.2 Survey Participant Information Sheet — ready-to-adapt draft

> **Study title:** The AI Leadership Credential Gap — Expert Validation Survey
> **Researcher:** Samiksha Dhere, MSc Applied Data Science & Analytics, SRH University Heidelberg (Campus Hamburg). **Supervisor:** [name]. **Contact:** [university email].
>
> **What is this study?** This research develops a framework for describing the credentials that people holding AI-leadership titles present on professional profiles. You are invited to take part in a short expert-validation survey.
>
> **Why me?** You have been invited because of your professional expertise in [AI / data science / leadership / recruitment]. Your judgement helps assess whether the framework's dimensions sensibly cover the domain.
>
> **What would I do?** Complete a survey of approximately [N] questions, taking about [X] minutes. There are no right or wrong answers.
>
> **Do I have to?** No. Participation is voluntary. You may skip any question and stop at any time. You may withdraw before submission without giving a reason; because responses are pseudonymous, withdrawal after submission may not be possible once responses are aggregated — this is explained before you consent.
>
> **What data is collected?** Your survey answers and a coarse indication of your expertise area and years of experience (in bands, e.g. 5–9 years). No name, employer, or contact detail is stored with your responses.
>
> **How is my data protected?** Responses are stored pseudonymously on [secure university-approved storage], accessible only to the researcher and supervisor, and reported only in aggregate. Data are retained until [retention point] and then securely deleted.
>
> **Legal basis (GDPR).** [To be completed after §3 — typically consent for the survey strand.] You have the right to access, rectify, or request erasure of your data, and to complain to the [competent supervisory authority — e.g. the Hamburg Commissioner for Data Protection and Freedom of Information]. Data Protection contact: [university DPO].
>
> **Approvals.** This study has been reviewed by [ethics body], reference [number].

### 2.3 Survey Informed Consent Form — ready-to-adapt draft

> **Please confirm each statement before proceeding.** *(The database records consent as a single confirmed state; a respondent who does not confirm cannot enter the dataset.)*
>
> - [ ] I have read and understood the Participant Information Sheet (version [x], dated [ ]).
> - [ ] I understand my participation is voluntary and I may stop at any time before submitting.
> - [ ] I understand my responses are pseudonymous and reported only in aggregate.
> - [ ] I understand withdrawal after submission may not be possible once responses are aggregated.
> - [ ] I consent to my pseudonymous responses being used for this research and its thesis and any resulting publications.
>
> **[ ] I consent and wish to proceed.**  Date auto-recorded.

*Note on schema alignment:* the frozen `survey_respondent` table records `consent_confirmed` (which must be TRUE for a row to exist), `consent_ts`, and a `withdrawal_flag`. The consent flow above maps onto those fields without any schema change.

---

## 3. GDPR / Privacy Assessment

**[INSTITUTIONAL] [BLOCKER]** The determinations here must be confirmed with your DPO. This section structures the assessment; it does not substitute for the DPO's sign-off.

### 3.1 Are you processing personal data? Yes.
Profiles describe identified or identifiable natural persons. Pseudonymising at storage reduces risk but does **not** remove the data from GDPR scope, and the *act of collection* touches identifiable data. Treat the whole pipeline as personal-data processing.

### 3.2 Who is the controller?
Typically the university (with you as the researcher acting on its behalf), but this must be confirmed — it determines who signs the DPIA and bears accountability. **[INSTITUTIONAL]**

### 3.3 Legal basis — Article 6
For the LinkedIn strand, consent is infeasible, so the realistic basis is **legitimate interests (Art 6(1)(f))**, supported by the scientific-research provisions (Art 89 safeguards) and, in Germany, the relevant BDSG research provisions. Legitimate interests is available for research, **but the balancing test is mandatory**: your research interest must be weighed against the data subjects' rights, and the assessment documented. <cite index="11-1">Scientific research can constitute a legitimate interest, including where consent is impractical, but this does not lower the bar — the balancing test remains critical, especially given the scale and sensitivity of the data.</cite> For the survey strand, use **consent (Art 6(1)(a))**.

Produce a short written **Legitimate Interests Assessment (LIA)**: purpose test (is the interest legitimate?), necessity test (is processing necessary, or could a smaller/aggregated approach achieve it?), balancing test (do the individuals' rights override it?). *[Established]*

### 3.4 Special-category data — Article 9
You do **not** intend to process Article 9 data. Adopt an explicit rule: incidental special-category content encountered on a profile is **not recorded**. Document this as a safeguard. *[Thesis-specific — recommended]*

### 3.5 Transparency — Articles 13 and 14 *(the hard one)*
Article 14 governs data **not obtained from the data subject**, i.e. exactly your case, and in principle requires notifying each of the 500 individuals. <cite index="12-1">When personal data comes from publicly available sources, data subjects must in principle be notified under Article 14.</cite> There is a research/"disproportionate effort" exemption (Art 14(5)(b)), **but it is narrow and case-specific, not automatic.** <cite index="10-1">A researcher may claim exemption where providing notice would render impossible or seriously impair the research objectives, provided appropriate safeguards are in place, including making the information publicly available.</cite> <cite index="16-1">The room accorded to controllers by Article 14(5) should not be overestimated, particularly for research relying on legitimate interests.</cite>

**Recommended, defensible position:** rather than rely silently on the exemption, publish a **public privacy notice** for the study (on a university or project page) describing the processing, the legal basis, retention, and data-subject rights — this is exactly the "making the information publicly available" safeguard the exemption contemplates, and it materially strengthens your position. Decide with the DPO whether individual notification is genuinely disproportionate given your (deliberately modest) sample size; the smaller the sample, the weaker the "disproportionate effort" argument becomes, which is a real tension you should discuss openly rather than hide. **[INSTITUTIONAL]**

### 3.6 Data-subject rights
Even under legitimate interests, subjects retain rights (access, rectification, erasure, objection), some of which have research qualifications. Your public notice must state how a person can exercise them and whom to contact. Pseudonymisation may make locating one person's record genuinely hard — document this honestly.

### 3.7 DPIA screening — Article 35
Large-scale processing of personal data, and systematic evaluation/scoring of individuals, are exactly the triggers that point toward a **Data Protection Impact Assessment**. A framework that *scores individuals on their credentials* is a form of systematic evaluation. **My assessment as reviewer: a DPIA is likely required, and you should assume it is until the DPO says otherwise.** Budget time for it; it is not a formality and it must precede collection. **[INSTITUTIONAL] [BLOCKER]**

### 3.8 International transfer
If any storage, processing, or tooling sits outside the EEA (some cloud services, some NLP APIs), Chapter V transfer rules engage. Keep storage and processing within EEA/university-approved infrastructure to avoid this. **[INSTITUTIONAL]**

---

## 4. Data Management Plan (DMP)

**[Established]** Structure follows standard funder/university DMP templates (e.g. Horizon Europe / Science Europe style). Adapt to SRH's template if one exists.

| DMP element | Entry for this project |
|---|---|
| **Data description** | Two collected corpora (≈500 pseudonymised profiles, ≈200 job postings) + expert survey responses; derived annotation, criterion, and NLP-prediction data. Formats: PostgreSQL relations, text, CSV exports. |
| **Volume** | Small — low gigabytes at most. |
| **Personal data** | Yes (profiles, survey). Pseudonymised at capture; no direct identifiers in the research database. |
| **Storage** | University-approved, access-controlled, EEA-resident storage. Database on [approved host]. **No profile data on personal laptops or consumer cloud drives.** *[Thesis-specific, strongly recommended]* |
| **Access control** | Researcher + supervisor only. Any re-identification mapping (if it exists at all) stored **separately** from the research database, under stricter control (see §4.1). |
| **Backup** | Regular encrypted backups to approved storage; backup restore tested (already exercised in Task 4 validation). |
| **Security** | Encryption at rest and in transit; pseudonymous keys; principle of least privilege. |
| **Retention** | Retain only as long as needed for the thesis and its examination + any required post-examination period per university policy; then secure deletion. State a concrete date/trigger. **[INSTITUTIONAL]** |
| **Destruction** | Documented secure-deletion procedure for database, backups, and any mapping. |
| **Sharing / openness** | Aggregate results and the *framework/schema/code* can be shared openly (they contain no personal data); **raw profile-level data will not be shared or published.** The taxonomies, rulebook, and schema are the shareable research outputs. |
| **Roles** | Controller: [university, TBC]. Researcher: Samiksha Dhere. Supervisor: [name]. DPO: [name]. |

### 4.1 The re-identification mapping decision *(carried from Task 4, still open)*
The frozen schema deliberately contains **no** pseudonym↔real-person mapping. You have three options, in ascending order of risk:
1. **No mapping at all** — once a profile is pseudonymised and captured, the link to the real person is not retained. Lowest risk; makes rectification/erasure requests hard to honour (disclose this).
2. **Temporary mapping** — retained only during collection/QA, destroyed before analysis, with a documented destruction date.
3. **Retained mapping** — kept outside the research database under separate, stricter access control, justified by a specific need.

**Reviewer recommendation:** option 1 or 2. Retaining a mapping (option 3) creates the most sensitive artefact in the whole project and needs a strong, specific justification. Whatever you choose, **document it in the DMP and the DPIA.** **[INSTITUTIONAL decision, thesis-specific documentation]**

---

## 5. Sampling Protocol

**[Thesis-specific]** Carries forward the frozen framework's sampling requirements (purposive/title-based; provenance captured; honest limitation disclosure).

### 5.1 Target population and frame
- **Target population:** individuals who *publicly present AI-leadership titles* on LinkedIn. State this narrowly and honestly — it is **not** "all AI leaders," and the gap between the two is itself a limitation (the title-gated frame structurally excludes competent-but-untitled leaders, colliding with your "under-signalled expert" category).
- **Frame:** results returned by a defined set of title-based search queries on a defined date, within defined filters.

### 5.2 Inclusion / exclusion criteria *(fix before collection; do not adjust mid-collection)*
- **Include:** profile publicly presents a qualifying AI-leadership title (from a pre-registered title list, e.g. "Chief AI Officer," "Head of AI," "VP of AI/ML," "Director of AI," "AI Lead"); profile is publicly viewable; language within your fixed scope (§ language decision).
- **Exclude:** duplicate of an already-captured individual; profile not publicly viewable without login/connection; title outside the pre-registered list; language outside scope; obvious non-person/company page.

### 5.3 Query and quota design
- Pre-register the **exact query strings**, the platform surface, filters, and the target count per query. Record `search_query`, `search_rank_position`, `collection_ts`, `inclusion_reason` for every record (the schema mandates these).
- **Sample-size honesty:** 500 is a defensible pragmatic target for an MSc, but state *why* 500 (feasibility of manual coding, not a power calculation). For RQ4 correlation, note descriptively what magnitude of association 500 profiles could detect; a full power analysis is optional at MSc level but strengthens the design.

### 5.4 Selection-bias disclosures *(mandatory in the thesis)*
Title-gating; algorithmic ranking and truncation of search results (not a random draw); language/geography skew; self-presentation/completeness variation. These do not invalidate the audit but bound its generalisability — state them in Methods, not just Limitations.

---

## 6. LinkedIn Collection Protocol

**[BLOCKER] [INSTITUTIONAL]** Do not finalise or execute this until §2 and §3 are approved.

### 6.1 Method — the decision that matters most
**Reviewer recommendation: manual, human-driven collection.** A human viewing public profiles and recording the ALCSM-relevant fields by hand into the pseudonymised database avoids the "automated means" prohibition that produced the hiQ judgment, and keeps volume proportionate. It is slower — but 500 profiles is manually tractable over a defined collection window, and it is far more defensible at examination and to a DPO than automated scraping. If you or your supervisor believe an automated method is necessary, that decision must be taken *with* the DPO and legal/IT, documented, and justified against the ToS exposure — do not default into it. **[INSTITUTIONAL]**

### 6.2 Pseudonymisation at capture *(not after)*
Assign `PRF-#####` at the moment of capture. Record only the ALCSM-relevant field content and the RQ4 indicators. **Do not** store name, profile URL, photograph, or contact details in the research database. If a temporary mapping is used (§4.1 option 2), it lives outside the database.

### 6.3 What to capture, per the frozen schema
Section text into `profile_raw_section` (with `section_available` set correctly — the empty-vs-not-retrieved distinction matters); provenance fields; `activity_data_collected` flag set only if post-level activity is collected, which needs its own ethics justification (§3, and the frozen ethics flag). Nothing here changes the schema.

### 6.4 Collection window and consistency
Fix a **collection window** (e.g. a two-week period) and hold query definitions constant within it, so `collection_ts` bounds the temporal validity of findings. Record deviations in the collection log.

### 6.5 Collection log
Maintain a running log (outside the research DB): date, queries run, counts returned vs. included, exclusions and reasons, anomalies. This is your audit trail and feeds the Methods chapter.

---

## 7. Job-Posting Collection Protocol

Lower personal-data sensitivity (postings are org-authored, though named recruiters may appear — avoid capturing individual recruiter data). **[Thesis-specific]**

- **Sources:** pre-registered job boards/platforms; record `posting_source`, `search_query`, `collection_ts`, `posting_language`, `posting_geography`, `posted_date`.
- **Retain raw text.** `raw_posting_text` is `NOT NULL` in the schema precisely because taxonomy anchoring and requirement scoring need verbatim text, not summaries. Capture the full posting and the requirements section.
- **Inclusion:** AI-leadership-relevant role at the target seniority, per a pre-registered rule mirroring the profile title list.
- **ToS note:** the same "automated means" caution applies to job boards; check each source's terms, and prefer manual capture for a 200-item corpus. **[INSTITUTIONAL where a source's ToS is restrictive]**
- **Recruiter privacy:** if a posting names an individual recruiter, do not record that individual's personal data; the unit of analysis is the posting's *requirements*, not the poster.

---

## 8. File Organisation

**[Convention]** A clean, reproducible layout. Personal data never leaves the secure store; the repository holds only code, schema, and non-personal artefacts.

```
alcsm-thesis/
├── README.md
├── docs/
│   ├── framework/            # frozen ALCSM v1.0 documents (read-only reference)
│   ├── ethics/               # ethics application, approvals, privacy notice
│   ├── gdpr/                 # LIA, DPIA, DMP
│   └── protocols/            # sampling, collection, annotation, reliability
├── schema/
│   ├── alcsm_schema_v1.0.1.sql
│   ├── alcsm_patch_v1.0.0_to_v1.0.1.sql
│   └── alcsm_optional_recommendations.sql
├── validation/
│   ├── alcsm_validation_harness_v1.0.1.py
│   └── alcsm_gap_probes_v1.0.1.py
├── src/                      # NLP pipeline, analysis code (later tasks)
├── annotation/
│   ├── codebook/             # frozen rulebook + precedent library (reference)
│   └── logs/                 # coding logs, revision log exports (NON-personal)
├── outputs/                  # aggregate results, figures (NO personal data)
└── .gitignore                # excludes any data/, secrets, credentials
─────────────────────────────────────────────────────────────────
SECURE STORE (NOT in the repo, university-approved, access-controlled):
  data/  → the PostgreSQL database, raw captures, any temporary mapping
```

**Hard rule:** the `data/` directory and any credentials are **never** committed. `.gitignore` must exclude them, and this should be verified before the first commit. *[Established / security]*

---

## 9. Version-Control Strategy

**[Convention]** Git for code, schema, and documents. **Never for personal data.**

- **Repository scope:** code, frozen framework docs, schema, protocols, aggregate outputs. No `data/`, no secrets.
- **Tags for frozen artefacts:** tag the frozen states — `framework-v1.0`, `schema-v1.0.1` — so the thesis can cite exact commits.
- **Branching:** lightweight. `main` stays runnable; use short-lived branches for pipeline/analysis work in later tasks.
- **Commit hygiene:** meaningful messages; reference the task/section. The schema already records `code_commit_hash` on NLP runs, so keeping commits clean feeds reproducibility.
- **Secrets:** database credentials and any API keys in environment variables or an ignored secrets file, never committed. Pre-commit check for accidental secrets recommended.
- **Data snapshots:** if you must version data states, snapshot *inside the secure store* with dated encrypted dumps, referenced by ID from the repo — the data itself stays out of Git.

---

## 10. Annotation Workflow

**[Frozen rulebook — operationalised, not modified]**

1. **Rater onboarding.** Both raters read the frozen rulebook and precedent library (P-01–P-15), then jointly code 2–3 non-sample practice profiles, discussing discrepancies. Practice profiles are excluded from all reliability figures.
2. **Interface constraints (from the frozen design).** The annotation interface must (a) present one profile's six dimensions together; (b) **never** display RQ4 criterion values during coding (predictor/criterion contamination); (c) prevent a rater from seeing the other rater's scores before both submit (blind cross-check); (d) capture evidence spans, missing-status, ambiguity/contradiction flags, precedent applied, and verification metadata (D4 only).
3. **Coding order.** Score all six dimensions for one profile before moving on, to limit sequential-context bias.
4. **Logging.** Every score writes a full coding-log row (schema-enforced). No score sheet exists detached from its evidence.
5. **Verification discipline.** External verification only for D4, only via profile-provided links or standard public indices, never score-inflating — enforced by the schema's `CHECK` constraint, so it cannot be violated even by accident.

---

## 11. Double-Coding Protocol

**[Frozen design — operational detail]**

- **Subset selection *(a decision you still owe, from Task 4)*.** Decide which records are double-coded. **Reviewer recommendation:** either double-code **100%** if two raters and 500 profiles is feasible within your timeline, or a **randomly selected ≥15%** if not. If you sample, the selection must be **random and pre-registered** — a non-random double-coded subset means reliability does not generalise to the full corpus, which an examiner will challenge. State the method and seed. **[Thesis-specific] [BLOCKER before main coding]**
- **Independence.** The two raters code the double-coded records independently, with no communication about specific profiles, submitting complete logs before any comparison.
- **What "independent" requires here.** State who the raters are and their expertise. If you must be one of the two coders, pair with a second coder who is, as far as possible, blind to the hypotheses, and disclose the arrangement — researcher-expectancy bias is a real threat on the low-verifiability dimensions (D5, D6). **[Thesis-specific]**

---

## 12. Reliability Workflow

**[Frozen method — operational sequence]** Schema already stores results in `reliability_result` and protects the input via `v_reliability_input`.

1. **Pilot first.** Run the 10–20-profile purposive pilot (clear, borderline, sparse, contradictory, under-signalled, inflation cases) before main coding.
2. **Compute per dimension, never pooled.** Krippendorff's α for each of the six dimensions separately, on independent pre-adjudication rows only (`v_reliability_input` enforces this; the v1.0.1 role-alignment constraint prevents a mis-flagged row from silently corrupting it).
3. **Report with diagnostics.** For each α: bootstrap confidence interval, raw percentage agreement, `n_units`, and `score_variance` — because low variance on D5/D6 can deflate α despite high raw agreement. All these columns exist in the frozen schema.
4. **Decision rule (from the frozen framework).** α ≥ .80 proceed; .667–.80 acceptable with a review of disagreement cases; < .667 revise the *rulebook wording* (never the frozen criteria) via the revision-log procedure and re-pilot. Expect D5/D6 to be lower — state this expectation *before* running the pilot so a low value reads as confirmed, not discovered.
5. **Sustained reliability.** Double-code the agreed subset of the *main* sample too, and report reliability on it — reliability is not a one-time pilot gate; drift over 500 profiles is real.
6. **Adjudication.** Disagreements resolved per the frozen tie-break (magnitude 1 → consensus permitted; ≥ 2 → escalate; now enforced by the v1.0.1 constraint), stored additively; α always computed on pre-adjudication scores.

---

## 13. Data-Quality Checklist

Run these before analysis. The Task 4 validation plan's integrity queries (Q-01…Q-14) are the technical layer; this is the research layer on top.

- [ ] Every profile has provenance (`search_query`, `inclusion_reason`, `collection_ts`) — schema-enforced, verify anyway.
- [ ] `section_available` correctly distinguishes empty from not-retrieved on every raw section.
- [ ] Missing-status coding coherent: no `absent_stated` without evidence, no `unavailable` with evidence (v1.0.1 enforces; confirm zero violations).
- [ ] Completeness computed on denominator = 6 (v1.0.1 correction applied); low-completeness records flagged as a separate analytic category.
- [ ] Contradiction flags (`title_substance_contradiction_flag`) populated where P-03 applies — this is your primary phenomenon, not noise.
- [ ] Every human score traceable to an evidence span.
- [ ] Double-coded subset is the pre-registered random selection; reliability computed on pre-adjudication rows only.
- [ ] RQ4 criterion values physically separate from dimension scores; no criterion variable derived from any dimension (circularity check), and no D4-overlapping metric reused as criterion.
- [ ] Job postings retain full raw text; requirement `not_applicable` rows excluded from `Gap_i`, not read as zero.
- [ ] No special-category data recorded (Article 9 rule honoured).
- [ ] No direct identifiers anywhere in the research database.

---

## 14. Collection-Readiness Checklist *(the final gate)*

**Do not collect a single profile until every [BLOCKER] item is checked.**

**Governance — [BLOCKER]s**
- [ ] Ethics approval obtained (reference recorded).
- [ ] GDPR legal basis documented; LIA written for the LinkedIn strand.
- [ ] Article 14 position decided with the DPO (public privacy notice published, and/or notification approach justified).
- [ ] DPIA completed or DPO confirmation in writing that none is required.
- [ ] Controller identified; storage confirmed EEA-resident and access-controlled.
- [ ] Collection **method** decided with supervisor/DPO in a way that does not breach LinkedIn's ToS (manual collection recommended).
- [ ] Re-identification-mapping decision made and documented (§4.1).

**Design**
- [ ] Sampling frame, title list, inclusion/exclusion criteria pre-registered and frozen.
- [ ] Query strings and quotas pre-registered.
- [ ] Language/localisation scope fixed.
- [ ] Collection window defined.
- [ ] Activity observation window fixed (for RQ4 engagement).

**Operations**
- [ ] Secure store provisioned; database deployed from `alcsm_schema_v1.0.1.sql`.
- [ ] Reference data loaded (6 dimensions, 4 missing states, 15 precedents with real text, raters).
- [ ] Taxonomy anchoring plan ready (raw job-posting text captured first, then term lists stamped as a `taxonomy_version`); F-06 NOT-NULL enabled only after anchoring.
- [ ] Repository initialised; `.gitignore` verified to exclude `data/` and secrets.
- [ ] Annotation interface honours the four frozen constraints (§10.2).
- [ ] Raters onboarded; double-coding subset selection pre-registered.
- [ ] Pilot profiles selected (purposive, difficulty-stratified).

**Sign-off**
- [ ] Supervisor sign-off that governance blockers are cleared.
- [ ] Data-quality checklist (§13) dry-run on the pilot data returns clean.

---

## 15. Reviewer's closing note

The operational parts of this task (§8–§14) are straightforward and the frozen schema already does much of the enforcement for you. The part that genuinely determines whether this thesis is defensible — and whether it exposes you or the university to risk — is §2–§3 and the collection-method decision in §6.1. My strongest single recommendation: **take the ethics application, the GDPR assessment (including the DPIA question and the Article 14 notification question), and the collection-method decision to your supervisor and DPO as one package, before you build the annotation interface or write a line of collection code.** Everything downstream is cheap to change now and expensive to change after you have collected 500 people's data on a basis that later proves unsound.

I have not modified ALCSM v1.0 or Schema v1.0.1 anywhere in this document.
