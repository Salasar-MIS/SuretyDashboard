"""
Streamlit entry point.
Run with: streamlit run app/main.py
"""
import streamlit as st
from pages import branch_dashboard, naveen_aggarwal, summary
from utils.queries import get_branch_by_code, get_sub_branches

st.set_page_config(
    page_title="Surety Dashboard",
    page_icon="📊",
    layout="wide",
)

# Sub-branch codes under Naveen Aggarwal (in display order)
SUB_BRANCH_CODES = [
    "bangalore", "bhubaneswar", "guwahati", "hyderabad", "indore",
    "jamshedpur", "kanpur", "kolkata", "mayank_shukla", "nagpur",
    "raipur", "ranchi",
]

# ── Sidebar navigation ────────────────────────────────────────────────────────

with st.sidebar:
    st.title("📊 Surety Dashboard")
    st.divider()

    # Use session_state to track which page is active
    if "page" not in st.session_state:
        st.session_state.page = "summary"

    def nav(label, page_key, indent=False):
        prefix = "  " if indent else ""
        if st.button(f"{prefix}{label}", use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key

    nav("Summary", "summary")
    st.divider()
    nav("Delhi (NCR)", "ncr")
    nav("Ahmedabad", "ahmedabad")
    nav("Mumbai", "mumbai")
    st.divider()

    # Naveen Aggarwal section with expandable sub-branches
    nav("Naveen Aggarwal", "naveen_aggarwal")
    with st.expander("Sub-branches", expanded=False):
        naveen = get_branch_by_code("naveen_aggarwal")
        if naveen:
            sub_branches = get_sub_branches(naveen["_id"])
            for sb in sub_branches:
                nav(sb["branch_name"], sb["branch_code"], indent=True)

# ── Page routing ──────────────────────────────────────────────────────────────

page = st.session_state.page

if page == "summary":
    summary.render()

elif page == "naveen_aggarwal":
    naveen_aggarwal.render()

elif page in SUB_BRANCH_CODES:
    branch_dashboard.render(page)

elif page in ("ncr", "ahmedabad", "mumbai"):
    branch_dashboard.render(page)

else:
    st.error(f"Unknown page: {page}")
