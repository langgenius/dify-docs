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

**Exception:** No space between two adjacent punctuation marks. Punctuation includes full-width CJK marks (。、，；：）, backticks, and markdown brackets (`[`, `]`, `(`, `)`).

| Correct | Incorrect |
|:--------|:----------|
| 默认为 `"untitled"`。 | 默认为 `"untitled"` 。 |
| `"page"`、`"database"` | `"page"` 、 `"database"` |
| 详见（[链接](/path)）。 | 详见（ [链接](/path) ）。 |
| 返回。`streaming` 模式 | 返回。 `streaming` 模式 |

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

### API Reference Cross-Links

In OpenAPI spec descriptions, cross-links use the pattern `/api-reference/{tag-kebab}/{summary-kebab}`. When translating, replace both the tag and summary segments with their translated equivalents from the target language's spec.

| English | Chinese |
|:--------|:--------|
| `/api-reference/knowledge-pipeline/upload-pipeline-file` | `/api-reference/知识流水线/上传流水线文件` |

The translated tag and summary must match the `tags` and `summary` fields in the corresponding endpoint of the zh OpenAPI spec.

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
## Cross-Reference Anchors

When a link includes `#slug`, the slug must match the **translated** text, not the English original. Mintlify generates slugs from the source text, so an untranslated anchor will break the link. This applies to both heading anchors and Tab title anchors (`<Tab title="...">` values).

| English source | Chinese translation |
|:---------------|:--------------------|
| `external-knowledge-api#response` | `external-knowledge-api#响应` |
| `setting-indexing-methods#setting-the-retrieval-setting` | `setting-indexing-methods#指定检索设置` |

## Em Dashes

Avoid using `——` in Chinese text. Restructure instead:

| Instead of | Use |
|:-----------|:----|
| A——B——C | A，即 B，C（parenthetical alternative） |
| 如数据库、文件系统——使其可访问 | 如数据库、文件系统，使其可访问 |

## Translation Quality

### Translate Meaning, Not Structure

The single most important rule: after understanding what an English sentence says, write the Chinese from scratch as if you were writing it natively. Do not preserve English clause order, modifier chains, or connector words just because they appear in the source. Fidelity to natural Chinese always outranks fidelity to English structure.

Before finalizing any sentence, ask: "Would a Chinese technical writer actually write this?" If the answer is no, rewrite.

### Patterns to Eliminate

These constructions immediately mark output as machine-translated. Eliminate them whenever possible:

| English source | Translationese (avoid) | Natural Chinese |
|:---------------|:-----------------------|:----------------|
| If your team maintains its own RAG system, you can connect... | 如果你的团队维护着自己的 RAG 系统，你可以将... | 团队自建 RAG 系统时，可将... |
| This lets your AI applications retrieve information directly | 这让你的 AI 应用能够直接检索信息 | AI 应用即可直接检索信息 |
| When your application runs, Dify sends... | 当你的应用运行时，Dify 会发送... | 应用运行时，Dify 发送... |
| You can connect these external sources to Dify | 你可以将这些外部知识源连接到 Dify | 可将这些外部知识源连接到 Dify |
| The API service you registered | 你已注册的 API 服务 | 已注册的 API 服务 |

Specific words to drop or shorten when context allows:

- **Drop redundant 「你的」 only when ownership is unambiguously clear and the sentence subject doesn't shift.** Keep 「你/你的」 when: the subject of the current clause differs from the previous one; without it the referent could be misread; or the sentence describes an action the reader performs. Over-dropping creates ambiguity—when in doubt, keep it.
- **Drop 「会」** in present-tense system behavior descriptions. `Dify 发送请求` is cleaner than `Dify 会发送请求`.
- **Drop 「当...时」** wrappers around simple time clauses. `应用运行时` is cleaner than `当应用运行时`.
- **Replace 「能够」 with 「能」 or just the verb.** 「让...可以」 chains should be restructured with 「即可」 or rewritten.
- **Default to 「可」 over 「可以」.** Use `可以` only when `可` causes ambiguity or sounds unnatural.

| Instead of | Use |
|:-----------|:----|
| 多个知识库可以共享同一个 API | 多个知识库可共享同一个 API |
| 你可以参考其源代码 | 你可参考其源代码 |
| 你可以选择在 JSON 中返回 | 你可选择在 JSON 中返回 |

### Other Quality Issues

- **Passive voice retention:** Prefer active voice. Write `已启用该功能` instead of `该功能已被启用`.
- **Translationese (翻译腔):** Avoid overuse of `的`, `被`, `和`, and long modifier chains before nouns. Break into shorter clauses.
- **Half-width punctuation leakage:** Ensure all Chinese punctuation is full-width; do not carry over half-width commas or periods from the English source.

### Standard Phrase Translations

| English | Chinese |
|:--------|:--------|
| See xx for details / for more information | 详见 xx |
