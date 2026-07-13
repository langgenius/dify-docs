# Translation Rules and Utilities

Chinese and Japanese documentation is translated alongside each English change — by the docs team and contributors alike, typically with AI-agent assistance following the rules in this directory.

## What lives here

| File | Purpose |
|:-----|:--------|
| `formatting-zh.md` | Chinese formatting and localization rules — read before writing any zh content |
| `formatting-ja.md` | Japanese formatting and localization rules — read before writing any ja content |
| `termbase_i18n.md` | Terminology database (en/zh/ja) — derived from `writing-guides/glossary.md` |
| `derive-termbase.py` | Regenerates the termbase from the glossary; `--check` verifies sync (used by CI) |
| `json_formatter.py` | Format-preserving JSON writer for `docs.json` edits (keeps diffs clean) |
| `openapi/` | OpenAPI spec translation utilities: extract translatable fields to markdown, rehydrate translated values back into the JSON |

## Translation workflow

1. Make the English change.
2. Update the zh and ja counterparts in the same pass: read `formatting-zh.md` / `formatting-ja.md` and `writing-guides/glossary.md` first; check codebase i18n strings for UI labels; keep the translation Note at the top of zh/ja pages.
3. If `docs.json` structure changed, mirror the change in the zh and ja navigation sections.
