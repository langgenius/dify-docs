# Dify 文档工具脚本

此目录包含用于Dify文档维护的实用工具脚本。

## 可用脚本

### 1. 修复Markdown链接 (fix_markdown_links.py)

此脚本用于自动修复Markdown文件中的相对路径引用，以符合Mintlify文档格式要求。它会：

- 移除.md和.mdx文件后缀
- 为同级目录文件引用添加./前缀
- 正确处理相对路径和锚点

#### 使用方法

```bash
# 确保脚本有执行权限
chmod +x scripts/fix_markdown_links.py

# 处理整个文档目录
./scripts/fix_markdown_links.py /Users/allen/Documents/dify-docs-mintlify

# 或者处理特定子目录
./scripts/fix_markdown_links.py /Users/allen/Documents/dify-docs-mintlify/zh-hans
```

也可以不设置执行权限，直接使用Python运行：

```bash
python scripts/fix_markdown_links.py [directory]
```

如果不提供目录参数，将使用当前工作目录。

### 2. 交互式链接修复工具 (fix_links_interactive.py)

这是一个高度交互式的工具，用于精确控制Markdown文件中的链接修复过程。该工具支持：

- 单文件或目录处理
- 修改预览
- 选择性应用修改
- 将相对路径转换为绝对路径 (/zh-hans/xxx 格式)
- 交互式确认每个文件和修改

#### 使用方法

```bash
# 确保脚本有执行权限
chmod +x scripts/fix_links_interactive.py

# 运行交互式工具
./scripts/fix_links_interactive.py
```

也可以不设置执行权限，直接使用Python运行：

```bash
python scripts/fix_links_interactive.py
```

脚本会引导你完成所有步骤，包括：
1. 选择处理单个文件或整个目录
2. 输入文件或目录路径
3. 预览修改内容
4. 确认修改
