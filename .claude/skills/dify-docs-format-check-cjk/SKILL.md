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

Verify Chinese (`zh/`) and Japanese (`ja/`) documentation against every rule in:

- `writing-guides/formatting-guide.md` — general rules
- `tools/translate/formatting-zh.md` — Chinese-specific rules
- `tools/translate/formatting-ja.md` — Japanese-specific rules

Mechanical rules are enforced by the linter script (`check-format-cjk.py`); judgment-call rules are checked by reading the file. The linter automatically selects the right rule set based on whether the path starts with `zh/` or `ja/`.

## Before Starting

Audit the entire file, not just the diff. Default to files currently under review, detected via:

- `git diff --name-only`
- `git diff --cached --name-only`
- Untracked files from `git status --porcelain` (lines starting with `??`)

Filter for `.mdx` and `.md` files under `zh/` or `ja/`. If no files are detected, ask the user which files to check.

Because translations are typically produced as a zh/ja pair from the same English source, it is natural to audit both languages in a single session.

## Checks

### Part 1 — Deterministic (run the linter, paste the output)

Run the linter and paste its output into your report:

```bash
python3 .claude/skills/dify-docs-format-check-cjk/check-format-cjk.py <file> [<file> ...]
```

The script selects the zh or ja rule set from the file path and is the authoritative rule list. It prints one line per violation, grouped by file, as `line [rule-id] message`; the messages are self-describing, so do not re-summarize each rule. Rule IDs are prefixed by family: `F-` frontmatter, `H-` headings (including `H-heading-end-punct` for CJK), `B-` bold, `L-` lists, `C-` code, `Li-` links, `I-` images, `M-` Mintlify components, `S-` spacing, `P-` punctuation; `CJK-` rules apply to both languages; `ZH-` are Chinese-only and `JA-` are Japanese-only.

Two `CJK-` rules need context the message alone does not give:

- `CJK-disclaimer-missing`: the script looks for the translation-disclaimer text only within the ~10 lines just below the frontmatter, so a disclaimer placed lower in the file still trips it.
- `CJK-cross-lang-link`: `/en/...` links are flagged everywhere *except* on the disclaimer line, which is allowed to point at the English source.

### Part 2 — Judgment-call review (where your attention goes)

Part 1 is run-and-paste; this pass is where you actually read and reason. The two findings the linter misses most often are **translated anchor slugs** (a cross-reference must use the translated heading slug, e.g. `#响应`, not `#response`) and **`{{placeholder}}` variables left unchanged** inside otherwise-translated prompt examples. For each changed file, read it and look for:

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

Paste the script's raw output first, then append your judgment findings under each file. The script already groups by file (with `({lang})` in the header) and ends each file with either its violation lines or `✅ no deterministic issues found`. It reports only violations, so do not add per-rule "clean" lines it never printed.

```
[script output, verbatim. Per file: "### {path} ({lang})", then
"line [rule-id] message" lines, or "✅ no deterministic issues found",
ending with "Total violations: {n}"]

### Judgment findings

**{path} ({lang})**
- Line {n}: {description of issue} ({rule area})
- ...
```

If a file has no deterministic violations and no judgment findings, the script's `✅ no deterministic issues found` line stands on its own.

## Important

- Do NOT modify any files. This is a read-only audit.
- When a deterministic rule flags something that is clearly intentional on inspection (e.g., a half-width comma inside a Latin acronym, a mainland quotation mark quoted from an external source), surface it but note the ambiguity so the user can decide.
- The terminology-check skill is the authoritative source for glossary and UI-label verification. If a finding overlaps, defer to that skill and just note the overlap.
- Japanese sentence-length and style-mix checks are heuristic. They flag candidates for human review; they are not definitive rules violations.
