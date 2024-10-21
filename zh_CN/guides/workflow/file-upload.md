---
description: 作者：Steven, Allen, Evan. Technical Writer
---

# 文件上传

许多专业的内容存储在文档文件内，例如学术报告、法律合同。受限于 LLM 仅能够文本或者图片输入源，难以获取文件内更加丰富的上下文信息，许多用户不得不手动复制粘贴大量信息与 LLM 对话，应用场景有限。

文件上传功能允许将文件以 File variables 的形式在工作流应用中上传、解析、引用、和下载。**开发者现可轻松构建能理解和处理图片、音频、视频的复杂工作。**



### 应用场景

1. **文档分析**: 上传学术研究报告文件，LLM 可以快速总结要点，根据文件内容回答相关问题。
2. **代码审查**: 开发者上传代码文件，获得优化建议与 bug 检测。
3. **学习辅导**: 学生上传作业或学习资料，获得个性化的解释和指导。
4. **法律援助**: 上传完整的合同文本，由 LLM 协助审查条款，指出潜在风险。

### 文件上传和知识库的关系

文件上传和知识库都是为 LLM 提供额外上下文信息的方式，但它们在使用场景和功能上有明显区别：

1. **信息来源**：
   - 文件上传：允许终端用户在对话过程中动态上传文件，提供即时的、个性化的上下文信息。
   - 知识库：由应用开发者预先设置和管理，包含相对固定的信息集合。

2. **使用灵活性**：
   - 文件上传：更加灵活，用户可以根据具体需求上传不同类型的文件。
   - 知识库：内容相对固定，但可以被多个会话重复利用。

3. **信息处理**：
   - 文件上传：需要通过文档提取器或其他工具将文件内容转换为 LLM 可理解的文本。
   - 知识库：通常已经过预处理和索引，可以直接进行检索。

4. **应用场景**：
   - 文件上传：适用于需要处理用户特定文档的场景，如文档分析、个性化学习辅导等。
   - 知识库：适用于需要访问大量预设信息的场景，如客户服务、产品咨询等。

5. **数据持久性**：
   - 文件上传：通常为临时使用，不会长期存储在系统中。
   - 知识库：作为应用的一部分长期存在，可以持续更新和维护。



### 快速开始

Dify 支持在 [ChatFlow](key-concept.md#chatflow-he-workflow) 和 [WorkFlow](key-concept.md#chatflow-he-workflow) 类型应用中上传文件，并通过[变量](variables.md)交由 LLM 处理。以下是文件上传功能的主要组成部分:

#### 文件上传

应用开发者可以参考以下方法为应用开启文件上传功能：

* 在 Workflow 应用中：
  - 在 ["开始节点"](node/start.md) 添加文件变量

* 在 ChatFlow 应用中：
  - 在 ["附加功能"](additional-features.md) 中开启文件上传，允许在聊天窗中直接上传文件
  - 在 ["开始节点"](node/start.md) 添加文件变量
  - 注意：这两种方法可以同时配置，它们是彼此独立的。附加功能中的文件上传设置（包括上传方式和数量限制）不会影响开始节点中的文件变量。例如只想通过开始节点创建文件变量，则无需开启附加功能中的文件上传功能。

这两种方法为应用提供了灵活的文件上传选项，以满足不同场景的需求。


file variables 和 array[file] variables 支持以下文件类型与格式：

<table data-header-hidden><thead><tr><th width="227"></th><th></th></tr></thead><tbody><tr><td>文件类型</td><td>支持格式</td></tr><tr><td>文档</td><td>TXT, MARKDOWN, PDF, HTML, XLSX, XLS, DOCX, CSV, EML, MSG, PPTX, PPT, XML, EPUB.</td></tr><tr><td>图片</td><td>JPG, JPEG, PNG, GIF, WEBP, SVG.</td></tr><tr><td>音频</td><td>MP3, M4A, WAV, WEBM, AMR.</td></tr><tr><td>视频</td><td>MP4, MOV, MPEG, MPGA.</td></tr><tr><td>其他</td><td>自定义后缀名支持</td></tr></tbody></table>

##### 方法一：在应用聊天框中开启文件上传（仅适用于 Chatflow）

1.  点击 Chatflow 应用右上角的 **“功能”** 按钮即可为应用添加更多功能。

    开启此功能后，应用使用者可以在应用对话的过程中随时上传并更新文件。最多支持同时上传 10 个文件，每个文件的大小上限为 15MB。

<figure><img src="../../.gitbook/assets/image (379).png" alt=""><figcaption><p>文件上传功能</p></figcaption></figure>

开启该功能并不意味着赋予 LLM 直接读取文件的能力，还需要配备[**文档提取器**](node/doc-extractor.md)将文档解析为文本供 LLM 理解。音频、视频和其他文件类型暂无对应的提取器，需要应用开发者接入[外部工具](../tools/advanced-tool-integration.md)进行处理。或者使用gpt-4o-audio-preview等支持多模态输入的模型，模型可以直接处理音频，无需额外的提取器。

2. 添加[文档提取器](node/doc-extractor.md)节点，在输入变量中选中 `sys.files` 变量。
3. 添加 LLM 节点，在系统提示词中选中文档提取器节点的输出变量。
4. 在末尾添加 “直接回复” 节点，填写 LLM 节点的输出变量。

<figure><img src="../../.gitbook/assets/image (380).png" alt=""><figcaption></figcaption></figure>

开启后，用户可以在对话框中上传文件并进行对话。但通过此方式， LLM 应用并不具备记忆文件内容的能力，每次对话时需要上传文件。

<figure><img src="../../.gitbook/assets/image (381).png" alt=""><figcaption></figcaption></figure>

若希望 LLM 能够在对话中记忆文件内容，请参考方法二。

##### 方法二：通过添加文件变量开启文件上传功能


在应用的[“开始”](node/start.md)节点内添加输入字段，选择**“单文件”**或**“文件列表”** 字段类型的变量。

{% @arcade/embed flowId="TiLAgL3vgozVhuLBmob9" url="https://app.arcade.software/share/TiLAgL3vgozVhuLBmob9" %}

*   **单文件**

    仅允许应用使用者上传单个文件。
*   **文件列表**

    允许应用使用者单词批量上传多个文件。

> 为了便于操作，将使用单文件变量作为示例。
#### 文件解析
文件变量的使用方式主要分为两种：

1. 使用工具节点转换文件内容：
   - 对于文档类型的文件，可以使用"文档提取器"节点将文件内容转换为文本形式。
   - 这种方法适用于需要将文件内容解析为模型可理解的格式（如string、array[string]等）的情况。

2. 直接在LLM节点中使用文件变量：
   - 对于某些特定类型的文件（如图片），可以在LLM节点中直接使用文件变量。
   - 例如，对于图片类型的file variables，可以在LLM节点中启用vision功能，然后在变量选择器中直接引用对应的文件变量。

选择哪种方式取决于文件类型和您的具体需求。接下来，我们将详细介绍这两种方法的具体操作步骤。

##### 添加文档提取器节点

上传文件后将存储至单文件变量内，LLM 暂不支持直接读取变量中的文件。因此需要先添加 [**“文档提取器”**](node/doc-extractor.md)&#x20;

节点，从已上传的文档文件内提取内容并发送至 LLM 节点完成信息处理。

将“开始”节点内的文件变量作为**“文档提取器”**节点的输入变量。

<figure><img src="../../.gitbook/assets/截屏2024-10-12 15.45.45.png" alt=""><figcaption><p>添加输入变量</p></figcaption></figure>

将“文档提取器”节点的输出变量填写至 LLM 节点的系统提示词内。

<figure><img src="../../.gitbook/assets/image (376).png" alt=""><figcaption><p>粘贴系统提示词</p></figcaption></figure>

完成上述设置后，应用的使用者可以在 WebApp 内粘贴文件 URL 或上传本地文件，然后就文档内容与 LLM 展开互动。应用使用者可以在对话过程中随时替换文件，LLM 将获取最新的文件内容。

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>粘贴 URL 进行对话</p></figcaption></figure>

##### 直接在 LLM 节点中使用文件变量


### 进阶使用

若希望应用能够支持上传多种文件，例如允许用户同时上传文档文件、图片和音视频文件，此时需要在 “开始节点” 中添加  “文件列表” 变量，并通过“列表操作”节点针对不同的文件类型进行处理。详细说明请参考[列表操作](node/list-operator.md)节点。

<figure><img src="../../.gitbook/assets/image (378).png" alt=""><figcaption></figcaption></figure>

如需查看更多使用案例，请参考以下内容：

动手实验室 - 使用文件上传搭建文章理解助手（上线后替换链接）

