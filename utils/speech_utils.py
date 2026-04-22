"""
Speech Processing Utilities
Provides: simulated STT demo + optional real microphone capture via SpeechRecognition
"""

import random
import re


FILLER_WORDS = [
    "um", "uh", "like", "you know", "sort of", "kind of",
    "basically", "literally", "actually", "honestly", "right"
]

CLARITY_PHRASES = {
    "good": [
        "to summarize", "in conclusion", "the key point is",
        "to clarify", "what I mean is", "specifically"
    ],
    "poor": [
        "i don't know", "i'm not sure", "it's complicated",
        "that's hard to explain", "i forget"
    ]
}


def analyze_speech_text(text: str) -> dict:
    """
    Analyse a transcribed answer for filler words, clarity, pacing proxy,
    and confidence signals.
    """
    if not text or not text.strip():
        return {"error": "No text to analyse."}

    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # ── Filler word detection ─────────────────────────────────────────────
    filler_hits = []
    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        hits = re.findall(pattern, text_lower)
        if hits:
            filler_hits.extend(hits)

    filler_count = len(filler_hits)
    filler_ratio = filler_count / max(word_count, 1)

    # ── Clarity signals ───────────────────────────────────────────────────
    good_clarity = sum(1 for p in CLARITY_PHRASES["good"] if p in text_lower)
    poor_clarity = sum(1 for p in CLARITY_PHRASES["poor"] if p in text_lower)

    # ── Pacing proxy (sentence length variance) ───────────────────────────
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sent_lengths = [len(s.split()) for s in sentences]
    avg_sent_len = sum(sent_lengths) / max(len(sent_lengths), 1)
    pacing_score = _pacing_score(avg_sent_len)

    # ── Confidence score ──────────────────────────────────────────────────
    confidence = _confidence_score(filler_ratio, good_clarity, poor_clarity)

    # ── Clarity score ─────────────────────────────────────────────────────
    clarity = _clarity_score(sentences, good_clarity, poor_clarity)

    return {
        "word_count": word_count,
        "sentence_count": len(sentences),
        "filler_words_found": list(set(filler_hits))[:8],
        "filler_count": filler_count,
        "filler_ratio": round(filler_ratio, 3),
        "clarity_score": clarity,
        "confidence_score": confidence,
        "pacing_score": pacing_score,
        "avg_sentence_length": round(avg_sent_len, 1),
        "feedback": _speech_feedback(filler_count, confidence, clarity, pacing_score),
    }


def _pacing_score(avg_sent_len: float) -> int:
    """Ideal spoken answer: 12–20 words per sentence."""
    if 12 <= avg_sent_len <= 20:
        return 90
    elif 8 <= avg_sent_len < 12 or 20 < avg_sent_len <= 28:
        return 70
    elif avg_sent_len < 8:
        return 50  # too choppy
    else:
        return 45  # run-on sentences


def _confidence_score(filler_ratio: float, good: int, poor: int) -> int:
    score = 80
    score -= min(40, int(filler_ratio * 150))
    score += good * 5
    score -= poor * 8
    return max(10, min(100, score))


def _clarity_score(sentences: list, good: int, poor: int) -> int:
    score = 65
    # Reward having multiple complete sentences
    if len(sentences) >= 3:
        score += 15
    score += good * 8
    score -= poor * 10
    return max(10, min(100, score))


def _speech_feedback(filler_count: int, confidence: int, clarity: int, pacing: int) -> list:
    tips = []
    if filler_count > 5:
        tips.append(f"⚠️ You used {filler_count} filler words. Practice pausing instead of saying 'um' or 'uh'.")
    elif filler_count > 2:
        tips.append(f"🟡 {filler_count} filler words detected — slight improvement possible.")
    else:
        tips.append("✅ Minimal filler words — great fluency!")

    if confidence < 55:
        tips.append("💪 Work on projecting confidence — avoid hedging phrases like 'I'm not sure'.")
    elif confidence >= 80:
        tips.append("✅ You sound confident and assertive.")

    if clarity < 55:
        tips.append("📝 Improve clarity by organizing your answer with clear signpost phrases.")
    elif clarity >= 80:
        tips.append("✅ Your answer is clear and well-structured.")

    if pacing < 60:
        tips.append("⏱️ Adjust your pacing — try forming complete, medium-length sentences.")

    return tips


# ── Optional real microphone capture ────────────────────────────────────────

def transcribe_audio_file(audio_path: str) -> dict:
    """
    Attempt real transcription via SpeechRecognition.
    Falls back gracefully if the package isn't installed.
    """
    try:
        import speech_recognition as sr  # type: ignore
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return {"success": True, "text": text}
    except ImportError:
        return {"success": False, "error": "speech_recognition not installed. Run: pip install SpeechRecognition"}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_demo_transcription(question_type: str = "technical") -> str:
    """Return a realistic demo transcription for UI testing."""
    samples = {
        "technical": [
            "So basically, the difference between a list and a tuple in Python is that lists are mutable, "
            "um, meaning you can change their contents, whereas tuples are immutable. For example, if you "
            "have a list, you can append or remove elements, but with a tuple you cannot. Tuples are also "
            "slightly more memory efficient and can be used as dictionary keys because they are hashable.",

            "A decorator in Python is essentially a function that wraps another function to extend its "
            "behaviour without modifying it. For instance, you might use a decorator to add logging or "
            "timing to a function. The way it works is you define a wrapper function inside the decorator, "
            "and then return that wrapper. The at-sign syntax is syntactic sugar for this pattern.",
        ],
        "hr": [
            "Sure, so I would describe myself as someone who is really passionate about solving complex "
            "technical problems. I have, um, around three years of experience in software development, "
            "and I particularly enjoy working on backend systems and APIs. In my last role, I led a team "
            "that, you know, rebuilt our payment processing pipeline which reduced latency by about forty percent.",

            "I think my greatest strength is my ability to break down complex problems into manageable pieces. "
            "For example, when I joined my last company, the codebase was quite disorganised and I systematically "
            "refactored it over three months. As for areas of improvement, I'm working on delegating more "
            "effectively rather than trying to do everything myself.",
        ]
    }
    pool = samples.get(question_type, samples["technical"])
    return random.choice(pool)