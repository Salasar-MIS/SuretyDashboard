"""Naveen Aggarwal aggregation dashboard (read-only)."""
import streamlit as st
from ..utils.queries import (
    get_branch_by_code, get_sub_branches, get_rms,
    get_revenue_for_branch, get_targets_for_branch, get_proposals_for_branch,
    MONTHS,
)
from ..utils.transforms import branch_revenue_table, branch_lakhs_table, branch_proposals_table
from ..utils.styles import GLOBAL_CSS
from .summary import _section, _html_revenue, _html_lakhs, _html_proposals  # reuse builders

FY = "2026-27"


def render():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    naveen = get_branch_by_code("naveen_aggarwal")
    if not naveen:
        st.error("Naveen Aggarwal branch not found in database.")
        return

    sub_branches = get_sub_branches(naveen["_id"])
    st.title("Surety Dashboard — Naveen Aggarwal")
    st.caption(f"Financial Year {FY}  •  Aggregated from {len(sub_branches)} sub-branches  •  Read-only")

    if not sub_branches:
        st.info("No sub-branches found.")
        return

    rev_rows, lkh_rows, prop_rows = [], [], []
    for sb in sub_branches:
        rms  = get_rms(sb["_id"])
        rev  = get_revenue_for_branch(sb["_id"], FY)
        tgt  = get_targets_for_branch(sb["_id"], FY)
        prop = get_proposals_for_branch(sb["_id"], FY)
        r_gt = branch_revenue_table(rms, rev)[-1]
        l_gt = branch_lakhs_table(rms, rev, tgt)[-1]
        p_gt = branch_proposals_table(rms, prop)[-1]
        r_gt["rm_name"] = sb["branch_name"]
        l_gt["rm_name"] = sb["branch_name"]
        p_gt["rm_name"] = sb["branch_name"]
        rev_rows.append(r_gt); lkh_rows.append(l_gt); prop_rows.append(p_gt)

    st.markdown(_section("Section 1", "Month Wise Branch Revenue",
                         _html_revenue(rev_rows)), unsafe_allow_html=True)
    st.markdown(_section("Section 2", f"Revenue in Lakhs — FY {FY}",
                         _html_lakhs(lkh_rows)), unsafe_allow_html=True)
    st.markdown(_section("Section 3 &nbsp;<small style='font-weight:400;color:#6b7a99;font-size:11px'>P = Proposals | C = Converted</small>",
                         "Month Wise Proposal Conversions",
                         _html_proposals(prop_rows)), unsafe_allow_html=True)
