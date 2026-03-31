---
name: dify-docs-terminology-check
description: >
  Check terminology consistency in changed documentation against the glossary
  and codebase UI labels. Use after finalizing a draft, or when the user says
  "check terminology", "check terms", "verify glossary", or "terminology audit".
---

# Terminology Consistency Check

## Purpose

Verify that changed documentation uses terms consistently with the glossary
(`writing-guides/glossary.md`) and that bolded UI labels match the Dify
codebase i18n files.

## Before Starting

1. Ask the user: **"Which branch in the Dify codebase should I check UI labels
   against?"** (e.g., `main`, `feat/support-agent-sandbox`). The Dify codebase
   is at the additional working directory for the Dify repo.

2. Detect changed `.mdx` files via `git diff` (staged + unstaged). If no
   changes are detected, ask the user which files to check.

## Checks to Perform

### 1. General Term Consistency

Read `writing-guides/glossary.md` — General Terms section.

For each changed file, verify:

- **English docs**: Terms match the English column. Flag any deviations
  (e.g., "sandbox runtime" instead of "sandboxed runtime").
- **Chinese docs**: Terms match the Chinese column. Flag mismatches
  (e.g., 沙箱 instead of 沙盒).
- **Japanese docs**: Terms match the Japanese column. Flag mismatches.

Skip zh/ja checks if the corresponding translation files don't exist locally
(they may not have been generated yet for new documents).

### 2. UI Label Consistency

Read `writing-guides/glossary.md` — UI Labels section.

For each changed file, find all **bolded terms** (text wrapped in `**...**`).
Cross-reference against the UI Labels tables:

- The bolded text in English docs must match the English (UI) column.
- The bolded text in Chinese docs must match the Chinese (UI) column.
- The bolded text in Japanese docs must match the Japanese (UI) column.

Not all bolded terms are UI labels — use judgment to distinguish UI references
from emphasis. UI labels typically appear in instructional context ("click
**Publish**", "enable **Agent Mode**").

### 3. Codebase Verification (UI Labels Only)

For any UI label flagged as potentially inconsistent, or for new UI labels
not yet in the glossary, verify against the codebase:

1. Checkout the user-specified branch in the Dify repo.
2. Search `web/i18n/en-US/`, `web/i18n/zh-Hans/`, `web/i18n/ja-JP/` for the
   relevant i18n key.
3. Report the actual codebase values.
4. If the glossary is outdated compared to the codebase, flag it.

After checking, switch back to the original branch.

### 4. First-Mention Rule (zh/ja Only)

For Chinese and Japanese docs, check that general terms follow the
first-mention parenthetical rule (defined in the glossary):

- **Local term is primary**: First mention should be "本地术语（English term）"
- **English term is primary**: First mention should be "English Term（本地术语）"
- **Same across all languages**: No parenthetical needed

Scope is per document — each page resets.

## Output Format

```
## Terminology Check Results

### File: {path}

**General Terms**
- ✅ No issues found
  OR
- ⚠️ Line {n}: "{found}" should be "{expected}" per glossary

**UI Labels**
- ✅ All bolded UI labels match glossary
  OR
- ⚠️ Line {n}: **{label}** — glossary says "{expected}", codebase says "{actual}"

**First-Mention Rule** (zh/ja only)
- ✅ All terms properly introduced
  OR
- ⚠️ Line {n}: "{term}" — missing first-mention parenthetical

**Glossary Gaps**
- Terms used in docs but missing from glossary: {list}
- Glossary entries outdated compared to codebase: {list}
```

## Important

- Do NOT modify any files. This is a read-only audit.
- Report findings to the user for review.
- If the glossary and codebase disagree, report both values and let the user
  decide which to update.
