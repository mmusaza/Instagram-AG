from __future__ import annotations

from dataclasses import dataclass

from agent.ai.response_generator import ResponseGenerator
from agent.core.comment_analyzer import analyze_comment
from agent.instagram.provider import InstagramComment, InstagramProvider


@dataclass(slots=True)
class AgentResult:
    post_id: str
    comment_id: str
    username: str
    replied: bool
    reply_text: str | None
    reason: str


class InstagramAgent:
    """Provider-agnostic orchestration layer."""

    def __init__(self, provider: InstagramProvider, response_generator: ResponseGenerator) -> None:
        self.provider = provider
        self.response_generator = response_generator

    def process_comment(self, comment: InstagramComment) -> AgentResult:
        analysis = analyze_comment(comment.text, comment.has_reply_from_page)
        if not analysis.needs_reply:
            return AgentResult(
                comment.post_id,
                comment.id,
                comment.username,
                False,
                None,
                analysis.reason,
            )

        reply = self.response_generator.generate(comment, analysis.intent.value)
        self.provider.reply_to_comment(comment, reply)
        return AgentResult(
            comment.post_id,
            comment.id,
            comment.username,
            True,
            reply,
            "reply sent",
        )

    def run_once(self) -> list[AgentResult]:
        results: list[AgentResult] = []
        for post in self.provider.list_posts():
            for comment in self.provider.list_comments(post):
                results.append(self.process_comment(comment))
        return results
