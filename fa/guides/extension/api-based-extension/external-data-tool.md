# ابزارهای داده خارجی

ابزارهای داده خارجی برای بازیابی داده‌های اضافی از منابع خارجی پس از ارسال داده توسط کاربر نهایی استفاده می‌شوند و سپس این داده‌ها را به عنوان اطلاعات زمینه اضافی برای LLM جمع‌آوری می‌کنند. Dify یک ابزار پیش‌فرض برای تماس با APIهای خارجی ارائه می‌دهد، برای جزئیات به [ابزار داده خارجی](https://docs.dify.ai/guides/knowledge-base/external-data-tool) مراجعه کنید.

برای توسعه‌دهندگانی که Dify را به صورت محلی مستقر می‌کنند، برای برآورده کردن نیازهای سفارشی‌تر یا اجتناب از توسعه سرور API اضافی، می‌توانید مستقیماً منطق ابزار داده خارجی سفارشی را به صورت افزونه بر اساس سرویس Dify قرار دهید. پس از گسترش ابزارهای سفارشی، گزینه‌های ابزار سفارشی شما به لیست کشویی انواع ابزار اضافه می‌شود و اعضای تیم می‌توانند از این ابزارهای سفارشی برای بازیابی داده‌های خارجی استفاده کنند.

## راهنمای سریع

در اینجا مثالی از گسترش یک ابزار داده خارجی برای `جستجوی آب و هوا` با مراحل زیر آورده شده است:

1.  ایجاد پوشه
2.  اضافه کردن مشخصات فرم سمت کلاینت
3.  اضافه کردن کلاس پیاده‌سازی
4.  پیش‌نمایش رابط سمت کلاینت
5.  رفع اشکال افزونه

### 1. **ایجاد پوشه**

برای اضافه کردن یک نوع سفارشی `جستجوی آب و هوا`، باید پوشه و فایل‌های مربوطه را در `api/core/external_data_tool` ایجاد کنید.

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

### 2. **اضافه کردن مشخصات مؤلفه سمت کلاینت**

*   `schema.json` که مشخصات مؤلفه سمت کلاینت را تعریف می‌کند، جزئیات در [.](./ "mention")

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

قالب کد `weather_search.py`، جایی که می‌توانید منطق تجاری خاص را پیاده‌سازی کنید.

{% hint style="warning" %}
توجه: متغیر کلاس `name` باید نام نوع سفارشی باشد، با نام پوشه و فایل مطابقت داشته باشد و باید منحصر به فرد باشد.
{% endhint %}

```python
from typing import Optional

from core.external_data_tool.base import ExternalDataTool


class WeatherSearch(ExternalDataTool):
    """
    نام نوع سفارشی باید منحصر به فرد باشد، با نام پوشه و فایل مطابقت داشته باشد.
    """
    name: str = "weather_search"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        اعتبارسنجی schema.json. این تابع هنگام ذخیره پیکربندی توسط کاربر فراخوانی می‌شود.

        مثال:
            .. code-block:: python
                config = {
                    "temperature_unit": "centigrade"
                }

        :param tenant_id: شناسه فضای کاری
        :param config: متغیرهای پیکربندی فرم
        :return:
        """

        if not config.get('temperature_unit'):
            raise ValueError('واحد دما الزامی است')

    def query(self, inputs: dict, query: Optional[str] = None) -> str:
        """
        پرس و جو از ابزار داده خارجی.

        :param inputs: ورودی‌های کاربر
        :param query: پرس و جوی برنامه چت
        :return: نتیجه پرس و جوی ابزار
        """
        city = inputs.get('city')
        temperature_unit = self.config.get('temperature_unit')

        if temperature_unit == 'fahrenheit':
            return f'آب و هوا در {city} 32°F است'
        else:
            return f'آب و هوا در {city} 0°C است'
```

<!-- ### 4. **پیش‌نمایش رابط سمت کلاینت**

مراحل بالا را دنبال کنید و سرویس را اجرا کنید تا نوع سفارشی جدید اضافه شده را ببینید.

![](todo)-->

### 4. **رفع اشکال افزونه**

اکنون، می‌توانید نوع افزونه ابزار داده خارجی سفارشی `جستجوی آب و هوا` را در رابط هماهنگی برنامه Dify برای اشکال‌زدایی انتخاب کنید.

## قالب کلاس پیاده‌سازی

```python
from typing import Optional

from core.external_data_tool.base import ExternalDataTool


class WeatherSearch(ExternalDataTool):
    """
    نام نوع سفارشی باید منحصر به فرد باشد، با نام پوشه و فایل مطابقت داشته باشد.
    """
    name: str = "weather_search"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        اعتبارسنجی schema.json. این تابع هنگام ذخیره پیکربندی توسط کاربر فراخوانی می‌شود.

        :param tenant_id: شناسه فضای کاری
        :param config: متغیرهای پیکربندی فرم
        :return:
        """

        # منطق خود را در اینجا پیاده‌سازی کنید

    def query(self, inputs: dict, query: Optional[str] = None) -> str:
        """
        پرس و جو از ابزار داده خارجی.

        :param inputs: ورودی‌های کاربر
        :param query: پرس و جوی برنامه چت
        :return: نتیجه پرس و جوی ابزار
        """
       
        # منطق خود را در اینجا پیاده‌سازی کنید
        return "داده‌های خودتان."
```

### معرفی مفصل توسعه کلاس پیاده‌سازی

### def validate_config

روش اعتبارسنجی فرم `schema.json`، هنگام کلیک کاربر بر روی "انتشار" برای ذخیره پیکربندی فراخوانی می‌شود.

*   `config`: پارامترهای فرم
    *   `{{variable}}`: متغیرهای فرم سفارشی

### def query

پیاده‌سازی پرس و جوی داده تعریف شده توسط کاربر، نتیجه برگردانده شده به متغیر مشخص شده جایگزین می‌شود.

*   `inputs`: متغیرهای منتقل شده توسط کاربر نهایی
*   `query`: محتوای فعلی ورودی مکالمه از کاربر نهایی، یک پارامتر ثابت برای برنامه‌های مکالمه‌ای.
