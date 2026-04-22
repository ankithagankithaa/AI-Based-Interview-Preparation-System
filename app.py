import streamlit as st

st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished dark UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --text: #e8e8f0;
    --muted: #8888aa;
    --border: #2a2a3a;
    --success: #4ade80;
    --warning: #facc15;
    --danger: #f87171;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background-color: var(--bg); }

h1, h2, h3 { font-family: 'Space Mono', monospace; }

.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(108,99,255,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.main-header h1 {
    font-size: 2rem;
    background: linear-gradient(135deg, #6c63ff, #ff6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
}

.main-header p { color: var(--muted); margin: 0; font-size: 1rem; }

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    transition: border-color 0.2s;
}

.metric-card:hover { border-color: var(--accent); }

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6c63ff, #ff6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label { color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }

.question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.question-card .badge {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    color: var(--accent);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.75rem;
}

.feedback-card {
    border-radius: 12px;
    padding: 1.25rem;
    margin-top: 1rem;
}

.feedback-card.good { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); }
.feedback-card.avg  { background: rgba(250,204,21,0.08); border: 1px solid rgba(250,204,21,0.2); }
.feedback-card.poor { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.2); }

.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover { opacity: 0.85 !important; }

.stTextArea textarea, .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

.stProgress .st-bo { background: linear-gradient(90deg, #6c63ff, #ff6584); }

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

.sidebar-logo {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6c63ff, #ff6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

.stRadio label { color: var(--text) !important; }
.stCheckbox label { color: var(--text) !important; }

div[data-testid="stMarkdownContainer"] p { color: var(--text); }

.score-ring {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 4px solid var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    margin: 0 auto;
}

.tag {
    display: inline-block;
    background: rgba(108,99,255,0.1);
    border: 1px solid rgba(108,99,255,0.25);
    color: #a78bfa;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    margin: 0.15rem;
}

.stTab [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}

hr { border-color: var(--border) !important; }

.step-indicator {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-bottom: 1.5rem;
}

.step {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
}

.step.active { color: var(--accent); }
.step.done { color: var(--success); }

.step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--muted);
}
.step.active .step-dot { background: var(--accent); }
.step.done .step-dot { background: var(--success); }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎯 AI Interview Prep</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📄 Resume Analyzer", "❓ Question Bank", "🎙️ Mock Interview", "📊 Performance"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "questions_answered": 0,
            "sessions_completed": 0,
            "avg_score": 0,
            "total_scores": []
        }
    
    stats = st.session_state.session_stats
    st.markdown("*Session Stats*")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Answered", stats["questions_answered"])
    with col2:
        avg = round(sum(stats["total_scores"]) / len(stats["total_scores"]), 1) if stats["total_scores"] else 0
        st.metric("Avg Score", f"{avg}%")
    
    st.markdown("---")
    st.markdown('<p style="color:#8888aa; font-size:0.75rem;">Powered by NLP + ML</p>', unsafe_allow_html=True)

# Route pages
page_name = page.split(" ", 1)[1]

if page_name == "Dashboard":
    from pages import dashboard
    dashboard.show()
elif page_name == "Resume Analyzer":
    from pages import resume_analyzer
    resume_analyzer.show()
elif page_name == "Question Bank":
    from pages import question_bank
    question_bank.show()
elif page_name == "Mock Interview":
    from pages import mock_interview
    mock_interview.show()
elif page_name == "Performance":
    from pages import performance
    performance.show()