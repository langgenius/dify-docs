# Terminology Database

## General Terms

### Core Concepts

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Workflow | 工作流 | ワークフロー |
| Chatflow | 对话流 | チャットフロー |
| Agent | Agent | Agent |
| Text Generator | 文本生成应用 | テキストジェネレーター |
| Agent app | Agent 应用 | エージェントアプリ |
| knowledge base | 知识库 | ナレッジベース |
| plugin | 插件 | プラグイン |
| Dify tool | Dify 工具 | ツール |
| workspace | 工作区 | ワークスペース |
| template | 模板 | テンプレート |
| WebApp | WebApp | WebApp |

### Models

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| model | 模型 | モデル |
| model provider | 模型供应商 | モデルプロバイダー |
| LLM (large language model) | 大语言模型 | 大規模言語モデル |
| chat model | 对话模型 | チャットモデル |
| completion model | 文本续写模型 | 補完モデル |
| embedding model | 嵌入模型 | 埋め込みモデル |
| text embedding model | 文本嵌入模型 | テキスト埋め込みモデル |
| multimodal embedding model | 多模态嵌入模型 | マルチモーダル埋め込みモデル |
| rerank model | 重排序模型 | リランクモデル |
| reasoning model | 推理模型 | 推論モデル |
| moderation model | 内容审核模型 | モデレーションモデル |
| TTS model | 文字转语音模型 | TTSモデル |
| Speech2Text model | 语音转文字模型 | 音声認識モデル |
| token | token | token |
| API token | API 令牌 | APIトークン |
| prompt | 提示词 | プロンプト |
| system instruction | 系统指令 | システムインストラクション |
| user message | User 消息 | ユーザーメッセージ |
| assistant message | Assistant 消息 | アシスタントメッセージ |
| model tag | 模型标签 | モデルタグ |

### Nodes

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| node | 节点 | ノード |
| User Input | 用户输入 | ユーザー入力 |
| Output | 输出 | 出力 |
| Answer | 直接回复 | 回答 |
| LLM | LLM | LLM |
| Knowledge Retrieval | 知识检索 | ナレッジ検索 |
| Question Classifier | 问题分类器 | 質問分類器 |
| IF/ELSE | 条件分支 | IF/ELSE |
| Code | 代码执行 | コード実行 |
| Template | 模板转换 | テンプレート |
| HTTP Request | HTTP 请求 | HTTP リクエスト |
| Variable Aggregator | 变量聚合器 | 変数集約器 |
| Variable Assigner | 变量赋值器 | 変数代入器 |
| Tool | 工具 | ツール |
| Parameter Extractor | 参数提取器 | パラメータ抽出 |
| Iteration | 迭代 | イテレーション |
| Loop | 循环 | ループ |
| Doc Extractor | 文档提取器 | テキスト抽出 |
| List Operator | 列表操作 | リスト処理 |
| Agent | Agent | エージェント |
| Human Input | 人工介入 | 人間の入力 |
| Schedule Trigger | 定时触发器 | スケジュールトリガー |
| Webhook Trigger | Webhook 触发器 | Webhook トリガー |
| Plugin Trigger | 插件触发器 | プラグイントリガー |
| Command | 命令 | コマンド |
| Upload File to Sandbox | 上传文件至沙盒 | サンドボックスへのファイルアップロード |

### Knowledge & Retrieval

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| knowledge base | 知识库 | ナレッジベース |
| chunk | 分段 | チャンク |
| chunking | 分段 | チャンキング |
| retrieval | 检索 | 検索 |
| retrieval mode | 检索模式 | 検索モード |
| indexing | 索引 | インデックス |
| index method | 索引方法 | インデックス方法 |
| embedding | 嵌入 | 埋め込み |
| metadata | 元数据 | メタデータ |
| delimiter | 分隔符 | デリミタ |
| maximum chunk length | 最大分段长度 | 最大チャンク長 |
| chunk overlap | 分段重叠 | チャンクオーバーラップ |
| General mode | 通用模式 | 汎用モード |
| Parent-child mode | 父子模式 | 親子モード |
| parent chunk | 父分段 | 親チャンク |
| child chunk | 子分段 | 子チャンク |
| Paragraph mode | 段落模式 | 段落モード |
| Full Doc mode | 全文档模式 | 全文書モード |
| pre-processing | 预处理 | 前処理 |
| Summary Auto-Gen | 摘要自动生成 | 要約自動生成 |
| Top K | Top K | Top K |
| score threshold | 分数阈值 | スコアしきい値 |

### Configuration & Parameters

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| variable | 变量 | 変数 |
| environment variable | 环境变量 | 環境変数 |
| Top P | Top P | Top P |
| context variable | 上下文变量 | コンテキスト変数 |
| conversation memory | 对话记忆 | 会話メモリ |
| window size | 窗口大小 | ウィンドウサイズ |
| structured output | 结构化输出 | 構造化出力 |
| input field | 输入字段 | 入力フィールド |
| request form | 请求表单 | リクエストフォーム |
| Assemble Variable | 变量组装 | 変数アセンブル |

### Agent

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Max Iterations | 最大迭代次数 | 最大イテレーション数 |

### Infrastructure

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| self-hosted | 自托管 | セルフホスト |
| SaaS | SaaS | SaaS |
| Docker | Docker | Docker |
| sandbox | 沙箱 | サンドボックス |
| API | API | API |
| runtime | 运行时 | ランタイム |
| classic runtime | 经典运行时 | クラシックランタイム |
| sandboxed runtime | 沙盒运行时 | サンドボックスランタイム |
| skill | 技能 | スキル |
| file system | 文件系统 | ファイルシステム |

### Marketplace

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Marketplace | 市场 | マーケットプレイス |
| Creator Center | 创作者中心 | クリエイターセンター |

## UI Labels

### Sidebar & Navigation

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Studio | 工作室 | スタジオ |
| Knowledge | 知识库 | ナレッジ |
| Explore | 探索 | 探索 |
| Plugins | 插件 | プラグイン |
| Tools | 工具 | ツール |

### App Detail Tabs

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Orchestrate | 编排 | オーケストレート |
| Monitoring | 监测 | 監視 |
| API Access | 访问 API | API アクセス |
| Logs & Annotations | 日志与标注 | ログ＆注釈 |

### Knowledge Detail Tabs

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Documents | 文档 | ドキュメント |
| Retrieval Testing | 召回测试 | 検索テスト |
| Settings | 设置 | 設定 |
| Pipeline | 流水线 | パイプライン |

### Settings Panel

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| My account | 我的账户 | マイアカウント |
| Members | 成员 | メンバー |
| Model Provider | 模型供应商 | モデルプロバイダー |
| Data Source | 数据来源 | データソース |
| API Extension | API 扩展 | API 拡張 |
| Billing | 账单 | 請求 |
| Integrations | 集成 | 統合 |
| Default Model Settings | 默认模型设置 | デフォルトモデル設定 |
| System Reasoning Model | 系统推理模型 | システム推論モデル |
| Embedding Model | Embedding 模型 | 埋め込みモデル |
| Rerank Model | Rerank 模型 | Rerank モデル |
| Speech-to-Text Model | 语音转文本模型 | 音声-to-テキストモデル |
| Text-to-Speech Model | 文本转语音模型 | テキスト-to-音声モデル |
| Load Balancing | 负载均衡 | 負荷分散 |
| AI Credits | AI Credits | AI クレジット |
| Usage Priority | 使用优先级 | 利用優先度 |
| API Key | API 密钥 | API キー |

### Workspace Roles

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Owner | 所有者 | オーナー |
| Admin | 管理员 | 管理者 |
| Editor | 编辑 | エディター |
| Builder | 构建器 | ビルダー |
| Knowledge Admin | 知识库管理员 | ナレッジ管理員 |
| Normal | 成员 | 通常 |

### App Type Selectors

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Assistant | 助手 | アシスタント |
| Chatbot | 聊天助手 | チャットボット |
| Chatflow | Chatflow | チャットフロー |
| Completion | 文本生成 | テキスト生成 |

### App Actions

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Duplicate | 复制 | 複製 |
| Export DSL | 导出 DSL | DSL をエクスポート |
| Import DSL file | 导入 DSL 文件 | DSL ファイルをインポート |
| Create from Blank | 创建空白应用 | 最初から作成 |
| Create from Template | 从应用模板创建 | テンプレートから作成 |
| Tracing | 追踪 | 追跡 |
| Web App Access Control | Web 应用访问控制 | Web アプリアクセス制御 |

### Workflow Node Names

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| User Input | 用户输入 | ユーザー入力 |
| LLM | LLM | LLM |
| Knowledge Retrieval | 知识检索 | 知識検索 |
| IF/ELSE | 条件分支 | IF/ELSE |
| Code | 代码执行 | コード実行 |
| Template | 模板转换 | テンプレート |
| Question Classifier | 问题分类器 | 質問分類器 |
| HTTP Request | HTTP 请求 | HTTP リクエスト |
| Variable Aggregator | 变量聚合器 | 変数集約器 |
| Variable Assigner | 变量赋值 | 変数代入 |
| Iteration | 迭代 | イテレーション |
| Loop | 循环 | ループ |
| Parameter Extractor | 参数提取器 | パラメータ抽出 |
| Doc Extractor | 文档提取器 | テキスト抽出 |
| List Operator | 列表操作 | リスト処理 |
| Output | 输出 | 出力 |
| Answer | 直接回复 | 回答 |
| Human Input | 人工介入 | 人間の入力 |
| Webhook Trigger | Webhook 触发器 | Webhook トリガー |
| Schedule Trigger | 定时触发器 | スケジュールトリガー |
| Plugin Trigger | 插件触发器 | プラグイントリガー |
| Knowledge Base | 知识库 | 知識ベース |

### Workflow Controls

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Publish | 发布 | 公開する |
| Published | 已发布 | 公開済み |
| Unpublished | 未发布 | 未公開 |
| Preview | 预览 | プレビュー |
| Test Run | 测试运行 | テスト実行 |
| Run App | 运行 | アプリを実行 |
| Features | 功能 | 機能 |
| Version History | 版本历史 | バージョン履歴 |
| Workflow as Tool | 发布为工具 | ワークフローをツールとして公開する |
| Embed Into Site | 嵌入网站 | サイトに埋め込む |
| Conversation Variables | 会话变量 | 会話変数 |
| Environment Variables | 环境变量 | 環境変数 |
| System Variables | 系统变量 | システム変数 |

### Agent Node Config

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Agentic Strategy | Agent 策略 | エージェンティック戦略 |
| Query Variable | 查询变量 | 検索変数 |
| Metadata Filtering | 元数据过滤 | メタデータフィルタ |

### Knowledge Retrieval Methods

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Vector Search | 向量检索 | ベクトル検索 |
| Full-Text Search | 全文检索 | 全文検索 |
| Hybrid Search | 混合检索 | ハイブリッド検索 |
| Inverted Index | 倒排索引 | 転置インデックス |
| Weighted Score | 权重设置 | ウェイト設定 |

### Knowledge Settings

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| External Knowledge Base | 外部知识库 | 外部知識ベース |
| External API | 外部 API | 外部 API |
| Service API | 服务 API | サービスAPI |
| Multimodal | 多模态 | マルチモーダル |

### Chunking Mode Labels

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| General | 通用 | 汎用 |
| Parent-child | 父子 | 親子 |
| Q&A | 问答 | Q&A |
| Graph | 图 | グラフ |
| Full-doc | 全文 | 全体 |
| Paragraph | 段落 | 段落 |

### Document Processing

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Index Method | 索引方式 | インデックス方法 |
| High Quality | 高质量 | 高品質 |
| Economical | 经济 | 経済的 |
| Chunk Settings | 分段设置 | チャンク設定 |
| Text Pre-processing Rules | 文本预处理规则 | テキストの前処理ルール |
| Automatic | 自动分段与清洗 | 自動 |
| Custom | 自定义 | カスタム |
| Preview Chunk | 预览块 | チャンクをプレビュー |
| Data Source | 选择数据源 | データソース |
| Document Processing | 文本分段与清洗 | テキスト進行中 |
| Execute & Finish | 处理并完成 | 実行と完成 |
| Import from file | 导入已有文本 | テキストファイルからインポート |
| Sync from Notion | 同步自 Notion 内容 | Notion から同期 |
| Sync from website | 同步自 Web 站点 | ウェブサイトから同期 |

### Document Status Labels

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Enabled | 已启用 | 有効 |
| Disabled | 已禁用 | 無効 |
| Archived | 已归档 | アーカイブ済み |
| Available | 可用 | 利用可能 |
| Indexing | 索引中 | インデックス化中 |
| Queuing | 排队中 | キューイング中 |
| Paused | 已暂停 | 一時停止中 |
| Error | 错误 | エラー |

### Document Embedding Modes

| English | Chinese | Japanese |
|:--------|:--------|:---------|
| Chunking Setting | 分段模式 | チャンキングモード |
| High-quality mode | 高质量模式 | 高品質モード |
| Economy mode | 经济模式 | 経済モード |

## General Guidelines

Technical accuracy, English identifiers preserved, markdown formatting
maintained, professional tone.
