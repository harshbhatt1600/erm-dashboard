import streamlit as st
import os
import sys

# Add project root to path so all imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import load_all_data
from pages import overview, risk_cyber, kpi, ai_analytics

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ERM Dashboard | Enterprise Risk Management",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f8f9fa; }

    /* Remove default padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Header bar */
    .erm-header {
        background: linear-gradient(135deg, #1a2744 0%, #2c3e6b 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .erm-header h1 {
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
    }
    .erm-header p {
        color: #a8b4d0;
        font-size: 0.85rem;
        margin: 0.2rem 0 0 0;
    }
    .header-badge {
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* KPI metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e8ecf0;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    div[data-testid="metric-container"] label {
        color: #6b7280 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1a2744 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 10px;
        padding: 0.3rem;
        border: 1px solid #e8ecf0;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.88rem;
        color: #6b7280;
    }
    .stTabs [aria-selected="true"] {
        background: #1a2744 !important;
        color: white !important;
    }

    /* Alert strip */
    .alert-critical {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.88rem;
        color: #991b1b;
        font-weight: 500;
    }
    .alert-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.88rem;
        color: #92400e;
        font-weight: 500;
    }
    .alert-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.88rem;
        color: #065f46;
        font-weight: 500;
    }

    /* Section headers */
    .section-header {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e8ecf0;
        margin-bottom: 1rem;
    }

    /* Dataframe styling */
    .dataframe-container {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e8ecf0;
    }

    /* Chat messages */
    .chat-user {
        background: #1a2744;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-ai {
        background: white;
        border: 1px solid #e8ecf0;
        padding: 0.75rem 1rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        max-width: 85%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────

@st.cache_data
def get_data():
    return load_all_data()

risk_df, cyber_df, kpi_df = get_data()

# ── HEADER ─────────────────────────────────────────────────────────────────────

from datetime import datetime

st.markdown(f"""
<div class="erm-header">
    <div>
        <h1>🛡️ Enterprise Risk Management Dashboard</h1>
        <p>Integrated risk intelligence for executive decision making</p>
    </div>
    <div class="header-badge">
        Last Updated: {datetime.today().strftime("%d %b %Y, %H:%M")}
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Overview",
    "⚠️ Risk Register & Cyber",
    "🎯 KRA / KPI Tracker",
    "🤖 AI Risk Advisor"
])

with tab1:
    overview.render(risk_df, cyber_df)

with tab2:
    risk_cyber.render(risk_df, cyber_df)

with tab3:
    kpi.render(kpi_df)

with tab4:
    ai_analytics.render(risk_df, cyber_df, kpi_df)