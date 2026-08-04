# P3 Sampling Framework Design — LinkedIn Profile Corpus

**Version:** 0.1-DRAFT
**Status:** Design document only. No real data has been collected under this framework. Execution remains gated on real ethics-committee approval, DPO sign-off, and the `Task5_Implementation_Readiness_Checklist.md` §3 exit criteria — see that document and `Implementation_Phase_Roadmap.md` §7.
**Purpose:** formalise, extend, and operationalise the profile-sampling design already reasoned through in `Task5_PreCollection_Roadmap.md` §5 and `04_Ethics/01_Ethics_Approval/ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §3, into a single implementation-ready reference for the ~500-profile corpus. This document changes no ALCSM methodology and no database schema — it specifies how the frozen `sampling_batch` → `profile` → `profile_raw_section` structure (`03_Database_Design/02_Schema/alcsm_schema_v1.0.1.sql`) is populated.
**Last Updated:** 2026-08-02
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance, Phase P3 Session 1
**Related documents:** `Task5_PreCollection_Roadmap.md` §5, `Task5_LinkedIn_Collection_Workflow.md`, `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md`, `ALCSM_Measurement_Specification_v1.0.md` §2.4 (leadership-level taxonomy), `src/alcsm/collection/helper.py`

---

## 1. Target population

Individuals who **publicly present a qualifying AI-leadership title** on LinkedIn. This is deliberately narrower than "all AI leaders in practice" — the frame structurally excludes competent-but-untitled leaders (the "under-signalled expert" category ALCSM itself is designed to detect). This gap is a disclosed limitation of the design, not something this framework attempts to correct (`ALCSM_Measurement_Specification_v1.0.md` §7.6; `PROJECT_CONTEXT.md` §43).

**Frame:** the union of results returned by a fixed set of pre-registered title-based search queries, run on a fixed date/window, within fixed filters. The frame is *purposive/title-based*, not a probability sample — this must be stated as such in the Methods chapter, never described as random or representative.

## 2. Sampling strategy

- **Design:** purposive, quota-free, title-gated sampling with pre-registered per-query targets. No stratified or probability-proportional design is applied — every included profile must satisfy the same inclusion rule, applied uniformly by search query and processed in the order search results return them.
- **Result-order discipline:** results are worked through as returned; they are never re-ordered, filtered by perceived "quality," or cherry-picked. Algorithmic-ranking bias is a disclosed limitation (§7 below), not something to correct by hand-selection.
- **Batch structure:** collection is organised into `sampling_batch` rows (`corpus = 'profile'`), one row per documented, reproducible search — never one giant undocumented sweep. Each batch has a fixed `search_query`, a start/end timestamp pair, a `result_set_size` (denominator for selection-rate reporting), and a `records_included` count.
- **Target:** ~500 profiles in total, reached by running successive pre-registered queries/batches until the target is met or the pre-registered query list is exhausted (whichever comes first — the list is not open-endedly expanded mid-collection to "top up" the count, since that would silently change the frame after the fact).

## 3. Title list and normalisation strategy

**Do not invent a new taxonomy.** The title list is an *operational sampling filter*, distinct from the frozen leadership-level taxonomy (`ALCSM_Measurement_Specification_v1.0.md` §2.4) that later *scores* D5. Conflating the two would let the sampling frame quietly pre-judge the D5 score — a halo risk at the frame level. This section only specifies which titles bring a profile *into* the sample; scoring is untouched.

- **Qualifying-title source list** (to be pre-registered verbatim before collection begins, drawn from titles already cited across the frozen documents — `Task5_PreCollection_Roadmap.md` §5.1, the Collection Protocol §3, and the taxonomy's Tier 3–5 examples): e.g. *Chief AI Officer, Chief Data Officer, Chief AI/ML Scientist, VP of AI, VP of Machine Learning, Head of AI, Head of Data Science, Director of AI, Director of Machine Learning, AI Lead, ML Lead*. **[INSERT: final, exact, pre-registered list — must be fixed before the collection window opens and never edited mid-window.]**
- **Normalisation procedure (applied by the human collector before an inclusion/exclusion decision, not by any automated matcher):**
  1. Read the profile's headline/current-position title exactly as displayed.
  2. Strip company name, emoji, and decorative punctuation only (e.g. "Jane D. | Chief AI Officer @ Acme 🚀" → "Chief AI Officer").
  3. Match the normalised string against the pre-registered title list using two tiers:
     - **`title_match`** — exact (case-insensitive) match to a list entry.
     - **`title_variant_match`** — a documented equivalent variant (e.g. "Head of Artificial Intelligence" as a variant of "Head of AI"); the variant mapping itself is pre-registered, not decided ad hoc per profile.
  4. A title not matching either tier is **excluded**, full stop — it is not escalated to a subjective "does this basically count" judgement call during collection. (A separate, rare `manual_review_included` path exists in the schema's `inclusion_reason` CHECK constraint for documented edge cases the collector flags for the researcher's own later review, decided outside the live collection session, never in the moment.)
- **Why this three-way `inclusion_reason` split matters:** it is queryable after the fact — a reviewer or examiner can ask "how much of the sample came from exact matches vs. variants vs. manual inclusion?" without re-deriving it from notes.

## 4. Inclusion criteria

A profile is included only if **all** of the following hold:
1. Publicly presents a qualifying title per §3.
2. Publicly viewable (see the logged-out/logged-in fallback policy in `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §2).
3. Within the pre-registered language scope. **[INSERT: final language scope, e.g. "English-language profiles only" — this is an intentionally-open decision per `PROJECT_CONTEXT.md` §44/§46 and must be fixed by the author before collection, not decided by this document.]**
4. Not already represented in the sample (§6, deduplication).

## 5. Exclusion criteria

Excluded, with the reason logged against the batch (not silently dropped):
- Title outside the pre-registered list/variant map.
- Not publicly viewable (requires login/connection beyond the permitted fallback).
- Language out of scope.
- Duplicate of an already-captured individual.
- Obvious non-person page (company page, product page, bot/spam account).
- Profile content that is essentially empty (no section beyond a bare name/title) — logged as an exclusion, not a `present`-with-nothing profile, since an empty profile at the sampling stage is a frame decision, not a D1–D6 missing-status decision.

## 6. Country / geography and industry filters

- **Geography:** no blanket country inclusion/exclusion filter is applied at the query-design stage beyond what the pre-registered query strings themselves target (e.g. if a query is scoped to a platform-level geography filter, that scoping is part of the pre-registered query, recorded in `sampling_batch.search_query`/`notes`). `profile.profile_geography` (ISO 3166-1 alpha-2) is captured **per profile** at collection time from the profile's stated location, purely as a descriptive/provenance field — it is not used to admit or reject a candidate. **[INSERT: confirm with the author/DPO whether a geography scope restriction is wanted for this study, e.g. "EEA + UK + US only" — currently open, consistent with `PROJECT_CONTEXT.md` §44's language/localisation-scope item.]**
- **Industry:** ALCSM's population is defined by *title*, not industry/sector. No industry filter is applied — an "AI Lead" at a bank and an "AI Lead" at a software company are both in-frame. If the query platform surface itself exposes an industry facet, it is not used as a filter, to avoid silently narrowing "AI leadership" to "AI leadership in tech."

## 7. Language handling

- `profile_language` (ISO 639-1, or `und` if undetermined) is captured per profile at collection, matching the schema's default.
- The pre-registered language scope (§4.3) determines *inclusion*; `profile_language` itself is recorded regardless, for two reasons: (a) it is the descriptive field the gap/analysis modules will eventually report against, and (b) it lets a later reviewer audit that the inclusion rule was actually followed.
- Non-English (or out-of-scope-language) credentials that appear *within* an otherwise in-scope profile (e.g. a non-English certification name) are handled by the existing frozen precedent **P-11** (map if defensible, else default-low, log verbatim) — this is an annotation-time rule, already frozen, and is not re-specified here.

## 8. Duplicate detection

- **Within-session, transient check only** (per `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §6): before capture, the collector confirms the candidate is not already represented in the sample. This check uses a session-local working list (e.g. a scratch note of titles+companies+approximate-names already captured this session) that is **discarded at the end of each collection session and never persisted into the research database** — the database itself stores no name or other discriminator that would make a persistent duplicate-check index possible.
- **Cross-batch/cross-session duplicate risk:** because the transient check does not persist, a duplicate could in principle slip through across two different sessions. Two independent mitigations, both pre-registered rather than improvised:
  1. Query design deliberately minimises overlap between batches (e.g. different title queries, or the same title query on a materially later date so the ranked result set has moved on).
  2. A **secondary, session-local re-check** is run at the end of each batch, comparing that batch's just-captured `search_query` + normalised-title + approximate-seniority combination against the *prior* batch's equivalent working notes (kept only for the duration of the collection window, then destroyed) — not against the database, and not retained past the collection window.
- **What this does not do:** it does not, and cannot, guarantee zero duplicates with mathematical certainty without storing a persistent identifying discriminator — which would itself violate the no-persistent-mapping default (§9 of the Collection Protocol). This trade-off is disclosed, not hidden.

## 9. Quality control

- **Per-batch spot-check:** after each `sampling_batch` closes, a sample of its included records (e.g. 10%, rounded up to at least 3) is re-opened by the researcher and checked against the collection log for: correct `inclusion_reason` classification, section-availability coherence (`section_available=False` carrying no text), and absence of any forbidden identifier field — mirroring what `collection/helper.py`'s `validate_profile_record` already enforces structurally, but checked here at the *content* level the validator cannot see (e.g. "does this transcribed text actually match what a human would read on the page," which no automated check can verify).
- **Structural validation is automatic and non-negotiable:** every insert already passes through `validate_profile_record` (profile-ID format, provenance completeness, controlled-vocabulary `inclusion_reason`, ISO code shape, section coherence, activity-ethics gate) before it reaches the database — see Task 2 review. Quality control here is about what that validator *cannot* check: transcription fidelity and inclusion-rule judgement calls.
- **Escalation:** a spot-check finding (e.g. a misclassified `inclusion_reason`) is logged in the collection log with the correction applied at the source record, never silently patched without a note — consistent with the project's standing "report, don't silently fix" discipline.

## 10. Batch management

- One `sampling_batch` row per pre-registered query, `corpus='profile'`, created via `collection/helper.py`'s `create_sampling_batch()` (idempotent — a re-run with the same `sampling_batch_id` is a no-op, not a duplicate).
- `sampling_batch_id` format: `BATCH-###` (schema-enforced `^BATCH-[0-9]{3}$`), allocated sequentially at the start of each session, never reused.
- A batch is opened (`collection_started_ts` set) only once its query string and inclusion-protocol version are finalised; it is closed (`collection_ended_ts`, `result_set_size`, `records_included` set) at the end of that session — a batch is never left open across sessions.
- `inclusion_protocol_version` ties every batch to the exact version of this document (and the title/variant list it fixes) in force when that batch ran — see §11.

## 11. Sampling metadata, tracking IDs, and versioning

- **Profile tracking ID:** `PRF-#####` (schema-enforced `^PRF-[0-9]{5}$`), assigned at the moment of capture per the frozen pseudonymisation-at-capture rule — never before, never derived from any identifying value.
- **Provenance captured per profile (already schema-mandated, not new):** `sampling_batch_id`, `search_query`, `search_rank_position`, `inclusion_reason`, `collection_ts`, `profile_language`, `profile_geography`, `observation_window_days`, `activity_data_collected`.
- **Document versioning:** this design document itself is versioned (`0.1-DRAFT` → future minor/major bumps); `sampling_batch.inclusion_protocol_version` records *which* version of the title list/inclusion rule governed a given batch, so a later change to the title list (e.g. after author review) does not silently reinterpret earlier batches — it is visible, per-batch, which rule set applied.
- **No retroactive edits:** once a batch closes, its `inclusion_protocol_version` is fixed. If the inclusion rule changes, that is a **new** protocol version applied to **new** batches, exactly mirroring the frozen "rulebook wording, not criteria" revision pattern (`DECISION_LOG.md` D-0004) applied here to the sampling protocol rather than the coding rulebook.

## 12. Reproducibility

- Every profile is traceable to: the exact `search_query` string, the platform surface, the `search_rank_position` it held in that result set, the `collection_ts`, and the `inclusion_protocol_version` in force — sufficient to describe (though not to re-execute identically, since LinkedIn's live index changes) exactly how each record entered the sample.
- `sampling_batch.result_set_size` and `records_included` together let a later reader compute the realised selection rate per query, supporting the selection-bias disclosure required in the thesis Methods chapter (§13 below).
- The collection log (kept outside the database and outside Git, per `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §7) is the audit trail of record-level decisions; the database is the audit trail of what was actually captured. The two are cross-referenced by `sampling_batch_id`.

## 13. Audit logging

- **Collection log (operational, outside the repo and outside the database):** per `Task5_LinkedIn_Collection_Workflow.md` and the Collection Protocol §7 — session date, queries run, results returned vs. included, every exclusion and its reason, anomalies/deviations from this protocol.
- **Database-level audit trail:** `sampling_batch` itself *is* a structural audit record (one row per documented search); nothing about it needs to be duplicated in application code.
- **Deviation handling:** any deviation from this framework during a live session (e.g. a query returning far fewer results than expected, a title ambiguity not covered by the variant map) is logged in the collection log at the time it occurs, with the resolution taken — never resolved silently and never reconstructed from memory afterward.

## 14. Manual verification workflow

- **Pre-insertion:** the collector reads the live public profile and transcribes section text directly into the `ProfileRecord`/`ProfileSection` structures `collection/helper.py` already defines — no intermediate automated parsing step exists, so there is nothing to "verify against a scrape," by construction.
- **Post-insertion:** `verify_profile()` (already implemented, `collection/helper.py`) re-reads the inserted row set and confirms the section count and the empty/not-retrieved coherence rule hold in the database, as a defence-in-depth check independent of the pre-insertion validator.
- **Human cross-check (new to this design, not yet built — a Session 2 candidate, see the Final Report §6):** for the quality-control spot-check in §9, a second person (or the researcher at a later sitting) re-reads the *live* profile against the *stored* transcription for the sampled subset, checking fidelity — this is a manual, non-automated step, consistent with the "no automated verification of collection content" boundary.

## 15. Sampling checkpoints

Fixed points at which collection **pauses** for a documented check before continuing — not a rigid schedule, but a rule that these checks happen at these points, every time:

1. **After every batch closes:** run the §9 spot-check; confirm `records_included` and `result_set_size` are both recorded before opening the next batch.
2. **At every 100 profiles collected (~5 batches at ~20/batch, indicative only):** review the running `profile_geography`/`profile_language` distribution and the realised `inclusion_reason` split (exact vs. variant vs. manual) against expectations — not to "correct" the sample toward a target distribution (that would reintroduce the cherry-picking this framework explicitly avoids, §2), but to catch a structurally broken query (e.g. one query silently returning 90% non-person pages) before it wastes further collection time.
3. **Before the final ~50 profiles:** confirm the pre-registered query list still has capacity to reach ~500 without extending the list ad hoc; if it does not, that is an author decision (extend the pre-registered list as a new, dated addendum — never an undocumented on-the-fly expansion), not a collector's call.
4. **At collection close:** final tally against `sampling_batch` rows; selection-bias disclosure figures (§16) computed from the closed batches.

## 16. Selection-bias disclosures (mandatory in the thesis, carried forward from `Task5_PreCollection_Roadmap.md` §5.4)

To be stated in Methods, not buried in Limitations:
- **Title-gating** structurally excludes untitled-but-competent AI leaders (the direct collision with the "under-signalled expert" category ALCSM itself detects — `ALCSM_Measurement_Specification_v1.0.md` §7.6).
- **Algorithmic ranking and truncation** of platform search results means the sample is not a random draw over all qualifying profiles, even within the title frame.
- **Language/geography skew**, to the extent the pre-registered scope narrows either.
- **Self-presentation and completeness variation** — profiles differ in how much they disclose regardless of underlying credential, which is itself part of what the study measures, not a defect to correct for at the sampling stage.

---

## 17. What this document does not do

- It does not collect any real profile.
- It does not change `sampling_batch`, `profile`, or `profile_raw_section` in the schema — every field referenced above already exists in `alcsm_schema_v1.0.1.sql`.
- It does not change the D5 leadership-level taxonomy or any other frozen scoring criterion — the title list in §3 is a sampling-frame filter, structurally and conceptually separate from the scoring taxonomy it happens to draw examples from.
- It does not resolve the two `[INSERT: ...]` open items above (final title list, language/geography scope) — those are author decisions, flagged here for approval, not decided unilaterally.

---

*This design document draws on `Task5_PreCollection_Roadmap.md` §5 and `ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §3, extending rather than replacing them. No frozen ALCSM methodology or database schema element is altered by this document.*
