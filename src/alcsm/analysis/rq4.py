"""Ordinal correlation between credential signal and RQ4 impact indicators.

TODO (Phase P8): implement. `rq4_impact_indicator` values are
*external validation criteria*, physically isolated from the ALCSM
dimensions — they must never be used as a scoring input, and mixing
them into a dimension score would make the validation circular
(PROJECT_CONTEXT.md §5, §15, §27).

Use ordinal-appropriate correlation methods; never a hard-coded
composite dimension score as the predictor.

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def correlate_with_impact_indicators(*args: object, **kwargs: object) -> dict:
    """Placeholder for the RQ4 correlation analysis. See module TODO."""
    raise NotImplementedError("Implemented in Phase P8 (analysis).")
