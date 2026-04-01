# Dify Documentation — AI Agent Instructions

For documentation tasks, read these guides before starting:

1. `writing-guides/style-guide.md` — Voice, tone, writing patterns
2. `writing-guides/formatting-guide.md` — MDX formatting, Mintlify components
3. `writing-guides/glossary.md` — Standardized terminology

For task-specific guidance, see `writing-guides/index.md`.

## Key Rules

- Write in English only, except when specifically optimizing Chinese
  or Japanese translations.
- Only edit the English section in `docs.json`. Translation sections sync
  automatically.
- MDX files require `title` and `description` in YAML frontmatter.
- Never use `--no-verify` when committing.

## Repository Structure

en/, zh/, ja/         Documentation content (en is source)
writing-guides/       Style guide, formatting guide, glossary
tools/translate/      Translation pipeline and language-specific formatting
.claude/skills/       Documentation writing skills (auto-discovered)
docs.json             Navigation structure

## Development

mintlify dev          Local preview at localhost:3000

## Commit and PR Title Conventions

{type}: {description} — lowercase, imperative, no trailing period, under 72 chars.

| Type | When | Example |
|:-----|:-----|:--------|
| `docs` | New or updated content | `docs: add workflow node configuration guide` |
| `fix` | Typos, broken links, incorrect info | `fix: correct broken link in knowledge base page` |
| `feat` | Tooling or structural changes | `feat: add search index to knowledge section` |
| `refactor` | Reorganization without content changes | `refactor: restructure knowledge base section` |
| `translate` | Translation additions or updates | `translate: update Japanese workflow pages` |
| `style` | Formatting-only changes | `style: fix heading levels in plugin guide` |
| `chore` | Dependencies, config | `chore: bump mintlify to 4.0.710` |