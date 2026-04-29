import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import (
    apply_filters, bar_chart, donut_chart, scatter_chart,
    style_severity, style_status,
    SEVERITY_COLOURS, STATUS_COLOURS, CATEGORY_COLOURS
)

def render(risk_df, cyber_df):

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — RISK REGISTER
    # ══════════════════════════════════════════════════════════════════════════

    st.markdown(
        '<div class="section-header">⚠️ Risk Register</div>',
        unsafe_allow_html=True
    )

    # ── FILTERS ────────────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        cat_filter = st.selectbox(
            "Category",
            ["All"] + sorted(risk_df["Category"].unique().tolist()),
            key="rr_cat"
        )
    with f2:
        sev_filter = st.selectbox(
            "Severity",
            ["All"] + ["Critical", "High", "Medium", "Low"],
            key="rr_sev"
        )
    with f3:
        status_filter = st.selectbox(
            "Status",
            ["All"] + sorted(risk_df["Status"].unique().tolist()),
            key="rr_status"
        )
    with f4:
        dept_filter = st.selectbox(
            "Department",
            ["All"] + sorted(risk_df["Department"].unique().tolist()),
            key="rr_dept"
        )

    # Apply filters
    filtered_risk = apply_filters(risk_df, {
        "Category":   cat_filter,
        "Severity":   sev_filter,
        "Status":     status_filter,
        "Department": dept_filter
    })

    # ── FILTERED SUMMARY STRIP ─────────────────────────────────────────────────
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Filtered Risks",  len(filtered_risk))
    m2.metric("Critical",
              len(filtered_risk[filtered_risk["Severity"] == "Critical"]))
    m3.metric("Open",
              len(filtered_risk[filtered_risk["Status"] == "Open"]))
    m4.metric("Escalated",
              len(filtered_risk[filtered_risk["Status"] == "Escalated"]))
    m5.metric("Avg Days Open",
              round(filtered_risk["Days Open"].mean(), 0)
              if len(filtered_risk) > 0 else 0)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ─────────────────────────────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        # Severity breakdown of filtered data
        sev_counts = filtered_risk["Severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        fig = px.bar(
            sev_counts, x="Severity", y="Count",
            color="Severity",
            color_discrete_map=SEVERITY_COLOURS,
            title="Severity Breakdown",
            text_auto=True
        )
        fig.update_layout(
            height=320,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        # Status breakdown of filtered data
        stat_counts = filtered_risk["Status"].value_counts().reset_index()
        stat_counts.columns = ["Status", "Count"]
        fig2 = px.bar(
            stat_counts, x="Status", y="Count",
            color="Status",
            color_discrete_map=STATUS_COLOURS,
            title="Status Breakdown",
            text_auto=True
        )
        fig2.update_layout(
            height=320,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── RISK SCATTER — Age vs Score ────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Risk Age vs Risk Score Analysis</div>',
        unsafe_allow_html=True
    )

    fig3 = scatter_chart(
        filtered_risk,
        x_col="Days Open",
        y_col="Risk Score",
        colour_col="Severity",
        size_col="Risk Score",
        colour_map=SEVERITY_COLOURS,
        title="Risk Age (Days Open) vs Risk Score — sized by severity"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── FULL RISK TABLE ────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Full Risk Register</div>',
        unsafe_allow_html=True
    )

    display_cols = [
        "Risk ID", "Risk Title", "Category", "Department",
        "Risk Owner", "Likelihood", "Severity", "Risk Score",
        "Status", "Days Open", "Target Closure Date",
        "Mitigation Action", "Escalated to Management"
    ]

    st.dataframe(
        filtered_risk[display_cols].style
        .map(style_severity, subset=["Severity"])
        .map(style_status,   subset=["Status"]),
        use_container_width=True,
        height=420
    )

    st.caption(
        f"Showing {len(filtered_risk)} of {len(risk_df)} risks"
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — CYBERSECURITY DEEP DIVE
    # ══════════════════════════════════════════════════════════════════════════

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a2744 0%, #2c3e6b 100%);
                padding: 0.8rem 1.2rem; border-radius: 10px; margin-bottom: 1rem;">
        <span style="color:white; font-size:1rem; font-weight:700;">
            🔐 Cybersecurity Risk Deep Dive
        </span>
        <span style="color:#a8b4d0; font-size:0.82rem; margin-left:1rem;">
            Dedicated threat intelligence view for CISO & IT leadership
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── CYBER FILTERS ──────────────────────────────────────────────────────────
    cf1, cf2, cf3, cf4 = st.columns(4)

    with cf1:
        threat_filter = st.selectbox(
            "Threat Type",
            ["All"] + sorted(cyber_df["Threat Type"].unique().tolist()),
            key="cy_threat"
        )
    with cf2:
        cyber_sev = st.selectbox(
            "Severity",
            ["All"] + ["Critical", "High", "Medium", "Low"],
            key="cy_sev"
        )
    with cf3:
        contain_filter = st.selectbox(
            "Containment Status",
            ["All"] + sorted(
                cyber_df["Containment Status"].unique().tolist()
            ),
            key="cy_contain"
        )
    with cf4:
        breach_filter = st.selectbox(
            "Data Breach Risk",
            ["All"] + ["High", "Medium", "Low"],
            key="cy_breach"
        )

    filtered_cyber = apply_filters(cyber_df, {
        "Threat Type":        threat_filter,
        "Severity":           cyber_sev,
        "Containment Status": contain_filter,
        "Data Breach Risk":   breach_filter
    })

    # ── CYBER KPI STRIP ────────────────────────────────────────────────────────
    cm1, cm2, cm3, cm4, cm5 = st.columns(5)
    cm1.metric("Threats Shown",     len(filtered_cyber))
    cm2.metric("Avg CVSS Score",
               round(filtered_cyber["CVSS Score"].mean(), 1)
               if len(filtered_cyber) > 0 else 0)
    cm3.metric("Uncontained",
               len(filtered_cyber[
                   filtered_cyber["Containment Status"] == "Uncontained"
               ]))
    cm4.metric("Patch Available",
               len(filtered_cyber[filtered_cyber["Patch Available"] == "Yes"]))
    cm5.metric("Regulatory Alerts",
               len(filtered_cyber[
                   filtered_cyber["Regulatory Notification Required"] == "Yes"
               ]))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CYBER CHARTS ───────────────────────────────────────────────────────────
    cc1, cc2, cc3 = st.columns(3)

    with cc1:
        # Threat type distribution
        tt = filtered_cyber["Threat Type"].value_counts().reset_index()
        tt.columns = ["Threat Type", "Count"]
        fig4 = px.bar(
            tt, x="Count", y="Threat Type",
            orientation="h",
            title="Threats by Type",
            text_auto=True,
            color_discrete_sequence=["#e67e22"]
        )
        fig4.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)

    with cc2:
        # Affected systems
        sys_counts = (
            filtered_cyber["Affected System"]
            .value_counts().reset_index()
        )
        sys_counts.columns = ["System", "Count"]
        fig5 = px.bar(
            sys_counts, x="Count", y="System",
            orientation="h",
            title="Most Targeted Systems",
            text_auto=True,
            color_discrete_sequence=["#1a2744"]
        )
        fig5.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True)

    with cc3:
        # Containment status donut
        cont = filtered_cyber["Containment Status"].value_counts()
        fig6 = donut_chart(
            labels=cont.index.tolist(),
            values=cont.values.tolist(),
            colours=["#2ecc71", "#f39c12", "#e74c3c"],
            title="Containment Status"
        )
        st.plotly_chart(fig6, use_container_width=True)

    # ── CVSS SCATTER ───────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">CVSS Score Analysis</div>',
        unsafe_allow_html=True
    )

    cc4, cc5 = st.columns(2)

    with cc4:
        fig7 = px.box(
            filtered_cyber,
            x="Threat Type",
            y="CVSS Score",
            color="Severity",
            color_discrete_map=SEVERITY_COLOURS,
            title="CVSS Score Distribution by Threat Type"
        )
        fig7.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig7, use_container_width=True)

    with cc5:
        # Threat actor breakdown
        actor = filtered_cyber["Threat Actor"].value_counts().reset_index()
        actor.columns = ["Threat Actor", "Count"]
        fig8 = px.pie(
            actor,
            names="Threat Actor",
            values="Count",
            title="Threats by Actor Type",
            hole=0.4
        )
        fig8.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig8, use_container_width=True)

    # ── CYBER THREAT TABLE ─────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Cybersecurity Threat Register</div>',
        unsafe_allow_html=True
    )

    cyber_display = [
        "Threat ID", "Threat Type", "Affected System", "Threat Actor",
        "CVSS Score", "Severity", "Business Impact", "Detection Method",
        "Status", "Containment Status", "Patch Available",
        "Data Breach Risk", "Regulatory Notification Required",
        "Days Since Detection", "Assigned To"
    ]

    st.dataframe(
        filtered_cyber[cyber_display].style
        .map(style_severity, subset=["Severity"])
        .map(style_severity, subset=["Business Impact"])
        .map(style_status,   subset=["Status"]),
        use_container_width=True,
        height=420
    )

    st.caption(
        f"Showing {len(filtered_cyber)} of {len(cyber_df)} threats"
    )