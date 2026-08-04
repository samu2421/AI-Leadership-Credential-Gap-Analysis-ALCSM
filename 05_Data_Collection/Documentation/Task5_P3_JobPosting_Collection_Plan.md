# P3 Job Posting Collection Plan

**Version:** 0.1-DRAFT
**Status:** Planning document only. No job posting has been collected under this plan. Execution remains gated on the P2 ethics/GDPR position covering the posting corpus and on `Implementation_Phase_Roadmap.md` §3 (P3)'s dependency on P2.
**Purpose:** formalise and extend the job-posting collection design already reasoned through in `Task5_PreCollection_Roadmap.md` §7, into an implementation-ready plan covering sources, eligibility, storage, QA, and taxonomy-anchoring preparation for the ~200-posting corpus. Changes no ALCSM methodology and no database schema — it specifies how the frozen `sampling_batch` (`corpus='job_posting'`) → `job_posting` structure is populated, and how that corpus feeds `taxonomy/anchoring.py` (P3's other deliverable).
**Last Updated:** 2026-08-02
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance, Phase P3 Session 1
**Related documents:** `Task5_PreCollection_Roadmap.md` §7, `ALCSM_Measurement_Specification_v1.0.md` §2 (the eight taxonomies), `src/alcsm/taxonomy/anchoring.py`, `Task5_P3_Sampling_Framework_Design.md` (the profile-side counterpart this plan mirrors)

---

## 1. Purpose within P3

Job postings are the *required*-side corpus: RQ2's credential-gap analysis (`v_credential_gap_by_dimension`) compares what postings ask for against what profiles show. The postings corpus also supplies the vocabulary that anchors the eight frozen taxonomies' term lists (structure frozen; content anchored here — `PROJECT_CONTEXT.md` §17, §44). Both uses depend on the same ~200-posting corpus, collected once, under one plan.

## 2. Sources

- **Pre-registered job boards/platforms only** — the exact source list is fixed before collection begins and held constant across the window. **[INSERT: final source list, e.g. LinkedIn Jobs, a general job board, and/or company career pages — to be confirmed by the author.]**
- Each source's Terms of Service is checked before use; a source with restrictive ToS around automated *or* bulk manual extraction is either excluded or collected under an explicitly institution-approved exception (`Task5_PreCollection_Roadmap.md` §7, "ToS note"). This mirrors, for postings, the same `hiQ Labs v. LinkedIn` reasoning already governing the profile side (`ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §1) — the legal exposure of automated collection is not specific to LinkedIn profiles.
- **Method: manual, human-driven collection**, matching the profile side exactly. No scraping, no browser automation, no API usage, no bulk-download tooling. A 200-item corpus is manually tractable within a defined window, the same proportionality argument already accepted for the 500-profile corpus.

## 3. Eligibility rules (inclusion criteria)

A posting is included only if **all** of the following hold:
1. Advertises an AI-leadership-relevant role at a qualifying seniority level, judged against a title/seniority rule that **mirrors, but is not required to be byte-identical to,** the profile-side title list in `Task5_P3_Sampling_Framework_Design.md` §3 — postings use job-ad language ("Head of AI wanted," "seeking a Director of Machine Learning") which is typically already close to the profile-title vocabulary. **[INSERT: final posting-title/seniority rule, pre-registered before collection.]**
2. Publicly accessible without login/paywall beyond the same logged-out-preferred/logged-in-fallback policy already governing profile collection.
3. Within the pre-registered language scope (recommended: matching the profile-side decision, so the two corpora remain comparable — see the open item in `Task5_P3_Sampling_Framework_Design.md` §4.3).
4. Has a substantive requirements section (not a placeholder/expired listing with no real content) — a posting that is essentially a title and nothing else cannot support taxonomy anchoring or requirement scoring, and is excluded at intake rather than captured as a near-empty record.

## 4. Exclusion criteria

Excluded, with the reason logged against the batch:
- Title/seniority outside the pre-registered rule.
- Not publicly accessible within the permitted browsing policy.
- Language out of scope.
- Duplicate posting (same role, same employer, re-posted or cross-posted across sources within the collection window — see §9).
- Expired or content-free listing (§3.4).
- A posting that is, in substance, a *recruiting agency* advertisement not tied to one specific role/employer (the unit of analysis is a specific role's requirements, not an agency's general pitch).

## 5. Storage workflow

- One `sampling_batch` row per pre-registered query/source combination, `corpus='job_posting'` — structurally identical pattern to the profile side, using the same `create_sampling_batch()` function in `collection/helper.py` (which already accepts `corpus` implicitly via the fixed `'profile'` literal for profiles; **see the Task 2 finding below — this function currently hard-codes `corpus='profile'` and has no job-posting equivalent yet**, a genuine, scoped gap this plan surfaces for Session 2, not fixed here).
- `posting_id` format: `JOB-#####` (schema-enforced `^JOB-[0-9]{5}$`), assigned at capture, sequential, never reused.
- **Full verbatim retention:** `raw_posting_text` (`NOT NULL` in the schema) captures the entire posting; `raw_requirements_text` captures the requirements section specifically where the posting structurally separates one out. Verbatim retention is required because taxonomy anchoring cannot operate on a paraphrased summary (`job_posting.raw_posting_text` column comment, schema file).
- Provenance fields captured per posting, mirroring the profile side exactly: `sampling_batch_id`, `search_query`, `search_rank_position`, `inclusion_reason`, `collection_ts`, `posting_language`, `posting_geography`, `posted_date`, `seniority_label_raw`.
- All data enters the same access-controlled, EEA-resident secure store as the profile corpus — no separate storage arrangement, no personal-laptop or consumer-cloud staging, ever, even for the (lower-sensitivity) posting corpus.

## 6. Quality assurance

- **Structural validation:** a job-posting equivalent of `validate_profile_record`/`insert_profile` is needed (currently does not exist — see the Task 2 finding and Session 2 recommendation) to enforce, before insert: `posting_id` format, provenance completeness, controlled-vocabulary `inclusion_reason`, ISO-code shape for `posting_language`/`posting_geography`, and non-empty `raw_posting_text`.
- **Per-batch spot-check:** mirrors §9 of the sampling framework design — after each batch closes, a sample of included postings (≥10%, minimum 3) is re-checked against the collection log for correct classification and transcription fidelity.
- **Recruiter-privacy check (posting-specific QA step, no profile-side equivalent):** every included posting is checked for an incidentally-named individual recruiter (a person's name/contact in the posting body, e.g. "Contact Jane Smith at..."). Where present, that individual's name/contact detail is **not** transcribed into `raw_posting_text` — it is redacted at transcription time, with a note in the collection log that a redaction occurred (not what was redacted). The unit of analysis is the posting's *requirements*, never the poster (`Task5_PreCollection_Roadmap.md` §7).

## 7. Manual verification workflow

- **Pre-insertion:** the collector reads the live posting and transcribes `raw_posting_text`/`raw_requirements_text` and the provenance fields directly — no automated extraction step exists to verify against, by construction, mirroring the profile side.
- **Post-insertion:** a posting-side `verify_posting()` (to be built alongside the storage helper in §5/§9) re-reads the inserted row and confirms `raw_posting_text` is non-empty and the recruiter-redaction check was applied — the posting-side analogue of `verify_profile()`.
- **Taxonomy-anchoring readiness check (posting-specific, run once the full corpus is collected, before `taxonomy/anchoring.py` is invoked):** confirm every included posting has non-null `raw_posting_text`, since `anchor_taxonomy_from_postings()` depends on that field being populated for the whole corpus, not a partial one — anchoring runs once, over the complete ~200-posting set, not incrementally per batch (partial-corpus anchoring would bias term-frequency counts toward whichever batches happened to run first).

## 8. Taxonomy preparation (the P3-specific deliverable this corpus exists to support)

This plan does **not** perform anchoring — `taxonomy/anchoring.py` remains a P3-Session-2-or-later implementation task, explicitly gated on the full corpus existing (its own module docstring: *"implement once ~200 job postings are collected"*). What this plan prepares:

- **Eight target taxonomies** (structure frozen, content to be anchored): degree, certification, `ai_role`, `leadership_level`, `technical_contribution`, `professional_engagement`, `ai_keyword_ontology`, `automation_augmentation` — matching `taxonomy_version.taxonomy_name`'s CHECK constraint exactly (schema file, §1).
- **Anchoring procedure (already defined in `Task5_PreCollection_Roadmap.md`, restated here for this corpus specifically):** once the corpus is complete, extract candidate terms from `raw_posting_text`/`raw_requirements_text` per taxonomy category, count `source_frequency` per term, and stamp a `taxonomy_version` row (`taxonomy_version_id` e.g. `TAX-1.0`, `anchored_to_batch` recording which posting batch(es) fed it) before freezing it (`frozen=TRUE`). **No term may be invented without evidence in the posting text** (`PROJECT_CONTEXT.md` §27) — this is a hard constraint on the anchoring step this corpus feeds, not a new rule introduced here.
- **F-06 activation:** `taxonomy_version_id NOT NULL` on `alcsm_dimension_score`/`job_requirement_score` is enabled only *after* a taxonomy version is stamped and frozen from this corpus — never before (`DECISION_LOG.md` D-0014; `PROJECT_CONTEXT.md` §17).
- **What this plan explicitly leaves open for Session 2 or a dedicated P3 anchoring session:** the extraction method itself (keyword frequency threshold, manual review of candidate terms before freezing, etc.) is an implementation detail of `taxonomy/anchoring.py`, not decided in this collection plan.

## 9. Version tracking

- This plan is versioned (`0.1-DRAFT` → future bumps) independently of the sampling framework design, but the two are intended to move together where they share a decision (e.g. language scope) — a change to one should trigger a check of the other, not an automatic edit.
- `sampling_batch.inclusion_protocol_version` (job-posting batches) records which version of *this* plan's eligibility rule governed a given batch, exactly mirroring the profile-side mechanism in `Task5_P3_Sampling_Framework_Design.md` §11.
- Once anchored, a `taxonomy_version` is **frozen** and never edited in place — a later change to term-list content is a new version, never a retroactive edit to a version already used to score anything (`PROJECT_CONTEXT.md` §37).

---

## 10. Gaps this plan surfaces (not fixed here — for the Task 2 review and the Session 2 recommendation list)

1. `collection/helper.py` has no job-posting write path today — only `create_sampling_batch()` (hard-coded `corpus='profile'` in its INSERT), `insert_profile()`, and `verify_profile()` exist. A `create_job_posting_batch()`/`insert_job_posting()`/`verify_posting()` trio, structurally parallel to the profile-side functions, is needed before any real posting collection can begin.
2. No recruiter-redaction helper or check currently exists in code — §6's redaction step is presently a manual, undocumented-in-code discipline; it could be encoded as a lightweight validator (e.g. rejecting an obviously-named contact pattern) in the same way `_FORBIDDEN_IDENTIFIER_FIELDS` works for profiles, but that is a Session 2 implementation decision, not made here.
3. `taxonomy/anchoring.py`'s extraction method is unspecified beyond "seed term lists from posting vocabulary" — a concrete algorithm/threshold choice is needed before it can be implemented.

## 11. What this document does not do

- It does not collect any real job posting.
- It does not change `sampling_batch`, `job_posting`, `taxonomy_version`, or `taxonomy_term` in the schema.
- It does not implement `taxonomy/anchoring.py` or any job-posting write path — see §10.
- It does not resolve its own `[INSERT: ...]` open items (source list, posting-title rule) — author decisions, flagged for approval.

---

*This plan draws on `Task5_PreCollection_Roadmap.md` §7, extending rather than replacing it. No frozen ALCSM methodology or database schema element is altered by this document.*
