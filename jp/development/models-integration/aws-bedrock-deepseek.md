# AWS Bedrock上のモデル（DeepSeek）の接続

## 機能紹介

**AWS Bedrock Marketplace** は、LLM（大規模言語モデル）の統合展開プラットフォームであり、開発者はこのプラットフォーム上で100種類以上の新興専門基盤モデル（FM）を発見、テスト、利用し、簡単にデプロイおよびアクセスすることができます。

本記事では、Bedrock Marketplaceプラットフォーム上でDeepSeekモデルをデプロイし、Difyプラットフォームと統合する方法を解説します。これにより、DeepSeekモデルに基づくAIアプリケーションを迅速に構築することが可能となります。

## 前提条件

- [Bedrock](https://aws.amazon.com/bedrock/) にアクセス可能なAWSアカウント
- [Dify.AI アカウント](https://cloud.dify.ai/)

## デプロイの開始

### 1. DeepSeekモデルのデプロイ

**1.1** **Bedrock Marketplace** で **DeepSeek** を検索し、任意の **DeepSeek R1** モデルまたはその蒸留版を選択します。

![](https://assets-docs.dify.ai/2025/02/9c6e17fc0cf262b2005013bf122251d1.png)

**1.2** モデル詳細ページに移動し、**"Deploy"** をクリックして、画面の指示に従い必要な情報を入力し、ワンクリックでデプロイを完了します。

> **注意：** モデルのバージョンにより、必要な計算インスタンスの構成が異なり、料金に差異が生じる場合があります。

![](https://assets-docs.dify.ai/2025/02/613497e3473d9b6eaa7cb5611decee0c.png)

**1.3** デプロイが完了すると、**Marketplace Deployments** ページで自動生成された **Endpoint** を確認できます。このパラメータは、後でDifyプラットフォームとの接続に使用されます。

このEndpointは、SageMaker Endpointと同一です。

![Endpoint の確認](https://assets-docs.dify.ai/2025/02/82a1d6406662b83386b86ec511ab20be.png)

### 2. DeepSeekモデルとDifyプラットフォームの接続の確立

**2.1** **Dify** 管理ダッシュボードにアクセスし、**Settings** ページを開きます。

**2.2** **Model Provider** セクションで **SageMaker** を見つけ、SageMakerカードの右下にある **"Add Model"** ボタンをクリックして設定画面に進みます。

![モデルの追加](https://assets-docs.dify.ai/2025/02/864fc8476c47b460b67f14152cbbf360.png)

**2.3** SageMaker設定画面に入り、以下の内容に従って入力してください。

- **Model Type**: モデルタイプとしてLLMを選択
- **Model Name**: 任意に設定可能なモデル名
- **sagemaker endpoint**: 前述の **Endpoint** パラメータを入力してください。このパラメータは、AWS Bedrock Marketplaceの **Endpoint** ページで取得可能です。

※ **Marketplace Deployments** ページで自動生成された **Endpoint** をご確認ください。

![](https://assets-docs.dify.ai/2025/02/1feaa8d5054933f42da25a8f655b5a9e.png)

### 3. モデルの実行

**Chatflow / Workflow タイプのアプリケーション**

設定が完了したら、Difyプラットフォーム内でDeepSeekモデルが正常に動作するかをテストできます。Difyプラットフォームのホーム画面左側にある「空白アプリの作成」をクリックし、[Chatflow または Workflow] タイプのアプリケーションを選択してLLMノードを追加してください。

以下のスクリーンショットを参照し、アプリケーションプレビュー画面でモデルが正常に応答するかを確認してください。

![モデルの実行](https://assets-docs.dify.ai/2025/02/e7fb06888101662ecb970401fdba63b5.png)

**Chatbot タイプのアプリケーション**

また、アプリケーション構築時にDeepSeekモデルを利用することで、推論速度の向上や複雑なタスクの処理能力の強化が期待できます。

![使用例](https://assets-docs.dify.ai/2025/02/6f55a1d12ad020517c2bcda0a5b3aee8.png)

## よくある質問

### 1. **デプロイ後にEndpointパラメータが表示されない場合は？**

インスタンスが正しく設定され、AWSの権限設定が適切に行われていることを確認してください。それでも問題が解決しない場合は、再度デプロイするか、AWSカスタマーサポートにお問い合わせください。

### 2. **Difyでモデルをテストする方法は？**

Difyでの設定が完了した後、提供されたインターフェースを使用してモデルを呼び出し、入力データとモデルの出力結果が一致することを確認して、正常に動作しているか検証してください。