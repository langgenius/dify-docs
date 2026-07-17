---
name: dify-docs-terminology-check
description: >
  Audit terminology consistency across documentation against the codebase UI
  labels and the glossary. Covers full files, not just diffs; excludes env var
  docs. Use after finalizing a draft, or when the user says "check
  terminology", "check terms", "verify glossary", or "terminology audit".
---

# Terminology Consistency Check

Read-only audit. Verify that documentation terms match the glossary (general terms) and the Dify codebase i18n (UI labels). Covers the whole file, not just the diff. Do NOT modify any files during the audit; report findings and stop.

## Step 1 — Read the sources of truth

1. Read `writing-guides/glossary.md`. Two sections matter here:
   - `## General Terms` — standard body-text terms with English/Chinese/Japanese columns.
   - `## UI Labels` — product UI strings with an `i18n Key` column mapping each label to the codebase.
2. Locate the Dify codebase. If it is available as an additional working directory, use it; otherwise ask the user for the local path to their Dify repo.
3. Ask the user: **"Which branch in the Dify codebase should I check UI labels against?"** (e.g., `main`, a feature branch). Default to `main` if they have no preference.

## Step 2 — Pin the codebase ref

1. Sync and read the Dify codebase per `writing-guides/index.md` → "Syncing the Dify codebase safely". Never `git checkout` or `git pull` in the Dify tree.
2. Fetch, then resolve the ref once and record it for the report. In the Dify repo:
   ```bash
   git fetch --tags origin
   REF=$(git rev-parse origin/<branch>)
   ```
   All i18n lookups below use `"$REF"`; the report cites it (short form, e.g. `61d2ad572a`).

## Step 3 — Set the scope

1. Default scope: the whole file(s) currently under review (not just the diff), plus their zh/ja siblings when they exist. Expand to a directory or the full docs tree only if the user says so.
2. Skip zh/ja checks for files whose translations don't exist yet.
3. Always exclude (env var names are not UI labels):
   - `en/self-host/deploy/configuration/environments.mdx`
   - `zh/self-host/deploy/configuration/environments.mdx`
   - `ja/self-host/deploy/configuration/environments.mdx`

## Step 4 — Extract candidate terms

For each file in scope, in the docs repo:

```bash
grep -anoE '\*\*[^*]+\*\*' <file>    # bolded terms, prints line:**term**
grep -anE '^#{2,3} ' <file>          # section headings, prints line:## Heading
```

The `-a` flag is required: some legacy zh/ja pages contain stray NUL bytes, and without it grep prints only `Binary file … matches` and silently drops the term inventory.

Every bolded term and every heading is a candidate. Step 5 decides deterministically which are UI labels; do not pre-filter by intuition.

## Step 5 — Classify and verify UI labels against codebase i18n

The codebase i18n is the source of truth for UI labels: `web/i18n/en-US/` (flat JSON files with dot-flattened keys, e.g. `"menus.apps": "Studio"`), plus `zh-Hans/` and `ja-JP/` siblings. The glossary's `i18n Key` column maps to them: `common.menus.apps` → file `common.json`, key `"menus.apps"`.

For each candidate term (use the English term; for zh/ja files, take the candidate from the same position in the en sibling):

1. If the term has a `## UI Labels` row in the glossary, read its `i18n Key`; skip to substep 3 to confirm the codebase still agrees.
2. Otherwise search the en-US i18n values. In the Dify repo:
   ```bash
   git grep -nF '"<Term>"' "$REF" -- 'web/i18n/en-US/*.json'
   ```
   - Exact-value hit (e.g., `<REF>:web/i18n/en-US/common.json:285:  "menus.apps": "Studio",`) → it is a UI label; note the file and key.
   - No hit → retry case-insensitively: `git grep -inF '<term>' "$REF" -- 'web/i18n/en-US/*.json'`. A hit here means the doc's casing or wording deviates from the UI string — flag it.
   - Still no hit → not a UI label. Headings fall out of scope here; bolded terms go to Step 6 (general terms) instead.
3. Confirm the exact string at the key:
   ```bash
   git grep -nF '"<key>"' "$REF" -- web/i18n/en-US/<file>.json
   ```
   The doc's English term must match the printed value exactly (casing included). If the glossary row disagrees with the codebase, the codebase wins — record a glossary gap.
4. For zh/ja siblings, look up the same key in the matching locale:
   ```bash
   git grep -nF '"<key>"' "$REF" -- web/i18n/zh-Hans/<file>.json
   git grep -nF '"<key>"' "$REF" -- web/i18n/ja-JP/<file>.json
   ```
   Each prints one line with the localized string; the zh/ja doc's bolded term must match it exactly.

## Step 6 — Check general terms against the glossary

For candidates that are not UI labels, and for terms noticed while reading the prose:

1. Find the term's row: `grep -in '<term>' writing-guides/glossary.md`. Expected output: the table row(s) containing the term; no hit means the term is not standardized (consider it for Glossary Gaps if it recurs).
2. Verify the file's usage against the column for its language — English column for `en/`, Chinese for `zh/`, Japanese for `ja/`. Honor the row's Notes (casing rules, context restrictions). Flag every deviation with its line number.

## Step 7 — Report

Report findings in this format, then STOP. Do not edit any file until the user responds.

```
## Terminology Check Results

Checked against Dify codebase `origin/<branch>` at `<short REF>`.

### File: {path}

**General Terms**
- ✅ No issues found
  OR
- ⚠️ Line {n}: "{found}" should be "{expected}" per glossary

**UI Labels**
- ✅ All UI labels (bolded terms and feature section headings) match codebase
  OR
- ⚠️ Line {n}: **{label}** — codebase says "{expected}" (web/i18n/<locale>/<file>.json, key "<key>")

**Glossary Gaps**
- Terms used in docs but missing from glossary: {list}
- Glossary entries outdated compared to codebase: {list}
```

## Step 8 — Glossary updates (only after user approval)

If the user approves fixes for Glossary Gaps:

1. Edit `writing-guides/glossary.md` with the approved rows.
2. Regenerate the termbase. In the docs repo:
   ```bash
   python3 tools/translate/derive-termbase.py
   ```
   Must print `Generated .../tools/translate/termbase_i18n.md`.
3. Verify sync:
   ```bash
   python3 tools/translate/derive-termbase.py --check
   ```
   Must print `termbase_i18n.md is in sync with glossary.md.` and exit 0. `git diff tools/translate/termbase_i18n.md` must show only rows corresponding to the approved glossary edits.
