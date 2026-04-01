# Japanese Documentation Formatting Guide

Formatting rules specific to Japanese (ja) translations. These supplement the general formatting guide at `writing-guides/formatting-guide.md`.

---

## CJK-Latin Spacing

Insert a space between Japanese characters and adjacent Latin letters, numbers, or backticked code—same principle as Chinese.

| Correct | Incorrect |
|:--------|:----------|
| Docker を使用 | Dockerを使用 |
| 最大 15 MB | 最大15MB |
| `Temperature` パラメータ | `Temperature`パラメータ |

## Punctuation

Use full-width punctuation in Japanese text:

| Type | Full-width | Half-width (do not use) |
|:-----|:-----------|:------------------------|
| Comma | 、 | , |
| Period | 。 | . |
| Middle dot | ・ | · |
| Parentheses | （） | () |

**Exception:** Use half-width punctuation inside code, URLs, and backticked text.

## Katakana Conventions

Use katakana for foreign loanwords and technical terms that have established katakana equivalents. Refer to the glossary for standard translations.

When a loanword ending in "-er", "-or", "-ar" is written in katakana, follow the Microsoft Language Portal convention: include the trailing long vowel mark (ー) for words of 3 morae or fewer, omit it for longer words.

| English | Katakana |
|:--------|:---------|
| server | サーバー |
| parameter | パラメータ |
| provider | プロバイダー |

## Emphasis

Do not use italic emphasis (`*text*`) in Japanese text. CJK italic rendering is poor in most fonts. Use bold (`**text**`) instead when emphasis is needed.

## Numbers

- Use Arabic numerals, not kanji numerals, for technical content.
- Use half-width numbers even in Japanese text.
