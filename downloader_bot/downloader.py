from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from .config import Settings


@dataclass(frozen=True)
class DownloadedMedia:
    path: Path
    size: int


@dataclass(frozen=True)
class DownloadResult:
    title: str
    caption: str | None
    uploader: str | None
    source_url: str
    files: list[DownloadedMedia]
    workdir: Path


class Downloader:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.download_dir.mkdir(parents=True, exist_ok=True)

    async def download(
        self,
        url: str,
        cookies_file: Path | None = None,
        *,
        audio_only: bool = False,
    ) -> DownloadResult:
        import asyncio

        return await asyncio.to_thread(self._download_sync, url, cookies_file, audio_only)

    def _download_sync(
        self,
        url: str,
        cookies_file: Path | None = None,
        audio_only: bool = False,
    ) -> DownloadResult:
        workdir = Path(tempfile.mkdtemp(prefix="job-", dir=self.settings.download_dir))
        try:
            options = self._build_options(
                workdir,
                cookies_file,
                self._should_write_thumbnail(url) and not audio_only,
                audio_only=audio_only,
            )
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)

            files = self._collect_files(workdir, info)
            if not files:
                raise RuntimeError("No downloadable media file was produced.")

            return DownloadResult(
                title=self._title_from_info(info),
                caption=self._caption_from_info(info),
                uploader=self._uploader_from_info(info),
                source_url=info.get("webpage_url") or url if isinstance(info, dict) else url,
                files=files,
                workdir=workdir,
            )
        except DownloadError as exc:
            self.cleanup(workdir)
            raise RuntimeError(str(exc)) from exc
        except Exception:
            self.cleanup(workdir)
            raise

    def _build_options(
        self,
        workdir: Path,
        cookies_file: Path | None,
        write_thumbnail: bool = False,
        audio_only: bool = False,
    ) -> dict[str, Any]:
        options: dict[str, Any] = {
            "paths": {"home": str(workdir)},
            "outtmpl": {
                "default": "%(title).120B.%(ext)s",
                "thumbnail": "%(title).120B.%(ext)s",
            },
            "format": "bestaudio/best"
            if audio_only
            else (
                "bv*[ext=mp4][vcodec^=avc1]+ba[ext=m4a]/"
                "b[ext=mp4][vcodec^=avc1]/"
                "bv*[ext=mp4]+ba[ext=m4a]/"
                "best[ext=mp4]/best"
            ),
            "merge_output_format": "mp4",
            "writethumbnail": write_thumbnail,
            "noplaylist": False,
            "playlistend": self.settings.playlist_limit,
            "ignoreerrors": False,
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True,
            "retries": 3,
            "fragment_retries": 3,
            "concurrent_fragment_downloads": 4,
        }
        if audio_only:
            options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]

        if cookies_file and cookies_file.exists():
            options["cookiefile"] = str(cookies_file)

        return options

    @staticmethod
    def _should_write_thumbnail(url: str) -> bool:
        lowered = url.lower()
        return "soundcloud.com" in lowered or "on.soundcloud.com" in lowered

    @staticmethod
    def _collect_files(workdir: Path, info: Any) -> list[DownloadedMedia]:
        ignored_suffixes = {".part", ".ytdl", ".temp", ".tmp", ".json"}
        ordered_paths = Downloader._paths_from_info(info)
        seen: set[Path] = set()
        files = []

        for path in ordered_paths:
            resolved = path if path.is_absolute() else workdir / path
            if resolved.is_file() and resolved.suffix.lower() not in ignored_suffixes:
                seen.add(resolved.resolve())
                files.append(DownloadedMedia(path=resolved, size=resolved.stat().st_size))

        for path in sorted(workdir.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() in ignored_suffixes:
                continue
            if path.resolve() in seen:
                continue
            files.append(DownloadedMedia(path=path, size=path.stat().st_size))
        return files

    @staticmethod
    def _paths_from_info(info: Any) -> list[Path]:
        paths: list[Path] = []

        def visit(item: Any) -> None:
            if not isinstance(item, dict):
                return
            for download in item.get("requested_downloads") or []:
                if isinstance(download, dict):
                    value = download.get("filepath") or download.get("_filename")
                    if value:
                        paths.append(Path(str(value)))
            value = item.get("filepath") or item.get("_filename")
            if value:
                paths.append(Path(str(value)))
            for entry in item.get("entries") or []:
                visit(entry)

        visit(info)
        deduped = []
        seen = set()
        for path in paths:
            key = str(path)
            if key not in seen:
                seen.add(key)
                deduped.append(path)
        return deduped

    @staticmethod
    def _title_from_info(info: Any) -> str:
        if isinstance(info, dict):
            return str(info.get("title") or info.get("fulltitle") or "Downloaded media")
        return "Downloaded media"

    @staticmethod
    def _uploader_from_info(info: Any) -> str | None:
        if not isinstance(info, dict):
            return None
        value = info.get("uploader") or info.get("channel") or info.get("artist") or info.get("creator")
        if value:
            return str(value)
        entries = info.get("entries")
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict):
                    entry_value = (
                        entry.get("uploader")
                        or entry.get("channel")
                        or entry.get("artist")
                        or entry.get("creator")
                    )
                    if entry_value:
                        return str(entry_value)
        return None

    @staticmethod
    def _caption_from_info(info: Any) -> str | None:
        if not isinstance(info, dict):
            return None
        description = info.get("description")
        if description:
            return str(description)
        entries = info.get("entries")
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and entry.get("description"):
                    return str(entry["description"])
        return str(info.get("title")) if info.get("title") else None

    @staticmethod
    def cleanup(path: Path) -> None:
        shutil.rmtree(path, ignore_errors=True)
