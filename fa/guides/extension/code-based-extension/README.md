#  افزونه‌های مبتنی بر کد

برای توسعه‌دهندگانی که Dify را به صورت محلی مستقر می‌کنند، اگر می‌خواهید قابلیت‌های افزونه را بدون بازنویسی سرویس API پیاده‌سازی کنید، می‌توانید از افزونه‌های کد استفاده کنید. این امکان به شما اجازه می‌دهد تا قابلیت‌های برنامه را به شکل کد (مثلا قابلیت پلاگین) گسترش یا ارتقا دهید، بدون اینکه منطق اصلی کد Dify را مختل کنید. این افزونه‌ها از رابط‌ها یا مشخصات خاصی پیروی می‌کنند تا سازگاری و قابلیت اتصال و استفاده آسان را با برنامه اصلی تضمین کنند. در حال حاضر، Dify دو نوع افزونه کد ارائه می‌دهد:

* اضافه کردن نوع جدیدی از ابزار داده خارجی [ابزار داده خارجی](https://docs.dify.ai/guides/extension/api-based-extension/external-data-tool)
* گسترش استراتژی‌های تعدیل محتوای حساس [تعدیل](https://docs.dify.ai/guides/extension/api-based-extension/moderation)

با توجه به قابلیت‌های بالا، می‌توانید با پیروی از مشخصات رابطه‌ سطح کد، گسترش افقی را انجام دهید. اگر تمایل دارید افزونه‌های خود را به ما ارائه دهید، از ارسال PR به Dify استقبال می‌کنیم.

## تعریف مشخصات مؤلفه سمت کاربر

سبک‌های سمت کاربر افزونه‌های کد از طریق `schema.json` تعریف می‌شوند:

* label: نام نوع سفارشی، از تغییر زبان سیستم پشتیبانی می‌کند
* form_schema: لیستی از محتویات فرم
  * type: نوع مؤلفه
    * select: گزینه‌های کشویی
    * text-input: متن
    * paragraph: پاراگراف
  * label: نام مؤلفه، از تغییر زبان سیستم پشتیبانی می‌کند
  * variable: نام متغیر
  * required: آیا الزامی است
  * default: مقدار پیش‌فرض
  * placeholder: محتوای راهنما برای مؤلفه
  * options: ویژگی اختصاصی برای مؤلفه "select"، تعریف محتویات کشویی
    * label: نام کشویی، از تغییر زبان سیستم پشتیبانی می‌کند
    * value: مقدار گزینه کشویی
  * max_length: ویژگی اختصاصی برای مؤلفه "text-input"، حداکثر طول

### مثال الگو

```json
{
    "label": {
        "en-US": "Cloud Service",
        "zh-Hans": "云服务"
    },
    "form_schema": [
        {
            "type": "select",
            "label": {
                "en-US": "Cloud Provider",
                "zh-Hans": "云厂商"
            },
            "variable": "cloud_provider",
            "required": true,
            "options": [
                {
                    "label": {
                        "en-US": "AWS",
                        "zh-Hans": "亚马逊"
                    },
                    "value": "AWS"
                },
                {
                    "label": {
                        "en-US": "Google Cloud",
                        "zh-Hans": "谷歌云"
                    },
                    "value": "GoogleCloud"
                },
                {
                    "label": {
                        "en-US": "Azure Cloud",
                        "zh-Hans": "微软云"
                    },
                    "value": "Azure"
                }
            ],
            "default": "GoogleCloud",
            "placeholder": ""
        },
        {
            "type": "text-input",
            "label": {
                "en-US": "API Endpoint",
                "zh-Hans": "API Endpoint"
            },
            "variable": "api_endpoint",
            "required": true,
            "max_length": 100,
            "default": "",
            "placeholder": "https://api.example.com"
        },
        {
            "type": "paragraph",
            "label": {
                "en-US": "API Key",
                "zh-Hans": "API Key"
            },
            "variable": "api_keys",
            "required": true,
            "default": "",
            "placeholder": "Paste your API key here"
        }
    ]
}
```
