"""Section 1 — Month Wise Branch Revenue (data-entry)."""
import pandas as pd
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_revenue

MONTH_ABBR = ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]
_ABBR_TO_FULL = dict(zip(MONTH_ABBR, MONTHS))


def render_section_revenue(branch_id: ObjectId, fy: str, rms: list, revenue_data: dict):
    with st.container(border=True):
        st.markdown('<p class="section-label">Section 1</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Month Wise Branch Revenue</p>', unsafe_allow_html=True)

        if not rms:
            st.info("No active RMs. Add RMs via the Admin panel below.")
            return

        # Build DataFrame: rows = RM names, cols = month abbreviations
        data = {
            rm["rm_name"]: {
                abbr: float(revenue_data.get(rm["_id"], {}).get(_ABBR_TO_FULL[abbr], 0.0))
                for abbr in MONTH_ABBR
            }
            for rm in rms
        }
        original_df = pd.DataFrame(data).T.astype(float)
        original_df.index.name = "RM Name"

        edited_df = st.data_editor(
            original_df,
            column_config={
                abbr: st.column_config.NumberColumn(abbr, min_value=0.0, step=0.01, format="%.2f")
                for abbr in MONTH_ABBR
            },
            use_container_width=True,
            num_rows="fixed",
            key=f"rev_{branch_id}_{fy}",
        )

        # Detect changes and persist
        if not edited_df.equals(original_df):
            rm_map = {rm["rm_name"]: rm for rm in rms}
            for rm_name in edited_df.index:
                for abbr in MONTH_ABBR:
                    new_val = float(edited_df.loc[rm_name, abbr])
                    old_val = float(original_df.loc[rm_name, abbr])
                    if abs(new_val - old_val) > 1e-9:
                        upsert_revenue(rm_map[rm_name]["_id"], branch_id, fy,
                                       _ABBR_TO_FULL[abbr], new_val)
            st.rerun()

        # Grand Total (read-only row)
        totals = edited_df.sum().to_frame().T
        totals["TOTAL"] = totals[list(MONTH_ABBR)].sum(axis=1)
        totals.index = ["GRAND TOTAL"]
        totals.index.name = "RM Name"
        st.dataframe(totals, use_container_width=True, hide_index=False)
