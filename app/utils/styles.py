"""
Global CSS injected on every page via st.markdown(GLOBAL_CSS, unsafe_allow_html=True).
Design language: clean light theme, dark sidebar, shadcn-inspired cards.
"""

GLOBAL_CSS = """
<style>

/* ── Reset & base ──────────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background-color: #F1F5F9;
}
[data-testid="stHeader"] {
    background-color: #F1F5F9;
    border-bottom: 1px solid #E2E8F0;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ── Sidebar — dark panel, never closeable ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0F172A !important;
    border-right: 1px solid #1E293B !important;
    min-width: 230px !important;
    max-width: 230px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}
[data-testid="stSidebar"] hr {
    border-color: #1E293B !important;
    margin: 6px 0 !important;
}
/* Sidebar nav buttons */
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: #94A3B8 !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 7px 14px !important;
    transition: background 0.15s, color 0.15s !important;
    width: 100% !important;
}
[data-testid="stSidebar"] button:hover {
    background: #1E293B !important;
    color: #F1F5F9 !important;
}
/* Hide sidebar collapse arrow — prevents accidental close */
[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* ── Page title ─────────────────────────────────────────────────────────────── */
h1 {
    color: #0F172A !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}
[data-testid="stCaptionContainer"] p {
    color: #64748B !important;
    font-size: 13px !important;
}

/* ── Section card wrapper ───────────────────────────────────────────────────── */
.section-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px 24px 24px 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06);
}
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 4px;
}
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #0F172A;
    margin-bottom: 16px;
}

/* ── Data editor ────────────────────────────────────────────────────────────── */
[data-testid="stDataEditor"] {
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
}

/* ── HTML dashboard tables (read-only sections) ─────────────────────────────── */
.dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    font-family: inherit;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #CBD5E1;
}
.dash-table thead tr.main-header th {
    background-color: #1E3A5F;
    color: #FFFFFF;
    font-weight: 700;
    padding: 9px 10px;
    text-align: center;
    border: 1px solid #2A4A7A;
    font-size: 12px;
    letter-spacing: 0.04em;
}
.dash-table thead tr.sub-header th {
    background-color: #2563EB;
    color: #FFFFFF;
    font-weight: 600;
    padding: 6px 8px;
    text-align: center;
    border: 1px solid #3B82F6;
    font-size: 11px;
    letter-spacing: 0.03em;
}
.dash-table tbody tr td {
    padding: 7px 10px;
    border: 1px solid #E2E8F0;
    text-align: right;
    color: #1E293B;
    white-space: nowrap;
}
.dash-table tbody tr td:first-child {
    text-align: left;
    font-weight: 500;
    color: #334155;
    min-width: 130px;
}
.dash-table tbody tr:nth-child(even) {
    background-color: #F8FAFC;
}
.dash-table tbody tr:hover {
    background-color: #EFF6FF;
}
.dash-table tfoot tr td {
    background-color: #1E3A5F;
    color: #FFFFFF;
    font-weight: 700;
    padding: 8px 10px;
    border: 1px solid #2A4A7A;
    text-align: right;
}
.dash-table tfoot tr td:first-child {
    text-align: left;
    color: #FFFFFF;
}

/* ── Divider ────────────────────────────────────────────────────────────────── */
hr {
    border-color: #E2E8F0 !important;
    margin: 4px 0 16px 0 !important;
}

/* ── Expander (Admin panel) ─────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
}

/* ── Buttons ────────────────────────────────────────────────────────────────── */
[data-testid="stMainBlockContainer"] button[kind="primary"] {
    background: #2563EB !important;
    border: none !important;
    border-radius: 6px !important;
    color: white !important;
    font-weight: 600 !important;
}
[data-testid="stMainBlockContainer"] button[kind="secondary"] {
    border-radius: 6px !important;
    border: 1px solid #E2E8F0 !important;
    font-weight: 500 !important;
}

/* ── Info / warning boxes ───────────────────────────────────────────────────── */
[data-testid="stInfo"] {
    background: #EFF6FF !important;
    border-left-color: #2563EB !important;
    border-radius: 6px !important;
}

</style>
"""
