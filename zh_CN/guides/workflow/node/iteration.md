# 迭代

🚧 维护中

### 定义

对数组执行多次步骤直至输出所有结果。

迭代步骤在列表中的每个条目（item）上执行相同的步骤。使用迭代的条件是确保输入值已经格式化为列表对象。迭代节点允许 AI 工作流处理更复杂的处理逻辑，迭代节点是循环节点的友好版本，它在自定义程度上做出了一些妥协，以便非技术用户能够快速入门。

***

### 场景&#x20;

使用迭代节点可以实现更灵活的多步骤生成，充分发挥 Workflow 的能力。

例如首先让 LLM 根据用户提供主题和摘要生成故事章节提纲，然后将故事章节提纲作为数组输入，再使用 LLM 节点中进行多次迭代，直到生成完整故事内容。

<figure><img src="../../../.gitbook/assets/image (207).png" alt=""><figcaption><p>长故事生成器</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (222).png" alt=""><figcaption><p>按故事章节多轮迭代生成</p></figcaption></figure>

**配置步骤**

1. 在开始节点配置故事标题（title）和大纲（outline）；

<figure><img src="../../../.gitbook/assets/image (211).png" alt="" width="375"><figcaption><p>开始节点配置</p></figcaption></figure>

1. 通过 Jinja-2 模板节点将故事标题与大纲转换为完整文本；

<figure><img src="../../../.gitbook/assets/image (209).png" alt="" width="375"><figcaption><p>模板节点</p></figcaption></figure>

3. 通过参数提取节点，将故事文本转换成为数组（Array）结构。提取参数为 `sections` ，参数类型为 `Array[Object]`

<figure><img src="../../../.gitbook/assets/image (210).png" alt="" width="375"><figcaption><p>参数提取</p></figcaption></figure>

{% hint style="info" %}
参数提取效果受模型推理能力和指令影响，使用推理能力更强的模型，在**指令**内增加示例可以提高参数提取的效果。
{% endhint %}

4. 将数组格式的故事大纲作为迭代节点的输入，在 Iteration 内添加 LLM 节点处理

<figure><img src="../../../.gitbook/assets/image (220).png" alt="" width="375"><figcaption><p>配置迭代节点</p></figcaption></figure>

5. 在 LLM 节点内配置输入变量 `GenerateOverallOutline/output` 和 `Iteration/item`

<figure><img src="../../../.gitbook/assets/image (221).png" alt="" width="375"><figcaption><p>配置 LLM 节点</p></figcaption></figure>

{% hint style="info" %}
迭代的内置变量：`items[object]` 和 `index[number]`

`items[object] 代表以每轮迭代的输入条目；`

`index[number] 代表当前迭代的轮次；`
{% endhint %}

6. 在迭代节点内部配置 Answer ，可以实现迭代过程中的流式输出。

<figure><img src="../../../.gitbook/assets/image (223).png" alt="" width="375"><figcaption><p>配置 Answer 节点</p></figcaption></figure>

### 什么是数组内容

列表是一种特定的数据类型，其中的元素用逗号分隔，以 `[` 开头，以 `]` 结尾。例如：

**数字型：**

```
[0,1,2,3,4,5]
```

**字符串型：**

```
["monday", "Tuesday", "Wednesday", "Thursday"]
```

**JSON 对象：**

```
[
    {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    },
    {
        "name": "Bob",
        "age": 25,
        "email": "bob@example.com"
    },
    {
        "name": "Charlie",
        "age": 35,
        "email": "charlie@example.com"
    }
]
```

***

### 支持返回数组的节点

* 代码节点
* 参数提取
* 知识库检索
* 迭代
* 工具
* HTTP 请求

### 如何获取数组格式的内容

**使用 CODE 节点返回**

<figure><img src="../../../.gitbook/assets/image (213).png" alt="" width="375"><figcaption><p>code 节点输出 array</p></figcaption></figure>

**使用 参数提取 节点返回**

<figure><img src="../../../.gitbook/assets/image (214).png" alt="" width="375"><figcaption><p>参数提取节点输出 array</p></figcaption></figure>

**使用 知识检索 节点返回**

<figure><img src="../../../.gitbook/assets/image (218).png" alt="" width="375"><figcaption><p>知识检索节点输出 array</p></figcaption></figure>

