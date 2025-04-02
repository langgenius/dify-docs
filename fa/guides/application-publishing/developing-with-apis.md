# توسعه با APIها

Dify یک API "Backend-as-a-Service" ارائه می‌دهد که مزایای متعددی برای توسعه‌دهندگان برنامه‌های هوش مصنوعی به ارمغان می‌آورد. این رویکرد به توسعه‌دهندگان اجازه می‌دهد تا مستقیماً به قابلیت‌های قدرتمند مدل‌های زبانی بزرگ (LLM) در برنامه‌های سمت کاربر دسترسی داشته باشند بدون اینکه پیچیدگی‌های معماری سمت سرور و فرآیندهای استقرار را تحمل کنند.

### مزایای استفاده از API Dify

*  اجازه دسترسی امن برنامه‌های سمت کاربر به قابلیت‌های LLM بدون توسعه سمت سرور 
*  طراحی بصری برنامه‌ها با به‌روزرسانی‌های بلادرنگ در تمام کلاینت‌ها
*  APIهای LLM اصلی با احاطه کامل 
*  جابه‌جایی آسان بین ارائه ‌دهندگان LLM و مدیریت متمرکز کلیدهای API
*  عملیات بصری برنامه‌ها، از جمله تجزیه و تحلیل لاگ، حاشیه نویسی و مشاهده فعالیت‌های کاربر 
*  ارائه مداوم ابزارها، افزونه‌ها و دانش جدید

### چگونگی استفاده

یک برنامه را انتخاب کنید و در بخش برنامه‌ها، در ناوبری سمت چپ، "دسترسی به API" را پیدا کنید. در این صفحه، می‌توانید مستندات API ارائه شده توسط Dify را مشاهده کنید و اعتبارنامه‌های دسترسی به API را مدیریت کنید.

<figure><img src="/en/.gitbook/assets/guides\application-publishing\launch-your-webapp-quickly/API Access.png" alt=""><figcaption><p>مستندات API</p></figcaption></figure>

شما می‌توانید اعتبارنامه‌های دسترسی چندگانه برای یک برنامه ایجاد کنید تا به کاربران یا توسعه‌دهندگان مختلف تحویل دهید. این به این معنی است که کاربران API می‌توانند از قابلیت‌های هوش مصنوعی ارائه شده توسط توسعه‌دهنده برنامه استفاده کنند، اما مهندسی Prompt، دانش و قابلیت‌های ابزاری زیربنایی حفظ می‌شوند.

{% hint style="warning" %}
در بهترین روش‌ها، کلیدهای API باید از طریق سمت سرور فراخوانی شوند، نه اینکه به طور مستقیم در کد یا درخواست‌های سمت کاربر در متن ساده نمایش داده شوند. این به جلوگیری از سوء استفاده یا حمله به برنامه شما کمک می‌کند.
{% endhint %}

به عنوان مثال، اگر شما یک توسعه‌دهنده در یک شرکت مشاوره‌ای هستید، می‌توانید قابلیت‌های هوش مصنوعی مبتنی بر پایگاه داده خصوصی شرکت را به کاربران نهایی یا توسعه‌دهندگان ارائه دهید، بدون اینکه داده‌ها و طراحی منطق هوش مصنوعی خود را در معرض دید قرار دهید. این امر تضمین می‌کند که ارائه خدمات ایمن و پایدار است که به اهداف تجاری پاسخ می‌دهد.

### برنامه تولید متن

این برنامه‌ها با فراخوانی API completion-messages و ارسال ورودی کاربر برای دریافت نتایج متن تولید شده، برای تولید متن با کیفیت بالا، مانند مقالات، خلاصه‌ ها، ترجمه‌ها و غیره استفاده می‌شوند. پارامترهای مدل و الگوهای Prompt استفاده شده برای تولید متن بستگی به تنظیمات توسعه‌دهنده در صفحه Dify Prompt Arrangement دارد.

شما می‌توانید مستندات API و درخواست‌های نمونه برای این برنامه را در **برنامه‌ها -> دسترسی به API** بیابید.

به عنوان مثال، در اینجا یک نمونه از فراخوانی یک API برای تولید متن ارائه شده است:

{% tabs %}
{% tab title="cURL" %}
```
curl --location --request POST 'https://api.dify.ai/v1/completion-messages' \
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {},
    "response_mode": "streaming",
    "user": "abc-123"
}'
```
{% endtab %}

{% tab title="Python" %}
```python
import requests
import json

url = "https://api.dify.ai/v1/completion-messages"

headers = {
    'Authorization': 'Bearer ENTER-YOUR-SECRET-KEY',
    'Content-Type': 'application/json',
}

data = {
    "inputs": {"text": 'سلام، حالت چطوره؟'},
    "response_mode": "streaming",
    "user": "abc-123"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)
```
{% endtab %}
{% endtabs %}

### برنامه‌های محاوره‌ای

برنامه‌های محاوره‌ای از طریق یک فرمت سوال و جواب، گفتگوی مداوم با کاربران را تسهیل می‌کنند. برای شروع یک مکالمه، شما باید API `chat-messages` را فراخوانی کنید. یک `conversation_id` برای هر جلسه تولید می‌شود و باید در تماس‌های API بعدی برای حفظ جریان مکالمه گنجانده شود.

#### نکات کلیدی برای `conversation_id`:

- **تولید `conversation_id`:** هنگام شروع یک مکالمه جدید، فیلد `conversation_id` را خالی بگذارید. سیستم یک `conversation_id` جدید تولید می‌کند و آن را برمی‌گرداند، که شما در تعاملات بعدی برای ادامه گفتگو از آن استفاده خواهید کرد.
- **مدیریت `conversation_id` در جلسات موجود:** پس از تولید یک `conversation_id`، تماس‌های آینده با API باید این `conversation_id` را شامل شوند تا اطمینان حاصل شود که گفتگو با ربات Dify ادامه دارد. وقتی یک `conversation_id` قبلی منتقل می‌شود، هر `inputs` جدیدی نادیده گرفته خواهد شد. فقط `query` برای ادامه گفتگو پردازش می‌شود.
- **مدیریت متغیرهای پویا:** اگر نیازی به تغییر منطق یا متغیرها در طول جلسه وجود دارد، می‌توانید از متغیرهای مکالمه (متغیرهای خاص جلسه) برای تنظیم رفتار یا پاسخ ربات استفاده کنید.

شما می‌توانید مستندات API و درخواست‌های نمونه برای این برنامه را در **برنامه‌ها -> دسترسی به API** بیابید.

در اینجا مثالی از فراخوانی API `chat-messages` ارائه شده است:

{% tabs %}
{% tab title="cURL" %}
```
curl --location --request POST 'https://api.dify.ai/v1/chat-messages' \
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {},
    "query": "سلام",
    "response_mode": "streaming",
    "conversation_id": "1c7e55fb-1ba2-4e10-81b5-30addcea2276",
    "user": "abc-123"
}'
```
{% endtab %}

{% tab title="Python" %}
```python
import requests
import json

url = 'https://api.dify.ai/v1/chat-messages'
headers = {
    'Authorization': 'Bearer ENTER-YOUR-SECRET-KEY',
    'Content-Type': 'application/json',
}
data = {
    "inputs": {},
    "query": "سلام",
    "response_mode": "streaming",
    "conversation_id": "1c7e55fb-1ba2-4e10-81b5-30addcea2276",
    "user": "abc-123"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())
```
{% endtab %}
{% endtabs %}


