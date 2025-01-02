# روش‌های رابط کاربری

این بخش روش‌های رابط کاربری و توضیحات پارامترها را شرح می‌دهد که باید توسط ارائه دهندگان و انواع مختلف مدل پیاده‌سازی شود.

## ارائه دهنده

کلاس پایه `__base.model_provider.ModelProvider` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

```python
def validate_provider_credentials(self, credentials: dict) -> None:
    """
    اعتبارنامه‌های ارائه دهنده را تأیید کنید
    شما می‌توانید هر روش validate_credentials از نوع مدل را انتخاب کنید یا روش تأیید را خودتان پیاده‌سازی کنید،
    مانند: دریافت API لیست مدل

    در صورت عدم تأیید، استثناء را ایجاد کنید

    :param credentials: اعتبارنامه‌های ارائه دهنده، فرم اعتبارنامه در `provider_credential_schema` تعریف شده است.
    """
```

- `credentials` (object) اطلاعات اعتبارنامه

  پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

در صورت شکست تأیید، خطای `errors.validate.CredentialsValidateFailedError` را ایجاد کنید.

## مدل

مدل‌ها به 5 نوع مختلف تقسیم می‌شوند که هر کدام از کلاس‌های پایه متفاوتی ارث می‌برند و نیاز به پیاده‌سازی روش‌های متفاوتی دارند.

همه مدل‌ها باید به طور یکسان دو روش زیر را پیاده‌سازی کنند:

- تأیید اعتبارنامه مدل

  مشابه تأیید اعتبارنامه ارائه دهنده، این مرحله شامل تأیید برای یک مدل خاص است.


  ```python
  def validate_credentials(self, model: str, credentials: dict) -> None:
      """
      اعتبارنامه‌های مدل را تأیید کنید
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :return:
      """
  ```

  پارامترها:

  - `model` (string) نام مدل

  - `credentials` (object) اطلاعات اعتبارنامه

    پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

  در صورت شکست تأیید، خطای `errors.validate.CredentialsValidateFailedError` را ایجاد کنید.

- جدول نگاشت خطای فراخوانی

  هنگامی که در فراخوانی مدل استثنا وجود دارد، باید به نوع `InvokeError` مشخص شده توسط Runtime نگاشت شود. این امر به Dify اجازه می‌دهد تا خطاهای مختلف را با اقدامات بعدی مناسب مدیریت کند.

  خطاهای Runtime:

  - `InvokeConnectionError` خطای اتصال فراخوانی
  - `InvokeServerUnavailableError` ارائه دهنده سرویس فراخوانی در دسترس نیست
  - `InvokeRateLimitError` فراخوانی به محدودیت نرخ رسید
  - `InvokeAuthorizationError`  فراخوانی مجوز ناموفق بود
  - `InvokeBadRequestError`  فراخوانی پارامتر خطا

  ```python
  @property
  def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
      """
      خطای فراخوانی مدل را به خطای یکپارچه نگاشت کنید
      کلید نوع خطای پرتاب شده به فراخوانی کننده است
      مقدار نوع خطای پرتاب شده توسط مدل است،
      که باید به نوع خطای یکپارچه برای فراخوانی کننده تبدیل شود.
  
      :return: نگاشت خطای فراخوانی
      """
  ```

​	می‌توانید به `_invoke_error_mapping` OpenAI برای مثال مراجعه کنید.

### LLM

کلاس پایه `__base.large_language_model.LargeLanguageModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی LLM

  روش اصلی برای فراخوانی LLM را پیاده‌سازی کنید، که می‌تواند هر دو بازگشت جریان و همگام را پشتیبانی کند.


  ```python
  def _invoke(self, model: str, credentials: dict,
              prompt_messages: list[PromptMessage], model_parameters: dict,
              tools: Optional[list[PromptMessageTool]] = None, stop: Optional[List[str]] = None,
              stream: bool = True, user: Optional[str] = None) \
          -> Union[LLMResult, Generator]:
      """
      فراخوانی مدل زبان بزرگ
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param prompt_messages: پیام‌های تقاضا
      :param model_parameters: پارامترهای مدل
      :param tools: ابزارها برای فراخوانی ابزار
      :param stop: کلمات توقف
      :param stream: آیا جریان پاسخ است
      :param user: شناسه کاربری منحصر به فرد
      :return: پاسخ کامل یا نتیجه مولد تکه پاسخ جریان
      """
  ```

  - پارامترها:

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `prompt_messages` (array[[PromptMessage](#PromptMessage)]) لیست تقاضاها

      اگر مدل از نوع `Completion` باشد، لیست فقط باید شامل یک عنصر [UserPromptMessage](#UserPromptMessage) باشد.

      اگر مدل از نوع `Chat` باشد، به لیستی از عناصر مانند [SystemPromptMessage](#SystemPromptMessage)، [UserPromptMessage](#UserPromptMessage)، [AssistantPromptMessage](#AssistantPromptMessage)، [ToolPromptMessage](#ToolPromptMessage) بسته به پیام نیاز دارد.

    - `model_parameters` (object) پارامترهای مدل

      پارامترهای مدل توسط `parameter_rules` در پیکربندی YAML مدل تعریف شده‌اند.

    - `tools` (array[[PromptMessageTool](#PromptMessageTool)]) [optional] لیست ابزار، معادل `function` در `function calling`.

      یعنی لیست ابزار برای فراخوانی ابزار.

    - `stop` (array[string]) [optional] دنباله‌های توقف

      خروجی مدل قبل از رشته‌ای که توسط دنباله توقف تعریف شده است، متوقف خواهد شد.

    - `stream` (bool) آیا به صورت جریان خروجی تولید شود، پیش فرض True است

      خروجی جریان Generator[[LLMResultChunk](#LLMResultChunk)] را برمی‌گرداند، خروجی غیر جریان [LLMResult](#LLMResult) را برمی‌گرداند.

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها

    خروجی جریان Generator[[LLMResultChunk](#LLMResultChunk)] را برمی‌گرداند، خروجی غیر جریان [LLMResult](#LLMResult) را برمی‌گرداند.

- پیش محاسبه توکن‌های ورودی

  اگر مدل رابط توکن‌های پیش محاسبه شده را ارائه نمی‌دهد، می‌توانید مستقیماً 0 را برگردانید.

  ```python
  def get_num_tokens(self, model: str, credentials: dict, prompt_messages: list[PromptMessage],
                     tools: Optional[list[PromptMessageTool]] = None) -> int:
      """
      تعداد توکن‌ها را برای پیام‌های تقاضای داده شده دریافت کنید

      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param prompt_messages: پیام‌های تقاضا
      :param tools: ابزارها برای فراخوانی ابزار
      :return:
      """
  ```

  برای توضیحات پارامتر، به بخش بالا در مورد `فراخوانی LLM` مراجعه کنید.

- دریافت طرح مدل سفارشی [اختیاری]

  ```python
  def get_customizable_model_schema(self, model: str, credentials: dict) -> Optional[AIModelEntity]:
      """
      طرح مدل قابل تنظیم را دریافت کنید

      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :return: طرح مدل
      """
  ```

  هنگامی که ارائه دهنده از اضافه کردن LLMهای سفارشی پشتیبانی می‌کند، می‌توان این روش را برای اجازه دادن به مدل‌های سفارشی برای دریافت طرح مدل پیاده‌سازی کرد. بازگشت پیش فرض null است.


### TextEmbedding

کلاس پایه `__base.text_embedding_model.TextEmbeddingModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی تعبیه

  ```python
  def _invoke(self, model: str, credentials: dict,
              texts: list[str], user: Optional[str] = None) \
          -> TextEmbeddingResult:
      """
      فراخوانی مدل زبان بزرگ
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param texts: متن‌هایی که باید تعبیه شوند
      :param user: شناسه کاربری منحصر به فرد
      :return: نتایج تعبیه
      """
  ```

  - پارامترها:

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `texts` (array[string]) لیست متن‌ها، قادر به پردازش دسته ای

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها:

    موجودیت [TextEmbeddingResult](#TextEmbeddingResult).

- پیش محاسبه توکن‌ها

  ```python
  def get_num_tokens(self, model: str, credentials: dict, texts: list[str]) -> int:
      """
      تعداد توکن‌ها را برای پیام‌های تقاضای داده شده دریافت کنید

      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param texts: متن‌هایی که باید تعبیه شوند
      :return:
      """
  ```

  برای توضیحات پارامتر، به بخش بالا در مورد `فراخوانی تعبیه` مراجعه کنید.

### Rerank

کلاس پایه `__base.rerank_model.RerankModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی Rerank

  ```python
  def _invoke(self, model: str, credentials: dict,
              query: str, docs: list[str], score_threshold: Optional[float] = None, top_n: Optional[int] = None,
              user: Optional[str] = None) \
          -> RerankResult:
      """
      فراخوانی مدل Rerank
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param query: جستجوی پرس و جو
      :param docs: اسناد برای Reranking
      :param score_threshold: آستانه نمره
      :param top_n: top n
      :param user: شناسه کاربری منحصر به فرد
      :return: نتیجه Rerank
      """
  ```

  - پارامترها:

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `query` (string) محتوای درخواست پرس و جو

    - `docs` (array[string]) لیست بخش‌هایی که باید Rerank شوند

    - `score_threshold` (float) [optional] آستانه نمره

    - `top_n` (int) [optional] انتخاب top n بخش‌ها

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها:

    موجودیت [RerankResult](#RerankResult).

### Speech2text

کلاس پایه `__base.speech2text_model.Speech2TextModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی Invoke

  ```python
  def _invoke(self, model: str, credentials: dict, file: IO[bytes], user: Optional[str] = None) -> str:
      """
      فراخوانی مدل زبان بزرگ
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param file: فایل صوتی
      :param user: شناسه کاربری منحصر به فرد
      :return: متن برای فایل صوتی داده شده
      """	
  ```

  - پارامترها:

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `file` (File) جریان فایل

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها:

    رشته‌ای که بعد از تبدیل گفتار به متن است.

### Text2speech

کلاس پایه `__base.text2speech_model.Text2SpeechModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی Invoke

  ```python
  def _invoke(self, model: str, credentials: dict, content_text: str, streaming: bool, user: Optional[str] = None):
      """
      فراخوانی مدل زبان بزرگ
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param content_text: محتوای متنی که باید ترجمه شود
      :param streaming: خروجی جریان است
      :param user: شناسه کاربری منحصر به فرد
      :return: فایل صوتی ترجمه شده
      """	
  ```

  - پارامترها：

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `content_text` (string) محتوای متنی که باید تبدیل شود

    - `streaming` (bool) آیا به صورت جریان خروجی تولید شود

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها：

    جریان گفتار تبدیل شده از متن。

### Moderation

کلاس پایه `__base.moderation_model.ModerationModel` را به ارث ببرید و رابط‌های زیر را پیاده‌سازی کنید:

- فراخوانی Invoke

  ```python
  def _invoke(self, model: str, credentials: dict,
              text: str, user: Optional[str] = None) \
          -> bool:
      """
      فراخوانی مدل زبان بزرگ
  
      :param model: نام مدل
      :param credentials: اعتبارنامه‌های مدل
      :param text: متن برای نظارت
      :param user: شناسه کاربری منحصر به فرد
      :return: false اگر متن امن باشد، در غیر این صورت true
      """
  ```

  - پارامترها:

    - `model` (string) نام مدل

    - `credentials` (object) اطلاعات اعتبارنامه

      پارامترهای اطلاعات اعتبارنامه توسط `provider_credential_schema` یا `model_credential_schema` در فایل پیکربندی YAML ارائه دهنده تعریف شده‌اند. ورودی‌هایی مانند `api_key`  شامل می‌شوند.

    - `text` (string) محتوای متن

    - `user` (string) [optional] شناسه منحصر به فرد کاربر

      این می‌تواند به ارائه دهنده کمک کند تا رفتارهای سوء استفاده را کنترل و تشخیص دهد.

  - بازگشت‌ها:

    False نشان می‌دهد که متن ورودی امن است، True نشان می‌دهد که این طور نیست.



## موجودیت‌ها

### PromptMessageRole 

نقش پیام تقاضا

```python
class PromptMessageRole(Enum):
    """
    کلاس Enum برای پیام تقاضا.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
```

### PromptMessageContentType

انواع محتوای پیام تقاضا، به متن و تصویر تقسیم شده است.

```python
class PromptMessageContentType(Enum):
    """
    کلاس Enum برای نوع محتوای پیام تقاضا.
    """
    TEXT = 'text'
    IMAGE = 'image'
```

### PromptMessageContent

کلاس پایه محتوای پیام تقاضا، فقط برای اعلام پارامتر استفاده می‌شود و نمی‌توان آن را مقداردهی اولیه کرد.

```python
class PromptMessageContent(BaseModel):
    """
    کلاس مدل برای محتوای پیام تقاضا.
    """
    type: PromptMessageContentType
    data: str
```

در حال حاضر، دو نوع پشتیبانی می‌شوند: متن و تصویر. امکان ورودی همزمان متن و چندین تصویر وجود دارد.

برای ورودی، باید `TextPromptMessageContent` و `ImagePromptMessageContent` را به طور جداگانه مقداردهی اولیه کنید.

### TextPromptMessageContent

```python
class TextPromptMessageContent(PromptMessageContent):
    """
    کلاس مدل برای محتوای پیام تقاضای متن.
    """
    type: PromptMessageContentType = PromptMessageContentType.TEXT
```

اگر ترکیبی از متن و تصاویر را وارد می‌کنید، متن باید به عنوان بخشی از لیست `content` به این موجودیت ساخته شود.

### ImagePromptMessageContent

```python
class ImagePromptMessageContent(PromptMessageContent):
    """
    کلاس مدل برای محتوای پیام تقاضای تصویر.
    """
    class DETAIL(Enum):
        LOW = 'low'
        HIGH = 'high'

    type: PromptMessageContentType = PromptMessageContentType.IMAGE
    detail: DETAIL = DETAIL.LOW  # رزولوشن
```

اگر ترکیبی از متن و تصاویر را وارد می‌کنید، تصاویر باید به عنوان بخشی از لیست `content` به این موجودیت ساخته شوند.

`data` می‌تواند یک `url` یا یک رشته کدگذاری شده `base64` از تصویر باشد.

### PromptMessage

کلاس پایه برای همه بدنه‌های پیام نقش، فقط برای اعلام پارامتر استفاده می‌شود و نمی‌توان آن را مقداردهی اولیه کرد.

```python
class PromptMessage(ABC, BaseModel):
    """
    کلاس مدل برای پیام تقاضا.
    """
    role: PromptMessageRole
    content: Optional[str | list[PromptMessageContent]] = None  # دو نوع را پشتیبانی می‌کند: رشته و لیست محتوا. لیست محتوا برای پاسخگویی به نیازهای ورودی‌های چندوجهی طراحی شده است. برای اطلاعات بیشتر، به توضیحات PromptMessageContent مراجعه کنید.
    name: Optional[str] = None
```

### UserPromptMessage

بدنه پیام UserMessage، نشان دهنده پیام یک کاربر است.

```python
class UserPromptMessage(PromptMessage):
    """
    کلاس مدل برای پیام تقاضای کاربر.
    """
    role: PromptMessageRole = PromptMessageRole.USER
```

### AssistantPromptMessage

نمایشگر پیامی که توسط مدل برگردانده شده است، معمولاً برای `few-shots` یا وارد کردن تاریخچه چت استفاده می‌شود.

```python
class AssistantPromptMessage(PromptMessage):
    """
    کلاس مدل برای پیام تقاضای دستیار.
    """
    class ToolCall(BaseModel):
        """
        کلاس مدل برای فراخوانی ابزار پیام تقاضای دستیار.
        """
        class ToolCallFunction(BaseModel):
            """
            کلاس مدل برای تابع فراخوانی ابزار پیام تقاضای دستیار.
            """
            name: str  # نام ابزار
            arguments: str  # استدلال‌های ابزار

        id: str  # شناسه ابزار، فقط در فراخوانی‌های ابزار OpenAI مؤثر است. این شناسه منحصر به فرد برای فراخوانی ابزار است و یک ابزار می‌تواند چندین بار فراخوانی شود.
        type: str  # پیش فرض: function
        function: ToolCallFunction  # اطلاعات فراخوانی ابزار

    role: PromptMessageRole = PromptMessageRole.ASSISTANT
    tool_calls: list[ToolCall] = []  # نتیجه فراخوانی ابزار در پاسخ از مدل (فقط در هنگام ورودی ابزارها و زمانی که مدل آن را برای فراخوانی ابزار لازم می‌داند، برگردانده می‌شود).
```

که در آن `tool_calls` لیست `فراخوانی‌های ابزار` برگردانده شده توسط مدل بعد از فراخوانی مدل با ورودی `tools` است.

### SystemPromptMessage

نمایشگر پیام‌های سیستم، معمولاً برای تنظیم دستورات سیستم داده شده به مدل استفاده می‌شود.

```python
class SystemPromptMessage(PromptMessage):
    """
    کلاس مدل برای پیام تقاضای سیستم.
    """
    role: PromptMessageRole = PromptMessageRole.SYSTEM
```

### ToolPromptMessage

نمایشگر پیام‌های ابزار، برای انتقال نتایج اجرای یک ابزار به مدل برای مرحله بعدی پردازش استفاده می‌شود.

```python
class ToolPromptMessage(PromptMessage):
    """
    کلاس مدل برای پیام تقاضای ابزار.
    """
    role: PromptMessageRole = PromptMessageRole.TOOL
    tool_call_id: str  # شناسه فراخوانی ابزار. اگر فراخوانی ابزار OpenAI پشتیبانی نشود، نام ابزار نیز می‌تواند وارد شود.
```

`content` کلاس پایه نتایج اجرای ابزار را دریافت می‌کند.

### PromptMessageTool

```python
class PromptMessageTool(BaseModel):
    """
    کلاس مدل برای ابزار پیام تقاضا.
    """
    name: str
    description: str
    parameters: dict
```

---

### LLMResult

```python
class LLMResult(BaseModel):
    """
    کلاس مدل برای نتیجه LLM.
    """
    model: str  # مدل واقعی استفاده شده
    prompt_messages: list[PromptMessage]  # پیام‌های تقاضا
    message: AssistantPromptMessage  # پیام پاسخ
    usage: LLMUsage  # اطلاعات استفاده
    system_fingerprint: Optional[str] = None  # اثر انگشت درخواست، به تعریف OpenAI مراجعه کنید
```

### LLMResultChunkDelta

در بازگشت‌های جریان، هر تکرار شامل موجودیت `delta` است.

```python
class LLMResultChunkDelta(BaseModel):
    """
    کلاس مدل برای delta تکه نتیجه LLM.
    """
    index: int
    message: AssistantPromptMessage  # پیام پاسخ
    usage: Optional[LLMUsage] = None  # اطلاعات استفاده
    finish_reason: Optional[str] = None  # دلیل اتمام، فقط آخرین مورد بازگردانده می‌شود
```

### LLMResultChunk

هر موجودیت تکرار در بازگشت‌های جریان.

```python
class LLMResultChunk(BaseModel):
    """
    کلاس مدل برای تکه نتیجه LLM.
    """
    model: str  # مدل واقعی استفاده شده
    prompt_messages: list[PromptMessage]  # پیام‌های تقاضا
    system_fingerprint: Optional[str] = None  # اثر انگشت درخواست، به تعریف OpenAI مراجعه کنید
    delta: LLMResultChunkDelta
```

### LLMUsage

```python
class LLMUsage(ModelUsage):
    """
    کلاس مدل برای استفاده LLM.
    """
    prompt_tokens: int  # توکن‌های استفاده شده برای تقاضا
    prompt_unit_price: Decimal  # قیمت واحد برای تقاضا
    prompt_price_unit: Decimal  # واحد قیمت برای تقاضا، یعنی قیمت واحد بر اساس تعداد توکن‌ها
    prompt_price: Decimal  # هزینه تقاضا
    completion_tokens: int  # توکن‌های استفاده شده برای پاسخ
    completion_unit_price: Decimal  # قیمت واحد برای پاسخ
    completion_price_unit: Decimal  # واحد قیمت برای پاسخ، یعنی قیمت واحد بر اساس تعداد توکن‌ها
    completion_price: Decimal  # هزینه پاسخ
    total_tokens: int  # تعداد کل توکن‌های استفاده شده
    total_price: Decimal  # هزینه کل
    currency: str  # واحد پول
    latency: float  # تأخیر درخواست (ثانیه)
```

---

### TextEmbeddingResult

```python
class TextEmbeddingResult(BaseModel):
    """
    کلاس مدل برای نتیجه تعبیه متن.
    """
    model: str  # مدل واقعی استفاده شده
    embeddings: list[list[float]]  # لیست بردارهای تعبیه، مطابق با لیست متن‌های ورودی
    usage: EmbeddingUsage  # اطلاعات استفاده
```

### EmbeddingUsage

```python
class EmbeddingUsage(ModelUsage):
    """
    کلاس مدل برای استفاده تعبیه.
    """
    tokens: int  # تعداد توکن‌های استفاده شده
    total_tokens: int  # تعداد کل توکن‌های استفاده شده
    unit_price: Decimal  # قیمت واحد
    price_unit: Decimal  # واحد قیمت، یعنی قیمت واحد بر اساس تعداد توکن‌ها
    total_price: Decimal  # هزینه کل
    currency: str  # واحد پول
    latency: float  # تأخیر درخواست (ثانیه)
```

---

### RerankResult

```python
class RerankResult(BaseModel):
    """
    کلاس مدل برای نتیجه Rerank.
    """
    model: str  # مدل واقعی استفاده شده
    docs: list[RerankDocument]  # لیست اسناد Rerank شده	
```

### RerankDocument

```python
class RerankDocument(BaseModel):
    """
    کلاس مدل برای سند Rerank.
    """
    index: int  # شاخص اصلی
    text: str
    score: float
```


