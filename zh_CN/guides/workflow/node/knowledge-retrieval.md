# 知识检索

### 1 定义

从知识库中检索与用户问题相关的文本内容，可作为下游 LLM 节点的上下文来使用。

***

### 2 场景

常见情景：构建基于外部数据/知识的 AI 问答系统（RAG）。了解更多关于 RAG 的[基本概念](../../../learn-more/extended-reading/retrieval-augment/)。

下图为一个最基础的知识库问答应用示例，该流程的执行逻辑为：知识库检索作为 LLM 节点的前置步骤，在用户问题传递至 LLM 节点之前，先在知识检索节点内将匹配用户问题最相关的文本内容并召回，随后在 LLM 节点内将用户问题与检索到的上下文一同作为输入，让 LLM 根据检索内容来回复问题。

<figure><img src="../../../.gitbook/assets/image (193).png" alt=""><figcaption><p>知识库问答应用示例</p></figcaption></figure>

***

### 3 如何配置

<figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>知识检索配置</p></figcaption></figure>

**配置流程：**

1. 选择查询变量，用于作为输入来检索知识库中的相关文本分段，在常见的对话类应用中一般将开始节点的 `sys.query` 作为查询变量；
2. 选择需要查询的知识库，可选知识库需要在 Dify 知识库内预先[创建](../../knowledge-base/create-knowledge-and-upload-documents/#id-1-chuang-jian-zhi-shi-ku)；
3. 指定[召回模式](../../../learn-more/extended-reading/retrieval-augment/retrieval.md)。自 9 月 1 日后，知识库的召回模式将自动切换为多路召回，不再建议使用 N 选 1 召回模式；
4. 连接并配置下游节点，一般为 LLM 节点；

> 建议将知识库的召回模式切换为多路召回，详细说明请参考[《在应用内集成知识库》](https://docs.dify.ai/v/zh-hans/guides/knowledge-base/integrate-knowledge-within-application)。

**输出变量**

<figure><img src="../../../.gitbook/assets/image (199).png" alt="" width="272"><figcaption><p>输出变量</p></figcaption></figure>

知识检索的输出变量 `result` 为从知识库中检索到的相关文本分段。其变量数据结构中包含了分段内容、标题、链接、图标、元数据信息。

**配置下游节点**

在常见的对话类应用中，知识库检索的下游节点一般为 LLM 节点，知识检索的**输出变量** `result` 需要配置在 LLM 节点中的 **上下文变量** 内关联赋值。关联后你可以在提示词的合适位置插入 **上下文变量**。

{% hint style="info" %}
上下文变量是 LLM 节点内定义的特殊变量类型，用于在提示词内插入外部检索的文本内容。
{% endhint %}

当用户提问时，若在知识检索中召回了相关文本，文本内容会作为上下文变量中的值填入提示词，提供 LLM 回复问题；若未在知识库检索中召回相关的文本，上下文变量值为空，LLM 则会直接回复用户问题。

<figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>配置下游 LLM 节点</p></figcaption></figure>

该变量除了可以作为 LLM 回复问题时的提示词上下文作为外部知识参考引用，另外由于其数据结构中包含了分段引用信息，同时可以支持应用端的 [**引用与归属**](../../knowledge-base/retrieval-test-and-citation.md#id-2-yin-yong-yu-gui-shu) 功能。
