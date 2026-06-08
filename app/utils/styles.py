"""
Global CSS — Salasar brand colours + clean light dashboard.
Primary:  #2d448d  (deep blue)
Accent:   #a6ce39  (lime green)
Dark:     #172962  (navy)
Hover:    #459fda  (sky blue)
"""

GLOBAL_CSS = """
<style>

/* ── Base & background ─────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #f0f4f8 !important;
}
[data-testid="stHeader"] {
    background-color: #f0f4f8 !important;
    border-bottom: 1px solid #dde3ef !important;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* ── Sidebar ────────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172962 0%, #2d448d 100%) !important;
    min-width: 250px !important;
    max-width: 250px !important;
    border-right: none !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #c8d6f5 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
    margin: 6px 0 !important;
}
/* Nav buttons */
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: #c8d6f5 !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 7px 14px !important;
    transition: background 0.15s, color 0.15s !important;
    width: 100% !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(166,206,57,0.18) !important;
    color: #a6ce39 !important;
}
/* ── Hide collapse / close arrow — all known selectors ────────────────────── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
section[data-testid="stSidebar"] > div > button,
section[data-testid="stSidebar"] > div > div > button,
button[title="Close sidebar"],
button[title="collapse sidebar"],
button[aria-label="Close sidebar"],
button[aria-label="collapse sidebar"],
[class*="collapseSidebar"],
[class*="CloseSidebar"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ── Page headings ──────────────────────────────────────────────────────────── */
h1 {
    color: #172962 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    border-left: 4px solid #a6ce39;
    padding-left: 12px;
}
[data-testid="stCaptionContainer"] p {
    color: #6b7a99 !important;
    font-size: 12.5px !important;
}

/* ── Section labels (SECTION 1 / 2 / 3) ─────────────────────────────────── */
.section-label {
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a6ce39;
    margin: 0 0 3px 0;
}
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: #172962;
    margin: 0 0 14px 0;
}

/* ── st.container(border=True) — section cards ──────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #dde3ef !important;
    border-radius: 10px !important;
    padding: 6px 8px !important;
    box-shadow: 0 1px 4px rgba(23,41,98,0.07) !important;
    margin-bottom: 16px !important;
}

/* ── st.data_editor ──────────────────────────────────────────────────────── */
[data-testid="stDataEditor"] {
    border-radius: 7px !important;
    overflow: hidden !important;
    border: 1px solid #dde3ef !important;
}

/* ── st.dataframe (grand total rows) ────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 7px !important;
    overflow: hidden !important;
}

/* ── HTML dashboard tables ──────────────────────────────────────────────── */
.dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    font-family: inherit;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #c9d2e8;
}
.dash-table thead tr.main-header th {
    background-color: #2d448d;
    color: #ffffff;
    font-weight: 700;
    padding: 9px 10px;
    text-align: center;
    border: 1px solid #3a56a8;
    font-size: 11.5px;
    letter-spacing: 0.05em;
    white-space: nowrap;
}
.dash-table thead tr.sub-header th {
    background-color: #172962;
    color: #c8d6f5;
    font-weight: 600;
    padding: 5px 8px;
    text-align: center;
    border: 1px solid #1e3580;
    font-size: 11px;
    letter-spacing: 0.03em;
}
.dash-table tbody tr td {
    padding: 7px 10px;
    border: 1px solid #e4eaf5;
    text-align: right;
    color: #263354;
    white-space: nowrap;
}
.dash-table tbody tr td:first-child {
    text-align: left;
    font-weight: 600;
    color: #172962;
    min-width: 130px;
}
.dash-table tbody tr:nth-child(even) {
    background-color: #f5f7fc;
}
.dash-table tbody tr:hover {
    background-color: #edf1fb;
}
.dash-table tfoot tr td {
    background-color: #172962;
    color: #a6ce39;
    font-weight: 700;
    padding: 8px 10px;
    border: 1px solid #1e3580;
    text-align: right;
    white-space: nowrap;
}
.dash-table tfoot tr td:first-child {
    text-align: left;
    color: #ffffff;
}

/* ── Dividers ──────────────────────────────────────────────────────────────── */
hr {
    border-color: #dde3ef !important;
    margin: 4px 0 14px 0 !important;
}

/* ── Expander (Admin) ──────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #dde3ef !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* ── Buttons (main content) ────────────────────────────────────────────────── */
[data-testid="stMainBlockContainer"] button[kind="primary"] {
    background: #2d448d !important;
    border: none !important;
    border-radius: 6px !important;
    color: white !important;
    font-weight: 700 !important;
    transition: background 0.15s !important;
}
[data-testid="stMainBlockContainer"] button[kind="primary"]:hover {
    background: #172962 !important;
}

/* ── Info box ──────────────────────────────────────────────────────────────── */
[data-testid="stInfo"] {
    background: #eef3fc !important;
    border-left-color: #2d448d !important;
    border-radius: 6px !important;
}

</style>
"""
