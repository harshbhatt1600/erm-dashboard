import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import apply_filters, style_rag, RAG_COLOURS

def render(kpi_df):

    st.markdown(
        '<div class="section-header">🎯 KRA / KPI Performance Tracker</div>',
        unsafe_allow_html=True
    )

    # ── FILTERS ────────────────────────────────────────────────────────────────
    f1, f2, f3 = st.columns(3)

    with f1:
        dept_filter = st.selectbox(
            "Department",
            ["All"] + sorted(kpi_df["Department"].unique().tolist()),
            key="kpi_dept"
        )
    with f2:
        quarter_filter = st.selectbox(
            "Quarter",
            ["All"] + sorted(kpi_df["Quarter"].unique().tolist()),
            key="kpi_qtr"
        )
    with f3:
        rag_filter = st.selectbox(
            "RAG Status",
            ["All", "Red", "Amber", "Green"],
            key="kpi_rag"
        )

    filtered_kpi = apply_filters(kpi_df, {
        "Department": dept_filter,
        "Quarter":    quarter_filter,
        "RAG Status": rag_filter
    })

    # ── KPI SUMMARY STRIP ──────────────────────────────────────────────────────
    total       = len(filtered_kpi)
    green_count = len(filtered_kpi[filtered_kpi["RAG Status"] == "Green"])
    amber_count = len(filtered_kpi[filtered_kpi["RAG Status"] == "Amber"])
    red_count   = len(filtered_kpi[filtered_kpi["RAG Status"] == "Red"])
    avg_ach     = round(filtered_kpi["Achievement %"].mean(), 1) \
                  if total > 0 else 0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total KPIs",        total)
    m2.metric("On Target (Green)", green_count)
    m3.metric("At Risk (Amber)",   amber_count,  delta_color="inverse")
    m4.metric("Off Track (Red)",   red_count,    delta_color="inverse")
    m5.metric("Avg Achievement",   f"{avg_ach}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RAG OVERVIEW CHARTS ────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Performance Overview</div>',
        unsafe_allow_html=True
    )

    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        # RAG donut
        rag_counts = filtered_kpi["RAG Status"].value_counts()
        fig = go.Figure(go.Pie(
            labels=rag_counts.index.tolist(),
            values=rag_counts.values.tolist(),
            hole=0.55,
            marker=dict(colors=[
                RAG_COLOURS.get(r, "#95a5a6")
                for r in rag_counts.index
            ]),
            textinfo="percent+label",
        ))
        fig.update_layout(
            title="Overall RAG Distribution",
            height=320,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        # RAG by department stacked bar
        dept_rag = (
            filtered_kpi.groupby(["Department", "RAG Status"])
            .size().reset_index(name="Count")
        )
        fig2 = px.bar(
            dept_rag,
            x="Count", y="Department",
            color="RAG Status",
            color_discrete_map=RAG_COLOURS,
            orientation="h",
            title="RAG Status by Department",
            text_auto=True
        )
        fig2.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with ch3:
        # Average achievement by department
        dept_ach = (
            filtered_kpi.groupby("Department")["Achievement %"]
            .mean().reset_index()
            .sort_values("Achievement %", ascending=True)
        )
        dept_ach["Achievement %"] = dept_ach["Achievement %"].round(1)
        fig3 = px.bar(
            dept_ach,
            x="Achievement %", y="Department",
            orientation="h",
            title="Avg Achievement % by Department",
            text_auto=True,
            color="Achievement %",
            color_continuous_scale="RdYlGn",
            range_color=[50, 120]
        )
        fig3.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── TREND ANALYSIS ─────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Quarterly Trend Analysis</div>',
        unsafe_allow_html=True
    )

    ch4, ch5 = st.columns(2)

    with ch4:
        # Achievement trend over quarters
        quarter_trend = (
            filtered_kpi.groupby("Quarter")["Achievement %"]
            .mean().reset_index()
        )
        quarter_trend["Achievement %"] = (
            quarter_trend["Achievement %"].round(1)
        )
        fig4 = px.line(
            quarter_trend,
            x="Quarter", y="Achievement %",
            title="Average Achievement % Trend by Quarter",
            markers=True,
            text="Achievement %"
        )
        fig4.update_traces(
            line=dict(color="#1a2744", width=3),
            marker=dict(size=10, color="#1a2744"),
            textposition="top center"
        )
        fig4.add_hline(
            y=90, line_dash="dash",
            line_color="#2ecc71",
            annotation_text="Target: 90%"
        )
        fig4.add_hline(
            y=70, line_dash="dash",
            line_color="#e74c3c",
            annotation_text="Warning: 70%"
        )
        fig4.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig4, use_container_width=True)

    with ch5:
        # Red KPIs trend — how many off-track per quarter
        red_trend = (
            filtered_kpi[filtered_kpi["RAG Status"] == "Red"]
            .groupby("Quarter")
            .size().reset_index(name="Red KPIs")
        )
        fig5 = px.bar(
            red_trend,
            x="Quarter", y="Red KPIs",
            title="Off-Track KPIs (Red) per Quarter",
            text_auto=True,
            color_discrete_sequence=["#e74c3c"]
        )
        fig5.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig5, use_container_width=True)

    # ── DEPARTMENT DEEP DIVE ───────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Department KPI Deep Dive</div>',
        unsafe_allow_html=True
    )

    selected_dept = st.selectbox(
        "Select department for detailed view",
        sorted(kpi_df["Department"].unique().tolist()),
        key="kpi_deep"
    )

    dept_data = filtered_kpi[
        filtered_kpi["Department"] == selected_dept
    ].copy()

    if len(dept_data) > 0:
        # Progress bars for each KPI
        latest_quarter = dept_data["Quarter"].max()
        latest_data = dept_data[dept_data["Quarter"] == latest_quarter]

        st.markdown(
            f"**{selected_dept} — {latest_quarter} Performance**"
        )

        for _, row in latest_data.iterrows():
            col_label, col_bar, col_metric = st.columns([3, 5, 2])

            with col_label:
                rag_emoji = {
                    "Green": "🟢", "Amber": "🟡", "Red": "🔴"
                }.get(row["RAG Status"], "⚪")
                st.markdown(
                    f"{rag_emoji} **{row['KPI']}**",
                    unsafe_allow_html=True
                )

            with col_bar:
                pct = min(row["Achievement %"], 120)
                colour = RAG_COLOURS.get(row["RAG Status"], "#95a5a6")
                bar_html = f"""
                <div style="background:#f0f0f0; border-radius:6px;
                            height:22px; margin-top:6px; overflow:hidden;">
                    <div style="background:{colour}; width:{pct}%;
                                height:100%; border-radius:6px;
                                transition: width 0.5s;">
                    </div>
                </div>"""
                st.markdown(bar_html, unsafe_allow_html=True)

            with col_metric:
                st.markdown(
                    f"<div style='text-align:right; font-weight:700; "
                    f"color:{RAG_COLOURS.get(row['RAG Status'],'#333')};'>"
                    f"{row['Achievement %']}%</div>",
                    unsafe_allow_html=True
                )

            st.caption(
                f"Target: {row['Target']} {row['Unit']} | "
                f"Actual: {row['Actual']} {row['Unit']} | "
                f"{row['Comments']}"
            )

        st.markdown("<br>", unsafe_allow_html=True)

    # ── FULL KPI TABLE ─────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Full KPI Register</div>',
        unsafe_allow_html=True
    )

    display_cols = [
        "Department", "KRA", "KPI", "Quarter",
        "Target", "Actual", "Unit",
        "Achievement %", "RAG Status",
        "KPI Owner", "Comments"
    ]

    st.dataframe(
        filtered_kpi[display_cols].style
        .map(style_rag, subset=["RAG Status"]),
        use_container_width=True,
        height=420
    )

    st.caption(
        f"Showing {len(filtered_kpi)} of {len(kpi_df)} KPI records"
    )