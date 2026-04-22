# 🎯 AI Interview Preparation System

A full-featured, AI-powered interview prep platform built with Python, NLP, ML, and Streamlit.

## Features

| Module | Description |
|--------|-------------|
| 📄 Resume Analyzer | NLP-based skill extraction, experience detection, resume quality scoring |
| ❓ Question Bank | 100+ technical + HR questions filtered by skill, topic & difficulty |
| 🎙️ Mock Interview | Real-time answer evaluation with NLP + ML scoring |
| 📊 Performance Tracker | Score trend charts, focus area recommendations, history |
| 🗣️ Speech Analysis | Filler word detection, confidence & clarity scoring |

## Quick Start

```bash
# 1. Clone / unzip the project
cd interview_prep

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

## Project Structure

```
interview_prep/
├── app.py                    # Main entry point + global CSS
├── requirements.txt
├── pages/
│   ├── dashboard.py          # Home dashboard
│   ├── resume_analyzer.py    # Resume upload + NLP analysis
│   ├── question_bank.py      # Browsable question library
│   ├── mock_interview.py     # Practice session + feedback
│   └── performance.py        # Charts + progress tracking
├── utils/
│   ├── nlp_utils.py          # Resume parsing, keyword extraction, Q generation, answer evaluation
│   └── speech_utils.py       # STT simulation + filler word analysis
└── models/
    └── scoring_model.py      # Feature extraction + weighted ML scoring model
```

## How It Works

### NLP Pipeline
1. **Resume Parsing** — regex + keyword matching extracts skills, experience years, education
2. **Question Generation** — selects questions from a taxonomy weighted by detected skills and candidate level
3. **Answer Evaluation** — scores on 4 dimensions: completeness, keyword coverage, structure, confidence

### ML Scoring Model
- Extracts 12 features from answers (word count, technical terms, transitions, relevance, etc.)
- Applies weighted feature scoring with sigmoid normalization
- Blends with NLP score (60% NLP / 40% ML) for final result

### Speech Analysis
- Detects filler words (um, uh, like, you know…)
- Scores clarity, confidence, and pacing
- Real microphone support via `SpeechRecognition` (optional)

## Optional: Real Speech-to-Text

```bash
pip install SpeechRecognition pyaudio
```

Then use `transcribe_audio_file(path)` from `utils/speech_utils.py`.

## Extending the Project

- **Add questions**: Edit `TECHNICAL_QUESTIONS` or `HR_QUESTIONS` dicts in `utils/nlp_utils.py`
- **Improve scoring**: Replace `AnswerScoringModel` in `models/scoring_model.py` with a trained sklearn model
- **Add auth**: Integrate `streamlit-authenticator` for multi-user support
- **Database**: Swap `st.session_state` for SQLite/PostgreSQL to persist data across sessions
[README.md](https://github.com/user-attachments/files/26979763/README.md)

