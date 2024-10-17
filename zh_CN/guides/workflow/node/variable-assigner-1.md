# 变量赋值

### 1 定义

变量赋值节点用于向可写入变量进行变量赋值。目前已支持的可写入变量为[会话变量](../key-concept.md#hui-hua-bian-liang)。

通过变量赋值节点可以将工作流内的变量赋值到会话变量中临时存储，并在后续对话中引用该变量值。

<figure><img src="../../../.gitbook/assets/image (8).png" alt="" width="375"><figcaption></figcaption></figure>

***

### 2 场景

将会话中的**上下文、上传的文件、用户偏好**等通过变量赋值写入到会话变量中，并在后续对话中引用已存储的信息导向不同的处理流程或者进行回复。

**场景 1** &#x20;

**用户偏好记录**，在会话内记住用户语言偏好并在后续对话中持续使用该语言类型进行回复。

<figure><img src="../../../.gitbook/assets/image (265).png" alt=""><figcaption></figcaption></figure>

**配置流程：**

**设置会话变量**：首先设置一个会话变量 `language`，在会话流程开始时添加一个条件判断节点，用来判断 `language` 变量的值是否为空。

**变量写入/赋值**：首轮对话开始时， `language` 变量值为空，则使用 LLM 节点来提取用户输入的语言，再通过变量赋值节点将该语言类型写入到会话变量 `language` 中。

**变量读取**：在后续的对话轮次内： `language` 变量已存储用户语言偏好，LLM 节点可以通过引用 language 变量，使用用户的偏好语言类型进行回复。

**场景 2**

**Checklist 打卡**，在会话内记住用户的 checklist 输入项并在后续对话中检查未完成项。

<figure><img src="../../../.gitbook/assets/image (266).png" alt=""><figcaption></figcaption></figure>

会话开始时 LLM 会要求用户检查 Checklist 是否都已填写。

<figure><img src="../../../.gitbook/assets/image (267).png" alt=""><figcaption></figcaption></figure>

会话过程中，根据用户已填写的信息，LLM 会每轮检查未填写的 Checklist，并提醒用户继续填写。\


<figure><img src="../../../.gitbook/assets/image (268).png" alt=""><figcaption></figcaption></figure>

**配置流程：**

* **设置会话变量：**首先设置一个会话变量 `ai_checklist`,在 LLM 内引用该变量作为上下文进行检查。
* **变量赋值/写入**：每一轮对话时，在 LLM 节点内检查 `ai_checklist` 内的值并比对用户输入，若用户提供了新的信息，则更新 Checklist 并将输出内容通过变量赋值节点写入到 `ai_checklist` 内。
* **变量读取：**每一轮对话读取 `ai_cheklist` 内的值并比对用户输入直至所有 checklist 完成。

***

### 3 如何操作

<figure><img src="../../../.gitbook/assets/image (7).png" alt="" width="375"><figcaption></figcaption></figure>

**设置变量：**

Assigned Variable 指定变量：选择被赋值变量

Set Variable 设置变量：选择需要赋值的变量

以上图为例，赋值逻辑：将 `Language Recognition/text`  变量的值赋值到 `language` 变量中。

**写入模式：**

* Overwrite 写入
* Append 追加，指定变量为 Array 类型时
* Clear 清除

