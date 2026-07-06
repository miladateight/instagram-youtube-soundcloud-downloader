from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path, PurePosixPath
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import install


class InstallerTests(unittest.TestCase):
    def test_systemd_service_paths_are_not_quoted(self) -> None:
        service_text = install.build_service_text(
            PurePosixPath("/opt/downloader/.venv/bin/python"),
            "telegrambot",
        )

        self.assertIn(f"WorkingDirectory={install.PROJECT_DIR}", service_text)
        self.assertIn(f"EnvironmentFile={install.PROJECT_DIR / '.env'}", service_text)
        self.assertIn("ExecStart=/opt/downloader/.venv/bin/python -m downloader_bot", service_text)
        self.assertNotIn('WorkingDirectory="', service_text)
        self.assertNotIn('EnvironmentFile="', service_text)
        self.assertNotIn('ExecStart="', service_text)

    def test_env_quote_escapes_special_characters(self) -> None:
        self.assertEqual(install.env_quote("simple"), '"simple"')
        self.assertEqual(install.env_quote('with"quote'), '"with\\"quote"')
        self.assertEqual(install.env_quote("back\\slash"), '"back\\\\slash"')

    def test_feature_defaults_has_all_platforms(self) -> None:
        expected_keys = {"ENABLE_YOUTUBE", "ENABLE_INSTAGRAM", "ENABLE_SOUNDCLOUD", "ENABLE_SONG_DETECTION"}
        self.assertEqual(set(install.FEATURE_DEFAULTS.keys()), expected_keys)
        for value in install.FEATURE_DEFAULTS.values():
            self.assertTrue(value)

    def test_write_env_includes_feature_toggles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            original_project = install.PROJECT_DIR
            try:
                install.PROJECT_DIR = Path(directory)
                features = {
                    "ENABLE_YOUTUBE": True,
                    "ENABLE_INSTAGRAM": False,
                    "ENABLE_SOUNDCLOUD": True,
                    "ENABLE_SONG_DETECTION": True,
                }
                install.write_env("MyBot", "token:abc", "12345", features, "shazamkey123", "adminname", "mybot")

                env_content = (Path(directory) / ".env").read_text(encoding="utf-8")
                self.assertIn('BOT_NAME="MyBot"', env_content)
                self.assertIn('BOT_TOKEN="token:abc"', env_content)
                self.assertIn("ADMIN_ID=12345", env_content)
                self.assertIn("SUPPORT_USERNAME=\"adminname\"", env_content)
                self.assertIn("BOT_USERNAME=\"mybot\"", env_content)
                self.assertIn("ENABLE_YOUTUBE=true", env_content)
                self.assertIn("ENABLE_INSTAGRAM=false", env_content)
                self.assertIn("ENABLE_SOUNDCLOUD=true", env_content)
                self.assertIn("ENABLE_SONG_DETECTION=true", env_content)
                self.assertIn('SHAZAM_API_KEY="shazamkey123"', env_content)
            finally:
                install.PROJECT_DIR = original_project

    def test_write_env_empty_shazam_key_when_song_detection_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            original_project = install.PROJECT_DIR
            try:
                install.PROJECT_DIR = Path(directory)
                features = {
                    "ENABLE_YOUTUBE": True,
                    "ENABLE_INSTAGRAM": True,
                    "ENABLE_SOUNDCLOUD": True,
                    "ENABLE_SONG_DETECTION": False,
                }
                install.write_env("Bot", "tok", "1", features, "", "", "")

                env_content = (Path(directory) / ".env").read_text(encoding="utf-8")
                self.assertIn("ENABLE_SONG_DETECTION=false", env_content)
                self.assertIn('SHAZAM_API_KEY=""', env_content)
                self.assertIn('SUPPORT_USERNAME=""', env_content)
                self.assertIn('BOT_USERNAME=""', env_content)
            finally:
                install.PROJECT_DIR = original_project


if __name__ == "__main__":
    unittest.main()
