"""
Top-level Summary Dashboard (read-only).
Each section is one st.markdown call — no orphaned div white bars.
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
DISPLAY_NAMES   = {
    "naveen_aggarwal": "Naveen Aggarwal",
    "ncr":             "Delhi (NCR)",
    "ahmedabad":       "Ahmedabad",
    "mumbai":          "Mumbai",
}
MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]


# ── Data helpers ──────────────────────────────────────────────────────────────

def _naveen_grand_totals(fy):
    naveen = get_branch_by_code("naveen_aggarwal")
    if not naveen:
        rev = {m: 0.0 for m in MONTHS}; rev["total"] = 0.0
        prop = {f"{m}_p": 0 for m in MONTHS}; prop.update({f"{m}_c": 0 for m in MONTHS})
        return rev, {"target": 0.0, "achievement": 0.0}, prop
    rev_sum  = {m: 0.0 for m in MONTHS}; rev_sum["total"] = 0.0
    lkh_sum  = {"target": 0.0, "achievement": 0.0}
    prop_sum = {f"{m}_p": 0 for m in MONTHS}; prop_sum.update({f"{m}_c": 0 for m in MONTHS})
    for sb in get_sub_branches(naveen["_id"]):
        rms  = get_rms(sb["_id"])
        rev  = get_revenue_for_branch(sb["_id"], fy)
        tgt  = get_targets_for_branch(sb["_id"], fy)
        prop = get_proposals_for_branch(sb["_id"], fy)
        r_gt = branch_revenue_table(rms, rev)[-1]
        l_gt = branch_lakhs_table(rms, rev, tgt)[-1]
        p_gt = branch_proposals_table(rms, prop)[-1]
        for m in MONTHS:
            rev_sum[m] += r_gt.get(m, 0.0)
        rev_sum["total"] += r_gt.get("total", 0.0)
        lkh_sum["target"]      += l_gt["target"]
        lkh_sum["achievement"] += l_gt["achievement"]
        for m in MONTHS:
            prop_sum[f"{m}_p"] += p_gt.get(f"{m}_p", 0)
            prop_sum[f"{m}_c"] += p_gt.get(f"{m}_c", 0)
    return rev_sum, lkh_sum, prop_sum


def _branch_grand_totals(code, fy):
    branch = get_branch_by_code(code)
    if not branch:
        return {m: 0.0 for m in MONTHS}, {"target": 0.0, "achievement": 0.0}, {}
    rms  = get_rms(branch["_id"])
    rev  = get_revenue_for_branch(branch["_id"], fy)
    tgt  = get_targets_for_branch(branch["_id"], fy)
    prop = get_proposals_for_branch(branch["_id"], fy)
    return branch_revenue_table(rms, rev)[-1], \
           branch_lakhs_table(rms, rev, tgt)[-1], \
           branch_proposals_table(rms, prop)[-1]


# ── HTML builders ─────────────────────────────────────────────────────────────

def _fmt(v):  return f"{v:,.2f}"
def _fmti(v): return str(int(v))


def _section(label, title, table_html):
    """Wrap label + title + table in one card string."""
    return f"""
<div style="background:#fff;border:1px solid #dde3ef;border-radius:10px;
            padding:20px 22px;margin-bottom:18px;
            box-shadow:0 1px 4px rgba(23,41,98,0.07);">
  <p class="section-label">{label}</p>
  <p class="section-title">{title}</p>
  {table_html}
</div>"""


def _html_revenue(rows):
    hdrs = "".join(f"<th>{a}</th>" for a in MONTH_ABBR)
    html = f"""<table class="dash-table">
      <thead><tr class="main-header"><th>Name</th>{hdrs}<th>TOTAL</th></tr></thead>
      <tbody>"""
    grand = {m: 0.0 for m in MONTHS}; grand_t = 0.0
    for r in rows:
        cells = "".join(f"<td>{_fmt(r.get(m,0.0))}</td>" for m in MONTHS)
        tot   = r.get("total", 0.0)
        html += f"<tr><td>{r['rm_name']}</td>{cells}<td>{_fmt(tot)}</td></tr>"
        for m in MONTHS: grand[m] += r.get(m, 0.0)
        grand_t += tot
    gcells = "".join(f"<td>{_fmt(grand[m])}</td>" for m in MONTHS)
    html += f"</tbody><tfoot><tr><td>Grand Total</td>{gcells}<td>{_fmt(grand_t)}</td></tr></tfoot></table>"
    return html


def _html_lakhs(rows):
    html = """<table class="dash-table">
      <thead><tr class="main-header"><th>Name</th><th>Target (₹ Lakhs)</th><th>Achievement (₹ Lakhs)</th></tr></thead>
      <tbody>"""
    gt, ga = 0.0, 0.0
    for r in rows:
        html += f"<tr><td>{r['rm_name']}</td><td>{_fmt(r['target'])}</td><td>{_fmt(r['achievement'])}</td></tr>"
        gt += r["target"]; ga += r["achievement"]
    html += f"</tbody><tfoot><tr><td>Grand Total</td><td>{_fmt(gt)}</td><td>{_fmt(ga)}</td></tr></tfoot></table>"
    return html


def _html_proposals(rows):
    mhdr  = "".join(f'<th colspan="2">{a}</th>' for a in MONTH_ABBR)
    shdr  = "<th>P</th><th>C</th>" * 12
    html  = f"""<table class="dash-table">
      <thead>
        <tr class="main-header"><th rowspan="2">Name</th>{mhdr}</tr>
        <tr class="sub-header">{shdr}</tr>
      </thead><tbody>"""
    grand = {f"{m}_p": 0 for m in MONTHS}; grand.update({f"{m}_c": 0 for m in MONTHS})
    for r in rows:
        cells = "".join(
            f"<td>{_fmti(r.get(f'{m}_p',0))}</td><td>{_fmti(r.get(f'{m}_c',0))}</td>"
            for m in MONTHS)
        html += f"<tr><td>{r['rm_name']}</td>{cells}</tr>"
        for m in MONTHS:
            grand[f"{m}_p"] += r.get(f"{m}_p", 0)
            grand[f"{m}_c"] += r.get(f"{m}_c", 0)
    gcells = "".join(f"<td>{_fmti(grand[f'{m}_p'])}</td><td>{_fmti(grand[f'{m}_c'])}</td>" for m in MONTHS)
    html  += f"</tbody><tfoot><tr><td>Grand Total</td>{gcells}</tr></tfoot></table>"
    return html


# ── Render ────────────────────────────────────────────────────────────────────

def render():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.title("Surety Dashboard — Summary")
    st.caption(f"Financial Year {FY}  •  Read-only aggregated view")

    rev_rows, lkh_rows, prop_rows = [], [], []
    for code in TOP_LEVEL_CODES:
        r, l, p = _naveen_grand_totals(FY) if code == "naveen_aggarwal" \
                  else _branch_grand_totals(code, FY)
        name = DISPLAY_NAMES[code]
        r["rm_name"] = name; l["rm_name"] = name; p["rm_name"] = name
        rev_rows.append(r); lkh_rows.append(l); prop_rows.append(p)

    st.markdown(_section("Section 1", "Month Wise Branch Revenue",
                         _html_revenue(rev_rows)), unsafe_allow_html=True)
    st.markdown(_section("Section 2", f"Revenue in Lakhs — FY {FY}",
                         _html_lakhs(lkh_rows)), unsafe_allow_html=True)
    st.markdown(_section("Section 3 &nbsp;<small style='font-weight:400;color:#6b7a99;font-size:11px'>P = Proposals | C = Converted</small>",
                         "Month Wise Proposal Conversions",
                         _html_proposals(prop_rows)), unsafe_allow_html=True)
