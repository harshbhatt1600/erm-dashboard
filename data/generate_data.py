import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)
Faker.seed(42)

# ── CONSTANTS ──────────────────────────────────────────────────────────────────

DEPARTMENTS = [
    "Information Technology", "Finance", "Human Resources",
    "Operations", "Legal & Compliance", "Supply Chain",
    "Customer Experience", "Strategy & Planning"
]

RISK_CATEGORIES = [
    "Operational", "Financial", "Strategic",
    "Compliance", "Reputational", "Cybersecurity"
]

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
SEVERITY_WEIGHTS = [20, 35, 30, 15]

STATUS_OPTIONS = ["Open", "In Progress", "Escalated", "Closed", "Mitigated"]
STATUS_WEIGHTS = [25, 30, 10, 25, 10]

LIKELIHOOD_LEVELS = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]

MITIGATION_ACTIONS = [
    "Implement additional access controls",
    "Conduct staff awareness training",
    "Review and update policy framework",
    "Deploy monitoring and alerting tools",
    "Engage third-party audit firm",
    "Establish incident response protocol",
    "Strengthen vendor due diligence process",
    "Implement multi-factor authentication",
    "Conduct quarterly risk reviews",
    "Update business continuity plan",
    "Enhance data encryption standards",
    "Deploy endpoint detection and response",
    "Establish backup and recovery procedures",
    "Review regulatory compliance framework",
    "Implement zero-trust network architecture"
]

RISK_OWNERS = [
    "Rajiv Sharma", "Priya Mehta", "Ankit Gupta", "Sneha Patel",
    "Vikram Singh", "Neha Joshi", "Rohit Kumar", "Divya Nair",
    "Amit Verma", "Pooja Agarwal", "Suresh Reddy", "Kavita Shah"
]

OPERATIONAL_RISKS = [
    "Process failure in core banking system",
    "Supply chain disruption due to vendor bankruptcy",
    "Key person dependency in critical operations",
    "Manual process errors in financial reporting",
    "System downtime during peak business hours",
    "Inadequate business continuity planning",
    "Third party vendor non-performance",
    "Fraud in procurement process",
    "Regulatory non-compliance in operations",
    "Workforce shortage in critical departments"
]

FINANCIAL_RISKS = [
    "Foreign exchange rate volatility impact",
    "Credit default by major client",
    "Liquidity shortage during market stress",
    "Budget overrun in capital projects",
    "Revenue loss due to contract termination",
    "Pension fund liability exposure",
    "Interest rate risk on variable loans",
    "Tax compliance penalties",
    "Audit qualification risk",
    "Insurance coverage gap identified"
]

STRATEGIC_RISKS = [
    "Market share loss to new competitor",
    "Digital transformation initiative failure",
    "Merger and acquisition integration risk",
    "Failure to achieve ESG targets",
    "Brand positioning misalignment",
    "New product launch failure",
    "Talent acquisition strategy gap",
    "Geographic expansion risk",
    "Board level governance weakness",
    "Innovation pipeline insufficient"
]

COMPLIANCE_RISKS = [
    "GDPR data protection violation",
    "Anti-money laundering control failure",
    "Health and safety regulation breach",
    "Employment law non-compliance",
    "Environmental regulation violation",
    "Financial reporting standard deviation",
    "Data retention policy non-adherence",
    "Export control regulation breach",
    "Consumer protection law violation",
    "Whistleblower policy inadequacy"
]

REPUTATIONAL_RISKS = [
    "Negative media coverage of data breach",
    "Social media crisis mismanagement",
    "Customer complaint escalation to regulator",
    "Executive misconduct allegation",
    "Product recall public impact",
    "ESG rating downgrade by agency",
    "Supplier ethics violation link",
    "Employee discrimination lawsuit",
    "Data privacy scandal exposure",
    "Corporate governance failure publicity"
]

CYBER_RISKS = [
    "Ransomware attack on production systems",
    "Phishing attack on executive accounts",
    "Insider threat data exfiltration",
    "Third party API vulnerability exploitation",
    "DDoS attack on customer portal",
    "Zero-day vulnerability in core software",
    "Credential stuffing on customer accounts",
    "Supply chain software compromise",
    "Cloud misconfiguration data exposure",
    "Social engineering attack on IT staff"
]

ALL_RISKS = {
    "Operational": OPERATIONAL_RISKS,
    "Financial": FINANCIAL_RISKS,
    "Strategic": STRATEGIC_RISKS,
    "Compliance": COMPLIANCE_RISKS,
    "Reputational": REPUTATIONAL_RISKS,
    "Cybersecurity": CYBER_RISKS
}

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────

def get_risk_score(severity, likelihood):
    severity_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    likelihood_map = {
        "Rare": 1, "Unlikely": 2, "Possible": 3,
        "Likely": 4, "Almost Certain": 5
    }
    return severity_map[severity] * likelihood_map[likelihood]

def get_status_for_severity(severity):
    # Higher severity = less likely to be closed
    if severity == "Critical":
        return random.choices(
            STATUS_OPTIONS,
            weights=[30, 35, 20, 5, 10]
        )[0]
    elif severity == "High":
        return random.choices(
            STATUS_OPTIONS,
            weights=[25, 35, 15, 15, 10]
        )[0]
    elif severity == "Medium":
        return random.choices(
            STATUS_OPTIONS,
            weights=[20, 30, 5, 30, 15]
        )[0]
    else:
        return random.choices(
            STATUS_OPTIONS,
            weights=[10, 20, 2, 45, 23]
        )[0]

def generate_dates(status):
    # Date identified — between 1 and 18 months ago
    days_ago = random.randint(30, 540)
    date_identified = datetime.today() - timedelta(days=days_ago)

    # Target closure — between 30 and 180 days after identification
    target_closure = date_identified + timedelta(days=random.randint(30, 180))

    # Actual closure — only if closed or mitigated
    if status in ["Closed", "Mitigated"]:
        actual_closure = date_identified + timedelta(
            days=random.randint(20, (target_closure - date_identified).days + 30)
        )
        days_open = (actual_closure - date_identified).days
    else:
        actual_closure = None
        days_open = (datetime.today() - date_identified).days

    return (
        date_identified.strftime("%Y-%m-%d"),
        target_closure.strftime("%Y-%m-%d"),
        actual_closure.strftime("%Y-%m-%d") if actual_closure else None,
        days_open
    )

# ── GENERATE RISK REGISTER ─────────────────────────────────────────────────────

def generate_risk_register(n=500):
    records = []
    used_risks = {cat: list(risks) for cat, risks in ALL_RISKS.items()}

    for i in range(1, n + 1):
        category = random.choices(
            RISK_CATEGORIES,
            weights=[20, 15, 15, 15, 10, 25]
        )[0]

        risk_pool = used_risks[category]
        if not risk_pool:
            risk_pool = list(ALL_RISKS[category])
            used_risks[category] = risk_pool

        risk_title = random.choice(risk_pool)
        severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS)[0]
        likelihood = random.choice(LIKELIHOOD_LEVELS)
        status = get_status_for_severity(severity)
        department = random.choice(DEPARTMENTS)
        owner = random.choice(RISK_OWNERS)
        risk_score = get_risk_score(severity, likelihood)
        date_identified, target_closure, actual_closure, days_open = generate_dates(status)
        last_updated = (
            datetime.today() - timedelta(days=random.randint(1, 30))
        ).strftime("%Y-%m-%d")

        records.append({
            "Risk ID": f"RISK-{i:04d}",
            "Risk Title": risk_title,
            "Category": category,
            "Department": department,
            "Risk Owner": owner,
            "Likelihood": likelihood,
            "Severity": severity,
            "Risk Score": risk_score,
            "Status": status,
            "Date Identified": date_identified,
            "Target Closure Date": target_closure,
            "Actual Closure Date": actual_closure,
            "Days Open": days_open,
            "Last Updated": last_updated,
            "Mitigation Action": random.choice(MITIGATION_ACTIONS),
            "Review Frequency": random.choice(
                ["Monthly", "Quarterly", "Bi-Annual", "Annual"]
            ),
            "Escalated to Management": "Yes" if status == "Escalated" else random.choice(
                ["Yes", "No", "No", "No"]
            )
        })

    return pd.DataFrame(records)

# ── GENERATE CYBERSECURITY THREATS ─────────────────────────────────────────────

THREAT_TYPES = [
    "Ransomware", "Phishing", "DDoS", "Insider Threat",
    "Zero-Day Exploit", "SQL Injection", "Man-in-the-Middle",
    "Credential Stuffing", "Supply Chain Attack", "Social Engineering"
]

AFFECTED_SYSTEMS = [
    "Customer Portal", "Core Banking System", "HR Management System",
    "ERP Platform", "Email Infrastructure", "Cloud Storage",
    "Payment Gateway", "VPN & Remote Access", "Active Directory",
    "Mobile Application", "API Gateway", "Data Warehouse"
]

DETECTION_METHODS = [
    "SIEM Alert", "Penetration Testing", "Employee Report",
    "Automated Scan", "Threat Intelligence Feed",
    "Third Party Audit", "IDS/IPS Alert", "SOC Monitoring"
]

THREAT_ACTORS = [
    "External Hacker", "Nation State", "Insider Employee",
    "Competitor", "Hacktivist", "Organised Crime", "Unknown"
]

def generate_cyber_threats(n=150):
    records = []

    for i in range(1, n + 1):
        severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS)[0]
        status = get_status_for_severity(severity)
        date_detected = (
            datetime.today() - timedelta(days=random.randint(1, 365))
        ).strftime("%Y-%m-%d")

        # CVSS score — mapped to severity
        cvss_map = {
            "Low": round(random.uniform(0.1, 3.9), 1),
            "Medium": round(random.uniform(4.0, 6.9), 1),
            "High": round(random.uniform(7.0, 8.9), 1),
            "Critical": round(random.uniform(9.0, 10.0), 1)
        }
        cvss_score = cvss_map[severity]

        days_since_detection = random.randint(1, 365)

        records.append({
            "Threat ID": f"CYBER-{i:04d}",
            "Threat Type": random.choice(THREAT_TYPES),
            "Affected System": random.choice(AFFECTED_SYSTEMS),
            "Threat Actor": random.choice(THREAT_ACTORS),
            "CVSS Score": cvss_score,
            "Severity": severity,
            "Business Impact": random.choice(SEVERITY_LEVELS),
            "Detection Method": random.choice(DETECTION_METHODS),
            "Status": status,
            "Assigned To": random.choice(RISK_OWNERS),
            "Date Detected": date_detected,
            "Days Since Detection": days_since_detection,
            "Patch Available": random.choice(["Yes", "No", "Partial"]),
            "Data Breach Risk": random.choice(["High", "Medium", "Low"]),
            "Regulatory Notification Required": random.choice(["Yes", "No"]),
            "Containment Status": random.choice(
                ["Contained", "Partially Contained", "Uncontained"]
            )
        })

    return pd.DataFrame(records)

# ── GENERATE KRA/KPI DATA ──────────────────────────────────────────────────────

KRAS_AND_KPIS = {
    "Information Technology": [
        ("System Availability", "Uptime %", 99.9, "%"),
        ("Incident Response", "Avg Resolution Time (hrs)", 4, "hrs"),
        ("Cybersecurity", "Security Incidents Resolved %", 95, "%"),
        ("Digital Transformation", "Projects On-Time Delivery %", 85, "%"),
        ("IT Cost Efficiency", "IT Cost as % of Revenue", 8, "%"),
    ],
    "Finance": [
        ("Revenue Growth", "Revenue Growth Rate %", 15, "%"),
        ("Cost Management", "Operating Cost Reduction %", 10, "%"),
        ("Financial Reporting", "Reports Delivered On Time %", 100, "%"),
        ("Budget Adherence", "Budget Variance %", 5, "%"),
        ("Audit Compliance", "Audit Findings Resolved %", 90, "%"),
    ],
    "Human Resources": [
        ("Talent Acquisition", "Time to Hire (days)", 30, "days"),
        ("Employee Retention", "Retention Rate %", 90, "%"),
        ("Training & Development", "Training Hours per Employee", 40, "hrs"),
        ("Employee Engagement", "Engagement Score", 75, "score"),
        ("Diversity & Inclusion", "Diversity Ratio %", 40, "%"),
    ],
    "Operations": [
        ("Process Efficiency", "Process Automation Rate %", 70, "%"),
        ("Quality Management", "Defect Rate %", 2, "%"),
        ("Customer Satisfaction", "CSAT Score", 85, "score"),
        ("Operational Cost", "Cost per Transaction", 50, "INR"),
        ("SLA Adherence", "SLA Compliance %", 95, "%"),
    ],
    "Legal & Compliance": [
        ("Regulatory Compliance", "Compliance Rate %", 100, "%"),
        ("Risk Management", "Risks Closed on Time %", 80, "%"),
        ("Policy Management", "Policies Reviewed Annually %", 100, "%"),
        ("Legal Disputes", "Cases Resolved %", 75, "%"),
        ("Training Compliance", "Staff Trained on Compliance %", 95, "%"),
    ],
    "Supply Chain": [
        ("Vendor Performance", "On-Time Delivery Rate %", 92, "%"),
        ("Inventory Management", "Inventory Turnover Ratio", 8, "ratio"),
        ("Cost Optimisation", "Procurement Cost Savings %", 12, "%"),
        ("Supplier Risk", "High Risk Vendors Mitigated %", 85, "%"),
        ("Sustainability", "Sustainable Suppliers %", 60, "%"),
    ],
    "Customer Experience": [
        ("Customer Retention", "Churn Rate %", 5, "%"),
        ("Net Promoter Score", "NPS Score", 50, "score"),
        ("Query Resolution", "First Call Resolution %", 80, "%"),
        ("Digital Adoption", "Digital Channel Usage %", 65, "%"),
        ("Complaint Management", "Complaints Resolved in 48hrs %", 90, "%"),
    ],
    "Strategy & Planning": [
        ("Strategic Initiatives", "Initiatives On-Track %", 80, "%"),
        ("Market Expansion", "New Markets Entered", 2, "count"),
        ("Innovation", "New Products Launched", 3, "count"),
        ("ESG Performance", "ESG Score", 70, "score"),
        ("Stakeholder Satisfaction", "Board Satisfaction Score", 80, "score"),
    ]
}

def get_rag_status(actual, target, unit):
    # For metrics where lower is better
    lower_is_better = ["Defect Rate %", "Churn Rate %",
                       "Budget Variance %", "Time to Hire (days)",
                       "IT Cost as % of Revenue", "Cost per Transaction"]

    if unit in lower_is_better or "cost" in unit.lower():
        achievement = (target / actual * 100) if actual > 0 else 0
    else:
        achievement = (actual / target * 100) if target > 0 else 0

    if achievement >= 90:
        return "Green", round(achievement, 1)
    elif achievement >= 70:
        return "Amber", round(achievement, 1)
    else:
        return "Red", round(achievement, 1)

def generate_kpi_data():
    records = []
    quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"]

    for department, kpis in KRAS_AND_KPIS.items():
        for kra, kpi_name, target, unit in kpis:
            for quarter in quarters:
                # Simulate realistic actual vs target
                variance = random.uniform(0.7, 1.15)
                actual = round(target * variance, 1)

                rag_status, achievement_pct = get_rag_status(
                    actual, target, kpi_name
                )

                records.append({
                    "Department": department,
                    "KRA": kra,
                    "KPI": kpi_name,
                    "Target": target,
                    "Actual": actual,
                    "Unit": unit,
                    "Achievement %": achievement_pct,
                    "RAG Status": rag_status,
                    "Quarter": quarter,
                    "KPI Owner": random.choice(RISK_OWNERS),
                    "Comments": random.choice([
                        "On track with mitigation plan in place",
                        "Requires immediate management attention",
                        "Improvement noted from last quarter",
                        "External factors impacting performance",
                        "New initiatives launched to address gap",
                        "Consistent performance maintained",
                        "Under review by senior management"
                    ])
                })

    return pd.DataFrame(records)

# ── MAIN — GENERATE AND SAVE ALL DATA ─────────────────────────────────────────

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))

    print("Generating Risk Register (500 rows)...")
    risk_df = generate_risk_register(500)
    risk_df.to_csv(os.path.join(output_dir, "risk_register.csv"), index=False)
    print(f"Risk Register saved — {len(risk_df)} rows")

    print("Generating Cybersecurity Threats (150 rows)...")
    cyber_df = generate_cyber_threats(150)
    cyber_df.to_csv(os.path.join(output_dir, "cyber_threats.csv"), index=False)
    print(f"Cyber Threats saved — {len(cyber_df)} rows")

    print("Generating KRA/KPI Data...")
    kpi_df = generate_kpi_data()
    kpi_df.to_csv(os.path.join(output_dir, "kpi_data.csv"), index=False)
    print(f"KPI Data saved — {len(kpi_df)} rows")

    print("\nAll data generated successfully!")
    print(f"Risk Register: {len(risk_df)} rows")
    print(f"Cyber Threats: {len(cyber_df)} rows")
    print(f"KPI Data: {len(kpi_df)} rows")