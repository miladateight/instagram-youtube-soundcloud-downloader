from __future__ import annotations

import asyncio
import logging
import shutil
import subprocess
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import Settings
from .downloader import Downloader, DownloadResult


@dataclass(frozen=True)
class SongInfo:
    title: str | None
    artist: str | None
    album: str | None
    cover_url: str | None
    spotify_url: str | None
    apple_url: str | None
    shazam_url: str | None
    raw: dict[str, Any]


class SongRecognizer:
    """Recognize songs in videos using Shazam (via shazamio library)."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.downloader = Downloader(settings)

    async def recognize(
        self,
        url: str,
        cookies_file: Path | None = None,
    ) -> tuple[SongInfo | None, DownloadResult | None]:
        """Download audio from url, recognize song with Shazam.

        Returns (SongInfo or None if not recognized, DownloadResult of the audio).
        The DownloadResult is returned so the caller can fall back to sending
        the MP3 if recognition fails.
        """
        try:
            result = await self.downloader.download(url, cookies_file, audio_only=True)
        except Exception as exc:
            logging.exception("Audio download for song detection failed: %s", exc)
            raise

        if not result.files:
            return None, result

        snippet = await self._extract_snippet(result)
        if snippet is None:
            logging.warning("Could not extract snippet for Shazam, using full audio")
            audio_path = result.files[0].path
        else:
            audio_path = snippet

        if not audio_path or not audio_path.exists():
            return None, result

        try:
            info = await self._shazam_recognize(audio_path)
        except Exception as exc:
            logging.exception("Shazam recognition failed: %s", exc)
            return None, result
        finally:
            if snippet is not None and snippet != (result.files[0].path if result.files else None):
                with suppress(Exception):
                    snippet.unlink()

        return info, result

    async def _extract_snippet(self, result: DownloadResult) -> Path | None:
        """Extract a 15-second snippet from the middle of the audio using ffmpeg."""
        if not result.files:
            return None
        source = result.files[0].path
        duration = result.files[0].duration

        if not shutil.which("ffmpeg"):
            return None

        start = max(0.0, (duration or 60.0) / 2 - 7.5) if duration else 0.0
        snippet_path = source.with_suffix(".snippet.mp3")

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", f"{start:.2f}",
            "-i", str(source),
            "-t", "15",
            "-vn",
            "-ac", "1",
            "-ar", "16000",
            "-b:a", "64k",
            str(snippet_path),
        ]
        try:
            proc = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, timeout=30
            )
            if proc.returncode != 0 or not snippet_path.exists():
                logging.warning("ffmpeg snippet extraction failed: %s", proc.stderr[:200] if proc.stderr else "")
                return None
            return snippet_path
        except Exception as exc:
            logging.warning("ffmpeg snippet extraction error: %s", exc)
            return None

    async def _shazam_recognize(self, audio_path: Path) -> SongInfo | None:
        try:
            from shazamio import Shazam
        except ModuleNotFoundError:
            logging.warning("shazamio not installed, song detection unavailable")
            return None

        shazam = Shazam()
        data = await asyncio.to_thread(lambda: audio_path.read_bytes())
        raw = await shazam.recognize(data)
        return self._parse_shazam_result(raw)

    @staticmethod
    def _parse_shazam_result(raw: dict[str, Any]) -> SongInfo | None:
        if not isinstance(raw, dict):
            return None

        track = raw.get("track")
        if not isinstance(track, dict):
            return None

        title = track.get("title") or None
        subtitle = track.get("subtitle") or None

        album = None
        sections = track.get("sections") or []
        for section in sections:
            if not isinstance(section, dict):
                continue
            if section.get("type") == "SONG":
                for meta in section.get("metadata") or []:
                    if isinstance(meta, dict) and meta.get("title") == "Album":
                        album = meta.get("text")
                        break

        cover_url = None
        images = track.get("images") or {}
        if isinstance(images, dict):
            cover_url = images.get("coverarthumbnail") or images.get("coverart")

        spotify_url = None
        apple_url = None
        shazam_url = None
        share = track.get("share") or {}
        if isinstance(share, dict):
            shazam_url = share.get("href") or share.get("subject")

        for section in sections:
            if not isinstance(section, dict):
                continue
            for link in section.get("youtubeactions") or []:
                if isinstance(link, dict) and "spotify" in (link.get("uri", "") or "").lower():
                    spotify_url = link.get("uri")
            share_section = section.get("share") or {}
            if isinstance(share_section, dict):
                if "spotify" in (share_section.get("provider", "") or "").lower():
                    spotify_url = spotify_url or share_section.get("href")
                if "apple" in (share_section.get("provider", "") or "").lower():
                    apple_url = share_section.get("href")

        if not title and not subtitle:
            return None

        return SongInfo(
            title=title,
            artist=subtitle,
            album=album,
            cover_url=cover_url,
            spotify_url=spotify_url,
            apple_url=apple_url,
            shazam_url=shazam_url,
            raw=raw,
        )