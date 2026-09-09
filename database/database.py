from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def connect() -> sqlite3.Connection:
    """Return a local SQLite connection for the first development phase."""
    url = os.getenv("DATABASE_URL", "sqlite:///runtime/instagram_ag.db")
    if not url.startswith("sqlite:///"):
        raise ValueError("Initial version supports SQLite DATABASE_URL only")

    path = Path(url.removeprefix("sqlite:///"))
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS processed_comments (
                comment_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                username TEXT NOT NULL,
                text TEXT NOT NULL,
                reply_text TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_processed_comments_post
            ON processed_comments(post_id);
            """
        )
