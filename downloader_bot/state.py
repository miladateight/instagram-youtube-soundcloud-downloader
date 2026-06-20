from __future__ import annotations

import sqlite3
from pathlib import Path


class BotState:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

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

    def cookies_path(self) -> Path | None:
        value = self.get("cookies_file")
        return Path(value).expanduser() if value else None

    def set_cookies_path(self, path: Path) -> None:
        self.set("cookies_file", str(path))

    def clear_cookies_path(self) -> None:
        self.delete("cookies_file")
