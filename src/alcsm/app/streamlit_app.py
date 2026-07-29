"""ALCSM screening tool — Streamlit app (RQ5 demonstration artefact).

TODO (Phase P9): implement per CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §9.

The dashboard MUST display, per profile: the six ALCSM dimension
scores (0-5); missingness status per dimension; the completeness
index; evidence summaries; validation indicators (ambiguity /
contradiction flags, NLP confidence where available).

The dashboard MUST NOT display a single ALCSM composite score.
Aggregation is exploratory only until empirically validated — if ever
offered, it must be a clearly-labelled panel comparing candidate
aggregation methods, never one hard-coded number presented as "the"
score (PROJECT_CONTEXT.md §24, §44, CLAUDE_CODE_RULES.md rule 2).

No RQ4 impact values may be shown as if they were part of ALCSM. No
browser storage of personal data.

Depends on the NLP pipeline (Phase P7) producing predictions to
display. Intentionally left unimplemented — no Streamlit page is
built in Phase P0 (repository scaffolding only).
"""

from __future__ import annotations


def main() -> None:
    """Entry point placeholder. See module TODO."""
    raise NotImplementedError(
        "Streamlit screening tool is built in Phase P9, after the "
        "NLP pipeline (P7) exists."
    )


if __name__ == "__main__":
    main()
