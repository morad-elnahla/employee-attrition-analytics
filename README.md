<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Syne&weight=800&size=36&pause=1000&color=E45756&center=true&vCenter=true&width=600&lines=Employee+Attrition+⚡;Who+Leaves+%26+Why;Data+Analytics+End-to-End)](https://git.io/typing-svg)

[![Python](https://img.shields.io/badge/Python-3.10-E8FF47?style=for-the-badge&logo=python&logoColor=black&labelColor=0a0c10)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-E8FF47?style=for-the-badge&logo=pandas&logoColor=black&labelColor=0a0c10)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-E8FF47?style=for-the-badge&logo=plotly&logoColor=black&labelColor=0a0c10)](https://plotly.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-E8FF47?style=for-the-badge&logo=streamlit&logoColor=black&labelColor=0a0c10)](https://streamlit.io)

> **74,498 employee records. 13 analyses. One dashboard HR can actually use.**

| 👥 Total Employees | 📉 Attrition Rate | 💰 Avg Salary | 🔍 Analyses |
|:-----------------:|:-----------------:|:-------------:|:-----------:|
| **74,498** | **47.5%** | **~$6,500** | **13** |

**[🚀 Try the Live Dashboard →](https://your-app.streamlit.app)**

</div>

---

## ✦ What is This?

An end-to-end HR analytics project that answers one question:

> *"Why are employees leaving — and what can we do about it?"*

This isn't machine learning. It's exploratory analysis and storytelling — clean data, honest charts, and insights sharp enough to hand to an HR director tomorrow.

---

## ✦ Screenshots

*(Add your dashboard screenshots here after deployment)*

---

## ✦ Project Structure

```
employee-attrition-dashboard/
│
├── 📓 employee_attrition_analytics.ipynb
│   ├── Section 1  Load & Combine
│   ├── Section 2  Cleaning & Preprocessing
│   ├── Section 3  EDA — 13 analyses
│   └── Section 4  Key Findings & HR Recommendations
│
├── 🎛️  app.py                 ← Streamlit dashboard
├── 📋  requirements.txt
├── 📊  train.csv
└── 📊  test.csv
```

---

## ✦ The Pipeline

| # | Phase | What Happens |
|:--|:------|:-------------|
| 1 | **Load & Combine** | Merge train + test → 74,498-row DataFrame |
| 2 | **Cleaning** | Snake_case columns · null check · duplicate check · ordinal casting |
| 3 | **EDA** | 13 analyses measuring attrition *rates* (%), not raw counts |
| 4 | **Dashboard** | Filterable Streamlit app — KPIs, charts, findings |

---

## ✦ Key Findings

| # | Finding | Recommended Action |
|:--|:--------|:-------------------|
| 1 | **Overtime** is the sharpest single attrition predictor | Cap mandatory overtime; introduce compensatory time-off |
| 2 | **Low job satisfaction** nearly doubles attrition risk | Regular 1-on-1s; satisfaction pulse surveys; clear growth paths |
| 3 | **Entry-level employees** churn at the highest rate | Structured onboarding + mentorship; 6-month and 1-year milestones |
| 4 | **Remote workers** stay significantly longer | Expand hybrid/remote eligibility where feasible |
| 5 | **Zero promotions** = highest attrition in the dataset | Review promotion cadence; create visible career ladders |
| 6 | **Lower income** correlates strongly with leaving | Benchmark salaries; prioritize raises in high-attrition roles |
| 7 | **Long commutes** compound into burnout and exit | Remote flexibility for high-distance employees |

---

## ✦ Dashboard Features

**Sidebar filters** — Gender · Job Role · Remote Work · Marital Status · Job Level

**Live KPIs** — Total Employees · Attrition Rate · Avg Salary · Avg Age
> Attrition Rate card turns red automatically when rate exceeds 30%

**6 chart sections** — Overview · Compensation · Flexibility & Growth · Role & Seniority · Demographics · Correlation

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
| 📈 Charts | Plotly — violin, box, bar, line, pie, correlation |
| 🎛️ Dashboard | Streamlit |
| 📦 Dataset | Kaggle · Synthetic Employee Attrition · 74,498 rows |

---

<div align="center">

Built with ⚡ for **Kayfa AI & Data Analytics Internship · Week 1**

*Synthetic dataset — patterns are realistic but not real-world data.*

</div>
