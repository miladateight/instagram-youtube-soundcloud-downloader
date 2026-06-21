from __future__ import annotations

import asyncio
import logging
import math
import secrets
import time
from contextlib import suppress
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from .config import Settings
from .downloader import Downloader
from .i18n import LANGUAGE_BUTTONS, SUPPORTED_LANGUAGES, normalize_language, t
from .sender import TelegramSender
from .state import BotState
from .utils import (
    detect_platform,
    extract_urls,
    looks_like_cookies_file,
    platform_label,
    short_url_label,
)


def create_dispatcher(settings: Settings) -> Dispatcher:
    settings.download_dir.mkdir(parents=True, exist_ok=True)
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.log_dir.mkdir(parents=True, exist_ok=True)

    dp = Dispatcher()
    state = BotState(settings.data_dir / "bot_state.sqlite3")
    downloader = Downloader(settings)
    user_locks: dict[int, asyncio.Lock] = {}
    last_download_started: dict[int, float] = {}
    user_cooldown_seconds = 5

    def message_user_id(message: Message) -> int:
        return message.from_user.id if message.from_user else 0

    def callback_user_id(callback: CallbackQuery) -> int:
        return callback.from_user.id if callback.from_user else 0

    def is_admin_id(user_id: int) -> bool:
        return user_id == settings.admin_id

    def is_admin(message: Message) -> bool:
        return is_admin_id(message_user_id(message))

    def public_access_enabled() -> bool:
        return state.public_access(settings.allow_all_users)

    def is_allowed(message: Message) -> bool:
        return public_access_enabled() or is_admin(message)

    def default_language(message: Message) -> str:
        language_code = message.from_user.language_code if message.from_user else None
        return normalize_language(language_code)

    def message_language(message: Message) -> str:
        return state.user_language(message_user_id(message), default_language(message))

    def callback_language(callback: CallbackQuery) -> str:
        language_code = callback.from_user.language_code if callback.from_user else None
        return state.user_language(callback_user_id(callback), normalize_language(language_code))

    def active_cookies_path(user_id: int | None = None) -> Path | None:
        if user_id:
            user_path = state.user_cookies_path(user_id)
            if user_path and user_path.exists():
                return user_path
        return global_cookies_path()

    def global_cookies_path() -> Path | None:
        state_path = state.cookies_path()
        if state_path and state_path.exists():
            return state_path
        if settings.cookies_file and settings.cookies_file.exists():
            return settings.cookies_file
        default_path = settings.data_dir / "cookies.txt"
        return default_path if default_path.exists() else None

    def language_keyboard() -> InlineKeyboardMarkup:
        rows = [
            [
                InlineKeyboardButton(text=LANGUAGE_BUTTONS["fa"], callback_data="lang:fa"),
                InlineKeyboardButton(text=LANGUAGE_BUTTONS["en"], callback_data="lang:en"),
            ],
            [
                InlineKeyboardButton(text=LANGUAGE_BUTTONS["ar"], callback_data="lang:ar"),
                InlineKeyboardButton(text=LANGUAGE_BUTTONS["de"], callback_data="lang:de"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def main_keyboard(language: str, *, admin: bool = False) -> InlineKeyboardMarkup:
        rows = [
            [
                InlineKeyboardButton(text=t(language, "button_download"), callback_data="user:download"),
                InlineKeyboardButton(text=t(language, "button_mp3"), callback_data="user:mp3"),
            ],
            [
                InlineKeyboardButton(text=t(language, "button_my_cookies"), callback_data="user:cookies"),
                InlineKeyboardButton(text=t(language, "button_status"), callback_data="user:status"),
            ],
            [
                InlineKeyboardButton(text=t(language, "button_language"), callback_data="user:language"),
            ],
        ]
        if admin:
            rows.append(
                [
                    InlineKeyboardButton(text=t(language, "button_admin_panel"), callback_data="user:admin"),
                ]
            )
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def admin_keyboard(language: str) -> InlineKeyboardMarkup:
        active = state.is_active()
        force_join_enabled = state.is_force_join_enabled()
        rows = [
            [
                InlineKeyboardButton(
                    text=t(language, "button_deactivate") if active else t(language, "button_activate"),
                    callback_data="admin:disable" if active else "admin:activate",
                )
            ],
            [
                InlineKeyboardButton(text=t(language, "button_status"), callback_data="admin:status"),
                InlineKeyboardButton(text=t(language, "button_global_cookies"), callback_data="admin:global_cookies"),
            ],
            [
                InlineKeyboardButton(text=t(language, "button_language"), callback_data="admin:language"),
                InlineKeyboardButton(text=t(language, "button_force_join"), callback_data="admin:forcejoin"),
            ],
            [
                InlineKeyboardButton(text=t(language, "button_cookies"), callback_data="admin:cookies"),
                InlineKeyboardButton(
                    text=t(language, "button_clear_global_cookies"),
                    callback_data="admin:clear_global_cookies",
                ),
            ],
        ]
        if force_join_enabled:
            rows.append(
                [
                    InlineKeyboardButton(
                        text=t(language, "button_force_join_off"),
                        callback_data="admin:forcejoin_off",
                    )
                ]
            )
        rows.append(
            [
                InlineKeyboardButton(
                    text=t(language, "button_public_off")
                    if public_access_enabled()
                    else t(language, "button_public_on"),
                    callback_data="admin:public_off" if public_access_enabled() else "admin:public_on",
                )
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def force_join_keyboard(language: str) -> InlineKeyboardMarkup:
        channel = state.force_join_chat()
        rows = []
        if channel and channel.startswith("@"):
            rows.append(
                [
                    InlineKeyboardButton(
                        text=t(language, "join_channel"),
                        url=f"https://t.me/{channel.removeprefix('@')}",
                    )
                ]
            )
        rows.append(
            [
                InlineKeyboardButton(
                    text=t(language, "check_membership"),
                    callback_data="check_sub",
                )
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def status_label(language: str, enabled: bool) -> str:
        return t(language, "enabled") if enabled else t(language, "disabled")

    def status_text(language: str) -> str:
        cookies = global_cookies_path()
        force_join_chat = state.force_join_chat() or t(language, "force_join_not_set")
        return t(
            language,
            "status",
            bot_name=settings.bot_name,
            active=status_label(language, state.is_active()),
            public_access=status_label(language, public_access_enabled()),
            force_join=status_label(language, state.is_force_join_enabled()),
            force_join_channel=force_join_chat,
            upload_limit=t(language, "unlimited")
            if settings.max_upload_mb <= 0
            else f"{settings.max_upload_mb}MB",
            playlist_limit=settings.playlist_limit,
            concurrent_downloads=settings.concurrent_downloads,
            cookies=t(language, "cookies_set") if cookies else t(language, "cookies_not_set"),
        )

    def user_status_text(user_id: int, language: str) -> str:
        user_cookies = state.user_cookies_path(user_id)
        cookies_ok = bool(user_cookies and user_cookies.exists())
        global_cookies_ok = bool(global_cookies_path())
        return t(
            language,
            "user_status",
            cookies=t(language, "cookies_set") if cookies_ok else t(language, "cookies_not_set"),
            global_cookies=t(language, "cookies_set")
            if global_cookies_ok
            else t(language, "cookies_not_set"),
        )

    def clear_global_cookies() -> None:
        cookies = state.cookies_path() or (settings.data_dir / "cookies.txt")
        with suppress(OSError):
            if cookies.exists() and cookies.is_file():
                cookies.unlink()
        state.clear_cookies_path()

    def force_join_status_text(language: str) -> str:
        channel = state.force_join_chat() or t(language, "force_join_not_set")
        return t(
            language,
            "force_join_status",
            status=status_label(language, state.is_force_join_enabled()),
            channel=channel,
        )

    def normalize_force_join_chat(raw: str) -> str:
        value = raw.strip()
        if value.startswith("https://t.me/"):
            username = value.removeprefix("https://t.me/").strip("/")
            if username and not username.startswith("+"):
                return "@" + username
        if value.startswith("http://t.me/"):
            username = value.removeprefix("http://t.me/").strip("/")
            if username and not username.startswith("+"):
                return "@" + username
        return value

    def friendly_error(exc: Exception, language: str) -> str:
        raw = str(exc)
        lowered = raw.lower()

        if any(token in lowered for token in ("captcha", "not a robot", "verify you are human")):
            return t(language, "captcha_error")
        if any(token in lowered for token in ("login", "cookie", "cookies", "sign in")):
            return t(language, "login_error")
        if any(token in lowered for token in ("private", "not available", "unavailable")):
            return t(language, "private_error")
        if any(
            token in lowered
            for token in (
                "larger than max-filesize",
                "file is larger",
                "file is too big",
                "too large",
                "request entity too large",
            )
        ):
            return t(language, "telegram_size_error")
        if "ffmpeg" in lowered:
            return t(language, "ffmpeg_error")
        if "unsupported url" in lowered:
            return t(language, "unsupported_error")

        return raw[:900] if raw else t(language, "unknown_error")

    def progress_bar(percent: int) -> str:
        filled = max(0, min(10, percent // 10))
        return ("#" * filled) + ("-" * (10 - filled))

    async def edit_status(message: Message, text: str) -> None:
        with suppress(Exception):
            await message.edit_text(text)

    async def animate_progress(
        status_message: Message,
        language: str,
        platform: str,
        url: str,
        finished: asyncio.Event,
    ) -> None:
        percent = 0
        while not finished.is_set():
            await edit_status(
                status_message,
                t(
                    language,
                    "progress",
                    percent=percent,
                    bar=progress_bar(percent),
                    platform=platform,
                    url=url,
                ),
            )
            if percent < 90:
                percent = min(90, percent + 10)
                await asyncio.sleep(1.2)
            else:
                await asyncio.sleep(3)
        await edit_status(
            status_message,
            t(
                language,
                "progress",
                percent=100,
                bar=progress_bar(100),
                platform=platform,
                url=url,
            ),
        )

    async def is_subscribed(bot: Bot, user_id: int) -> bool | None:
        if not state.is_force_join_enabled():
            return True
        channel = state.force_join_chat()
        if not channel:
            return True
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        except Exception:
            logging.exception("Could not verify forced subscription for %s in %s", user_id, channel)
            return None
        status = getattr(member.status, "value", str(member.status))
        if status in {"creator", "administrator", "member"}:
            return True
        if status == "restricted":
            return bool(getattr(member, "is_member", False))
        return False

    async def reject_if_needed(message: Message, bot: Bot) -> bool:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return True

        if not state.is_active():
            if is_admin(message):
                await message.answer(
                    t(language, "bot_not_active_admin"),
                    reply_markup=admin_keyboard(language),
                )
            else:
                await message.answer(t(language, "bot_not_active_user"))
            return True

        if not is_admin(message) and state.is_force_join_enabled() and state.force_join_chat():
            subscribed = await is_subscribed(bot, message_user_id(message))
            if subscribed is True:
                return False
            if subscribed is None:
                await message.answer(t(language, "membership_check_failed"))
                return True
            await message.answer(t(language, "must_join"), reply_markup=force_join_keyboard(language))
            return True

        return False

    async def send_start_help(message: Message, bot: Bot) -> None:
        language = message_language(message)
        if not state.has_user_language(message_user_id(message)):
            await message.answer(t(language, "choose_language"), reply_markup=language_keyboard())
            return

        if is_admin(message):
            await message.answer(t(language, "start_ready"), reply_markup=main_keyboard(language, admin=True))
            return

        if not state.is_active():
            await message.answer(t(language, "bot_not_active_user"), reply_markup=main_keyboard(language))
            return

        if state.is_force_join_enabled() and state.force_join_chat():
            subscribed = await is_subscribed(bot, message_user_id(message))
            if subscribed is False:
                await message.answer(t(language, "must_join"), reply_markup=force_join_keyboard(language))
                return
            if subscribed is None:
                await message.answer(t(language, "membership_check_failed"))
                return

        await message.answer(t(language, "start_ready"), reply_markup=main_keyboard(language))

    @dp.message(CommandStart())
    async def start(message: Message, bot: Bot) -> None:
        if not is_allowed(message):
            language = message_language(message)
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return
        await send_start_help(message, bot)

    @dp.message(Command("language", "lang"))
    async def language_command(message: Message) -> None:
        language = message_language(message)
        await message.answer(t(language, "choose_language"), reply_markup=language_keyboard())

    @dp.callback_query(F.data.startswith("lang:"))
    async def language_callback(callback: CallbackQuery) -> None:
        language = callback.data.split(":", 1)[1] if callback.data else "fa"
        if language not in SUPPORTED_LANGUAGES:
            language = "fa"
        state.set_user_language(callback_user_id(callback), language)
        if callback.message:
            await callback.message.answer(
                t(language, "language_selected"),
                reply_markup=main_keyboard(language, admin=is_admin_id(callback_user_id(callback))),
            )
        await callback.answer()

    @dp.message(Command("help"))
    async def help_command(message: Message) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return
        text = t(language, "help") + ("\n\n" + t(language, "admin_help") if is_admin(message) else "")
        await message.answer(text, reply_markup=admin_keyboard(language) if is_admin(message) else main_keyboard(language))

    @dp.message(Command("id"))
    async def id_command(message: Message) -> None:
        await message.answer(t(message_language(message), "your_id", id=message_user_id(message)))

    @dp.message(Command("admin"))
    async def admin_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "admin_only"))
            return
        await message.answer(
            t(language, "admin_help") + "\n\n" + status_text(language),
            reply_markup=admin_keyboard(language),
        )

    @dp.message(Command("activate"))
    async def activate_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        state.set_active(True)
        await message.answer(t(language, "bot_activated"), reply_markup=admin_keyboard(language))

    @dp.message(Command("deactivate"))
    async def deactivate_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        state.set_active(False)
        await message.answer(t(language, "bot_deactivated"), reply_markup=admin_keyboard(language))

    @dp.message(Command("cookies"))
    async def cookies_command(message: Message) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return
        await message.answer(t(language, "cookie_help"), reply_markup=main_keyboard(language, admin=is_admin(message)))

    @dp.message(Command("clearcookies"))
    async def clear_cookies_command(message: Message) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return

        if is_admin(message) and "global" in (message.text or "").lower():
            clear_global_cookies()
            await message.answer(t(language, "global_cookies_cleared"), reply_markup=admin_keyboard(language))
            return

        cookies = state.user_cookies_path(message_user_id(message))
        with suppress(OSError):
            if cookies and cookies.exists() and cookies.is_file():
                cookies.unlink()
        state.clear_user_cookies_path(message_user_id(message))
        await message.answer(t(language, "personal_cookies_cleared"), reply_markup=main_keyboard(language, admin=is_admin(message)))

    @dp.message(Command("public_on", "publicon"))
    async def public_on_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        state.set_public_access(True)
        await message.answer(t(language, "public_enabled"), reply_markup=admin_keyboard(language))

    @dp.message(Command("public_off", "publicoff"))
    async def public_off_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        state.set_public_access(False)
        await message.answer(t(language, "public_disabled"), reply_markup=admin_keyboard(language))

    @dp.message(Command("forcejoin"))
    async def force_join_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        await message.answer(force_join_status_text(language), reply_markup=admin_keyboard(language))

    @dp.message(Command("forcejoin_on", "forcejoinon", "setchannel"))
    async def force_join_on_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        parts = (message.text or "").split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await message.answer(t(language, "force_join_missing_channel"))
            return
        channel = normalize_force_join_chat(parts[1])
        state.set_force_join_chat(channel)
        state.set_force_join_enabled(True)
        await message.answer(
            t(language, "force_join_enabled", channel=channel),
            reply_markup=admin_keyboard(language),
        )

    @dp.message(Command("forcejoin_off", "forcejoinoff"))
    async def force_join_off_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        state.set_force_join_enabled(False)
        await message.answer(t(language, "force_join_disabled"), reply_markup=admin_keyboard(language))

    @dp.message(Command("status"))
    async def status_command(message: Message) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return
        if is_admin(message):
            await message.answer(status_text(language), reply_markup=admin_keyboard(language))
        else:
            await message.answer(
                user_status_text(message_user_id(message), language),
                reply_markup=main_keyboard(language),
            )

    @dp.callback_query(F.data == "check_sub")
    async def check_subscription_callback(callback: CallbackQuery, bot: Bot) -> None:
        language = callback_language(callback)
        result = await is_subscribed(bot, callback_user_id(callback))
        if result is True:
            await callback.answer(t(language, "membership_ok"), show_alert=True)
            if callback.message:
                await callback.message.answer(t(language, "membership_ok"))
        elif result is False:
            await callback.answer(t(language, "membership_missing"), show_alert=True)
        else:
            await callback.answer(t(language, "membership_check_failed"), show_alert=True)

    @dp.callback_query(F.data.startswith("user:"))
    async def user_callback(callback: CallbackQuery) -> None:
        language = callback_language(callback)
        action = callback.data.split(":", 1)[1] if callback.data else ""
        is_admin_user = is_admin_id(callback_user_id(callback))
        reply_markup: InlineKeyboardMarkup | None = main_keyboard(language, admin=is_admin_user)
        if action == "download":
            text = t(language, "download_button_hint")
        elif action == "mp3":
            text = t(language, "mp3_help")
        elif action == "cookies":
            text = t(language, "cookie_help")
        elif action == "status":
            text = user_status_text(callback_user_id(callback), language)
        elif action == "language":
            text = t(language, "choose_language")
            reply_markup = language_keyboard()
        elif action == "admin" and is_admin_user:
            text = t(language, "admin_help") + "\n\n" + status_text(language)
            reply_markup = admin_keyboard(language)
        else:
            text = t(language, "start_ready")
        if callback.message:
            await callback.message.answer(text, reply_markup=reply_markup)
        await callback.answer()

    @dp.callback_query(F.data.startswith("admin:"))
    async def admin_callback(callback: CallbackQuery) -> None:
        language = callback_language(callback)
        if not is_admin_id(callback_user_id(callback)):
            await callback.answer(t(language, "only_admin_access"), show_alert=True)
            return

        action = callback.data.split(":", 1)[1] if callback.data else ""
        reply_markup: InlineKeyboardMarkup | None = admin_keyboard(language)
        if action == "activate":
            state.set_active(True)
            text = t(language, "bot_activated") + "\n\n" + status_text(language)
        elif action == "disable":
            state.set_active(False)
            text = t(language, "bot_deactivated") + "\n\n" + status_text(language)
        elif action == "cookies":
            text = t(language, "cookie_help")
            reply_markup = admin_keyboard(language)
        elif action == "global_cookies":
            text = t(language, "global_cookie_help")
            reply_markup = admin_keyboard(language)
        elif action == "clear_global_cookies":
            clear_global_cookies()
            text = t(language, "global_cookies_cleared")
            reply_markup = admin_keyboard(language)
        elif action == "language":
            text = t(language, "choose_language")
            reply_markup = language_keyboard()
        elif action == "forcejoin":
            text = force_join_status_text(language)
        elif action == "forcejoin_off":
            state.set_force_join_enabled(False)
            text = t(language, "force_join_disabled") + "\n\n" + force_join_status_text(language)
        elif action == "public_on":
            state.set_public_access(True)
            text = t(language, "public_enabled") + "\n\n" + status_text(language)
        elif action == "public_off":
            state.set_public_access(False)
            text = t(language, "public_disabled") + "\n\n" + status_text(language)
        else:
            text = status_text(language)

        if callback.message:
            await callback.message.answer(text, reply_markup=reply_markup)
        await callback.answer()

    @dp.message(F.document)
    async def handle_document(message: Message, bot: Bot) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"))
            return

        document = message.document
        if not document:
            return

        filename = (document.file_name or "").lower()
        caption = (message.caption or "").lower()
        wants_cookie_upload = "cookie" in filename or "/cookies" in caption
        if not wants_cookie_upload:
            await message.answer(t(language, "cookie_upload_hint"))
            return

        if document.file_size and document.file_size > 5 * 1024 * 1024:
            await message.answer(t(language, "cookies_too_large"))
            return

        is_global_cookie = is_admin(message) and "global" in caption
        if is_global_cookie:
            target = settings.data_dir / "cookies.txt"
        else:
            target = settings.data_dir / "user_cookies" / f"{message_user_id(message)}.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        temp_target = target.with_suffix(".upload")
        with suppress(OSError):
            temp_target.unlink()

        await bot.download(document, destination=temp_target)
        if not looks_like_cookies_file(temp_target):
            with suppress(OSError):
                temp_target.unlink()
            await message.answer(t(language, "invalid_cookies"))
            return

        temp_target.replace(target)
        if is_global_cookie:
            state.set_cookies_path(target)
            await message.answer(t(language, "global_cookies_saved"), reply_markup=admin_keyboard(language))
        else:
            state.set_user_cookies_path(message_user_id(message), target)
            await message.answer(t(language, "personal_cookies_saved"), reply_markup=main_keyboard(language, admin=is_admin(message)))

    @dp.callback_query(F.data.startswith("caption:"))
    async def caption_callback(callback: CallbackQuery) -> None:
        language = callback_language(callback)
        caption_id = callback.data.split(":", 1)[1] if callback.data else ""
        caption = state.caption(caption_id)
        if not caption:
            await callback.answer(t(language, "caption_unavailable"), show_alert=True)
            return
        if callback.message:
            for start in range(0, len(caption), 3900):
                await callback.message.answer(caption[start : start + 3900])
        await callback.answer()

    async def process_downloads(
        message: Message,
        bot: Bot,
        urls: list[str],
        *,
        audio_only: bool = False,
    ) -> None:
        language = message_language(message)
        if await reject_if_needed(message, bot):
            return

        user_id = message_user_id(message)
        now = time.monotonic()
        remaining = math.ceil((last_download_started.get(user_id, 0) + user_cooldown_seconds) - now)
        lock = user_locks.setdefault(user_id, asyncio.Lock())
        if lock.locked():
            await message.answer(t(language, "download_already_running"))
            return
        if remaining > 0:
            await message.answer(t(language, "download_cooldown", seconds=remaining))
            return
        last_download_started[user_id] = now

        async with lock:
            if len(urls) > 1:
                await message.answer(t(language, "multiple_links", count=len(urls)))

            sender = TelegramSender(bot, settings, state)
            for url in urls:
                platform = detect_platform(url)
                platform_name = platform_label(platform)
                url_label = short_url_label(url)
                status_message = await message.answer(
                    t(
                        language,
                        "preparing_audio" if audio_only else "preparing",
                        platform=platform_name,
                        url=url_label,
                    )
                )
                result = None
                finished = asyncio.Event()
                progress_task = asyncio.create_task(
                    animate_progress(status_message, language, platform_name, url_label, finished)
                )
                try:
                    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
                    cookies_path = active_cookies_path(user_id)
                    result = await downloader.download(url, cookies_path, audio_only=audio_only)
                    finished.set()
                    await progress_task
                    await status_message.edit_text(t(language, "uploading"))
                    await sender.send_result(
                        message.chat.id,
                        result,
                        language,
                        secrets.token_urlsafe(8),
                    )
                    with suppress(Exception):
                        await status_message.delete()
                except Exception as exc:
                    finished.set()
                    with suppress(Exception):
                        await progress_task
                    logging.exception("Download failed for %s", url)
                    await status_message.edit_text(
                        t(language, "download_failed", error=friendly_error(exc, language))
                    )
                finally:
                    if result is not None:
                        Downloader.cleanup(result.workdir)

    @dp.message(Command("mp3", "audio"))
    async def mp3_command(message: Message, bot: Bot) -> None:
        language = message_language(message)
        urls = extract_urls(message.text or "")
        if not urls:
            await message.answer(t(language, "mp3_help"), reply_markup=main_keyboard(language, admin=is_admin(message)))
            return
        urls = [url for url in urls if detect_platform(url)]
        if not urls:
            await message.answer(t(language, "unsupported_links"))
            return
        await process_downloads(message, bot, urls, audio_only=True)

    @dp.message(F.text)
    async def handle_text(message: Message, bot: Bot) -> None:
        language = message_language(message)
        if await reject_if_needed(message, bot):
            return

        urls = extract_urls(message.text or "")
        if not urls:
            await message.answer(t(language, "send_supported_link"), reply_markup=main_keyboard(language, admin=is_admin(message)))
            return

        unsupported = [url for url in urls if not detect_platform(url)]
        if unsupported:
            await message.answer(t(language, "unsupported_links"))
            urls = [url for url in urls if detect_platform(url)]
            if not urls:
                return

        await process_downloads(message, bot, urls)

    return dp


async def run_bot(settings: Settings) -> None:
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(settings.log_dir / "bot.log", encoding="utf-8"),
        ],
    )
    bot = Bot(settings.bot_token)
    await setup_bot_commands(bot, settings)
    dp = create_dispatcher(settings)
    await dp.start_polling(bot)


async def setup_bot_commands(bot: Bot, settings: Settings) -> None:
    user_commands = [
        BotCommand(command="start", description="Open buttons"),
        BotCommand(command="mp3", description="Download audio as MP3"),
        BotCommand(command="language", description="Change language"),
        BotCommand(command="cookies", description="Upload cookies guide"),
        BotCommand(command="clearcookies", description="Remove my cookies"),
        BotCommand(command="status", description="My cookies status"),
    ]
    admin_commands = [
        *user_commands,
        BotCommand(command="admin", description="Admin panel"),
        BotCommand(command="activate", description="Enable downloads"),
        BotCommand(command="deactivate", description="Disable downloads"),
        BotCommand(command="public_on", description="Open public access"),
        BotCommand(command="public_off", description="Close public access"),
        BotCommand(command="forcejoin_on", description="Enable forced join"),
        BotCommand(command="forcejoin_off", description="Disable forced join"),
    ]
    try:
        await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=settings.admin_id))
    except Exception:
        logging.exception("Could not set Telegram command menu")
