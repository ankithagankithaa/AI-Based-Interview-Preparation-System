import streamlit as st
from utils.nlp_utils import (
    TECHNICAL_QUESTIONS, HR_QUESTIONS, GENERIC_TECHNICAL_QUESTIONS,
    generate_questions, parse_resume
)


def show():
    st.markdown("""
    <div class="main-header">
        <h1>❓ Question Bank</h1>
        <p>Browse all generated questions filtered by type, topic, and difficulty.</p>
    </div>
    """, unsafe_allow_html=True)

    questions = st.session_state.get("generated_questions")

    if not questions:
        st.info("⚡ No questions generated yet. Go to *Resume Analyzer* first — or explore the full bank below.")
        _show_full_bank()
        return

    tab1, tab2, tab3 = st.tabs(["🔧 Technical Questions", "🤝 HR Questions", "📚 Full Question Bank"])

    with tab1:
        _show_technical(questions)

    with tab2:
        _show_hr(questions)

    with tab3:
        _show_full_bank()


def _show_technical(questions: dict):
    tech = questions.get("technical", [])
    level = questions.get("candidate_level", "mid")

    st.markdown(f"*{len(tech)} questions* tailored for a *{level.title()}* candidate")
    st.markdown("")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        topics = ["All"] + sorted(set(q.get("topic", "General") for q in tech))
        topic_filter = st.selectbox("Filter by Topic", topics)
    with col2:
        diff_filter = st.selectbox("Filter by Difficulty", ["All", "basic", "intermediate", "advanced"])

    filtered = [
        q for q in tech
        if (topic_filter == "All" or q.get("topic") == topic_filter)
        and (diff_filter == "All" or q.get("difficulty") == diff_filter)
    ]

    if not filtered:
        st.warning("No questions match the selected filters.")
        return

    DIFF_COLORS = {"basic": "#4ade80", "intermediate": "#facc15", "advanced": "#f87171"}
    DIFF_LABELS = {"basic": "🟢 Basic", "intermediate": "🟡 Intermediate", "advanced": "🔴 Advanced"}

    for i, q in enumerate(filtered, 1):
        diff = q.get("difficulty", "intermediate")
        color = DIFF_COLORS.get(diff, "#8888aa")
        label = DIFF_LABELS.get(diff, diff.title())

        st.markdown(f"""
        <div class="question-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem">
                <span class="badge">{q.get('topic', 'General')}</span>
                <span style="font-family:'Space Mono',monospace; font-size:0.75rem; color:{color}">{label}</span>
            </div>
            <p style="margin:0; color:#e8e8f0; font-size:0.95rem">
                <strong style="color:#8888aa; font-family:'Space Mono',monospace">Q{i}.</strong> {q['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)


def _show_hr(questions: dict):
    hr = questions.get("hr", [])
    st.markdown(f"*{len(hr)} HR / Behavioural questions* generated")
    st.markdown("")

    cat_filter = st.selectbox(
        "Filter by Category",
        ["All"] + sorted(set(q.get("category", "General") for q in hr))
    )

    filtered = [q for q in hr if cat_filter == "All" or q.get("category") == cat_filter]

    CAT_ICONS = {"Behavioral": "🎭", "Situational": "🤔", "Career": "🚀"}

    for i, q in enumerate(filtered, 1):
        cat = q.get("category", "General")
        icon = CAT_ICONS.get(cat, "💬")
        st.markdown(f"""
        <div class="question-card" style="border-left-color:#ff6584">
            <div class="badge" style="background:rgba(255,101,132,0.1); color:#ff6584; border-color:rgba(255,101,132,0.3)">
                {icon} {cat}
            </div>
            <p style="margin:0.5rem 0 0; color:#e8e8f0; font-size:0.95rem">
                <strong style="color:#8888aa; font-family:'Space Mono',monospace">Q{i}.</strong> {q['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # STAR Method reminder
    with st.expander("💡 STAR Method for Behavioural Answers"):
        st.markdown("""
        Structure every behavioral answer using the *STAR* framework:

        - *S*ituation — Set the scene briefly (1–2 sentences)
        - *T*ask — Describe your responsibility or challenge
        - *Action — Explain what *you specifically did (use "I", not "we")
        - *R*esult — Share the measurable outcome

        > 💡 Aim for a 2–3 minute response. Quantify results wherever possible.
        """)


def _show_full_bank():
    st.markdown("### 📚 Full Question Bank")
    st.markdown("Explore all available questions. Use this to study even before uploading your resume.")

    topic = st.selectbox(
        "Choose a Topic",
        ["python", "javascript", "react", "machine learning", "databases", "docker", "kubernetes", "aws", "git"] +
        ["HR — Behavioral", "HR — Situational", "HR — Career"]
    )

    if topic.startswith("HR"):
        cat = topic.split("— ")[1].lower()
        qs = HR_QUESTIONS.get(cat, [])
        for i, q in enumerate(qs, 1):
            st.markdown(f"""
            <div class="question-card" style="border-left-color:#ff6584">
                <p style="margin:0; color:#e8e8f0">
                    <strong style="color:#8888aa; font-family:'Space Mono',monospace">Q{i}.</strong> {q}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        qs = TECHNICAL_QUESTIONS.get(topic, [])
        DIFF_COLORS = {"basic": "#4ade80", "intermediate": "#facc15", "advanced": "#f87171"}
        for i, (q, diff) in enumerate(qs, 1):
            color = DIFF_COLORS.get(diff, "#aaa")
            st.markdown(f"""
            <div class="question-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem">
                    <span class="badge">{topic.title()}</span>
                    <span style="font-size:0.75rem; color:{color}; font-family:'Space Mono',monospace">{diff.upper()}</span>
                </div>
                <p style="margin:0; color:#e8e8f0">
                    <strong style="color:#8888aa; font-family:'Space Mono',monospace">Q{i}.</strong> {q}
                </p>
            </div>
            """, unsafe_allow_html=True)