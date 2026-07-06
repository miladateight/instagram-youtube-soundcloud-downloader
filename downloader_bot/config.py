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
    enable_youtube: bool
    enable_instagram: bool
    enable_soundcloud: bool
    enable_song_detection: bool
    shazam_api_key: str | None
    force_ipv4: bool
    support_username: str | None
    bot_username: str | None
    http_proxy: str | None

    @property
    def max_upload_bytes(self) -> int:
        if self.max_upload_mb <= 0:
            return sys.maxsize
        return self.max_upload_mb * 1024 * 1024

    def support_url(self) -> str:
        if self.support_username:
            return f"https://t.me/{self.support_username.lstrip('@')}"
        return f"https://t.me/user?id={self.admin_id}"

    def share_url(self) -> str | None:
        if self.bot_username:
            return f"https://t.me/{self.bot_username.lstrip('@')}"
        return None

    def platform_enabled(self, platform: str | None) -> bool:
        if platform == "youtube":
            return self.enable_youtube
        if platform == "instagram":
            return self.enable_instagram
        if platform == "soundcloud":
            return self.enable_soundcloud
        return False


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
        enable_youtube=_bool_env("ENABLE_YOUTUBE", True),
        enable_instagram=_bool_env("ENABLE_INSTAGRAM", True),
        enable_soundcloud=_bool_env("ENABLE_SOUNDCLOUD", True),
        enable_song_detection=_bool_env("ENABLE_SONG_DETECTION", True),
        shazam_api_key=(os.getenv("SHAZAM_API_KEY", "").strip() or None),
        force_ipv4=_bool_env("FORCE_IPV4", False),
        support_username=(os.getenv("SUPPORT_USERNAME", "").strip().lstrip("@") or None),
        bot_username=(os.getenv("BOT_USERNAME", "").strip().lstrip("@") or None),
        http_proxy=(os.getenv("HTTP_PROXY", "").strip() or None),
    )
