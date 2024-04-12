# 手摸手教你把 Dify 接入微信生态

> 作者：韩方圆，"Dify on WeChat"开源项目作者

## 1. 概述

微信作为最热门的即时通信软件，拥有巨大的流量。

微信友好的聊天窗口是天然的AI应用LUI(Language User Interface)/CUI(Command User Interface)。

微信不仅有个人微信，同时提供了公众号、企业微信、企业微信应用、企业微信客服等对话渠道，拥有良好的微信生态。

把Dify应用接入微信生态，就能打造一个功能强大的智能客服，大大降低客服成本，同时也能够提升客户体验。本篇教程就是手摸手地教你如何利用[Dify on WeChat](https://github.com/hanfangyuan4396/dify-on-wechat)项目，把Dify应用接入微信生态。

## 2. Dify接入个人微信

### 2.1. 准备工作

#### 2.1.1. 创建聊天助手

##### （1）Dify简介

Dify是一个优秀的LLMOps（大型语言模型运维）平台，Dify的详细介绍请移步官方文档[欢迎使用 Dify | 中文 | Dify](https://docs.dify.ai/v/zh-hans)。

##### （2）登录Dify官方应用平台

首先，登录[Dify官方应用平台](https://cloud.dify.ai/signin)，你可以选择使用Github登录或者使用Google登录。此外，你也可以参考Dify官方教程[Docker Compose 部署 | 中文 | Dify](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/docker-compose) 私有部署，Dify是开源项目，支持私有部署。

<figure><img src="../../.gitbook/assets/dify-on-wechat/login.jpg" alt=""><figcaption></figcaption></figure>

##### （3）创建Dify基础编排聊天助手应用
<figure><img src="../../.gitbook/assets/dify-on-wechat/create-basic-chatbot.jpg" alt=""><figcaption></figcaption></figure>

登录成功后，进入Dify页面，我们按照下方步骤创建一个基础编排聊天助手应用

1. 点击页面上方的工作室
2. 创建空白应用
3. 应用类型选择聊天助手
4. 聊天助手编排方式选择基础编排
5. 选择应用图标并为应用填写一个名称，比如基础编排聊天助手
6. 点击创建

<figure><img src="../../.gitbook/assets/dify-on-wechat/config-basic-chatbot.jpg" alt=""><figcaption></figcaption></figure>
创建成功后我们会跳转到上图所示页面，我们继续配置应用

1. 选择模型，如gpt-3.5-turbo-0125
2. 设置模型参数
3. 填写应用提示词
<figure><img src="../../.gitbook/assets/dify-on-wechat/publish-basic-chatbot.jpg" alt=""><figcaption></figcaption></figure>

在配置完成后，我们可以在右侧对话框进行测试，在测试完成后，进行如下操作

1. 发布
2. 更新
3. 访问API

##### （4）生成基础编排聊天助手API密钥
<figure><img src="../../.gitbook/assets/dify-on-wechat/create-basic-chatbot-apikey.jpg" alt=""><figcaption></figcaption></figure>

在点击"访问API"后，我们会跳转到上图的API管理页面，在这个页面我们按照如下步骤获取API密钥：

1. 点击右上角API密钥
2. 点击创建密钥
3. 复制保存密钥

在保存密钥后，还需要查看右上角的API服务器，如果是Dify官网的应用，API服务器地址为 "https://api.dify.ai/v1", 如果是私有部署的，请确认你自己的API服务器地址。

至此，创建聊天助手的准备工作结束，在此小节中我们只需要保存好两个东西：**API密钥**与**API服务器地址**

#### 2.1.2. 下载Dify on WeChat项目

##### （1）Dify on WeChat项目简介

[Dify on WeChat](https://github.com/hanfangyuan4396/dify-on-wechat)是[ ChatGPT on WeChat](https://github.com/zhayujie/chatgpt-on-wechat)的下游分支，额外实现了对接[Dify](https://github.com/langgenius/dify) API，支持Dify聊天助手、支持Agent调用工具和知识库，支持Dify工作流，详情请查看GitHub仓库[Dify on WeChat](https://github.com/hanfangyuan4396/dify-on-wechat)。

##### （2）下载代码并安装依赖

1. 下载项目代码

```bash
git clone https://github.com/hanfangyuan4396/dify-on-wechat
cd dify-on-wechat/
```

2. 安装python

Dify on WeChat项目使用python语言编写，请在[python官网](https://www.python.org/downloads/)下载安装python，推荐安装python3.8以上版本，我在ubuntu测试过3.11.6版本，可以正常运行。

3. 安装核心依赖（必选）：

```bash
pip3 install -r requirements.txt  # 国内可以在该命令末尾添加 "-i https://mirrors.aliyun.com/pypi/simple" 参数，使用阿里云镜像源安装依赖
```

4. 拓展依赖 （可选，建议安装）：

```bash
pip3 install -r requirements-optional.txt # 国内可以在该命令末尾添加 "-i https://mirrors.aliyun.com/pypi/simple" 参数，使用阿里云镜像源安装依赖
```

##### （3）填写配置文件

我们在项目根目录创建名为config.json的文件，文件内容如下，我们在**2.1.1小节（4）**
最后保存了**API密钥**与**API服务器地址**，请把**dify_api_base**配置为**API服务器地址**；**dify_api_key**配置为**API密钥。**其他配置保持不变

```bash
{ 
  "dify_api_base": "https://api.dify.ai/v1",
  "dify_api_key": "app-xxx",
  "dify_app_type": "chatbot",
  "channel_type": "wx",
  "model": "dify",
  "single_chat_prefix": [""],
  "single_chat_reply_prefix": "",
  "group_chat_prefix": ["@bot"],
  "group_name_white_list": ["ALL_GROUP"]
}
```

### 2.2. 把基础编排聊天助手接入微信

#### 2.2.1. 快速启动测试

##### （1）在Dify on Wechat项目根目录执行如下命令

```bash
cd dify-on-wechat
python3 app.py   # windows环境下该命令通常为 python app.py
```

##### （2）扫码登录
<figure><img src="../../.gitbook/assets/dify-on-wechat/wechat-login.jpg" alt=""><figcaption></figcaption></figure>


本项目使用itchat实现个人微信登录，有封号风险，建议使用**实名认证**过的**微信小号**进行测试，在执行上述命令后，我们可以在控制台看到打印如上图所示二维码，使用微信扫码登录，登录后当看到"itchat:Start auto replying."字符，表示登录成功，我们可以进行测试。

##### （3）对话测试
<figure><img src="../../.gitbook/assets/dify-on-wechat/basic-chatbot-on-wechat.jpg" alt=""><figcaption></figcaption></figure>

我们看到，微信机器人的回复与在Dify测试页面上的回复一致。至此，恭喜你成功把Dify接入了个人微信🎉🎉🎉

##### （4）服务器部署

1. 源码部署

```bash
cd dify-on-wechat
nohup python3 app.py & tail -f nohup.out   # 在后台运行程序并通过日志输出二维码
```

2. docker部署

```bash
cd dify-on-wechat/docker       # 进入docker目录
docker compose up -d           # 启动docker容器
docker logs -f dify-on-wechat  # 查看二维码并登录
```

### 2.3. 把工作流编排聊天助手接入微信

在把Dify基础的聊天助手应用接入微信后，我们接下来增加难度，尝试把工作流编排聊天助手应用接入微信，实现一个具有Dify平台知识的微信智能客服，为我们解答Dify工作流相关知识。

#### 2.3.1. 创建知识库

##### （1）下载知识库文件
<figure><img src="../../.gitbook/assets/dify-on-wechat/download-dify-workflow-knowledge.jpg" alt=""><figcaption></figcaption></figure>

我们到[dify文档仓库](https://github.com/langgenius/dify-docs/blob/main/zh_CN/guides/workflow/introduce.md)下载Dify工作流介绍的文档。

##### （2）Dify中导入知识库
<figure><img src="../../.gitbook/assets/dify-on-wechat/create-knowledge-1.jpg" alt=""><figcaption></figcaption></figure>

进入知识库页面，创建知识库

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-knowledge-2.jpg" alt=""><figcaption></figcaption></figure>
选择导入已有文本，上传刚才下载的introduce.md文件，点击下一步

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-knowledge-3.jpg" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-knowledge-4.jpg" alt=""><figcaption></figcaption></figure>

选择如下配置

- 分段设置：自动分段与清洗
- 索引方式：高质量
- 检索设置：向量检索

最后点击保存并处理

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-knowledge-5.jpg" alt=""><figcaption></figcaption></figure>

我们看到知识库正在进行嵌入处理，稍等片刻，即可嵌入成功。

#### 2.3.2. 创建工作流编排聊天助手

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-1.jpg" alt=""><figcaption></figcaption></figure>

我们进入Dify工作室，点击从应用模板创建

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-2.jpg" alt=""><figcaption></figcaption></figure>

我们使用知识库+聊天机器人类型的模板，设置应用图标与名称，点击创建


<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-3.jpg" alt=""><figcaption></figcaption></figure>

跳转到工作流编排页面后，先点击知识检索节点，点击最右侧"+"添加知识库。我们选择之前上传好的introduce.md知识库，该知识库是对Dify工作流的基本介绍。最后我们点击添加，知识库节点设置完成。


<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-4.jpg" alt=""><figcaption></figcaption></figure>

接下来选择LLM节点，点击设置上下文，我们选择result变量，该变量存有知识检索的结果。


<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-5.jpg" alt=""><figcaption></figcaption></figure>

设置完LLM节点后，我们点击预览进行测试，输入问题：请介绍一下dify工作流。可以看到最终输出了Dify工作流的正确介绍。测试正常后，我们返回编辑模式。


<figure><img src="../../.gitbook/assets/dify-on-wechat/create-workflow-chatbot-6.jpg" alt=""><figcaption></figcaption></figure>
返回编辑模式后，依次点击发布、更新、访问API



#### 2.3.3. 生成工作流编排聊天助手API密钥

在跳转到API管理页面后，我们参照**2.1.1小节（4）**获取"知识库+聊天机器人"应用的**API密钥**与**API服务器地址**

#### 2.3.4. 接入微信

与**2.1.2小节（3）**类似，我们在项目根目录创建名为config.json的文件，文件内容如下，同样把**dify_api_base**配置为**"知识库+聊天机器人"应用**的API服务器地址；**dify_api_key**配置为**"知识库+聊天机器人"应用**的API密钥**。**其他配置保持不变

```bash
{ 
  "dify_api_base": "https://api.dify.ai/v1",
  "dify_api_key": "app-xxx",
  "dify_app_type": "chatbot",
  "channel_type": "wx",
  "model": "dify",
  "single_chat_prefix": [""],
  "single_chat_reply_prefix": "",
  "group_chat_prefix": ["@bot"],
  "group_name_white_list": ["ALL_GROUP"]
}
```

我们按照**2.2.1小节**启动程序并扫码登录，然后给微信机器人发送消息，进行测试
<figure><img src="../../.gitbook/assets/dify-on-wechat/workflow-chatbot-on-wechat.jpg" alt=""><figcaption></figcaption></figure>

微信机器人的回复与在Dify测试页面上的回复一致。恭喜你更进一步，把工作流编排应用接入了个人微信，你可以向知识库中导入更多的Dify官方文档，让微信机器人为你解答更多的Dify相关问题。

### 2.4. 把Agent接入微信

#### 2.4.1. 创建Agent应用

<figure><img src="../../.gitbook/assets/dify-on-wechat/create-agent.jpg" alt=""><figcaption></figcaption></figure>

进入工作室页面，点击创建空白应用，选择Agent，设置图标和应用名称，最后点击创建

<figure><img src="../../.gitbook/assets/dify-on-wechat/config-agent-auth-dalle.jpg" alt=""><figcaption></figcaption></figure>

创建成功后，我们会进入Agent应用配置页面，在这个页面我们选择好对话模型，然后添加工具。我们首先添加DALL-E绘画工具，首次使用该工具需要授权，一般我们设置好OpenAI API key和OpenAI base URL即可使用该DALL-E绘画工具。

<figure><img src="../../.gitbook/assets/dify-on-wechat/config-agent-add-dalle.jpg" alt=""><figcaption></figcaption></figure>

授权成功后，我们添加DALL-E 3绘画工具

<figure><img src="../../.gitbook/assets/dify-on-wechat/config-agent-add-duck-calc.jpg" alt=""><figcaption></figcaption></figure>

接着，继续添加DuckDuckGo搜索引擎和数学工具，进行后续的工具测试

<figure><img src="../../.gitbook/assets/dify-on-wechat/publish-agent.jpg" alt=""><figcaption></figcaption></figure>

我们输入问题"搜索开源项目Dify的star数量，这个数量乘以3.14是多少"，确认应用能够正常调用工具，我们依次点击发布、更新、访问API

#### 2.4.2. 生成Agent API密钥

我们继续参照**2.1.1小节（4）**获取"**智能助手**"应用的**API密钥**与**API服务器地址**

#### 2.4.3. 接入微信

我们在项目根目录创建名为config.json的文件，文件内容如下，同样把**dify_api_base**配置为**"智能助手"**应用的API服务器地址；**dify_api_key**配置为**"智能助手"**应用的API密钥**，**注意该应用为**智能助手**类型应用，还需要把**dify_app_type**设置为**agent**，其他配置保持不变

```bash
  {
    "dify_api_base": "https://api.dify.ai/v1",
    "dify_api_key": "app-xxx",
    "dify_app_type": "agent",
    "channel_type": "wx",
    "model": "dify",
    "single_chat_prefix": [""],
    "single_chat_reply_prefix": "",
    "group_chat_prefix": ["@bot"],
    "group_name_white_list": ["ALL_GROUP"]
 }

```

继续参照**2.2.1小节**启动程序并扫码登录，然后给微信机器人发送消息，进行测试
<figure><img src="../../.gitbook/assets/dify-on-wechat/agent-on-wechat.jpg" alt=""><figcaption></figcaption></figure>

可以看到微信机器人可以正常使用搜索和绘画工具。再一次恭喜你，把Dify Agent应用接入微信。也恭喜我，写到这里可以先睡觉了。

### 2.5. 把工作流接入微信

#### 2.5.1. 创建工作流应用

待更新~

#### 2.5.2. 接入微信

待更新~

## 3. Dify接入公众号

待更新~

## 4. Dify接入企业微信应用

待更新~

## 5. Dify接入微信其他渠道

Dify on WeChat项目后续会逐步支持Dify接入微信的其他渠道，包括企业微信客服、企业微信个人号。



## 6. 后记

我是社畜打工人，精力实在有限，只能晚上下班还有周末空闲时间维护[Dify on WeChat](https://github.com/hanfangyuan4396/dify-on-wechat)项目，单靠我个人开发项目进度十分缓慢，希望大家能一起参与进来这个项目，多多提PR，让Dify的生态变得更好~

