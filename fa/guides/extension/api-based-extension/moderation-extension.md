# اعتدال

این ماژول برای بررسی محتوای ورودی از سوی کاربران نهایی و خروجی از LLM ها در برنامه استفاده می شود که به دو نوع نقطه توسعه تقسیم می شود.

لطفاً [.](./ "mention") را برای تکمیل توسعه و ادغام قابلیت های اولیه خدمات API بخوانید.

## نقطه توسعه

`app.moderation.input`: نقطه توسعه بررسی محتوای ورودی کاربر نهایی. برای بررسی محتوای متغیرهای ارسال شده توسط کاربران نهایی و محتوای ورودی گفتگوها در برنامه های مکالمه ای استفاده می شود.

`app.moderation.output`: نقطه توسعه بررسی محتوای خروجی LLM. برای بررسی محتوای خروجی LLM استفاده می شود. هنگامی که خروجی LLM در حال جریان است، محتوا به صورت تکه های 100 کاراکتری توسط API درخواست می شود تا از تأخیر در بررسی هنگام طولانی بودن محتوای خروجی جلوگیری شود.

### `app.moderation.input`

#### بدنه درخواست

```json
{
    "point": "app.moderation.input", 
        "app_id": string,  
        "inputs": {  
            "var_1": "value_1",
            "var_2": "value_2",
            ...
        },
        "query": string | null  
    }
}
```

* مثال

```json
{
    "point": "app.moderation.input",
    "params": {
        "app_id": "61248ab4-1125-45be-ae32-0ce91334d021",
        "inputs": {
            "var_1": "I will kill you.",
            "var_2": "I will fuck you."
        },
        "query": "Happy everydays."
    }
}
```

#### پاسخ API

```json
{
    "flagged": bool,  
    "action": string, 
    "preset_response": string,  
    "inputs": {  
        "var_1": "value_1",
        "var_2": "value_2",
        ...
    },
    "query": string | null  
}
```

* مثال

`action=direct_output`

```json
{
    "flagged": true,
    "action": "direct_output",
    "preset_response": "Your content violates our usage policy."
}
```

`action=overridden`

```
{
    "flagged": true,
    "action": "overridden",
    "inputs": {
        "var_1": "I will *** you.",
        "var_2": "I will *** you."
    },
    "query": "Happy everydays."
}
```

### `app.moderation.output`

#### بدنه درخواست

```JSON
{
    "point": "app.moderation.output", 
    "params": {
        "app_id": string,  
        "text": string  
    }
}
```

*   مثال



    ```JSON
    {
        "point": "app.moderation.output",
        "params": {
            "app_id": "61248ab4-1125-45be-ae32-0ce91334d021",
            "text": "I will kill you."
        }
    }
    ```

#### پاسخ API

```JSON
{
    "flagged": bool,  
    "action": string, 
    "preset_response": string,  
    "text": string  
```

* مثال

`action=direct_output`

* ```JSON
  {
      "flagged": true,
      "action": "direct_output",
      "preset_response": "Your content violates our usage policy."
  }
  ```

`action=overridden`

* ```JSON
  {
      "flagged": true,
      "action": "overridden",
      "text": "I will *** you."
  }
  ```



