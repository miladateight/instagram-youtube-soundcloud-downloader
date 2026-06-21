# Telegram Downloader Bot

**Sprache:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

Ein privater, portfolio-tauglicher Telegram-Bot zum Herunterladen unterstützter Medien von YouTube, YouTube Shorts, Instagram und SoundCloud.

Das Projekt ist vollständig in Python geschrieben und enthält einen einfachen Ubuntu-Installer. Nach der Installation bleibt der Bot inaktiv, bis der Admin ihn in Telegram aktiviert.

> Rechtlicher Hinweis: Dieses Projekt ist für Tests, Lernen und private Nutzung gedacht. Prüfe vor öffentlicher Nutzung die Plattformregeln, Urheberrechte, Datenschutzregeln und Telegram Bot API Limits.

## Funktionen

- Automatische Link-Erkennung für YouTube, `youtu.be`, Shorts, Instagram und SoundCloud
- Download und Versand von Videos, Fotos, Audio und allgemeinen Dateien über `yt-dlp`
- Unterstützung für Instagram-Posts, Reels, Profile und viele Carousel-Posts
- Instagram-Posts mit mehreren Medien werden als Album/media group gesendet
- Lange Captions werden gekürzt und per Button vollständig abrufbar gemacht
- Vier Sprachversionen im Bot: Persisch, Englisch, Arabisch und Deutsch
- Die Sprache wird nur beim ersten Start gefragt; spätere Änderungen laufen über `/language`
- Admin-Aktivierung direkt in Telegram
- Öffentlicher Zugriff kann mit `/public_on` und `/public_off` geöffnet oder geschlossen werden
- Persönliche Cookies für erlaubte Nutzer und globale Cookies für den Admin
- Admin-gesteuerte Pflichtmitgliedschaft in einem Kanal
- Verbesserter SoundCloud-Versand mit Coverbild, Titel und Künstler
- Installation, Update und vollständige Entfernung per Python-Skripten auf Ubuntu
- Dauerbetrieb über systemd und Service-Logs in `logs/bot.log`

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

## Nutzerbefehle

- `/start` startet den Bot; wenn die Sprache bereits gespeichert ist, kommt nur eine kurze Nachricht
- `/language` oder `/lang` ändert die Nutzersprache
- `/help` zeigt Hilfe
- `/id` zeigt die numerische Telegram-ID
- `/status` zeigt den Bot-Status
- `/cookies` erklärt den Upload persönlicher Cookies
- `/clearcookies` entfernt gespeicherte persönliche Cookies

## Admin-Befehle

- `/admin` öffnet das Admin-Panel
- `/activate` aktiviert Downloads
- `/deactivate` deaktiviert Downloads
- `/public_on` öffnet den öffentlichen Zugriff
- `/public_off` schließt den öffentlichen Zugriff
- `/clearcookies global` entfernt globale Bot-Cookies
- `/forcejoin` zeigt den Status der Pflichtmitgliedschaft
- `/forcejoin_on @channel` aktiviert die Pflichtmitgliedschaft
- `/forcejoin_off` deaktiviert die Pflichtmitgliedschaft

## Öffentlicher Zugriff

Der Bot ist standardmäßig privat. Der Admin kann den öffentlichen Zugriff direkt im Bot öffnen oder schließen:

```text
/public_on
/public_off
```

Wenn öffentlicher Zugriff geschlossen ist, können nur Admin und ausdrücklich erlaubte Nutzer den Bot verwenden.

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

## Cookies Für Instagram Und YouTube

Einige Instagram- oder YouTube-Links benötigen Login. Jeder erlaubte Nutzer kann persönliche Cookies als `cookies.txt` hochladen. Passwörter werden nicht gespeichert; nur die Cookies-Datei bleibt auf dem Server und kann mit `/clearcookies` entfernt werden.

So erstellst du Cookies:

1. Im Browser einloggen.
2. Cookies im Netscape-Format `cookies.txt` exportieren.
3. Die Datei an den Bot senden.

Der Admin kann globale Bot-Cookies speichern, indem `cookies.txt` mit der Caption `global` hochgeladen wird. Entfernen geht mit:

```text
/clearcookies global
```

## CAPTCHA Und "I'm not a robot"

Der Bot umgeht kein CAPTCHA und klickt nicht automatisch auf Prüfungen wie `I'm not a robot`.

Wenn Instagram oder YouTube eine Sicherheitsprüfung verlangt, muss der Nutzer sich manuell im Browser anmelden, die Prüfung manuell lösen, Cookies im Netscape-Format exportieren und `cookies.txt` an den Bot senden. Das reduziert Login-Probleme, garantiert aber nicht, dass eine Plattform nie wieder eine Prüfung verlangt.

## Server-Verwaltung

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

Für App-Update, Dependency-Update und Service-Neustart:

```bash
cd instagram-youtube-soundcloud-downloader
python3 update.py
```

Nur den systemd-Service entfernen:

```bash
python3 uninstall.py
```

Service entfernen und den gesamten Projektordner löschen:

```bash
python3 remove.py
```

`remove.py` fragt vor der vollständigen Entfernung deutlich nach Bestätigung.

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

Instagram, YouTube und SoundCloud können Seiten oder Einschränkungen ändern. Halte `yt-dlp` aktuell und nutze für Updates `python3 update.py`.
