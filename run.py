from __future__ import annotations

import os

from dotenv import load_dotenv

from agent.ai.response_generator import ResponseGenerator
from agent.core.agent import InstagramAgent
from agent.instagram.browser import BrowserSession
from agent.instagram.browser_provider import PlaywrightInstagramProvider


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    load_dotenv()

    username = os.getenv("INSTAGRAM_USERNAME", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    auto_reply = env_bool("AUTO_REPLY", False)

    if not username:
        raise SystemExit("INSTAGRAM_USERNAME is required in .env")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required in .env")

    session = BrowserSession()
    try:
        session.start()
        session.ensure_login()

        provider = PlaywrightInstagramProvider(
            session=session,
            username=username,
            auto_reply=auto_reply,
        )
        generator = ResponseGenerator(api_key=api_key)
        agent = InstagramAgent(
            provider=provider,
            response_generator=generator,
            auto_reply=auto_reply,
        )

        print(f"Mode: {'AUTO REPLY' if auto_reply else 'DRY RUN'}")
        results = agent.run_once()
        print(f"Processed: {len(results)} comments")
        for result in results:
            print(
                f"[{result.reason}] @{result.username}: "
                f"{result.reply_text or '-'}"
            )
    finally:
        session.close()


if __name__ == "__main__":
    main()
