from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart
from aiogram.types import (
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
    semaphore = asyncio.Semaphore(settings.concurrent_downloads)

    def message_user_id(message: Message) -> int:
        return message.from_user.id if message.from_user else 0

    def callback_user_id(callback: CallbackQuery) -> int:
        return callback.from_user.id if callback.from_user else 0

    def is_admin_id(user_id: int) -> bool:
        return user_id == settings.admin_id

    def is_admin(message: Message) -> bool:
        return is_admin_id(message_user_id(message))

    def is_allowed(message: Message) -> bool:
        return settings.allow_all_users or is_admin(message)

    def default_language(message: Message) -> str:
        language_code = message.from_user.language_code if message.from_user else None
        return normalize_language(language_code)

    def message_language(message: Message) -> str:
        return state.user_language(message_user_id(message), default_language(message))

    def callback_language(callback: CallbackQuery) -> str:
        language_code = callback.from_user.language_code if callback.from_user else None
        return state.user_language(callback_user_id(callback), normalize_language(language_code))

    def active_cookies_path() -> Path | None:
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
                InlineKeyboardButton(text=t(language, "button_cookies"), callback_data="admin:cookies"),
            ],
            [
                InlineKeyboardButton(text=t(language, "button_language"), callback_data="admin:language"),
                InlineKeyboardButton(text=t(language, "button_force_join"), callback_data="admin:forcejoin"),
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
        cookies = active_cookies_path()
        force_join_chat = state.force_join_chat() or t(language, "force_join_not_set")
        return t(
            language,
            "status",
            bot_name=settings.bot_name,
            active=status_label(language, state.is_active()),
            public_access=status_label(language, settings.allow_all_users),
            force_join=status_label(language, state.is_force_join_enabled()),
            force_join_channel=force_join_chat,
            max_upload_mb=settings.max_upload_mb,
            playlist_limit=settings.playlist_limit,
            concurrent_downloads=settings.concurrent_downloads,
            cookies=t(language, "cookies_set") if cookies else t(language, "cookies_not_set"),
        )

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
        if any(token in lowered for token in ("larger than max-filesize", "file is larger")):
            return t(language, "size_error", limit=settings.max_upload_mb)
        if "ffmpeg" in lowered:
            return t(language, "ffmpeg_error")
        if "unsupported url" in lowered:
            return t(language, "unsupported_error")

        return raw[:900] if raw else t(language, "unknown_error")

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
        await message.answer(t(language, "choose_language"), reply_markup=language_keyboard())

        if is_admin(message):
            await message.answer(
                t(language, "help") + "\n\n" + t(language, "admin_help"),
                reply_markup=admin_keyboard(language),
            )
            return

        if not state.is_active():
            await message.answer(t(language, "bot_not_active_user"))
            return

        if state.is_force_join_enabled() and state.force_join_chat():
            subscribed = await is_subscribed(bot, message_user_id(message))
            if subscribed is False:
                await message.answer(t(language, "must_join"), reply_markup=force_join_keyboard(language))
                return
            if subscribed is None:
                await message.answer(t(language, "membership_check_failed"))
                return

        await message.answer(t(language, "help"))

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
            await callback.message.answer(t(language, "language_selected"), reply_markup=language_keyboard())
        await callback.answer()

    @dp.message(Command("help"))
    async def help_command(message: Message) -> None:
        language = message_language(message)
        if not is_allowed(message):
            await message.answer(t(language, "private_bot"), reply_markup=language_keyboard())
            return
        text = t(language, "help") + ("\n\n" + t(language, "admin_help") if is_admin(message) else "")
        await message.answer(text, reply_markup=admin_keyboard(language) if is_admin(message) else None)

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
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        await message.answer(t(language, "cookie_help"))

    @dp.message(Command("clearcookies"))
    async def clear_cookies_command(message: Message) -> None:
        language = message_language(message)
        if not is_admin(message):
            await message.answer(t(language, "command_admin_only"))
            return
        cookies = state.cookies_path() or (settings.data_dir / "cookies.txt")
        with suppress(OSError):
            if cookies.exists() and cookies.is_file():
                cookies.unlink()
        state.clear_cookies_path()
        await message.answer(t(language, "cookies_cleared"))

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
        await message.answer(status_text(language), reply_markup=admin_keyboard(language) if is_admin(message) else None)

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
            reply_markup = None
        elif action == "language":
            text = t(language, "choose_language")
            reply_markup = language_keyboard()
        elif action == "forcejoin":
            text = force_join_status_text(language)
        elif action == "forcejoin_off":
            state.set_force_join_enabled(False)
            text = t(language, "force_join_disabled") + "\n\n" + force_join_status_text(language)
        else:
            text = status_text(language)

        if callback.message:
            await callback.message.answer(text, reply_markup=reply_markup)
        await callback.answer()

    @dp.message(F.document)
    async def handle_document(message: Message, bot: Bot) -> None:
        language = message_language(message)
        if not is_admin(message):
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

        target = settings.data_dir / "cookies.txt"
        temp_target = settings.data_dir / "cookies.upload"
        with suppress(OSError):
            temp_target.unlink()

        await bot.download(document, destination=temp_target)
        if not looks_like_cookies_file(temp_target):
            with suppress(OSError):
                temp_target.unlink()
            await message.answer(t(language, "invalid_cookies"))
            return

        temp_target.replace(target)
        state.set_cookies_path(target)
        await message.answer(t(language, "cookies_saved"))

    @dp.message(F.text)
    async def handle_text(message: Message, bot: Bot) -> None:
        language = message_language(message)
        if await reject_if_needed(message, bot):
            return

        urls = extract_urls(message.text or "")
        if not urls:
            await message.answer(t(language, "send_supported_link"))
            return

        unsupported = [url for url in urls if not detect_platform(url)]
        if unsupported:
            await message.answer(t(language, "unsupported_links"))
            urls = [url for url in urls if detect_platform(url)]
            if not urls:
                return

        if len(urls) > 1:
            await message.answer(t(language, "multiple_links", count=len(urls)))

        sender = TelegramSender(bot, settings)
        for url in urls:
            platform = detect_platform(url)
            status_message = await message.answer(
                t(
                    language,
                    "preparing",
                    platform=platform_label(platform),
                    url=short_url_label(url),
                )
            )
            result = None
            try:
                async with semaphore:
                    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
                    cookies_path = active_cookies_path()
                    await status_message.edit_text(
                        t(
                            language,
                            "downloading",
                            platform=platform_label(platform),
                            url=short_url_label(url),
                        )
                    )
                    result = await downloader.download(url, cookies_path)
                    await status_message.edit_text(t(language, "uploading"))
                    await sender.send_result(message.chat.id, result, language)
                    with suppress(Exception):
                        await status_message.delete()
            except Exception as exc:
                logging.exception("Download failed for %s", url)
                await status_message.edit_text(
                    t(language, "download_failed", error=friendly_error(exc, language))
                )
            finally:
                if result is not None:
                    Downloader.cleanup(result.workdir)

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
    dp = create_dispatcher(settings)
    await dp.start_polling(bot)
