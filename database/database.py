from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: str = "data/instagram_ag.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_comments (
                comment_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                username TEXT NOT NULL,
                comment_text TEXT NOT NULL,
                reply_text TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def seen(self, comment_id: str) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM processed_comments WHERE comment_id = ? LIMIT 1", (comment_id,)
        ).fetchone()
        return row is not None

    def record(self, comment_id: str, post_id: str, username: str, comment_text: str, reply_text: str | None, status: str) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO processed_comments
            (comment_id, post_id, username, comment_text, reply_text, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (comment_id, post_id, username, comment_text, reply_text, status),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
