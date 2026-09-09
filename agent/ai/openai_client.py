from __future__ import annotations

import os

from openai import OpenAI


class AIClient:
    def __init__(self, api_key: str | None = None, model: str = "gpt-4.1-mini") -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is not configured")
        self.client = OpenAI(api_key=key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text.strip()
