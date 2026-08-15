from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys
from subprocess import CompletedProcess
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from downloader_bot.config import Settings
    from downloader_bot.downloader import DownloadedMedia, Downloader
except ModuleNotFoundError as exc:  # pragma: no cover - depends on local test env
    if exc.name != "yt_dlp":
        raise
    Downloader = None


def make_settings(directory: Path) -> Settings:
    return Settings(
        bot_name="test",
        bot_token="test",
        admin_id=1,
        allow_all_users=False,
        max_upload_mb=50,
        playlist_limit=5,
        concurrent_downloads=1,
        download_dir=directory / "downloads",
        data_dir=directory / "data",
        log_dir=directory / "logs",
        cookies_file=None,
        enable_youtube=True,
        enable_instagram=True,
        enable_soundcloud=True,
        enable_song_detection=True,
        shazam_api_key=None,
        force_ipv4=False,
        support_username=None,
        bot_username=None,
        http_proxy=None,
    )


class DownloaderMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        if Downloader is None:
            self.skipTest("yt-dlp is not installed in this local test environment")

    def test_meta_for_path_extracts_dimensions_and_thumbnail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / "video.mp4"
            video.write_bytes(b"\x00\x00\x00\x20mp4")
            thumb = Path(directory) / "video.jpg"
            thumb.write_bytes(b"\xff\xd8\xff\xe0")

            info = {
                "requested_downloads": [
                    {
                        "filepath": str(video),
                        "width": 1080,
                        "height": 1920,
                        "duration": 30.5,
                    }
                ],
            }
            meta = Downloader._meta_for_path(info, video)
            self.assertEqual(meta.width, 1080)
            self.assertEqual(meta.height, 1920)
            self.assertEqual(meta.duration, 30.5)
            self.assertIsNotNone(meta.thumbnail_path)

    def test_extracts_uploader_from_single_or_playlist_info(self) -> None:
        self.assertEqual(Downloader._uploader_from_info({"artist": "Artist Name"}), "Artist Name")
        self.assertEqual(
            Downloader._uploader_from_info({"entries": [{"channel": "Channel Name"}]}),
            "Channel Name",
        )
        self.assertIsNone(Downloader._uploader_from_info({}))

    def test_collect_files_attaches_metadata_to_video(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / "reel.mp4"
            video.write_bytes(b"\x00\x00\x00\x20mp4")
            thumb = Path(directory) / "reel.jpg"
            thumb.write_bytes(b"\xff\xd8\xff\xe0")

            info = {
                "requested_downloads": [
                    {
                        "filepath": str(video),
                        "width": 607,
                        "height": 1080,
                        "duration": 15.0,
                    }
                ],
            }
            files = Downloader._collect_files(Path(directory), info)
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].path, video)
            self.assertEqual(files[0].width, 607)
            self.assertEqual(files[0].height, 1080)
            self.assertEqual(files[0].duration, 15.0)
            self.assertEqual(files[0].thumbnail_path, thumb)

    def test_collect_files_skips_temp_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ok = Path(directory) / "audio.mp3"
            ok.write_bytes(b"ID3")
            for name in ("clip.part", "info.json", "clip.ytdl"):
                (Path(directory) / name).write_bytes(b"x")
            files = Downloader._collect_files(Path(directory), {})
            paths = [f.path for f in files]
            self.assertIn(ok, paths)
            self.assertNotIn(Path(directory) / "clip.part", paths)
            self.assertNotIn(Path(directory) / "info.json", paths)

    def test_collect_files_carousel_returns_each_item_with_meta(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            v1 = Path(directory) / "v1.mp4"
            v1.write_bytes(b"\x00\x00\x00\x20mp4")
            v2 = Path(directory) / "v2.mp4"
            v2.write_bytes(b"\x00\x00\x00\x20mp4")

            info = {
                "entries": [
                    {"requested_downloads": [{"filepath": str(v1), "width": 720, "height": 1280, "duration": 12.0}]},
                    {"requested_downloads": [{"filepath": str(v2), "width": 720, "height": 1280, "duration": 8.0}]},
                ]
            }
            files = Downloader._collect_files(Path(directory), info)
            self.assertEqual(len(files), 2)
            widths = {f.width for f in files}
            self.assertEqual(widths, {720})

    def test_collect_files_accepts_an_actual_photo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            photo = Path(directory) / "post.jpg"
            photo.write_bytes(b"\xff\xd8\xff\xe0")
            info = {"requested_downloads": [{"filepath": str(photo)}]}

            files = Downloader._collect_files(Path(directory), info)

            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].path, photo)
            self.assertEqual(files[0].thumbnail_path, photo)

    def test_instagram_gallery_fallback_collects_photos(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloader = Downloader(make_settings(root))
            workdir = root / "job"
            gallery_dir = workdir / "instagram" / "instagram" / "account"
            gallery_dir.mkdir(parents=True)
            photo = gallery_dir / "post.jpg"
            photo.write_bytes(b"\xff\xd8\xff\xe0")

            with patch(
                "downloader_bot.downloader.subprocess.run",
                return_value=CompletedProcess([], 0, stdout="", stderr=""),
            ):
                files = downloader._download_instagram_gallery(
                    "https://www.instagram.com/p/example/",
                    workdir,
                    None,
                )

            self.assertEqual([item.path for item in files], [photo])

    def test_compatible_youtube_formats_prefer_progressive_mp4(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloader = Downloader(make_settings(root))

            video = downloader._build_options(
                root,
                None,
                compatible_formats=True,
                youtube_client="android_vr",
            )
            audio = downloader._build_options(
                root,
                None,
                audio_only=True,
                compatible_formats=True,
            )

            self.assertTrue(video["format"].startswith("b[ext=mp4]"))
            self.assertEqual(
                video["extractor_args"]["youtube"]["player_client"],
                ["android_vr"],
            )
            self.assertIn("abr<=192", audio["format"])

    def test_visual_request_rejects_orphan_audio_stream(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "orphan.m4a"
            audio.write_bytes(b"audio")
            video = Path(directory) / "video.mp4"
            video.write_bytes(b"video")

            self.assertFalse(
                Downloader._has_visual_media(
                    [DownloadedMedia(path=audio, size=audio.stat().st_size)]
                )
            )
            self.assertTrue(
                Downloader._has_visual_media(
                    [DownloadedMedia(path=video, size=video.stat().st_size)]
                )
            )


    def test_soundcloud_format_short_track_picks_best_quality(self) -> None:
        self.assertEqual(Downloader._soundcloud_format_by_duration(120.0), "bestaudio/best")

    def test_soundcloud_format_long_track_picks_worst_quality(self) -> None:
        self.assertEqual(Downloader._soundcloud_format_by_duration(1800.0), "worstaudio/best")

    def test_soundcloud_format_unknown_duration_picks_best_quality(self) -> None:
        self.assertEqual(Downloader._soundcloud_format_by_duration(None), "bestaudio/best")
        self.assertEqual(Downloader._soundcloud_format_by_duration(0), "bestaudio/best")

    def test_soundcloud_format_boundary_at_15_minutes(self) -> None:
        self.assertEqual(Downloader._soundcloud_format_by_duration(900.0), "bestaudio/best")
        self.assertEqual(Downloader._soundcloud_format_by_duration(901.0), "worstaudio/best")

    def test_detect_platform_identifies_supported_hosts(self) -> None:
        self.assertEqual(Downloader._detect_platform("https://soundcloud.com/artist/track"), "soundcloud")
        self.assertEqual(Downloader._detect_platform("https://on.soundcloud.com/abc"), "soundcloud")
        self.assertEqual(Downloader._detect_platform("https://youtube.com/watch?v=abc"), "youtube")
        self.assertEqual(Downloader._detect_platform("https://youtu.be/abc"), "youtube")
        self.assertEqual(Downloader._detect_platform("https://instagram.com/reel/abc"), "instagram")
        self.assertIsNone(Downloader._detect_platform("https://example.com/video"))


if __name__ == "__main__":
    unittest.main()
