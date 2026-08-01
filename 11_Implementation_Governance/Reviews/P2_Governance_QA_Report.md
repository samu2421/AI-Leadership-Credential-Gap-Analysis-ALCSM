# P2 Governance QA Report
### Comprehensive Quality-Assurance Review of the Phase P2 Governance Package (Sessions 1–2)

**Session:** P2 Session 3 — Governance Validation (review only; no documents modified as part of producing this report, per session instruction).
**Scope reviewed:** all documents created in P2 Sessions 1–2 (`04_Ethics/` — 9 READMEs + 11 substantive documents), cross-checked against `PROJECT_CONTEXT.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `CLAUDE_CODE_RULES.md`, `Document_Version_Policy.md`, `DECISION_LOG.md`, `Implementation_Phase_Roadmap.md`, `README.md`, `VERSION.md`, `PROJECT_STRUCTURE.md`.
**Method:** every finding below was verified directly (grep-based cross-reference checks, side-by-side header comparison, close reading) — nothing here is asserted from memory alone.

---

## Executive Summary

The P2 governance package (folder structure + 11 substantive draft documents) is **substantively sound**: no frozen ALCSM methodology, database schema, or governance decision is contradicted anywhere in it, and the content itself (legal reasoning, GDPR structure, protocol design) is coherent and well-grounded in the pre-existing canonical sources (`Task5_PreCollection_Roadmap.md`, `Task5_LinkedIn_Collection_Workflow.md`). Nothing found in this review rises to the level of a substantive/legal defect.

What this review found instead is a set of **real but minor documentation-hygiene issues** — a naming-convention self-contradiction, one missing document header, one placeholder-format outlier, a stale top-level structure diagram, and several places where the ethics documents could be strengthened before an actual DPO/committee ever sees them. None of these block continued work; several are worth fixing before a real submission is prepared, and are listed as recommendations, not applied.

**Overall recommendation: Ready to Freeze P2 documentation-drafting work, conditional on the minor fixes in §7 being addressed (by the author, or by Claude Code with explicit approval in a future session) before actual submission.** See §9 for the full readiness assessment.

---

## 1. Repository Audit (Task 2)

Consistency checked pairwise across the nine named governance documents plus `04_Ethics/`.

| Check | Result |
|---|---|
| `PROJECT_CONTEXT.md` ↔ `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` ↔ `PROJECT_STRUCTURE.md` roadmap phase count | **Already-known, already-documented disagreement** (P0–P8 vs. P0–P9). Not new; tracked as `DECISION_LOG.md` §8 open item and `Implementation_Phase_Roadmap.md` §9 finding F-1. No change in status. |
| `DECISION_LOG.md` entries vs. what actually happened in P2 Sessions 1–2 | **Gap found.** No `DECISION_LOG.md` entry exists for "P2 Sessions 1–2: ethics/GDPR governance package drafted" or for "04_Ethics folder structure approved and instantiated" — both are exactly the kind of consequential decision/milestone the log's own §2 purpose statement says it exists to capture (compare to D-0017/D-0021 for P0/P1 completion). **Not fixed — flagged for the author, since editing `DECISION_LOG.md` was not authorised this session.** |
| `VERSION.md` vs. the new `04_Ethics/` package | `VERSION.md` tracks "frozen/major project component" versions and hasn't been touched — reasonably, since the ethics package is explicitly draft, not frozen. No entry is strictly required, but consider whether "P2 governance drafting begun" belongs in the Version Log for completeness, given `VERSION.md` already logs non-frozen structural events (e.g. the 2026-07-28 Project Structure v1.1 row). **Judgment call for the author, not a defect.** |
| `PROJECT_STRUCTURE.md` §2 folder-tree diagram vs. actual `04_Ethics/` content | **Stale.** The tree gives `03_Database_Design/` four labelled subfolder lines but still shows `04_Ethics/` as a single unexpanded leaf ("IRB approvals, consent forms"), even though `04_Ethics/` now has the same kind of nine-subfolder structure. This is the same class of issue already corrected once before for the top-level 00–17 numbering (`DECISION_LOG.md` D-0018) — it has recurred at one level deeper. **Not fixed — reported per this session's "report first" instruction.** |
| `README.md` (root) vs. `04_Ethics/` content | No new inconsistency. `README.md` already only describes the aspirational flat `docs/ethics/` layout in passing, unrelated to the actual numbered-folder structure; this was already a known, separately tracked gap (not something P2 Sessions 1–2 made worse). |
| `Document_Version_Policy.md` vs. `04_Ethics/` | No conflict. `Document_Version_Policy.md`'s canonical register does not (and is not expected to) list draft ethics documents — its scope is the Task 1–4 frozen-artefact register specifically. Each `04_Ethics/` subfolder's own README carries its own versioning rules instead, which is consistent with the delegated-ownership pattern already used elsewhere (e.g. `15_Scripts/README.md` owning its own naming rule). |
| `Implementation_Phase_Roadmap.md` P2 definition vs. what was actually done in Sessions 1–2 | **Consistent.** Everything produced is a governance/document artefact; nothing in `04_Ethics/` contains code, SQL, or an implementation decision, matching P2's "Allowed implementation work: None in the software-engineering sense" boundary exactly. |

---

## 2. Document Audit (Task 1)

Findings from a full pass over all 20 files in `04_Ethics/` (9 READMEs + 11 substantive documents), checked against every category the session asked for.

### 2.1 Confirmed issues

**D-1 (naming convention self-contradiction — the most concrete finding in this review).**
Three different naming-convention statements exist for documents in this folder tree, and the files actually created don't match two of the three:
- `04_Ethics/README.md` (pre-existing, root): `ALCSM_Ethics_<Description>_v<Major>.<Minor>_<YYYY-MM-DD>.<ext>` — **requires** a trailing date.
- `04_Ethics/01_Ethics_Approval/README.md` (new): states the *same* date-suffixed pattern (`...[-STATUS]_<YYYY-MM-DD>.<ext>`) — but its own very next line's example, `ALCSM_Ethics_ApplicationDraft_v0.1-DRAFT.md`, **omits the date entirely**. The stated rule and its own worked example contradict each other within the same file.
- `04_Ethics/02_DPIA/README.md`, `03_LIA/README.md`, `04_Privacy_Notice/README.md`, `05_Consent_Materials/README.md`, `06_GDPR_Documentation/README.md`, `09_Review_Logs/README.md` (all new): state a *third*, no-date pattern (`ALCSM_Ethics_<Name>_v<Major>.<Minor>[-STATUS].<ext>`).
- **The ten actual files created follow the third (no-date) pattern** — which matches `PROJECT_STRUCTURE.md` §4's project-wide convention, but matches neither of the two ethics-folder-specific conventions stated above.
- *Not fixed.* Recommended resolution (author's choice, not applied): either (a) drop the date-suffix requirement from `04_Ethics/README.md` and `01_Ethics_Approval/README.md` to match the other six subfolder READMEs and the files actually in use, or (b) rename the ten files to add a date suffix and keep the stricter rule. Option (a) requires touching two README files; option (b) requires renaming ten documents and updating every cross-reference to them (see D-3 below for why that's a non-trivial ripple).

**D-2 (missing document header).**
Every one of the 11 substantive documents states an explicit `**STATUS: DRAFT — ...**` line at the top **except** `09_Review_Logs/ALCSM_Ethics_GovernanceConsistencyReview_v0.1-DRAFT.md`, which has a `**Version:**` line but no `STATUS:` line at all. Minor, but it is the one document in the set that doesn't visibly assert its own draft/unapproved status at a glance.

**D-3 (placeholder format outlier).**
38 of 39 placeholder fields in the package use the form `` `[INSERT: <description>]` `` (colon). One uses an em dash instead: `04_Ethics/06_GDPR_Documentation/ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md:82` — `` `[INSERT — typically the university, to be confirmed]` ``. Purely cosmetic, but worth normalising since a find-and-replace pass by the author (filling in real values before submission) is more reliable against one consistent pattern.

**D-4 (header block spacing inconsistency).**
Eight of the eleven documents put a blank line between the `STATUS:` line and the `Version:` line; two (`ALCSM_Ethics_SurveyInfoSheet_v0.1-DRAFT.md`, `ALCSM_Ethics_SurveyConsentForm_v0.1-DRAFT.md`) run them back-to-back with no blank line. Purely cosmetic Markdown rendering difference, not a content issue.

### 2.2 Checked and found consistent (verified, not assumed)

- **Cross-references / filenames:** every backtick-quoted `ALCSM_Ethics_*.md` filename referenced anywhere in the package (Annex lists, "related documents" lines, the Consistency Review's document table) resolves to a real file at the path implied. No broken cross-reference found.
- **Version numbers:** all 11 substantive documents are tagged `0.1-DRAFT`, with no stray `0.2`, `1.0`, or mismatched version anywhere.
- **Terminology:** "signal, not competence" framing, "credential signal," and the six-dimension language are used consistently and correctly wherever the ALCSM methodology is referenced.
- **No duplicated-and-conflicting statements:** the *hiQ Labs v. LinkedIn* reasoning and the Article 14 transparency reasoning are independently restated (by design, so each document is legible standalone to a reviewer who may not read the others) in the Ethics Application, the Collection Protocol, and the DPIA — but the wording differs each time (paraphrased, not copy-pasted) and no restatement contradicts another. This repetition is already self-flagged, accurately, in the Consistency Review's own §5.
- **No contradictory requirements:** retention, controller identification, and supervisory-authority fields are consistently deferred to placeholders everywhere they appear, all pointing back to the DMP as the source of truth, rather than different documents asserting different concrete (and possibly conflicting) values.
- **Folder references:** every subfolder README's "What Belongs Here" content matches what was actually placed in that subfolder.
- **Spelling:** no spelling errors found in a full read-through of all 11 documents.

---

## 3. Cross-reference Audit

Performed by extracting every backtick-quoted `.md` filename mentioned inside `04_Ethics/` and confirming each resolves to an actual file (see §2.2). Result: **zero broken cross-references.** The one non-resolving bracketed string found (`ALCSM_Ethics_ApplicationDraft_v1.0-SUBMITTED_2026-XX-XX.md`) is an illustrative *future* filename inside a naming-convention example, not a reference to a document expected to exist now — not a defect, but see D-1 above for the convention it illustrates being internally contradictory.

---

## 4. Placeholder Audit (Task 3) — Consolidated Master Checklist

39 placeholder fields across the 11 substantive documents, grouped by category. Each item names every document it appears in, so a single real value can be propagated to every occurrence.

### Committee information
- Name of institutional ethics committee / research ethics board — *Ethics Application, DPIA Screening, Privacy Notice, Data Management Plan*
- Committee decision (Approved / Approved with conditions / Rejected / Deferred), reference number, date, conditions, signature — *Ethics Application (decision table)*

### Supervisor information
- Supervisor name — *Ethics Application, Survey Information Sheet*

### DPO information
- Institutional DPO name/contact — *Ethics Application, Privacy Notice, Survey Information Sheet, Data Management Plan*
- DPO review of DPIA screening (yes/no, date) and conclusion — *DPIA Screening*
- DPO review of full DPIA (yes/no, date), residual-risk determination, conditions, sign-off (name/role/date) — *Full DPIA*
- DPO review of LIA (yes/no, date) and conclusion — *LIA*

### Institution-specific values
- Controller identity (university vs. researcher, to be confirmed) — *Full DPIA, Data Management Plan* (⚠ inconsistent bracket punctuation between these two — see D-3)
- Relevant data-protection supervisory authority (for complaints) — *Privacy Notice, Survey Information Sheet*
- University-approved storage system / specific approved host — *Survey Information Sheet, Data Management Plan*
- University email address(es) for the researcher — *Privacy Notice, Survey Information Sheet*
- DMP template basis — confirm or replace with SRH's own DMP template if one exists — *Data Management Plan*

### Dates
- Application preparation date — *Ethics Application*
- Collection window (start/end dates) — *LinkedIn Collection Protocol* (appears twice: §3 and §7)
- Language scope for collection (e.g. "English-language profiles") — *LinkedIn Collection Protocol*
- Final AI-leadership title list — *LinkedIn Collection Protocol*

### Approval references
- Ethics approval reference number — *Ethics Application, Privacy Notice*

### Retention periods
- Retention period/trigger for profile and survey data — *Ethics Application, Privacy Notice, Data Management Plan, Survey Information Sheet* (four places; DMP §8 is the source of truth, the others should quote it once fixed)
- Name of person responsible for executing data destruction — *Data Management Plan*

### Survey details
- Number of survey questions (N) — *Survey Information Sheet*
- Expected survey duration (X minutes) — *Survey Information Sheet*
- Respondent expertise-area description (e.g. "AI / data science / leadership / recruitment") — *Survey Information Sheet*
- Consent-form version date shown to respondents — *Survey Consent Form* (must match the Information Sheet's own date — see the versioning rule already stated in `05_Consent_Materials/README.md`)

### Publication information
- Privacy notice intended publication URL — *Privacy Notice*

### Decisions requiring judgment, not just a fill-in-the-blank value
- Re-identification-mapping option (no mapping / temporary / retained — DMP recommends "no mapping" as the default) — *Data Management Plan §4.1, LinkedIn Collection Protocol §9* — this is the one placeholder category that is a genuine open decision for the author and DPO, not a fact to transcribe.

---

## 5. Recommended Improvements (Task 4) — not applied

Reviewed each substantive document as if preparing it for actual institutional submission. Recommendations below; none applied.

| Document | Recommendation |
|---|---|
| **Ethics Application** | Add an explicit sample-size-honesty line ("500 is a pragmatic, manually-tractable target, not derived from a power calculation") — this is already disclosed in the LIA and the pre-collection roadmap but is a natural committee question the Application itself doesn't pre-empt. Also missing a direct citation to `DECISION_LOG.md`/`Implementation_Phase_Roadmap.md` for a reader who wants the fuller governance trail (the Protocol and Checklist documents already do this). §12 ("Committee questions this application anticipates") reads more like an internal prep note than committee-facing prose — consider moving it to `09_Review_Logs/` as a prep aid and trimming it from the actual submission copy. |
| **LinkedIn Collection Protocol** | Does not address whether the researcher browses LinkedIn while logged into a personal account (common in practice) versus fully logged-out — this materially affects the "public-only" claim's strength and is exactly the kind of question a DPO is likely to ask. Recommend adding an explicit line stating the browsing mode and, if logged-in browsing is used, addressing that directly rather than leaving it implicit. |
| **DPIA Screening** | Solid; no changes recommended beyond what's already flagged in D-1–D-4. |
| **Full DPIA** | No "Consultation" section addressing Art 35(9)'s expectation that the views of data subjects (or their representatives) be sought "where appropriate." Given the population size and pseudonymisation constraints this may reasonably be judged infeasible/inappropriate here, but the DPIA should say so explicitly and justify the omission rather than being silent on it. Also consider whether the institution's own DPIA template uses a numeric likelihood × severity risk matrix rather than the qualitative Low/Medium/High labels used here — flag this as a possible format (not substance) change once the institution's template is known. |
| **LIA** | The "reasonable expectation" consideration is present but folded into the balancing-test prose rather than labelled as its own sub-test, which is how the ICO's commonly-used three-part LIA template presents it. Consider giving it an explicit subheading for ease of committee review. |
| **Privacy Notice** | Add one sentence confirming no international data transfer occurs (a standard, reassuring line in public privacy notices, and directly supported by the DMP's EEA-residency commitment). Consider a short "how was I found" sentence, since a member of the public reading this notice may not otherwise understand how their specific profile came to be in scope. |
| **Survey Information Sheet / Consent Form** | "Withdrawal after submission may not be possible" — clarify precisely what "submission" means (submitting the full survey vs. each individual answer) to remove a small but real ambiguity a respondent could reasonably raise. |
| **Data Management Plan** | Otherwise strong; the em-dash placeholder (D-3) is the only concrete issue found in this document. |
| **GDPR Compliance Checklist** | No changes recommended — it is explicitly an index into the other documents and does so accurately. |
| **Governance Consistency Review** | Add the missing `STATUS:` header (D-2) for consistency with the rest of the package. |

None of the above are legal defects — they are the kind of tightening a supervisor or DPO would likely ask for on a first read, flagged here so they can be addressed in one pass rather than discovered piecemeal.

---

## 6. Risk Assessment

| Risk | Severity | Notes |
|---|---|---|
| A committee/DPO reads the naming-convention contradiction (D-1) and questions document-control rigour | Low | Cosmetic; does not affect the substance of any claim made in the documents themselves. |
| The missing DPIA "Consultation" section is queried by the DPO | Low–Medium | A real, foreseeable question; better to pre-empt it with an explicit justification than to be asked for one later, which would cost a review cycle. |
| The "logged-in vs. logged-out browsing" gap in the Collection Protocol is queried | Medium | This is the single highest-value fix in this review — it goes directly to the strength of the "public-only" collection claim, which `Task5_PreCollection_Roadmap.md` §0 already identifies as the single largest risk in the whole thesis. |
| `DECISION_LOG.md` gap (no entry for P2 Sessions 1–2) is noticed by an examiner reviewing the governance trail | Low | Purely a completeness gap in an internal audit tool, not visible to an external committee. |
| Any of the above blocks actual ethics submission | **None** | Every finding here is a documentation-quality issue, not a substantive gap in the legal/ethical reasoning itself. |

**No finding in this report identifies a legal, methodological, or schema risk.** Every finding is a documentation-hygiene or submission-polish item.

---

## 7. Remaining Blockers (unchanged from P2 Session 2, restated for completeness)

1. Every `[INSERT: ...]` placeholder in §4 needs a real value.
2. Supervisor review of the full package.
3. DPO review and sign-off on the LIA's balancing test and the DPIA.
4. Actual submission to the ethics committee and its decision.
5. Publication of the privacy notice.

None of these are new; this session did not resolve or advance any of them, by design (governance validation only).

---

## 8. Summary of Findings by Severity

| Severity | Count | Items |
|---|---|---|
| Legal/methodological defect | 0 | — |
| Moderate (should fix before submission) | 2 | Logged-in/out browsing gap (Protocol); DPIA Consultation section gap |
| Minor (documentation hygiene) | 4 | D-1 naming convention, D-2 missing header, D-3 placeholder punctuation, D-4 header spacing |
| Low (polish/nice-to-have) | 7 | The remaining §5 recommendations not already counted above |
| Repository-level (not new, already tracked) | 3 | P8/P9 roadmap split, P4 granularity, stale `PROJECT_STRUCTURE.md` tree (new instance of a known pattern) |

---

## 9. Readiness Assessment

- **Internal consistency:** sound, with the minor documentation-hygiene exceptions listed above.
- **Terminology and methodology fidelity:** fully consistent with frozen ALCSM methodology and all prior governance decisions — no violation found anywhere in the package.
- **Cross-references:** all verified resolvable; zero broken links.
- **Substantive legal/ethical content:** coherent and well-grounded; the two moderate-severity gaps (§5, §6) are the kind of thing a first-pass reviewer flags, not the kind that would cause a rejection.
- **Placeholders:** fully catalogued (§4); none silently guessed at anywhere in the package.

### Recommendation: **Ready to Freeze P2 (documentation-drafting stage)**

The governance package is ready to be treated as the frozen basis for the next stage of work (placeholder resolution and supervisor/DPO review), **provided** the four minor documentation-hygiene items (D-1–D-4) and, ideally, the two moderate-severity content gaps (§5: logged-in/out browsing clarification; DPIA Consultation section) are addressed first — none of which require new documents, only edits to the ones that already exist, with your explicit approval.

**Not** recommending "Additional Work Required" as a blocking verdict, because nothing found here is a defect in the underlying reasoning — it is a polish pass on an otherwise sound package.

---

*This report is itself a governance document. No file inside `04_Ethics/` or any of the nine cross-checked governance documents was modified in the course of producing it.*
