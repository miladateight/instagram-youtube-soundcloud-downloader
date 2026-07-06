from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from downloader_bot.downloader import Downloader
except ModuleNotFoundError as exc:  # pragma: no cover
    if exc.name != "yt_dlp":
        raise
    Downloader = None


class ProbeContentTests(unittest.TestCase):
    """Tests for probe_content logic (no network needed for static parts)."""

    def setUp(self) -> None:
        if Downloader is None:
            self.skipTest("yt-dlp is not installed")

    def test_probe_detects_single_video(self) -> None:
        info = {
            "ext": "mp4",
            "vcodec": "avc1.42001E",
            "duration": 120,
            "title": "Test Video",
            "uploader": "TestChannel",
        }
        result = Downloader._classify_probe_info(info, "youtube")
        self.assertTrue(result["has_video"])
        self.assertFalse(result["is_carousel"])
        self.assertEqual(result["photo_count"], 0)
        self.assertEqual(result["duration"], 120)
        self.assertEqual(result["title"], "Test Video")

    def test_probe_detects_carousel_with_photos(self) -> None:
        info = {
            "entries": [
                {"_type": "photo", "ext": "jpg"},
                {"_type": "photo", "ext": "jpg"},
                {"_type": "photo", "ext": "png"},
            ]
        }
        result = Downloader._classify_probe_info(info, "instagram")
        self.assertTrue(result["is_carousel"])
        self.assertEqual(result["photo_count"], 3)
        self.assertFalse(result["has_video"])

    def test_probe_detects_mixed_carousel(self) -> None:
        info = {
            "entries": [
                {"_type": "photo", "ext": "jpg"},
                {"ext": "mp4", "vcodec": "avc1.42001E"},
                {"_type": "photo", "ext": "jpg"},
            ]
        }
        result = Downloader._classify_probe_info(info, "instagram")
        self.assertTrue(result["is_carousel"])
        self.assertTrue(result["has_video"])
        self.assertEqual(result["photo_count"], 2)

    def test_probe_detects_audio_only(self) -> None:
        info = {
            "ext": "m4a",
            "vcodec": "none",
            "acodec": "mp4a.40.2",
            "duration": 200,
        }
        result = Downloader._classify_probe_info(info, "soundcloud")
        self.assertTrue(result["has_audio"])
        self.assertFalse(result["has_video"])

    def test_probe_handles_empty_info(self) -> None:
        result = Downloader._classify_probe_info({}, "youtube")
        self.assertFalse(result["is_carousel"])
        self.assertEqual(result["photo_count"], 0)
        self.assertTrue(result["has_video"])

    def test_probe_handles_non_dict_info(self) -> None:
        result = Downloader._classify_probe_info("not a dict", "youtube")
        self.assertFalse(result["is_carousel"])
        self.assertTrue(result["has_video"])


if __name__ == "__main__":
    unittest.main()