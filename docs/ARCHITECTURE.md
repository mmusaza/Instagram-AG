# Architecture v1

## Core principle

Instagram connectivity is an adapter, not the Agent itself.

```text
+---------------------+
| Instagram Provider  |
| Browser / API / ... |
+----------+----------+
           |
           v
+---------------------+
| Comment / Post Flow |
+----------+----------+
           |
           v
+---------------------+      +------------------+
| Decision / Rules    | ---> | Database/Memory  |
+----------+----------+      +------------------+
           |
           v
+---------------------+
| AI Response Engine  |
+----------+----------+
           |
           v
+---------------------+
| Reply Executor      |
+---------------------+
```

## Why this design

The previous prototype mixed browser selectors, comment discovery, AI prompting, and reply submission in one script. That makes every Instagram UI change expensive to fix.

In v1, the Agent core only knows about `InstagramProvider` methods:

- `list_posts()`
- `list_comments(post)`
- `reply_to_comment(comment, text)`

A future provider can implement the same contract without changing the decision engine or AI layer.

## Provider strategy

1. **Development provider:** browser automation can be used while we validate the workflow.
2. **Production provider:** use an appropriate supported/official integration when available for the required account and permissions.
3. **Fallback:** keep browser-specific code isolated so it can be replaced without touching core logic.

## Safety defaults

Automatic reply is disabled by default in configuration. The first end-to-end tests should support dry-run mode, logging the intended reply before enabling actual sending.

## Data model direction

The initial SQLite table only tracks processed comments. The production model will expand to accounts, posts, comments, replies, agent runs, errors, and configuration.
