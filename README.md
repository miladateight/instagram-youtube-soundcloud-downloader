# Ateight Downloader

**Language:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

**Version 1.1.0**

A private, portfolio-ready Telegram bot for downloading media from YouTube, YouTube Shorts, Instagram, and SoundCloud — with inline buttons, song detection, and an interactive installer.

The project is written completely in Python and includes a simple Ubuntu installer with a feature checklist. The bot stays inactive after installation until the admin enables it from inside Telegram.

> Legal note: This project is intended for testing, learning, and personal use. Before public or production use, review platform terms, copyright rules, privacy rules, and Telegram Bot API limits.

## Features

### Download
- Automatic link detection for YouTube, `youtu.be`, Shorts, `m.youtube.com`, `music.youtube.com`, Instagram, and SoundCloud
- Video, photo, audio, and document delivery through `yt-dlp`
- Instagram posts, Reels, profiles, and many carousel posts
- Photo-only Instagram posts and profiles use a `gallery-dl` fallback when `yt-dlp` has no video result
- Instagram multi-item posts sent as Telegram albums/media groups
- **Correct video dimensions** — Reels and Shorts keep their original aspect ratio (no more square videos)
- YouTube video downloads prefer Telegram-friendly MP4 instead of WebM
- SoundCloud: best audio quality for tracks under 15 minutes, cover art sent separately before the audio
- Captions added to the first uploaded file
- Long captions are shortened safely with a "Get full caption" button
- Fallback to document upload if Telegram rejects the media upload

### User Experience
- **Inline glass buttons** — after sending a link, the bot asks what you want: Video, Audio (MP3), or Find Song
- **Reply keyboard menu** — persistent buttons at the bottom: Download, MP3, Status, Language, Share, Support
- **Song detection** — recognize the song inside a video using Shazam (free, no API key required)
- **Support button** — users can contact the admin directly from any error message
- **Share button** — users can forward the bot to their friends
- Real download progress (using yt-dlp progress hooks)
- Per-user anti-spam guard: one active download and one new request every 5 seconds
- Download buttons are bound to the user who submitted the link and re-check access rules before running
- Four-language bot UI: Persian, English, Arabic, and German
- One-time user language selection, with manual changes through `/language`
- Categorized error messages (no raw yt-dlp errors shown to users)

### Admin
- Admin activation from inside Telegram
- Personal per-user `cookies.txt` upload and removal
- Optional admin global `cookies.txt`
- Admin-controlled forced channel subscription
- Private-by-default access, with public mode controlled from the admin panel
- Feature toggles: enable/disable YouTube, Instagram, SoundCloud, or Song Detection per bot

### Installer
- **Interactive feature checklist** (whiptail on Linux, text fallback elsewhere)
- Ateight ASCII art banner
- Asks for bot name, token, admin ID, support username, and bot username
- Lets you choose which platforms and features to enable
- Optional custom Shazam API key
- Python installer and systemd service for Ubuntu
- Update and full removal scripts for Ubuntu servers
- Service logs in `logs/bot.log`

## Quick Install On Ubuntu

```bash
bash -c 'set -e; repo=instagram-youtube-soundcloud-downloader; if [ -f install.py ] && [ -d .git ]; then python3 install.py; elif [ -d "$repo/.git" ]; then cd "$repo" && python3 install.py; elif [ -e "$repo" ]; then echo "$repo already exists but is not a git checkout. Remove it first or choose another directory."; exit 1; else git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git "$repo" && cd "$repo" && python3 install.py; fi'
```

`python3 install.py` is also the update command. If `.env` already exists, it updates dependencies, pulls the latest code when possible, and restarts the service:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```

The installer asks for:

- Bot name (default: Ateight Downloader)
- Bot token from BotFather
- Admin numeric Telegram ID
- Admin Telegram username for the support button (optional)
- Bot username for the share button (optional)
- Which platforms to enable (YouTube, Instagram, SoundCloud)
- Whether to enable song detection (Shazam)
- Optional custom Shazam API key

After installation, open the bot in Telegram as the admin and send:

```text
/activate
```

The bot will not download anything until it is activated.

## Bot Commands

- `/start` starts the bot; language is requested only once
- `/language` or `/lang` changes the user language
- `/help` shows the help text
- `/id` shows the user's numeric Telegram ID
- `/mp3 <link>` sends audio only as MP3
- `/status` shows personal cookies status for users and full status for the admin
- `/admin` opens the admin panel
- `/activate` enables downloads
- `/deactivate` disables downloads
- `/public_on` opens public access
- `/public_off` closes public access
- `/cookies` explains how to upload cookies
- `/clearcookies` removes the user's personal cookies
- `/clearcookies global` removes admin global cookies
- `/forcejoin` shows forced subscription status
- `/forcejoin_on @channel` enables forced subscription
- `/forcejoin_off` disables forced subscription
- `/support` shows the support button
- `/share` shows a ready-to-forward share message
- `/about` shows bot info and version

## How It Works

1. **Send a link** — paste a YouTube, Instagram, or SoundCloud link
2. **Choose a format** — the bot shows inline buttons: Video, Audio (MP3), or Find Song
3. **Get the result** — the bot downloads and sends the media with correct dimensions and thumbnail

For SoundCloud, the bot downloads audio automatically (no buttons needed) and sends the cover art separately before the audio.

## Forced Subscription

The admin can require users to join a Telegram channel before downloading.

```text
/forcejoin_on @your_channel
```

To disable it:

```text
/forcejoin_off
```

The bot must be a member or admin in the required channel so Telegram can verify membership. Admin users are not blocked by forced subscription.

## Service Management

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

Update the installed bot:

```bash
python3 install.py
```

Uninstall only the systemd service:

```bash
python3 uninstall.py
```

Remove the service and delete the project directory:

```bash
python3 remove.py
```

## Development Run

```bash
cp .env.example .env
nano .env
python3 run.py
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## Cookies For Instagram And YouTube

Some Instagram or YouTube links may require login. Each allowed user can upload a personal `cookies.txt` file from inside Telegram:

1. Log in through a browser.
2. Export cookies in Netscape `cookies.txt` format.
3. Send the file to the bot.

If the file name is not clear, send it with this caption:

```text
/cookies
```

The bot stores personal cookies in `data/user_cookies/`. Passwords are not stored; only the exported cookies file is kept on the server. A user can remove their personal cookies with `/clearcookies`.

The admin can upload global bot cookies by sending `cookies.txt` with the caption:

```text
global
```

Admin global cookies are stored in `data/cookies.txt` and can be removed with `/clearcookies global`. Cookie files are sensitive and are ignored by Git.

## CAPTCHA And "I'm not a robot"

The bot does not bypass CAPTCHA and does not automatically click verification prompts such as `I'm not a robot`.

If Instagram or YouTube asks for a security challenge:

1. The user or admin logs in manually in a browser.
2. The challenge is solved manually in the browser.
3. Cookies are exported in Netscape `cookies.txt` format.
4. The cookies file is uploaded to the bot.

This improves login reliability but cannot guarantee that a platform will never request verification again.

## `.env` Settings

```env
BOT_NAME=Ateight Downloader
BOT_TOKEN=123456789:replace-me
ADMIN_ID=123456789
SUPPORT_USERNAME=
BOT_USERNAME=
ALLOW_ALL_USERS=false
MAX_UPLOAD_MB=0
PLAYLIST_LIMIT=20
CONCURRENT_DOWNLOADS=4
DOWNLOAD_DIR=downloads
DATA_DIR=data
LOG_DIR=logs
COOKIES_FILE=
ENABLE_YOUTUBE=true
ENABLE_INSTAGRAM=true
ENABLE_SOUNDCLOUD=true
ENABLE_SONG_DETECTION=true
SHAZAM_API_KEY=
FORCE_IPV4=false
HTTP_PROXY=
```

`ALLOW_ALL_USERS` is only the initial default. After installation, the admin can change public access with `/public_on`, `/public_off`, or the admin panel.

`PLAYLIST_LIMIT` protects the server from very large profile or playlist downloads.

`MAX_UPLOAD_MB=0` means the app does not block files by size. Telegram Bot API can still reject files above its real upload limit.

`SUPPORT_USERNAME` — if set, the support button links to `t.me/yourname`. Otherwise it falls back to `t.me/user?id=ADMIN_ID`.

`BOT_USERNAME` — if set, the share button links to `t.me/your_bot`.

`FORCE_IPV4` — can help with YouTube HTTP 403 errors on some servers or VPNs.

`HTTP_PROXY` — optional proxy for yt-dlp downloads.

## Example Links

```text
https://youtube.com/shorts/...
https://www.youtube.com/watch?v=...
https://youtu.be/...
https://m.youtube.com/watch?v=...
https://music.youtube.com/watch?v=...
https://www.instagram.com/reel/...
https://www.instagram.com/p/...
https://www.instagram.com/username/
https://soundcloud.com/...
https://on.soundcloud.com/...
```

## Keeping Download Support Healthy

Instagram, YouTube, and SoundCloud may change their pages or restrictions. Keep the bot and `yt-dlp` updated:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```
