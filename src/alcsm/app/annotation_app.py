"""P4 annotation interface — Streamlit app.

Distinct from ``app/streamlit_app.py`` (the P9 NLP-screening tool, RQ5
demonstration artefact, still unimplemented pending Phase P7). This
app is the human-coding tool built in Phase P4 (CLAUDE_CODE_
IMPLEMENTATION_GUIDE.md §9 describes the P9 tool; the P4 tool's
requirements live in PROJECT_CONTEXT.md §11 and
``Implementation_Phase_Roadmap.md`` "P4 — Annotation interface and
pilot coding"). Keeping the two apps as separate entry points avoids
conflating a researcher-facing coding tool with a reader-facing
screening demo — they have different audiences, different data-safety
postures (this one needs a rater identity; the P9 tool does not), and
different lifecycles.

Workflow (this task's "Annotation Workflow" section):
    profile selection -> display evidence -> display D1-D6 ->
    researcher review -> accept/change/defer -> capture rationale ->
    save -> validation -> next profile

Enforces the four frozen constraints from PROJECT_CONTEXT.md §11 --
see :mod:`alcsm.annotation.workflow`'s module docstring for exactly
how each one is enforced, since this file is UI wiring around that
module's state machine, not where the enforcement logic itself lives.

Run with: ``streamlit run src/alcsm/app/annotation_app.py``
(requires the ``app`` extra: ``pip install -e ".[app]"``).

Runs against fixtures by default (no real data, no live DB required)
so the interface can be exercised right now, before P2/P3 clear — see
``11_Implementation_Governance/Reviews/P4_Dry_Run_Instructions.md``.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from alcsm.annotation.audit import AuditAction, AuditLogger, default_audit_log_path
from alcsm.annotation.dimension_config import DEFAULT_VERSION, get_dimension_config
from alcsm.annotation.fixtures import (
    FIXTURE_EVIDENCE,
    FIXTURE_SCORES,
    SYNTHETIC_PROFILES,
)
from alcsm.annotation.models import AnnotationScore, ReviewDecision
from alcsm.annotation.validation import validate_annotation_score
from alcsm.constants import MISSING_STATUSES, SCORE_MAX, SCORE_MIN

st.set_page_config(page_title="ALCSM P4 Annotation (dry run)", layout="wide")


def _get_audit_logger() -> AuditLogger:
    if "audit_logger" not in st.session_state:
        st.session_state.audit_logger = AuditLogger(default_audit_log_path())
    return st.session_state.audit_logger


def _get_decisions() -> dict[tuple[str, int], str]:
    """In-memory decision store for this dry-run session. A real pilot
    session persists to the database via alcsm.annotation.store instead
    of session_state -- this default keeps the dry run usable with no
    live database at all."""
    if "decisions" not in st.session_state:
        st.session_state.decisions = {}
    return st.session_state.decisions


def main() -> None:
    st.title("ALCSM P4 Annotation Interface — Dry Run")
    st.caption(
        "Fixture data only (constructed, non-personal profiles). "
        "Real pilot coding is blocked until P2 (ethics) and P3 (taxonomy "
        "anchoring) both clear, per Implementation_Phase_Roadmap.md."
    )

    with st.sidebar:
        st.header("Session")
        rater_id = st.selectbox("Rater", ["RATER_A", "RATER_B", "ADJUDICATOR"])
        dimension_version = st.selectbox(
            "Dimension config version",
            ["v1_1", "v1_0"],
            index=0 if DEFAULT_VERSION == "v1_1" else 1,
            help="v1_1 shows the proposed D6 (AI Industry/Application Breadth, "
            "PROPOSED/PILOT_REQUIRED). v1_0 shows the original, retired D6 "
            "(Professional Engagement) for comparison.",
        )
        profile_ids = [p.profile_id for p in SYNTHETIC_PROFILES]
        profile_id = st.selectbox("Profile", profile_ids)
        decisions = _get_decisions()
        done = sum(1 for d in range(1, 7) if (profile_id, d) in decisions)
        st.metric("Profile progress", f"{done} / 6 dimensions")
        st.caption(
            "A profile is not complete until all six dimensions have a decision "
            "(frozen constraint #1: score six dimensions together)."
        )

    dims = get_dimension_config(dimension_version)
    scores = FIXTURE_SCORES[profile_id]

    st.subheader(f"Profile {profile_id}")
    profile = next(p for p in SYNTHETIC_PROFILES if p.profile_id == profile_id)
    with st.expander("Profile text (fixture)", expanded=False):
        for name, section in profile.sections.items():
            if section.available:
                st.markdown(f"**{name}**: {section.text}")

    st.info(
        "No RQ4 impact indicators are shown here, by design (frozen "
        "constraint #2) -- RQ4 criterion variables are physically "
        "isolated from ALCSM dimension scoring."
    )

    for dim in dims:
        first_pass_score, missing_status = scores[dim.number]
        evidence = FIXTURE_EVIDENCE.get(dim.number, "")
        decision_key = (profile_id, dim.number)

        st.markdown("---")
        cols = st.columns([3, 2])
        with cols[0]:
            label = f"D{dim.number} — {dim.label}"
            if dim.is_proposed:
                label += "  ⚠️ PROPOSED/PILOT_REQUIRED"
            st.markdown(f"### {label}")
            st.caption(dim.definition)
            with st.expander("0-5 rubric"):
                for i, criterion in enumerate(dim.criteria):
                    st.write(f"**{i}** — {criterion}")

        with cols[1]:
            st.markdown("**First-pass reference (read-only)**")
            st.write(f"FIRST_PASS_SCORE = {first_pass_score}")
            st.write(f"Missing status: {missing_status}")
            if evidence:
                st.write(f"Evidence: _{evidence}_")
            st.caption(
                "This is a reference only, never the final score. "
                "FIRST_PASS_SCORE and FINAL_HUMAN_SCORE are distinct "
                "concepts; nothing here is written until you submit below."
            )

        st.markdown("**Your review (FINAL_HUMAN_SCORE)**")
        decision = st.radio(
            "Decision",
            [d.value for d in ReviewDecision],
            key=f"decision_{profile_id}_{dim.number}",
            horizontal=True,
        )
        rcols = st.columns(3)
        with rcols[0]:
            final_score = st.number_input(
                "Score (0-5)",
                min_value=SCORE_MIN,
                max_value=SCORE_MAX,
                value=first_pass_score,
                key=f"score_{profile_id}_{dim.number}",
            )
        with rcols[1]:
            missing_status_options: list[str] = list(MISSING_STATUSES)
            final_missing = st.selectbox(
                "Missing status",
                missing_status_options,
                index=missing_status_options.index(missing_status),
                key=f"missing_{profile_id}_{dim.number}",
            )
        with rcols[2]:
            precedent = st.text_input(
                "Precedent applied (optional, P-01..P-15)",
                key=f"precedent_{profile_id}_{dim.number}",
            )
        rationale = st.text_area(
            "Rationale / evidence for FINAL_HUMAN_SCORE",
            value=evidence if decision == ReviewDecision.ACCEPT.value else "",
            key=f"rationale_{profile_id}_{dim.number}",
        )

        if st.button("Save", key=f"save_{profile_id}_{dim.number}"):
            record = AnnotationScore(
                profile_id=profile_id,
                dimension_number=dim.number,
                rater_id=rater_id,
                score=int(final_score),
                missing_status=final_missing,  # type: ignore[arg-type]
                rulebook_version="v1.1-addendum" if dim.number == 6 else "1.0",
                coding_ts=datetime.now(),
                evidence_text=(
                    (rationale or None) if final_missing != "unavailable" else None
                ),
                precedent_applied=precedent or None,
            )
            problems = validate_annotation_score(record)
            if problems:
                st.error(
                    "Not saved -- validation failed:\n"
                    + "\n".join(f"- {p}" for p in problems)
                )
            else:
                decisions[decision_key] = decision
                audit_action = (
                    AuditAction.SCORE_SUBMITTED
                    if decision == ReviewDecision.ACCEPT.value
                    else AuditAction.SCORE_CHANGED
                )
                _get_audit_logger().record(
                    actor=rater_id,
                    action=audit_action,
                    profile_id=profile_id,
                    dimension_number=dim.number,
                    detail=decision,
                )
                st.success(
                    f"Saved (dry run, in-session only). "
                    f"D{dim.number} decision recorded: {decision}."
                )
                if (
                    decision != ReviewDecision.ACCEPT.value
                    and int(final_score) == first_pass_score
                ):
                    st.warning(
                        "Decision is not ACCEPT but the score matches the "
                        "first pass exactly -- confirm this is intended "
                        "(a CHANGE decision should usually change something)."
                    )

    st.markdown("---")
    if done < 6:
        st.warning(
            f"{6 - done} dimension(s) still need a decision before this "
            "profile counts as complete."
        )
    else:
        st.success("All six dimensions reviewed for this profile.")


if __name__ == "__main__":
    main()
