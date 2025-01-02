# 通过 API 维护标注

> 鉴权、调用方式与App Service API 保持一致。

通过 API 维护标注，可以实现标注的增、删、改、查等操作。提供更加完整的第三方系统集成能力。

## 如何使用

进入工作室，进入应用，在左侧点击访问API。在右上角点击API密钥，然后点击创建密钥。即可获得这个应用专用的密钥。API接口会根据该密钥识别应用。

## API调用示例

### 获取标注列表

```bash
curl --location --request GET 'https://api.dify.ai/v1/apps/annotations?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

输出示例：

```json
{
  "data": [
    {
      "id": "69d48372-ad81-4c75-9c46-2ce197b4d402",
      "question": "What is your name?",
      "answer": "I am Dify.",
      "hit_count": 0,
      "created_at": 1735625869
    }
  ],
  "has_more": false,
  "limit": 20,
  "total": 1,
  "page": 1
}
```

### 创建标注

```bash
curl --location --request POST 'https://api.dify.ai/v1/apps/annotations' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "What is your name?",
    "answer": "I am Dify."
}'
```

输出示例：

```json
{
  "id": "69d48372-ad81-4c75-9c46-2ce197b4d402",
  "question": "What is your name?",
  "answer": "I am Dify.",
  "hit_count": 0,
  "created_at": 1735625869
}
```

### 更新标注

```bash
curl --location --request PUT 'https://api.dify.ai/v1/apps/annotations/{annotation_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "What is your name?",
    "answer": "I am Dify."
}'
```

输出示例：

```json
{
  "id": "69d48372-ad81-4c75-9c46-2ce197b4d402",
  "question": "What is your name?",
  "answer": "I am Dify.",
  "hit_count": 0,
  "created_at": 1735625869
}
```

### 删除标注

```bash
curl --location --request DELETE 'https://api.dify.ai/v1/apps/annotations/{annotation_id}' \
--header 'Authorization: Bearer {api_key}'
```

输出示例：

```json
{"result": "success"}
```

### 标注回复初始设置

```bash
curl --location --request POST 'https://api.dify.ai/v1/apps/annotation-reply/{action}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "score_threshold": 0.9,
    "embedding_provider_name": "zhipu",
    "embedding_model_name": "embedding_3"
}'
```

入参说明：
- `action`： 只能是enable或者disable
- `embedding_model_provider`: 指定的嵌入模型提供商, 必须先在系统内设定好接入的模型，对应的是provider字段
- `embedding_model`: 指定的嵌入模型，对应的是model字段
- `retrieval_model`: 指定的检索模型，对应的是model字段

嵌入模型的提供商和模型名称可以通过以下接口获取：`v1/workspaces/current/models/model-types/text-embedding`，
具体见：[通过 API 维护知识库](guides/knowledge-base/maintain-dataset-via-api.md)。
使用的Authorization是Dataset的API Token

输出示例：

```json
{
  "job_id": "b15c8f68-1cf4-4877-bf21-ed7cf2011802",
  "job_status": "waiting"
}
```
该接口是异步执行，所以会返回一个job_id，通过查询job状态接口可以获取到最终的执行结果。

### 查询标注回复初始设置任务状态

```bash
curl --location --request GET 'https://api.dify.ai/v1/apps/annotation-reply/{action}/status/{job_id}' \
--header 'Authorization: Bearer {api_key}'
```

输出示例：

```json
{
  "job_id": "b15c8f68-1cf4-4877-bf21-ed7cf2011802",
  "job_status": "waiting",
  "error_msg": ""
}
```