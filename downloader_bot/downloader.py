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
    width: int | None = None
    height: int | None = None
    duration: float | None = None
    thumbnail_path: Path | None = None


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
        progress_callback: Any = None,
    ) -> DownloadResult:
        import asyncio

        return await asyncio.to_thread(
            self._download_sync, url, cookies_file, audio_only, progress_callback
        )

    def _download_sync(
        self,
        url: str,
        cookies_file: Path | None = None,
        audio_only: bool = False,
        progress_callback: Any = None,
    ) -> DownloadResult:
        workdir = Path(tempfile.mkdtemp(prefix="job-", dir=self.settings.download_dir))
        try:
            platform = self._detect_platform(url)
            audio_format = self._audio_format_for(url, platform, audio_only)

            options = self._build_options(
                workdir,
                cookies_file,
                write_thumbnail=True,
                audio_only=audio_only,
                audio_format=audio_format,
                progress_callback=progress_callback,
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

    @staticmethod
    def _detect_platform(url: str) -> str | None:
        lowered = url.lower()
        if "soundcloud.com" in lowered or "on.soundcloud.com" in lowered:
            return "soundcloud"
        if "youtube.com" in lowered or "youtu.be" in lowered:
            return "youtube"
        if "instagram.com" in lowered or "instagr.am" in lowered:
            return "instagram"
        return None

    def _audio_format_for(
        self,
        url: str,
        platform: str | None,
        audio_only: bool,
    ) -> str | None:
        """Pick the audio format based on platform and duration.

        For SoundCloud: best quality if duration < 15min, else first available.
        Returns None to use the default audio format for other platforms.
        """
        if platform != "soundcloud" or not audio_only:
            return None

        duration = self._probe_duration(url)
        return self._soundcloud_format_by_duration(duration)

    @staticmethod
    def _soundcloud_format_by_duration(duration: float | None) -> str:
        if not duration or duration <= 900:
            return "bestaudio/best"
        return "worstaudio/best"

    def _probe_duration(self, url: str) -> float | None:
        probe_options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
        }
        try:
            with YoutubeDL(probe_options) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception:
            return None
        if isinstance(info, dict):
            value = info.get("duration")
            if value is not None:
                return float(value)
        return None

    def _build_options(
        self,
        workdir: Path,
        cookies_file: Path | None,
        write_thumbnail: bool = False,
        audio_only: bool = False,
        audio_format: str | None = None,
        progress_callback: Any = None,
    ) -> dict[str, Any]:
        if audio_format:
            audio_fmt = audio_format
        else:
            audio_fmt = "bestaudio/best"

        options: dict[str, Any] = {
            "paths": {"home": str(workdir)},
            "outtmpl": {
                "default": "%(title).120B.%(ext)s",
                "thumbnail": "%(title).120B.%(ext)s",
            },
            "format": audio_fmt
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
            "ignoreerrors": True,
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True,
            "retries": 3,
            "fragment_retries": 3,
            "concurrent_fragment_downloads": max(1, self.settings.concurrent_downloads),
            "sleep_interval": 2,
            "max_sleep_interval": 5,
            "sleep_interval_requests": 1,
            "max_filesize": self.settings.max_upload_bytes if self.settings.max_upload_mb > 0 else None,
        }
        if self.settings.force_ipv4:
            options["force_ipv4"] = True
        if self.settings.http_proxy:
            options["proxy"] = self.settings.http_proxy
        if progress_callback is not None:
            options["progress_hooks"] = [progress_callback]
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
    def _collect_files(workdir: Path, info: Any) -> list[DownloadedMedia]:
        ignored_suffixes = {".part", ".ytdl", ".temp", ".tmp", ".json"}
        photo_suffixes = {".jpg", ".jpeg", ".png", ".webp"}

        ordered = Downloader._paths_from_info(info)
        seen: set[Path] = set()
        files: list[DownloadedMedia] = []

        for path in ordered:
            resolved = path if path.is_absolute() else workdir / path
            if not resolved.is_file():
                continue
            if resolved.suffix.lower() in ignored_suffixes:
                continue
            key = resolved.resolve()
            if key in seen:
                continue
            seen.add(key)

            meta = Downloader._meta_for_path(info, resolved)
            if resolved.suffix.lower() in photo_suffixes and meta.thumbnail_path is None:
                meta = meta._replace(thumbnail_path=resolved)

            files.append(
                DownloadedMedia(
                    path=resolved,
                    size=resolved.stat().st_size,
                    width=meta.width,
                    height=meta.height,
                    duration=meta.duration,
                    thumbnail_path=meta.thumbnail_path,
                )
            )

        for path in sorted(workdir.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() in ignored_suffixes:
                continue
            if path.suffix.lower() in photo_suffixes:
                continue
            if path.resolve() in seen:
                continue
            files.append(DownloadedMedia(path=path, size=path.stat().st_size))
        return files

    @staticmethod
    def _meta_for_path(info: Any, path: Path) -> DownloadedMedia:
        width: int | None = None
        height: int | None = None
        duration: float | None = None
        thumbnail_path: Path | None = None
        target = path.resolve()

        def visit(item: Any) -> None:
            nonlocal width, height, duration
            if not isinstance(item, dict):
                return
            for download in item.get("requested_downloads") or []:
                if not isinstance(download, dict):
                    continue
                fp = download.get("filepath") or download.get("_filename")
                if fp and Path(str(fp)).resolve() == target:
                    if width is None and download.get("width"):
                        width = int(download["width"])
                    if height is None and download.get("height"):
                        height = int(download["height"])
                    if duration is None and download.get("duration"):
                        duration = float(download["duration"])
            fp = item.get("filepath") or item.get("_filename")
            if fp and Path(str(fp)).resolve() == target:
                if width is None and item.get("width"):
                    width = int(item["width"])
                if height is None and item.get("height"):
                    height = int(item["height"])
                if duration is None and item.get("duration"):
                    duration = float(item["duration"])
            for entry in item.get("entries") or []:
                visit(entry)

        visit(info)

        stem = path.stem
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            candidate = path.with_suffix(ext)
            if candidate.exists() and candidate != path:
                thumbnail_path = candidate
                break
            sibling = path.parent / f"{stem}{ext}"
            if sibling.exists() and sibling != path:
                thumbnail_path = sibling
                break

        return DownloadedMedia(
            path=path,
            size=0,
            width=width,
            height=height,
            duration=duration,
            thumbnail_path=thumbnail_path,
        )

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
