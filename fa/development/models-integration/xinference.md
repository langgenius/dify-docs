# ادغام مدل‌های محلی مستقر شده توسط Xinference

[استنباط Xorbits](https://github.com/xorbitsai/inference) یک کتابخانه قدرتمند و همه کاره است که برای خدمت رسانی به مدل‌های زبان، تشخیص گفتار و چند رسانه‌ای طراحی شده است و حتی می‌تواند روی لپ‌تاپ‌ها مورد استفاده قرار گیرد. این کتابخانه از مدل‌های مختلفی که با GGML سازگار هستند، مانند chatglm، baichuan، whisper، vicuna، orca و غیره پشتیبانی می‌کند. Dify از اتصال به استنباط مدل‌های زبانی بزرگ و قابلیت‌های جاسازی  Xinference که به طور محلی مستقر شده‌اند، پشتیبانی می‌کند.

## استقرار Xinference

لطفاً توجه داشته باشید که معمولاً نیازی به جستجوی دستی آدرس IP کانتینر Docker برای دسترسی به سرویس ندارید، زیرا Docker ویژگی نگاشت پورت را ارائه می‌دهد. این ویژگی به شما امکان می‌دهد پورت‌های کانتینر را به پورت‌های ماشین محلی نگاشت کنید، که دسترسی از طریق آدرس محلی شما را فعال می‌کند. به عنوان مثال، اگر از پارامتر `-p 80:80` هنگام اجرای کانتینر استفاده کردید، می‌توانید با مراجعه به `http://localhost:80` یا `http://127.0.0.1:80` به سرویس داخل کانتینر دسترسی پیدا کنید.

اگر نیاز دارید مستقیماً از آدرس IP کانتینر استفاده کنید، مراحل بالا به شما در به دست آوردن این اطلاعات کمک خواهد کرد.

### شروع Xinference

دو روش برای استقرار Xinference وجود دارد، به نام [استقرار محلی](https://github.com/xorbitsai/inference/blob/main/README.md#local) و [استقرار توزیع شده](https://github.com/xorbitsai/inference/blob/main/README.md#distributed)، در اینجا استقرار محلی را به عنوان مثال می‌آوریم.

1.  اول، Xinference را از طریق PyPI نصب کنید:

    ```bash
    $ pip install "xinference[all]"
    ```
2.  Xinference را به طور محلی شروع کنید:

    ```bash
    $ xinference-local
    2023-08-20 19:21:05,265 xinference   10148 INFO     Xinference successfully started. Endpoint: http://127.0.0.1:9997
    2023-08-20 19:21:05,266 xinference.core.supervisor 10148 INFO     Worker 127.0.0.1:37822 has been added successfully
    2023-08-20 19:21:05,267 xinference.deploy.worker 10148 INFO     Xinference worker successfully started.
    ```

    Xinference به طور پیش فرض یک worker به طور محلی شروع خواهد کرد، با نقطه انتهایی: `http://127.0.0.1:9997` و پورت پیش فرض `9997` است. به طور پیش فرض، دسترسی فقط به دستگاه محلی محدود می‌شود، اما می‌توان آن را با `-H 0.0.0.0` پیکربندی کرد تا اجازه دسترسی از هر کلاینت غیر محلی را بدهد. برای تغییر میزبان یا پورت، می‌توانید به اطلاعات راهنمایی xinference مراجعه کنید: `xinference-local --help`.

    > اگر از روش استقرار Dify Docker استفاده می‌کنید، باید به پیکربندی شبکه توجه کنید تا مطمئن شوید که کانتینر Dify می‌تواند به نقطه انتهایی Xinference دسترسی داشته باشد. کانتینر Dify نمی‌تواند به localhost در داخل دسترسی داشته باشد و شما باید از آدرس IP میزبان استفاده کنید.
3.  مدل را ایجاد و مستقر کنید

    به `http://127.0.0.1:9997` مراجعه کنید، مدل و مشخصات مورد نیاز خود را برای استقرار انتخاب کنید، همانطور که در زیر نشان داده شده است:

    <figure><img src="../../.gitbook/assets/image (16) (1) (1).png" alt=""><figcaption></figcaption></figure>

    از آنجایی که مدل‌های مختلف سازگاری متفاوتی روی پلتفرم‌های سخت افزاری مختلف دارند، لطفاً به [مدل‌های داخلی Xinference](https://inference.readthedocs.io/en/latest/models/builtin/index.html) مراجعه کنید تا مطمئن شوید که مدل ایجاد شده از پلتفرم سخت افزاری فعلی پشتیبانی می‌کند.
4.  UID مدل را به دست آورید

    ID مدل را از صفحه `Running Models` کپی کنید، مانند: `2c886330-8849-11ee-9518-43b0b8f40bea`
5.  پس از استقرار مدل، مدل مستقر شده را در Dify متصل کنید.

    در `Settings > Model Providers > Xinference`، موارد زیر را وارد کنید:

    * نام مدل: `vicuna-v1.3`
    * آدرس سرور: `http://<Machine_IP>:9997` **با آدرس IP دستگاه خود جایگزین کنید**
    * UID مدل: `2c886330-8849-11ee-9518-43b0b8f40bea`

    برای استفاده از مدل در برنامه dify، روی "ذخیره" کلیک کنید.

Dify از استفاده از [مدل‌های داخلی Xinference](https://github.com/xorbitsai/inference/blob/main/README.md#builtin-models) به عنوان مدل‌های جاسازی نیز پشتیبانی می‌کند، فقط در کادر تنظیمات، نوع جاسازی را انتخاب کنید.

برای اطلاعات بیشتر در مورد Xinference، لطفاً به [Xorbits Inference](https://github.com/xorbitsai/inference) مراجعه کنید.

