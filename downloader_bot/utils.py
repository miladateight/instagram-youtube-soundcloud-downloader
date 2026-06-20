from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse


URL_RE = re.compile(
    r"(?:(?:https?://)?(?:www\.)?"
    r"(?:youtube\.com|youtu\.be|instagram\.com|instagr\.am|soundcloud\.com|on\.soundcloud\.com)"
    r"/[^\s<>()\"']+)",
    re.IGNORECASE,
)

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".ogg", ".opus", ".wav", ".flac"}

SUPPORTED_PLATFORMS = {
    "youtube": ("youtube.com", "youtu.be"),
    "instagram": ("instagram.com", "instagr.am"),
    "soundcloud": ("soundcloud.com", "on.soundcloud.com"),
}


def extract_urls(text: str) -> list[str]:
    urls = []
    for match in URL_RE.findall(text or ""):
        cleaned = match.rstrip(".,;!؟،)")
        if not cleaned.lower().startswith(("http://", "https://")):
            cleaned = "https://" + cleaned
        if cleaned not in urls:
            urls.append(cleaned)
    return urls


def detect_platform(url: str) -> str | None:
    host = urlparse(url).netloc.lower().replace("www.", "")
    for platform, domains in SUPPORTED_PLATFORMS.items():
        if any(host == domain or host.endswith("." + domain) for domain in domains):
            return platform
    return None


def platform_label(platform: str | None) -> str:
    labels = {
        "youtube": "YouTube",
        "instagram": "Instagram",
        "soundcloud": "SoundCloud",
    }
    return labels.get(platform or "", "Unknown")


def short_url_label(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/")
    if len(path) > 42:
        path = path[:39] + "..."
    return f"{host}/{path}" if path else host


def truncate_caption(text: str | None, limit: int = 1024) -> str | None:
    if not text:
        return None
    normalized = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in PHOTO_EXTENSIONS:
        return "photo"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    return "document"


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def looks_like_cookies_file(path: Path) -> bool:
    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    except OSError:
        return False

    if "Netscape HTTP Cookie File" in sample:
        return True

    for line in sample.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if len(stripped.split("\t")) >= 7:
            return True
    return False
