"""
Section 3 — Month Wise Proposal Conversions
Uses st.data_editor with "APR (P)" / "APR (C)" column naming.
Grand Total shown as read-only dataframe below.
"""
import pandas as pd
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_proposals

MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]
_ABBR_TO_FULL = dict(zip(MONTH_ABBR, MONTHS))

# Flat column names for data_editor: "APR (P)", "APR (C)", ...
_COLS = [f"{a} ({t})" for a in MONTH_ABBR for t in ("P", "C")]


def render_section_proposals(branch_id: ObjectId, fy: str, rms: list, proposals_data: dict):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Section 3</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Month Wise Proposal Conversions</p>', unsafe_allow_html=True)
    st.caption("P = Proposals &nbsp;|&nbsp; C = Converted")

    if not rms:
        st.info("No active RMs for this branch.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Build DataFrame: one column per (month, type) pair
    rows = {}
    for rm in rms:
        rm_prop = proposals_data.get(rm["_id"], {})
        row = {}
        for abbr, full in _ABBR_TO_FULL.items():
            month_data = rm_prop.get(full, {})
            row[f"{abbr} (P)"] = int(month_data.get("proposals", 0))
            row[f"{abbr} (C)"] = int(month_data.get("converted", 0))
        rows[rm["rm_name"]] = row

    original_df = pd.DataFrame(rows).T[_COLS].astype(int)
    original_df.index.name = "RM Name"

    edited_df = st.data_editor(
        original_df,
        column_config={
            col: st.column_config.NumberColumn(col, min_value=0, step=1, format="%d")
            for col in _COLS
        },
        use_container_width=True,
        num_rows="fixed",
        key=f"prop_{branch_id}_{fy}",
    )

    # Detect changes and persist
    if not edited_df.equals(original_df):
        rm_map = {rm["rm_name"]: rm for rm in rms}
        for rm_name in edited_df.index:
            for abbr, full in _ABBR_TO_FULL.items():
                p_col = f"{abbr} (P)"
                c_col = f"{abbr} (C)"
                new_p = int(edited_df.loc[rm_name, p_col])
                new_c = int(edited_df.loc[rm_name, c_col])
                old_p = int(original_df.loc[rm_name, p_col])
                old_c = int(original_df.loc[rm_name, c_col])
                if new_p != old_p or new_c != old_c:
                    upsert_proposals(rm_map[rm_name]["_id"], branch_id, fy,
                                     full, new_p, new_c)
        st.rerun()

    # Grand Total row (read-only)
    totals = edited_df.sum().to_frame().T
    totals.index = ["GRAND TOTAL"]
    totals.index.name = "RM Name"
    st.dataframe(totals, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
