# AWS Bedrock Knowledge Baseに統合する方法

本文では、外部ナレッジベースAPIを利用して、DifyプラットフォームとAWS Bedrock Knowledge Baseを接続する方法を簡潔に紹介します。この接続により、Difyプラットフォーム内のAIアプリケーションは、AWS Bedrock Knowledge Baseに保存されているコンテンツを直接取得でき、新たな情報源を拡充することが可能となります。

### 準備

* AWS Bedrock Knowledge Base
* DifyのSaaSサービス / Dify コミュニティ版
* バックエンドAPI開発の基礎知識

### 1. AWS Bedrock Knowledge Baseの登録と作成

[AWS Bedrock](https://aws.amazon.com/bedrock/)にアクセスし、ナレッジベースサービスを作成してください。

<figure><img src="../../../zh_CN/.gitbook/assets/image (360).png" alt=""><figcaption><p>AWS Bedrock Knowledge Baseを作成</p></figcaption></figure>

### 2. バックエンドAPIサービスの構築

Difyプラットフォームは、直接的にAWS Bedrock Knowledge Baseに接続することができません。開発チームは、Difyの外部ナレッジベース接続に関する[API定義](../../guides/knowledge-base/external-knowledge-api-documentation.md)を参照し、バックエンドAPIサービスを手動で構築してAWS Bedrockと接続する必要があります。具体的なアーキテクチャの概要は以下の通りです：

<figure><img src="../../../zh_CN/.gitbook/assets/image.png" alt=""><figcaption><p>バックエンドAPIサービスの構築</p></figcaption></figure>

以下の2つのコードファイルを参考にして、バックエンドサービスAPIを構築できます。

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

このプロセスでは、APIエンドポイントの構築と認証用のAPIキーの生成が行われます。

### 3. AWS Bedrock Knowledge BaseのIDの取得

AWS Bedrockの管理画面にログインし、作成したナレッジベースのIDを取得します。このパラメータは、Difyプラットフォームとの接続に使用されます。

<figure><img src="../../../zh_CN/.gitbook/assets/image (359).png" alt=""><figcaption><p>AWS Bedrock Knowledge BaseのIDを取得</p></figcaption></figure>

### 4. 外部知識APIの関連付け

Difyプラットフォームの**"ナレッジベース"**ページに移動し、右上の**"外部ナレッジベースAPI"**をクリックし、**"外部ナレッジベースAPIを追加"**を選択します。

ページの指示に従い、以下の内容を順番に入力します：

- ナレッジベースの名称（カスタマイズ可能で、Difyプラットフォーム内の異なる外部知識APIを区別するために使用）
- APIエンドポイント（外部ナレッジベースへの接続アドレス、2ステップ目でカスタマイズ可能）。例：`api-endpoint/retrieval`
- APIキー（外部ナレッジベースへの接続キー、2ステップ目でカスタマイズ可能）

<figure><img src="../../../zh_CN/.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

### 5. 外部ナレッジベースの接続

**"ナレッジベース"**ページに移動し、ナレッジベースのカードの下にある**"外部ナレッジベースを接続"**をクリックして、パラメータ設定ページに移動します。

以下のパラメータを入力してください：

* **ナレッジベースの名称と説明**
* **外部知識API**

  4ステップで関連付けた外部ナレッジベースAPIを選択

* **外部ナレッジベースID**

  3ステップで取得したAWS Bedrock Knowledge BaseIDを入力

* **検索設定の調整**

  **Top K:** ユーザーが質問をした際に、関連性の高いコンテンツセグメントを取得するために外部知識APIにリクエストを送ります。このパラメータは、ユーザーの質問に類似したテキストセグメントを選ぶために使用されます。デフォルト値は3で、値が大きいほど関連性の高いテキストセグメントが取得されます。

  **スコア閾値:** テキストセグメントの選択に使用される類似度の閾値です。設定されたスコアを超えるテキストセグメントのみが取得され、デフォルト値は0.5です。数値が高くなるほど、テキストと質問の類似度が高く、取得されるテキストの数は減少し、結果もより精度が高くなります。

<figure><img src="../../../zh_CN/.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

設定が完了すると、外部ナレッジベースAPIとの接続が確立されます。

### 6. 外部ナレッジベースの接続と検索のテスト

外部ナレッジベースとの接続が確立された後、開発者は**"テスト取得"**で可能な質問のキーワードをシミュレートし、AWS Bedrock Knowledge Baseから取得したテキストセグメントをプレビューできます。

<figure><img src="../../../zh_CN/.gitbook/assets/image (366).png" alt=""><figcaption><p>外部データベースの接続と検索をテスト</p></figcaption></figure>

検索結果に満足できない場合は、検索設定を変更したり、AWS Bedrock Knowledge Baseの検索設定を調整したりすることができます。

<figure><img src="../../../zh_CN/.gitbook/assets/image (367).png" alt=""><figcaption><p>调整 AWS Bedrock Knowledge Base の検索設定を調整</p></figcaption></figure>
