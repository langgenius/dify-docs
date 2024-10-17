# Agent

### 定义

智能助手（Agent Assistant），利用大语言模型的推理能力，能够自主对复杂的人类任务进行目标规划、任务拆解、工具调用、过程迭代，并在没有人类干预的情况下完成任务。

### 如何使用智能助手

为了方便快速上手使用，您可以在“探索”中找到智能助手的应用模板，添加到自己的工作区，或者在此基础上进行自定义。在全新的 Dify 工作室中，你也可以从零编排一个专属于你自己的智能助手，帮助你完成财务报表分析、撰写报告、Logo 设计、旅程规划等任务。

<figure><img src="../../.gitbook/assets/image (98).png" alt=""><figcaption><p>探索-智能助手应用模板</p></figcaption></figure>

选择智能助手的推理模型，智能助手的任务完成能力取决于模型推理能力，我们建议在使用智能助手时选择推理能力更强的模型系列如 gpt-4 以获得更稳定的任务完成效果。

<figure><img src="../../.gitbook/assets/image (102).png" alt=""><figcaption><p>选择智能助手的推理模型</p></figcaption></figure>

你可以在“提示词”中编写智能助手的指令，为了能够达到更优的预期效果，你可以在指令中明确它的任务目标、工作流程、资源和限制等。

<figure><img src="../../.gitbook/assets/image (99).png" alt=""><figcaption><p>编排智能助手的指令提示词</p></figcaption></figure>

### 添加助手需要的工具

在“上下文”中，你可以添加智能助手可以用于查询的知识库工具，这将帮助它获取外部背景知识。

在“工具”中，你可以添加需要使用的工具。工具可以扩展 LLM 的能力，比如联网搜索、科学计算或绘制图片，赋予并增强了 LLM 连接外部世界的能力。Dify 提供了两种工具类型：**第一方工具**和**自定义工具**。

你可以直接使用 Dify 生态提供的第一方内置工具，或者轻松导入自定义的 API 工具（目前支持 OpenAPI / Swagger 和 OpenAI Plugin 规范）。

<figure><img src="../../.gitbook/assets/image (100).png" alt=""><figcaption><p>添加助手需要的工具</p></figcaption></figure>

“工具”功能允许用户借助外部能力，在 Dify 上创建出更加强大的 AI 应用。例如你可以为智能助理型应用（Agent）编排合适的工具，它可以通过任务推理、步骤拆解、调用工具完成复杂任务。

另外工具也可以方便将你的应用与其他系统或服务连接，与外部环境交互。例如代码执行、对专属信息源的访问等。你只需要在对话框中谈及需要调用的某个工具的名字，即可自动调用该工具。

![](../../.gitbook/assets/zh-agent-dalle3.png)

### 配置 Agent

在 Dify 上为智能助手提供了 Function calling（函数调用）和 ReAct 两种推理模式。已支持 Function Call 的模型系列如 gpt-3.5/gpt-4 拥有效果更佳、更稳定的表现，尚未支持 Function calling 的模型系列，我们支持了 ReAct 推理框架实现类似的效果。

在 Agent 配置中，你可以修改助手的迭代次数限制。

<figure><img src="../../.gitbook/assets/image (108).png" alt=""><figcaption><p>Function Calling 模式</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (110).png" alt=""><figcaption><p>ReAct 模式</p></figcaption></figure>

### 配置对话开场白

您可以为智能助手配置一套会话开场白和开场问题，配置的对话开场白将在每次用户初次对话中展示助手可以完成什么样的任务，以及可以提出的问题示例。

<figure><img src="../../.gitbook/assets/image (101).png" alt=""><figcaption><p>配置会话开场白和开场问题</p></figcaption></figure>

### 调试与预览

编排完智能助手之后，你可以在发布成应用之前进行调试与预览，查看助手的任务完成效果。

<figure><img src="../../.gitbook/assets/image (104).png" alt=""><figcaption><p>调试与预览</p></figcaption></figure>

### 应用发布

<figure><img src="../../.gitbook/assets/image (105).png" alt=""><figcaption><p>应用发布为 Webapp</p></figcaption></figure>
