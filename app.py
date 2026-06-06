import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import base64
import io
from PIL import Image

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Employee Attrition · Kayfa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Logo ───────────────────────────────────────────────────────────────────────
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
LEFT    = "#E45756"
STAYED  = "#4E79A7"
PRIMARY = "#6366f1"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

html,body,[class*="css"],.stApp {
    font-family:'DM Sans',sans-serif !important;
}
.main .block-container {
    padding-top:1.8rem !important;
    padding-bottom:3rem !important;
    max-width:1400px !important;
}

/* ── KPI Cards ── */
.kpi-card {
    background:rgba(99,102,241,0.04);
    border:1px solid rgba(99,102,241,0.15);
    border-radius:16px;
    padding:1.4rem 1.7rem 1.2rem;
    position:relative;
    overflow:hidden;
    height:100%;
}
.kpi-card-1::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,#6366f1,#818cf8); border-radius:16px 16px 0 0; }
.kpi-card-2::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,#ef4444,#f87171); border-radius:16px 16px 0 0; }
.kpi-card-3::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,#f97316,#fb923c); border-radius:16px 16px 0 0; }
.kpi-card-4::before { content:''; position:absolute; top:0;left:0;right:0;height:3px; background:linear-gradient(90deg,#10b981,#34d399); border-radius:16px 16px 0 0; }
.kpi-label {
    font-size:0.66rem;
    font-weight:700;
    letter-spacing:0.13em;
    text-transform:uppercase;
    margin-bottom:0.6rem;
    opacity:0.6;
}
.kpi-value {
    font-family:'Inter',sans-serif !important;
    font-size:2.2rem;
    font-weight:800;
    line-height:1;
    margin-bottom:0.35rem;
    letter-spacing:-0.03em;
}
.kpi-blue   { color:#6366f1; }
.kpi-red    { color:#ef4444; }
.kpi-orange { color:#f97316; }
.kpi-green  { color:#10b981; }
.kpi-sub    { font-size:0.73rem; font-weight:500; opacity:0.5; }

/* ── Section headers ── */
.sec-head {
    display:flex;
    align-items:center;
    gap:0.8rem;
    margin:2.2rem 0 1rem;
}
.sec-dot {
    width:8px;height:8px;
    border-radius:50%;
    background:#6366f1;
    flex-shrink:0;
}
.sec-title {
    font-size:1rem;
    font-weight:800;
    color:#6366f1;
    letter-spacing:0.06em;
    text-transform:uppercase;
    white-space:nowrap;
}
.sec-line {
    flex:1;
    height:1px;
    background:rgba(99,102,241,0.2);
}

/* ── Insight boxes ── */
.insight {
    background:rgba(99,102,241,0.06);
    border:1px solid rgba(99,102,241,0.2);
    border-left:3px solid #6366f1;
    border-radius:0 12px 12px 0;
    padding:1.1rem 1.4rem;
    margin-top:0.6rem;
    font-size:0.95rem;
    line-height:1.75;
}
.itag {
    display:inline-flex;
    align-items:center;
    gap:0.3rem;
    background:rgba(99,102,241,0.12);
    color:#6366f1;
    font-size:0.72rem;
    font-weight:700;
    letter-spacing:0.09em;
    text-transform:uppercase;
    padding:0.22rem 0.75rem;
    border-radius:20px;
    margin-bottom:0.55rem;
    border:1px solid rgba(99,102,241,0.2);
}

/* ── Action Plan cards ── */
.action-card {
    border:1px solid rgba(99,102,241,0.2);
    border-radius:14px;
    padding:1.2rem 1.4rem;
    margin-bottom:1rem;
}
.action-free  { border-left:4px solid #10b981; background:rgba(16,185,129,0.04); }
.action-low   { border-left:4px solid #6366f1; background:rgba(99,102,241,0.04); }
.action-med   { border-left:4px solid #f97316; background:rgba(249,115,22,0.04); }
.action-title { font-weight:700; font-size:1rem; margin-bottom:0.4rem; }
.action-meta  { font-size:0.78rem; opacity:0.6; margin-bottom:0.6rem; }
.action-body  { font-size:0.9rem; line-height:1.7; opacity:0.85; }
.cost-badge {
    display:inline-block;
    font-size:0.7rem;
    font-weight:700;
    padding:0.15rem 0.6rem;
    border-radius:20px;
    margin-right:0.4rem;
}
.free-badge { background:rgba(16,185,129,0.15); color:#10b981; }
.low-badge  { background:rgba(99,102,241,0.15); color:#6366f1; }
.med-badge  { background:rgba(249,115,22,0.15); color:#f97316; }
            
.stAlert { border-radius:10px !important; }

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(27, 42, 107, 0.15) !important;
    border: 1px solid rgba(27, 42, 107, 0.4) !important;
    border-radius: 5px !important;
    color: #1B2A6B !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.concat([pd.read_csv("train.csv"), pd.read_csv("test.csv")], ignore_index=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ","_").str.replace("-","_")
    ORDINALS = {
        "work_life_balance"   : ["Poor","Fair","Good","Excellent"],
        "job_satisfaction"    : ["Low","Medium","High","Very High"],
        "performance_rating"  : ["Low","Below Average","Average","High"],
        "education_level"     : ["High School","Associate Degree","Bachelor's Degree","Master's Degree","PhD"],
        "job_level"           : ["Entry","Mid","Senior"],
        "company_size"        : ["Small","Medium","Large"],
        "company_reputation"  : ["Poor","Fair","Good","Excellent"],
        "employee_recognition": ["Low","Medium","High","Very High"],
    }
    for col, order in ORDINALS.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=order, ordered=True)
    df["attrition_flag"] = (df["attrition"] == "Left").astype(int)
    df['pay_band'] = df.groupby('job_level', observed=True)['monthly_income'].transform(
        lambda x: pd.qcut(x, 4, labels=['Lowest 25%', 'Lower-Mid', 'Upper-Mid', 'Highest 25%'])
    )
    df['tenure_stage'] = pd.cut(df['years_at_company'], bins=[-1, 2, 5, 10, 100],
                                labels=['New (0-2y)', 'Established (3-5y)', 'Experienced (6-10y)', 'Veteran (10y+)'])
    df['age_group'] = pd.cut(df['age'], bins=[17, 30, 45, 100],
                             labels=['Young (18-30)', 'Middle (31-45)', 'Senior (45+)'])
    # ── Edge case removal (noisy synthetic records) ───────────────────────────
    edge_mask = (
        ((df['age'] < 25) & (df['education_level'].isin(["Master's Degree", "PhD"]))) |
        ((df['job_level'] == 'Entry') & (df['monthly_income'] > df['monthly_income'].quantile(0.95))) |
        ((df['years_at_company'] <= 1) & (df['number_of_promotions'] > 2))
    )
    df = df[~edge_mask].copy()

    df['dependents_group'] = df['number_of_dependents'].apply(
        lambda x: 'No Dependents' if x == 0 else ('1–2 Dependents' if x <= 2 else '3+ Dependents')
    )
    df['stuck_profile'] = np.where(
        (df['number_of_promotions'] == 0) &
        (df['leadership_opportunities'] == 'No') &
        (df['innovation_opportunities'] == 'No'),
        "Stuck (No Growth)", "Growth Access"
    )
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
    st.markdown("**Filters**")
    level_sel = st.multiselect(
        "Job Level", ["Entry","Mid","Senior"], default=["Entry","Mid","Senior"]
    )
    role_sel = st.multiselect(
        "Job Role",
        sorted(df_all["job_role"].dropna().unique()),
        default=sorted(df_all["job_role"].dropna().unique()),
    )
    gender_sel = st.multiselect(
        "Gender",
        sorted(df_all["gender"].dropna().unique()),
        default=sorted(df_all["gender"].dropna().unique()),
    )
    remote_sel = st.multiselect(
        "Remote Work",
        sorted(df_all["remote_work"].dropna().unique()),
        default=sorted(df_all["remote_work"].dropna().unique()),
    )
    marital_sel = st.multiselect(
        "Marital Status",
        sorted(df_all["marital_status"].dropna().unique()),
        default=sorted(df_all["marital_status"].dropna().unique()),
    )
    st.markdown("---")
    st.caption("AI & Data Analytics Internship\nMonth 1 · Week 1 · Data Analytics Track")


# ── Guard ──────────────────────────────────────────────────────────────────────
if not all([level_sel, role_sel, gender_sel, remote_sel, marital_sel]):
    st.warning("⚠️ Select at least one option in each filter.")
    st.stop()

df = df_all[
    df_all["job_level"].isin(level_sel) &
    df_all["job_role"].isin(role_sel) &
    df_all["gender"].isin(gender_sel) &
    df_all["remote_work"].isin(remote_sel) &
    df_all["marital_status"].isin(marital_sel)
].copy()


# ── Helpers ────────────────────────────────────────────────────────────────────
def group_attrition(col):
    g = (df.groupby(col, observed=True)["attrition_flag"]
         .agg(total="count", left="sum").reset_index())
    g["rate"] = (g["left"] / g["total"] * 100).round(1)
    return g

def qlayout(fig, h=360):
    fig.update_layout(
        height=h,
        margin=dict(t=46,b=12,l=10,r=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_white",
        font=dict(family="DM Sans", size=11),
        title_font=dict(family="DM Sans", size=13, weight=600),
    )
    fig.update_traces(textfont_size=13)
    fig.update_xaxes(gridcolor="rgba(0,0,0,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.05)", zeroline=False)
    return fig

def insight(emoji, tag, text):
    return (f"<div class='insight'>"
            f"<div class='itag'>{emoji} {tag}</div><br>{text}</div>")

def smart_ymax(series, pad=1.35):
    return min(100, round(series.max() * pad, 0))

def sec(title):
    return (f"<div class='sec-head'>"
            f"<span class='sec-dot'></span>"
            f"<span class='sec-title'>{title}</span>"
            f"<span class='sec-line'></span></div>")


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:0 0 0.6rem">
  <div>
    <div style="font-size:2rem;font-weight:800;letter-spacing:-0.02em;line-height:1.1">
      <span style="color:#6366f1;font-size:1.50rem;font-weight:700;
                    letter-spacing:0.08em;text-transform:uppercase;display:block;
                    margin-bottom:0.3rem">Week #1 Task:</span>
      Employee Attrition Analytics
    </div>
    <div style="font-size:0.78rem;margin-top:0.2rem;font-weight:500;opacity:0.5">
      74,498 synthetic employee records &nbsp;·&nbsp;
      Kayfa AI & Data Analytics &nbsp;·&nbsp; Week 1
    </div>
  </div>
  {LOGO_IMG.format(s="height:50px;flex-shrink:0;position:relative;top:-60px")}
</div>
<hr style="margin:0.4rem 0 1.2rem;opacity:0.15">
""", unsafe_allow_html=True)


# ── KPIs ───────────────────────────────────────────────────────────────────────
total       = len(df)
left_count  = int(df["attrition_flag"].sum())
rate        = left_count / total * 100 if total else 0
company_avg = df_all["attrition_flag"].mean() * 100
avg_salary  = df["monthly_income"].mean() if total else 0

entry_df  = group_attrition("job_level")
entry_row = entry_df[entry_df["job_level"] == "Entry"]
entry_pct = f'{entry_row["rate"].values[0]:.1f}%' if len(entry_row) else "—"

rate_cls = "kpi-red" if rate > 45 else "kpi-green" if rate < 30 else "kpi-orange"

c1, c2, c3, c4 = st.columns(4)
for col, label, val, cls, sub, card_cls in [
    (c1, "Headcount",       f"{total:,}",        "kpi-blue",  f"of {len(df_all):,} total",   "kpi-card-1"),
    (c2, "Attrition Rate",  f"{rate:.1f}%",      rate_cls,    "filtered selection",            "kpi-card-2"),
    (c3, "Avg Monthly Salary", f"${avg_salary:,.0f}", "kpi-orange", "filtered employees",      "kpi-card-3"),
    (c4, "Entry-Level Risk",entry_pct,            "kpi-red",   "highest risk segment",          "kpi-card-4"),
]:
    with col:
        st.markdown(f"""
        <div class='kpi-card {card_cls}'>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value {cls}'>{val}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Attrition Headlines",
    "💰  Pay & Retention",
    "⚡  Engagement & Growth",
    "🎯  Risk Profiles & Drivers",
    "📈  Executive Summary",
    "💡  Action Plan",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 · Q1-Q3
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:

    # Q1
    st.markdown(sec("Q1 · The Headline: Overall Attrition & Top Leaking Role"), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        role_count = group_attrition("job_role").sort_values("left", ascending=False)
        fig = px.bar(role_count, x="left", y="job_role", orientation="h", text_auto=True,
                     title="Employees Who Left by Job Role (Volume)",
                     labels={"left": "Number of Leavers", "job_role": "Job Role"},
                     color_discrete_sequence=[LEFT])
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(qlayout(fig), use_container_width=True)
    with col_b:
        role_rate = group_attrition("job_role").sort_values("rate", ascending=False)
        fig = px.bar(role_rate, x="rate", y="job_role", orientation="h", text_auto=".1f",
                     title="Attrition Rate (%) by Job Role",
                     labels={"rate": "Attrition Rate (%)", "job_role": "Job Role"},
                     color_discrete_sequence=["#6366f1"])
        fig.add_vline(x=rate, line_dash="dash",
                      annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#9333ea", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)", line_color="#9333ea")
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(qlayout(fig), use_container_width=True)

    top_role_vol  = role_count.iloc[0]
    top_role_rate = role_rate.iloc[0]
    st.markdown(
        insight("💡","INSIGHTS",
                f"Overall attrition is <b>{rate:.1f}%</b> — nearly 1 in 2 employees. "
                f"<b>{top_role_vol['job_role']}</b> has the most leavers in volume ({int(top_role_vol['left']):,} people). "
                f"<b>{top_role_rate['job_role']}</b> has the highest rate ({top_role_rate['rate']:.1f}%). "
                "Leadership should start retention efforts with the highest-rate role, not just the highest count."),
        unsafe_allow_html=True,
    )

    # Q2
    st.markdown(sec("Q2 · Overtime: Is Workload Driving Exits?"), unsafe_allow_html=True)

    ot_stats = group_attrition("overtime")
    fig = px.bar(ot_stats, x="overtime", y="rate", color="overtime", text_auto=".1f",
                 title="Attrition Rate: Overtime vs No Overtime",
                 labels={"overtime": "Overtime Status", "rate": "Attrition Rate (%)"},
                 color_discrete_map={"Yes": LEFT, "No": STAYED})
    fig.add_hline(y=rate, line_dash="dash",
                  annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#9333ea", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)", line_color="#9333ea")
    fig.update_layout(showlegend=False, yaxis_range=[0, smart_ymax(ot_stats["rate"])])
    st.plotly_chart(qlayout(fig), use_container_width=True)

    _oy = ot_stats[ot_stats["overtime"] == "Yes"]
    _on = ot_stats[ot_stats["overtime"] == "No"]
    ot_yes = float(_oy["rate"].values[0]) if len(_oy) else None
    ot_no  = float(_on["rate"].values[0])  if len(_on)  else None
    if ot_yes is not None and ot_no is not None:
        st.markdown(
            insight("💡","INSIGHTS",
                    f"Overtime workers leave at <b>{ot_yes:.1f}%</b> vs {ot_no:.1f}% for non-overtime — "
                    f"a <b>{ot_yes - ot_no:.1f} percentage point gap</b>. "
                    "This is the clearest single burnout signal in the data. "
                    "HR should audit overtime hours by department and cap mandatory overtime immediately."),
            unsafe_allow_html=True,
        )
    else:
        st.info("⚠️ Enable both Overtime options in the filter to compare groups.")

    # Q3
    st.markdown(sec("Q3 · Remote Work: Does Flexibility Retain People?"), unsafe_allow_html=True)

    remote_stats = group_attrition("remote_work")
    fig = px.bar(remote_stats, x="remote_work", y="rate", color="remote_work", text_auto=".1f",
                 title="Attrition Rate: Remote vs On-Site",
                 labels={"remote_work": "Work Mode", "rate": "Attrition Rate (%)"},
                 color_discrete_map={"Yes": "#10b981", "No": LEFT})
    fig.add_hline(y=rate, line_dash="dash", line_color="#6366f1",
              annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#6366f1", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)")
    fig.update_layout(showlegend=False, yaxis_range=[0, smart_ymax(remote_stats["rate"])])
    st.plotly_chart(qlayout(fig), use_container_width=True)

    _ry = remote_stats[remote_stats["remote_work"] == "Yes"]
    _rn = remote_stats[remote_stats["remote_work"] == "No"]
    remote_yes = float(_ry["rate"].values[0]) if len(_ry) else None
    remote_no  = float(_rn["rate"].values[0]) if len(_rn) else None
    remote_pop = (df_all["remote_work"] == "Yes").mean() * 100
    if remote_yes is not None and remote_no is not None:
        st.markdown(
            insight("💡","INSIGHTS",
                    f"Remote workers have significantly lower attrition ({remote_yes:.1f}%) vs on-site ({remote_no:.1f}%). "
                    f"However, only <b>{remote_pop:.1f}% of staff</b> currently work remotely — "
                    "so we can't yet conclude this scales company-wide. "
                    "Recommendation: pilot expanded remote/hybrid options for the 2 highest-attrition roles first, "
                    "then measure before rolling out broadly."),
            unsafe_allow_html=True,
        )
    else:
        st.info("⚠️ Enable both Remote Work options in the filter to compare groups.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 · Q4-Q5
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:

    # Q4
    st.markdown(sec("Q4 · Pay Fairness: Does Lower Pay Within Levels Drive Attrition?"), unsafe_allow_html=True)

    pay_stats = group_attrition(["job_level", "pay_band"])
    fig = px.line(pay_stats, x="pay_band", y="rate", color="job_level", markers=True,
                  title="Attrition Rate by Pay Band Within Job Levels",
                  labels={"pay_band": "Pay Band", "rate": "Attrition Rate (%)", "job_level": "Job Level"})
    fig.add_hline(y=rate, line_dash="dash",
                  annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#9333ea", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)", line_color="#9333ea")
    fig.update_layout(yaxis_range=[0, smart_ymax(pay_stats["rate"])])
    st.plotly_chart(qlayout(fig), use_container_width=True)

    st.markdown(
        insight("💡","INSIGHTS",
                "Lower-paid employees within the same job level consistently leave at higher rates. "
                "The retention benefit of pay increases flattens after the <b>'Upper-Mid' band</b> — "
                "meaning paying above that threshold yields diminishing returns on retention. "
                "HR should focus salary adjustments on the <b>'Lowest 25%' band first</b>, "
                "particularly in high-attrition roles, rather than blanket raises across all levels."),
        unsafe_allow_html=True,
    )

    # Q5
    st.markdown(sec("Q5 · Retention Timeline: When Are Employees Most at Risk?"), unsafe_allow_html=True)

    tenure_stats = group_attrition("tenure_stage")
    fig = px.bar(tenure_stats, x="tenure_stage", y="rate", text_auto=".1f",
                 title="Attrition Rate by Tenure Stage",
                 labels={"tenure_stage": "Tenure Stage", "rate": "Attrition Rate (%)"},
                 color_discrete_sequence=["#f97316"])
    fig.add_hline(y=rate, line_dash="dash",
                  annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#9333ea", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)", line_color="#9333ea")
    fig.update_layout(yaxis_range=[0, smart_ymax(tenure_stats["rate"])])
    st.plotly_chart(qlayout(fig), use_container_width=True)

    peak_stage = tenure_stats.loc[tenure_stats["rate"].idxmax(), "tenure_stage"]
    peak_rate  = tenure_stats["rate"].max()
    st.markdown(
        insight("💡","INSIGHTS",
                f"Attrition peaks in the <b>{peak_stage}</b> stage at <b>{peak_rate:.1f}%</b>. "
                "Employees who make it past 5 years show dramatically lower exit rates. "
                "The first 2 years are the critical retention window. "
                "HR should invest in structured 30/60/90-day onboarding check-ins, "
                "strong first-manager assignment, and a 6-month milestone review for all new hires."),
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 · Q6-Q8
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:

    # Q6
    st.markdown(sec("Q6 · Engagement Warning Signs: Which Combination Signals Exit?"), unsafe_allow_html=True)

    eng_stats = group_attrition(["job_satisfaction", "work_life_balance"])
    pivot_eng = eng_stats.pivot(index="job_satisfaction", columns="work_life_balance", values="rate")
    fig = px.imshow(pivot_eng, text_auto=".1f", aspect="auto",
                    title="Attrition Heatmap: Job Satisfaction × Work-Life Balance (%)",
                    labels=dict(x="Work-Life Balance", y="Job Satisfaction", color="Rate (%)"),
                    color_continuous_scale="RdYlGn_r")
    st.plotly_chart(qlayout(fig, h=400), use_container_width=True)

    st.markdown(
        insight("💡","INSIGHTS",
                "<b>Low satisfaction + Poor work-life balance</b> is the strongest early-warning combination — "
                "producing the highest attrition in the dataset. "
                "Managers should treat any direct report scoring 'Low' on satisfaction surveys "
                "as a flight-risk trigger and schedule a stay interview within 2 weeks."),
        unsafe_allow_html=True,
    )

    # Q7
    st.markdown(sec("Q7 · Life Stage: Do Age, Marital Status & Dependents Change Attrition?"), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        life_stats = group_attrition(["age_group", "marital_status"])
        fig = px.bar(life_stats, x="age_group", y="rate", color="marital_status", barmode="group",
                     title="Attrition by Age Group & Marital Status",
                     labels={"age_group": "Age Group", "rate": "Attrition Rate (%)", "marital_status": "Marital Status"})
        fig.add_hline(y=rate, line_dash="dash", line_color="#6366f1",
              annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#6366f1", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)")
        fig.update_layout(yaxis_range=[0, smart_ymax(life_stats["rate"])])
        st.plotly_chart(qlayout(fig), use_container_width=True)
    with col_b:
        dep_stats = group_attrition(["age_group", "dependents_group"])
        fig = px.bar(dep_stats, x="age_group", y="rate", color="dependents_group", barmode="group",
                     title="Attrition by Age Group & Number of Dependents",
                     labels={"age_group": "Age Group", "rate": "Attrition Rate (%)", "dependents_group": "Dependents"})
        fig.add_hline(y=rate, line_dash="dash", line_color="#6366f1",
              annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#6366f1", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)")
        fig.update_layout(yaxis_range=[0, smart_ymax(dep_stats["rate"])])
        st.plotly_chart(qlayout(fig), use_container_width=True)

    full_life = group_attrition(["age_group", "marital_status", "dependents_group"])
    top_life  = full_life.sort_values("rate", ascending=False).iloc[0]
    st.markdown(
        insight("💡","INSIGHTS",
                f"<b>Young (18–30), Single employees with no dependents</b> are the highest-risk life stage — "
                f"the riskiest combination shows <b>{top_life['rate']:.1f}% attrition</b> ({int(top_life['total']):,} employees). "
                "They have the fewest financial and social anchors keeping them at the company. "
                "To retain them: offer mentorship programs, visible career paths, skill development budgets, "
                "and early-tenure recognition — not just salary."),
        unsafe_allow_html=True,
    )

    # Q8
    st.markdown(sec("Q8 · Career Stagnation: Does Lack of Growth Drive Exits?"), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        stuck_stats = group_attrition("stuck_profile")
        fig = px.bar(stuck_stats, x="stuck_profile", y="rate", color="stuck_profile", text_auto=".1f",
                     title="Attrition: Stuck vs Growth Access",
                     labels={"stuck_profile": "Growth Profile", "rate": "Attrition Rate (%)"},
                     color_discrete_map={"Stuck (No Growth)": LEFT, "Growth Access": "#10b981"})
        fig.add_hline(y=rate, line_dash="dash", line_color="#6366f1",
              annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#6366f1", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)")
        fig.update_layout(showlegend=False, yaxis_range=[0, smart_ymax(stuck_stats["rate"])])
        st.plotly_chart(qlayout(fig), use_container_width=True)
    with col_b:
        promo_stats = group_attrition("number_of_promotions")
        promo_stats = promo_stats[promo_stats["total"] > 100]
        fig = px.bar(promo_stats, x="number_of_promotions", y="rate", text_auto=".1f",
                     title="Attrition Rate by Number of Promotions",
                     labels={"number_of_promotions": "Number of Promotions", "rate": "Attrition Rate (%)"},
                     color_discrete_sequence=["#6366f1"])
        fig.add_hline(y=rate, line_dash="dash", line_color="#6366f1",
              annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#6366f1", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)")
        fig.update_layout(yaxis_range=[0, smart_ymax(promo_stats["rate"])])
        st.plotly_chart(qlayout(fig), use_container_width=True)

    _sk = stuck_stats[stuck_stats["stuck_profile"] == "Stuck (No Growth)"]
    _gr = stuck_stats[stuck_stats["stuck_profile"] == "Growth Access"]
    stuck_rate  = float(_sk["rate"].values[0]) if len(_sk) else None
    growth_rate = float(_gr["rate"].values[0]) if len(_gr) else None
    if stuck_rate is not None and growth_rate is not None:
        st.markdown(
            insight("💡","INSIGHTS",
                    f"Employees with <b>no growth signals</b> (zero promotions + no leadership/innovation opportunities) "
                    f"leave at <b>{stuck_rate:.1f}%</b> vs {growth_rate:.1f}% for those with growth access. "
                    "Zero promotions is the single strongest career-stagnation signal. "
                    "HR should launch an <b>internal mobility program</b> — lateral moves, stretch projects, "
                    "and innovation task forces — to provide growth even when vertical promotions aren't available."),
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 · Q9-Q10
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:

    # Q9
    st.markdown(sec("Q9 · The Highest-Risk Profile: Who Should HR Target?"), unsafe_allow_html=True)

    risk_cols = ["overtime", "job_satisfaction", "work_life_balance"]
    profiles  = group_attrition(risk_cols)
    top_risk  = profiles.sort_values("rate", ascending=False).iloc[0]
    lift      = top_risk["rate"] - rate

    # Chart: top 10 profiles
    top10 = profiles.sort_values("rate", ascending=False).head(10).copy()
    top10["Profile"] = (
        "OT:" + top10["overtime"].astype(str) + " | " +
        "Sat:" + top10["job_satisfaction"].astype(str) + " | " +
        "WLB:" + top10["work_life_balance"].astype(str)
    )
    fig = px.bar(top10, x="rate", y="Profile", orientation="h", text_auto=".1f",
                 title="Top 10 Highest-Risk Employee Profiles (Attrition Rate %)",
                 labels={"rate": "Attrition Rate (%)", "Profile": "Profile"},
                 color="rate", color_continuous_scale="Reds")
    fig.add_vline(x=rate, line_dash="dash",
                  annotation_text=f"<b>Filtered Avg ({rate:.1f}%)</b>",
              annotation_font_color="#9333ea", annotation_font_size=11,
              annotation_bgcolor="rgba(255,255,255,0.75)", line_color="#9333ea")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(qlayout(fig, h=420), use_container_width=True)

    st.markdown(f"""
    <div class='insight'>
    <div class='itag'>💡 INSIGHTS</div><br>
    <b>Highest-risk profile:</b> Overtime = {top_risk['overtime']} &nbsp;|&nbsp;
    Job Satisfaction = {top_risk['job_satisfaction']} &nbsp;|&nbsp;
    Work-Life Balance = {top_risk['work_life_balance']}<br><br>
    <b>Attrition rate:</b> {top_risk['rate']:.1f}% &nbsp;—&nbsp;
    <b style="color:#ef4444">{lift:+.1f} percentage points above company average</b><br>
    <b>Employees matching this profile:</b> {int(top_risk['total']):,} people
    — large enough to act on immediately.<br><br>
    HR should flag these {int(top_risk['total']):,} employees for priority workload audits,
    manager check-ins, and flexible scheduling within the next 30 days.
    </div>
    """, unsafe_allow_html=True)

    # Q10
    st.markdown(sec("Q10 · What Moves the Needle: Top 3 Drivers"), unsafe_allow_html=True)

    drivers = [
        ("Overtime",        "overtime",      "Yes"),
        ("Job Satisfaction","job_satisfaction","Low"),
        ("Work-Life Balance","work_life_balance","Poor"),
        ("Career Stagnation","stuck_profile", "Stuck (No Growth)"),
    ]
    driver_results = []
    for name, col, val in drivers:
        stats = group_attrition(col)
        row   = stats[stats[col] == val]
        r     = row["rate"].values[0] if len(row) else 0
        n     = row["total"].values[0] if len(row) else 0
        driver_results.append({"Driver": name, "Rate": r, "Lift": r - rate, "Count": int(n)})

    driver_df  = pd.DataFrame(driver_results).sort_values("Lift", ascending=False)
    top3       = driver_df.head(3)

    fig = px.bar(top3, x="Lift", y="Driver", orientation="h", text_auto=".1f",
                 title="Top 3 Attrition Drivers — Lift Above Company Average (Percentage Points)",
                 labels={"Lift": "Lift Above Baseline (pp)", "Driver": "Driver"},
                 color="Lift", color_continuous_scale="Reds")
    fig.update_layout(coloraxis_showscale=False, yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(qlayout(fig), use_container_width=True)

    best = top3.iloc[0]
    st.markdown(
        insight("💡","INSIGHTS",
                f"<b>{best['Driver']}</b> is the #1 needle-mover with a lift of <b>{best['Lift']:.1f} percentage points</b> "
                f"above the baseline, affecting <b>{best['Count']:,} employees</b>. "
                f"Next quarter, a focused initiative on {best['Driver']} has the highest potential ROI. "
                "Fixing overtime alone — by capping it across 2–3 high-risk departments — "
                "could move the overall attrition rate by several points within 6 months."),
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 · Executive Summary
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:

    st.markdown(sec("Executive Summary: Three Pillars for Retention"), unsafe_allow_html=True)

    st.markdown(f"""
    <div class='insight'>
    <div class='itag'>🚨 Pillar 1 — Burnout Prevention</div><br>
    Overtime and Poor Work-Life Balance are the strongest predictors of exit.
    Employees working overtime leave at <b>{(ot_yes or 0):.1f}%</b> vs {(ot_no or 0):.1f}% for non-overtime.
    <b>Immediate action:</b> audit overtime hours and cap mandatory overtime in high-risk departments.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='insight'>
    <div class='itag'>📅 Pillar 2 — Early Intervention</div><br>
    The first 2 years of tenure are the critical retention window. Attrition peaks in the early stage.
    <b>Immediate action:</b> structured 30/60/90-day check-ins, strong first-manager pairing,
    and a 6-month milestone review for all new hires.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='insight'>
    <div class='itag'>📈 Pillar 3 — Growth as Retention</div><br>
    Employees with no growth signals (no promotions, no leadership or innovation opportunities)
    are significantly more likely to leave.
    <b>Immediate action:</b> launch an internal mobility program — lateral moves, stretch assignments,
    and innovation task forces — to provide growth even when vertical promotions aren't available.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Data Source: 74,498 synthetic employee records · Kayfa AI & Data Analytics Internship · Week 1")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 · Action Plan (Budget-Aware)
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:

    st.markdown(sec("Retention Action Plan — Budget-Aware HR Roadmap"), unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.92rem;opacity:0.7;margin-bottom:1.5rem">
    Every action below is tied directly to a finding from the data.
    Actions are sorted by cost tier so HR can act regardless of budget cycle.
    <b>Start with the free actions — they move the needle fastest.</b>
    </p>
    """, unsafe_allow_html=True)

    # ── FREE ACTIONS ──────────────────────────────────────────────────────────
    st.markdown("#### 🟢 Zero-Cost Actions — Start This Week")

    st.markdown(f"""
    <div class='action-card action-free'>
        <div class='action-title'>1. Cap Overtime for the Highest-Attrition Roles</div>
        <div class='action-meta'>
            <span class='cost-badge free-badge'>FREE</span>
            Driven by: Q2 · Q9 · Q10 &nbsp;|&nbsp; Timeline: Immediate
        </div>
        <div class='action-body'>
            Overtime workers leave at <b>{(ot_yes or 0):.1f}%</b> vs {(ot_no or 0):.1f}% — the largest single gap in the dataset.
            Identify the top 2–3 job roles with highest overtime rates.
            Issue a manager directive: no mandatory overtime beyond X hours/week without director approval.
            Cost: zero. A policy memo and a manager briefing is all it takes.
            <br><b>Expected impact:</b> reduce attrition risk for the ~{int(df_all[df_all['overtime']=='Yes'].shape[0]):,} overtime employees.
        </div>
    </div>

    <div class='action-card action-free'>
        <div class='action-title'>2. Deploy Stay Interviews for Flight-Risk Employees</div>
        <div class='action-meta'>
            <span class='cost-badge free-badge'>FREE</span>
            Driven by: Q6 · Q9 &nbsp;|&nbsp; Timeline: Within 2 weeks
        </div>
        <div class='action-body'>
            Low satisfaction + Poor work-life balance is the strongest warning-sign combination.
            Ask managers to identify any direct report who scored low on either dimension in the last review cycle.
            Run a 20-minute structured stay interview: "What would make you stay? What's frustrating you?"
            This costs nothing but manager time and surfaces problems before the resignation letter arrives.
            <br><b>Target group:</b> overtime + low satisfaction + poor WLB = {int(top_risk['total']):,} employees at {top_risk['rate']:.1f}% attrition risk.
        </div>
    </div>

    <div class='action-card action-free'>
        <div class='action-title'>3. Assign Stretch Projects & Innovation Task Forces</div>
        <div class='action-meta'>
            <span class='cost-badge free-badge'>FREE</span>
            Driven by: Q8 &nbsp;|&nbsp; Timeline: This quarter
        </div>
        <div class='action-body'>
            Employees with no growth signals leave at <b>{(stuck_rate or 0):.1f}%</b>.
            You don't need to promote everyone — you need to make people feel like they're going somewhere.
            Create cross-functional task forces, assign "innovation owner" roles on existing projects,
            and let employees lead internal workshops.
            All of this signals growth without a budget line.
        </div>
    </div>

    <div class='action-card action-free'>
        <div class='action-title'>4. Implement 30/60/90-Day New Hire Check-ins</div>
        <div class='action-meta'>
            <span class='cost-badge free-badge'>FREE</span>
            Driven by: Q5 &nbsp;|&nbsp; Timeline: Start with next new hire batch
        </div>
        <div class='action-body'>
            Attrition peaks in the first 2 years. A structured check-in cadence costs only manager time.
            At 30 days: "Are you getting what you need?" At 60 days: "What's unclear or frustrating?"
            At 90 days: "What would make you stay long-term?"
            Document responses — patterns across new hires reveal systemic issues.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── LOW COST ACTIONS ──────────────────────────────────────────────────────
    st.markdown("#### 🔵 Low-Cost Actions — Plan for Next Quarter")

    st.markdown(f"""
    <div class='action-card action-low'>
        <div class='action-title'>5. Launch an Internal Mobility Program</div>
        <div class='action-meta'>
            <span class='cost-badge low-badge'>LOW COST</span>
            Driven by: Q8 &nbsp;|&nbsp; Timeline: Next quarter &nbsp;|&nbsp; Est. cost: Staff time to coordinate
        </div>
        <div class='action-body'>
            Post internal job openings before external ones. Create a simple internal job board (even a shared doc works).
            Encourage lateral moves — a Finance analyst moving to Technology costs far less than replacing them.
            Pair with a "career conversation" template managers use in 1-on-1s.
            Retention through internal mobility is 3–5x cheaper than external recruiting.
        </div>
    </div>

    <div class='action-card action-low'>
        <div class='action-title'>6. Pilot Hybrid/Remote for Top 2 High-Attrition Roles</div>
        <div class='action-meta'>
            <span class='cost-badge low-badge'>LOW COST</span>
            Driven by: Q3 &nbsp;|&nbsp; Timeline: Next quarter &nbsp;|&nbsp; Est. cost: Minor IT/tooling adjustments
        </div>
        <div class='action-body'>
            Remote workers leave at <b>{(remote_yes or 0):.1f}%</b> vs {(remote_no or 0):.1f}% on-site.
            Don't roll this out company-wide without data — pilot it in the 2 roles with highest attrition rates first.
            Measure attrition at 3 and 6 months. If it drops, expand. If not, adjust the policy.
            This costs IT setup time, not headcount.
        </div>
    </div>

    <div class='action-card action-low'>
        <div class='action-title'>7. Introduce Peer Mentorship for Young Single Employees</div>
        <div class='action-meta'>
            <span class='cost-badge low-badge'>LOW COST</span>
            Driven by: Q7 &nbsp;|&nbsp; Timeline: Next quarter &nbsp;|&nbsp; Est. cost: Program coordination only
        </div>
        <div class='action-body'>
            Young (18–30) single employees with no dependents are the highest-risk life-stage group.
            They respond strongly to belonging and growth signals.
            Pair each new hire under 30 with a mid-level mentor for their first year.
            Monthly 30-min coffee chats. No budget needed — just a matching spreadsheet and manager buy-in.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MEDIUM COST ACTIONS ───────────────────────────────────────────────────
    st.markdown("#### 🟠 Medium-Cost Actions — Budget Planning for Next Cycle")

    st.markdown(f"""
    <div class='action-card action-med'>
        <div class='action-title'>8. Salary Band Audit for Lowest 25% in High-Attrition Roles</div>
        <div class='action-meta'>
            <span class='cost-badge med-badge'>MEDIUM COST</span>
            Driven by: Q4 &nbsp;|&nbsp; Timeline: Next budget cycle &nbsp;|&nbsp; Est. cost: Targeted raises, not blanket increases
        </div>
        <div class='action-body'>
            Lower-paid employees within the same job level leave more often.
            The retention benefit of pay flattens after the Upper-Mid band —
            so you don't need to raise everyone, just lift the bottom quartile.
            Start with a market benchmarking exercise (free via LinkedIn Salary or Glassdoor).
            Then budget targeted adjustments for the Lowest 25% in roles with attrition above {rate:.0f}%.
            <br><b>Key principle:</b> fix the floor, not the ceiling. That's where the exits are happening.
        </div>
    </div>

    <div class='action-card action-med'>
        <div class='action-title'>9. Promotion Cadence Review & Transparent Career Ladders</div>
        <div class='action-meta'>
            <span class='cost-badge med-badge'>MEDIUM COST</span>
            Driven by: Q8 &nbsp;|&nbsp; Timeline: Next review cycle &nbsp;|&nbsp; Est. cost: HR time + potential promotion budget
        </div>
        <div class='action-body'>
            Zero promotions is the single clearest career-stagnation signal in the data.
            Even if budget doesn't allow salary increases, publish a clear promotion criteria document:
            "To reach Mid level, you need X, Y, Z." Employees who can see the path stay longer.
            Then audit: who has been in the same role for 2+ years with no promotion or title change?
            That list is your near-term attrition risk register.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary table ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(sec("Priority Matrix — Where to Start"), unsafe_allow_html=True)

    st.markdown("""
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
        <thead>
            <tr style="border-bottom:2px solid rgba(99,102,241,0.3)">
            <th style="text-align:left;padding:0.6rem">Action</th>
            <th style="text-align:left;padding:0.6rem">Cost</th>
            <th style="text-align:left;padding:0.6rem">Speed</th>
            <th style="text-align:left;padding:0.6rem">Data Driver</th>
            <th style="text-align:left;padding:0.6rem">Impact</th>
            </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Cap overtime (policy memo)</td>
            <td style="padding:0.6rem"><span style="background:rgba(16,185,129,0.15);color:#10b981;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Free</span></td>
            <td style="padding:0.6rem">Immediate</td>
            <td style="padding:0.6rem">Q2, Q9, Q10</td>
            <td style="padding:0.6rem">🔴 High</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Stay interviews for flight-risk employees</td>
            <td style="padding:0.6rem"><span style="background:rgba(16,185,129,0.15);color:#10b981;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Free</span></td>
            <td style="padding:0.6rem">2 weeks</td>
            <td style="padding:0.6rem">Q6, Q9</td>
            <td style="padding:0.6rem">🔴 High</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Stretch projects & task forces</td>
            <td style="padding:0.6rem"><span style="background:rgba(16,185,129,0.15);color:#10b981;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Free</span></td>
            <td style="padding:0.6rem">This quarter</td>
            <td style="padding:0.6rem">Q8</td>
            <td style="padding:0.6rem">🟡 Medium</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">30/60/90-day new hire check-ins</td>
            <td style="padding:0.6rem"><span style="background:rgba(16,185,129,0.15);color:#10b981;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Free</span></td>
            <td style="padding:0.6rem">Next hire batch</td>
            <td style="padding:0.6rem">Q5</td>
            <td style="padding:0.6rem">🔴 High</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Internal mobility program</td>
            <td style="padding:0.6rem"><span style="background:rgba(99,102,241,0.15);color:#6366f1;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Low</span></td>
            <td style="padding:0.6rem">Next quarter</td>
            <td style="padding:0.6rem">Q8</td>
            <td style="padding:0.6rem">🔴 High</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Hybrid pilot for top 2 roles</td>
            <td style="padding:0.6rem"><span style="background:rgba(99,102,241,0.15);color:#6366f1;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Low</span></td>
            <td style="padding:0.6rem">Next quarter</td>
            <td style="padding:0.6rem">Q3</td>
            <td style="padding:0.6rem">🟡 Medium</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Peer mentorship for young employees</td>
            <td style="padding:0.6rem"><span style="background:rgba(99,102,241,0.15);color:#6366f1;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Low</span></td>
            <td style="padding:0.6rem">Next quarter</td>
            <td style="padding:0.6rem">Q7</td>
            <td style="padding:0.6rem">🟡 Medium</td>
          </tr>
          <tr style="border-bottom:1px solid rgba(99,102,241,0.1)">
            <td style="padding:0.6rem">Salary band audit (bottom quartile)</td>
            <td style="padding:0.6rem"><span style="background:rgba(249,115,22,0.15);color:#f97316;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Medium</span></td>
            <td style="padding:0.6rem">Next cycle</td>
            <td style="padding:0.6rem">Q4</td>
            <td style="padding:0.6rem">🔴 High</td>
          </tr>
          <tr>
            <td style="padding:0.6rem">Promotion cadence review</td>
            <td style="padding:0.6rem"><span style="background:rgba(249,115,22,0.15);color:#f97316;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">Medium</span></td>
            <td style="padding:0.6rem">Next cycle</td>
            <td style="padding:0.6rem">Q8</td>
            <td style="padding:0.6rem">🟡 Medium</td>
          </tr>
        </tbody>
        </table>
""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("All actions derived directly from the 10-question EDA analysis · Kayfa AI & Data Analytics Internship · Week 1")