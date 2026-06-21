from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    bot_name: str
    bot_token: str
    admin_id: int
    allow_all_users: bool
    max_upload_mb: int
    playlist_limit: int
    concurrent_downloads: int
    download_dir: Path
    data_dir: Path
    log_dir: Path
    cookies_file: Path | None

    @property
    def max_upload_bytes(self) -> int:
        if self.max_upload_mb <= 0:
            return sys.maxsize
        return self.max_upload_mb * 1024 * 1024


def load_settings() -> Settings:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing. Run install.py or create a .env file.")

    admin_id = _int_env("ADMIN_ID", 0)
    if admin_id <= 0:
        raise RuntimeError("ADMIN_ID must be a positive numeric Telegram user id.")

    cookies_value = os.getenv("COOKIES_FILE", "").strip()
    cookies_file = Path(cookies_value).expanduser() if cookies_value else None

    return Settings(
        bot_name=os.getenv("BOT_NAME", "DownloaderBot").strip() or "DownloaderBot",
        bot_token=bot_token,
        admin_id=admin_id,
        allow_all_users=_bool_env("ALLOW_ALL_USERS", False),
        max_upload_mb=_int_env("MAX_UPLOAD_MB", 0),
        playlist_limit=max(1, _int_env("PLAYLIST_LIMIT", 20)),
        concurrent_downloads=max(1, _int_env("CONCURRENT_DOWNLOADS", 1)),
        download_dir=Path(os.getenv("DOWNLOAD_DIR", "downloads")).expanduser(),
        data_dir=Path(os.getenv("DATA_DIR", "data")).expanduser(),
        log_dir=Path(os.getenv("LOG_DIR", "logs")).expanduser(),
        cookies_file=cookies_file,
    )
