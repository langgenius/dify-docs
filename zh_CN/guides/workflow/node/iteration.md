# 迭代

### 定义

对数组执行多次步骤直至输出所有结果。

迭代步骤在列表中的每个条目（item）上执行相同的步骤。使用迭代的条件是确保输入值已经格式化为列表对象。迭代节点允许 AI 工作流处理更复杂的处理逻辑，迭代节点是循环节点的友好版本，它在自定义程度上做出了一些妥协，以便非技术用户能够快速入门。

***

### 场景&#x20;

#### **示例1：长文章迭代生成器**

<figure><img src="../../../.gitbook/assets/image (207).png" alt=""><figcaption><p>长故事生成器</p></figcaption></figure>

1. 在 **开始节点** 内输入故事标题和大纲
2. 使用 **代码节点** 从用户输入中提取出完整内容
3. 使用 **参数提取节点** 将完整内容转换成数组格式
4. 通过 **迭代节点** 包裹的 **LLM 节点** 循环多次生成各章节内容
5. 将 **直接回复** 节点添加在迭代节点内部，实现在每轮迭代生成之后流式输出

**具体配置步骤**

1. 在 **开始节点** 配置故事标题（title）和大纲（outline）；

<figure><img src="../../../.gitbook/assets/image (211).png" alt="" width="375"><figcaption><p>开始节点配置</p></figcaption></figure>

1. 通过 **Jinja-2 模板节点** 将故事标题与大纲转换为完整文本；

<figure><img src="../../../.gitbook/assets/image (209).png" alt="" width="375"><figcaption><p>模板节点</p></figcaption></figure>

3. 通过 **参数提取节点**，将故事文本转换成为数组（Array）结构。提取参数为 `sections` ，参数类型为 `Array[Object]`

<figure><img src="../../../.gitbook/assets/image (210).png" alt="" width="375"><figcaption><p>参数提取</p></figcaption></figure>

{% hint style="info" %}
参数提取效果受模型推理能力和指令影响，使用推理能力更强的模型，在**指令**内增加示例可以提高参数提取的效果。
{% endhint %}

4. 将数组格式的故事大纲作为迭代节点的输入，在迭代节点内部使用 **LLM 节点** 进行处理

<figure><img src="../../../.gitbook/assets/image (220).png" alt="" width="375"><figcaption><p>配置迭代节点</p></figcaption></figure>

在 LLM 节点内配置输入变量 `GenerateOverallOutline/output` 和 `Iteration/item`

<figure><img src="../../../.gitbook/assets/image (221).png" alt="" width="375"><figcaption><p>配置 LLM 节点</p></figcaption></figure>

{% hint style="info" %}
迭代的内置变量：`items[object]` 和 `index[number]`

`items[object] 代表以每轮迭代的输入条目；`

`index[number] 代表当前迭代的轮次；`
{% endhint %}

5. 在迭代节点内部配置 **直接回复节点** ，可以实现在每轮迭代生成之后流式输出。

<figure><img src="../../../.gitbook/assets/image (223).png" alt="" width="375"><figcaption><p>配置 Answer 节点</p></figcaption></figure>

6. 完整调试和预览

<figure><img src="../../../.gitbook/assets/image (222).png" alt=""><figcaption><p>按故事章节多轮迭代生成</p></figcaption></figure>

#### **示例 2：长文章迭代生成器（另一种编排方式）**

<figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

* 在 **开始节点** 内输入故事标题和大纲
* 使用 **LLM 节点** 生成文章小标题，以及小标题对应的内容
* 使用 **代码节点** 将完整内容转换成数组格式
* 通过 **迭代节点** 包裹的 **LLM 节点** 循环多次生成各章节内容
* 使用 **模板转换** 节点将迭代节点输出的字符串数组转换为字符串
* 在最后添加 **直接回复节点** 将转换后的字符串直接输出

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

### 如何将数组转换为文本

迭代节点的输出变量为数组格式，无法直接输出。你可以使用一个简单的步骤将数组转换回文本。

**使用代码节点转换**

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt="" width="334"><figcaption><p>代码节点转换</p></figcaption></figure>

```python
def main(articleSections: list):
    data = articleSections
    return {
        "result": "\n".join(data)
    }
```

**使用模板节点转换**

<figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1).png" alt="" width="332"><figcaption><p>模板节点转换</p></figcaption></figure>

```django
{{ articleSections | join("\n") }}
```
