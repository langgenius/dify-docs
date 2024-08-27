# APIを使用したデータセットの管理

> 認証や呼び出し方法はサービスAPIと同じですが、データセットAPIトークン一つで全てのデータセットを操作できます。

### データセットAPIの利点

* あなたのデータシステムをDifyデータセットに同期させ、強力なワークフローを構築できます。
* データセットリスト、ドキュメントリストおよび詳細検索を提供し、あなた自身のデータ管理ページを構築しやすくします。
* テキストとファイルの両方のアップロードおよび更新インターフェースをサポートし、セグメントレベルでのバッチ追加および変更も可能で、同期方法が便利になります。
* ドキュメントの手動処理同期の時間を削減し、Difyのソフトウェアおよびサービスの可視性を向上させます。

### 使用方法

データセットページに入り、左側のナビゲーションから **API** ページに切り替えることができます。このページでは、Difyが提供するデータセットAPIドキュメントを確認し、 **APIキー** でデータセットAPIにアクセスできる資格情報を管理できます。

<figure><img src="../../../img/knowledge-base-api-token.png" alt=""><figcaption><p>Knowledge API ドキュメント</p></figcaption></figure>

### API呼び出しの例

#### **空のデータセットを作成**

{% hint style="warning" %}
空のデータセットを作成するためだけに使用
{% endhint %}

```
curl --location --request POST 'https://api.dify.ai/v1/datasets' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name"}'

```

#### **データセットリスト**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets?page=1&limit=20' \
--header 'Authorization: Bearer {api_key}'

```

#### **テキストでドキュメントを作成**

```
curl --location --request POST '<https://api.dify.ai/v1/datasets/<uuid:dataset_id>/document/create_by_text>' \
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

#### **ファイルでドキュメントを作成**

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

#### **ドキュメント埋め込みステータス（進捗）を取得**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
```

#### **ドキュメントを削除**

```
curl --location --request DELETE 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
```

#### **データセットドキュメントリスト**

```
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'

```

#### **セグメントの追加**

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

### エラーメッセージ

* `document_indexing`，ドキュメントインデックス失敗
* `provider_not_initialize`，埋め込みモデル未初期化
* `not_found`，ドキュメントが見つかりません
* `dataset_name_duplicate`，データセット名重複
* `provider_quota_exceeded`，プロバイダーのクオータ超過
* `dataset_not_initialized`，データセット未初期化
* `unsupported_file_type`，サポートされていないファイルタイプ
  * 現在サポートされているのは：txt, markdown, md, pdf, html, htm, xlsx, docx, csv
* `too_many_files`，ファイルが多すぎます、一時的に単一ファイルのアップロードのみをサポート
* `file_too_large`，ファイルが大きすぎます、15M以下をサポート