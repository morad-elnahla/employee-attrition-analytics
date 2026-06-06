<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Syne&weight=800&size=36&pause=1000&color=1B2A6B&center=true&vCenter=true&width=600&lines=Employee+Attrition+⚡;Who+Leaves+%26+Why;Data+Analytics+End-to-End)](https://git.io/typing-svg)

[![Python](https://img.shields.io/badge/Python-3.10-E8FF47?style=for-the-badge&logo=python&logoColor=black&labelColor=0a0c10)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-E8FF47?style=for-the-badge&logo=pandas&logoColor=black&labelColor=0a0c10)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-E8FF47?style=for-the-badge&logo=plotly&logoColor=black&labelColor=0a0c10)](https://plotly.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-E8FF47?style=for-the-badge&logo=streamlit&logoColor=black&labelColor=0a0c10)](https://streamlit.io)

> **74,498 employee records. 10 questions. One dashboard HR can actually use.**

| 👥 Total Employees | 📉 Attrition Rate | 💰 Avg Salary | 🔍 HR Questions |
|:-----------------:|:-----------------:|:-------------:|:---------------:|
| **74,498** | **47.5%** | **~$7,299** | **10** |

**[🚀 Try the Live Dashboard →](https://employee-attrition-analytics.streamlit.app/)**

</div>

## ✦ Dashboard Preview

### 📊 Executive Overview
<p align="center">
  <img src="images/1.png" width="95%">
</p>

### 🎯 Risk Profiles & Drivers
<p align="center">
  <img src="images/2.png" width="95%">
</p>

### ⚡ Engagement, Growth & Action Plan
<p align="center">
  <img src="images/3.png" width="95%">
</p>

---

## ✦ What is This?

An end-to-end HR analytics project built for the **Kayfa AI & Data Analytics Internship · Week 1 Task**.

> *"Why are employees leaving — and what can we do about it?"*

This isn't machine learning. It's exploratory analysis and storytelling — clean data, honest charts, and insights sharp enough to hand to an HR director tomorrow. Every finding ends with a concrete, budget-aware recommendation.

---

## ✦ Project Structure

```
employee-attrition-analytics/
│
├── 📓 employee_attrition_analytics.ipynb
│   ├── Section 1  Load & Combine
│   ├── Section 2  Cleaning & Preprocessing
│   ├── Section 3  EDA — 10 HR questions answered
│   └── Section 4  Key Findings & HR Recommendations
│
├── 🎛️  app.py                 ← Streamlit dashboard (6 tabs)
├── 📋  requirements.txt
├── 🖼️  images/                ← Dashboard screenshots
├── 📊  train.csv
└── 📊  test.csv
```

---

## ✦ The Pipeline

| # | Phase | What Happens |
|:--|:------|:-------------|
| 1 | **Load & Combine** | Merge train + test → 74,498-row DataFrame |
| 2 | **Cleaning** | Snake_case columns · null check · duplicate check · ordinal casting |
| 3 | **EDA** | 10 questions measuring attrition *rates* (%), not raw counts |
| 4 | **Dashboard** | Filterable Streamlit app — KPIs, charts, insights, action plan |

---

## ✦ The 10 HR Questions Answered

| # | Question | Difficulty |
|:--|:---------|:----------:|
| Q1 | What share of employees left & which role is losing the most? | 🟢 Easy |
| Q2 | Are overtime workers more likely to leave — and by how much? | 🟢 Easy |
| Q3 | Does remote work appear to keep people? | 🟢 Easy |
| Q4 | Within the same job level, do lower-paid employees leave more? | 🟡 Medium |
| Q5 | At what tenure stage is attrition highest? | 🟡 Medium |
| Q6 | Which satisfaction × work-life balance combo is the strongest flight-risk signal? | 🟡 Medium |
| Q7 | Do age, marital status & dependents change who leaves? | 🟡 Medium |
| Q8 | Does feeling "stuck" (no promotions/opportunities) drive attrition? | 🔴 Hard |
| Q9 | What is the single highest-risk employee profile? | 🔴 Hard |
| Q10 | If HR could fix only one thing next quarter — what should it be? | 🔴 Hard |

---

## ✦ Key Findings

| # | Finding | Recommended Action |
|:--|:--------|:-------------------|
| 1 | **Overtime** is the sharpest single attrition predictor (+20+ pts above avg) | Cap mandatory overtime; immediate policy memo to managers |
| 2 | **Low job satisfaction + Poor work-life balance** is the strongest flight-risk combo | Stay interviews within 2 weeks for any employee hitting this combination |
| 3 | **New employees (0–2 years)** churn at the highest rate | 30/60/90-day check-ins; strong first-manager assignment |
| 4 | **Remote workers** stay significantly longer (lowest attrition segment) | Pilot hybrid/remote for the 2 highest-attrition roles first |
| 5 | **Zero promotions** = highest career-stagnation attrition signal | Internal mobility program; transparent career ladders |
| 6 | **Lower pay within the same job level** drives exits — but only up to the Upper-Mid band | Raise the bottom 25% first; diminishing returns above that |
| 7 | **Young (18–30), single, no dependents** = highest-risk life stage | Mentorship, skill development, and early-tenure recognition |

---

## ✦ Dashboard Features

**Sidebar filters** — Job Level · Job Role · Gender · Remote Work · Marital Status

**Live KPIs** — Headcount · Attrition Rate · Avg Monthly Salary · Entry-Level Risk
> Attrition Rate card turns red automatically when rate exceeds 45%

**6 tabs:**
| Tab | Content |
|:----|:--------|
| 📊 Q1–Q3: Headlines | Overall attrition rate, job role comparison (volume + rate), overtime, remote work |
| 💰 Q4–Q5: Pay & Timeline | Pay fairness by level & band, retention timeline by tenure stage |
| ⚡ Q6–Q8: Engagement & Growth | Satisfaction × WLB heatmap, life stage analysis, career stagnation |
| 🎯 Q9–Q10: Risk & Drivers | Highest-risk profile chart, top 3 attrition drivers ranked by lift |
| 📈 Executive Summary | Three retention pillars with immediate action items |
| 💡 Action Plan | Budget-aware roadmap: Free → Low Cost → Medium Cost actions |

---

## ✦ Budget-Aware Action Plan

The dashboard includes a full HR action plan sorted by cost tier:

| Tier | Actions | Examples |
|:-----|:--------|:---------|
| 🟢 **Free** | 4 actions — start this week | Cap overtime · Stay interviews · Stretch projects · 30/60/90 check-ins |
| 🔵 **Low Cost** | 3 actions — next quarter | Internal mobility program · Hybrid pilot · Peer mentorship |
| 🟠 **Medium Cost** | 2 actions — next budget cycle | Salary band audit (bottom 25% only) · Promotion cadence review |

> Every action is tied directly to a question from the EDA — no generic HR advice.

---

## ✦ Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Dashboard opens at `http://localhost:8501`

---

## ✦ Deploy to Streamlit Cloud

```
1. Push repo to GitHub  (train.csv + test.csv must be included)
2. Go to share.streamlit.io
3. Connect repo → main file: app.py → Deploy
4. Get a public link in ~2 minutes
```

---

## ✦ Tech Stack

| Layer | Technology |
|:------|:-----------|
| 🐍 Language | Python 3.10 |
| 📊 Data | Pandas · NumPy |
| 📈 Charts | Plotly — bar, line, heatmap, horizontal bar |
| 🎛️ Dashboard | Streamlit |
| 📦 Dataset | Kaggle · Synthetic Employee Attrition · 74,498 rows |

---

<div align="center">

Built with ⚡ for **Kayfa AI & Data Analytics Internship · Week 1**

*Synthetic dataset — patterns are realistic but not real-world data.*

</div>