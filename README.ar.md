# بوت تنزيل تيليجرام

**اللغة:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

بوت تيليجرام خاص ومناسب للعرض في السيرة المهنية لتنزيل الوسائط المدعومة من YouTube و YouTube Shorts و Instagram و SoundCloud.

المشروع مكتوب بالكامل بلغة Python ويحتوي على مثبت بسيط لـ Ubuntu. بعد التثبيت يبقى البوت غير مفعل حتى يقوم المدير بتفعيله من داخل تيليجرام.

> ملاحظة قانونية: هذا المشروع مخصص للاختبار والتعلم والاستخدام الشخصي. قبل الاستخدام العام، راجع شروط المنصات وحقوق النشر والخصوصية وحدود Telegram Bot API.

## الميزات

- اكتشاف تلقائي لروابط YouTube و `youtu.be` و Shorts و Instagram و SoundCloud
- إرسال الفيديو والصور والصوت والملفات العامة عبر `yt-dlp`
- دعم منشورات Instagram و Reels والملفات الشخصية والعديد من منشورات carousel
- إرسال منشورات Instagram متعددة العناصر كألبوم أو media group
- وضع الوصف على أول ملف مرسل
- واجهة بوت بأربع لغات: الفارسية، الإنجليزية، العربية، والألمانية
- اختيار لغة المستخدم عبر `/language`
- تفعيل المدير للبوت من داخل تيليجرام
- رفع وحذف `cookies.txt` بواسطة المدير
- اشتراك إجباري في قناة يتحكم به المدير
- وصول خاص افتراضياً، مع إمكانية فتحه للعامة من خلال `.env`
- مثبت Python وخدمة systemd على Ubuntu
- سجلات الخدمة داخل `logs/bot.log`

## التثبيت السريع على Ubuntu

```bash
git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git && cd instagram-youtube-soundcloud-downloader && python3 install.py
```

سيسألك المثبت عن:

- اسم البوت
- توكن البوت من BotFather
- المعرّف الرقمي للمدير في تيليجرام

بعد التثبيت، افتح البوت في تيليجرام كمدير وأرسل:

```text
/activate
```

لن يقوم البوت بأي تنزيل حتى يتم تفعيله.

## أوامر البوت

- `/start` بدء البوت وعرض اختيار اللغة
- `/language` أو `/lang` تغيير لغة المستخدم
- `/help` عرض المساعدة
- `/id` عرض المعرّف الرقمي للمستخدم
- `/status` عرض حالة البوت
- `/admin` فتح لوحة المدير
- `/activate` تفعيل التنزيلات
- `/deactivate` تعطيل التنزيلات
- `/cookies` شرح رفع cookies
- `/clearcookies` حذف cookies المحفوظة
- `/forcejoin` عرض حالة الاشتراك الإجباري
- `/forcejoin_on @channel` تفعيل الاشتراك الإجباري
- `/forcejoin_off` تعطيل الاشتراك الإجباري

## الاشتراك الإجباري

يمكن للمدير إجبار المستخدمين على الاشتراك في قناة تيليجرام قبل التنزيل.

```text
/forcejoin_on @your_channel
```

للتعطيل:

```text
/forcejoin_off
```

يجب أن يكون البوت عضواً أو مديراً في القناة المطلوبة حتى يستطيع Telegram التحقق من العضوية. المدير لا يتم منعه بسبب الاشتراك الإجباري.

## إدارة الخدمة

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

إزالة الخدمة:

```bash
python3 uninstall.py
```

## التشغيل اليدوي للتطوير

```bash
cp .env.example .env
nano .env
python3 run.py
```

## الاختبارات

```bash
python3 -m unittest discover -s tests
```

## Cookies لـ Instagram و YouTube

قد تحتاج بعض روابط Instagram أو YouTube إلى تسجيل دخول. يمكن للمدير رفع `cookies.txt` من داخل تيليجرام:

1. سجّل الدخول من المتصفح.
2. صدّر cookies بصيغة Netscape `cookies.txt`.
3. أرسل الملف إلى البوت.

إذا لم يكن اسم الملف واضحاً، أرسله مع الوصف التالي:

```text
/cookies
```

يحفظ البوت cookies داخل `data/cookies.txt`. هذا الملف حساس ويتم تجاهله من Git.

## CAPTCHA ورسالة "I'm not a robot"

البوت لا يتجاوز CAPTCHA ولا يضغط تلقائياً على رسائل مثل `I'm not a robot`.

إذا طلب Instagram أو YouTube تحدياً أمنياً:

1. يقوم المدير بتسجيل الدخول يدوياً في المتصفح.
2. يحل التحدي يدوياً.
3. يصدّر cookies بصيغة Netscape `cookies.txt`.
4. يرفع الملف إلى البوت من داخل تيليجرام.

هذا يقلل مشاكل تسجيل الدخول، لكنه لا يضمن أن المنصة لن تطلب تحققاً مرة أخرى.

## إعدادات `.env`

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

`PLAYLIST_LIMIT` يحمي الخادم من تنزيل عدد كبير جداً من عناصر profile أو playlist.

`MAX_UPLOAD_MB` يجب أن يتوافق مع قدرة الرفع في Telegram Bot API لديك.

## روابط أمثلة

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

## الحفاظ على دعم التنزيل

قد يغير Instagram و YouTube و SoundCloud صفحاتهم أو قيودهم. حافظ على تحديث `yt-dlp`:

```bash
cd instagram-youtube-soundcloud-downloader
.venv/bin/pip install --upgrade yt-dlp
sudo systemctl restart telegram-downloader.service
```
