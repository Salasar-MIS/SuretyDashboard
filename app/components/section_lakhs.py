"""
Section 2 — Revenue in Lakhs (FY Target vs Achievement)
Target is editable per RM; Achievement is auto-computed and read-only.
"""
import pandas as pd
import streamlit as st
from bson import ObjectId
from ..utils.queries import MONTHS, upsert_target
from ..utils.transforms import branch_lakhs_table


def render_section_lakhs(branch_id: ObjectId, fy: str, rms: list,
                          revenue_data: dict, target_data: dict):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Section 2</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">Revenue in Lakhs — FY {fy}</p>', unsafe_allow_html=True)

    if not rms:
        st.info("No active RMs for this branch.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    rows = branch_lakhs_table(rms, revenue_data, target_data)
    data_rows = rows[:-1]   # RM rows only
    grand_row  = rows[-1]   # Grand Total

    # Build DataFrame with Target (editable) and Achievement (read-only)
    df = pd.DataFrame(
        [{"Target": r["target"], "Achievement": r["achievement"]} for r in data_rows],
        index=[r["rm_name"] for r in data_rows],
    ).astype(float)
    df.index.name = "RM Name"

    edited_df = st.data_editor(
        df,
        column_config={
            "Target":      st.column_config.NumberColumn("Target (₹ Lakhs)", min_value=0.0,
                                                          step=0.01, format="%.2f"),
            "Achievement": st.column_config.NumberColumn("Achievement (₹ Lakhs)", disabled=True,
                                                          format="%.2f"),
        },
        use_container_width=True,
        num_rows="fixed",
        key=f"lkh_{branch_id}_{fy}",
    )

    # Detect Target changes and save
    if not edited_df["Target"].equals(df["Target"]):
        rm_map = {rm["rm_name"]: rm for rm in rms}
        for rm_name in edited_df.index:
            new_t = float(edited_df.loc[rm_name, "Target"])
            old_t = float(df.loc[rm_name, "Target"])
            if abs(new_t - old_t) > 1e-9:
                upsert_target(rm_map[rm_name]["_id"], branch_id, fy, new_t)
        st.rerun()

    # Grand Total row (read-only)
    grand_df = pd.DataFrame(
        [{"Target": grand_row["target"], "Achievement": grand_row["achievement"]}],
        index=["GRAND TOTAL"],
    )
    grand_df.index.name = "RM Name"
    st.dataframe(grand_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
