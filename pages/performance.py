import streamlit as st
import random


def show():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Performance Tracker</h1>
        <p>Review your progress, score trends, and areas that need more focus.</p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("answer_history", [])
    stats   = st.session_state.get("session_stats", {
        "questions_answered": 0, "sessions_completed": 0, "total_scores": []
    })

    if not history:
        st.info("📭 No performance data yet. Complete a *Mock Interview* session to see your stats here.")
        _show_sample_tips()
        return

    # ── Summary metrics ───────────────────────────────────────────────────
    scores = [h["score"] for h in history]
    tech_scores = [h["score"] for h in history if h.get("type") == "technical"]
    hr_scores   = [h["score"] for h in history if h.get("type") == "hr"]

    avg  = round(sum(scores) / len(scores), 1)
    best = max(scores)
    worst = min(scores)
    tech_avg = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 0
    hr_avg   = round(sum(hr_scores)   / len(hr_scores),   1) if hr_scores   else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, (val, label) in zip([c1, c2, c3, c4, c5], [
        (f"{avg}%",      "Overall Avg"),
        (f"{best}%",     "Best Score"),
        (f"{worst}%",    "Lowest Score"),
        (f"{tech_avg}%", "Technical Avg"),
        (f"{hr_avg}%",   "HR Avg"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score Trend (simple ASCII-style bar chart via st.bar_chart) ───────
    tab1, tab2, tab3 = st.tabs(["📈 Score Trend", "📋 Answer History", "🎯 Focus Areas"])

    with tab1:
        st.markdown("#### Score Trend")

        if len(scores) >= 2:
            import pandas as pd
            df = pd.DataFrame({
                "Question": [f"Q{i+1}" for i in range(len(scores))],
                "Score": scores
            }).set_index("Question")
            st.line_chart(df, height=280, use_container_width=True)

            # Trend analysis
            if len(scores) >= 4:
                first_half = scores[:len(scores)//2]
                second_half = scores[len(scores)//2:]
                avg1 = sum(first_half) / len(first_half)
                avg2 = sum(second_half) / len(second_half)
                diff = avg2 - avg1

                if diff > 5:
                    st.success(f"📈 Your scores are *improving* (+{diff:.1f} pts average in second half). Keep going!")
                elif diff < -5:
                    st.warning(f"📉 Scores dipped in the second half ({diff:.1f} pts). Take a break and review tips.")
                else:
                    st.info("📊 Your performance is *consistent*. Focus on pushing past your current plateau.")
        else:
            st.info("Answer at least 2 questions to see your trend chart.")

        # Breakdown by type
        if tech_scores and hr_scores:
            st.markdown("#### Technical vs HR Comparison")
            import pandas as pd
            comp_df = pd.DataFrame({
                "Technical": [tech_avg],
                "HR / Behavioral": [hr_avg]
            })
            st.bar_chart(comp_df, height=200)

    with tab2:
        st.markdown("#### Answer History")

        for i, item in enumerate(reversed(history)):
            score = item["score"]
            color = "#4ade80" if score >= 70 else "#facc15" if score >= 50 else "#f87171"
            q_type = item.get("type", "technical")
            border = "#6c63ff" if q_type == "technical" else "#ff6584"

            st.markdown(f"""
            <div class="question-card" style="border-left-color:{border}; display:flex; align-items:center; gap:1rem; padding:0.9rem 1.2rem">
                <div style="min-width:50px; text-align:center">
                    <div style="font-family:'Space Mono',monospace; font-size:1.3rem; font-weight:700; color:{color}">{score}</div>
                    <div style="font-size:0.65rem; color:#8888aa">score</div>
                </div>
                <div style="flex:1">
                    <div style="color:#e8e8f0; font-size:0.9rem">{item['question']}</div>
                    <div style="color:#8888aa; font-size:0.75rem; margin-top:0.25rem">
                        {q_type.upper()} • {len(item.get('answer','').split())} words
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History"):
            st.session_state["answer_history"] = []
            st.session_state["session_stats"] = {"questions_answered": 0, "sessions_completed": 0, "total_scores": []}
            st.rerun()

    with tab3:
        st.markdown("#### 🎯 Areas to Focus On")
        _show_focus_areas(scores, tech_avg, hr_avg, history)


def _show_focus_areas(scores, tech_avg, hr_avg, history):
    recommendations = []

    if tech_avg < 60:
        recommendations.append({
            "area": "Technical Depth",
            "insight": f"Your technical average is {tech_avg}%. Focus on adding definitions, examples, and trade-offs to your answers.",
            "action": "Study: system design, data structures, and language-specific internals."
        })

    if hr_avg < 60:
        recommendations.append({
            "area": "Behavioral Answers",
            "insight": f"HR average: {hr_avg}%. Practice structuring stories using the STAR method.",
            "action": "Prepare 5–6 strong STAR stories covering: leadership, conflict, failure, success."
        })

    if len(scores) >= 3:
        last3 = scores[-3:]
        if last3[-1] < last3[0]:
            recommendations.append({
                "area": "Stamina & Consistency",
                "insight": "Your scores decline as the session progresses — you may be rushing later questions.",
                "action": "Practise mock interviews of 45–60 minutes to build mental stamina."
            })

    low_scores = [h for h in history if h["score"] < 50]
    if low_scores:
        recommendations.append({
            "area": "Low-scoring Questions",
            "insight": f"{len(low_scores)} answer(s) scored below 50%. Review these topics specifically.",
            "action": "Re-read fundamentals for topics where you scored lowest."
        })

    if not recommendations:
        recommendations.append({
            "area": "Keep Pushing",
            "insight": "You're performing well! Challenge yourself with harder questions.",
            "action": "Filter questions by 'Advanced' difficulty in the Question Bank."
        })

    for rec in recommendations:
        st.markdown(f"""
        <div class="question-card" style="border-left-color:#facc15">
            <div class="badge" style="background:rgba(250,204,21,0.1);color:#facc15;border-color:rgba(250,204,21,0.3)">
                ⚡ {rec['area']}
            </div>
            <p style="color:#c8c8d8; margin:0.5rem 0 0.25rem; font-size:0.9rem">{rec['insight']}</p>
            <p style="color:#6c63ff; font-size:0.85rem; margin:0"><strong>→</strong> {rec['action']}</p>
        </div>
        """, unsafe_allow_html=True)


def _show_sample_tips():
    st.markdown("### 📚 While You're Here — Study Guide")
    topics = {
        "Data Structures & Algorithms": ["Arrays & Hashing", "Trees & Graphs", "Dynamic Programming", "Sorting"],
        "System Design": ["Load Balancing", "Caching Strategies", "Database Sharding", "Microservices"],
        "Behavioral": ["STAR Method", "Leadership Stories", "Conflict Resolution", "Career Narrative"],
    }
    cols = st.columns(3)
    for col, (category, items) in zip(cols, topics.items()):
        with col:
            st.markdown(f"*{category}*")
            for item in items:
                st.markdown(f"<span class='tag'>{item}</span>", unsafe_allow_html=True)
            st.markdown("")