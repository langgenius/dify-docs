# مدریت محتوای حساس

علاوه بر انواع مدریت محتوای داخلی سیستم، Dify  از قوانین مدریت محتوای تعریف شده توسط کاربر نیز پشتیبانی می‌کند. این روش برای توسعه‌دهندگانی که استقرار شخصی خود را سفارشی می‌کنند مناسب است. به عنوان مثال، در یک راه‌اندازی سرویس مشتری داخلی شرکتی، ممکن است لازم باشد که کاربران هنگام پرس و جو یا نمایندگان سرویس مشتری هنگام پاسخ، نه تنها از وارد کردن کلماتی مربوط به خشونت، سکس و فعالیت‌های غیرقانونی خودداری کنند، بلکه از اصطلاحات خاصی که توسط شرکت ممنوع شده‌اند یا منطق مدریت داخلی را نقض می‌کنند، دوری کنند. توسعه‌دهندگان می‌توانند قوانین مدریت محتوای سفارشی را در سطح کد در یک استقرار خصوصی Dify  توسعه دهند.

## راهنمای سریع

در اینجا مثالی از توسعه نوع مدریت محتوای  `Cloud Service`  با مراحل زیر آورده شده است:

1.  ایجاد دایرکتوری
2.  افزودن فایل تعریف کامپوننت فرانت‌اند
3.  افزودن کلاس پیاده‌سازی
4.  پیش‌نمایش رابط فرانت‌اند
5.  اشکال‌زدایی افزونه

### 1.  ایجاد دایرکتوری

برای افزودن نوع سفارشی `Cloud Service`، دایرکتوری‌ها و فایل‌های مربوطه را در دایرکتوری `api/core/moderation` ایجاد کنید.

```Plain
.
└── api
    └── core
        └── moderation
            └── cloud_service
                ├── __init__.py
                ├── cloud_service.py
                └── schema.json
```

### 2.  افزودن مشخصات کامپوننت فرانت‌اند

*   `schema.json`: این فایل مشخصات کامپوننت فرانت‌اند را تعریف می‌کند. برای جزئیات، به [.](./ "mention") مراجعه کنید.

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

### 3.  افزودن کلاس پیاده‌سازی

قالب کد  `cloud_service.py`  که می‌توانید منطق تجاری خاص خود را پیاده‌سازی کنید.

{% hint style="warning" %}
توجه داشته باشید که نام متغیر کلاس باید با نام نوع سفارشی مطابقت داشته باشد، مطابق با نام دایرکتوری و فایل و باید منحصر به فرد باشد.
{% endhint %}

```python
from core.moderation.base import Moderation, ModerationAction, ModerationInputsResult, ModerationOutputsResult

class CloudServiceModeration(Moderation):
    """
    The name of custom type must be unique, keep the same with directory and file name.
    """
    name: str = "cloud_service"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        schema.json validation. It will be called when user saves the config.

        Example:
            .. code-block:: python
                config = {
                    "cloud_provider": "GoogleCloud",
                    "api_endpoint": "https://api.example.com",
                    "api_keys": "123456",
                    "inputs_config": {
                        "enabled": True,
                        "preset_response": "Your content violates our usage policy. Please revise and try again."
                    },
                    "outputs_config": {
                        "enabled": True,
                        "preset_response": "Your content violates our usage policy. Please revise and try again."
                    }
                }

        :param tenant_id: the id of workspace
        :param config: the variables of form config
        :return:
        """

        cls._validate_inputs_and_outputs_config(config, True)

        if not config.get("cloud_provider"):
            raise ValueError("cloud_provider is required")

        if not config.get("api_endpoint"):
            raise ValueError("api_endpoint is required")

        if not config.get("api_keys"):
            raise ValueError("api_keys is required")

    def moderation_for_inputs(self, inputs: dict, query: str = "") -> ModerationInputsResult:
        """
        Moderation for inputs.

        :param inputs: user inputs
        :param query: the query of chat app, there is empty if is completion app
        :return: the moderation result
        """
        flagged = False
        preset_response = ""

        if self.config['inputs_config']['enabled']:
            preset_response = self.config['inputs_config']['preset_response']

            if query:
                inputs['query__'] = query
            flagged = self._is_violated(inputs)

        # return ModerationInputsResult(flagged=flagged, action=ModerationAction.overridden, inputs=inputs, query=query)
        return ModerationInputsResult(flagged=flagged, action=ModerationAction.DIRECT_OUTPUT, preset_response=preset_response)

    def moderation_for_outputs(self, text: str) -> ModerationOutputsResult:
        """
        Moderation for outputs.

        :param text: the text of LLM response
        :return: the moderation result
        """
        flagged = False
        preset_response = ""

        if self.config['outputs_config']['enabled']:
            preset_response = self.config['outputs_config']['preset_response']

            flagged = self._is_violated({'text': text})

        # return ModerationOutputsResult(flagged=flagged, action=ModerationAction.overridden, text=text)
        return ModerationOutputsResult(flagged=flagged, action=ModerationAction.DIRECT_OUTPUT, preset_response=preset_response)

    def _is_violated(self, inputs: dict):
        """
        The main logic of moderation.

        :param inputs:
        :return: the moderation result
        """
        return False
```

<!-- ### 4. Preview Frontend Interface

Following the above steps, run the service to see the newly added custom type. -->

<!-- ![](todo) -->

### 4. اشکال‌زدایی افزونه

در این مرحله، می‌توانید نوع توسعه مدریت محتوای سفارشی `Cloud Service` را برای اشکال‌زدایی در رابط برنامه‌نویسی Dify انتخاب کنید.

## قالب کلاس پیاده‌سازی

```python
from core.moderation.base import Moderation, ModerationAction, ModerationInputsResult, ModerationOutputsResult

class CloudServiceModeration(Moderation):
    """
    The name of custom type must be unique, keep the same with directory and file name.
    """
    name: str = "cloud_service"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        schema.json validation. It will be called when user saves the config.
        
        :param tenant_id: the id of workspace
        :param config: the variables of form config
        :return:
        """
        cls._validate_inputs_and_outputs_config(config, True)
        
        # implement your own logic here

    def moderation_for_inputs(self, inputs: dict, query: str = "") -> ModerationInputsResult:
        """
        Moderation for inputs.

        :param inputs: user inputs
        :param query: the query of chat app, there is empty if is completion app
        :return: the moderation result
        """
        flagged = False
        preset_response = ""
        
        # implement your own logic here
        
        # return ModerationInputsResult(flagged=flagged, action=ModerationAction.overridden, inputs=inputs, query=query)
        return ModerationInputsResult(flagged=flagged, action=ModerationAction.DIRECT_OUTPUT, preset_response=preset_response)

    def moderation_for_outputs(self, text: str) -> ModerationOutputsResult:
        """
        Moderation for outputs.

        :param text: the text of LLM response
        :return: the moderation result
        """
        flagged = False
        preset_response = ""
        
        # implement your own logic here

        # return ModerationOutputsResult(flagged=flagged, action=ModerationAction.overridden, text=text)
        return ModerationOutputsResult(flagged=flagged, action=ModerationAction.DIRECT_OUTPUT, preset_response=preset_response)
```

## معرفی دقیق توسعه کلاس پیاده‌سازی

### def validate\_config

روش اعتبارسنجی فرم  `schema.json`  هنگامی که کاربر روی "انتشار" برای ذخیره پیکربندی کلیک می‌کند، فراخوانی می‌شود.

*   پارامترهای فرم `config`
    *   `{{variable}}`  متغیر سفارشی فرم
    *   `inputs_config` پاسخ پیش‌فرض مدریت ورودی
        *   `enabled`  فعال بودن یا نبودن
        *   `preset_response`  پاسخ پیش‌فرض ورودی
    *   `outputs_config` پاسخ پیش‌فرض مدریت خروجی
        *   `enabled`  فعال بودن یا نبودن
        *   `preset_response`  پاسخ پیش‌فرض خروجی

### def moderation\_for\_inputs

عملکرد اعتبارسنجی ورودی

*   `inputs`:  ارزشی که توسط کاربر نهایی ارسال می‌شود.
*   `query`:  محتوای ورودی فعلی کاربر نهایی در مکالمه، یک پارامتر ثابت برای برنامه‌های مکالمه‌ای.
*   `ModerationInputsResult`
    *   `flagged`:  آیا قوانین مدریت را نقض می‌کند؟
    *   `action`:  عملکردی که باید انجام شود
        *   `direct_output`:  مستقیم خروجی پاسخ پیش‌فرض
        *   `overridden`:  غیرفعال کردن مقادیر متغیرهای ارسال شده
    *   `preset_response`:  پاسخ پیش‌فرض (فقط در صورت `action=direct_output`  بازگردانده می‌شود)
    *   `inputs`:  ارزشی که توسط کاربر نهایی ارسال می‌شود، با کلید به عنوان نام متغیر و مقدار به عنوان مقدار متغیر (فقط در صورت `action=overridden`  بازگردانده می‌شود)
    *   `query`:  محتوای ورودی فعلی کاربر نهایی در مکالمه، یک پارامتر ثابت برای برنامه‌های مکالمه‌ای (فقط در صورت `action=overridden`  بازگردانده می‌شود)

### def moderation\_for\_outputs

عملکرد اعتبارسنجی خروجی

*   `text`:  محتوای خروجی مدل
*   `moderation_for_outputs`:  عملکرد اعتبارسنجی خروجی
    *   `text`:  محتوای پاسخ LLM. هنگامی که خروجی LLM به صورت قطعه قطعه ارسال می‌شود، این محتوا در بخش‌های 100 کاراکتری است.
    *   `ModerationOutputsResult`
        *   `flagged`:  آیا قوانین مدریت را نقض می‌کند؟
        *   `action`:  عملکردی که باید انجام شود
            *   `direct_output`:  مستقیم خروجی پاسخ پیش‌فرض
            *   `overridden`:  غیرفعال کردن مقادیر متغیرهای ارسال شده
        *   `preset_response`:  پاسخ پیش‌فرض (فقط در صورت `action=direct_output`  بازگردانده می‌شود)
        *   `text`:  محتوای غیراctive شده پاسخ LLM (فقط در صورت `action=overridden`  بازگردانده می‌شود).

