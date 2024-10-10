# How to connect with AWS Bedrock Knowledge Base？

This article will briefly introduce how to connect the Dify platform with the AWS Bedrock knowledge base through the external knowledge base API, so that AI applications in the Dify platform can directly obtain content stored in the AWS Bedrock knowledge base and expand new information source channels.

### Pre-preparation

* AWS Bedrock Knowledge Base
* Dify SaaS Service / Dify Community Version
* Backend API Development Basics

### 1. Register and create AWS Bedrock Knowledge Base

Visit [AWS Bedrock](https://aws.amazon.com/bedrock/) and create the Knowledge Base service.

<figure><img src="../../../en/.gitbook/assets/image (360).png" alt=""><figcaption><p>Create AWS Bedrock Knowledge Base</p></figcaption></figure>

### 2. Build the backend API service

The Dify platform cannot directly connect to AWS Bedrock Knowledge Base. The development team needs to refer to Dify's [API definition](../../guides/knowledge-base/external-knowledge-api-documentation.md) on external knowledge base connection, manually create the backend API service, and establish a connection with AWS Bedrock. Please refer to the specific architecture diagram:

<figure><img src="../../../en/.gitbook/assets/image.png" alt=""><figcaption><p>Build the backend API service</p></figcaption></figure>

You can refer to the following 2 code.


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

During this process, you can construct the API interface address and the API Key for authentication and use them for subsequent connections.

### 3. Get the AWS Bedrock Knowledge Base ID

After log in to the AWS Bedrock Knowledge backend and get the ID of the created Knowledge Base, you can use this parameter to connect to the Dify platform in the [subsequent steps](how-to-connect-aws-bedrock.md#id-5.-lian-jie-wai-bu-zhi-shi-ku).

<figure><img src="../../../zh_CN/.gitbook/assets/image (359).png" alt=""><figcaption><p>Get the AWS Bedrock Knowledge Base ID</p></figcaption></figure>

### 4. Associate the external knowledge API

Go to the **"Knowledge Base"** page in the Dify platform, click **"External Knowledge Base API"** in the upper right corner, and tap **"Add External Knowledge Base API"**.

Follow the prompts on the page and fill in the following information:

* The name of the knowledge base. Custom names are allowed to distinguish different external knowledge APIs connected to the Dify platform;
* API interface address, the connection address of the external knowledge base, which can be customized in [Step 2](how-to-connect-aws-bedrock.md#id-2.-gou-jian-hou-duan-api-fu-wu). Example `api-endpoint/retrieval`;
* API Key, the external knowledge base connection key, which can be customized in [Step 2](how-to-connect-aws-bedrock.md#id-2.-gou-jian-hou-duan-api-fu-wu).

<figure><img src="../../../zh_CN/.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

### 5. Connect to external knowledge base

Go to the **“Knowledge base”** page, click **“Connect to external knowledge base”** below the add knowledge base card to jump to the parameter configuration page.

<figure><img src="../../../zh_CN/.gitbook/assets/image (363).png" alt=""><figcaption></figcaption></figure>

Fill in the following parameters:

* **Knowledge base name and description**
* **External knowledge base API**&#x20;

Select the external knowledge base API associated in [Step 4](how-to-connect-aws-bedrock.md#id-4.-guan-lian-wai-bu-zhi-shi-api)
* **External knowledge base ID**&#x20;

&#x20;Fill in the AWS Bedrock knowledge base ID obtained in [Step 3](how-to-connect-aws-bedrock.md#id-3.-huo-qu-aws-bedrock-knowledge-base-id)
* **Adjust recall settings**

**Top K:** When a user asks a question, the external knowledge API will be requested to obtain the most relevant content segments. This parameter is used to filter text segments with high similarity to user questions. The default value is 3. The higher the value, the more relevant text segments will be recalled.

**Score threshold: **The similarity threshold for text segment filtering. Only text segments with a score exceeding the set score will be recalled. The default value is 0.5. The higher the value, the higher the similarity required between the text and the question, the smaller the number of texts expected to be recalled, and the more accurate the result will be.

<figure><img src="../../../zh_CN/.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

After the settings are completed, you can establish a connection with the external knowledge base API.

### 6. Test external knowledge base connection and recall

After establishing a connection with an external knowledge base, developers can simulate possible question keywords in **"Recall Test"** and preview the text segments recalled from AWS Bedrock Knowledge Base.

<figure><img src="../../../zh_CN/.gitbook/assets/image (366).png" alt=""><figcaption><p>Test the connection and recall of the external database</p></figcaption></figure>

If you are not satisfied with the recall results, you can try to modify the recall parameters or adjust the search settings of AWS Bedrock Knowledge Base yourself.

<figure><img src="../../../zh_CN/.gitbook/assets/image (367).png" alt=""><figcaption><p>Adjust the text processing parameters of AWS Bedrock Knowledge Base</p></figcaption></figure>