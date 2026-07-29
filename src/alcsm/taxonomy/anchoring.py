"""Seed the eight taxonomies' term lists from collected job postings.

TODO (Phase P3): implement once ~200 job postings are collected
(gated on ethics approval, PROJECT_CONTEXT.md §38, §46).

Must:
    - derive term lists only from evidenced job-posting vocabulary,
      never invent unevidenced terms (PROJECT_CONTEXT.md §27);
    - stamp a `taxonomy_version` and freeze it — no edits to a frozen
      version (PROJECT_CONTEXT.md §15, §37);
    - the eight taxonomies' *structure* (degree, certification,
      AI-role, leadership-level, technical-contribution,
      professional-engagement, AI-keyword-ontology,
      automation/augmentation) is frozen; only term-list *content* is
      anchored here (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §2, §16).

F-06 (`taxonomy_version_id NOT NULL`) is enabled only after a taxonomy
version is stamped here — not before (PROJECT_CONTEXT.md §17, §44).

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def anchor_taxonomy_from_postings(*args: object, **kwargs: object) -> None:
    """Placeholder for taxonomy anchoring. See module TODO."""
    raise NotImplementedError(
        "Implemented in Phase P3, after job postings are collected."
    )
