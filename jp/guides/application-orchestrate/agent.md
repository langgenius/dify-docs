# エージェント

### 定義

エージェントアシスタントは、大規模言語モデルの推論能力を活用し、複雑な人間のタスクを自律的に目標設定、タスク分解、ツールの呼び出し、プロセスのイテレーションを行い、人間の介入なしでタスクを完了することができます。

### エージェントアシスタントの使い方

迅速に使い始めるために、「探索」でエージェントアシスタントのアプリケーションテンプレートを見つけて自分のワークスペースに追加するか、それを基にカスタマイズすることができます。新しいDifyスタジオでは、ゼロから自分専用のエージェントアシスタントを編成し、財務報告書の分析、レポートの作成、ロゴデザイン、旅行計画などのタスクを完了する手助けをすることができます。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/71476bdcc7d15c5da041e6ba49367e06.webp" alt=""><figcaption><p>探索 - エージェントアシスタントアプリケーションテンプレート</p></figcaption></figure>

エージェントアシスタントの推論モデルを選択します。エージェントアシスタントのタスク完了能力はモデルの推論能力に依存しますので、より強力な推論能力を持つモデルシリーズ、例えばgpt-4を選択することをお勧めします。これにより、より安定したタスク完了効果が得られます。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/66ad43e3c6fc2ff9ff5ed0d5ac9a1c5b.webp" alt=""><figcaption><p>エージェントアシスタントの推論モデルを選択</p></figcaption></figure>

「プロンプト」でエージェントアシスタントの指示を作成できます。より良い結果を得るために、指示の中でタスクの目標、ワークフロー、リソース、制約などを明確にすることが重要です。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/6dff9ce6c4d16be4d439b46d4e7aa343.webp" alt=""><figcaption><p>エージェントアシスタントの指示プロンプトを編成</p></figcaption></figure>

### アシスタントに必要なツールを追加

「コンテキスト」では、エージェントアシスタントが参照できるナレッジベースツールを追加できます。これにより、外部の背景知識を取得することができます。

「ツール」では、使用する必要があるツールを追加できます。ツールはLLMの能力を拡張し、例えばネット検索、科学計算、画像の作成などが可能になります。これにより、LLMは外部世界と接続する能力を持つようになります。Difyは2種類のツールタイプを提供しています：**ファーストパーティツール**と**カスタムツール**です。

Difyエコシステムが提供するファーストパーティ内蔵ツールを直接使用するか、カスタムAPIツール（現在はOpenAPI / SwaggerおよびOpenAIプラグイン規格をサポート）を簡単にインポートすることができます。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/cbd5cfc1c80101428a0263d8ebef7f1d.webp" alt=""><figcaption><p>アシスタントに必要なツールを追加</p></figcaption></figure>

**ツール** 機能を使用すると、Dify でより強力な AIアプリを作成できます。たとえば、エージェントアシスタントに適したツールを編成して、推論、ステップ分解、ツール呼び出しを通じて複雑なタスクを完了できるようにすることができます。

さらに、このツールにより、アプリと他のシステムやサービスの統合が簡素化され、コードの実行や独自の情報ソースへのアクセスなど、外部環境とのやり取りが可能になります。チャット ボックスで呼び出したいツールの名前を言うだけで、自動的にアクティブ化されます。

![](https://assets-docs.dify.ai/img/jp/application-orchestrate/ba7d5da39f6d9de497fa75e72381b3a8.webp)

### エージェントの設定

DifyではエージェントアシスタントにFunction Calling（関数呼び出し）とReActの2つの推論モードを提供しています。関数呼び出しをサポートするモデルシリーズ（例：gpt-3.5/gpt-4）はより良い、安定したパフォーマンスを持っています。関数呼び出しをサポートしていないモデルシリーズには、ReAct推論フレームワークで類似の効果を実現しています。

エージェント設定では、アシスタントのイテレーション制限を変更できます。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/96dfd5b4a3ddd0a855c61bc4ab611d54.webp" alt=""><figcaption><p>Function Calling モード</p></figcaption></figure>

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/885f8e644f83a40313b307b2fa8d37a1.webp" alt=""><figcaption><p>ReAct モード</p></figcaption></figure>

### 会話のオープニング設定

エージェントアシスタントの会話オープニングとオープニング質問を設定できます。設定された会話オープニングは、ユーザーが初めて対話を開始する際に、アシスタントが完了できるタスクや提案される質問の例を表示します。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/1fb7a75b0e82abecf96bcdcdf904737a.webp" alt=""><figcaption><p>会話のオープニングとオープニング質問を設定</p></figcaption></figure>

### ファイルのアップロード

Claude 3.5 Sonnet (https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) や Gemini 1.5 Pro (https://ai.google.dev/api/files) など、一部のLLMはファイル処理に標準対応しています。各LLMのウェブサイトで、ファイルのアップロード機能について詳しくご確認ください。

ファイルの読み込みに対応したLLMを選択し、「Document」を有効にしてください。これにより、チャットボットは複雑な設定なしでファイルの内容を理解し、利用できるようになります。

![](https://assets-docs.dify.ai/2024/11/9f0b7a3c67b58c0bd7926501284cbb7d.png)

### デバッグとプレビュー

エージェントアシスタントの編成が完了したら、アプリとして公開する前にデバッグとプレビューを行い、アシスタントのタスク完了効果を確認できます。

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/67a2317d28479f9aa8f33e3290499f32.webp" alt=""><figcaption><p>デバッグとプレビュー</p></figcaption></figure>

### アプリの公開

<figure><img src="https://assets-docs.dify.ai/img/jp/application-orchestrate/eaba771226ebef8944f017b777da1642.webp" alt=""><figcaption><p>アプリをWebアプリとして公開</p></figcaption></figure>
