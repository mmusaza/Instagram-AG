# Project Context

## Product vision

Instagram-AG is being developed as a reusable Instagram AI assistant rather than a one-off script. The target is a product that can eventually be deployed in the cloud and configured for multiple brands/accounts.

## Requirements gathered so far

- Manual Instagram login is acceptable during early browser-based testing.
- The agent should discover posts instead of requiring a manually entered post ID.
- It should inspect comments across posts.
- It should determine whether a page has already answered a comment.
- A commenter does not need to follow the page for the comment workflow to matter.
- AI should generate concise, friendly, professional Persian replies.
- The brand context can be configured rather than hard-coded into the entire system.
- Duplicate processing must be prevented once persistent storage is active.
- The system should eventually expose a dashboard, logs, memory, cloud workers, and multi-account support.

## Lessons from the prototype

The first Playwright scripts combined navigation, DOM selectors, comment detection, OpenAI calls, and reply submission. Instagram's UI/DOM is dynamic, so those selectors must be isolated inside a provider instead of becoming dependencies of the whole system.

## Current development order

1. Stable architecture and interfaces.
2. Deterministic comment filtering/decision layer.
3. AI response generation.
4. Persistent state and idempotency.
5. Browser provider for controlled end-to-end tests.
6. Dry-run tests.
7. Explicitly enabled reply execution.
8. Dashboard and cloud worker architecture.
9. Multi-account/product layer.

## Important security rule

Project documentation must never contain API keys, passwords, cookies, browser session files, or other secrets. Chat history is represented here as a sanitized project context, not as a raw private transcript.
