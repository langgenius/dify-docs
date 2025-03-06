# Hugging Faceのオープンソースモデルを統合

Difyはテキスト生成（Text-Generation）と埋め込み（Embeddings）をサポートしており、以下はそれに対応するHugging Faceモデルの種類です：

* テキスト生成：[text-generation](https://huggingface.co/models?pipeline\_tag=text-generation\&sort=trending)，[text2text-generation](https://huggingface.co/models?pipeline\_tag=text2text-generation\&sort=trending)
* 埋め込み：[feature-extraction](https://huggingface.co/models?pipeline\_tag=feature-extraction\&sort=trending)

具体的な手順は以下の通りです：

1. Hugging Faceのアカウントが必要です（[登録はこちら](https://huggingface.co/join)）。
2. Hugging FaceのAPIキーを設定します（[取得はこちら](https://huggingface.co/settings/tokens)）。
3. [Hugging Faceのモデル一覧ページ](https://huggingface.co/models)にアクセスし、対応するモデルの種類を選択します。

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/dafa87c38d57e81d4b9e71e221b8a42d.webp" alt=""><figcaption></figcaption></figure>

DifyはHugging Face上のモデルを次の2つの方法で接続できます：

1. Hosted Inference API。この方法はHugging Face公式がデプロイしたモデルを使用します。料金はかかりませんが、サポートされているモデルは少ないです。
2. Inference Endpoint。この方法は、Hugging Faceが接続しているAWSなどのリソースを使用してモデルをデプロイします。料金が発生します。

### Hosted Inference APIのモデルを接続する

#### 1 モデルを選択

モデルの詳細ページの右側にHosted Inference APIのセクションがあるモデルのみがHosted Inference APIをサポートしています。以下の図のように表示されます：

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/2dab3b4e18ba2142888bb3164d891787.webp" alt=""><figcaption></figcaption></figure>

モデルの詳細ページで、モデルの名前を取得できます。

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/79678881bbf8773154bc72288e9921dd.webp" alt=""><figcaption></figcaption></figure>

#### 2 Difyで接続モデルを使用する

`設定 > モデルプロバイダー > Hugging Face > モデルタイプ`のエンドポイントタイプでHosted Inference APIを選択します。以下の図のように設定します：

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/07d5486577b75203a8f53cfe2068b46b.webp" alt=""><figcaption></figcaption></figure>

APIトークンは記事の冒頭で設定したAPIキーです。モデル名は前のステップで取得したモデル名を入力します。

### 方法 2: Inference Endpoint

#### 1 デプロイするモデルを選択

モデルの詳細ページの右側にある`Deploy`ボタンの下にInference EndpointsオプションがあるモデルのみがInference Endpointをサポートしています。以下の図のように表示されます：

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/ddd118e18fc0b57323b757d6605bcf65.webp" alt=""><figcaption></figcaption></figure>

#### 2 モデルをデプロイ

モデルのデプロイボタンをクリックし、Inference Endpointオプションを選択します。以前にクレジットカードを登録していない場合は、カードの登録が必要です。手順に従って進めてください。カードを登録した後、以下の画面が表示されます：必要に応じて設定を変更し、左下のCreate EndpointボタンをクリックしてInference Endpointを作成します。

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/9dd475f2a873a4f14bcd6b5b178314da.webp" alt=""><figcaption></figcaption></figure>

モデルがデプロイされると、エンドポイントURLが表示されます。

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/98dccb0e2519e1f0c6183c03dc5306b3.webp" alt=""><figcaption></figcaption></figure>

#### 3 Difyで接続モデルを使用する

`設定 > モデルプロバイダー > Hugging Face > モデルタイプ`のエンドポイントタイプでInference Endpointsを選択します。以下の図のように設定します：

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/1759b2098b5cd42b36a472e40232fe19.webp" alt=""><figcaption></figcaption></figure>

APIトークンは記事の冒頭で設定したAPIキーです。`テキスト生成モデルの名前は任意に設定可能ですが、埋め込みモデルの名前はHugging Faceの名前と一致する必要があります。`エンドポイントURLは前のステップでデプロイしたモデルのエンドポイントURLを入力します。

<figure><img src="https://assets-docs.dify.ai/img/jp/models-integration/d50aa4a34851bd159140034d42a6c5b8.webp" alt=""><figcaption></figcaption></figure>

> 注意点：埋め込みの「ユーザー名 / 組織名」は、Hugging Faceの[Inference Endpoints](https://huggingface.co/docs/inference-endpoints/guides/access)のデプロイ方法に基づいて、「[ユーザー名](https://huggingface.co/settings/account)」または「[組織名](https://ui.endpoints.huggingface.co/)」を入力する必要があります。
