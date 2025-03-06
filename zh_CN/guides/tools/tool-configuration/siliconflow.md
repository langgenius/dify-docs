# SiliconFlow (支持 Flux 绘图)

> 工具作者 @hjlarry

SiliconCloud 基于优秀的开源基础模型，提供高性价比的 GenAI 服务。你可以通过 **SiliconFlow** 在 Dify 内调用 Flux 、Stable Diffusion 绘图模型，搭建你的专属 AI 绘图应用。以下是在 Dify 中配置 SiliconFlow 工具的步骤。

### 1. 申请 SiliconCloud API Key

请在 [SiliconCloud API 管理页面](https://cloud.siliconflow.cn/account/ak) 新建 API Key 并保证有足够余额。

### 2. 在 Dify 内填写配置

在 Dify 的工具页中点击 `SiliconCloud > 去授权` 填写 API Key。

<figure><img src="https://assets-docs.dify.ai/img/zh_CN/tool-configuration/b21f0c07957271d293bccf95985827cf.webp" alt=""><figcaption></figcaption></figure>

### 3. 使用工具

* **Chatflow / Workflow 应用**

Chatflow 和 Workflow 应用均支持添加 `SiliconFlow` 工具节点。

将用户输入的内容通过[变量](../../workflow/variables.md)传递至 Siliconflow 工具的 Flux 或 Stable Diffusion 节点内的“提示词”“负面提示词”框中，按照需求调整内置参数，最后在“结束”节点的回复框中选中 Siliconflow 工具节点的输出内容（文本、图片等）。

<figure><img src="https://assets-docs.dify.ai/img/zh_CN/tool-configuration/54d1f190b238e57b276e41ff4a60b21a.webp" alt=""><figcaption></figcaption></figure>

* **Agent 应用**

在 Agent 应用内添加 `Stable Diffusion` 或 `Flux` 工具，然后在对话框内发送图片描述，调用工具生成 AI 图像。

<figure><img src="https://assets-docs.dify.ai/img/zh_CN/tool-configuration/28886349b35e6a644cfe867d7bc6545e.webp" alt=""><figcaption></figcaption></figure>

<figure><img src="https://assets-docs.dify.ai/img/zh_CN/tool-configuration/91406c48e7ea85da374869f747fa3664.webp" alt=""><figcaption></figcaption></figure>
