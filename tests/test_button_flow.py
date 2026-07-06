from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.utils import detect_platform, extract_urls
from downloader_bot.state import BotState


class ButtonFlowTests(unittest.TestCase):
    """Tests for the inline-button download flow (Phase 2)."""

    def test_url_token_is_stable_and_short(self) -> None:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        token = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
        self.assertEqual(token, hashlib.md5(url.encode("utf-8")).hexdigest()[:12])
        self.assertLessEqual(len(token), 12)

    def test_callback_data_fits_telegram_limit(self) -> None:
        url = "https://www.instagram.com/reel/CtB6xWqBaYJ/?igshid=verylongqueryparam1234567890"
        token = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
        callback_data = f"dl:video:{token}"
        self.assertLessEqual(len(callback_data), 64, "Telegram callback_data must be <= 64 bytes")

    def test_soundcloud_link_detected_for_auto_flow(self) -> None:
        urls = extract_urls("https://soundcloud.com/artist/track")
        self.assertEqual(len(urls), 1)
        self.assertEqual(detect_platform(urls[0]), "soundcloud")

    def test_youtube_link_detected_for_button_flow(self) -> None:
        urls = extract_urls("https://youtube.com/shorts/abc")
        self.assertEqual(len(urls), 1)
        self.assertEqual(detect_platform(urls[0]), "youtube")

    def test_instagram_link_detected_for_button_flow(self) -> None:
        urls = extract_urls("https://instagram.com/reel/abc")
        self.assertEqual(len(urls), 1)
        self.assertEqual(detect_platform(urls[0]), "instagram")

    def test_pending_link_persists_until_used(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")
            url = "https://youtube.com/watch?v=test"
            token = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
            state.save_pending_link(100, url, "youtube", token)

            pending = state.get_pending_link(token)
            self.assertIsNotNone(pending)
            self.assertEqual(pending[0], url)

            state.delete_pending_link(token)
            self.assertIsNone(state.get_pending_link(token))
            state.close()


if __name__ == "__main__":
    unittest.main()