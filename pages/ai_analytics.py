import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# ── GROQ CLIENT ────────────────────────────────────────────────────────────────

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in .env file.")
        st.stop()
    return Groq(api_key=api_key)

# ── DATA CONTEXT BUILDER ───────────────────────────────────────────────────────

def build_context(risk_df, cyber_df, kpi_df):
    """
    Serialises key statistics from all three datasets into
    a structured text block for the LLM to reason over.
    """

    # Risk register stats
    total_risks     = len(risk_df)
    critical_risks  = len(risk_df[risk_df["Severity"] == "Critical"])
    high_risks      = len(risk_df[risk_df["Severity"] == "High"])
    open_risks      = len(risk_df[risk_df["Status"] == "Open"])
    escalated_risks = len(risk_df[risk_df["Status"] == "Escalated"])
    overdue_risks = len(
    risk_df[
        (risk_df["Status"].isin(["Open", "In Progress", "Escalated"])) &
        (pd.to_datetime(risk_df["Target Closure Date"], errors="coerce") < pd.Timestamp.today())
    ]
)
    # Top 10 oldest open risks
    top_open = (
        risk_df[risk_df["Status"].isin(["Open", "In Progress", "Escalated"])]
        .sort_values("Days Open", ascending=False)
        .head(10)[["Risk ID", "Risk Title", "Category", "Department",
                   "Severity", "Days Open", "Risk Owner",
                   "Mitigation Action"]]
        .to_string(index=False)
    )

    # Category breakdown
    cat_breakdown = (
        risk_df.groupby("Category")
        .size().reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .to_string(index=False)
    )

    # Department breakdown
    dept_breakdown = (
        risk_df[risk_df["Status"].isin(["Open", "In Progress", "Escalated"])]
        .groupby("Department")
        .size().reset_index(name="Open Risks")
        .sort_values("Open Risks", ascending=False)
        .to_string(index=False)
    )

    # Cyber stats
    total_threats    = len(cyber_df)
    critical_threats = len(cyber_df[cyber_df["Severity"] == "Critical"])
    uncontained      = len(
        cyber_df[cyber_df["Containment Status"] == "Uncontained"]
    )
    avg_cvss         = round(cyber_df["CVSS Score"].mean(), 1)
    breach_risk      = len(cyber_df[cyber_df["Data Breach Risk"] == "High"])
    regulatory_notif = len(
        cyber_df[cyber_df["Regulatory Notification Required"] == "Yes"]
    )

    # Top cyber threats
    top_cyber = (
        cyber_df[cyber_df["Severity"].isin(["Critical", "High"])]
        .sort_values("CVSS Score", ascending=False)
        .head(10)[["Threat ID", "Threat Type", "Affected System",
                   "CVSS Score", "Severity", "Containment Status",
                   "Data Breach Risk", "Assigned To"]]
        .to_string(index=False)
    )

    # KPI stats
    total_kpis   = len(kpi_df)
    red_kpis     = len(kpi_df[kpi_df["RAG Status"] == "Red"])
    amber_kpis   = len(kpi_df[kpi_df["RAG Status"] == "Amber"])
    green_kpis   = len(kpi_df[kpi_df["RAG Status"] == "Green"])
    avg_ach      = round(kpi_df["Achievement %"].mean(), 1)

    # Worst performing KPIs
    worst_kpis = (
        kpi_df[kpi_df["RAG Status"] == "Red"]
        .sort_values("Achievement %", ascending=True)
        .head(10)[["Department", "KRA", "KPI", "Target",
                   "Actual", "Unit", "Achievement %",
                   "Quarter", "Comments"]]
        .to_string(index=False)
    )

    context = f"""
=== ENTERPRISE RISK MANAGEMENT DATA CONTEXT ===

--- RISK REGISTER SUMMARY ---
Total Risks: {total_risks}
Critical Severity: {critical_risks}
High Severity: {high_risks}
Currently Open: {open_risks}
Escalated to Management: {escalated_risks}
Overdue Past Target Closure: {overdue_risks}

--- CATEGORY BREAKDOWN ---
{cat_breakdown}

--- OPEN RISKS BY DEPARTMENT ---
{dept_breakdown}

--- TOP 10 OLDEST UNRESOLVED RISKS ---
{top_open}

--- CYBERSECURITY THREAT SUMMARY ---
Total Threats: {total_threats}
Critical Threats: {critical_threats}
Uncontained Threats: {uncontained}
Average CVSS Score: {avg_cvss}
High Data Breach Risk: {breach_risk}
Regulatory Notification Required: {regulatory_notif}

--- TOP 10 CRITICAL/HIGH CYBER THREATS ---
{top_cyber}

--- KPI PERFORMANCE SUMMARY ---
Total KPI Records: {total_kpis}
On Target (Green): {green_kpis}
At Risk (Amber): {amber_kpis}
Off Track (Red): {red_kpis}
Average Achievement: {avg_ach}%

--- WORST PERFORMING KPIs (RED STATUS) ---
{worst_kpis}

=== END OF DATA CONTEXT ===
"""
    return context

# ── SYSTEM PROMPT ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a Senior Enterprise Risk Management Consultant with 20 years of
experience advising Fortune 500 boards and C-suite executives.

You have been provided with complete risk register data, cybersecurity threat
intelligence, and KPI performance data for this organisation.

Your role is to:
1. Answer management queries with specific, data-driven insights
2. Reference exact Risk IDs, Threat IDs, departments, and owners by name
3. Prioritise actionable recommendations over generic advice
4. Highlight interconnections between operational risks, cyber threats, and KPI gaps
5. Flag regulatory and compliance implications where relevant
6. Be concise but thorough — executives need clarity, not lengthy reports

Response format:
- Lead with the direct answer to the question
- Support with specific data points from the context
- End with 2-3 prioritised recommended actions
- Use bullet points for readability
- Keep responses under 400 words unless complexity demands more

Always be specific. Never give generic risk management advice without
referencing the actual data provided.
"""

# ── SUGGESTED QUERIES ──────────────────────────────────────────────────────────

SUGGESTED_QUERIES = [
    "Which are the top 5 risks we have not been able to close in the last 3 months?",
    "What are our most critical cybersecurity threats right now and what action should be taken?",
    "Which department has the highest risk exposure and why?",
    "Which KPIs are most off-track and what is the business impact?",
    "Are there any regulatory or compliance risks that need immediate escalation?",
    "Give me an executive summary of our overall risk posture for the board meeting.",
    "Which risk owners have the highest workload and are any risks at risk of being neglected?",
    "What are the top 3 interconnected risks that could trigger a cascade failure?"
]

# ── MAIN RENDER FUNCTION ───────────────────────────────────────────────────────

def render(risk_df, cyber_df, kpi_df):

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a2744 0%, #2c3e6b 100%);
                padding: 1rem 1.5rem; border-radius: 10px;
                margin-bottom: 1.5rem;">
        <h3 style="color:white; margin:0; font-size:1.1rem;">
            🤖 AI Risk Advisor
        </h3>
        <p style="color:#a8b4d0; margin:0.3rem 0 0 0; font-size:0.85rem;">
            Powered by Groq — Ask any question about your risk data
            and get instant executive-grade insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── INITIALISE SESSION STATE ───────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "data_context" not in st.session_state:
        st.session_state.data_context = build_context(
            risk_df, cyber_df, kpi_df
        )

    # ── SUGGESTED QUERY CHIPS ──────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Suggested Queries</div>',
        unsafe_allow_html=True
    )

    # Display chips in rows of 4
    rows = [SUGGESTED_QUERIES[:4], SUGGESTED_QUERIES[4:]]
    for row in rows:
        cols = st.columns(4)
        for col, query in zip(cols, row):
            if col.button(
                query[:55] + "..." if len(query) > 55 else query,
                key=f"chip_{query[:20]}",
                use_container_width=True
            ):
                st.session_state.pending_query = query

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHAT INPUT ─────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Ask the AI Advisor</div>',
        unsafe_allow_html=True
    )

    # Get input from chat box
    user_input = st.chat_input(
        "Ask anything about your risks, threats, or KPIs..."
    )

    # Override with chip query if one was clicked
    if "pending_query" in st.session_state:
        user_input = st.session_state.pending_query
        del st.session_state.pending_query

    # ── PROCESS QUERY ──────────────────────────────────────────────────────────
    if user_input:
        # Check if this exact query was already just processed
        already_processed = (
            len(st.session_state.chat_history) > 0 and
            st.session_state.chat_history[-1]["role"] == "user" and
            st.session_state.chat_history[-1]["content"] == user_input
        )

        if not already_processed:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            # Build messages for API call
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT + "\n\n" +
                               st.session_state.data_context
                }
            ]

            # Add conversation history — last 20 messages
            for msg in st.session_state.chat_history[-20:]:
                messages.append({
                    "role":    msg["role"],
                    "content": msg["content"]
                })

            # Call Groq API
            with st.spinner("Analysing your risk data..."):
                try:
                    client   = get_groq_client()
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        max_tokens=1000,
                        temperature=0.3
                    )
                    ai_response = response.choices[0].message.content

                except Exception as e:
                    ai_response = (
                        f"Unable to connect to AI service. "
                        f"Please check your API key. Error: {str(e)}"
                    )

            # Add AI response to history
            st.session_state.chat_history.append({
                "role":    "assistant",
                "content": ai_response
            })

            # Force clean rerun to display new message
            st.rerun()

    # ── DISPLAY CHAT HISTORY ───────────────────────────────────────────────────
    if st.session_state.chat_history:
        st.markdown(
            '<div class="section-header">Conversation</div>',
            unsafe_allow_html=True
        )

        # Clear chat button at top
        if st.button("🗑️ Clear Conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Reverse the history — most recent first
        reversed_history = list(reversed(st.session_state.chat_history))

        # Display in pairs — user question first, AI answer below
        i = 0
        while i < len(reversed_history):
            msg = reversed_history[i]

            if msg["role"] == "assistant":
                # Look ahead — is there a user message next?
                # If yes, show user first then AI
                if i + 1 < len(reversed_history) and \
                   reversed_history[i + 1]["role"] == "user":
                    # Show user question first
                    st.markdown(f"""
                    <div class="chat-user">
                        👤 {reversed_history[i + 1]["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Then show AI response
                    with st.container():
                        st.markdown("""
                        <div class="chat-ai">
                            🤖 <strong>AI Risk Advisor</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(msg["content"])
                        st.markdown("---")
                    i += 2  # Skip both
                else:
                    # No user message paired — show AI alone
                    with st.container():
                        st.markdown("""
                        <div class="chat-ai">
                            🤖 <strong>AI Risk Advisor</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(msg["content"])
                        st.markdown("---")
                    i += 1

            elif msg["role"] == "user":
                # Unpaired user message
                st.markdown(f"""
                <div class="chat-user">
                    👤 {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                i += 1

            else:
                i += 1

    else:
        # Empty state message
        st.markdown("""
        <div style="text-align:center; padding:3rem;
                    background:white; border-radius:12px;
                    border: 1px solid #e8ecf0;">
            <div style="font-size:3rem; margin-bottom:1rem;">🤖</div>
            <div style="font-weight:700; color:#1a2744;
                        font-size:1.1rem; margin-bottom:0.5rem;">
                AI Risk Advisor Ready
            </div>
            <div style="color:#6b7280; font-size:0.88rem;">
                Click a suggested query above or type your own question.<br>
                The AI has full access to your risk register,
                cyber threats, and KPI data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SIDEBAR INFO ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 📊 Data Context")
        st.markdown(f"""
        The AI advisor has access to:
        - **{len(risk_df)}** risk records
        - **{len(cyber_df)}** cyber threats
        - **{len(kpi_df)}** KPI records
        """)
        st.markdown("### 🔧 Model")
        st.markdown("Llama 3.3 70B via Groq API")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Ask about specific departments
        - Request board-ready summaries
        - Ask about interconnected risks
        - Request action plans
        """)