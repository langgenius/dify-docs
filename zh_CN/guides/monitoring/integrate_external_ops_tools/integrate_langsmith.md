# 集成 LangSmith

### 1 什么是 LangSmith

LangSmith 是一个用于构建生产级 LLM 应用程序的平台，它用于开发、协作、测试、部署和监控 LLM 应用程序。

{% hint style="info" %}
LangSmith 官网介绍：[https://www.langchain.com/langsmith](https://www.langchain.com/langsmith)
{% endhint %}

***

### 2 如何配置 LangSmith

1. 在[官网注册](https://www.langchain.com/langsmith)并登录 LangSmith
2. 在 LangSmith 内创建项目，登录后在主页点击 **New Project** 创建一个自己的项目，**项目**将用于与 Dify 内的**应用**关联进行数据监测。

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption><p>在 LangSmith 内创建项目</p></figcaption></figure>

创建完成之后在 Projects 内可以查看到所有已创建的项目。

<figure><img src="../../../.gitbook/assets/image (7).png" alt=""><figcaption><p>在 LangSmith 内查看已创建项目</p></figcaption></figure>

3. 创建项目凭据，在左侧边栏内找到项目设置 **Settings**。

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>项目设置</p></figcaption></figure>

点击 **Create API Key**，创建一个项目凭据。

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>创建一个项目 API Key</p></figcaption></figure>

选择 **Personal Access Token** ，用于后续的 API 身份校验。

<figure><img src="../../../.gitbook/assets/image (5).png" alt=""><figcaption><p>创建一个 API Key</p></figcaption></figure>

将创建的 API key 复制保存。

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption><p>复制 API Key</p></figcaption></figure>

4. 在 Dify 应用内配置 LangSmith，打开需要监测的应用，在侧边菜单打开**监测**，在页面中选择**配置。**

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption><p>配置 LangSmith</p></figcaption></figure>



点击配置后，将在 LangSmith 内创建的 **API Key** 和**项目名**粘贴到配置内并保存。

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption><p>配置 LangSmith</p></figcaption></figure>

{% hint style="info" %}
配置项目名需要与 LangSmith 内设置的项目一致，若项目名不一致，数据同步时 LangSmith 会自动创建一个新的项目。
{% endhint %}

成功保存后可以在当前页面查看监测状态。

<figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption><p>查看配置状态</p></figcaption></figure>

### 3 在 LangSmith 内查看监测数据

配置完成后， Dify 内应用的调试或生产数据可以在 LangSmith 查看监测数据。

<figure><img src="../../../.gitbook/assets/image (17).png" alt=""><figcaption><p>在 Dify 内调试应用</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption><p>在 LangSmith 内查看应用数据</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption><p>在 LangSmith 内查看应用数据</p></figcaption></figure>

