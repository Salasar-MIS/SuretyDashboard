"""
Section 1 — Month Wise Branch Revenue
Renders the editable revenue table for a single branch dashboard.
"""
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_revenue
from ..utils.transforms import branch_revenue_table


def render_section_revenue(branch_id: ObjectId, fy: str, rms: list, revenue_data: dict):
    """
    Display Section 1. Shows an editable number input per RM per month.
    Saves each value immediately on change via upsert_revenue().
    """
    st.subheader("Section 1 — Month Wise Branch Revenue")

    if not rms:
        st.info("No active RMs for this branch. Add RMs via the Admin panel.")
        return

    rows = branch_revenue_table(rms, revenue_data)
    # Separate data rows from Grand Total
    data_rows = rows[:-1]
    grand_total = rows[-1]

    # Build a column layout: Name + 12 months + Total
    cols = st.columns([2] + [1] * 12 + [1])
    headers = ["Name"] + MONTHS + ["Total"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    # Editable rows
    for row in data_rows:
        cols = st.columns([2] + [1] * 12 + [1])
        cols[0].write(row["rm_name"])
        row_total = 0.0
        for i, month in enumerate(MONTHS):
            val = cols[i + 1].number_input(
                label=f"{row['rm_name']}_{month}",
                value=float(row.get(month, 0.0)),
                min_value=0.0,
                step=0.01,
                label_visibility="collapsed",
                key=f"rev_{branch_id}_{row['rm_id']}_{month}",
            )
            # Persist if value changed
            if val != row.get(month, 0.0):
                upsert_revenue(row["rm_id"], branch_id, fy, month, val)
                st.rerun()
            row_total += val
        cols[13].write(f"{row_total:,.2f}")

    # Grand Total row (read-only)
    cols = st.columns([2] + [1] * 12 + [1])
    cols[0].markdown("**Grand Total**")
    for i, month in enumerate(MONTHS):
        cols[i + 1].markdown(f"**{grand_total.get(month, 0.0):,.2f}**")
    cols[13].markdown(f"**{grand_total['total']:,.2f}**")
