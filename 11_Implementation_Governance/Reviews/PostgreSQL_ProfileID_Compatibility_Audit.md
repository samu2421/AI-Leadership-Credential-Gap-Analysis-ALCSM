# PostgreSQL Profile_ID Compatibility Audit

**Status:** Investigation complete. **No schema, application, or data change has been made.** This report stops at the point Part D of this session's brief requires — awaiting an explicit decision before any fix is applied.
**Author:** Samiksha Dhere (researcher) — investigated with Claude Code assistance
**Date:** 2026-08-24

---

## Method

Every finding below was verified directly against the real, currently-running local PostgreSQL 16 instance and its `alcsm_dev` database (confirmed live via `pg_isready`, `psql -l`) — not inferred from the schema file alone. `alcsm.profile` currently contains **zero rows**; every test in this audit that touches the database was run inside a transaction that was rolled back, so nothing was left changed.

## A. Actual database constraint

```sql
"profile_profile_id_check" CHECK (profile_id ~ '^PRF-[0-9]{5}$'::text)
```

Confirmed via `\d alcsm.profile` against the live `alcsm_dev` database — matches `alcsm_schema_v1.0.1.sql` exactly (line 151). `profile_id` is the table's primary key, referenced by six foreign keys (`adjudication_record`, `alcsm_dimension_score`, `nlp_prediction`, `profile_derived`, `profile_raw_section`, `rq4_impact_indicator`) — none of these carry their own separate profile_id format constraint; they simply require the referenced `profile` row to already exist, which itself requires satisfying the CHECK above.

## B. Actual application expectation

Two independent layers both currently expect `PRF-#####`, and one previously-unverified layer does not work against the real database at all:

1. **`collection/helper.py`**'s own Python-level validator: `_PROFILE_ID_PATTERN = re.compile(r"^PRF-\d{5}$")`, enforced in `validate_profile_record()` before any DB round-trip — rejects `LP####` even before an insert is attempted.
2. **The `alcsm.annotation` package** (built for the P4 interface) does not independently validate profile_id format — `validate_annotation_score()` only checks for presence, not shape — so a malformed id would only be caught downstream, either by `profile`'s own CHECK (if the profile row is being created) or by the FK constraint (if it is not).
3. **`db/models.py::reflect_metadata()`/`get_table()`** — a separate, newly-confirmed bug, unrelated to Profile_ID format but discovered while completing this audit's checklist point 4: `MetaData().reflect(bind=engine)` is called with no `schema=` argument, and the real database's tables all live under the `alcsm` schema, not the connection's default (`public`). Verified directly: unqualified `reflect()` finds **zero** tables against `alcsm_dev`; `reflect(schema="alcsm")` finds all 22. `tests/db/test_models.py`'s existing coverage never caught this because it only exercises the reflection wrapper against an in-memory SQLite database with no schema at all — it has never been run against the real ALCSM schema shape. This means `db/models.py` in its current form cannot be used to inspect the real database regardless of the Profile_ID question. Reported here because it directly bears on checklist point 4 ("inspect the current SQLAlchemy reflection"); recommended fix in §E is independent of, and much lower-risk than, the Profile_ID question.
4. **A third, smaller, related finding:** `config.py::load_settings()` currently cannot load the project's own `.env` file as delivered (`DATABASE_PASSWORD=` — empty) because `_require_env` treats an empty string the same as a missing variable. Local Postgres uses trust authentication (no password needed), so this is a false rejection, not a real missing-credential case. This blocked the reflection check above until `Settings`/`DatabaseSettings` were constructed directly, bypassing `load_settings()`. Noted for completeness; not a Profile_ID issue.

## C. Actual final-data ID format

`LP####` (e.g., `LP0041`, `LP0170`, `LP0182`) — confirmed as the format used throughout the frozen final annotation dataset (`06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`, all 500 profiles) and the processed LinkedIn workbook it derives from. This is not a hypothesis; it is the verified, actual, exclusive format across every real profile record in the project.

## D. Exact incompatibility

Empirically confirmed by direct test (rolled back, no lasting change):

```sql
INSERT INTO alcsm.profile (profile_id, sampling_batch_id, search_query, inclusion_reason, collection_ts)
VALUES ('LP0041', 'BATCH-999', 'test', 'title_match', now());
-- ERROR: new row for relation "profile" violates check constraint "profile_profile_id_check"
```

**No profile from the final annotation dataset can currently be loaded into `alcsm.profile` without transformation.** Since `alcsm_dimension_score`, `profile_raw_section`, `rq4_impact_indicator`, etc. all require the referenced profile to already exist, this blocks the entire real-data database path, not just the `profile` table itself — exactly the same conclusion reached in the P4 session (D-0039) and D6 v1.1 task, now confirmed against the live database rather than inferred from the schema file.

## E. Least-invasive recommended fix (not applied)

Given the constraints this task sets — preserve `LP####` as the external analytical identifier, do not rename the 500 analytical Profile_IDs, do not silently change the framework, use the smallest safe change — **two candidate fixes exist, and choosing between them is a methodology decision the author should make, not one this audit resolves on its own:**

**Option 1 — Widen the CHECK constraint's accepted pattern.**
```sql
ALTER TABLE alcsm.profile
  DROP CONSTRAINT profile_profile_id_check,
  ADD CONSTRAINT profile_profile_id_check
    CHECK (profile_id ~ '^(PRF-[0-9]{5}|LP[0-9]{4,5})$');
```
`LP####` is stored and used as the actual primary key, unchanged, everywhere (database, Excel, every document). Smallest possible schema footprint: one constraint's regex text changes; no new column, no mapping table, no structural change to any table, view, or relationship. Requires a schema version bump (`v1.0.1` → `v1.0.2`, this project's own versioning convention for any DDL edit) and a corresponding `collection/helper.py` validator update (`_PROFILE_ID_PATTERN`) so the two layers stay in agreement. This is the option this audit leans toward recommending, on the grounds that it is genuinely the smallest possible change satisfying every stated constraint — but it is still a frozen-schema edit, which this project's standing rule requires the author to authorize explicitly, not an implementation judgment call.

**Option 2 — Add an ID-mapping layer, leave the CHECK constraint untouched.**
Keep `profile.profile_id` as `PRF-#####`-only (unchanged), add a new column (e.g., `external_profile_id`) to carry `LP####` as a parallel, UNIQUE, non-key reference, and generate a deterministic `PRF-#####` value at load time for the actual primary key. Leaves the frozen constraint's original intent (a single fixed ID format) fully intact and treats `LP####` as an external cross-reference rather than a database identifier change. Larger footprint than Option 1 (a new column, a generation/mapping step, and every downstream query that currently assumes `profile_id` *is* the analytical id would need to join through the mapping column instead) — for that reason, not the leading recommendation, but included because it is the more conservative reading of "do not silently change the framework": under Option 2 the database's original ID contract is never touched at all.

**Not recommended, and not compatible with this task's explicit constraints:** renaming the 500 analytical Profile_IDs to `PRF-#####` — this is Part D's own explicit prohibition, restated here only to confirm it was considered and rejected, not overlooked.

## What was NOT done in this audit

- No `ALTER TABLE`, no constraint change, no schema version bump.
- No code change to `collection/helper.py`, `db/models.py`, or `config.py` — the two additional bugs found in §B are reported, not fixed.
- No profile was inserted, updated, or left behind in `alcsm_dev` — the database is exactly as it was before this audit (0 rows in every table this audit touched).
- No decision was made between Option 1 and Option 2 above — that choice is exactly the kind of conceptual/methodological decision this session's closing instruction requires stopping for.

---

**STOP.** This audit is complete. A schema change (Option 1 or 2), the `db/models.py` schema-qualification fix, and the `config.py` empty-password handling are all ready to be scoped into concrete, tested changes the moment the author confirms which approach to take — none has been started.
