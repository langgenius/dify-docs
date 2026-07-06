サーバー送信イベント (SSE) のストリームです。

**パース**：各イベントは `data: ` プレフィックス付きの JSON オブジェクトの行で、`\n\n` で終了します。JSON をパースする前に `data: ` プレフィックスを除去し、`event` フィールドを読み取ってイベントタイプを判定してください。`ping` イベントは `event: ping` 行（`data:` ペイロードなし）として 10 秒ごとに接続維持のために送信されるため、無視してください。

**ストリームライフサイクル**：チャットボットアプリでは、回答は `message` イベントとしてストリーミングされます。Agent アプリでは `agent_thought` と `agent_message` イベントになります。ストリームは `message_end` で終了します。テキスト読み上げ（TTS）の自動再生が有効な場合、`tts_message` イベントが間に挟まり、`tts_message_end` が最後のイベントになります。

チャットフローアプリでは、ワークフローの進行は `workflow_started`、ノードイベント（`node_started` と `node_finished`、およびイテレーションとループの各バリアント）として、回答は `message` イベントとしてストリーミングされます（`reasoning_format: separated` を指定した LLM ノードは、モデルの思考過程を伝える `reasoning_chunk` イベントも並行して発行します）。テキスト読み上げ（TTS）の自動再生が有効な場合、`tts_message_end` が終了イベントの後に続きます。終了シーケンスは実行結果によって異なります：
- **成功**：`message_end`、続いて `workflow_finished`
- **失敗**：ステータスが `failed` の `workflow_finished`、続いて `error`。`message_end` は送信されません
- **一時停止**：`human_input_required`、続いて `workflow_paused`（ストリームはここで終了し、実行は別途再開されます）

New Agent アプリでは、回答は `message` イベントとしてストリーミングされ、`message_end` で終了します。モデルの推論やツール使用はストリームイベントとして公開されません。`message_end` の `metadata` には `usage` が含まれ（アノテーションが一致した場合は `annotation_reply` も含まれます）、`retriever_resources` は含まれません。

**イベント**：`ping` を除き、すべてのイベントには `conversation_id`、`message_id`、`created_at`（Unix エポック秒）が含まれます。`error` を除くイベントには `task_id` も含まれます。ワークフロー、ノード、人間の入力イベント（チャットフローアプリ）は、ペイロードを `data` の下にネストし、`agent_log` を除いてトップレベルの `workflow_run_id` を持ちます。

**応答イベント**

| イベント | アプリ | 発生タイミング | 主なフィールド |
|:---|:---|:---|:---|
| `message` | チャットボット、チャットフロー、New Agent | 回答の各チャンク（順番に連結） | `answer` |
| `agent_message` | Agent | 回答の各チャンク（順番に連結） | `answer` |
| `agent_thought` | Agent | 推論またはツール呼び出しの各ステップ | `position`、`thought`、`tool`、`tool_input`（JSON）、`observation`、`message_files` |
| `message_replace` | すべて | 出力モデレーションがそれまでの回答を置き換える | `answer`。チャットフローでは `reason` も含む |
| `reasoning_chunk` | チャットフロー | 思考過程の各デルタ（LLM ノードが `reasoning_format: separated` を使用する場合）。順番に連結してください。`is_final: true` の最終イベントは思考の完了を示し、空の `reasoning` を伴う場合があります | `data.message_id`、`data.reasoning`、`data.node_id`、`data.is_final` |
| `message_file` | チャットボット、Agent | アシスタントがファイルを返す | `type`、`belongs_to`、`url` |
| `message_end` | すべて | 回答が完了 | `metadata`（`usage`、`retriever_resources`） |
| `tts_message`、`tts_message_end` | チャットボット、Agent、チャットフロー | 音声チャンク/終了（TTS 自動再生が有効な場合） | `audio` |

**ワークフロー・ノードイベント**（チャットフローアプリのみ）

各イベントはペイロードを `data` オブジェクトの下にネストします。

| イベント | 発生タイミング | 主な `data` フィールド |
|:---|:---|:---|
| `workflow_started` | 実行開始 | `inputs` |
| `node_started` | ノード開始 | `node_id`、`node_type`、`title` |
| `node_finished` | ノード終了 | `status`、`outputs`、`execution_metadata` |
| `node_retry` | 失敗後にノードを再試行 | `retry_index` |
| `iteration_started`、`iteration_next`、`iteration_completed` | イテレーションノードの進行（情報提供のみ、処理は任意） | `data` |
| `loop_started`、`loop_next`、`loop_completed` | ループノードの進行（情報提供のみ、処理は任意） | `data` |
| `agent_log` | Agent ノードのステップログ（情報提供のみ、処理は任意、`workflow_run_id` なし） | `data` |
| `workflow_finished` | 実行終了 | `status`（`succeeded`、`failed`、`partial-succeeded`、`stopped`）、`outputs`、`total_tokens` |
| `workflow_paused` | 実行が一時停止 | `paused_nodes`、`reasons` |
| `human_input_required` | 実行が人間の入力ノードに到達 | `form_token`、`form_content`、`expiration_time` |

一時停止後、このストリームは `workflow_paused` で終了します。[人間の入力フォームを送信](/ja/api-reference/human-input/submit-human-input-form) でフォームを送信するか、タイムアウトさせてください。再開後の実行（`human_input_form_filled`/`human_input_form_timeout` から `workflow_finished` までを含む）は、[ワークフローイベントをストリーム](/ja/api-reference/workflows/stream-workflow-events) からストリーミングされます。

**トランスポートイベント**

| イベント | 発生タイミング | 主なフィールド |
|:---|:---|:---|
| `error` | 失敗によりストリームが終了。HTTP は `200` のまま | `status`（例：`400`）、`code`（例：`invalid_param`）、`message` |
| `ping` | 10 秒ごとのキープアライブ | なし |
