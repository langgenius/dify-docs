# 在应用内集成知识库

### 1 创建知识库应用

知识库可以作为外部知识提供给大语言模型用于精确回复用户问题，你可以在 Dify 的[所有应用类型](../application-design/#application\_type)内关联已创建的知识库。

以聊天助手为例，使用流程如下：

1. 进入 **工作室 -- 创建应用 --创建聊天助手**
2. 进入 **上下文设置** 点击 **添加** 选择已创建的知识库
3. 在 **上下文设置 -- 参数设置** 内配置**召回策略**
4. 在 **添加功能** 内打开 **引用和归属**&#x20;
5. 在 **调试与预览** 内输入与知识库相关的用户问题进行调试
6. 调试完成之后**保存并发布**为一个 AI 知识库问答类应用

<figure><img src="../../.gitbook/assets/image (187).png" alt=""><figcaption><p>在应用内关联知识库</p></figcaption></figure>

***

### 2 召回模式

进入 **上下文 -- 参数设置 -- 召回设置**，可以选择知识库的召回模式。

**N 选 1 召回**，根据用户意图和知识库描述，由 LLM 自主判断选择最匹配的单个知识库来查询相关文本。

**多路召回**，根据用户意图同时匹配所有知识库，从多路知识库查询相关文本片段，经过重排序步骤，从多路查询结果中选择匹配用户问题的最佳结果，需配置 Rerank 模型 API。

<figure><img src="../../.gitbook/assets/image (189).png" alt=""><figcaption></figcaption></figure>

**如何选择召回模式**

N 选 1 召回由  Function Call/ReAct 进行驱动，每一个关联的知识库作为工具函数，LLM 会自主选择与用户问题最匹配的 1 个知识库来进行查询，**推理依据为用户问题与知识库描述的语义匹配性**。

因此 N 选 1 模式的召回效果主要受三个因素影响：

* **系统推理模型的能力，**部分模型对于 Function Call/ReAct 的指令遵循程度不稳定
* **知识库描述是否清晰**，描述内容会影响 LLM 对用户问题与相关知识库的推理
* **知识库的个数**，知识库过多会影响 LLM 的推理精确性，同时可能会超出推理模型的上下文窗口长度。

**N 选 1 模式的推荐配置方法：**选择效果更好的系统推理模型，关联尽量少的知识库，提供精确的知识库描述。

用户上传知识库时，系统推理模型将自动为知识库生成一个摘要描述。为了在该模式下获得最佳的召回效果，你可以在“知识库->设置->知识库描述”中查看到系统默认创建的摘要描述，并检查该内容是否可以清晰的概括知识库的内容。

以下是 N 选 1 召回模式的技术流程图：

<figure><img src="../../.gitbook/assets/image (190).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
N 选 1 召回依赖模型的推理能力，使用限制较多，计划在 2024 Q3 调整该模式的召回策略。
{% endhint %}

#### 多路召回模式（推荐） <a href="#duo-lu-zhao-hui-mo-shi" id="duo-lu-zhao-hui-mo-shi"></a>

在多路召回模式下，检索器会在所有与应用关联的知识库中去检索与用户问题相关的文本内容，并将多路召回的相关文档结果合并，并通过后置的重排序（Rerank）步骤对检索召回的文档进行语义重排。

以下是多路召回模式的技术流程图：

<figure><img src="https://docs.dify.ai/~gitbook/image?url=https%3A%2F%2F1288284732-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FCdDIVDY6AtAz028MFT4d%252Fuploads%252Fgit-blob-9bb237ea9a2b4cc09637e951e696d5b52eb31033%252Fimage.png%3Falt%3Dmedia&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=0790e257848b5e6c45ce226109aa1c2f5d54bae1c04d1e14dec9fa6a46bdee17" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
多路召回模式下需要配置 Rerank 模型。
{% endhint %}

多路召回模式不依赖于模型的推理能力或知识库描述，该模式在多知识库检索时能够获得质量更高的召回效果，因此更**推荐将召回模式设置为多路召回**。

***

### 3 重排序（Rerank）

重排序模型通过将候选文档列表与用户问题语义匹配度进行重新排序，从而改进语义排序的结果。其原理是计算用户问题与给定的每个候选文档之间的相关性分数，并返回按相关性从高到低排序的文档列表。

<figure><img src="../../.gitbook/assets/image (128).png" alt=""><figcaption><p>混合检索+重排序</p></figcaption></figure>

{% hint style="info" %}
想了解更多关于 Rerank 的相关知识，请查阅扩展阅读[重排序](integrate\_knowledge\_within\_application.md#zhong-pai-xu-rerank)。
{% endhint %}

#### 如何配置 Rerank 模型？

Dify 目前已支持 Cohere Rerank 模型，通过进入“模型供应商-> Cohere”页面填入 Rerank 模型的 API 秘钥：

<figure><img src="../../.gitbook/assets/image (112).png" alt=""><figcaption><p>在模型供应商内配置 Cohere Rerank 模型</p></figcaption></figure>

如何获取 Cohere Rerank 模型？

登录：[https://cohere.com/rerank](https://cohere.com/rerank)，在页内注册并申请 Rerank 模型的使用资格，获取 API 秘钥。

{% hint style="info" %}
除了支持 Cohere Rerank API ，你也可以在使用本地推理框架如 Ollama、Xinference，并在推理框架内部署本地 Rerank 模型例如： bge-reranker。
{% endhint %}

#### 设置 Rerank 模型

通过进入“数据集->创建数据集->检索设置”页面并在添加 Rerank 设置。除了在创建数据集可以设置 Rerank ，你也可以在已创建的数据集设置内更改 Rerank 配置，在应用编排的数据集召回模式设置中更改 Rerank 配置。

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt="" width="563"><figcaption><p>数据集检索模式中设置 Rerank 模型</p></figcaption></figure>

**TopK**：用于设置 Rerank 后返回相关文档的数量。

**Score 阈值**：用于设置 Rerank 后返回相关文档的最低分值。设置 Rerank 模型后，TopK 和 Score 阈值设置仅在 Rerank 步骤生效。

通过进入“提示词编排->上下文->设置”页面中设置为多路召回模式时需开启 Rerank 模型。

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>数据集多路召回模式中设置 Rerank 模型</p></figcaption></figure>
