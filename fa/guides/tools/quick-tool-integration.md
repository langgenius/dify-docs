# ادغام سریع ابزار

در اینجا، از GoogleSearch به عنوان مثال استفاده خواهیم کرد تا نشان دهیم چگونه یک ابزار را به سرعت ادغام کنیم.

### 1. آماده سازی فایل YAML ارائه دهنده ابزار

#### مقدمه

این فایل YAML یک ارائه دهنده ابزار جدید را اعلام می کند و اطلاعاتی مانند نام ارائه دهنده، آیکون، نویسنده و سایر جزئیات را شامل می شود که توسط فرانت اند برای نمایش بازیابی می شوند.

#### مثال

باید یک ماژول `google` (پوشه) زیر `core/tools/provider/builtin` ایجاد کنیم و `google.yaml` را بسازیم. نام باید با نام ماژول مطابقت داشته باشد.

پس از آن، تمام عملیات مرتبط با این ابزار در این ماژول انجام خواهد شد.

```yaml
identity: # اطلاعات پایه ارائه دهنده ابزار
  author: Dify # نویسنده
  name: google # نام، منحصر به فرد، بدون تکرار با سایر ارائه دهندگان
  label: # برچسب برای نمایش در فرانت اند
    en_US: Google # برچسب انگلیسی
    zh_Hans: Google # برچسب چینی
  description: # توضیحات برای نمایش در فرانت اند
    en_US: Google # توضیحات انگلیسی
    zh_Hans: Google # توضیحات چینی
  icon: icon.svg # آیکون، باید در پوشه _assets ماژول فعلی قرار داده شود

```

* فیلد `identity` الزامی است، این فیلد اطلاعات پایه ارائه دهنده ابزار را شامل می شود، از جمله نویسنده، نام، برچسب، توضیحات، آیکون، و غیره.
  * آیکون باید در پوشه `_assets` ماژول فعلی قرار داده شود، می توانید به: api/core/tools/provider/builtin/google/\_assets/icon.svg مراجعه کنید

      ```xml
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="25" viewBox="0 0 24 25" fill="none">
        <path d="M22.501 12.7332C22.501 11.8699 22.4296 11.2399 22.2748 10.5865H12.2153V14.4832H18.12C18.001 15.4515 17.3582 16.9099 15.9296 17.8898L15.9096 18.0203L19.0902 20.435L19.3106 20.4565C21.3343 18.6249 22.501 15.9298 22.501 12.7332Z" fill="#4285F4"/>
        <path d="M12.214 23C15.1068 23 17.5353 22.0666 19.3092 20.4567L15.9282 17.8899C15.0235 18.5083 13.8092 18.9399 12.214 18.9399C9.38069 18.9399 6.97596 17.1083 6.11874 14.5766L5.99309 14.5871L2.68583 17.0954L2.64258 17.2132C4.40446 20.6433 8.0235 23 12.214 23Z" fill="#34A853"/>
        <path d="M6.12046 14.5766C5.89428 13.9233 5.76337 13.2233 5.76337 12.5C5.76337 11.7766 5.89428 11.0766 6.10856 10.4233L6.10257 10.2841L2.75386 7.7355L2.64429 7.78658C1.91814 9.20993 1.50146 10.8083 1.50146 12.5C1.50146 14.1916 1.91814 15.7899 2.64429 17.2132L6.12046 14.5766Z" fill="#FBBC05"/>
        <path d="M12.2141 6.05997C14.2259 6.05997 15.583 6.91163 16.3569 7.62335L19.3807 4.73C17.5236 3.03834 15.1069 2 12.2141 2C8.02353 2 4.40447 4.35665 2.64258 7.78662L6.10686 10.4233C6.97598 7.89166 9.38073 6.05997 12.2141 6.05997Z" fill="#EB4335"/>
      </svg>
      ```

### 2. آماده سازی گواهی نامه ارائه دهنده

Google، به عنوان یک ابزار شخص ثالث، از API ارائه شده توسط SerpApi استفاده می کند که برای استفاده به یک API Key نیاز دارد. این به این معنی است که این ابزار برای استفاده به یک گواهی نامه نیاز دارد. برای ابزارهایی مانند `wikipedia`، نیازی به پر کردن فیلد گواهی نامه نیست، می توانید به: api/core/tools/provider/builtin/wikipedia/wikipedia.yaml مراجعه کنید

```yaml
identity:
  author: Dify
  name: wikipedia
  label:
    en_US: Wikipedia
    zh_Hans: 维基百科
    pt_BR: Wikipedia
  description:
    en_US: Wikipedia is a free online encyclopedia, created and edited by volunteers around the world.
    zh_Hans: 维基百科是一个由全世界的志愿者创建和编辑的免费在线百科全书。
    pt_BR: Wikipedia is a free online encyclopedia, created and edited by volunteers around the world.
  icon: icon.svg
credentials_for_provider:
```

پس از پیکربندی فیلد گواهی نامه، اثر به شرح زیر خواهد بود:

```yaml
identity:
  author: Dify
  name: google
  label:
    en_US: Google
    zh_Hans: Google
  description:
    en_US: Google
    zh_Hans: Google
  icon: icon.svg
credentials_for_provider: # فیلد گواهی نامه
  serpapi_api_key: # نام فیلد گواهی نامه
    type: secret-input # نوع فیلد گواهی نامه
    required: true # الزامی بودن یا نبودن
    label: # برچسب فیلد گواهی نامه
      en_US: SerpApi API key # برچسب انگلیسی
      zh_Hans: SerpApi API key # برچسب چینی
    placeholder: # جایگزین فیلد گواهی نامه
      en_US: Please input your SerpApi API key # جایگزین انگلیسی
      zh_Hans: 请输入你的 SerpApi API key # جایگزین چینی
    help: # متن راهنما فیلد گواهی نامه
      en_US: Get your SerpApi API key from SerpApi # متن راهنما انگلیسی
      zh_Hans: 从 SerpApi 获取您的 SerpApi API key # متن راهنما چینی
    url: https://serpapi.com/manage-api-key # لینک راهنما فیلد گواهی نامه

```

* `type`: نوع فیلد گواهی نامه، در حال حاضر می تواند `secret-input`, `text-input`, یا `select` باشد، که به ترتیب مربوط به کادر ورودی رمز عبور، کادر ورودی متن، و کادر انتخاب کشویی می شود. اگر به `secret-input` تنظیم شود، محتوای ورودی در فرانت اند مخفی می شود و بکند محتوای ورودی را رمزگذاری می کند.

### 3. آماده سازی فایل YAML ابزار

یک ارائه دهنده می تواند چندین ابزار داشته باشد، هر ابزار به یک فایل YAML برای توصیف نیاز دارد، این فایل اطلاعات پایه، پارامترها، خروجی، و غیره ابزار را شامل می شود.

با استفاده از GoogleSearch به عنوان مثال، باید یک ماژول `tools` زیر ماژول `google` ایجاد کنیم و `tools/google_search.yaml` را بسازیم، محتوای آن به شرح زیر است.

```yaml
identity: # اطلاعات پایه ابزار
  name: google_search # نام ابزار، منحصر به فرد، بدون تکرار با سایر ابزارها
  author: Dify # نویسنده
  label: # برچسب برای نمایش در فرانت اند
    en_US: GoogleSearch # برچسب انگلیسی
    zh_Hans: 谷歌搜索 # برچسب چینی
description: # توضیحات برای نمایش در فرانت اند
  human: # مقدمه برای نمایش در فرانت اند، از چندین زبان پشتیبانی می کند
    en_US: A tool for performing a Google SERP search and extracting snippets and webpages.Input should be a search query.
    zh_Hans: 一个用于执行 Google SERP 搜索并提取片段和网页的工具。输入应该是一个搜索查询。
  llm: A tool for performing a Google SERP search and extracting snippets and webpages.Input should be a search query. # مقدمه برای LLM، به منظور درک بهتر LLM از این ابزار، پیشنهاد می شود اطلاعات دقیق در مورد این ابزار را به طور کامل در اینجا بنویسید، تا LLM بتواند این ابزار را درک کند و از آن استفاده کند
parameters: # لیست پارامترها
  - name: query # نام پارامتر
    type: string # نوع پارامتر
    required: true # الزامی بودن یا نبودن
    label: # برچسب پارامتر
      en_US: Query string # برچسب انگلیسی
      zh_Hans: 查询语句 # برچسب چینی
    human_description: # مقدمه برای نمایش در فرانت اند، از چندین زبان پشتیبانی می کند
      en_US: used for searching
      zh_Hans: 用于搜索网页内容
    llm_description: key words for searching # مقدمه برای LLM، به طور مشابه، به منظور درک بهتر LLM از این پارامتر، پیشنهاد می شود اطلاعات دقیق در مورد این پارامتر را به طور کامل در اینجا بنویسید، تا LLM بتواند این پارامتر را درک کند
    form: llm # نوع فرم، llm به این معنی است که این پارامتر باید توسط Agent استنتاج شود، فرانت اند این پارامتر را نمایش نخواهد داد
  - name: result_type
    type: select # نوع پارامتر
    required: true
    options: # گزینه های کادر انتخاب کشویی
      - value: text
        label:
          en_US: text
          zh_Hans: 文本
      - value: link
        label:
          en_US: link
          zh_Hans: 链接
    default: link
    label:
      en_US: Result type
      zh_Hans: 结果类型
    human_description:
      en_US: used for selecting the result type, text or link
      zh_Hans: 用于选择结果类型，使用文本还是链接进行展示
    form: form # نوع فرم، form به این معنی است که این پارامتر باید توسط کاربر در فرانت اند قبل از شروع مکالمه پر شود

```

* فیلد `identity` الزامی است، این فیلد اطلاعات پایه ابزار را شامل می شود، از جمله نام، نویسنده، برچسب، توضیحات، و غیره.
* `parameters` لیست پارامترها
  * `name` نام پارامتر، منحصر به فرد، بدون تکرار با سایر پارامترها
  * `type` نوع پارامتر، در حال حاضر از `string`, `number`, `boolean`, `select` چهار نوع پشتیبانی می کند، که به ترتیب مربوط به رشته، عدد، بولی، کادر انتخاب کشویی می شود.
  * `required` الزامی بودن یا نبودن
    * در حالت `llm`، اگر پارامتر الزامی باشد، Agent ملزم به استنتاج این پارامتر است.
    * در حالت `form`، اگر پارامتر الزامی باشد، کاربر ملزم به پر کردن این پارامتر در فرانت اند قبل از شروع مکالمه است.
  * `options` گزینه های پارامتر
    * در حالت `llm`، Dify تمام گزینه ها را به LLM منتقل می کند، LLM می تواند بر اساس این گزینه ها استنتاج کند.
    * در حالت `form`، هنگامی که `type` برابر با `select` است، فرانت اند این گزینه ها را نمایش خواهد داد.
  * `default` مقدار پیش فرض
  * `label` برچسب پارامتر، برای نمایش در فرانت اند
  * `human_description` مقدمه برای نمایش در فرانت اند، از چندین زبان پشتیبانی می کند.
  * `llm_description` مقدمه برای LLM، به منظور درک بهتر LLM از این پارامتر، پیشنهاد می شود اطلاعات دقیق در مورد این پارامتر را به طور کامل در اینجا بنویسید، تا LLM بتواند این پارامتر را درک کند.
  * `form` نوع فرم، در حال حاضر از `llm`, `form` دو نوع پشتیبانی می کند، که به ترتیب مربوط به استنتاج خودکار Agent و پر کردن توسط فرانت اند می شود.

### 4. اضافه کردن منطق ابزار

پس از تکمیل پیکربندی ابزار، می توانیم شروع به نوشتن کد ابزار کنیم که نحوه فراخوانی آن را تعریف می کند.

`google_search.py` را در زیر ماژول `google/tools` ایجاد کنید، محتوای آن به شرح زیر است.

```python
from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage

from typing import Any, Dict, List, Union

class GoogleSearchTool(BuiltinTool):
    def _invoke(self, 
                user_id: str,
               tool_parameters: Dict[str, Any], 
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query = tool_parameters['query']
        result_type = tool_parameters['result_type']
        api_key = self.runtime.credentials['serpapi_api_key']
        # TODO: search with serpapi
        result = SerpAPI(api_key).run(query, result_type=result_type)

        if result_type == 'text':
            return self.create_text_message(text=result)
        return self.create_link_message(link=result)
```

#### پارامترها

منطق کلی ابزار در متد `_invoke` است، این متد دو پارامتر می پذیرد: `user_id` و `tool_parameters`، که به ترتیب نشان دهنده شناسه کاربر و پارامترهای ابزار هستند.

#### بازگرداندن داده ها

هنگامی که ابزار بازمی گردد، می توانید انتخاب کنید که یک پیام یا چند پیام را بازگردانید، در اینجا یک پیام را بازمی گردانیم، با استفاده از `create_text_message` و `create_link_message` می توان یک پیام متنی یا یک پیام پیوند ایجاد کرد.

### 5. اضافه کردن کد ارائه دهنده

در نهایت، باید یک کلاس ارائه دهنده را در زیر ماژول ارائه دهنده ایجاد کنیم تا منطق تأیید اعتبار ارائه دهنده را پیاده سازی کنیم. اگر تأیید اعتبار گواهی نامه با شکست مواجه شود، یک استثنا `ToolProviderCredentialValidationError` را پرتاب خواهد کرد.

`google.py` را در زیر ماژول `google` ایجاد کنید، محتوای آن به شرح زیر است.

```python
from core.tools.entities.tool_entities import ToolInvokeMessage, ToolProviderType
from core.tools.tool.tool import Tool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError

from core.tools.provider.builtin.google.tools.google_search import GoogleSearchTool

from typing import Any, Dict

class GoogleProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            # 1. در اینجا باید GoogleSearchTool را با GoogleSearchTool() نمونه سازی کنید، این عمل به طور خودکار پیکربندی YAML GoogleSearchTool را بارگیری می کند، اما در این زمان اطلاعات گواهی نامه در داخل آن وجود ندارد.
            # 2. سپس باید از متد fork_tool_runtime برای انتقال اطلاعات گواهی نامه فعلی به GoogleSearchTool استفاده کنید.
            # 3. در نهایت، آن را فراخوانی کنید، پارامترها باید با توجه به قوانین پارامتر پیکربندی شده در YAML GoogleSearchTool منتقل شوند.
            GoogleSearchTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "query": "test",
                    "result_type": "link"
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
```

### تکمیل

پس از تکمیل مراحل فوق، می توانیم این ابزار را در فرانت اند مشاهده کنیم و می توان آن را در Agent استفاده کرد.

البته، از آنجایی که google\_search به یک گواهی نامه نیاز دارد، قبل از استفاده از آن، باید گواهی نامه خود را در فرانت اند وارد کنید.

<figure><img src="../../.gitbook/assets/Feb 4, 2024 (1).png" alt=""><figcaption></figcaption></figure>
