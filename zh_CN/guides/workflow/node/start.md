# 开始

### 定义

为启动工作流设置初始参数。

在开始节点中，您可以自定义启动工作流的输入变量。每个工作流都需要一个开始节点。

<figure><img src="../../../.gitbook/assets/image (236) (1).png" alt="" width="375"><figcaption><p>工作流开始节点</p></figcaption></figure>

开始节点支持定义四种类型输入变量：

* 文本
* 段落
* 下拉选项
* 数字
* 文件（即将推出）

<figure><img src="../../../.gitbook/assets/output (2) (1) (1).png" alt=""><figcaption><p>配置开始节点的变量</p></figcaption></figure>

配置完成后，工作流在执行时将提示您提供开始节点中定义的变量值。

<figure><img src="../../../.gitbook/assets/output (3) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Tip: 在Chatflow中，开始节点提供了内置系统变量：`sys.query` 和 `sys.files`。

`sys.query` 用于对话应用中的用户输入问题。

`sys.files` 用于对话中的文件上传，如上传图片，这需要与图片理解模型配合使用。
{% endhint %}
