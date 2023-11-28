# 通过 API 维护数据集

> 鉴权、调用方式与应用 Service API 保持一致，不同的是一个数据集 API token 可操作所有数据集

### 使用数据集API的优势

* 将您的数据系统同步至 Dify 数据集，创建强大的工作流程。
* 提供数据集列表，文档列表及详情查询，方便构建您自己的数据管理页。
* 同时支持纯文本和文件两种上传和更新文档的接口，并支持分段级的批量新增和修改，便捷您的同步方式。
* 减少文档手动处理同步的时间,提高您对 Dify 的软件和服务的可见性。

### 如何使用

进入数据集页面，你可以在左侧的导航中切换至 **API** 页面。在该页面中你可以查看 Dify 提供的数据集 API 文档，并可以在 **API 密钥** 中管理可访问数据集 API 的凭据。

<figure><img src="../../.gitbook/assets/dataset-api-token.png" alt=""><figcaption><p>Knowledge API Document</p></figcaption></figure>

### API 调用示例

#### **创建空数据集**

{% hint style="warning" %}
仅用来创建空数据集
{% endhint %}

```
curl --location --request POST 'https://api.dify.ai/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name"}'

```

#### **数据集列表**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'

```

#### **通过文本创建文档**

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

#### **通过文件创建文档**

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

#### **获取文档嵌入状态（进度）**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```

#### **删除文档**

```
curl --location --request DELETE 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### **数据集文档列表**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'

```

#### **新增分段**

```
curl 'https://api.dify.ai/v1/datasets/aac47674-31a8-4f12-aab2-9603964c4789/documents/2034e0c1-1b75-4532-849e-24e72666595b/segment' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw $'"chunks":[
  {"content":"Dify means Do it for you",
  "keywords":["Dify","Do"]
  }
  ]'
  --compressed

```

### 错误信息

* `document_indexing`，文档索引失败
* `provider_not_initialize`， Embedding 模型未配置
* `not_found`，文档不存在
* `dataset_name_duplicate` ，数据集名称重复
* `provider_quota_exceeded`，模型额度超过限制
* `dataset_not_initialized`，数据集还未初始化
* `unsupported_file_type`，不支持的文件类型
  * 目前只支持：txt, markdown, md, pdf, html, htm, xlsx, docx, csv
* `too_many_files`，文件数量过多，暂时只支持单一文件上传
* `file_too_large`，文件太大，支持15M以下
