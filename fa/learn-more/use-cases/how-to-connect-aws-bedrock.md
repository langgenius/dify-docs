# نحوه اتصال به پایگاه دانش AWS Bedrock؟

این مقاله به طور مختصر نحوه اتصال پلتفرم Dify به پایگاه دانش AWS Bedrock از طریق  [API پایگاه دانش خارجی](https://docs.dify.ai/guides/knowledge-base/external-knowledge-api-documentation) را معرفی می کند، به طوری که برنامه های هوش مصنوعی در پلتفرم Dify می توانند به طور مستقیم محتوای ذخیره شده در پایگاه دانش AWS Bedrock را بدست آورند و کانال های جدید منبع اطلاعات را گسترش دهند.

### آماده سازی اولیه

* پایگاه دانش AWS Bedrock
* سرویس Dify SaaS / نسخه Dify Community
* اصول توسعه API Back-end

### 1. ثبت نام و ایجاد پایگاه دانش AWS Bedrock

از [AWS Bedrock](https://aws.amazon.com/bedrock/) دیدن کرده و سرویس پایگاه دانش را ایجاد کنید.

<figure><img src="../../../en/.gitbook/assets/image (360).png" alt=""><figcaption><p>ایجاد پایگاه دانش AWS Bedrock</p></figcaption></figure>

### 2. ساخت سرویس API Back-end

پلتفرم Dify نمی تواند مستقیماً به پایگاه دانش AWS Bedrock متصل شود. توسعه دهنده باید به  [تعریف API](../../guides/knowledge-base/external-knowledge-api-documentation.md) Dify در مورد اتصال به پایگاه دانش خارجی مراجعه کند، سرویس API Back-end را به طور دستی ایجاد کند و ارتباطی با AWS Bedrock برقرار کند. لطفاً به نمودار معماری خاص مراجعه کنید:

<figure><img src="../../../zh_CN/.gitbook/assets/image (1).png" alt=""><figcaption><p>ساخت سرویس API Back-end</p></figcaption></figure>

شما می توانید به 2 کد دمو زیر مراجعه کنید.

`knowledge.py`

```python
from flask import request
from flask_restful import Resource, reqparse

from bedrock.knowledge_service import ExternalDatasetService


class BedrockRetrievalApi(Resource):
    # url : <your-endpoint>/retrieval
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("retrieval_setting", nullable=False, required=True, type=dict, location="json")
        parser.add_argument("query", nullable=False, required=True, type=str,)
        parser.add_argument("knowledge_id", nullable=False, required=True, type=str)
        args = parser.parse_args()

        # بررسی مجوز
        auth_header = request.headers.get("Authorization")
        if " " not in auth_header:
            return {
                "error_code": 1001,
                "error_msg": "فرمت هدر مجوز نامعتبر است. فرمت مورد انتظار 'Bearer <api-key>' است."
            }, 403
        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != "bearer":
            return {
                "error_code": 1001,
                "error_msg": "فرمت هدر مجوز نامعتبر است. فرمت مورد انتظار 'Bearer <api-key>' است."
            }, 403
        if auth_token:
            # منطق مجوز خود را در اینجا پردازش کنید
            pass

        # فراخوانی سرویس بازیابی دانش
        result = ExternalDatasetService.knowledge_retrieval(
            args["retrieval_setting"], args["query"], args["knowledge_id"]
        )
        return result, 200
```

`knowledge_service.py`

```python
import boto3


class ExternalDatasetService:
    @staticmethod
    def knowledge_retrieval(retrieval_setting: dict, query: str, knowledge_id: str):
        # دریافت کلاینت bedrock
        client = boto3.client(
            "bedrock-agent-runtime",
            aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
            aws_access_key_id="AWS_ACCESS_KEY_ID",
            # مثال: us-east-1
            region_name="AWS_REGION_NAME",
        )
        # دریافت بازیابی دانش خارجی
        response = client.retrieve(
            knowledgeBaseId=knowledge_id,
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": retrieval_setting.get("top_k"), "overrideSearchType": "HYBRID"}
            },
            retrievalQuery={"text": query},
        )
        # تجزیه پاسخ
        results = []
        if response.get("ResponseMetadata") and response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            if response.get("retrievalResults"):
                retrieval_results = response.get("retrievalResults")
                for retrieval_result in retrieval_results:
                    # فیلتر کردن نتایج با نمره کمتر از آستانه
                    if retrieval_result.get("score") < retrieval_setting.get("score_threshold", .0):
                        continue
                    result = {
                        "metadata": retrieval_result.get("metadata"),
                        "score": retrieval_result.get("score"),
                        "title": retrieval_result.get("metadata").get("x-amz-bedrock-kb-source-uri"),
                        "content": retrieval_result.get("content").get("text"),
                    }
                    results.append(result)
        return {
            "records": results
        }
```

در طول فرآیند، شما می توانید آدرس انتهای API و کلید API را برای احراز هویت بسازید و از آنها برای اتصالات بعدی استفاده کنید.

### 3. دریافت شناسه پایگاه دانش AWS Bedrock

پس از ورود به سیستم به پشت صحنه AWS Bedrock Knowledge و دریافت شناسه پایگاه دانش ایجاد شده، می توانید از این پارامتر برای اتصال به پلتفرم Dify در مراحل بعدی استفاده کنید.

<figure><img src="../../../zh_CN/.gitbook/assets/image (359).png" alt=""><figcaption><p>دریافت شناسه پایگاه دانش AWS Bedrock</p></figcaption></figure>

### 4. مرتبط کردن API دانش خارجی

به صفحه **"دانش"** در پلتفرم Dify بروید، روی **"API دانش خارجی"** در گوشه بالا سمت راست کلیک کنید و **"اضافه کردن API دانش خارجی"** را لمس کنید.

دستورالعمل های روی صفحه را دنبال کرده و اطلاعات زیر را پر کنید:

* نام پایگاه دانش. نام های سفارشی مجاز هستند تا API های مختلف دانش خارجی متصل شده به پلتفرم Dify را از هم متمایز کنند.
* آدرس انتهای API، آدرس اتصال به پایگاه دانش خارجی، که می تواند در  [مرحله 2](how-to-connect-aws-bedrock.md#id-2.build-the-backend-api-service) سفارشی شود. مثال: `api-endpoint/retrieval`؛
* کلید API، کلید اتصال به پایگاه دانش خارجی، که می تواند در  [مرحله 2](how-to-connect-aws-bedrock.md#id-2.build-the-backend-api-service) سفارشی شود.

<figure><img src="../../../zh_CN/.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

### 5. اتصال به پایگاه دانش خارجی

به صفحه **“دانش”** بروید، روی **“اتصال به پایگاه دانش خارجی”** در زیر کارت اضافه کردن پایگاه دانش کلیک کنید تا به صفحه پیکربندی پارامترها بروید.

<figure><img src="../../../zh_CN/.gitbook/assets/image (363).png" alt=""><figcaption></figcaption></figure>

پارامترهای زیر را پر کنید:

* **نام و توضیحات پایگاه دانش**
* **API پایگاه دانش خارجی**

API پایگاه دانش خارجی مرتبط شده در مرحله 4 را انتخاب کنید.
* **شناسه پایگاه دانش خارجی**

شناسه پایگاه دانش AWS Bedrock دریافت شده در مرحله 3 را پر کنید.
* **تنظیمات یادآوری را تنظیم کنید**

**Top K:**  هنگامی که کاربر سؤالی می پرسد، از API دانش خارجی خواسته می شود تا محتواهای مرتبط را بازیابی کند. از این پارامتر برای فیلتر کردن بخش های متن با شباهت زیاد به سوالات کاربر استفاده می شود. مقدار پیش فرض 3 است. هرچه این مقدار بیشتر باشد، بخش های متن مرتبط تری بازیابی می شوند.

**آستانه امتیاز:** آستانه شباهت برای فیلتر کردن بخش های متن. فقط بخش های متن با امتیازی که از امتیاز تنظیم شده بیشتر است بازیابی می شوند. مقدار پیش فرض 0.5 است. هر چه این مقدار بیشتر باشد، شباهت مورد نیاز بین متن و سوال بیشتر است، تعداد متن های مورد انتظار برای بازیابی کمتر است و نتیجه دقیق تر خواهد بود.

<figure><img src="../../../zh_CN/.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

پس از تکمیل تنظیمات، می توانید ارتباطی با API پایگاه دانش خارجی برقرار کنید.

### 6. تست اتصال و بازیابی پایگاه دانش خارجی

پس از برقراری ارتباط با پایگاه دانش خارجی، توسعه دهندگان می توانند کلمات کلیدی سوالات احتمالی کاربر را در **"تست بازیابی"** شبیه سازی کرده و پیش نمایش بخش های متن بازیابی شده از پایگاه دانش AWS Bedrock را مشاهده کنند.

<figure><img src="../../../zh_CN/.gitbook/assets/image (366).png" alt=""><figcaption><p>تست اتصال و بازیابی پایگاه دانش خارجی</p></figcaption></figure>

اگر از نتایج بازیابی راضی نیستید، می توانید سعی کنید پارامترهای بازیابی را تغییر دهید یا تنظیمات بازیابی پایگاه دانش AWS Bedrock را تنظیم کنید.

<figure><img src="../../../zh_CN/.gitbook/assets/image (367).png" alt=""><figcaption><p>تنظیم پارامترهای بخش بندی متن پایگاه دانش AWS Bedrock</p></figcaption></figure>


