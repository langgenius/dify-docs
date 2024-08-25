# 知识库及文档维护

### 1 查看文本分段

知识库内已上传的每个文档都会以文本分段（Chunks）的形式进行存储，你可以在分段列表内查看每一个分段的具体文本内容。

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>查看已上传的文档分段</p></figcaption></figure>

***

### 2 检查分段质量

文档分段对于知识库应用的问答效果有明显影响，在将知识库与应用关联之前，建议人工检查分段质量。

通过字符长度、标识符或者 NLP 语义分段等机器自动化的分段方式虽然能够显著减少大规模文本分段的工作量，但分段质量与不同文档格式的文本结构、前后文的语义联系都有关系，通过人工检查和订正可以有效弥补机器分段在语义识别方面的缺点。

检查分段质量时，一般需要关注以下几种情况：

* **过短的文本分段**，导致语义缺失；

<figure><img src="../../.gitbook/assets/image (183).png" alt="" width="373"><figcaption><p>过短的文本分段</p></figcaption></figure>

* **过长的文本分段**，导致语义噪音影响匹配准确性；

<figure><img src="../../.gitbook/assets/image (186).png" alt="" width="375"><figcaption><p>过长的文本分段</p></figcaption></figure>

* **明显的语义截断**，在使用最大分段长度限制时会出现强制性的语义截断，导致召回时缺失内容；

<figure><img src="../../.gitbook/assets/image (185).png" alt="" width="357"><figcaption><p>明显的语义截断</p></figcaption></figure>

***

### 3 添加文本分段

在分段列表内点击 「 添加分段 」 ，可以在文档内自行添加一个或批量添加多个自定义分段。

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

批量添加分段时，你需要先下载 CSV 格式的分段上传模板，并按照模板格式在 Excel 内编辑所有的分段内容，再将 CSV 文件保存后上传。

<figure><img src="../../.gitbook/assets/image (4) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>批量添加自定义分段</p></figcaption></figure>

***

### 4 编辑文本分段

在分段列表内，你可以对已添加的分段内容直接进行编辑修改。包括分段的文本内容和关键词。

<figure><img src="../../.gitbook/assets/image (5) (1) (1) (1) (1).png" alt=""><figcaption><p>编辑文档分段</p></figcaption></figure>

***

### 5 元数据管理

除了用于标记不同来源文档的元数据信息，例如网页数据的标题、网址、关键词、描述等。元数据将被用于知识库的分段召回过程中，作为结构化字段参与召回过滤或者显示引用来源。

{% hint style="info" %}
元数据过滤及引用来源功能当前版本尚未支持。
{% endhint %}

<figure><img src="../../.gitbook/assets/image (179).png" alt=""><figcaption><p>元数据管理</p></figcaption></figure>

***

### 6 添加文档

在「 知识库 > 文档列表 」 点击 「 添加文件 」，可以在已创建的知识库内上传新的文档或者 [Notion 页面](sync-from-notion.md)。

知识库（Knowledge）是一些文档（Documents）的集合。文档可以由开发者或运营人员上传，或由其它数据源同步（通常对应数据源中的一个文件单位）。

<figure><img src="../../.gitbook/assets/image (181).png" alt=""><figcaption><p>知识库上传新文档</p></figcaption></figure>

***

### 7 文档禁用和归档

**禁用**：数据集支持将暂时不想被索引的文档或分段进行禁用，在数据集文档列表，点击禁用按钮，则文档被禁用；也可以在文档详情，点击禁用按钮，禁用整个文档或某个分段，禁用的文档将不会被索引。禁用的文档点击启用，可以取消禁用。

**归档**：一些不再使用的旧文档数据，如果不想删除可以将它进行归档，归档后的数据就只能查看或删除，不可以进行编辑。在数据集文档列表，点击归档按钮，则文档被归档，也可以在文档详情，归档文档。归档的文档将不会被索引。归档的文档也可以点击撤销归档。

***

### 8 知识库设置

在知识库的左侧导航中点击**设置**，你可以改变知识库的以下设置项：

<figure><img src="../../.gitbook/assets/image (182).png" alt=""><figcaption><p>知识库设置</p></figcaption></figure>

**知识库名称**，定义一个名称用于识别一个知识库。

**知识库描述**，用于描述知识库内文档代表的信息

{% hint style="info" %}
在知识库召回模式为 N 选 1 时，知识库作为工具提供给 LLM 进行推理调用，推理依据是知识库的描述，如果描述为空则会使用 Dify 的自动索引策略
{% endhint %}

**可见权限**，可选择 「 只有我 」 或 「 所有团队成员 」，不具有权限的人将无法查阅和编辑数据集。

**索引模式**，[参考文档](https://docs.dify.ai/v/zh-hans/guides/knowledge-base/create-knowledge-and-upload-documents#id-5-suo-yin-fang-shi)

\*\*Embedding 模型，\*\*修改知识库的嵌入模型，修改 Embedding 模型将对知识库内的所有文档重新嵌入，原先的嵌入将会被删除。

**检索设置**，[参考文档](https://docs.dify.ai/v/zh-hans/guides/knowledge-base/create-knowledge-and-upload-documents#id-6-jian-suo-she-zhi)

***

### 9 知识库 API 管理

Dify 知识库提供整套标准 API ，开发者通过 API 调用对知识库内的文档、分段进行增删改查等日常管理维护操作，请参考[知识库 API 文档](maintain-dataset-via-api.md)。

<figure><img src="../../.gitbook/assets/image (180).png" alt=""><figcaption><p>知识库 API 管理</p></figcaption></figure>
