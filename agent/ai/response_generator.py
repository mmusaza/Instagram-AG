from __future__ import annotations

from openai import OpenAI

from agent.instagram.provider import InstagramComment


class ResponseGenerator:
    def __init__(self, client: OpenAI, brand_name: str = "QaravaParalq", model: str = "gpt-4.1-mini") -> None:
        self.client = client
        self.brand_name = brand_name
        self.model = model

    def generate(self, comment: InstagramComment, intent: str) -> str:
        prompt = f"""
You are the Instagram assistant for {self.brand_name}.
Tone: short, friendly, professional, natural Persian.
Never invent prices, promises, discounts, or facts.
Do not spam. Reply directly to the comment.
Intent: {intent}
Username: @{comment.username}
Comment: {comment.text}
Return only the reply text.
""".strip()
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text.strip()
