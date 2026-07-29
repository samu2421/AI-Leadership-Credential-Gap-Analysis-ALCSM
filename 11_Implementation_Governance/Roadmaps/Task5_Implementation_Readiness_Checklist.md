# Task 5 Implementation Readiness Checklist
### Clean Handover Point Before Any Code Is Written

**Purpose:** confirm the project is in a safe, unambiguous state for Claude Code to begin Task 5 implementation. **Coding has not started and must not start until the governance gate (Section 3) is cleared for any step touching real data.**

Legend: ✅ done · ⏳ pending (external) · ▶️ ready for implementation to begin · ⛔ blocker.

---

## 1. Documentation freeze — ✅ COMPLETED

- [x] Tasks 1–4 frozen (framework, scoring model, rulebook, schema v1.0.1).
- [x] Approved reconciliation **C-1** applied — coding rulebook now reads *"revise the rulebook wording (never the frozen scoring criteria) and re-pilot."*
- [x] Approved reconciliation **C-2** applied — `Task4_Data_Schema_Design.md` now reads *"twenty-two base tables and five analysis views."*
- [x] Duplicate documents resolved; canonical files fixed in `Document_Version_Policy.md`.
- [x] Superseded files moved to `Archive/Superseded_Task1_Task4/` (retained, not deleted).
- [x] `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` finalised — all confirmation markers removed; final decisions embedded.
- [x] `README.md` and `CLAUDE_CODE_RULES.md` created.

**Status: documentation is frozen and internally consistent.**

---

## 2. Repository structure — ▶️ READY (to be instantiated)

- [x] Target folder architecture defined (`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §5).
- [x] Root governance files authored (`README.md`, `CLAUDE_CODE_RULES.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `Document_Version_Policy.md`).
- [ ] ▶️ Repository initialised with the defined layout (**Phase P0** — first implementation action).
- [ ] ▶️ `.gitignore` verified to exclude `data/`, `.env`, secrets **before first commit**.
- [ ] ▶️ `pyproject.toml` created (Python 3.11+, deps, black/ruff/mypy/pytest).
- [ ] ▶️ Frozen `docs/` and `schema/` populated; superseded files under `Archive/`.
- [ ] ▶️ Frozen states tagged (`framework-v1.0`, `schema-v1.0.1`).

**Status: fully specified; instantiation is the first coding task (no methodology risk).**

---

## 3. Ethics / GDPR — ⏳ PENDING · ⛔ BLOCKER for real data

- [ ] ⛔ Ethics committee approval obtained (reference recorded).
- [ ] ⛔ GDPR legal basis documented; Legitimate Interests Assessment written.
- [ ] ⛔ Article 14 notification position decided with DPO; public privacy notice published.
- [ ] ⛔ DPIA completed, or written DPO confirmation none is required.
- [ ] ⛔ Controller identified; storage confirmed EEA-resident and access-controlled.
- [ ] ⛔ Collection **method** approved (manual collection recommended; no scraping).
- [ ] ⛔ Re-identification-mapping decision made and documented.

**Status: PENDING. No LinkedIn profile may be collected until every box here is checked. Non-personal-data implementation (Sections 2, 7) may proceed in parallel during the approval wait.**

---

## 4. Database — ✅ READY

- [x] Schema frozen at v1.0.1; deploys clean on PostgreSQL 16.
- [x] 22 tables, 5 views, 66 CHECK constraints, 33 FKs — validated (67-test harness passes).
- [x] Backup/restore round-trip verified (`scripts/backup_alcsm.sh`).
- [x] Deferred hardening documented (F-06 after taxonomy anchoring; F-07 optional; F-08 after ethics).
- [ ] ▶️ Deploy to the project's secure-store PostgreSQL instance (Phase P0).
- [ ] ▶️ Load reference data (6 dimensions, 4 missing states, 15 precedents **with real text**, raters).

**Status: schema is production-ready; deployment to the live secure store is a P0 task.**

---

## 5. Collection workflow — ▶️ READY

- [x] Manual collection SOP written (`Task5_LinkedIn_Collection_Workflow.md`).
- [x] Validated insertion helper (`collection_helper.py`) — 8/8 tests pass, atomic, privacy-enforcing.
- [x] Provenance, pseudonymisation-at-capture, empty-vs-not-retrieved handling all implemented and tested.
- [x] Single authoritative write path confirmed (the helper; no duplicate ORM write path).
- [ ] ▶️ Port helper into `src/alcsm/collection/helper.py` with tests (Phase P1).
- [ ] ⏳ Execute only after Section 3 clears.

**Status: tooling ready; live collection gated on ethics.**

---

## 6. Annotation workflow — ▶️ READY

- [x] Annotation handbook complete (`ALCSM_Annotation_Handbook.md`): sequence, decision tree, evidence rules, ambiguity/contradiction handling, precedents, adjudication, examples, QA, reliability.
- [x] Rulebook and pilot design frozen; C-1 reconciliation applied.
- [x] Double-coding policy fixed: *"100% double coding if feasible; otherwise a pre-registered random subset of at least 15%."*
- [ ] ▶️ Annotation interface built honouring the four constraints (one profile's six dimensions together; no RQ4 values visible; blind cross-check; full evidence/flag capture) — Phase P4.
- [ ] ⏳ Rater onboarding + certification, pilot coding — after Section 3 clears and taxonomy anchoring (Section 7) is done.

**Status: methodology and rules ready; interface build is a P4 task.**

---

## 7. NLP preparation — ▶️ READY (architecture fixed; build later)

- [x] NLP architecture and stages defined (`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §10).
- [x] Local-only model policy fixed: **no external-API processing of profile text**; spaCy / sentence-transformers / HuggingFace only.
- [x] Comparability rule fixed (same information base as human coders; recorded per run).
- [x] Evaluation path defined (`v_nlp_evaluation`, per-dimension, ordinal metrics).
- [ ] ▶️ Depends on a human gold standard existing (Phase P6) and taxonomies anchored (Phase P3) — **do not train before both exist.**

**Status: architecture frozen; implementation deferred to after the gold standard exists.**

---

## 8. Taxonomy anchoring — ⏳ sequenced

- [x] Anchoring procedure defined (seed term lists from the 200 job postings, then stamp `taxonomy_version`).
- [ ] ⏳ Requires job-posting collection first (Phase P3, after ethics).
- [ ] ⏳ Enable F-06 (`taxonomy_version_id NOT NULL`) only after a taxonomy version is stamped.

**Status: sequenced correctly; cannot begin before job postings are collected.**

---

## Overall readiness summary

| Area | State |
|---|---|
| Documentation freeze | ✅ Complete |
| Repository structure | ▶️ Ready to instantiate (P0) |
| Ethics / GDPR | ⏳ **Pending — blocks real data** |
| Database | ✅ Ready; deploy in P0 |
| Collection workflow | ▶️ Ready; gated on ethics |
| Annotation workflow | ▶️ Ready; interface in P4 |
| NLP preparation | ▶️ Architecture fixed; build after P6 |
| Taxonomy anchoring | ⏳ After job postings (P3) |

## What Claude Code may start immediately (no real data, no methodology risk)

- **P0:** initialise repo, `.gitignore`, `pyproject.toml`, deploy schema to a local/dev PostgreSQL, run the validation harness, populate `docs/`, `schema/`, `Archive/`, tag frozen states.
- **P1:** port and test the collection helper (against constructed fixtures only).
- Scaffold (with tests) the `reliability/`, `taxonomy/`, `nlp/`, `analysis/`, and `app/` modules **using constructed fixtures** — no real data.

## What must NOT start yet

- ⛔ Any collection of real LinkedIn profiles (needs Section 3).
- ⛔ Taxonomy anchoring / F-06 (needs job postings, Section 8).
- ⛔ NLP model training (needs a human gold standard, Phase P6).

**This is a clean handover point. Implementation of non-personal-data scaffolding (P0–P1 and module skeletons with fixtures) may begin. Nothing touching real personal data proceeds until the ethics gate clears.**
