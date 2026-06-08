"""
Top-level Summary Dashboard (read-only).
Uses HTML tables for pixel-perfect layout including Section 3 merged headers.
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

FY = "2026-27"
TOP_LEVEL_CODES = ["naveen_aggarwal", "ncr", "ahmedabad", "mumbai"]
DISPLAY_NAMES = {
    "naveen_aggarwal": "Naveen Aggarwal",
    "ncr":             "Delhi (NCR)",
    "ahmedabad":       "Ahmedabad",
    "mumbai":          "Mumbai",
}
MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]


def _naveen_grand_totals(fy):
    naveen = get_branch_by_code("naveen_aggarwal")
    if not naveen:
        rev  = {m: 0.0 for m in MONTHS}
        rev["total"] = 0.0
        lkh  = {"target": 0.0, "achievement": 0.0}
        prop = {f"{m}_p": 0 for m in MONTHS}
        prop.update({f"{m}_c": 0 for m in MONTHS})
        return rev, lkh, prop
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
    if not branch:
        return {m: 0.0 for m in MONTHS}, {"target": 0.0, "achievement": 0.0}, \
               {f"{m}_p": 0 for m in MONTHS}
    rms            = get_rms(branch["_id"])
    revenue_data   = get_revenue_for_branch(branch["_id"], fy)
    target_data    = get_targets_for_branch(branch["_id"], fy)
    proposals_data = get_proposals_for_branch(branch["_id"], fy)
    r_gt = branch_revenue_table(rms, revenue_data)[-1]
    l_gt = branch_lakhs_table(rms, revenue_data, target_data)[-1]
    p_gt = branch_proposals_table(rms, proposals_data)[-1]
    return r_gt, l_gt, p_gt


def _fmt(v): return f"{v:,.2f}"
def _fmti(v): return str(int(v))


def _html_revenue(rows):
    """Section 1 HTML table."""
    month_headers = "".join(f"<th>{a}</th>" for a in MONTH_ABBR)
    html = f"""
    <table class="dash-table">
      <thead>
        <tr class="main-header">
          <th>Name</th>{month_headers}<th>TOTAL</th>
        </tr>
      </thead>
      <tbody>"""
    grand = {m: 0.0 for m in MONTHS}
    grand_total = 0.0
    for row in rows:
        cells = "".join(f"<td>{_fmt(row.get(m, 0.0))}</td>" for m in MONTHS)
        total = row.get("total", 0.0)
        html += f"<tr><td>{row['rm_name']}</td>{cells}<td>{_fmt(total)}</td></tr>"
        for m in MONTHS:
            grand[m] += row.get(m, 0.0)
        grand_total += total
    grand_cells = "".join(f"<td>{_fmt(grand[m])}</td>" for m in MONTHS)
    html += f"""
      </tbody>
      <tfoot>
        <tr><td>Grand Total</td>{grand_cells}<td>{_fmt(grand_total)}</td></tr>
      </tfoot>
    </table>"""
    return html


def _html_lakhs(rows):
    """Section 2 HTML table."""
    html = """
    <table class="dash-table">
      <thead>
        <tr class="main-header">
          <th>Name</th><th>Target (₹ Lakhs)</th><th>Achievement (₹ Lakhs)</th>
        </tr>
      </thead>
      <tbody>"""
    grand_t, grand_a = 0.0, 0.0
    for row in rows:
        html += f"<tr><td>{row['rm_name']}</td><td>{_fmt(row['target'])}</td><td>{_fmt(row['achievement'])}</td></tr>"
        grand_t += row["target"]
        grand_a += row["achievement"]
    html += f"""
      </tbody>
      <tfoot>
        <tr><td>Grand Total</td><td>{_fmt(grand_t)}</td><td>{_fmt(grand_a)}</td></tr>
      </tfoot>
    </table>"""
    return html


def _html_proposals(rows):
    """Section 3 HTML table with merged month headers."""
    # Top header: Name (rowspan 2) + APR (colspan 2) + MAY (colspan 2) ...
    month_headers = "".join(f'<th colspan="2">{a}</th>' for a in MONTH_ABBR)
    sub_headers   = "<th>P</th><th>C</th>" * 12
    html = f"""
    <table class="dash-table">
      <thead>
        <tr class="main-header">
          <th rowspan="2">Name</th>{month_headers}
        </tr>
        <tr class="sub-header">
          {sub_headers}
        </tr>
      </thead>
      <tbody>"""
    grand = {f"{m}_p": 0 for m in MONTHS}
    grand.update({f"{m}_c": 0 for m in MONTHS})
    for row in rows:
        cells = "".join(
            f"<td>{_fmti(row.get(f'{m}_p', 0))}</td><td>{_fmti(row.get(f'{m}_c', 0))}</td>"
            for m in MONTHS
        )
        html += f"<tr><td>{row['rm_name']}</td>{cells}</tr>"
        for m in MONTHS:
            grand[f"{m}_p"] += row.get(f"{m}_p", 0)
            grand[f"{m}_c"] += row.get(f"{m}_c", 0)
    grand_cells = "".join(
        f"<td>{_fmti(grand[f'{m}_p'])}</td><td>{_fmti(grand[f'{m}_c'])}</td>"
        for m in MONTHS
    )
    html += f"""
      </tbody>
      <tfoot>
        <tr><td>Grand Total</td>{grand_cells}</tr>
      </tfoot>
    </table>"""
    return html


def render():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.title("Surety Dashboard — Summary")
    st.caption(f"Financial Year {FY}  •  Read-only aggregated view")

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
