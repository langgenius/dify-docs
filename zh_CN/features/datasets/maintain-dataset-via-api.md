# 维护 Knowledge API

> 身份验证、调用方法和应用服务API保持一致。区别在于知识API令牌可以对所有知识库进行操作.

### 使用 Knowledge API 的好处
* 同步您的数据系统以分散Knowledge以创建强大的工作流.
* 提供知识列表和文档列表API以及详细查询接口, 目的是为了便于生成自己的数据管理页.
* 为了简化您的同步进程，支持纯文本和  文件上传 / 更新文档 以及批量新增和修改.
* 提高Dify软件和服务的可见性，缩短手动处理文档和同步的时间.

### 如何使用

请转到知识页面，您可以在左侧导航中切换到API页面。在此页面上，您可以查看dify提供的API文档并管理用于访问Knowledge API的凭据.

<figure><img src="../../.gitbook/assets/dataset-api-token.png" alt=""><figcaption><p>Knowledge API Document</p></figcaption></figure>

## **创建空的 Knowledge**

**`POST /datasets`**

{% hint style="warning" %}
仅用于创建空数据集
{% endhint %}

```
curl --location --request POST 'https://api.dify.ai/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name"}'

```

#### **Knowledge 列表**


```
curl --location --request GET 'https://api.dify.ai/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'

```

#### **文本创建文档**

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

#### **文件创建文档**

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

#### **获取文档嵌入状态**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```

#### **删除文档**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'

```

#### **添加新的片段**

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


### 报错信息

- `document_indexing`，表示文档正处于索引过程中
- `provider_not_initialize`， 表示未配置嵌入模型
- `not_found`，文档不存在
- `dataset_name_duplicate` ，重复命名
- `provider_quota_exceeded`，配额已超出最大限制
- `dataset_not_initialized`，未进行初始化
- `unsupported_file_type`，不支持的文件类型
    - 现支持的文件类型如下：txt, markdown, md, pdf, html, htm, xlsx, docx, csv
- `too_many_files`，表示文件数量太大，暂时只支持单文件上传
- `file_too_large`，表示文件太大，仅支持15M以下的文件