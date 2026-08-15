from __future__ import annotations

import os
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.config import Settings


class ConfigTests(unittest.TestCase):
    def test_platform_enabled_reports_each_platform(self) -> None:
        settings = Settings(
            bot_name="t",
            bot_token="t",
            admin_id=1,
            allow_all_users=False,
            max_upload_mb=0,
            playlist_limit=20,
            concurrent_downloads=4,
            download_dir=Path("downloads"),
            data_dir=Path("data"),
            log_dir=Path("logs"),
            cookies_file=None,
            enable_youtube=True,
            enable_instagram=False,
            enable_soundcloud=True,
            enable_song_detection=True,
            shazam_api_key=None,
            force_ipv4=False,
            support_username=None,
            bot_username=None,
            http_proxy=None,
        )
        self.assertTrue(settings.platform_enabled("youtube"))
        self.assertFalse(settings.platform_enabled("instagram"))
        self.assertTrue(settings.platform_enabled("soundcloud"))
        self.assertFalse(settings.platform_enabled("unknown"))
        self.assertFalse(settings.platform_enabled(None))

    def test_max_upload_bytes_unlimited_when_zero(self) -> None:
        settings = Settings(
            bot_name="t",
            bot_token="t",
            admin_id=1,
            allow_all_users=False,
            max_upload_mb=0,
            playlist_limit=20,
            concurrent_downloads=4,
            download_dir=Path("downloads"),
            data_dir=Path("data"),
            log_dir=Path("logs"),
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
        self.assertEqual(settings.max_upload_bytes, sys.maxsize)

    def test_max_upload_bytes_calculated_when_set(self) -> None:
        settings = Settings(
            bot_name="t",
            bot_token="t",
            admin_id=1,
            allow_all_users=False,
            max_upload_mb=5,
            playlist_limit=20,
            concurrent_downloads=4,
            download_dir=Path("downloads"),
            data_dir=Path("data"),
            log_dir=Path("logs"),
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
        self.assertEqual(settings.max_upload_bytes, 5 * 1024 * 1024)

    def test_load_settings_reads_feature_toggles(self) -> None:
        old_env = dict(os.environ)
        try:
            os.environ["BOT_NAME"] = "TestBot"
            os.environ["BOT_TOKEN"] = "123:abc"
            os.environ["ADMIN_ID"] = "42"
            os.environ["ENABLE_YOUTUBE"] = "true"
            os.environ["ENABLE_INSTAGRAM"] = "false"
            os.environ["ENABLE_SOUNDCLOUD"] = "true"
            os.environ["ENABLE_SONG_DETECTION"] = "false"
            os.environ["SHAZAM_API_KEY"] = "mykey123"
            os.environ["FORCE_IPV4"] = "true"
            os.environ["CONCURRENT_DOWNLOADS"] = "100"
            for key in ["DOWNLOAD_DIR", "DATA_DIR", "LOG_DIR", "COOKIES_FILE"]:
                os.environ.pop(key, None)

            from downloader_bot.config import load_settings
            settings = load_settings()
            self.assertEqual(settings.bot_name, "TestBot")
            self.assertEqual(settings.admin_id, 42)
            self.assertTrue(settings.enable_youtube)
            self.assertFalse(settings.enable_instagram)
            self.assertTrue(settings.enable_soundcloud)
            self.assertFalse(settings.enable_song_detection)
            self.assertEqual(settings.shazam_api_key, "mykey123")
            self.assertTrue(settings.force_ipv4)
            self.assertEqual(settings.concurrent_downloads, 8)
        finally:
            os.environ.clear()
            os.environ.update(old_env)


    def test_support_url_uses_username_when_set(self) -> None:
        settings = Settings(
            bot_name="t", bot_token="t", admin_id=42, allow_all_users=False,
            max_upload_mb=0, playlist_limit=20, concurrent_downloads=4,
            download_dir=Path("downloads"), data_dir=Path("data"), log_dir=Path("logs"),
            cookies_file=None, enable_youtube=True, enable_instagram=True, enable_soundcloud=True,
            enable_song_detection=True, shazam_api_key=None, force_ipv4=False,
            support_username="adminname", bot_username=None, http_proxy=None,
        )
        self.assertEqual(settings.support_url(), "https://t.me/adminname")

    def test_support_url_falls_back_to_admin_id(self) -> None:
        settings = Settings(
            bot_name="t", bot_token="t", admin_id=42, allow_all_users=False,
            max_upload_mb=0, playlist_limit=20, concurrent_downloads=4,
            download_dir=Path("downloads"), data_dir=Path("data"), log_dir=Path("logs"),
            cookies_file=None, enable_youtube=True, enable_instagram=True, enable_soundcloud=True,
            enable_song_detection=True, shazam_api_key=None, force_ipv4=False,
            support_username=None, bot_username=None, http_proxy=None,
        )
        self.assertEqual(settings.support_url(), "https://t.me/user?id=42")

    def test_share_url_returns_none_when_no_username(self) -> None:
        settings = Settings(
            bot_name="t", bot_token="t", admin_id=42, allow_all_users=False,
            max_upload_mb=0, playlist_limit=20, concurrent_downloads=4,
            download_dir=Path("downloads"), data_dir=Path("data"), log_dir=Path("logs"),
            cookies_file=None, enable_youtube=True, enable_instagram=True, enable_soundcloud=True,
            enable_song_detection=True, shazam_api_key=None, force_ipv4=False,
            support_username=None, bot_username=None, http_proxy=None,
        )
        self.assertIsNone(settings.share_url())

    def test_share_url_builds_link_when_username_set(self) -> None:
        settings = Settings(
            bot_name="t", bot_token="t", admin_id=42, allow_all_users=False,
            max_upload_mb=0, playlist_limit=20, concurrent_downloads=4,
            download_dir=Path("downloads"), data_dir=Path("data"), log_dir=Path("logs"),
            cookies_file=None, enable_youtube=True, enable_instagram=True, enable_soundcloud=True,
            enable_song_detection=True, shazam_api_key=None, force_ipv4=False,
            support_username=None, bot_username="mybot", http_proxy=None,
        )
        self.assertEqual(settings.share_url(), "https://t.me/mybot")


if __name__ == "__main__":
    unittest.main()
