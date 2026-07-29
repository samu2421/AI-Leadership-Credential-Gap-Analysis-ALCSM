"""Parse profile_raw_section text into per-dimension features.

TODO (Phase P7): implement. The AI-keyword ontology is used only to
*locate* candidate evidence spans — it must never itself set or raise
a score (PROJECT_CONTEXT.md §8, §27, common mistake #6 in §39).

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def extract_features(*args: object, **kwargs: object) -> dict:
    """Placeholder for per-dimension feature extraction. See module TODO."""
    raise NotImplementedError("Implemented in Phase P7 (nlp pipeline).")
