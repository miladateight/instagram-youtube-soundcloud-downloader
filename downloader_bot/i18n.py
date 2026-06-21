from __future__ import annotations


SUPPORTED_LANGUAGES = ("fa", "en", "ar", "de")

LANGUAGE_NAMES = {
    "fa": "فارسی",
    "en": "English",
    "ar": "العربية",
    "de": "Deutsch",
}

LANGUAGE_BUTTONS = {
    "fa": "فارسی",
    "en": "English",
    "ar": "العربية",
    "de": "Deutsch",
}

RTL_LANGUAGES = {"fa", "ar"}


BASE_MESSAGES = {
    "language_selected": "Bot language has been saved.",
    "choose_language": "Choose your language:",
    "private_bot": "This bot is private.",
    "admin_only": "This section is for the admin only.",
    "command_admin_only": "This command is for the admin only.",
    "bot_not_active_admin": "Downloads are not active yet. Send /activate to start.",
    "bot_not_active_user": "The bot has not been activated by the admin yet.",
    "bot_activated": "The bot is active. Links will be downloaded now.",
    "bot_deactivated": "The bot is inactive. Downloads are paused until it is activated again.",
    "cookies_cleared": "Cookies were removed.",
    "send_supported_link": "Send a YouTube, Instagram, or SoundCloud link.",
    "unsupported_links": "Some links are not supported. YouTube, Instagram, and SoundCloud are enabled for now.",
    "multiple_links": "{count} links found. I will download them one by one.",
    "preparing": "Preparing {platform}:\n{url}",
    "downloading": "Downloading from {platform}...\n{url}",
    "uploading": "Download finished. Uploading now...",
    "download_failed": "Download failed.\n{error}",
    "your_id": "Your numeric ID: {id}",
    "only_admin_access": "Only the admin has access.",
    "cookie_upload_hint": "If this is a cookies file, send it as cookies.txt or with /cookies in the caption.",
    "cookies_too_large": "The cookies file is too large. cookies.txt should usually be under 5MB.",
    "invalid_cookies": "This file does not look like a Netscape cookies.txt file.",
    "cookies_saved": "Cookies saved. Login-required downloads will use this file.",
    "force_join_enabled": "Forced subscription is enabled.\nChannel: {channel}",
    "force_join_disabled": "Forced subscription is disabled.",
    "force_join_missing_channel": "Send the channel too:\n/forcejoin_on @your_channel\n\nThe bot must be a member or admin in that channel.",
    "force_join_status": "Forced subscription: {status}\nChannel: {channel}",
    "force_join_not_set": "Not set",
    "enabled": "Enabled",
    "disabled": "Disabled",
    "must_join": "To use this bot, join the channel below first, then send your link again.",
    "join_channel": "Join channel",
    "check_membership": "Check membership",
    "membership_ok": "Membership verified. Send your link again.",
    "membership_missing": "Your membership is not verified yet.",
    "membership_check_failed": "I could not verify membership. Make sure the bot is a member or admin in the channel.",
    "admin_panel_title": "Admin panel",
    "button_activate": "Activate",
    "button_deactivate": "Deactivate",
    "button_status": "Status",
    "button_cookies": "Cookies help",
    "button_language": "Language",
    "button_force_join": "Forced subscription",
    "button_force_join_off": "Turn forced subscription off",
    "button_public_on": "Open public access",
    "button_public_off": "Close public access",
    "public_enabled": "Public access is enabled.",
    "public_disabled": "Public access is disabled.",
    "start_ready": "The bot is ready. Send a link or use /help.",
    "full_caption_button": "Get full caption",
    "caption_unavailable": "The full caption was not found or has expired.",
    "personal_cookies_saved": "Your personal cookies were saved. Passwords are not stored; only this cookies file is kept on the server.",
    "personal_cookies_cleared": "Your personal cookies were removed.",
    "global_cookies_saved": "Admin global cookies were saved.",
    "help": (
        "Send a YouTube, YouTube Shorts, Instagram, or SoundCloud link.\n\n"
        "Features:\n"
        "- Automatic link detection\n"
        "- Instagram posts, Reels, profiles, and carousel posts\n"
        "- YouTube videos and Shorts\n"
        "- SoundCloud tracks with cover art when available\n\n"
        "Commands:\n"
        "/language - choose language\n"
        "/cookies - cookies.txt upload guide\n"
        "/clearcookies - remove your cookies\n"
        "/id - show your numeric ID\n"
        "/status - bot status\n"
        "/help - help"
    ),
    "admin_help": (
        "Admin panel:\n"
        "/activate - enable downloads\n"
        "/deactivate - disable downloads\n"
        "/public_on - open public access\n"
        "/public_off - close public access\n"
        "/cookies - cookies.txt upload guide\n"
        "/clearcookies - remove your personal cookies\n"
        "/clearcookies global - remove admin global cookies\n"
        "/forcejoin - forced subscription status\n"
        "/forcejoin_on @channel - enable forced subscription\n"
        "/forcejoin_off - disable forced subscription\n"
        "/status - full status"
    ),
    "cookie_help": (
        "For links where Instagram or YouTube requires login, each user can upload a personal cookies.txt file.\n\n"
        "How it works:\n"
        "1. Log in with your browser.\n"
        "2. Export cookies in Netscape cookies.txt format.\n"
        "3. Send cookies.txt to this bot.\n\n"
        "Passwords are not stored; only the cookies file is kept on this server. Use /clearcookies to remove your personal cookies.\n\n"
        "The admin can upload global bot cookies by sending cookies.txt with the caption global, and remove them with /clearcookies global."
    ),
    "captcha_error": (
        "The target service requested CAPTCHA or human verification.\n"
        "The bot should not bypass CAPTCHA. Log in with a browser, solve the challenge manually, then upload cookies.txt."
    ),
    "login_error": "This link probably requires login or cookies.\nUse /cookies to see the cookies.txt upload guide. Passwords are not stored.",
    "private_error": "This content is private, removed, or unavailable.",
    "size_error": "The file is larger than the current upload limit. Current limit: {limit}MB",
    "ffmpeg_error": "ffmpeg is not installed correctly. Check the service logs.",
    "unsupported_error": "This link is not supported. YouTube, Instagram, and SoundCloud are enabled for now.",
    "unknown_error": "An unknown error occurred.",
    "oversized_all": "The file was downloaded, but it is larger than the current upload limit. Current limit: {limit}MB",
    "skipped_files": "Some files were not sent because they are too large:\n{files}",
    "status": (
        "Bot name: {bot_name}\n"
        "Downloads: {active}\n"
        "Public access: {public_access}\n"
        "Forced subscription: {force_join}\n"
        "Subscription channel: {force_join_channel}\n"
        "Upload limit: {max_upload_mb}MB\n"
        "Playlist/profile limit: {playlist_limit} items\n"
        "Concurrent downloads: {concurrent_downloads}\n"
        "Cookies: {cookies}"
    ),
    "cookies_set": "Set",
    "cookies_not_set": "Not set",
}


MESSAGES: dict[str, dict[str, str]] = {
    "en": dict(BASE_MESSAGES),
    "fa": {
        **BASE_MESSAGES,
        "language_selected": "زبان ربات ذخیره شد.",
        "choose_language": "زبان مورد نظر را انتخاب کن:",
        "private_bot": "این ربات خصوصی است.",
        "admin_only": "این بخش فقط برای مدیر است.",
        "command_admin_only": "این دستور فقط برای مدیر است.",
        "bot_not_active_admin": "دانلودها هنوز فعال نیستند. برای شروع /activate را بزن.",
        "bot_not_active_user": "ربات هنوز توسط مدیر فعال نشده است.",
        "bot_activated": "ربات فعال شد. حالا لینک‌ها دانلود می‌شوند.",
        "bot_deactivated": "ربات غیرفعال شد.",
        "cookies_cleared": "cookies حذف شد.",
        "send_supported_link": "یک لینک YouTube، Instagram یا SoundCloud بفرست.",
        "unsupported_links": "بعضی لینک‌ها پشتیبانی نمی‌شوند. فعلا YouTube، Instagram و SoundCloud فعال هستند.",
        "multiple_links": "{count} لینک پیدا شد. به ترتیب دانلودشان می‌کنم.",
        "preparing": "در حال آماده‌سازی {platform}:\n{url}",
        "downloading": "در حال دانلود از {platform}...\n{url}",
        "uploading": "دانلود تمام شد. دارم ارسال می‌کنم...",
        "download_failed": "دانلود ناموفق بود.\n{error}",
        "your_id": "آیدی عددی شما: {id}",
        "only_admin_access": "فقط مدیر دسترسی دارد.",
        "cookie_upload_hint": "اگر این فایل cookies است، آن را با نام cookies.txt یا کپشن /cookies بفرست.",
        "cookies_too_large": "فایل cookies خیلی بزرگ است. معمولا cookies.txt باید کمتر از 5MB باشد.",
        "invalid_cookies": "این فایل شبیه cookies.txt با فرمت Netscape نیست.",
        "force_join_enabled": "عضویت اجباری فعال شد.\nکانال: {channel}",
        "force_join_disabled": "عضویت اجباری غیرفعال شد.",
        "force_join_missing_channel": "کانال را هم بفرست:\n/forcejoin_on @your_channel\n\nربات باید داخل کانال عضو یا ادمین باشد.",
        "force_join_status": "عضویت اجباری: {status}\nکانال: {channel}",
        "force_join_not_set": "تنظیم نشده",
        "enabled": "فعال",
        "disabled": "غیرفعال",
        "must_join": "برای استفاده از ربات، اول عضو کانال زیر شو و بعد لینک را دوباره بفرست.",
        "join_channel": "عضویت در کانال",
        "check_membership": "بررسی عضویت",
        "membership_ok": "عضویت تایید شد. لینک را دوباره بفرست.",
        "membership_missing": "هنوز عضویتت تایید نشده.",
        "membership_check_failed": "نتوانستم عضویت را بررسی کنم. مطمئن شو ربات داخل کانال عضو یا ادمین است.",
        "button_activate": "فعال کردن",
        "button_deactivate": "غیرفعال کردن",
        "button_status": "وضعیت",
        "button_cookies": "راهنمای cookies",
        "button_language": "زبان",
        "button_force_join": "عضویت اجباری",
        "button_force_join_off": "خاموش کردن عضویت اجباری",
        "button_public_on": "باز کردن دسترسی عمومی",
        "button_public_off": "بستن دسترسی عمومی",
        "public_enabled": "دسترسی عمومی فعال شد.",
        "public_disabled": "دسترسی عمومی غیرفعال شد.",
        "start_ready": "ربات آماده است. لینک بفرست یا برای راهنما /help را بزن.",
        "full_caption_button": "دریافت کامل کپشن",
        "caption_unavailable": "کپشن کامل پیدا نشد یا منقضی شده است.",
        "personal_cookies_saved": "cookies شخصی شما ذخیره شد. رمز عبور ذخیره نمی‌شود؛ فقط همین فایل cookies روی سرور می‌ماند.",
        "personal_cookies_cleared": "cookies شخصی شما حذف شد.",
        "global_cookies_saved": "cookies عمومی مدیر ذخیره شد.",
        "help": (
            "لینک YouTube، YouTube Shorts، Instagram یا SoundCloud را بفرست.\n\n"
            "دستورها:\n/language - انتخاب زبان\n/cookies - راهنمای cookies.txt\n"
            "/clearcookies - حذف cookies شخصی\n/id - آیدی عددی\n/status - وضعیت\n/help - راهنما"
        ),
        "admin_help": (
            "پنل مدیر:\n/activate - فعال کردن دانلودها\n/deactivate - غیرفعال کردن دانلودها\n"
            "/public_on - باز کردن دسترسی عمومی\n/public_off - بستن دسترسی عمومی\n"
            "/cookies - راهنمای cookies.txt\n/clearcookies global - حذف cookies عمومی مدیر\n"
            "/forcejoin_on @channel - فعال کردن عضویت اجباری\n/forcejoin_off - غیرفعال کردن عضویت اجباری\n/status - وضعیت کامل"
        ),
        "cookie_help": (
            "برای لینک‌هایی که لاگین می‌خواهند، هر کاربر می‌تواند cookies.txt شخصی خودش را آپلود کند.\n\n"
            "رمز عبور ذخیره نمی‌شود؛ فقط فایل cookies روی همین سرور می‌ماند. برای حذف /clearcookies را بزن.\n\n"
            "مدیر می‌تواند cookies عمومی را با کپشن global ارسال کند و با /clearcookies global حذف کند."
        ),
        "login_error": "این لینک احتمالا نیاز به لاگین یا cookies دارد.\nبا /cookies راهنمای آپلود cookies.txt را ببین. رمز عبور ذخیره نمی‌شود.",
        "captcha_error": "سرویس مقصد CAPTCHA یا تایید انسانی خواسته است. ربات CAPTCHA را دور نمی‌زند؛ در مرورگر حل کن و بعد cookies.txt بده.",
        "private_error": "این محتوا خصوصی، حذف‌شده، یا در دسترس نیست.",
        "size_error": "حجم فایل از حد ارسال فعلی بزرگ‌تر است. حد فعلی: {limit}MB",
        "ffmpeg_error": "ffmpeg درست نصب نیست. لاگ سرویس را بررسی کن.",
        "unsupported_error": "این لینک پشتیبانی نمی‌شود. فعلا YouTube، Instagram و SoundCloud فعال هستند.",
        "unknown_error": "خطای نامشخص رخ داد.",
        "oversized_all": "فایل دانلود شد، اما حجم آن از محدودیت ارسال فعلی بزرگ‌تر بود. حد فعلی: {limit}MB",
        "skipped_files": "چند فایل به خاطر حجم بالا ارسال نشدند:\n{files}",
        "status": (
            "نام بات: {bot_name}\nوضعیت دانلود: {active}\nدسترسی عمومی: {public_access}\n"
            "عضویت اجباری: {force_join}\nکانال عضویت: {force_join_channel}\nحد ارسال: {max_upload_mb}MB\n"
            "حد playlist/profile: {playlist_limit} آیتم\nدانلود همزمان: {concurrent_downloads}\ncookies: {cookies}"
        ),
        "cookies_set": "تنظیم شده",
        "cookies_not_set": "تنظیم نشده",
    },
    "ar": {
        **BASE_MESSAGES,
        "language_selected": "تم حفظ لغة البوت.",
        "choose_language": "اختر لغتك:",
        "private_bot": "هذا البوت خاص.",
        "admin_only": "هذا القسم للمدير فقط.",
        "command_admin_only": "هذا الأمر للمدير فقط.",
        "bot_not_active_user": "لم يتم تفعيل البوت من المدير بعد.",
        "button_public_on": "فتح الوصول العام",
        "button_public_off": "إغلاق الوصول العام",
        "public_enabled": "تم تفعيل الوصول العام.",
        "public_disabled": "تم تعطيل الوصول العام.",
        "start_ready": "البوت جاهز. أرسل رابطاً أو استخدم /help.",
        "full_caption_button": "الحصول على الوصف الكامل",
        "personal_cookies_saved": "تم حفظ cookies الخاصة بك. لا يتم حفظ كلمات المرور؛ يتم حفظ ملف cookies فقط.",
        "personal_cookies_cleared": "تم حذف cookies الخاصة بك.",
        "global_cookies_saved": "تم حفظ cookies العامة للمدير.",
        "login_error": "غالباً يحتاج هذا الرابط إلى تسجيل دخول أو cookies.\nاستخدم /cookies لعرض الدليل. لا يتم حفظ كلمات المرور.",
    },
    "de": {
        **BASE_MESSAGES,
        "language_selected": "Die Bot-Sprache wurde gespeichert.",
        "choose_language": "Wähle deine Sprache:",
        "private_bot": "Dieser Bot ist privat.",
        "admin_only": "Dieser Bereich ist nur für den Admin.",
        "command_admin_only": "Dieser Befehl ist nur für den Admin.",
        "bot_not_active_user": "Der Bot wurde vom Admin noch nicht aktiviert.",
        "button_public_on": "Öffentlichen Zugriff öffnen",
        "button_public_off": "Öffentlichen Zugriff schließen",
        "public_enabled": "Öffentlicher Zugriff ist aktiviert.",
        "public_disabled": "Öffentlicher Zugriff ist deaktiviert.",
        "start_ready": "Der Bot ist bereit. Sende einen Link oder nutze /help.",
        "full_caption_button": "Vollständige Caption abrufen",
        "personal_cookies_saved": "Deine persönlichen Cookies wurden gespeichert. Passwörter werden nicht gespeichert; nur diese Cookies-Datei bleibt auf dem Server.",
        "personal_cookies_cleared": "Deine persönlichen Cookies wurden entfernt.",
        "global_cookies_saved": "Globale Admin-Cookies wurden gespeichert.",
        "login_error": "Dieser Link erfordert wahrscheinlich Login oder Cookies.\nNutze /cookies für die Anleitung. Passwörter werden nicht gespeichert.",
    },
}


def normalize_language(language: str | None) -> str:
    if not language:
        return "fa"
    value = language.lower().split("-", 1)[0]
    return value if value in SUPPORTED_LANGUAGES else "fa"


def t(language: str | None, key: str, **kwargs: object) -> str:
    lang = normalize_language(language)
    template = MESSAGES.get(lang, MESSAGES["fa"]).get(key, MESSAGES["fa"].get(key, key))
    return template.format(**kwargs)
