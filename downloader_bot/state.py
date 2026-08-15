from __future__ import annotations

import time
import sqlite3
import secrets
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


PENDING_LINK_TTL_SECONDS = 5 * 60


class BotState:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def close(self) -> None:
        """Kept for callers; database connections are closed per operation."""

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS bot_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "INSERT OR IGNORE INTO bot_state(key, value) VALUES('active', 'false')"
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pending_links (
                    token TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )

    def get(self, key: str, default: str | None = None) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT value FROM bot_state WHERE key = ?",
                (key,),
            ).fetchone()
        return str(row[0]) if row else default

    def set(self, key: str, value: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO bot_state(key, value)
                VALUES(?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )

    def delete(self, key: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM bot_state WHERE key = ?", (key,))

    def is_active(self) -> bool:
        return self.get("active", "false") == "true"

    def set_active(self, active: bool) -> None:
        self.set("active", "true" if active else "false")

    def public_access(self, default: bool = False) -> bool:
        fallback = "true" if default else "false"
        return self.get("public_access", fallback) == "true"

    def set_public_access(self, enabled: bool) -> None:
        self.set("public_access", "true" if enabled else "false")

    def cookies_path(self) -> Path | None:
        value = self.get("cookies_file")
        return Path(value).expanduser() if value else None

    def set_cookies_path(self, path: Path) -> None:
        self.set("cookies_file", str(path))

    def clear_cookies_path(self) -> None:
        self.delete("cookies_file")

    def has_user_language(self, user_id: int) -> bool:
        return self.get(f"user_language:{user_id}") is not None

    def user_language(self, user_id: int, default: str = "fa") -> str:
        return self.get(f"user_language:{user_id}", default) or default

    def set_user_language(self, user_id: int, language: str) -> None:
        self.set(f"user_language:{user_id}", language)

    def user_cookies_path(self, user_id: int) -> Path | None:
        value = self.get(f"user_cookies_file:{user_id}")
        return Path(value).expanduser() if value else None

    def set_user_cookies_path(self, user_id: int, path: Path) -> None:
        self.set(f"user_cookies_file:{user_id}", str(path))

    def clear_user_cookies_path(self, user_id: int) -> None:
        self.delete(f"user_cookies_file:{user_id}")

    def save_caption(self, caption_id: str, caption: str) -> None:
        self.set(f"caption:{caption_id}", caption)

    def caption(self, caption_id: str) -> str | None:
        return self.get(f"caption:{caption_id}")

    def is_force_join_enabled(self) -> bool:
        return self.get("force_join_enabled", "false") == "true"

    def set_force_join_enabled(self, enabled: bool) -> None:
        self.set("force_join_enabled", "true" if enabled else "false")

    def force_join_chat(self) -> str | None:
        value = self.get("force_join_chat")
        return value.strip() if value and value.strip() else None

    def set_force_join_chat(self, chat: str) -> None:
        self.set("force_join_chat", chat.strip())

    def clear_force_join_chat(self) -> None:
        self.delete("force_join_chat")

    def save_pending_link(self, user_id: int, url: str, platform: str) -> str:
        token = secrets.token_urlsafe(9)
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM pending_links WHERE user_id = ? AND url = ?",
                (user_id, url),
            )
            connection.execute(
                """
                INSERT INTO pending_links(token, user_id, url, platform, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (token, user_id, url, platform, time.time()),
            )
        return token

    def get_pending_link(self, token: str, user_id: int) -> tuple[str, str] | None:
        self._purge_pending_links()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT url, platform FROM pending_links WHERE token = ? AND user_id = ?",
                (token, user_id),
            ).fetchone()
        return (str(row[0]), str(row[1])) if row else None

    def delete_pending_link(self, token: str, user_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM pending_links WHERE token = ? AND user_id = ?",
                (token, user_id),
            )

    def _purge_pending_links(self) -> None:
        cutoff = time.time() - PENDING_LINK_TTL_SECONDS
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM pending_links WHERE created_at < ?",
                (cutoff,),
            )
