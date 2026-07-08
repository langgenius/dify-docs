服务器发送事件 (SSE) 流。

**解析**：每个事件是一行以 `data: ` 为前缀的 JSON 对象，以 `\n\n` 终止。解析 JSON 前先去除 `data: ` 前缀，再读取 `event` 字段确定事件类型。忽略 `ping` 事件，它以 `event: ping` 行的形式（无 `data:` 载荷）每 10 秒发送一次以保持连接活跃。

**流生命周期**：聊天助手应用的回复以 `message` 事件流式返回，Agent 应用则以 `agent_thought` 与 `agent_message` 事件返回。流以 `message_end` 结束；开启文本转语音（TTS）自动播放时，`tts_message` 事件会穿插其间，`tts_message_end` 成为最后一个事件。

Chatflow 应用中，工作流进度以 `workflow_started`、节点事件（`node_started` 和 `node_finished`，以及迭代和循环的相应变体）流式返回，回复则以 `message` 事件返回（设置 `reasoning_format: separated` 的 LLM 节点还会同时发送 `reasoning_chunk` 事件，承载模型的推理内容）。开启文本转语音（TTS）自动播放时，`tts_message_end` 跟随在结束事件之后。结束序列取决于运行结果：
- **成功**：`message_end`，随后 `workflow_finished`
- **失败**：`workflow_finished`（状态为 `failed`），随后 `error`；不发送 `message_end`
- **暂停**：`human_input_required`，随后 `workflow_paused`（流到此结束，运行将另行恢复）

新 Agent 应用的回复以 `message` 文本片段流式返回，模型的推理和工具调用会同时以 `agent_thought` 事件返回。`message_end` 的 `metadata` 包含 `usage`（命中标注回复时还包含 `annotation_reply`），不会包含 `retriever_resources`。

**事件**：除 `ping` 外，每个事件都包含 `conversation_id`、`message_id` 和 `created_at`（Unix 纪元秒）；除 `error` 外，其余事件还包含 `task_id`。工作流、节点和人工介入事件（Chatflow 应用）还将载荷嵌套在 `data` 中，且除 `agent_log` 外都带有顶层 `workflow_run_id`。

**回复事件**

| 事件 | 应用 | 触发时机 | 关键字段 |
|:---|:---|:---|:---|
| `message` | 聊天助手、对话流、新 Agent | 每个回答片段（按顺序拼接） | `answer` |
| `agent_message` | Agent | 每个回答片段（按顺序拼接） | `answer` |
| `agent_thought` | Agent、新 Agent | 每个推理或工具调用步骤 | `position`、`thought`、`tool`、`tool_input`（JSON）、`observation`、`message_files` |
| `message_replace` | 全部 | 内容审核替换已生成的回答 | `answer`；Chatflow 应用还包含 `reason` |
| `reasoning_chunk` | 对话流 | 每个推理内容增量，当 LLM 节点使用 `reasoning_format: separated` 时（按顺序拼接；`is_final: true` 的事件标志推理结束，且 `reasoning` 可能为空） | `data.message_id`、`data.reasoning`、`data.node_id`、`data.is_final` |
| `message_file` | 聊天助手、Agent | 助手返回文件 | `type`、`belongs_to`、`url` |
| `message_end` | 全部 | 回答完成 | `metadata`（`usage`、`retriever_resources`） |
| `tts_message`、`tts_message_end` | 聊天助手、Agent、对话流 | 音频片段/结束，开启 TTS 自动播放时 | `audio` |

**工作流与节点事件**（仅 Chatflow 应用）

每个事件都将载荷嵌套在 `data` 对象中。

| 事件 | 触发时机 | 关键 `data` 字段 |
|:---|:---|:---|
| `workflow_started` | 运行开始 | `inputs` |
| `node_started` | 节点开始 | `node_id`、`node_type`、`title` |
| `node_finished` | 节点结束 | `status`、`outputs`、`execution_metadata` |
| `node_retry` | 节点失败后重试 | `retry_index` |
| `iteration_started`、`iteration_next`、`iteration_completed` | 迭代节点进度（信息性，可不处理） | `data` |
| `loop_started`、`loop_next`、`loop_completed` | 循环节点进度（信息性，可不处理） | `data` |
| `agent_log` | Agent 节点步骤日志（信息性，可不处理；无 `workflow_run_id`） | `data` |
| `workflow_finished` | 运行结束 | `status`（`succeeded`、`failed`、`partial-succeeded`、`stopped`）、`outputs`、`total_tokens` |
| `workflow_paused` | 运行暂停 | `paused_nodes`、`reasons` |
| `human_input_required` | 运行到达人工介入节点 | `form_token`、`form_content`、`expiration_time` |

暂停后，本流在 `workflow_paused` 处结束。通过 [提交人工介入表单](/zh/api-reference/human-input/submit-human-input-form) 提交表单，或等待其超时；恢复后的运行（包括从 `human_input_form_filled`/`human_input_form_timeout` 到 `workflow_finished` 的事件）由 [流式获取工作流事件](/zh/api-reference/workflow-runs/stream-workflow-events) 流式返回。

**传输事件**

| 事件 | 触发时机 | 关键字段 |
|:---|:---|:---|
| `error` | 失败导致流结束；HTTP 仍为 `200` | `status`（如 `400`）、`code`（如 `invalid_param`）、`message` |
| `ping` | 每 10 秒保持连接 | 无 |
