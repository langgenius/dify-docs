# ساخت دستیار هوش مصنوعی Notion

### مقدمه

Notion یک ابزار قدرتمند برای مدیریت دانش است. انعطاف‌پذیری و قابلیت توسعه آن، آن را به یک کتابخانه دانش شخصی و فضای کاری مشترک عالی تبدیل می‌کند. بسیاری از افراد از آن برای ذخیره دانش و کار در کنار دیگران استفاده می‌کنند و تبادل ایده‌ها و ایجاد دانش جدید را تسهیل می‌کنند.

با این حال، این دانش ثابت باقی می‌ماند، زیرا کاربران باید به دنبال اطلاعات مورد نیاز خود باشند و آن را مطالعه کنند تا پاسخ‌های مورد نظر خود را پیدا کنند. این فرآیند نه به طور خاص کارآمد است و نه هوشمندانه.

آیا تا به حال آرزو کرده‌اید که یک دستیار هوش مصنوعی مبتنی بر کتابخانه Notion خود داشته باشید؟ این دستیار نه تنها شما را در مرور پایگاه دانش خود یاری می‌کند، بلکه مانند یک خدمتکار باتجربه، حتی در پاسخگویی به سوالات دیگران نیز مشارکت می‌کند، گویی که شما صاحب کتابخانه شخصی Notion خود هستید.

### چگونه دستیار هوش مصنوعی Notion خود را به واقعیت تبدیل کنیم؟

اکنون، می‌توانید این رویا را از طریق [Dify](https://dify.ai/) به حقیقت تبدیل کنید. Dify یک پلتفرم LLMOps (عملیات مدل‌های زبان بزرگ) متن‌باز است.

مدل‌های زبان بزرگ مانند ChatGPT و Claude، از توانایی‌های چشمگیر خود برای تغییر شکل جهان استفاده می‌کنند. توانایی یادگیری قدرتمند آنها عمدتا به دلیل داده‌های آموزشی قوی است. خوشبختانه، آنها به اندازه کافی باهوش شده‌اند تا از محتوایی که شما ارائه می‌کنید بیاموزند و بدین ترتیب، فرآیند ایده پردازی از کتابخانه شخصی Notion شما، به واقعیت تبدیل می‌شود.

بدون Dify، ممکن است نیاز باشد که خودتان را با langchain، یک انتزاع که فرآیند مونتاژ این قطعات را ساده می‌کند، آشنا کنید.

### چگونه از Dify برای ساخت دستیار هوش مصنوعی شخصی Notion خود استفاده کنیم؟

فرآیند آموزش یک دستیار هوش مصنوعی Notion نسبتاً ساده است. فقط مراحل زیر را دنبال کنید:

1. وارد Dify شوید.
2. یک پایگاه دانش جدید ایجاد کنید.
3. با Notion و پایگاه داده‌های خود ارتباط برقرار کنید.
4. آموزش را شروع کنید.
5. برنامه هوش مصنوعی خود را ایجاد کنید.

#### 1. ورود به Dify

برای ورود به Dify، روی [اینجا](https://dify.ai/) کلیک کنید. می‌توانید به راحتی از طریق حساب GitHub یا Google خود وارد شوید.

> اگر از حساب GitHub برای ورود استفاده می‌کنید، چگونه است که این [پروژه](https://github.com/langgenius/dify) را با یک ستاره برجسته می‌کنید؟ این واقعاً به ما کمک زیادی می‌کند!

#### 2. ایجاد پایگاه دانش جدید

روی دکمه `Knowledge` در نوار کناری بالا، و سپس روی دکمه `Create Knowledge` کلیک کنید.

![login-2](../../.gitbook/assets/login-2.png)

#### 3. اتصال با Notion و پایگاه داده‌های خود[​](https://wsyfin.com/notion-dify#3-connect-with-notion-and-datasets)

"Sync from Notion" را انتخاب کنید و سپس روی دکمه "Connect" کلیک کنید.

![connect-with-notion-1](../../.gitbook/assets/connect-with-notion-1.png)

سپس، به صفحه ورود Notion هدایت خواهید شد. با حساب Notion خود وارد شوید.

<figure><img src="../../.gitbook/assets/connect-with-notion-2.png" alt=""><figcaption></figcaption></figure>

مجوزهای مورد نیاز Dify را بررسی کنید و سپس روی دکمه "Select pages" کلیک کنید.

<figure><img src="../../.gitbook/assets/connect-with-notion-3.png" alt=""><figcaption></figcaption></figure>

صفحاتی را که می‌خواهید با Dify همگام‌سازی کنید، انتخاب کنید و روی دکمه "Allow access" کلیک کنید.

<figure><img src="../../.gitbook/assets/connect-with-notion-4.png" alt=""><figcaption></figcaption></figure>

#### 4. شروع آموزش[​](https://wsyfin.com/notion-dify#4-start-training) <a href="#id-4-start-training" id="id-4-start-training"></a>

صفحاتی را که هوش مصنوعی باید آنها را مطالعه کند، مشخص کنید، و به آن اجازه دهید تا محتوای موجود در این بخش از Notion را درک کند. سپس روی دکمه "next" کلیک کنید.

![train-1](../../.gitbook/assets/train-1.png)

ما پیشنهاد می‌کنیم که گزینه‌های "Automatic" و "High Quality" را برای آموزش دستیار هوش مصنوعی خود انتخاب کنید. سپس روی دکمه "Save & Process" کلیک کنید.

![train-2](../../.gitbook/assets/train-2.png)

در حالی که منتظر اتمام فرآیند آموزش هستید، از قهوه خود لذت ببرید.

![train-3](../../.gitbook/assets/train-3.png)

#### 5. ایجاد برنامه هوش مصنوعی خود[​](https://wsyfin.com/notion-dify#5-create-your-ai-application) <a href="#id-5-create-your-own-ai-application" id="id-5-create-your-own-ai-application"></a>

باید یک برنامه هوش مصنوعی ایجاد کنید و آن را با دانش تازه ایجاد شده خود پیوند دهید.

به داشبورد برگردید و روی دکمه "Create new APP" کلیک کنید. توصیه می‌شود که مستقیماً از "Chat App" استفاده کنید.

![create-app-1](../../.gitbook/assets/create-app-1.png)

"Prompt Eng." را انتخاب کنید و پایگاه داده‌های Notion خود را در "context" پیوند دهید.

![create-app-2](../../.gitbook/assets/create-app-2.png)

من توصیه می‌کنم که "Pre Prompt" را به برنامه هوش مصنوعی خود اضافه کنید. درست مانند طلسم‌ها که برای هری پاتر ضروری هستند، ابزارها یا ویژگی‌های خاصی می‌توانند توانایی برنامه هوش مصنوعی را به شدت افزایش دهند.

به عنوان مثال، اگر یادداشت‌های Notion شما بر حل مسئله در توسعه نرم‌افزار متمرکز است، می‌توانید در یکی از دستورالعمل‌ها بنویسید:

_من می‌خواهم شما به عنوان یک متخصص فناوری اطلاعات در فضای کاری Notion من عمل کنید، از دانش خود در مورد علوم کامپیوتر، زیرساخت‌های شبکه، یادداشت‌های Notion و امنیت فناوری اطلاعات برای حل مشکلات استفاده کنید_.

<figure><img src="../../.gitbook/assets/image (40) (2).png" alt=""><figcaption></figcaption></figure>

توصیه می‌شود که در ابتدا هوش مصنوعی را قادر سازید که به طور فعال به کاربران یک جمله آغازین ارائه دهد و به آنها سرنخی در مورد آنچه که می‌توانند بپرسند، ارائه دهد. علاوه بر این، فعال کردن ویژگی "Speech to Text" می‌تواند به کاربران اجازه دهد تا با استفاده از صدای خود با دستیار هوش مصنوعی شما تعامل داشته باشند.

<figure><img src="../../.gitbook/assets/notion-speech-to-text.png" alt=""><figcaption></figcaption></figure>

در نهایت، روی دکمه "Publish" در سمت راست بالای صفحه کلیک کنید. اکنون می‌توانید روی URL عمومی در بخش "Monitoring" کلیک کنید تا با دستیار هوش مصنوعی شخصی خود گفتگو کنید!

![create-app-4](../../.gitbook/assets/app-url.png)

### استفاده از API برای ادغام با پروژه خود <a href="#utilizing-api-to-integrate-with-your-project" id="utilizing-api-to-integrate-with-your-project"></a>

هر برنامه هوش مصنوعی که توسط Dify ساخته شده است، از طریق API آن قابل دسترسی است. این روش به توسعه‌دهندگان امکان می‌دهد تا مستقیماً از ویژگی‌های قدرتمند مدل‌های زبان بزرگ (LLMs) در برنامه‌های سمت کاربر استفاده کنند و یک تجربه "Backend-as-a-Service" (BaaS) واقعی را ارائه دهند.

با ادغام API بدون دردسر، می‌توانید به راحتی برنامه هوش مصنوعی Notion خود را بدون نیاز به تنظیمات پیچیده فراخوانی کنید.

روی دکمه "API Reference" در صفحه Overview page کلیک کنید. می‌توانید به آن به عنوان سند API برنامه خود مراجعه کنید.

![using-api-1](../../.gitbook/assets/api-reference.png)

#### 1. تولید کلید مخفی API[​](https://wsyfin.com/notion-dify#1-generate-api-secret-key) <a href="#id-1-generate-api-secret-key" id="id-1-generate-api-secret-key"></a>

به دلایل امنیتی، توصیه می‌شود که یک کلید مخفی API جدید برای دسترسی به برنامه هوش مصنوعی خود ایجاد کنید.

![using-api-2](../../.gitbook/assets/using-api-2.png)

#### 2. بازیابی ID مکالمه[​](https://wsyfin.com/notion-dify#2-retrieve-conversation-id) <a href="#id-2-retrieve-conversation-id" id="id-2-retrieve-conversation-id"></a>

پس از گفتگو با برنامه هوش مصنوعی خود، می‌توانید ID جلسه را از صفحات "Logs & Ann." بازیابی کنید.

![using-api-3](../../.gitbook/assets/using-api-3.png)

#### 3. فراخوانی API[​](https://wsyfin.com/notion-dify#3-invoke-api) <a href="#id-3-invoke-api" id="id-3-invoke-api"></a>

می‌توانید کد درخواست نمونه را در سند API برای فراخوانی برنامه هوش مصنوعی خود در ترمینال اجرا کنید.

به یاد داشته باشید که `YOUR SECRET KEY` و `conversation_id` را در کد خود جایگزین کنید.

> می‌توانید در اولین بار `conversation_id` خالی را وارد کنید و بعد از دریافت پاسخ حاوی `conversation_id`، آن را جایگزین کنید.

```
curl --location --request POST 'https://api.dify.ai/v1/chat-messages' \
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {},
    "query": "eh",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123"
}'
```

درخواست را در ترمینال ارسال کنید و یک پاسخ موفقیت‌آمیز دریافت خواهید کرد.

![using-api-4](../../.gitbook/assets/using-api-4.png)

اگر می‌خواهید این گفتگو را ادامه دهید، `conversation_id` کد درخواست را به `conversation_id` که از پاسخ دریافت کرده‌اید، جایگزین کنید.

و می‌توانید تمام تاریخچه مکالمه را در صفحه "Logs & Ann." بررسی کنید.

![using-api-5](../../.gitbook/assets/using-api-5.png)

### همگام‌سازی با Notion به طور دوره‌ای[​](https://wsyfin.com/notion-dify#sync-with-notion-periodically) <a href="#sync-with-notion-periodically" id="sync-with-notion-periodically"></a>

اگر صفحات Notion شما به روز شده‌اند، می‌توانید به طور دوره‌ای با Dify همگام‌سازی کنید تا دستیار هوش مصنوعی شما به روز باشد. دستیار هوش مصنوعی شما از محتوای جدید یاد خواهد گرفت.

![create-app-5](../../.gitbook/assets/create-app-5.png)

### خلاصه[​](https://wsyfin.com/notion-dify#summary) <a href="#summary" id="summary"></a>

در این آموزش، نه تنها نحوه وارد کردن داده‌های Notion خود به Dify را آموخته‌ایم، بلکه نحوه استفاده از API برای ادغام آن با پروژه خود را نیز می‌دانیم.

[Dify](https://dify.ai/) یک پلتفرم LLMOps کاربرپسند است که برای توانمندسازی افراد بیشتر برای ایجاد برنامه‌های پایدار و بومی AI طراحی شده است. Dify با ارکستراسیون بصری که برای انواع مختلف برنامه‌ها طراحی شده است، برنامه‌های آماده استفاده‌ای را ارائه می‌دهد که می‌توانند شما را در استفاده از داده‌ها برای ساخت دستیار هوش مصنوعی منحصر به فرد خود کمک کنند. اگر سوالی دارید، دریغ نکنید که با ما تماس بگیرید.


