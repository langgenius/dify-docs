# Maintain Annotations via API

> Authentication and invocation methods are consistent with the App Service API.

Maintaining annotations via API allows for operations such as adding, deleting, updating, and querying annotations. This provides more comprehensive third-party system integration capabilities.

## How to Use

Enter the workspace, go to the application, and click on Access API on the left side. Click on API Key in the upper right corner, then click Create Key. This will give you a key specific to this application. The API interface will recognize the application based on this key.

## API Call Examples

### Get Annotation List

```bash
curl --location --request GET 'https://api.dify.ai/v1/apps/annotations?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

Output Example:

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

### Create Annotation

```bash
curl --location --request POST 'https://api.dify.ai/v1/apps/annotations' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "What is your name?",
    "answer": "I am Dify."
}'
```

Output Example:

```json
{
  "id": "69d48372-ad81-4c75-9c46-2ce197b4d402",
  "question": "What is your name?",
  "answer": "I am Dify.",
  "hit_count": 0,
  "created_at": 1735625869
}
```

### Update Annotation

```bash
curl --location --request PUT 'https://api.dify.ai/v1/apps/annotations/{annotation_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "What is your name?",
    "answer": "I am Dify."
}'
```

Output Example:

```json
{
  "id": "69d48372-ad81-4c75-9c46-2ce197b4d402",
  "question": "What is your name?",
  "answer": "I am Dify.",
  "hit_count": 0,
  "created_at": 1735625869
}
```

### Delete Annotation

```bash
curl --location --request DELETE 'https://api.dify.ai/v1/apps/annotations/{annotation_id}' \
--header 'Authorization: Bearer {api_key}'
```

Output Example:

```json
{"result": "success"}
```

### Initial Annotation Reply Settings

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

Parameter Description:
- `action`: Can only be `enable` or `disable`
- `embedding_model_provider`: Specified embedding model provider, must be set up in the system first, corresponding to the provider field
- `embedding_model`: Specified embedding model, corresponding to the model field
- `retrieval_model`: Specified retrieval model, corresponding to the model field

The provider and model name of the embedding model can be obtained through the following interface: `v1/workspaces/current/models/model-types/text-embedding`. For specific instructions, see: [Maintain Knowledge Base via API](guides/knowledge-base/maintain-dataset-via-api.md). The Authorization used is the Dataset API Token.

Output Example:

```json
{
  "job_id": "b15c8f68-1cf4-4877-bf21-ed7cf2011802",
  "job_status": "waiting"
}
```
This interface is executed asynchronously, so it will return a job_id. You can get the final execution result by querying the job status interface.

### Query Initial Annotation Reply Settings Task Status

```bash
curl --location --request GET 'https://api.dify.ai/v1/apps/annotation-reply/{action}/status/{job_id}' \
--header 'Authorization: Bearer {api_key}'
```

Output Example:

```json
{
  "job_id": "b15c8f68-1cf4-4877-bf21-ed7cf2011802",
  "job_status": "waiting",
  "error_msg": ""
}
```