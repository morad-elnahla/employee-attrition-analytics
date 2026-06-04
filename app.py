import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Employee Attrition · Kayfa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

import io
from PIL import Image

def _clean_logo(path):
    try:
        img = Image.open(path).convert("RGBA")
        arr = np.array(img)
        white = (arr[:,:,0] > 230) & (arr[:,:,1] > 230) & (arr[:,:,2] > 230)
        arr[white, 3] = 0
        buf = io.BytesIO()
        Image.fromarray(arr).save(buf, "PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return ""

LOGO_B64 = _clean_logo("logo.png")
LOGO_IMG  = f'<img src="data:image/png;base64,{LOGO_B64}" style="{{s}}">'

# ── Palette ────────────────────────────────────────────────────────────────────
LEFT    = "#f87171"
STAYED  = "#6366f1"
PRIMARY = "#6366f1"
ACCENT  = "#3D3DB4"
BG      = "#07081a"
CARD_BG = "rgba(99,102,241,0.07)"
BORDER  = "rgba(99,102,241,0.22)"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html,body,[class*="css"],.stApp {{
    font-family:'Plus Jakarta Sans',sans-serif !important;
    background:{BG} !important;
    color:#e2e8f0 !important;
}}
.main .block-container {{
    padding-top:1.5rem !important;
    padding-bottom:3rem !important;
    max-width:1380px !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background:#0b0c22 !important;
    border-right:1px solid rgba(99,102,241,0.12) !important;
}}
[data-testid="stSidebar"] * {{ color:#c7d0e8 !important; }}
[data-testid="stSidebar"] .stMultiSelect label {{
    color:#4a5480 !important;
    font-size:0.68rem !important;
    letter-spacing:0.1em !important;
    text-transform:uppercase !important;
    font-weight:700 !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background:rgba(99,102,241,0.18) !important;
    border:1px solid rgba(99,102,241,0.35) !important;
    border-radius:6px !important;
    color:#a5b4fc !important;
}}

/* ── KPI cards ── */
.kpi-card {{
    background:{CARD_BG};
    border:1px solid {BORDER};
    border-radius:14px;
    padding:1.3rem 1.6rem;
    position:relative;
    overflow:hidden;
    height:100%;
}}
.kpi-card::after {{
    content:'';
    position:absolute;
    top:0;left:0;right:0;
    height:2px;
    background:linear-gradient(90deg,#3D3DB4,#6366f1,#818cf8);
}}
.kpi-label {{
    color:#374060;
    font-size:0.67rem;
    font-weight:700;
    letter-spacing:0.11em;
    text-transform:uppercase;
    margin-bottom:0.55rem;
}}
.kpi-value {{
    font-size:2.15rem;
    font-weight:800;
    line-height:1;
    margin-bottom:0.3rem;
    color:#e2e8f0;
}}
.kpi-blue  {{ color:#818cf8; }}
.kpi-red   {{ color:#f87171; }}
.kpi-green {{ color:#34d399; }}
.kpi-sub   {{ color:#374060; font-size:0.74rem; font-weight:500; }}

/* ── Section header ── */
.sec-head {{
    display:flex;
    align-items:center;
    gap:0.75rem;
    margin:2rem 0 0.9rem;
}}
.sec-title {{
    font-size:0.72rem;
    font-weight:700;
    color:#6366f1;
    letter-spacing:0.12em;
    text-transform:uppercase;
    white-space:nowrap;
}}
.sec-line {{
    flex:1;
    height:1px;
    background:linear-gradient(90deg,rgba(99,102,241,0.3),transparent);
}}

/* ── Insight box ── */
.insight {{
    background:rgba(99,102,241,0.05);
    border:1px solid rgba(99,102,241,0.12);
    border-left:3px solid #6366f1;
    border-radius:0 10px 10px 0;
    padding:0.85rem 1.15rem;
    margin-top:0.3rem;
    font-size:0.83rem;
    color:#94a3b8;
    line-height:1.65;
}}
.itag {{
    display:inline-block;
    background:rgba(99,102,241,0.14);
    color:#818cf8;
    font-size:0.66rem;
    font-weight:700;
    letter-spacing:0.08em;
    text-transform:uppercase;
    padding:0.15rem 0.55rem;
    border-radius:4px;
    margin-bottom:0.45rem;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background:transparent !important;
    border-bottom:1px solid rgba(99,102,241,0.18) !important;
    gap:0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    background:transparent !important;
    border:none !important;
    color:#374060 !important;
    font-weight:600 !important;
    font-size:0.82rem !important;
    padding:0.6rem 1.3rem !important;
    letter-spacing:0.03em !important;
}}
.stTabs [aria-selected="true"] {{
    color:#818cf8 !important;
    border-bottom:2px solid #6366f1 !important;
    background:transparent !important;
}}

/* ── Misc ── */
hr {{ border-color:rgba(99,102,241,0.1) !important; }}
[data-testid="stDataFrame"] {{ border-radius:10px; overflow:hidden; }}
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.concat([pd.read_csv("train.csv"), pd.read_csv("test.csv")], ignore_index=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ","_").str.replace("-","_")
    for col, order in {
        "work_life_balance"   : ["Poor","Fair","Good","Excellent"],
        "job_satisfaction"    : ["Low","Medium","High","Very High"],
        "job_level"           : ["Entry","Mid","Senior"],
        "employee_recognition": ["Low","Medium","High","Very High"],
    }.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)
    df["attrition_flag"] = (df["attrition"] == "Left").astype(int)
    return df

df_all = load_data()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="padding:0 0.25rem 1.8rem">'
        f'{LOGO_IMG.format(s="width:150px")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#2a3050;font-size:0.66rem;font-weight:700;'
        'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.7rem">Filters</p>',
        unsafe_allow_html=True,
    )

    level_sel = st.multiselect(
        "Job Level", ["Entry","Mid","Senior"], default=["Entry","Mid","Senior"]
    )
    remote_sel = st.multiselect(
        "Remote Work",
        sorted(df_all["remote_work"].dropna().unique()),
        default=sorted(df_all["remote_work"].dropna().unique()),
    )
    gender_sel = st.multiselect(
        "Gender",
        sorted(df_all["gender"].dropna().unique()),
        default=sorted(df_all["gender"].dropna().unique()),
    )
    overtime_sel = st.multiselect(
        "Overtime",
        sorted(df_all["overtime"].dropna().unique()),
        default=sorted(df_all["overtime"].dropna().unique()),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#1e2340;font-size:0.7rem;line-height:1.7;'
        'border-top:1px solid rgba(99,102,241,0.08);padding-top:0.9rem">'
        'AI & Data Analytics Internship<br>Month 1 · Week 1 · Data Analytics Track</p>',
        unsafe_allow_html=True,
    )

# ── Guard: empty filter ────────────────────────────────────────────────────────
if not all([level_sel, remote_sel, gender_sel, overtime_sel]):
    st.warning("⚠️ Select at least one option in each filter.")
    st.stop()

df = df_all[
    df_all["job_level"].isin(level_sel) &
    df_all["remote_work"].isin(remote_sel) &
    df_all["gender"].isin(gender_sel) &
    df_all["overtime"].isin(overtime_sel)
].copy()


# ── Helpers ────────────────────────────────────────────────────────────────────
def group_attrition(col):
    g = (
        df.groupby(col, observed=True)["attrition_flag"]
        .agg(total="count", left="sum").reset_index()
    )
    g["rate"] = (g["left"] / g["total"] * 100).round(1)
    return g

def qlayout(fig, h=360):
    fig.update_layout(
        height=h,
        margin=dict(t=46,b=12,l=10,r=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        font=dict(family="Plus Jakarta Sans", color="#64748b", size=11),
        title_font=dict(family="Plus Jakarta Sans", color="#c7d0e8", size=13, weight=600),
    )
    fig.update_xaxes(gridcolor="rgba(99,102,241,0.07)", linecolor="rgba(99,102,241,0.1)",
                     zeroline=False)
    fig.update_yaxes(gridcolor="rgba(99,102,241,0.07)", linecolor="rgba(99,102,241,0.1)",
                     zeroline=False)
    return fig

def insight(emoji, tag, text):
    return (f"<div class='insight'>"
            f"<div class='itag'>{emoji} {tag}</div><br>{text}</div>")

def sec(title):
    return (f"<div class='sec-head'>"
            f"<span class='sec-title'>{title}</span>"
            f"<span class='sec-line'></span></div>")

CMAP  = ["#6366f1","#818cf8","#a5b4fc","#f87171"]
CMAP2 = ["#34d399","#818cf8","#f87171"]


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:1rem;padding:0.4rem 0 0.6rem">
  {LOGO_IMG.format(s="height:44px;flex-shrink:0")}

  <div>
    <div style="font-size:1.55rem;font-weight:800;color:#e2e8f0;
                letter-spacing:-0.02em;line-height:1.1">
      Employee Attrition Analytics
    </div>
    <div style="color:#2a3458;font-size:0.78rem;margin-top:0.2rem;font-weight:500">
      74,498 synthetic employee records &nbsp;·&nbsp;
      Kayfa AI & Data Analytics &nbsp;·&nbsp; Week 1
    </div>
  </div>
</div>
<hr style="margin:0.4rem 0 1.2rem">
""", unsafe_allow_html=True)


# ── KPIs ───────────────────────────────────────────────────────────────────────
total      = len(df)
left_count = int(df["attrition_flag"].sum())
rate       = left_count / total * 100 if total else 0

entry_df   = group_attrition("job_level")
entry_row  = entry_df[entry_df["job_level"] == "Entry"]
entry_pct  = f'{entry_row["rate"].values[0]:.1f}%' if len(entry_row) else "—"

remote_df  = group_attrition("remote_work")
remote_row = remote_df[remote_df["remote_work"] == "Yes"]
remote_pct = f'{remote_row["rate"].values[0]:.1f}%' if len(remote_row) else "—"

rate_cls = "kpi-red" if rate > 45 else "kpi-green" if rate < 30 else "kpi-blue"

c1, c2, c3, c4 = st.columns(4)
for col, label, val, cls, sub in [
    (c1, "Headcount",       f"{total:,}",       "kpi-blue",  f"of {len(df_all):,} total"),
    (c2, "Attrition Rate",  f"{rate:.1f}%",     rate_cls,    "filtered selection"),
    (c3, "Entry-Level Risk",entry_pct,           "kpi-red",   "highest risk segment"),
    (c4, "Remote Attrition",remote_pct,          "kpi-green", "lowest risk segment"),
]:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value {cls}'>{val}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔑  Key Drivers",
    "💡  Supporting Factors",
    "📊  Risk Overview",
])

CMAP_BAR = ["#3D3DB4","#6366f1","#818cf8","#a78bfa"]

# ─── Tab 1: Key Drivers ────────────────────────────────────────────────────────
with tab1:
    st.markdown(sec("Seniority & Burnout"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        grp = group_attrition("job_level")
        fig = px.bar(grp, x="job_level", y="rate",
                     color="rate", color_continuous_scale=CMAP,
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","job_level":""},
                     title="Attrition by Job Level",
                     category_orders={"job_level":["Entry","Mid","Senior"]})
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(yaxis_range=[0,100], coloraxis_showscale=False)
        st.plotly_chart(qlayout(fig), use_container_width=True)

    with col2:
        grp = group_attrition("overtime")
        fig = px.bar(grp, x="overtime", y="rate",
                     color="overtime",
                     color_discrete_map={"Yes":LEFT,"No":STAYED},
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","overtime":""},
                     title="Attrition · Overtime vs Non-Overtime")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, yaxis_range=[0,100])
        st.plotly_chart(qlayout(fig), use_container_width=True)

    st.markdown(
        insight("⚡","Burnout Signal",
                "Entry-level employees carry the highest churn rate across all seniority bands. "
                "Overtime workers show the sharpest attrition split in the entire dataset — "
                "the clearest burnout signal HR has available."),
        unsafe_allow_html=True,
    )

    st.markdown(sec("Role & Career Growth"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        grp = group_attrition("job_role").sort_values("rate", ascending=True)
        fig = px.bar(grp, y="job_role", x="rate", orientation="h",
                     color="rate", color_continuous_scale=CMAP,
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","job_role":""},
                     title="Attrition Rate by Job Role")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(xaxis_range=[0,100], coloraxis_showscale=False)
        st.plotly_chart(qlayout(fig, h=390), use_container_width=True)

    with col2:
        grp = group_attrition("number_of_promotions").sort_values("number_of_promotions")
        fig = px.line(grp, x="number_of_promotions", y="rate", markers=True,
                      labels={"rate":"Attrition Rate (%)","number_of_promotions":"Promotions"},
                      title="Attrition Rate vs Promotions Received")
        fig.update_traces(line_color=PRIMARY, marker_size=9, marker_color="#818cf8",
                          fill="tozeroy", fillcolor="rgba(99,102,241,0.08)")
        fig.update_layout(yaxis_range=[0,100])
        st.plotly_chart(qlayout(fig, h=390), use_container_width=True)

    st.markdown(
        insight("📈","Career Stagnation",
                "Employees with zero promotions consistently leave the most. "
                "Each additional promotion is associated with a measurable drop in exit probability — "
                "visible, achievable career ladders are a direct retention lever."),
        unsafe_allow_html=True,
    )


# ─── Tab 2: Supporting Factors ─────────────────────────────────────────────────
with tab2:
    st.markdown(sec("Compensation & Satisfaction"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, x="attrition", y="monthly_income",
                     color="attrition",
                     color_discrete_map={"Left":LEFT,"Stayed":STAYED},
                     labels={"monthly_income":"Monthly Income ($)","attrition":""},
                     title="Income Distribution · Leavers vs Stayers")
        fig.update_layout(showlegend=False)
        st.plotly_chart(qlayout(fig), use_container_width=True)

    with col2:
        grp = group_attrition("job_satisfaction")
        fig = px.bar(grp, x="job_satisfaction", y="rate",
                     color="rate", color_continuous_scale=CMAP2,
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","job_satisfaction":""},
                     title="Attrition by Job Satisfaction",
                     category_orders={"job_satisfaction":["Low","Medium","High","Very High"]})
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(yaxis_range=[0,100], coloraxis_showscale=False)
        st.plotly_chart(qlayout(fig), use_container_width=True)

    st.markdown(
        insight("💰","Retention Levers",
                "Lower earners leave at significantly higher rates. "
                "Low satisfaction nearly doubles attrition risk. "
                "Compensation and engagement aren't soft metrics — they're the two most actionable "
                "retention levers available to HR."),
        unsafe_allow_html=True,
    )

    st.markdown(sec("Flexibility & Work-Life Balance"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        grp = group_attrition("remote_work")
        fig = px.bar(grp, x="remote_work", y="rate",
                     color="remote_work",
                     color_discrete_map={"Yes":STAYED,"No":LEFT},
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","remote_work":""},
                     title="Attrition · Remote vs On-Site")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, yaxis_range=[0,100])
        st.plotly_chart(qlayout(fig), use_container_width=True)

    with col2:
        grp = group_attrition("work_life_balance")
        fig = px.bar(grp, x="work_life_balance", y="rate",
                     color="rate", color_continuous_scale=CMAP2,
                     text=grp["rate"].apply(lambda x: f"{x}%"),
                     labels={"rate":"Attrition Rate (%)","work_life_balance":""},
                     title="Attrition by Work-Life Balance",
                     category_orders={"work_life_balance":["Poor","Fair","Good","Excellent"]})
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(yaxis_range=[0,100], coloraxis_showscale=False)
        st.plotly_chart(qlayout(fig), use_container_width=True)

    st.markdown(
        insight("🏠","Flexibility Signal",
                "Remote workers stay significantly longer than on-site peers. "
                "Poor work-life balance is a consistent exit predictor across all roles. "
                "Schedule flexibility is a low-cost, high-impact retention tool."),
        unsafe_allow_html=True,
    )


# ─── Tab 3: Risk Overview ──────────────────────────────────────────────────────
with tab3:
    st.markdown(sec("Numeric Correlations with Attrition"), unsafe_allow_html=True)

    numeric_cols = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if c not in ("employee_id","attrition_flag")
    ]
    corr = (
        df[numeric_cols + ["attrition_flag"]]
        .corr()["attrition_flag"].drop("attrition_flag").sort_values()
    )
    colors = [LEFT if v > 0 else STAYED for v in corr.values]

    fig = go.Figure(go.Bar(
        y=corr.index, x=corr.values, orientation="h",
        marker_color=colors,
        text=[f"{v:.3f}" for v in corr.values],
        textposition="outside",
        marker_line_width=0,
    ))
    fig.update_layout(title="Pearson Correlation with Attrition Flag",
                      xaxis_title="Correlation Coefficient")
    st.plotly_chart(qlayout(fig, h=430), use_container_width=True)

    st.markdown(
        insight("📊","Ranked Levers",
                "Distance from home and number of dependents push toward leaving. "
                "Monthly income, years at company, and promotions pull toward staying — "
                "a clear shortlist of where HR interventions have the highest expected return."),
        unsafe_allow_html=True,
    )

    st.markdown(sec("Key Findings & HR Recommendations"), unsafe_allow_html=True)

    findings_df = pd.DataFrame([
        ("⚡ Overtime",         "Sharpest single attrition predictor",           "Cap mandatory overtime; introduce compensatory time-off"),
        ("😟 Job Satisfaction", "Low satisfaction nearly doubles attrition risk", "Regular 1-on-1s; pulse surveys; visible growth paths"),
        ("🔰 Entry-Level",      "Highest churn rate across all seniority bands",  "Structured onboarding + mentorship; 6-month check-ins"),
        ("🏠 Remote Work",      "Remote employees stay significantly longer",     "Expand hybrid/remote eligibility where operationally feasible"),
        ("📈 Promotions",       "Zero promotions correlates with highest attrition","Review promotion cadence; build transparent career ladders"),
        ("💵 Income",           "Lower earners leave at higher rates",            "Benchmark salaries; prioritize raises in high-attrition roles"),
        ("🚗 Commute Distance", "Long commutes consistently correlate with exit", "Remote flexibility for high-distance employees"),
    ], columns=["Factor","Finding","Recommended Action"])
    findings_df.index += 1
    st.dataframe(findings_df, use_container_width=True, height=295)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;color:#1a1e36;font-size:0.72rem;
            border-top:1px solid rgba(99,102,241,0.07);padding-top:1rem">
  <span style="opacity:.35">{LOGO_IMG.format(s="height:18px;vertical-align:middle;margin-right:.4rem")}</span>
  Kayfa AI &amp; Data Analytics Internship &nbsp;·&nbsp; Week 1 · Data Analytics Track
  &nbsp;·&nbsp; Synthetic HR Dataset · 74,498 records
</div>
""", unsafe_allow_html=True)