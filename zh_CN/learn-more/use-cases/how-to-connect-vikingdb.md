# 如何连接 火山 VikingDB 知识库？

## 1. 概览
当下数字化时代，数据整合对提升 AI 应用效能极为关键。本文将详细说明如何利用外部知识库 API，把 Dify 平台和火山 VikingDB 知识库连接起来。连接完成后，Dify 平台的 AI 应用便能迅速获取火山 VikingDB 知识库中的丰富内容，拓宽信息来源，助力其在智能服务方面实现显著提升 。

### 前置准备

### 1. 注册火山账号并开通 VikingDB 知识库服务
访问 [火山引擎](https://www.volcengine.com/) 并登录，进入[VikingDB知识库](https://console.volcengine.com/vikingdb/knowledge/region:vdb-knowledge+cn-beijing)
<figure><img src="../../.gitbook/assets/vikingdb-image-1.png" alt=""><figcaption><p>开通火山 VikingDB 知识库</p></figcaption></figure>

### 2. 构建后端 API 服务

火山 VikingDB 知识库提供的[检索接口](https://www.volcengine.com/docs/84313/1350012) 和 Dify 定义的[外部数据库 API 定义](../../guides/knowledge-base/external-knowledge-api-documentation.md)不完全适配，需要开发团队人工维护 API 服务，包装 火山 VikingDB 知识库提供的检索接口，再建立与 Dify 的连接。

##### 火山 VikingDB 知识库检索 API 与 Dify 外部知识库 API 的映射
###### 请求参数

| Dify 属性 | VikingDB 属性 | 是否必需 | 类型 | 描述 | 示例值 |
|----------|---------------|--------|------|------|------|
| knowledge_id | name | 是 | 字符串 | 知识库唯一 ID | AAA-BBB-CCC |
| query | query | 是 | 字符串 | 用户的查询 | Dify 是什么？ |
| retrieval_setting | --- | 是 | 对象 | 知识检索参数 | 见下文 |

`retrieval_setting` 映射如下：

| Dify 属性 | VikingDB 属性 | 是否必需 | 类型 | 描述 | 示例值 |
|------|---|------|------|------|--------|
| top_k | limit | 是 | 整数 | 检索结果的最大数量 | 5 |
| score_threshold | --- | 是 | 浮点数 | 结果与查询相关性的分数限制，范围：0~1 | 0.5 |
> VikingDB 知识库检索接口没有 score_threshold 参数，返回的切片是按 score 倒序排序的，为适配 Dify 协议，需要手动过滤。

###### 响应消息

| Dify属性 | VikingDB 属性 | 是否必需 | 类型 | 描述 | 示例值 |
|------|---|-------|------|------|--------|
| records | data.result_list | 是 | 对象列表 | 从知识库查询的记录列表 | 见下文 |

`records` 属性是一个包含以下键的对象列表：

| Dify 属性 | VikingDB 属性 | 是否必需 | 类型 | 描述 | 示例值 |
|------|---|-------|------|------|--------|
| content | content | 是 | 字符串 | 包含知识库中数据源的文本块 | Dify：GenAI 应用程序的创新引擎 |
| score | score | 是 | 浮点数 | 结果与查询的相关性分数，范围：0~1 | 0.5 |
| title | chunk_title | 是 | 字符串 | 文档标题 | Dify 简介 |
| metadata | doc_info | 否 | json | 包含数据源中文档的元数据属性及其值 | 见示例 |
> VikingDB 检索接口返回的切片包含切片标题和原文本标题，切片标题对应字段为 chunk_title，原文档标题对应字段在 doc_info 元信息中的 title 字段。

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
>火山 VikingDB 知识库 API [签名鉴权方式](https://www.volcengine.com/docs/84313/1254485)
> 
> 示例中基于 Python SDK 生成签名。
> 安装火山引擎程序包: _pip install volcengine_

```python
from volcengine.viking_knowledgebase import VikingKnowledgeBaseService


viking_knowledgebase_service = VikingKnowledgeBaseService(host="api-knowledgebase.mlp.cn-beijing.volces.com", scheme="https", connection_timeout=30, socket_timeout=30)
viking_knowledgebase_service.set_ak("自己的ak")
viking_knowledgebase_service.set_sk("自己的sk")

class ExternalDatasetService:
    @staticmethod
    def knowledge_retrieval(retrieval_setting: dict, query: str, knowledge_id: str):
        top_k = retrieval_setting.get("top_k")
        res = viking_knowledgebase_service.search_knowledge(collection_name=knowledge_id, query=query, limit=top_k)
        result_list = res["result_list"]
        if len(result_list) <= top_k:
            top_result = result_list
        else:
            top_result = result_list[:top_k]
        # parse response
        results = []

        for retrieval_result in top_result:
            # filter out results with score less than threshold
            if retrieval_result.get("score") < retrieval_setting.get("score_threshold", .0):
                continue
            result = {
                "metadata": retrieval_result.get("doc_info"),
                "score": retrieval_result.get("score"),
                "title": retrieval_result.get("chunk_title"), # chunk title
                "content": retrieval_result.get("content"),
            }
            results.append(result)
        return {
            "records": results
        }
```
> 在该示例中，Dify 传递的 knowledge_id 实际作为火山 VikingDB 知识库中的知识库名，默认 project 为 default，可以根据自身需要调整代码。

### 3. 获取火山 VikingDB 知识库 Knowledge Base ID

登录 VikingDB 知识库，获取已创建知识库名。此参数将会在[后续步骤](how-to-connect-vikingdb.md#id-5.-lian-jie-wai-bu-zhi-shi-ku)用于与 Dify 平台的连接。

<figure><img src="../../.gitbook/assets/vikingdb-image-2.png" alt=""><figcaption><p>获取火山 VikingDB Knowledge Collection Name</p></figcaption></figure>

### 4. 关联外部知识 API

前往 Dify 平台中的 **“知识库”** 页，点击右上角的 **“外部知识库 API”**，轻点 **“添加外部知识库 API”**。

按照页面提示，依次填写以下内容：

* 知识库的名称，允许自定义名称，用于区分 Dify 平台内所连接的不同外部知识 API；
* API 接口地址，外部知识库的连接地址，可在[第二步](how-to-connect-vikingdb.md#id-2.-gou-jian-hou-duan-api-fu-wu)中自定义。示例 `api-endpoint/retrieval`；
* API Key，外部知识库连接密钥，可在[第二步](how-to-connect-vikingdb.md#id-2.-gou-jian-hou-duan-api-fu-wu)中自定义。

<figure><img src="../../.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

### 5. 连接外部知识库

前往 **“知识库”** 页，点击添加知识库卡片下方的 **“连接外部知识库”** 跳转至参数配置页面。

<figure><img src="../../.gitbook/assets/image (363).png" alt=""><figcaption></figcaption></figure>

填写以下参数：

* **知识库名称与描述**
*   **外部知识库 API**

    选择在[第四步](how-to-connect-vikingdb.md#id-4.-guan-lian-wai-bu-zhi-shi-api)中关联的外部知识库 API
*   **外部知识库 ID**

    填写在[第三步](how-to-connect-vikingdb.md#id-3.-huo-qu-vikingdb-knowledge-base-id)中获取的火山 VikingDB Knowledge Collection Name
*   **调整召回设置**

    **Top K**：用户发起提问时，将请求外部知识 API 获取相关性较高的内容分段。该参数用于筛选与用户问题相似度较高的文本片段。默认值为 3，数值越高，召回存在相关性的文本分段也就越多。

    **Score 阈值**：文本片段筛选的相似度阈值，只召回超过设置分数的文本片段，默认值为 0.5。数值越高说明对于文本与问题要求的相似度越高，预期被召回的文本数量也越少，结果也会相对而言更加精准。

<figure><img src="../../.gitbook/assets/vikingdb-image-3.png" alt=""><figcaption></figcaption></figure>

设置完成后即可建立与外部知识库 API 的连接。

### 6. 测试外部知识库连接与召回

建立与外部知识库的连接后，开发者可以在 **“召回测试”** 中模拟可能的问题关键词，预览从火山 VikingDB 知识库召回的文本分段。

<figure><img src="../../.gitbook/assets/vikingdb-image-4.png" alt=""><figcaption><p>测试外部知识库的连接与召回</p></figcaption></figure>

若对于召回结果不满意，可以根据[召回接口](https://www.volcengine.com/docs/84313/1350012)尝试在代码中修改召回参数，当前 VikingDB 知识库还未提供固化召回参数的实体概念（敬请期待）。

### 7. 应用案例：基于豆包模型 + VikingDB 知识库构建聊天 bot

在建立好外部知识库后，可以在 **“工作室”** 中使用豆包模型和上面建立的外部 VikingDB 知识库构建聊天机器人。

<figure><img src="../../.gitbook/assets/vikingdb-image-5.png" alt=""><figcaption><p>集成聊天机器人</p></figcaption></figure>