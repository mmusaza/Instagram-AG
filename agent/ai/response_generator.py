from __future__ import annotations

from agent.ai.openai_client import AIClient
from agent.instagram.provider import InstagramComment


class ResponseGenerator:
    def __init__(self, ai: AIClient, brand_name: str = "QaravaParalq") -> None:
        self.ai = ai
        self.brand_name = brand_name

    def generate(self, comment: InstagramComment, intent: str) -> str:
        prompt = f"""
You are the Instagram assistant for {self.brand_name}, a music/video production brand.
Write one short Persian reply to the following comment.
Tone: friendly, professional, natural, not robotic.
Intent: {intent}
Rules:
- Do not invent prices, discounts, availability, or promises.
- Do not spam.
- Keep the answer concise.
- If the user asks for price, invite them to contact the page for current details.

Comment by @{comment.username}:
{comment.text}
""".strip()
        return self.ai.generate(prompt)
