#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess


SERVICE_NAME = "telegram-downloader.service"


def sudo_command(command: list[str]) -> list[str]:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return command
    if shutil.which("sudo"):
        return ["sudo", *command]
    return command


def run(command: list[str], *, check: bool = False) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, check=check)


def main() -> None:
    run(sudo_command(["systemctl", "stop", SERVICE_NAME]))
    run(sudo_command(["systemctl", "disable", SERVICE_NAME]))
    run(sudo_command(["rm", "-f", f"/etc/systemd/system/{SERVICE_NAME}"]))
    run(sudo_command(["systemctl", "daemon-reload"]))
    print("Service removed. Project files were kept.")


if __name__ == "__main__":
    main()
