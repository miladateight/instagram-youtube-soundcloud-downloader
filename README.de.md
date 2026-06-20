# Telegram Downloader Bot

**Sprache:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

Ein privater, portfolio-tauglicher Telegram-Bot zum Herunterladen unterstützter Medien von YouTube, YouTube Shorts, Instagram und SoundCloud.

Das Projekt ist vollständig in Python geschrieben und enthält einen einfachen Ubuntu-Installer. Nach der Installation bleibt der Bot inaktiv, bis der Admin ihn in Telegram aktiviert.

> Rechtlicher Hinweis: Dieses Projekt ist für Tests, Lernen und private Nutzung gedacht. Prüfe vor öffentlicher Nutzung die Plattformregeln, Urheberrechte, Datenschutzregeln und Telegram Bot API Limits.

## Funktionen

- Automatische Link-Erkennung für YouTube, `youtu.be`, Shorts, Instagram und SoundCloud
- Versand von Videos, Fotos, Audio und allgemeinen Dateien über `yt-dlp`
- Unterstützung für Instagram-Posts, Reels, Profile und viele Carousel-Posts
- Instagram-Posts mit mehreren Medien werden als Album/media group gesendet
- Caption auf der ersten gesendeten Datei
- Vier Sprachversionen im Bot: Persisch, Englisch, Arabisch und Deutsch
- Sprachauswahl pro Nutzer mit `/language`
- Admin-Aktivierung direkt in Telegram
- Admin-Upload und Entfernung von `cookies.txt`
- Admin-gesteuerte Pflichtmitgliedschaft in einem Kanal
- Standardmäßig privater Zugriff, optional öffentlich über `.env`
- Python-Installer und systemd-Service für Ubuntu
- Service-Logs in `logs/bot.log`

## Schnellinstallation Auf Ubuntu

```bash
git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git && cd instagram-youtube-soundcloud-downloader && python3 install.py
```

Der Installer fragt nach:

- Bot-Name
- Bot-Token von BotFather
- Numerische Telegram-ID des Admins

Nach der Installation öffnest du den Bot in Telegram als Admin und sendest:

```text
/activate
```

Der Bot lädt nichts herunter, bis er aktiviert wurde.

## Bot-Befehle

- `/start` startet den Bot und zeigt die Sprachauswahl
- `/language` oder `/lang` ändert die Nutzersprache
- `/help` zeigt Hilfe
- `/id` zeigt die numerische Telegram-ID
- `/status` zeigt den Bot-Status
- `/admin` öffnet das Admin-Panel
- `/activate` aktiviert Downloads
- `/deactivate` deaktiviert Downloads
- `/cookies` erklärt den Cookies-Upload
- `/clearcookies` entfernt gespeicherte Cookies
- `/forcejoin` zeigt den Status der Pflichtmitgliedschaft
- `/forcejoin_on @channel` aktiviert die Pflichtmitgliedschaft
- `/forcejoin_off` deaktiviert die Pflichtmitgliedschaft

## Pflichtmitgliedschaft

Der Admin kann Nutzer verpflichten, vor dem Download einem Telegram-Kanal beizutreten.

```text
/forcejoin_on @your_channel
```

Zum Deaktivieren:

```text
/forcejoin_off
```

Der Bot muss Mitglied oder Admin im gewünschten Kanal sein, damit Telegram die Mitgliedschaft prüfen kann. Admin-Nutzer werden durch diese Prüfung nicht blockiert.

## Service-Verwaltung

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

Service entfernen:

```bash
python3 uninstall.py
```

## Manuell Für Entwicklung Starten

```bash
cp .env.example .env
nano .env
python3 run.py
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## Cookies Für Instagram Und YouTube

Einige Instagram- oder YouTube-Links benötigen Login. Der Admin kann `cookies.txt` direkt in Telegram hochladen:

1. Im Browser einloggen.
2. Cookies im Netscape-Format `cookies.txt` exportieren.
3. Die Datei an den Bot senden.

Wenn der Dateiname nicht eindeutig ist, sende sie mit dieser Caption:

```text
/cookies
```

Der Bot speichert Cookies in `data/cookies.txt`. Diese Datei ist sensibel und wird von Git ignoriert.

## CAPTCHA Und "I'm not a robot"

Der Bot umgeht kein CAPTCHA und klickt nicht automatisch auf Prüfungen wie `I'm not a robot`.

Wenn Instagram oder YouTube eine Sicherheitsprüfung verlangt:

1. Der Admin meldet sich manuell im Browser an.
2. Der Admin löst die Prüfung manuell.
3. Der Admin exportiert Cookies im Netscape-Format `cookies.txt`.
4. Der Admin lädt die Datei in Telegram beim Bot hoch.

Das verbessert die Login-Zuverlässigkeit, garantiert aber nicht, dass eine Plattform nie wieder eine Prüfung verlangt.

## `.env` Einstellungen

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

`PLAYLIST_LIMIT` schützt den Server vor sehr großen Profile- oder Playlist-Downloads.

`MAX_UPLOAD_MB` sollte zu deiner Telegram Bot API Upload-Fähigkeit passen.

## Beispiel-Links

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

## Download-Support Stabil Halten

Instagram, YouTube und SoundCloud können Seiten oder Einschränkungen ändern. Halte `yt-dlp` aktuell:

```bash
cd instagram-youtube-soundcloud-downloader
.venv/bin/pip install --upgrade yt-dlp
sudo systemctl restart telegram-downloader.service
```
