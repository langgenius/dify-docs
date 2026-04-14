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

**Exception:** No space between two adjacent punctuation marks. Punctuation includes full-width CJK marks (。、：）, backticks, and markdown brackets (`[`, `]`, `(`, `)`).

| Correct | Incorrect |
|:--------|:----------|
| `"page"`、`"database"` | `"page"` 、 `"database"` |
| 参照（[リンク](/path)）。 | 参照（ [リンク](/path) ）。 |
| です。`streaming` モード | です。 `streaming` モード |

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

When link text is adjacent to Japanese characters, insert a space on each side:

| Correct | Incorrect |
|:--------|:----------|
| 詳細は [環境変数](/path) を参照してください | 詳細は[環境変数](/path)を参照してください |
| 代わりに [回答](/path) ノードを使用 | 代わりに[回答](/path)ノードを使用 |

No space is needed when link text is adjacent to punctuation.

For cross-links to other documentation pages, change the `/en/` path prefix in the English source to `/ja/`.

### API Reference Cross-Links

In OpenAPI spec descriptions, cross-links use the pattern `/api-reference/{tag-kebab}/{summary-kebab}`. When translating, replace both the tag and summary segments with their translated equivalents from the target language's spec.

| English | Japanese |
|:--------|:---------|
| `/api-reference/knowledge-pipeline/upload-pipeline-file` | `/api-reference/ナレッジパイプライン/パイプラインファイルをアップロード` |

The translated tag and summary must match the `tags` and `summary` fields in the corresponding endpoint of the ja OpenAPI spec.

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
## Cross-Reference Anchors

When a link includes `#slug`, the slug must match the **translated** text, not the English original. Mintlify generates slugs from the source text, so an untranslated anchor will break the link. This applies to both heading anchors and Tab title anchors (`<Tab title="...">` values).

| English source | Japanese translation |
|:---------------|:---------------------|
| `external-knowledge-api#response` | `external-knowledge-api#レスポンス` |
| `setting-indexing-methods#setting-the-retrieval-setting` | `setting-indexing-methods#検索設定の指定` |

## Em Dashes

Avoid using `—` or `——` in Japanese text. Restructure instead:

| Instead of | Use |
|:-----------|:----|
| A—B—C | A、つまり B。C |
| データベース、ファイルシステム—これらを | データベースやファイルシステムなどを |

## Translation Quality

### Translate Meaning, Not Structure

The single most important rule: after understanding what an English sentence says, write the Japanese from scratch as if you were writing it natively. Do not preserve English clause order, modifier chains, or connector words just because they appear in the source. Fidelity to natural Japanese always outranks fidelity to English structure.

Before finalizing any sentence, ask: "Would a Japanese technical writer actually write this?" If the answer is no, rewrite.

### Patterns to Eliminate

These constructions immediately mark output as machine-translated:

| English source | Translationese (avoid) | Natural Japanese |
|:---------------|:-----------------------|:-----------------|
| If your team maintains its own RAG system, you can connect... | あなたのチームが独自の RAG システムを維持している場合、接続できます... | 自社で RAG システムを運用している場合、接続できます... |
| When your application runs, Dify sends... | アプリケーションが実行されるとき、Dify は送信します | アプリケーション実行時、Dify は送信します |
| You can connect these external sources to Dify | あなたはこれらの外部ソースを Dify に接続することができます | これらの外部ソースを Dify に接続できます |
| The API service you registered | あなたが登録した API サービス | 登録した API サービス |

Specific patterns to drop or shorten when context allows:

- **Drop redundant 「あなたの／あなたが」 only when ownership is unambiguously clear.** Japanese naturally omits subjects more than English, but keep the possessive when the sentence subject shifts, when the referent could be misread, or when the clause describes an action the reader performs. Over-dropping creates ambiguity.
- **Drop 「〜することができます」.** Use `〜できます` directly. The longer form is verbose and translationese.
- **Drop 「〜とき／〜場合」 wrappers** around simple time clauses when 「〜時」 suffix or noun-form works. `実行時` is cleaner than `実行されるとき`.
- **Avoid stacked 「の」.** 「あなたのチームのRAGシステムの設定」 reads as MT; restructure into shorter phrases.

### Other Quality Issues

- **Missing CJK-Latin spaces.** The most visible quality signal. Missing spaces immediately mark output as machine-translated.
- **Literal English syntax.** Restructure English relative clauses and long modifier chains into natural Japanese clause order.
- **Inconsistent terminology.** Always follow the glossary. Do not alternate between different translations of the same term.
- **Over-translation.** Brand names, feature names, API parameter names, and code identifiers must remain in English.
- **Passive voice overuse.** Japanese prefers active constructions. Avoid literal passive translations (〜される) when an active form is more natural.
- **Register mixing.** Never mix です/ます and だ/である within a single page.
