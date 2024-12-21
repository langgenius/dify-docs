# ادغام ابزار پیشرفته

قبل از شروع این راهنمای پیشرفته، لطفاً اطمینان حاصل کنید که درک پایه ای از فرآیند ادغام ابزار در Dify دارید. [ادغام سریع](https://docs.dify.ai/tutorials/quick-tool-integration) را برای یک مرور سریع ببینید.

### رابط ابزار

ما مجموعه ای از متدهای کمکی را در کلاس `Tool` برای کمک به توسعه دهندگان برای ساخت سریعتر ابزارهای پیچیده تر تعریف کرده ایم.

#### بازگشت پیام

Dify از انواع مختلف پیام مانند `text`، `link`، `image` و `file BLOB` پشتیبانی می کند. شما می توانید انواع مختلفی از پیام ها را از طریق رابط های زیر به LLM و کاربران برگردانید.

لطفاً توجه داشته باشید که برخی از پارامترها در رابط های زیر در بخش های بعدی معرفی خواهند شد.

**آدرس اینترنتی تصویر**

شما فقط باید آدرس اینترنتی تصویر را ارسال کنید و Dify به طور خودکار تصویر را دانلود کرده و به کاربر باز می گرداند.

```python
    def create_image_message(self, image: str, save_as: str = '') -> ToolInvokeMessage:
        """
            ایجاد یک پیام تصویر

            :param image: آدرس اینترنتی تصویر
            :return: پیام تصویر
        """
```

**لینک**

اگر نیاز به بازگشت یک لینک دارید، می توانید از رابط زیر استفاده کنید.

```python
    def create_link_message(self, link: str, save_as: str = '') -> ToolInvokeMessage:
        """
            ایجاد یک پیام لینک

            :param link: آدرس اینترنتی لینک
            :return: پیام لینک
        """
```

**متن**

اگر نیاز به بازگشت یک پیام متنی دارید، می توانید از رابط زیر استفاده کنید.

```python
    def create_text_message(self, text: str, save_as: str = '') -> ToolInvokeMessage:
        """
            ایجاد یک پیام متنی

            :param text: متن پیام
            :return: پیام متنی
        """
```

**فایل BLOB**

اگر نیاز به بازگشت داده های خام یک فایل مانند تصاویر، صدا، فیلم، PPT، Word، Excel و غیره دارید، می توانید از رابط زیر استفاده کنید.

* `blob` داده های خام فایل، از نوع بایت
* `meta` متاداده فایل، اگر نوع فایل را می دانید، بهتر است `mime_type` را ارسال کنید، در غیر این صورت Dify از `octet/stream` به عنوان نوع پیش فرض استفاده می کند.

```python
    def create_blob_message(self, blob: bytes, meta: dict = None, save_as: str = '') -> ToolInvokeMessage:
        """
            ایجاد یک پیام Blob

            :param blob: Blob
            :return: پیام Blob
        """
```

#### ابزارهای میانبر

در برنامه های مدل بزرگ، دو نیاز متداول داریم:

* اول، خلاصه کردن یک متن طولانی به طور پیشرفته و سپس ارسال محتوای خلاصه شده به LLM برای جلوگیری از طولانی بودن متن اصلی برای LLM.
* محتوای به دست آمده توسط ابزار یک لینک است و اطلاعات صفحه وب باید قبل از اینکه به LLM برگردانده شود، خزیده شود.

برای کمک به توسعه دهندگان برای پیاده سازی سریع این دو نیاز، دو ابزار میانبر زیر را ارائه می دهیم.

**ابزار خلاصه متن**

این ابزار یک `user_id` و متنی که باید خلاصه شود را دریافت می کند و متن خلاصه شده را بر می گرداند. Dify از مدل پیش فرض فضای کاری فعلی برای خلاصه کردن متن طولانی استفاده می کند.

```python
    def summary(self, user_id: str, content: str) -> str:
        """
            خلاصه کردن محتوا

            :param user_id: شناسه کاربر
            :param content: محتوا
            :return: خلاصه
        """
```

**ابزار خزیدن صفحه وب**

این ابزار یک لینک صفحه وب که باید خزیده شود و یک `user_agent` (که می تواند خالی باشد) را دریافت می کند و رشته ای حاوی اطلاعات صفحه وب را بر می گرداند. `user_agent` یک پارامتر اختیاری است که می تواند برای شناسایی ابزار استفاده شود. اگر ارسال نشود، Dify از `user_agent` پیش فرض استفاده می کند.

```python
    def get_url(self, url: str, user_agent: str = None) -> str:
        """
            دریافت URL
        """ نتیجه خزیده شده
```

#### استخر متغیر

ما یک استخر متغیر را در `Tool` برای ذخیره متغیرها، فایل ها و غیره که در طول عملیات ابزار تولید می شوند، معرفی کرده ایم. این متغیرها می توانند در طول عملیات ابزار توسط ابزارهای دیگر استفاده شوند.

در ادامه، `DallE3` و `Vectorizer.AI` را به عنوان مثال برای معرفی نحوه استفاده از استخر متغیر استفاده خواهیم کرد.

* `DallE3` یک ابزار تولید تصویر است که می تواند تصاویر را بر اساس متن ایجاد کند. در اینجا، ما از `DallE3` می خواهیم که یک لوگو برای یک کافی شاپ ایجاد کند.
* `Vectorizer.AI` یک ابزار تبدیل تصویر برداری است که می تواند تصاویر را به تصاویر برداری تبدیل کند، به طوری که تصاویر را می توان بدون اعوجاج به طور نامحدود بزرگ کرد. در اینجا، ما آیکون PNG تولید شده توسط `DallE3` را به یک تصویر برداری تبدیل می کنیم تا بتوان از آن توسط طراحان استفاده کرد.

**DallE3**

اول، از DallE3 استفاده می کنیم. پس از ایجاد تصویر، تصویر را در استخر متغیر ذخیره می کنیم. کد به شرح زیر است:

```python
from typing import Any, Dict, List, Union
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

from base64 import b64decode

from openai import OpenAI

class DallE3Tool(BuiltinTool):
    def _invoke(self, 
                user_id: str, 
               tool_Parameters: Dict[str, Any], 
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            فراخوانی ابزارها
        """
        client = OpenAI(
            api_key=self.runtime.credentials['openai_api_key'],
        )

        # درخواست
        prompt = tool_Parameters.get('prompt', '')
        if not prompt:
            return self.create_text_message('لطفاً درخواست را وارد کنید')

        # تماس با openapi dalle3
        response = client.images.generate(
            prompt=prompt, model='dall-e-3',
            size='1024x1024', n=1, style='vivid', quality='standard',
            response_format='b64_json'
        )

        result = []
        for image in response.data:
            # ذخیره همه تصاویر در استخر متغیر از طریق پارامتر save_as. نام متغیر self.VARIABLE_KEY.IMAGE.value است. اگر بعداً تصاویر جدیدی تولید شود، تصاویر قبلی را بازنویسی خواهند کرد.
            result.append(self.create_blob_message(blob=b64decode(image.b64_json), 
                                                   meta={ 'mime_type': 'image/png' },
                                                    save_as=self.VARIABLE_KEY.IMAGE.value))

        return result
```

توجه داشته باشید که ما از `self.VARIABLE_KEY.IMAGE.value` به عنوان نام متغیر تصویر استفاده کردیم. برای اینکه ابزارهای توسعه دهندگان بتوانند با یکدیگر همکاری کنند، این `KEY` را تعریف کرده ایم. می توانید از آن به طور آزاد استفاده کنید یا می توانید انتخاب کنید که از آن استفاده نکنید. ارسال یک KEY سفارشی نیز قابل قبول است.

**Vectorizer.AI**

در ادامه، از Vectorizer.AI برای تبدیل آیکون PNG تولید شده توسط DallE3 به یک تصویر برداری استفاده می کنیم. بیایید توابعی را که در اینجا تعریف کرده ایم، مرور کنیم. کد به شرح زیر است:

```python
from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage, ToolParameter
from core.tools.errors import ToolProviderCredentialValidationError

from typing import Any, Dict, List, Union
from httpx import post
from base64 import b64decode

class VectorizerTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_Parameters: Dict[str, Any]) \
        -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
        فراخوانی ابزار، نام متغیر تصویر باید از اینجا ارسال شود تا بتوانیم تصویر را از استخر متغیر دریافت کنیم
        """
        
    
    def get_runtime_parameters(self) -> List[ToolParameter]:
        """
        فهرست پارامترهای ابزار را دوباره تعریف می کنیم، می توانیم به طور پویا فهرست پارامترها را بر اساس شرایط واقعی در استخر متغیر فعلی ایجاد کنیم تا LLM بتواند فرم را بر اساس فهرست پارامترها ایجاد کند
        """
        
    
    def is_tool_available(self) -> bool:
        """
        آیا ابزار فعلی در دسترس است، اگر هیچ تصویری در استخر متغیر فعلی وجود نداشته باشد، پس نیازی به نمایش این ابزار نیست، فقط False را در اینجا برگردانید
        """     
```

در ادامه، این سه تابع را پیاده سازی می کنیم

```python
from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage, ToolParameter
from core.tools.errors import ToolProviderCredentialValidationError

from typing import Any, Dict, List, Union
from httpx import post
from base64 import b64decode

class VectorizerTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_Parameters: Dict[str, Any]) \
        -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            فراخوانی ابزارها
        """
        api_key_name = self.runtime.credentials.get('api_key_name', None)
        api_key_value = self.runtime.credentials.get('api_key_value', None)

        if not api_key_name or not api_key_value:
            raise ToolProviderCredentialValidationError('لطفاً نام و مقدار کلید API را وارد کنید')

        # دریافت image_id، تعریف image_id را می توان در get_runtime_parameters یافت
        image_id = tool_Parameters.get('image_id', '')
        if not image_id:
            return self.create_text_message('لطفاً شناسه تصویر را وارد کنید')

        # دریافت تصویر تولید شده توسط DallE از استخر متغیر
        image_binary = self.get_variable_file(self.VARIABLE_KEY.IMAGE)
        if not image_binary:
            return self.create_text_message('تصویر یافت نشد، لطفاً از کاربر بخواهید که ابتدا تصویر را ایجاد کند.')

        # تولید تصویر برداری
        response = post(
            'https://vectorizer.ai/api/v1/vectorize',
            files={ 'image': image_binary },
            data={ 'mode': 'test' },
            auth=(api_key_name, api_key_value), 
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(response.text)
        
        return [
            self.create_text_message('تصویر برداری شده SVG به عنوان یک تصویر ذخیره شده است.'),
            self.create_blob_message(blob=response.content,
                                    meta={'mime_type': 'image/svg+xml'})
        ]
    
    def get_runtime_parameters(self) -> List[ToolParameter]:
        """
        پارامترهای زمان اجرا را دوباره تعریف می کنیم
        """
        # در اینجا، فهرست پارامترهای ابزار را دوباره تعریف می کنیم، image_id را تعریف می کنیم و فهرست گزینه های آن را به همه تصاویر در استخر متغیر فعلی تنظیم می کنیم. پیکربندی اینجا با پیکربندی در yaml مطابقت دارد.
        return [
            ToolParameter.get_simple_instance(
                name='image_id',
                llm_description=f'شناسه تصویری که می خواهید برداری کنید، \
                    و شناسه تصویر باید در \
                        {[i.name for i in self.list_default_image_variables()]} مشخص شود.',
                type=ToolParameter.ToolParameterType.SELECT,
                required=True,
                options=[i.name for i in self.list_default_image_variables()]
            )
        ]
    
    def is_tool_available(self) -> bool:
        # فقط وقتی تصاویر در استخر متغیر وجود داشته باشد، LLM باید از این ابزار استفاده کند
        return len(self.list_default_image_variables()) > 0
```

لازم به ذکر است که در اینجا از `image_id` استفاده نکردیم. فرض کردیم که هنگام فراخوانی این ابزار، باید یک تصویر در استخر متغیر پیش فرض وجود داشته باشد، بنابراین به طور مستقیم از `image_binary = self.get_variable_file(self.VARIABLE_KEY.IMAGE)` برای دریافت تصویر استفاده کردیم. در مواردی که قابلیت های مدل ضعیف است، به توسعه دهندگان توصیه می کنیم که همین کار را انجام دهند که می تواند به طور موثری تحمل خطا را بهبود بخشد و از ارسال پارامترهای نادرست توسط مدل جلوگیری کند.


