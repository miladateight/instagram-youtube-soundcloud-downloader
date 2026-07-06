from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from downloader_bot.song_recognizer import SongRecognizer, SongInfo
except ModuleNotFoundError as exc:  # pragma: no cover
    if exc.name not in {"yt_dlp", "aiogram", "shazamio"}:
        raise
    SongRecognizer = None


class SongRecognizerParseTests(unittest.TestCase):
    """Tests for the Shazam result parser (no network needed)."""

    def setUp(self) -> None:
        if SongRecognizer is None:
            self.skipTest("shazamio/yt-dlp/aiogram not installed")

    def test_parse_returns_none_for_empty_result(self) -> None:
        self.assertIsNone(SongRecognizer._parse_shazam_result({}))
        self.assertIsNone(SongRecognizer._parse_shazam_result({"track": {}}))

    def test_parse_extracts_title_and_artist(self) -> None:
        raw = {
            "track": {
                "title": "Never Gonna Give You Up",
                "subtitle": "Rick Astley",
                "sections": [],
                "images": {},
            }
        }
        info = SongRecognizer._parse_shazam_result(raw)
        self.assertIsNotNone(info)
        self.assertEqual(info.title, "Never Gonna Give You Up")
        self.assertEqual(info.artist, "Rick Astley")

    def test_parse_extracts_album_from_metadata(self) -> None:
        raw = {
            "track": {
                "title": "Song",
                "subtitle": "Artist",
                "sections": [
                    {
                        "type": "SONG",
                        "metadata": [
                            {"title": "Album", "text": "Whenever You Need Somebody"},
                            {"title": "Released", "text": "1987"},
                        ],
                    }
                ],
                "images": {},
            }
        }
        info = SongRecognizer._parse_shazam_result(raw)
        self.assertEqual(info.album, "Whenever You Need Somebody")

    def test_parse_extracts_cover_url(self) -> None:
        raw = {
            "track": {
                "title": "Song",
                "subtitle": "Artist",
                "images": {
                    "coverart": "https://example.com/cover.jpg",
                },
                "sections": [],
            }
        }
        info = SongRecognizer._parse_shazam_result(raw)
        self.assertEqual(info.cover_url, "https://example.com/cover.jpg")

    def test_parse_extracts_shazam_share_url(self) -> None:
        raw = {
            "track": {
                "title": "Song",
                "subtitle": "Artist",
                "share": {
                    "href": "https://www.shazam.com/track/123",
                    "subject": "Song - Artist",
                },
                "sections": [],
                "images": {},
            }
        }
        info = SongRecognizer._parse_shazam_result(raw)
        self.assertEqual(info.shazam_url, "https://www.shazam.com/track/123")

    def test_parse_returns_none_when_no_title_or_subtitle(self) -> None:
        raw = {"track": {"sections": [], "images": {}}}
        info = SongRecognizer._parse_shazam_result(raw)
        self.assertIsNone(info)

    def test_parse_handles_non_dict_input(self) -> None:
        self.assertIsNone(SongRecognizer._parse_shazam_result("not a dict"))
        self.assertIsNone(SongRecognizer._parse_shazam_result(None))
        self.assertIsNone(SongRecognizer._parse_shazam_result({"track": "not a dict"}))


if __name__ == "__main__":
    unittest.main()