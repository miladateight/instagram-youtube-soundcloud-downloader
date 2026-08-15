from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from downloader_bot.sender import TelegramSender
    from downloader_bot.downloader import DownloadedMedia, DownloadResult
    from downloader_bot.config import Settings
except ModuleNotFoundError as exc:  # pragma: no cover
    if exc.name != "yt_dlp" and exc.name != "aiogram":
        raise
    TelegramSender = None


def make_settings(max_upload_mb: int = 0) -> Settings:
    return Settings(
        bot_name="t",
        bot_token="t",
        admin_id=1,
        allow_all_users=False,
        max_upload_mb=max_upload_mb,
        playlist_limit=20,
        concurrent_downloads=4,
        download_dir=Path("downloads"),
        data_dir=Path("data"),
        log_dir=Path("logs"),
        cookies_file=None,
        enable_youtube=True,
        enable_instagram=True,
        enable_soundcloud=True,
        enable_song_detection=False,
        shazam_api_key=None,
        force_ipv4=False,
        support_username=None,
        bot_username=None,
        http_proxy=None,
    )


class SenderFallbackTests(unittest.TestCase):
    def setUp(self) -> None:
        if TelegramSender is None:
            self.skipTest("aiogram/yt-dlp not installed")

    def _make_media(self, directory: Path, kind: str, size: int = 10, width: int = 720, height: int = 1280, duration: float = 12.0) -> DownloadedMedia:
        suffix = {"video": ".mp4", "audio": ".mp3", "photo": ".jpg", "document": ".bin"}[kind]
        path = directory / f"item{suffix}"
        path.write_bytes(b"x" * size)
        thumb = None
        if kind in {"video", "audio"}:
            thumb_path = directory / "thumb.jpg"
            thumb_path.write_bytes(b"\xff\xd8\xff\xe0")
            thumb = thumb_path
        return DownloadedMedia(
            path=path,
            size=size,
            width=width if kind == "video" else None,
            height=height if kind == "video" else None,
            duration=duration if kind in {"video", "audio"} else None,
            thumbnail_path=thumb,
        )

    def test_oversized_video_falls_back_to_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            item = self._make_media(directory, "video", size=5)
            result = DownloadResult(
                title="t",
                caption=None,
                uploader=None,
                source_url="u",
                files=[item],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_video = AsyncMock(side_effect=Exception("file is too big"))
            bot.send_document = AsyncMock()
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(max_upload_mb=1), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            bot.send_video.assert_awaited_once()
            bot.send_document.assert_awaited_once()

    def test_size_limit_triggers_document_without_trying_video(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            item = self._make_media(directory, "video", size=2 * 1024 * 1024)
            result = DownloadResult(
                title="t",
                caption=None,
                uploader=None,
                source_url="u",
                files=[item],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_video = AsyncMock()
            bot.send_document = AsyncMock()
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(max_upload_mb=1), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            bot.send_video.assert_not_awaited()
            bot.send_document.assert_awaited_once()

    def test_video_send_passes_width_height_duration_thumbnail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            item = self._make_media(directory, "video")
            result = DownloadResult(
                title="t",
                caption=None,
                uploader=None,
                source_url="u",
                files=[item],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_video = AsyncMock()
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            kwargs = bot.send_video.await_args.kwargs
            self.assertEqual(kwargs["width"], 720)
            self.assertEqual(kwargs["height"], 1280)
            self.assertEqual(kwargs["duration"], 12)
            self.assertTrue(kwargs["supports_streaming"])
            self.assertIsNotNone(kwargs["thumbnail"])

    def test_audio_send_includes_thumbnail_and_duration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            item = self._make_media(directory, "audio")
            result = DownloadResult(
                title="Song",
                caption=None,
                uploader="Artist",
                source_url="u",
                files=[item],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_audio = AsyncMock()
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            kwargs = bot.send_audio.await_args.kwargs
            self.assertEqual(kwargs["duration"], 12)
            self.assertIsNotNone(kwargs["thumbnail"])
            self.assertEqual(kwargs["performer"], "Artist")
            self.assertEqual(kwargs["title"], "Song")

    def test_soundcloud_bundle_sends_photo_before_audio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            photo = self._make_media(directory, "photo", size=8)
            audio = self._make_media(directory, "audio", size=20)
            result = DownloadResult(
                title="Track",
                caption=None,
                uploader="Artist",
                source_url="u",
                files=[photo, audio],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_photo = AsyncMock()
            bot.send_audio = AsyncMock()
            bot.send_message = AsyncMock()
            bot.send_document = AsyncMock()

            sender = TelegramSender(bot, make_settings(), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            self.assertGreaterEqual(bot.send_photo.await_count, 1)
            self.assertGreaterEqual(bot.send_audio.await_count, 1)
            self.assertEqual(bot.send_document.await_count, 0)

    def test_soundcloud_thumbnail_is_sent_as_separate_cover(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            audio = self._make_media(directory, "audio", size=20)
            result = DownloadResult(
                title="Track",
                caption=None,
                uploader="Artist",
                source_url="https://soundcloud.com/artist/track",
                files=[audio],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_photo = AsyncMock()
            bot.send_audio = AsyncMock()
            bot.send_message = AsyncMock()
            bot.send_document = AsyncMock()

            sender = TelegramSender(bot, make_settings(), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            bot.send_photo.assert_awaited_once()
            bot.send_audio.assert_awaited_once()

    def test_document_failure_is_reported_to_caller(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            item = self._make_media(directory, "video")
            result = DownloadResult(
                title="t",
                caption=None,
                uploader=None,
                source_url="u",
                files=[item],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_video = AsyncMock(side_effect=Exception("video rejected"))
            bot.send_document = AsyncMock(side_effect=Exception("document rejected"))
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(), None)
            with self.assertRaisesRegex(Exception, "document rejected"):
                asyncio.run(sender.send_result(1, result, "en", "id"))

    def test_soundcloud_bundle_falls_back_to_document_for_oversized_audio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            photo = self._make_media(directory, "photo", size=8)
            audio = self._make_media(directory, "audio", size=2 * 1024 * 1024)
            result = DownloadResult(
                title="Track",
                caption=None,
                uploader="Artist",
                source_url="u",
                files=[photo, audio],
                workdir=directory,
            )
            bot = MagicMock()
            bot.send_photo = AsyncMock()
            bot.send_audio = AsyncMock()
            bot.send_document = AsyncMock()
            bot.send_message = AsyncMock()

            sender = TelegramSender(bot, make_settings(max_upload_mb=1), None)
            asyncio.run(sender.send_result(1, result, "en", "id"))

            bot.send_photo.assert_awaited()
            bot.send_audio.assert_not_awaited()
            bot.send_document.assert_awaited()


if __name__ == "__main__":
    unittest.main()
