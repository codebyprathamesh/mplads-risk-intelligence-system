from __future__ import annotations

import io
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="MPLADS Risk Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# Theme / CSS
# ------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

:root {
    --bg: #07111f;
    --panel: #0d1a2b;
    --panel-2: #102238;
    --border: rgba(255,255,255,0.08);
    --muted: #90a4bb;
    --text: #eef5ff;
    --accent: #4fd1c5;
    --accent-2: #7c9cff;
    --critical: #ff6b6b;
    --high: #ff9f43;
    --medium: #f4d35e;
    --low: #4fd1c5;
}

[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 85% 0%, rgba(124,156,255,0.09), transparent 28%),
      radial-gradient(circle at 10% 10%, rgba(79,209,197,0.06), transparent 24%),
      var(--bg);
}

[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: #091626;
    border-right: 1px solid var(--border);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em;
    color: var(--text);
}

.hero {
    padding: 1.1rem 0 0.7rem 0;
}

.eyebrow {
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-size: 0.74rem;
    font-weight: 700;
}

.hero-title {
    font-size: clamp(2rem, 4vw, 3.6rem);
    line-height: 0.98;
    margin: 0.25rem 0 0.7rem;
}

.hero-copy {
    color: #a9bdd3;
    max-width: 850px;
    font-size: 1.02rem;
    line-height: 1.55;
}

.signal-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}

.signal {
    background: rgba(255,255,255,0.045);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.35rem 0.65rem;
    color: #b8c8d8;
    font-size: 0.78rem;
}

.metric-card {
    background: linear-gradient(180deg, rgba(17,35,56,0.96), rgba(10,26,43,0.96));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem 1.05rem;
    min-height: 118px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.14);
}

.metric-label {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.68rem;
    font-weight: 700;
}

.metric-value {
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin-top: 0.25rem;
}

.metric-note {
    color: #71879e;
    font-size: 0.78rem;
    margin-top: 0.2rem;
}

.section-kicker {
    color: var(--accent-2);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.7rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 0.7rem;
}

.alert-box {
    background: rgba(255,159,67,0.08);
    border: 1px solid rgba(255,159,67,0.23);
    border-radius: 14px;
    padding: 0.8rem 0.9rem;
    color: #e9c79f;
    font-size: 0.84rem;
}

.clean-box {
    background: rgba(79,209,197,0.065);
    border: 1px solid rgba(79,209,197,0.16);
    border-radius: 14px;
    padding: 0.9rem;
}

.queue-card {
    background: #0c1a2c;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.8rem;
}

.queue-title {
    color: #f1f6fd;
    font-weight: 700;
    font-size: 0.9rem;
}

.queue-meta {
    color: #788da4;
    font-size: 0.74rem;
    margin-top: 0.15rem;
}

.reason-chip {
    display: inline-block;
    border-radius: 6px;
    padding: 0.22rem 0.42rem;
    margin: 0.18rem 0.12rem 0 0;
    background: rgba(124,156,255,0.09);
    color: #afbefa;
    font-size: 0.69rem;
    border: 1px solid rgba(124,156,255,0.12);
}

[data-testid="stMetricValue"] {
    color: var(--text);
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(124,156,255,0.2);
    background: rgba(124,156,255,0.08);
    color: #dbe5ff;
}

.stButton > button:hover {
    border-color: rgba(124,156,255,0.45);
    color: white;
}

div[data-baseweb="select"] > div {
    background: #0c1a2b;
    border-color: var(--border);
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

.footer-note {
    border-top: 1px solid var(--border);
    margin-top: 2rem;
    padding-top: 1rem;
    color: #70869e;
    font-size: 0.75rem;
}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Data layer
# ------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent

# The deployed app lives in repo/v1/app.py while the scored dataset
# lives in repo/data/MPLAD_cleaned_v2.csv. Keep several fallbacks so the
# same app also works locally and when the repository layout changes.
DATA_PATHS = [
    APP_DIR.parent / "data" / "MPLAD_cleaned_v2.csv",  # repo/v1/app.py -> repo/data/
    APP_DIR / "data" / "MPLAD_cleaned_v2.csv",
    APP_DIR / "MPLAD_cleaned_v2.csv",
    Path.cwd() / "data" / "MPLAD_cleaned_v2.csv",
    Path.cwd() / "MPLAD_cleaned_v2.csv",
]

DEFAULT_DATA_PATH = DATA_PATHS[0]

GITHUB_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "codebyprathamesh/mplads-risk-intelligence-system/"
    "main/data/MPLAD_cleaned_v2.csv"
)

REQUIRED_COLUMNS = [
    "work_id", "mp_name", "state_name", "constituency", "activity_name",
    "work_description", "work_stage", "recommended_amount", "sanction_amount",
    "actual_amount", "recommendation_date", "sanction_date",
    "funnel_status", "days_since_recommendation", "days_since_sanction",
    "sanction_overdue", "completion_overdue", "cost_overrun",
    "simple_category", "amount_percentile", "high_cost_outlier",
    "missing_description", "sanction_amount_missing", "risk_score", "risk_tier",
    "risk_reason", "anomaly_flag", "anomaly_score", "possible_duplicate",
]

RISK_ORDER = ["Critical", "High", "Medium", "Low", "No Risk"]
RISK_SCORE = {"No Risk": 0, "Low": 1, "Medium": 2, "High": 3, "Critical": 4}

FLAG_META = {
    "completion_overdue": ("Completion overdue", ">365 days after sanction"),
    "sanction_overdue": ("Sanction overdue", ">75 days after recommendation"),
    "high_cost_outlier": ("High-cost outlier", ">95th percentile in peer group"),
    "missing_description": ("Missing description", "Work description unavailable"),
    "sanction_amount_missing": ("Missing sanction amount", "Sanction amount is blank"),
    "possible_duplicate": ("Duplicate-like match", "Description similarity >0.85 within MP"),
    "anomaly_flag": ("ML anomaly", "Isolation Forest flagged record"),
    "cost_overrun": ("Cost overrun", ">10% over recommended amount"),
}


@st.cache_data(show_spinner=False)
def load_data(source: str | None = None) -> pd.DataFrame:
    # 1. Explicit source (including an uploaded CSV).
    if source:
        source_path = Path(source)
        if source_path.exists() and source_path.is_file():
            df = pd.read_csv(source_path, low_memory=False)
        else:
            raise FileNotFoundError(f"Dataset not found at: {source_path}")
    else:
        df = None

        # 2. Repository/local paths.
        for path in DATA_PATHS:
            try:
                if path.exists() and path.is_file():
                    candidate = pd.read_csv(path, low_memory=False)
                    if not candidate.empty:
                        df = candidate
                        break
            except Exception:
                continue

        # 3. GitHub fallback for Streamlit Cloud.
        if df is None:
            try:
                import urllib.request

                with urllib.request.urlopen(GITHUB_DATA_URL, timeout=30) as response:
                    raw_data = response.read()
                df = pd.read_csv(io.BytesIO(raw_data), low_memory=False)
            except Exception as exc:
                raise FileNotFoundError(
                    "No dataset found locally and the GitHub dataset could not be loaded."
                ) from exc
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {', '.join(missing)}")

    for col in [
        "recommended_amount", "sanction_amount", "actual_amount", "risk_score",
        "days_since_recommendation", "days_since_sanction", "amount_percentile",
        "anomaly_score",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in [
        "sanction_overdue", "completion_overdue", "cost_overrun", "high_cost_outlier",
        "missing_description", "sanction_amount_missing", "anomaly_flag", "possible_duplicate",
    ]:
        df[col] = df[col].fillna(False).astype(bool)

    for col in ["recommendation_date", "sanction_date", "actual_end_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["risk_tier"] = pd.Categorical(df["risk_tier"], categories=RISK_ORDER, ordered=True)
    df["risk_rank"] = df["risk_tier"].map(RISK_SCORE).fillna(0).astype(int)
    df["recommendation_date_str"] = df["recommendation_date"].dt.strftime("%d %b %Y").fillna("—")
    df["sanction_date_str"] = df["sanction_date"].dt.strftime("%d %b %Y").fillna("—")
    df["amount_display"] = df["recommended_amount"].map(format_inr)
    return df


def format_inr(value: float | int | None) -> str:
    if pd.isna(value):
        return "—"
    value = float(value)
    if abs(value) >= 1e7:
        return f"₹{value/1e7:.2f} Cr"
    if abs(value) >= 1e5:
        return f"₹{value/1e5:.2f} L"
    if abs(value) >= 1e3:
        return f"₹{value/1e3:.1f} K"
    return f"₹{value:,.0f}"


def compact_number(value: int | float) -> str:
    value = float(value)
    if abs(value) >= 1e6:
        return f"{value/1e6:.1f}M"
    if abs(value) >= 1e3:
        return f"{value/1e3:.1f}K"
    return f"{value:,.0f}"


def risk_color(tier: str) -> str:
    return {
        "Critical": "#ff6b6b",
        "High": "#ff9f43",
        "Medium": "#f4d35e",
        "Low": "#4fd1c5",
        "No Risk": "#51677f",
    }.get(str(tier), "#51677f")


def humanize_reason(reason: str, limit: int = 3) -> list[str]:
    if not isinstance(reason, str) or not reason.strip() or reason == "No major risks.":
        return []
    pieces = []
    for chunk in reason.split("."):
        chunk = chunk.strip()
        if chunk:
            pieces.append(chunk)
    return pieces[:limit]


def issue_labels(row: pd.Series) -> list[str]:
    labels = []
    for key, (name, _) in FLAG_META.items():
        if bool(row.get(key, False)):
            labels.append(name)
    return labels


def make_risk_bar(series: pd.Series, title: str) -> go.Figure:
    counts = series.value_counts().reindex(RISK_ORDER).fillna(0).astype(int)
    fig = go.Figure(
        go.Bar(
            x=counts.index,
            y=counts.values,
            marker_color=[risk_color(x) for x in counts.index],
            hovertemplate="%{x}: %{y:,}<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        height=320,
        margin=dict(l=0, r=0, t=44, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b8c8d8"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
    )
    return fig


def apply_filters(
    df: pd.DataFrame,
    state: str,
    mp: str,
    category: str,
    tiers: Iterable[str],
    only_attention: bool,
    search: str,
) -> pd.DataFrame:
    out = df
    if state != "All states":
        out = out[out["state_name"] == state]
    if mp != "All MPs":
        out = out[out["mp_name"] == mp]
    if category != "All categories":
        out = out[out["simple_category"] == category]
    if tiers:
        out = out[out["risk_tier"].astype(str).isin(tiers)]
    if only_attention:
        out = out[out["risk_score"] > 0]
    if search.strip():
        needle = search.strip().lower()
        mask = (
            out["work_id"].astype(str).str.lower().str.contains(needle, na=False)
            | out["mp_name"].astype(str).str.lower().str.contains(needle, na=False)
            | out["constituency"].astype(str).str.lower().str.contains(needle, na=False)
            | out["activity_name"].astype(str).str.lower().str.contains(needle, na=False)
            | out["work_description"].astype(str).str.lower().str.contains(needle, na=False)
        )
        out = out[mask]
    return out


def render_filters(df: pd.DataFrame, key_prefix: str = "global") -> pd.DataFrame:
    with st.sidebar:
        st.markdown("### Control room")
        st.caption("Shape the evidence set without changing the underlying risk logic.")

        state_options = ["All states"] + sorted(df["state_name"].dropna().astype(str).unique().tolist())
        state = st.selectbox("State", state_options, key=f"{key_prefix}_state")

        mp_pool = df if state == "All states" else df[df["state_name"] == state]
        mp_options = ["All MPs"] + sorted(mp_pool["mp_name"].dropna().astype(str).unique().tolist())
        mp = st.selectbox("MP", mp_options, key=f"{key_prefix}_mp")

        cat_options = ["All categories"] + sorted(df["simple_category"].dropna().astype(str).unique().tolist())
        category = st.selectbox("Work category", cat_options, key=f"{key_prefix}_cat")

        tiers = st.multiselect(
            "Risk tiers",
            RISK_ORDER,
            default=["Critical", "High", "Medium", "Low"],
            key=f"{key_prefix}_tiers",
        )
        only_attention = st.toggle("Attention queue only", value=True, key=f"{key_prefix}_attention")
        search = st.text_input("Search works / MP / constituency", key=f"{key_prefix}_search")

        st.markdown("---")
        st.markdown("**Signal coverage**")
        st.caption("Rule layer + ML anomaly layer + duplicate-like similarity layer")

    return apply_filters(df, state, mp, category, tiers, only_attention, search)


# ------------------------------------------------------------
# Source resolution
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("# ◈ MPLADS")
    st.caption("RISK INTELLIGENCE / DECISION SUPPORT")

    uploaded = st.file_uploader("Use another scored CSV", type=["csv"], help="Your scored CSV should contain the risk columns produced by your notebook.")

if uploaded is not None:
    source_bytes = uploaded.getvalue()
    source_path = Path(st.session_state.get("uploaded_path", APP_DIR / "_uploaded_scored.csv"))
    source_path.write_bytes(source_bytes)
    source = str(source_path)
    source_label = uploaded.name
else:
    source = None
    source_label = "Repository / GitHub dataset"


# ------------------------------------------------------------
# Load
# ------------------------------------------------------------
try:
    df = load_data(source)
except Exception as exc:
    st.error(f"Could not load the scored dataset: {exc}")
    st.stop()


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------
with st.sidebar:
    page = st.radio(
        "Navigate",
        ["Command Center", "Attention Queue", "Work Explorer", "MP & State Lens", "Risk Method"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption(f"Source · {source_label}")
    st.caption(f"Records · {len(df):,}")
    st.caption("Human review support · Not a fraud verdict")

filtered = render_filters(df, key_prefix=page.lower().replace(" ", "_"))


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="eyebrow">MPLADS / RISK INTELLIGENCE SYSTEM</div>
  <div class="hero-title">From 103K works to a review queue.</div>
  <div class="hero-copy">
    Surface the works that deserve attention first, then show the evidence behind each signal.
    The system combines deterministic risk rules with an ML anomaly layer and duplicate-like
    similarity detection to help human reviewers focus their time.
  </div>
  <div class="signal-strip">
    <span class="signal">Rule-based risk score</span>
    <span class="signal">Isolation Forest anomalies</span>
    <span class="signal">TF-IDF duplicate-like similarity</span>
    <span class="signal">Stage / funnel tracking</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Command Center
# ------------------------------------------------------------
def command_center(view: pd.DataFrame) -> None:
    risked = view[view["risk_score"] > 0]
    critical = int((view["risk_tier"].astype(str) == "Critical").sum())
    high = int((view["risk_tier"].astype(str) == "High").sum())
    anomalous = int(view["anomaly_flag"].sum())
    dupes = int(view["possible_duplicate"].sum())
    sanction_overdue = int(view["sanction_overdue"].sum())
    completion_overdue = int(view["completion_overdue"].sum())

    cols = st.columns(5)
    cards = [
        ("Works in view", compact_number(len(view)), "filtered evidence set"),
        ("Attention required", compact_number(len(risked)), f"{(len(risked)/len(view)*100 if len(view) else 0):.1f}% of view"),
        ("High + Critical", compact_number(high + critical), "highest-priority review tier"),
        ("ML anomalies", compact_number(anomalous), "Isolation Forest flags"),
        ("Duplicate-like", compact_number(dupes), "similar-description flags"),
    ]
    for col, (label, value, note) in zip(cols, cards):
        with col:
            st.markdown(
                f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>",
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown("### What deserves attention?")
    st.markdown("<div class='section-subtitle'>The queue is intentionally ordered by explainable risk, not by a black-box probability.</div>", unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.5])
    with left:
        st.plotly_chart(make_risk_bar(view["risk_tier"].astype(str), "Risk tier distribution"), use_container_width=True, config={"displayModeBar": False})
    with right:
        funnel = view["funnel_status"].value_counts().rename_axis("status").reset_index(name="works")
        fig = px.bar(funnel, x="works", y="status", orientation="h", title="Workflow funnel")
        fig.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=44, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b8c8d8"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### Review pressure points")
    pressure = pd.DataFrame({
        "Signal": ["Completion overdue", "Sanction overdue", "ML anomaly", "Duplicate-like", "High-cost outlier", "Missing description", "Missing sanction amount", "Cost overrun"],
        "Flags": [
            completion_overdue,
            sanction_overdue,
            anomalous,
            dupes,
            int(view["high_cost_outlier"].sum()),
            int(view["missing_description"].sum()),
            int(view["sanction_amount_missing"].sum()),
            int(view["cost_overrun"].sum()),
        ],
    }).sort_values("Flags", ascending=True)
    fig = px.bar(pressure, x="Flags", y="Signal", orientation="h", text="Flags")
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(height=360, margin=dict(l=0, r=20, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#b8c8d8"), xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"), yaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### Why this queue is different")
    a, b = st.columns(2)
    with a:
        st.markdown("<div class='clean-box'><b>Not a verdict engine.</b><br><span style='color:#8da4bb;font-size:.82rem;'>A high score means the work has more observable risk signals. It is a prioritization mechanism for human review.</span></div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='alert-box'><b>Data-quality visibility.</b><br><span style='color:#cfb58f;font-size:.82rem;'>Cost-overrun is currently 0 in this scored dataset. The interface shows that honestly instead of inferring missing financial behavior.</span></div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# Attention Queue
# ------------------------------------------------------------
def attention_queue(view: pd.DataFrame) -> None:
    queue = view[view["risk_score"] > 0].copy()
    if queue.empty:
        st.info("No works match the current attention filters.")
        return

    queue = queue.sort_values(["risk_rank", "risk_score", "anomaly_flag", "possible_duplicate"], ascending=[False, False, False, False]).head(150)

    st.markdown("### Attention queue")
    st.markdown("<div class='section-subtitle'>A reviewer can start at the top, inspect the explanation, and decide whether to escalate, verify, or close the item.</div>", unsafe_allow_html=True)

    cols = st.columns([1.4, 0.7, 0.9, 1.5, 0.9, 1.0])
    headers = ["Work", "Risk", "MP", "Signals", "Stage", "Score"]
    for c, h in zip(cols, headers):
        c.markdown(f"**{h}**")

    for _, row in queue.iterrows():
        labels = issue_labels(row)
        signal_text = " · ".join(labels[:3]) + (" · +more" if len(labels) > 3 else "")
        cols = st.columns([1.4, 0.7, 0.9, 1.5, 0.9, 1.0])
        cols[0].markdown(f"**{row['work_id']}**  \n<span style='color:#71869d;font-size:.72rem'>{str(row['activity_name'])[:80]}</span>", unsafe_allow_html=True)
        cols[1].markdown(f"<span style='color:{risk_color(str(row['risk_tier']))};font-weight:700'>{row['risk_tier']}</span>", unsafe_allow_html=True)
        cols[2].markdown(str(row["mp_name"])[:28])
        cols[3].markdown(f"<span style='color:#9eb2c8;font-size:.74rem'>{signal_text}</span>", unsafe_allow_html=True)
        cols[4].markdown(f"<span style='color:#9eb2c8;font-size:.74rem'>{str(row['funnel_status']).replace('-', ' · ')}</span>", unsafe_allow_html=True)
        cols[5].markdown(f"**{int(row['risk_score'])}/100**")

        with st.expander(f"Inspect {row['work_id']} — evidence trail"):
            l, r = st.columns([1.25, 1])
            with l:
                st.markdown("**Why it was flagged**")
                reasons = humanize_reason(row["risk_reason"])
                if reasons:
                    for reason in reasons:
                        st.markdown(f"<span class='reason-chip'>{reason}</span>", unsafe_allow_html=True)
                else:
                    st.caption("No rule-based risk reason recorded.")
                st.markdown("**Work description**")
                st.write(row["work_description"] if pd.notna(row["work_description"]) else "Description unavailable.")
            with r:
                evidence = pd.DataFrame({
                    "Evidence": [
                        "Risk score", "Risk tier", "ML anomaly", "Duplicate-like", "Recommendation date", "Sanction date",
                        "Recommended amount", "Sanction amount", "Actual amount", "Days since recommendation", "Days since sanction",
                    ],
                    "Value": [
                        f"{int(row['risk_score'])}/100", str(row["risk_tier"]), "Yes" if row["anomaly_flag"] else "No",
                        "Yes" if row["possible_duplicate"] else "No", row["recommendation_date_str"], row["sanction_date_str"],
                        format_inr(row["recommended_amount"]), format_inr(row["sanction_amount"]), format_inr(row["actual_amount"]),
                        f"{int(row['days_since_recommendation']):,}" if pd.notna(row["days_since_recommendation"]) else "—",
                        f"{int(row['days_since_sanction']):,}" if pd.notna(row["days_since_sanction"]) else "—",
                    ],
                })
                st.dataframe(evidence, hide_index=True, use_container_width=True, height=340)


# ------------------------------------------------------------
# Work Explorer
# ------------------------------------------------------------
def work_explorer(view: pd.DataFrame) -> None:
    st.markdown("### Work explorer")
    st.markdown("<div class='section-subtitle'>Move from system-level signals into individual records. Filters are preserved from the sidebar.</div>", unsafe_allow_html=True)

    if view.empty:
        st.info("No records match the current filters.")
        return

    display_cols = [
        "work_id", "mp_name", "state_name", "constituency", "simple_category", "work_stage",
        "recommended_amount", "risk_score", "risk_tier", "anomaly_flag", "possible_duplicate",
    ]
    table = view[display_cols].copy().sort_values(["risk_rank", "risk_score"], ascending=[False, False])
    table["recommended_amount"] = table["recommended_amount"].map(format_inr)
    table.columns = [
        "Work ID", "MP", "State", "Constituency", "Category", "Stage",
        "Recommended", "Risk score", "Risk tier", "ML anomaly", "Duplicate-like",
    ]

    st.dataframe(
        table.head(300),
        hide_index=True,
        use_container_width=True,
        height=560,
        column_config={
            "Risk score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d"),
            "Recommended": st.column_config.TextColumn("Recommended"),
            "ML anomaly": st.column_config.CheckboxColumn("ML anomaly"),
            "Duplicate-like": st.column_config.CheckboxColumn("Duplicate-like"),
        },
    )

    export = view.copy()
    export = export.drop(columns=[c for c in export.columns if c.endswith("_str") or c in ["risk_rank", "amount_display"]], errors="ignore")
    st.download_button(
        "Download current evidence set",
        data=export.to_csv(index=False).encode("utf-8"),
        file_name="mplads_risk_evidence.csv",
        mime="text/csv",
    )


# ------------------------------------------------------------
# MP & State Lens
# ------------------------------------------------------------
def mp_state_lens(view: pd.DataFrame) -> None:
    st.markdown("### MP & state lens")
    st.markdown("<div class='section-subtitle'>Compare where attention signals cluster. Counts are descriptive; they are not a judgment about an MP or state.</div>", unsafe_allow_html=True)

    state_summary = (
        view.groupby("state_name", dropna=False)
        .agg(
            works=("work_id", "count"),
            attention=("risk_score", lambda s: int((s > 0).sum())),
            high_critical=("risk_score", lambda s: int((s >= 31).sum())),
            anomalies=("anomaly_flag", "sum"),
            duplicate_like=("possible_duplicate", "sum"),
            total_risk=("risk_score", "sum"),
        )
        .reset_index()
    )
    state_summary["attention_rate"] = np.where(state_summary["works"] > 0, state_summary["attention"] / state_summary["works"] * 100, 0)

    left, right = st.columns(2)
    with left:
        top = state_summary.sort_values("total_risk", ascending=False).head(12)
        fig = px.bar(top.sort_values("total_risk"), x="total_risk", y="state_name", orientation="h", title="Highest total risk score by state")
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=44, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#b8c8d8"), xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"), yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right:
        top = state_summary.sort_values("attention_rate", ascending=False).head(12)
        fig = px.bar(top.sort_values("attention_rate"), x="attention_rate", y="state_name", orientation="h", title="Attention rate within state")
        fig.update_traces(hovertemplate="%{y}: %{x:.1f}%<extra></extra>")
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=44, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#b8c8d8"), xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", ticksuffix="%"), yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### MP review concentration")
    mp_summary = (
        view.groupby("mp_name", dropna=False)
        .agg(
            works=("work_id", "count"),
            attention=("risk_score", lambda s: int((s > 0).sum())),
            risk_score=("risk_score", "sum"),
            anomalies=("anomaly_flag", "sum"),
        )
        .reset_index()
        .sort_values(["risk_score", "attention"], ascending=False)
        .head(30)
    )
    st.dataframe(mp_summary, hide_index=True, use_container_width=True, height=420)


# ------------------------------------------------------------
# Method / explainability
# ------------------------------------------------------------
def risk_method() -> None:
    st.markdown("### Risk method")
    st.markdown("<div class='section-subtitle'>A transparent account of the logic already present in your scored CSV.</div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("#### Rule layer")
        rules = pd.DataFrame([
            ["Completion overdue", "+30", "Sanctioned but not completed and >365 days since sanction"],
            ["Cost overrun", "+10 / +18 / +25", "Actual >110% of recommended, with severity by overrun"],
            ["High-cost outlier", "+15", ">95th percentile within state + work category"],
            ["Missing description", "+10", "Description is null or blank"],
            ["Sanction overdue", "+15", "Recommended but not sanctioned after 75 days"],
            ["Sanction amount missing", "+5", "Sanction amount missing"],
        ], columns=["Signal", "Score", "Condition"])
        st.dataframe(rules, hide_index=True, use_container_width=True)

        st.markdown("#### Risk bands")
        bands = pd.DataFrame([
            ["0", "No Risk"], ["1–15", "Low"], ["16–30", "Medium"], ["31–45", "High"], [">45", "Critical"]
        ], columns=["Score", "Tier"])
        st.dataframe(bands, hide_index=True, use_container_width=True)

    with right:
        st.markdown("#### ML anomaly layer")
        st.markdown("""
<div class='clean-box'>
<b>Isolation Forest</b><br>
<span style='color:#94a9c0;font-size:.82rem;'>
Features: recommended amount, sanction amount, actual amount, amount percentile,
 days since recommendation, and days since sanction. Missing numeric values are filled with -1.
</span>
</div>
""", unsafe_allow_html=True)
        st.write("")
        st.markdown("#### Duplicate-like layer")
        st.markdown("""
<div class='clean-box'>
<b>TF-IDF + cosine similarity</b><br>
<span style='color:#94a9c0;font-size:.82rem;'>
Descriptions are compared within each MP. A record is flagged when any other description in that MP group reaches similarity above 0.85.
</span>
</div>
""", unsafe_allow_html=True)
        st.write("")
        st.markdown("#### Interpretation rule")
        st.markdown("""
<div class='alert-box'>
A flag is an <b>investigation signal</b>, not proof of wrongdoing. The strongest workflow is:<br><br>
<strong>Prioritize → Inspect evidence → Verify source documents → Decide action</strong>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Routing
# ------------------------------------------------------------
if page == "Command Center":
    command_center(filtered)
elif page == "Attention Queue":
    attention_queue(filtered)
elif page == "Work Explorer":
    work_explorer(filtered)
elif page == "MP & State Lens":
    mp_state_lens(filtered)
elif page == "Risk Method":
    risk_method()


st.markdown(
    """
<div class='footer-note'>
  <b>MPLADS Risk Intelligence</b> · Decision-support interface for prioritizing human review.<br>
  The current interface presents the scored dataset as supplied; it does not establish fraud, corruption, or wrongdoing.
</div>
""",
    unsafe_allow_html=True,
)
