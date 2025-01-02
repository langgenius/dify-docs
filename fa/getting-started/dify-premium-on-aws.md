# Dify Premium در AWS

Dify Premium پیشنهاد AMI ما در AWS است که به شما اجازه می‌دهد برندینگ سفارشی داشته باشید و با یک کلیک قابل نصب در VPC AWS شما به عنوان یک EC2 است. برای اشتراک به [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-t22mebxzwjhu6) مراجعه کنید. این در چندین سناریو مفید است:

* شما به دنبال ایجاد یک یا چند برنامه به عنوان یک کسب و کار کوچک/متوسط هستید و به اقامت داده ها اهمیت می دهید.
* شما به [Dify Cloud](cloud.md) علاقه مند هستید، اما مورد استفاده شما به منابع بیشتری نسبت به آنچه در [برنامه ها](https://dify.ai/pricing) پشتیبانی می شود، نیاز دارد.
* شما می خواهید قبل از پذیرش Dify Enterprise در سازمان خود، یک POC اجرا کنید.

### تنظیم

اگر این اولین باری است که به Dify دسترسی پیدا می کنید، برای شروع فرآیند راه اندازی، رمز عبور راه اندازی Admin (که به ID نمونه EC2 شما تنظیم شده است) را وارد کنید.

پس از استقرار AMI، از طریق IP عمومی نمونه (که در کنسول EC2 یافت می شود) به Dify دسترسی پیدا کنید (به طور پیش فرض از پورت HTTP 80 استفاده می شود).

### ارتقا

در نمونه EC2، دستورات زیر را اجرا کنید:

```
git clone https://github.com/langgenius/dify.git /tmp/dify
mv -f /tmp/dify/docker/* /dify/
rm -rf /tmp/dify
docker-compose down
docker-compose pull
docker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d
```

### سفارشی سازی

مانند استقرار خود میزبانی، می توانید متغیرهای محیطی را در `.env` در نمونه EC2 خود به دلخواه تغییر دهید. سپس Dify را با:

```
docker-compose down
ocker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d
```
 
 مجددا راه اندازی کنید. 
