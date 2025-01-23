---
description: 'Author: Allen'
---

# 安装与使用插件

### 安装插件

点击 Dify 平台右上角的“插件”，前往插件管理页，支持通过 **Marketplace、GitHub、本地上传**三种方式安装插件。

<figure><img src="https://assets-docs.dify.ai/2025/01/a56c40245090d9252557dcc6f4064a14.png" alt=""><figcaption><p>安装插件</p></figcaption></figure>

#### Marketplace

你可以选择任意插件，点击“安装”按钮即可轻松将插件安装至当前 Workspace 内。

![通过 Marketplace 安装插件](https://assets-docs.dify.ai/2025/01/6ae8b661b7fa01b228a954d00ef552f3.png)

#### GitHub

你可以直接通过 GitHub 代码仓库链接安装插件。使用此方法安装插件时需确保插件满足代码规范。插件代码仓库需创建 Release 并在附件中包含 `.difypkg` 后缀的文件包。详细要求请参考[发布插件：GitHub](../publish-plugins/publish-plugin-on-personal-github-repo.md)。

<figure><img src="https://assets-docs.dify.ai/2025/01/4026a12a915e3fe9bd057d8827acfdce.png" alt=""><figcaption><p>GitHub Installation</p></figcaption></figure>

**本地上传**

将[插件打包](../publish-plugins/package-and-publish-plugin-file.md)后即可得到 `.difypkg` 后缀的文件包，常用于离线环境或测试环境，允许安装官方市场以外的插件文件。对于组织而言，可以开发维护内部插件并通过本地上传的方式安装，避免公开敏感信息。

#### 授权插件

部分插件在安装后可能还要求进行 API Key 或其它形式的授权，手动添加授权后才能正常使用。

> API Key 属敏感信息，授权仅对当前用户有效。团队中的其他人使用该插件时仍需手动输入授权密钥。

![授权插件](https://assets-docs.dify.ai/2024/11/972de4c9fa00f792a1ab734b080aafdc.png)

### 使用插件

将插件安装至 Workspace 后即可在 Dify 应用内进行使用。下文将简要介绍不同类型的插件对应不同的使用方法。

#### 模型插件

以 `OpenAI` 为例，安装模型插件后，点击右上角的**头像页 → 设置 → 模型供应商**，配置 API Key 即可激活该模型供应商。

<figure><img src="https://assets-docs.dify.ai/2025/01/3bf32d49975931e5924baa749aa7812f.png" alt=""><figcaption><p>授权 OpenAI API Key</p></figcaption></figure>

授权后可以在所有应用类型内选择并使用该大语言模型。

![使用模型类型插件](https://assets-docs.dify.ai/2024/12/4a38b1ea534ca68515839c518c250d2f.png)

#### 工具插件

工具插件支持在 Chatflow、Workflow、Agent 应用内使用。本章节将以 `Google` 工具插件为例，演示如何在以上应用类型内使用。

> 部分工具插件要求输入 API Key 授权后使用，因此在安装插件后可以进行配置以供后续使用。

#### Agent

创建 Agent 应用后，在应用编排页下方找到 **“工具”** 选项。选中已安装的工具插件。

使用应用时，输入使用工具的指令文本，例如输入 “当日新闻” 即可调用插件使用谷歌搜索引擎进行在线内容检索。

![Agent Tools](https://assets-docs.dify.ai/2024/12/78f833811cb0c3d5cbbb1a941cffc769.png)

#### Chatflow / Workflow

Chatflow 和 Workflow 类型应用共用一套工作流编排画布，因此使用工具插件的方法是一致的。

你可以点击节点末尾的 + 号，选择已安装的谷歌插件工具，并将节点与上游节点相连线。

![Chatflow / Workflow Tools](https://assets-docs.dify.ai/2024/12/7e7bcf1f9e3acf72c6917ea9de4e4613.png)

在插件的输入变量中填写用户输入的查询内容 query 变量，或其它需要在线检索的信息。

![Tools input](https://assets-docs.dify.ai/2024/12/a67c4cffd8fdf33297d462b2e6d01d27.png)

如需了解其它类型插件的使用方法，请参考插件详情页的指导使用插件。

<figure><img src="https://assets-docs.dify.ai/2025/01/9d826302637638f705a94f73bd653958.png" alt=""><figcaption><p>使用插件</p></figcaption></figure>

### 阅读更多

如需了解如何上手插件开发，请阅读以下内容：

{% content-ref url="develop-plugins/" %}
[develop-plugins](develop-plugins/)
{% endcontent-ref %}

