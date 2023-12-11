# Maintain Knowledge via API

> Authentication, invocation method and application Service API remain consistent. The difference is that a knowledge API token can operate on all knowledge bases.

### Benefits of Using the Knowledge API
* Sync your data systems to Dify knowledge to create powerful workflows.
* Provide knowledge list and document list APIs as well as detail query interfaces, to facilitate building your own data management page.
* Support both plain text and file uploads/updates documents, as well as batch additions and modifications, to simplify your sync process.
* Reduce manual document handling and syncing time, improving visibility of Dify's software and services.

### How to use

Please go to the knowledge page, you can switch tap to the API page in the navigation on the left side. On this page, you can view the API documentation provided by Dify and manage credentials for accessing the Knowledge API.

<figure><img src="../../.gitbook/assets/dataset-api-token.png" alt=""><figcaption><p>Knowledge API Document</p></figcaption></figure>

## **Create Empty Knowledge**

**`POST /datasets`**

{% hint style="warning" %}
Used only to create an empty dataset
{% endhint %}

```
curl --location --request POST 'https://api.dify.ai/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name"}'

```

#### **List of Knowledge**


```
curl --location --request GET 'https://api.dify.ai/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'

```

#### **Create A Document From Text**

```
curl --location --request POST '<https://api.dify.ai/v1/datasets/<uuid:dataset_id>/document/create_by_text>' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "name": "Dify",
    "text": "Dify means Do it for you...",
    "indexing_technique": "high_quality",
    "process_rule": {
        "rules": {
                "pre_processing_rules": [{
                        "id": "remove_extra_spaces",
                        "enabled": true
                }, {
                        "id": "remove_urls_emails",
                        "enabled": true
                }],
                "segmentation": {
                        "separator": "###",
                        "max_tokens": 500
                }
        },
        "mode": "custom"
    }
}'

```

#### **Create A Document From File**

```
curl --location POST 'https://api.dify.ai/v1/datasets/{dataset_id}/document/create_by_file' \
--header 'Authorization: Bearer {api_key}' \
--form 'data="{
	"name": "Dify",
	"indexing_technique": "high_quality",
	"process_rule": {
		"rules": {
			"pre_processing_rules": [{
				"id": "remove_extra_spaces",
				"enabled": true
			}, {
				"id": "remove_urls_emails",
				"enabled": true
			}],
			"segmentation": {
				"separator": "###",
				"max_tokens": 500
			}
		},
		"mode": "custom"
	}
    }";
    type=text/plain' \
--form 'file=@"/path/to/file"'

```

#### **Get Document Embedding Status**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```


#### **Delete Document**

```
curl --location --request DELETE 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### **Get Document List**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'

```

#### **Add New Segment**

```
curl 'https://api.dify.ai/v1/datasets/aac47674-31a8-4f12-aab2-9603964c4789/documents/2034e0c1-1b75-4532-849e-24e72666595b/segment' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw $'"segments":[
  {"content":"Dify means Do it for you",
  "keywords":["Dify","Do"]
  }
  ]'
  --compressed

```


### Error Message

- `document_indexing`，document is in indexing status
- `provider_not_initialize`， Embedding model is not configured
- `not_found`，document not exist
- `dataset_name_duplicate` ，have existing knowledge name
- `provider_quota_exceeded`，The model quota has exceeded the limit
- `dataset_not_initialized`，The knowledge has not been initialized
- `unsupported_file_type`，Unsupported file type
    - support file type：txt, markdown, md, pdf, html, htm, xlsx, docx, csv
- `too_many_files`，The number of files is too large, and only single file upload is temporarily supported
- `file_too_large`，The file is too large, supporting files under 15M