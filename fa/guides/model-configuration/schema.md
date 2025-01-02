# قوانین پیکربندی

- قوانین ارائه دهنده بر اساس موجودیت  [ارائه دهنده](#ارائه دهنده) است.
- قوانین مدل بر اساس موجودیت  [AIModelEntity](#AIModelEntity) است.

> تمام موجودیت های ذکر شده در زیر بر اساس  `Pydantic BaseModel` هستند و می توان آنها را در ماژول `entities` یافت.

### ارائه دهنده

- `provider` (string) شناسه ارائه دهنده، مانند `openai`
- `label` (object) نام نمایش ارائه دهنده، i18n، با تنظیمات زبان انگلیسی `en_US` و چینی `zh_Hans`
  - `zh_Hans` (string) [optional] نام برچسب چینی، در صورت عدم تنظیم `zh_Hans`، `en_US` به طور پیش فرض استفاده می شود.
  - `en_US` (string) نام برچسب انگلیسی
- `description` (object) توضیحات ارائه دهنده، i18n
  - `zh_Hans` (string) [optional] توضیحات چینی
  - `en_US` (string) توضیحات انگلیسی
- `icon_small` (string) [optional] نماد کوچک ارائه دهنده، ذخیره شده در فهرست `_assets` در فهرست پیاده سازی ارائه دهنده مربوطه، با همان استراتژی زبان `label`
  - `zh_Hans` (string) نماد چینی
  - `en_US` (string) نماد انگلیسی
- `icon_large` (string) [optional] نماد بزرگ ارائه دهنده، ذخیره شده در فهرست `_assets` در فهرست پیاده سازی ارائه دهنده مربوطه، با همان استراتژی زبان `label`
  - `zh_Hans` (string) نماد چینی
  - `en_US` (string) نماد انگلیسی
- `background` (string) [optional] مقدار رنگ پس زمینه، مانند #FFFFFF، اگر خالی باشد، مقدار رنگ پیش فرض فرانت اند نمایش داده می شود.
- `help` (object) [optional] اطلاعات راهنما
  - `title` (object) عنوان راهنما، i18n
    - `zh_Hans` (string) [optional] عنوان چینی
    - `en_US` (string) عنوان انگلیسی
  - `url` (object) پیوند راهنما، i18n
    - `zh_Hans` (string) [optional] پیوند چینی
    - `en_US` (string) پیوند انگلیسی
- `supported_model_types` (array[[ModelType](#ModelType)]) انواع مدل پشتیبانی شده
- `configurate_methods` (array[[ConfigurateMethod](#ConfigurateMethod)]) روش های پیکربندی
- `provider_credential_schema` ([ProviderCredentialSchema](#ProviderCredentialSchema)) مشخصات اعتبار ارائه دهنده
- `model_credential_schema` ([ModelCredentialSchema](#ModelCredentialSchema)) مشخصات اعتبار مدل

### AIModelEntity

- `model` (string) شناسه مدل، مانند `gpt-3.5-turbo`
- `label` (object) [optional] نام نمایش مدل، i18n، با تنظیمات زبان انگلیسی `en_US` و چینی `zh_Hans`
  - `zh_Hans` (string) [optional] نام برچسب چینی
  - `en_US` (string) نام برچسب انگلیسی
- `model_type` ([ModelType](#ModelType)) نوع مدل
- `features` (array[[ModelFeature](#ModelFeature)]) [optional] فهرست ویژگی پشتیبانی شده
- `model_properties` (object) ویژگی های مدل
  - `mode` ([LLMMode](#LLMMode)) حالت (برای نوع مدل `llm` در دسترس است)
  - `context_size` (int) اندازه زمینه (برای انواع مدل `llm`، `text-embedding` در دسترس است)
  - `max_chunks` (int) حداکثر تعداد بخش (برای انواع مدل `text-embedding`، `moderation` در دسترس است)
  - `file_upload_limit` (int) حداکثر حد مجاز آپلود فایل، بر حسب مگابایت (برای نوع مدل `speech2text` در دسترس است)
  - `supported_file_extensions` (string) فرمت های پسوند فایل پشتیبانی شده، مانند mp3، mp4 (برای نوع مدل `speech2text` در دسترس است)
  - `default_voice` (string)  صدای پیش فرض، مانند: alloy,echo,fable,onyx,nova,shimmer（برای نوع مدل `tts` در دسترس است）
  - `voices` (list)  فهرست صدای در دسترس.（برای نوع مدل `tts` در دسترس است）
    - `mode` (string)  مدل صدا.（برای نوع مدل `tts` در دسترس است）
    - `name` (string)  نام نمایش مدل صدا.（برای نوع مدل `tts` در دسترس است）
    - `language` (string)  زبان های پشتیبانی شده توسط مدل صدا.（برای نوع مدل `tts` در دسترس است）
  - `word_limit` (int)  حد مجاز کلمات تبدیل تک، به طور پیش فرض پاراگراف به پاراگراف（برای نوع مدل `tts` در دسترس است）
  - `audio_type` (string)  فرمت پسوند فایل صوتی پشتیبانی شده، مانند: mp3,wav（برای نوع مدل `tts` در دسترس است）
  - `max_workers` (int)  تعداد کارگران همزمان که تبدیل متن و صدا را پشتیبانی می کنند（برای نوع مدل`tts` در دسترس است）
  - `max_characters_per_chunk` (int) حداکثر کاراکتر در هر بخش (برای نوع مدل `moderation` در دسترس است)
- `parameter_rules` (array[[ParameterRule](#ParameterRule)]) [optional] قوانین پارامتر فراخوانی مدل
- `pricing` ([PriceConfig](#PriceConfig)) [optional] اطلاعات قیمت گذاری
- `deprecated` (bool) آیا منسوخ شده است. اگر منسوخ شده باشد، مدل دیگر در فهرست نمایش داده نمی شود، اما کسانی که قبلاً پیکربندی شده اند می توانند به استفاده از آن ادامه دهند. پیش فرض False.

### ModelType

- `llm` مدل تولید متن
- `text-embedding` مدل Embedding متن
- `rerank` مدل Rerank
- `speech2text` تبدیل گفتار به متن
- `tts` تبدیل متن به گفتار
- `moderation` تعدیل

### ConfigurateMethod

- `predefined-model` مدل از پیش تعریف شده

  نشان می دهد که کاربران می توانند با پیکربندی اعتبار ارائه دهنده یکپارچه از مدل های از پیش تعریف شده در ارائه دهنده استفاده کنند.
- `customizable-model` مدل قابل تنظیم

  کاربران باید برای هر مدل پیکربندی اعتبار را اضافه کنند.

- `fetch-from-remote` دریافت از راه دور

  مطابق با روش پیکربندی `predefined-model`، فقط نیاز به پیکربندی اعتبار ارائه دهنده یکپارچه است و مدل ها از طریق اطلاعات اعتبار از ارائه دهنده دریافت می شوند.

### ModelFeature

- `agent-thought` استدلال عامل، به طور کلی بیش از 70B با قابلیت زنجیره تفکر.
- `vision` بینایی، یعنی درک تصویر.
- `tool-call`
- `multi-tool-call`
- `stream-tool-call`

### FetchFrom

- `predefined-model` مدل از پیش تعریف شده
- `fetch-from-remote` مدل راه دور

### LLMMode

- `completion` تکمیل متن
- `chat` گفتگو

### ParameterRule

- `name` (string) نام واقعی پارامتر فراخوانی مدل
- `use_template` (string) [optional] استفاده از الگو

  به طور پیش فرض، 5 الگوی پیکربندی محتوای متغیر از پیش تعیین شده است:

  - `temperature`
  - `top_p`
  - `frequency_penalty`
  - `presence_penalty`
  - `max_tokens`
  
  در use_template، می توانید مستقیماً نام متغیر الگو را تنظیم کنید، که از پیکربندی پیش فرض در entities.defaults.PARAMETER_RULE_TEMPLATE استفاده می کند.
  نیازی به تنظیم هیچ پارامتری به غیر از `name` و `use_template` نیست. اگر پارامترهای پیکربندی اضافی تنظیم شوند، پیکربندی پیش فرض را لغو می کنند.
  به `openai/llm/gpt-3.5-turbo.yaml` مراجعه کنید.

- `label` (object) [optional] برچسب، i18n

  - `zh_Hans`(string) [optional] نام برچسب چینی
  - `en_US` (string) نام برچسب انگلیسی

- `type`(string) [optional] نوع پارامتر

  - `int` عدد صحیح
  - `float` اعشاری
  - `string` رشته
  - `boolean` بولی

- `help` (string) [optional] اطلاعات راهنما

  - `zh_Hans` (string) [optional] اطلاعات راهنما به زبان چینی
  - `en_US` (string) اطلاعات راهنما به زبان انگلیسی

- `required` (bool) الزامی، پیش فرض False.

- `default`(int/float/string/bool) [optional] مقدار پیش فرض

- `min`(int/float) [optional] حداقل مقدار، فقط برای انواع عددی قابل اجرا است

- `max`(int/float) [optional] حداکثر مقدار، فقط برای انواع عددی قابل اجرا است

- `precision`(int) [optional] دقت، تعداد ارقام اعشار برای حفظ، فقط برای انواع عددی قابل اجرا است

- `options` (array[string]) [optional] مقادیر گزینه های کشویی، فقط در صورتی که `type` `string` باشد قابل اجرا است، اگر تنظیم نشده باشد یا پوچ باشد، مقادیر گزینه محدود نمی شوند

### PriceConfig

- `input` (float) قیمت ورودی، یعنی قیمت Prompt
- `output` (float) قیمت خروجی، یعنی قیمت محتوای برگردانده شده
- `unit` (float) واحد قیمت گذاری، مانند اگر قیمت بر حسب 1M توکن اندازه گیری شود، مقدار توکن مربوط به قیمت واحد `0.000001` است.
- `currency` (string) واحد پول

### ProviderCredentialSchema

- `credential_form_schemas` (array[[CredentialFormSchema](#CredentialFormSchema)]) استاندارد فرم اعتبار

### ModelCredentialSchema

- `model` (object) شناسه مدل، نام متغیر به طور پیش فرض `model` است
  - `label` (object) نام نمایش آیتم فرم مدل
    - `en_US` (string) انگلیسی
    - `zh_Hans`(string) [optional] چینی
  - `placeholder` (object) محتوای پیام آیتم فرم مدل
    - `en_US`(string) انگلیسی
    - `zh_Hans`(string) [optional] چینی
- `credential_form_schemas` (array[[CredentialFormSchema](#CredentialFormSchema)]) استاندارد فرم اعتبار

### CredentialFormSchema

- `variable` (string) نام متغیر آیتم فرم
- `label` (object) نام برچسب آیتم فرم
  - `en_US`(string) انگلیسی
  - `zh_Hans` (string) [optional] چینی
- `type` ([FormType](#FormType)) نوع آیتم فرم
- `required` (bool) آیا الزامی است
- `default`(string) مقدار پیش فرض
- `options` (array[[FormOption](#FormOption)]) ویژگی خاص آیتم های فرم از نوع `select` یا `radio`، تعریف محتوای کشویی
- `placeholder`(object) ویژگی خاص آیتم های فرم از نوع `text-input`، محتوای جایگزین
  - `en_US`(string) انگلیسی
  - `zh_Hans` (string) [optional] چینی
- `max_length` (int) ویژگی خاص آیتم های فرم از نوع `text-input`، تعریف حداکثر طول ورودی، 0 برای بدون محدودیت.
- `show_on` (array[[FormShowOnObject](#FormShowOnObject)]) در صورتیکه مقادیر آیتم فرم دیگر شرایط خاصی را برآورده کنند، نمایش داده می شود، در صورت خالی بودن، همیشه نمایش داده می شود.

### FormType

- `text-input` کامپوننت ورودی متن
- `secret-input` کامپوننت ورودی رمز عبور
- `select` کشویی انتخاب تک
- `radio` کامپوننت رادیویی
- `switch` کامپوننت سوئیچ، فقط مقادیر `true` و `false` را پشتیبانی می کند

### FormOption

- `label` (object) برچسب
  - `en_US`(string) انگلیسی
  - `zh_Hans`(string) [optional] چینی
- `value` (string) مقدار گزینه کشویی
- `show_on` (array[[FormShowOnObject](#FormShowOnObject)]) در صورتیکه مقادیر آیتم فرم دیگر شرایط خاصی را برآورده کنند، نمایش داده می شود، در صورت خالی بودن، همیشه نمایش داده می شود.

### FormShowOnObject

- `variable` (string) نام متغیر آیتم های فرم دیگر
- `value` (string) مقدار متغیر آیتم های فرم دیگر


