from __future__ import annotations


SUPPORTED_LANGUAGES = ("fa", "en", "ar", "de")

LANGUAGE_NAMES = {
    "fa": "فارسی",
    "en": "English",
    "ar": "العربية",
    "de": "Deutsch",
}

LANGUAGE_BUTTONS = {
    "fa": "🇮🇷 فارسی",
    "en": "🇬🇧 English",
    "ar": "🇸🇦 العربية",
    "de": "🇩🇪 Deutsch",
}

RTL_LANGUAGES = {"fa", "ar"}


MESSAGES: dict[str, dict[str, str]] = {
    "fa": {
        "language_selected": "زبان ربات روی فارسی تنظیم شد.",
        "choose_language": "زبان مورد نظر را انتخاب کن:",
        "private_bot": "این ربات خصوصی است.",
        "admin_only": "این بخش فقط برای مدیر است.",
        "command_admin_only": "این دستور فقط برای مدیر است.",
        "bot_not_active_admin": "دانلودها هنوز فعال نیستند. برای شروع، /activate را بزن.",
        "bot_not_active_user": "ربات هنوز توسط مدیر فعال نشده است.",
        "bot_activated": "ربات فعال شد. حالا لینک‌ها دانلود می‌شوند.",
        "bot_deactivated": "ربات غیرفعال شد. تا فعال‌سازی دوباره، دانلود انجام نمی‌شود.",
        "cookies_cleared": "cookies حذف شد.",
        "send_supported_link": "یک لینک YouTube، Instagram یا SoundCloud بفرست.",
        "unsupported_links": "چند لینک پشتیبانی نمی‌شوند. فعلاً YouTube، Instagram و SoundCloud فعال هستند.",
        "multiple_links": "{count} لینک پیدا شد. به ترتیب دانلودشان می‌کنم.",
        "preparing": "در حال آماده‌سازی {platform}:\n{url}",
        "downloading": "در حال دانلود از {platform}...\n{url}",
        "uploading": "دانلود تمام شد. دارم ارسال می‌کنم...",
        "download_failed": "دانلود ناموفق بود.\n{error}",
        "your_id": "آیدی عددی شما: {id}",
        "only_admin_access": "فقط مدیر دسترسی دارد.",
        "cookie_upload_hint": "اگر این فایل cookies است، آن را با نام cookies.txt یا کپشن /cookies بفرست.",
        "cookies_too_large": "فایل cookies خیلی بزرگ است. معمولاً cookies.txt باید کمتر از 5MB باشد.",
        "invalid_cookies": "این فایل شبیه cookies.txt با فرمت Netscape نیست.",
        "cookies_saved": "cookies ذخیره شد. از این به بعد دانلودهای نیازمند لاگین با همین فایل انجام می‌شوند.",
        "force_join_enabled": "عضویت اجباری فعال شد.\nکانال: {channel}",
        "force_join_disabled": "عضویت اجباری غیرفعال شد.",
        "force_join_missing_channel": "برای فعال‌سازی، کانال را هم بده:\n/forcejoin_on @your_channel\n\nربات باید داخل کانال عضو یا ادمین باشد.",
        "force_join_status": "عضویت اجباری: {status}\nکانال: {channel}",
        "force_join_not_set": "تنظیم نشده",
        "enabled": "فعال",
        "disabled": "غیرفعال",
        "must_join": "برای استفاده از ربات، اول عضو کانال زیر شو و بعد دوباره لینک را بفرست.",
        "join_channel": "عضویت در کانال",
        "check_membership": "بررسی عضویت",
        "membership_ok": "عضویت تایید شد. حالا لینک را دوباره بفرست.",
        "membership_missing": "هنوز عضویتت تایید نشد.",
        "membership_check_failed": "نتوانستم عضویت را بررسی کنم. مطمئن شو ربات داخل کانال عضو یا ادمین است.",
        "admin_panel_title": "پنل مدیر",
        "button_activate": "فعال کردن",
        "button_deactivate": "غیرفعال کردن",
        "button_status": "وضعیت",
        "button_cookies": "راهنمای cookies",
        "button_language": "زبان",
        "button_force_join": "عضویت اجباری",
        "button_force_join_off": "خاموش کردن عضویت اجباری",
        "help": (
            "سلام. لینک YouTube، YouTube Shorts، Instagram یا SoundCloud را بفرست.\n\n"
            "قابلیت‌ها:\n"
            "• تشخیص خودکار لینک\n"
            "• پشتیبانی از پست، ریلز، شورت و لینک‌های SoundCloud\n"
            "• ارسال پست‌های چندتایی Instagram به شکل آلبوم\n"
            "• قرار دادن کپشن روی اولین فایل\n\n"
            "دستورها:\n"
            "/language - انتخاب زبان\n"
            "/id - نمایش آیدی عددی شما\n"
            "/status - وضعیت بات\n"
            "/help - راهنما"
        ),
        "admin_help": (
            "پنل مدیر:\n"
            "/activate - فعال کردن دانلودها\n"
            "/deactivate - غیرفعال کردن دانلودها\n"
            "/cookies - راهنمای آپلود cookies.txt\n"
            "/clearcookies - حذف cookies فعلی\n"
            "/forcejoin - وضعیت عضویت اجباری\n"
            "/forcejoin_on @channel - فعال کردن عضویت اجباری\n"
            "/forcejoin_off - غیرفعال کردن عضویت اجباری\n"
            "/status - وضعیت کامل"
        ),
        "cookie_help": (
            "برای لینک‌هایی که Instagram یا YouTube لاگین می‌خواهند، مدیر می‌تواند cookies.txt بدهد.\n\n"
            "روش کار:\n"
            "1. در مرورگر وارد حساب خودت شو.\n"
            "2. cookies را با فرمت Netscape cookies.txt خروجی بگیر.\n"
            "3. فایل cookies.txt را همین‌جا برای ربات بفرست.\n\n"
            "ربات فایل را فقط روی همین سرور ذخیره می‌کند. این فایل حساس است؛ داخل GitHub قرارش نده."
        ),
        "captcha_error": (
            "سرویس مقصد CAPTCHA یا تایید انسانی خواسته است.\n"
            "ربات نباید CAPTCHA را دور بزند. مدیر باید در مرورگر خودش لاگین کند، چالش را دستی حل کند، "
            "بعد cookies.txt را با دستور /cookies به ربات بدهد."
        ),
        "login_error": (
            "این لینک احتمالاً نیاز به لاگین یا cookies دارد.\n"
            "مدیر می‌تواند با دستور /cookies فایل cookies.txt را به ربات بدهد."
        ),
        "private_error": "این محتوا خصوصی، حذف‌شده، یا در دسترس نیست.",
        "size_error": "حجم فایل از حد ارسال فعلی بزرگ‌تر است. حد فعلی: {limit}MB",
        "ffmpeg_error": "ffmpeg روی سیستم درست نصب نیست. لاگ سرویس را بررسی کن.",
        "unsupported_error": "این لینک پشتیبانی نمی‌شود. فعلاً YouTube، Instagram و SoundCloud فعال هستند.",
        "unknown_error": "خطای نامشخص رخ داد.",
        "oversized_all": "فایل دانلود شد، اما حجم آن از محدودیت ارسال فعلی بزرگ‌تر بود. حد فعلی: {limit}MB",
        "skipped_files": "چند فایل به خاطر حجم بالا ارسال نشدند:\n{files}",
        "status": (
            "نام بات: {bot_name}\n"
            "وضعیت دانلود: {active}\n"
            "دسترسی عمومی: {public_access}\n"
            "عضویت اجباری: {force_join}\n"
            "کانال عضویت: {force_join_channel}\n"
            "حد ارسال: {max_upload_mb}MB\n"
            "حد playlist/profile: {playlist_limit} آیتم\n"
            "دانلود همزمان: {concurrent_downloads}\n"
            "cookies: {cookies}"
        ),
        "cookies_set": "تنظیم شده",
        "cookies_not_set": "تنظیم نشده",
    },
    "en": {
        "language_selected": "Bot language has been set to English.",
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
        "help": (
            "Hi. Send a YouTube, YouTube Shorts, Instagram, or SoundCloud link.\n\n"
            "Features:\n"
            "• Automatic link detection\n"
            "• Posts, Reels, Shorts, and SoundCloud links\n"
            "• Instagram multi-item posts as albums\n"
            "• Caption on the first uploaded file\n\n"
            "Commands:\n"
            "/language - choose language\n"
            "/id - show your numeric ID\n"
            "/status - bot status\n"
            "/help - help"
        ),
        "admin_help": (
            "Admin panel:\n"
            "/activate - enable downloads\n"
            "/deactivate - disable downloads\n"
            "/cookies - cookies.txt upload guide\n"
            "/clearcookies - remove current cookies\n"
            "/forcejoin - forced subscription status\n"
            "/forcejoin_on @channel - enable forced subscription\n"
            "/forcejoin_off - disable forced subscription\n"
            "/status - full status"
        ),
        "cookie_help": (
            "For links where Instagram or YouTube requires login, the admin can upload cookies.txt.\n\n"
            "How it works:\n"
            "1. Log in with your browser.\n"
            "2. Export cookies in Netscape cookies.txt format.\n"
            "3. Send cookies.txt to this bot.\n\n"
            "The bot stores the file only on this server. It is sensitive; do not commit it to GitHub."
        ),
        "captcha_error": (
            "The target service requested CAPTCHA or human verification.\n"
            "The bot should not bypass CAPTCHA. The admin must log in in a browser, solve the challenge manually, "
            "then upload cookies.txt with /cookies."
        ),
        "login_error": "This link probably requires login or cookies.\nThe admin can upload cookies.txt with /cookies.",
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
    },
    "ar": {
        "language_selected": "تم ضبط لغة البوت على العربية.",
        "choose_language": "اختر اللغة:",
        "private_bot": "هذا البوت خاص.",
        "admin_only": "هذا القسم للمدير فقط.",
        "command_admin_only": "هذا الأمر للمدير فقط.",
        "bot_not_active_admin": "التنزيلات غير مفعلة بعد. أرسل /activate للبدء.",
        "bot_not_active_user": "لم يقم المدير بتفعيل البوت بعد.",
        "bot_activated": "تم تفعيل البوت. يمكن تنزيل الروابط الآن.",
        "bot_deactivated": "تم تعطيل البوت. لن تتم التنزيلات حتى يتم تفعيله من جديد.",
        "cookies_cleared": "تم حذف cookies.",
        "send_supported_link": "أرسل رابط YouTube أو Instagram أو SoundCloud.",
        "unsupported_links": "بعض الروابط غير مدعومة. حالياً YouTube و Instagram و SoundCloud مدعومة.",
        "multiple_links": "تم العثور على {count} روابط. سأقوم بتنزيلها بالترتيب.",
        "preparing": "جاري تجهيز {platform}:\n{url}",
        "downloading": "جاري التنزيل من {platform}...\n{url}",
        "uploading": "اكتمل التنزيل. جاري الإرسال...",
        "download_failed": "فشل التنزيل.\n{error}",
        "your_id": "معرّفك الرقمي: {id}",
        "only_admin_access": "الوصول للمدير فقط.",
        "cookie_upload_hint": "إذا كان هذا ملف cookies، أرسله باسم cookies.txt أو مع /cookies في الوصف.",
        "cookies_too_large": "ملف cookies كبير جداً. عادة يجب أن يكون cookies.txt أقل من 5MB.",
        "invalid_cookies": "هذا الملف لا يبدو كملف Netscape cookies.txt.",
        "cookies_saved": "تم حفظ cookies. سيتم استخدامها للتنزيلات التي تحتاج إلى تسجيل دخول.",
        "force_join_enabled": "تم تفعيل الاشتراك الإجباري.\nالقناة: {channel}",
        "force_join_disabled": "تم تعطيل الاشتراك الإجباري.",
        "force_join_missing_channel": "أرسل القناة أيضاً:\n/forcejoin_on @your_channel\n\nيجب أن يكون البوت عضواً أو مديراً في القناة.",
        "force_join_status": "الاشتراك الإجباري: {status}\nالقناة: {channel}",
        "force_join_not_set": "غير محددة",
        "enabled": "مفعل",
        "disabled": "معطل",
        "must_join": "لاستخدام هذا البوت، اشترك أولاً في القناة أدناه ثم أرسل الرابط مرة أخرى.",
        "join_channel": "الاشتراك في القناة",
        "check_membership": "فحص الاشتراك",
        "membership_ok": "تم تأكيد الاشتراك. أرسل الرابط مرة أخرى.",
        "membership_missing": "لم يتم تأكيد اشتراكك بعد.",
        "membership_check_failed": "لم أتمكن من فحص الاشتراك. تأكد أن البوت عضو أو مدير في القناة.",
        "admin_panel_title": "لوحة المدير",
        "button_activate": "تفعيل",
        "button_deactivate": "تعطيل",
        "button_status": "الحالة",
        "button_cookies": "مساعدة cookies",
        "button_language": "اللغة",
        "button_force_join": "الاشتراك الإجباري",
        "button_force_join_off": "إيقاف الاشتراك الإجباري",
        "help": (
            "مرحباً. أرسل رابط YouTube أو YouTube Shorts أو Instagram أو SoundCloud.\n\n"
            "المزايا:\n"
            "• اكتشاف تلقائي للروابط\n"
            "• دعم المنشورات و Reels و Shorts وروابط SoundCloud\n"
            "• إرسال منشورات Instagram متعددة العناصر كألبوم\n"
            "• وضع الوصف على أول ملف مرسل\n\n"
            "الأوامر:\n"
            "/language - اختيار اللغة\n"
            "/id - عرض المعرف الرقمي\n"
            "/status - حالة البوت\n"
            "/help - المساعدة"
        ),
        "admin_help": (
            "لوحة المدير:\n"
            "/activate - تفعيل التنزيلات\n"
            "/deactivate - تعطيل التنزيلات\n"
            "/cookies - دليل رفع cookies.txt\n"
            "/clearcookies - حذف cookies الحالية\n"
            "/forcejoin - حالة الاشتراك الإجباري\n"
            "/forcejoin_on @channel - تفعيل الاشتراك الإجباري\n"
            "/forcejoin_off - تعطيل الاشتراك الإجباري\n"
            "/status - الحالة الكاملة"
        ),
        "cookie_help": (
            "للروابط التي تتطلب تسجيل دخول في Instagram أو YouTube، يمكن للمدير رفع cookies.txt.\n\n"
            "الطريقة:\n"
            "1. سجّل الدخول من المتصفح.\n"
            "2. صدّر cookies بصيغة Netscape cookies.txt.\n"
            "3. أرسل cookies.txt إلى هذا البوت.\n\n"
            "يحفظ البوت الملف على هذا الخادم فقط. الملف حساس؛ لا ترفعه إلى GitHub."
        ),
        "captcha_error": (
            "طلبت الخدمة المستهدفة CAPTCHA أو تحققاً بشرياً.\n"
            "لا ينبغي للبوت تجاوز CAPTCHA. يجب على المدير تسجيل الدخول في المتصفح وحل التحدي يدوياً، "
            "ثم رفع cookies.txt باستخدام /cookies."
        ),
        "login_error": "غالباً يحتاج هذا الرابط إلى تسجيل دخول أو cookies.\nيمكن للمدير رفع cookies.txt باستخدام /cookies.",
        "private_error": "هذا المحتوى خاص أو محذوف أو غير متاح.",
        "size_error": "حجم الملف أكبر من حد الإرسال الحالي. الحد الحالي: {limit}MB",
        "ffmpeg_error": "ffmpeg غير مثبت بشكل صحيح. تحقق من سجلات الخدمة.",
        "unsupported_error": "هذا الرابط غير مدعوم. حالياً YouTube و Instagram و SoundCloud مدعومة.",
        "unknown_error": "حدث خطأ غير معروف.",
        "oversized_all": "تم تنزيل الملف، لكنه أكبر من حد الإرسال الحالي. الحد الحالي: {limit}MB",
        "skipped_files": "لم يتم إرسال بعض الملفات لأنها كبيرة جداً:\n{files}",
        "status": (
            "اسم البوت: {bot_name}\n"
            "التنزيلات: {active}\n"
            "الوصول العام: {public_access}\n"
            "الاشتراك الإجباري: {force_join}\n"
            "قناة الاشتراك: {force_join_channel}\n"
            "حد الإرسال: {max_upload_mb}MB\n"
            "حد playlist/profile: {playlist_limit} عنصر\n"
            "التنزيلات المتزامنة: {concurrent_downloads}\n"
            "Cookies: {cookies}"
        ),
        "cookies_set": "مضبوطة",
        "cookies_not_set": "غير مضبوطة",
    },
    "de": {
        "language_selected": "Die Bot-Sprache wurde auf Deutsch gesetzt.",
        "choose_language": "Wähle deine Sprache:",
        "private_bot": "Dieser Bot ist privat.",
        "admin_only": "Dieser Bereich ist nur für den Admin.",
        "command_admin_only": "Dieser Befehl ist nur für den Admin.",
        "bot_not_active_admin": "Downloads sind noch nicht aktiv. Sende /activate zum Starten.",
        "bot_not_active_user": "Der Bot wurde vom Admin noch nicht aktiviert.",
        "bot_activated": "Der Bot ist aktiv. Links werden jetzt heruntergeladen.",
        "bot_deactivated": "Der Bot ist inaktiv. Downloads sind bis zur erneuten Aktivierung pausiert.",
        "cookies_cleared": "Cookies wurden entfernt.",
        "send_supported_link": "Sende einen YouTube-, Instagram- oder SoundCloud-Link.",
        "unsupported_links": "Einige Links werden nicht unterstützt. Aktuell sind YouTube, Instagram und SoundCloud aktiv.",
        "multiple_links": "{count} Links gefunden. Ich lade sie nacheinander herunter.",
        "preparing": "{platform} wird vorbereitet:\n{url}",
        "downloading": "Download von {platform} läuft...\n{url}",
        "uploading": "Download fertig. Upload läuft...",
        "download_failed": "Download fehlgeschlagen.\n{error}",
        "your_id": "Deine numerische ID: {id}",
        "only_admin_access": "Nur der Admin hat Zugriff.",
        "cookie_upload_hint": "Wenn dies eine Cookies-Datei ist, sende sie als cookies.txt oder mit /cookies in der Beschriftung.",
        "cookies_too_large": "Die Cookies-Datei ist zu groß. cookies.txt sollte normalerweise unter 5MB sein.",
        "invalid_cookies": "Diese Datei sieht nicht wie eine Netscape cookies.txt-Datei aus.",
        "cookies_saved": "Cookies gespeichert. Downloads mit Login-Anforderung nutzen diese Datei.",
        "force_join_enabled": "Pflichtmitgliedschaft ist aktiviert.\nKanal: {channel}",
        "force_join_disabled": "Pflichtmitgliedschaft ist deaktiviert.",
        "force_join_missing_channel": "Sende auch den Kanal:\n/forcejoin_on @your_channel\n\nDer Bot muss Mitglied oder Admin in diesem Kanal sein.",
        "force_join_status": "Pflichtmitgliedschaft: {status}\nKanal: {channel}",
        "force_join_not_set": "Nicht gesetzt",
        "enabled": "Aktiv",
        "disabled": "Inaktiv",
        "must_join": "Um diesen Bot zu nutzen, tritt zuerst dem Kanal unten bei und sende den Link danach erneut.",
        "join_channel": "Kanal beitreten",
        "check_membership": "Mitgliedschaft prüfen",
        "membership_ok": "Mitgliedschaft bestätigt. Sende deinen Link erneut.",
        "membership_missing": "Deine Mitgliedschaft wurde noch nicht bestätigt.",
        "membership_check_failed": "Ich konnte die Mitgliedschaft nicht prüfen. Stelle sicher, dass der Bot Mitglied oder Admin im Kanal ist.",
        "admin_panel_title": "Admin-Panel",
        "button_activate": "Aktivieren",
        "button_deactivate": "Deaktivieren",
        "button_status": "Status",
        "button_cookies": "Cookies-Hilfe",
        "button_language": "Sprache",
        "button_force_join": "Pflichtmitgliedschaft",
        "button_force_join_off": "Pflichtmitgliedschaft aus",
        "help": (
            "Hallo. Sende einen YouTube-, YouTube Shorts-, Instagram- oder SoundCloud-Link.\n\n"
            "Funktionen:\n"
            "• Automatische Link-Erkennung\n"
            "• Posts, Reels, Shorts und SoundCloud-Links\n"
            "• Instagram-Posts mit mehreren Medien als Album\n"
            "• Beschriftung auf der ersten gesendeten Datei\n\n"
            "Befehle:\n"
            "/language - Sprache wählen\n"
            "/id - deine numerische ID anzeigen\n"
            "/status - Bot-Status\n"
            "/help - Hilfe"
        ),
        "admin_help": (
            "Admin-Panel:\n"
            "/activate - Downloads aktivieren\n"
            "/deactivate - Downloads deaktivieren\n"
            "/cookies - Anleitung zum Hochladen von cookies.txt\n"
            "/clearcookies - aktuelle Cookies entfernen\n"
            "/forcejoin - Status der Pflichtmitgliedschaft\n"
            "/forcejoin_on @channel - Pflichtmitgliedschaft aktivieren\n"
            "/forcejoin_off - Pflichtmitgliedschaft deaktivieren\n"
            "/status - vollständiger Status"
        ),
        "cookie_help": (
            "Für Links, bei denen Instagram oder YouTube ein Login verlangt, kann der Admin cookies.txt hochladen.\n\n"
            "Ablauf:\n"
            "1. Melde dich im Browser an.\n"
            "2. Exportiere Cookies im Netscape cookies.txt-Format.\n"
            "3. Sende cookies.txt an diesen Bot.\n\n"
            "Der Bot speichert die Datei nur auf diesem Server. Sie ist sensibel; committe sie nicht zu GitHub."
        ),
        "captcha_error": (
            "Der Zieldienst verlangt CAPTCHA oder menschliche Verifizierung.\n"
            "Der Bot sollte CAPTCHA nicht umgehen. Der Admin muss sich im Browser anmelden, die Prüfung manuell lösen "
            "und danach cookies.txt mit /cookies hochladen."
        ),
        "login_error": "Dieser Link erfordert wahrscheinlich Login oder Cookies.\nDer Admin kann cookies.txt mit /cookies hochladen.",
        "private_error": "Dieser Inhalt ist privat, entfernt oder nicht verfügbar.",
        "size_error": "Die Datei ist größer als das aktuelle Upload-Limit. Aktuelles Limit: {limit}MB",
        "ffmpeg_error": "ffmpeg ist nicht korrekt installiert. Prüfe die Service-Logs.",
        "unsupported_error": "Dieser Link wird nicht unterstützt. Aktuell sind YouTube, Instagram und SoundCloud aktiv.",
        "unknown_error": "Ein unbekannter Fehler ist aufgetreten.",
        "oversized_all": "Die Datei wurde heruntergeladen, ist aber größer als das aktuelle Upload-Limit. Aktuelles Limit: {limit}MB",
        "skipped_files": "Einige Dateien wurden nicht gesendet, weil sie zu groß sind:\n{files}",
        "status": (
            "Bot-Name: {bot_name}\n"
            "Downloads: {active}\n"
            "Öffentlicher Zugriff: {public_access}\n"
            "Pflichtmitgliedschaft: {force_join}\n"
            "Mitgliedschaftskanal: {force_join_channel}\n"
            "Upload-Limit: {max_upload_mb}MB\n"
            "Playlist/Profile-Limit: {playlist_limit} Elemente\n"
            "Gleichzeitige Downloads: {concurrent_downloads}\n"
            "Cookies: {cookies}"
        ),
        "cookies_set": "Gesetzt",
        "cookies_not_set": "Nicht gesetzt",
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
