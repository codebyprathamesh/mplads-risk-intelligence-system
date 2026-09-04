# =========================================================
# MPLADS RISK INTELLIGENCE SYSTEM — AUDIT & CASE-FILE REGISTER
# =========================================================
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import html

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_OK = True
except Exception:
    PLOTLY_OK = False

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MPLADS Risk Intelligence System",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. CONSOLIDATED AUDIT LEDGER CSS & TYPOGRAPHY
# =========================================================
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">

<style>
/* Root Design Tokens: Paper, Ink, Hairline & Semantic Risk Scale */
:root {
    --paper-bg: #FAFAF7;
    --paper-card: #FFFFFF;
    --paper-panel: #F4F3EE;
    --paper-hover: #ECEAE3;
    --hairline: #DDDAD2;
    --hairline-light: #EBE8E1;
    --ink-primary: #1A1A1A;
    --ink-secondary: #4A4F58; /* High-contrast readable dark gray */
    --ink-muted: #4A4F58;     /* Unified readable secondary gray floor */
    
    /* Semantic Risk Scale (The ONLY accents in the entire system for risk tiers) */
    --risk-none: #6B7280;
    --risk-low: #4B7A5E;
    --risk-medium: #9C6B2E;
    --risk-high: #B0522D;
    --risk-critical: #8B2E22;

    /* Non-Risk Categorical Accent Family */
    --accent-teal: #2B6B6B;
    --accent-teal-light: #6B9C9C;
}

/* Global Reset & Base Typography */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--ink-primary);
    font-size: 14px;
}

.stApp {
    background-color: var(--paper-bg) !important;
    color: var(--ink-primary) !important;
}

/* Streamlit Chrome Suppression */
#MainMenu { visibility: hidden !important; display: none !important; }
footer { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { display: none !important; height: 0px !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }

/* Main Container Layout */
.block-container {
    padding-top: 2.2rem !important;
    padding-bottom: 4.5rem !important;
    max-width: 1480px !important;
}

/* Headings: Source Serif 4 (Official Gazette / Register Heading) */
h1, h2, h3, h4, .serif-title, .section-head {
    font-family: 'Source Serif 4', Georgia, 'Times New Roman', serif !important;
    font-weight: 600 !important;
    color: var(--ink-primary) !important;
    letter-spacing: -0.01em !important;
}

.section-head {
    font-size: 20px !important;
    margin: 34px 0 7px 0 !important;
    padding-bottom: 5px;
    border-bottom: 1px solid var(--hairline-light);
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
    line-height: 1.35 !important;
}

.section-desc {
    font-size: 13.5px !important;
    color: var(--ink-secondary) !important;
    margin-bottom: 12px !important;
    line-height: 1.4;
    white-space: normal !important;
    word-break: normal !important;
}

/* Monospace Authority: Numbers, IDs, Amounts, Dates & Traceable Codes */
.mono, .mono-val, .ledger-code,
[data-testid="stMetricValue"],
div[data-testid="stDataFrame"] table,
div[data-testid="stDataFrame"] td,
div[data-testid="stDataFrame"] th {
    font-family: 'IBM Plex Mono', 'JetBrains Mono', Courier, monospace !important;
}

/* Official Page Header Banner */
.page-header {
    border-bottom: 1px solid var(--hairline);
    padding-bottom: 14px;
    margin-bottom: 20px;
}

.page-title {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 24px;
    font-weight: 600;
    color: var(--ink-primary);
    margin: 0;
    line-height: 1.25;
}

.page-desc {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--ink-secondary);
    margin-top: 5px;
    margin-bottom: 8px;
    line-height: 1.4;
}

/* Stacked Key-Value Metadata Block */
.header-meta-block {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-top: 9px;
    padding-top: 9px;
    border-top: 1px dotted var(--hairline-light);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--ink-secondary);
    line-height: 1.45;
}

.header-meta-row {
    display: flex;
    gap: 8px;
}

.header-meta-key {
    color: var(--ink-secondary);
    font-weight: 500;
}

.header-meta-val {
    color: var(--ink-primary);
    font-weight: 600;
}

.header-callout-line {
    margin-top: 8px;
    padding-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13.5px;
    font-weight: 500;
    color: var(--ink-secondary);
    letter-spacing: 0;
    border-top: 1px dotted var(--hairline-light);
}

.header-callout-line b {
    color: var(--ink-primary);
}

/* Horizontal Stacked Risk Bar Component — No card wrapper, bare bar + single legend row */
.stacked-risk-bar {
    display: flex;
    width: 100%;
    height: 16px;
    border: 1px solid var(--hairline);
    overflow: hidden;
    margin: 0 0 8px 0;
}

.stacked-risk-legend-row {
    display: flex;
    flex-direction: row;
    gap: 20px;
    flex-wrap: nowrap;
    margin-bottom: 18px;
}

.stacked-risk-legend-cell {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--ink-secondary);
    white-space: nowrap;
}

.stacked-risk-sq {
    width: 10px;
    height: 10px;
    flex-shrink: 0;
}

.stacked-risk-lbl {
    font-weight: 500;
}

.stacked-risk-cnt {
    font-weight: 700;
    color: var(--ink-primary);
}

/* Sidebar: force the panel open/visible; simple clickable navigation */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
    transform: translateX(0) !important;
}

section[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebar"] > div:first-child {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] .sidebar-nav-label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--ink-secondary) !important;
    margin: 0 0 8px 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stButton"] {
    margin: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stButton"] > button {
    width: 100% !important;
    min-height: 42px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 9px 12px !important;
    margin: 0 !important;
    border: 0 !important;
    border-bottom: 1px solid var(--hairline-light) !important;
    border-radius: 0 !important;
    background: transparent !important;
    color: var(--ink-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: var(--paper-hover) !important;
    color: var(--ink-primary) !important;
    border-color: var(--hairline-light) !important;
}

section[data-testid="stSidebar"] [data-testid="stButton"] > button:focus,
section[data-testid="stSidebar"] [data-testid="stButton"] > button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .sidebar-nav-active > button {
    background: #E8E6DF !important;
    color: var(--ink-primary) !important;
    font-weight: 650 !important;
    border-left: 3px solid var(--ink-primary) !important;
    padding-left: 9px !important;
}

/* Summary cards used across operational pages */
.ledger-summary-strip {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin: 8px 0 30px 0;
}

.ledger-cell {
    position: relative;
    padding: 18px 18px 16px 20px;
    border: 1px solid var(--hairline);
    border-radius: 8px;
    background: var(--paper-card);
    min-height: 122px;
}

.ledger-cell-label {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    font-weight: 650;
    color: var(--ink-secondary);
    letter-spacing: 0.035em;
    text-transform: uppercase;
    line-height: 1.35;
}

.ledger-cell-val {
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--ink-primary);
    margin-top: 8px;
    letter-spacing: -0.025em;
    line-height: 1.05;
}

.ledger-cell-sub {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--ink-secondary);
    margin-top: 8px;
    line-height: 1.35;
}

.ledger-cell.tone-critical { border-left: 4px solid var(--risk-critical); }
.ledger-cell.tone-critical .ledger-cell-val { color: var(--risk-critical); }
.ledger-cell.tone-high { border-left: 4px solid var(--risk-high); }
.ledger-cell.tone-high .ledger-cell-val { color: var(--risk-high); }
.ledger-cell.tone-medium { border-left: 4px solid var(--risk-medium); }
.ledger-cell.tone-medium .ledger-cell-val { color: var(--risk-medium); }
.ledger-cell.tone-low { border-left: 4px solid var(--risk-low); }
.ledger-cell.tone-low .ledger-cell-val { color: var(--risk-low); }
.ledger-cell.tone-neutral { border-left: 4px solid var(--accent-teal-light); }
.ledger-cell.tone-neutral .ledger-cell-val { color: var(--accent-teal); }

@media (max-width: 1050px) {
    .ledger-summary-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 640px) {
    .ledger-summary-strip { grid-template-columns: 1fr; }
}


/* Dashboard Flash Cards — quiet hierarchy, minimal ornament */
.dashboard-cards {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin: 6px 0 40px 0;
}
.dashboard-card {
    position: relative;
    background: var(--paper-card);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    padding: 20px 22px 18px 22px;
    min-height: 128px;
    box-sizing: border-box;
}
.dashboard-card:hover { border-color: #C8C4BA; }
.dashboard-card.tone-neutral { border-left: 1px solid var(--hairline); }
.dashboard-card.tone-neutral .dashboard-card-value { color: var(--ink-primary); }
.dashboard-card.tone-critical { border-left: 4px solid var(--risk-critical); }
.dashboard-card.tone-critical .dashboard-card-value { color: var(--risk-critical); }
.dashboard-card.tone-medium { border-left: 4px solid var(--risk-medium); }
.dashboard-card.tone-medium .dashboard-card-value { color: var(--risk-medium); }
.dashboard-card.tone-high { border-left: 4px solid var(--risk-high); }
.dashboard-card.tone-high .dashboard-card-value { color: var(--risk-high); }
.dashboard-card-kicker {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 650;
    color: var(--ink-secondary);
    letter-spacing: 0.055em;
    text-transform: uppercase;
    margin-bottom: 11px;
}
.dashboard-card-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    line-height: 1;
    font-weight: 700;
    color: var(--ink-primary);
    letter-spacing: -0.03em;
}
.dashboard-card-sub {
    margin-top: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--ink-secondary);
    line-height: 1.4;
}

/* Plotly content sits on the page itself; section headings provide the hierarchy. */
div[data-testid="stPlotlyChart"] {
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    box-sizing: border-box;
}
@media (max-width: 900px) {
    .dashboard-cards { grid-template-columns: 1fr; }
}

/* Graph presentation: clean containers without artificial 'AI dashboard' decoration */
div[data-testid="stPlotlyChart"] {
    background: var(--paper-card);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    padding: 2px 2px 0 2px;
    box-sizing: border-box;
}

/* Sidebar Telemetry Block */

/* Tables: Hairline borders, sharp 0px corners, no shadows */
[data-testid="stDataFrame"] {
    border: 1px solid var(--hairline) !important;
    border-radius: 0px !important;
    box-shadow: none !important;
    background: var(--paper-card) !important;
}

/* Native Metrics Overrides */
[data-testid="stMetric"] {
    border: 1px solid var(--hairline) !important;
    border-radius: 0px !important;
    box-shadow: none !important;
    background: var(--paper-card) !important;
    padding: 12px 16px !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--ink-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: var(--ink-primary) !important;
}

/* Filters & Inputs: High Contrast Labels & Clean Type */
.stSelectbox label, .stMultiSelect label, .stTextInput label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: var(--ink-secondary) !important;
}

.stTextInput input, .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
    border-radius: 0px !important;
    border: 1px solid var(--hairline) !important;
    background-color: var(--paper-card) !important;
    color: var(--ink-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important;
    box-shadow: none !important;
}

.stButton > button {
    border-radius: 0px !important;
    border: 1px solid var(--ink-primary) !important;
    background-color: var(--paper-card) !important;
    color: var(--ink-primary) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: background-color 0.1s ease !important;
}

.stButton > button:hover {
    background-color: var(--ink-primary) !important;
    color: #FFFFFF !important;
}

/* Case-File Dossier Sheet */
.casefile-sheet {
    border: 1px solid var(--hairline);
    background: var(--paper-card);
    padding: 18px 22px;
    margin-top: 16px;
}

.casefile-header {
    border-bottom: 1px solid var(--hairline);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.casefile-id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    color: var(--ink-primary);
}

.casefile-sub {
    font-size: 14.5px;
    color: var(--ink-secondary);
    margin-top: 4px;
    line-height: 1.4;
}

.casefile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
}

.casefile-field {
    border: 1px solid var(--hairline-light);
    background: var(--paper-bg);
    padding: 10px 14px;
}

.casefile-field-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-secondary);
}

.casefile-field-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: var(--ink-primary);
    margin-top: 3px;
    word-break: break-word;
}

/* Custom Horizontal Tick Scale Container */
.tick-scale-container {
    border: 1px solid var(--hairline);
    background: var(--paper-card);
    padding: 18px 22px 16px 22px;
    margin: 16px 0 20px 0;
}

.tick-scale-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--hairline-light);
    padding-bottom: 9px;
}

.tick-scale-title {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--ink-primary);
}

.tick-scale-readout {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    color: var(--ink-secondary);
}

.tick-scale-bar-wrap {
    position: relative;
    height: 42px;
    margin: 10px 0 22px 0;
}

.tick-scale-bands {
    display: flex;
    height: 14px;
    width: 100%;
    border: 1px solid var(--hairline);
}

.tick-band {
    height: 100%;
    position: relative;
}

.tick-scale-axis {
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--ink-secondary);
    margin-top: 5px;
}

.tick-marker-arrow {
    position: absolute;
    top: 15px;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-bottom: 9px solid var(--ink-primary);
}

.tick-marker-label {
    position: absolute;
    top: 25px;
    transform: translateX(-50%);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    color: var(--ink-primary);
    white-space: nowrap;
}

.tick-scale-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px dotted var(--hairline-light);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--ink-secondary);
}

.tick-legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

.tick-legend-sq {
    width: 10px;
    height: 10px;
    display: inline-block;
}

/* Audit Signals Register Table */
.audit-signals-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 22px;
    background: var(--paper-card);
    border: 1px solid var(--hairline);
    font-size: 13.5px;
}

.audit-signals-table th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-secondary);
    background: var(--paper-bg);
    border-bottom: 1px solid var(--hairline);
    border-right: 1px solid var(--hairline-light);
    padding: 10px 14px;
    text-align: left;
}

.audit-signals-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--hairline-light);
    border-right: 1px solid var(--hairline-light);
    color: var(--ink-primary);
}

.audit-signals-table tr:last-child td {
    border-bottom: none;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 3. DATA INGESTION & ROBUST DATASET RESOLUTION
# =========================================================
APP_DIR = Path(__file__).resolve().parent
DATA_PATHS = [
    # Deployed repository layout: repo/v1/app.py -> repo/data/MPLAD_cleaned_v2.csv
    APP_DIR.parent / "data" / "MPLAD_cleaned_v2.csv",
    # Other valid local layouts
    APP_DIR / "data" / "MPLAD_cleaned_v2.csv",
    APP_DIR / "MPLAD_cleaned_v2.csv",
    Path.cwd() / "data" / "MPLAD_cleaned_v2.csv",
    Path.cwd() / "MPLAD_cleaned_v2.csv",
]

GITHUB_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "codebyprathamesh/mplads-risk-intelligence-system/"
    "main/data/MPLAD_cleaned_v2.csv"
)

@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file, low_memory=False), "Uploaded File"

    for path in DATA_PATHS:
        try:
            if path.exists() and path.is_file():
                df = pd.read_csv(path, low_memory=False)
                if not df.empty:
                    return df, str(path)
        except Exception:
            continue

    # Final fallback for Streamlit Cloud.
    try:
        import urllib.request
        import io
        with urllib.request.urlopen(GITHUB_DATA_URL, timeout=30) as response:
            raw_data = response.read()
        df = pd.read_csv(io.BytesIO(raw_data), low_memory=False)
        if not df.empty:
            return df, "GitHub Repository Dataset"
    except Exception:
        pass

    return None, None

def find_col(df, candidates):
    for name in candidates:
        if name in df.columns:
            return name
    return None

def money(value):
    if pd.isna(value) or value is None:
        return "₹0"
    val = float(value)
    if abs(val) >= 1e7:
        return f"₹{val / 1e7:.2f} Cr"
    if abs(val) >= 1e5:
        return f"₹{val / 1e5:.2f} L"
    return f"₹{val:,.0f}"

def render_page_header(title, description, meta_pairs, callout=None):
    rows_html = "".join(
        f'<div class="header-meta-row"><span class="header-meta-key">{html.escape(k)}:</span> <span class="header-meta-val">{html.escape(str(v))}</span></div>'
        for k, v in meta_pairs
    )
    callout_html = f'<div class="header-callout-line">{callout}</div>' if callout else ""
    header_html = f"""
<div class="page-header">
  <h1 class="page-title">{html.escape(title)}</h1>
  <div class="page-desc">{html.escape(description)}</div>
  <div class="header-meta-block">
    {rows_html}
  </div>
  {callout_html}
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)

def prepare_data(df):
    df = df.copy()

    # Standardized friendly aliases
    aliases = {
        "Work ID": ["work_id", "Work ID", "ID", "id"],
        "State": ["state_name", "State", "state", "State Name"],
        "MP Name": ["mp_name", "MP Name", "mp", "MP"],
        "Constituency": ["constituency", "Constituency"],
        "Work Stage": ["work_stage", "Work Stage", "stage"],
        "Work Description": ["work_description", "Work Description", "description", "Description"],
        "Sanction Amount": ["sanction_amount", "Sanction Amount", "Sanctioned Amount"],
        "Actual Amount": ["actual_amount", "Actual Amount", "expenditure", "actual_expenditure", "Expenditure Amount"],
        "Recommended Amount": ["recommended_amount", "Recommended Amount"],
        "IDA Name": ["ida_name", "IDA Name", "IDA", "Implementing Agency"],
        "Letter No": ["letter_no", "Letter No", "Letter Number"],
    }
    for alias, candidates in aliases.items():
        col = find_col(df, candidates)
        if col and alias not in df.columns:
            df[alias] = df[col]

    if "Work Stage" not in df.columns or df["Work Stage"].isna().all():
        df["Work Stage"] = "Not Reported"
    else:
        df["Work Stage"] = df["Work Stage"].fillna("Not Reported").astype(str).str.strip()

    # Financial conversions
    for col in df.columns:
        low = col.lower()
        if any(x in low for x in ["amount", "cost", "expenditure", "expense", "fund", "value", "payment"]):
            if df[col].dtype == "object":
                cleaned = (
                    df[col].astype(str)
                    .str.replace(",", "", regex=False)
                    .str.replace("₹", "", regex=False)
                    .str.strip()
                )
                converted = pd.to_numeric(cleaned, errors="coerce")
                if converted.notna().mean() > 0.5:
                    df[col] = converted

    # Financial Year synthesis
    if "Financial Year" not in df.columns:
        fy_series = None
        if "letter_no" in df.columns:
            extracted = df["letter_no"].astype(str).str.extract(r'(\b\d{4}[-/]\d{4}\b)')[0]
            if extracted.notna().sum() > len(df) * 0.15:
                fy_series = extracted
        if (fy_series is None or fy_series.isna().mean() > 0.5) and "recommendation_date" in df.columns:
            r_dates = pd.to_datetime(df["recommendation_date"], errors="coerce")
            years = r_dates.dt.year
            months = r_dates.dt.month
            valid_mask = years.notna() & months.notna()
            fy_vals = np.where(
                valid_mask,
                np.where(
                    months >= 4,
                    years.astype(str) + "-" + ((years + 1) % 100).apply(lambda x: f"{int(x):02d}" if pd.notna(x) else ""),
                    (years - 1).astype(str) + "-" + (years % 100).apply(lambda x: f"{int(x):02d}" if pd.notna(x) else "")
                ),
                np.nan
            )
            fy_series = pd.Series(fy_vals, index=df.index)
        if fy_series is not None:
            df["Financial Year"] = fy_series.fillna("Not Specified").astype(str)
        else:
            df["Financial Year"] = "Not Specified"

    # Category normalization
    category_col = find_col(df, ["simple_category", "Work Category", "work_category", "Category", "category"])
    description_col = find_col(df, ["Work Description", "work_description", "Description", "description"])

    if "simple_category" in df.columns:
        df["Display Category"] = df["simple_category"].fillna("Other").astype(str)
    elif category_col:
        df["Display Category"] = df[category_col].fillna("Other").astype(str)
    elif description_col:
        text = df[description_col].fillna("").astype(str).str.lower()
        df["Display Category"] = np.select(
            [
                text.str.contains("road|street|bridge|transport|highway"),
                text.str.contains("school|education|college|classroom"),
                text.str.contains("hospital|health|clinic|medical"),
                text.str.contains("water|pipeline|tank|borewell|sanitation"),
                text.str.contains("electric|lighting|solar|street light"),
            ],
            ["Roads & Transport", "Education", "Health & Medical", "Water & Sanitation", "Electricity & Lighting"],
            default="Other",
        )
    else:
        df["Display Category"] = "Other"

    # Risk fields
    risk_col = find_col(df, ["Risk Score", "risk_score", "RiskScore"])
    tier_col = find_col(df, ["Risk Tier", "risk_tier", "RiskTier"])
    reason_col = find_col(df, ["Risk Reasons", "risk_reasons", "Risk Reason", "risk_reason"])
    anomaly_col = find_col(df, ["Anomaly", "anomaly", "anomaly_flag", "Anomaly Flag"])

    if risk_col:
        df["Risk Score"] = pd.to_numeric(df[risk_col], errors="coerce").fillna(0).clip(0, 100)
    else:
        score = pd.Series(0.0, index=df.index)
        for col in df.columns:
            if any(x in col.lower() for x in ["overdue", "overrun", "duplicate", "anomaly"]):
                vals = pd.to_numeric(df[col], errors="coerce").fillna(0)
                score += vals.clip(0, 1) * 20
        df["Risk Score"] = score.clip(0, 100)

    if tier_col:
        df["Risk Tier"] = (
            df[tier_col]
            .fillna("No Risk")
            .astype("string")
            .str.strip()
            .str.title()
        )
    else:
        df["Risk Tier"] = pd.cut(
            df["Risk Score"], bins=[-0.01, 15, 30, 45, 60, 100.01],
            labels=["No Risk", "Low", "Medium", "High", "Critical"]
        ).astype(str)

    df["Risk Reasons"] = df[reason_col].fillna("").astype(str) if reason_col else ""
    if anomaly_col:
        df["Anomaly"] = df[anomaly_col].astype(str).str.lower().isin(["1", "true", "yes", "y", "anomaly", "outlier"])
    else:
        df["Anomaly"] = False

    # Normalize boolean ML signals
    for target, candidates in {
        "Sanction Overdue": ["sanction_overdue", "Sanction Overdue"],
        "Completion Overdue": ["completion_overdue", "Completion Overdue"],
        "Cost Overrun": ["cost_overrun", "Cost Overrun"],
        "High Cost Outlier": ["high_cost_outlier", "High Cost Outlier"],
        "Missing Description": ["missing_description", "Missing Description"],
        "Sanction Amount Missing": ["sanction_amount_missing", "Sanction Amount Missing"],
        "Possible Duplicate": ["possible_duplicate", "Possible Duplicate"],
    }.items():
        col = find_col(df, candidates)
        if col:
            values = df[col].astype("string").str.strip().str.lower()
            df[target] = values.isin(["1", "1.0", "true", "yes", "y", "anomaly", "outlier"])
        else:
            df[target] = False

    return df

# =========================================================
# 4. PLOTLY CHART STYLING & SEMANTIC COLOR SYSTEM
# =========================================================
PAPER_BG = "#FAFAF7"
PLOT_BG = "#FAFAF7"
INK_PRIMARY = "#1A1A1A"
INK_SECONDARY = "#4A4F58"  # High-contrast readable dark gray floor
GRID_COLOR = "#DDDAD2"

# Strict Risk Colors (Applied ONLY to risk-tier data)
RISK_COLORS = {
    "Critical": "#8B2E22",  # Deep brick red
    "High": "#B0522D",      # Burnt orange
    "Medium": "#9C6B2E",    # Muted amber
    "Low": "#4B7A5E",       # Muted green
    "No Risk": "#6B7280",   # Neutral gray
}

# Non-Risk Categorical Color Family (Muted deep teal)
TEAL_BASE = "#2B6B6B"
TEAL_LIGHT = "#6B9C9C"

# Regulatory signals get their own accent (distinct from both risk tiers and categorical palette)
SIGNAL_ACCENT = "#8A7355"  # warm taupe — risk-adjacent but not a risk tier color

def style_fig(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=INK_SECONDARY, family="Inter, sans-serif", size=13),
        margin=dict(l=45, r=25, t=15, b=40),
        legend=dict(
            font=dict(family="IBM Plex Mono", size=13, color=INK_SECONDARY),
            bgcolor="rgba(250,250,247,0.9)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=GRID_COLOR,
            font=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
        ),
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zerolinecolor=GRID_COLOR,
        tickfont=dict(family="IBM Plex Mono", color=INK_SECONDARY, size=13),
        title_font=dict(family="Inter, sans-serif", color=INK_PRIMARY, size=13.5),
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zerolinecolor=GRID_COLOR,
        tickfont=dict(family="IBM Plex Mono", color=INK_SECONDARY, size=13),
        title_font=dict(family="Inter, sans-serif", color=INK_PRIMARY, size=13.5),
    )
    return fig

# =========================================================
# 6. PLOTLY CHARTS WITH UNIFIED COLOR SYSTEM
# =========================================================
def risk_distribution_chart(counts):
    labels = ["Critical", "High", "Medium", "Low", "No Risk"]
    values = [int(counts.get(x, 0)) for x in labels]
    total = max(sum(values), 1)
    shares = [(v / total * 100) for v in values]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(
            color=[RISK_COLORS[x] for x in labels],
            line=dict(color=PAPER_BG, width=0.8),
        ),
        text=[f"{v:,}  ·  {pct:.1f}%" for v, pct in zip(values, shares)],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Works: %{x:,}<extra></extra>",
    ))
    fig.update_layout(
        template="plotly_white",
        height=395,
        showlegend=False,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="Inter, sans-serif", color=INK_SECONDARY, size=13),
        margin=dict(l=88, r=110, t=10, b=28),
        bargap=0.28,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=GRID_COLOR, font=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13)),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=False,
        title=None,
        tickfont=dict(family="IBM Plex Mono", color=INK_SECONDARY, size=12),
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        title=None,
        tickfont=dict(family="Inter", color=INK_PRIMARY, size=12.5),
        categoryorder="array",
        categoryarray=labels,
    )
    return fig

def proportional_teal_colors(values):
    vals = np.asarray(values, dtype=float)
    if len(vals) == 0:
        return []
    vmax = float(vals.max())
    vmin = float(vals.min())
    if vmax == vmin:
        t = np.ones_like(vals) * 0.65
    else:
        t = 0.35 + 0.65 * ((vals - vmin) / (vmax - vmin))
    base = np.array([43, 107, 107], dtype=float)
    bg = np.array([250, 250, 247], dtype=float)
    return [
        "rgb({},{},{})".format(*np.round(bg * (1 - x) + base * x).astype(int))
        for x in t
    ]

def stage_chart(df):
    s = df["Work Stage"].fillna("Not Reported").astype(str).value_counts().head(8).sort_values()
    bar_colors = proportional_teal_colors(s.values)
    fig = go.Figure(go.Bar(
        x=s.values,
        y=s.index,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0.15)", width=0.5)),
        text=[f"{v:,}" for v in s.values],
        textposition="outside",
        cliponaxis=False,
        textfont=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
        hovertemplate="<b>%{y}</b><br>Works: %{x:,}<extra></extra>",
    ))
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig = style_fig(fig, height=410)
    fig.update_layout(margin=dict(l=185, r=45, t=15, b=40))
    return fig

def category_chart(df):
    s = df["Display Category"].fillna("Other").astype(str).value_counts().head(8).sort_values()
    bar_colors = proportional_teal_colors(s.values)
    fig = go.Figure(go.Bar(
        x=s.values,
        y=s.index,
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0.15)", width=0.5)),
        text=[f"{v:,}" for v in s.values],
        textposition="outside",
        cliponaxis=False,
        textfont=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
        hovertemplate="<b>%{y}</b><br>Works: %{x:,}<extra></extra>",
    ))
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig = style_fig(fig, height=410)
    fig.update_layout(margin=dict(l=185, r=45, t=15, b=40))
    return fig

def risk_signal_chart(df):
    signals = {
        "Completion overdue": int(df["Completion Overdue"].sum()),
        "Sanction overdue": int(df["Sanction Overdue"].sum()),
        "Cost overrun": int(df["Cost Overrun"].sum()),
        "High-cost outlier": int(df["High Cost Outlier"].sum()),
        "Possible duplicate": int(df["Possible Duplicate"].sum()),
        "Model anomaly flag": int(df["Anomaly"].sum()),
        "Missing description": int(df["Missing Description"].sum()),
        "Sanction amount missing": int(df["Sanction Amount Missing"].sum()),
    }
    s = pd.Series(signals).sort_values()
    signal_tiers = {
        "Completion overdue": "Critical",
        "Sanction overdue": "Medium",
        "Cost overrun": "High",
        "High-cost outlier": "High",
        "Possible duplicate": "Medium",
        "Model anomaly flag": "Critical",
        "Missing description": "Medium",
        "Sanction amount missing": "Medium",
    }

    fig = px.bar(
        x=s.values,
        y=s.index,
        orientation="h",
        labels={"x": "", "y": ""},
        text=s.values,
    )
    fig.update_traces(
        marker_color=[RISK_COLORS[signal_tiers[name]] for name in s.index],
        marker_line=dict(color="#5C4A2A", width=0.5),
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        textfont=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
        hovertemplate="<b>%{y}</b><br>Flagged works: %{x:,}<extra></extra>",
    )
    fig = style_fig(fig, height=410)
    fig.update_layout(margin=dict(l=195, r=50, t=15, b=40))
    return fig

def india_risk_map(df):
    if "State" not in df.columns or df["State"].dropna().empty:
        return None

    centroids = {
        "andaman and nicobar islands": (11.7401, 92.6586),
        "andhra pradesh": (15.9129, 79.7400),
        "arunachal pradesh": (28.2180, 94.7278),
        "assam": (26.2006, 92.9376),
        "bihar": (25.0961, 85.3131),
        "chandigarh": (30.7333, 76.7794),
        "chhattisgarh": (21.2787, 81.8661),
        "dadra and nagar haveli and daman and diu": (20.4283, 72.8397),
        "delhi": (28.7041, 77.1025),
        "goa": (15.2993, 74.1240),
        "gujarat": (22.2587, 71.1924),
        "haryana": (29.0588, 76.0856),
        "himachal pradesh": (31.1048, 77.1734),
        "jammu and kashmir": (33.7782, 76.5762),
        "jharkhand": (23.6102, 85.2799),
        "karnataka": (15.3173, 75.7139),
        "kerala": (10.8505, 76.2711),
        "ladakh": (34.1526, 77.5771),
        "lakshadweep": (10.5667, 72.6417),
        "madhya pradesh": (22.9734, 78.6569),
        "maharashtra": (19.7515, 75.7139),
        "manipur": (24.6637, 93.9063),
        "meghalaya": (25.4670, 91.3662),
        "mizoram": (23.1645, 92.9376),
        "nagaland": (26.1584, 94.5624),
        "odisha": (20.9517, 85.0985),
        "puducherry": (11.9416, 79.8083),
        "punjab": (31.1471, 75.3412),
        "rajasthan": (27.0238, 74.2179),
        "sikkim": (27.5330, 88.5122),
        "tamil nadu": (11.1271, 78.6569),
        "telangana": (18.1124, 79.0193),
        "the dadra and nagar haveli and daman and diu": (20.4283, 72.8397),
        "dadra and nagar haveli": (20.4283, 72.8397),
        "daman and diu": (20.4283, 72.8397),
        "tripura": (23.9408, 91.9882),
        "uttar pradesh": (26.8467, 80.9462),
        "uttarakhand": (30.0668, 79.0193),
        "west bengal": (22.9868, 87.8550),
    }

    g = df.groupby("State", dropna=False).agg(
        Works=("Risk Score", "size"),
        AvgRisk=("Risk Score", "mean"),
        HighRisk=("Risk Tier", lambda x: x.isin(["High", "Critical"]).sum()),
    ).reset_index()

    def get_coords(state_name):
        norm = str(state_name).strip().lower()
        return centroids.get(norm, (np.nan, np.nan))

    coords = g["State"].apply(get_coords)
    g["lat"] = [c[0] for c in coords]
    g["lon"] = [c[1] for c in coords]
    g = g.dropna(subset=["lat", "lon"])
    if g.empty:
        return None

    g["HighRiskShare"] = (g["HighRisk"] / g["Works"] * 100).fillna(0)
    custom_hover = (
        "<b>%{hovertext}</b><br><br>"
        + "Works registered: <b>%{customdata[0]:,}</b><br>"
        + "Average risk: <b>%{customdata[1]:.1f} / 100</b><br>"
        + "High / critical cases: <b>%{customdata[2]:,}</b><br>"
        + "High risk share: <b>%{customdata[3]:.1f}%</b><extra></extra>"
    )

    # Use Plotly's built-in geographic layer so the dashboard never depends on a Mapbox token.
    share_max = max(float(g["HighRiskShare"].max()), 1.0)
    fig = px.scatter_geo(
        g,
        lat="lat",
        lon="lon",
        size="Works",
        color="HighRiskShare",
        hover_name="State",
        size_max=30,
        projection="mercator",
        range_color=(0, share_max),
        color_continuous_scale=[
            [0.00, RISK_COLORS["Low"]],
            [0.35, RISK_COLORS["Medium"]],
            [0.65, RISK_COLORS["High"]],
            [1.00, RISK_COLORS["Critical"]],
        ],
    )
    fig.update_traces(
        marker=dict(
            opacity=0.76,
            line=dict(color=PAPER_BG, width=1),
        ),
        hovertext=g["State"],
        customdata=g[["Works", "AvgRisk", "HighRisk", "HighRiskShare"]].values,
        hovertemplate=custom_hover,
    )
    fig.update_geos(
        visible=True,
        scope="asia",
        projection_type="mercator",
        center=dict(lat=22.5, lon=79.6),
        lataxis_range=[6, 38],
        lonaxis_range=[67, 99],
        showland=True,
        landcolor="#F0EFEA",
        showocean=True,
        oceancolor="#FAFAF7",
        showcountries=True,
        countrycolor="#D6D2C9",
        coastlinecolor="#CFCBC2",
        showlakes=False,
        bgcolor=PAPER_BG,
    )
    fig.update_layout(
        template="plotly_white",
        height=430,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        font=dict(family="Inter, sans-serif", color=INK_SECONDARY, size=13),
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor=PAPER_BG),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=GRID_COLOR,
            font=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
        ),
        coloraxis_colorbar=dict(
            title="High / critical share (%)",
            ticksuffix="%",
            thickness=10,
            len=0.62,
            outlinewidth=0,
            tickfont=dict(family="IBM Plex Mono", size=11, color=INK_SECONDARY),
            title_font=dict(family="Inter", size=11, color=INK_SECONDARY),
        ),
    )
    return fig

# =========================================================
# 7. DISTINCTIVE HORIZONTAL TICK SCALE (0 - 100)
# =========================================================
def render_risk_tick_scale(score, tier, reason):
    score = float(score)
    score_clamped = max(0.0, min(100.0, score))
    tier_str = str(tier).title().strip()
    tier_color = RISK_COLORS.get(tier_str, "#1A1A1A")
    reason_clean = html.escape(str(reason).strip() if reason and str(reason).lower() != "nan" else "No statutory triggers flagged.")

    bands_html = f"""
    <div class="tick-scale-container">
      <div class="tick-scale-header">
        <div class="tick-scale-title">Traceable risk score & statutory evaluation</div>
        <div class="tick-scale-readout">
          Score: <span style="font-weight:700; color:{INK_PRIMARY}; font-size:15px;">{score_clamped:.0f} / 100</span>
          &nbsp;&nbsp;·&nbsp;&nbsp;
          Tier: <span style="font-weight:700; color:{tier_color}; font-size:14px;">{tier_str}</span>
        </div>
      </div>

      <div class="tick-scale-bar-wrap">
        <div class="tick-scale-bands">
          <div class="tick-band" style="width:15%; background:{RISK_COLORS['No Risk']};" title="0 - 15: No Risk"></div>
          <div class="tick-band" style="width:15%; background:{RISK_COLORS['Low']};" title="15 - 30: Low Risk"></div>
          <div class="tick-band" style="width:15%; background:{RISK_COLORS['Medium']};" title="30 - 45: Medium Risk"></div>
          <div class="tick-band" style="width:15%; background:{RISK_COLORS['High']};" title="45 - 60: High Risk"></div>
          <div class="tick-band" style="width:40%; background:{RISK_COLORS['Critical']};" title="60 - 100: Critical Risk"></div>
        </div>
        <div class="tick-marker-arrow" style="left:{score_clamped}%;"></div>
        <div class="tick-marker-label" style="left:{score_clamped}%;">{score_clamped:.0f}</div>
      </div>

      <div class="tick-scale-axis">
        <span>0</span>
        <span>15</span>
        <span>30</span>
        <span>45</span>
        <span>60</span>
        <span>100</span>
      </div>

      <div style="font-family:'IBM Plex Mono', monospace; font-size:13px; margin-top:14px; padding:9px 12px; background:{PAPER_BG}; border:1px solid {GRID_COLOR}; line-height:1.45;">
        <span style="font-weight:600; color:{INK_SECONDARY};">Named trigger reason:</span>
        <span style="color:{INK_PRIMARY}; margin-left:8px; font-weight:500;">{reason_clean}</span>
      </div>

      <div class="tick-scale-legend">
        <div class="tick-legend-item"><span class="tick-legend-sq" style="background:{RISK_COLORS['No Risk']};"></span> No risk (0–15)</div>
        <div class="tick-legend-item"><span class="tick-legend-sq" style="background:{RISK_COLORS['Low']};"></span> Low (15–30)</div>
        <div class="tick-legend-item"><span class="tick-legend-sq" style="background:{RISK_COLORS['Medium']};"></span> Medium (30–45)</div>
        <div class="tick-legend-item"><span class="tick-legend-sq" style="background:{RISK_COLORS['High']};"></span> High (45–60)</div>
        <div class="tick-legend-item"><span class="tick-legend-sq" style="background:{RISK_COLORS['Critical']};"></span> Critical (60–100)</div>
      </div>
    </div>
    """
    st.markdown(bands_html, unsafe_allow_html=True)

# =========================================================
# 8. APPLICATION BOOTSTRAP & SIDEBAR INDEX
# =========================================================
uploaded = st.sidebar.file_uploader(
    "Import dataset (CSV)",
    type=["csv"],
    help="Default repository dataset is used when no upload is provided.",
)
df, source = load_data(uploaded)

if df is None:
    st.error("No dataset available. Expected data/MPLAD_cleaned_v2.csv in the repository, or a CSV uploaded through the sidebar.")
    st.stop()

df = prepare_data(df)

# Navigation Index List — simple clickable buttons, no radio controls.
NAV_ITEMS = [
    "Dashboard",
    "Risk Signals",
    "Anomaly Center",
    "Cost Intelligence",
    "Project Monitoring",
    "Works Explorer",
    "Similar Works",
]

if "page" not in st.session_state or st.session_state.page not in NAV_ITEMS:
    st.session_state.page = "Dashboard"

st.sidebar.markdown(
    "<div class='sidebar-nav-label'>Navigation</div>",
    unsafe_allow_html=True,
)
for nav_item in NAV_ITEMS:
    if st.sidebar.button(nav_item, key=f"nav_{nav_item.lower().replace(' ', '_')}", width="stretch"):
        st.session_state.page = nav_item
        st.rerun()

page = st.session_state.page

st.sidebar.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='font-family:\"IBM Plex Mono\", monospace; font-size:13px; font-weight:600; color:var(--ink-secondary); margin-bottom:8px;'>Scope filters</div>",
    unsafe_allow_html=True,
)

state_col = find_col(df, ["State", "state", "State Name", "state_name"])
constituency_col = find_col(df, ["Constituency", "constituency"])
ida_col = find_col(df, ["IDA Name", "ida_name", "Implementing Agency"])
fy_col = find_col(df, ["Financial Year", "financial_year", "FY", "fy"])

filtered = df
if state_col:
    states = sorted(filtered[state_col].dropna().astype(str).unique())
    selected_states = st.sidebar.multiselect("Filter by state", states, placeholder="All 36 States & UTs")
    if selected_states:
        filtered = filtered[filtered[state_col].astype(str).isin(selected_states)]

if constituency_col:
    constituencies = sorted(filtered[constituency_col].dropna().astype(str).unique())
    selected_constituencies = st.sidebar.multiselect("Filter by constituency", constituencies, placeholder="All constituencies")
    if selected_constituencies:
        filtered = filtered[filtered[constituency_col].astype(str).isin(selected_constituencies)]

if ida_col:
    idas = sorted(filtered[ida_col].dropna().astype(str).unique())
    if len(idas) > 0 and len(idas) < 2000:
        selected_idas = st.sidebar.multiselect("Filter by agency (IDA)", idas[:100], placeholder="All agencies")
        if selected_idas:
            filtered = filtered[filtered[ida_col].astype(str).isin(selected_idas)]

if fy_col:
    years = sorted(filtered[fy_col].dropna().astype(str).unique())
    selected_years = st.sidebar.multiselect("Filter by financial year", years, placeholder="All financial years")
    if selected_years:
        filtered = filtered[filtered[fy_col].astype(str).isin(selected_years)]

if st.sidebar.button("Reset scope filters", width="stretch"):
    st.rerun()

filter_ratio = (len(filtered) / len(df) * 100) if len(df) else 100.0

# Core Aggregates
risk_counts = filtered["Risk Tier"].value_counts()
high_risk_count = int(filtered["Risk Tier"].isin(["High", "Critical"]).sum())
critical_count = int((filtered["Risk Tier"] == "Critical").sum())
anomaly_count = int(filtered["Anomaly"].sum())
duplicate_count = int(filtered["Possible Duplicate"].sum())


sanction_col = find_col(filtered, ["Sanction Amount", "sanction_amount", "Sanctioned Amount", "Recommended Amount", "recommended_amount"])
expenditure_col = find_col(filtered, ["Actual Amount", "actual_amount", "Expenditure", "expenditure", "Actual Expenditure", "actual_expenditure"])
total_sanction = pd.to_numeric(filtered[sanction_col], errors="coerce").sum() if sanction_col else 0
total_expenditure = pd.to_numeric(filtered[expenditure_col], errors="coerce").sum() if expenditure_col else 0
utilization = (total_expenditure / total_sanction * 100) if total_sanction > 0 else 0

# =========================================================
# VIEW 1: DASHBOARD (RISK-FIRST EXECUTIVE AUDIT REGISTER)
# =========================================================
if page == "Dashboard":
    st.markdown("<div class='page-header'><h1 class='page-title'>MPLADS Risk Intelligence System</h1></div>", unsafe_allow_html=True)

    review_count = high_risk_count
    flag_count = anomaly_count + duplicate_count
    st.markdown(
        f"""
<div class="dashboard-cards">
  <div class="dashboard-card tone-neutral">
    <div class="dashboard-card-kicker">Total works</div>
    <div class="dashboard-card-value">{len(filtered):,}</div>
    <div class="dashboard-card-sub">{filter_ratio:.1f}% of the registered portfolio is in the active scope.</div>
  </div>
  <div class="dashboard-card tone-critical">
    <div class="dashboard-card-kicker">Priority review</div>
    <div class="dashboard-card-value">{review_count:,}</div>
    <div class="dashboard-card-sub">High or Critical risk tier · {critical_count:,} currently Critical.</div>
  </div>
  <div class="dashboard-card tone-medium">
    <div class="dashboard-card-kicker">Risk signals</div>
    <div class="dashboard-card-value">{flag_count:,}</div>
    <div class="dashboard-card-sub">{anomaly_count:,} model anomalies + {duplicate_count:,} possible duplicate matches.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    col_map, col_risk = st.columns([1.16, 0.94], gap="large")
    with col_map:
        st.markdown("<div class='section-head'>Geographic risk exposure</div>", unsafe_allow_html=True)
        if PLOTLY_OK:
            map_fig = india_risk_map(filtered)
            if map_fig is not None:
                st.plotly_chart(map_fig, width="stretch", config={"displayModeBar": False})
            else:
                st.info("State geographical data not available for rendering map.")
        else:
            st.info("Plotly is required for interactive map visualization.")

    with col_risk:
        st.markdown("<div class='section-head'>Risk classification</div>", unsafe_allow_html=True)
        if PLOTLY_OK:
            st.plotly_chart(risk_distribution_chart(risk_counts), width="stretch", config={"displayModeBar": False})
        else:
            st.bar_chart(risk_counts)

    st.markdown("<div class='section-head'>Portfolio composition</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>Current implementation stage and infrastructure mix across the active scope.</div>", unsafe_allow_html=True)
    c_stg, c_cat = st.columns(2, gap="large")
    with c_stg:
        if PLOTLY_OK:
            st.plotly_chart(stage_chart(filtered), width="stretch", config={"displayModeBar": False})
        else:
            st.bar_chart(filtered["Work Stage"].fillna("Not Reported").value_counts())

    with c_cat:
        if PLOTLY_OK:
            st.plotly_chart(category_chart(filtered), width="stretch", config={"displayModeBar": False})
        else:
            st.bar_chart(filtered["Display Category"].value_counts())

    st.markdown("<div class='section-head'>Active regulatory signals</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>Counts are colour-coded by the severity of the underlying signal.</div>", unsafe_allow_html=True)
    if PLOTLY_OK:
        st.plotly_chart(risk_signal_chart(filtered), width="stretch", config={"displayModeBar": False})

    st.markdown("<div class='section-head'>Priority inspection queue</div>", unsafe_allow_html=True)

    top_works = filtered.sort_values("Risk Score", ascending=False).head(20).copy()
    top_works.insert(0, "SR NO", range(1, len(top_works) + 1))
    cols_to_show = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Display Category", "Work Stage", "Sanction Amount", "Actual Amount", "Risk Score", "Risk Tier", "Risk Reasons"] if c in top_works.columns]

    st.dataframe(
        top_works[cols_to_show],
        width="stretch",
        hide_index=True,
        column_config={
            "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
            "Work ID": st.column_config.TextColumn("Work ID", width="small"),
            "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f", help="Composite 0-100 audit score"),
            "Risk Tier": st.column_config.TextColumn("Risk tier"),
            "Sanction Amount": st.column_config.NumberColumn("Sanction amt (₹)", format="₹%d"),
            "Actual Amount": st.column_config.NumberColumn("Actual exp (₹)", format="₹%d"),
            "Risk Reasons": st.column_config.TextColumn("Named risk reasons"),
        },
    )

# =========================================================
# VIEW 2: RISK SIGNALS
# =========================================================
elif page == "Risk Signals":
    render_page_header(
        title="Risk Signals Surveillance Queue",
        description="Explainable statutory compliance triggers and rule-based risk signals produced by the audit pipeline",
        meta_pairs=[
            ("Monitored signals", "8 regulatory rules"),
            ("Critical & high risk cases", f"{high_risk_count:,}"),
            ("Queue status", "Active statutory review"),
        ],
    )

    # Summary Strip
    st.markdown(
        f"""
<div class="ledger-summary-strip">
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">High & critical cohort</span>
    <span class="ledger-cell-val" style="color:{RISK_COLORS['Critical']};">{high_risk_count:,}</span>
    <span class="ledger-cell-sub">Requires direct inquiry</span>
  </div>
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">Machine learning anomalies</span>
    <span class="ledger-cell-val" >{anomaly_count:,}</span>
    <span class="ledger-cell-sub">Isolation Forest flags</span>
  </div>
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">Duplicate text signals</span>
    <span class="ledger-cell-val" >{duplicate_count:,}</span>
    <span class="ledger-cell-sub">Semantic match cluster</span>
  </div>
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">Completion overdue</span>
    <span class="ledger-cell-val" >{int(filtered['Completion Overdue'].sum()):,}</span>
    <span class="ledger-cell-sub">Beyond statutory timeline</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-head'>Active regulatory signals triggered</div>", unsafe_allow_html=True)
    if PLOTLY_OK:
        st.plotly_chart(risk_signal_chart(filtered), width="stretch", config={"displayModeBar": False})

    # Audit Signal Register (Plain Ledger Table)
    st.markdown("<div class='section-head'>Regulatory signal breakdown register</div>", unsafe_allow_html=True)

    signal_definitions = [
        ("SIG-01", "Completion overdue", "Sanctioned works operating past the stipulated milestone completion date.", "Completion Overdue", "Critical", RISK_COLORS["Critical"]),
        ("SIG-02", "Sanction overdue", "Recommended works pending administrative sanction beyond statutory 75-day window.", "Sanction Overdue", "Medium", RISK_COLORS["Medium"]),
        ("SIG-03", "Cost overrun", "Cumulative reported expenditure exceeds the approved baseline sanction allocation.", "Cost Overrun", "High", RISK_COLORS["High"]),
        ("SIG-04", "High-cost outlier", "Work allocation exceeds the 95th percentile within its state and category cohort.", "High Cost Outlier", "High", RISK_COLORS["High"]),
        ("SIG-05", "Possible duplicate", "Natural language processing model detected highly repetitive semantic project description.", "Possible Duplicate", "Medium", RISK_COLORS["Medium"]),
        ("SIG-06", "Multivariate anomaly", "Isolation Forest detected abnormal multivariate latency and cost variance pattern.", "Anomaly", "Critical", RISK_COLORS["Critical"]),
        ("SIG-07", "Missing description", "Work description field is blank, truncated, or lacks statutory operational details.", "Missing Description", "No Risk", RISK_COLORS["No Risk"]),
        ("SIG-08", "Missing sanction amount", "Work marked sanctioned without recorded sanction amount in database.", "Sanction Amount Missing", "No Risk", RISK_COLORS["No Risk"]),
    ]

    table_rows = []
    for sig_id, name, rule, col_name, tier_name, tier_color in signal_definitions:
        cnt = int(filtered[col_name].sum()) if col_name in filtered.columns else 0
        table_rows.append(
            f"<tr>"
            f"<td style='font-family:\"IBM Plex Mono\", monospace; font-weight:600;'>{sig_id}</td>"
            f"<td style='font-weight:600;'>{name}</td>"
            f"<td style='color:var(--ink-secondary);'>{rule}</td>"
            f"<td style='font-family:\"IBM Plex Mono\", monospace; font-weight:700; text-align:right;'>{cnt:,}</td>"
            f"<td style='font-family:\"IBM Plex Mono\", monospace; font-weight:700; color:{tier_color};'>{tier_name}</td>"
            f"</tr>"
        )

    rows_joined = "".join(table_rows)
    signals_html = (
        '<table class="audit-signals-table">'
        '<thead><tr>'
        '<th style="width:75px;">Code</th>'
        '<th style="width:210px;">Regulatory risk signal</th>'
        '<th>Statutory rule / audit threshold</th>'
        '<th style="width:130px;text-align:right;">Flagged works</th>'
        '<th style="width:130px;">Severity tier</th>'
        f'</tr></thead><tbody>{rows_joined}</tbody></table>'
    )
    st.markdown(signals_html, unsafe_allow_html=True)

    # Priority Inspection Queue
    st.markdown("<div class='section-head'>Priority inspection queue</div>", unsafe_allow_html=True)

    priority_queue = filtered[filtered["Risk Tier"].isin(["Critical", "High"])].sort_values(
        ["Risk Score", "Anomaly"], ascending=[False, False]
    ).copy()
    
    if priority_queue.empty:
        st.info("No High or Critical risk records present under the active filter selection.")
    else:
        priority_queue.insert(0, "SR NO", range(1, len(priority_queue) + 1))
        p_cols = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Display Category", "Work Stage", "Sanction Amount", "Risk Score", "Risk Tier", "Anomaly", "Possible Duplicate", "Risk Reasons"] if c in priority_queue.columns]
        st.dataframe(
            priority_queue[p_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
                "Work ID": st.column_config.TextColumn("Work ID", width="small"),
                "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Risk Tier": st.column_config.TextColumn("Risk tier"),
                "Sanction Amount": st.column_config.NumberColumn("Sanction amt (₹)", format="₹%d"),
                "Risk Reasons": st.column_config.TextColumn("Named risk reasons"),
            },
        )

# =========================================================
# VIEW 3: ANOMALY CENTER (MULTIVARIATE OUTLIER LOG)
# =========================================================
elif page == "Anomaly Center":
    render_page_header(
        title="Multivariate Anomaly Center",
        description="Statistical outliers and execution irregularities identified via unsupervised machine learning models",
        meta_pairs=[
            ("Model specification", "Isolation Forest multivariate pipeline"),
            ("Total observations evaluated", f"{len(df):,}"),
            ("Baseline contamination rate", "3.0%"),
        ],
    )

    anomaly_rate = (anomaly_count / len(filtered) * 100) if len(filtered) else 0
    high_crit_anomaly = int((filtered["Anomaly"] & filtered["Risk Tier"].isin(["High", "Critical"])).sum())

    st.markdown(
        f"""
<div class="ledger-summary-strip">
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">Detected statistical anomalies</span>
    <span class="ledger-cell-val" >{anomaly_count:,}</span>
    <span class="ledger-cell-sub">Multivariate outliers</span>
  </div>
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">Cohort anomaly rate</span>
    <span class="ledger-cell-val" >{anomaly_rate:.2f}%</span>
    <span class="ledger-cell-sub">Baseline contamination: 3.0%</span>
  </div>
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">High/critical anomaly overlap</span>
    <span class="ledger-cell-val" >{high_crit_anomaly:,}</span>
    <span class="ledger-cell-sub">Dual-flagged priority cases</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    anomalies_df = filtered[filtered["Anomaly"]].sort_values("Risk Score", ascending=False).copy()
    if anomalies_df.empty:
        st.info("No anomaly flags identified in the active filter selection.")
    else:
        anomalies_df.insert(0, "SR NO", range(1, len(anomalies_df) + 1))
        st.markdown("<div class='section-head'>Flagged anomaly register</div>", unsafe_allow_html=True)

        cols_anom = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Display Category", "Work Stage", "Sanction Amount", "Risk Score", "Risk Tier", "Anomaly", "Risk Reasons"] if c in anomalies_df.columns]
        st.dataframe(
            anomalies_df[cols_anom],
            width="stretch",
            hide_index=True,
            column_config={
                "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
                "Work ID": st.column_config.TextColumn("Work ID", width="small"),
                "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Risk Tier": st.column_config.TextColumn("Risk tier"),
                "Sanction Amount": st.column_config.NumberColumn("Sanction amt (₹)", format="₹%d"),
                "Risk Reasons": st.column_config.TextColumn("Named risk reasons"),
            },
        )

# =========================================================
# VIEW 4: COST INTELLIGENCE (DENSITY-SIZED SCATTER PLOT)
# =========================================================
elif page == "Cost Intelligence":
    render_page_header(
        title="Cost Intelligence & Fiscal Audit",
        description="Statutory expenditure distribution, allocation vs actuals, and cost overrun audits",
        meta_pairs=[
            ("Sanctioned baseline", money(total_sanction)),
            ("Cumulative expenditure", money(total_expenditure)),
            ("Disbursement rate", f"{utilization:.1f}%"),
        ],
    )

    if sanction_col:
        s_vals = pd.to_numeric(filtered[sanction_col], errors="coerce").dropna()
        p50 = s_vals.median() if not s_vals.empty else 0
        p95 = s_vals.quantile(0.95) if not s_vals.empty else 0
        p99 = s_vals.quantile(0.99) if not s_vals.empty else 0
        overrun_cases = filtered[filtered["Cost Overrun"]]

        st.markdown(
            f"""
<div class="ledger-summary-strip">
  <div class="ledger-cell tone-neutral">
    <span class="ledger-cell-label">Aggregate sanctioned</span>
    <span class="ledger-cell-val" >{money(s_vals.sum())}</span>
    <span class="ledger-cell-sub">National allocation</span>
  </div>
  <div class="ledger-cell tone-neutral">
    <span class="ledger-cell-label">Median allocation</span>
    <span class="ledger-cell-val" >{money(p50)}</span>
    <span class="ledger-cell-sub">50th percentile</span>
  </div>
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">95th percentile threshold</span>
    <span class="ledger-cell-val" >{money(p95)}</span>
    <span class="ledger-cell-sub">Outlier boundary</span>
  </div>
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">Cost overrun works</span>
    <span class="ledger-cell-val" >{len(overrun_cases):,}</span>
    <span class="ledger-cell-sub">Expenditure > sanction</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # Cost Intelligence Density-Calibrated Scatter Plot
    if sanction_col and expenditure_col and PLOTLY_OK:
        comp = filtered[[sanction_col, expenditure_col, "Cost Overrun", "Work ID"]].apply(
            lambda x: pd.to_numeric(x, errors="coerce") if x.name in [sanction_col, expenditure_col] else x
        ).dropna(subset=[sanction_col, expenditure_col])

        if not comp.empty:
            comp.columns = ["Sanction Amount", "Expenditure Amount", "Cost Overrun", "Work ID"]
            
            st.markdown("<div class='section-head'>Allocation vs actual expenditure scatter analysis</div>", unsafe_allow_html=True)

            scatter_scope = st.radio(
                "Display scope",
                [
                    "Dense operational range (≤ 99th percentile: ₹0 to ₹26.0 L)",
                    "Macro outliers range (> 99th percentile: ₹26.0 L to ₹4.65 Cr)",
                    "Complete register (logarithmic scale)",
                ],
                horizontal=True,
            )

            p99_thresh = 2600000.0
            if "Dense operational" in scatter_scope:
                plot_data = comp[(comp["Sanction Amount"] <= p99_thresh) & (comp["Expenditure Amount"] <= p99_thresh)]
                max_x = p99_thresh * 1.05
                max_y = p99_thresh * 1.05
                is_log = False
            elif "Macro outliers" in scatter_scope:
                plot_data = comp[(comp["Sanction Amount"] > p99_thresh) | (comp["Expenditure Amount"] > p99_thresh)]
                max_x = None
                max_y = None
                is_log = False
            else:
                plot_data = comp[(comp["Sanction Amount"] > 0) & (comp["Expenditure Amount"] > 0)]
                max_x = None
                max_y = None
                is_log = True

            if len(plot_data) > 4000:
                plot_data = plot_data.sample(4000, random_state=42)

            # Unified color rule: Non-risk points in TEAL_BASE (#2B6B6B), overrun in RISK_COLORS['High'] (#B0522D)
            point_colors = np.where(plot_data["Cost Overrun"], RISK_COLORS["High"], TEAL_BASE)

            fig_scatter = go.Figure()

            # 45-degree parity reference line
            if not is_log and max_x is not None:
                fig_scatter.add_trace(
                    go.Scatter(
                        x=[0, max_x],
                        y=[0, max_y],
                        mode="lines",
                        line=dict(color=GRID_COLOR, width=1.5, dash="dash"),
                        name="Parity (exp = sanction)",
                        hoverinfo="skip",
                    )
                )

            fig_scatter.add_trace(
                go.Scatter(
                    x=plot_data["Sanction Amount"],
                    y=plot_data["Expenditure Amount"],
                    mode="markers",
                    marker=dict(
                        color=point_colors,
                        size=6,
                        opacity=0.7,
                        line=dict(color="#1D4A4A", width=0.5),
                    ),
                    customdata=plot_data[["Work ID", "Cost Overrun"]].values,
                    hovertemplate="Work ID: #%{customdata[0]}<br>Sanction: ₹%{x:,.0f}<br>Expenditure: ₹%{y:,.0f}<br>Overrun: %{customdata[1]}<extra></extra>",
                    name="Works record",
                )
            )

            fig_scatter = style_fig(fig_scatter, height=430)
            fig_scatter.update_layout(
                xaxis_title="Sanction amount (₹)",
                yaxis_title="Actual expenditure (₹)",
                margin=dict(l=65, r=25, t=20, b=45),
            )
            if not is_log and max_x is not None:
                fig_scatter.update_xaxes(range=[0, max_x])
                fig_scatter.update_yaxes(range=[0, max_y])
            elif is_log:
                fig_scatter.update_xaxes(type="log")
                fig_scatter.update_yaxes(type="log")

            st.plotly_chart(fig_scatter, width="stretch", config={"displayModeBar": False})

    # Cost Overrun Register Table
    overrun_df = filtered[filtered["Cost Overrun"]].sort_values("Risk Score", ascending=False).copy()
    st.markdown("<div class='section-head'>Cost overrun register</div>", unsafe_allow_html=True)

    if overrun_df.empty:
        st.info("No cost overrun instances detected in the current scope.")
    else:
        overrun_df.insert(0, "SR NO", range(1, len(overrun_df) + 1))
        o_cols = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Display Category", "Work Stage", "Sanction Amount", "Actual Amount", "Risk Score", "Risk Tier", "Risk Reasons"] if c in overrun_df.columns]
        st.dataframe(
            overrun_df[o_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
                "Work ID": st.column_config.TextColumn("Work ID", width="small"),
                "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Risk Tier": st.column_config.TextColumn("Risk tier"),
                "Sanction Amount": st.column_config.NumberColumn("Sanction amt (₹)", format="₹%d"),
                "Actual Amount": st.column_config.NumberColumn("Actual exp (₹)", format="₹%d"),
                "Risk Reasons": st.column_config.TextColumn("Named risk reasons"),
            },
        )

# =========================================================
# VIEW 5: PROJECT MONITORING (TIMELINE AUDIT & LATENCIES)
# =========================================================
elif page == "Project Monitoring":
    render_page_header(
        title="Project Monitoring & Timeline Audit",
        description="Statutory sanction latencies, milestone completion progress, and project delay queues",
        meta_pairs=[
            ("Completion overdue works", f"{int(filtered['Completion Overdue'].sum()):,}"),
            ("Sanction overdue works", f"{int(filtered['Sanction Overdue'].sum()):,}"),
            ("Milestone monitoring status", "Active"),
        ],
    )

    stage_series = filtered["Work Stage"].fillna("Not Reported").astype(str).value_counts().sort_values()
    if PLOTLY_OK:
        st.markdown("<div class='section-head'>Implementation milestone distribution</div>", unsafe_allow_html=True)
        stg_colors = proportional_teal_colors(stage_series.values)
        fig_stg = go.Figure(go.Bar(
            x=stage_series.values,
            y=stage_series.index,
            orientation="h",
            marker=dict(color=stg_colors, line=dict(color="rgba(0,0,0,0.15)", width=0.5)),
            text=[f"{v:,}" for v in stage_series.values],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(family="IBM Plex Mono", color=INK_PRIMARY, size=13),
            hovertemplate="<b>%{y}</b><br>Works: %{x:,}<extra></extra>",
        ))
        fig_stg.update_layout(xaxis_title=None, yaxis_title=None)
        fig_stg = style_fig(fig_stg, height=390)
        fig_stg.update_layout(margin=dict(l=185, r=45, t=15, b=35))
        st.plotly_chart(fig_stg, width="stretch", config={"displayModeBar": False})

    completed_count = int(filtered["Work Stage"].astype(str).str.contains("Complete", case=False, na=False).sum())
    completion_rate = (completed_count / len(filtered) * 100) if len(filtered) else 0

    st.markdown(
        f"""
<div class="ledger-summary-strip">
  <div class="ledger-cell tone-critical">
    <span class="ledger-cell-label">Completion overdue works</span>
    <span class="ledger-cell-val" >{int(filtered['Completion Overdue'].sum()):,}</span>
    <span class="ledger-cell-sub">Operating past stipulated date</span>
  </div>
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">Sanction overdue works</span>
    <span class="ledger-cell-val" >{int(filtered['Sanction Overdue'].sum()):,}</span>
    <span class="ledger-cell-sub">Pending > 75 days</span>
  </div>
  <div class="ledger-cell tone-low">
    <span class="ledger-cell-label">Completed works</span>
    <span class="ledger-cell-val" >{completed_count:,}</span>
    <span class="ledger-cell-sub">Reported finished</span>
  </div>
  <div class="ledger-cell tone-low">
    <span class="ledger-cell-label">Completion rate</span>
    <span class="ledger-cell-val" >{completion_rate:.1f}%</span>
    <span class="ledger-cell-sub">Of active register</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    delay_cases = filtered[filtered["Completion Overdue"] | filtered["Sanction Overdue"]].sort_values("Risk Score", ascending=False).copy()
    st.markdown("<div class='section-head'>Overdue works requiring expedited administrative action</div>", unsafe_allow_html=True)

    if delay_cases.empty:
        st.info("No overdue cases registered under active filters.")
    else:
        delay_cases.insert(0, "SR NO", range(1, len(delay_cases) + 1))
        d_cols = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Work Stage", "Risk Score", "Risk Tier", "Completion Overdue", "Sanction Overdue", "Risk Reasons"] if c in delay_cases.columns]
        st.dataframe(
            delay_cases[d_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
                "Work ID": st.column_config.TextColumn("Work ID", width="small"),
                "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Risk Tier": st.column_config.TextColumn("Risk tier"),
                "Risk Reasons": st.column_config.TextColumn("Named risk reasons"),
            },
        )

# =========================================================
# VIEW 6: WORKS EXPLORER (CASE-FILE DOSSIER & TICK SCALE)
# =========================================================
elif page == "Works Explorer":
    render_page_header(
        title="Works Deep-Dive Explorer & Case Dossier",
        description="Search, inspect, and audit individual MPLADS records with comprehensive attribute breakdown",
        meta_pairs=[
            ("Records in active scope", f"{len(filtered):,}"),
            ("Inspection mode", "Individual case-file dossier"),
            ("Verification standard", "Statutory documentation & field inquiry"),
        ],
    )

    search_query = st.text_input(
        "Search register by work ID, Hon. MP name, constituency, or description keyword",
        placeholder="Type search terms (e.g. 10243, Solar, Road, MP Name)...",
    )

    explorer_view = filtered
    search_cols = [c for c in ["Work ID", "MP Name", "Constituency", "Work Description", "State", "IDA Name"] if c in explorer_view.columns]

    if search_query and search_cols:
        mask = pd.Series(False, index=explorer_view.index)
        for col in search_cols:
            mask |= explorer_view[col].astype(str).str.contains(search_query, case=False, na=False, regex=False)
        explorer_view = explorer_view[mask]

    st.markdown(f"<div style='font-family:\"IBM Plex Mono\", monospace; font-size:13px; color:var(--ink-secondary); margin: 8px 0 16px 0;'>Register matches: <b>{len(explorer_view):,}</b> works found</div>", unsafe_allow_html=True)

    explorer_view_table = explorer_view.copy()
    explorer_view_table.insert(0, "SR NO", range(1, len(explorer_view_table) + 1))
    e_cols = [c for c in ["SR NO", "Work ID", "State", "Constituency", "MP Name", "Display Category", "Work Stage", "Sanction Amount", "Actual Amount", "Risk Score", "Risk Tier", "Anomaly", "Possible Duplicate"] if c in explorer_view_table.columns]
    
    st.dataframe(
        explorer_view_table[e_cols],
        width="stretch",
        hide_index=True,
        column_config={
            "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
            "Work ID": st.column_config.TextColumn("Work ID", width="small"),
            "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
            "Risk Tier": st.column_config.TextColumn("Risk tier"),
            "Sanction Amount": st.column_config.NumberColumn("Sanction amt (₹)", format="₹%d"),
            "Actual Amount": st.column_config.NumberColumn("Actual exp (₹)", format="₹%d"),
        },
    )

    if not explorer_view.empty:
        st.markdown("<div class='section-head'>Individual case-file dossier</div>", unsafe_allow_html=True)
        id_field = "Work ID" if "Work ID" in explorer_view.columns else explorer_view.columns[0]
        sample_indices = list(explorer_view.index[:250])
        
        selected_idx = st.selectbox(
            "Select a work to open official case dossier",
            sample_indices,
            format_func=lambda x: f"Work ID #{explorer_view.loc[x, id_field]} — {explorer_view.loc[x, 'MP Name'] if 'MP Name' in explorer_view.columns else ''} ({explorer_view.loc[x, 'State'] if 'State' in explorer_view.columns else ''})"
        )

        rec = explorer_view.loc[selected_idx]

        # Distinctive 0-100 Horizontal Tick Scale Display
        render_risk_tick_scale(
            score=rec["Risk Score"],
            tier=rec["Risk Tier"],
            reason=rec.get("Risk Reasons", "")
        )

        work_desc = rec.get("Work Description", "Not Provided")
        sanction_val = money(rec.get("Sanction Amount", 0))
        actual_val = money(rec.get("Actual Amount", 0))
        letter_no = rec.get("Letter No", rec.get("letter_no", "N/A"))

        # Formal Case-File Sheet Layout
        st.markdown(
            f"""
<div class="casefile-sheet">
  <div class="casefile-header">
    <div class="casefile-id">Case dossier: Record ID #{rec.get('Work ID', 'N/A')}</div>
    <div class="casefile-sub"><b>Description:</b> {work_desc}</div>
  </div>
  <div class="casefile-grid">
    <div class="casefile-field"><div class="casefile-field-lbl">Hon. MP name</div><div class="casefile-field-val">{rec.get('MP Name', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Constituency</div><div class="casefile-field-val">{rec.get('Constituency', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">State / UT</div><div class="casefile-field-val">{rec.get('State', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Implementation stage</div><div class="casefile-field-val">{rec.get('Work Stage', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Category</div><div class="casefile-field-val">{rec.get('Display Category', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Sanction amount</div><div class="casefile-field-val">{sanction_val}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Actual expenditure</div><div class="casefile-field-val">{actual_val}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Implementing agency (IDA)</div><div class="casefile-field-val">{rec.get('IDA Name', 'N/A')}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Sanction letter no</div><div class="casefile-field-val">{letter_no}</div></div>
    <div class="casefile-field"><div class="casefile-field-lbl">Financial year</div><div class="casefile-field-val">{rec.get('Financial Year', 'N/A')}</div></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

# =========================================================
# VIEW 7: SIMILAR WORKS (DUPLICATE SCREENING REGISTER)
# =========================================================
elif page == "Similar Works":
    render_page_header(
        title="Similar Works & Duplicate Screening Register",
        description="Semantic text clustering and repetitive project descriptions flagged by the NLP similarity model",
        meta_pairs=[
            ("Detection pipeline", "NLP semantic text clustering"),
            ("Flagged duplicate records", f"{duplicate_count:,}"),
            ("Audit scope", "Repetitive project description screening"),
        ],
    )

    dup_df = filtered[filtered["Possible Duplicate"]].copy()
    s_mps = dup_df['MP Name'].nunique() if "MP Name" in dup_df.columns else 0

    st.markdown(
        f"""
<div class="ledger-summary-strip">
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">Flagged duplicate records</span>
    <span class="ledger-cell-val" >{len(dup_df):,}</span>
    <span class="ledger-cell-sub">Semantic text overlap</span>
  </div>
  <div class="ledger-cell">
    <span class="ledger-cell-label">Distinct MPs affected</span>
    <span class="ledger-cell-val" >{s_mps:,}</span>
    <span class="ledger-cell-sub">Parliamentary cohort</span>
  </div>
  <div class="ledger-cell tone-medium">
    <span class="ledger-cell-label">Duplication proportion</span>
    <span class="ledger-cell-val" >{(len(dup_df) / len(filtered) * 100) if len(filtered) else 0:.2f}%</span>
    <span class="ledger-cell-sub">Of active register</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if dup_df.empty:
        st.info("No potential duplicate works detected in the active scope.")
    else:
        if "MP Name" in dup_df.columns:
            mp_filter = st.selectbox("Filter duplicate register by MP name", ["All MPs"] + sorted(dup_df["MP Name"].dropna().astype(str).unique()))
            if mp_filter != "All MPs":
                dup_df = dup_df[dup_df["MP Name"].astype(str) == mp_filter]

        dup_df.insert(0, "SR NO", range(1, len(dup_df) + 1))
        dup_cols = [c for c in ["SR NO", "Work ID", "MP Name", "State", "Constituency", "Work Description", "Display Category", "Risk Score", "Risk Tier"] if c in dup_df.columns]
        
        st.dataframe(
            dup_df[dup_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "SR NO": st.column_config.NumberColumn("Sr no", format="%d", width="small"),
                "Work ID": st.column_config.TextColumn("Work ID", width="small"),
                "Risk Score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Risk Tier": st.column_config.TextColumn("Risk tier"),
            },
        )
        
        st.markdown(
            f"""
<div style="font-family:'IBM Plex Mono', monospace; font-size:13px; color:{INK_SECONDARY}; border:1px solid {GRID_COLOR}; padding:12px 14px; margin-top:16px; background:{PAPER_BG}; line-height:1.45;">
  Audit note: Semantic flags indicate text-level clustering candidates. Field inspection, physical GPS geo-tagging, and site measurement records are required to substantiate physical duplicate claims.
</div>
""",
            unsafe_allow_html=True,
        )


