---
name: dify-docs-format-check-cjk
description: >
  Check formatting compliance in changed Chinese and Japanese documentation
  against writing-guides/formatting-guide.md, tools/translate/formatting-zh.md,
  and tools/translate/formatting-ja.md. Use after finalizing a translation
  batch, or when the user says "check formatting (zh/ja)", "check CJK
  formatting", or "format audit" on translated content.
---

# CJK Formatting Check (Chinese + Japanese)

## Purpose

Verify changed Chinese (`zh/`) and Japanese (`ja/`) documentation against every rule in:

- `writing-guides/formatting-guide.md` — general rules
- `tools/translate/formatting-zh.md` — Chinese-specific rules
- `tools/translate/formatting-ja.md` — Japanese-specific rules

Mechanical rules are enforced by the linter script (`check-format-cjk.py`); judgment-call rules are checked by reading the file. The linter automatically selects the right rule set based on whether the path starts with `zh/` or `ja/`.

## Before Starting

Detect changed documentation files by combining:

- `git diff --name-only`
- `git diff --cached --name-only`
- Untracked files from `git status --porcelain` (lines starting with `??`)

Filter for `.mdx` and `.md` files under `zh/` or `ja/`. If no changed files are detected, ask the user which files to check.

Because translations are typically produced as a zh/ja pair from the same English source, it is natural to audit both languages in a single session.

## Checks

### Part 1 — Deterministic (run the linter)

Run the linter:

```bash
python3 .claude/skills/dify-docs-format-check-cjk/check-format-cjk.py <file> [<file> ...]
```

The script selects zh or ja rules based on the file path. Rules fall into three groups: shared (both zh and ja), zh-only, and ja-only.

**Shared structural rules (zh + ja)**

- `F-title-missing` — frontmatter missing `title`.
- `F-desc-trailing-period` — `description` ends with a period.
- `F-quote-needed` / `F-quote-unnecessary` / `F-single-quote` — frontmatter quoting rules.
- `F-blank-after-fm` — no blank line between frontmatter close and body.
- `H-trailing-hash`, `H-blank-before`, `H-blank-after`, `H-skip-level` — heading structure rules from the general guide.
- `B-trailing-colon-inside` — colon inside `**...**`.
- `L-asterisk-bullet`, `L-nested-indent`, `L-blank-before`, `L-blank-after` — list structure.
- `C-no-language`, `C-blank-before`, `C-blank-after` — code block rules.
- `Li-click-here`, `Li-http-external` — link rules.
- `I-raw-img-tag`, `I-alt-too-long`, `I-caption-alt-mismatch`, `I-filename-*` — image rules (same set as the EN skill).
- `M-tab-no-title`, `M-component-blank-before`, `M-component-blank-after` — Mintlify component rules.
- `S-double-blank`, `S-trailing-whitespace` — spacing.
- `P-em-dash-spaces`, `P-en-dash-spaces` — general punctuation.

**Shared CJK rules (zh + ja)**

- `CJK-latin-spacing` — CJK character directly adjacent to Latin letter, digit, or backtick without a space. Exceptions: punctuation boundary, start/end of line, inside code/URLs.
- `CJK-halfwidth-punct` — half-width punctuation `, . : ; ? ! ( )` directly adjacent to a CJK character. (Slash and other exceptions are handled by language-specific rules below.)
- `CJK-bold-no-space` — bold span `**...**` adjacent to CJK character without a space on each side.
- `CJK-link-no-space` — markdown link text adjacent to CJK character without a space on each side.
- `CJK-italic` — `*text*` italic used on a CJK span. Chinese and Japanese should use bold, never italic.
- `CJK-em-dash` — em dash `—` or double em dash `——` appears in CJK text. Restructure the sentence.
- `CJK-disclaimer-missing` — translation disclaimer (`<Note> ⚠️ ...`) missing directly below the frontmatter.
- `CJK-cross-lang-link` — internal link begins with the wrong language prefix (e.g., `/en/...` inside a `zh/` file).

**Heading rules**

- `H-heading-end-punct` — CJK heading ends with sentence-ending punctuation (`。，、；：`).

**Chinese-only rules**

- `ZH-ascii-ellipsis` — `...` used where Chinese ellipsis `……` is expected.
- `ZH-fullwidth-slash` — full-width slash `／` used; must be `/`.
- `ZH-quotes` — mainland-style double or single quotation marks `""`, `''` used; must be corner brackets `「」` (single) or `『』` (nested).
- `ZH-range-hyphen` — numeric range uses `-` or `–`; must use `～`.
- `ZH-percent-space` — space between a digit and `%` or `°`.

**Japanese-only rules**

- `JA-fullwidth-digit` — full-width digit used (`１`, `２`, ...).
- `JA-fullwidth-latin` — full-width Latin letter used (`Ａ`, `Ｂ`, ...).
- `JA-fullwidth-space` — full-width space (`　`) used.
- `JA-sentence-too-long` — sentence longer than 80 Japanese characters.
- `JA-go-prefix` — `ご` prefix used on a verb in the "avoid" list (`ご確認ください`, `ご参照ください`, `ご入力ください`). `ご利用` is allowed.
- `JA-heading-sentence-ending` — heading ends with `します` / `します。` / `します？`, indicating a full-sentence rather than noun-phrase form.
- `JA-style-mix` — the file contains both です/ます and だ/である forms in body text. Only one register should be used.

### Part 2 — Judgment-call review (LLM reads each file)

For each changed file, read it and look for:

**Translatable elements**

- Tab titles (`<Tab title="...">`) translated with the glossary value.
- Frame captions and image alt text translated.
- Bold UI labels translated, matching the codebase i18n file (`web/i18n/zh-Hans/` for zh, `web/i18n/ja-JP/` for ja). Cross-check with the terminology-check skill.
- Natural-language prompt examples inside code blocks translated. Variable placeholders (`{{variable_name}}`) stay unchanged.

**Anchor translation (zh/ja)**

- Cross-references `[text](#anchor)` or `[text](/path#anchor)` use the translated heading slug, not the English original. Example: the heading `## 响应` produces `#响应`, not `#response`.

**Chinese style**

- Enumeration comma `、` used for parallel items within a sentence (where Chinese separates items that would use commas in English).
- Chinese ellipsis `……` used correctly; not combined with `等` in the same phrase.
- Arabic numerals used for technical content (`3 种`, not `三种`) — judgment call since some idiomatic expressions use Chinese numerals.
- Translationese patterns from `tools/translate/formatting-zh.md`: redundant `你的`, unnecessary `会`, `当...时` wrappers, `能够` instead of `能`, `可以` where `可` would suffice. Flag sentences that read as machine-translated.

**Japanese style**

- `です/ます` maintained in body text.
- Headings are noun phrases, not full sentences.
- Katakana long-vowel mark rules: short loanwords (3 morae or fewer) keep the trailing `ー`; longer ones drop it. Established compound katakana terms (ワークフロー, ナレッジベース) match the glossary.
- Middle dot `・` only where needed for readability; established compound terms have no middle dot.
- Translationese patterns from `tools/translate/formatting-ja.md`: redundant `あなたの`, `〜することができます` instead of `〜できます`, `〜とき/〜場合` wrappers, stacked `の`. Flag sentences that read as machine-translated.

**General**

- Terminology matches the glossary (`writing-guides/glossary.md`). Prefer invoking the terminology-check skill for rigorous checking rather than duplicating its logic here.

## Output Format

```
## CJK Formatting Check Results

### File: {path} ({lang})

**Deterministic violations** ({n})
- Line {n} [{rule-id}]: {message}
- ...

**Judgment-call findings** ({n})
- Line {n}: {description of issue} — {rule area}
- ...

**Clean checks**
- ✅ Disclaimer present
- ✅ No bold/CJK spacing issues
- ...
```

Group by file. If a file has no issues at all, report a single ✅ line.

## Important

- Do NOT modify any files. This is a read-only audit.
- When a deterministic rule flags something that is clearly intentional on inspection (e.g., a half-width comma inside a Latin acronym, a mainland quotation mark quoted from an external source), surface it but note the ambiguity so the user can decide.
- The terminology-check skill is the authoritative source for glossary and UI-label verification. If a finding overlaps, defer to that skill and just note the overlap.
- Japanese sentence-length and style-mix checks are heuristic. They flag candidates for human review; they are not definitive rules violations.
