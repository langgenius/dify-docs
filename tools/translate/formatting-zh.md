# Chinese Documentation Formatting Guide

Formatting rules specific to Chinese (zh) translations. These supplement the general formatting guide at `writing-guides/formatting-guide.md`.

---

## CJK-Latin Spacing

Always insert a space between Chinese characters and adjacent Latin letters, numbers, or backticked code.

| Correct | Incorrect |
|:--------|:----------|
| 使用 Docker 部署 | 使用Docker部署 |
| 最大文件大小为 15 MB | 最大文件大小为15MB |
| 设置 `Temperature` 参数 | 设置`Temperature`参数 |
| 支持 3 种模型 | 支持3种模型 |

## Punctuation

Use full-width punctuation in Chinese text:

| Type | Full-width | Half-width (do not use) |
|:-----|:-----------|:------------------------|
| Comma | ， | , |
| Period | 。 | . |
| Colon | ： | : |
| Semicolon | ； | ; |
| Question mark | ？ | ? |
| Exclamation | ！ | ! |
| Parentheses | （） | () |

**Exception:** Use half-width punctuation inside code, URLs, and backticked text.

### Enumeration Comma

Use the enumeration comma `、` (not `，`) to separate parallel items within a sentence.

| Correct | Incorrect |
|:--------|:----------|
| 支持 Workflow、Chatflow、Agent | 支持 Workflow，Chatflow，Agent |
| 包括文本、图片、音频 | 包括文本，图片，音频 |

### Ellipsis

Use the Chinese ellipsis `……` (two full-width ellipsis characters, six dots). Never use `...` (three half-width dots).

Do not combine `……` with `等` in the same phrase.

### Slash

Use a half-width slash `/` (not full-width `／`) to express alternatives between two short items. For three or more parallel items, use `、` instead.

| Correct | Incorrect |
|:--------|:----------|
| 开启/关闭 | 开启／关闭 |
| 支持 Workflow、Chatflow、Agent | 支持 Workflow/Chatflow/Agent |

## Quotation Marks

Use corner bracket quotation marks:

- Single: 「  」
- Double (nested): 『  』

## Emphasis

Do not use italic emphasis (`*text*`) in Chinese text. CJK italic rendering is poor in most fonts. Use bold (`**text**`) instead when emphasis is needed.

When bold text is adjacent to Chinese characters, insert a space on each side:

| Correct | Incorrect |
|:--------|:----------|
| 点击 **发布** 使应用可用 | 点击**发布**使应用可用 |
| 前往 **工具** 或 **插件** | 前往**工具**或**插件** |
| 以 **高质量** 模式索引 | 以**高质量**模式索引 |

No space is needed when bold text is adjacent to punctuation or the start of a line.

## Links

When link text is adjacent to Chinese characters, insert a space on each side:

| Correct | Incorrect |
|:--------|:----------|
| 详见 [环境变量](/path) 了解更多 | 详见[环境变量](/path)了解更多 |
| 请参考 [API 文档](/path) | 请参考[API 文档](/path) |

No space is needed when link text is adjacent to punctuation.

For cross-links to other documentation pages, change the `/en/` path prefix in the English source to `/zh/`.

## Numbers

- Use Arabic numerals (1, 2, 3), not Chinese numerals (一、二、三), for
  technical content.
- Use half-width numbers even in Chinese text.
- Use `～` (full-width tilde) for numeric ranges, not hyphens or en dashes.
- No space before `%` or `°`.

| Correct | Incorrect |
|:--------|:----------|
| 第 10～15 页 | 第 10-15 页 |
| 15% | 15 % |

## Headings

Do not end headings with sentence-ending punctuation (`。，、；：`). Paired marks like quotation marks and parentheses are acceptable.

## Lists

- If list items are complete sentences, end each with `。`.
- If list items are short phrases or fragments, omit trailing punctuation.
- Never mix the two styles within a single list.

## Translatable Elements

These elements must be translated, not left in English:

- **Tab titles:** `<Tab title="...">` values must use the Chinese UI label from the glossary.
- **Frame captions and image alt text:** Translate both `<Frame caption="...">` and `![alt text]`.
- **Bold UI labels:** When a UI label appears in **bold**, use the official Chinese translation from `web/i18n/zh-Hans/`. Refer to the glossary.
- **Prompt examples:** Translate natural language text inside code blocks. Keep variable placeholders (`{{variable_name}}`) unchanged.
- **Cross-reference heading anchors:** When a link includes `#heading-slug`, update the slug to match the translated heading.

## Em Dashes

Avoid using `——` in Chinese text. Restructure instead:

| Instead of | Use |
|:-----------|:----|
| A——B——C | A，即 B，C（parenthetical alternative） |
| 如数据库、文件系统——使其可访问 | 如数据库、文件系统，使其可访问 |

## Translation Quality

Avoid these common issues in EN→ZH translation:

- **Passive voice retention:** Prefer active voice. Write `已启用该功能` instead of `该功能已被启用`.
- **Translationese (翻译腔):** Avoid overuse of `的`, `被`, `和`, and long modifier chains before nouns. Break into shorter clauses.
- **Half-width punctuation leakage:** Ensure all Chinese punctuation is full-width; do not carry over half-width commas or periods from the English source.
