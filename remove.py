#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SERVICE_NAME = "telegram-downloader.service"


def sudo_command(command: list[str]) -> list[str]:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return command
    if shutil.which("sudo"):
        return ["sudo", *command]
    return command


def run(command: list[str], *, check: bool = False) -> None:
    print("+ " + " ".join(map(str, command)))
    subprocess.run(command, check=check)


def main() -> None:
    print("This will remove the systemd service and delete this project directory:")
    print(PROJECT_DIR)
    confirmation = input("Type DELETE to continue: ").strip()
    if confirmation != "DELETE":
        raise SystemExit("Cancelled.")

    run(sudo_command(["systemctl", "stop", SERVICE_NAME]))
    run(sudo_command(["systemctl", "disable", SERVICE_NAME]))
    run(sudo_command(["rm", "-f", f"/etc/systemd/system/{SERVICE_NAME}"]))
    run(sudo_command(["systemctl", "daemon-reload"]))

    parent = PROJECT_DIR.parent
    os.chdir(parent)
    shutil.rmtree(PROJECT_DIR)
    print("Project directory removed.")


if __name__ == "__main__":
    main()
