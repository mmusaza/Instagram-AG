from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    NORMAL = "normal"
    QUESTION = "question"
    PURCHASE = "purchase"
    POSITIVE = "positive"
    SPAM = "spam"


@dataclass(frozen=True, slots=True)
class CommentAnalysis:
    intent: Intent
    needs_reply: bool
    reason: str


def analyze_comment(text: str, has_reply_from_page: bool = False) -> CommentAnalysis:
    value = text.strip()
    if not value:
        return CommentAnalysis(Intent.NORMAL, False, "empty comment")
    if has_reply_from_page:
        return CommentAnalysis(Intent.NORMAL, False, "already answered")

    lower = value.lower()
    if "http://" in lower or "https://" in lower or "www." in lower:
        return CommentAnalysis(Intent.SPAM, False, "contains link")

    purchase_words = ("قیمت", "خرید", "سفارش", "هزینه", "price", "buy")
    question_words = ("؟", "?", "چطور", "چگونه", "کجا", "how", "what", "where")
    positive_words = ("عالی", "خوبه", "عاشق", "perfect", "great", "love")

    if any(word in lower for word in purchase_words):
        return CommentAnalysis(Intent.PURCHASE, True, "purchase intent")
    if any(word in lower for word in question_words):
        return CommentAnalysis(Intent.QUESTION, True, "question")
    if any(word in lower for word in positive_words):
        return CommentAnalysis(Intent.POSITIVE, True, "positive comment")
    return CommentAnalysis(Intent.NORMAL, True, "normal unanswered comment")
