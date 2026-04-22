

import re
import random
from collections import Counter


# ── Skill taxonomy ──────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "kotlin", "swift", "ruby", "php", "scala", "r", "matlab"
    ],
    "Web Frameworks": [
        "react", "angular", "vue", "django", "flask", "fastapi", "spring",
        "node.js", "express", "next.js", "nuxt", "laravel", "rails", "asp.net"
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "cassandra",
        "dynamodb", "elasticsearch", "neo4j", "firebase", "supabase"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
        "github actions", "gitlab ci", "ansible", "helm", "prometheus", "grafana"
    ],
    "ML & Data Science": [
        "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy",
        "matplotlib", "seaborn", "nlp", "computer vision", "deep learning",
        "machine learning", "data analysis", "spark", "hadoop", "airflow"
    ],
    "Tools & Practices": [
        "git", "agile", "scrum", "rest api", "graphql", "microservices",
        "ci/cd", "tdd", "solid", "design patterns", "linux", "bash"
    ]
}

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "project management", "time management", "adaptability", "collaboration",
    "mentoring", "decision making", "presentation"
]

EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*years?\s+(?:of\s+)?experience",
    r"(?:over|more than)\s+(\d+)\s*years?",
    r"(\d+)\s*-\s*(\d+)\s*years?"
]

EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
    "b.sc", "m.sc", "mba", "computer science", "information technology",
    "software engineering", "data science", "electrical", "electronics"
]

SECTION_HEADERS = [
    "experience", "education", "skills", "projects", "certifications",
    "summary", "objective", "achievements", "publications", "awards"
]


# ── Resume Parser ────────────────────────────────────────────────────────────

def parse_resume(text: str) -> dict:
    """Extract structured info from raw resume text."""
    text_lower = text.lower()

    return {
        "raw_text": text,
        "skills": extract_skills(text_lower),
        "experience_years": extract_experience_years(text_lower),
        "education": extract_education(text_lower),
        "sections": detect_sections(text_lower),
        "word_count": len(text.split()),
        "has_quantified_achievements": bool(re.search(r'\d+%|\d+x|\$[\d,]+', text)),
    }


def extract_skills(text_lower: str) -> dict:
    found = {}
    for category, skills in SKILL_TAXONOMY.items():
        matched = [s for s in skills if s in text_lower]
        if matched:
            found[category] = matched
    soft = [s for s in SOFT_SKILLS if s in text_lower]
    if soft:
        found["Soft Skills"] = soft
    return found


def extract_experience_years(text_lower: str) -> int:
    for pattern in EXPERIENCE_PATTERNS:
        m = re.search(pattern, text_lower)
        if m:
            return int(m.group(1))
    # Fallback: count job/work mentions
    job_mentions = len(re.findall(r'\b(engineer|developer|analyst|manager|intern|associate)\b', text_lower))
    if job_mentions >= 3:
        return 3
    if job_mentions >= 1:
        return 1
    return 0


def extract_education(text_lower: str) -> list:
    return [kw for kw in EDUCATION_KEYWORDS if kw in text_lower]


def detect_sections(text_lower: str) -> list:
    return [s for s in SECTION_HEADERS if s in text_lower]


def get_candidate_level(years: int) -> str:
    if years == 0:
        return "fresher"
    if years <= 2:
        return "junior"
    if years <= 5:
        return "mid"
    return "senior"


# ── Question Bank ────────────────────────────────────────────────────────────

TECHNICAL_QUESTIONS = {
    "python": [
        ("What is the difference between a list and a tuple in Python?", "basic"),
        ("Explain Python's GIL (Global Interpreter Lock) and its implications.", "intermediate"),
        ("How does Python's memory management and garbage collection work?", "intermediate"),
        ("What are Python decorators and how would you implement one?", "intermediate"),
        ("Explain generators and the yield keyword with a practical example.", "intermediate"),
        ("What are metaclasses in Python and when would you use them?", "advanced"),
        ("Explain the asyncio event loop and when to use async/await.", "advanced"),
        ("How would you profile and optimize a slow Python application?", "advanced"),
    ],
    "javascript": [
        ("What is the difference between var, let, and const?", "basic"),
        ("Explain event bubbling and event capturing in the DOM.", "intermediate"),
        ("What are Promises and how do they differ from callbacks?", "intermediate"),
        ("Explain the JavaScript prototype chain.", "intermediate"),
        ("What is closure and provide a real-world use case?", "intermediate"),
        ("Explain the event loop and microtask queue in Node.js.", "advanced"),
        ("What are Web Workers and when would you use them?", "advanced"),
    ],
    "react": [
        ("What is the Virtual DOM and why does React use it?", "basic"),
        ("Explain the difference between controlled and uncontrolled components.", "intermediate"),
        ("What are React Hooks and why were they introduced?", "intermediate"),
        ("Explain useEffect dependencies and how to avoid infinite loops.", "intermediate"),
        ("How would you implement code splitting in React?", "advanced"),
        ("Explain React's reconciliation algorithm.", "advanced"),
        ("What are React Server Components and their advantages?", "advanced"),
    ],
    "machine learning": [
        ("What is the bias-variance tradeoff?", "basic"),
        ("Explain the difference between supervised and unsupervised learning.", "basic"),
        ("How does gradient descent work?", "intermediate"),
        ("What is regularization and why is it important?", "intermediate"),
        ("Explain cross-validation and k-fold validation.", "intermediate"),
        ("What is the vanishing gradient problem?", "advanced"),
        ("Explain transformer architecture and self-attention.", "advanced"),
        ("How would you handle class imbalance in a classification problem?", "intermediate"),
    ],
    "deep learning": [
        ("What is backpropagation and how does it work?", "intermediate"),
        ("Explain batch normalization and why it helps training.", "intermediate"),
        ("What is dropout and how does it prevent overfitting?", "basic"),
        ("Explain convolutional neural networks (CNNs).", "intermediate"),
        ("What are LSTMs and how do they solve vanishing gradients?", "advanced"),
        ("Explain attention mechanisms in transformers.", "advanced"),
    ],
    "databases": [
        ("What is the difference between SQL and NoSQL databases?", "basic"),
        ("Explain database normalization and the normal forms.", "intermediate"),
        ("What are database indexes and how do they work?", "intermediate"),
        ("Explain ACID properties in database transactions.", "intermediate"),
        ("What is database sharding and when would you use it?", "advanced"),
        ("Explain CAP theorem.", "advanced"),
    ],
    "docker": [
        ("What is the difference between a Docker image and a container?", "basic"),
        ("Explain the Dockerfile build process.", "intermediate"),
        ("What is Docker Compose and when would you use it?", "intermediate"),
        ("How does Docker networking work?", "advanced"),
    ],
    "kubernetes": [
        ("What problem does Kubernetes solve?", "basic"),
        ("Explain Pods, Deployments, and Services in Kubernetes.", "intermediate"),
        ("What is a Kubernetes namespace?", "intermediate"),
        ("Explain horizontal pod autoscaling.", "advanced"),
        ("What is a Kubernetes StatefulSet vs Deployment?", "advanced"),
    ],
    "aws": [
        ("What is the difference between EC2 and Lambda?", "basic"),
        ("Explain S3 storage classes.", "intermediate"),
        ("What is VPC and why is it important?", "intermediate"),
        ("How does AWS IAM work?", "intermediate"),
        ("Explain CloudFormation and infrastructure as code.", "advanced"),
    ],
    "git": [
        ("What is the difference between git merge and git rebase?", "intermediate"),
        ("Explain git branching strategies (GitFlow, trunk-based).", "intermediate"),
        ("How do you resolve a merge conflict?", "basic"),
        ("What is cherry-picking in Git?", "intermediate"),
    ],
}

GENERIC_TECHNICAL_QUESTIONS = [
    ("Explain the concept of RESTful APIs and their best practices.", "basic"),
    ("What is the difference between synchronous and asynchronous programming?", "intermediate"),
    ("Explain microservices architecture and its trade-offs.", "intermediate"),
    ("What is caching and what caching strategies do you know?", "intermediate"),
    ("Explain the SOLID principles.", "intermediate"),
    ("What is Big O notation? Give examples of different time complexities.", "basic"),
    ("How would you design a URL shortener system?", "advanced"),
    ("Explain load balancing strategies.", "advanced"),
    ("What is the difference between authentication and authorization?", "basic"),
    ("Explain the CAP theorem in distributed systems.", "advanced"),
]

HR_QUESTIONS = {
    "behavioral": [
        "Tell me about yourself and walk me through your resume.",
        "Why are you interested in this position and our company?",
        "Describe a challenging project you worked on and how you handled it.",
        "Tell me about a time you had to meet a tight deadline. How did you manage it?",
        "Describe a situation where you disagreed with your manager. How did you handle it?",
        "Tell me about a time you failed and what you learned from it.",
        "Describe a time you had to work with a difficult team member.",
        "Tell me about your greatest professional achievement.",
        "Describe a time you had to learn a new technology quickly.",
        "Give an example of when you showed leadership.",
    ],
    "situational": [
        "How would you handle receiving critical feedback about your work?",
        "What would you do if you discovered a critical bug one hour before a release?",
        "How would you approach a project where requirements keep changing?",
        "What would you do if you strongly disagreed with a technical decision made by the team?",
        "How would you handle a situation where you're stuck on a problem for multiple days?",
        "What would you do if a colleague wasn't contributing their fair share to a team project?",
    ],
    "career": [
        "Where do you see yourself in 5 years?",
        "What are your greatest strengths and areas for improvement?",
        "Why are you looking to leave your current job?",
        "What motivates you in your work?",
        "How do you stay updated with the latest developments in your field?",
        "What type of work environment do you thrive in?",
        "What are your salary expectations?",
        "Do you have any questions for us?",
    ]
}

LEVEL_QUESTION_WEIGHTS = {
    "fresher": {"basic": 0.6, "intermediate": 0.35, "advanced": 0.05},
    "junior":  {"basic": 0.3, "intermediate": 0.55, "advanced": 0.15},
    "mid":     {"basic": 0.1, "intermediate": 0.5,  "advanced": 0.4},
    "senior":  {"basic": 0.0, "intermediate": 0.3,  "advanced": 0.7},
}


def generate_questions(parsed_resume: dict, num_technical: int = 8, num_hr: int = 5) -> dict:
    """Generate a personalized question set from a parsed resume."""
    skills = parsed_resume.get("skills", {})
    years = parsed_resume.get("experience_years", 0)
    level = get_candidate_level(years)
    weights = LEVEL_QUESTION_WEIGHTS[level]

    all_skills_flat = [s for skills_list in skills.values() for s in skills_list]

    tech_questions = _pick_technical_questions(all_skills_flat, num_technical, weights)
    hr_q = _pick_hr_questions(num_hr)

    return {
        "technical": tech_questions,
        "hr": hr_q,
        "candidate_level": level,
        "detected_skills": all_skills_flat[:10],
    }


def _pick_technical_questions(skills: list, n: int, weights: dict) -> list:
    pool = []

    # Add skill-specific questions
    for skill in skills:
        if skill in TECHNICAL_QUESTIONS:
            for q, difficulty in TECHNICAL_QUESTIONS[skill]:
                pool.append({"question": q, "difficulty": difficulty, "topic": skill.title()})

    # Add generic questions
    for q, difficulty in GENERIC_TECHNICAL_QUESTIONS:
        pool.append({"question": q, "difficulty": difficulty, "topic": "General"})

    # Filter & weight by difficulty
    def score(item):
        d = item["difficulty"]
        return weights.get(d, 0.1) + random.uniform(0, 0.1)

    pool.sort(key=score, reverse=True)
    seen = set()
    result = []
    for item in pool:
        if item["question"] not in seen and len(result) < n:
            seen.add(item["question"])
            result.append(item)

    return result


def _pick_hr_questions(n: int) -> list:
    result = []
    cats = list(HR_QUESTIONS.keys())
    per_cat = max(1, n // len(cats))
    for cat in cats:
        chosen = random.sample(HR_QUESTIONS[cat], min(per_cat, len(HR_QUESTIONS[cat])))
        for q in chosen:
            result.append({"question": q, "category": cat.title()})
    return result[:n]


# ── Answer Evaluation ────────────────────────────────────────────────────────

def evaluate_answer(question: str, answer: str, expected_keywords: list = None) -> dict:
    """Score an answer across multiple dimensions."""
    if not answer or not answer.strip():
        return {"overall_score": 0, "feedback": "No answer provided.", "breakdown": {}}

    answer_lower = answer.lower()
    words = answer.split()

    # ── Dimension 1: Length / Completeness ───────────────────────────────
    length_score = min(100, (len(words) / 80) * 100)
    if len(words) < 10:
        length_score = 20
    elif len(words) > 300:
        length_score = min(100, length_score * 0.85)  # slight penalty for rambling

    # ── Dimension 2: Keyword Coverage ────────────────────────────────────
    extracted_kw = _extract_expected_keywords(question)
    if expected_keywords:
        extracted_kw.extend(expected_keywords)
    extracted_kw = list(set(extracted_kw))

    matched_kw = [kw for kw in extracted_kw if kw.lower() in answer_lower]
    keyword_score = (len(matched_kw) / len(extracted_kw) * 100) if extracted_kw else 60

    # ── Dimension 3: Structure ────────────────────────────────────────────
    structure_score = 50
    has_intro   = any(w in answer_lower for w in ["first", "to begin", "essentially", "basically", "in summary"])
    has_example = any(w in answer_lower for w in ["for example", "for instance", "such as", "like when", "e.g"])
    has_detail  = any(w in answer_lower for w in ["because", "therefore", "which means", "this allows", "as a result"])

    if has_intro:   structure_score += 15
    if has_example: structure_score += 20
    if has_detail:  structure_score += 15
    structure_score = min(100, structure_score)

    # ── Dimension 4: Confidence Indicators ───────────────────────────────
    hedge_words = ["maybe", "i think", "i'm not sure", "probably", "i guess", "perhaps", "might be"]
    confident_words = ["definitely", "clearly", "specifically", "precisely", "importantly"]
    hedges    = sum(1 for h in hedge_words if h in answer_lower)
    confident = sum(1 for c in confident_words if c in answer_lower)
    confidence_score = max(20, min(100, 70 - hedges * 10 + confident * 8))

    # ── Weighted Overall ──────────────────────────────────────────────────
    overall = round(
        length_score    * 0.25 +
        keyword_score   * 0.35 +
        structure_score * 0.25 +
        confidence_score * 0.15
    )
    overall = max(0, min(100, overall))

    return {
        "overall_score": overall,
        "breakdown": {
            "Completeness": round(length_score),
            "Keyword Coverage": round(keyword_score),
            "Structure": round(structure_score),
            "Confidence": round(confidence_score),
        },
        "matched_keywords": matched_kw[:8],
        "missing_keywords": [kw for kw in extracted_kw if kw not in matched_kw][:5],
        "word_count": len(words),
        "feedback": _generate_feedback(overall, matched_kw, extracted_kw, len(words), has_example),
    }


def _extract_expected_keywords(question: str) -> list:
    """Heuristically pull expected terms from the question text."""
    q_lower = question.lower()
    kw = []
    all_terms = [s for skills in SKILL_TAXONOMY.values() for s in skills] + [
        "example", "difference", "explain", "advantage", "disadvantage",
        "use case", "performance", "scalability", "security"
    ]
    kw = [t for t in all_terms if t in q_lower]

    # Add question-type keywords
    if "difference between" in q_lower:
        parts = re.findall(r'between\s+(\w+)\s+and\s+(\w+)', q_lower)
        for a, b in parts:
            kw += [a, b]
    if "explain" in q_lower:
        kw.append("example")
    if "design" in q_lower:
        kw += ["scalability", "availability", "database"]

    return list(set(kw))[:10]


def _generate_feedback(score: int, matched: list, expected: list, wc: int, has_example: bool) -> str:
    parts = []

    if score >= 80:
        parts.append("✅ Strong answer — well-structured and comprehensive.")
    elif score >= 60:
        parts.append("🟡 Good answer with room for improvement.")
    else:
        parts.append("🔴 Needs significant improvement. Focus on depth and clarity.")

    if wc < 30:
        parts.append("Your answer is too brief — aim for at least 50–80 words.")
    elif wc > 250:
        parts.append("Consider tightening your answer; avoid unnecessary repetition.")

    if not has_example:
        parts.append("Adding a concrete example would strengthen your answer.")

    missing = [kw for kw in expected if kw not in matched][:3]
    if missing:
        parts.append(f"Consider mentioning: {', '.join(missing)}.")

    return " ".join(parts)


# ── Text utilities ───────────────────────────────────────────────────────────

def extract_keywords_from_text(text: str, top_n: int = 15) -> list:
    """Simple frequency-based keyword extraction (no NLTK required)."""
    STOP = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "i", "you", "we", "they",
        "he", "she", "it", "my", "your", "our", "their", "this", "that",
        "these", "those", "as", "if", "when", "where", "which", "who", "what",
        "how", "not", "no", "so", "up", "out", "about", "into", "through",
        "during", "before", "after", "between", "each", "more", "also", "than",
        "then", "its", "been", "very", "just"
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    freq = Counter(w for w in words if w not in STOP)
    return [word for word, _ in freq.most_common(top_n)]