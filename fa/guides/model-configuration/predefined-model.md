# ادغام مدل از پیش تعریف شده

پس از اتمام ادغام تأمین‌کننده، مرحله بعدی ادغام مدل‌ها در زیر تأمین‌کننده است.

ابتدا باید نوع مدل مورد ادغام را تعیین کرده و ماژول مربوطه به نوع مدل را در دایرکتوری تأمین‌کننده مربوطه ایجاد کنیم.

نوع مدل‌های پشتیبانی شده در حال حاضر به شرح زیر است:

* `llm` مدل تولید متن
* `text_embedding` مدل Embedding متن
* `rerank` مدل  Rerank
* `speech2text` تبدیل گفتار به متن
* `tts` تبدیل متن به گفتار
* `moderation` تعدیل

با استفاده از `Anthropic` به عنوان مثال، `Anthropic` فقط از LLM پشتیبانی می‌کند، بنابراین ما یک ماژول به نام `llm` در `model_providers.anthropic` ایجاد می‌کنیم.

برای مدل‌های از پیش تعریف شده، ابتدا باید یک فایل YAML با نام مدل را در ماژول `llm` ایجاد کنیم، مانند: `claude-2.1.yaml`.

#### آماده سازی فایل YAML مدل

```yaml
model: claude-2.1  # شناسه مدل
# نام نمایش مدل، می تواند در انگلیسی `en_US` و چینی `zh_Hans` تنظیم شود. اگر `zh_Hans` تنظیم نشود، به صورت پیش‌فرض از `en_US` استفاده خواهد شد.
# همچنین می‌توانید برچسبی تنظیم نکنید، در این صورت از شناسه مدل استفاده خواهد شد.
label:
  en_US: claude-2.1
model_type: llm  # نوع مدل، claude-2.1 یک LLM است
features:  # ویژگی‌های پشتیبانی شده، agent-thought از استدلال Agent پشتیبانی می‌کند، vision از درک تصویر پشتیبانی می‌کند
- agent-thought
model_properties:  # ویژگی‌های مدل
  mode: chat  # حالت LLM، complete برای مدل تکمیل متن، chat برای مدل گفتگو
  context_size: 200000  # حداکثر اندازه زمینه پشتیبانی شده
parameter_rules:  # قوانین پارامترهای فراخوانی مدل، فقط LLM باید این موارد را ارائه دهد
- name: temperature  # نام متغیر پارامتر فراخوانی
  # 5 الگوی تنظیم محتوای متغیر پیش‌فرض وجود دارد: temperature/top_p/max_tokens/presence_penalty/frequency_penalty
  # می توانید مستقیماً نام متغیر الگو را در use_template تنظیم کنید، و از پیکربندی پیش‌فرض در entities.defaults.PARAMETER_RULE_TEMPLATE استفاده خواهد شد.
  # اگر پارامترهای پیکربندی اضافی تنظیم شوند، بر روی پیکربندی پیش‌فرض غلبه خواهند کرد.
  use_template: temperature
- name: top_p
  use_template: top_p
- name: top_k
  label:  # نام نمایش پارامتر فراخوانی
    zh_Hans: 取样数量
    en_US: Top k
  type: int  # نوع پارامتر، از float/int/string/boolean پشتیبانی می‌کند.
  help:  # اطلاعات راهنما، عملکرد پارامتر را شرح می‌دهد.
    zh_Hans: 仅从 هر بعدی بعدی علامت گذاری در بین انتخاب‌های K برتر انتخاب کنید.
    en_US: Only sample from the top K options for each subsequent token.
  required: false  # اینکه آیا الزامی است، قابل حذف است.
- name: max_tokens_to_sample
  use_template: max_tokens
  default: 4096  # مقدار پیش‌فرض پارامتر
  min: 1  # حداقل مقدار پارامتر، فقط برای float/int قابل استفاده است.
  max: 4096  # حداکثر مقدار پارامتر، فقط برای float/int قابل استفاده است.
pricing:  # اطلاعات قیمت‌گذاری
  input: '8.00'  # قیمت واحد ورودی، به عنوان مثال، قیمت واحد Prompt
  output: '24.00'  # قیمت واحد خروجی، به عنوان مثال، قیمت واحد بازگشت محتوا
  unit: '0.000001'  # واحد قیمت، قیمت بالا به ازای هر 100K است.
  currency: USD  # واحد پول قیمت
```

توصیه می‌شود تمام پیکربندی‌های مدل را قبل از شروع پیاده‌سازی کد مدل آماده کنید.

به طور مشابه، می‌توانید به اطلاعات پیکربندی YAML در دایرکتوری‌های تأمین‌کنندگان دیگر در دایرکتوری `model_providers` مراجعه کنید. قوانین کامل YAML را می‌توان در: Schema[^1] یافت.

#### پیاده‌سازی کد فراخوانی مدل

در مرحله بعد، یک فایل Python با همان نام `llm.py` را در ماژول `llm` برای نوشتن کد پیاده‌سازی ایجاد کنید.

یک کلاس Anthropic LLM را در `llm.py` ایجاد کنید، که ما آن را `AnthropicLargeLanguageModel` (نام می‌تواند دلخواه باشد) می‌نامیم، که از کلاس پایه `__base.large_language_model.LargeLanguageModel` ارث‌بری می‌کند، و روش‌های زیر را پیاده‌سازی می‌کند:

*   فراخوانی LLM

    روش اصلی را برای فراخوانی LLM پیاده‌سازی کنید، که از پاسخ‌های همزمان و Streaming پشتیبانی می‌کند.

    ```python
    def _invoke(self, model: str, credentials: dict,
                prompt_messages: list[PromptMessage], model_parameters: dict,
                tools: Optional[list[PromptMessageTool]] = None, stop: Optional[List[str]] = None,
                stream: bool = True, user: Optional[str] = None) \
            -> Union[LLMResult, Generator]:
        """
        فراخوانی مدل زبان بزرگ

        :param model: نام مدل
        :param credentials: اعتبارنامه مدل
        :param prompt_messages: پیام‌های Prompt
        :param model_parameters: پارامترهای مدل
        :param tools: ابزارها برای فراخوانی ابزار
        :param stop: کلمات توقف
        :param stream: آیا پاسخ Streaming است
        :param user: شناسه کاربری منحصر به فرد
        :return: پاسخ کامل یا نتیجه مولد قطعه پاسخ Streaming
        """
    ```

    هنگام پیاده‌سازی، توجه داشته باشید که از دو تابع برای بازگرداندن داده‌ها استفاده کنید، یکی برای رسیدگی به پاسخ‌های همزمان و دیگری برای پاسخ‌های Streaming. از آنجایی که پایتون توابع حاوی کلمه کلیدی `yield` را به عنوان توابع مولد تشخیص می‌دهد، بازگرداندن یک نوع داده ثابت `Generator`، پاسخ‌های همزمان و Streaming باید به طور جداگانه پیاده‌سازی شوند، مانند این (توجه داشته باشید که مثال زیر از پارامترهای ساده‌شده استفاده می‌کند، پیاده‌سازی واقعی باید از لیست پارامتر بالا پیروی کند):

    ```python
    def _invoke(self, stream: bool, **kwargs) \
            -> Union[LLMResult, Generator]:
        if stream:
              return self._handle_stream_response(**kwargs)
        return self._handle_sync_response(**kwargs)

    def _handle_stream_response(self, **kwargs) -> Generator:
        for chunk in response:
              yield chunk
    def _handle_sync_response(self, **kwargs) -> LLMResult:
        return LLMResult(**response)
    ```
*   محاسبه قبلی توکن‌های ورودی

    اگر مدل رابط محاسبه قبلی توکن را ارائه نمی‌دهد، 0 را مستقیماً بازگردانید.

    ```python
    def get_num_tokens(self, model: str, credentials: dict, prompt_messages: list[PromptMessage],
                       tools: Optional[list[PromptMessageTool]] = None) -> int:
        """
        تعداد توکن‌ها را برای پیام‌های Prompt مشخص شده دریافت کنید

        :param model: نام مدل
        :param credentials: اعتبارنامه مدل
        :param prompt_messages: پیام‌های Prompt
        :param tools: ابزارها برای فراخوانی ابزار
        :return:
        """
    ```
*   اعتبارسنجی اعتبارنامه مدل

    مشابه اعتبارسنجی اعتبارنامه تأمین‌کننده، این اعتبارنامه‌ها را برای یک مدل واحد اعتبارسنجی می‌کند.

    ```python
    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        اعتبارسنجی اعتبارنامه مدل

        :param model: نام مدل
        :param credentials: اعتبارنامه مدل
        :return:
        """
    ```
*   جدول نگاشت خطای فراخوانی

    هنگامی که خطای فراخوانی مدل رخ می‌دهد، باید به نوع `InvokeError` مشخص شده توسط Runtime نگاشت شود، که به Dify کمک می‌کند تا خطاهای مختلف را به طور متفاوتی اداره کند.

    خطاهای Runtime:

    * `InvokeConnectionError` خطای اتصال فراخوانی
    * `InvokeServerUnavailableError` سرویس فراخوانی در دسترس نیست
    * `InvokeRateLimitError` محدودیت سرعت فراخوانی به پایان رسید
    * `InvokeAuthorizationError` مجوز فراخوانی با شکست مواجه شد
    * `InvokeBadRequestError` خطای پارامتر فراخوانی

    ```python
    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        """
        خطای فراخوانی مدل را به خطای یکسان نگاشت کنید
        کلید نوع خطایی است که به فراخوانی کننده پرتاب می‌شود
        مقدار نوع خطایی است که توسط مدل پرتاب می‌شود،
        که باید به یک نوع خطای یکسان برای فراخوانی کننده تبدیل شود.

        :return: نگاشت خطای فراخوانی
        """
    ```

    برای توضیحات روش رابط، به: [Interfaces](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/docs/en_US/interfaces.md) مراجعه کنید، و برای پیاده‌سازی خاص، به: [llm.py](https://github.com/langgenius/dify-runtime/blob/main/lib/model_providers/anthropic/llm/llm.py) مراجعه کنید.

[^1]: #### Provider

    * `provider` (string) شناسه تأمین‌کننده، به عنوان مثال، `openai`
    * `label` (object) نام نمایش تأمین‌کننده، i18n، می‌تواند در `en_US` انگلیسی و `zh_Hans` چینی تنظیم شود
      * `zh_Hans` (string) [optional] نام برچسب چینی، اگر `zh_Hans` تنظیم نشود، به صورت پیش‌فرض از `en_US` استفاده خواهد شد.
      * `en_US` (string) نام برچسب انگلیسی
    * `description` (object) [optional] توضیحات تأمین‌کننده، i18n
      * `zh_Hans` (string) [optional] توضیحات چینی
      * `en_US` (string) توضیحات انگلیسی
    * `icon_small` (string) [optional] آیکون کوچک تأمین‌کننده، در دایرکتوری `_assets` در زیر دایرکتوری پیاده‌سازی تأمین‌کننده مربوطه ذخیره شده است، از همان استراتژی زبان `label` پیروی می‌کند
      * `zh_Hans` (string) [optional] آیکون چینی
      * `en_US` (string) آیکون انگلیسی
    * `icon_large` (string) [optional] آیکون بزرگ تأمین‌کننده، در دایرکتوری `_assets` در زیر دایرکتوری پیاده‌سازی تأمین‌کننده مربوطه ذخیره شده است، از همان استراتژی زبان `label` پیروی می‌کند
      * `zh_Hans` (string) [optional] آیکون چینی
      * `en_US` (string) آیکون انگلیسی
    * `background` (string) [optional] مقدار رنگ پس‌زمینه، به عنوان مثال، #FFFFFF، اگر خالی باشد، مقدار رنگ پیش‌فرض در رابط کاربری نمایش داده خواهد شد.
    * `help` (object) [optional] اطلاعات راهنما
      * `title` (object) عنوان راهنما، i18n
        * `zh_Hans` (string) [optional] عنوان چینی
        * `en_US` (string) عنوان انگلیسی
      * `url` (object) لینک راهنما، i18n
        * `zh_Hans` (string) [optional] لینک چینی
        * `en_US` (string) لینک انگلیسی
    * `supported_model_types` (array[ModelType]) نوع مدل‌های پشتیبانی شده
    * `configurate_methods` (array[ConfigurateMethod]) روش‌های پیکربندی
    * `provider_credential_schema` (ProviderCredentialSchema) طرح اعتبارنامه تأمین‌کننده
    * `model_credential_schema` (ModelCredentialSchema) طرح اعتبارنامه مدل
