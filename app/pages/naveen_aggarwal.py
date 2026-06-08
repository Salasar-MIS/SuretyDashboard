"""
Naveen Aggarwal aggregation dashboard (read-only).
Uses the same HTML table helpers as summary.py.
"""
import streamlit as st
from ..utils.queries import (
    get_branch_by_code, get_sub_branches, get_rms,
    get_revenue_for_branch, get_targets_for_branch, get_proposals_for_branch,
    MONTHS,
)
from ..utils.transforms import (
    branch_revenue_table, branch_lakhs_table, branch_proposals_table,
)
from ..utils.styles import GLOBAL_CSS
from .summary import _html_revenue, _html_lakhs, _html_proposals   # reuse helpers

FY = "2026-27"
MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]


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
        rms            = get_rms(sb["_id"])
        revenue_data   = get_revenue_for_branch(sb["_id"], FY)
        target_data    = get_targets_for_branch(sb["_id"], FY)
        proposals_data = get_proposals_for_branch(sb["_id"], FY)

        r_gt = branch_revenue_table(rms, revenue_data)[-1]
        l_gt = branch_lakhs_table(rms, revenue_data, target_data)[-1]
        p_gt = branch_proposals_table(rms, proposals_data)[-1]

        r_gt["rm_name"] = sb["branch_name"]
        l_gt["rm_name"] = sb["branch_name"]
        p_gt["rm_name"] = sb["branch_name"]
        rev_rows.append(r_gt)
        lkh_rows.append(l_gt)
        prop_rows.append(p_gt)

    # ── Section 1 ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Section 1</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Month Wise Branch Revenue</p>', unsafe_allow_html=True)
    st.markdown(_html_revenue(rev_rows), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 2 ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Section 2</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Revenue in Lakhs — FY {FY}</p>', unsafe_allow_html=True)
    st.markdown(_html_lakhs(lkh_rows), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 3 ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Section 3</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Month Wise Proposal Conversions</p>', unsafe_allow_html=True)
    st.caption("P = Proposals &nbsp;|&nbsp; C = Converted")
    st.markdown(_html_proposals(prop_rows), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
