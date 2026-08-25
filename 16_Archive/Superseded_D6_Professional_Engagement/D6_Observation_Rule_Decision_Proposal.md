# D6 Observation Rule — Decision Proposal

**Version:** 1.0
**Status:** Proposal, pending author decision. Not an authorization to collect supplementary evidence. Nothing in this document has been executed — no data has been collected, no raw file has been modified, no annotation has occurred.
**Purpose:** resolve the D6 (Professional Engagement & Continuous Development) evidence gap identified in `P3_Final_Data_QA_Report.md` (Findings ALCSM-D6-01, EVID-01) by proposing a precise, reproducible observation rule, before any supplementary LinkedIn review is performed.
**Last Updated:** 2026-08-17
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

**Governing documents consulted:** `PROJECT_CONTEXT.md`, `CLAUDE_CODE_RULES.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `DECISION_LOG.md`, `Implementation_Phase_Roadmap.md`, `ALCSM_Measurement_Specification_v1.0.md`, `ALCSM_Coding_Rulebook_and_Pilot_Design.md`, `ALCSM_Annotation_Handbook.md`, `alcsm_schema_v1.0.1.sql`, `04_Ethics/01_Ethics_Approval/ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md`, `11_Implementation_Governance/Reviews/P3_Final_Data_QA_Report.md`.

---

## 0. What this document is and is not

This is a **decision proposal**, not a decision. It exists to give the author a single, complete basis for authorizing (or declining) supplementary D6 evidence collection. It does not itself authorize collection. Per instruction, no data was collected and no raw file was touched in producing it.

---

## 1. Frozen elements reaffirmed (not touched by this proposal)

- The D6 dimension itself (`d6_engagement`), its definition, and its theoretical anchor (Tadelis 2002, reputation as an ongoing/renewable signal) — unchanged.
- The 0–5 scoring rubric for D6 — unchanged, reproduced here only for reference:

  | Score | Criterion |
  |---|---|
  | 0 | No visible engagement |
  | 1 | Passive engagement (likes/shares) only |
  | 2 | Regular passive engagement, no original content |
  | 3 | Occasional original commentary |
  | 4 | Regular original commentary plus community membership |
  | 5 | Sustained thought leadership plus a community leadership role |

- The professional-engagement taxonomy's frozen *structure* (`ALCSM_Measurement_Specification_v1.0.md` §2.6) — unchanged. This proposal draws on the taxonomy's existing vocabulary; it does not add, remove, or rename a tier.
- The four missing-data states (`present`, `absent_stated`, `unavailable`, `not_applicable`) and their database semantics — unchanged; applied, not redefined.
- The formative-index model, the "signal not competence" framing, and the disclosed platform-usage-habit confound ("some strong people simply don't post... a known limitation to disclose, not to 'correct'") — unchanged and explicitly carried forward into §3 below.
- The frozen schema — no table, column, or constraint is proposed to be added, altered, or removed. §6 documents that every field this proposal needs already exists.

If any determination below appeared to require touching one of the above, it would be flagged here for author approval rather than proposed. None did — see §9 for the reasoning.

---

## 2. What observable evidence qualifies for D6

Evidence qualifies only if it is (a) publicly visible on the individual's LinkedIn profile without a connection or login beyond the already-approved logged-out-preferred/logged-in-fallback browsing policy, and (b) directly observable — not inferred, not assumed from seniority or company context, per the standing "never infer missing information" rule already governing every other dimension.

Within that boundary, evidence qualifying under the existing rubric vocabulary:

- **Original posts** the individual authored, visible on their public Activity/Posts feed, within the observation window (§3).
- **Reshares/reposts**, with or without added commentary, visible on the same feed within the window — the rubric's "passive engagement (likes/shares)" and "original commentary" tiers already require distinguishing a bare reshare from a reshare with substantive added commentary; that distinction is preserved, not introduced, here.
- **Publicly visible reactions (likes) or comments** the individual made on others' content, where LinkedIn's public activity view surfaces them.
- **Publicly stated community roles** — group membership, community organizer/leadership roles — where stated on the profile itself (e.g. a "Featured" or "About" mention, a listed group affiliation) or directly observable on the public activity feed.
- **Publicly stated continuing-education signal presented as ongoing engagement** (e.g. a listed course-in-progress, conference attendance/speaking role) — only where it is presented as activity/engagement rather than as a completed academic or certification credential. Where the same item could plausibly be read as a D1 (education) or D2 (certification) signal instead, the existing precedent **P-12** ("one artefact evidences two dimensions; each dimension is scored on its own criterion, no double-inflation") governs — this proposal does not change that precedent, it names it as the controlling rule for this boundary case.

## 3. What does not qualify

- **Anything not publicly visible** — connection-gated content, content requiring a login beyond the approved fallback, or content the collector could only see because of an existing connection to the individual. This is a restatement of the standing collection-method boundary, not a new rule.
- **Follower count, connection count, or reach metrics.** These are `rq4_impact_indicator` territory (network reach), which is **structurally isolated from ALCSM scoring by frozen design** — the schema gives it its own table and its own, separate `rq4_observation_window_days` field, deliberately distinct from `profile.observation_window_days`. Using a reach/follower figure as D6 evidence would violate the frozen predictor/criterion separation (`PROJECT_CONTEXT.md` §5, §15) and is explicitly excluded here to prevent that boundary being blurred in practice.
- **Content from any platform other than LinkedIn**, unless the profile's own LinkedIn content explicitly and visibly links or embeds it (e.g. a "Featured" section linking an external talk) — in which case the *LinkedIn presentation of it* is the evidence, not the external content itself.
- **Inferred engagement** — e.g. treating a senior title or a large company as implying an active public presence. Never inferred, per the standing rule already governing every other dimension.
- **Keyword presence used to raise a score** — an activity feed dense with AI-related terminology does not, by that fact alone, score higher; the ontology locates, it never scores (unchanged frozen rule, restated here because D6 is exactly the dimension where an "active-looking" feed could tempt this error).

## 4. Observation date and window

The schema already carries a dedicated, currently-unset field for this purpose: `profile.observation_window_days` ("Denominator context for engagement-based criterion variables; must be fixed and constant across records"). No new field is needed — a **value** needs to be fixed.

**Proposed rule:** a fixed window of **12 months immediately preceding `collection_ts`** for every profile where activity is observed, applied identically and without exception across the full collection batch. The window is anchored to each profile's own `collection_ts`, not to a single calendar date, so that profiles collected at different points in the collection window remain individually well-defined.

This specific figure (12 months) is a **proposal, not a decision** — it is offered as a defensible default (long enough to distinguish "occasional" from "sustained" per the rubric's own language, short enough to stay reproducible and manually tractable) and requires the same pre-registration-and-sign-off treatment already applied to the title list and language scope in `Task5_P3_Sampling_Framework_Design.md`. Once set, it must be fixed before any supplementary collection begins and not adjusted mid-collection, per the project's standing pre-registration discipline.

## 5. "Observed absence" vs. "unavailable / no evidence"

This is an application of the already-frozen four-state missing-data framework to the specific case of an activity feed, not a new distinction:

| Scenario | `profile_raw_section` (collection-time) | Later annotation-time `missing_status` | Score |
|---|---|---|---|
| The activity feed **is** publicly visible, and, applying the fixed window, shows no posts, reshares, comments, or community indicators. | `section_available = TRUE`, `section_text` records the observation (see §7) | `present` | 0 (per rubric: "No visible engagement" is itself the score-0 criterion — an observed, evidenced finding, not a data gap) |
| The activity feed **cannot** be viewed at all under the approved public-access method (e.g. the individual has restricted activity visibility, or no activity surface renders publicly). | `section_available = FALSE`, `section_text = NULL` | `unavailable` | 0 (per the existing frozen coherence constraint — `unavailable` implies score 0 and no evidence) |

Both rows numerically score 0, but they are not the same finding and must never be conflated: the first is confirmed information ("this individual, observably, does not engage publicly") and counts toward the profile's completeness index; the second is a data gap and does not. This mirrors precedent **P-13** ("stated absence vs. missing") applied to a collector's direct observation rather than a profile owner's textual claim — a distinct evidentiary situation the existing precedent did not previously need to cover explicitly, which is exactly why this proposal exists.

No missing value is converted into a substantive claim by this rule. An `unavailable` activity section is never read as "this person doesn't engage" — only an `available`-and-empty one is.

## 6. Fields to be stored for D6 evidence

**No new field, table, or constraint is required.** Every field this proposal needs already exists in the frozen schema:

| Field | Table | Role |
|---|---|---|
| `activity_data_collected` | `profile` | Ethics gate — set `TRUE` only for a profile where activity was actually observed under an approved justification (§8). Already carries the schema comment "separate ethics justification." |
| `observation_window_days` | `profile` | Carries the fixed window value from §4, constant across every profile with activity collected. |
| `section_name = 'activity'` | `profile_raw_section` | Already a valid, frozen value of the section-name vocabulary — no change to the `CHECK` constraint needed. |
| `section_text` | `profile_raw_section` | The verbatim/observational record described in §7, for the `activity` row. |
| `section_available` | `profile_raw_section` | Distinguishes "observed empty" from "unavailable" per §5, for the `activity` row — same mechanism already used for every other section. |
| `evidence_text`, `missing_status`, `score` | `alcsm_dimension_score` | Populated at annotation time (P4, out of scope here), using the collected `activity` section exactly as every other dimension already does. |

This is a load-bearing finding of this proposal: the schema anticipated D6/activity collection from the outset (the `activity` section value and the two dedicated `profile` columns existed before this gap was found) — the gap identified in the QA report was a **collection-execution gap**, not a missing design element.

## 7. Citation in the annotator evidence trail

D6 evidence is characteristically a *pattern* across several items (posting frequency, mix of original vs. passive activity, community role) rather than a single fact captured in one quoted sentence, unlike, say, a D1 degree title. The existing evidence rule ("quote, don't paraphrase") is preserved, adapted to that shape:

- Where a specific post or comment is cited as evidence, it is quoted verbatim, exactly as any other dimension's evidence.
- Where the evidence is a *pattern* (e.g. "regular original commentary" for a score of 4), `evidence_text` records the countable, dated basis for that pattern rather than a subjective summary — e.g. *"4 original posts observed in the 12-month window (dates: …), each with substantive commentary (>2 sentences); listed as a member of 2 professional groups; no organizer/leadership role stated."* Every specific claim inside that description must trace to something the collector or annotator could point to on the profile — no aggregate claim without an enumerable basis.
- An `unavailable` activity section carries no `evidence_text`, per the existing coherence constraint (§5).

This is an extension of the existing evidence-citation discipline to a pattern-shaped dimension, not a new evidentiary standard.

## 8. Ethics implications and permission status

**Two separate gates apply, and neither is currently confirmed clear:**

1. **General ethics/DPO approval.** `P3_Final_Data_QA_Report.md` (Finding GOV-01) found no documented record — in `DECISION_LOG.md`, `04_Ethics/`, or elsewhere — of real ethics-committee approval or DPO sign-off having been obtained for *any* collection, static or activity-level. This proposal does not resolve that finding; it remains open and blocking, independent of D6 specifically.
2. **The activity-specific gate.** Independent of (1), the draft ethics package already anticipates that activity/post-level data carries "its own, separate ethics consideration beyond static profile content" (`ALCSM_Ethics_LinkedInCollectionProtocol_v0.1-DRAFT.md` §5; mirrored by the `activity_data_collected` flag's own schema comment). That separate justification — the actual DPIA/LIA content explaining and bounding *why* activity-level observation is proportionate and how its risks are mitigated — has not been drafted anywhere found in this repository. The flag mechanism exists; the substantive ethics writing that would justify setting it does not yet exist.

**Conclusion: the approved ethics/collection protocol does not currently permit the proposed observation**, because no approved protocol has been confirmed to exist at all (gate 1), and even the *draft* protocol treats activity-level observation as requiring a justification that has not yet been written (gate 2). Both gates must clear — and gate 2's justification must be drafted, reviewed, and incorporated into the DPIA/LIA — before any supplementary D6 evidence collection begins.

## 9. Operational clarification or methodological change?

**This proposal is an operational clarification of the frozen D6 dimension, with one parameter left open for author sign-off — it is not a conceptual or methodological change.** Reasoning:

- No dimension definition, rubric criterion, taxonomy tier, or missing-data state is added, removed, or redefined — §§2–3, 5, and 7 apply existing frozen concepts (the rubric's own vocabulary, the four-state missing-data framework, precedents P-12 and P-13, the standard evidence-citation rule) to a case — activity observation — that the frozen documents named but had not yet operationally specified.
- No schema element is added — §6 shows every needed field already exists, pre-dating this proposal.
- The one substantive open decision — the numeric observation-window value in §4 — is a **pre-registration parameter**, of the same kind and same standing as the title list or language scope already flagged for author sign-off elsewhere in this project's governance record. Fixing a parameter the frozen schema already reserved a field for is not the same act as changing what the field, or the dimension, means.

Because this is assessed as an operational clarification (not a conceptual change), a `DECISION_LOG.md` entry is appended per instruction (§10) — recording that this proposal was drafted and its status, not that the open window value has been finalized.

## 10. Decision Log Entry

The corresponding entry, **D-0035**, has been appended to `DECISION_LOG.md` §7 (append-only, no historical entry altered). See that file for the full entry; it records this proposal's existence and status, not a finalized observation-window value or an authorization to collect.

---

## Summary

- **Proposed D6 rule:** observe only publicly visible LinkedIn activity-feed content (original posts, reshares, visible reactions/comments, stated community roles, engagement-framed continuing-education signals) within a fixed, author-confirmed window (proposed default: 12 months preceding `collection_ts`); record an available-but-empty feed as `present`/score 0 (an observed finding) and a non-viewable feed as `unavailable`/score 0 (a data gap) — never conflate the two; never substitute reach/follower metrics, inferred engagement, or non-LinkedIn content for direct observation.
- **Affected fields:** none new. `profile.activity_data_collected`, `profile.observation_window_days`, `profile_raw_section` (`section_name='activity'`, `section_text`, `section_available`), and, later at annotation, the standard `alcsm_dimension_score` fields — all pre-existing, frozen fields, applied as designed.
- **Ethics implications:** two gates, neither confirmed clear — (1) general ethics/DPO approval status is undocumented anywhere in this repository; (2) the draft protocol's own activity-specific justification requirement has not yet been drafted. Both must close before execution.
- **Author approval required:** **Yes** — to confirm this proposal is accepted as an operational clarification (not a methodological change, consistent with §9's reasoning), and specifically to fix the observation-window value in §4. No supplementary evidence collection may begin without that sign-off, independent of and in addition to the ethics gates in §8.
- **Readiness for supplementary evidence collection: NOT READY.** Blocked on (a) author sign-off on this proposal and the window value, and (b) both ethics gates in §8 clearing. This proposal makes collection *specifiable*; it does not make it *permitted*.

---

*This document is a decision proposal. It modifies no ALCSM methodology, no database schema, no raw data, and (until the author acts on §10) no governance record beyond the single append-only entry it introduces.*
