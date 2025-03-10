# ابزارهای داده خارجی

ابزارهای داده خارجی برای بازیابی داده‌های اضافی از منابع خارجی پس از ارسال داده‌ها توسط کاربر نهایی و سپس  مونتاژ این داده‌ها به عنوان اطلاعات زمینه اضافی برای LLM استفاده می‌شوند. Dify یک ابزار پیش‌فرض برای تماس‌های API خارجی ارائه می‌کند، برای جزئیات [api-based-extension](../api-based-extension/ "mention") را بررسی کنید.

برای توسعه‌دهندگانی که Dify را به صورت محلی مستقر می‌کنند، برای برآورده کردن نیازهای سفارشی‌تر یا برای جلوگیری از توسعه سرور API اضافی، می‌توانید مستقیماً منطق ابزار داده خارجی سفارشی را به شکل پلاگین مبتنی بر سرویس Dify وارد کنید. پس از گسترش ابزارهای سفارشی، گزینه‌های ابزار سفارشی شما به لیست کشویی انواع ابزار اضافه می‌شوند و اعضای تیم می‌توانند از این ابزارهای سفارشی برای بازیابی داده‌های خارجی استفاده کنند.

## راهنماي سریع

در اینجا مثالی از گسترش ابزار داده خارجی برای `Weather Search` با مراحل زیر آورده شده است:

1.  ایجاد دایرکتوری
2.  اضافه کردن مشخصات فرم فرانت‌اند
3.  اضافه کردن کلاس پیاده‌سازی
4.  پیش نمایش رابط کاربری فرانت‌اند
5.  اشکال‌زدایی پسوند

### 1.  **ایجاد دایرکتوری**

برای اضافه کردن نوع سفارشی `Weather Search`، باید دایرکتوری و فایل‌های مربوطه را در `api/core/external_data_tool` ایجاد کنید.

```python
.
└── api
    └── core
        └── external_data_tool
            └── weather_search
                ├── __init__.py
                ├── weather_search.py
                └── schema.json
```

### 2.  **اضافه کردن مشخصات کامپوننت فرانت‌اند**

*   `schema.json` که مشخصات کامپوننت فرانت‌اند را تعریف می‌کند، در [.](./ "mention") به تفصیل توضیح داده شده است.

```json
{
    "label": {
        "en-US": "Weather Search",
        "zh-Hans": "天气查询"
    },
    "form_schema": [
        {
            "type": "select",
            "label": {
                "en-US": "Temperature Unit",
                "zh-Hans": "温度单位"
            },
            "variable": "temperature_unit",
            "required": true,
            "options": [
                {
                    "label": {
                        "en-US": "Fahrenheit",
                        "zh-Hans": "华氏度"
                    },
                    "value": "fahrenheit"
                },
                {
                    "label": {
                        "en-US": "Centigrade",
                        "zh-Hans": "摄氏度"
                    },
                    "value": "centigrade"
                }
            ],
            "default": "centigrade",
            "placeholder": "Please select temperature unit"
        }
    ]
}
```

### 3. **اضافه کردن کلاس پیاده‌سازی**

الگوی کد `weather_search.py`، جایی که می‌توانید منطق تجاری خاص را پیاده‌سازی کنید.

{% hint style="warning" %}
توجه: متغیر کلاس `name` باید نام نوع سفارشی باشد، با نام دایرکتوری و فایل مطابقت داشته باشد و باید منحصر به فرد باشد.
{% endhint %}

```python
from typing import Optional

from core.external_data_tool.base import ExternalDataTool


class WeatherSearch(ExternalDataTool):
    """
    نام نوع سفارشی باید منحصر به فرد باشد، با نام دایرکتوری و فایل یکسان باشد.
    """
    name: str = "weather_search"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        اعتبارسنجی schema.json. این هنگام ذخیره پیکربندی توسط کاربر فراخوانی می‌شود.

        مثال:
            .. code-block:: python
                config = {
                    "temperature_unit": "centigrade"
                }

        :param tenant_id: شناسه فضای کار
        :param config: متغیرهای پیکربندی فرم
        :return:
        """

        if not config.get('temperature_unit'):
            raise ValueError('temperature unit is required')

    def query(self, inputs: dict, query: Optional[str] = None) -> str:
        """
        پرس و جو از ابزار داده خارجی.

        :param inputs: ورودی‌های کاربر
        :param query: پرس و جوی برنامه گفتگو
        :return: نتیجه پرس و جوی ابزار
        """
        city = inputs.get('city')
        temperature_unit = self.config.get('temperature_unit')

        if temperature_unit == 'fahrenheit':
            return f'Weather in {city} is 32°F'
        else:
            return f'Weather in {city} is 0°C'
```

<!-- ### 4.  **پیش نمایش رابط کاربری فرانت‌اند**

مراحل بالا را دنبال کنید و سرویس را اجرا کنید تا نوع سفارشی جدیدی را که اضافه کرده‌اید مشاهده کنید. -->

<!-- ![](todo) -->

### 4.  **اشکال‌زدایی پسوند**

اکنون می‌توانید نوع پسوند ابزار داده خارجی سفارشی `Weather Search` را در رابط ارکستراسیون برنامه Dify برای اشکال‌زدایی انتخاب کنید.

## الگوی کلاس پیاده‌سازی

```python
from typing import Optional

from core.external_data_tool.base import ExternalDataTool


class WeatherSearch(ExternalDataTool):
    """
    نام نوع سفارشی باید منحصر به فرد باشد، با نام دایرکتوری و فایل یکسان باشد.
    """
    name: str = "weather_search"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        اعتبارسنجی schema.json. این هنگام ذخیره پیکربندی توسط کاربر فراخوانی می‌شود.

        :param tenant_id: شناسه فضای کار
        :param config: متغیرهای پیکربندی فرم
        :return:
        """

        # منطق خودتان را در اینجا پیاده‌سازی کنید

    def query(self, inputs: dict, query: Optional[str] = None) -> str:
        """
        پرس و جو از ابزار داده خارجی.

        :param inputs: ورودی‌های کاربر
        :param query: پرس و جوی برنامه گفتگو
        :return: نتیجه پرس و جوی ابزار
        """
       
        # منطق خودتان را در اینجا پیاده‌سازی کنید
        return "data you own."
```

### معرفی مفصل توسعه کلاس پیاده‌سازی

### def validate_config

روش اعتبارسنجی فرم `schema.json`، که هنگام کلیک کاربر روی "Publish" برای ذخیره پیکربندی فراخوانی می‌شود.

*   `config` پارامترهای فرم
    *   `{{variable}}` متغیرهای فرم سفارشی

### def query

پیاده‌سازی پرس و جوی داده‌های تعریف‌شده توسط کاربر، نتیجه برگردانده شده به متغیر مشخص شده جایگزین می‌شود.

*   `inputs`: متغیرهایی که توسط کاربر نهایی منتقل می‌شوند
*   `query`: محتوای ورودی مکالمه فعلی از کاربر نهایی، یک پارامتر ثابت برای برنامه‌های مکالمه‌ای.
