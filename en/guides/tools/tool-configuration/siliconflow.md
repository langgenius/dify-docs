# SiliconFlow (Flux AI Supported)

> Tool author @hjlarry.

SiliconFlow provides high-quality GenAI services based on excellent open-source foundation models. You can use SiliconFlow in Dify to call image generation models like Flux and Stable Diffusion, and build your own AI image generation application.

## 1. Apply for SiliconCloud API Key

Create a new API Key on the [SiliconCloud API management page](https://cloud.siliconflow.cn/account/ak) and ensure that you have sufficient balance.

## 2. Fill in the Configuration in Dify

In the Dify tool page, click on `SiliconCloud > To Authorize` and fill in the API Key.

<figure><img src="https://assets-docs.dify.ai/img/en/tool-configuration/60148f07cd10c270fad8e49677f97748.webp" alt=""><figcaption></figcaption></figure>

## 3. Using the Tool

* **Chatflow/Workflow Application**

Chatflow and Workflow applications both support adding `SiliconFlow` tool nodes. You can pass user input content to the SiliconFlow tool node's "prompt" and "negative prompt" boxes through [variables](https://docs.dify.ai/v/zh-hans/guides/workflow/variables), adjust the built-in parameters as needed, and finally select the output content (text, images, etc.) of the SiliconFlow tool node in the "end" node's reply box.

<figure><img src="https://assets-docs.dify.ai/img/en/tool-configuration/df1f7f81b119e6bb2c62010dc5a8dc4a.webp" alt=""><figcaption></figcaption></figure>

* **Agent Application**

In the Agent application, add the `Stable Diffusion` or `Flux` tool, and then send a picture description in the conversation box to call the tool to generate images.

<figure><img src="https://assets-docs.dify.ai/img/en/tool-configuration/ca9d68592cbddf1e25a57284605270b5.webp" alt=""><figcaption></figcaption></figure>

<figure><img src="https://assets-docs.dify.ai/img/en/tool-configuration/e26ed41f76b6b82ed0e084805e21e245.webp" alt=""><figcaption></figcaption></figure>
