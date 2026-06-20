#!/usr/bin/env python3
from __future__ import annotations

import getpass
import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SERVICE_NAME = "telegram-downloader.service"


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command))
    return subprocess.run(command, check=check, text=True)


def sudo_command(command: list[str]) -> list[str]:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return command
    if shutil.which("sudo"):
        return ["sudo", *command]
    return command


def prompt(label: str, *, required: bool = True, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if not value and default:
            value = default
        if value or not required:
            return value
        print("This value is required.")


def env_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def current_service_user() -> str:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return os.environ.get("SUDO_USER") or getpass.getuser()
    return getpass.getuser()


def systemd_quote(path: Path) -> str:
    return '"' + str(path).replace("\\", "\\\\").replace('"', '\\"') + '"'


def install_system_packages() -> None:
    if not shutil.which("apt-get"):
        print("apt-get was not found. Skipping system package installation.")
        print("Make sure python3-venv, python3-pip, and ffmpeg are installed.")
        return

    run(sudo_command(["apt-get", "update"]))
    run(sudo_command(["apt-get", "install", "-y", "python3", "python3-venv", "python3-pip", "ffmpeg"]))


def create_virtualenv() -> Path:
    venv_dir = PROJECT_DIR / ".venv"
    python_bin = venv_dir / "bin" / "python"
    pip_bin = venv_dir / "bin" / "pip"

    if not python_bin.exists():
        run(["python3", "-m", "venv", str(venv_dir)])

    run([str(python_bin), "-m", "pip", "install", "--upgrade", "pip", "wheel"])
    run([str(pip_bin), "install", "-r", str(PROJECT_DIR / "requirements.txt")])
    return python_bin


def write_env(bot_name: str, bot_token: str, admin_id: str) -> None:
    download_dir = PROJECT_DIR / "downloads"
    data_dir = PROJECT_DIR / "data"
    log_dir = PROJECT_DIR / "logs"

    download_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    env_text = "\n".join(
        [
            f"BOT_NAME={env_quote(bot_name)}",
            f"BOT_TOKEN={env_quote(bot_token)}",
            f"ADMIN_ID={admin_id}",
            "ALLOW_ALL_USERS=false",
            "MAX_UPLOAD_MB=49",
            "PLAYLIST_LIMIT=20",
            "CONCURRENT_DOWNLOADS=1",
            f"DOWNLOAD_DIR={env_quote(str(download_dir))}",
            f"DATA_DIR={env_quote(str(data_dir))}",
            f"LOG_DIR={env_quote(str(log_dir))}",
            "COOKIES_FILE=",
            "",
        ]
    )
    env_path = PROJECT_DIR / ".env"
    env_path.write_text(env_text, encoding="utf-8")
    try:
        env_path.chmod(0o600)
    except OSError:
        pass


def install_service(python_bin: Path) -> None:
    service_user = current_service_user()
    service_text = f"""[Unit]
Description=Telegram Downloader Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={service_user}
WorkingDirectory={systemd_quote(PROJECT_DIR)}
EnvironmentFile={systemd_quote(PROJECT_DIR / ".env")}
ExecStart={systemd_quote(python_bin)} -m downloader_bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    temp_service = PROJECT_DIR / f".{SERVICE_NAME}.tmp"
    temp_service.write_text(service_text, encoding="utf-8")
    run(sudo_command(["mv", str(temp_service), f"/etc/systemd/system/{SERVICE_NAME}"]))
    run(sudo_command(["systemctl", "daemon-reload"]))
    run(sudo_command(["systemctl", "enable", SERVICE_NAME]))
    run(sudo_command(["systemctl", "restart", SERVICE_NAME]))


def main() -> None:
    print("Telegram Downloader installer")
    print("The bot will stay inactive until the admin sends /activate in Telegram.")
    print()

    bot_name = prompt("Bot name", default="DownloaderBot")
    bot_token = prompt("Bot token")
    admin_id = prompt("Admin numeric Telegram ID")
    if not admin_id.isdigit():
        raise SystemExit("Admin ID must be numeric.")

    install_system_packages()
    python_bin = create_virtualenv()
    write_env(bot_name, bot_token, admin_id)
    install_service(python_bin)

    print()
    print("Done.")
    print("Open your bot in Telegram and send /activate as the admin.")
    print(f"Status: sudo systemctl status {SERVICE_NAME}")
    print(f"Logs:   sudo journalctl -u {SERVICE_NAME} -f")


if __name__ == "__main__":
    main()
