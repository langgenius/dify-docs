# Translation Prompts

Dify workflow "Auto Translate" 的 prompt 模板本地副本，便于版本控制和 Claude Code 优化。

## 文件对应关系

| 本地文件 | Dify Workflow Node | 触发条件 |
|----------|-------------------|----------|
| `1.md` | Template (1) | 新文档翻译（只有 `the_doc`） |
| `2.md` | Template (2) | 更新翻译（`the_doc` + `the_doc_exist`） |
| `3.md` | Template (3) | 更新翻译 + diff（`the_doc` + `the_doc_exist` + `diff_original`） |

## 工作流程

### 修改 Prompt

1. 编辑本地 `1.md` / `2.md` / `3.md`
2. 复制内容到 Dify workflow 对应的 Template node
3. 测试验证（见下方）
4. 提交到 git

### 测试验证

```bash
cd tools/translate-test-dify
source venv/bin/activate

# 创建测试 spec（示例）
cat > test.md << 'EOF'
# Test

## keys
app-YOUR_API_KEY
Test

## target_languages
zh

## test_file
en/use-dify/getting-started/introduction.mdx

## existing_file
zh/use-dify/getting-started/introduction.mdx

## diff_content
(optional - triggers prompt 3)
EOF

# 运行测试
python run_test.py test.md

# 检查结果
grep -o 'href="[^"]*"' results/*/variant_A/*.md | head -10

# 清理
rm test.md
```

### API 参数

```
必需: original_language, output_language1, the_doc, termbase
可选: the_doc_exist (→ prompt 2), diff_original (→ prompt 3)
```

查看参数: `curl -H "Authorization: Bearer $API_KEY" https://api.dify.ai/v1/parameters`

## 关键规则

所有 prompt 必须包含 **URL Localization** 规则：

```
/en/ → /zh/ (Chinese)
/en/ → /ja/ (Japanese)
plugin-dev-en/ → plugin-dev-zh/ (Chinese)
plugin-dev-en/ → plugin-dev-ja/ (Japanese)
```

## 问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| URL 未映射 `/en/` | prompt 缺少 URL Localization 规则 | 添加 Rule 3 |
| 语言代码错误 | 使用了旧代码 `cn`/`jp` | 改为 `zh`/`ja` |

## 历史修复

- **2024-12**: `1.md` 缺少 URL Localization 规则，`3.md` 语言代码注释错误
