# Instagram-AG

Modular Instagram AI Agent for comment analysis, AI-assisted replies, memory, and future multi-account/cloud deployment.

## Project goals

- Discover posts and comments through a replaceable Instagram provider.
- Detect comments that need a response.
- Analyze comment intent and basic risk signals.
- Generate short brand-aware replies with OpenAI.
- Prevent duplicate processing and duplicate replies.
- Persist state in a database.
- Provide clear logs and a path to a dashboard/cloud worker architecture.
- Keep Instagram connectivity separate from the Agent core so the connector can change without rewriting the business logic.

## Architecture

```text
Instagram Provider
       |
       v
  Comment Engine
       |
       v
 Decision Engine -----> Memory / Database
       |
       v
    AI Engine
       |
       v
 Reply Executor
```

The first implementation is intentionally a small, testable core. Instagram-specific behavior belongs behind `agent/instagram/provider.py`.

## Security

Never commit API keys, passwords, browser sessions, cookies, or access tokens. Use `.env` locally and keep real secrets outside Git.

## Status

Architecture v1 is being built incrementally. Browser-based Instagram interaction is treated as an experimental provider; the core agent must not depend on Playwright-specific selectors.
