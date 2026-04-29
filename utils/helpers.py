import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── COLOUR MAPS ────────────────────────────────────────────────────────────────

SEVERITY_COLOURS = {
    "Low":      "#2ecc71",
    "Medium":   "#f39c12",
    "High":     "#e67e22",
    "Critical": "#e74c3c"
}

STATUS_COLOURS = {
    "Open":        "#3498db",
    "In Progress": "#f39c12",
    "Escalated":   "#e74c3c",
    "Closed":      "#2ecc71",
    "Mitigated":   "#9b59b6"
}

RAG_COLOURS = {
    "Green": "#2ecc71",
    "Amber": "#f39c12",
    "Red":   "#e74c3c"
}

CATEGORY_COLOURS = {
    "Operational":   "#3498db",
    "Financial":     "#e74c3c",
    "Strategic":     "#9b59b6",
    "Compliance":    "#f39c12",
    "Reputational":  "#1abc9c",
    "Cybersecurity": "#e67e22"
}

# ── KPI CARD HELPER ────────────────────────────────────────────────────────────

def render_kpi_cards(cols, metrics):
    """
    Renders a row of KPI metric cards.
    metrics = list of (label, value, delta, delta_color) tuples
    delta_color = 'normal' | 'inverse' | 'off'
    """
    for col, (label, value, delta, delta_color) in zip(cols, metrics):
        col.metric(
            label=label,
            value=value,
            delta=delta,
            delta_color=delta_color
        )

# ── SUMMARY STATS ──────────────────────────────────────────────────────────────

def get_risk_summary(df):
    """Returns key summary statistics from the risk register."""
    total           = len(df)
    critical        = len(df[df["Severity"] == "Critical"])
    high            = len(df[df["Severity"] == "High"])
    open_risks      = len(df[df["Status"] == "Open"])
    escalated       = len(df[df["Status"] == "Escalated"])
    closed          = len(df[df["Status"].isin(["Closed", "Mitigated"])])
    overdue         = len(
        df[
            (df["Status"].isin(["Open", "In Progress", "Escalated"])) &
            (pd.to_datetime(df["Target Closure Date"]) < pd.Timestamp.today())
        ]
    )
    closure_rate    = round((closed / total) * 100, 1) if total > 0 else 0
    avg_days_open   = round(
        df[df["Status"].isin(["Open", "In Progress", "Escalated"])]["Days Open"].mean(), 1
    )

    return {
        "total":        total,
        "critical":     critical,
        "high":         high,
        "open":         open_risks,
        "escalated":    escalated,
        "closed":       closed,
        "overdue":      overdue,
        "closure_rate": closure_rate,
        "avg_days_open": avg_days_open
    }

def get_cyber_summary(df):
    """Returns key summary statistics from the cyber threats dataset."""
    total        = len(df)
    critical     = len(df[df["Severity"] == "Critical"])
    uncontained  = len(df[df["Containment Status"] == "Uncontained"])
    breach_risk  = len(df[df["Data Breach Risk"] == "High"])
    notification = len(df[df["Regulatory Notification Required"] == "Yes"])
    avg_cvss     = round(df["CVSS Score"].mean(), 1)

    return {
        "total":        total,
        "critical":     critical,
        "uncontained":  uncontained,
        "breach_risk":  breach_risk,
        "notification": notification,
        "avg_cvss":     avg_cvss
    }

# ── CHART HELPERS ──────────────────────────────────────────────────────────────

def donut_chart(labels, values, colours, title):
    """Reusable donut chart."""
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colours),
        textinfo="percent+label",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        showlegend=True,
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def bar_chart(df, x_col, y_col, colour_col=None,
              colour_map=None, title="", orientation="v"):
    """Reusable bar chart."""
    if colour_col and colour_map:
        colour_sequence = [
            colour_map.get(v, "#95a5a6")
            for v in df[colour_col].unique()
        ]
    else:
        colour_sequence = px.colors.qualitative.Set2

    fig = px.bar(
        df, x=x_col, y=y_col,
        color=colour_col,
        color_discrete_map=colour_map,
        orientation=orientation,
        title=title,
        text_auto=True
    )
    fig.update_layout(
        height=380,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True
    )
    fig.update_traces(textposition="outside")
    return fig

def heatmap_chart(df, x_col, y_col, value_col, title=""):
    """Reusable heatmap."""
    pivot = df.pivot_table(
        index=y_col, columns=x_col,
        values=value_col, aggfunc="count", fill_value=0
    )
    fig = px.imshow(
        pivot,
        color_continuous_scale="RdYlGn_r",
        title=title,
        text_auto=True,
        aspect="auto"
    )
    fig.update_layout(
        height=380,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def scatter_chart(df, x_col, y_col, colour_col,
                  size_col=None, title="", colour_map=None):
    """Reusable scatter / bubble chart."""
    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=colour_col,
        size=size_col,
        color_discrete_map=colour_map,
        title=title,
        hover_data=df.columns.tolist()
    )
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# ── TABLE STYLING ──────────────────────────────────────────────────────────────

def style_severity(val):
    """Applies background colour to severity cells in dataframes."""
    colours = {
        "Low":      "background-color: #d5f5e3; color: #1e8449",
        "Medium":   "background-color: #fef9e7; color: #b7950b",
        "High":     "background-color: #fdebd0; color: #a04000",
        "Critical": "background-color: #fadbd8; color: #922b21"
    }
    return colours.get(val, "")

def style_status(val):
    """Applies background colour to status cells in dataframes."""
    colours = {
        "Open":        "background-color: #d6eaf8; color: #1a5276",
        "In Progress": "background-color: #fef9e7; color: #b7950b",
        "Escalated":   "background-color: #fadbd8; color: #922b21",
        "Closed":      "background-color: #d5f5e3; color: #1e8449",
        "Mitigated":   "background-color: #e8daef; color: #6c3483"
    }
    return colours.get(val, "")

def style_rag(val):
    """Applies background colour to RAG status cells."""
    colours = {
        "Green": "background-color: #d5f5e3; color: #1e8449",
        "Amber": "background-color: #fef9e7; color: #b7950b",
        "Red":   "background-color: #fadbd8; color: #922b21"
    }
    return colours.get(val, "")

# ── FILTER HELPER ──────────────────────────────────────────────────────────────

def apply_filters(df, filters: dict):
    """
    Applies multiple filters to a dataframe.
    filters = {column_name: selected_value_or_list}
    Pass "All" to skip a filter.
    """
    filtered = df.copy()
    for col, val in filters.items():
        if val and val != "All" and val != []:
            if isinstance(val, list):
                filtered = filtered[filtered[col].isin(val)]
            else:
                filtered = filtered[filtered[col] == val]
    return filtered

# ── DATA LOADER ────────────────────────────────────────────────────────────────

def load_all_data():
    """
    Loads all three datasets from the data/ folder.
    Returns (risk_df, cyber_df, kpi_df)
    """
    import os
    base = os.path.join(os.path.dirname(__file__), "..", "data")

    risk_df  = pd.read_csv(os.path.join(base, "risk_register.csv"))
    cyber_df = pd.read_csv(os.path.join(base, "cyber_threats.csv"))
    kpi_df   = pd.read_csv(os.path.join(base, "kpi_data.csv"))

    # Parse date columns
    for col in ["Date Identified", "Target Closure Date",
                "Actual Closure Date", "Last Updated"]:
        if col in risk_df.columns:
            risk_df[col] = pd.to_datetime(risk_df[col], errors="coerce")

    if "Date Detected" in cyber_df.columns:
        cyber_df["Date Detected"] = pd.to_datetime(
            cyber_df["Date Detected"], errors="coerce"
        )

    return risk_df, cyber_df, kpi_df