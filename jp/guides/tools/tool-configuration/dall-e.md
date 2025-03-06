# Dall-e

> ツール作成者：@Dify。 DALL-E は、入力したテキストに基づいて画像を生成するツールで、OpenAIによって開発されました。以下はDifyでDALL-E絵画ツールを設定および使用する手順です。

## 1. OpenAIのAPIキーを申請する

[OpenAI Platform](https://platform.openai.com/) でAPIキーを申請し、アカウントに十分なクレジットがあることを確認してください。

## 2. Dify内で設定する

Difyのナビゲーションページで `ツール > DALL-E > 認証する` の順にクリックし、API キーを入力してください。

![](https://assets-docs.dify.ai/img/jp/tool-configuration/3fe0eb51cfc75f0b6facb518d5e789a5.webp)

## 3. ツールの使用方法

* **チャットフロー / ワークフロー アプリ**

チャットフローやワークフローアプリでは、`DALL-E 絵画` ツールノードを追加することができます。追加後、ノード内の "入力変数 → プロンプト" に、ユーザーの入力プロンプトや前のノードで生成されたコンテンツへの[変数](https://docs.dify.ai/v/ja-jp/guides/workflow/variables)を入力する必要があります。最後に、変数を使用して `DALL-E 絵画` の出力画像を "終了" ノードで参照します。

![](https://assets-docs.dify.ai/img/jp/tool-configuration/2c7bb68fe4a5b591f18b697696fdfee9.webp)

* **エージェントアプリ**

エージェントアプリ内で `DALL-E` ツールを追加し、ダイアログボックスに画像の説明を送信して、ツールを呼び出してAI画像を生成します。

![](https://assets-docs.dify.ai/img/jp/tool-configuration/ba7d5da39f6d9de497fa75e72381b3a8.webp)
