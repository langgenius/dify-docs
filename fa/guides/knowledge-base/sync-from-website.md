---
description: >-
  این سند در درجه اول به نحوه جمع‌آوری داده‌ها از یک صفحه وب، تجزیه آن به Markdown و وارد کردن آن به پایگاه دانش Dify می‌پردازد.
---

# همگام‌سازی داده‌ها از وب‌سایت

پایگاه دانش Dify از خزش محتوا از صفحات وب عمومی با استفاده از ابزارهای شخص ثالث مانند [Jina Reader](https://jina.ai/reader/) و [Firecrawl](https://www.firecrawl.dev/)، تجزیه آن به محتوای Markdown و وارد کردن آن به پایگاه دانش پشتیبانی می‌کند.

{% hint style="info" %}
​[Firecrawl](https://www.firecrawl.dev/) و [Jina Reader](https://jina.ai/reader/) هر دو ابزار تجزیه وب متن باز هستند که می‌توانند صفحات وب را به متن تمیز Markdown که برای LLM ها قابل تشخیص است، تبدیل کنند، در حالی که خدمات API آسان برای استفاده را ارائه می‌دهند.
{% endhint %}

بخش‌های بعدی به ترتیب روش‌های استفاده برای Firecrawl و Jina Reader را معرفی می‌کنند.

### Firecrawl <a href="#how-to-configure" id="how-to-configure"></a>

#### **1. پیکربندی اعتبارنامه‌های API Firecrawl**

روی آواتار در گوشه بالا سمت راست کلیک کنید، سپس به صفحه **DataSource** بروید و روی دکمه **Configure** در کنار Firecrawl کلیک کنید.

<figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FRncMhlfeYTrpujwzDIqw%2Fuploads%2FQ2CvvgqQXmsUMXZR4u8N%2Fimage.png?alt=media&#x26;token=f7273557-94f7-4250-adfe-8d2e11f6a307" alt=""><figcaption><p>پیکربندی اعتبارنامه‌های Firecrawl</p></figcaption></figure>

برای تکمیل ثبت نام، به [وب سایت Firecrawl](https://www.firecrawl.dev/) وارد شوید، API Key خود را دریافت کنید و سپس آن را وارد کنید و در Dify ذخیره کنید.

<figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FRncMhlfeYTrpujwzDIqw%2Fuploads%2FtAwcLoAYT1A2v12pfJC3%2Fimage.png?alt=media&#x26;token=3b5b784f-2808-431f-8595-2638d038c190" alt=""><figcaption><p>API Key را دریافت کنید و آن را در Dify ذخیره کنید</p></figcaption></figure>

#### 2. خراشیدن صفحه وب هدف

در صفحه ایجاد پایگاه دانش، **Sync from website** را انتخاب کنید، Firecrawl را به عنوان ارائه دهنده انتخاب کنید و URL هدف را برای خزش وارد کنید.

<figure><img src="../../.gitbook/assets/image (102).png" alt=""><figcaption><p>پیکربندی خراشیدن وب</p></figcaption></figure>

گزینه‌های پیکربندی شامل: آیا باید زیرصفحات را خزش کنید، محدودیت خزش صفحه، حداکثر عمق خراشیدن صفحه، مسیرهای حذف شده، شامل فقط مسیرها و دامنه استخراج محتوا. پس از تکمیل پیکربندی، روی **Run** کلیک کنید تا صفحات تجزیه شده را پیش‌نمایش کنید.

<figure><img src="../../.gitbook/assets/image (103).png" alt=""><figcaption><p>اجرای خراشیدن</p></figcaption></figure>

#### 3. بررسی نتایج واردات

پس از وارد کردن متن تجزیه شده از صفحه وب، در اسناد پایگاه دانش ذخیره می‌شود. نتایج واردات را مشاهده کنید و روی **Add URL** کلیک کنید تا واردات صفحات وب جدید ادامه یابد.

<figure><img src="../../.gitbook/assets/image (104).png" alt=""><figcaption><p>وارد کردن متن وب تجزیه شده به پایگاه دانش</p></figcaption></figure>

***

### Jina Reader

#### 1. پیکربندی اعتبارنامه‌های Jina Reader&#x20;

روی آواتار در گوشه بالا سمت راست کلیک کنید، سپس به صفحه **DataSource** بروید و روی دکمه **Configure** در کنار Jina Reader کلیک کنید.

<figure><img src="../../.gitbook/assets/image (105).png" alt=""><figcaption><p>پیکربندی Jina Reader</p></figcaption></figure>

به [وب سایت Jina Reader](https://jina.ai/reader/) وارد شوید، ثبت نام را کامل کنید، API Key را دریافت کنید، سپس آن را پر کنید و ذخیره کنید.

<figure><img src="../../.gitbook/assets/image (106).png" alt=""><figcaption><p>پر کردن پیکربندی Jina</p></figcaption></figure>

#### 2. استفاده از Jina Reader برای خزش محتوای وب&#x20;

در صفحه ایجاد پایگاه دانش، Sync from website را انتخاب کنید، Jina Reader را به عنوان ارائه دهنده انتخاب کنید و URL هدف را برای خزش وارد کنید.

<figure><img src="../../.gitbook/assets/image (107).png" alt=""><figcaption><p>پیکربندی خزش وب</p></figcaption></figure>

گزینه‌های پیکربندی شامل: آیا باید زیرصفحات را خزش کنید، حداکثر تعداد صفحات برای خزش و آیا باید از sitemap برای خزش استفاده کنید. پس از تکمیل پیکربندی، روی دکمه **Run** کلیک کنید تا پیوندهای صفحه ای که باید خزش شوند را پیش‌نمایش کنید.

<figure><img src="../../.gitbook/assets/image (109).png" alt=""><figcaption><p>اجرای خزش</p></figcaption></figure>

متن تجزیه شده را از صفحات وب وارد کنید و آن را در اسناد پایگاه دانش ذخیره کنید، سپس نتایج واردات را مشاهده کنید. برای ادامه اضافه کردن صفحات وب، روی دکمه Add URL در سمت راست کلیک کنید تا صفحات وب جدید وارد شوند.

<figure><img src="../../.gitbook/assets/image (110).png" alt=""><figcaption><p>وارد کردن متن وب تجزیه شده به پایگاه دانش</p></figcaption></figure>

پس از اتمام خزش، محتوای صفحات وب در پایگاه دانش ادغام خواهد شد.


