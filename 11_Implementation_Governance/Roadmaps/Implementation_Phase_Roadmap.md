# Implementation Phase Roadmap
### The Authoritative P0–P8 Roadmap for ALCSM Software Implementation

**Document status:** governance document — authoritative for phase sequencing, scope boundaries, and completion criteria from this point forward. It formalizes what already exists across `PROJECT_CONTEXT.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `Task5_Implementation_Readiness_Checklist.md`, and `Task5_Implementation_Plan.md`. It does not redefine methodology, does not alter the database schema, and does not invent, merge, or split any phase.
**Created:** 2026-07-30, during a governance-review session (no software, schema, or methodology changes made). Supersedes no prior document — it consolidates and reconciles their phase-numbering for future reference. Where it clarifies an ambiguity found across those documents, this is noted explicitly (§9); the source documents themselves were not edited.
**Companion documents:** `PROJECT_CONTEXT.md` §38–40 (roadmap, frozen boundaries), `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14–17, `Task5_Implementation_Readiness_Checklist.md` (what is ready now), `Task5_Implementation_Plan.md` (the M0–M8 governance-milestone breakdown underneath P2), `CLAUDE_CODE_RULES.md` (the eight hard rules), `P1_Completion_Summary.md` (P1's own closure record).

---

## 1. Overview

This repository implements the software side of an MSc thesis (*The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*) whose research design — the ALCSM six-dimension scoring model and the PostgreSQL schema (v1.0.1) — is finished and frozen. The remaining work is building the *software* that operates that frozen design: collection tooling, an annotation interface, reliability computation, an NLP pipeline, analysis, and a screening app.

**Two roadmaps exist in this project, at two different levels of granularity, and this document is explicit about how they relate:**

- **P0–P8** (this document, `PROJECT_CONTEXT.md` §38, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14) are **software-engineering phases**, each producing a piece of the codebase under `src/alcsm/`, tested and committed to this repository.
- **M0–M8** (`Task5_Implementation_Plan.md`) is a **project-management/governance milestone breakdown that sits underneath and around P2 specifically** — it is the detailed institutional-approval and pre-collection-readiness plan (ethics package, DPO review, DMP, secure-store provisioning, protocol pre-registration, pilot, reliability check, sign-off gate). M0–M8 does not replace P2–P6; it is the operational detail of *how* P2 is executed and *what exactly* gates the transition into P3/P4's real-data work.

A rough correspondence (not a strict 1:1 mapping — M-milestones are finer-grained and some span parts of two P-phases):

| P-phase | Corresponding M-milestone(s) |
|---|---|
| P0 | M4 (environment/schema — but M4 targets the **production secure store**; P0 targets the **local dev database**. Same schema file, different host — see §9, finding F-3.) |
| P1 | (no direct M-equivalent — M-plan starts from governance; P1 is pure software tooling) |
| P2 | M0 (governance package drafting) + M1 (institutional approval) + M2 (DMP/secure infrastructure) + M3 (protocol pre-registration) |
| P3 | M6 (job postings + taxonomy anchoring) |
| P4 | M5 (annotation system + rater readiness) + the pilot-coding portion of M7 |
| P5 | the reliability-computation portion of M7, plus the M8 sign-off gate |
| P6 | "COLLECT" — the main collection that M8's gate releases |
| P7, P8 | not covered by the M-plan (which is scoped to pre-collection readiness only) |

---

## 2. Timeline

Only P0 and P1 have actually executed, so only they have real dates. Later phases' durations are governed by institutional turnaround (P2) and by data-dependent effort (P3–P8) that neither source document estimates in wall-clock terms beyond the M0–M8 breakdown for the pre-collection portion. This document does not invent estimates the source material doesn't provide.

| Phase | Status | Date / estimate | Source |
|---|---|---|---|
| P0 | ✅ Complete | committed, tagged `p0-complete` | this repo's git history |
| P1 | ✅ Complete | committed, tagged `p1-complete` | this repo's git history |
| P2 | Not started | Effort ~1 week (M0) + **3–8 weeks elapsed, institution-controlled** (M1) + 1–2 weeks (M2, parallel) + ~1 week (M3, parallel) | `Task5_Implementation_Plan.md` M0–M3 |
| P3 | Blocked on P2 | Effort 4–6 days; elapsed 1–2 weeks | `Task5_Implementation_Plan.md` M6 |
| P4 | Interface build: unblocked now (fixtures only). Pilot coding: blocked on P2+P3 | Effort 4–7 days (interface) + 3–5 days/round (pilot); elapsed 1–2 weeks each | `Task5_Implementation_Plan.md` M5, M7 |
| P5 | Blocked on P4 | Bundled into M7's elapsed estimate above | `Task5_Implementation_Plan.md` M7 |
| P6 | Blocked on P5 gate | Not estimated in source documents | — |
| P7 | Blocked on P6 | Not estimated in source documents | — |
| P8 | Blocked on P6 + P7 | Not estimated in source documents | — |

**Realistic total elapsed for the pre-collection portion (P0 through the M8 gate immediately before P6):** roughly 7–12 weeks per `Task5_Implementation_Plan.md`'s consolidated schedule, dominated by the P2/M1 institutional review, not by engineering effort.

---

## 3. Phase descriptions (P0–P8)

Each phase below gives the nine fields requested: name, purpose, objectives, allowed implementation work, explicitly out-of-scope items, expected deliverables, dependencies, completion criteria, and the git tag expected on completion.

### P0 — Environment

- **Purpose.** Stand up a working, versioned software repository and a local development database from the frozen schema, so implementation can proceed on tested foundations.
- **Objectives.** Initialise the repo layout; configure tooling (`pyproject.toml`, `.gitignore`); deploy `alcsm_schema_v1.0.1.sql` to a local/dev PostgreSQL instance; run the 67-test validation harness; load the DDL-seeded reference data (6 dimensions, 4 missing-status values); tag the frozen baseline.
- **Allowed implementation work.** `src/alcsm/` package scaffolding (`config.py`, logging, constants, `db/engine.py`, `db/models.py`, `db/queries.py`); `tests/` mirroring that structure; module *skeletons* (with clear TODOs, no real logic) for `reliability/`, `taxonomy/`, `nlp/`, `analysis/`, `app/`; deploying the DDL as-is to a dev/throwaway database; running the validation harness and gap probes; tagging frozen states.
- **Explicitly out of scope.** Any schema modification; any scoring/business logic; any NLP implementation; any Streamlit page; any real personal data; placeholder implementations that could conflict with frozen methodology.
- **Expected deliverables.** Running repository; DDL deployed to a dev database; harness green (67/67 tests); `README.md`; 6-dimension and 4-missing-status reference data loaded; frozen-state tags.
- **Dependencies.** None — first phase.
- **Completion criteria.** Fresh install loads with zero errors; validation harness reports its expected clean baseline; repository excludes all personal data and secrets (verified by inspection).
- **Git tag.** `p0-complete` — **already applied.**

---

### P1 — Collection tooling

- **Purpose.** Build and prove the software that will eventually record real profiles, entirely against constructed fixtures, so the write path is validated before any real data touches it.
- **Objectives.** Port and test `collection/helper.py` against constructed fixtures; verify the backup script.
- **Allowed implementation work.** Refactoring the prototype helper into `src/alcsm/collection/` as a production module (types, dataclasses, logging, config-driven connection, proper exceptions); pytest coverage using constructed fixtures only; backup/restore script verification using non-personal, throwaway data only.
- **Explicitly out of scope.** Any real profile collection; any browser automation or scraping; any schema change; a second (ORM-based) write path — `collection/helper.py` (psycopg2) remains the single authoritative insertion path.
- **Expected deliverables.** Tested collection helper; verified backup/restore round-trip against the current v1.0.1 schema.
- **Dependencies.** P0.
- **Completion criteria.** Collection helper ported and tested (spec-based assertions, no real data); backup script verified end-to-end against the live schema.
- **Git tag.** `p1-complete` — **already applied.**

---

### P2 — Governance (ethics / GDPR / DPIA approval)

- **Purpose.** Obtain the institutional authorisation required before any real personal data may be collected. This is the single hard gate for the rest of the project — every later phase either directly or transitively depends on it.
- **Objectives.** Draft the governance package (ethics application, GDPR Legitimate Interests Assessment, DPIA screening/DPIA, public privacy notice, collection-method proposal, survey consent materials); submit for institutional review; obtain ethics approval, DPO sign-off, and a documented Article 14 position; finalise the Data Management Plan; provision the EEA-resident, access-controlled secure store; pre-register the sampling and collection protocol.
- **Allowed implementation work.** None in the software-engineering sense — this phase is document drafting and institutional liaison, not code. Non-personal-data software scaffolding of later-phase modules (`reliability/`, `taxonomy/`, `nlp/`, `analysis/`, `app/`) **may continue in parallel** using constructed fixtures (this is explicitly sanctioned — see §7) but that work belongs to its own later phase number, not to P2.
- **Explicitly out of scope.** Any real data collection of any kind; any scraping or browser automation; any code change made in anticipation of an approval outcome not yet granted; any change to frozen methodology or schema to work around a governance concern.
- **Expected deliverables.** Ethics approval with a reference number, recorded in `docs/ethics/`; DPO sign-off (or written confirmation no DPIA is required); documented Article 14 position and legal basis; approved collection method on record; completed DMP; provisioned and verified secure store; pre-registered sampling/collection protocol.
- **Dependencies.** P1 (tooling must exist so the approved method points at real, tested software); externally, institutional committee and DPO calendar.
- **Completion criteria.** Written ethics approval on file; no open committee conditions (or all logged with a plan to satisfy them); DMP approved; secure store live, access-restricted, EEA-resident, backup/restore verified; approved scope matches what P3/P4/P6 actually intend to do.
- **Git tag.** `p2-complete` — marks the point where the (non-personal-data) governance artefacts — approval references, DMP, protocol — are committed to the repository and the gate formally clears. No application code is produced in this phase.

---

### P3 — Job postings and taxonomy anchoring

- **Purpose.** Build the *required*-side corpus (job postings) and use its vocabulary to anchor the eight frozen taxonomies' term lists — the prerequisite for reproducible scoring on either corpus.
- **Objectives.** Collect ~200 job postings per the pre-registered protocol; seed taxonomy term lists from posting vocabulary; stamp and freeze `taxonomy_version`; enable the deferred F-06 constraint.
- **Allowed implementation work.** `taxonomy/anchoring.py` implementation; job-posting collection tooling (manual, human-driven, never scraped or automated); recruiter-privacy enforcement (no individual recruiter personal data recorded).
- **Explicitly out of scope.** Scoring any profile; editing a taxonomy version after it is stamped and frozen; automated/scraped collection of postings; inventing taxonomy terms not evidenced in posting text.
- **Expected deliverables.** ~200 postings with verbatim `raw_posting_text` and full provenance; taxonomy versions stamped and frozen with terms, frequencies, and date documented; F-06 enabled.
- **Dependencies.** P2 (ethics approval for collection).
- **Completion criteria.** Postings captured with full provenance; anchoring documented; no recruiter personal data recorded; frozen taxonomy versions in place before any scoring begins.
- **Git tag.** `p3-complete`.

---

### P4 — Annotation interface and pilot coding

- **Purpose.** Build the human-annotation tool that enforces the four frozen constraints, and use it to run the reliability pilot that determines whether the rulebook is ready for full-scale coding.
- **Objectives.** Build the annotation interface honouring all four frozen constraints; onboard both raters; run pilot coding on 10–20 purposively selected real profiles.
- **Allowed implementation work — no further gate needed.** Building the interface itself and running a fixture-based dry run (constructed, non-personal profiles) to prove all four constraints hold. This is explicitly documented in `Task5_Implementation_Plan.md` (Milestone 5: *"The interface build and dry-run need no real data and can proceed during the M1 [ethics] wait"*) and matches the general principle that non-personal-data software work may proceed in parallel with P2.
- **Allowed only after P2 and P3 both clear.** Pilot coding on real profiles; rater onboarding using real material; reliability computation on pilot data (this portion is P5, see below).
- **Explicitly out of scope.** Displaying RQ4 impact values during scoring; letting either rater see the other's score before both submit; any pilot coding on real profiles before P2 and P3 both clear; changing frozen scoring criteria in response to a low pilot result (only rulebook *wording* may be revised, and only via the revision-log procedure).
- **Expected deliverables.** Annotation interface passing a four-constraint checklist test (including a deliberate, blocked attempt to view another rater's score); completed rater onboarding; a pre-registered double-coding subset (or an explicit 100%-double-coding decision) with method and seed recorded; pilot coding completed on the selected profiles.
- **Dependencies.** Interface build: none (fixtures only). Pilot coding: P2, P3.
- **Completion criteria.** Interface passes all four constraint tests; raters trained and able to articulate the missing-status and D4-verification rules; double-coding subset fixed and pre-registered before any pilot coding begins.
- **Git tag.** `p4-complete`.

---

### P5 — Reliability

- **Purpose.** Formally establish, per dimension, whether human coding is reliable enough to scale from the P4 pilot to the full ~500-profile collection.
- **Objectives.** Compute per-dimension Krippendorff's α with bootstrap confidence intervals, raw percentage agreement, `n_units`, and variance from the P4 pilot data; store results in `reliability_result`; apply the frozen decision rule.
- **Allowed implementation work.** `reliability/krippendorff.py` implementation, reading exclusively through `v_reliability_input` (pre-adjudication, independent rows only).
- **Explicitly out of scope.** Cronbach's alpha in any form, across dimensions (wrong statistic for a formative index — this is a frozen methodological boundary, not a style choice); computing reliability on adjudicated rows; pooling dimensions; changing frozen scoring *criteria* if a dimension underperforms (only rulebook *wording* may be revised, via the revision log, with a mandatory re-pilot).
- **Expected deliverables.** `reliability_result` populated with full per-dimension diagnostics; the pre-stated expectation that D5/D6 will show lower reliability recorded *before* results are seen; any rulebook-wording revisions logged.
- **Dependencies.** P4 (pilot data).
- **Completion criteria.** Every dimension meets the frozen decision rule (α ≥ .80 proceed; .667–.80 acceptable with review; < .667 revise rulebook wording and re-pilot); results stored with full diagnostics; no frozen criterion altered.
- **Git tag.** `p5-complete`.

---

### P6 — Main collection and coding

- **Purpose.** Execute the full-scale data collection (~500 profiles) and human coding that produces the project's gold standard.
- **Objectives.** Collect ~500 profiles per the pre-registered protocol; code them under the double-coding policy (100% if feasible, otherwise a pre-registered random subset of at least 15%); sustain the reliability level demonstrated in P5.
- **Allowed implementation work.** Operational use of the tools already built in P1 (collection helper) and P4 (annotation interface) — this phase is data collection and coding, not new tool-building.
- **Explicitly out of scope.** Building new collection or annotation tooling (already built); deviating from the pre-registered sampling frame; treating a mid-collection reliability dip as licence to change frozen criteria (escalate to the author instead).
- **Expected deliverables.** ~500 profiles collected and coded; `v_final_profile_score` populated (the gold standard); a sustained-reliability report covering the full run, not just the pilot.
- **Dependencies.** The P5/M8 readiness gate — all governance blockers cleared, pilot criteria met, supervisor sign-off obtained.
- **Completion criteria.** ~500 profiles collected and coded per protocol; reliability sustained at the required threshold across the full run; gold standard available via `v_final_profile_score`.
- **Git tag.** `p6-complete`.

---

### P7 — NLP pipeline

- **Purpose.** Build and evaluate the automated scoring pipeline (RQ5) against the human gold standard produced in P6.
- **Objectives.** Implement extract → classify → evaluate, per dimension, using only local or explicitly approved models; evaluate against the gold standard via `v_nlp_evaluation`.
- **Allowed implementation work.** `nlp/extract.py`, `nlp/classify.py`, `nlp/evaluate.py` — spaCy, sentence-transformers, and locally-run HuggingFace models only, on approved infrastructure.
- **Explicitly out of scope.** Any external-API processing of profile text (a hard GDPR-tied constraint, never a convenience trade-off); using information a human coder could not see; training before both the gold standard (P6) and anchored taxonomies (P3) exist.
- **Expected deliverables.** A working NLP pipeline operating on the same information base as the human coders; per-dimension `v_nlp_evaluation` results, reported honestly including where the model fails; fixed `random_seed` and recorded `code_commit_hash` on every `nlp_model_run`.
- **Dependencies.** P6 (the gold standard must exist first); P3 (anchored taxonomies).
- **Completion criteria.** Pipeline runs end-to-end; per-dimension evaluation results are stored and reported, including failure cases.
- **Git tag.** `p7-complete`.

---

### P8 — Analysis and screening app

- **Purpose.** Answer the thesis's research questions from the completed data (RQ1 patterns, RQ2 credential gap, RQ4 correlation) and deliver the RQ5 demonstration tool.
- **Objectives.** Implement the credential-gap analysis (RQ2), the RQ4 correlation analysis, descriptive RQ1 pattern analysis, and the Streamlit dimension-level screening tool.
- **Allowed implementation work.** `analysis/gap.py`, `analysis/rq4.py`, and descriptive analysis reading exclusively through the frozen views (`v_credential_gap_by_dimension`, etc.), using ordinal-appropriate statistics throughout; `app/streamlit_app.py` showing the six ALCSM dimension scores, missingness, completeness index, evidence summaries, and validation indicators.
- **Explicitly out of scope.** Any composite/aggregate ALCSM score presented as authoritative — aggregation remains exploratory-only, clearly labelled if shown at all, never a single hard-coded number; using an ALCSM dimension as an RQ4 predictor (circularity); displaying RQ4 values as if they were part of ALCSM.
- **Expected deliverables.** Credential-gap analysis (RQ2); RQ4 correlation results; RQ1 descriptive patterns; a working Streamlit screening tool.
- **Dependencies.** P6 (gold standard) and P7 (NLP predictions) — both are needed before the app or the full analysis suite is meaningful.
- **Completion criteria.** All three analyses produced via the frozen views; the Streamlit tool passes a manual walkthrough showing six scores, missingness, completeness, evidence, and flags, with no single composite score displayed by default.
- **Git tag.** `p8-complete`.

**Note on this phase's numbering:** `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14/§17 and `PROJECT_STRUCTURE.md` describe the Streamlit app as a separate **P9**, distinct from a narrower P8 ("Analysis" only). This document follows the phase count given in this session's own instructions ("every phase from P0 through P8") and in `PROJECT_CONTEXT.md` §38's roadmap table, which bundles the app into P8. This is a deliberate, transparent reconciliation of a real cross-document inconsistency, not a silent decision — see §9, finding F-1, for the full analysis and a recommended documentation fix.

---

## 4. Exit criteria (cross-phase)

No phase is "done" until:

1. Its **completion criteria** above are met and evidenced (test results, stored diagnostics, approval references, etc. — not a verbal assertion).
2. `black`, `ruff`, `mypy`, and `pytest` are clean for any code the phase touched (where the phase produces code at all).
3. Its deliverables are committed, and the phase's git tag (§5) is applied.
4. Nothing in the phase violated a frozen boundary (§7) or introduced a second write path, a schema change, or a composite score.
5. For any phase touching real data (P3, P4's pilot, P6): the relevant governance gate (P2, and for P6 specifically the full P5/M8 readiness gate) has actually cleared — not "is expected to clear soon."

---

## 5. Git tagging strategy

This repository already uses the convention `p{N}-complete`, applied to exactly one commit per completed phase:

| Tag | Status |
|---|---|
| `p0-complete` | ✅ applied |
| `p1-complete` | ✅ applied |
| `p2-complete` | to be applied when P2's governance artefacts are committed and the gate clears |
| `p3-complete` … `p8-complete` | to be applied in the same pattern, one per phase, in order |

Rules for this convention going forward:
- One tag per phase, applied only once that phase's exit criteria (§4) are all met.
- Never re-tag or move a tag after the fact — if a phase needed rework after tagging, that rework ships as a new commit under the *next* phase's work, with a note explaining what was revisited.
- Tags mark **software and non-personal governance artefacts only**. No tag, commit, or piece of git history may include real personal data at any point — this is independent of and in addition to `.gitignore` excluding `data/`.

---

## 6. Never skip a phase

The phase order is not a suggestion; it encodes real dependencies that produce silent corruption if skipped:

- **P3 before any scoring.** Taxonomies must be anchored and frozen before P4 pilot coding begins — scoring against a term list that later changes breaks reproducibility.
- **P4 and P5 before P6.** The pilot and its reliability check exist specifically to catch a broken rulebook *before* it is applied to 500 profiles at cost. Skipping to P6 risks discovering a systemic coding problem only after the main collection is done.
- **P6 before P7.** The NLP pipeline is evaluated *against* the human gold standard; there is nothing to evaluate against until P6 produces `v_final_profile_score`.
- **P6 and P7 before P8.** The analysis and app both need real, completed data and real predictions — building them earlier only produces a UI/analysis shell with nothing to show, and risks silently hard-coding assumptions about data shape that turn out wrong.
- **P2 before P3, P4's pilot, and P6, always.** This is the one gate with zero exceptions: *"no real profile data before P2; no scoring before taxonomies are anchored (P3); no NLP training before a gold standard exists (P6)"* (`PROJECT_CONTEXT.md` §38, verbatim). Software scaffolding of later phases against constructed fixtures is the only work permitted to run ahead of P2.

If a later phase's work seems to require starting before an earlier phase's gate has cleared, that is a signal to stop and ask the author — not a scheduling inconvenience to route around.

---

## 7. Notes on ethics gates

- **P2 is the only phase with a hard external dependency** (institutional committee and DPO calendar) rather than an internal engineering dependency. Its elapsed time (3–8 weeks per `Task5_Implementation_Plan.md` M1) dominates the whole project schedule and is not compressible by working harder.
- **Non-personal-data work may run in parallel with the P2 wait.** This is explicit and deliberate, not a loophole: `PROJECT_CONTEXT.md` §38 states plainly that "non-personal-data work (P0, P1, and scaffolding of later modules with fixtures) may proceed at any time, including in parallel with the P2 approval wait." Use this window — it is the only way to avoid the institutional clock being pure idle time.
- **What may proceed during the P2 wait:** module scaffolding for `reliability/`, `taxonomy/`, `nlp/`, `analysis/`, `app/` against constructed fixtures; the P4 annotation interface build and its fixture-based dry run; DMP drafting and secure-store provisioning (P2's own M2); protocol pre-registration (P2's own M3).
- **What must never proceed before P2 clears:** any collection of real LinkedIn profiles or job postings; any scoring of real data; any use of real personal data in a test, log, or commit, under any circumstance.
- **A cleared P2 does not retroactively bless out-of-scope work done during the wait.** If real data were ever touched before P2 formally cleared, that is a compliance incident to escalate immediately, not a timing technicality.

---

## 8. Frozen methodology reminders

These do not change across any phase, and no phase's implementation work may alter them (`CLAUDE_CODE_RULES.md`, `PROJECT_CONTEXT.md` §40–43):

1. The six dimensions, their definitions, and their 0–5 criteria are frozen.
2. ALCSM is a **formative composite index** — the six dimensions need not correlate, and **Cronbach's alpha across dimensions must never be computed or reported**. Krippendorff's alpha per dimension is the correct (and required) reliability statistic.
3. The verifiability gradient (D1/D2/D4 high, D3/D5/D6 low) is reported per dimension, never pooled.
4. Signal-not-competence terminology is used everywhere in code, UI, and analysis.
5. The coding rulebook, the fifteen precedents (P-01…P-15), and the four missing-data states (`present`, `absent_stated`, `unavailable`, `not_applicable`) are frozen.
6. The eight taxonomies' *structure* is frozen; only term-list *content* is anchored (P3), never invented.
7. External verification is permitted for **D4 only**, and only to confirm or lower a score, never to raise it beyond what the text supports.
8. The database schema is frozen at v1.0.1: 22 tables, 5 views, 33 `ON DELETE RESTRICT` foreign keys, 66 CHECK constraints. No composite/total/weight/band column may ever be added — aggregation is deliberately open.
9. SQLAlchemy is an application layer only; it never defines, creates, alters, or migrates schema. The psycopg2-based collection helper is the single authoritative write path.

If any phase's work appears to require changing one of these, that is a stop-and-ask, not an implementation choice.

---

## 9. Known documentation inconsistencies (flagged, not silently resolved)

Found during this governance review. None of these were edited in the source documents — they are reported here per this session's explicit instruction, with a recommended minimal fix for the author to apply (or decline) at their discretion.

### F-1 — P8/P9 phase-count disagreement (the most significant finding)

- **Which documents disagree:** `PROJECT_CONTEXT.md` §38 titles its table "Phase-by-Phase Implementation Roadmap (**P0–P8**)" and bundles the Streamlit app into P8 ("Analysis + app"). `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14 and §17 both list a separate **P9** ("Streamlit app") after an P8 that covers analysis *only*. `PROJECT_STRUCTURE.md` independently says "its own phase roadmap (**P0–P9**)," agreeing with the Implementation Guide, not with `PROJECT_CONTEXT.md`.
- **Why:** apparent drift between the two primary technical documents — `PROJECT_CONTEXT.md` reads as a slightly earlier/looser summary; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` gives the app its own numbered milestone with its own dependency line.
- **Which version should become authoritative:** on balance, treating the app as its own **P9** (the Implementation Guide's framing) is better supported: (a) the Implementation Guide's own header claims its architectural decisions are "final and author-approved," a stronger status than `PROJECT_CONTEXT.md`'s self-description as a "living engineering reference"; (b) `PROJECT_STRUCTURE.md` independently agrees with it; (c) the P0-produced code skeletons already cite this split (`analysis/gap.py`'s docstring says "Implemented in Phase P8"; `app/streamlit_app.py`'s says "Implemented in Phase P9"), so treating P8-only-analysis/P9-app as authoritative avoids contradicting code comments already shipped in `p0-complete`.
- **However:** this session's own instructions (Task 1 and Task 2) explicitly enumerate the roadmap as "P0 through P8," matching `PROJECT_CONTEXT.md`'s 9-phase framing. §3 of this document follows that explicit instruction and folds the app into P8, while flagging this note so the discrepancy is not silently buried. **This is a decision the author should confirm** — if P0–P9 (ten phases) was intended, only §3's final "P8" section needs renaming to "P9" with a preceding pure-analysis P8; nothing else in this document changes.
- **Minimal edit to resolve, if P0–P9 is preferred:** in `PROJECT_CONTEXT.md` §38, split the current P8 row into two rows (P8 = analysis only; P9 = Streamlit app, dependency P7) and retitle the section "(P0–P9)". No other document needs to change.

### F-2 — P4 conflates a software-engineering task with a real-data research task

- **Which documents disagree:** `PROJECT_CONTEXT.md` §38 and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14 both list P4 as a single row ("Annotation interface (four constraints) + pilot coding") with one dependency ("P2, P3") and "touches real data: Yes" — implying the entire phase, including *building the interface*, waits on ethics approval. `Task5_Implementation_Plan.md` Milestone 5 explicitly splits this: *"The interface build and dry-run need no real data and can proceed during the M1 wait"* — only the pilot itself (M7) needs approval.
- **Why:** the summary tables in the two primary roadmap documents operate at phase-level granularity and don't carry the milestone-level nuance that `Task5_Implementation_Plan.md` documents.
- **Which version should become authoritative:** `Task5_Implementation_Plan.md`'s split is more consistent with the project's own stated principle (`PROJECT_CONTEXT.md` §38's own footnote) that non-personal-data scaffolding may proceed in parallel with the P2 wait, and it is the more specific, later, more detailed document.
- **Minimal edit to resolve:** in `PROJECT_CONTEXT.md` §38 and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §14, add a footnote to the P4 row distinguishing "interface build + fixture dry-run: no dependency" from "pilot coding: depends on P2, P3" — this document's §3 (P4) already carries that distinction forward as the working definition.

### F-3 — "P0" (this repo's dev environment) and "M4" (the production secure store) are not the same deployment target, though both are described with similar language

- **Which documents disagree:** no document states this incorrectly, but none states the distinction explicitly either. `PROJECT_CONTEXT.md` §38 describes P0 as "deploy schema to dev PostgreSQL" (confirmed in practice: this repository's `p0-complete`/`p1-complete` work targets a local database, `alcsm_dev`, on the author's own machine). `Task5_Implementation_Plan.md` Milestone 4 describes deploying "into the secure store" — the approved, EEA-resident, access-controlled production environment, which does not yet exist in this repository's history.
- **Why:** both use the phrase "deploy the schema" for what are, in fact, two separate deployments (dev, and later production) of the same DDL file to two different hosts.
- **Recommendation:** no document is wrong; this document's §1 table makes the distinction explicit going forward so "P0 is done" is never misread as "the production secure-store deployment is done."

### Verified consistent (checked, not flagged)

- Phase **ordering** (P0→P1→…→P8) is presented identically and without reordering across every document.
- Phase **names** for P0, P1, P2, P3, P5, P6, P7 match exactly across `PROJECT_CONTEXT.md` and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`.
- No phase is **duplicated** under two different numbers.
- **P2 is never given a software deliverable** anywhere — `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §17's deliverables table correctly omits it, treating it as the non-code governance phase it is.
- **Taxonomy structure vs. content** (methodology vs. engineering) is consistently and correctly distinguished everywhere it appears (P3's scope is anchoring *content* to already-frozen *structure*).
- `Task5_Implementation_Readiness_Checklist.md`'s inline phase references (P0, P1, P3, P4, P6) agree with `PROJECT_CONTEXT.md`/`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` wherever it cites a phase number explicitly; it does not discuss P7/P8/P9 at all, which reads as an intentional scope limit (it documents only what is ready or near-ready), not a contradiction.

---

## 10. Scope boundaries (standing, all phases)

Restated from `CLAUDE_CODE_RULES.md` for a governance reader — these apply regardless of which phase is active:

1. Never modify frozen ALCSM methodology.
2. Never change the database schema without author approval.
3. Treat `alcsm_schema_v1.0.1.sql` as the sole schema authority; SQLAlchemy never defines or migrates it.
4. Ask before any architectural change (new write path, new external dependency, migration tool, external processing step).
5. Maintain reproducibility (version stamps, fixed seeds, commit hashes, `v_reliability_input`-only reliability reads).
6. Every module ships with spec-based tests using non-personal fixtures.
7. Keep documentation synchronised; edit only canonical files; never edit an archived file.
8. Never send profile data to an external API, commit personal data, or collect real data before ethics approval.

If a task in any phase appears to require crossing one of these, stop and ask the author — it is a version decision, never an implementation choice.
