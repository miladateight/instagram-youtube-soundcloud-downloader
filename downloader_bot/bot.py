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
from .sender import TelegramSender
from .state import BotState
from .utils import (
    detect_platform,
    extract_urls,
    looks_like_cookies_file,
    platform_label,
    short_url_label,
)


HELP_TEXT = """سلام. لینک YouTube، YouTube Shorts، Instagram یا SoundCloud را بفرست.

قابلیت‌ها:
• تشخیص خودکار لینک
• پشتیبانی از پست، ریلز، شورت، و لینک‌های SoundCloud
• ارسال پست‌های چندتایی Instagram به شکل آلبوم
• قرار دادن کپشن روی اولین فایل

دستورها:
/id - نمایش آیدی عددی شما
/status - وضعیت بات
/admin - پنل مدیر
/help - راهنما
"""

ADMIN_HELP_TEXT = """پنل مدیر:
/activate - فعال کردن دانلودها
/deactivate - غیرفعال کردن دانلودها
/cookies - راهنمای آپلود cookies.txt
/clearcookies - حذف cookies فعلی
/status - وضعیت کامل

برای آپلود cookies، فایل cookies.txt را به همین ربات بفرست. اگر خواستی دقیق‌تر باشد، در کپشن فایل بنویس /cookies.
"""

COOKIE_HELP_TEXT = """برای لینک‌هایی که Instagram یا YouTube لاگین می‌خواهند، مدیر می‌تواند cookies.txt بدهد.

روش کار:
1. در مرورگر وارد حساب خودت شو.
2. cookies را با فرمت Netscape cookies.txt خروجی بگیر.
3. فایل cookies.txt را همین‌جا برای ربات بفرست.

ربات فایل را فقط روی همین سرور ذخیره می‌کند. این فایل حساس است؛ داخل GitHub قرارش نده.
"""


def create_dispatcher(settings: Settings) -> Dispatcher:
    settings.download_dir.mkdir(parents=True, exist_ok=True)
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.log_dir.mkdir(parents=True, exist_ok=True)

    dp = Dispatcher()
    state = BotState(settings.data_dir / "bot_state.sqlite3")
    downloader = Downloader(settings)
    semaphore = asyncio.Semaphore(settings.concurrent_downloads)

    def user_id(message: Message) -> int:
        return message.from_user.id if message.from_user else 0

    def is_admin(message: Message) -> bool:
        return user_id(message) == settings.admin_id

    def is_allowed(message: Message) -> bool:
        return settings.allow_all_users or is_admin(message)

    def active_cookies_path() -> Path | None:
        state_path = state.cookies_path()
        if state_path and state_path.exists():
            return state_path
        if settings.cookies_file and settings.cookies_file.exists():
            return settings.cookies_file
        default_path = settings.data_dir / "cookies.txt"
        return default_path if default_path.exists() else None

    def admin_keyboard() -> InlineKeyboardMarkup:
        active = state.is_active()
        buttons = [
            [
                InlineKeyboardButton(
                    text="غیرفعال کردن" if active else "فعال کردن",
                    callback_data="admin:disable" if active else "admin:activate",
                )
            ],
            [
                InlineKeyboardButton(text="وضعیت", callback_data="admin:status"),
                InlineKeyboardButton(text="راهنمای cookies", callback_data="admin:cookies"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    def status_text() -> str:
        cookies = active_cookies_path()
        return (
            f"نام بات: {settings.bot_name}\n"
            f"وضعیت دانلود: {'فعال' if state.is_active() else 'غیرفعال'}\n"
            f"دسترسی عمومی: {'فعال' if settings.allow_all_users else 'غیرفعال'}\n"
            f"حد ارسال: {settings.max_upload_mb}MB\n"
            f"حد playlist/profile: {settings.playlist_limit} آیتم\n"
            f"دانلود همزمان: {settings.concurrent_downloads}\n"
            f"cookies: {'تنظیم شده' if cookies else 'تنظیم نشده'}"
        )

    def friendly_error(exc: Exception) -> str:
        raw = str(exc)
        lowered = raw.lower()

        if any(token in lowered for token in ("captcha", "not a robot", "verify you are human")):
            return (
                "سرویس مقصد CAPTCHA یا تایید انسانی خواسته است.\n"
                "ربات نباید CAPTCHA را دور بزند. مدیر باید در مرورگر خودش لاگین کند، چالش را دستی حل کند، "
                "بعد cookies.txt را با دستور /cookies به ربات بدهد."
            )
        if any(token in lowered for token in ("login", "cookie", "cookies", "sign in")):
            return (
                "این لینک احتمالاً نیاز به لاگین یا cookies دارد.\n"
                "مدیر می‌تواند با دستور /cookies فایل cookies.txt را به ربات بدهد."
            )
        if any(token in lowered for token in ("private", "not available", "unavailable")):
            return "این محتوا خصوصی، حذف‌شده، یا در دسترس نیست."
        if any(token in lowered for token in ("larger than max-filesize", "file is larger")):
            return f"حجم فایل از حد ارسال فعلی بزرگ‌تر است. حد فعلی: {settings.max_upload_mb}MB"
        if "ffmpeg" in lowered:
            return "ffmpeg روی سیستم درست نصب نیست. نصب‌کننده آن را نصب می‌کند؛ لاگ سرویس را بررسی کن."
        if "unsupported url" in lowered:
            return "این لینک پشتیبانی نمی‌شود. فعلاً YouTube، Instagram و SoundCloud فعال هستند."

        return raw[:900] if raw else "خطای نامشخص رخ داد."

    async def reject_if_needed(message: Message) -> bool:
        if not is_allowed(message):
            await message.answer("این ربات خصوصی است.")
            return True

        if not state.is_active():
            if is_admin(message):
                await message.answer(
                    "دانلودها هنوز فعال نیستند. برای شروع، /activate را بزن.",
                    reply_markup=admin_keyboard(),
                )
            else:
                await message.answer("ربات هنوز توسط مدیر فعال نشده است.")
            return True

        return False

    @dp.message(CommandStart())
    async def start(message: Message) -> None:
        if not is_allowed(message):
            await message.answer("این ربات خصوصی است.")
            return

        if is_admin(message):
            await message.answer(HELP_TEXT + "\n" + ADMIN_HELP_TEXT, reply_markup=admin_keyboard())
            return

        if not state.is_active():
            await message.answer("ربات هنوز توسط مدیر فعال نشده است.")
            return

        await message.answer(HELP_TEXT)

    @dp.message(Command("help"))
    async def help_command(message: Message) -> None:
        if not is_allowed(message):
            await message.answer("این ربات خصوصی است.")
            return
        await message.answer(HELP_TEXT + ("\n" + ADMIN_HELP_TEXT if is_admin(message) else ""))

    @dp.message(Command("id"))
    async def id_command(message: Message) -> None:
        await message.answer(f"آیدی عددی شما: {user_id(message)}")

    @dp.message(Command("admin"))
    async def admin_command(message: Message) -> None:
        if not is_admin(message):
            await message.answer("این بخش فقط برای مدیر است.")
            return
        await message.answer(ADMIN_HELP_TEXT + "\n" + status_text(), reply_markup=admin_keyboard())

    @dp.message(Command("activate"))
    async def activate_command(message: Message) -> None:
        if not is_admin(message):
            await message.answer("این دستور فقط برای مدیر است.")
            return
        state.set_active(True)
        await message.answer("ربات فعال شد. حالا لینک‌ها دانلود می‌شوند.", reply_markup=admin_keyboard())

    @dp.message(Command("deactivate"))
    async def deactivate_command(message: Message) -> None:
        if not is_admin(message):
            await message.answer("این دستور فقط برای مدیر است.")
            return
        state.set_active(False)
        await message.answer("ربات غیرفعال شد. تا فعال‌سازی دوباره، دانلود انجام نمی‌شود.", reply_markup=admin_keyboard())

    @dp.message(Command("cookies"))
    async def cookies_command(message: Message) -> None:
        if not is_admin(message):
            await message.answer("این دستور فقط برای مدیر است.")
            return
        await message.answer(COOKIE_HELP_TEXT)

    @dp.message(Command("clearcookies"))
    async def clear_cookies_command(message: Message) -> None:
        if not is_admin(message):
            await message.answer("این دستور فقط برای مدیر است.")
            return
        cookies = state.cookies_path() or (settings.data_dir / "cookies.txt")
        with suppress(OSError):
            if cookies.exists() and cookies.is_file():
                cookies.unlink()
        state.clear_cookies_path()
        await message.answer("cookies حذف شد.")

    @dp.message(Command("status"))
    async def status_command(message: Message) -> None:
        if not is_allowed(message):
            await message.answer("این ربات خصوصی است.")
            return
        await message.answer(status_text(), reply_markup=admin_keyboard() if is_admin(message) else None)

    @dp.callback_query(F.data.startswith("admin:"))
    async def admin_callback(callback: CallbackQuery) -> None:
        if not callback.from_user or callback.from_user.id != settings.admin_id:
            await callback.answer("فقط مدیر دسترسی دارد.", show_alert=True)
            return

        action = callback.data.split(":", 1)[1] if callback.data else ""
        if action == "activate":
            state.set_active(True)
            text = "ربات فعال شد.\n\n" + status_text()
        elif action == "disable":
            state.set_active(False)
            text = "ربات غیرفعال شد.\n\n" + status_text()
        elif action == "cookies":
            text = COOKIE_HELP_TEXT
        else:
            text = status_text()

        if callback.message:
            await callback.message.answer(text, reply_markup=admin_keyboard())
        await callback.answer()

    @dp.message(F.document)
    async def handle_document(message: Message, bot: Bot) -> None:
        if not is_admin(message):
            await message.answer("این ربات خصوصی است.")
            return

        document = message.document
        if not document:
            return

        filename = (document.file_name or "").lower()
        caption = (message.caption or "").lower()
        wants_cookie_upload = "cookie" in filename or "/cookies" in caption
        if not wants_cookie_upload:
            await message.answer("اگر این فایل cookies است، آن را با نام cookies.txt یا کپشن /cookies بفرست.")
            return

        if document.file_size and document.file_size > 5 * 1024 * 1024:
            await message.answer("فایل cookies خیلی بزرگ است. معمولاً cookies.txt باید کمتر از 5MB باشد.")
            return

        target = settings.data_dir / "cookies.txt"
        temp_target = settings.data_dir / "cookies.upload"
        with suppress(OSError):
            temp_target.unlink()

        await bot.download(document, destination=temp_target)
        if not looks_like_cookies_file(temp_target):
            with suppress(OSError):
                temp_target.unlink()
            await message.answer("این فایل شبیه cookies.txt با فرمت Netscape نیست.")
            return

        temp_target.replace(target)
        state.set_cookies_path(target)
        await message.answer("cookies ذخیره شد. از این به بعد دانلودهای نیازمند لاگین با همین فایل انجام می‌شوند.")

    @dp.message(F.text)
    async def handle_text(message: Message, bot: Bot) -> None:
        if await reject_if_needed(message):
            return

        urls = extract_urls(message.text or "")
        if not urls:
            await message.answer("یک لینک YouTube، Instagram یا SoundCloud بفرست.")
            return

        unsupported = [url for url in urls if not detect_platform(url)]
        if unsupported:
            await message.answer("چند لینک پشتیبانی نمی‌شوند. فعلاً YouTube، Instagram و SoundCloud فعال هستند.")
            urls = [url for url in urls if detect_platform(url)]
            if not urls:
                return

        if len(urls) > 1:
            await message.answer(f"{len(urls)} لینک پیدا شد. به ترتیب دانلودشان می‌کنم.")

        sender = TelegramSender(bot, settings)
        for url in urls:
            platform = detect_platform(url)
            status_message = await message.answer(
                f"در حال آماده‌سازی {platform_label(platform)}:\n{short_url_label(url)}"
            )
            result = None
            try:
                async with semaphore:
                    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
                    cookies_path = active_cookies_path()
                    await status_message.edit_text(
                        f"در حال دانلود از {platform_label(platform)}...\n{short_url_label(url)}"
                    )
                    result = await downloader.download(url, cookies_path)
                    await status_message.edit_text("دانلود تمام شد. دارم ارسال می‌کنم...")
                    await sender.send_result(message.chat.id, result)
                    with suppress(Exception):
                        await status_message.delete()
            except Exception as exc:
                logging.exception("Download failed for %s", url)
                await status_message.edit_text("دانلود ناموفق بود.\n" + friendly_error(exc))
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
