# SiliconFlow（Flux AI サポート）

> ツール制作者 @hjlarry。

{% hint style="warning" %}
「ツール」は「プラグイン」エコシステムに完全アップグレードされました。詳しい使用方法については[プラグイン開発](https://docs.dify.ai/ja-jp/plugins/quick-start/install-plugins)をご参照ください。以下の内容はアーカイブされています。
{% endhint %}

SiliconFlowは、優れたオープンソースの基盤モデルをもとに、高品質なGenAIサービスを提供します。Difyを通じて、SiliconFlowを利用してFluxやStable Diffusionなどの画像生成モデルを呼び出し、自分自身のAI画像生成アプリケーションを構築できます。

## 1. SiliconCloud APIキーの取得

[SiliconCloud API管理ページ](https://cloud.siliconflow.cn/account/ak)で新しいAPIキーを作成し、十分な残高があることを確認してください。

## 2. Difyでの設定

Difyのツールページで、`SiliconCloud > To Authorize`をクリックし、APIキーを入力します。

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.04.16.png" alt=""><figcaption></figcaption></figure>

## 3. ツールの使用

* **チャットフロー / ワークフロー アプリ**

ChatflowおよびWorkflowアプリケーションでは、`SiliconFlow`ツールノードを追加できます。ユーザーの入力内容を[変数](https://docs.dify.ai/v/ja-jp/guides/workflow/variables)を通じてSiliconFlowツールノードの「prompt」や「negative prompt」ボックスに渡し、必要に応じて内蔵パラメータを調整します。最後に、「end」ノードの返信ボックスでSiliconFlowツールノードの出力内容（テキスト、画像など）を選択します。

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.17.40.png" alt=""><figcaption></figcaption></figure>

* **エージェントアプリ**

エージェントアプリでは、`Stable Diffusion`または`Flux`ツールを追加し、対話ボックスで画像の説明を送信することで、そのツールを呼び出して画像を生成します。

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.14.16.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.13.06.png" alt=""><figcaption></figcaption></figure>
