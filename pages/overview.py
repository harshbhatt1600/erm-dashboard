import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import (
    get_risk_summary, get_cyber_summary,
    donut_chart, bar_chart, heatmap_chart,
    SEVERITY_COLOURS, STATUS_COLOURS, CATEGORY_COLOURS
)

def render(risk_df, cyber_df):

    # ── SUMMARY STATS ──────────────────────────────────────────────────────────
    rs = get_risk_summary(risk_df)
    cs = get_cyber_summary(cyber_df)

    # ── ALERT STRIP ────────────────────────────────────────────────────────────
    if rs["critical"] > 0:
        st.markdown(f"""
        <div class="alert-critical">
            🚨 <strong>{rs["critical"]} Critical Risks</strong> require
            immediate executive attention —
            {rs["escalated"]} currently escalated to management
        </div>""", unsafe_allow_html=True)

    if rs["overdue"] > 0:
        st.markdown(f"""
        <div class="alert-warning">
            ⚠️ <strong>{rs["overdue"]} risks are overdue</strong>
            past their target closure date
        </div>""", unsafe_allow_html=True)

    # ── KPI CARDS ROW 1 — RISK REGISTER ───────────────────────────────────────
    st.markdown(
        '<div class="section-header">Risk Register Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Risks",      rs["total"])
    c2.metric("Critical",         rs["critical"],
              delta=f"{round(rs['critical']/rs['total']*100,1)}% of total",
              delta_color="inverse")
    c3.metric("High Severity",    rs["high"])
    c4.metric("Open Risks",       rs["open"])
    c5.metric("Escalated",        rs["escalated"],
              delta_color="inverse")
    c6.metric("Closure Rate",     f"{rs['closure_rate']}%",
              delta=f"Avg {rs['avg_days_open']} days open")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI CARDS ROW 2 — CYBERSECURITY ───────────────────────────────────────
    st.markdown(
        '<div class="section-header">Cybersecurity Threat Overview</div>',
        unsafe_allow_html=True
    )

    d1, d2, d3, d4, d5, d6 = st.columns(6)
    d1.metric("Total Threats",      cs["total"])
    d2.metric("Critical Threats",   cs["critical"],
              delta_color="inverse")
    d3.metric("Uncontained",        cs["uncontained"],
              delta_color="inverse")
    d4.metric("High Breach Risk",   cs["breach_risk"],
              delta_color="inverse")
    d5.metric("Avg CVSS Score",     cs["avg_cvss"])
    d6.metric("Regulatory Alerts",  cs["notification"],
              delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ROW 1 ───────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Risk Distribution Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        # Donut — risk by status
        status_counts = risk_df["Status"].value_counts()
        fig = donut_chart(
            labels=status_counts.index.tolist(),
            values=status_counts.values.tolist(),
            colours=[STATUS_COLOURS.get(s, "#95a5a6")
                     for s in status_counts.index],
            title="Risks by Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Donut — risk by severity
        sev_counts = risk_df["Severity"].value_counts()
        fig2 = donut_chart(
            labels=sev_counts.index.tolist(),
            values=sev_counts.values.tolist(),
            colours=[SEVERITY_COLOURS.get(s, "#95a5a6")
                     for s in sev_counts.index],
            title="Risks by Severity"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        # Donut — risk by category
        cat_counts = risk_df["Category"].value_counts()
        fig3 = donut_chart(
            labels=cat_counts.index.tolist(),
            values=cat_counts.values.tolist(),
            colours=[CATEGORY_COLOURS.get(c, "#95a5a6")
                     for c in cat_counts.index],
            title="Risks by Category"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── CHARTS ROW 2 ───────────────────────────────────────────────────────────
    col4, col5 = st.columns(2)

    with col4:
        # Bar — risks by department
        dept_counts = (
            risk_df.groupby("Department")
            .size().reset_index(name="Count")
            .sort_values("Count", ascending=True)
        )
        fig4 = bar_chart(
            dept_counts, x_col="Count", y_col="Department",
            title="Risk Count by Department",
            orientation="h"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col5:
        # Heatmap — category vs severity
        fig5 = heatmap_chart(
            risk_df,
            x_col="Severity",
            y_col="Category",
            value_col="Risk ID",
            title="Risk Heatmap — Category vs Severity"
        )
        st.plotly_chart(fig5, use_container_width=True)

    # ── CHARTS ROW 3 ───────────────────────────────────────────────────────────
    col6, col7 = st.columns(2)

    with col6:
        # Bar — top risk owners by open risk count
        owner_counts = (
            risk_df[risk_df["Status"].isin(["Open", "In Progress", "Escalated"])]
            .groupby("Risk Owner")
            .size().reset_index(name="Open Risks")
            .sort_values("Open Risks", ascending=False)
            .head(10)
        )
        fig6 = bar_chart(
            owner_counts,
            x_col="Risk Owner", y_col="Open Risks",
            title="Top 10 Risk Owners by Open Risk Count"
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col7:
        # Bar — cybersecurity threats by type
        threat_counts = (
            cyber_df.groupby("Threat Type")
            .size().reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )
        fig7 = bar_chart(
            threat_counts,
            x_col="Threat Type", y_col="Count",
            title="Cybersecurity Threats by Type"
        )
        st.plotly_chart(fig7, use_container_width=True)

    # ── TOP CRITICAL RISKS TABLE ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Top Critical & Escalated Risks</div>',
        unsafe_allow_html=True
    )

    top_risks = (
        risk_df[risk_df["Severity"].isin(["Critical", "High"])]
        .sort_values(["Risk Score", "Days Open"], ascending=[False, False])
        .head(10)[["Risk ID", "Risk Title", "Category", "Department",
                   "Severity", "Status", "Risk Score",
                   "Days Open", "Risk Owner", "Mitigation Action"]]
    )

    st.dataframe(
        top_risks.style
        .map(lambda v: f"background-color: {SEVERITY_COLOURS.get(v,'#fff')}22; "
                       f"color: {SEVERITY_COLOURS.get(v,'#333')}; font-weight:600",
             subset=["Severity"])
        .map(lambda v: f"background-color: {STATUS_COLOURS.get(v,'#fff')}22; "
                       f"color: {STATUS_COLOURS.get(v,'#333')}",
             subset=["Status"]),
        use_container_width=True,
        height=380
    )