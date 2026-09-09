from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommentIntent(str, Enum):
    QUESTION = "question"
    PURCHASE = "purchase"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    SPAM = "spam"
    NORMAL = "normal"


@dataclass(slots=True)
class CommentAnalysis:
    intent: CommentIntent
    needs_reply: bool
    reason: str


def analyze_comment(text: str, has_reply_from_page: bool) -> CommentAnalysis:
    """Fast deterministic pre-filter before calling an LLM."""
    clean = " ".join(text.lower().split())

    if has_reply_from_page:
        return CommentAnalysis(CommentIntent.NORMAL, False, "already answered")

    if not clean:
        return CommentAnalysis(CommentIntent.NORMAL, False, "empty comment")

    spam_terms = ("http://", "https://", "buy followers", "free followers")
    if any(term in clean for term in spam_terms):
        return CommentAnalysis(CommentIntent.SPAM, False, "possible spam")

    question_mark = "?" in clean
    purchase_terms = ("price", "قیمت", "هزینه", "سفارش", "خرید")
    positive_terms = ("عالی", "خوبه", "love", "great", "beautiful")
    negative_terms = ("بد", "افتضاح", "مشکل", "bad", "terrible")

    if any(term in clean for term in purchase_terms):
        return CommentAnalysis(CommentIntent.PURCHASE, True, "purchase-related terms")
    if question_mark:
        return CommentAnalysis(CommentIntent.QUESTION, True, "question detected")
    if any(term in clean for term in positive_terms):
        return CommentAnalysis(CommentIntent.POSITIVE, True, "positive feedback")
    if any(term in clean for term in negative_terms):
        return CommentAnalysis(CommentIntent.NEGATIVE, True, "negative feedback")

    return CommentAnalysis(CommentIntent.NORMAL, True, "new comment")
