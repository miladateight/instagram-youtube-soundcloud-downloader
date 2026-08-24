# Security policy

## Reporting a vulnerability

Report security issues privately to **ateight088@gmail.com**. Please do not open a public issue for a vulnerability. Include the version, the steps to reproduce, and what an attacker would gain. I aim to acknowledge a report within seven days.

## What this bot handles

The bot is self-hosted. Every secret stays on the machine you install it on — nothing is sent to me or to any third-party service beyond the platforms the bot downloads from.

| Secret | Where it lives | Notes |
| :-- | :-- | :-- |
| Telegram bot token | `.env` as `BOT_TOKEN` | Full control of the bot. Rotate it in BotFather if it leaks. |
| Admin Telegram ID | `.env` | Decides who can enable the bot and manage it. |
| Cookie files | the path you configure | Instagram and YouTube session cookies. |
| Proxy credentials | `.env` | Only when you configure an outbound proxy. |

## Cookie files are account credentials

A `cookies.txt` exported from a logged-in browser is equivalent to a live session for that account. Anyone who reads the file can act as you on that platform until the session expires.

- Keep cookie files outside the repository and outside any backup that syncs to a cloud drive.
- Restrict them to the service user: `chmod 600` and an owner-only parent directory.
- Prefer a throwaway account over your personal one.
- Rotate them by logging out on the source browser, which invalidates the exported session.
- Never attach a cookie file to an issue, a pull request or a chat message.

## Installation hardening

- Run the bot as a dedicated non-root user; the installer's systemd unit is written for that.
- Keep `.env` at `chmod 600`, owned by the service user.
- The bot stays inactive after installation until the admin enables it from inside Telegram; leave it that way until the configuration is finished.
- Restrict who may use the bot with the admin controls rather than exposing it to everyone.

## Reporting scope

In scope: authentication and access-control flaws, secret leakage through logs or error messages, command or path injection in the installer or download paths, and privilege escalation in the systemd unit.

Out of scope: rate limits and terms-of-service decisions made by YouTube, Instagram, SoundCloud or Telegram, and anything that requires an attacker to already have root on the host.
