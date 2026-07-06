# Atieght Downloader

**اللغة:** [English](README.md) | [فارسی](README.fa.md) | [العربية](README.ar.md) | [Deutsch](README.de.md)

**الإصدار 1.0.0**

بوت تيليجرام خاص ومناسب للعرض في السيرة المهنية لتنزيل الوسائط من YouTube و YouTube Shorts و Instagram و SoundCloud — مع أزرار شفافة واكتشاف الأغاني ومثبت تفاعلي.

المشروع مكتوب بالكامل بلغة Python ويحتوي على مثبت تفاعلي لـ Ubuntu مع قائمة اختيار الميزات. بعد التثبيت يبقى البوت غير مفعل حتى يقوم المدير بتفعيله من داخل تيليجرام.

> ملاحظة قانونية: هذا المشروع مخصص للاختبار والتعلم والاستخدام الشخصي. قبل الاستخدام العام، راجع شروط المنصات وحقوق النشر والخصوصية وحدود Telegram Bot API.

## الميزات

### التنزيل
- اكتشاف تلقائي للروابط من YouTube و `youtu.be` و Shorts و `m.youtube.com` و `music.youtube.com` و Instagram و SoundCloud
- تنزيل وإرسال الفيديو والصور والصوت والملفات عبر `yt-dlp`
- دعم منشورات Instagram و Reels والملفات الشخصية والعديد من carousel
- إرسال منشورات carousel كألبومات تيليجرام
- **أبعاد فيديو صحيحة** — تحافظ Reels و Shorts على نسبة أبعادها الأصلية
- تفضيل تنزيل فيديوهات YouTube بصيغة MP4 بدلاً من WebM
- SoundCloud: أفضل جودة صوت للملفات أقل من 15 دقيقة، غلاف الألبوم يُرسل بشكل منفصل قبل الصوت
- إضافة تعليق للملف الأول
- اختصار التعليقات الطويلة بأمان مع زر "الحصول على الوصف الكامل"
- التحويل إلى إرسال كملف إذا كان الحجم كبيراً جداً لتيليجرام

### تجربة المستخدم
- **أزرار شفافة** — بعد إرسال الرابط، يسأل البوت ما تريد: فيديو، صوت (MP3)، أو اكتشاف الأغنية
- **قائمة لوحة مفاتيح دائمة** — أزرار في الأسفل: تنزيل، MP3، الحالة، اللغة، مشاركة، دعم
- **اكتشاف الأغاني** — التعرف على الأغنية داخل الفيديو باستخدام Shazam (مجاني، بدون مفتاح API)
- **زر الدعم** — يمكن للمستخدمين الاتصال بالمدير مباشرة من أي رسالة خطأ
- **زر المشاركة** — يمكن للمستخدمين مشاركة البوت مع أصدقائهم
- تقدم تنزيل حقيقي (باستخدام yt-dlp progress hooks)
- حماية ضد الرسائل المزعجة لكل مستخدم
- واجهة بأربع لغات: الفارسية والإنجليزية والعربية والألمانية
- رسائل خطأ مصنفة (لا تُعرض أخطاء yt-dlp الخام للمستخدمين)

### المدير
- التفعيل من داخل تيليجرام
- رفع وإزالة `cookies.txt` شخصي لكل مستخدم
- `cookies.txt` عام اختياري للمدير
- اشتراك قناة إجباري يتحكم فيه المدير
- وصول خاص افتراضياً، مع وضع عام يتحكم فيه المدير
- تفعيل/تعطيل المنصات: YouTube و Instagram و SoundCloud أو اكتشاف الأغاني

### المثبت
- **قائمة تفاعلية لاختيار الميزات** (whiptail على Linux، بديل نصي في غيره)
- لافتة ASCII art بعلامة Atieght
- يسأل عن اسم البوت والرمز ومعرف المدير واسم المستخدم للدعم واسم البوت
- اختيار المنصات والميزات
- مفتاح API اختياري لـ Shazam
- مثبت Python وخدمة systemd لـ Ubuntu
- نصوص التحديث والإزالة لخوادم Ubuntu
- سجلات الخدمة في `logs/bot.log`

## التثبيت السريع على Ubuntu

```bash
bash -c 'set -e; repo=instagram-youtube-soundcloud-downloader; if [ -f install.py ] && [ -d .git ]; then python3 install.py; elif [ -d "$repo/.git" ]; then cd "$repo" && python3 install.py; elif [ -e "$repo" ]; then echo "$repo already exists but is not a git checkout. Remove it first or choose another directory."; exit 1; else git clone https://github.com/miladateight/instagram-youtube-soundcloud-downloader.git "$repo" && cd "$repo" && python3 install.py; fi'
```

`python3 install.py` هو أيضاً أمر التحديث. إذا كان `.env` موجوداً، يقوم بتحديث التبعيات وسحب أحدث كود وإعادة تشغيل الخدمة:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```

يسأل المثبت عن:

- اسم البوت (افتراضي: Atieght Downloader)
- رمز البوت من BotFather
- معرف المدير الرقمي في تيليجرام
- اسم مستخدم المدير للدعم (اختياري)
- اسم مستخدم البوت للمشاركة (اختياري)
- المنصات المراد تفعيلها (YouTube و Instagram و SoundCloud)
- هل تفعيل اكتشاف الأغاني (Shazam)
- مفتاح API اختياري لـ Shazam

بعد التثبيت، افتح البوت في تيليجرام كمدير وأرسل:

```text
/activate
```

لن يقوم البوت بتنزيل أي شيء حتى يتم تفعيله.

## أوامر البوت

- `/start` يبدأ البوت؛ تُطلب اللغة مرة واحدة فقط
- `/language` أو `/lang` تغيير لغة المستخدم
- `/help` عرض المساعدة
- `/id` عرض معرف المستخدم الرقمي
- `/mp3 <link>` تنزيل الصوت فقط بصيغة MP3
- `/status` عرض حالة cookies للمستخدم والحالة الكاملة للمدير
- `/admin` فتح لوحة المدير
- `/activate` تفعيل التنزيلات
- `/deactivate` تعطيل التنزيلات
- `/public_on` فتح الوصول العام
- `/public_off` إغلاق الوصول العام
- `/cookies` شرح كيفية رفع cookies
- `/clearcookies` إزالة cookies الشخصية
- `/clearcookies global` إزالة cookies العامة للمدير
- `/forcejoin` عرض حالة الاشتراك الإجباري
- `/forcejoin_on @channel` تفعيل الاشتراك الإجباري
- `/forcejoin_off` تعطيل الاشتراك الإجباري
- `/support` عرض زر الدعم
- `/share` عرض رسالة مشاركة جاهزة
- `/about` عرض معلومات البوت والإصدار

## كيف يعمل

1. **أرسل رابطاً** — الصق رابط YouTube أو Instagram أو SoundCloud
2. **اختر صيغة** — يعرض البوت أزراراً شفافة: فيديو، صوت (MP3)، أو اكتشاف أغنية
3. **احصل على النتيجة** — يقوم البوت بتنزيل وإرسال الوسائط بأبعاد صحيحة وصورة مصغرة

بالنسبة لـ SoundCloud، يقوم البوت بتنزيل الصوت تلقائياً (بدون أزرار) ويرسل غلاف الألبوم بشكل منفصل قبل الصوت.

## الاشتراك الإجباري

يمكن للمدير طلب انضمام المستخدمين إلى قناة تيليجرام قبل التنزيل.

```text
/forcejoin_on @your_channel
```

للتعطيل:

```text
/forcejoin_off
```

يجب أن يكون البوت عضواً أو مديراً في القناة المطلوبة حتى يتمكن تيليجرام من التحقق من العضوية. لا يتم حظر المستخدمين المديرين بواسطة الاشتراك الإجباري.

## إدارة الخدمة

```bash
sudo systemctl status telegram-downloader.service
sudo journalctl -u telegram-downloader.service -f
sudo systemctl restart telegram-downloader.service
```

تحديث البوت المثبت:

```bash
python3 install.py
```

إزالة خدمة systemd فقط:

```bash
python3 uninstall.py
```

إزالة الخدمة وحذف مجلد المشروع:

```bash
python3 remove.py
```

## التشغيل التطويري

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

قد تتطلب بعض روابط Instagram أو YouTube تسجيل الدخول. يمكن لكل مستخدم مسموح رفع ملف `cookies.txt` شخصي من داخل تيليجرام:

1. سجل الدخول عبر متصفح.
2. صدّر cookies بصيغة Netscape `cookies.txt`.
3. أرسل الملف إلى البوت.

إذا لم يكن اسم الملف واضحاً، أرسله مع هذا التعليق:

```text
/cookies
```

يخزن البوت cookies الشخصية في `data/user_cookies/`. لا يتم تخزين كلمات المرور؛ فقط ملف cookies يبقى على الخادم. يمكن للمستخدم إزالة cookies الشخصية بـ `/clearcookies`.

يمكن للمدير رفع cookies عامة للبوت بإرسال `cookies.txt` مع التعليق:

```text
global
```

يتم تخزين cookies العامة في `data/cookies.txt` ويمكن إزالتها بـ `/clearcookies global`. ملفات cookies حساسة ويتم تجاهلها بواسطة Git.

## CAPTCHA و "أنا لست روبوتاً"

لا يتجاوز البوت CAPTCHA ولا ينقر تلقائياً على عبارات التحقق مثل "أنا لست روبوتاً".

إذا طلب Instagram أو YouTube تحدي أمني:

1. يسجل المستخدم أو المدير الدخول يدوياً في متصفح.
2. يتم حل التحدي يدوياً في المتصفح.
3. يتم تصدير cookies بصيغة Netscape `cookies.txt`.
4. يتم رفع ملف cookies إلى البوت.

## إعدادات `.env`

```env
BOT_NAME=Atieght Downloader
BOT_TOKEN=123456789:replace-me
ADMIN_ID=123456789
SUPPORT_USERNAME=
BOT_USERNAME=
ALLOW_ALL_USERS=false
MAX_UPLOAD_MB=0
PLAYLIST_LIMIT=20
CONCURRENT_DOWNLOADS=100
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

## روابط نموذجية

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

## الحفاظ على سلامة التنزيلات

قد تغير Instagram و YouTube و SoundCloud صفحاتها أو قيودها. حافظ على تحديث البوت و `yt-dlp`:

```bash
cd instagram-youtube-soundcloud-downloader
python3 install.py
```