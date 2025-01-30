# DeepSeek & Dify Integration Guide: Building AI Applications with Multi-Turn Reasoning

## Overview

[DeepSeek](https://www.deepseek.com/) is a next-generation open-source large language model that offers multiple access methods: **web interface, mobile apps, and API**. While the official web and mobile interfaces provide an intuitive user experience, they may face service stability issues or registration restrictions due to high traffic.

In contrast, the API provides a more stable and reliable access method. However, using the API alone lacks a user-friendly interface and is not ideal for team collaboration. To address this, this guide explains how to integrate the DeepSeek API with the Dify platform to achieve:

- Rapidly building an AI chatbot powered by the DeepSeek R1 model.
- Enabling Retrieval-Augmented Generation (RAG) capabilities to create AI applications combining DeepSeek R1 with a knowledge base.

> For data security reasons, you can also deploy both Dify and DeepSeek on a private server. See [Deploy DeepSeek + Dify Locally to Build a Private AI Assistant](./private-ai-deepseek-dify.md) for details.

---

## Prerequisites

### 1. Obtain DeepSeek API Key

Visit the [DeepSeek API Platform](https://platform.deepseek.com/) and follow the instructions to request an API Key.

> If the link is inaccessible, consider deploying DeepSeek locally. See the [local deployment guide](./private-ai-deepseek-dify.md) for more details.

### 2. Register on Dify

Dify is a platform that helps you quickly build generative AI applications. By integrating DeepSeek’s API, you can easily create a functional DeepSeek-powered AI app.

---

## Integration Steps

### 1. Connect DeepSeek to Dify

Go to the Dify platform and navigate to **Profile → Settings → Model Providers**. Locate DeepSeek, paste the API Key obtained earlier, and click **Save**. Once validated, you will see a success message.

![](https://assets-docs.dify.ai/2025/01/a7d6b4e05a3c9d85d0cb42f4dd018bc8.png)

---

### 2. Create a DeepSeek AI Application

1. On the Dify homepage, click **Create Blank App** on the left sidebar and select **Chatbot**. Give it a simple name.

![](https://assets-docs.dify.ai/2025/01/7f56bc3c836c7248043b656fa95e474e.png)

2. Choose the `deepseek-reasoner` model.

> The deepseek-reasoner model is also known as the deepseek-r1 model.

![](https://assets-docs.dify.ai/2025/01/de134c6285985fe1552223eb33641b9f.png)

Once configured, you can start interacting with the chatbot.

![](https://assets-docs.dify.ai/2025/01/3760e9a0cb7c2070978134d8f7f13929.png)

---

### 3. Enable Text Analysis with Knowledge Base

[Retrieval-Augmented Generation (RAG)](https://docs.dify.ai/zh-hans/learn-more/extended-reading/retrieval-augment) is an advanced technique that enhances AI responses by retrieving relevant knowledge. By providing the model with necessary contextual information, it improves response accuracy and relevance. When you upload internal documents or domain-specific materials, the AI can generate more informed answers based on this knowledge.

#### 3.1 Create a Knowledge Base

Upload documents containing information you want the AI to analyze. To ensure DeepSeek accurately understands document content, it is recommended to use the **Parent-Child Segmentation** mode. This preserves document hierarchy and context. See [Create a Knowledge Base](https://docs.dify.ai/zh-hans/guides/knowledge-base/create-knowledge-and-upload-documents) for detailed steps.

![](https://assets-docs.dify.ai/2025/01/f38af53d2b124391e2ea32f29da7d87d.png)

#### 3.2 Integrate the Knowledge Base into the AI App

In the AI app's **Context** settings, add the knowledge base. When users ask questions, the LLM will first retrieve relevant information from the knowledge base before generating a response.

![](https://assets-docs.dify.ai/2025/01/4254ec131fece172a59304414a060f4e.png)

---

### 4. Share the AI Application

Once built, you can share the AI application with others or integrate it into other websites.

![](https://assets-docs.dify.ai/2025/01/d32857964683b48027d20d029e7e06c0.png)

---

## Further Reading

Beyond simple chatbot applications, you can also use Chatflow or Workflow to build more complex AI solutions with capabilities like document recognition, image processing, and speech recognition. See the following resources for more details:

- [Workflow](https://docs.dify.ai/zh-hans/guides/workflow)
- [File Upload](https://docs.dify.ai/zh-hans/guides/workflow/file-upload)
- [Deploy DeepSeek + Dify Locally to Build a Private AI Assistant](./private-ai-deepseek-dify.md)