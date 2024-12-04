# ادغام با LocalAI برای استقرار مدل‌های محلی

[LocalAI](https://github.com/go-skynet/LocalAI) یک جایگزین API REST  است که با مشخصات API OpenAI برای استنتاج محلی سازگار است.  به شما اجازه می‌دهد تا LLMs (و نه فقط) را به صورت محلی یا در محل با سخت افزار درجه مصرف کننده اجرا کنید و از خانواده‌های مدل‌های مختلفی که با فرمت ggml سازگار هستند، پشتیبانی می‌کند. به GPU نیاز ندارد.

Dify امکان ادغام با LocalAI را برای استقرار محلی قابلیت‌های استنتاج و جاسازی مدل‌های زبان بزرگ فراهم می‌کند.

## استقرار LocalAI

### راه اندازی LocalAI

برای استقرار می‌توانید به راهنمای رسمی [شروع کار](https://localai.io/basics/getting_started/) مراجعه کنید، یا مراحل زیر را به سرعت انجام دهید:

(این مراحل از [مثال پرس و جو داده LocalAI](https://github.com/go-skynet/LocalAI/blob/master/examples/langchain-chroma/README.md) گرفته شده‌اند)

1. ابتدا، مخزن کد LocalAI را کپی کنید و به دایرکتوری مشخص شده بروید.

    ```bash
    $ git clone https://github.com/go-skynet/LocalAI
    $ cd LocalAI/examples/langchain-chroma
    ```

2. مدل‌های LLM و جاسازی مثال را دانلود کنید.

    ```bash
    $ wget https://huggingface.co/skeskinen/ggml/resolve/main/all-MiniLM-L6-v2/ggml-model-q4_0.bin -O models/bert
    $ wget https://gpt4all.io/models/ggml-gpt4all-j.bin -O models/ggml-gpt4all-j
    ```

    در اینجا، ما دو مدل کوچکتر را انتخاب می‌کنیم که در همه پلتفرم‌ها سازگار هستند. `ggml-gpt4all-j` به عنوان مدل LLM پیش فرض و `all-MiniLM-L6-v2` به عنوان مدل جاسازی پیش فرض برای استقرار محلی سریع عمل می‌کنند.

3. فایل .env را پیکربندی کنید.

   ```shell
   $ mv .env.example .env
   ```
   
   نکته: اطمینان حاصل کنید که مقدار متغیر THREADS در `.env` از تعداد هسته‌های CPU روی دستگاه شما تجاوز نکند.

4. LocalAI را راه‌اندازی کنید.

    ```shell
    # با docker-compose راه‌اندازی کنید
    $ docker-compose up -d --build

    # لاگ‌ها را دنبال کنید و منتظر اتمام ساخت باشید
    $ docker logs -f langchain-chroma-api-1
    7:16AM INF Starting LocalAI using 4 threads, with models path: /models
    7:16AM INF LocalAI version: v1.24.1 (9cc8d9086580bd2a96f5c96a6b873242879c70bc)
    ```

	نقطه پایانی API درخواست LocalAI در http://127.0.0.1:8080 در دسترس خواهد بود.

    و دو مدل را ارائه می‌دهد:

    - مدل LLM: `ggml-gpt4all-j`

      نام دسترسی خارجی: `gpt-3.5-turbo` (این نام قابل تنظیم است و می‌تواند در `models/gpt-3.5-turbo.yaml` پیکربندی شود).

    - مدل جاسازی: `all-MiniLM-L6-v2`

      نام دسترسی خارجی: `text-embedding-ada-002` (این نام قابل تنظیم است و می‌تواند در `models/embeddings.yaml` پیکربندی شود).
    > اگر از روش استقرار Dify Docker استفاده می‌کنید، باید به پیکربندی شبکه توجه کنید تا اطمینان حاصل شود که کانتینر Dify می‌تواند به نقطه پایانی LocalAI دسترسی پیدا کند. کانتینر Dify نمی‌تواند به localhost در داخل دسترسی پیدا کند و باید از آدرس IP میزبان استفاده کنید.

5. مدل‌ها را در Dify ادغام کنید.

   به `Settings > Model Providers > LocalAI` بروید و موارد زیر را وارد کنید:

   مدل 1: `ggml-gpt4all-j`

   - نوع مدل: تولید متن

   - نام مدل: `gpt-3.5-turbo`

   - URL سرور: http://127.0.0.1:8080

     اگر Dify از طریق docker مستقر شده است، دامنه میزبان را وارد کنید: `http://<your-LocalAI-endpoint-domain>:8080`، که می‌تواند یک آدرس IP شبکه محلی مانند: `http://192.168.1.100:8080` باشد.

   برای استفاده از مدل در برنامه، روی "ذخیره" کلیک کنید.

   مدل 2: `all-MiniLM-L6-v2`

   - نوع مدل: جاسازی‌ها

   - نام مدل: `text-embedding-ada-002`

   - URL سرور: http://127.0.0.1:8080

     > اگر Dify از طریق docker مستقر شده است، دامنه میزبان را وارد کنید: `http://<your-LocalAI-endpoint-domain>:8080`، که می‌تواند یک آدرس IP شبکه محلی مانند: `http://192.168.1.100:8080` باشد.

   برای استفاده از مدل در برنامه، روی "ذخیره" کلیک کنید.

برای اطلاعات بیشتر در مورد LocalAI، لطفاً به: https://github.com/go-skynet/LocalAI مراجعه کنید.
