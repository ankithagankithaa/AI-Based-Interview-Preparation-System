import streamlit as st
import random
from utils.nlp_utils import evaluate_answer, TECHNICAL_QUESTIONS, HR_QUESTIONS, GENERIC_TECHNICAL_QUESTIONS
from utils.speech_utils import analyze_speech_text, get_demo_transcription
from models.scoring_model import AnswerScoringModel, extract_features


MODEL = AnswerScoringModel()


def _get_question_pool():
    """Build a flat question pool from session or defaults."""
    questions = st.session_state.get("generated_questions")
    pool = []

    if questions:
        for q in questions.get("technical", []):
            pool.append({"question": q["question"], "type": "technical",
                         "topic": q.get("topic", "General"), "difficulty": q.get("difficulty", "intermediate")})
        for q in questions.get("hr", []):
            pool.append({"question": q["question"], "type": "hr",
                         "topic": q.get("category", "Behavioral"), "difficulty": "behavioral"})
    else:
        # Default pool
        for q, diff in random.sample(GENERIC_TECHNICAL_QUESTIONS, min(5, len(GENERIC_TECHNICAL_QUESTIONS))):
            pool.append({"question": q, "type": "technical", "topic": "General", "difficulty": diff})
        for cat, qs in HR_QUESTIONS.items():
            for q in random.sample(qs, min(2, len(qs))):
                pool.append({"question": q, "type": "hr", "topic": cat.title(), "difficulty": "behavioral"})

    return pool


def show():
    st.markdown("""
    <div class="main-header">
        <h1>🎙️ Mock Interview</h1>
        <p>Practice answering questions and get instant AI feedback on content, structure, and delivery.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Session init ──────────────────────────────────────────────────────
    if "interview_pool" not in st.session_state:
        pool = _get_question_pool()
        random.shuffle(pool)
        st.session_state["interview_pool"] = pool
        st.session_state["interview_idx"] = 0
        st.session_state["answer_history"] = st.session_state.get("answer_history", [])
        st.session_state["current_feedback"] = None

    pool = st.session_state["interview_pool"]
    idx  = st.session_state.get("interview_idx", 0)

    # ── Top bar ───────────────────────────────────────────────────────────
    col_prog, col_ctrl = st.columns([3, 1])
    with col_prog:
        progress = min(idx / max(len(pool), 1), 1.0)
        st.progress(progress)
        st.caption(f"Question {min(idx + 1, len(pool))} of {len(pool)}")
    with col_ctrl:
        if st.button("🔀 New Session", use_container_width=True):
            for k in ["interview_pool", "interview_idx", "current_feedback"]:
                st.session_state.pop(k, None)
            st.rerun()

    if idx >= len(pool):
        _show_session_complete()
        return

    current_q = pool[idx]

    # ── Question card ─────────────────────────────────────────────────────
    q_type = current_q["type"]
    topic  = current_q["topic"]
    diff   = current_q["difficulty"]
    DIFF_COLORS = {"basic": "#4ade80", "intermediate": "#facc15",
                   "advanced": "#f87171", "behavioral": "#a78bfa"}
    border = "#6c63ff" if q_type == "technical" else "#ff6584"
    diff_color = DIFF_COLORS.get(diff, "#aaa")

    st.markdown(f"""
    <div class="question-card" style="border-left-color:{border}; padding:1.5rem">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.75rem">
            <span class="badge">{topic}</span>
            <span style="font-size:0.75rem; font-family:'Space Mono',monospace; color:{diff_color}">{diff.upper()}</span>
        </div>
        <p style="font-size:1.1rem; color:#e8e8f0; margin:0; line-height:1.6">{current_q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input mode toggle ─────────────────────────────────────────────────
    input_mode = st.radio(
        "Input Mode",
        ["✍️ Type Answer", "🎙️ Use Speech (Demo)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    user_answer = ""

    if "Type" in input_mode:
        user_answer = st.text_area(
            "Your Answer",
            height=180,
            placeholder="Type your answer here. Aim for 60–150 words with a clear structure...",
            key=f"answer_input_{idx}",
            label_visibility="collapsed"
        )
    else:
        st.info("🎙️ Speech-to-Text Demo — click below to simulate a transcription.")
        if st.button("🎙️ Simulate Transcription"):
            demo = get_demo_transcription(q_type)
            st.session_state[f"speech_text_{idx}"] = demo

        speech_text = st.session_state.get(f"speech_text_{idx}", "")
        if speech_text:
            user_answer = st.text_area(
                "Transcribed Text (editable)",
                value=speech_text,
                height=150,
                key=f"speech_edit_{idx}",
                label_visibility="collapsed"
            )

    # ── Action buttons ────────────────────────────────────────────────────
    col_submit, col_skip, col_hint = st.columns([2, 1, 1])

    with col_submit:
        submit = st.button("📤 Submit Answer", use_container_width=True)
    with col_skip:
        if st.button("⏭️ Skip", use_container_width=True):
            st.session_state["interview_idx"] += 1
            st.session_state["current_feedback"] = None
            for k in [f"answer_input_{idx}", f"speech_text_{idx}", f"speech_edit_{idx}"]:
                st.session_state.pop(k, None)
            st.rerun()
    with col_hint:
        show_hint = st.button("💡 Hint", use_container_width=True)

    if show_hint:
        _show_hint(current_q)

    # ── Evaluate ─────────────────────────────────────────────────────────
    if submit:
        if not user_answer or not user_answer.strip():
            st.warning("Please write or transcribe an answer before submitting.")
        else:
            with st.spinner("🧠 Evaluating your answer..."):
                # NLP evaluation
                nlp_result = evaluate_answer(current_q["question"], user_answer)

                # ML scoring
                features = extract_features(user_answer, current_q["question"])
                ml_score = MODEL.predict_score(features)
                grade    = MODEL.predict_grade(ml_score)
                tips     = MODEL.get_improvement_tips(features, ml_score)

                # Speech analysis (always run on typed text too for demo)
                speech = analyze_speech_text(user_answer)

                # Blend scores
                final_score = round(nlp_result["overall_score"] * 0.6 + ml_score * 0.4)

                feedback = {
                    "score": final_score,
                    "grade": grade,
                    "nlp": nlp_result,
                    "ml_score": round(ml_score),
                    "ml_tips": tips,
                    "speech": speech,
                    "features": features,
                }
                st.session_state["current_feedback"] = feedback

                # Persist to history
                history = st.session_state.get("answer_history", [])
                history.append({
                    "question": current_q["question"],
                    "answer": user_answer[:200],
                    "score": final_score,
                    "type": q_type,
                })
                st.session_state["answer_history"] = history

                # Update global stats
                s = st.session_state.get("session_stats", {
                    "questions_answered": 0, "sessions_completed": 0, "total_scores": []
                })
                s["questions_answered"] += 1
                s["total_scores"].append(final_score)
                st.session_state["session_stats"] = s

    # ── Show feedback ─────────────────────────────────────────────────────
    fb = st.session_state.get("current_feedback")
    if fb:
        _render_feedback(fb)

        if st.button("➡️ Next Question", use_container_width=True):
            st.session_state["interview_idx"] += 1
            st.session_state["current_feedback"] = None
            for k in [f"answer_input_{idx}", f"speech_text_{idx}", f"speech_edit_{idx}"]:
                st.session_state.pop(k, None)
            st.rerun()


def _render_feedback(fb: dict):
    score = fb["score"]
    grade = fb["grade"]
    color_class = "good" if score >= 70 else "avg" if score >= 50 else "poor"
    score_color = "#4ade80" if score >= 70 else "#facc15" if score >= 50 else "#f87171"

    st.markdown("---")
    st.markdown("### 📊 Feedback")

    # Score + grade
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem">
            <div style="font-family:'Space Mono',monospace; font-size:3rem; font-weight:700; color:{score_color}">{score}</div>
            <div style="color:#8888aa; font-size:0.85rem">out of 100</div>
            <div style="color:{score_color}; font-weight:600; margin-top:0.25rem">{grade}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("*Score Breakdown*")
        breakdown = fb["nlp"].get("breakdown", {})
        ICONS = {"Completeness": "📏", "Keyword Coverage": "🔑", "Structure": "🏗️", "Confidence": "💪"}
        for dim, val in breakdown.items():
            icon = ICONS.get(dim, "•")
            st.markdown(f"<small>{icon} {dim}</small>", unsafe_allow_html=True)
            st.progress(val / 100)

    # NLP feedback
    nlp = fb["nlp"]
    if nlp.get("feedback"):
        st.markdown(f"""
        <div class="feedback-card {color_class}">
            <strong>AI Feedback</strong>
            <p style="margin:0.5rem 0 0; color:#c8c8d8">{nlp['feedback']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Keywords
    col_kw1, col_kw2 = st.columns(2)
    with col_kw1:
        matched = nlp.get("matched_keywords", [])
        if matched:
            st.markdown("*✅ Keywords Covered*")
            st.markdown(" ".join([f'<span class="tag" style="background:rgba(74,222,128,0.1);border-color:rgba(74,222,128,0.3);color:#4ade80">{k}</span>' for k in matched]), unsafe_allow_html=True)
    with col_kw2:
        missing = nlp.get("missing_keywords", [])
        if missing:
            st.markdown("*❌ Consider Adding*")
            st.markdown(" ".join([f'<span class="tag" style="background:rgba(248,113,113,0.1);border-color:rgba(248,113,113,0.3);color:#f87171">{k}</span>' for k in missing]), unsafe_allow_html=True)

    # ML improvement tips
    if fb.get("ml_tips"):
        with st.expander("🤖 ML Model Suggestions"):
            for tip in fb["ml_tips"]:
                st.markdown(f"- {tip}")

    # Speech analysis
    speech = fb.get("speech", {})
    if speech and not speech.get("error"):
        with st.expander("🎙️ Speech / Delivery Analysis"):
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric("Clarity", f"{speech.get('clarity_score', 0)}%")
            with sc2:
                st.metric("Confidence", f"{speech.get('confidence_score', 0)}%")
            with sc3:
                st.metric("Pacing", f"{speech.get('pacing_score', 0)}%")

            fillers = speech.get("filler_words_found", [])
            if fillers:
                st.markdown(f"*Filler words detected:* {', '.join(fillers)}")

            for tip in speech.get("feedback", []):
                st.markdown(f"- {tip}")


def _show_hint(q: dict):
    hints = {
        "technical": "💡 Think about: *definition → how it works → example → trade-offs*. Use technical terminology.",
        "hr": "💡 Use the *STAR method*: Situation → Task → Action → Result. Keep it concise (2 min).",
    }
    q_text = q["question"].lower()
    specific = ""
    if "difference" in q_text:
        specific = " Start by defining both concepts before comparing them."
    elif "design" in q_text or "system" in q_text:
        specific = " Consider: requirements → components → scalability → trade-offs."
    elif "tell me about yourself" in q_text:
        specific = " Structure: current role → key experience → why this opportunity."

    st.info(hints.get(q["type"], "💡 Structure your answer clearly.") + specific)


def _show_session_complete():
    history = st.session_state.get("answer_history", [])
    session_scores = [h["score"] for h in history[-10:]]

    avg = round(sum(session_scores) / len(session_scores), 1) if session_scores else 0

    st.markdown(f"""
    <div class="main-header" style="text-align:center">
        <h1>🏆 Session Complete!</h1>
        <p>You answered all {len(session_scores)} questions in this session.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, (val, label) in zip([c1, c2, c3], [
        (f"{avg}%", "Average Score"),
        (len(session_scores), "Questions Done"),
        (f"{max(session_scores, default=0)}%", "Best Score")
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # Update sessions count
    s = st.session_state.get("session_stats", {"questions_answered": 0, "sessions_completed": 0, "total_scores": []})
    s["sessions_completed"] = s.get("sessions_completed", 0) + 1
    st.session_state["session_stats"] = s

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Session", use_container_width=True):
        for k in ["interview_pool", "interview_idx", "current_feedback"]:
            st.session_state.pop(k, None)
        st.rerun()