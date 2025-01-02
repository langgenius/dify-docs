# جاسازی در وب‌سایت‌ها

اپلیکیشن‌های Dify را می‌توان با استفاده از یک iframe در وب‌سایت‌ها جاسازی کرد. این کار به شما امکان می‌دهد اپلیکیشن Dify خود را در وب‌سایت، وبلاگ یا هر صفحه وب دیگری ادغام کنید.

هنگامی که از جاسازی دکمه حباب گفتگوی Dify در وب‌سایت خود استفاده می‌کنید، می‌توانید سبک، موقعیت و سایر تنظیمات دکمه را سفارشی کنید.

## سفارشی‌سازی دکمه حباب گفتگوی Dify

دکمه حباب گفتگوی Dify را می‌توان از طریق گزینه‌های پیکربندی زیر سفارشی کرد:

```javascript
window.difyChatbotConfig = {
    // اجباری، به طور خودکار توسط Dify تولید می‌شود
    token: 'YOUR_TOKEN',
    // اختیاری، پیش‌فرض false است
    isDev: false,
    // اختیاری، وقتی isDev برابر true است، پیش‌فرض 'https://dev.udify.app' است، در غیر این صورت پیش‌فرض 'https://udify.app' است
    baseUrl: 'YOUR_BASE_URL',
    // اختیاری، می‌تواند هر ویژگی معتبر HTMLElement به غیر از `id`، مانند `style`، `className` و غیره را بپذیرد
    containerProps: {},
    // اختیاری، اینکه آیا اجازه داده می‌شود دکمه کشیده شود، پیش‌فرض `false` است
    draggable: false,
    // اختیاری، محوری که دکمه اجازه کشیدن در آن را دارد، پیش‌فرض `both` است، می‌تواند `x`، `y`، `both` باشد
    dragAxis: 'both',
    // اختیاری، یک شیء از ورودی‌هایی که در گفتگوی Dify تنظیم شده‌اند
    inputs: {
        // کلید نام متغیر است
        // به عنوان مثال:
        // name: "NAME"
    }
}
```

## نادیده گرفتن سبک‌های پیش‌فرض دکمه

می‌توانید سبک پیش‌فرض دکمه را با استفاده از متغیرهای CSS یا گزینه `containerProps` نادیده بگیرید. این روش‌ها را بر اساس خاص بودن CSS اعمال کنید تا به سفارشی‌سازی مورد نظر خود برسید.

### 1. اصلاح متغیرهای CSS

متغیرهای CSS زیر برای سفارشی‌سازی پشتیبانی می‌شوند:

```css
/* فاصله دکمه تا پایین، پیش‌فرض `1rem` است */
--dify-chatbot-bubble-button-bottom

/* فاصله دکمه تا راست، پیش‌فرض `1rem` است */
--dify-chatbot-bubble-button-right

/* فاصله دکمه تا چپ، پیش‌فرض `unset` است */
--dify-chatbot-bubble-button-left

/* فاصله دکمه تا بالا، پیش‌فرض `unset` است */
--dify-chatbot-bubble-button-top

/* رنگ پس‌زمینه دکمه، پیش‌فرض `#155EEF` است */
--dify-chatbot-bubble-button-bg-color

/* عرض دکمه، پیش‌فرض `50px` است */
--dify-chatbot-bubble-button-width

/* ارتفاع دکمه، پیش‌فرض `50px` است */
--dify-chatbot-bubble-button-height

/* شعاع مرز دکمه، پیش‌فرض `25px` است */
--dify-chatbot-bubble-button-border-radius

/* سایه جعبه دکمه، پیش‌فرض `rgba(0, 0, 0, 0.2) 0px 4px 8px 0px)` است */
--dify-chatbot-bubble-button-box-shadow

/* تبدیل شناور دکمه، پیش‌فرض `scale(1.1)` است */
--dify-chatbot-bubble-button-hover-transform
```

برای تغییر رنگ پس‌زمینه به #ABCDEF، این CSS را اضافه کنید:

```css
#dify-chatbot-bubble-button {
    --dify-chatbot-bubble-button-bg-color: #ABCDEF;
}
```

### 2. استفاده از `containerProps`

سبک‌های inline را با استفاده از ویژگی `style` تنظیم کنید:

```javascript
window.difyChatbotConfig = {
    // ... سایر پیکربندی‌ها
    containerProps: {
        style: {
            backgroundColor: '#ABCDEF',
            width: '60px',
            height: '60px',
            borderRadius: '30px',
        },
        // برای سرریزهای کوچک سبک، می‌توانید از یک مقدار رشته‌ای برای ویژگی `style` نیز استفاده کنید:
        // style: 'background-color: #ABCDEF; width: 60px;',
    },
}
```

کلاس‌های CSS را با استفاده از ویژگی `className` اعمال کنید:

```javascript
window.difyChatbotConfig = {
    // ... سایر پیکربندی‌ها
    containerProps: {
        className: 'dify-chatbot-bubble-button-custom my-custom-class',
    },
}
```

### 3. ارسال `inputs`

چهار نوع ورودی پشتیبانی می‌شوند:

1. **`text-input`**: هر مقداری را می‌پذیرد. اگر طول رشته ورودی از حداکثر طول مجاز فراتر رود، رشته کوتاه می‌شود.
2. **`paragraph`**: مشابه `text-input`، هر مقداری را می‌پذیرد و اگر رشته طولانی‌تر از حداکثر طول باشد، کوتاه می‌شود.
3. **`number`**: یک عدد یا یک رشته عددی را می‌پذیرد. اگر یک رشته داده شود، با استفاده از تابع `Number` به یک عدد تبدیل می‌شود.
4. **`options`**: هر مقداری را می‌پذیرد، به شرطی که با یکی از گزینه‌های پیش‌تنظیم مطابقت داشته باشد.

مثال پیکربندی:

```javascript
window.difyChatbotConfig = {
    // سایر تنظیمات پیکربندی...
    inputs: {
        name: 'apple',
    },
}
```

توجه: هنگام استفاده از اسکریپت embed.js برای ایجاد یک iframe، هر مقدار ورودی پردازش می‌شود — فشرده شده با استفاده از GZIP و رمزگذاری شده در base64 — قبل از الحاق به URL.

به عنوان مثال، URL با مقادیر ورودی پردازش شده به این شکل خواهد بود:
`http://localhost/chatbot/{token}?name=H4sIAKUlmWYA%2FwWAIQ0AAACDsl7gLuiv2PQEUNAuqQUAAAA%3D`
