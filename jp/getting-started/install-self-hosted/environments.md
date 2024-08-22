# 環境変数の説明

### 公共変数

#### CONSOLE\_API\_URL

コンソールAPIのバックエンドのURLです。認証コールバックを組み合わせるために使用され、空の場合は同じドメインになります。例：`https://api.console.dify.ai`。

#### CONSOLE\_WEB\_URL

コンソールウェブの**フロントエンド**のURLです。フロントエンドアドレスの一部を組み合わせたり、CORS設定に使用されます。空の場合は同じドメインになります。例：`https://console.dify.ai`

#### SERVICE\_API\_URL

サービスAPIのURLです。**フロントエンド**にサービスAPIのベースURLを表示するために使用されます。空の場合は同じドメインになります。例：`https://api.dify.ai`

#### APP\_API\_URL

WebアプリAPIのバックエンドURLです。**フロントエンド**APIのバックエンドアドレスを宣言するために使用されます。空の場合は同じドメインになります。例：`https://app.dify.ai`

#### APP\_WEB\_URL

WebアプリのURLです。**フロントエンド**にWebアプリAPIのベースURLを表示するために使用されます。空の場合は同じドメインになります。例：`https://api.app.dify.ai`

#### FILES\_URL

ファイルプレビューまたはダウンロード用のURLプレフィックスです。ファイルプレビューやダウンロードURLをフロントエンドに表示したり、マルチモーダルモデルの入力として使用します。他人による偽造を防ぐため、画像プレビューURLは署名付きで、5分の有効期限があります。

***

### サーバー側

#### MODE

起動モードです。dockerによる起動時にのみ有効で、ソースコード起動では無効です。

*   api

    APIサーバーを起動します。
*   worker

    非同期キューのワーカーを起動します。

#### DEBUG

デバッグモード。デフォルトはfalse。ローカル開発時にはこの設定をオンにすることをお勧めします。これにより、モンキーパッチによって発生する問題を防ぐことができます。

#### FLASK\_DEBUG

Flaskのデバッグモード。オンにすると、インターフェースでトレース情報が出力され、デバッグが容易になります。

#### SECRET\_KEY

セッションクッキーを安全に署名し、データベース上の機密情報を暗号化するためのキー。初回起動時にこの変数を設定する必要があります。`openssl rand -base64 42`を使用して強力なキーを生成できます。

#### DEPLOY\_ENV

デプロイ環境。

*   PRODUCTION（デフォルト）

    プロダクション環境。
*   TESTING

    テスト環境。フロントエンドページにはテスト環境を示す明確な色の識別が表示されます。

#### LOG\_LEVEL

ログ出力レベル。デフォルトはINFO。プロダクション環境ではERRORに設定することをお勧めします。

#### MIGRATION\_ENABLED

trueに設定した場合、コンテナ起動時に自動的にデータベースのマイグレーションが実行されます。dockerによる起動時にのみ有効で、ソースコード起動では無効です。ソースコード起動の場合、apiディレクトリで手動で`flask db upgrade`を実行する必要があります。

#### CHECK\_UPDATE\_URL

バージョンチェックポリシーを有効にするかどうか。falseに設定した場合、`https://updates.dify.ai`を呼び出してバージョンチェックを行いません。現在、国内から直接CloudFlare Workerのバージョンインターフェースにアクセスできないため、この変数を空に設定すると、このインターフェースの呼び出しをブロックできます。

#### コンテナ起動関連設定

dockerイメージまたはdocker-composeによる起動時にのみ有効です。

*   DIFY\_BIND\_ADDRESS

    APIサービスのバインドアドレス。デフォルト：0.0.0.0、すべてのアドレスからアクセス可能にします。
*   DIFY\_PORT

    APIサービスのバインドポート番号。デフォルト5001。
*   SERVER\_WORKER\_AMOUNT

    APIサービスのServer worker数。すなわちgevent workerの数。公式：`CPUのコア数 x 2 + 1`。詳細はこちら：https://docs.gunicorn.org/en/stable/design.html#how-many-workers
*   SERVER\_WORKER\_CLASS

    デフォルトはgevent。Windowsの場合、syncまたはsoloに切り替えることができます。
*   GUNICORN\_TIMEOUT

    リクエスト処理のタイムアウト時間。デフォルト200。360に設定することをお勧めします。これにより、長時間のSSE接続をサポートできます。
*   CELERY\_WORKER\_CLASS

    `SERVER_WORKER_CLASS`と同様に、デフォルトはgevent。Windowsの場合、syncまたはsoloに切り替えることができます。
*   CELERY\_WORKER\_AMOUNT

    Celery workerの数。デフォルトは1。必要に応じて設定します。
*   HTTP\_PROXY

    HTTPプロキシのアドレス。国内からOpenAIやHuggingFaceにアクセスできない問題を解決するために使用されます。注意：プロキシがホストマシンにデプロイされている場合（例：`http://127.0.0.1:7890`）、このプロキシアドレスはローカルモデルに接続する場合と同様に、dockerコンテナ内のホストマシンアドレスを使用する必要があります（例：`http://192.168.1.100:7890`または`http://172.17.0.1:7890`）。
*   HTTPS\_PROXY

    HTTPSプロキシのアドレス。国内からOpenAIやHuggingFaceにアクセスできない問題を解決するために使用されます。HTTPプロキシと同様に設定します。

#### データベース設定

データベースにはPostgreSQLを使用します。public schemaを使用してください。

* DB\_USERNAME：ユーザー名
* DB\_PASSWORD：パスワード
* DB\_HOST：データベースホスト
* DB\_PORT：データベースポート番号。デフォルト5432
* DB\_DATABASE：データベース名
* SQLALCHEMY\_POOL\_SIZE：データベース接続プールのサイズ。デフォルトは30接続。必要に応じて増やせます。
* SQLALCHEMY\_POOL\_RECYCLE：データベース接続プールのリサイクル時間。デフォルト3600秒。
* SQLALCHEMY\_ECHO：SQLを出力するかどうか。デフォルトはfalse。

#### Redis 設定

このRedis設定はキャッシュおよび対話時のpub/subに使用されます。

* REDIS\_HOST：Redisホスト
* REDIS\_PORT：Redisポート。デフォルト6379
* REDIS\_DB：Redisデータベース。デフォルトは0。セッションRedisおよびCeleryブローカーとは異なるデータベースを使用してください。
* REDIS\_USERNAME：Redisユーザー名。デフォルトは空
* REDIS\_PASSWORD：Redisパスワード。デフォルトは空。パスワードを設定することを強くお勧めします。
* REDIS\_USE\_SSL：SSLプロトコルを使用して接続するかどうか。デフォルトはfalse

#### Celery 設定

*   CELERY\_BROKER\_URL

    フォーマットは以下の通りです。

    <pre><code><strong>redis://&#x3C;redis_username>:&#x3C;redis_password>@&#x3C;redis_host>:&#x3C;redis_port>/&#x3C;redis_database>
    </strong><strong>  
    </strong></code></pre>

    例：`redis://:difyai123456@redis:6379/1`
*   BROKER\_USE\_SSL

    trueに設定した場合、SSLプロトコルを使用して接続します。デフォルトはfalse。

#### CORS 設定

フロントエンドのクロスオリジンアクセスポリシーを設定するために使用します。

*   CONSOLE\_CORS\_ALLOW\_ORIGINS

    コンソールのCORSクロスオリジンポリシー。デフォルトは`*`、すべてのドメインがアクセス可能です。
*   WEB\_API\_CORS\_ALLOW\_ORIGINS

    WebアプリのCORSクロスオリジンポリシー。デフォルトは`*`、すべてのドメインがアクセス可能です。

詳細な設定については、次のガイドを参照してください：[クロスオリジン/認証関連ガイド](https://docs.dify.ai/v/ja-jp/learn-more/faq/install-faq)

#### ファイルストレージ設定

データセットのアップロードファイル、チーム/テナントの暗号化キーなどのファイルを保存するために使用します。

*   STORAGE\_TYPE

    ストレージ施設のタイプ

    *   local（デフォルト）

        ローカルファイルストレージ。この場合、以下の`STORAGE\_LOCAL\_PATH`設定を設定する必要があります。
    *   s3

        S3オブジェクトストレージ。この場合、以下のS3\_プレフィックスの設定を設定する必要があります。
    *   azure-blob

        Azure Blobストレージ。この場合、以下のAZURE\_BLOB\_プレフィックスの設定を設定する必要があります。
*   STORAGE\_LOCAL\_PATH

    デフォルトはstorage、すなわち現在のディレクトリのstorageディレクトリに保存します。dockerまたはdocker-composeでデプロイする場合、2つのコンテナにある`/app/api/storage`ディレクトリを同じローカルディレクトリにマウントする必要があります。そうしないと、ファイルが見つからないエラーが発生する可能性があります。
* S3\_ENDPOINT：S3エンドポイントアドレス
* S3\_BUCKET\_NAME：S3バケット名
* S3\_ACCESS\_KEY：S3アクセスキー
* S3\_SECRET\_KEY：S3シークレットキー
* S3\_REGION：S3リージョン情報（例：us-east-1）
* AZURE\_BLOB\_ACCOUNT\_NAME: アカウント名（例：'difyai'）
* AZURE\_BLOB\_ACCOUNT\_KEY: アカウントキー（例：'difyai'）
* AZURE\_BLOB\_CONTAINER\_NAME: コンテナ名（例：'difyai-container'）
* AZURE\_BLOB\_ACCOUNT\_URL: 'https://\<your\_account\_name>.blob.core.windows.net'

#### ベクトルデータベース設定

*   VECTOR\_STORE

    **使用可能な列挙型は以下を含みます：**

    * `weaviate`
    * `qdrant`
    * `milvus`
    * `zilliz`（`milvus`と同じ）
    * `pinecone`（現在未公開）
    * `tidb_vector`
*   WEAVIATE\_ENDPOINT

    Weaviateエンドポイントアドレス（例：`http://weaviate:8080`）。
*   WEAVIATE\_API\_KEY

    Weaviateに接続するために使用するapi-keyの資格情報。
*   WEAVIATE\_BATCH\_SIZE

    Weaviateでオブジェクトのバッチ作成数。デフォルトは100。詳細はこちらのドキュメントを参照してください：https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters
*   WEAVIATE\_GRPC\_ENABLED

    Weaviateとの通信にgRPC方式を使用するかどうか。オンにすると性能が大幅に向上しますが、ローカルでは使用できない可能性があります。デフォルトはtrueです。
*   QDRANT\_URL

    Qdrantエンドポイントアドレス（例：`https://your-qdrant-cluster-url.qdrant.tech/`）。
*   QDRANT\_API\_KEY

    Qdrantに接続するために使用するapi-keyの資格情報。
*   PINECONE\_API\_KEY

    Pineconeに接続するために使用するapi-keyの資格情報。
*   PINECONE\_ENVIRONMENT

    Pineconeの環境（例：`us-east4-gcp`）。
*   MILVUS\_HOST

    Milvusホストの設定。
*   MILVUS\_PORT

    Milvusポートの設定。
*   MILVUS\_USER

    Milvusユーザーの設定。デフォルトは空。
*   MILVUS\_PASSWORD

    Milvusパスワードの設定。デフォルトは空。
*   MILVUS\_SECURE

    MilvusがSSL接続を使用するかどうか。デフォルトはfalse。
*   TIDB\_VECTOR\_HOST

    TiDB Vectorホスト設定（例：`xxx.eu-central-1.xxx.tidbcloud.com`）
*   TIDB\_VECTOR\_PORT

    TiDB Vectorポート番号設定（例：`4000`）
*   TIDB\_VECTOR\_USER

    TiDB Vectorユーザー設定（例：`xxxxxx.root`）
*   TIDB\_VECTOR\_PASSWORD

    TiDB Vectorパスワード設定
*   TIDB\_VECTOR\_DATABASE

    TiDB Vectorデータベース設定（例：`dify`）

#### ナレッジベース設定

*   UPLOAD\_FILE\_SIZE\_LIMIT

    アップロードファイルのサイズ制限。デフォルトは15M。
*   UPLOAD\_FILE\_BATCH\_LIMIT

    一度にアップロードできるファイル数の上限。デフォルトは5個。
*   ETL\_TYPE

    **使用可能な列挙型は以下を含みます：**

    *   dify

        Dify独自のファイル抽出ソリューション
    *   Unstructured

        Unstructured.ioのファイル抽出ソリューション
*   UNSTRUCTURED\_API\_URL

    ETL\_TYPEがUnstructuredの場合、Unstructured APIパスの設定が必要です。

    例：`http://unstructured:8000/general/v0/general`

#### マルチモーダルモデル設定

*   MULTIMODAL\_SEND\_IMAGE\_FORMAT

    マルチモーダルモデルの入力時に画像を送信する形式。デフォルトは`base64`、オプションで`url`。`url`モードでは呼び出しの遅延が`base64`モードよりも少なく、一般的には互換性が高い`base64`モードをお勧めします。`url`に設定する場合、`FILES\_URL`を外部からアクセス可能なアドレスに設定する必要があります。これにより、マルチモーダルモデルが画像にアクセスできるようになります。
*   UPLOAD\_IMAGE\_FILE\_SIZE\_LIMIT

    アップロード画像ファイルのサイズ制限。デフォルトは10M。

#### Sentry 設定

アプリの監視およびエラーログトラッキングに使用されます。

*   SENTRY\_DSN

    Sentry DSNアドレス。デフォルトは空。空の場合、すべての監視情報はSentryに報告されません。
*   SENTRY\_TRACES\_SAMPLE\_RATE

    Sentryイベントの報告割合。例えば、0.01に設定すると1%となります。
*   SENTRY\_PROFILES\_SAMPLE\_RATE

    Sentryプロファイルの報告割合。例えば、0.01に設定すると1%となります。

#### Notion 統合設定

Notion統合設定。変数はNotion integrationを申請することで取得できます：[https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

* NOTION\_CLIENT\_ID
* NOTION\_CLIENT\_SECRET

#### メール関連の設定

* MAIL\_TYPE
  * resend
    * MAIL\_DEFAULT\_SEND\_FROM\ 送信者のメール名（例：no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai)）、必須ではありません。
    * RESEND\_API\_KEY\ ResendメールプロバイダーのAPIキー。APIキーから取得できます。
  * smtp
    * SMTP\_SERVER\ SMTPサーバーアドレス
    * SMTP\_PORT\ SMTPサーバ ，用于验证接口身份。
* SESSION\_タイプ： セッションコンポーネントのタイプ
  *   redis（デフォルト）

      これを選択した場合、下記の SESSION\_REDIS\_ で始まる環境変数を設定する必要があります。
  *   sqlalchemy

      これを選択した場合、現在のデータベース接続を使用し、sessions テーブルを使用してセッションレコードを読み書きします。
* SESSION\_REDIS\_HOST：Redis ホスト
* SESSION\_REDIS\_PORT：Redis ポート、デフォルトは 6379
* SESSION\_REDIS\_DB：Redis データベース、デフォルトは 0、Redis および Celery ブローカーとは異なるデータベースを使用してください。
* SESSION\_REDIS\_ユーザー名：Redis ユーザー名、デフォルトは空
* SESSION\_REDIS\_パスワード：Redis パスワード、デフォルトは空、パスワードの設定を強く推奨します。
* SESSION\_REDIS\_USE\_SSL：SSL プロトコルを使用して接続するかどうか、デフォルトは false

#### クッキー戦略の設定

> ⚠️ この設定はバージョン 0.3.24 から廃止されました。

セッションクッキーのブラウザ戦略を設定するために使用されます。

*   COOKIE\_HTTPONLY

    クッキーの HttpOnly 設定、デフォルトは true。
*   COOKIE\_SAMESITE

    クッキーの SameSite 設定、デフォルトは Lax。
*   COOKIE\_SECURE

    クッキーの Secure 設定、デフォルトは false。
