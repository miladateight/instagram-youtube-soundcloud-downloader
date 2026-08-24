# Ateight Downloader

**زبان:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

**نسخه ۱.۱.۰**

یک ربات خصوصی و رزومه‌ای تلگرام برای دانلود رسانه از YouTube، YouTube Shorts، Instagram و SoundCloud — با دکمه‌های شیشه‌ای، تشخیص آهنگ و نصب تعاملی.

این پروژه کاملاً با Python نوشته شده و برای نصب ساده روی Ubuntu آماده است. ربات بعد از نصب به صورت پیش‌فرض غیرفعال می‌ماند تا مدیر از داخل تلگرام آن را فعال کند.

> نکته حقوقی: این پروژه برای تست، یادگیری و استفاده شخصی ساخته شده است. قبل از استفاده عمومی، قوانین سرویس‌ها، حق نشر، حریم خصوصی و محدودیت‌های Telegram Bot API را بررسی کن.

## قابلیت‌ها

### دانلود
- تشخیص خودکار لینک‌های YouTube، `youtu.be`، Shorts، `m.youtube.com`، `music.youtube.com`، Instagram و SoundCloud
- دانلود و ارسال ویدیو، عکس، فایل صوتی و فایل‌های عمومی با `yt-dlp`
- پشتیبانی از پست‌ها، ریلزها، پروفایل‌ها و بسیاری از carouselهای Instagram
- استفاده از fallback مبتنی بر `gallery-dl` برای پست‌ها و پروفایل‌های صرفاً عکس وقتی `yt-dlp` ویدیویی برنمی‌گرداند
- ارسال carouselهای Instagram به‌صورت آلبوم تلگرام
- **ابعاد صحیح ویدیو** — ریلزها و شورتزها نسبت ابعاد اصلی خود را حفظ می‌کنند (دیگه مربعی نمی‌شوند)
- دانلود ویدیوهای YouTube ترجیحاً به‌صورت MP4 دوستانه تلگرام به‌جای WebM
- SoundCloud: بهترین کیفیت صوتی برای فایل‌های زیر ۱۵ دقیقه، کاور آلبوم جداگانه قبل از صدا ارسال می‌شود
- کپشن به اولین فایل اضافه می‌شود
- کپشن‌های طولانی به‌صورت ایمن کوتاه می‌شوند با دکمه «دریافت کامل کپشن»
- fallback به ارسال به‌عنوان فایل اگه حجم از حد تلگرام بیشتر باشه

### تجربه کاربری
- **دکمه‌های شیشه‌ای** — بعد از فرستادن لینک، ربات می‌پرسه چه می‌خوای: فیلم، صدا (MP3) یا پیدا کردن آهنگ
- **منوی کیبورد دائمی** — دکمه‌های پایین چت: دانلود، MP3، وضعیت، زبان، اشتراک‌گذاری، پشتیبانی
- **تشخیص آهنگ** — آهنگ داخل ویدیو رو با شزم شناسایی می‌کنه (رایگان، بدون نیاز به API key)
- **دکمه پشتیبانی** — کاربرا می‌تونن مستقیم از هر پیام خطایی با مدیر در ارتباط باشن
- **دکمه اشتراک‌گذاری** — کاربرا می‌تونن ربات رو به دوستاشون معرفی کنن
- پیشرفت واقعی دانلود (با استفاده از progress hookهای yt-dlp)
- محافظ ضد اسپم برای هر کاربر: یه دانلود فعال و یه درخواست جدید هر ۵ ثانیه
- رابط کاربری چهار زبانه: فارسی، انگلیسی، عربی و آلمانی
- انتخاب زبان یک‌باره، با تغییر دستی از `/language`
- پیام‌های خطای دسته‌بندی‌شده (ارورهای خام yt-dlp به کاربر نشون داده نمی‌شه)

### مدیر
- فعال‌سازی از داخل تلگرام
- آپلود و حذف `cookies.txt` شخصی برای هر کاربر
- `cookies.txt` عمومی اختیاری برای مدیر
- عضویت اجباری کانال کنترل‌شده توسط مدیر
- دسترسی خصوصی به‌صورت پیش‌فرض، با حالت عمومی کنترل‌شده از پنل مدیر
- فعال/غیرفعال کردن پلتفرم‌ها: YouTube، Instagram، SoundCloud یا تشخیص آهنگ

### نصب
- **منوی تعاملی انتخاب ویژگی‌ها** (whiptail روی لینوکس، fallback متنی)
- بنر ASCII art برند Ateight
- پرسیدن نام ربات، توکن، آیدی مدیر، username پشتیبانی و username ربات
- انتخاب پلتفرم‌ها و قابلیت‌ها
- API key اختیاری برای شزم
- نصب Python و سرویس systemd برای Ubuntu
- اسکریپت‌های آپدیت و حذف برای سرورهای Ubuntu
- لاگ‌های سرویس در `logs/bot.log`

## نصب سریع روی Ubuntu

```bash
bash -c 'set -e; repo=instagram-youtube-soundcloud-downloader; if [ -f install.py ] && [ -d .git ]; then python3 install.py; elif [ -d "$repo/.git" ]; then cd "$repo" && python3 install.py; elif [ -e "$repo" ]; then echo "$repo already exists but is not a git checkout. Remove it first or choose another directory."; exit 1; else git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git "$repo" && cd "$repo" && python3 install.py; fi'
```

`python3 install.py` هم دستور آپدیت هست. اگه `.env` وجود داشته باشه، وابستگی‌ها رو آپدیت می‌کنه، آخرین کد رو می‌گیره و سرویس رو ری‌استارت می‌کنه:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```

نصب‌کننده این موارد رو می‌پرسه:

- نام ربات (پیش‌فرض: Ateight Downloader)
- توکن ربات از BotFather
- آیدی عددی مدیر تلگرام
- username مدیر تلگرام برای دکمه پشتیبانی (اختیاری)
- username ربات برای دکمه اشتراک‌گذاری (اختیاری)
- کدوم پلتفرم‌ها فعال باشن (YouTube، Instagram، SoundCloud)
- آیا تشخیص آهنگ (شزم) فعال باشه
- API key اختیاری برای شزم

بعد از نصب، ربات رو تو تلگرام باز کن و به‌عنوان مدیر بفرست:

```text
/activate
```

ربات تا فعال نشده چیزی دانلود نمی‌کنه.

## دستورات ربات

- `/start` شروع ربات؛ زبان فقط یک‌بار پرسیده می‌شه
- `/language` یا `/lang` تغییر زبان کاربر
- `/help` نمایش راهنما
- `/id` نمایش آیدی عددی کاربر
- `/mp3 <link>` دانلود فقط صدا به‌صورت MP3
- `/status` نمایش وضعیت cookies کاربر و وضعیت کامل برای مدیر
- `/admin` باز کردن پنل مدیر
- `/activate` فعال کردن دانلودها
- `/deactivate` غیرفعال کردن دانلودها
- `/public_on` باز کردن دسترسی عمومی
- `/public_off` بستن دسترسی عمومی
- `/cookies` راهنمای آپلود cookies
- `/clearcookies` حذف cookies شخصی کاربر
- `/clearcookies global` حذف cookies عمومی مدیر
- `/forcejoin` نمایش وضعیت عضویت اجباری
- `/forcejoin_on @channel` فعال کردن عضویت اجباری
- `/forcejoin_off` غیرفعال کردن عضویت اجباری
- `/support` نمایش دکمه پشتیبانی
- `/share` نمایش پیام آماده اشتراک‌گذاری
- `/about` نمایش اطلاعات ربات و نسخه

## چطور کار می‌کنه

۱. **لینک بفرست** — یه لینک YouTube، Instagram یا SoundCloud بفرست
۲. **فرمت رو انتخاب کن** — ربات دکمه‌های شیشه‌ای نشون می‌ده: فیلم، صدا (MP3) یا پیدا کردن آهنگ
۳. **نتیجه رو بگیر** — ربات دانلود می‌کنه و رسانه رو با ابعاد صحیح و thumbnail می‌فرسته

برای SoundCloud، ربات خودکار صدا رو دانلود می‌کنه (بدون دکمه) و کاور آلبوم رو جداگانه قبل از صدا می‌فرسته.

## عضویت اجباری

مدیر می‌تونه قبل از دانلود، عضویت کاربرا تو یه کانال تلگرام رو اجبار کنه.

```text
/forcejoin_on @your_channel
```

برای غیرفعال کردن:

```text
/forcejoin_off
```

ربات باید تو کانال عضو یا ادمین باشه تا تلگرام بتونه عضویت رو بررسی کنه. کاربرای ادمین توسط عضویت اجباری مسدود نمی‌شن.

## مدیریت سرویس

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

آپدیت ربات نصب‌شده:

```bash
python3 install.py
```

حذف فقط سرویس systemd:

```bash
python3 uninstall.py
```

حذف سرویس و پوشه پروژه:

```bash
python3 remove.py
```

## اجرای توسعه

```bash
cp .env.example .env
nano .env
python3 run.py
```

## تست‌ها

```bash
python3 -m unittest discover -s tests
```

## Cookies برای Instagram و YouTube

برخی لینک‌های Instagram یا YouTube ممکنه نیاز به لاگین داشته باشن. هر کاربر مجاز می‌تونه فایل `cookies.txt` شخصی خودش رو از داخل تلگرام آپلود کنه:

۱. تو مرورگر لاگین کن.
۲. cookies رو به فرمت Netscape `cookies.txt` خروجی بگیر.
۳. فایل رو به ربات بفرست.

اگه نام فایل واضح نیست، با این کپشن بفرست:

```text
/cookies
```

ربات cookies شخصی رو در `data/user_cookies/` ذخیره می‌کنه. رمز عبور ذخیره نمی‌شه؛ فقط فایل cookies روی سرور می‌ماند. کاربر می‌تونه با `/clearcookies` cookies خودش رو حذف کنه.

مدیر می‌تونه cookies عمومی ربات رو با ارسال `cookies.txt` با کپشن `global` آپلود کنه:

```text
global
```

cookies عمومی مدیر در `data/cookies.txt` ذخیره می‌شه و با `/clearcookies global` حذف می‌شه. فایل‌های cookies حساس هستن و توسط Git نادیده گرفته می‌شن.

## CAPTCHA و «من ربات نیستم»

ربات CAPTCHA رو دور نمی‌زنه و به‌صورت خودکار روی تاییدهایی مثل «من ربات نیستم» کلیک نمی‌کنه.

اگه Instagram یا YouTube چالش امنیتی خواست:

۱. کاربر یا مدیر تو مرورگر دستی لاگین کنه.
۲. چالش رو تو مرورگر دستی حل کنه.
۳. cookies رو به فرمت Netscape `cookies.txt` خروجی بگیره.
۴. فایل cookies رو به ربات آپلود کنه.

این کار可靠性 لاگین رو بهتر می‌کنه ولی تضمین نمی‌کنه که یه سرویس دیگه چالش نخواد.

## تنظیمات `.env`

```env
BOT_NAME=Ateight Downloader
BOT_TOKEN=123456789:replace-me
ADMIN_ID=123456789
SUPPORT_USERNAME=
BOT_USERNAME=
ALLOW_ALL_USERS=false
MAX_UPLOAD_MB=0
PLAYLIST_LIMIT=20
CONCURRENT_DOWNLOADS=4
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

`ALLOW_ALL_USERS` فقط پیش‌فرض اولیه‌ست. بعد از نصب، مدیر می‌تونه با `/public_on`، `/public_off` یا پنل مدیر دسترسی عمومی رو تغییر بده.

`PLAYLIST_LIMIT` سرور رو از دانلود profile یا playlistهای خیلی بزرگ محافظت می‌کنه.

`MAX_UPLOAD_MB=0` یعنی ربات فایل‌ها رو بر اساس حجم مسدود نمی‌کنه. Telegram Bot API همچنان ممکنه فایل‌های بالاتر از حد واقعیش رو رد کنه.

`SUPPORT_USERNAME` — اگه تنظیم بشه، دکمه پشتیبانی به `t.me/yourname` لینک می‌شه. وگرنه به `t.me/user?id=ADMIN_ID` برمی‌گرده.

`BOT_USERNAME` — اگه تنظیم بشه، دکمه اشتراک‌گذاری به `t.me/your_bot` لینک می‌شه.

`FORCE_IPV4` — می‌تونه با ارورهای YouTube HTTP 403 روی برخی سرورها یا VPNها کمک کنه.

`HTTP_PROXY` — proxy اختیاری برای دانلودهای yt-dlp.

## لینک‌های نمونه

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

## سلامت دانلودها

Instagram، YouTube و SoundCloud ممکنه صفحه‌ها یا محدودیت‌هاتون رو تغییر بدن. ربات و `yt-dlp` رو آپدیت نگه دار:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```
