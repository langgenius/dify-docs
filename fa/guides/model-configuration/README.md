---
description: درباره مدل‌های مختلف پشتیبانی شده توسط Dify بیاموزید.
---

# مدل

Dify یک پلتفرم توسعه برای برنامه‌های هوش مصنوعی مبتنی بر LLM Apps است، وقتی برای اولین بار از Dify استفاده می‌کنید، باید به **تنظیمات --> ارائه دهنده‌های مدل** بروید تا LLM مورد استفاده خود را اضافه و پیکربندی کنید.

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption><p>تنظیمات - ارائه دهنده مدل</p></figcaption></figure>

Dify از ارائه دهندگان مدل اصلی مانند سری GPT OpenAI و سری Claude Anthropic پشتیبانی می‌کند. قابلیت‌ها و پارامترهای هر مدل متفاوت است، بنابراین ارائه دهنده مدل مناسب برای نیازهای برنامه خود را انتخاب کنید. **قبل از استفاده از آن در Dify، کلید API را از وب سایت رسمی ارائه دهنده مدل دریافت کنید.**

## انواع مدل در Dify

Dify مدل‌ها را به 4 نوع طبقه‌بندی می‌کند که هر یک برای استفاده‌های مختلفی هستند:

1.  **مدل‌های استنباط سیستم:** در برنامه‌هایی برای وظایفی مانند چت، تولید نام و پیشنهاد سوالات بعدی استفاده می‌شود.

    > ارائه دهندگان شامل [OpenAI](https://platform.openai.com/account/api-keys) 、 [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/) 、 [Anthropic](https://console.anthropic.com/account/keys) 、 Hugging Face Hub 、 Replicate 、 Xinference 、 OpenLLM 、 [iFLYTEK SPARK](https://www.xfyun.cn/solutions/xinghuoAPI) 、 [WENXINYIYAN](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) 、 [TONGYI](https://dashscope.console.aliyun.com/api-key_management?spm=a2c4g.11186623.0.0.3bbc424dxZms9k) 、 [Minimax](https://api.minimax.chat/user-center/basic-information/interface-key) 、 ZHIPU(ChatGLM) [Ollama](https://docs.dify.ai/tutorials/model-configuration/ollama) 、 [LocalAI](https://github.com/mudler/LocalAI) 、 .
2.  **مدل‌های جاسازی:** برای جاسازی اسناد بخش بندی شده در دانش و پردازش پرس و جوهای کاربر در برنامه‌ها به کار می‌روند.

    > ارائه دهندگان شامل OpenAI، ZHIPU (ChatGLM)، Jina AI([Jina Embeddings](https://jina.ai/embeddings/)).
3.  [**مدل‌های Rerank**](https://docs.dify.ai/advanced/retrieval-augment/rerank)**:** قابلیت‌های جستجو را در LLMs ارتقا می‌دهند.

    > ارائه دهندگان شامل Cohere، Jina AI([Jina Reranker](https://jina.ai/reranker)).
4.  **مدل‌های گفتار به متن:** کلمات گفتاری را در برنامه‌های مکالمه‌ای به متن تبدیل می‌کنند.

    > ارائه دهنده: OpenAI.

Dify قصد دارد با پیشرفت فناوری و نیازهای کاربران، ارائه دهندگان LLM بیشتری را اضافه کند.

## خدمات آزمایشی مدل میزبانی شده

Dify سهمیه‌های آزمایشی را برای کاربران خدمات ابری ارائه می‌دهد تا مدل‌های مختلف را آزمایش کنند. ارائه دهنده مدل خود را قبل از پایان آزمایش تنظیم کنید تا اطمینان حاصل شود که استفاده از برنامه شما بدون وقفه ادامه دارد.

*  آزمایش مدل میزبانی شده OpenAI: شامل 200 فراخوانی برای مدل‌هایی مانند GPT3.5-turbo، GPT3.5-turbo-16k، مدل‌های text-davinci-003 است.

## تنظیم مدل پیش فرض

Dify به طور خودکار مدل پیش فرض را براساس استفاده انتخاب می‌کند. این را در `تنظیمات > ارائه دهنده مدل` پیکربندی کنید.

<figure><img src="../../.gitbook/assets/image-default-models (1).png" alt=""><figcaption></figcaption></figure>

## تنظیمات ادغام مدل

مدل خود را در `تنظیمات > ارائه دهنده مدل` Dify انتخاب کنید.

<figure><img src="../../.gitbook/assets/image-20231210143654461 (1).png" alt=""><figcaption></figcaption></figure>

ارائه دهندگان مدل به دو دسته تقسیم می‌شوند:

1.  مدل‌های اختصاصی: توسط ارائه دهندگانی مانند OpenAI و Anthropic توسعه یافته‌اند.
2.  مدل‌های میزبانی شده: مدل‌های شخص ثالث را مانند Hugging Face و Replicate ارائه می‌دهند.

روش‌های ادغام بین این دسته‌ها متفاوت است.

**ارائه دهندگان مدل اختصاصی:** Dify به تمام مدل‌ها از یک ارائه دهنده یکپارچه متصل می‌شود. کلید API ارائه دهنده را در Dify تنظیم کنید تا ادغام انجام شود.

{% hint style="info" %}
Dify از رمزگذاری [PKCS1_OAEP](https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html) برای محافظت از کلیدهای API شما استفاده می‌کند. هر کاربر (اجاره دهنده) یک جفت کلید منحصر به فرد برای رمزگذاری دارد که اطمینان حاصل می‌کند کلیدهای API شما محرمانه باقی می‌مانند.
{% endhint %}

**ارائه دهندگان مدل میزبانی شده:** به صورت جداگانه با مدل‌های شخص ثالث ادغام کنید.

روش‌های ادغام خاص در اینجا شرح داده نشده‌اند.

* [Hugging Face](https://docs.dify.ai/advanced/model-configuration/hugging-face)
* [Replicate](https://docs.dify.ai/advanced/model-configuration/replicate)
* [Xinference](https://docs.dify.ai/advanced/model-configuration/xinference)
* [OpenLLM](https://docs.dify.ai/advanced/model-configuration/openllm)

## استفاده از مدل‌ها

پس از پیکربندی، این مدل‌ها برای استفاده از برنامه آماده هستند.

<figure><img src="../../.gitbook/assets/choice-model-in-app (1).png" alt=""><figcaption></figcaption></figure>


