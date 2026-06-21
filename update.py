#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SERVICE_NAME = "telegram-downloader.service"


def sudo_command(command: list[str]) -> list[str]:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return command
    if shutil.which("sudo"):
        return ["sudo", *command]
    return command


def run(command: list[str]) -> None:
    print("+ " + " ".join(map(str, command)))
    subprocess.run(command, check=True)


def service_exists() -> bool:
    result = subprocess.run(
        sudo_command(["systemctl", "cat", SERVICE_NAME]),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> None:
    if not (PROJECT_DIR / ".git").exists():
        raise SystemExit("This directory is not a git checkout. Clone the repository first.")
    if not (PROJECT_DIR / ".env").exists():
        raise SystemExit("No .env file found. Run python3 install.py for the first installation.")

    python_bin = PROJECT_DIR / ".venv" / "bin" / "python"
    pip_bin = PROJECT_DIR / ".venv" / "bin" / "pip"
    if not python_bin.exists():
        run(["python3", "-m", "venv", str(PROJECT_DIR / ".venv")])

    run(["git", "pull", "--ff-only"])
    run([str(pip_bin), "install", "--upgrade", "-r", str(PROJECT_DIR / "requirements.txt")])

    if service_exists():
        run(sudo_command(["systemctl", "daemon-reload"]))
        run(sudo_command(["systemctl", "restart", SERVICE_NAME]))
    else:
        sys.path.insert(0, str(PROJECT_DIR))
        from install import install_service

        install_service(python_bin)

    print("Update complete.")
    print(f"Status: sudo systemctl status {SERVICE_NAME}")


if __name__ == "__main__":
    main()
