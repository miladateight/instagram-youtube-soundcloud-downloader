from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
