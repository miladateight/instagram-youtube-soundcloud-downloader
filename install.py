#!/usr/bin/env python3
from __future__ import annotations

import getpass
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
SERVICE_NAME = "telegram-downloader.service"

FEATURE_DEFAULTS = {
    "ENABLE_YOUTUBE": True,
    "ENABLE_INSTAGRAM": True,
    "ENABLE_SOUNDCLOUD": True,
    "ENABLE_SONG_DETECTION": True,
}


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


def systemd_path(path: Path) -> str:
    return str(path)


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
    run([str(pip_bin), "install", "--upgrade", "-r", str(PROJECT_DIR / "requirements.txt")])
    return python_bin


def whiptail_available() -> bool:
    return sys.stdin.isatty() and bool(shutil.which("whiptail"))


def feature_checklist_whiptail() -> dict[str, bool]:
    items = [
        ("ENABLE_YOUTUBE", "YouTube (videos, shorts, mp3, song detection)", FEATURE_DEFAULTS["ENABLE_YOUTUBE"]),
        ("ENABLE_INSTAGRAM", "Instagram (reels, posts, mp3, song detection)", FEATURE_DEFAULTS["ENABLE_INSTAGRAM"]),
        ("ENABLE_SOUNDCLOUD", "SoundCloud (high quality audio + cover art)", FEATURE_DEFAULTS["ENABLE_SOUNDCLOUD"]),
        ("ENABLE_SONG_DETECTION", "Song detection via Shazam (Find song button)", FEATURE_DEFAULTS["ENABLE_SONG_DETECTION"]),
    ]
    args = ["whiptail", "--title", "Select features to enable", "--output-fd", "1", "--checklist",
            "Use SPACE to toggle. ENTER to confirm.", "0", "0", "0"]
    for key, label, default in items:
        args.append(key)
        args.append(label)
        args.append("ON" if default else "OFF")

    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise SystemExit("Feature selection cancelled.")
    selected = set(shlex.split(result.stdout)) if result.stdout.strip() else set()
    chosen = {}
    for key, label, default in items:
        chosen[key] = key in selected
    if not any(chosen.values()):
        print("No features selected. Aborting.")
        raise SystemExit(1)
    return chosen


def feature_checklist_text() -> dict[str, bool]:
    print("\n=== Feature selection ===")
    print("Type y/n for each feature. Just press Enter to accept the default.\n")
    items = [
        ("ENABLE_YOUTUBE", "YouTube (videos, shorts, mp3, song detection)", FEATURE_DEFAULTS["ENABLE_YOUTUBE"]),
        ("ENABLE_INSTAGRAM", "Instagram (reels, posts, mp3, song detection)", FEATURE_DEFAULTS["ENABLE_INSTAGRAM"]),
        ("ENABLE_SOUNDCLOUD", "SoundCloud (high quality audio + cover art)", FEATURE_DEFAULTS["ENABLE_SOUNDCLOUD"]),
        ("ENABLE_SONG_DETECTION", "Song detection via Shazam (Find song button)", FEATURE_DEFAULTS["ENABLE_SONG_DETECTION"]),
    ]
    chosen: dict[str, bool] = {}
    for key, label, default in items:
        hint = "Y/n" if default else "y/N"
        while True:
            answer = input(f"{label} [{hint}]: ").strip().lower()
            if not answer:
                chosen[key] = default
                break
            if answer in {"y", "yes"}:
                chosen[key] = True
                break
            if answer in {"n", "no"}:
                chosen[key] = False
                break
            print("Please answer y or n.")
    if not any(chosen.values()):
        print("No features selected. Aborting.")
        raise SystemExit(1)
    return chosen


def collect_features() -> dict[str, bool]:
    if whiptail_available():
        return feature_checklist_whiptail()
    return feature_checklist_text()


def prompt_shazam_key(features: dict[str, bool]) -> str:
    if not features.get("ENABLE_SONG_DETECTION"):
        return ""
    print("\n=== Shazam API key (optional) ===")
    print("The bot uses the free shazamio library by default. If you have a custom")
    print("Shazam API key, paste it here. Otherwise just press Enter to use the free mode.")
    return prompt("Shazam API key", required=False, default="")


def write_env(
    bot_name: str,
    bot_token: str,
    admin_id: str,
    features: dict[str, bool],
    shazam_api_key: str,
    support_username: str = "",
    bot_username: str = "",
) -> None:
    download_dir = PROJECT_DIR / "downloads"
    data_dir = PROJECT_DIR / "data"
    log_dir = PROJECT_DIR / "logs"

    download_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"BOT_NAME={env_quote(bot_name)}",
        f"BOT_TOKEN={env_quote(bot_token)}",
        f"ADMIN_ID={admin_id}",
        f"SUPPORT_USERNAME={env_quote(support_username.lstrip('@'))}",
        f"BOT_USERNAME={env_quote(bot_username.lstrip('@'))}",
        "ALLOW_ALL_USERS=false",
        "MAX_UPLOAD_MB=0",
        "PLAYLIST_LIMIT=20",
        "CONCURRENT_DOWNLOADS=4",
        f"DOWNLOAD_DIR={env_quote(str(download_dir))}",
        f"DATA_DIR={env_quote(str(data_dir))}",
        f"LOG_DIR={env_quote(str(log_dir))}",
        "COOKIES_FILE=",
        f"ENABLE_YOUTUBE={'true' if features.get('ENABLE_YOUTUBE') else 'false'}",
        f"ENABLE_INSTAGRAM={'true' if features.get('ENABLE_INSTAGRAM') else 'false'}",
        f"ENABLE_SOUNDCLOUD={'true' if features.get('ENABLE_SOUNDCLOUD') else 'false'}",
        f"ENABLE_SONG_DETECTION={'true' if features.get('ENABLE_SONG_DETECTION') else 'false'}",
        f"SHAZAM_API_KEY={env_quote(shazam_api_key)}",
        "",
    ]
    env_path = PROJECT_DIR / ".env"
    env_path.write_text("\n".join(lines), encoding="utf-8")
    try:
        env_path.chmod(0o600)
    except OSError:
        pass


def build_service_text(python_bin: Path, service_user: str) -> str:
    service_text = f"""[Unit]
Description=Telegram Downloader Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={service_user}
WorkingDirectory={systemd_path(PROJECT_DIR)}
EnvironmentFile={systemd_path(PROJECT_DIR / ".env")}
ExecStart={systemd_path(python_bin)} -m downloader_bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    return service_text


def install_service(python_bin: Path) -> None:
    service_text = build_service_text(python_bin, current_service_user())
    temp_service = PROJECT_DIR / f".{SERVICE_NAME}.tmp"
    temp_service.write_text(service_text, encoding="utf-8")
    run(sudo_command(["mv", str(temp_service), f"/etc/systemd/system/{SERVICE_NAME}"]))
    run(sudo_command(["systemctl", "daemon-reload"]))
    run(sudo_command(["systemctl", "enable", SERVICE_NAME]))
    run(sudo_command(["systemctl", "restart", SERVICE_NAME]))


def update_existing_installation() -> None:
    print("Existing .env found. Running update mode.")
    print("Use python3 install.py --reconfigure if you want to enter a new token/admin or change features.")
    print()

    install_system_packages()
    if (PROJECT_DIR / ".git").exists():
        run(["git", "pull", "--ff-only"], check=False)
    python_bin = create_virtualenv()
    install_service(python_bin)

    print()
    print("Update complete.")
    print(f"Status: sudo systemctl status {SERVICE_NAME}")
    print(f"Logs:   sudo journalctl -u {SERVICE_NAME} -f")


def print_summary(features: dict[str, bool], shazam_key: bool) -> None:
    print("\n=== Installation summary ===")
    for key, label in [
        ("ENABLE_YOUTUBE", "YouTube"),
        ("ENABLE_INSTAGRAM", "Instagram"),
        ("ENABLE_SOUNDCLOUD", "SoundCloud"),
        ("ENABLE_SONG_DETECTION", "Song detection (Shazam)"),
    ]:
        status = "ON" if features.get(key) else "OFF"
        print(f"  {label}: {status}")
    if features.get("ENABLE_SONG_DETECTION"):
        print(f"  Shazam API key: {'custom' if shazam_key else 'free (shazamio)'}")
    print()


def print_banner() -> None:
    banner = """
  ___  _       _       _     _
 / _ \\| |     (_)     | |   | |
/ /_\\ \\ |_ ___ _  __ _| |__ | |_
|  _  | __/ _ \\ |/ _` | '_ \\| __|
| | | | ||  __/ | (_| | | | | |_
\\_| |_/\\__\\___|_|\\__, |_| |_|\\__|
                  __/ |
                 |___/

    Telegram Downloader Bot  |  By Milad Ateight
"""
    print(banner)


def main() -> None:
    print_banner()
    print("The bot will stay inactive until the admin sends /activate in Telegram.")
    print()

    if (PROJECT_DIR / ".env").exists() and "--reconfigure" not in sys.argv:
        update_existing_installation()
        return

    print("=== Bot configuration ===")
    bot_name = prompt("Bot name", default="Atieght Downloader")
    bot_token = prompt("Bot token (from BotFather)")
    admin_id = prompt("Admin numeric Telegram ID")
    if not admin_id.isdigit():
        raise SystemExit("Admin ID must be numeric.")

    support_username = prompt("Admin Telegram username for support (e.g. @yourname, optional)", required=False, default="")
    bot_username = prompt("Bot username (e.g. @atieght_bot, for share button)", required=False, default="")

    features = collect_features()
    shazam_api_key = prompt_shazam_key(features)
    print_summary(features, bool(shazam_api_key))

    install_system_packages()
    python_bin = create_virtualenv()
    write_env(bot_name, bot_token, admin_id, features, shazam_api_key, support_username, bot_username)
    install_service(python_bin)

    print()
    print("Done.")
    print("Open your bot in Telegram and send /activate as the admin.")
    print(f"Status: sudo systemctl status {SERVICE_NAME}")
    print(f"Logs:   sudo journalctl -u {SERVICE_NAME} -f")


if __name__ == "__main__":
    main()
