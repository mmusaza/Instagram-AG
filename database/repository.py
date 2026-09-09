from __future__ import annotations

import sqlite3

from agent.instagram.provider import InstagramComment


class CommentRepository:
    """Small persistence layer used to prevent duplicate processing."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.db = connection

    def was_processed(self, comment_id: str) -> bool:
        row = self.db.execute(
            "SELECT 1 FROM processed_comments WHERE comment_id = ? LIMIT 1",
            (comment_id,),
        ).fetchone()
        return row is not None

    def record(
        self,
        comment: InstagramComment,
        reply_text: str | None,
        status: str,
    ) -> None:
        self.db.execute(
            """
            INSERT OR REPLACE INTO processed_comments
            (comment_id, post_id, username, text, reply_text, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                comment.id,
                comment.post_id,
                comment.username,
                comment.text,
                reply_text,
                status,
            ),
        )
        self.db.commit()
