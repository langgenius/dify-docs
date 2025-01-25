# Telegram Bot連携プラグインの開発

### **プロジェクトの背景**

LLMサービスを一般的なリアルタイムチャットプラットフォーム（IM）と連携させることは、常に重要な取り組みとして注目されています。Difyプラグインのエコシステムは、よりシンプルで使いやすい連携方法を提供することを目指しています。この記事では、Telegramを例に、Telegram Botに接続するプラグインを開発する方法を詳しく解説します。

[Telegram](https://telegram.org/)は、豊富なAPIを提供する無料のオープンなリアルタイムコミュニプラットフォームです。イベントベースの仕組みである使いやすいWebhook機能も備えています。この仕組みを利用して、次の図に示すようにTelegram Botプラグインを作成します。

<figure><img src="https://assets-docs.dify.ai/2024/12/08d0cc0074efe3b81b15ade2d888e785.png" alt=""><figcaption></figcaption></figure>

**連携の流れ:**

1.  **ユーザーがTelegram Botを使用**

    ユーザーがTelegramでメッセージを送信すると、TelegramはDifyプラグインにHTTPリクエストを送信します。

2.  **メッセージがTelegram Botプラグインに転送される**

    メールシステムで受信者のアドレスが必要なように、Telegram Botを使用する場合、メッセージは処理のためにDifyアプリに転送される必要があります。これは、Telegram APIを通じてTelegram Webhookアドレスを設定し、そのアドレスをプラグインに入力することで実現できます。

3.  **プラグインがメッセージを受信し、Difyアプリに返す**

    プラグインはTelegramからのリクエストを処理し、ユーザーが入力した内容を解析します。そして、Difyアプリを呼び出して、返信内容を取得します。
    
4.  **Difyアプリが応答し、Telegram Botにメッセージを返す**

    Difyアプリからの応答を受信した後、プラグインは同じ経路でTelegram Botにメッセージを返します。これにより、ユーザーはTelegramを使いながらDifyアプリと直接対話できます。

### 前提条件

*   Telegram Botの作成
*   Difyプラグインのスキャフォールディングツール
*   Python環境（バージョン3.10以上）

#### **Telegram Botの作成**

[@BotFather](https://t.me/BotFather)のガイドに従って、新しいBotを作成してください。詳しい作成手順については、[Telegramの公式ドキュメント](https://core.telegram.org/bots/tutorial)を参照してください。

作成後、次のステップで使用するHTTP APIトークンが発行されます。

<figure><img src="https://assets-docs.dify.ai/2024/12/668783d0362200257b2cb5385ecbacff.png" alt="" width="375"><figcaption></figcaption></figure>

**Difyプラグインのスキャフォールディングツールのインストール**

詳細については、[initialize-development-tools.md](../initialize-development-tools.md "mention")を参照してください。

**Python環境の準備**

詳しい手順については、[Pythonインストールチュートリアル](https://pythontest.com/python/installing-python-3-11/)を参照するか、LLMに詳しいインストール手順を問い合わせてください。

### プラグインの開発

それでは、実際のプラグインのコーディング作業を開始しましょう。始める前に、[クイックスタート：拡張タイププラグインの開発](../extension-plugin.md) を確認するか、Difyプラグインの開発経験があることを確認してください。

#### **プロジェクトの初期化**

次のコマンドを実行して、プラグイン開発プロジェクトを初期化します：

```bash
./dify-plugin-darwin-arm64 plugin init
```

プロンプトに従って、プロジェクトの基本情報を入力し、`extension`テンプレートを選択します。権限設定では、`Apps`と`Endpoints`の両方にチェックを入れてください。

Difyプラットフォームの機能に対するプラグインからのリクエスト（逆呼び出し）については、[逆呼び出し：App](../../schema-definition/reverse-invocation-of-the-dify-service/)を参照してください。

<figure><img src="https://assets-docs.dify.ai/2024/12/d89a6282c5584fc43a9cadeddf09c0de.png" alt=""><figcaption><p>プラグインの権限</p></figcaption></figure>

#### **1. 設定フォームの編集**

このプラグインでは、返信に使用するDifyアプリを指定する必要があります。また、返信時にTelegramボットトークンが必要になるため、これらの2つのフィールドをプラグインフォームに追加する必要があります。

`group/your-project.yaml`のように、グループパスにあるyamlファイルを編集してください。フォームの設定ファイル名は、プラグイン作成時に入力した基本情報によって決まります。対応するyamlファイルを編集してください。

**コード例:**

`your-project.yaml`

```yaml
settings:
  - name: bot_token
    type: secret-input
    required: true
    label:
      en_US: Bot Token
      pt_BR: Token do Bot
      ja_JP: ボットトークン
  - name: app
    type: app-selector
    scope: chat
    required: true
    label:
      en_US: App
      ja_JP: アプリ
    placeholder:
      en_US: the app you want to use to answer telegram messages
      pt_BR: o app que você deseja usar para responder mensagens do Telegram
      ja_JP: あなたが Telegram メッセージに回答するために使用するアプリ
endpoints:
  - endpoints/your_project.yaml
```

コードデータ構造の説明：

```
  - name: app
    type: app-selector
    scope: chat
```

* プラグインを利用すると、特定のDifyアプリにアクセスし、メッセージを転送できます。
* `scope`フィールドはチャットフィールドとして定義されており、エージェント、チャットボット、チャットフローといったアプリでのみ利用可能です。

**例**:

`endpoints/your_path.yaml`

```yaml
path: "/your_project/message"
method: "POST"
extra:
  python:
    source: "endpoints/your_project.py"
```

#### 2. 機能コードを編集する

`endpoints/your_project.py`ファイルを編集し、以下のコードを追加してください：

```python
import json
import traceback
import requests
from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint

class TelegramWebhook(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """
        data = r.get_json()

        message = data.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        if not chat or not message:
            return Response(status=200, response="ok")

        message_id = message.get("message_id")
        bot_token = settings.get("bot_token", "")
        chat_type = chat.get("type")

        reply_message = {
            "method": "sendMessage",
            "chat_id": chat_id,
            "reply_to_message_id": message_id,
            "text": message.get("text"),
        }
        
        return Response(
            status=200,
            response=json.dumps(reply_message),
            content_type="application/json",
        )
```

### 2.1 プラグインのデバッグ

Difyではリモートデバッグ機能が利用できます。「プラグイン管理」ページで、デバッグキーとリモートサーバーアドレスを取得してください。

<figure><img src="https://assets-docs.dify.ai/2024/12/053415ef127f1f4d6dd85dd3ae79626a.png" alt=""><figcaption></figcaption></figure>

プラグインプロジェクトに戻り、`.env.example`ファイルをコピーして`.env`にリネームします。そして、リモートサーバーアドレスとデバッグキーを`.env`ファイルに記入してください。

`.env`ファイルの内容は以下の通りです：

```bash
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=localhost
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=****-****-****-****-****
```

`python -m main`コマンドを実行してプラグインを起動します。プラグインページで、プラグインがワークスペースにインストールされたことを確認できます。他のチームメンバーもこのプラグインにアクセス可能です。

```bash
python -m main
```

#### プラグインのエンドポイント設定

Difyのプラグイン管理ページで、自動的にインストールされたテストプラグインを見つけます。新しいエンドポイントを作成し、名前、Botトークンを入力し、接続先のアプリを選択してください。

![プラグインのデバッグ](https://assets-docs.dify.ai/2024/12/93f1bc3d52635ff5bf177331caaf7afa.png)

プラグインからURLをコピーし、以下のコマンドと組み合わせてテストリクエストコマンドを作成します。

ここで、`<hook_url>`には先ほどコピーしたアドレスを、`<bot_token>`には[準備](developing-a-plugin-that-integrated-with-telegram-bot.md#prerequisites)で取得したTelegram HTTP APIトークンを入力します。

```bash
curl -F "url=<hook_url>" https://api.telegram.org/bot<bot_token>/setWebhook
```

実行すると、以下の結果が表示されるはずです。

<figure><img src="https://assets-docs.dify.ai/2024/12/4e2a924cfed25ea88d6692d55fac39e3.png" alt=""><figcaption><p>curlのレスポンス</p></figcaption></figure>

Telegramボットにメッセージを送信すると、送信したメッセージがそのまま繰り返されることを確認できます。これは、プラグインがTelegramボットとの接続を正しく確立したことを示しています。

<figure><img src="https://assets-docs.dify.ai/2024/12/a7c4f708fd0c11734f3359c1e1b6ad5a.png" alt=""><figcaption></figcaption></figure>

#### 2.2 Difyアプリで返信する

Difyアプリを使用して返信するコードを追加するために、関数コードを修正します：

```python
import json
import traceback
from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint

class TelegramWebhook(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """
        data = r.get_json()

        message = data.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        if not chat or not message:
            return Response(status=200, response="ok")

        message_id = message.get("message_id")
        bot_token = settings.get("bot_token", "")
        chat_type = chat.get("type")

        try:
            response = self.session.app.chat.invoke(
                app_id=settings["app"]["app_id"],
                query=message.get("text", ""),
                inputs={},
                response_mode="blocking",
            )
            return Response(
                status=200,
                response=json.dumps({
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "reply_to_message_id": message_id,
                    "text": response.get("answer", ""),
                }),
                content_type="text/plain",
            )
        except Exception as e:
            err = traceback.format_exc()
            return Response(
                status=200,
                response="Sorry, I'm having trouble processing your request. Please try again later." + str(err),
                content_type="text/plain",
            )
```

このコードでは、`self.session.app.chat.invoke` を使用してDifyプラットフォーム内のアプリを呼び出します。`app_id` や `query` などの情報を渡し、最終的にその応答をTelegram Botに返します。

プラグインを再起動し、再度デバッグを実行すると、Telegram BotがDifyアプリからの返信メッセージを正しく出力していることを確認できます。

<figure><img src="https://assets-docs.dify.ai/2024/12/5987709c373903925ba8f639606aa554.png" alt=""><figcaption></figcaption></figure>

### プラグインのパッケージ化

プラグインが正常に動作することを確認したら、以下のコマンドラインツールでプラグインをパッケージ化できます。実行すると、現在のフォルダに `telegram.difypkg` ファイルが作成されます。これがプラグインの最終的なパッケージです。

```
dify plugin package ./telegram
```

おめでとうございます！ツールタイプのプラグイン開発、デバッグ、パッケージ化の全工程が完了しました。

### プラグインの公開

作成したプラグインは、[Dify Plugins コードリポジトリ](https://github.com/langgenius/dify-plugins) にアップロードして公開できます。アップロード前に、プラグインが[プラグイン公開ガイド](../../publish-plugins/publish-to-dify-marketplace.md) に準拠していることを確認してください。承認されると、コードはmasterブランチにマージされ、[Dify Marketplace](https://marketplace.dify.ai/) で自動的に公開されます。

### 参考情報

Difyプラグインのプロジェクトコード全体を確認したい場合は、[Githubコードリポジトリ](https://github.com/langgenius/dify-official-plugins) を参照してください。他のプラグインの完全なコードとその詳細も確認できます。

プラグインに関する詳細は、以下のコンテンツをご覧ください。

**クイックスタート:**

* [拡張タイププラグインの開発](../extension-plugin.md)
* [モデルタイププラグインの開発](../model-plugin/)
* [バンドルタイププラグイン：複数のプラグインをパッケージ化](../bundle.md)

**プラグイン仕様定義ドキュメント:**

* [マニフェスト](../../schema-definition/manifest.md)
* [エンドポイント](../../schema-definition/endpoint.md)
* [Difyサービスの逆呼び出し](../../schema-definition/reverse-invocation-of-the-dify-service/)
* [ツール](../../../guides/tools/)
* [モデル](../../schema-definition/model/model-schema.md)
* [エージェント戦略の拡張](../../schema-definition/agent.md)
