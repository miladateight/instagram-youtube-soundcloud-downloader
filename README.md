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
- Four-language bot UI: Persian, English, Arabic, and German
- User language selection with `/language`
- Admin activation from inside Telegram
- Admin-managed `cookies.txt` upload and removal
- Admin-controlled forced channel subscription
- Private-by-default access, with optional public mode through `.env`
- Python installer and systemd service for Ubuntu
- Service logs in `logs/bot.log`

## Quick Install On Ubuntu

```bash
git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git && cd instagram-youtube-soundcloud-downloader && python3 install.py
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

- `/start` starts the bot and shows language selection
- `/language` or `/lang` changes the user language
- `/help` shows the help text
- `/id` shows the user's numeric Telegram ID
- `/status` shows bot status
- `/admin` opens the admin panel
- `/activate` enables downloads
- `/deactivate` disables downloads
- `/cookies` explains how to upload cookies
- `/clearcookies` removes saved cookies
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

Uninstall the service:

```bash
python3 uninstall.py
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

Some Instagram or YouTube links may require login. The admin can upload `cookies.txt` from inside Telegram:

1. Log in through a browser.
2. Export cookies in Netscape `cookies.txt` format.
3. Send the file to the bot.

If the file name is not clear, send it with this caption:

```text
/cookies
```

The bot stores cookies in `data/cookies.txt`. This file is sensitive and is ignored by Git.

## CAPTCHA And "I'm not a robot"

The bot does not bypass CAPTCHA and does not automatically click verification prompts such as `I'm not a robot`.

If Instagram or YouTube asks for a security challenge:

1. The admin logs in manually in a browser.
2. The admin solves the challenge manually.
3. The admin exports cookies in Netscape `cookies.txt` format.
4. The admin uploads the file to the bot.

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

Instagram, YouTube, and SoundCloud may change their pages or restrictions. Keep `yt-dlp` updated:

```bash
cd instagram-youtube-soundcloud-downloader
.venv/bin/pip install --upgrade yt-dlp
sudo systemctl restart telegram-downloader.service
```
