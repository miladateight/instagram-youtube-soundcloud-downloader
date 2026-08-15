from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys
import gc

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.i18n import MESSAGES, SUPPORTED_LANGUAGES, normalize_language, t
from downloader_bot.state import BotState


class I18nTests(unittest.TestCase):
    def test_all_languages_have_same_message_keys(self) -> None:
        expected = set(MESSAGES["fa"])
        for language in SUPPORTED_LANGUAGES:
            self.assertEqual(set(MESSAGES[language]), expected)

    def test_normalizes_supported_language_codes(self) -> None:
        self.assertEqual(normalize_language("en-US"), "en")
        self.assertEqual(normalize_language("de"), "de")
        self.assertEqual(normalize_language("unknown"), "fa")
        self.assertEqual(normalize_language(None), "fa")

    def test_formats_translated_message(self) -> None:
        self.assertIn("42", t("en", "your_id", id=42))


class StateTests(unittest.TestCase):
    def test_stores_runtime_settings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")

            state.set_user_language(100, "de")
            state.set_public_access(True)
            state.set_user_cookies_path(100, Path(directory) / "cookies.txt")
            state.save_caption("abc", "long caption")
            state.set_force_join_chat("@channel")
            state.set_force_join_enabled(True)

            self.assertTrue(state.has_user_language(100))
            self.assertEqual(state.user_language(100), "de")
            self.assertTrue(state.public_access())
            self.assertEqual(state.user_cookies_path(100), Path(directory) / "cookies.txt")
            self.assertEqual(state.caption("abc"), "long caption")
            self.assertEqual(state.force_join_chat(), "@channel")
            self.assertTrue(state.is_force_join_enabled())

            state.set_public_access(False)
            state.clear_user_cookies_path(100)
            state.set_force_join_enabled(False)
            state.clear_force_join_chat()

            self.assertFalse(state.public_access())
            self.assertIsNone(state.user_cookies_path(100))
            self.assertFalse(state.is_force_join_enabled())
            self.assertIsNone(state.force_join_chat())
            state.close()

    def test_pending_link_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")
            token = state.save_pending_link(100, "https://youtube.com/watch?v=abc", "youtube")
            pending = state.get_pending_link(token, 100)
            self.assertIsNotNone(pending)
            self.assertEqual(pending[0], "https://youtube.com/watch?v=abc")
            self.assertEqual(pending[1], "youtube")

            state.delete_pending_link(token, 100)
            self.assertIsNone(state.get_pending_link(token, 100))
            state.close()

    def test_pending_link_unknown_token_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")
            self.assertIsNone(state.get_pending_link("nonexistent", 100))
            state.close()

            del state
            gc.collect()

    def test_pending_link_is_private_to_its_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")
            token = state.save_pending_link(100, "https://youtube.com/watch?v=abc", "youtube")

            self.assertIsNotNone(state.get_pending_link(token, 100))
            self.assertIsNone(state.get_pending_link(token, 200))

    def test_same_url_for_two_users_gets_distinct_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = BotState(Path(directory) / "state.sqlite3")
            url = "https://youtube.com/watch?v=abc"
            first = state.save_pending_link(100, url, "youtube")
            second = state.save_pending_link(200, url, "youtube")

            self.assertNotEqual(first, second)
            self.assertLessEqual(len(first), 12)
            self.assertLessEqual(len(second), 12)


if __name__ == "__main__":
    unittest.main()
