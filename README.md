# Telegram Downloader Bot

**Language:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

A private, portfolio-ready Telegram bot for downloading supported media from YouTube, YouTube Shorts, Instagram, and SoundCloud.

The project is written completely in Python and includes a simple Ubuntu installer. The bot stays inactive after installation until the admin enables it from inside Telegram.

> Legal note: This project is intended for testing, learning, and personal use. Before public or production use, review platform terms, copyright rules, privacy rules, and Telegram Bot API limits.

## Features

- Automatic link detection for YouTube, `youtu.be`, Shorts, Instagram, and SoundCloud
- Video, photo, audio, and document delivery through `yt-dlp`
- Instagram posts, Reels, profiles, and many carousel posts
- Instagram multi-item posts sent as Telegram albums/media groups
- Captions added to the first uploaded file
- Long captions are shortened safely with a "Get full caption" button
- SoundCloud cover art is sent before the audio when available
- Four-language bot UI: Persian, English, Arabic, and German
- One-time user language selection, with manual changes through `/language`
- Admin activation from inside Telegram
- Personal per-user `cookies.txt` upload and removal
- Optional admin global `cookies.txt`
- Admin-controlled forced channel subscription
- Private-by-default access, with public mode controlled from the admin panel
- Python installer and systemd service for Ubuntu
- Update and full removal scripts for Ubuntu servers
- Service logs in `logs/bot.log`

## Quick Install On Ubuntu

```bash
bash -c 'set -e; repo=instagram-youtube-soundcloud-downloader; if [ -f install.py ] && [ -d .git ]; then python3 install.py; elif [ -d "$repo/.git" ]; then cd "$repo" && python3 update.py; elif [ -e "$repo" ]; then echo "$repo already exists but is not a git checkout. Remove it first or choose another directory."; exit 1; else git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git "$repo" && cd "$repo" && python3 install.py; fi'
```

If the repository already exists on the server, update it instead of cloning inside itself:

```bash
cd instagram-youtube-soundcloud-downloader
python3 update.py
```

The installer asks for:

- Bot name
- Bot token from BotFather
- Admin numeric Telegram ID

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
- `/status` shows bot status
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
python3 update.py
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
BOT_NAME=DownloaderBot
BOT_TOKEN=123456789:replace-me
ADMIN_ID=123456789
ALLOW_ALL_USERS=false
MAX_UPLOAD_MB=49
PLAYLIST_LIMIT=20
CONCURRENT_DOWNLOADS=1
DOWNLOAD_DIR=downloads
DATA_DIR=data
LOG_DIR=logs
COOKIES_FILE=
```

`ALLOW_ALL_USERS` is only the initial default. After installation, the admin can change public access with `/public_on`, `/public_off`, or the admin panel.

`PLAYLIST_LIMIT` protects the server from very large profile or playlist downloads.

`MAX_UPLOAD_MB` should match your Telegram Bot API upload capability.

## Example Links

```text
https://youtube.com/shorts/...
https://www.youtube.com/watch?v=...
https://youtu.be/...
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
python3 update.py
```
