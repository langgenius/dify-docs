# 集成 Langfuse

### 1 什么是 Langfuse

Langfuse 是一个开源的 LLM 工程平台，可以帮助团队协作调试、分析和迭代他们的应用程序。

{% hint style="info" %}
Langfuse 官网介绍：[https://langfuse.com/](https://langfuse.com/)
{% endhint %}

***

### 2 如何配置 Langfuse

1. 在[官网注册](https://langfuse.com/)并登录 Langfuse
2. 在 Langfuse 内创建项目，登录后在主页点击 **New** ，创建一个自己的项目，**项目**将用于与 Dify 内的**应用**关联进行数据监测。

<figure><img src="../../../.gitbook/assets/image (249).png" alt=""><figcaption><p>在 Langfuse 内创建项目</p></figcaption></figure>

为项目编辑一个名称。

<figure><img src="../../../.gitbook/assets/image (251).png" alt=""><figcaption><p>在 Langfuse 内创建项目</p></figcaption></figure>

3. 创建项目 API 凭据，在项目内左侧边栏中点击 **Settings** 打开设置

<figure><img src="../../../.gitbook/assets/image (253).png" alt=""><figcaption><p>创建一个项目 API 凭据</p></figcaption></figure>

在 Settings 内点击 **Create API Keys** 创建一个项目 API 凭据。

<figure><img src="../../../.gitbook/assets/image (252).png" alt=""><figcaption><p>创建一个项目 API 凭据</p></figcaption></figure>

复制并保存 **Secret Key** ，**Public Key，Host**

<figure><img src="../../../.gitbook/assets/image (254).png" alt=""><figcaption><p>获取 API Key 配置</p></figcaption></figure>

4\. 在 Dify 内配置 Langfuse，打开需要监测的应用，在侧边菜单打开**监测**，在页面中选择**配置。**

<figure><img src="../../../.gitbook/assets/image (255).png" alt=""><figcaption><p>配置 Langfuse</p></figcaption></figure>

点击配置后，将在 Langfuse 内创建的 **Secret Key, Public Key, Host** 粘贴到配置内并保存。

<figure><img src="../../../.gitbook/assets/image (256).png" alt=""><figcaption><p>配置 Langfuse</p></figcaption></figure>

成功保存后可以在当前页面查看到状态，显示已启动即正在监测。

<figure><img src="../../../.gitbook/assets/image (257).png" alt=""><figcaption><p>查看配置状态</p></figcaption></figure>

***

### 3 在 Langfuse 内查看监测数据

配置完成后， Dify 内应用的调试或生产数据可以在 Langfuse 查看监测数据。

<figure><img src="../../../.gitbook/assets/image (259).png" alt=""><figcaption><p>在 Dify 内调试应用</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (258).png" alt=""><figcaption><p>在 Langfuse 内查看应用数据</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image.png" alt=""><figcaption><p>在 Langfuse 内查看应用数据</p></figcaption></figure>
