# Instagram-AG

A modular Instagram AI Agent for discovering comments, analyzing intent, generating brand-aware replies, tracking processed work, and eventually running as a multi-account cloud service.

## Current build

- Provider-independent Agent core
- Deterministic comment analysis
- OpenAI response generation
- Safe `dry_run` mode (default)
- SQLite processing store
- Persistent Playwright browser session for manual Instagram login
- Environment-based configuration template

## Architecture

```text
Instagram Browser / Future API Provider
                  |
                  v
          InstagramProvider
                  |
                  v
          InstagramAgent
            /          \
           v            v
    Comment Analyzer   AI Engine
           |            |
           +-----+------+
                 v
          Reply Executor
                 |
                 v
              SQLite
```

Instagram-specific browser behavior stays behind `InstagramProvider`, so the connector can change without rewriting the Agent core.

## Safety-first execution

`AGENT_DRY_RUN=true` is the default. Dry-run generates and logs proposed replies without sending them. Real sending will only be enabled explicitly after the real-account test workflow is validated.

## Local setup

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Install Playwright Chromium with `python -m playwright install chromium`.
4. Copy `.env.example` to `.env` and add the OpenAI API key.
5. Run the application entry point after the browser workflow is enabled.

Never commit API keys, passwords, browser sessions, cookies, or access tokens.

## Roadmap

1. Finish BrowserProvider post discovery.
2. Implement robust comment discovery and reply detection against the real test account.
3. Connect SQLite state to the Agent loop.
4. Add structured logs and error recovery.
5. Add dashboard and configuration management.
6. Add supported production Instagram integration where account permissions allow it.
7. Add multi-account and cloud worker architecture.
