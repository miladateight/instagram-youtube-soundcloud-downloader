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
- قرار دادن caption روی اولین فایل ارسالی
- رابط کاربری چهارزبانه: فارسی، انگلیسی، عربی و آلمانی
- انتخاب زبان کاربر با `/language`
- فعال‌سازی ربات توسط مدیر از داخل تلگرام
- آپلود و حذف `cookies.txt` توسط مدیر از داخل ربات
- عضویت اجباری قابل فعال/غیرفعال‌سازی توسط مدیر
- دسترسی خصوصی به صورت پیش‌فرض، با امکان عمومی‌سازی از طریق `.env`
- نصب با Python و اجرای دائمی با systemd روی Ubuntu
- لاگ فایل داخل `logs/bot.log`

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

## دستورهای داخل ربات

- `/start` شروع ربات و نمایش انتخاب زبان
- `/language` یا `/lang` تغییر زبان کاربر
- `/help` راهنما
- `/id` نمایش آیدی عددی کاربر
- `/status` نمایش وضعیت ربات
- `/admin` پنل مدیر
- `/activate` فعال کردن دانلودها
- `/deactivate` غیرفعال کردن دانلودها
- `/cookies` راهنمای آپلود cookies
- `/clearcookies` حذف cookies ذخیره‌شده
- `/forcejoin` وضعیت عضویت اجباری
- `/forcejoin_on @channel` فعال کردن عضویت اجباری
- `/forcejoin_off` غیرفعال کردن عضویت اجباری

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

## Cookies برای Instagram و YouTube

بعضی لینک‌های Instagram یا YouTube بدون لاگین دانلود نمی‌شوند. مدیر می‌تواند از داخل خود ربات `cookies.txt` بدهد:

1. در مرورگر وارد حساب خودت شو.
2. cookies را با فرمت Netscape `cookies.txt` خروجی بگیر.
3. فایل را به ربات بفرست.

اگر اسم فایل مشخص نیست، آن را با کپشن زیر ارسال کن:

```text
/cookies
```

ربات فایل cookies را داخل `data/cookies.txt` ذخیره می‌کند. این فایل حساس است و در Git قرار نمی‌گیرد.

## CAPTCHA و پیام "I'm not a robot"

ربات CAPTCHA را دور نمی‌زند و روی پیام‌هایی مثل `I'm not a robot` کلیک خودکار نمی‌کند.

اگر Instagram یا YouTube چنین چالشی خواست:

1. مدیر باید در مرورگر خودش لاگین کند.
2. چالش امنیتی را دستی حل کند.
3. cookies را با فرمت Netscape `cookies.txt` خروجی بگیرد.
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

Instagram، YouTube و SoundCloud ممکن است ساختار یا محدودیت‌هایشان را تغییر دهند. برای سالم ماندن پروژه، `yt-dlp` را به‌روز نگه دار:

```bash
cd instagram-youtube-soundcloud-downloader
.venv/bin/pip install --upgrade yt-dlp
sudo systemctl restart telegram-downloader.service
```
