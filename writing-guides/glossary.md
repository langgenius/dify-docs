# Dify Documentation Glossary

Standard terminology for Dify documentation. Single source of truth for writers, translators, and the automated translation pipeline.

---

## General Terms

Terms appear in body text exactly as written in this table. Capitalize them further only when external rules require it (start of a sentence, title case headings).

### Core Concepts

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| Workflow | 工作流 | ワークフロー | |
| Chatflow | 对话流 | チャットフロー | |
| Agent | Agent | Agent | Dify App type (alongside Workflow, Chatflow, etc.) that autonomously uses tools|
| Text Generator | 文本生成应用 | テキストジェネレーター | |
| knowledge base | 知识库 | ナレッジベース | Always lowercase unless at sentence start |
| plugin | 插件 | プラグイン | |
| Dify tool | Dify 工具 | ツール | |
| workspace | 工作区 | ワークスペース | |
| template | 模板 | テンプレート | Published app that others can download from Dify Marketplace and use |
| WebApp | WebApp | WebApp | |

### Models

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| model | 模型 | モデル | |
| model provider | 模型供应商 | モデルプロバイダー | |
| LLM (large language model) | 大语言模型 | 大規模言語モデル | |
| chat model | 对话模型 | チャットモデル | Models that support role-based conversations (System/User/Assistant) |
| completion model | 文本续写模型 | 補完モデル | Models designed for simple text continuation |
| embedding model | 嵌入模型 | 埋め込みモデル | |
| text embedding model | 文本嵌入模型 | テキスト埋め込みモデル | Models that convert text into vector representations |
| multimodal embedding model | 多模态嵌入模型 | マルチモーダル埋め込みモデル | Models that convert text and images into vector representations |
| rerank model | 重排序模型 | リランクモデル | Models that reorder retrieval results by relevance |
| reasoning model | 推理模型 | 推論モデル | Models that output thinking process before final response |
| moderation model | 内容审核模型 | モデレーションモデル | Models that detect and filter inappropriate content |
| TTS model | 文字转语音模型 | TTSモデル | Text-to-speech models |
| Speech2Text model | 语音转文字模型 | 音声認識モデル | Speech-to-text models |
| token | token | token | |
| API token | API 令牌 | APIトークン | |
| prompt | 提示词 | プロンプト | |
| system instruction | 系统指令 | システムインストラクション | Defines the model's behavior and role |
| user message | User 消息 | ユーザーメッセージ | Passes user input or provides example queries |
| assistant message | Assistant 消息 | アシスタントメッセージ | Provides example responses to guide model behavior |
| model tag | 模型标签 | モデルタグ | Indicators of model capabilities (Vision, Tool Call, context window, etc.) |

### Nodes

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| node | 节点 | ノード | |
| User Input | 用户输入 | ユーザー入力 | Start node; collects information from end users during application runtime |
| Output | 输出 | 出力 | End node for Workflows; defines output variables |
| Answer | 直接回复 | 回答 | End node for Chatflows; streams response text to the user |
| LLM | LLM | LLM | Node that calls large language models to generate responses |
| Knowledge Retrieval | 知识检索 | ナレッジ検索 | Retrieves relevant information from knowledge bases |
| Question Classifier | 问题分类器 | 質問分類器 | Classifies user input into categories using an LLM |
| IF/ELSE | 条件分支 | IF/ELSE | Splits workflow into branches based on conditions |
| Code | 代码执行 | コード実行 | Executes custom Python or JavaScript code |
| Template | 模板转换 | テンプレート | Transforms data using Jinja2 templates |
| HTTP Request | HTTP 请求 | HTTP リクエスト | Sends HTTP requests to external APIs |
| Variable Aggregator | 变量聚合器 | 変数集約器 | Aggregates multi-branch variables into one |
| Variable Assigner | 变量赋值器 | 変数代入器 | Assigns values to conversation/environment variables |
| Tool | 工具 | ツール | Calls external tools and services |
| Parameter Extractor | 参数提取器 | パラメータ抽出 | Extracts structured parameters from natural language using an LLM |
| Iteration | 迭代 | イテレーション | Processes array items sequentially |
| Loop | 循环 | ループ | Repeats steps until a condition is met |
| Doc Extractor | 文档提取器 | テキスト抽出 | Extracts text content from document files |
| List Operator | 列表操作 | リスト処理 | Filters, sorts, and limits list data |
| Agent | Agent | Agent | Workflow node (distinct from Agent app type above) |
| Human Input | 人工介入 | 人間の入力 | Pauses workflow execution to request human review or decisions |
| Schedule Trigger | 定时触发器 | スケジュールトリガー | Triggers workflow execution on a cron schedule |
| Webhook Trigger | Webhook 触发器 | Webhook トリガー | Triggers workflow execution via incoming HTTP webhook |
| Plugin Trigger | 插件触发器 | プラグイントリガー | Triggers workflow execution from a plugin |
| Command | 命令 | コマンド | Executes commands in the sandboxed runtime environment |
| Upload File to Sandbox | 上传文件至沙盒 | サンドボックスへのファイルアップロード | Uploads files to the sandboxed runtime environment |

### Knowledge & Retrieval

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| knowledge base | 知识库 | ナレッジベース | Always lowercase unless at sentence start |
| chunk | 分段 | チャンク | Use "chunk" not "segment"; a segment of text resulting from the chunking process |
| chunking | 分段 | チャンキング | Use "chunking" consistently; avoid "segmentation" or "splitting" |
| retrieval | 检索 | 検索 | Always lowercase in body text |
| retrieval mode | 检索模式 | 検索モード | Strategy for finding and ranking relevant chunks |
| indexing | 索引 | インデックス | Use "Index Method" consistently in documentation |
| index method | 索引方法 | インデックス方法 | Also referred to as "Index Method" in some UI contexts |
| embedding | 嵌入 | 埋め込み | |
| metadata | 元数据 | メタデータ | |
| delimiter | 分隔符 | デリミタ | The character or sequence used to split text during chunking |
| maximum chunk length | 最大分段长度 | 最大チャンク長 | The maximum size of each chunk in characters |
| chunk overlap | 分段重叠 | チャンクオーバーラップ | Characters overlapping between adjacent chunks; specific to General mode |
| General mode | 通用模式 | 汎用モード | Single-tier chunking where all chunks use the same settings |
| Parent-child mode | 父子模式 | 親子モード | Two-tier hierarchical chunking strategy |
| parent chunk | 父分段 | 親チャンク | Larger text blocks that provide context to the LLM |
| child chunk | 子分段 | 子チャンク | Smaller, fine-grained pieces used for semantic search |
| Paragraph mode | 段落模式 | 段落モード | Parent chunk creation mode that splits documents into multiple chunks |
| Full Doc mode | 全文档模式 | 全文書モード | Parent chunk creation mode where the entire document is a single chunk; capitalize "Full Doc" |
| pre-processing | 预处理 | 前処理 | Text cleaning operations before chunking; use "pre-processing" (noun) or "pre-process" (verb) |
| Summary Auto-Gen | 摘要自动生成| 要約自動生成 | Feature that automatically generates summaries for chunks |
| Top K | Top K | Top K | Number of most relevant chunks to retrieve |
| score threshold | 分数阈值 | スコアしきい値 | Minimum relevance score required for chunks to be included |

### Configuration & Parameters

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| variable | 变量 | 変数 | |
| environment variable | 环境变量 | 環境変数 | |
| Top P | Top P | Top P | |
| context variable | 上下文变量 | コンテキスト変数 | Variables injected to provide additional information to the LLM node |
| conversation memory | 对话记忆 | 会話メモリ | Feature that retains recent chat history (Chatflows only) |
| window size | 窗口大小 | ウィンドウサイズ | Controls how many recent exchanges to retain in memory |
| structured output | 结构化输出 | 構造化出力 | Feature that enforces JSON schema for reliable formatting |
| input field | 输入字段 | 入力フィールド | Form fields where people provide requested information |
| request form | 请求表单 | リクエストフォーム | The form sent to recipients asking for input/review; use "request form" not "request page" |
| Assemble Variable | 变量组装 | 変数アセンブル | On-demand data transformation using natural language descriptions |

### Agent

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| Max Iterations | 最大迭代次数 | 最大イテレーション数 | Limits the maximum number of reasoning loops and tool actions |

### Infrastructure

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| self-hosted | 自托管 | セルフホスト | |
| SaaS | SaaS | SaaS | |
| Docker | Docker | Docker | |
| sandbox | 沙箱 | サンドボックス | |
| API | API | API | |
| runtime | 运行时 | ランタイム | The execution environment for workflow nodes |
| classic runtime | 经典运行时 | クラシックランタイム | Original lightweight execution environment focused on speed and token efficiency |
| sandboxed runtime | 沙盒运行时 | サンドボックスランタイム | Enhanced execution environment with file system access and autonomous tool installation |
| skill | 技能 | スキル | Reusable expertise packages that eliminate repetitive prompt writing (Sandboxed runtime) |
| file system | 文件系统 | ファイルシステム | Sandboxed file access for reading/writing during execution |

### Marketplace

| English | Chinese | Japanese | Notes |
|:--------|:--------|:---------|:------|
| Marketplace | 市场 | マーケットプレイス | Platform where users publish and discover app templates |
| Creator Center | 创作者中心 | クリエイターセンター | Interface for managing template submissions and publications |

## UI Labels

Terms in this section must match the Dify product interface exactly. When these terms appear **bolded** in documentation, translations MUST use the corresponding UI string from the product.

### Sidebar & Navigation

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Studio | 工作室 | スタジオ | common.menus.apps | Sidebar menu label for the app workspace |
| Knowledge | 知识库 | ナレッジ | common.menus.datasets | Sidebar menu label; not to be confused with lowercase "knowledge base" in prose |
| Explore | 探索 | 探索 | common.menus.explore | Sidebar menu label |
| Plugins | 插件 | プラグイン | common.menus.plugins | Sidebar menu label |
| Tools | 工具 | ツール | common.menus.tools | Sidebar menu label |

### App Detail Tabs

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Orchestrate | 编排 | オーケストレート | common.appMenus.promptEng | App configuration tab |
| Monitoring | 监测 | 監視 | common.appMenus.overview | App metrics/overview tab |
| API Access | 访问 API | API アクセス | common.appMenus.apiAccess | Also used in Knowledge detail |
| Logs & Annotations | 日志与标注 | ログ＆注釈 | common.appMenus.logAndAnn | |

### Knowledge Detail Tabs

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Documents | 文档 | ドキュメント | common.datasetMenus.documents | |
| Retrieval Testing | 召回测试 | 検索テスト | common.datasetMenus.hitTesting | |
| Settings | 设置 | 設定 | common.datasetMenus.settings | |
| Pipeline | 流水线 | パイプライン | common.datasetMenus.pipeline | |

### Settings Panel

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| My account | 我的账户 | マイアカウント | common.settings.account | |
| Members | 成员 | メンバー | common.settings.members | |
| Model Provider | 模型供应商 | モデルプロバイダー | common.settings.provider | |
| Data Source | 数据来源 | データソース | common.settings.dataSource | |
| API Extension | API 扩展 | API 拡張 | common.settings.apiBasedExtension | |
| Billing | 账单 | 請求 | common.settings.billing | |
| Integrations | 集成 | 統合 | common.settings.integrations | |
| Default Model Settings | 默认模型设置 | システムモデル設定 | common.modelProvider.systemModelSettings | Renamed from "System Model Settings" in v1.13.1. EN/ZH UI updated; JA UI still shows "システムモデル設定" until i18n update. Planned JA label:「デフォルトモデル設定」. |
| System Reasoning Model | 系统推理模型 | システム推論モデル | common.modelProvider.systemReasoningModel.key | |
| Embedding Model | Embedding 模型 | 埋め込みモデル | common.modelProvider.embeddingModel.key | |
| Rerank Model | Rerank 模型 | Rerank モデル | common.modelProvider.rerankModel.key | |
| Speech-to-Text Model | 语音转文本模型 | 音声-to-テキストモデル | common.modelProvider.speechToTextModel.key | |
| Text-to-Speech Model | 文本转语音模型 | テキスト-to-音声モデル | common.modelProvider.ttsModel.key | |
| Load Balancing | 负载均衡 | 負荷分散 | common.modelProvider.loadBalancing |  |
| AI Credits | AI Credits | AI クレジット | common.modelProvider.quota | Renamed from "Message Credits" in v1.13.1. ZH uses English "AI Credits" in UI. |
| Usage Priority | 使用优先级 | 使用優先度 | common.modelProvider.card.usagePriority | New in v1.13.1. Determines fallback order between API Key and AI Credits. |
| API Key | API Key | API キー | common.modelProvider.card.apiKeyOption | New in v1.13.1. Model provider credential option alongside AI Credits. |

### Workspace Roles

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Owner | 所有者 | オーナー | common.members.owner | |
| Admin | 管理员 | 管理者 | common.members.admin | |
| Editor | 编辑 | エディター | common.members.editor | |
| Builder | 构建器 | ビルダー | common.members.builder | REVIEW: ZH "构建器" seems unusual for a role name |
| Knowledge Admin | 知识库管理员 | ナレッジ管理員 | common.members.datasetOperator | Formerly "Dataset Operator" in code |
| Normal | 成员 | 通常 | common.members.normal | REVIEW: ZH uses "成员" (member); verify intended translation |

### App Type Selectors

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Assistant | 助手 | アシスタント | app.newApp.chatApp | Chat app creation label |
| Chatbot | 聊天助手 | チャットボット | app.typeSelector.chatbot | App type filter |
| Chatflow | Chatflow | チャットフロー | app.typeSelector.advanced | App type filter |
| Completion | 文本生成 | テキスト生成 | app.typeSelector.completion | App type filter |

### App Actions

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Duplicate | 复制 | 複製 | app.duplicate | |
| Export DSL | 导出 DSL | DSL をエクスポート | app.export | |
| Import DSL file | 导入 DSL 文件 | DSL ファイルをインポート | app.importDSL | |
| Create from Blank | 创建空白应用 | 最初から作成 | app.newApp.startFromBlank | |
| Create from Template | 从应用模板创建 | テンプレートから作成 | app.newApp.startFromTemplate | |
| Tracing | 追踪 | 追跡 | app.tracing.tracing | LLMOps tracing feature |
| Web App Access Control | Web 应用访问控制 | Web アプリアクセス制御 | app.accessControl | |

### Workflow Node Names

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| User Input | 用户输入 | ユーザー入力 | workflow.blocks.start | Start node display name |
| LLM | LLM | LLM | workflow.blocks.llm | |
| Knowledge Retrieval | 知识检索 | 知識検索 | workflow.blocks.knowledge-retrieval | |
| IF/ELSE | 条件分支 | IF/ELSE | workflow.blocks.if-else | |
| Code | 代码执行 | コード実行 | workflow.blocks.code | |
| Template | 模板转换 | テンプレート | workflow.blocks.template-transform | Jinja template transform node |
| Question Classifier | 问题分类器 | 質問分類器 | workflow.blocks.question-classifier | |
| HTTP Request | HTTP 请求 | HTTP リクエスト | workflow.blocks.http-request | |
| Variable Aggregator | 变量聚合器 | 変数集約器 | workflow.blocks.variable-aggregator | |
| Variable Assigner | 变量赋值 | 変数代入 | workflow.blocks.assigner | |
| Iteration | 迭代 | イテレーション | workflow.blocks.iteration | |
| Loop | 循环 | ループ | workflow.blocks.loop | |
| Parameter Extractor | 参数提取器 | パラメータ抽出 | workflow.blocks.parameter-extractor | |
| Doc Extractor | 文档提取器 | テキスト抽出 | workflow.blocks.document-extractor | |
| List Operator | 列表操作 | リスト処理 | workflow.blocks.list-operator | |
| Output | 输出 | 出力 | workflow.blocks.end | End/output node |
| Answer | 直接回复 | 回答 | workflow.blocks.answer | |
| Human Input | 人工介入 | 人間の入力 | workflow.blocks.human-input | |
| Webhook Trigger | Webhook 触发器 | Webhook トリガー | workflow.blocks.trigger-webhook | |
| Schedule Trigger | 定时触发器 | スケジュールトリガー | workflow.blocks.trigger-schedule | |
| Plugin Trigger | 插件触发器 | プラグイントリガー | workflow.blocks.trigger-plugin | |
| Knowledge Base | 知识库 | 知識ベース | workflow.blocks.knowledge-index | Knowledge index node |

### Workflow Controls

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Publish | 发布 | 公開する | workflow.common.publish | |
| Published | 已发布 | 公開済み | workflow.common.published | Status label |
| Unpublished | 未发布 | 未公開 | workflow.common.unpublished | Status label |
| Preview | 预览 | プレビュー | workflow.common.debugAndPreview | Debug & preview button |
| Test Run | 测试运行 | テスト実行 | workflow.common.run | |
| Run App | 运行 | アプリを実行 | workflow.common.runApp | |
| Features | 功能 | 機能 | workflow.common.features | Panel for web app features |
| Version History | 版本历史 | バージョン履歴 | workflow.common.versionHistory | |
| Workflow as Tool | 发布为工具 | ワークフローをツールとして公開する | workflow.common.workflowAsTool | REVIEW: ZH/JA much longer than EN label |
| Embed Into Site | 嵌入网站 | サイトに埋め込む | workflow.common.embedIntoSite | |
| Conversation Variables | 会话变量 | 会話変数 | workflow.chatVariable.panelTitle | Panel label |
| Environment Variables | 环境变量 | 環境変数 | workflow.env.envPanelTitle | Panel label |
| System Variables | 系统变量 | システム変数 | workflow.globalVar.title | Panel label |

### Agent Node Config

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Agentic Strategy | Agent 策略 | エージェンティック戦略 | workflow.nodes.agent.strategy.label | |
| Query Variable | 查询变量 | 検索変数 | workflow.nodes.knowledgeRetrieval.queryVariable | Knowledge retrieval node config |
| Metadata Filtering | 元数据过滤 | メタデータフィルタ | workflow.nodes.knowledgeRetrieval.metadata.title | Knowledge retrieval node config |

### Knowledge Retrieval Methods

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Vector Search | 向量检索 | ベクトル検索 | dataset.retrieval.semantic_search.title | |
| Full-Text Search | 全文检索 | 全文検索 | dataset.retrieval.full_text_search.title | |
| Hybrid Search | 混合检索 | ハイブリッド検索 | dataset.retrieval.hybrid_search.title | |
| Inverted Index | 倒排索引 | 転置インデックス | dataset.retrieval.invertedIndex.title | |
| Weighted Score | 权重设置 | ウェイト設定 | dataset.weightedScore.title | Rerank strategy option |

### Knowledge Settings

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| External Knowledge Base | 外部知识库 | 外部知識ベース | dataset.externalKnowledgeBase | |
| External API | 外部 API | 外部 API | dataset.externalAPI | |
| Service API | 服务 API | サービスAPI | dataset.serviceApi.title | |
| Multimodal | 多模态 | マルチモーダル | dataset.multimodal | REVIEW: Verify this is user-facing |

### Chunking Mode Labels

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| General | 通用 | 汎用 | dataset.chunkingMode.general | |
| Parent-child | 父子 | 親子 | dataset.chunkingMode.parentChild | |
| Q&A | 问答 | Q&A | dataset.chunkingMode.qa | |
| Graph | 图 | グラフ | dataset.chunkingMode.graph | |
| Full-doc | 全文 | 全体 | dataset.parentMode.fullDoc | Parent chunk mode |
| Paragraph | 段落 | 段落 | dataset.parentMode.paragraph | Parent chunk mode |

### Document Processing

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Index Method | 索引方式 | インデックス方法 | dataset-creation.stepTwo.indexMode | |
| High Quality | 高质量 | 高品質 | dataset-creation.stepTwo.qualified | Index quality level |
| Economical | 经济 | 経済的 | dataset-creation.stepTwo.economical | Index quality level |
| Chunk Settings | 分段设置 | チャンク設定 | dataset-creation.stepTwo.segmentation | |
| Text Pre-processing Rules | 文本预处理规则 | テキストの前処理ルール | dataset-creation.stepTwo.rules | |
| Automatic | 自动分段与清洗 | 自動 | dataset-creation.stepTwo.auto | Processing mode |
| Custom | 自定义 | カスタム | dataset-creation.stepTwo.custom | Processing mode |
| Preview Chunk | 预览块 | チャンクをプレビュー | dataset-creation.stepTwo.previewChunk | |
| Data Source | 选择数据源 | データソース | dataset-creation.steps.one | Wizard step 1 label |
| Document Processing | 文本分段与清洗 | テキスト進行中 | dataset-creation.steps.two | Wizard step 2 label |
| Execute & Finish | 处理并完成 | 実行と完成 | dataset-creation.steps.three | Wizard step 3 label |
| Import from file | 导入已有文本 | テキストファイルからインポート | dataset-creation.stepOne.dataSourceType.file | |
| Sync from Notion | 同步自 Notion 内容 | Notion から同期 | dataset-creation.stepOne.dataSourceType.notion | |
| Sync from website | 同步自 Web 站点 | ウェブサイトから同期 | dataset-creation.stepOne.dataSourceType.web | |

### Document Status Labels

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Enabled | 已启用 | 有効 | dataset-documents.list.status.enabled | |
| Disabled | 已禁用 | 無効 | dataset-documents.list.status.disabled | |
| Archived | 已归档 | アーカイブ済み | dataset-documents.list.status.archived | |
| Available | 可用 | 利用可能 | dataset-documents.list.status.available | |
| Indexing | 索引中 | インデックス化中 | dataset-documents.list.status.indexing | |
| Queuing | 排队中 | キューイング中 | dataset-documents.list.status.queuing | |
| Paused | 已暂停 | 一時停止中 | dataset-documents.list.status.paused | |
| Error | 错误 | エラー | dataset-documents.list.status.error | |

### Document Embedding Modes

| English (UI) | Chinese (UI) | Japanese (UI) | i18n Key | Notes |
|:-------------|:-------------|:--------------|:---------|:------|
| Chunking Setting | 分段模式 | チャンキングモード | dataset-documents.embedding.mode | Section heading |
| High-quality mode | 高质量模式 | 高品質モード | dataset-documents.embedding.highQuality | |
| Economy mode | 经济模式 | 経済モード | dataset-documents.embedding.economy | |

