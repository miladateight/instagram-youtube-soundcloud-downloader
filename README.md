# Telegram Downloader Bot

ربات خصوصی و قابل ارائه برای دانلود لینک‌های YouTube، YouTube Shorts، Instagram و SoundCloud در تلگرام.

این پروژه با Python نوشته شده و برای نصب ساده روی Ubuntu آماده است. ربات بعد از نصب به صورت پیش‌فرض غیرفعال می‌ماند و فقط مدیر می‌تواند از داخل تلگرام آن را فعال کند.

> نکته حقوقی: این پروژه برای تست، یادگیری و استفاده شخصی ساخته شده است. قبل از استفاده عمومی، قوانین سرویس‌ها، حق نشر، حریم خصوصی و محدودیت‌های Telegram Bot API را بررسی کن.

## قابلیت‌ها

- تشخیص خودکار لینک‌های YouTube، `youtu.be`، Shorts، Instagram و SoundCloud
- دانلود و ارسال ویدیو، عکس، فایل صوتی و فایل‌های عمومی قابل دریافت با `yt-dlp`
- پشتیبانی از پست‌ها، ریلزها و بسیاری از carouselهای Instagram
- ارسال پست‌های چندتایی Instagram به شکل album/media group
- قرار دادن caption روی اولین فایل ارسالی
- پنل مدیریتی داخل خود ربات
- فعال‌سازی/غیرفعال‌سازی از داخل تلگرام
- آپلود و حذف `cookies.txt` توسط مدیر از داخل ربات
- محدودسازی ربات به مدیر یا باز کردن دسترسی عمومی با تنظیم `.env`
- نصب با Python و اجرای دائمی با systemd
- لاگ فایل داخل `logs/bot.log`

## نصب سریع روی Ubuntu

بعد از اینکه پروژه را روی GitHub گذاشتی، دستور را با آدرس repo خودت جایگزین کن:

```bash
git clone https://github.com/YOUR_USERNAME/Downloader.git && cd Downloader && python3 install.py
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

## مدیریت سرویس

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

برای حذف سرویس:

```bash
python3 uninstall.py
```

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

## دستورهای داخل ربات

- `/start` شروع و راهنما
- `/help` راهنما
- `/id` نمایش آیدی عددی کاربر
- `/status` نمایش وضعیت ربات
- `/admin` پنل مدیر
- `/activate` فعال کردن دانلودها
- `/deactivate` غیرفعال کردن دانلودها
- `/cookies` راهنمای آپلود cookies
- `/clearcookies` حذف cookies ذخیره‌شده

## فعال‌سازی و امنیت

ربات بعد از نصب inactive است. حتی اگر سرویس systemd روشن باشد، تا وقتی مدیر `/activate` نزند دانلود انجام نمی‌شود.

در حالت پیش‌فرض فقط مدیر می‌تواند از ربات استفاده کند:

```env
ALLOW_ALL_USERS=false
```

اگر برای دمو خواستی همه بتوانند بعد از فعال‌سازی از آن استفاده کنند:

```env
ALLOW_ALL_USERS=true
```

سپس سرویس را ری‌استارت کن:

```bash
sudo systemctl restart telegram-downloader.service
```

## Cookies برای Instagram و YouTube

بعضی لینک‌های Instagram یا YouTube بدون لاگین دانلود نمی‌شوند. مدیر می‌تواند از داخل خود ربات cookies بدهد:

1. در مرورگر وارد حساب خودت شو.
2. cookies را با فرمت Netscape `cookies.txt` خروجی بگیر.
3. فایل `cookies.txt` را به ربات بفرست.

اگر اسم فایل مشخص نیست، آن را با کپشن زیر ارسال کن:

```text
/cookies
```

ربات فایل cookies را داخل `data/cookies.txt` ذخیره می‌کند. این فایل حساس است و در `.gitignore` قرار دارد؛ آن را داخل GitHub نگذار.

## CAPTCHA و پیام I'm not a robot

ربات CAPTCHA را دور نمی‌زند و روی پیام‌هایی مثل `I'm not a robot` کلیک خودکار نمی‌کند. این کار از نظر فنی پایدار نیست و می‌تواند خلاف قوانین سرویس‌ها باشد.

اگر Instagram یا YouTube چنین چیزی خواست:

1. مدیر باید در مرورگر خودش لاگین کند.
2. اگر CAPTCHA یا چالش امنیتی آمد، همان‌جا دستی حلش کند.
3. بعد cookies را با فرمت Netscape `cookies.txt` خروجی بگیرد.
4. فایل را از داخل تلگرام برای ربات بفرستد.

این روش احتمال خطاهای لاگین را کم می‌کند، اما تضمین نمی‌کند که سرویس مقصد هیچ‌وقت دوباره چالش امنیتی نخواهد.

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

`MAX_UPLOAD_MB` باید با محدودیت ارسال Bot API محیط تو هماهنگ باشد. مقدار پیش‌فرض محافظه‌کارانه است.

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

## محدودیت‌های واقعی

این ربات تا حد ممکن کامل طراحی شده، اما خود Instagram، YouTube و SoundCloud ممکن است ساختار یا محدودیت‌هایشان را تغییر دهند. برای سالم ماندن پروژه، وابستگی `yt-dlp` را به‌روز نگه دار:

```bash
cd Downloader
.venv/bin/pip install --upgrade yt-dlp
sudo systemctl restart telegram-downloader.service
```
