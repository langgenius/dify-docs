# DifySandbox

### مقدمه
`DifySandbox` یک محیط اجرای کد سبک، سریع و امن است که از زبان‌های برنامه‌نویسی مختلفی مانند پایتون و Node.js پشتیبانی می‌کند. این محیط به عنوان بستر اجرایی زیربنایی برای اجزای مختلف در Dify Workflow مانند گره کد، گره تبدیل قالب، گره LLM و مترجم کد در گره ابزار عمل می‌کند. DifySandbox امنیت سیستم را تضمین می‌کند و در عین حال به Dify اجازه می‌دهد کدهای ارائه‌شده توسط کاربر را اجرا کند.

### ویژگی‌ها
- **پشتیبانی چند زبانه**: DifySandbox بر اساس Seccomp، یک مکانیسم امنیتی سطح پایین ساخته شده است که امکان پشتیبانی از چندین زبان برنامه‌نویسی را فراهم می‌کند. در حال حاضر از پایتون و Node.js پشتیبانی می‌کند.
- **امنیت سیستم**: از یک سیاست لیست سفید استفاده می‌کند که فقط به تماس‌های سیستم خاص اجازه می‌دهد تا از نقض امنیتی غیرمنتظره جلوگیری کند.
- **جداسازی فایل سیستم**: کد کاربر در یک محیط جداگانه فایل سیستم اجرا می‌شود.
- **جداسازی شبکه**:
    - **DockerCompose**: از یک شبکه Sandbox جداگانه و کانتینرهای پروکسی برای دسترسی به شبکه استفاده می‌کند و امنیت سیستم درون شبکه را حفظ می‌کند و در عین حال گزینه‌های پیکربندی پروکسی انعطاف‌پذیری را ارائه می‌دهد.
    - **K8s**: استراتژی‌های جداسازی شبکه را می‌توان به طور مستقیم با استفاده از سیاست‌های خروجی پیکربندی کرد.

### مخزن پروژه
می‌توانید با دسترسی به [DifySandbox](https://github.com/langgenius/dify-sandbox) ، کد منبع پروژه را دریافت کرده و برای دستورالعمل‌های استقرار و استفاده، مستندات پروژه را دنبال کنید.

### مشارکت
لطفاً به [راهنمای مشارکت](contribution.md) مراجعه کنید تا نحوه مشارکت در توسعه DifySandbox را یاد بگیرید. 