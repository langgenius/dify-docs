# سوالات متداول در مورد میزبانی خود / استقرار محلی (FAQs)

### 1. چگونه می توان رمز عبور را پس از مقداردهی اولیه استقرار محلی، در صورت نادرست بودن،  ریست کرد؟

اگر از Docker Compose برای استقرار استفاده کردید، می توانید با دستور زیر رمز عبور را ریست کنید:

```
docker exec -it docker-api-1 flask reset-password
```

ایمیل حساب و رمز عبور جدید را دو بار وارد کنید.

### 2. چگونه می توان خطای "فایل یافت نشد" را در لاگ های استقرار محلی حل کرد؟

```
ERROR:root:Unknown Error in completion
Traceback (most recent call last):
  File "/www/wwwroot/dify/dify/api/libs/rsa.py", line 45, in decrypt
    private_key = storage.load(filepath)
  File "/www/wwwroot/dify/dify/api/extensions/ext_storage.py", line 65, in load
    raise FileNotFoundError("File not found")
FileNotFoundError: File not found
```

این خطا ممکن است به دلیل تغییر روش استقرار یا حذف دایرکتوری `api/storage/privkeys` رخ دهد. این فایل برای رمزگذاری کلیدهای مدل بزرگ استفاده می شود، بنابراین از دست دادن آن غیرقابل برگشت است. می توانید با دستورات زیر جفت کلید رمزنگاری را ریست کنید:

* استقرار Docker Compose

    ```
    docker exec -it docker-api-1 flask reset-encrypt-key-pair
    ```
* راه اندازی کد منبع

    به دایرکتوری `api` بروید

    ```
    flask reset-encrypt-key-pair
    ```

    دستورالعمل ها را برای ریست دنبال کنید.

### 3. بعد از نصب، قادر به ورود نیستم یا  بعد از ورود موفقیت آمیز،  در رابط های بعدی با خطای 401 مواجه می شوم؟

این ممکن است به دلیل تغییر دامنه/URL رخ دهد و  باعث ایجاد مشکلات بین سرور  و کلاینت می شود.  مشکلات  تعیین هویت و  متقاطع دامنه شامل  تنظیمات زیر است:

1. تنظیمات Cross-Domain CORS
   1. `CONSOLE_CORS_ALLOW_ORIGINS`

       سیاست CORS کنسول، پیش فرض آن `*` است، به این معنی که تمام دامنه ها می توانند دسترسی داشته باشند.
   2. `WEB_API_CORS_ALLOW_ORIGINS`

       سیاست CORS وب اپلیکیشن، پیش فرض آن `*` است، به این معنی که تمام دامنه ها می توانند دسترسی داشته باشند.

### 4. بعد از راه اندازی، صفحه  به طور مداوم در حال بارگیری است و درخواست ها خطای CORS نشان می دهند؟

این ممکن است به دلیل تغییر دامنه/URL رخ دهد و  باعث ایجاد مشکلات بین سرور  و کلاینت می شود.  آیتم های پیکربندی زیر را در `docker-compose.yml` به دامنه جدید به روز رسانی کنید:

`CONSOLE_API_URL:` URL سرور برای API کنسول.
`CONSOLE_WEB_URL:` URL کلاینت برای وب کنسول.
`SERVICE_API_URL:` URL برای API سرویس.
`APP_API_URL:` URL سرور برای API وب اپلیکیشن.
`APP_WEB_URL:` URL برای وب اپلیکیشن.

برای اطلاعات بیشتر،  لطفاً به: [متغیرهای محیطی](../../getting-started/install-self-hosted/environments.md) مراجعه کنید.

### 5.  بعد از استقرار،  چگونه  نسخه را ارتقا دهیم؟

اگر از تصویر شروع کردید،  آخرین تصویر را بکشید تا ارتقا تکمیل شود. اگر از کد منبع شروع کردید،  آخرین کد را بکشید و  سپس  آن را راه اندازی کنید تا ارتقا تکمیل شود.

برای بروزرسانی های استقرار کد منبع، به دایرکتوری `api`  بروید  و  دستور زیر را برای مهاجرت ساختار پایگاه داده به آخرین نسخه اجرا کنید:

`flask db upgrade`

### 6.  نحوه  تنظیم متغیرهای محیطی هنگام وارد کردن با استفاده از Notion

[**آدرس پیکربندی ادغام Notion**](https://www.notion.so/my-integrations). هنگام انجام استقرار خصوصی، تنظیمات زیر را انجام دهید:

1. **`NOTION_INTEGRATION_TYPE`**:  این مقدار باید به عنوان **public/internal**  تنظیم شود. از آنجایی که آدرس  مجدد  OAuth Notion فقط  از https پشتیبانی می کند، از ادغام داخلی Notion برای استقرار محلی استفاده کنید.
2. **`NOTION_CLIENT_SECRET`**:  راز  مشتری  OAuth Notion (برای نوع ادغام عمومی).
3. **`NOTION_CLIENT_ID`**:  شناسه  مشتری  OAuth (برای نوع ادغام عمومی).
4. **`NOTION_INTERNAL_SECRET`**:  راز ادغام داخلی Notion. اگر مقدار `NOTION_INTEGRATION_TYPE`   **internal**  باشد، این متغیر را  تنظیم کنید.

### 7. چگونه می توان  نام فضای  را در نسخه  استقرار محلی تغییر داد؟

 آن را در جدول `tenants`   پایگاه داده  تغییر دهید.

### 8.   کجا می توان دامنه را  برای دسترسی به  برنامه تغییر داد؟

دامنه پیکربندی `APP_WEB_URL`   را در `docker_compose.yaml`   پیدا کنید.

### 9. در صورت انجام مهاجرت پایگاه داده، چه چیزی را باید  بکاپ گرفت؟

پایگاه داده،  ذخیره سازی  تنظیم شده  و  داده های  پایگاه داده وکتوری را بکاپ بگیرید.  اگر  از  Docker Compose  برای استقرار استفاده کردید،  مستقیماً  همه داده ها را  در دایرکتوری `dify/docker/volumes`  بکاپ بگیرید.

### 10.  چرا  Dify  استقرار Docker نمی تواند به  پورت محلی  با استفاده از 127.0.0.1  هنگام راه اندازی OpenLLM  به طور محلی  دسترسی پیدا کند؟

127.0.0.1   آدرس داخلی  کانتینر است.  آدرس سرور پیکربندی شده  Dify  باید  آدرس شبکه  محلی  میزبان باشد.

### 11.   چگونه می توان   محدودیت  اندازه  و  تعداد آپلود  اسناد  در  مجموعه  داده ها  برای  نسخه  استقرار محلی را  حل کرد؟

برای  تنظیم  به  مستندات  متغیرهای محیطی  وب سایت  رسمی  [مستندات  متغیرهای محیطی](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/environments) مراجعه کنید.

### 12.   چگونه می توان در نسخه استقرار محلی از طریق ایمیل  اعضای جدید دعوت کرد؟

در  نسخه  استقرار محلی،  اعضای جدید  را  از  طریق ایمیل دعوت کنید.  بعد از  وارد کردن  ایمیل  و  ارسال دعوتنامه، صفحه  یک  لینک  دعوت نمایش می دهد.  لینک  دعوت را  کپی کنید و  آن  را  به  کاربر  ارسال کنید.  کاربر  می تواند  لینک  را  باز کند، از طریق  ایمیل  وارد  شود،  رمز عبور  را  تنظیم کند  و  به  فضای  شما  وارد شود.

### 13.   در صورت مواجهه با خطای "Can't load tokenizer for 'gpt2'"   در نسخه  استقرار محلی چه کاری باید  انجام داد؟

```
Can't load tokenizer for 'gpt2'. If you were trying to load it from 'https://huggingface.co/models', make sure you don't have a local directory with the same name. Otherwise, make sure 'gpt2' is the correct path to a directory containing all relevant files for a GPT2TokenizerFast tokenizer.
```

برای  تنظیم،  به  مستندات  وب سایت  رسمی  [مستندات  متغیرهای محیطی](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/environments)  و   [ایجاد  issue](https://github.com/langgenius/dify/issues/1261)  مرتبط  مراجعه کنید.

### 14.  چگونه می توان  تداخل پورت 80  را در نسخه  استقرار محلی  حل کرد؟

اگر  پورت 80  اشغال شده است،  سرویس  اشغال کننده پورت 80  را  متوقف کنید یا  نقشه برداری  پورت را  در `docker-compose.yaml`  تغییر دهید تا  پورت 80  به  پورت  دیگری  نقشه برداری شود.  معمولاً  Apache  و  Nginx  این پورت را  اشغال می کنند، که  می توان با  توقف  این دو  سرویس  آن  را  حل کرد.

### 15.   در صورت مواجهه با خطای "[openai] Error: ffmpeg is not installed"   در  هنگام  تبدیل  متن به  گفتار چه کاری باید  انجام داد؟

```
[openai] Error: ffmpeg is not installed
```

از آنجایی که OpenAI TTS  بخش بندی  جریان  صوتی را  پیاده سازی می کند،  ffmpeg  برای  کارکرد صحیح  استقرار  کد  منبع  باید  نصب شود.  مراحل  جزئی:

**Windows:**

1. به [وب سایت  رسمی  FFmpeg](https://ffmpeg.org/download.html)  مراجعه کنید و  کتابخانه  مشترک  Windows  پیش  کامپایل شده  را  دانلود کنید.
2.  FFmpeg  را  دانلود کنید  و  آن  را  استخراج کنید، که  یک  پوشه  مانند "ffmpeg-20200715-51db0a4-win64-static"   ایجاد می  کند.
3.  پوشه  استخراج شده  را  به  مکان دلخواه  خود،  مثلاً  C:\Program Files  ،  انتقال دهید.
4.  مسیر مطلق  دایرکتوری  bin  FFmpeg  را  به  متغیرهای محیطی  سیستم  اضافه کنید.
5.  Command Prompt را  باز کنید و  "ffmpeg -version"   را  وارد کنید.  اگر  اطلاعات  نسخه  FFmpeg   را  مشاهده کردید،  نصب  با  موفقیت  انجام شده است.

**Ubuntu:**

1.  Terminal را  باز کنید.
2.  دستورات  زیر را  برای  نصب  FFmpeg  وارد کنید: `sudo apt-get update`، سپس  `sudo apt-get install ffmpeg`.
3.  "ffmpeg -version"  را  وارد کنید تا  بررسی کنید  که  نصب  با  موفقیت  انجام شده است.

**CentOS:**

1.  ابتدا  ریپوزیتوری EPEL  را  فعال کنید. در Terminal  وارد کنید: `sudo yum install epel-release`
2.  سپس  وارد کنید: `sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm`
3.  بسته های  yum  را  بروزرسانی کنید، وارد کنید: `sudo yum update`
4.  در نهایت،  FFmpeg  را  نصب کنید، وارد کنید: `sudo yum install ffmpeg ffmpeg-devel`
5.  "ffmpeg -version"  را  وارد کنید تا  بررسی کنید  که  نصب  با  موفقیت  انجام شده است.

**Mac OS X:**

1.  Terminal را  باز کنید.
2.  اگر  Homebrew  را  نصب نکرده اید،  می توانید  آن  را  با  وارد کردن  دستور  زیر  در  Terminal  نصب کنید: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3.  از  Homebrew  برای  نصب  FFmpeg  استفاده کنید،  وارد کنید: `brew install ffmpeg`
4.  "ffmpeg -version"  را  وارد کنید تا  بررسی کنید  که  نصب  با  موفقیت  انجام شده است.

### 16.  چگونه می توان  خطای  عدم موفقیت  نصب  فایل  پیکربندی  Nginx  را  در  هنگام  استقرار  محلی  حل کرد؟

```
Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: error mounting "/run/desktop/mnt/host/d/Documents/docker/nginx/nginx.conf" to rootfs at "/etc/nginx/nginx.conf": mount /run/desktop/mnt/host/d/Documents/docker/nginx/nginx.conf:/etc/nginx/nginx.conf (via /proc/self/fd/9), flags: 0x5000: not a directory: unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
```

  پروژه  را  به طور کامل  دانلود کنید،  به دایرکتوری docker  بروید، و  `docker-compose up -d`   را  اجرا کنید.

```
git clone https://github.com/langgenius/dify.git
cd dify/docker
docker compose up -d
```

### 17.  مهاجرت پایگاه داده  وکتوری به  Qdrant  یا Milvus

اگر  می خواهید  پایگاه داده  وکتوری را  از  Weaviate  به  Qdrant  یا Milvus  مهاجرت دهید،  باید  داده ها  را  در  پایگاه داده  وکتوری  مهاجرت دهید.  مراحل  به شرح زیر است:

1.  اگر  از  کد  منبع  محلی  شروع می کنید،  متغیرهای محیطی  را  در  فایل `.env`   به  پایگاه داده  وکتوری  که  می خواهید  به  آن  مهاجرت کنید  تغییر دهید.  برای  مثال: `VECTOR_STORE=qdrant`
2.  اگر  از  docker-compose  شروع می کنید،  متغیرهای محیطی  را  در  فایل  `docker-compose.yaml`   به  پایگاه داده  وکتوری  که  می خواهید  به  آن  مهاجرت کنید  تغییر دهید،  هم  api  و  هم  worker  باید  تغییر داده شوند.  برای  مثال:

```
# نوع  پایگاه  داده  وکتوری  که  باید  استفاده شود.  ارزش های  پشتیبانی  شده  `weaviate`، `qdrant`، `milvus`  هستند.
VECTOR_STORE: weaviate
```

3.  دستور  زیر را  اجرا کنید

```
flask vdb-migrate # or docker exec -it docker-api-1 flask vdb-migrate
```

### 18.  چرا   SSRF_PROXY  لازم  است؟

در  `docker-compose.yaml`   نسخه  جامعه،  ممکن است  متوجه  شده باشید که  برخی  سرویس ها  با   متغیرهای  محیطی  `SSRF_PROXY`   و  `HTTP_PROXY`  تنظیم  شده اند،  که  همه  آن ها  به  یک  کانتینر  `ssrf_proxy`   اشاره می کنند.  این  برای  جلوگیری از  حمله های  SSRF  است.  برای  اطلاعات  بیشتر  در  مورد  حمله های  SSRF،  می توانید  [این  مقاله](https://portswigger.net/web-security/ssrf)   را  مطالعه کنید.

برای  جلوگیری از  خطرات  غیرضروری،  ما  یک  پراکسی  برای  همه  سرویس هایی  که  ممکن است  باعث  حمله های  SSRF  شوند  تنظیم  می کنیم  و  سرویس هایی  مانند  Sandbox  را  مجبور می کنیم  که  فقط  از  طریق  پراکسی  به  شبکه های  خارجی  دسترسی  داشته باشند  و  امنیت  داده ها  و  سرویس شما  را  تضمین  کنیم.  به  طور  پیش فرض،  این  پراکسی  هیچ  درخواست  محلی  را  جلوگیری  نمی کند،  اما  می توانید  با  تغییر  فایل  پیکربندی  `squid`،  رفتار  پراکسی  را  سفارشی  کنید.

####  چگونه  رفتار  پراکسی  را  سفارشی  کنیم؟

در  `docker/volumes/ssrf_proxy/squid.conf`،  می توانید  فایل  پیکربندی  `squid`   را  پیدا کنید.  می توانید  رفتار  پراکسی  را  در  اینجا  سفارشی  کنید،  مثلاً  قوانین  ACL  را  برای  محدود کردن  دسترسی  پراکسی  یا  اضافه کردن  قوانین  `http_access`  برای  محدود کردن  دسترسی  پراکسی.  برای  مثال،  شبکه  محلی  شما  می تواند  به  بخش  `192.168.101.0/24`  دسترسی  داشته باشد،  اما  `192.168.101.19`  داده های  حساس  دارد  که  نمی خواهید  کاربران  Dify   استقرار محلی  به آن  دسترسی  داشته باشند،  اما  IP های  دیگر  می توانند.  می توانید  قوانین  زیر را  در  `squid.conf`  اضافه کنید:

```
acl restricted_ip dst 192.168.101.19
acl localnet src 192.168.101.0/24

http_access deny restricted_ip
http_access allow localnet
http_access deny all
```

این  فقط  یک  مثال  ساده  است.  می توانید  رفتار  پراکسی  را  مطابق  نیازهای  خود  سفارشی  کنید.  اگر  کسب و کار  شما  پیچیده تر  است،  مثلاً  نیاز  به  پیکربندی  یک  پراکسی  بالادستی  یا  کش  دارید،  می توانید  برای  اطلاعات  بیشتر  به  [مستندات  پیکربندی  squid](http://www.squid-cache.org/Doc/config/)  مراجعه کنید.

### 19.   چگونه   برنامه   ایجاد شده  را  به  عنوان  یک  الگو  تنظیم  کنیم؟

در حال حاضر،   تنظیم  برنامه  ایجاد شده  به  عنوان  الگو  پشتیبانی  نمی شود.  الگوهای  موجود  توسط   Dify  رسمی  برای  کاربران  نسخه  ابری   ارائه شده  است تا  به  آن ها  مراجعه کنند.  اگر  از  نسخه  ابری  استفاده می کنید،  می توانید  برنامه ها  را  به  فضای  کار  خود  اضافه کنید  یا  پس  از  تغییر،  آن ها  را  سفارشی  کنید تا  الگوهای  برنامه  خودتان  را  ایجاد کنید.  اگر  از  نسخه  جامعه  استفاده می کنید و  نیاز  به  ایجاد  الگوهای  برنامه  بیشتر  برای  تیم  خود  دارید،  می توانید  برای  پشتیبانی  فنی  پرداختنی  با  تیم  کسب و کار  ما  تماس بگیرید: [business@dify.ai](mailto:business@dify.ai)

### 20.  502 Bad Gateway

این  به  این  دلیل  است  که  Nginx  سرویس  را  به  مکان  اشتباه  هدایت می کند.  ابتدا  اطمینان  حاصل کنید  که  کانتینر  در  حال  اجرا  است،  سپس  دستور  زیر را  با  امتیازات  root   اجرا کنید:

```
docker ps -q | xargs -n 1 docker inspect --format '{{ .Name }}: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

این  دو  خط  را  در  خروجی  پیدا کنید:

```
/docker-web-1: 172.19.0.5
/docker-api-1: 172.19.0.7
```

آدرس های  IP  را  به  یاد داشته باشید.  سپس  دایرکتوری  را  که  کد  منبع  Dify  را  در  آن ذخیره کرده اید،  باز کنید،  `dify/docker/nginx/conf.d`   را  باز کنید،  `http://api:5001`   را  با  `http://172.19.0.7:5001`  و  `http://web:3000`   را  با  `http://172.19.0.5:3000`  جایگزین کنید،  سپس  کانتینر  Nginx  را  راه اندازی  مجدد  کنید  یا  پیکربندی  را  بارگذاری مجدد کنید.

این  آدرس های  IP  _**مثال**_  هستند،   شما  باید  دستور  را  اجرا کنید تا  آدرس های  IP   خودتان  را  به دست آورید،  آن ها  را  مستقیماً  وارد  نکنید.  ممکن است  نیاز  به  پیکربندی  مجدد  آدرس های  IP   هنگام  راه اندازی مجدد  کانتینرهای  مربوطه  داشته باشید.
