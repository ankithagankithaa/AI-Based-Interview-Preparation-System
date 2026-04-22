import streamlit as st
from utils.nlp_utils import parse_resume, generate_questions, extract_keywords_from_text


SAMPLE_RESUME = """
John Doe
Software Engineer | 3 Years Experience
john.doe@email.com | LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

SUMMARY
Experienced software engineer with 3 years of experience building scalable web applications 
and data pipelines. Proficient in Python, JavaScript, and cloud technologies.

SKILLS
Languages: Python, JavaScript, TypeScript, SQL, Bash
Frameworks: React, FastAPI, Django, Node.js
Databases: PostgreSQL, MongoDB, Redis
Cloud/DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, GitHub Actions
ML/AI: scikit-learn, pandas, numpy, machine learning, NLP
Tools: Git, Agile, Scrum, REST API, Microservices

EXPERIENCE
Senior Software Engineer — TechCorp Inc. (2022 – Present)
* Designed and implemented a microservices architecture that reduced system latency by 40%
* Led a team of 4 engineers to deliver a real-time analytics dashboard using React and FastAPI
* Automated CI/CD pipelines using GitHub Actions, reducing deployment time by 60%
* Integrated machine learning models into production APIs serving 500k daily users

Software Engineer — StartupXYZ (2021 – 2022)
* Built RESTful APIs in Django serving mobile and web clients
* Optimised PostgreSQL queries, improving response times by 35%
* Developed data pipelines using pandas and numpy processing 10GB+ daily

EDUCATION
B.Tech in Computer Science — XYZ University (2017–2021)
GPA: 8.5/10 | Relevant coursework: Data Structures, Algorithms, Machine Learning, Databases

PROJECTS
Real-time Chat Application — React, Node.js, WebSockets, Redis
* Built a scalable chat system supporting 10,000 concurrent users

ML-based Fraud Detection — Python, scikit-learn, FastAPI
* Achieved 94% accuracy detecting fraudulent transactions with gradient boosting

CERTIFICATIONS
* AWS Certified Solutions Architect – Associate
* Google Professional Data Engineer
"""


def show():
    st.markdown("""
    <div class="main-header">
        <h1>📄 Resume Analyzer</h1>
        <p>Paste your resume text below. Our NLP engine will extract skills, experience, and generate tailored interview questions.</p>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 1.1], gap="large")

    with col_input:
        st.markdown("#### 📝 Resume Input")

        use_sample = st.checkbox("Use sample resume (demo)", value=False)
        resume_text = SAMPLE_RESUME if use_sample else ""

        resume_input = st.text_area(
            "Paste your resume text here",
            value=resume_text,
            height=420,
            placeholder="Paste your resume text here...\n\nInclude: Skills, Experience, Education, Projects",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_btn = st.button("🔍 Analyse Resume", use_container_width=True)
        with col_btn2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.pop("resume_parsed", None)
                st.session_state.pop("generated_questions", None)
                st.rerun()

        if analyze_btn and resume_input.strip():
            with st.spinner("🧠 Analysing resume with NLP..."):
                parsed = parse_resume(resume_input)
                questions = generate_questions(parsed, num_technical=10, num_hr=6)

                # Merge into a single state object
                parsed_state = {**parsed, **questions}
                st.session_state["resume_parsed"] = parsed_state
                st.session_state["generated_questions"] = questions
                st.session_state["detected_skills"] = questions.get("detected_skills", [])

            st.success("✅ Resume analysed! Questions generated.")

        elif analyze_btn:
            st.warning("Please paste your resume text first.")

    with col_results:
        parsed = st.session_state.get("resume_parsed")

        if not parsed:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; color:#8888aa;">
                <div style="font-size:3rem">📋</div>
                <p>Your analysis results will appear here.</p>
                <p style="font-size:0.85rem">Paste your resume and click <strong>Analyse Resume</strong></p>
            </div>
            """, unsafe_allow_html=True)
            return

        # ── Summary cards ─────────────────────────────────────────────────
        level = parsed.get("candidate_level", "unknown").title()
        years = parsed.get("experience_years", 0)
        wc    = parsed.get("word_count", 0)

        c1, c2, c3 = st.columns(3)
        for col, (val, label) in zip(
            [c1, c2, c3],
            [(level, "Level"), (f"{years}y", "Experience"), (wc, "Words")]
        ):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Skills detected ───────────────────────────────────────────────
        st.markdown("#### 🔍 Detected Skills")
        skills_dict = parsed.get("skills", {})
        if skills_dict:
            for category, skill_list in skills_dict.items():
                if skill_list:
                    tags = " ".join([f'<span class="tag">{s}</span>' for s in skill_list])
                    st.markdown(f"*{category}*", unsafe_allow_html=False)
                    st.markdown(tags, unsafe_allow_html=True)
                    st.markdown("")
        else:
            st.info("No specific skills detected. Try adding a skills section.")

        # ── Resume quality indicators ─────────────────────────────────────
        st.markdown("#### 📊 Resume Quality")
        checks = {
            "Has quantified achievements": parsed.get("has_quantified_achievements", False),
            "Contains multiple sections":  len(parsed.get("sections", [])) >= 3,
            "Sufficient word count":       parsed.get("word_count", 0) >= 200,
            "Education mentioned":         bool(parsed.get("education")),
            "Technical skills listed":     bool(parsed.get("skills", {}).get("Programming Languages")),
        }
        for check, passed in checks.items():
            icon = "✅" if passed else "❌"
            color = "#4ade80" if passed else "#f87171"
            st.markdown(f'<span style="color:{color}">{icon}</span> {check}', unsafe_allow_html=True)

        # ── Top keywords ──────────────────────────────────────────────────
        raw_text = parsed.get("raw_text", "")
        if raw_text:
            kw = extract_keywords_from_text(raw_text, top_n=10)
            st.markdown("#### 🏷️ Top Keywords")
            st.markdown(" ".join([f'<span class="tag">{k}</span>' for k in kw]), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"✅ *{len(parsed.get('technical', []))} technical* and *{len(parsed.get('hr', []))} HR* questions generated. Go to *Question Bank* or *Mock Interview* to practise.")