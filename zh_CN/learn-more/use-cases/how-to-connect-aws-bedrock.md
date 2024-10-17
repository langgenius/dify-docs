# 如何连接 AWS Bedrock 知识库？

本文将简要介绍如何通过外部知识库 API 将 Dify 平台与 AWS Bedrock 知识库相连接，使得 Dify 平台内的 AI 应用能够直接获取存储在 AWS Bedrock 知识库中的内容，扩展新的信息来源渠道。

### 前置准备

* AWS Bedrock Knowledge Base
* Dify SaaS 服务 / Dify 社区版
* 后端 API 开发基础知识

### 1. 注册并创建 AWS Bedrock Knowledge Base

访问 [AWS Bedrock](https://aws.amazon.com/bedrock/)，创建 Knowledge Base 服务。

<figure><img src="../../.gitbook/assets/image (360).png" alt=""><figcaption><p>创建 AWS Bedrock Knowledge Base</p></figcaption></figure>

### 2. 构建后端 API 服务

Dify 平台尚不能直接连接 AWS Bedrock Knowledge Base，需要开发团队参考 Dify 关于外部知识库连接的 [API 定义](../../guides/knowledge-base/external-knowledge-api-documentation.md)，手动创建后端 API 服务，建立与 AWS Bedrock 的连接。具体架构示意图请参考：

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption><p>构建后端 API 服务</p></figcaption></figure>

你可以参考以下 2 个代码文件，构建后端服务 API。

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

        # Authorization check
        auth_header = request.headers.get("Authorization")
        if " " not in auth_header:
            return {
                "error_code": 1001,
                "error_msg": "Invalid Authorization header format. Expected 'Bearer <api-key>' format."
            }, 403
        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != "bearer":
            return {
                "error_code": 1001,
                "error_msg": "Invalid Authorization header format. Expected 'Bearer <api-key>' format."
            }, 403
        if auth_token:
            # process your authorization logic here
            pass

        # Call the knowledge retrieval service
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
        # get bedrock client
        client = boto3.client(
            "bedrock-agent-runtime",
            aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
            aws_access_key_id="AWS_ACCESS_KEY_ID",
            # example: us-east-1
            region_name="AWS_REGION_NAME",
        )
        # fetch external knowledge retrieval
        response = client.retrieve(
            knowledgeBaseId=knowledge_id,
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": retrieval_setting.get("top_k"), "overrideSearchType": "HYBRID"}
            },
            retrievalQuery={"text": query},
        )
        # parse response
        results = []
        if response.get("ResponseMetadata") and response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            if response.get("retrievalResults"):
                retrieval_results = response.get("retrievalResults")
                for retrieval_result in retrieval_results:
                    # filter out results with score less than threshold
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

在此过程中，你可以构建 API 接口地址以及用于鉴权的 API Key 并用于后续的连接。

### 3. 获取 AWS Bedrock Knowledge Base ID

登录 AWS Bedrock Knowledge 后台，获取已创建 Knowledge Base 的 ID。此参数将会在[后续步骤](how-to-connect-aws-bderock.md#id-5.-lian-jie-wai-bu-zhi-shi-ku)用于与 Dify 平台的连接。

<figure><img src="../../.gitbook/assets/image (359).png" alt=""><figcaption><p>获取 AWS Bedrock Knowledge Base ID</p></figcaption></figure>

### 4. 关联外部知识 API

前往 Dify 平台中的 **“知识库”** 页，点击右上角的 **“外部知识库 API”**，轻点 **“添加外部知识库 API”**。

按照页面提示，依次填写以下内容：

* 知识库的名称，允许自定义名称，用于区分 Dify 平台内所连接的不同外部知识 API；
* API 接口地址，外部知识库的连接地址，可在[第二步](how-to-connect-aws-bderock.md#id-2.-gou-jian-hou-duan-api-fu-wu)中自定义。示例 `api-endpoint/retrieval`；
* API Key，外部知识库连接密钥，可在[第二步](how-to-connect-aws-bderock.md#id-2.-gou-jian-hou-duan-api-fu-wu)中自定义。

<figure><img src="../../.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

### 5.  连接外部知识库

前往 **“知识库”** 页，点击添加知识库卡片下方的 **“连接外部知识库”** 跳转至参数配置页面。

<figure><img src="../../.gitbook/assets/image (363).png" alt=""><figcaption></figcaption></figure>

填写以下参数：

* **知识库名称与描述**
*   **外部知识库 API**&#x20;

    选择在[第四步](how-to-connect-aws-bderock.md#id-4.-guan-lian-wai-bu-zhi-shi-api)中关联的外部知识库 API
*   **外部知识库 ID**&#x20;

    &#x20;填写在[第三步](how-to-connect-aws-bderock.md#id-3.-huo-qu-aws-bedrock-knowledge-base-id)中获取的 AWS Bedrock knowledge base ID
*   **调整召回设置**

    **Top K：**用户发起提问时，将请求外部知识 API 获取相关性较高的内容分段。该参数用于筛选与用户问题相似度较高的文本片段。默认值为 3，数值越高，召回存在相关性的文本分段也就越多。

    **Score 阈值：**文本片段筛选的相似度阈值，只召回超过设置分数的文本片段，默认值为 0.5。数值越高说明对于文本与问题要求的相似度越高，预期被召回的文本数量也越少，结果也会相对而言更加精准。

<figure><img src="../../.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

设置完成后即可建立与外部知识库 API 的连接。

### 6. 测试外部知识库连接与召回

建立与外部知识库的连接后，开发者可以在 **“召回测试”** 中模拟可能的问题关键词，预览从 AWS Bedrock Knowledge Base 召回的文本分段。

<figure><img src="../../.gitbook/assets/image (366).png" alt=""><figcaption><p>测试外部知识库的连接与召回</p></figcaption></figure>

若对于召回结果不满意，可以尝试修改召回参数或自行调整 AWS Bedrock Knowledge Base 的检索设置。

<figure><img src="../../.gitbook/assets/image (367).png" alt=""><figcaption><p>调整 AWS Bedrock Knowledge Base 文本处理参数</p></figcaption></figure>
