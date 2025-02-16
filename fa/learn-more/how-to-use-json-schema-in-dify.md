# نحوه استفاده از خروجی JSON Schema در Dify

JSON Schema یک مشخصات برای توصیف ساختار داده‌های JSON است. توسعه‌دهندگان می‌توانند ساختارهای JSON Schema را برای تعیین اینکه خروجی‌های LLM دقیقاً از داده‌ها یا محتواهای تعریف‌شده پیروی می‌کنند، تعریف کنند، مانند تولید ساختارهای شفاف سند یا کد.

## مدل‌هایی که از قابلیت JSON Schema پشتیبانی می‌کنند

- `gpt-4o-mini-2024-07-18` و نسخه‌های بعد از آن
- `gpt-4o-2024-08-06` و نسخه‌های بعد از آن

> برای اطلاعات بیشتر در مورد قابلیت‌های خروجی ساخت‌یافته مدل‌های سری OpenAI، لطفاً به [خروجی‌های ساخت‌یافته](https://platform.openai.com/docs/guides/structured-outputs/introduction) مراجعه کنید.

## نحوه استفاده از خروجی‌های ساخت‌یافته

1. LLM را به ابزارها، توابع، داده‌ها و سایر اجزای موجود در سیستم متصل کنید. `strict: true` را در تعریف تابع تنظیم کنید. هنگامی که فعال است، ویژگی خروجی‌های ساخت‌یافته تضمین می‌کند که پارامترهای تولید شده توسط LLM برای فراخوانی‌های تابع دقیقاً با JSON Schema که در تعریف تابع ارائه کرده‌اید مطابقت دارند.

2. هنگامی که LLM به کاربران پاسخ می‌دهد، محتوا را در قالبی ساخت‌یافته مطابق با تعاریف موجود در JSON Schema  خروجی می‌دهد.

## فعال‌سازی JSON Schema در Dify

LLM در برنامه خود را به یکی از مدل‌های پشتیبانی کننده خروجی JSON Schema که در بالا ذکر شد، تغییر دهید. سپس، در فرم تنظیمات، `JSON Schema` را فعال کنید و الگوی JSON Schema را پر کنید. همزمان، ستون `response_format` را فعال کنید و آن را به فرمت `json_schema` تغییر دهید.

![](../../../img/learn-more-json-schema.png)

محتوای تولید شده توسط LLM از خروجی در قالب‌های زیر پشتیبانی می‌کند:

- **متن:** خروجی در قالب متن

## تعریف الگوهای JSON Schema

می‌توانید به فرمت JSON Schema زیر مراجعه کنید تا محتوای الگوی خود را تعریف کنید:

```json
{
    "name": "template_schema",
    "description": "یک الگوی عمومی برای JSON Schema",
    "strict": true,
    "schema": {
        "type": "object",
        "properties": {
            "field1": {
                "type": "string",
                "description": "شرح فیلد 1"
            },
            "field2": {
                "type": "number",
                "description": "شرح فیلد 2"
            },
            "field3": {
                "type": "array",
                "description": "شرح فیلد 3",
                "items": {
                    "type": "string"
                }
            },
            "field4": {
                "type": "object",
                "description": "شرح فیلد 4",
                "properties": {
                    "subfield1": {
                        "type": "string",
                        "description": "شرح زیر فیلد 1"
                    }
                },
                "required": ["subfield1"],
                "additionalProperties": false
            }
        },
        "required": ["field1", "field2", "field3", "field4"],
        "additionalProperties": false
    }
}
```


راهنمای گام به گام:

1. اطلاعات پایه را تعریف کنید:
   - `name` را تنظیم کنید: نامی توصیفی برای طرح خود انتخاب کنید.
   - `description` را اضافه کنید: هدف طرح را به طور خلاصه توضیح دهید.
   - `strict` را روی true تنظیم کنید: برای اطمینان از حالت دقیق.

2. شیء `schema` را ایجاد کنید:
   - `type: "object"` را برای تعیین سطح ریشه به عنوان یک نوع شیء تنظیم کنید.
   - یک شیء `properties` برای تعریف همه فیلدها اضافه کنید.

3. فیلدها را تعریف کنید:
   - برای هر فیلد یک شیء ایجاد کنید، از جمله `type` و `description`.
   - انواع رایج: `string`, `number`, `boolean`, `array`, `object`.
   - برای آرایه‌ها، از `items` برای تعریف انواع عنصر استفاده کنید.
   - برای اشیاء، `properties` را به صورت بازگشتی تعریف کنید.

4. محدودیت‌ها را تنظیم کنید:
   - یک آرایه `required` در هر سطح اضافه کنید، که تمام فیلدهای مورد نیاز را فهرست می‌کند.
   - `additionalProperties: false` را در هر سطح شیء تنظیم کنید.

5. فیلدهای ویژه را اداره کنید:
   - از `enum` برای محدود کردن مقادیر اختیاری استفاده کنید.
   - از `$ref` برای پیاده‌سازی ساختارهای بازگشتی استفاده کنید.

## مثال

### 1. زنجیره تفکر (روال)

**مثال JSON Schema**

```json
{
    "name": "math_reasoning",
    "description": "مراحل و پاسخ نهایی را برای استدلال ریاضی ثبت می‌کند",
    "strict": true,
    "schema": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "description": "آرایه‌ای از مراحل استدلال",
                "items": {
                    "type": "object",
                    "properties": {
                        "explanation": {
                            "type": "string",
                            "description": "توضیح مرحله استدلال"
                        },
                        "output": {
                            "type": "string",
                            "description": "خروجی مرحله استدلال"
                        }
                    },
                    "required": ["explanation", "output"],
                    "additionalProperties": false
                }
            },
            "final_answer": {
                "type": "string",
                "description": "پاسخ نهایی به مسئله ریاضی"
            }
        },
        "additionalProperties": false,
        "required": ["steps", "final_answer"]
    }
}
```

**دستورات**

```text
شما یک معلم خصوصی ریاضی مفید هستید. یک مسئله ریاضی به شما ارائه خواهد شد،
و هدف شما خروجی یک راه حل گام به گام، همراه با یک پاسخ نهایی است.
برای هر مرحله، فقط خروجی را به عنوان یک معادله ارائه دهید و از فیلد explanation برای شرح استدلال استفاده کنید.
```

### تولید UI (حالت بازگشتی ریشه)

**مثال JSON Schema**

```json
{
        "name": "ui",
        "description": "UI به صورت پویا تولید شده",
        "strict": true,
        "schema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "نوع مؤلفه UI",
                    "enum": ["div", "button", "header", "section", "field", "form"]
                },
                "label": {
                    "type": "string",
                    "description": "برچسب مؤلفه UI، که برای دکمه‌ها یا فیلدهای فرم استفاده می‌شود"
                },
                "children": {
                    "type": "array",
                    "description": "مؤلفه‌های UI تو در تو",
                    "items": {
                        "$ref": "#"
                    }
                },
                "attributes": {
                    "type": "array",
                    "description": "صفات دلخواه برای مؤلفه UI، مناسب برای هر عنصر",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "نام صفت، به عنوان مثال onClick یا className"
                            },
                            "value": {
                                "type": "string",
                                "description": "مقدار صفت"
                            }
                        },
                      "additionalProperties": false,
                      "required": ["name", "value"]
                    }
                }
            },
            "required": ["type", "label", "children", "attributes"],
            "additionalProperties": false
        }
    }
```

**دستورات**

```text
شما یک AI تولید کننده UI هستید. ورودی کاربر را به یک UI تبدیل کنید.
```

**مثال خروجی:**

![](../../img/best-practice-json-schema-ui-example.png)

## نکات

- اطمینان حاصل کنید که دستورالعمل برنامه شامل دستورالعمل‌های نحوه برخورد با مواردی است که ورودی کاربر نمی‌تواند پاسخ معتبر تولید کند.

- مدل همیشه تلاش می‌کند از طرح ارائه شده پیروی کند. اگر محتوای ورودی کاملاً بی ارتباط با طرح مشخص شده باشد، ممکن است باعث تولید توهم در LLM شود.

- اگر LLM تشخیص دهد که ورودی با کار ناسازگار است، می‌توانید در دستورالعمل، زبان مشخصی را برای تعیین بازگرداندن پارامترهای خالی یا جملات خاص بگنجانید.

- همه فیلدها باید `required` باشند، برای جزئیات، لطفاً به [طرح‌های پشتیبانی شده](https://platform.openai.com/docs/guides/structured-outputs/supported-schemas) مراجعه کنید.

- [additionalProperties: false](https://platform.openai.com/docs/guides/structured-outputs/additionalproperties-false-must-always-be-set-in-objects) باید همیشه در اشیاء تنظیم شود.

- شیء سطح ریشه طرح باید یک شیء باشد.

## پیوست

- [مقدمه‌ای بر خروجی‌های ساخت‌یافته](https://cookbook.openai.com/examples/structured_outputs_intro)

- [خروجی ساخت‌یافته](https://platform.openai.com/docs/guides/structured-outputs/json-mode?context=without_parse)


