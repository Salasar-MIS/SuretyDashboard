"""
Section 2 — Revenue in Lakhs (FY Target vs Achievement)
Renders editable Target per RM; Achievement is auto-computed.
"""
import streamlit as st
from bson import ObjectId
from ..utils.queries import upsert_target
from ..utils.transforms import branch_lakhs_table


def render_section_lakhs(branch_id: ObjectId, fy: str, rms: list,
                          revenue_data: dict, target_data: dict):
    """
    Display Section 2.
    Target is editable per RM; Achievement = sum of 12 months (read-only).
    """
    st.subheader(f"Section 2 — Revenue in Lakhs ({fy})")

    if not rms:
        st.info("No active RMs for this branch.")
        return

    rows = branch_lakhs_table(rms, revenue_data, target_data)
    data_rows = rows[:-1]
    grand_total = rows[-1]

    cols = st.columns([3, 2, 2])
    cols[0].markdown("**Name**")
    cols[1].markdown("**Target**")
    cols[2].markdown("**Achievement**")

    for row in data_rows:
        cols = st.columns([3, 2, 2])
        cols[0].write(row["rm_name"])
        new_target = cols[1].number_input(
            label=f"target_{row['rm_id']}",
            value=float(row["target"]),
            min_value=0.0,
            step=0.01,
            label_visibility="collapsed",
            key=f"tgt_{branch_id}_{row['rm_id']}",
        )
        if new_target != row["target"]:
            upsert_target(row["rm_id"], branch_id, fy, new_target)
            st.rerun()
        cols[2].write(f"{row['achievement']:,.2f}")

    # Grand Total row (read-only)
    cols = st.columns([3, 2, 2])
    cols[0].markdown("**Grand Total**")
    cols[1].markdown(f"**{grand_total['target']:,.2f}**")
    cols[2].markdown(f"**{grand_total['achievement']:,.2f}**")
