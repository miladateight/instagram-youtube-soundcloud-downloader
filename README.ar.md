# بوت تنزيل تيليجرام

**اللغة:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

بوت تيليجرام خاص ومناسب للعرض في السيرة المهنية لتنزيل الوسائط المدعومة من YouTube و YouTube Shorts و Instagram و SoundCloud.

المشروع مكتوب بالكامل بلغة Python ويحتوي على مثبت بسيط لـ Ubuntu. بعد التثبيت يبقى البوت غير مفعل حتى يقوم المدير بتفعيله من داخل تيليجرام.

> ملاحظة قانونية: هذا المشروع مخصص للاختبار والتعلم والاستخدام الشخصي. قبل الاستخدام العام، راجع شروط المنصات وحقوق النشر والخصوصية وحدود Telegram Bot API.

## الميزات

- اكتشاف تلقائي لروابط YouTube و `youtu.be` و Shorts و Instagram و SoundCloud
- تنزيل وإرسال الفيديو والصور والصوت والملفات العامة عبر `yt-dlp`
- دعم منشورات Instagram و Reels والملفات الشخصية والعديد من منشورات carousel
- إرسال منشورات Instagram متعددة العناصر كألبوم أو media group
- التعامل مع الوصف الطويل عبر معاينة قصيرة وزر لعرض الوصف الكامل
- واجهة بوت بأربع لغات: الفارسية، الإنجليزية، العربية، والألمانية
- سؤال المستخدم عن اللغة مرة واحدة فقط، وتغييرها لاحقاً عبر `/language`
- تفعيل البوت بواسطة المدير من داخل تيليجرام
- فتح وإغلاق الوصول العام عبر `/public_on` و `/public_off`
- رفع cookies شخصية بواسطة المستخدمين المسموح لهم، وcookies عامة بواسطة المدير
- اشتراك إجباري في قناة يتحكم به المدير
- إرسال SoundCloud بشكل أفضل مع صورة الغلاف واسم المقطع واسم الفنان
- تثبيت وتحديث وإزالة كاملة عبر سكربتات Python على Ubuntu
- تشغيل دائم عبر systemd وسجلات داخل `logs/bot.log`

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

## أوامر المستخدم

- `/start` يبدأ البوت؛ إذا كانت اللغة محفوظة يعرض رسالة قصيرة فقط
- `/language` أو `/lang` تغيير لغة المستخدم
- `/help` عرض المساعدة
- `/id` عرض المعرّف الرقمي للمستخدم
- `/status` عرض حالة البوت
- `/cookies` شرح رفع cookies الشخصية
- `/clearcookies` حذف cookies الشخصية المحفوظة

## أوامر المدير

- `/admin` فتح لوحة المدير
- `/activate` تفعيل التنزيلات
- `/deactivate` تعطيل التنزيلات
- `/public_on` فتح الوصول العام
- `/public_off` إغلاق الوصول العام
- `/clearcookies global` حذف cookies العامة للبوت
- `/forcejoin` عرض حالة الاشتراك الإجباري
- `/forcejoin_on @channel` تفعيل الاشتراك الإجباري
- `/forcejoin_off` تعطيل الاشتراك الإجباري

## الوصول العام

البوت خاص افتراضياً. يستطيع المدير فتح أو إغلاق الوصول العام من داخل البوت:

```text
/public_on
/public_off
```

إذا كان الوصول العام مغلقاً، يستطيع المدير والمستخدمون المسموح لهم فقط استخدام البوت.

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

## Cookies لـ Instagram و YouTube

قد تحتاج بعض روابط Instagram أو YouTube إلى تسجيل دخول. يستطيع كل مستخدم مسموح له رفع ملف cookies شخصي باسم `cookies.txt`. لا يتم حفظ كلمات المرور؛ يتم حفظ ملف cookies فقط على الخادم ويمكن حذفه عبر `/clearcookies`.

لإنشاء cookies:

1. سجّل الدخول من المتصفح.
2. صدّر cookies بصيغة Netscape `cookies.txt`.
3. أرسل الملف إلى البوت.

يستطيع المدير حفظ cookies عامة للبوت بإرسال `cookies.txt` مع الوصف `global`، ثم حذفها عبر:

```text
/clearcookies global
```

## CAPTCHA ورسالة "I'm not a robot"

البوت لا يتجاوز CAPTCHA ولا يضغط تلقائياً على رسائل مثل `I'm not a robot`.

إذا طلب Instagram أو YouTube تحدياً أمنياً، يجب على المستخدم تسجيل الدخول يدوياً في المتصفح، حل التحدي يدوياً، تصدير cookies بصيغة Netscape، ثم رفع `cookies.txt` إلى البوت. هذا يقلل مشاكل تسجيل الدخول، لكنه لا يضمن أن المنصة لن تطلب تحققاً مرة أخرى.

## إدارة الخادم

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

لتحديث البرنامج والاعتماديات وإعادة تشغيل الخدمة:

```bash
cd instagram-youtube-soundcloud-downloader
python3 update.py
```

لإزالة خدمة systemd فقط:

```bash
python3 uninstall.py
```

لإزالة الخدمة وحذف مجلد المشروع بالكامل:

```bash
python3 remove.py
```

`remove.py` يطلب تأكيداً واضحاً قبل الحذف الكامل.

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

قد يغير Instagram و YouTube و SoundCloud صفحاتهم أو قيودهم. للحفاظ على عمل المشروع، حدّث `yt-dlp` دائماً واستخدم `python3 update.py`.
