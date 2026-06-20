#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"
PYTHON_BIN = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
PIP_BIN = VENV_DIR / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")


def run(command: list[str]) -> None:
    print("+ " + " ".join(map(str, command)))
    subprocess.run(command, check=True)


def main() -> None:
    if not (PROJECT_DIR / ".env").exists():
        raise SystemExit("Create .env first. You can copy .env.example or run python3 install.py on Ubuntu.")

    if not PYTHON_BIN.exists():
        run([sys.executable, "-m", "venv", str(VENV_DIR)])

    run([str(PIP_BIN), "install", "-r", str(PROJECT_DIR / "requirements.txt")])
    run([str(PYTHON_BIN), "-m", "downloader_bot"])


if __name__ == "__main__":
    main()
