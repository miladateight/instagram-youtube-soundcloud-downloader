# ربات دانلودر تلگرام

**زبان:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

یک ربات خصوصی و رزومه‌ای تلگرام برای دانلود رسانه‌های پشتیبانی‌شده از YouTube، YouTube Shorts، Instagram و SoundCloud.

این پروژه کاملاً با Python نوشته شده و برای نصب ساده روی Ubuntu آماده است. ربات بعد از نصب به صورت پیش‌فرض غیرفعال می‌ماند تا مدیر از داخل تلگرام آن را فعال کند.

> نکته حقوقی: این پروژه برای تست، یادگیری و استفاده شخصی ساخته شده است. قبل از استفاده عمومی، قوانین سرویس‌ها، حق نشر، حریم خصوصی و محدودیت‌های Telegram Bot API را بررسی کن.

## قابلیت‌ها

- تشخیص خودکار لینک‌های YouTube، `youtu.be`، Shorts، Instagram و SoundCloud
- دانلود و ارسال ویدیو، عکس، فایل صوتی و فایل‌های عمومی با `yt-dlp`
- پشتیبانی از پست‌ها، ریلزها، پروفایل‌ها و بسیاری از carouselهای Instagram
- ارسال پست‌های چندتایی Instagram به شکل album/media group
- مدیریت caption طولانی با پیش‌نمایش کوتاه و دکمه «دریافت کامل کپشن»
- رابط کاربری چهارزبانه: فارسی، انگلیسی، عربی و آلمانی
- انتخاب زبان کاربر فقط بار اول، و تغییر بعدی با `/language`
- فعال‌سازی ربات توسط مدیر از داخل تلگرام
- باز و بسته کردن دسترسی عمومی با `/public_on` و `/public_off`
- آپلود cookies شخصی توسط کاربران مجاز و cookies عمومی توسط مدیر
- عضویت اجباری قابل فعال/غیرفعال‌سازی توسط مدیر
- ارسال بهتر SoundCloud با کاور، نام آهنگ و نام خواننده
- نصب، آپدیت و حذف کامل با اسکریپت‌های Python روی Ubuntu
- اجرای دائمی با systemd و لاگ داخل `logs/bot.log`

## نصب سریع روی Ubuntu

```bash
git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git && cd instagram-youtube-soundcloud-downloader && python3 install.py
```

نصاب از تو می‌پرسد:

- نام ربات
- توکن ربات از BotFather
- آیدی عددی مدیر

بعد از نصب، در تلگرام به ربات پیام بده و به عنوان مدیر دستور زیر را بزن:

```text
/activate
```

تا وقتی این دستور اجرا نشود، ربات هیچ دانلودی انجام نمی‌دهد.

## دستورهای کاربر

- `/start` شروع ربات؛ اگر زبان قبلاً انتخاب شده باشد فقط پیام کوتاه می‌دهد
- `/language` یا `/lang` تغییر زبان کاربر
- `/help` راهنما
- `/id` نمایش آیدی عددی کاربر
- `/status` نمایش وضعیت ربات
- `/cookies` راهنمای آپلود cookies شخصی
- `/clearcookies` حذف cookies شخصی ذخیره‌شده

## دستورهای مدیر

- `/admin` پنل مدیر
- `/activate` فعال کردن دانلودها
- `/deactivate` غیرفعال کردن دانلودها
- `/public_on` باز کردن دسترسی عمومی
- `/public_off` بستن دسترسی عمومی
- `/clearcookies global` حذف cookies عمومی ربات
- `/forcejoin` وضعیت عضویت اجباری
- `/forcejoin_on @channel` فعال کردن عضویت اجباری
- `/forcejoin_off` غیرفعال کردن عضویت اجباری

## دسترسی عمومی

ربات به صورت پیش‌فرض خصوصی است. مدیر می‌تواند از داخل ربات دسترسی عمومی را باز یا بسته کند:

```text
/public_on
/public_off
```

اگر دسترسی عمومی بسته باشد، فقط مدیر و کاربرانی که در تنظیمات مجاز شده‌اند می‌توانند از ربات استفاده کنند.

## عضویت اجباری

مدیر می‌تواند کاربران را ملزم کند قبل از دانلود عضو یک کانال تلگرام شوند.

```text
/forcejoin_on @your_channel
```

برای غیرفعال‌سازی:

```text
/forcejoin_off
```

ربات باید داخل کانال مورد نظر عضو یا ادمین باشد تا Telegram اجازه بررسی عضویت را بدهد. مدیر ربات توسط عضویت اجباری محدود نمی‌شود.

## Cookies برای Instagram و YouTube

بعضی لینک‌های Instagram یا YouTube بدون لاگین دانلود نمی‌شوند. کاربر مجاز می‌تواند cookies شخصی خودش را با فایل `cookies.txt` به ربات بدهد. رمز عبور ذخیره نمی‌شود؛ فقط فایل cookies روی سرور می‌ماند و با `/clearcookies` حذف می‌شود.

برای ساخت cookies:

1. در مرورگر وارد حساب خودت شو.
2. cookies را با فرمت Netscape `cookies.txt` خروجی بگیر.
3. فایل را به ربات بفرست.

مدیر می‌تواند cookies عمومی ربات را با ارسال `cookies.txt` و کپشن `global` ذخیره کند و با دستور زیر حذف کند:

```text
/clearcookies global
```

## CAPTCHA و پیام "I'm not a robot"

ربات CAPTCHA را دور نمی‌زند و روی پیام‌هایی مثل `I'm not a robot` کلیک خودکار نمی‌کند.

اگر Instagram یا YouTube چنین چالشی خواست، کاربر باید در مرورگر خودش لاگین کند، چالش را دستی حل کند، cookies را خروجی بگیرد و فایل `cookies.txt` را به ربات بدهد. این روش خطاهای لاگین را کمتر می‌کند، اما تضمین نمی‌کند که سرویس مقصد هیچ‌وقت دوباره چالش امنیتی نخواهد.

## مدیریت روی سرور

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

برای آپدیت برنامه، dependencyها و restart سرویس:

```bash
cd instagram-youtube-soundcloud-downloader
python3 update.py
```

برای حذف فقط سرویس systemd:

```bash
python3 uninstall.py
```

برای حذف سرویس و کل پوشه پروژه:

```bash
python3 remove.py
```

`remove.py` قبل از حذف کامل از تو تایید جدی می‌گیرد.

## اجرای دستی برای توسعه

```bash
cp .env.example .env
nano .env
python3 run.py
```

## اجرای تست‌ها

```bash
python3 -m unittest discover -s tests
```

## تنظیمات `.env`

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

`PLAYLIST_LIMIT` جلوی دانلود ناخواسته تعداد زیادی فایل از profile یا playlist را می‌گیرد.

`MAX_UPLOAD_MB` باید با محدودیت ارسال Bot API محیط تو هماهنگ باشد.

## لینک‌های نمونه

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

## سالم نگه داشتن دانلودها

Instagram، YouTube و SoundCloud ممکن است ساختار یا محدودیت‌هایشان را تغییر دهند. برای سالم ماندن پروژه، همیشه `yt-dlp` را به‌روز نگه دار و از `python3 update.py` استفاده کن.
