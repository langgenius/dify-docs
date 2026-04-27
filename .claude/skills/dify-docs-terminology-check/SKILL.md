---
name: dify-docs-terminology-check
description: >
  Audit terminology consistency across documentation against the codebase UI
  labels and the glossary. Covers full files, not just diffs; excludes env var
  docs. Use after finalizing a draft, or when the user says "check
  terminology", "check terms", "verify glossary", or "terminology audit".
---

# Terminology Consistency Check

## Purpose

Verify that documentation uses terms consistently with the codebase i18n
(source of truth for UI labels) and the glossary (source of truth for general
terms). Covers the whole file, not just the diff.

## Before Starting

1. Ask the user: **"Which branch in the Dify codebase should I check UI labels
   against?"** (e.g., `main`, `feat/support-agent-sandbox`). If the Dify
   codebase is available as an additional working directory, use that. Otherwise,
   ask the user for the local filesystem path to their Dify repo and use it for
   reading i18n files.

   Pull the latest code before checking. In the Dify codebase directory:
   ```bash
   git fetch origin && git checkout <branch> && git pull origin <branch>
   ```

2. Determine the audit scope. Default to the whole file(s) currently under
   review (not just the diff), plus their zh/ja siblings when they exist.
   Expand to a directory or the full docs tree if the user specifies.
   Always exclude:
   - `en/self-host/configuration/environments.mdx`
   - `zh/self-host/configuration/environments.mdx`
   - `ja/self-host/configuration/environments.mdx`

   Environment variable names are not UI labels and do not belong in the
   terminology check.

## Checks to Perform

### 1. General Term Consistency

Read `writing-guides/glossary.md` — General Terms section.

For each file in scope, verify:

- **English docs**: Terms match the English column. Flag any deviations.
- **Chinese docs**: Terms match the Chinese column. Flag mismatches.
- **Japanese docs**: Terms match the Japanese column. Flag mismatches.

Skip zh/ja checks if the corresponding translation files don't exist locally
(they may not have been generated yet for new documents).

### 2. UI Label Consistency

For each file in scope, collect:

- Every **bolded term** (text wrapped in `**...**`) that refers to a UI element.
- Every section heading (`##`, `###`) that names a product feature.

Use judgment to skip bolds that are pure emphasis (e.g., `**semantically**`).

Verify every collected term against the codebase i18n as the source of truth:
`web/i18n/en-US/`, `web/i18n/zh-Hans/`, `web/i18n/ja-JP/`. Read files with
`git show <branch>:<path>` so you don't need to switch branches. The
glossary (`writing-guides/glossary.md`) is a convenience lookup; the
codebase wins when they disagree.

### 3. Glossary Updates

When the audit surfaces a UI label that is new, renamed, or inconsistent
with the codebase, propose an update to `writing-guides/glossary.md` in the
report. Note that `tools/translate/derive-termbase.py` should be run
afterward so `tools/translate/termbase_i18n.md` stays in sync.

## Output Format

```
## Terminology Check Results

### File: {path}

**General Terms**
- ✅ No issues found
  OR
- ⚠️ Line {n}: "{found}" should be "{expected}" per glossary

**UI Labels**
- ✅ All UI labels (bolded terms and feature section headings) match codebase
  OR
- ⚠️ Line {n}: **{label}** — codebase says "{expected}"

**Glossary Gaps**
- Terms used in docs but missing from glossary: {list}
- Glossary entries outdated compared to codebase: {list}
```

## Important

- Do NOT modify any files. This is a read-only audit.
- Report findings to the user for review.
- Codebase i18n is the source of truth for UI labels. When the glossary
  disagrees, update the glossary.
