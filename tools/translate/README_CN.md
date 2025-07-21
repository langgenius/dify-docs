# 自动翻译文档

基于 GitHub Actions 和 Dify AI 的文档自动翻译系统，支持英文、中文、日文三语互译。

> **其他语言**: [English](README_EN.md) | [日本語](README_JA.md)

## 工作原理

1. **触发条件**: 推送到非 main 分支时自动运行
2. **智能检测**: 自动识别修改的 `.md/.mdx` 文件并判断源语言
3. **翻译逻辑**:
    - ✅ 翻译新增文档到其他语言
    - ❌ 跳过已存在的翻译文件（避免覆盖手动修改）
4. **自动提交**: 翻译结果自动推送到当前分支

## 系统特性

- 🌐 **多语言支持**: 基于配置的语言映射，理论上支持任意语言扩展
- 📚 **术语表一致性**: 内置专业术语库，LLM 智能遵循术语表确保技术词汇翻译统一
- 🔄 **并发处理**: 智能并发控制，同时翻译多个目标语言
- 🛡️ **容错机制**: 3 次重试机制，指数退避策略
- ⚡ **增量翻译**: 只处理变更文件，避免重复工作
- 🧠 **高性能模型**: 使用性能较强的 LLM 模型确保翻译质量

## 使用方法

### 文档编写者

1. 在任意语言目录下编写/修改文档
2. 推送到分支（非 main）
3. 等待 0.5-1 分钟自动翻译完成
4. **查看翻译结果**:
    - 创建 Pull Request 进行本地查看和后续编辑
    - 或在 GitHub 查看 Actions 推送的 commit 详情，直接审查翻译质量

### 支持的语言目录

- **通用文档**: `en/` ↔ `zh-hans/` ↔ `ja-jp/`
- **插件开发文档**: `plugin-dev-en/` ↔ `plugin-dev-zh/` ↔ `plugin-dev-ja/`

注：系统架构支持扩展更多语言，只需修改配置文件

## 注意事项

- 系统只翻译新文档，不会覆盖已存在的翻译
- 如需更新现有翻译，请手动删除目标文件后重新触发
- 术语翻译遵循 `termbase_i18n.md` 中的专业词汇表，LLM 具备智能术语识别能力
- 翻译质量依赖于配置的高性能模型，建议在 Dify Studio 中使用性能较强的基座模型

### 系统配置

#### 术语表

编辑 `tools/translate/termbase_i18n.md` 更新专业术语翻译对照表。

#### 翻译模型

访问 Dify Studio 调整翻译 prompt 或更换基座模型。

---

---

---

## 🔧 开发和部署配置

### 本地开发环境

#### 1. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

#### 2. 安装依赖

```bash
pip install -r tools/translate/requirements.txt
```

#### 3. 配置 API 密钥

在 `tools/translate/` 目录下创建 `.env` 文件：

```bash
DIFY_API_KEY=your_dify_api_key_here
```

#### 4. 运行翻译

```bash
# 交互模式（推荐新手使用）
python tools/translate/main.py

# 命令行模式（指定文件）
python tools/translate/main.py path/to/file.mdx [DIFY_API_KEY]
```

> **提示**: 在 IDE 中右键选择"复制相对路径"作为参数传入

### 部署到其他仓库

1. **复制文件**:

    - `.github/workflows/translate.yml`
    - `tools/translate/` 整个目录

2. **配置 GitHub Secrets**:

    - Repository Settings → Secrets and variables → Actions
    - 添加 `DIFY_API_KEY` 密钥

3. **测试**: 在分支中修改文档，验证自动翻译功能

### 技术细节

- 并发翻译限制为 2 个任务，避免 API 压力过大
- 支持 `.md` 和 `.mdx` 文件格式
- 基于 Dify API 的 workflow 模式

## TODO

- [ ] 支持更新现有翻译
