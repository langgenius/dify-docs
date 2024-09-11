# 变量

Workflow 和 Chatflow 类型应用由独立节点相构成。大部分节点设有输入和输出项，但每个节点的输入信息不一致，各个节点所输出的答复也不尽相同。

如何用一种固定的符号**指代动态变化的内容？** 变量作为一种动态数据容器，能够存储和传递不固定的内容，在不同的节点内被相互引用，实现信息在节点间的灵活通信。


### **系统变量**

系统变量指的是在 Chatflow / Workflow 应用内预设的系统级参数，可以被其它节点全局读取。系统级变量均以 `sys` 开头。

#### Workflow

Workflow 类型应用提供以下系统变量：

<table><thead><tr><th>变量名称</th><th>数据类型</th><th width="297">说明</th><th>备注</th></tr></thead><tbody><tr><td><code>sys.files</code></td><td> Array[File]</td><td>文件参数，存储用户初始使用应用时上传的图片</td><td>图片上传功能需在应用编排页右上角的 “功能” 处开启</td></tr><tr><td><code>sys.user_id</code></td><td>String</td><td>用户 ID，每个用户在使用工作流应用时，系统会自动向用户分配唯一标识符，用以区分不同的对话用户</td><td></td></tr></tbody></table>



<figure><img src="../../.gitbook/assets/image (2).png" alt="workflow-system-variable"><figcaption><p>Workflow 类型应用系统变量</p></figcaption></figure>

#### Chatflow

Chatflow 类型应用提供以下系统变量：

<table><thead><tr><th>变量名称</th><th>数据类型</th><th width="283">说明</th><th>备注</th></tr></thead><tbody><tr><td><code>sys.query</code></td><td> String</td><td>用户在对话框中初始输入的内容</td><td></td></tr><tr><td><code>sys.files</code></td><td> Array[File]</td><td>用户在对话框内上传的图片</td><td>图片上传功能需在应用编排页右上角的 “功能” 处开启</td></tr><tr><td><code>sys.dialogue_count</code></td><td>Number</td><td><p>用户在与 Chatflow 类型应用交互时的对话轮数。每轮对话后自动计数增加 1，可以和 if-else 节点搭配出丰富的分支逻辑。</p><p></p><p>例如到第 X 轮对话时，回顾历史对话并给出分析</p></td><td></td></tr><tr><td><code>sys.conversation_id</code></td><td>String</td><td>对话框交互会话的唯一标识符，将所有相关的消息分组到同一个对话中，确保 LLM 针对同一个主题和上下文持续对话</td><td></td></tr><tr><td><code>sys.user_id</code></td><td>String</td><td>分配给每个应用用户的唯一标识符，用以区分不同的对话用户</td><td></td></tr></tbody></table>



<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption><p>Chatflow 类型应用系统变量</p></figcaption></figure>

### 环境变量

**环境变量用于保护工作流内所涉及的敏感信息**，例如运行工作流时所涉及的 API 密钥、数据库密码等。它们被存储在工作流程中，而不是代码中，以便在不同环境中共享。

<figure><img src="../../.gitbook/assets/环境变量.jpeg" alt=""><figcaption><p>环境变量</p></figcaption></figure>

支持以下三种数据类型：

* String 字符串
* Number 数字
* Secret 密钥

环境变量拥有以下特性：

* 环境变量可在大部分节点内全局引用；
* 环境变量命名不可重复；
* 环境变量为只读变量，不可写入；

### 会话变量

> 会话变量面向多轮对话场景，而 Workflow 类型应用的交互是线性而独立的，不存在多次对话交互的情况，因此会话变量仅适用于 Chatflow 类型（聊天助手 → 工作流编排）应用。

**会话变量允许应用开发者在同一个 Chatflow 会话内，指定需要被临时存储的特定信息，并确保在当前工作流内的多轮对话内都能够引用该信息**，如上下文、上传至对话框的文件（即将上线）、 用户在对话过程中所输入的偏好信息等。好比为 LLM 提供一个可以被随时查看的“备忘录”，避免因 LLM 记忆出错而导致的信息偏差。

例如你可以将用户在首轮对话时输入的语言偏好存储至会话变量中，LLM 在回答时将参考会话变量中的信息，并在后续的对话中使用指定的语言回复用户。

<figure><img src="../../.gitbook/assets/会话变量.jpeg" alt=""><figcaption><p>会话变量</p></figcaption></figure>

**会话变量**支持以下六种数据类型：

* String 字符串
* Number 数值
* Object 对象
* Array\[string] 字符串数组
* Array\[number] 数值数组
* Array\[object] 对象数组

**会话变量**具有以下特性：

* 会话变量可在大部分节点内全局引用；
* 会话变量的写入需要使用[变量赋值](node/variable-assignment.md)节点；
* 会话变量为可读写变量；

关于如何将会话变量与变量赋值节点配合使用，请参考[变量赋值](node/variable-assignment.md)节点说明。



### 注意事项

* 为避免变量名重复，节点命名不可重复
* 节点的输出变量一般为固定变量，不可编辑
