# انتشار پایدار

انتشار پایدار ابزاری برای تولید تصاویر بر اساس  پیام های متنی است. دیفای رابط کاربری برای دسترسی به API انتشار پایدار را پیاده سازی کرده است، بنابراین می توانید از آن مستقیماً در دیفای استفاده کنید. مراحل زیر برای ادغام انتشار پایدار در دیفای هستند.

## 1. مطمئن شوید که یک دستگاه با GPU دارید
انتشار پایدار برای تولید تصاویر به دستگاهی با GPU نیاز دارد. اما این لازم نیست، می توانید از CPU برای تولید تصاویر استفاده کنید، اما این عمل کند خواهد بود.

## 2. راه اندازی  رابط کاربری  انتشار پایدار
رابط کاربری انتشار پایدار را روی دستگاه یا سرور محلی خود راه اندازی کنید.

### 2.1. مخزن  رابط کاربری انتشار پایدار را کلون کنید
مخزن  رابط کاربری انتشار پایدار را از [مخزن رسمی](https://github.com/AUTOMATIC1111/stable-diffusion-webui) کلون کنید.

```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
```

### 2.2. آن را به صورت محلی راه اندازی کنید
پس از کلون کردن مخزن، باید دایرکتوری را به مخزن کلون شده تغییر داده و دستور زیر را برای راه اندازی  رابط کاربری انتشار پایدار اجرا کنید.

#### ویندوز
```bash
cd stable-diffusion-webui
./webui.bat --api --listen
```

#### لینوکس
```bash
cd stable-diffusion-webui
./webui.sh --api --listen
```

### 2.3. مدل ها را آماده کنید
اکنون می توانید  رابط کاربری انتشار پایدار را در مرورگر خود بر اساس آدرس نمایش داده شده در ترمینال  دسترسی داشته باشید، اما مدل ها هنوز در دسترس نیستند. شما باید مدل ها را از HuggingFace یا منابع دیگر دانلود کرده و آنها را در دایرکتوری `models`  رابط کاربری انتشار پایدار قرار دهید.

برای مثال،  از [pastel-mix](https://huggingface.co/JamesFlare/pastel-mix)  به عنوان مدل استفاده می کنیم،  از  `git lfs`  برای دانلود مدل استفاده کنید و آن را در دایرکتوری `models`  در `stable-diffusion-webui`  قرار دهید.

```bash
git clone https://huggingface.co/JamesFlare/pastel-mix
```

### 2.4. نام مدل را  به دست آورید
اکنون می توانید `pastel-mix`  را در لیست مدل ها مشاهده کنید، اما هنوز باید نام مدل را به دست آورید، به `http://your_id:port/sdapi/v1/sd-models`  مراجعه کنید، نام مدل را مانند زیر مشاهده خواهید کرد.

```json
[
    {
        "title": "pastel-mix/pastelmix-better-vae-fp32.ckpt [943a810f75]",
        "model_name": "pastel-mix_pastelmix-better-vae-fp32",
        "hash": "943a810f75",
        "sha256": "943a810f7538b32f9d81dc5adea3792c07219964c8a8734565931fcec90d762d",
        "filename": "/home/takatost/stable-diffusion-webui/models/Stable-diffusion/pastel-mix/pastelmix-better-vae-fp32.ckpt",
        "config": null
    },
]
```

`model_name`  آن چیزی است که به آن نیاز داریم، در این مورد،  `pastel-mix_pastelmix-better-vae-fp32`  است.

## 3. انتشار پایدار را در دیفای ادغام کنید
اطلاعاتی را که از مراحل قبلی به دست آوردید در `ابزارها > انتشار پایدار > برای مجوز`  پر کنید.

## 4. پایان

- **برنامه های  چت فلو / گردش کار**

هر دو برنامه چت فلو و گردش کار از افزودن گره های ابزار `انتشار پایدار`  پشتیبانی می کنند. پس از اضافه کردن، باید [متغیر](https://docs.dify.ai/v/zh-hans/guides/workflow/variables)  را که به  پیام ورودی  کاربر یا محتوای تولید شده توسط گره قبلی در بخش "متغیرهای ورودی →  پیام"  در داخل گره ارجاع می دهد، پر کنید. در نهایت، از یک متغیر برای ارجاع به خروجی تصویر توسط `انتشار پایدار`  در گره "پایان"  استفاده کنید.

- **برنامه های  عامل**

ابزار `انتشار پایدار`  را در برنامه عامل اضافه کنید، سپس توصیف تصاویر را در کادر گفتگو ارسال کنید تا  ابزار را فعال کنید و تصاویر AI  را تولید کنید.

