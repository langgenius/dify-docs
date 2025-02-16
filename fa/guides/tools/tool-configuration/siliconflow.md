# سیلیکون‌فلُو (با پشتیبانی Flux AI)

> نویسنده ابزار @hjlarry.

سیلیکون‌فلُو خدمات GenAI با کیفیت بالا را بر اساس مدل‌های پایه منبع باز عالی ارائه می‌دهد. شما می‌توانید از سیلیکون‌فلُو در Dify برای فراخوانی مدل‌های تولید تصویر مانند Flux و Stable Diffusion و ساخت برنامه تولید تصویر هوش مصنوعی خودتان استفاده کنید.

## 1. درخواست کلید API SiliconCloud

یک کلید API جدید در [صفحه مدیریت API SiliconCloud](https://cloud.siliconflow.cn/account/ak) ایجاد کنید و مطمئن شوید که موجودی کافی دارید.

## 2. پر کردن پیکربندی در Dify

در صفحه ابزار Dify، روی `SiliconCloud > To Authorize` کلیک کنید و کلید API را پر کنید.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.04.16.png" alt=""><figcaption></figcaption></figure>

## 3. استفاده از ابزار

* **برنامه Chatflow/Workflow**

برنامه‌های Chatflow و Workflow از اضافه کردن گره‌های ابزار `SiliconFlow` پشتیبانی می‌کنند. شما می‌توانید محتوای ورودی کاربر را از طریق [متغیرها](https://docs.dify.ai/v/zh-hans/guides/workflow/variables) به کادرهای "prompt" و "negative prompt" گره ابزار SiliconFlow منتقل کنید، پارامترهای داخلی را به دلخواه تنظیم کنید و در نهایت محتوای خروجی (متن، تصاویر و غیره) گره ابزار SiliconFlow را در کادر پاسخ گره "end" انتخاب کنید.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.17.40.png" alt=""><figcaption></figcaption></figure>

* **برنامه Agent**

در برنامه Agent، ابزار `Stable Diffusion` یا `Flux` را اضافه کنید، و سپس یک شرح تصویر را در کادر گفتگو ارسال کنید تا ابزار برای تولید تصاویر فراخوانی شود.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.14.16.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.13.06.png" alt=""><figcaption></figcaption></figure>


