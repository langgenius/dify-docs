# Maintaining Datasets via API

> Authentication and invocation methods are consistent with the application Service API. The difference is that a single dataset API token can operate on all datasets.

### Advantages of Using Dataset API

* Synchronize your data system with Dify datasets to create powerful workflows.
* Provide dataset list, document list, and detail queries to facilitate building your own data management page.
* Support both plain text and file uploads and updates for documents, and support batch addition and modification at the segment level to streamline your synchronization process.
* Reduce the time spent on manual document processing and synchronization, enhancing your visibility into Dify's software and services.

### How to Use

Navigate to the dataset page, and you can switch to the **API** page from the left navigation. On this page, you can view the dataset API documentation provided by Dify and manage the credentials for accessing the dataset API in **API Keys**.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/dataset-api-token.png" alt=""><figcaption><p>Knowledge API Document</p></figcaption></figure>

### API Call Examples

#### **Create an Empty Dataset**

{% hint style="warning" %}
Only used to create an empty dataset
{% endhint %}

```
curl --location --request POST 'https://api.dify.ai/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name"}'
```

#### **Dataset List**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

#### **Create Document by Text**

```
curl --location --request POST 'https://api.dify.ai/v1/datasets/<uuid:dataset_id>/document/create_by_text' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
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

#### **Create Document by File**

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

#### **Get Document Embedding Status (Progress)**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```

#### **Delete Document**

```
curl --location --request DELETE 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### **Dataset Document List**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'
```

#### **Add Segments**

```
curl --location 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data '{"segments": [{"content": "1","answer": "1","keywords": ["a"]}]}'
```

### Error Messages

* `document_indexing`: Document indexing failed
* `provider_not_initialize`: Embedding model not configured
* `not_found`: Document not found
* `dataset_name_duplicate`: Dataset name duplicate
* `provider_quota_exceeded`: Model quota exceeded
* `dataset_not_initialized`: Dataset not initialized
* `unsupported_file_type`: Unsupported file type
  * Currently supported: txt, markdown, md, pdf, html, htm, xlsx, docx, csv
* `too_many_files`: Too many files, currently only single file uploads are supported
* `file_too_large`: File too large, supports files under 15MB