# ادغام مدل ها در پروکسی LiteLLM

[پروکسی LiteLLM](https://github.com/BerriAI/litellm) یک سرور پروکسی است که به شما امکان می‌دهد:

* تماس با بیش از 100 مدل زبان بزرگ (LLM) (OpenAI، Azure، Vertex، Bedrock) در قالب OpenAI
* استفاده از کلیدهای مجازی برای تنظیم بودجه، محدودیت نرخ و ردیابی استفاده

Dify از ادغام مدل‌های LLM و Text Embedding موجود در پروکسی LiteLLM پشتیبانی می‌کند.

## ادغام سریع

### گام 1. راه اندازی سرور پروکسی LiteLLM

LiteLLM برای پیکربندی به یک فایل پیکربندی با تمام مدل‌های شما نیاز دارد – ما این فایل را `litellm_config.yaml` می‌نامیم.

[مستندات دقیق در مورد نحوه تنظیم پیکربندی litellm – در اینجا](https://docs.litellm.ai/docs/proxy/configs)

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: azure/chatgpt-v-2
      api_base: https://openai-gpt-4-test-v-1.openai.azure.com/
      api_version: "2023-05-15"
      api_key: 
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4
      api_key: 
      api_base: https://openai-gpt-4-test-v-2.openai.azure.com/
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4
      api_key: 
      api_base: https://openai-gpt-4-test-v-2.openai.azure.com/
```

### گام 2. راه اندازی پروکسی LiteLLM

```shell
docker run \
    -v $(pwd)/litellm_config.yaml:/app/config.yaml \
    -p 4000:4000 \
    ghcr.io/berriai/litellm:main-latest \
    --config /app/config.yaml --detailed_debug
```

در صورت موفقیت، پروکسی در `http://localhost:4000` اجرا خواهد شد.

### گام 3. ادغام پروکسی LiteLLM در Dify

در `تنظیمات > ارائه دهندگان مدل > OpenAI-API-compatible`، موارد زیر را پر کنید:

<figure><img src="../../.gitbook/assets/image (115).png" alt=""><figcaption></figcaption></figure>

* نام مدل: `gpt-4`
*   URL پایه: `http://localhost:4000`

    URL پایه را که سرویس LiteLLM در آن قابل دسترسی است، وارد کنید.
* نوع مدل: `چت`
*   طول متن مدل: `4096`

    حداکثر طول متن مدل. در صورت عدم اطمینان، از مقدار پیش فرض 4096 استفاده کنید.
*   حداکثر تعداد توکن: `4096`

    حداکثر تعداد توکن‌های بازگردانده شده توسط مدل. در صورت عدم وجود نیازهای خاص برای مدل، این می‌تواند با طول متن مدل مطابقت داشته باشد.
*   پشتیبانی از دیداری: `بله`

    این گزینه را بررسی کنید اگر مدل از درک تصویر (چند حالته) پشتیبانی می‌کند، مانند `gpt4-o`.

برای استفاده از مدل در برنامه بعد از اطمینان از عدم وجود خطا، روی "ذخیره" کلیک کنید.

روش ادغام برای مدل‌های Embedding مشابه LLM است، فقط نوع مدل را به Text Embedding تغییر دهید.

## اطلاعات بیشتر

برای اطلاعات بیشتر در مورد LiteLLM، به موارد زیر مراجعه کنید:

* [LiteLLM](https://github.com/BerriAI/litellm)
* [سرور پروکسی LiteLLM](https://docs.litellm.ai/docs/simple\_proxy)


