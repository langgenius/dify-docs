# 手摸手教你把 Dify 接入微信生态

> 作者：韩方圆，"Dify on WeChat"开源项目作者

## 概述

微信作为最热门即时通信软件，拥有巨大的流量。
微信友好的聊天窗口是天然的AI应用LUI(Language User Interface)/CUI(Command User Interface)。
微信不仅有个人微信，同时提供了公众号、企业微信、企业微信应用、企业微信客服等对话渠道，拥有良好的微信生态。
把Dify应用接入微信生态，就能打造一个功能强大的智能客服，大大降低客服成本，同时也能够提升客户体验。本篇教程就是手摸手地教你如何利用[Dify on WeChat](https://github.com/hanfangyuan4396/dify-on-wechat)项目，把Dify应用接入微信生态。

## Dify接入个人微信

### 准备工作

#### 创建聊天助手

##### （1）Dify简介

Dify是一个优秀的LLMOps（大型语言模型运维）平台，Dify的详细介绍请移步官方文档[欢迎使用 Dify | 中文 | Dify](https://docs.dify.ai/v/zh-hans)。

##### （2）登录Dify官方应用平台

首先，登录[Dify官方应用平台](https://cloud.dify.ai/signin)，你可以选择使用Github登录或者使用Google登录。此外，你也可以参考Dify官方教程[Docker Compose 部署 | 中文 | Dify](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/docker-compose) 私有部署，Dify是开源项目，支持私有部署。
![login-large.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712758885446-bf6febc4-1b6f-4457-aa75-6522e4563dc1.jpeg#averageHue=%23fefefe&clientId=uf95630ca-a48c-4&from=paste&height=1064&id=uea4bac09&originHeight=1330&originWidth=2560&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=104054&status=done&style=none&taskId=ud36b0d40-e18d-4607-a731-4250a59065e&title=&width=2048)

##### （3）创建Dify基础编排聊天助手应用

![create-basic-chatbot.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712761219398-f06684c9-b12a-42bb-aee3-aaa56ed8cfb5.jpeg#averageHue=%23d6dadb&clientId=uf95630ca-a48c-4&from=paste&height=776&id=aI38l&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=125907&status=done&style=none&taskId=u26f83217-b32a-49e7-9937-725a9adee67&title=&width=1536)
登录成功后，进入Dify页面，我们按照下方步骤创建一个基础编排聊天助手应用

1. 点击页面上方的工作室
2. 创建空白应用
3. 应用类型选择聊天助手
4. 聊天助手编排方式选择基础编排
5. 选择应用图标并为应用填写一个名称，比如基础编排聊天助手
6. 点击创建

![config-basic-chatbot.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712761841353-0f4afa77-5808-49c5-9cab-d5582f520af7.jpeg#averageHue=%23f9faf6&clientId=uf95630ca-a48c-4&from=paste&height=776&id=u95ababd8&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=196784&status=done&style=none&taskId=u16141ed9-ecb6-49fc-8e56-957335a7853&title=&width=1536)
创建成功后我们会跳转到上图所示页面，我们继续配置应用

1. 选择模型，如gpt-3.5-turbo-0125
2. 设置模型参数
3. 填写应用提示词

![publish-basic-chatbot.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712762353322-5bdf7ae2-163c-4d9f-ab06-73ca86e8fc1e.jpeg#averageHue=%23e9efec&clientId=uf95630ca-a48c-4&from=paste&height=778&id=u7ed3dbc8&originHeight=972&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=164821&status=done&style=none&taskId=u715b03b2-4d6c-439c-a407-6e556fc8f61&title=&width=1536)
在配置完成后，我们可以在右侧对话框进行测试，在测试完成后，进行如下操作

1. 发布
2. 更新
3. 访问API

##### （4）生成基础编排聊天助手API密钥

![create-basic-chatbot-apikey.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712762697548-a43a6c97-47b6-4e33-acad-516460ea7f56.jpeg#averageHue=%23949393&clientId=uf95630ca-a48c-4&from=paste&height=776&id=u7c961748&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=136972&status=done&style=none&taskId=uefee6416-cdd8-4abe-9a83-4491d7dd097&title=&width=1536)
在点击"访问API"后，我们会跳转到上图的API管理页面，在这个页面我们按照如下步骤获取API密钥：

1. 点击右上角API密钥
2. 点击创建密钥
3. 复制保存密钥

在保存密钥后，还需要查看右上角的API服务器，如果是Dify官网的应用，API服务器地址为 "https://api.dify.ai/v1"，如果是私有部署的，请确认你自己的API服务器地址。

至此，创建聊天助手的准备工作结束，在此小节中我们只需要保存好两个东西：**API密钥**与**API服务器地址**

#### 下载Dify on WeChat项目

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

### 把基础编排聊天助手接入微信

#### 快速启动测试

##### （1）在Dify on Wechat项目根目录执行如下命令

```bash
cd dify-on-wechat
python3 app.py   # windows环境下该命令通常为 python app.py
```

##### （2）扫码登录

![wechat-login.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712766258919-a77331e7-751f-4a7f-ae5e-45f23ca12938.jpeg#averageHue=%23292827&clientId=u4e7645c6-dfe9-4&from=paste&height=994&id=ua902ff60&originHeight=1243&originWidth=2192&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=384128&status=done&style=none&taskId=ua5203795-7725-49f7-8a67-371a053bd0e&title=&width=1753.6)
本项目使用itchat实现个人微信登录，有封号风险，建议使用**实名认证**过的**微信小号**进行测试，在执行上述命令后，我们可以在控制台看到打印如上图所示二维码，使用微信扫码登录，登录后当看到"itchat:Start auto replying."字符，表示登录成功，我们可以进行测试。

##### （3）对话测试

![basic-chatbot-on-wechat.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712766396013-6d9719c7-6383-4919-9cee-52a4e48f520a.jpeg#averageHue=%23f1f1f1&clientId=u4e7645c6-dfe9-4&from=paste&height=574&id=ud0d16273&originHeight=717&originWidth=1094&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=84266&status=done&style=none&taskId=u586b389d-35da-40bb-9531-abb44bd018a&title=&width=875.2)
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

### 把工作流编排聊天助手接入微信

在把Dify基础的聊天助手应用接入微信后，我们接下来增加难度，尝试把工作流编排聊天助手应用接入微信，实现一个具有Dify平台知识的微信智能客服，为我们解答Dify工作流相关知识。

#### 创建知识库

##### （1）下载知识库文件

![download-dify-workflow-knowledge.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712767337929-aacef6c6-cab3-4a70-8fe8-5fe09a99a684.jpeg#averageHue=%23efefe7&clientId=u6ab45a82-9c40-4&from=paste&height=918&id=u4f9818b4&originHeight=1147&originWidth=2119&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=254485&status=done&style=none&taskId=ub9c3eaff-b9f3-4aad-af9c-4156a8e5414&title=&width=1695.2)
我们到[dify文档仓库](https://github.com/langgenius/dify-docs/blob/main/zh_CN/guides/workflow/introduce.md)下载Dify工作流介绍的文档。

##### （2）Dify中导入知识库

![create-knowledge-1.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712769071870-16bde701-a4b4-412e-a4e6-98b1cde08460.jpeg#averageHue=%23f1f2f5&clientId=u6ab45a82-9c40-4&from=paste&height=775&id=u7edb69df&originHeight=969&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=81099&status=done&style=none&taskId=u415544e0-487d-4260-b3b2-78464a9a88d&title=&width=1536)
进入知识库页面，创建知识库

![create-knowledge-2.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712769110297-81976cfc-949d-4ef7-a963-82cf87610c8b.jpeg#averageHue=%23fefefe&clientId=u6ab45a82-9c40-4&from=paste&height=774&id=uc70a0109&originHeight=967&originWidth=1912&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=110249&status=done&style=none&taskId=u527dd191-dd4c-43dd-b00d-5e16a24bef7&title=&width=1529.6)
选择导入已有文本，上传刚才下载的introduce.md文件，点击下一步

![create-knowledge-3.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712769144948-ec2d8cf9-ebc9-4745-8551-1caa12b9e4cb.jpeg#averageHue=%23fcfdfa&clientId=u6ab45a82-9c40-4&from=paste&height=773&id=u9d1e3eb5&originHeight=966&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=241881&status=done&style=none&taskId=uf411f81f-bf3b-4807-b670-a83a4e7240c&title=&width=1536)
![create-knowledge-4.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712769172956-d957071d-d4a8-4885-a7b5-34f683b06578.jpeg#averageHue=%23fdfdf8&clientId=u6ab45a82-9c40-4&from=paste&height=770&id=ua5fa4c8b&originHeight=962&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=226038&status=done&style=none&taskId=u2a42baba-7931-47bd-b0f1-0d78ede3a19&title=&width=1536)
选择如下配置

- 分段设置：自动分段与清洗
- 索引方式：高质量
- 检索设置：向量检索

最后点击保存并处理

![create-knowledge-5.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712769273663-e9440c75-d4aa-438f-b3be-2841bf57719c.jpeg#averageHue=%23fefefe&clientId=u6ab45a82-9c40-4&from=paste&height=774&id=u15fd251c&originHeight=967&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=124976&status=done&style=none&taskId=ub53031c6-3a80-4562-b527-c96c3dba455&title=&width=1536)
我们看到知识库正在进行嵌入处理，稍等片刻，即可嵌入成功。

#### 创建工作流编排聊天助手

![create-workflow-chatbot-1.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770231555-a58a5e7f-0e9f-40ac-8413-55650d0ecdd0.jpeg#averageHue=%23f1f2f4&clientId=u28af65e0-3c03-4&from=paste&height=774&id=u4a976665&originHeight=967&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=79038&status=done&style=none&taskId=ud46687d5-0cf0-47a4-8c07-bae9e7a7087&title=&width=1536)
我们进入Dify工作室，点击从应用模板创建



![create-workflow-chatbot-2.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770241473-9575955c-def4-4e85-877d-f9c23b8fadef.jpeg#averageHue=%23c4c8bf&clientId=u28af65e0-3c03-4&from=paste&height=776&id=uec264a7e&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=205288&status=done&style=none&taskId=u041cda82-c484-4d55-8b6a-3381f2e5bab&title=&width=1536)

我们使用知识库+聊天机器人类型的模板，设置应用图标与名称，点击创建



![create-workflow-chatbot-3.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770241827-0a50e5cb-67c8-4a14-a0f7-04db9264d6e4.jpeg#averageHue=%23bac2c0&clientId=u28af65e0-3c03-4&from=paste&height=776&id=wWhFF&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=172349&status=done&style=none&taskId=u26d05c29-f941-4285-9693-a0e7c929f76&title=&width=1536)
跳转到工作流编排页面后，先点击知识检索节点，点击最右侧"+"添加知识库。我们选择之前上传好的introduce.md知识库，该知识库是对Dify工作流的基本介绍。最后我们点击添加，知识库节点设置完成。



![create-workflow-chatbot-4.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770241952-56313be0-1484-498d-90de-ec60b687f957.jpeg#averageHue=%23eff1f5&clientId=u28af65e0-3c03-4&from=paste&height=768&id=udea7f90e&originHeight=960&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=183176&status=done&style=none&taskId=ua17fe6e6-b587-45c1-a242-8c258708ebf&title=&width=1536)
接下来选择LLM节点，点击设置上下文，我们选择result变量，该变量存有知识检索的结果。



![create-workflow-chatbot-5.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770241698-c1988a71-e00a-4870-ac6e-a562c0722172.jpeg#averageHue=%23eef0f5&clientId=u28af65e0-3c03-4&from=paste&height=746&id=rUXp6&originHeight=932&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=240156&status=done&style=none&taskId=ucf437be8-3d10-4d08-802e-a6b975ff492&title=&width=1536)
设置完LLM节点后，我们点击预览进行测试，输入问题：请介绍一下dify工作流。可以看到最终输出了Dify工作流的正确介绍。测试正常后，我们返回编辑模式。



![create-workflow-chatbot-6.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712770241415-2cea5f44-dedd-412f-a019-54f03445e8e6.jpeg#averageHue=%23eef0f6&clientId=u28af65e0-3c03-4&from=paste&height=774&id=u77b826cb&originHeight=968&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=165595&status=done&style=none&taskId=u7cd73d69-5595-4f81-b29a-a71cd3dfa56&title=&width=1536)
返回编辑模式后，依次点击发布、更新、访问API



#### 生成工作流编排聊天助手API密钥

在跳转到API管理页面后，我们参照**2.1.1小节（4）**获取"知识库+聊天机器人"应用的**API密钥**与**API服务器地址**

#### 接入微信

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
![workflow-chatbot-on-wechat.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712772240211-9799fe11-1954-4daa-a060-00d04e82c28f.jpeg#averageHue=%23eeeeee&clientId=u27d09495-7554-4&from=paste&height=641&id=u64b29ad3&originHeight=801&originWidth=1094&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=151907&status=done&style=none&taskId=u84344bd4-9654-42ef-89fd-09d3b03e822&title=&width=875.2)
微信机器人的回复与在Dify测试页面上的回复一致。恭喜你更进一步，把工作流编排应用接入了个人微信，你可以向知识库中导入更多的Dify官方文档，让微信机器人为你解答更多的Dify相关问题。

### 把Agent接入微信

#### 创建Agent应用

![create-agent.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712774615693-49b4c6c2-0741-4765-b350-92989583f87f.jpeg#averageHue=%23babcbf&clientId=u26a77d49-1b6e-4&from=paste&height=776&id=ua274142d&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=130511&status=done&style=none&taskId=u06dc5419-a3ec-4812-bc6f-f5405a2af7e&title=&width=1536)
进入工作室页面，点击创建空白应用，选择Agent，设置图标和应用名称，最后点击创建

![config-agent-auth-dalle.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712774713928-e61310e6-249b-4df9-ad68-69b415f119fd.jpeg#averageHue=%237e817f&clientId=u26a77d49-1b6e-4&from=paste&height=776&id=u6b9895fb&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=149885&status=done&style=none&taskId=ue2f3a821-57c2-41e6-9e5c-b17054e8ca3&title=&width=1536)
创建成功后，我们会进入Agent应用配置页面，在这个页面我们选择好对话模型，然后添加工具。我们首先添加DALL-E绘画工具，首次使用该工具需要授权，一般我们设置好OpenAI API key和OpenAI base URL即可使用该DALL-E绘画工具。

![config-agent-add-dalle.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712774946301-b9237b9b-38dc-4880-98c2-be4d308ce96d.jpeg#averageHue=%23c0c6ba&clientId=u26a77d49-1b6e-4&from=paste&height=776&id=ue42d8170&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=147540&status=done&style=none&taskId=uf6c61969-6736-4522-ad47-de2599dfd89&title=&width=1536)
授权成功后，我们添加DALL-E 3绘画工具

![config-agent-add-duck-calc.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712774998427-5485d91c-0e59-4947-9598-41ab5f092c64.jpeg#averageHue=%23bec1ba&clientId=u26a77d49-1b6e-4&from=paste&height=776&id=u74d514db&originHeight=970&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=159870&status=done&style=none&taskId=ua1737750-18f9-40da-bacd-c23987e7c6e&title=&width=1536)
接着，继续添加DuckDuckGo搜索引擎和数学工具，进行后续的工具测试

![publish-agent.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712775059570-2ca6e2b3-8d6a-4d5a-aa43-8625ee295447.jpeg#averageHue=%23e4eee9&clientId=u26a77d49-1b6e-4&from=paste&height=778&id=ub8a96eea&originHeight=972&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=194929&status=done&style=none&taskId=ue0501d85-7b32-4244-a86b-b490951b342&title=&width=1536)
我们输入问题"搜索开源项目Dify的star数量，这个数量乘以3.14是多少"，确认应用能够正常调用工具，我们依次点击发布、更新、访问API

#### 生成Agent API密钥

我们继续参照**2.1.1小节（4）**获取"**智能助手**"应用的**API密钥**与**API服务器地址**

#### 接入微信

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
![agent-on-wechat.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/35902554/1712775663572-67fa55c1-6522-433b-a7fe-850b7313ff8e.jpeg#averageHue=%23efeeed&clientId=u26a77d49-1b6e-4&from=paste&height=571&id=u5340a051&originHeight=714&originWidth=1058&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=101027&status=done&style=none&taskId=u69296ac9-b97a-4be5-ab21-a92a32ce35f&title=&width=846.4)
可以看到微信机器人可以正常使用搜索和绘画工具。再一次恭喜你，把Dify Agent应用接入微信。也恭喜我，写到这里可以先睡觉了。

### 把工作流接入微信

#### 创建工作流应用

待更新~

#### 接入微信

待更新~

## Dify接入公众号

待更新~

## Dify接入企业微信应用

待更新~

## Dify接入微信其他渠道

Dify on WeChat项目后续会逐步支持Dify接入微信的其他渠道，包括企业微信客服、企业微信个人号。
另外，我是社畜打工人，精力实在有限，只能晚上下班还有周末空闲时间维护这个项目，单靠我个人开发项目进度十分缓慢，希望大家能一起参与进来这个项目，多多提PR，让Dify的生态变得更好~

