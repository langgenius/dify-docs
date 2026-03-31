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

## Quotation Marks

Use corner bracket quotation marks:

- Single: 「  」
- Double (nested): 『  』

## Emphasis

Do not use italic emphasis (`*text*`) in Chinese text. CJK italic rendering is poor in most fonts. Use bold (`**text**`) instead when emphasis is needed.

## Numbers

- Use Arabic numerals (1, 2, 3), not Chinese numerals (一、二、三), for
  technical content.
- Use half-width numbers even in Chinese text.
