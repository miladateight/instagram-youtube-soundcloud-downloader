# Atieght Downloader

**Sprache:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

**Version 1.0.0**

Ein privater, portfolio-tauglicher Telegram-Bot zum Herunterladen von Medien von YouTube, YouTube Shorts, Instagram und SoundCloud — mit Inline-Buttons, Liederkennung und einem interaktiven Installer.

Das Projekt ist vollständig in Python geschrieben und enthält einen einfachen Ubuntu-Installer mit einer Feature-Checkliste. Der Bot bleibt nach der Installation inaktiv, bis der Administrator ihn aus Telegram heraus aktiviert.

> Rechtlicher Hinweis: Dieses Projekt ist für Tests, Lernen und persönliche Nutzung gedacht. Vor öffentlicher oder produktiver Nutzung müssen die Plattform-Bedingungen, Urheberrechtsregeln, Datenschutzregeln und Telegram-Bot-API-Limits geprüft werden.

## Funktionen

### Download
- Automatische Link-Erkennung für YouTube, `youtu.be`, Shorts, `m.youtube.com`, `music.youtube.com`, Instagram und SoundCloud
- Video-, Foto-, Audio- und Dokumentlieferung über `yt-dlp`
- Instagram-Posts, Reels, Profile und viele Carousel-Posts
- Instagram-Multi-Item-Posts als Telegram-Alben/Mediagruppen gesendet
- **Korrekte Videoabmessungen** — Reels und Shorts behalten ihr ursprüngliches Seitenverhältnis
- YouTube-Video-Downloads bevorzugen Telegram-freundliches MP4 statt WebM
- SoundCloud: beste Audioqualität für Tracks unter 15 Minuten, Cover-Art wird separat vor dem Audio gesendet
- Beschriftung wird zur ersten hochgeladenen Datei hinzugefügt
- Lange Beschriftungen werden sicher gekürzt mit einem "Vollständige Beschriftung abrufen"-Button
- Fallback auf Dokument-Upload, wenn eine Datei zu groß für Telegram ist

### Benutzererfahrung
- **Inline-Glas-Buttons** — nach dem Senden eines Links fragt der Bot, was du willst: Video, Audio (MP3) oder Lied finden
- **Reply-Keyboard-Menü** — dauerhafte Buttons unten: Download, MP3, Status, Sprache, Teilen, Support
- **Liederkennung** — erkennt das Lied in einem Video mit Shazam (kostenlos, kein API-Schlüssel erforderlich)
- **Support-Button** — Nutzer können den Administrator direkt aus jeder Fehlermeldung kontaktieren
- **Teilen-Button** — Nutzer können den Bot an Freunde weiterleiten
- Echter Download-Fortschritt (mit yt-dlp progress hooks)
- Anti-Spam-Schutz pro Nutzer: ein aktiver Download und eine neue Anfrage alle 5 Sekunden
- Bot-UI in vier Sprachen: Persisch, Englisch, Arabisch und Deutsch
- Einmalige Sprachauswahl, mit manuellen Änderungen über `/language`
- Kategorisierte Fehlermeldungen (keine rohen yt-dlp-Fehler werden Nutzern angezeigt)

### Administrator
- Aktivierung aus Telegram heraus
- Persönliche `cookies.txt`-Uploads und -Entfernung pro Nutzer
- Optionale globale `cookies.txt` für den Administrator
- Vom Administrator gesteuerter erzwungener Kanal-Beitritt
- Standardmäßig privater Zugriff, mit öffentlichem Modus gesteuert vom Admin-Panel
- Feature-Toggles: YouTube, Instagram, SoundCloud oder Liederkennung aktivieren/deaktivieren

### Installer
- **Interaktive Feature-Checkliste** (whiptail auf Linux, Text-Fallback anderswo)
- Atieght ASCII-Art-Banner
- Fragt nach Bot-Name, Token, Admin-ID, Support-Username und Bot-Username
- Auswahl welche Plattformen und Features aktiviert werden sollen
- Optionaler benutzerdefinierter Shazam-API-Schlüssel
- Python-Installer und systemd-Service für Ubuntu
- Update- und vollständige Entfernungsskripte für Ubuntu-Server
- Service-Logs in `logs/bot.log`

## Schnellinstallation auf Ubuntu

```bash
bash -c 'set -e; repo=instagram-youtube-soundcloud-downloader; if [ -f install.py ] && [ -d .git ]; then python3 install.py; elif [ -d "$repo/.git" ]; then cd "$repo" && python3 install.py; elif [ -e "$repo" ]; then echo "$repo already exists but is not a git checkout. Remove it first or choose another directory."; exit 1; else git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git "$repo" && cd "$repo" && python3 install.py; fi'
```

`python3 install.py` ist auch der Update-Befehl. Wenn `.env` bereits existiert, werden Abhängigkeiten aktualisiert, der neueste Code gezogen und der Service neu gestartet:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```

Der Installer fragt nach:

- Bot-Name (Standard: Atieght Downloader)
- Bot-Token von BotFather
- Numerische Telegram-Admin-ID
- Admin-Telegram-Username für den Support-Button (optional)
- Bot-Username für den Teilen-Button (optional)
- Welche Plattformen aktiviert werden sollen (YouTube, Instagram, SoundCloud)
- Ob Liederkennung (Shazam) aktiviert werden soll
- Optionaler benutzerdefinierter Shazam-API-Schlüssel

Nach der Installation öffne den Bot in Telegram als Administrator und sende:

```text
/activate
```

Der Bot lädt nichts herunter, bis er aktiviert ist.

## Bot-Befehle

- `/start` startet den Bot; Sprache wird nur einmal abgefragt
- `/language` oder `/lang` ändert die Nutzersprache
- `/help` zeigt den Hilfetext
- `/id` zeigt die numerische Telegram-ID des Nutzers
- `/mp3 <link>` sendet nur Audio als MP3
- `/status` zeigt persönlichen Cookies-Status für Nutzer und vollen Status für den Admin
- `/admin` öffnet das Admin-Panel
- `/activate` aktiviert Downloads
- `/deactivate` deaktiviert Downloads
- `/public_on` öffnet öffentlichen Zugriff
- `/public_off` schließt öffentlichen Zugriff
- `/cookies` erklärt, wie man Cookies hochlädt
- `/clearcookies` entfernt persönliche Cookies
- `/clearcookies global` entfernt globale Admin-Cookies
- `/forcejoin` zeigt Status des erzwungenen Beitrags
- `/forcejoin_on @channel` aktiviert erzwungenen Beitrag
- `/forcejoin_off` deaktiviert erzwungenen Beitrag
- `/support` zeigt den Support-Button
- `/share` zeigt eine bereit-to-forward Teilen-Nachricht
- `/about` zeigt Bot-Info und Version

## Wie es funktioniert

1. **Link senden** — füge einen YouTube-, Instagram- oder SoundCloud-Link ein
2. **Format wählen** — der Bot zeigt Inline-Buttons: Video, Audio (MP3) oder Lied finden
3. **Ergebnis erhalten** — der Bot lädt herunter und sendet die Medien mit korrekten Abmessungen und Thumbnail

Für SoundCloud lädt der Bot Audio automatisch herunter (keine Buttons) und sendet die Cover-Art separat vor dem Audio.

## Erzwungener Beitrag

Der Administrator kann verlangen, dass Nutzer einem Telegram-Kanal beitreten, bevor sie herunterladen.

```text
/forcejoin_on @your_channel
```

Zum Deaktivieren:

```text
/forcejoin_off
```

Der Bot muss Mitglied oder Admin im erforderlichen Kanal sein, damit Telegram die Mitgliedschaft verifizieren kann. Admin-Nutzer werden nicht durch erzwungenen Beitrag blockiert.

## Service-Verwaltung

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

Bot aktualisieren:

```bash
python3 install.py
```

Nur den systemd-Service deinstallieren:

```bash
python3 uninstall.py
```

Service entfernen und Projektverzeichnis löschen:

```bash
python3 remove.py
```

## Entwicklungsausführung

```bash
cp .env.example .env
nano .env
python3 run.py
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## Cookies für Instagram und YouTube

Einige Instagram- oder YouTube-Links erfordern möglicherweise eine Anmeldung. Jeder erlaubte Nutzer kann eine persönliche `cookies.txt`-Datei aus Telegram heraus hochladen:

1. Melde dich in einem Browser an.
2. Exportiere Cookies im Netscape `cookies.txt`-Format.
3. Sende die Datei an den Bot.

Wenn der Dateiname nicht klar ist, sende sie mit dieser Beschriftung:

```text
/cookies
```

Der Bot speichert persönliche Cookies in `data/user_cookies/`. Passwörter werden nicht gespeichert; nur die exportierte Cookies-Datei bleibt auf dem Server. Ein Nutzer kann persönliche Cookies mit `/clearcookies` entfernen.

Der Administrator kann globale Bot-Cookies hochladen, indem er `cookies.txt` mit der Beschriftung sendet:

```text
global
```

Globale Admin-Cookies werden in `data/cookies.txt` gespeichert und können mit `/clearcookies global` entfernt werden. Cookie-Dateien sind sensibel und werden von Git ignoriert.

## CAPTCHA und "Ich bin kein Roboter"

Der Bot umgeht kein CAPTCHA und klickt nicht automatisch auf Verifizierungsaufforderungen wie "Ich bin kein Roboter".

Wenn Instagram oder YouTube eine Sicherheitsabfrage verlangt:

1. Der Nutzer oder Administrator meldet sich manuell in einem Browser an.
2. Die Abfrage wird manuell im Browser gelöst.
3. Cookies werden im Netscape `cookies.txt`-Format exportiert.
4. Die Cookies-Datei wird zum Bot hochgeladen.

## `.env`-Einstellungen

```env
BOT_NAME=Atieght Downloader
BOT_TOKEN=123456789:replace-me
ADMIN_ID=123456789
SUPPORT_USERNAME=
BOT_USERNAME=
ALLOW_ALL_USERS=false
MAX_UPLOAD_MB=0
PLAYLIST_LIMIT=20
CONCURRENT_DOWNLOADS=100
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

## Beispiel-Links

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

## Download-Unterstützung gesund halten

Instagram, YouTube und SoundCloud können ihre Seiten oder Einschränkungen ändern. Halte den Bot und `yt-dlp` aktualisiert:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```