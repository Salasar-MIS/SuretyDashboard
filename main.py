"""
Streamlit Cloud entry point — root main.py
"""
import streamlit as st
from app.pages import branch_dashboard, naveen_aggarwal, summary
from app.utils.queries import get_branch_by_code, get_sub_branches
from app.utils.db import get_db
from app.utils.styles import GLOBAL_CSS

st.set_page_config(
    page_title="Surety Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global CSS on every load
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

SUB_BRANCH_CODES = [
    "bangalore", "bhubaneswar", "guwahati", "hyderabad", "indore",
    "jamshedpur", "kanpur", "kolkata", "mayank_shukla", "nagpur",
    "raipur", "ranchi",
]

# Auto-seed the database on first boot if branches collection is empty
@st.cache_resource
def _ensure_seeded():
    if get_db()["branches"].count_documents({}) == 0:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from seed import seed
        seed()

_ensure_seeded()

# ── Sidebar navigation ────────────────────────────────────────────────────────

LOGO_URL = "https://www.salasarservices.com/assets/Frontend/images/Salasar-New-Logo.png"

with st.sidebar:
    # Logo on a white panel so it stays visible over the navy gradient
    st.markdown(
        f"""
        <div style="background:#ffffff;border-radius:10px;padding:14px 16px;
                    margin:0 0 10px 0;text-align:center;
                    box-shadow:0 1px 4px rgba(0,0,0,0.15);">
            <img src="{LOGO_URL}" style="width:100%;min-width:200px;height:auto;" />
        </div>
        <p style="text-align:center;color:#a6ce39 !important;font-size:12px;
                  font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                  margin:0 0 8px 0;">Surety Dashboard</p>
        """,
        unsafe_allow_html=True,
    )
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
            for sb in get_sub_branches(naveen["_id"]):
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
