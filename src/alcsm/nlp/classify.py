"""Six ordinal 0-5 per-dimension predictors.

TODO (Phase P7): implement using the approved local-only stack in
order — spaCy, then sentence-transformers / local HuggingFace
embeddings, then an ordinal classifier (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
§10). No external-API calls on profile text, ever
(CLAUDE_CODE_RULES.md rule 8).

Must record `predicted_score`, optional confidence, and
`predicted_missing_status` per dimension, and a fixed `random_seed` +
`code_commit_hash` on the owning `nlp_model_run` for reproducibility
(PROJECT_CONTEXT.md §25, §37).

Depends on a human gold standard existing (Phase P6) and anchored
taxonomies (Phase P3) — do not train before both exist.

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def classify_dimension(*args: object, **kwargs: object) -> int:
    """Placeholder for an ordinal 0-5 dimension classifier. See module TODO."""
    raise NotImplementedError("Implemented in Phase P7 (nlp pipeline).")
