# Dify Documentation Repository

Documentation for Dify, built with Mintlify. English is the source language;
Chinese and Japanese translations are generated automatically.

## Before Any Documentation Task

Read `writing-guides/index.md` to identify the correct skill and shared
references for your task.

## Key Rules

- Write in English only, except when specifically optimizing Chinese or
  Japanese translations.
- Only edit the English section in `docs.json`. Translation sections sync
  automatically.
- MDX files require `title` and `description` in YAML frontmatter.
- When writing about a feature, verify behavior against the Dify codebase,
  not just existing docs. Existing docs may be outdated.
- For new features, the user may specify a development branch. Code on
  development branches may be in flux—when behavior is ambiguous, ask
  rather than assume.

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
