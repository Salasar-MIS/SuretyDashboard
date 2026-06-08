"""
Reusable data-entry dashboard for any branch or sub-branch.
Renders all 3 sections and an Admin panel for RM management.
Called by main.py with the branch_code of the selected branch.
"""
import streamlit as st
from ..utils.queries import (
    get_branch_by_code, get_rms,
    get_revenue_for_branch, get_targets_for_branch, get_proposals_for_branch,
    add_rm, deactivate_rm, rename_rm,
)
from ..components.section_revenue import render_section_revenue
from ..components.section_lakhs import render_section_lakhs
from ..components.section_proposals import render_section_proposals

FY = "2026-27"


def render(branch_code: str):
    branch = get_branch_by_code(branch_code)
    if not branch:
        st.error(f"Branch not found: {branch_code}")
        return

    branch_id = branch["_id"]
    st.title(f"Surety Dashboard — {branch['branch_name']}")
    st.caption(f"FY {FY}")

    # Load all data for this branch upfront
    rms          = get_rms(branch_id)
    revenue_data = get_revenue_for_branch(branch_id, FY)
    target_data  = get_targets_for_branch(branch_id, FY)
    proposals_data = get_proposals_for_branch(branch_id, FY)

    # ── Section 1 ─────────────────────────────────────────────────────────────
    render_section_revenue(branch_id, FY, rms, revenue_data)
    st.divider()

    # ── Section 2 ─────────────────────────────────────────────────────────────
    render_section_lakhs(branch_id, FY, rms, revenue_data, target_data)
    st.divider()

    # ── Section 3 ─────────────────────────────────────────────────────────────
    render_section_proposals(branch_id, FY, rms, proposals_data)
    st.divider()

    # ── Admin: RM Management ──────────────────────────────────────────────────
    with st.expander("Admin — Manage RMs", expanded=False):
        st.markdown("**Add RM**")
        new_name = st.text_input("New RM name", key=f"new_rm_{branch_code}")
        if st.button("Add", key=f"add_rm_{branch_code}"):
            name = new_name.strip()
            if name:
                add_rm(branch_id, name)
                st.success(f"Added RM: {name}")
                st.rerun()
            else:
                st.warning("Enter a name before adding.")

        all_rms = get_rms(branch_id, active_only=False)
        active_rms = [r for r in all_rms if r["is_active"]]

        if active_rms:
            st.markdown("**Rename / Remove RMs**")
            for rm in active_rms:
                col1, col2, col3 = st.columns([3, 2, 1])
                new_rm_name = col1.text_input(
                    "Name", value=rm["rm_name"],
                    key=f"rename_{rm['_id']}",
                    label_visibility="collapsed",
                )
                if col2.button("Rename", key=f"btn_rename_{rm['_id']}"):
                    name = new_rm_name.strip()
                    if name and name != rm["rm_name"]:
                        rename_rm(rm["_id"], name)
                        st.success(f"Renamed to: {name}")
                        st.rerun()
                if col3.button("Remove", key=f"btn_remove_{rm['_id']}"):
                    deactivate_rm(rm["_id"])
                    st.warning(f"Removed: {rm['rm_name']}")
                    st.rerun()
