---
description: Learn about the Different Models Supported by Dify.
---

# Model Configuration

Dify supports major model providers like OpenAI's GPT series and Anthropic's Claude series. Each model's capabilities and parameters differ, so select a model provider that suits your application's needs. **Obtain the API key from the model provider's official website before using it in Dify.**

## Model Types in Dify

Dify classifies models into 4 types, each for different uses:

1.  **System Inference Models:** Used in applications for tasks like chat, name generation, and suggesting follow-up questions.

    > Providers include [OpenAI](https://platform.openai.com/account/api-keys)、[Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)、[Anthropic](https://console.anthropic.com/account/keys)、Hugging Face Hub、Replicate、Xinference、OpenLLM、[iFLYTEK SPARK](https://www.xfyun.cn/solutions/xinghuoAPI)、[WENXINYIYAN](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)、[TONGYI](https://dashscope.console.aliyun.com/api-key\_management?spm=a2c4g.11186623.0.0.3bbc424dxZms9k)、[Minimax](https://api.minimax.chat/user-center/basic-information/interface-key)、ZHIPU(ChatGLM).
2.  **Embedding Models:** Employed for embedding segmented documents in knowledge and processing user queries in applications.

    > Providers include OpenAI, ZHIPU (ChatGLM), Jina AI([Jina Embeddings 2](https://jina.ai/embeddings/)).
3.  [**Rerank Models**](https://docs.dify.ai/advanced/retrieval-augment/rerank)**:** Enhance search capabilities in LLMs.

    > Provider: Cohere.
4.  **Speech-to-Text Models:** Convert spoken words to text in conversational applications.

    > Provider: OpenAI.

1. System Reasoning Model. In the created application, this type of model is used. Smart chat, dialogue name generation, and next question suggestions also use reasoning models.
2. Embedding Model. In the knowledge, this type of model is used to embedding segmented documents. In applications that use data sets, this type of model is also used to process user questions as Embedding.
3. Speech-to-Text model. In conversational applications, this type of model is used to convert speech to text.

Dify plans to add more LLM providers as technology and user needs evolve.

## Hosted Model Trial Service&#x20;

Dify offers trial quotas for cloud service users to experiment with different models. Set up your model provider before the trial ends to ensure uninterrupted application use.

* OpenAI Hosted Model Trial: Includes 200 invocations for models like GPT3.5-turbo, GPT3.5-turbo-16k, text-davinci-003 models.

## Setting the Default Model

Dify automatically selects the default model based on usage. Configure this in `Settings > Model Provider`.

<figure><img src="../../.gitbook/assets/spaces_CdDIVDY6AtAz028MFT4d_uploads_git-blob-db1690fa587d6135e70621a88aa6650ac4e4015a_image (15).webp" alt=""><figcaption></figcaption></figure>

## Model Integration Settings&#x20;

Choose your model in Dify's `Settings > Model Provider`.

<figure><img src="../../.gitbook/assets/spaces_CdDIVDY6AtAz028MFT4d_uploads_git-blob-97bdd290e257e10a5bfa723d02eea8fd0b159a9d_image (16).webp" alt=""><figcaption></figcaption></figure>

Model providers fall into two categories:

1. Proprietary Models: Developed by providers such as OpenAI and Anthropic.
2. Hosted Models: Offer third-party models, like Hugging Face and Replicate.

Integration methods differ between these categories.

**Proprietary Model Providers:** Dify connects to all models from an integrated provider. Set the provider's API key in Dify to integrate.

{% hint style="info" %}
Dify uses [PKCS1\_OAEP](https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html) encryption to protect your API keys. Each user (tenant) has a unique key pair for encryption, ensuring your API keys remain confidential.
{% endhint %}

**Hosted Model Providers:** Integrate third-party models individually.

Specific integration methods are not detailed here.

* [Hugging Face](https://docs.dify.ai/advanced/model-configuration/hugging-face)
* [Replicate](https://docs.dify.ai/advanced/model-configuration/replicate)
* [Xinference](https://docs.dify.ai/advanced/model-configuration/xinference)
* [OpenLLM](https://docs.dify.ai/advanced/model-configuration/openllm)

## Using Models&#x20;

Once configured, these models are ready for application use.

<figure><img src="../../.gitbook/assets/spaces_CdDIVDY6AtAz028MFT4d_uploads_git-blob-c1d474492bf80233df65284bdd8413f17930ae70_image.webp" alt=""><figcaption></figcaption></figure>
