import streamlit as st
import random


def show():
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Interview Prep</h1>
        <p>Personalized, AI-powered interview preparation — analyse your resume, practice questions, and track your growth.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Stats ───────────────────────────────────────────────────────
    stats = st.session_state.get("session_stats", {
        "questions_answered": 0, "sessions_completed": 0, "total_scores": []
    })
    avg = round(sum(stats["total_scores"]) / len(stats["total_scores"]), 1) if stats["total_scores"] else 0

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("Questions Answered", stats["questions_answered"], "📝"),
        ("Sessions Completed", stats["sessions_completed"], "🎙️"),
        ("Average Score", f"{avg}%", "📊"),
        ("Skills Detected", len(st.session_state.get("detected_skills", [])), "🔍"),
    ]
    for col, (label, val, icon) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.5rem">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Getting Started / Resume Status ───────────────────────────────────
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.markdown("### Getting Started")

        resume_parsed = st.session_state.get("resume_parsed")

        if not resume_parsed:
            st.info("👋 Start by uploading your resume in the *Resume Analyzer* tab to get personalised questions.")
            steps = [
                ("📄", "Upload Resume", "Paste your resume text for AI analysis"),
                ("❓", "Get Questions", "Receive tailored technical & HR questions"),
                ("🎙️", "Mock Interview", "Practice answering with real-time feedback"),
                ("📊", "Track Progress", "Review your scores and improvement areas"),
            ]
            for icon, title, desc in steps:
                st.markdown(f"""
                <div class="question-card" style="padding:1rem; margin-bottom:0.6rem;">
                    <span style="font-size:1.3rem">{icon}</span>
                    <strong style="color:#e8e8f0;"> {title}</strong>
                    <div style="color:#8888aa; font-size:0.85rem; margin-top:0.2rem">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            level = resume_parsed.get("candidate_level", "unknown").title()
            skills = resume_parsed.get("detected_skills", [])
            st.success(f"✅ Resume analysed — *{level}* level candidate detected.")
            st.markdown(f"*Detected Skills:* {' '.join([f'<span class=\"tag\">{s}</span>' for s in skills[:12]])}", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎙️ Start Mock Interview", use_container_width=True):
                st.info("Navigate to *Mock Interview* in the sidebar.")

    with col_right:
        st.markdown("### 💡 Interview Tips")
        tips = [
            ("STAR Method", "Structure behavioral answers: *Situation, Task, Action, Result*"),
            ("Quantify Impact", "Use numbers — 'Improved performance by *40%*' beats vague claims"),
            ("Think Aloud", "Walk through your reasoning — interviewers value process over perfect answers"),
            ("Ask Questions", "Prepare 2–3 thoughtful questions for your interviewer"),
            ("Pause, Don't Rush", "A 2-second pause beats an 'um' — collect your thoughts"),
        ]
        tip = random.choice(tips)
        st.markdown(f"""
        <div class="question-card">
            <div class="badge">💡 TIP OF THE SESSION</div>
            <strong style="color:#6c63ff">{tip[0]}</strong>
            <p style="color:#c8c8d8; margin-top:0.5rem; font-size:0.9rem">{tip[1]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📈 Difficulty Breakdown")
        levels = {"🟢 Basic": 30, "🟡 Intermediate": 50, "🔴 Advanced": 20}
        for label, pct in levels.items():
            st.markdown(f"<small>{label}</small>", unsafe_allow_html=True)
            st.progress(pct / 100)

    # ── Recent Activity ───────────────────────────────────────────────────
    history = st.session_state.get("answer_history", [])
    if history:
        st.markdown("---")
        st.markdown("### 📋 Recent Activity")
        for item in reversed(history[-5:]):
            color = "#4ade80" if item["score"] >= 70 else "#facc15" if item["score"] >= 50 else "#f87171"
            st.markdown(f"""
            <div class="question-card" style="display:flex; justify-content:space-between; align-items:center; padding:0.8rem 1rem">
                <div style="font-size:0.85rem; color:#c8c8d8; flex:1">{item['question'][:70]}...</div>
                <div style="font-family:'Space Mono',monospace; font-size:1rem; color:{color}; margin-left:1rem; font-weight:700">{item['score']}%</div>
            </div>
            """, unsafe_allow_html=True)