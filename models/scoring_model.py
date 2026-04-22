"""
ML Scoring Models — answer quality assessment without heavy dependencies
"""

import math
import random
import re
from datetime import datetime


# ── Feature Extraction ───────────────────────────────────────────────────────

def extract_features(answer: str, question: str = "") -> dict:
    """Extract ML-ready features from an answer string."""
    if not answer:
        return {f: 0 for f in _feature_names()}

    words = answer.split()
    sentences = re.split(r'[.!?]+', answer)
    sentences = [s.strip() for s in sentences if s.strip()]

    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    avg_sent_len = len(words) / max(len(sentences), 1)

    tech_terms = _count_technical_terms(answer.lower())
    transition_words = _count_transitions(answer.lower())
    numbers = len(re.findall(r'\b\d+\b', answer))
    bullet_points = answer.count('\n-') + answer.count('\n•') + answer.count('\n*')

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": round(avg_word_len, 2),
        "avg_sentence_length": round(avg_sent_len, 2),
        "technical_term_count": tech_terms,
        "transition_word_count": transition_words,
        "number_count": numbers,
        "bullet_point_count": bullet_points,
        "has_example": int(bool(re.search(r'for example|for instance|e\.g|such as', answer.lower()))),
        "has_definition": int(bool(re.search(r'is a|refers to|defined as|means that', answer.lower()))),
        "has_comparison": int(bool(re.search(r'whereas|however|on the other hand|in contrast|difference', answer.lower()))),
        "question_relevance": _simple_relevance(answer, question),
    }


def _feature_names():
    return [
        "word_count", "sentence_count", "avg_word_length", "avg_sentence_length",
        "technical_term_count", "transition_word_count", "number_count",
        "bullet_point_count", "has_example", "has_definition", "has_comparison",
        "question_relevance"
    ]


def _count_technical_terms(text: str) -> int:
    tech = [
        "algorithm", "function", "method", "class", "object", "instance",
        "variable", "parameter", "argument", "return", "loop", "recursion",
        "complexity", "performance", "memory", "cache", "database", "query",
        "api", "endpoint", "request", "response", "thread", "process",
        "async", "synchronous", "callback", "promise", "event", "state",
        "component", "module", "library", "framework", "architecture",
        "design pattern", "scalability", "latency", "throughput", "bottleneck"
    ]
    return sum(1 for t in tech if t in text)


def _count_transitions(text: str) -> int:
    transitions = [
        "first", "second", "third", "finally", "additionally", "furthermore",
        "moreover", "however", "therefore", "consequently", "in addition",
        "on the other hand", "for example", "specifically", "in summary"
    ]
    return sum(1 for t in transitions if t in text)


def _simple_relevance(answer: str, question: str) -> float:
    if not question:
        return 0.5
    q_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', question.lower()))
    a_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', answer.lower()))
    if not q_words:
        return 0.5
    overlap = q_words & a_words
    return round(min(1.0, len(overlap) / max(len(q_words), 1)), 2)


# ── Scoring Model (rule-based ML proxy) ─────────────────────────────────────

class AnswerScoringModel:
    """
    A transparent, rule-based scoring model that simulates a trained classifier.
    Uses weighted feature scoring with sigmoid normalization — no external ML deps.
    """

    WEIGHTS = {
        "word_count":            0.20,
        "technical_term_count":  0.25,
        "transition_word_count": 0.15,
        "has_example":           0.15,
        "has_definition":        0.10,
        "has_comparison":        0.08,
        "question_relevance":    0.07,
    }

    def predict_score(self, features: dict) -> float:
        """Return a 0–100 quality score."""
        raw = 0.0

        # Word count contribution (sigmoid-shaped)
        wc = features.get("word_count", 0)
        raw += self.WEIGHTS["word_count"] * self._sigmoid_score(wc, center=80, scale=30) * 100

        # Technical terms (log-scaled)
        tc = features.get("technical_term_count", 0)
        raw += self.WEIGHTS["technical_term_count"] * min(100, tc * 15)

        # Transition words
        tw = features.get("transition_word_count", 0)
        raw += self.WEIGHTS["transition_word_count"] * min(100, tw * 20)

        # Boolean features
        raw += self.WEIGHTS["has_example"]    * features.get("has_example", 0) * 100
        raw += self.WEIGHTS["has_definition"] * features.get("has_definition", 0) * 100
        raw += self.WEIGHTS["has_comparison"] * features.get("has_comparison", 0) * 100

        # Relevance
        raw += self.WEIGHTS["question_relevance"] * features.get("question_relevance", 0) * 100

        # Penalty for very long rambling answers
        if wc > 300:
            raw *= 0.92
        # Penalty for very short answers
        if wc < 15:
            raw *= 0.4

        return round(min(100, max(0, raw)), 1)

    def predict_grade(self, score: float) -> str:
        if score >= 85: return "Excellent"
        if score >= 70: return "Good"
        if score >= 55: return "Average"
        if score >= 40: return "Below Average"
        return "Needs Improvement"

    def get_improvement_tips(self, features: dict, score: float) -> list:
        tips = []
        wc = features.get("word_count", 0)
        if wc < 30:
            tips.append("Expand your answer — aim for at least 60–100 words for technical questions.")
        if features.get("has_example", 0) == 0:
            tips.append("Include a concrete example or real-world scenario to illustrate your point.")
        if features.get("technical_term_count", 0) < 2:
            tips.append("Use more domain-specific terminology to demonstrate technical depth.")
        if features.get("transition_word_count", 0) < 2:
            tips.append("Use transition words (first, additionally, therefore) to improve flow.")
        if features.get("has_definition", 0) == 0:
            tips.append("Start by defining the key concept before diving into details.")
        if features.get("question_relevance", 0) < 0.3:
            tips.append("Make sure your answer directly addresses what was asked.")
        if not tips:
            tips.append("Great answer! Consider adding more edge cases or trade-off discussions.")
        return tips

    @staticmethod
    def _sigmoid_score(x: float, center: float, scale: float) -> float:
        z = (x - center) / scale
        return 1 / (1 + math.exp(-z))


# ── Session Tracker ──────────────────────────────────────────────────────────

class PerformanceTracker:
    """Tracks scores across a mock interview session."""

    def _init_(self):
        self.records = []

    def record(self, question: str, answer: str, score: float, q_type: str):
        self.records.append({
            "timestamp": datetime.now().isoformat(),
            "question": question[:80] + "..." if len(question) > 80 else question,
            "score": score,
            "type": q_type,
            "word_count": len(answer.split()),
        })

    def summary(self) -> dict:
        if not self.records:
            return {}
        scores = [r["score"] for r in self.records]
        return {
            "total_questions": len(self.records),
            "average_score": round(sum(scores) / len(scores), 1),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "technical_avg": self._avg_by_type("technical"),
            "hr_avg": self._avg_by_type("hr"),
            "trend": self._trend(),
        }

    def _avg_by_type(self, q_type: str) -> float:
        subset = [r["score"] for r in self.records if r["type"] == q_type]
        return round(sum(subset) / len(subset), 1) if subset else 0.0

    def _trend(self) -> str:
        if len(self.records) < 3:
            return "neutral"
        first_half = self.records[:len(self.records)//2]
        second_half = self.records[len(self.records)//2:]
        avg1 = sum(r["score"] for r in first_half) / len(first_half)
        avg2 = sum(r["score"] for r in second_half) / len(second_half)
        if avg2 > avg1 + 5:
            return "improving"
        if avg2 < avg1 - 5:
            return "declining"
        return "stable"