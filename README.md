# 🛡️ Enterprise Risk Management Dashboard
### AI-Powered Risk Intelligence Platform for Executive Decision Making

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Built by Harsh Bhatt | BCA Final Year | DSEU New Delhi | CGPA 9.2**

[LinkedIn](https://linkedin.com/in/harsh-bhatt-2275182b0) • [GitHub](https://github.com/harshbhatt1600) • [AlphaAgent](https://github.com/harshbhatt1600/AlphaAgent)

</div>

---

## 📸 Dashboard Preview

> **Executive Overview — Risk Intelligence at a Glance**

![Executive Overview](photos\Executive.png)
```
[ Show: Header, Alert Strips, KPI Cards, Donut Charts, Heatmap ]
```

> **Risk Register & Cybersecurity — Operational Intelligence**
![Risk Register & Cybersecurity](photos\risk&cyber.png)
```
[ Show: Filters, Scatter Chart, Color-coded Risk Table ]
```

> **Cybersecurity Deep Dive — Threat Intelligence**
![Cybersecurity Deep Dive](photos\cyber.png)
```
[ Show: CVSS Box Plot, Threat Actor Pie, Containment Donut ]
```

> **KRA/KPI Tracker — Performance Intelligence**
![KRA/KPI Tracker](photos\KRA_KPI.png)
```
[ Show: RAG Donut, Department Stacked Bar, Progress Bars ]
```

> **AI Risk Advisor — Natural Language Intelligence**
![AI Risk Advisor](photos\AI1.png)
![AI Risk Advisor](photos\AI2.png)
```
[ Show: Suggested Chips, Query, AI Response with Risk IDs ]
```

---

## 📌 Overview

The **Enterprise Risk Management Dashboard** is an end-to-end MVP that consolidates risk intelligence, cybersecurity threat data, and KPI performance metrics into a single executive-facing platform — augmented by a Groq-powered AI advisor that answers natural language queries with specific, data-driven insights.

Built to demonstrate:
- **Data sanitisation skills** — research-backed schema design following ISO 31000 and CVSS standards
- **Dashboard development skills** — multi-tab Streamlit application with interactive Plotly visualisations
- **AI analytics integration** — LLM-powered advisor that references exact Risk IDs, owner names, and days open
- **Production-grade thinking** — clean project structure, separation of concerns, error handling, session state management

> *"I do not expect a full working app, but a decent MVP that can demonstrate your data sanitisation and development skills with use of AI analytics."* — Recruiter Brief

Every requirement in that brief is met. Tick by tick.

---

## 🎯 What Problem Does This Solve?

Every organisation manages hundreds of risks across multiple departments simultaneously. The traditional approach — weekly Excel sheets from 8 departments, each with 500+ rows — means critical risks go unnoticed for months. RISK-0168 in this dashboard has been open for **540 days.**

This platform replaces spreadsheet chaos with:

| Old Way | This Dashboard |
|---------|---------------|
| 8 separate Excel files every Monday | One URL, four tabs, everything visible |
| Manual pivot tables to find critical risks | Auto-generated alert strips on load |
| No AI — manual analysis only | Natural language queries answered in seconds |
| No cybersecurity integration | Dedicated CVSS-scored threat register |
| No KPI visibility | RAG-status KPI tracker across 5 quarters |

---

## 🏗️ Architecture

```
erm_dashboard/
│
├── app.py                    ← Entry point — page config, global CSS, tab routing
│
├── data/
│   ├── generate_data.py      ← Generates all 3 datasets (ISO 31000 + CVSS aligned)
│   ├── risk_register.csv     ← 500 rows — enterprise risk register
│   ├── cyber_threats.csv     ← 150 rows — cybersecurity threat intelligence
│   └── kpi_data.csv          ← 200 rows — KRA/KPI performance data
│
├── pages/
│   ├── overview.py           ← Tab 1 — Executive Overview
│   ├── risk_cyber.py         ← Tab 2 — Risk Register & Cybersecurity
│   ├── kpi.py                ← Tab 3 — KRA/KPI Tracker
│   └── ai_analytics.py       ← Tab 4 — AI Risk Advisor (Groq)
│
├── utils/
│   └── helpers.py            ← Shared colour maps, chart helpers, data loader
│
├── .env                      ← API keys (never committed)
├── .env.example              ← Key template for contributors
├── .gitignore
└── requirements.txt
```

**Design principle:** Each file has exactly one job. `generate_data.py` only generates data. `helpers.py` only provides shared utilities. Each page only renders its own tab. This is **Separation of Concerns** — the same principle used in AlphaAgent and production-grade systems.

---

## 📊 Dashboard Tabs

### Tab 1 — Executive Overview
Designed for: **CEO, CFO, Board of Directors**

- **Alert strips** — auto-generated for critical risks and overdue risks on every load
- **12 KPI metric cards** — split across Risk Register and Cybersecurity
- Risk: Total, Critical, High, Open, Escalated, Closure Rate
- Cyber: Total Threats, Critical, Uncontained, High Breach Risk, Avg CVSS, Regulatory Alerts
- **3 donut charts** — Risks by Status / Severity / Category
- **Risk Heatmap** — Category × Severity (Plotly imshow, color-scaled)
- **Department risk distribution** — horizontal bar chart
- **Top risk owners by open risk count** — workload visibility
- **Cybersecurity threats by type** — bar chart
- **Top 10 Critical & Escalated Risks table** — color-coded, sortable

### Tab 2 — Risk Register & Cybersecurity
Designed for: **Risk Manager, CISO, IT Leadership**

**Risk Register section:**
- 4 filters — Category, Severity, Status, Department
- Live summary strip — updates on every filter change
- Severity and status breakdown bar charts
- Risk Age vs Risk Score scatter analysis — bubble sized by severity
- Full color-coded risk table — 13 columns, color-mapped severity and status

**Cybersecurity Deep Dive section:**
- 4 filters — Threat Type, Severity, Containment Status, Data Breach Risk
- 5 KPI cards — Avg CVSS, Uncontained, Patch Available, Regulatory Alerts
- Horizontal bar — threats by type and affected system
- Containment status donut
- CVSS score box plot by threat type
- Threat actor pie chart
- Full threat register table — 15 columns

### Tab 3 — KRA/KPI Tracker
Designed for: **Department Heads, Operations**

- 3 filters — Department, Quarter, RAG Status
- 5 summary cards — Total KPIs, Green, Amber, Red, Avg Achievement
- Overall RAG distribution donut
- RAG status by department stacked horizontal bar
- Average achievement % by department — color gradient (red → green)
- Quarterly trend line — with 90% target and 70% warning threshold lines
- Off-track KPIs (Red) per quarter bar chart
- Department deep dive — live progress bars per KPI with RAG emoji
- Full KPI register table — color-coded RAG status

### Tab 4 — AI Risk Advisor
Designed for: **Any level of management**

- Groq API — Llama 3.3 70B
- Full data context serialised and passed on every API call
- Risk register statistics, top 10 oldest risks, department breakdown
- Cybersecurity threat summary, top 10 critical threats
- KPI performance summary, worst performing KPIs
- System prompt engineered as **Senior ERM Consultant** persona
- Temperature = 0.3 — factual, consistent responses over creative ones
- 8 suggested query chips for common management questions
- Persistent conversation memory within session (last 20 messages)
- Most recent query displayed at top — no scrolling required
- Clear conversation button

**Example AI response:**

> *"Which are the top 5 risks we have not been able to close in the last 3 months?"*
>
> The AI responds with exact Risk IDs, owner names, days open, categories, departments, and specific recommended actions — not generic advice.

---

## 🗄️ Data Schema

### Why Generated Data Over Kaggle?

The recruiter brief specifically asked for *"clean column headings through research"* and demonstration of *"data sanitisation skills."*

Kaggle datasets are built for ML practice — generic column names, no internal consistency, no ERM or cybersecurity terminology. Creating the data from scratch allowed:

- **Research-backed schema** — column headings derived from ISO 31000 (risk management) and CVSS (cybersecurity) frameworks
- **Internal consistency** — closed risks always have actual closure dates, CVSS scores correctly map to severity levels, RAG status always reflects achievement percentage, high-severity risks have lower probability of closure
- **Domain authenticity** — real risk titles, real threat types, real KPI categories

### Risk Register — 500 rows

| Column | Type | Description |
|--------|------|-------------|
| Risk ID | String | Unique — RISK-XXXX format |
| Risk Title | String | Descriptive risk name — 50 unique titles across 6 categories |
| Category | Categorical | Operational / Financial / Strategic / Compliance / Reputational / Cybersecurity |
| Department | Categorical | 8 departments |
| Risk Owner | String | 12 named owners |
| Likelihood | Ordinal | Rare / Unlikely / Possible / Likely / Almost Certain |
| Severity | Ordinal | Low / Medium / High / Critical |
| Risk Score | Integer | Severity × Likelihood (1–20) — ISO 31000 matrix |
| Status | Categorical | Open / In Progress / Escalated / Closed / Mitigated |
| Date Identified | Date | Between 30 and 540 days ago |
| Target Closure Date | Date | 30–180 days after identification |
| Actual Closure Date | Date | Only populated for Closed/Mitigated — ensures consistency |
| Days Open | Integer | Calendar days — drives age analysis and AI context |
| Mitigation Action | String | 15 unique realistic remediation actions |
| Review Frequency | Categorical | Monthly / Quarterly / Bi-Annual / Annual |
| Escalated to Management | Boolean | Yes/No — weighted by status |

**Internal consistency rule:** High and Critical severity risks have weighted status distributions — they are significantly less likely to be Closed than Low severity risks. This reflects real-world risk management behaviour.

### Cybersecurity Threats — 150 rows

| Column | Type | Description |
|--------|------|-------------|
| Threat ID | String | Unique — CYBER-XXXX format |
| Threat Type | Categorical | 10 types — Ransomware, Phishing, DDoS, Insider Threat, Zero-Day, SQL Injection, MitM, Credential Stuffing, Supply Chain, Social Engineering |
| Affected System | Categorical | 12 systems — Customer Portal, ERP, Active Directory, Payment Gateway etc. |
| Threat Actor | Categorical | External Hacker / Nation State / Insider / Hacktivist / Organised Crime |
| CVSS Score | Float | 0.1–10.0 — mapped to severity following CVSS v3.1 standard |
| Severity | Ordinal | Low / Medium / High / Critical — derived from CVSS range |
| Business Impact | Ordinal | Independent severity assessment of business consequence |
| Detection Method | Categorical | SIEM Alert / Penetration Testing / IDS/IPS / SOC Monitoring etc. |
| Containment Status | Categorical | Contained / Partially Contained / Uncontained |
| Data Breach Risk | Ordinal | High / Medium / Low |
| Regulatory Notification Required | Boolean | Yes / No — GDPR/regulatory implication flag |
| Patch Available | Categorical | Yes / No / Partial |

**CVSS mapping (following industry standard v3.1):**
- Critical severity → CVSS 9.0–10.0
- High severity → CVSS 7.0–8.9
- Medium severity → CVSS 4.0–6.9
- Low severity → CVSS 0.1–3.9

### KRA/KPI Data — 200 rows

| Column | Type | Description |
|--------|------|-------------|
| Department | Categorical | 8 departments |
| KRA | String | Key Result Area — strategic objective |
| KPI | String | Specific measurable indicator |
| Target | Numeric | Defined performance target |
| Actual | Numeric | Simulated actual (Target × random variance 0.7–1.15) |
| Unit | String | %, hrs, score, ratio, count, INR |
| Achievement % | Float | (Actual/Target) × 100 — direction-aware for inverse metrics |
| RAG Status | Categorical | Green ≥90% / Amber 70–89% / Red <70% |
| Quarter | Categorical | Q1 2025 through Q1 2026 — 5 quarters |
| KPI Owner | String | Named owner per KPI |
| Comments | String | 7 realistic management commentary options |

**Direction-aware achievement logic:** For metrics where lower is better (Defect Rate, Churn Rate, Budget Variance, Time to Hire), achievement is calculated as Target/Actual × 100 rather than Actual/Target × 100. This ensures RAG status is correctly assigned regardless of metric direction — a data sanitisation detail most dashboards miss.

---

## 🤖 AI Risk Advisor — Technical Deep Dive

### How It Works

The AI advisor doesn't use a generic LLM prompt. Before every API call, `build_context()` serialises the actual dataset into a structured intelligence brief:

```
=== ENTERPRISE RISK MANAGEMENT DATA CONTEXT ===

--- RISK REGISTER SUMMARY ---
Total Risks: 500
Critical Severity: 71
Currently Open: 111
Escalated to Management: 56
Overdue Past Target Closure: 290

--- TOP 10 OLDEST UNRESOLVED RISKS ---
RISK-0168 | GDPR data protection violation | Compliance | HR | Critical | 540 days | Rajiv Sharma
RISK-0264 | System downtime during peak hours | Operational | Operations | Medium | 538 days | Suresh Reddy
...

--- TOP 10 CRITICAL/HIGH CYBER THREATS ---
CYBER-0042 | Ransomware | Core Banking System | CVSS 9.8 | Critical | Uncontained
...
```

This context is attached to every single API call. The LLM reads real data and reasons over it — which is why responses reference exact Risk IDs, owner names, CVSS scores, and days open rather than producing generic advice.

### System Prompt Design

The system prompt engineers the LLM as a **Senior ERM Consultant** with explicit instructions to:
- Reference exact Risk IDs and Threat IDs in every response
- Name risk owners and departments specifically
- Prioritise actionable recommendations over generic guidance
- Highlight regulatory and compliance implications
- Connect operational risks to cybersecurity threats to KPI gaps
- Keep responses under 400 words for executive consumption

### Model Configuration

| Parameter | Value | Reason |
|-----------|-------|--------|
| Model | llama-3.3-70b-versatile | Best instruction-following at Groq's free tier |
| Temperature | 0.3 | Factual consistency — executives need reliable data, not creative responses |
| Max tokens | 1000 | Enough for detailed analysis, short enough for executive reading |
| Context window | Last 20 messages | Conversation memory without hitting token limits |

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| Frontend | Streamlit | Latest | Industry standard for data dashboards — pure Python, no HTML/CSS |
| Charts | Plotly | Latest | Interactive — zoom, hover, filter — management-ready |
| Data Processing | Pandas | Latest | Industry standard for tabular data manipulation |
| AI | Groq API | Latest | Fastest inference, free tier, Llama 3.3 70B |
| Data Generation | Faker | Latest | Realistic names, dates, values — no real company data |
| Environment | python-dotenv | Latest | Secure API key management |

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/harshbhatt1600/erm-dashboard
cd erm_dashboard

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and add your Groq API key:
# GROQ_API_KEY=your_key_here

# 5. Generate the data
cd data
python generate_data.py
cd ..

# 6. Launch the dashboard
streamlit run app.py
```

### Expected Output After Data Generation
```
Generating Risk Register (500 rows)...
Risk Register saved — 500 rows
Generating Cybersecurity Threats (150 rows)...
Cyber Threats saved — 150 rows
Generating KPI Data...
KPI Data saved — 200 rows

All data generated successfully!
```

---

## 💬 AI Advisor — Example Queries

These are built into the dashboard as suggested query chips:

| Query | What it demonstrates |
|-------|---------------------|
| *Which are the top 5 risks we have not been able to close in the last 3 months?* | Oldest unresolved risks with owner accountability |
| *What are our most critical cybersecurity threats right now?* | CVSS-ranked threats with containment status |
| *Which department has the highest risk exposure and why?* | Cross-tab risk concentration analysis |
| *Which KPIs are most off-track and what is the business impact?* | Red RAG KPIs with consequence mapping |
| *Are there any regulatory risks that need immediate escalation?* | Compliance and GDPR risk identification |
| *Give me an executive summary for the board meeting* | Consolidated risk posture narrative |
| *Which risk owners have the highest workload?* | Owner accountability and capacity analysis |
| *What are the top 3 interconnected risks that could trigger a cascade failure?* | Risk correlation and systemic threat analysis |

---

## 🔒 Security & Compliance Considerations

- API keys stored in `.env` — never committed to version control
- `.gitignore` excludes `.env`, `__pycache__`, `.venv`, and all CSV files
- No real company or personal data used — all data is programmatically generated
- GDPR-aware data model — `Regulatory Notification Required` field flags threats requiring regulatory disclosure
- Audit-ready design — Risk IDs, owner names, and timestamps on all records

---

## 📐 Design Decisions

### Why 4 Tabs?
Each tab serves a distinct user persona with different information needs. Combining them would produce cluttered, overwhelming views — exactly what executive dashboards must avoid. Clean separation = better decision making.

### Why Not Use a Live Database?
This is an MVP. Adding PostgreSQL, authentication, and live connections would demonstrate infrastructure skills but obscure the core value — risk intelligence and AI analytics. The focus is on what the recruiter asked for.

### Why Streamlit Over Flask/Django?
Streamlit is the industry standard for data analytics dashboards among data scientists and analysts. Flask and Django are better for full web applications with complex routing. Streamlit keeps the focus on analytics logic — appropriate for this use case and audience.

### Why Generated Data Over Kaggle?
Answered in the Data Schema section above. Short version: Kaggle data can't be data-sanitised. Generated data can be designed from scratch to meet exact schema requirements.

---

## 🗺️ Potential Extensions

| Feature | Description | Complexity |
|---------|-------------|------------|
| Live database | PostgreSQL backend — persist actual company risk data | Medium |
| Authentication | Role-based access — CEO sees different view than risk manager | Medium |
| Email alerts | Automated notifications for critical risks breaching thresholds | Low |
| PDF export | Downloadable board-ready risk report (ReportLab) | Low |
| Real data connectors | API integration with ServiceNow, Jira, or existing GRC tools | High |
| Predictive risk scoring | ML model to predict which open risks are unlikely to close | High |
| Multi-organisation | SaaS version — separate data per company | High |

---

## 👤 About the Author

**Harsh Bhatt** — Final Year BCA Student, Delhi Skill and Entrepreneurship University (CGPA 9.2/10)

Actively pursuing Data Analyst and Data Science roles in Delhi NCR. This project was built to demonstrate production-grade thinking, domain research capability, and AI integration skills — going beyond static dashboards to build intelligent, decision-support systems.

**Other Projects:**
- [AlphaAgent](https://github.com/harshbhatt1600/AlphaAgent) — Autonomous stock market AI agent with ReAct loop, PostgreSQL caching, Groq LLM integration, and PDF report generation
- [Retail Business Intelligence Dashboard](https://github.com/harshbhatt1600) — PostgreSQL star schema, DAX, Power BI
- [Job Market Intelligence Dashboard](https://github.com/harshbhatt1600) — 479K+ job postings, Power BI
- [Credit Card Customer Intelligence](https://github.com/harshbhatt1600) — Python/Pandas, 8,950 customers, behavioural segmentation

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">

**Built with 🛡️ for enterprise risk intelligence**

*Harsh Bhatt | DSEU New Delhi | 2026*

</div>