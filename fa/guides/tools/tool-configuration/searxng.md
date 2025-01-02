# SearXNG
SearXNG یک موتور جستجوی متا آزاد است که نتایج را از سرویس‌ها و پایگاه‌های داده مختلف جمع‌آوری می‌کند. کاربران نه ردیابی می‌شوند و نه پروفایل می‌شوند. اکنون می‌توانید مستقیماً از این ابزار در Dify استفاده کنید.

در زیر مراحل ادغام SearXNG در Dify با استفاده از Docker در [Community Edition](https://docs.dify.ai/getting-started/install-self-hosted/docker-compose) آورده شده است.

> اگر می‌خواهید از SearXNG در سرویس ابری Dify استفاده کنید، لطفاً به [مستندات نصب SearXNG](https://docs.searxng.org/admin/installation.html) مراجعه کنید تا سرویس خود را راه‌اندازی کنید، سپس به Dify برگردید و آدرس پایه سرویس را در صفحه "ابزارها > SearXNG > احراز هویت" وارد کنید.

## 1. تغییر فایل پیکربندی Dify

فایل پیکربندی در مسیر `dify/api/core/tools/provider/builtin/searxng/docker/settings.yml` قرار دارد و می‌توانید به مستندات پیکربندی [اینجا](https://docs.searxng.org/admin/settings/index.html) مراجعه کنید.

## 2. شروع سرویس

ظرف Docker را در دایرکتوری ریشه dify راه‌اندازی کنید.

```bash
cd dify
docker run --rm -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```

## 3. استفاده از SearXNG

آدرس دسترسی را در "ابزارها > SearXNG > احراز هویت" وارد کنید تا ارتباط بین سرویس Dify و سرویس SearXNG برقرار شود. آدرس داخلی Docker برای SearXNG معمولاً `http://host.docker.internal:8081` است.


