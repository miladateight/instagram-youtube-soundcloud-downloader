from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from downloader_bot.downloader import Downloader
except ModuleNotFoundError as exc:  # pragma: no cover - depends on local test env
    if exc.name != "yt_dlp":
        raise
    Downloader = None


class DownloaderMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        if Downloader is None:
            self.skipTest("yt-dlp is not installed in this local test environment")

    def test_soundcloud_links_enable_thumbnail_downloads(self) -> None:
        self.assertTrue(Downloader._should_write_thumbnail("https://soundcloud.com/artist/track"))
        self.assertTrue(Downloader._should_write_thumbnail("https://on.soundcloud.com/demo"))
        self.assertFalse(Downloader._should_write_thumbnail("https://youtube.com/watch?v=abc"))

    def test_extracts_uploader_from_single_or_playlist_info(self) -> None:
        self.assertEqual(Downloader._uploader_from_info({"artist": "Artist Name"}), "Artist Name")
        self.assertEqual(
            Downloader._uploader_from_info({"entries": [{"channel": "Channel Name"}]}),
            "Channel Name",
        )
        self.assertIsNone(Downloader._uploader_from_info({}))


if __name__ == "__main__":
    unittest.main()
