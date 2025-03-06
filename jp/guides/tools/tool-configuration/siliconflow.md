# SiliconFlow（Flux AI サポート）

> ツール制作者 @hjlarry。

SiliconFlowは、優れたオープンソースの基盤モデルをもとに、高品質なGenAIサービスを提供します。Difyを通じて、SiliconFlowを利用してFluxやStable Diffusionなどの画像生成モデルを呼び出し、自分自身のAI画像生成アプリケーションを構築できます。

## 1. SiliconCloud APIキーの取得

[SiliconCloud API管理ページ](https://cloud.siliconflow.cn/account/ak)で新しいAPIキーを作成し、十分な残高があることを確認してください。

## 2. Difyでの設定

Difyのツールページで、`SiliconCloud > To Authorize`をクリックし、APIキーを入力します。

<figure><img src="https://assets-docs.dify.ai/img/jp/tool-configuration/60148f07cd10c270fad8e49677f97748.webp" alt=""><figcaption></figcaption></figure>

## 3. ツールの使用

* **チャットフロー / ワークフロー アプリ**

ChatflowおよびWorkflowアプリケーションでは、`SiliconFlow`ツールノードを追加できます。ユーザーの入力内容を[変数](https://docs.dify.ai/v/ja-jp/guides/workflow/variables)を通じてSiliconFlowツールノードの「prompt」や「negative prompt」ボックスに渡し、必要に応じて内蔵パラメータを調整します。最後に、「end」ノードの返信ボックスでSiliconFlowツールノードの出力内容（テキスト、画像など）を選択します。

<figure><img src="https://assets-docs.dify.ai/img/jp/tool-configuration/df1f7f81b119e6bb2c62010dc5a8dc4a.webp" alt=""><figcaption></figcaption></figure>

* **エージェントアプリ**

エージェントアプリでは、`Stable Diffusion`または`Flux`ツールを追加し、対話ボックスで画像の説明を送信することで、そのツールを呼び出して画像を生成します。

<figure><img src="https://assets-docs.dify.ai/img/jp/tool-configuration/ca9d68592cbddf1e25a57284605270b5.webp" alt=""><figcaption></figcaption></figure>

<figure><img src="https://assets-docs.dify.ai/img/jp/tool-configuration/e26ed41f76b6b82ed0e084805e21e245.webp" alt=""><figcaption></figcaption></figure>
