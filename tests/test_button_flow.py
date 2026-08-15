from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.utils import detect_platform, extract_urls
from downloader_bot.state import BotState


class ButtonFlowTests(unittest.TestCase):
    """Tests for the inline-button download flow (Phase 2)."""

    def test_callback_data_fits_telegram_limit(self) -> None:
        token = "AbCdEf123456"
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
            token = state.save_pending_link(100, url, "youtube")

            pending = state.get_pending_link(token, 100)
            self.assertIsNotNone(pending)
            self.assertEqual(pending[0], url)

            state.delete_pending_link(token, 100)
            self.assertIsNone(state.get_pending_link(token, 100))
            state.close()


if __name__ == "__main__":
    unittest.main()
