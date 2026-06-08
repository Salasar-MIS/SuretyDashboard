"""
Section 3 — Month Wise Proposal Conversions
Renders editable Proposals and Converted counts per RM per month.
"""
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_proposals
from ..utils.transforms import branch_proposals_table


def render_section_proposals(branch_id: ObjectId, fy: str, rms: list, proposals_data: dict):
    """
    Display Section 3.
    Both Proposals and Converted are editable per RM per month.
    """
    st.subheader("Section 3 — Month Wise Proposal Conversions")

    if not rms:
        st.info("No active RMs for this branch.")
        return

    rows = branch_proposals_table(rms, proposals_data)
    data_rows = rows[:-1]
    grand_total = rows[-1]

    # Header row — Name + pairs per month
    header_cols = st.columns([2] + [1, 1] * 12)
    header_cols[0].markdown("**Name**")
    for i, month in enumerate(MONTHS):
        header_cols[1 + i * 2].markdown(f"**{month}**")
        header_cols[2 + i * 2].markdown("")

    # Sub-header row
    sub_cols = st.columns([2] + [1, 1] * 12)
    sub_cols[0].write("")
    for i in range(12):
        sub_cols[1 + i * 2].markdown("*Prop.*")
        sub_cols[2 + i * 2].markdown("*Conv.*")

    # Editable data rows
    for row in data_rows:
        cols = st.columns([2] + [1, 1] * 12)
        cols[0].write(row["rm_name"])
        for i, month in enumerate(MONTHS):
            p_key = f"prop_{branch_id}_{row['rm_id']}_{month}"
            c_key = f"conv_{branch_id}_{row['rm_id']}_{month}"
            new_p = cols[1 + i * 2].number_input(
                label=p_key, value=int(row.get(f"{month}_p", 0)),
                min_value=0, step=1, label_visibility="collapsed", key=p_key,
            )
            new_c = cols[2 + i * 2].number_input(
                label=c_key, value=int(row.get(f"{month}_c", 0)),
                min_value=0, step=1, label_visibility="collapsed", key=c_key,
            )
            if new_p != row.get(f"{month}_p", 0) or new_c != row.get(f"{month}_c", 0):
                upsert_proposals(row["rm_id"], branch_id, fy, month, new_p, new_c)
                st.rerun()

    # Grand Total row (read-only)
    cols = st.columns([2] + [1, 1] * 12)
    cols[0].markdown("**Grand Total**")
    for i, month in enumerate(MONTHS):
        cols[1 + i * 2].markdown(f"**{grand_total.get(f'{month}_p', 0)}**")
        cols[2 + i * 2].markdown(f"**{grand_total.get(f'{month}_c', 0)}**")
