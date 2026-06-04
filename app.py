import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Employee Attrition · Kayfa",
    page_icon="📊",
    layout="wide",
)

# ── Theme ───────────────────────────────────────────────────────────────────────
COLORS   = {"Left": "#E45756", "Stayed": "#4E79A7"}
TEMPLATE = "plotly_white"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #e8eaf0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #9aa0b0 !important; font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase; }

.kpi-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #141824 100%);
    border: 1px solid #2a2f42;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.kpi-label { color: #6b7280; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.3rem; }
.kpi-value { color: #f1f3f9; font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1; }
.kpi-sub   { color: #4E79A7; font-size: 0.78rem; margin-top: 0.25rem; }
.kpi-alert { color: #E45756; }

.section-head {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #c8ccd8;
    letter-spacing: 0.04em;
    border-left: 3px solid #4E79A7;
    padding-left: 0.7rem;
    margin: 1.6rem 0 0.8rem;
}

.insight-box {
    background: #141824;
    border-left: 3px solid #E45756;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    color: #9aa0b0;
    font-size: 0.84rem;
    margin-top: 0.5rem;
    line-height: 1.55;
}
</style>
""", unsafe_allow_html=True)


# ── Data ────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    train = pd.read_csv("train.csv")
    test  = pd.read_csv("test.csv")
    df = pd.concat([train, test], ignore_index=True)

    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(" ", "_").str.replace("-", "_")
    )

    ORDINALS = {
        "work_life_balance"   : ["Poor", "Fair", "Good", "Excellent"],
        "job_satisfaction"    : ["Low", "Medium", "High", "Very High"],
        "job_level"           : ["Entry", "Mid", "Senior"],
        "employee_recognition": ["Low", "Medium", "High", "Very High"],
    }
    for col, order in ORDINALS.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)

    df["attrition_flag"] = (df["attrition"] == "Left").astype(int)
    return df

df_all = load_data()


# ── Sidebar filters ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    gender_opts = ["All"] + sorted(df_all["gender"].dropna().unique().tolist())
    gender = st.selectbox("Gender", gender_opts)

    role_opts = ["All"] + sorted(df_all["job_role"].dropna().unique().tolist())
    role = st.selectbox("Job Role", role_opts)

    remote_opts = ["All"] + sorted(df_all["remote_work"].dropna().unique().tolist())
    remote = st.selectbox("Remote Work", remote_opts)

    marital_opts = ["All"] + sorted(df_all["marital_status"].dropna().unique().tolist())
    marital = st.selectbox("Marital Status", marital_opts)

    level_opts = ["All"] + ["Entry", "Mid", "Senior"]
    level = st.selectbox("Job Level", level_opts)

    st.markdown("---")
    st.markdown("<small style='color:#4a5060'>Kayfa · AI & Data Analytics<br>Week 1 · Data Analytics Track</small>", unsafe_allow_html=True)

# Apply filters
df = df_all.copy()
if gender  != "All": df = df[df["gender"]        == gender]
if role    != "All": df = df[df["job_role"]       == role]
if remote  != "All": df = df[df["remote_work"]    == remote]
if marital != "All": df = df[df["marital_status"] == marital]
if level   != "All": df = df[df["job_level"]      == level]


def group_attrition(col):
    g = (
        df.groupby(col, observed=True)["attrition_flag"]
        .agg(total="count", left="sum")
        .reset_index()
    )
    g["rate"] = (g["left"] / g["total"] * 100).round(1)
    return g


# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 1.5rem 0 0.5rem'>
  <div style='font-family:Syne,sans-serif; font-size:2.2rem; font-weight:800; color:#f1f3f9; line-height:1.1'>
    Employee Attrition<br><span style='color:#4E79A7'>Analytics Dashboard</span>
  </div>
  <div style='color:#6b7280; font-size:0.85rem; margin-top:0.5rem'>
    Kayfa AI & Data Analytics Internship · Week 1 · 74,498 synthetic employee records
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPIs ────────────────────────────────────────────────────────────────────────
total      = len(df)
left_count = df["attrition_flag"].sum()
rate       = left_count / total * 100 if total else 0
avg_salary = df["monthly_income"].mean()
avg_age    = df["age"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>Total Employees</div>
      <div class='kpi-value'>{total:,}</div>
      <div class='kpi-sub'>filtered population</div>
    </div>""", unsafe_allow_html=True)

with c2:
    alert = "kpi-alert" if rate > 30 else ""
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>Attrition Rate</div>
      <div class='kpi-value {alert}'>{rate:.1f}%</div>
      <div class='kpi-sub'>{left_count:,} employees left</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>Avg Monthly Salary</div>
      <div class='kpi-value'>${avg_salary:,.0f}</div>
      <div class='kpi-sub'>across filtered group</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>Average Age</div>
      <div class='kpi-value'>{avg_age:.1f}</div>
      <div class='kpi-sub'>years old</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Row 1: Overview + Overtime ──────────────────────────────────────────────────
st.markdown("<div class='section-head'>Attrition Overview</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    counts = df["attrition"].value_counts().reset_index()
    counts.columns = ["status", "employees"]
    fig = px.pie(
        counts, values="employees", names="status",
        color="status", color_discrete_map=COLORS,
        hole=0.52, template=TEMPLATE,
        title="Stayed vs Left"
    )
    fig.update_traces(textinfo="label+percent", textfont_size=13)
    fig.update_layout(showlegend=False, height=350, margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    grp = group_attrition("overtime")
    fig = px.bar(
        grp, x="overtime", y="rate",
        color="overtime",
        color_discrete_map={"Yes": COLORS["Left"], "No": COLORS["Stayed"]},
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "overtime": "Works Overtime"},
        title="Attrition · Overtime vs Non-Overtime",
        template=TEMPLATE, height=350
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='insight-box'>⚡ Overtime workers show the sharpest attrition split in the entire dataset — the clearest burnout signal HR has.</div>", unsafe_allow_html=True)


# ── Row 2: Income + Job Satisfaction ───────────────────────────────────────────
st.markdown("<div class='section-head'>Compensation & Satisfaction</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        df, x="attrition", y="monthly_income",
        color="attrition", color_discrete_map=COLORS,
        labels={"monthly_income": "Monthly Income ($)", "attrition": ""},
        title="Income Distribution · Leavers vs Stayers",
        template=TEMPLATE, height=370
    )
    fig.update_layout(showlegend=False, margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    grp = group_attrition("job_satisfaction")
    fig = px.bar(
        grp, x="job_satisfaction", y="rate",
        color="rate", color_continuous_scale="RdYlGn_r",
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "job_satisfaction": "Job Satisfaction"},
        title="Attrition Rate by Job Satisfaction",
        template=TEMPLATE, height=370,
        category_orders={"job_satisfaction": ["Low", "Medium", "High", "Very High"]}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='insight-box'>💰 Lower earners leave more. Dissatisfied employees leave more. Compensation and satisfaction aren't just HR metrics — they're retention levers.</div>", unsafe_allow_html=True)


# ── Row 3: Remote Work + Promotions ────────────────────────────────────────────
st.markdown("<div class='section-head'>Flexibility & Growth</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    grp = group_attrition("remote_work")
    fig = px.bar(
        grp, x="remote_work", y="rate",
        color="remote_work",
        color_discrete_map={"Yes": COLORS["Stayed"], "No": COLORS["Left"]},
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "remote_work": "Remote Work"},
        title="Attrition · Remote vs On-Site",
        template=TEMPLATE, height=360
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    grp = group_attrition("number_of_promotions").sort_values("number_of_promotions")
    fig = px.line(
        grp, x="number_of_promotions", y="rate",
        markers=True,
        labels={"rate": "Attrition Rate (%)", "number_of_promotions": "Promotions Received"},
        title="Attrition Rate vs Promotions",
        template=TEMPLATE, height=360
    )
    fig.update_traces(line_color=COLORS["Left"], marker_size=9, marker_color=COLORS["Left"])
    fig.update_layout(yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='insight-box'>🏠 Remote workers stay longer. Employees with zero promotions leave the most — career stagnation is an exit trigger.</div>", unsafe_allow_html=True)


# ── Row 4: Job Role + Job Level ─────────────────────────────────────────────────
st.markdown("<div class='section-head'>Role & Seniority</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    grp = group_attrition("job_role").sort_values("rate", ascending=True)
    fig = px.bar(
        grp, y="job_role", x="rate", orientation="h",
        color="rate", color_continuous_scale="RdYlBu_r",
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "job_role": ""},
        title="Attrition Rate by Job Role",
        template=TEMPLATE, height=360
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    grp = group_attrition("job_level")
    fig = px.bar(
        grp, x="job_level", y="rate",
        color="rate", color_continuous_scale="RdYlGn_r",
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "job_level": "Job Level"},
        title="Attrition Rate by Job Level",
        template=TEMPLATE, height=360,
        category_orders={"job_level": ["Entry", "Mid", "Senior"]}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='insight-box'>📊 Entry-level employees churn the most — lower pay, less clarity, more outside options. The first 12–18 months are the highest-risk window.</div>", unsafe_allow_html=True)


# ── Row 5: Age + Work-Life Balance ──────────────────────────────────────────────
st.markdown("<div class='section-head'>Demographics & Wellbeing</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        df, x="attrition", y="age",
        color="attrition", color_discrete_map=COLORS,
        labels={"age": "Age", "attrition": ""},
        title="Age Distribution · Leavers vs Stayers",
        template=TEMPLATE, height=360
    )
    fig.update_layout(showlegend=False, margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    grp = group_attrition("work_life_balance")
    fig = px.bar(
        grp, x="work_life_balance", y="rate",
        color="rate", color_continuous_scale="RdYlGn_r",
        text=grp["rate"].apply(lambda x: f"{x}%"),
        labels={"rate": "Attrition Rate (%)", "work_life_balance": "Work-Life Balance"},
        title="Attrition Rate by Work-Life Balance",
        template=TEMPLATE, height=360,
        category_orders={"work_life_balance": ["Poor", "Fair", "Good", "Excellent"]}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 100], margin=dict(t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='insight-box'>👥 Employees aged 25–40 show the highest churn volume. Poor work-life balance is a strong predictor — workload and schedule control are central to retention.</div>", unsafe_allow_html=True)


# ── Correlation ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-head'>Numeric Correlation with Attrition</div>", unsafe_allow_html=True)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [c for c in numeric_cols if c not in ("employee_id", "attrition_flag")]

corr = (
    df[numeric_cols + ["attrition_flag"]]
    .corr()["attrition_flag"]
    .drop("attrition_flag")
    .sort_values()
)

bar_colors = [COLORS["Left" if v > 0 else "Stayed"] for v in corr.values]

fig = go.Figure(go.Bar(
    y=corr.index, x=corr.values, orientation="h",
    marker_color=bar_colors,
    text=[f"{v:.3f}" for v in corr.values],
    textposition="outside"
))
fig.update_layout(
    title="Pearson Correlation with Attrition Flag",
    xaxis_title="Correlation Coefficient",
    template=TEMPLATE, height=400,
    margin=dict(t=50, b=10)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("<div class='insight-box'>📈 Distance from home and dependents push toward leaving. Income, tenure, and promotions pull toward staying — a ranked shortlist of HR levers.</div>", unsafe_allow_html=True)


# ── Key Findings table ───────────────────────────────────────────────────────────
st.markdown("<div class='section-head'>Key Findings & HR Recommendations</div>", unsafe_allow_html=True)

findings = [
    ("Overtime",          "Sharpest single attrition predictor",                  "Cap mandatory overtime; introduce compensatory time-off"),
    ("Job Satisfaction",  "Low satisfaction nearly doubles attrition risk",        "Regular 1-on-1s; satisfaction pulse surveys; clear growth paths"),
    ("Entry-Level",       "Highest churn rate across all job levels",              "Structured onboarding + mentorship; 6-month and 1-year milestones"),
    ("Remote Work",       "Remote employees stay significantly longer",            "Expand hybrid/remote eligibility where feasible"),
    ("Promotions",        "Zero promotions = highest attrition",                   "Review promotion cadence; visible, achievable career ladders"),
    ("Income",            "Lower earners leave at higher rates",                   "Benchmark salaries; prioritize raises in high-attrition roles"),
    ("Commute Distance",  "Longer commutes correlate with exit",                   "Remote flexibility for high-distance employees"),
]

findings_df = pd.DataFrame(findings, columns=["Factor", "Finding", "Recommended Action"])
findings_df.index = findings_df.index + 1
st.dataframe(findings_df, use_container_width=True, height=300)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#3a3f52; font-size:0.78rem; padding-bottom:1rem'>
  Kayfa AI & Data Analytics Internship · Week 1 · Data Analytics Track<br>
  Synthetic HR Dataset · 74,498 records · Pandas · Plotly · Streamlit
</div>
""", unsafe_allow_html=True)
