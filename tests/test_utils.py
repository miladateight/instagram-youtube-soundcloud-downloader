from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.utils import detect_platform, extract_urls, looks_like_cookies_file


class UrlDetectionTests(unittest.TestCase):
    def test_extracts_supported_urls_with_and_without_scheme(self) -> None:
        urls = extract_urls(
            "instagram.com/p/abc https://youtu.be/xyz https://on.soundcloud.com/demo"
        )

        self.assertEqual(
            urls,
            [
                "https://instagram.com/p/abc",
                "https://youtu.be/xyz",
                "https://on.soundcloud.com/demo",
            ],
        )

    def test_detects_platforms(self) -> None:
        self.assertEqual(detect_platform("https://youtube.com/shorts/abc"), "youtube")
        self.assertEqual(detect_platform("https://www.instagram.com/reel/abc"), "instagram")
        self.assertEqual(detect_platform("https://soundcloud.com/artist/track"), "soundcloud")
        self.assertIsNone(detect_platform("https://example.com/video"))


class CookiesTests(unittest.TestCase):
    def test_accepts_netscape_cookie_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cookies.txt"
            path.write_text(
                "# Netscape HTTP Cookie File\n"
                ".instagram.com\tTRUE\t/\tTRUE\t2147483647\tsessionid\tvalue\n",
                encoding="utf-8",
            )

            self.assertTrue(looks_like_cookies_file(path))

    def test_rejects_plain_text_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            path.write_text("hello world", encoding="utf-8")

            self.assertFalse(looks_like_cookies_file(path))


if __name__ == "__main__":
    unittest.main()
