from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from downloader_bot.utils import detect_platform, extract_urls


class ProgressHookLogicTests(unittest.TestCase):
    """Tests for the progress hook logic (mirrors bot.py make_progress_hook)."""

    @staticmethod
    def _run_hook(d: dict) -> int:
        percent_holder = {"percent": 0}

        def hook(data: dict) -> None:
            if data.get("status") == "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
                downloaded = data.get("downloaded_bytes") or 0
                if total > 0:
                    percent_holder["percent"] = int(downloaded * 100 / total)
                elif data.get("fragment_count") and data.get("fragment_index"):
                    fragments = data["fragment_count"]
                    index = data["fragment_index"]
                    if fragments > 0:
                        percent_holder["percent"] = int(index * 100 / fragments)
            elif data.get("status") == "finished":
                percent_holder["percent"] = 100

        hook(d)
        return percent_holder["percent"]

    def test_hook_downloading_with_total_bytes(self) -> None:
        d = {"status": "downloading", "total_bytes": 1000, "downloaded_bytes": 250}
        self.assertEqual(self._run_hook(d), 25)

    def test_hook_downloading_with_estimated_bytes(self) -> None:
        d = {"status": "downloading", "total_bytes_estimate": 2000, "downloaded_bytes": 500}
        self.assertEqual(self._run_hook(d), 25)

    def test_hook_downloading_with_fragments(self) -> None:
        d = {"status": "downloading", "fragment_count": 10, "fragment_index": 5}
        self.assertEqual(self._run_hook(d), 50)

    def test_hook_finished_sets_100(self) -> None:
        d = {"status": "finished"}
        self.assertEqual(self._run_hook(d), 100)

    def test_hook_downloading_no_info_stays_zero(self) -> None:
        d = {"status": "downloading"}
        self.assertEqual(self._run_hook(d), 0)


if __name__ == "__main__":
    unittest.main()