"""NLP engine: text preprocessing, TF-IDF vectorisation and cosine-similarity matching."""
import re
from dataclasses import dataclass, field

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Keep negations: "not receiving emails" differs from "receiving emails".
STOP_WORDS = set(ENGLISH_STOP_WORDS) - {"not", "no", "cannot"}

# Multi-word phrases are merged into one canonical word before tokenising.
PHRASES = {"sign up": "register", "sign in": "login", "log in": "login",
           "log on": "login", "log out": "logout", "sign out": "logout",
           "without internet": "offline", "no internet": "offline", "without wifi": "offline"}

# Small synonym map so differently worded questions land on the same token.
SYNONYMS = {
    "cost": "price", "costs": "price", "pricing": "price", "prices": "price", "fee": "price",
    "fees": "price", "charge": "price", "charges": "price", "expensive": "price", "cheap": "price",
    "signup": "register", "join": "register", "enroll": "register", "registration": "register",
    "remove": "delete", "erase": "delete", "terminate": "delete", "unsubscribe": "delete",
    "passcode": "password", "pwd": "password", "forgotten": "forgot",
    "application": "app", "software": "app", "mobile": "phone", "smartphone": "phone",
    "mail": "email", "emails": "email", "bug": "error", "glitch": "error", "problem": "error",
    "issue": "error", "broken": "error", "reimbursement": "refund", "money": "refund",
    "safe": "secure", "safety": "secure", "security": "secure", "protect": "secure",
    "hacked": "secure", "kept": "store", "keep": "store", "stored": "store", "contact": "support", "helpdesk": "support", "agent": "support",
}


def _stem(word: str) -> str:
    """Very light suffix stripping (no external downloads needed)."""
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def preprocess(text: str) -> list:
    """Lowercase -> merge phrases -> strip punctuation -> tokenise -> synonyms -> stop words -> stem."""
    text = re.sub(r"\s+", " ", str(text).lower()).strip()
    for phrase, canon in PHRASES.items():
        text = text.replace(phrase, canon)
    text = text.replace("can't", "cannot").replace("can not", "cannot")
    tokens = re.findall(r"[a-z0-9]+", text)
    tokens = [SYNONYMS.get(t, t) for t in tokens]
    return [_stem(t) for t in tokens if t not in STOP_WORDS]


@dataclass
class Result:
    matched: bool
    answer: str
    category: str = ""
    question: str = ""
    score: float = 0.0
    related: list = field(default_factory=list)


class FAQEngine:
    """Builds TF-IDF vectors for every FAQ and answers with the most similar one."""

    def __init__(self, faqs):
        self.faqs = faqs.reset_index(drop=True)
        self.ready = len(self.faqs) > 0
        if self.ready:
            self.vectorizer = TfidfVectorizer(tokenizer=preprocess, lowercase=False,
                                              token_pattern=None, ngram_range=(1, 2), sublinear_tf=True)
            questions = self.faqs["question"].tolist()
            answers = self.faqs["answer"].tolist()
            self.vectorizer.fit(questions + answers)
            self.q_matrix = self.vectorizer.transform(questions)
            self.a_matrix = self.vectorizer.transform(answers)

    def ask(self, text, threshold: float = 0.25) -> Result:
        if not self.ready:
            return Result(False, "The knowledge base is empty. Add FAQs in the Admin page.")
        if not text or not str(text).strip():
            return Result(False, "Please type a question first.")
        if not preprocess(text):
            return Result(False, "I could not understand that. Try asking a full question.")
        vec = self.vectorizer.transform([text])
        # Question similarity matters most; answer similarity helps with differently worded questions.
        scores = 0.8 * cosine_similarity(vec, self.q_matrix)[0] + 0.2 * cosine_similarity(vec, self.a_matrix)[0]
        order = np.argsort(scores)[::-1]
        best = int(order[0])
        related = [self.faqs.loc[i, "question"] for i in order[1:4] if scores[i] >= 0.03]
        row = self.faqs.loc[best]
        if scores[best] >= threshold:
            return Result(True, row["answer"], row["category"], row["question"], float(scores[best]), related)
        suggestions = [self.faqs.loc[i, "question"] for i in order[:3] if scores[i] >= 0.03]
        return Result(False, "I could not find a confident answer to that. Try rephrasing, or pick a related question below.",
                      score=float(scores[best]), related=suggestions)
