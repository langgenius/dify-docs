# Developing a Plugin that Integrated with Telegram Bot

### **Project Background**

Integrating LLM services with popular real-time chat platforms (IM) has always been a hot topic for best practices. The Dify plugin ecosystem is dedicated to supporting simpler, more user-friendly integration methods. This article will use Telegram as an example to detail how to develop a plugin that connects to a Telegram Bot.

[Telegram](https://telegram.org/) is a free and open real-time communication platform that provides rich APIs, including a user-friendly Webhook feature, which is an event-based mechanism. We'll use this mechanism to create a Telegram Bot plugin, as shown in the following diagram:

<figure><img src="https://assets-docs.dify.ai/2024/12/08d0cc0074efe3b81b15ade2d888e785.png" alt=""><figcaption></figcaption></figure>

**Integration Map:**

1.  **User uses Telegram Bot**

    When a user sends a message in Telegram, Telegram sends an HTTP request to the Dify plugin.
2.  **Message forwarded to Telegram Bot Plugin**

    Like an email system needing a recipient's address, when using a Telegram bot, messages need to be forwarded back to the Dify application for processing. This can be done by configuring a Telegram Webhook address through Telegram's API and entering it into the plugin for connection.
3.  **Plugin receives message and returns to a Dify application**

    The plugin processes Telegram's request, analyzes what the user has input, and calls a Dify App to get the reply content.
4.  **Dify application responds and returns message to Telegram Bot**

    After receiving the Dify application's reply, the plugin returns the message back to the Telegram Bot through the same route, allowing users to interact directly with the Dify application while using Telegram.

### Prerequisites

* Apply for a Telegram Bot
* Dify plugin scaffolding tool
* Python environment, version ≥ 3.10

#### **Apply for Telegram Bot**

Follow [@BotFather's](https://t.me/BotFather) guide to create a new bot. For detailed creation process, refer to [Telegram's official documentation](https://core.telegram.org/bots/tutorial).

After creation, you'll receive an HTTP API Token for use in subsequent steps.

<figure><img src="https://assets-docs.dify.ai/2024/12/668783d0362200257b2cb5385ecbacff.png" alt="" width="375"><figcaption></figcaption></figure>

**Install Dify Plugin Scaffolding Tool**

For more details, please take refer to [initialize-development-tools.md](../initialize-development-tools.md "mention")

**Initializing the Python Environment**

See the [Python Installation Tutorial](https://pythontest.com/python/installing-python-3-11/) for detailed instructions, or ask LLM for a complete installation tutorial.

### Developing Plugins

Now let's begin the actual plugin coding work. Before starting, make sure you've read [Quick Start: Developing Extension Type Plugin](../extension-plugin.md), or have previously developed a Dify plugin.

#### **Initialize Project**

Run the following command to initialize the plugin development project:

```bash
./dify-plugin-darwin-arm64 plugin init
```

Follow the prompts to fill in the project's basic information, select the `extension` template, and grant both `Apps` and `Endpoints` permissions in the permissions section.

For more information about plugins making reverse request to Dify platform capabilities, please refer to [Reverse Invocation: App](../../schema-definition/reverse-invocation-of-the-dify-service/).

<figure><img src="https://assets-docs.dify.ai/2024/12/d89a6282c5584fc43a9cadeddf09c0de.png" alt=""><figcaption><p>Plugins permission</p></figcaption></figure>

#### **1. Edit Configuration Form**

In this plugin, you need to specify which Dify App to use for replies, and you'll need the Telegram bot token when replying, so these two fields need to be added to the plugin form.

Modify the yaml file under the group path, for example `group/your-project.yaml`. The form configuration filename is determined by the basic information provided when creating the plugin, and you can modify the corresponding yaml file.

**Example Code:**

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

Code data structure description:

```
  - name: app
    type: app-selector
    scope: chat
```

* Users can access a particular Dify application and forward messages when using the plugin.
* The scope field is specified as a chat field Only apps such as agent, chatbot, chatflow can be used.

**Examples**:

`endpoints/your_path.yaml`

```yaml
path: "/your_project/message"
method: "POST"
extra:
  python:
    source: "endpoints/your_project.py"
```

#### 2. Edit Feature Code

Edit `endpoints/your_project.py` file, add the following code:

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

#### 2.1 Debug Plugins

Dify provides remote debugging method, go to "Plugin Management" page to get the debugging key and remote server address.

<figure><img src="https://assets-docs.dify.ai/2024/12/053415ef127f1f4d6dd85dd3ae79626a.png" alt=""><figcaption></figcaption></figure>

Go back to the plugin project, copy the `.env.example` file and rename it to .env. Fill it with the remote server address and debugging key.

The `.env` file:

```bash
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=localhost
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=****-****-****-****-****
```

Run the `python -m main` command to launch the plugin. You can see on the plugin page that the plugin has been installed into Workspace. Other team members can also access the plugin.

```bash
python -m main
```

#### Setting Plugin Endpoint

Find the auto-installed test plugin in Dify's plugin management page, create a new Endpoint, fill in the name, Bot token, and select the app you need to connect to.

![Debugging Plugin](https://assets-docs.dify.ai/2024/12/93f1bc3d52635ff5bf177331caaf7afa.png)

Copy the URL from the plugin and combine it with the following command to form a test request command.

Where `<hook_url>` is filled in with the address you just copied, and `<bot_token>` is filled in with the Telegram HTTP API Token obtained in the [prep](developing-a-plugin-that-integrated-with-telegram-bot.md#prerequisites).

```bash
curl -F "url=<hook_url>" https://api.telegram.org/bot<bot_token>/setWebhook
```

After execution, you should see the following result:

<figure><img src="https://assets-docs.dify.ai/2024/12/4e2a924cfed25ea88d6692d55fac39e3.png" alt=""><figcaption><p>curl response</p></figcaption></figure>

Send a message to the Telegram bot and you can see that it repeats the message we sent as is, indicating that the plugin has correctly established a connection with the Telegram bot.

<figure><img src="https://assets-docs.dify.ai/2024/12/a7c4f708fd0c11734f3359c1e1b6ad5a.png" alt=""><figcaption></figcaption></figure>

#### 2.2 Reply with the Dify App

Modify the function code to add code to reply using the Dify App:

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

The code uses `self.session.app.chat.invoke` to call an App within the Dify platform, passing information such as `app_id` and `query`, and finally returns the response content to the Telegram Bot.

After restarting the plugin and debugging again, it can be found that the Telegram Bot has correctly output the reply message from the Dify App.

<figure><img src="https://assets-docs.dify.ai/2024/12/5987709c373903925ba8f639606aa554.png" alt=""><figcaption></figcaption></figure>

### Packing Plugin

After confirming that the plugin works properly, you can package and name the plugin with the following command line tool. After running it you can find the `telegram.difypkg` file in the current folder, which is the final plugin package.

```
dify plugin package ./telegram
```

Congratulations, you have completed the complete development, debugging and packaging process of a tool type plugin!

### Publishing Plugins

You can now publish your plugin by uploading it to the [Dify Plugins code repository](https://github.com/langgenius/dify-plugins)! Before uploading, make sure your plugin follows the [plugin release guide](../../publish-plugins/publish-to-dify-marketplace.md). Once approved, the code will be merged into the master branch and automatically live in the [Dify Marketplace](https://marketplace.dify.ai/).

### Reference

If you want to see the full project code for the Dify plugin, head over to the [Github code repository](https://github.com/langgenius/dify-official-plugins). In addition to that, you can see the full code of other plugins with specific details.

If you want to know more about the plugin, please refer to the following content.

**Quick Start:**

* [Develop Extension Type Plugin](../extension-plugin.md)
* [Develop Model Type Plugin](../model-plugin/)
* [Bundle Type Plugin: Package Multiple Plugins](../bundle.md)

**Plugins Specification Definition Documentaiton:**

* [Minifest](../../schema-definition/manifest.md)
* [Endpoint](../../schema-definition/endpoint.md)
* [Reverse Invocation of the Dify Service](../../schema-definition/reverse-invocation-of-the-dify-service/)
* [Tools](../../../guides/tools/)
* [Models](../../schema-definition/model/model-schema.md)
* [Extend Agent Strategy](../../schema-definition/agent.md)



