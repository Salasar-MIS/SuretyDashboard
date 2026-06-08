"""Section 3 — Month Wise Proposal Conversions (data-entry)."""
import pandas as pd
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_proposals

MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]
_ABBR_TO_FULL = dict(zip(MONTH_ABBR, MONTHS))
# Flat column names: "APR (P)", "APR (C)", "MAY (P)", ...
_COLS = [f"{a} ({t})" for a in MONTH_ABBR for t in ("P", "C")]


def render_section_proposals(branch_id: ObjectId, fy: str, rms: list, proposals_data: dict):
    with st.container(border=True):
        st.markdown('<p class="section-label">Section 3</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Month Wise Proposal Conversions</p>',
                    unsafe_allow_html=True)
        st.caption("P = Proposals  |  C = Converted")

        if not rms:
            st.info("No active RMs for this branch.")
            return

        rows = {}
        for rm in rms:
            rm_prop = proposals_data.get(rm["_id"], {})
            row = {}
            for abbr, full in _ABBR_TO_FULL.items():
                md = rm_prop.get(full, {})
                row[f"{abbr} (P)"] = int(md.get("proposals", 0))
                row[f"{abbr} (C)"] = int(md.get("converted", 0))
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
                    new_p = int(edited_df.loc[rm_name, f"{abbr} (P)"])
                    new_c = int(edited_df.loc[rm_name, f"{abbr} (C)"])
                    old_p = int(original_df.loc[rm_name, f"{abbr} (P)"])
                    old_c = int(original_df.loc[rm_name, f"{abbr} (C)"])
                    if new_p != old_p or new_c != old_c:
                        upsert_proposals(rm_map[rm_name]["_id"], branch_id, fy,
                                         full, new_p, new_c)
            st.rerun()

        # Grand Total (read-only)
        totals = edited_df.sum().to_frame().T
        totals.index = ["GRAND TOTAL"]
        totals.index.name = "RM Name"
        st.dataframe(totals, use_container_width=True, hide_index=False)
