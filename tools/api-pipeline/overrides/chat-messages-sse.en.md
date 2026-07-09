A stream of Server-Sent Events (SSE).

**Parsing**: Each event is a line prefixed with `data: ` followed by a JSON object, terminated by `\n\n`. Strip the `data: ` prefix before parsing the JSON, then read the `event` field to determine the event type. Ignore `ping` events, which arrive as `event: ping` lines (no `data:` payload) every 10 seconds to keep the connection alive.

**Stream lifecycle**: For Chatbot apps, the reply streams as `message` events; for Agent apps, as `agent_thought` and `agent_message` events. The stream ends with `message_end`; when text-to-speech auto-play is enabled, `tts_message` events interleave and `tts_message_end` becomes the final event.

For Chatflow apps, workflow progress streams as `workflow_started`, node events (`node_started` and `node_finished`, plus iteration and loop variants), and the reply as `message` events (an LLM node with `reasoning_format: separated` also emits `reasoning_chunk` events alongside, carrying the model's reasoning content). When text-to-speech auto-play is enabled, `tts_message_end` trails the closing event. The closing sequence depends on the outcome:
- **Success**: `message_end`, then `workflow_finished`
- **Failure**: `workflow_finished` with status `failed`, then `error`; no `message_end`
- **Pause**: `human_input_required`, then `workflow_paused` (the stream ends here; the run resumes separately)

For New Agent apps, the reply streams incrementally as `agent_message` events, with the model's reasoning and tool calls streaming alongside as `agent_thought` events; a single closing `message` event then carries the complete answer (render the deltas live and treat that `message` as the final answer rather than appending it). `message_end` metadata carries `usage` (plus `annotation_reply` when an annotation match replies) and never includes `retriever_resources`.

**Events**: Apart from `ping`, every event includes `conversation_id`, `message_id`, and `created_at` (Unix epoch seconds); all but `error` also include `task_id`. Workflow, node, and human-input events (Chatflow apps) also nest their payload under `data` and, except for `agent_log`, carry a top-level `workflow_run_id`.

**Reply events**

| Event | App | Fires on | Key fields |
|:---|:---|:---|:---|
| `message` | Chatbot, Chatflow, New Agent | each answer chunk (concatenate in order); for New Agent, one closing chunk with the complete answer | `answer` |
| `agent_message` | Agent, New Agent | each answer chunk (concatenate in order) | `answer` |
| `agent_thought` | Agent, New Agent | each reasoning or tool-call step | `position`, `thought`, `tool`, `tool_input` (JSON), `observation`, `message_files` |
| `message_replace` | All | output moderation replaces the answer so far | `answer`; Chatflow also `reason` |
| `reasoning_chunk` | Chatflow | each reasoning-content delta, when an LLM node uses `reasoning_format: separated` (concatenate in order; a final `is_final: true` event marks reasoning finished and may carry an empty `reasoning`) | `data.message_id`, `data.reasoning`, `data.node_id`, `data.is_final` |
| `message_file` | Chatbot, Agent | the assistant returns a file | `type`, `belongs_to`, `url` |
| `message_end` | All | the answer is complete | `metadata` (`usage`, `retriever_resources`) |
| `tts_message`, `tts_message_end` | Chatbot, Agent, Chatflow | audio chunk / end, when TTS auto-play is on | `audio` |

**Workflow and node events** (Chatflow apps only)

Each event nests its payload under a `data` object.

| Event | Fires on | Key `data` fields |
|:---|:---|:---|
| `workflow_started` | the run begins | `inputs` |
| `node_started` | a node begins | `node_id`, `node_type`, `title` |
| `node_finished` | a node ends | `status`, `outputs`, `execution_metadata` |
| `node_retry` | a node retries after a failure | `retry_index` |
| `iteration_started`, `iteration_next`, `iteration_completed` | Iteration node progress (informational) | `data` |
| `loop_started`, `loop_next`, `loop_completed` | Loop node progress (informational) | `data` |
| `agent_log` | an Agent node step log (informational; no `workflow_run_id`) | `data` |
| `workflow_finished` | the run ends | `status` (`succeeded`, `failed`, `partial-succeeded`, `stopped`), `outputs`, `total_tokens` |
| `workflow_paused` | the run pauses | `paused_nodes`, `reasons` |
| `human_input_required` | the run reaches a Human Input node | `form_token`, `form_content`, `expiration_time` |

After a pause this stream ends at `workflow_paused`. Submit the form via [Submit Human Input Form](/en/api-reference/human-input/submit-human-input-form) or let it time out; the resumed run, including `human_input_form_filled`/`human_input_form_timeout` through `workflow_finished`, streams from [Stream Workflow Events](/en/api-reference/workflow-runs/stream-workflow-events).

**Transport events**

| Event | Fires on | Key fields |
|:---|:---|:---|
| `error` | a failure ends the stream; HTTP stays `200` | `status` (e.g. `400`), `code` (e.g. `invalid_param`), `message` |
| `ping` | keep-alive every 10 seconds | none |
