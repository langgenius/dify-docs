# 在 Dify 云端构建 AI Thesis Slack Bot

> 作者：Alec Lee。2025/03/11

## 1. 概述

随着信息时代的发展，学术研究的数量不断增长，研究人员需要更高效的方式获取最新的学术成果。AI Thesis Slack Bot 通过 AI 自动化工作流，帮助用户在 Slack 上快速获取 arXiv 论文的摘要。

它可以用于：

* 研究团队获取最新学术动态  
* 公司 AI 研究部门内部信息同步  
* 高校师生进行科研协作等场景需求

本指南将向您介绍如何搭建 AI Thesis Slack Bot，其核心工作原理，以及如何高效利用它提高生产力。

## 2. 准备工作

### 2.1 配置 OpenAI API

* 在帐户下的模型设置里配置 OpenAI 并安装 API 密钥。

![API](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/001API.jpg)

### 2.2 安装 ArXiv 和 Slack 插件

* 在 Dify 的工具里安装 **ArXiv** 和 **Slack**。

<img src="https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/002SlackArXiv.jpg" alt="Slack ArXiv" width="400"/>

### 2.3 Slack 账户创建

* 在 [Slack 官方网站](https://slack.com/intl/en-gb/get-started?entry_point=help_center#/createnew) 创建一个免费的 Slack 账户。

![Slack](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/003SlackAccount.jpg)

## 3. AI Thesis Slack Bot 的工作流搭建

a.用户在 Dify AI Thesis Slack Bot 里输入关键词（如"Large Language Model"）。 

b.机器人从 arXiv 检索相关论文，筛选最新的研究成果（例2024 年 1 月 1 日后的论文）。 

c.使用 GPT-4o 进行智能整理，读取论文并生成摘要，推送到 Slack 指定的 Channel 里，格式如下：

* 📄 论文标题  
* 👤 作者  
* 📆 发布日期  
* 📌 核心内容概述 

d.机器人自动将摘要推送到 Slack，团队成员可以第一时间在 Slack 频道或私聊中查看最新的论文信息。


## 4. 具体步骤

#### 4.1 创建工作流

a.在 Dify 主页面 选择 Create from Blank，然后选择 Workflow，输入名称（AI Thesis Slack Bot）。

![Create from Blank](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/004Createfromblank.jpg)

  b.在 Tools 里 选择已安装好的 ArXiv Search。

![Tools ArXiv](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/005ToolsArXiv.jpg)

c.在节点里选择 LLM，并设置已配置好的 OpenAI 模型。

![LLM](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/006LLM.jpg)

d.在 Tools 里 选择已安装的 Slack Incoming Webhook 并点击 Authorize，添加 Slack Webhook URL。

![Slack Incoming Webhook](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/007Slackincomingwebhook.jpg)

#### 4.2 添加 Slack Webhook URL

a.进入 [Slack API 管理页面](https://api.slack.com/apps)，点击 **Create New App**（创建新应用）。

![Slack API](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/008Slackapi.jpg)

b.选择 "From scratch"（从零开始），输入应用名称（如 AI Thesis Bot），选择要发送消息的 Slack 频道。

![From Scratch](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/009Fromscratch.jpg)

c.进入 Incoming Webhooks，激活 Activate Incoming Webhooks。点击 Add New Webhook to Workspace，选择 Slack 频道，复制生成的 Webhook URL。

![Incoming Webhooks Activate](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/010IncomingwebhooksActivate.jpg)

d.粘贴 Webhook URL 到 Slack 节点 的 Slack Webhook URL 位置。

![Slack Webhook URL](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/011SlackWehookURL.jpg)

e.选择工作流最后一个节点End后，整理工作节点组建都链接好了。下面就需要配置各个节点上的参数。

![End](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/012End.jpg)

#### 4.3 配置各个节点的参数

a.Start 节点：设置关键词查询参数。

![Start](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/013StartNode.jpg)

b.ArXiv Search 节点：添加 Query String 内容（可按需求调整）。

<img src="https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/014ArvPara.jpg" alt="ArXiv Search" width="400"/>

c.LLM 节点：选择模型,添加 CONTEXT,在 SYSTEM 里进行 Prompt Engineering（可按需求定制）,在 USER 里选择 Context.

![LLM Context](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/015LLMcontext.jpg)

d.Slack 节点：在 Content 里选择 LLM/Text String。

![Slack Content](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/016SlackEndP.jpg)

#### 4.4 测试和发布

a.在发布前 **试运行**，确认工作流程是否跑通后，点击 发布。

![Shiyunxing](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/018TestInupt.jpg)

b. 如果确认到 Dify 的搜索结果和Slack上的传输内容，恭喜您，跑通了。 

![Last P](https://raw.githubusercontent.com/aleclee1005/MyPic/refs/heads/img/019LastPTest.jpg)

## 5. 未来优化方向

目前，AI Thesis Slack Bot 主要专注于 arXiv 论文检索和摘要推送，后续可以优化： 
✅ 提高摘要质量：改进 LLM Prompt 提高精准度。 
✅ 积累检索结果：建立数据库存储历史论文。 
✅ 扩展更多数据源：支持 IEEE、Springer、ACL 等。 
✅ 个性化推荐：基于用户兴趣推送相关论文。 
✅ 多平台支持：兼容 WhatsApp、Teams、WeChat 等。

## 6. 结语

通过 AI Thesis Slack Bot，您可以实现学术信息的智能自动化推送，提升研究团队的生产力。如果希望进一步探索 AI Thesis Bot 的潜能，可以结合 Dify 和 Realtime API，开发更高级的应用，如 实时论文讨论 和 智能问答，让 AI 在学术交流和 AI 应用中发挥更大作用！ 🚀
