"""Credential gap per dimension (RQ2): mean required - mean held.

TODO (Phase P8): implement via
`db.queries.fetch_credential_gap_by_dimension`
(i.e. `v_credential_gap_by_dimension`).

Must never treat a job posting's silence about a dimension
(`not_applicable`) as "requires 0" — it is excluded from the gap
calculation entirely (PROJECT_CONTEXT.md §9, §27, common mistake #7 in
§39).

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def credential_gap_by_dimension(*args: object, **kwargs: object) -> list:
    """Placeholder for the RQ2 gap analysis. See module TODO."""
    raise NotImplementedError("Implemented in Phase P8 (analysis).")
