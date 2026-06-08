"""
Streamlit Cloud entry point — root main.py
Streamlit Cloud runs this file directly from the repo root.
"""
import streamlit as st
from app.pages import branch_dashboard, naveen_aggarwal, summary
from app.utils.queries import get_branch_by_code, get_sub_branches
from app.utils.db import get_db

# Auto-seed the database on first boot if branches collection is empty
@st.cache_resource
def _ensure_seeded():
    if get_db()["branches"].count_documents({}) == 0:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from seed import seed
        seed()

_ensure_seeded()

st.set_page_config(
    page_title="Surety Dashboard",
    page_icon="📊",
    layout="wide",
)

SUB_BRANCH_CODES = [
    "bangalore", "bhubaneswar", "guwahati", "hyderabad", "indore",
    "jamshedpur", "kanpur", "kolkata", "mayank_shukla", "nagpur",
    "raipur", "ranchi",
]

# ── Sidebar navigation ────────────────────────────────────────────────────────

with st.sidebar:
    st.title("📊 Surety Dashboard")
    st.divider()

    if "page" not in st.session_state:
        st.session_state.page = "summary"

    def nav(label, page_key, indent=False):
        prefix = "　" if indent else ""
        if st.button(f"{prefix}{label}", use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key

    nav("Summary", "summary")
    st.divider()
    nav("Delhi (NCR)", "ncr")
    nav("Ahmedabad", "ahmedabad")
    nav("Mumbai", "mumbai")
    st.divider()

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
elif page in SUB_BRANCH_CODES or page in ("ncr", "ahmedabad", "mumbai"):
    branch_dashboard.render(page)
else:
    st.error(f"Unknown page: {page}")
