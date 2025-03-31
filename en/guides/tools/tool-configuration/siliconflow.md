# SiliconFlow (Flux AI Supported)

> Tool author @hjlarry.

{% hint style="warning" %}
"Tools" has been fully upgraded to the "Plugins". For more details, please refer to [Install and Use Plugins](https://docs.dify.ai/plugins/quick-start/install-plugins). The content below has been archived.
{% endhint %}

SiliconFlow provides high-quality GenAI services based on excellent open-source foundation models. You can use SiliconFlow in Dify to call image generation models like Flux and Stable Diffusion, and build your own AI image generation application.

## 1. Apply for SiliconCloud API Key

Create a new API Key on the [SiliconCloud API management page](https://cloud.siliconflow.cn/account/ak) and ensure that you have sufficient balance.

## 2. Fill in the Configuration in Dify

In the Dify tool page, click on `SiliconCloud > To Authorize` and fill in the API Key.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.04.16.png" alt=""><figcaption></figcaption></figure>

## 3. Using the Tool

* **Chatflow/Workflow Application**

Chatflow and Workflow applications both support adding `SiliconFlow` tool nodes. You can pass user input content to the SiliconFlow tool node's "prompt" and "negative prompt" boxes through [variables](https://docs.dify.ai/v/zh-hans/guides/workflow/variables), adjust the built-in parameters as needed, and finally select the output content (text, images, etc.) of the SiliconFlow tool node in the "end" node's reply box.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.17.40.png" alt=""><figcaption></figcaption></figure>

* **Agent Application**

In the Agent application, add the `Stable Diffusion` or `Flux` tool, and then send a picture description in the conversation box to call the tool to generate images.

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.14.16.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/截屏2024-09-27 13.13.06.png" alt=""><figcaption></figcaption></figure>
