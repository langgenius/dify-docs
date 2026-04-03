# Japanese Documentation Formatting Guide

Formatting rules specific to Japanese (ja) translations. These supplement the general formatting guide at `writing-guides/formatting-guide.md`.

Primary references: [JTF Style Guide v3.0](https://www.jtf.jp/tips/styleguide), [Microsoft Japanese Localization Style Guide](https://learn.microsoft.com/en-us/globalization/reference/microsoft-style-guides).

---

## Writing Style

Use **敬体 (です/ます form)** throughout body text. Never mix 敬体 and 常体 within a page.

| Context | Style | Example |
|:--------|:------|:--------|
| Body text | 敬体 (です/ます) | Docker を使用してデプロイします |
| Headings | Noun phrase | プロンプトの作成 |
| Table cells | 常体 or noun phrase | 設定する / 設定 |
| Bullet lists | Consistent within each list | See [Lists](#lists) |

## CJK-Latin Spacing

Insert a space between Japanese characters and adjacent Latin letters, numbers, or backticked code—same principle as Chinese.

| Correct | Incorrect |
|:--------|:----------|
| Docker を使用 | Dockerを使用 |
| 最大 15 MB | 最大15MB |
| `Temperature` パラメータ | `Temperature`パラメータ |
| 3 つのノード | 3つのノード |

This rule also applies before Japanese particles (を、は、が、の、に、で、と) when they follow Latin text.

## Punctuation

Use full-width punctuation in Japanese text:

| Type | Full-width | Half-width (do not use) |
|:-----|:-----------|:------------------------|
| Comma | 、 | , |
| Period | 。 | . |
| Middle dot | ・ | · |
| Parentheses | （） | () |

**Exception:** Use half-width punctuation inside code, URLs, and backticked text.

## Brackets

| Bracket | Usage |
|:--------|:------|
| 「」 | Quoting UI labels, user input, or short phrases in prose |
| （） | Supplementary explanation or clarification, e.g., ナレッジベース（knowledge base） |
| 【】 | Strong visual emphasis in headings or labels; rare in body text |

## Emphasis

Do not use italic emphasis (`*text*`) in Japanese text. CJK italic rendering is poor in most fonts. Use bold (`**text**`) instead when emphasis is needed.

When bold text is adjacent to Japanese characters, insert a space on each side:

| Correct | Incorrect |
|:--------|:----------|
| サイドバーの **Studio** タブ | サイドバーの**Studio**タブ |
| **高品質** モードで索引 | **高品質**モードで索引 |
| **公開する** をクリック | **公開する**をクリック |

No space is needed when bold text is adjacent to punctuation or the start of a line.

## Links

For cross-links to other documentation pages, change the `/en/` path prefix in the English source to `/ja/`.

## Katakana Conventions

Use katakana for foreign loanwords and technical terms that have established katakana equivalents. Refer to the glossary for standard translations.

When a loanword ending in "-er", "-or", "-ar" is written in katakana, follow the Microsoft Language Portal convention: include the trailing long vowel mark (ー) for words of 3 morae or fewer, omit it for longer words.

| English | Katakana |
|:--------|:---------|
| server | サーバー |
| parameter | パラメータ |
| provider | プロバイダー |

### Middle Dot (・)

Use ・ to separate katakana words **only** when needed for readability:

- **Established compound terms:** No middle dot. Follow the glossary.
  e.g., ワークフロー, ナレッジベース, テキストジェネレーター, モデルプロバイダー
- **Three or more words where boundaries are unclear:** Use middle dot.
  e.g., ケース・バイ・ケース
- **Proper noun + common noun:** Use middle dot.

## Numbers

- Use Arabic numerals, not kanji numerals, for technical content.
- Use half-width numbers even in Japanese text.

## Full-Width vs Half-Width

- **Numbers:** Always half-width (1, 2, 3). Never full-width (１, ２, ３).
- **Latin letters:** Always half-width (A, B, C). Never full-width (Ａ, Ｂ, Ｃ).
- **Spaces:** Always half-width. Never use full-width spaces (　).
- **Punctuation:** Full-width for Japanese punctuation; half-width inside code and URLs.

## Headings

Use noun phrases for headings, not full sentences.

| Correct | Incorrect |
|:--------|:----------|
| プロンプトの作成 | プロンプトを作成します |
| 検索設定 | 検索設定について |

## Lists

All items in a list must use the same grammatical ending. Choose one pattern per list:

| Pattern | Example |
|:--------|:--------|
| Noun/noun phrase (concise) | Docker のインストール |
| Plain verb (常体) | Docker をインストールする |
| Polite verb (敬体) | Docker をインストールします |

Never mix these within a single list.

## Sentence Length

Aim for **50 characters or fewer** per sentence. Sentences beyond 80 characters should be split. If a sentence has more than one に/は/が clause, it likely needs splitting.

## Honorifics

Use minimal honorifics. Be polite but not overly formal.

| Recommended | Avoid |
|:------------|:------|
| 確認してください | ご確認ください |
| 参照してください | ご参照ください |
| 入力してください | ご入力ください |

**Exception:** ご利用 is idiomatic and reads naturally (e.g., ご利用のブラウザ).

## Translatable Elements

These elements must be translated, not left in English:

- **Tab titles:** `<Tab title="...">` values must use the Japanese UI label from the glossary.
- **Frame captions and image alt text:** Translate both `<Frame caption="...">` and `![alt text]`.
- **Bold UI labels:** When a UI label appears in **bold**, use the official Japanese translation from `web/i18n/ja-JP/`. Refer to the glossary.
- **Prompt examples:** Translate natural language text inside code blocks (using です/ます form). Keep variable placeholders (`{{variable_name}}`) unchanged.
- **Cross-reference heading anchors:** When a link includes `#heading-slug`, update the slug to match the translated heading.

## Em Dashes

Avoid using `—` or `——` in Japanese text. Restructure instead:

| Instead of | Use |
|:-----------|:----|
| A—B—C | A、つまり B。C |
| データベース、ファイルシステム—これらを | データベースやファイルシステムなどを |

## Translation Quality

Avoid these common issues in EN→JA translation:

- **Missing CJK-Latin spaces.** The most visible quality signal. Missing spaces immediately mark output as machine-translated.
- **Literal English syntax.** Restructure English relative clauses and long modifier chains into natural Japanese clause order.
- **Inconsistent terminology.** Always follow the glossary. Do not alternate between different translations of the same term.
- **Over-translation.** Brand names, feature names, API parameter names, and code identifiers must remain in English.
- **Passive voice overuse.** Japanese prefers active constructions. Avoid literal passive translations (〜される) when an active form is more natural.
- **Register mixing.** Never mix です/ます and だ/である within a single page.
