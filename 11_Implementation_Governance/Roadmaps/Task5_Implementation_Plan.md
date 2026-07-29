# Task 5 — Implementation Plan
### Milestone Breakdown for Pre-Collection Readiness

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Scope:** execution plan for the Task 5 roadmap. ALCSM v1.0 and Schema v1.0.1 are frozen; this plan **contains no database modifications** (Milestone 4 deploys from the frozen schema file, it does not alter it).

**How to read the durations.** Each milestone gives two figures: **effort** (your active working time) and **elapsed** (calendar time including waiting). For governance milestones these diverge sharply, because the schedule is dominated by *institutional turnaround you do not control* — ethics committee cycles and DPO review. Treating a two-week committee wait as "two weeks of work" is the most common planning error in thesis projects; this plan separates the two so you can parallelise around the waits. All figures are indicative and must be calibrated to SRH's actual review calendar. **[INSTITUTIONAL]**

**Marker convention (carried from the roadmap):** **[BLOCKER]** gates real data collection; **[INSTITUTIONAL]** needs a supervisor / ethics committee / DPO decision.

---

## Critical-path summary

The critical path runs through governance, not through your own labour:

```
M0 draft governance ──► M1 institutional review & approval ──────────────► M8 gate ──► COLLECT
   (your effort)         (committee/DPO calendar time — the bottleneck)      │
                                                                             │
Run in PARALLEL during the M1 wait (no personal data involved):             │
   M2 DMP + infrastructure ─┐                                               │
   M3 protocol pre-registration ─┤                                          │
   M4 environment + schema deploy ─┼──► all feed M8                          │
   M5 annotation interface + raters ─┤                                      │
   (M6/M7 need approval and so sit AFTER M1)                                 │
                                                                             │
Post-approval, pre-gate:                                                     │
   M6 job postings ──► taxonomy anchoring ──► taxonomy_version stamped       │
   M7 pilot annotation ──► per-dimension reliability ──► (revision loop)     │
```

**Planning consequence:** start M0 immediately, submit M1 as early as possible, and load the M1 waiting period with M2–M5 so the approval clock is not idle time. M6 and M7 cannot start until M1 clears, because both touch real collected data.

---

## Milestone 0 — Governance package assembly

**Objective.** Draft, as a single coordinated package, every governance document the institution needs to make a decision: the ethics application, the GDPR Legitimate Interests Assessment (LIA), the DPIA screening (and DPIA itself if indicated), the public privacy notice, and a written collection-method proposal.

**Deliverables.**
- Ethics application in SRH's format, covering the content in roadmap §2.1.
- LIA (purpose / necessity / balancing tests) for the LinkedIn strand.
- DPIA screening note; full DPIA draft if screening indicates one is needed.
- Draft public privacy notice (the Article 14 "make information publicly available" safeguard).
- Collection-method proposal recommending manual, human-driven collection with justification against the ToS exposure.
- Survey participant information sheet and consent form (adapted from roadmap §2.2–2.3).

**Dependencies.** The frozen framework, schema, and roadmap (all complete). No external dependency — this is your own drafting work and can start now.

**Estimated duration.** Effort **5–8 working days**; elapsed **1–2 weeks** (allowing for a supervisor pre-review before formal submission).

**Risks.**
- *Underestimating the DPIA.* If a DPIA is required (likely, per roadmap §3.7) and you discover this late, it adds weeks. *Mitigation:* treat the DPIA as required until the DPO says otherwise; draft the screening first.
- *Article 14 position left vague.* A committee will push back on "we'll rely on the research exemption" with no reasoning. *Mitigation:* write the reasoning and the public-notice safeguard into the package now.
- *Collection method left open.* Submitting without a method decision invites a conditional approval and a second review cycle. *Mitigation:* commit to a recommended method in the package.

**Acceptance criteria.**
- Every document in the package drafted and internally consistent (the legal basis in the ethics app matches the LIA matches the privacy notice).
- Supervisor has pre-reviewed and endorsed the package for formal submission.
- The collection-method recommendation is explicit and justified.

---

## Milestone 1 — Institutional review and approval  **[BLOCKER] [INSTITUTIONAL]**

**Objective.** Obtain written ethics approval and DPO clearance, including a documented resolution of the Article 14 notification question and the DPIA.

**Deliverables.**
- Ethics approval with a reference number.
- DPO sign-off (or written confirmation that no DPIA is required).
- Documented, DPO-endorsed Article 14 position and legal basis.
- Approved collection method on record.

**Dependencies.** M0 complete and supervisor-endorsed.

**Estimated duration.** Effort **1–3 days** (responding to reviewer queries); elapsed **3–8 weeks** — committee cadence and revision rounds dominate and are outside your control. **This is the critical-path bottleneck.**

**Risks.**
- *Committee revision rounds.* Most applications return with required changes; each round adds a full cycle. *Mitigation:* over-prepare M0; ask your supervisor which reviewers are strict and pre-empt their likely objections.
- *Calendar collision.* Committees may not sit over holidays/exam periods. *Mitigation:* check the review calendar before submitting and target an early slot.
- *Method rejection.* The committee or DPO may reject automated collection outright. *Mitigation:* the recommended manual method reduces this risk to near zero.

**Acceptance criteria.**
- Approval reference recorded in `docs/ethics/`.
- No open conditions remain, or all conditions are explicitly logged with a plan to satisfy them before M8.
- The approved scope matches what the protocols in M3/M6/M7 will actually do (no drift between what was approved and what you build).

---

## Milestone 2 — Data Management Plan and secure infrastructure

**Objective.** Finalise the DMP and stand up the EEA-resident, access-controlled secure store where all personal data will live. Resolve the re-identification-mapping decision.

**Deliverables.**
- Completed DMP (roadmap §4 structure), including concrete retention and destruction triggers.
- Provisioned secure store (university-approved), with access limited to researcher and supervisor.
- Documented re-identification-mapping decision (§4.1: no mapping / temporary / retained), recorded in DMP and DPIA.
- Tested encrypted backup and restore.

**Dependencies.** Storage provisioning may need IT/institutional action (**[INSTITUTIONAL]**); the mapping decision should align with the M1 DPIA. Can largely proceed *during* the M1 wait.

**Estimated duration.** Effort **2–4 days**; elapsed **1–2 weeks** if IT provisioning is involved.

**Risks.**
- *Storage outside the EEA.* A convenient cloud default may sit outside the EEA, triggering Chapter V transfer rules. *Mitigation:* confirm EEA residency before provisioning.
- *Mapping scope creep.* A "temporary" mapping that is never destroyed becomes the project's most sensitive artefact. *Mitigation:* set the destruction date now and put it in the DMP.

**Acceptance criteria.**
- DMP approved by supervisor; retention/destruction dates concrete.
- Secure store live, access-restricted, EEA-resident, backup/restore verified.
- Mapping decision documented and consistent across DMP and DPIA.

---

## Milestone 3 — Sampling and collection protocol pre-registration

**Objective.** Fix and pre-register every sampling and collection decision so nothing is adjusted mid-collection.

**Deliverables.**
- Pre-registered sampling frame: target population statement, qualifying AI-leadership title list, inclusion/exclusion criteria.
- Pre-registered query strings, platform surface, filters, and per-query quotas.
- Fixed language/localisation scope and collection window.
- Fixed activity observation window (for the RQ4 engagement indicator).
- Selection-bias disclosure paragraph drafted for the Methods chapter.

**Dependencies.** Should be consistent with the approved ethics scope (M1). Drafting can occur during the M1 wait; freeze it once approval confirms scope.

**Estimated duration.** Effort **2–3 days**; elapsed **~1 week**.

**Risks.**
- *Post-hoc criteria drift.* Adjusting inclusion rules after seeing results biases the sample. *Mitigation:* pre-register and date the criteria; log any forced change with justification.
- *Title-list too narrow or too broad.* Skews the frame. *Mitigation:* triangulate the title list against the job-posting titles (M6) where feasible, and state the rationale.

**Acceptance criteria.**
- All sampling parameters written, dated, and frozen before any collection.
- Inclusion/exclusion criteria unambiguous enough that two people would apply them identically.
- Bias disclosures drafted.

---

## Milestone 4 — Operational environment and schema deployment

**Objective.** Stand up the repository and deploy the frozen database, ready to receive data. **No schema modification.**

**Deliverables.**
- Git repository initialised with the roadmap §8 layout; `.gitignore` verified to exclude `data/` and secrets.
- Database deployed from `alcsm_schema_v1.0.1.sql` into the secure store.
- Reference data loaded: 6 dimensions, 4 missing-status values, 15 precedents **with real ruling text**, rater records.
- Frozen framework documents and validation harness committed; frozen states tagged (`framework-v1.0`, `schema-v1.0.1`).
- Task 4 validation harness re-run against the deployed instance to confirm a clean baseline.

**Dependencies.** Secure store from M2. Independent of M1 — can run fully during the approval wait.

**Estimated duration.** Effort **1–2 days**; elapsed **2–3 days**.

**Risks.**
- *Accidental secret/data commit.* A credential or data file committed to Git is a disclosure incident. *Mitigation:* verify `.gitignore` and run a pre-commit secret check before the first push.
- *Placeholder precedent text.* Loading `P-01…P-15` with dummy text breaks annotation traceability. *Mitigation:* load the real rulings from the frozen precedent library.

**Acceptance criteria.**
- Fresh install loads with zero errors; validation harness reports its expected clean baseline.
- Reference tables complete and correct (15 precedents present with genuine text).
- Repository excludes all personal data and secrets, confirmed by inspection.

---

## Milestone 5 — Annotation system and rater readiness

**Objective.** Build or configure the annotation interface to honour the four frozen constraints, and onboard the raters, including pre-registration of the double-coding subset.

**Deliverables.**
- Annotation interface that (a) shows one profile's six dimensions together, (b) never displays RQ4 criterion values during coding, (c) blinds each rater to the other until both submit, (d) captures evidence, missing-status, ambiguity/contradiction flags, precedent, and D4-only verification metadata.
- Rater onboarding completed: both raters trained on the frozen rulebook and precedent library; joint practice coding on **constructed** profiles (no real personal data needed for a workflow dry-run).
- Pre-registered, randomly selected double-coding subset (or a 100% double-coding decision), with method and seed recorded.
- Documented rater identities, expertise, and independence arrangement.

**Dependencies.** Deployed database (M4). The *interface build and dry-run* need no real data and can proceed during the M1 wait; the *methodological pilot* (M7) needs approval.

**Estimated duration.** Effort **4–7 days** (interface + onboarding); elapsed **1–2 weeks**.

**Risks.**
- *Interface leaks criterion values to raters.* Contaminates predictor/criterion independence. *Mitigation:* treat constraint (b) as a hard acceptance test, not a nice-to-have.
- *Non-random double-coding subset.* Reliability then fails to generalise. *Mitigation:* random selection, pre-registered with a seed.
- *Researcher as sole coder.* Expectancy bias, especially on D5/D6. *Mitigation:* pair with a second coder as blind to the hypotheses as feasible; disclose.

**Acceptance criteria.**
- Interface passes a checklist test of all four constraints, including a deliberate attempt to view another rater's score before submission (must be blocked).
- Raters complete practice coding and can articulate the missing-status and verification rules.
- Double-coding subset fixed and pre-registered.

---

## Milestone 6 — Job-posting collection and taxonomy anchoring  **[BLOCKER-gated]**

**Objective.** Collect the ~200 job postings and use their vocabulary to anchor and version the frozen taxonomies' term lists — the prerequisite for scoring either corpus reproducibly.

**Deliverables.**
- ~200 postings collected per the pre-registered protocol, with full `raw_posting_text` retained.
- Taxonomy anchoring performed: term lists seeded from posting vocabulary, frequencies recorded.
- Taxonomy versions stamped (`taxonomy_version`, `frozen = TRUE`), enabling the optional F-06 NOT-NULL constraint thereafter.
- Recruiter-privacy rule applied (no individual recruiter personal data recorded).

**Dependencies.** Ethics approval (M1) for collection; pre-registered protocol (M3); deployed schema (M4). Taxonomy anchoring **must precede** scoring in M7.

**Estimated duration.** Effort **4–6 days** (manual collection + anchoring); elapsed **1–2 weeks**.

**Risks.**
- *Job-board ToS restrictions.* Some boards prohibit automated collection too. *Mitigation:* prefer manual capture for 200 items; check each source's terms. **[INSTITUTIONAL where restrictive]**
- *Anchoring drift.* Editing term lists after scoring begins breaks reproducibility. *Mitigation:* stamp and freeze the taxonomy version before any scoring.
- *Requirement–possession commensurability.* Required and held levels are not interchangeable (frozen caveat). *Mitigation:* keep the posting scores in their separate table and validate posting-side scoring on its own small pilot.

**Acceptance criteria.**
- ~200 postings captured with verbatim raw text and full provenance.
- Taxonomy versions stamped and frozen; anchoring documented (terms, frequencies, date).
- No recruiter personal data recorded.

---

## Milestone 7 — Pilot annotation and reliability check  **[BLOCKER-gated]**

**Objective.** Run the purposive reliability pilot on real profiles, compute per-dimension reliability, and revise rulebook *wording* (never the frozen criteria) if a dimension underperforms.

**Deliverables.**
- 10–20 purposively selected pilot profiles (clear, borderline, sparse, contradictory, under-signalled, inflation cases), collected and double-coded independently.
- Per-dimension Krippendorff's α with bootstrap CIs, raw percentage agreement, `n_units`, and `score_variance`, stored in `reliability_result`.
- Pre-stated expectation (recorded *before* the pilot) that D5/D6 will show lower reliability.
- Any rulebook-wording revisions logged via the revision-log procedure; re-pilot if triggered.

**Dependencies.** Ethics approval (M1); raters and interface (M5); taxonomy versions stamped (M6). Cannot start before M1 clears.

**Estimated duration.** Effort **3–5 days** per pilot round; elapsed **1–2 weeks per round**, plus a possible second round if a dimension needs revision.

**Risks.**
- *Low α on D5/D6.* Expected, not a failure — but damaging if discovered rather than predicted. *Mitigation:* record the expectation in advance so it reads as confirmed.
- *Pilot too small for stable α.* Wide CIs on 10–20 units. *Mitigation:* report CIs and variance, treat pilot α as indicative, confirm on the main double-coded subset.
- *Pressure to change frozen criteria.* Only rulebook *wording* may change, never the criteria. *Mitigation:* route every change through the revision log; escalate to supervisor if a criterion seems genuinely broken (that would be a framework-version decision, not a Task 5 action).

**Acceptance criteria.**
- Every dimension meets the frozen decision rule (α ≥ .667 minimum to proceed; < .667 triggers revision and re-pilot).
- Reliability results stored with full diagnostics.
- Any revisions logged; no frozen criterion altered.

---

## Milestone 8 — Collection-readiness gate and sign-off  **[BLOCKER]**

**Objective.** Verify, as a single gate, that every prerequisite is satisfied before main collection begins.

**Deliverables.**
- Completed collection-readiness checklist (roadmap §14), every governance blocker checked.
- Data-quality checklist (roadmap §13) dry-run on the pilot data, returning clean.
- Supervisor sign-off that governance blockers are cleared and the pilot met its criteria.

**Dependencies.** M1–M7 complete.

**Estimated duration.** Effort **1–2 days**; elapsed **2–4 days**.

**Risks.**
- *Silent open condition.* An unresolved ethics condition or a failed pilot dimension slips through. *Mitigation:* the gate is pass/fail per item; a single unchecked blocker halts collection.
- *Scope drift since approval.* What you built differs from what was approved. *Mitigation:* cross-check the approved scope (M1) against the frozen protocols before sign-off.

**Acceptance criteria.**
- All [BLOCKER] items checked, with references recorded.
- Pilot data passes the data-quality dry-run.
- Written supervisor sign-off obtained. **Only now does main collection begin.**

---

## Consolidated schedule view

| M | Milestone | Effort | Elapsed | Can run during M1 wait? | Gates collection? |
|---|---|---|---|---|---|
| 0 | Governance package | 5–8 d | 1–2 wk | starts before M1 | — |
| 1 | Institutional approval | 1–3 d | **3–8 wk** | *is* the wait | **[BLOCKER]** |
| 2 | DMP + infrastructure | 2–4 d | 1–2 wk | ✅ yes | — |
| 3 | Protocol pre-registration | 2–3 d | ~1 wk | ✅ yes (freeze on approval) | — |
| 4 | Environment + schema deploy | 1–2 d | 2–3 d | ✅ yes | — |
| 5 | Annotation system + raters | 4–7 d | 1–2 wk | ✅ interface/dry-run yes | — |
| 6 | Job postings + taxonomy anchoring | 4–6 d | 1–2 wk | ❌ needs approval | precedes scoring |
| 7 | Pilot + reliability | 3–5 d/round | 1–2 wk/round | ❌ needs approval | — |
| 8 | Readiness gate | 1–2 d | 2–4 d | ❌ final gate | **[BLOCKER]** |

**Total elapsed, realistic range:** roughly **7–12 weeks**, of which perhaps 3–4 weeks is your own effort and the remainder is institutional turnaround overlapped with parallel work. Compress the timeline by submitting M1 early and filling the wait with M2–M5; you cannot compress the committee's clock, so protect the schedule by not letting it run idle.

---

## Reviewer's note on this plan

Two things determine whether this schedule holds. First, **submit the governance package as early as humanly possible** — every day M1 starts earlier is a day off the critical path, and nothing you do downstream recovers a late submission. Second, **do not treat the approval wait as downtime**: M2 through M5 involve no personal data and can be built entirely in parallel, so that the day approval lands you are ready to collect. The milestones that *cannot* be parallelised (M6 job postings and taxonomy anchoring, M7 pilot) are exactly the ones that need approval first, which is why front-loading everything else matters.

No database modifications are included in this plan; Milestone 4 deploys the frozen Schema v1.0.1 as-is.
