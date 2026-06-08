"""
Top-level Summary Dashboard (read-only).
Aggregates Grand Total rows from NCR, Ahmedabad, Mumbai, and Naveen Aggarwal.
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

FY = "2026-27"

# Display order of top-level branches in Summary
TOP_LEVEL_CODES = ["naveen_aggarwal", "ncr", "ahmedabad", "mumbai"]
DISPLAY_NAMES = {
    "naveen_aggarwal": "Naveen Aggarwal",
    "ncr":             "Delhi (NCR)",
    "ahmedabad":       "Ahmedabad",
    "mumbai":          "Mumbai",
}


def _naveen_grand_totals(fy):
    """
    Naveen Aggarwal's Grand Total = sum of all 12 sub-branch Grand Totals.
    """
    naveen = get_branch_by_code("naveen_aggarwal")
    sub_branches = get_sub_branches(naveen["_id"])

    rev_sum  = {m: 0.0 for m in MONTHS}
    rev_sum["total"] = 0.0
    lkh_sum  = {"target": 0.0, "achievement": 0.0}
    prop_sum = {f"{m}_p": 0 for m in MONTHS}
    prop_sum.update({f"{m}_c": 0 for m in MONTHS})

    for sb in sub_branches:
        rms            = get_rms(sb["_id"])
        revenue_data   = get_revenue_for_branch(sb["_id"], fy)
        target_data    = get_targets_for_branch(sb["_id"], fy)
        proposals_data = get_proposals_for_branch(sb["_id"], fy)

        r_gt = branch_revenue_table(rms, revenue_data)[-1]
        l_gt = branch_lakhs_table(rms, revenue_data, target_data)[-1]
        p_gt = branch_proposals_table(rms, proposals_data)[-1]

        for m in MONTHS:
            rev_sum[m] += r_gt.get(m, 0.0)
        rev_sum["total"] += r_gt.get("total", 0.0)
        lkh_sum["target"]      += l_gt["target"]
        lkh_sum["achievement"] += l_gt["achievement"]
        for m in MONTHS:
            prop_sum[f"{m}_p"] += p_gt.get(f"{m}_p", 0)
            prop_sum[f"{m}_c"] += p_gt.get(f"{m}_c", 0)

    return rev_sum, lkh_sum, prop_sum


def _branch_grand_totals(branch_code, fy):
    branch = get_branch_by_code(branch_code)
    rms            = get_rms(branch["_id"])
    revenue_data   = get_revenue_for_branch(branch["_id"], fy)
    target_data    = get_targets_for_branch(branch["_id"], fy)
    proposals_data = get_proposals_for_branch(branch["_id"], fy)

    r_gt = branch_revenue_table(rms, revenue_data)[-1]
    l_gt = branch_lakhs_table(rms, revenue_data, target_data)[-1]
    p_gt = branch_proposals_table(rms, proposals_data)[-1]
    return r_gt, l_gt, p_gt


def render():
    st.title("Surety Dashboard — Summary")
    st.caption(f"FY {FY}")

    rev_rows, lkh_rows, prop_rows = [], [], []

    for code in TOP_LEVEL_CODES:
        if code == "naveen_aggarwal":
            r, l, p = _naveen_grand_totals(FY)
        else:
            r, l, p = _branch_grand_totals(code, FY)

        name = DISPLAY_NAMES[code]
        r["rm_name"] = name
        l["rm_name"] = name
        p["rm_name"] = name
        rev_rows.append(r)
        lkh_rows.append(l)
        prop_rows.append(p)

    # ── Section 1 ─────────────────────────────────────────────────────────────
    st.subheader("Section 1 — Month Wise Branch Revenue")
    _render_revenue_table(rev_rows)
    st.divider()

    # ── Section 2 ─────────────────────────────────────────────────────────────
    st.subheader(f"Section 2 — Revenue in Lakhs ({FY})")
    _render_lakhs_table(lkh_rows)
    st.divider()

    # ── Section 3 ─────────────────────────────────────────────────────────────
    st.subheader("Section 3 — Month Wise Proposal Conversions")
    _render_proposals_table(prop_rows)


def _render_revenue_table(rows):
    grand = {m: 0.0 for m in MONTHS}
    grand["total"] = 0.0

    header_cols = st.columns([2] + [1] * 12 + [1])
    for col, h in zip(header_cols, ["Name"] + MONTHS + ["Total"]):
        col.markdown(f"**{h}**")

    for row in rows:
        cols = st.columns([2] + [1] * 12 + [1])
        cols[0].write(row["rm_name"])
        for i, m in enumerate(MONTHS):
            v = row.get(m, 0.0)
            cols[i + 1].write(f"{v:,.2f}")
            grand[m] += v
        total = row.get("total", 0.0)
        cols[13].write(f"{total:,.2f}")
        grand["total"] += total

    cols = st.columns([2] + [1] * 12 + [1])
    cols[0].markdown("**Grand Total**")
    for i, m in enumerate(MONTHS):
        cols[i + 1].markdown(f"**{grand[m]:,.2f}**")
    cols[13].markdown(f"**{grand['total']:,.2f}**")


def _render_lakhs_table(rows):
    grand_t, grand_a = 0.0, 0.0
    cols = st.columns([3, 2, 2])
    for col, h in zip(cols, ["Name", "Target", "Achievement"]):
        col.markdown(f"**{h}**")

    for row in rows:
        cols = st.columns([3, 2, 2])
        cols[0].write(row["rm_name"])
        cols[1].write(f"{row['target']:,.2f}")
        cols[2].write(f"{row['achievement']:,.2f}")
        grand_t += row["target"]
        grand_a += row["achievement"]

    cols = st.columns([3, 2, 2])
    cols[0].markdown("**Grand Total**")
    cols[1].markdown(f"**{grand_t:,.2f}**")
    cols[2].markdown(f"**{grand_a:,.2f}**")


def _render_proposals_table(rows):
    grand = {f"{m}_p": 0 for m in MONTHS}
    grand.update({f"{m}_c": 0 for m in MONTHS})

    header_cols = st.columns([2] + [1, 1] * 12)
    header_cols[0].markdown("**Name**")
    for i, m in enumerate(MONTHS):
        header_cols[1 + i * 2].markdown(f"**{m}**")

    sub_cols = st.columns([2] + [1, 1] * 12)
    sub_cols[0].write("")
    for i in range(12):
        sub_cols[1 + i * 2].markdown("*Prop.*")
        sub_cols[2 + i * 2].markdown("*Conv.*")

    for row in rows:
        cols = st.columns([2] + [1, 1] * 12)
        cols[0].write(row["rm_name"])
        for i, m in enumerate(MONTHS):
            p = row.get(f"{m}_p", 0)
            c = row.get(f"{m}_c", 0)
            cols[1 + i * 2].write(p)
            cols[2 + i * 2].write(c)
            grand[f"{m}_p"] += p
            grand[f"{m}_c"] += c

    cols = st.columns([2] + [1, 1] * 12)
    cols[0].markdown("**Grand Total**")
    for i, m in enumerate(MONTHS):
        cols[1 + i * 2].markdown(f"**{grand[f'{m}_p']}**")
        cols[2 + i * 2].markdown(f"**{grand[f'{m}_c']}**")
