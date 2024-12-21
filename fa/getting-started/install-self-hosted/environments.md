# محيط‌ها

### متغيرهاي رايج

#### CONSOLE_API_URL

آدرس URL سرور پشتيبان API کنسول. اين آدرس براي ساختن فراخواني مجدد تاييد هويت استفاده می‌شود. در صورت خالي گذاشتن، به طور پیش‌فرض به دامنه اي همانند برنامه تطبيق داده می‌شود. مثال: `https://api.console.dify.ai`

#### CONSOLE_WEB_URL

آدرس URL رابط وب کنسول در سمت کلاینت. اين آدرس براي ساختن آدرس‌های سمت کلاینت و پیکربندی CORS استفاده می‌شود. در صورت خالي گذاشتن، به طور پیش‌فرض به دامنه اي همانند برنامه تطبيق داده می‌شود. مثال: `https://console.dify.ai`

#### SERVICE_API_URL

آدرس URL API سرويس، که براي نمايش آدرس پايه API سرويس در سمت کلاینت استفاده می‌شود. در صورت خالي گذاشتن، به طور پیش‌فرض به دامنه اي همانند برنامه تطبيق داده می‌شود. مثال: `https://api.dify.ai`

#### APP_API_URL

آدرس URL سرور پشتيبان API برنامه وب، که براي مشخص کردن آدرس URL سرور پشتيبان API برنامه وب در سمت کلاینت استفاده می‌شود. در صورت خالي گذاشتن، به طور پیش‌فرض به دامنه اي همانند برنامه تطبيق داده می‌شود. مثال: `https://app.dify.ai`

#### APP_WEB_URL

آدرس URL برنامه وب، که براي نمايش پيش‌نمايش يا دانلود فايل در سمت کلاینت يا به عنوان ورودي مدل‌هاي چندرسانه‌اي استفاده می‌شود؛ در صورت خالي گذاشتن، به طور پیش‌فرض به دامنه اي همانند برنامه تطبيق داده می‌شود. مثال: `https://udify.app/`

#### FILES_URL

پيشوند آدرس URL پيش‌نمايش يا دانلود فايل، که براي نمايش اين آدرس‌ها در سمت کلاینت و ارائه آن‌ها به عنوان ورودي براي مدل‌هاي چندرسانه‌اي استفاده می‌شود. به منظور جلوگيري از جعل، آدرس URL پيش‌نمايش تصوير امضا می‌شود و پس از 5 دقيقه منقضي خواهد شد.

***

### سرور

#### MODE

حالت راه اندازي: اين فقط زماني در دسترس است که با استفاده از docker راه اندازي شده باشد. در صورت اجرا از کد منبع، قابل اعمال نيست.

- api

  شروع سرور API.

- worker

  شروع کارگر صف ناهمزمان.

#### DEBUG

حالت اشکال زدایی: به طور پیش‌فرض غیرفعال است. توصیه می‌شود این تنظیم را در حین توسعه محلی فعال کنید تا از مشکلات ناشی از وصله میمون جلوگیری شود.

#### FLASK_DEBUG

حالت اشکال زدایی Flask: هنگام فعال شدن، اطلاعات ردیابی را در پاسخ‌های API خروجی می‌دهد و اشکال زدایی را آسان‌تر می‌کند.

#### SECRET_KEY

یک کلید مخفی که برای امضای ایمن کوکی‌های جلسه و رمزگذاری اطلاعات حساس در پایگاه داده استفاده می‌شود.

این متغیر باید قبل از اولین راه اندازی تنظیم شود.

برای تولید یک کلید قوی برای آن، `openssl rand -base64 42` را اجرا کنید.

#### DEPLOY_ENV

محیط استقرار:

- PRODUCTION (پیش‌فرض)

  محیط تولید.

- TESTING

  محیط آزمایش. یک برچسب رنگی متمایز در صفحه سمت کلاینت وجود خواهد داشت که نشان می‌دهد این محیط یک محیط آزمایشی است.

#### LOG_LEVEL

سطح خروجی لاگ. پیش‌فرض INFO است. برای محیط‌های تولید، توصیه می‌شود این را به ERROR تنظیم کنید.

#### MIGRATION_ENABLED

هنگامی که به true تنظیم شود، مهاجرت‌های پایگاه داده به طور خودکار هنگام راه اندازی ظرف اجرا می‌شوند. این فقط زماني در دسترس است که با استفاده از docker راه اندازي شده باشد و در صورت اجرا از کد منبع، قابل اعمال نيست.

برای راه اندازی کد منبع، باید `flask db upgrade` را به صورت دستی در دایرکتوری api اجرا کنید.

#### CHECK_UPDATE_URL

سیاست بررسی نسخه را کنترل می‌کند. اگر به false تنظیم شود، سیستم برای بررسی وجود به روز رسانی ها به `https://updates.dify.ai` تماس نخواهد گرفت.

در حال حاضر، رابط بررسی نسخه مبتنی بر CloudFlare Worker به طور مستقیم در چین قابل دسترسی نیست. تنظیم این متغیر به یک مقدار خالی این فراخوانی API را غیرفعال می‌کند.

#### TEXT\_GENERATION\_TIMEOUT\_MS

مقدار پیش‌فرض: 60000 (میلی ثانیه). مدت زمان خاتمه برای تولید متن و فرایندهای گردش کار را مشخص می‌کند. این تنظیم از اختلالات سرویس در سطح سیستم که به دلیل فرایندهای فردی که زمان اختصاص داده شده به آن‌ها را تجاوز می‌کنند جلوگیری می‌کند.

#### OPENAI_API_BASE

برای تغییر آدرس پایه OpenAI استفاده می‌شود، پیش‌فرض [https://api.openai.com/v1](https://api.openai.com/v1) است.

هنگامی که OpenAI در چین قابل دسترسی نیست، آن را با یک آدرس آینه داخلی جایگزین کنید، یا زمانی که یک مدل محلی API سازگار با OpenAI ارائه می‌دهد، می‌توان آن را جایگزین کرد.

#### پیکربندی مرتبط با راه اندازی ظرف

فقط هنگام شروع با تصویر docker یا docker-compose مؤثر است.

- DIFY_BIND_ADDRESS

  آدرس اتصال سرویس API، پیش‌فرض: 0.0.0.0، یعنی همه آدرس‌ها قابل دسترسی هستند.

- DIFY_PORT

  شماره پورت اتصال سرویس API، پیش‌فرض به 5001.

- SERVER_WORKER_AMOUNT

  تعداد کارگران سرور API، یعنی تعداد کارگران gevent. فرمول: `تعداد هسته‌های CPU x 2 + 1`

  مراجعه: [https://docs.gunicorn.org/en/stable/design.html#how-many-workers](https://docs.gunicorn.org/en/stable/design.html#how-many-workers)

- SERVER_WORKER_CLASS

  پیش‌فرض gevent است. اگر از ویندوز استفاده می‌کنید، می‌توان آن را به sync یا solo تغییر داد.

- GUNICORN_TIMEOUT

  مدت زمان خاتمه رسیدگی به درخواست. پیش‌فرض 200 است. مقدار توصیه شده 360 برای پشتیبانی از زمان‌های طولانی‌تر اتصال SSE (وقایع ارسال شده توسط سرور) است.

- CELERY_WORKER_CLASS

  مشابه `SERVER_WORKER_CLASS`. پیش‌فرض gevent است. اگر از ویندوز استفاده می‌کنید، می‌توان آن را به sync یا solo تغییر داد.

- CELERY_WORKER_AMOUNT

  تعداد کارگران Celery. پیش‌فرض 1 است و می‌تواند به طور دلخواه تنظیم شود.

#### پیکربندی پایگاه داده

پایگاه داده از PostgreSQL استفاده می‌کند. لطفاً از طرح عمومی استفاده کنید.

- DB_USERNAME: نام کاربری
- DB_PASSWORD: رمز عبور
- DB_HOST: هاست پایگاه داده
- DB_PORT: شماره پورت پایگاه داده، پیش‌فرض 5432 است
- DB_DATABASE: نام پایگاه داده
- SQLALCHEMY_POOL_SIZE: اندازه استخر اتصال به پایگاه داده. پیش‌فرض 30 اتصال است که می‌تواند به طور مناسب افزایش یابد.
- SQLALCHEMY_POOL_RECYCLE: زمان بازیافت استخر اتصال به پایگاه داده، پیش‌فرض 3600 ثانیه است.
- SQLALCHEMY_ECHO: آیا SQL را چاپ کند، پیش‌فرض false است.

#### پیکربندی Redis

این پیکربندی Redis برای ذخیره سازی در حافظه نهان و انتشار/اشتراک در طول مکالمه استفاده می‌شود.

- REDIS_HOST: هاست Redis
- REDIS_PORT: پورت Redis، پیش‌فرض 6379 است
- REDIS_DB: پایگاه داده Redis، پیش‌فرض 0 است. لطفاً از یک پایگاه داده متفاوت از Redis جلسه و Celery Broker استفاده کنید.
- REDIS_USERNAME: نام کاربری Redis، پیش‌فرض خالی است
- REDIS_PASSWORD: رمز عبور Redis، پیش‌فرض خالی است. توصیه می‌شود یک رمز عبور تنظیم کنید.
- REDIS_USE_SSL: آیا از پروتکل SSL برای اتصال استفاده شود، پیش‌فرض false است
- REDIS_USE_SENTINEL: از Redis Sentinel برای اتصال به سرورهای Redis استفاده کنید
- REDIS_SENTINELS: گره‌های Sentinel، فرمت: `<آدرس IP Sentinel1>:<پورت Sentinel1>,<آدرس IP Sentinel2>:<پورت Sentinel2>,<آدرس IP Sentinel3>:<پورت Sentinel3>`
- REDIS_SENTINEL_SERVICE_NAME: نام سرویس Sentinel، همان نام Master
- REDIS_SENTINEL_USERNAME: نام کاربری Sentinel
- REDIS_SENTINEL_PASSWORD: رمز عبور Sentinel
- REDIS_SENTINEL_SOCKET_TIMEOUT: زمان خاتمه Sentinel، مقدار پیش‌فرض: 0.1، واحد: ثانیه


#### پیکربندی Celery

- CELERY_BROKER_URL

  فرمت به صورت زیر (حالت اتصال مستقیم):

  ```
  redis://<نام کاربری Redis>:<رمز عبور Redis>@<هاست Redis>:<پورت Redis>/<پایگاه داده Redis>
  ```

  مثال: `redis://:difyai123456@redis:6379/1`

  حالت Sentinel:

  ```
  sentinel://<نام کاربری Sentinel>:<رمز عبور Sentinel>@<هاست Sentinel>:<پورت Sentinel>/<پایگاه داده Redis>
  ```

  مثال: `sentinel://localhost:26379/1;sentinel://localhost:26380/1;sentinel://localhost:26381/1`

- BROKER_USE_SSL

  اگر به true تنظیم شود، از پروتکل SSL برای اتصال استفاده می‌شود، پیش‌فرض false است

- CELERY_USE_SENTINEL

  اگر به true تنظیم شود، حالت Sentinel فعال می‌شود، پیش‌فرض false است

- CELERY_SENTINEL_MASTER_NAME

  نام سرویس Sentinel، یعنی نام Master

- CELERY_SENTINEL_SOCKET_TIMEOUT

  زمان خاتمه اتصال به Sentinel، مقدار پیش‌فرض: 0.1، واحد: ثانیه

#### پیکربندی CORS

برای تنظیم سیاست دسترسی متقابل دامنه سمت کلاینت استفاده می‌شود.

- CONSOLE_CORS_ALLOW_ORIGINS

  سیاست متقابل دامنه CORS کنسول، پیش‌فرض `*` است، یعنی همه دامنه‌ها می‌توانند دسترسی داشته باشند.

- WEB_API_CORS_ALLOW_ORIGINS

  سیاست متقابل دامنه CORS برنامه وب، پیش‌فرض `*` است، یعنی همه دامنه‌ها می‌توانند دسترسی داشته باشند.

#### پیکربندی ذخیره سازی فایل

برای ذخیره سازی فایل‌های مجموعه داده آپلود شده، کلیدهای رمزگذاری تیم/مستاجر و سایر فایل‌ها استفاده می‌شود.

- STORAGE_TYPE

  نوع امکان ذخیره سازی

  - local (پیش‌فرض)

    ذخیره سازی فایل محلی، اگر این گزینه انتخاب شود، پیکربندی `STORAGE_LOCAL_PATH` زیر باید تنظیم شود.

  - s3

    ذخیره سازی شی S3، اگر این گزینه انتخاب شود، پیکربندی‌های S3\_ پیشوند زیر باید تنظیم شوند.

  - azure-blob

    ذخیره سازی شی Azure Blob، اگر این گزینه انتخاب شود، پیکربندی‌های AZURE_BLOB\_ پیشوند زیر باید تنظیم شوند.

  - huawei-obs

    ذخیره سازی شی Huawei OBS، اگر این گزینه انتخاب شود، پیکربندی‌های HUAWEI_OBS\_ پیشوند زیر باید تنظیم شوند.

  - volcengine-tos

    ذخیره سازی شی Volcengine TOS، اگر این گزینه انتخاب شود، پیکربندی‌های VOLCENGINE_TOS\_ پیشوند زیر باید تنظیم شوند.

- STORAGE_LOCAL_PATH

  پیش‌فرض storage است، یعنی در دایرکتوری storage دایرکتوری فعلی ذخیره می‌شود.

  اگر شما با docker یا docker-compose استقرار می‌دهید، مطمئن شوید که دایرکتوری `/app/api/storage` را در هر دو ظرف به یک دایرکتوری محلی یکسان نصب کنید، در غیر این صورت، ممکن است با خطاهای عدم وجود فایل مواجه شوید.

- S3_ENDPOINT: آدرس نقطه پایانی S3
- S3_BUCKET_NAME: نام سطل S3
- S3_ACCESS_KEY: کلید دسترسی S3
- S3_SECRET_KEY: کلید مخفی S3
- S3_REGION: اطلاعات منطقه S3، مانند: us-east-1
- AZURE_BLOB_ACCOUNT_NAME: نام حساب شما، مانند 'difyai'
- AZURE_BLOB_ACCOUNT_KEY: کلید حساب شما، مانند 'difyai'
- AZURE_BLOB_CONTAINER_NAME: نام ظرف شما، مانند 'difyai-container'
- AZURE_BLOB_ACCOUNT_URL: 'https://\<نام حساب شما>.blob.core.windows.net'
- ALIYUN_OSS_BUCKET_NAME: نام سطل شما، مانند 'difyai'
- ALIYUN_OSS_ACCESS_KEY: کلید دسترسی شما، مانند 'difyai'
- ALIYUN_OSS_SECRET_KEY: کلید مخفی شما، مانند 'difyai'
- ALIYUN_OSS_ENDPOINT: https://oss-ap-southeast-1-internal.aliyuncs.com # مرجع: https://www.alibabacloud.com/help/en/oss/user-guide/regions-and-endpoints
- ALIYUN_OSS_REGION: ap-southeast-1 # مرجع: https://www.alibabacloud.com/help/en/oss/user-guide/regions-and-endpoints
- ALIYUN_OSS_AUTH_VERSION: v4
- ALIYUN_OSS_PATH: مسیر شما # با '/' شروع نکنید. OSS از اسلش در ابتدای نام شی پشتیبانی نمی‌کند. مرجع: https://www.alibabacloud.com/help/en/oss/support/0016-00000005
- HUAWEI_OBS_BUCKET_NAME: نام سطل شما، مانند 'difyai'
- HUAWEI_OBS_SECRET_KEY: کلید مخفی شما، مانند 'difyai'
- HUAWEI_OBS_ACCESS_KEY: کلید دسترسی شما، مانند 'difyai'
- HUAWEI_OBS_SERVER: آدرس URL سرور شما # مرجع: https://support.huaweicloud.com/sdk-python-devg-obs/obs_22_0500.html
- VOLCENGINE_TOS_BUCKET_NAME: نام سطل شما، مانند 'difyai'
- VOLCENGINE_TOS_SECRET_KEY: کلید مخفی شما، مانند 'difyai'
- VOLCENGINE_TOS_ACCESS_KEY: کلید دسترسی شما، مانند 'difyai'
- VOLCENGINE_TOS_REGION: منطقه شما، مانند 'cn-guangzhou' # مرجع: https://www.volcengine.com/docs/6349/107356
- VOLCENGINE_TOS_ENDPOINT: نقطه پایانی شما، مانند 'tos-cn-guangzhou.volces.com' # مرجع: https://www.volcengine.com/docs/6349/107356

#### پیکربندی پایگاه داده برداری

- VECTOR_STORE
  - **انواع شمارش قابل دسترس عبارتند از:**
    - `weaviate`
    - `qdrant`
    - `milvus`
    - `zilliz` (همان پیکربندی `milvus` را به اشتراک می‌گذارد)
    - `myscale`
    - `pinecone` (هنوز باز نشده است)
    - `analyticdb`
- WEAVIATE_ENDPOINT

  آدرس نقطه پایانی Weaviate، مانند: `http://weaviate:8080`.

- WEAVIATE_API_KEY

  احراز هویت api-key که برای اتصال به Weaviate استفاده می‌شود.

- WEAVIATE_BATCH_SIZE

  تعداد اشیاء شاخص که در دسته‌ها در Weaviate ایجاد می‌شوند، پیش‌فرض 100 است.

  به این سند مراجعه کنید: [https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters](https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters)

- WEAVIATE_GRPC_ENABLED

  آیا از روش gRPC برای تعامل با Weaviate استفاده شود، عملکرد هنگام فعال شدن به طور قابل توجهی افزایش می‌یابد، ممکن است در محلي قابل استفاده نباشد، پیش‌فرض true است.

- QDRANT_URL

  آدرس نقطه پایانی Qdrant، مانند: `https://your-qdrant-cluster-url.qdrant.tech/`

- QDRANT_API_KEY

  احراز هویت api-key که برای اتصال به Qdrant استفاده می‌شود.

- PINECONE_API_KEY

  احراز هویت api-key که برای اتصال به Pinecone استفاده می‌شود.

- PINECONE_ENVIRONMENT

  محیطی که Pinecone در آن قرار دارد، مانند: `us-east4-gcp`

- MILVUS_URI

  پیکربندی uri Milvus. مثلاً http://localhost:19530. برای Zilliz Cloud، uri و token را به [نقطه پایانی عمومی و کلید Api](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) تنظیم کنید.

- MILVUS_TOKEN

  پیکربندی token Milvus، پیش‌فرض خالی است.

- MILVUS_USER

  پیکربندی کاربری Milvus، پیش‌فرض خالی است.

- MILVUS_PASSWORD

  پیکربندی رمز عبور Milvus، پیش‌فرض خالی است.

- MYSCALE_HOST

  پیکربندی هاست MyScale.

- MYSCALE_PORT

  پیکربندی پورت MyScale.

- MYSCALE_USER

  پیکربندی کاربری MyScale، پیش‌فرض `default` است.

- MYSCALE_PASSWORD

  پیکربندی رمز عبور MyScale، پیش‌فرض خالی است.

- MYSCALE_DATABASE

  پیکربندی پایگاه داده MyScale، پیش‌فرض `default` است.

- MYSCALE_FTS_PARAMS

  پارامترهای جستجوی متنی MyScale، برای پشتیبانی از چند زبان، [مستندات MyScale](https://myscale.com/docs/en/text-search/#understanding-fts-index-parameters) را بررسی کنید، پیش‌فرض خالی است.
  
- ANALYTICDB_KEY_ID

  شناسه کلید دسترسی که برای احراز هویت OpenAPI علی بابا استفاده می‌شود. برای ایجاد AccessKey خود، [مستندات Analyticdb](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/support/create-an-accesskey-pair) را مطالعه کنید.

- ANALYTICDB_KEY_SECRET

  راز کلید دسترسی که برای احراز هویت OpenAPI علی بابا استفاده می‌شود.

- ANALYTICDB_INSTANCE_ID

  شناسه منحصر به فرد نمونه AnalyticDB شما، مانند: `gp-xxxxxx`. برای ایجاد نمونه خود، [مستندات Analyticdb](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/getting-started/create-an-instance-1) را مطالعه کنید.

- ANALYTICDB_REGION_ID

  شناسه منطقه‌ای که نمونه AnalyticDB در آن قرار دارد، مانند: `cn-hangzhou`.

- ANALYTICDB_ACCOUNT

  نام حساب استفاده شده برای اتصال به نمونه AnalyticDB. برای ایجاد یک حساب، [مستندات Analyticdb](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/getting-started/createa-a-privileged-account) را مطالعه کنید.

- ANALYTICDB_PASSWORD

  رمز عبور حساب استفاده شده برای اتصال به نمونه AnalyticDB.

- ANALYTICDB_NAMESPACE

  فضای نام (طرح) در داخل نمونه AnalyticDB که می‌خواهید با آن تعامل داشته باشید، مانند `dify`. اگر این فضای نام وجود ندارد، به طور خودکار ایجاد می‌شود.

- ANALYTICDB_NAMESPACE_PASSWORD

  رمز عبور فضای نام (طرح). اگر فضای نام وجود ندارد، با این رمز عبور ایجاد می‌شود.

#### پیکربندی دانش

- UPLOAD_FILE_SIZE_LIMIT:

  حداکثر اندازه فایل آپلود، پیش‌فرض 15 مگابایت.

- UPLOAD_FILE_BATCH_LIMIT

  حداکثر تعداد فایل‌هایی که می‌توانند به طور همزمان آپلود شوند، پیش‌فرض 5.

- ETL_TYPE

  **انواع شمارش قابل دسترس:**

  - dify

    طرح استخراج فایل اختصاصی Dify

  - Unstructured

    طرح استخراج فایل Unstructured.io

- UNSTRUCTURED_API_URL

  مسیر API Unstructured، باید هنگام ETL_TYPE Unstructured تنظیم شود.

  مثلاً: `http://unstructured:8000/general/v0/general`

#### پیکربندی چندرسانه‌اي

- MULTIMODAL_SEND_IMAGE_FORMAT

  فرمت تصویری که هنگام ورودی مدل چندرسانه‌اي ارسال می‌شود، پیش‌فرض `base64` است، گزینه `url` نیز وجود دارد. تأخیر تماس در حالت `url` کمتر از حالت `base64` خواهد بود. به طور کلی توصیه می‌شود از حالت `base64` سازگارتر استفاده کنید. اگر به عنوان `url` پیکربندی شده باشد، باید `FILES_URL` را به عنوان یک آدرس قابل دسترسی از خارج تنظیم کنید تا مدل چندرسانه‌اي بتواند به تصویر دسترسی داشته باشد.

- UPLOAD_IMAGE_FILE_SIZE_LIMIT

  حداکثر اندازه فایل تصویر آپلود، پیش‌فرض 10 مگابایت.

#### پیکربندی Sentry

برای نظارت بر برنامه و ردیابی لاگ خطا استفاده می‌شود.

- SENTRY_DSN

  آدرس DSN Sentry، پیش‌فرض خالی است، هنگام خالی بودن، تمام اطلاعات نظارت به Sentry گزارش نمی‌شود.

- SENTRY_TRACES_SAMPLE_RATE

  نسبت گزارش رویدادهای Sentry، اگر 0.01 باشد، 1٪ است.

- SENTRY_PROFILES_SAMPLE_RATE

  نسبت گزارش نمایه‌های Sentry، اگر 0.01 باشد، 1٪ است.

#### پیکربندی ادغام Notion

متغیرهای پیکربندی ادغام Notion را می‌توان با درخواست ادغام Notion به دست آورد: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

- NOTION_INTEGRATION_TYPE: به عنوان "public" یا "internal" پیکربندی کنید. از آنجایی که URL هدایت مجدد OAuth Notion فقط از HTTPS پشتیبانی می‌کند، اگر به صورت محلی استقرار می‌دهید، لطفاً از ادغام داخلی Notion استفاده کنید.
- NOTION_CLIENT_SECRET: راز مشتری OAuth Notion (برای نوع ادغام عمومی استفاده می‌شود)
- NOTION_CLIENT_ID: شناسه مشتری OAuth (برای نوع ادغام عمومی استفاده می‌شود)
- NOTION_INTERNAL_SECRET: راز ادغام داخلی Notion. اگر مقدار `NOTION_INTEGRATION_TYPE` "internal" باشد، باید این متغیر را پیکربندی کنید.

#### پیکربندی مرتبط با ایمیل

- MAIL_TYPE
  - resend
    - MAIL_DEFAULT_SEND_FROM\
      نام ایمیل فرستنده، مانند: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai)، اجباری نیست.
    - RESEND_API_KEY\
      API-Key برای ارائه دهنده ایمیل Resend، را می‌توان از API-Key به دست آورد.
  - smtp
    - SMTP_SERVER\
      آدرس سرور SMTP
    - SMTP_PORT\
      شماره پورت سرور SMTP
    - SMTP_USERNAME\
      نام کاربری SMTP
    - SMTP_PASSWORD\
      رمز عبور SMTP
    - SMTP_USE_TLS\
      آیا از TLS استفاده شود، پیش‌فرض false است
    - MAIL_DEFAULT_SEND_FROM\
      نام ایمیل فرستنده، مانند: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai)، اجباری نیست.

#### پیکربندی موقعیت ارائه دهنده مدل و ابزار

برای مشخص کردن ارائه دهندگان مدل و ابزارهایی که می‌توانند در برنامه استفاده شوند، استفاده می‌شود. این تنظیمات به شما امکان می‌دهد که ارائه دهندگان مدل و ابزارهایی را که در دسترس هستند سفارشی کنید، و همچنین ترتیب و گنجاندن/استثنا آن‌ها را در رابط برنامه تنظیم کنید.

برای مشاهده لیست [ابزارها](https://github.com/langgenius/dify/blob/main/api/core/tools/provider/_position.yaml) و [ارائه دهندگان مدل](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/model_providers/_position.yaml) موجود، لطفاً به پیوندهای ارائه شده مراجعه کنید.

- POSITION_TOOL_PINS

  ابزارهای خاصی را در بالای لیست پین کنید، و مطمئن شوید که در رابط برنامه اول ظاهر می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_TOOL_PINS=bing,google`

- POSITION_TOOL_INCLUDES

  ابزارهایی را که باید در برنامه گنجانده شوند مشخص کنید. فقط ابزارهایی که در اینجا لیست شده‌اند برای استفاده در دسترس خواهند بود. اگر تنظیم نشده باشد، تمام ابزارها به جز موارد ذکر شده در POSITION_TOOL_EXCLUDES گنجانده می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_TOOL_INCLUDES=bing,google`

- POSITION_TOOL_EXCLUDES

  ابزارهای خاصی را از نمایش یا استفاده در برنامه مستثنی کنید. ابزارهایی که در اینجا لیست شده‌اند، به جز ابزارهای پین شده، از گزینه‌های موجود حذف می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_TOOL_EXCLUDES=yahoo,wolframalpha`

- POSITION_PROVIDER_PINS

  ارائه دهندگان مدل خاصی را در بالای لیست پین کنید، و مطمئن شوید که در رابط برنامه اول ظاهر می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_PROVIDER_PINS=openai,openllm`

- POSITION_PROVIDER_INCLUDES

  ارائه دهندگان مدل را که باید در برنامه گنجانده شوند مشخص کنید. فقط ارائه دهندگانی که در اینجا لیست شده‌اند برای استفاده در دسترس خواهند بود. اگر تنظیم نشده باشد، تمام ارائه دهندگان به جز موارد ذکر شده در POSITION_PROVIDER_EXCLUDES گنجانده می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_PROVIDER_INCLUDES=cohere,upstage`

- POSITION_PROVIDER_EXCLUDES

  ارائه دهندگان مدل خاصی را از نمایش یا استفاده در برنامه مستثنی کنید. ارائه دهندگانی که در اینجا لیست شده‌اند، به جز ارائه دهندگان پین شده، از گزینه‌های موجود حذف می‌شوند. (از مقادیر جدا شده با کاما با **بدون فاصله** بین آیتم‌ها استفاده کنید.)

  مثال: `POSITION_PROVIDER_EXCLUDES=openrouter,ollama`

#### سایر

- INVITE_EXPIRY_HOURS: مدت زمان معتبر لینک دعوت عضویت (ساعت)، پیش‌فرض: 72.
- HTTP\_REQUEST_NODE_MAX_TEXT_SIZE：حداکثر اندازه متن گره درخواست HTTP در گردش کار، پیش‌فرض 1 مگابایت.
- HTTP\_REQUEST_NODE_MAX_BINARY_SIZE：حداکثر اندازه باینری گره‌های درخواست HTTP در گردش کار، پیش‌فرض 10 مگابایت.

---

### رابط وب سمت کلاینت

#### SENTRY_DSN

آدرس DSN Sentry، پیش‌فرض خالی است، هنگام خالی بودن، تمام اطلاعات نظارت به Sentry گزارش نمی‌شود.

## منسوخ شده

#### CONSOLE_URL

> ⚠️ در 0.3.8 اصلاح شد، در 0.4.9 منسوخ خواهد شد، با: `CONSOLE_API_URL` و `CONSOLE_WEB_URL` جایگزین می‌شود.

آدرس URL کنسول، که برای الحاق فراخواني مجدد تاييد هويت، آدرس سمت کلاینت کنسول و استفاده از پیکربندی CORS استفاده می‌شود. اگر خالی باشد، همان دامنه است. مثال: `https://console.dify.ai`.

#### API_URL

> ⚠️ در 0.3.8 اصلاح شد، در 0.4.9 منسوخ خواهد شد، با `SERVICE_API_URL` جایگزین می‌شود.

آدرس URL API، که برای نمایش آدرس پايه API سرویس به سمت کلاینت استفاده می‌شود. اگر خالی باشد، همان دامنه است. مثال: `https://api.dify.ai`

#### APP_URL

> ⚠️ در 0.3.8 اصلاح شد، در 0.4.9 منسوخ خواهد شد، با `APP_API_URL` و `APP_WEB_URL` جایگزین می‌شود.

آدرس URL برنامه وب، که برای نمایش آدرس پايه API برنامه وب به سمت کلاینت استفاده می‌شود. اگر خالی باشد، همان دامنه است. مثال: `https://udify.app/`

#### پیکربندی جلسه

> ⚠️ این پیکربندی از نسخه 0.3.24 به بعد دیگر معتبر نیست.

فقط توسط سرویس API برای تأیید هویت رابط استفاده می‌شود.

- SESSION_TYPE：

  نوع مؤلفه جلسه

  - redis (پیش‌فرض)

    اگر این را انتخاب کنید، باید متغیرهای محیطی زیر را که با SESSION_REDIS\_ شروع می‌شوند تنظیم کنید.

  - sqlalchemy

    اگر این را انتخاب کنید، اتصال فعلی پایگاه داده استفاده می‌شود و از جدول sessions برای خواندن و نوشتن سوابق جلسه استفاده می‌شود.

- SESSION_REDIS_HOST: هاست Redis
- SESSION_REDIS_PORT: پورت Redis، پیش‌فرض 6379 است
- SESSION_REDIS_DB: پایگاه داده Redis، پیش‌فرض 0 است. لطفاً از یک پایگاه داده متفاوت از Redis و Celery Broker استفاده کنید.
- SESSION_REDIS_USERNAME: نام کاربری Redis، پیش‌فرض خالی است
- SESSION_REDIS_PASSWORD: رمز عبور Redis، پیش‌فرض خالی است. توصیه می‌شود یک رمز عبور تنظیم کنید.
- SESSION_REDIS_USE_SSL: آیا از پروتکل SSL برای اتصال استفاده شود، پیش‌فرض false است

#### پیکربندی سیاست کوکی

> ⚠️ این پیکربندی از نسخه 0.3.24 به بعد دیگر معتبر نیست.

برای تنظیم سیاست مرورگر برای کوکی‌های جلسه که برای تأیید هویت استفاده می‌شوند، استفاده می‌شود.

- COOKIE_HTTPONLY

  پیکربندی HttpOnly کوکی، پیش‌فرض true است.

- COOKIE_SAMESITE

  پیکربندی SameSite کوکی، پیش‌فرض Lax است.

- COOKIE_SECURE

  پیکربندی Secure کوکی، پیش‌فرض false است.


