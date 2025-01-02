# شروع کد منبع محلی

## پیش نیازها

> قبل از نصب Dify، مطمئن شوید که دستگاه شما حداقل شرایط سیستم زیر را برآورده می کند:
> - CPU >= 2 هسته
> - RAM >= 4 GiB

| سیستم عامل           | نرم افزار                                                       | توضیحات                                                                                                                                                                                                                                                                                                                               |
| -------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| macOS 10.14 یا بالاتر       | Docker Desktop                                                 | ماشین مجازی Docker (VM) را طوری تنظیم کنید که حداقل از 2 پردازنده مجازی (vCPU) و 8 گیگابایت حافظه اولیه استفاده کند. در غیر این صورت، نصب ممکن است با شکست مواجه شود. برای اطلاعات بیشتر، لطفاً به [راهنمای نصب Docker Desktop برای Mac](https://docs.docker.com/desktop/mac/install/) مراجعه کنید.                                                     |
| پلتفرم های لینوکس            | <p>Docker 19.03 یا بالاتر<br>Docker Compose 1.25.1 یا بالاتر</p> | لطفاً برای اطلاعات بیشتر در مورد نحوه نصب Docker و Docker Compose، به ترتیب، به [راهنمای نصب Docker](https://docs.docker.com/engine/install/) و [راهنمای نصب Docker Compose](https://docs.docker.com/compose/install/) مراجعه کنید.                                                                            |
| ویندوز با WSL 2 فعال | <p>Docker Desktop<br></p>                                      | ما توصیه می کنیم کد منبع و سایر داده هایی که به کانتینرهای لینوکس متصل هستند را در سیستم فایل لینوکس به جای سیستم فایل ویندوز ذخیره کنید. برای اطلاعات بیشتر، لطفاً به [راهنمای نصب Docker Desktop برای استفاده از بک اند WSL 2 در ویندوز](https://docs.docker.com/desktop/windows/install/#wsl-2-backend) مراجعه کنید. |

> اگر نیاز به استفاده از OpenAI TTS دارید، `FFmpeg` باید برای عملکرد صحیح آن در سیستم نصب شود. برای جزئیات بیشتر، به: [لینک](https://docs.dify.ai/getting-started/install-self-hosted/install-faq#id-14.-what-to-do-if-this-error-occurs-in-text-to-speech) مراجعه کنید.

### کپی Dify

```Bash
git clone https://github.com/langgenius/dify.git
```

قبل از فعال کردن سرویس های تجاری، ابتدا باید PostgresSQL / Redis / Weaviate (اگر در دسترس نیست) را مستقر کنیم. ما می توانیم آنها را با دستورات زیر شروع کنیم:

```Bash
cd docker
cp middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml up -d
```

---

### استقرار سرور

- سرویس رابط API
- سرویس مصرف صف غیر همزمان Worker

#### نصب محیط پایه:

شروع سرور به Python 3.10.x نیاز دارد. توصیه می شود از [pyenv](https://github.com/pyenv/pyenv) برای نصب سریع محیط Python استفاده کنید.

برای نصب نسخه های اضافی Python، از pyenv install استفاده کنید.

```Bash
pyenv install 3.10
```

برای تغییر به محیط Python "3.10"، از دستور زیر استفاده کنید:

```Bash
pyenv global 3.10
```

#### این مراحل را دنبال کنید:

1.  به دایرکتوری "api" بروید:

    ```
    cd api
    ```

2.  فایل پیکربندی متغیر محیط را کپی کنید:

    ```
    cp .env.example .env
    ```

3.  یک کلید مخفی تصادفی ایجاد کنید و مقدار SECRET_KEY را در فایل .env جایگزین کنید:

    ```
    awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env
    ```

4.  وابستگی های مورد نیاز را نصب کنید:

    سرویس API Dify از [Poetry](https://python-poetry.org/docs/) برای مدیریت وابستگی ها استفاده می کند. می توانید `poetry shell` را برای فعال کردن محیط اجرا کنید.

    ```
    poetry env use 3.10
    poetry install
    ```

5.  مهاجرت پایگاه داده را انجام دهید:

    مهاجرت پایگاه داده را به آخرین نسخه انجام دهید:

    ```
    poetry shell
    flask db upgrade
    ```

6.  سرور API را شروع کنید:

    ```
    flask run --host 0.0.0.0 --port=5001 --debug
    ```

    خروجی:

    ```
    * Debug mode: on
    INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5001
    INFO:werkzeug:Press CTRL+C to quit
    INFO:werkzeug: * Restarting with stat
    WARNING:werkzeug: * Debugger is active!
    INFO:werkzeug: * Debugger PIN: 695-801-919
    ```

7.  سرویس Worker را شروع کنید

    برای مصرف وظایف غیر همزمان از صف، مانند وارد کردن فایل مجموعه داده و به روزرسانی سند مجموعه داده، این مراحل را دنبال کنید تا سرویس Worker را در لینوکس یا macOS شروع کنید:

    ```
    celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q dataset,generation,mail,ops_trace
    ```

    اگر از سیستم ویندوز برای شروع سرویس Worker استفاده می کنید، لطفاً به جای آن از دستور زیر استفاده کنید:

    ```
    celery -A app.celery worker -P solo --without-gossip --without-mingle -Q dataset,generation,mail,ops_trace --loglevel INFO
    ```

    خروجی:

    ```
     -------------- celery@TAKATOST.lan v5.2.7 (dawn-chorus)
    --- ***** -----
    -- ******* ---- macOS-10.16-x86_64-i386-64bit 2023-07-31 12:58:08
    - *** --- * ---
    - ** ---------- [config]
    - ** ---------- .> app:         app:0x7fb568572a10
    - ** ---------- .> transport:   redis://:**@localhost:6379/1
    - ** ---------- .> results:     postgresql://postgres:**@localhost:5432/dify
    - *** --- * --- .> concurrency: 1 (gevent)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** -----
     -------------- [queues]
                    .> dataset          exchange=dataset(direct) key=dataset
                    .> generation       exchange=generation(direct) key=generation
                    .> mail             exchange=mail(direct) key=mail

    [tasks]
      . tasks.add_document_to_index_task.add_document_to_index_task
      . tasks.clean_dataset_task.clean_dataset_task
      . tasks.clean_document_task.clean_document_task
      . tasks.clean_notion_document_task.clean_notion_document_task
      . tasks.create_segment_to_index_task.create_segment_to_index_task
      . tasks.deal_dataset_vector_index_task.deal_dataset_vector_index_task
      . tasks.document_indexing_sync_task.document_indexing_sync_task
      . tasks.document_indexing_task.document_indexing_task
      . tasks.document_indexing_update_task.document_indexing_update_task
      . tasks.enable_segment_to_index_task.enable_segment_to_index_task
      . tasks.generate_conversation_summary_task.generate_conversation_summary_task
      . tasks.mail_invite_member_task.send_invite_member_mail_task
      . tasks.remove_document_from_index_task.remove_document_from_index_task
      . tasks.remove_segment_from_index_task.remove_segment_from_index_task
      . tasks.update_segment_index_task.update_segment_index_task
      . tasks.update_segment_keyword_index_task.update_segment_keyword_index_task

    [2023-07-31 12:58:08,831: INFO/MainProcess] Connected to redis://:**@localhost:6379/1
    [2023-07-31 12:58:08,840: INFO/MainProcess] mingle: searching for neighbors
    [2023-07-31 12:58:09,873: INFO/MainProcess] mingle: all alone
    [2023-07-31 12:58:09,886: INFO/MainProcess] pidbox: Connected to redis://:**@localhost:6379/1.
    [2023-07-31 12:58:09,890: INFO/MainProcess] celery@TAKATOST.lan ready.
    ```

---

## استقرار صفحه جلویی

شروع سرویس صفحه جلویی وب کلاینت

#### نصب محیط پایه:

برای شروع سرویس جلویی وب، به [Node.js v18.x (LTS)](http://nodejs.org/) و [NPM نسخه 8.x.x](https://www.npmjs.com/) یا [Yarn](https://yarnpkg.com/) نیاز دارید.

- نصب NodeJS + NPM

لطفاً از [https://nodejs.org/en/download](https://nodejs.org/en/download) بازدید کنید و بسته نصب را برای سیستم عامل مربوطه خود انتخاب کنید که v18.x یا بالاتر است. توصیه می شود نسخه پایدار را دانلود کنید، که NPM را به طور پیش فرض شامل می شود.

#### این مراحل را دنبال کنید:

1.  وارد دایرکتوری وب شوید

    ```
    cd web
    ```

2.  وابستگی ها را نصب کنید.

    ```
    npm install
    ```

3.  متغیرهای محیط را پیکربندی کنید. یک فایل با نام .env.local در دایرکتوری فعلی ایجاد کنید و محتوای آن را از .env.example کپی کنید. مقادیر این متغیرهای محیط را مطابق با نیاز خود تغییر دهید:

    ```
    # برای انتشار تولید، این را به PRODUCTION تغییر دهید
    NEXT_PUBLIC_DEPLOY_ENV=DEVELOPMENT
    # نسخه استقرار، SELF_HOSTED یا CLOUD
    NEXT_PUBLIC_EDITION=SELF_HOSTED
    # URL پایه برنامه کنسول، به URL پایه کنسول سرویس WEB اشاره می کند اگر دامنه کنسول
    # با دامنه api یا برنامه وب متفاوت باشد.
    # مثال: http://cloud.dify.ai/console/api
    NEXT_PUBLIC_API_PREFIX=http://localhost:5001/console/api
    # URL برای برنامه WEB، به URL پایه برنامه WEB سرویس WEB اشاره می کند اگر دامنه برنامه وب با
    # دامنه کنسول یا api متفاوت باشد.
    # مثال: http://udify.app/api
    NEXT_PUBLIC_PUBLIC_API_PREFIX=http://localhost:5001/api

    # SENTRY
    NEXT_PUBLIC_SENTRY_DSN=
    NEXT_PUBLIC_SENTRY_ORG=
    NEXT_PUBLIC_SENTRY_PROJECT=
    ```

4.  کد را بسازید

    ```
    npm run build
    ```

5.  سرویس وب را شروع کنید

    ```
    npm run start
    # یا
    yarn start
    # یا
    pnpm start
    ```

پس از راه اندازی موفق، ترمینال اطلاعات زیر را نمایش خواهد داد:

```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
warn  - You have enabled experimental feature (appDir) in next.config.js.
warn  - Experimental features are not covered by semver, and may cause unexpected or broken application behavior. Use at your own risk.
info  - Thank you for testing `appDir` please leave your feedback at https://nextjs.link/app-feedback
```

### دسترسی به Dify

در نهایت، به [http://127.0.0.1:3000](http://127.0.0.1:3000/) دسترسی پیدا کنید تا از Dify مستقر شده به صورت محلی استفاده کنید.


