# Dify Documentation — AI Agent Instructions

Documentation for Dify, built with Mintlify. English is the source, and every change ships English, Chinese, and Japanese together, external contributions included.

## Working on the docs

Write or revise any page, spec, or reference through the pipeline in `.claude/skills/dify-docs-write/SKILL.md`, a one-line correction included. It loads the writing guides and the doc-type rule pack at the stages that need them, verifies claims against the codebase at a pinned ref, ships all three languages with their navigation, and checks the work before it is presented. Hosts that do not auto-discover `.claude/skills` load that file explicitly. `writing-guides/index.md` maps tasks to skills and carries the codebase-sync procedure.

## Repository rules

- Paths that Mintlify must not publish (internal instructions, tooling, configs) are covered in `.mintignore`.
- Never use `--no-verify` when committing.

## Repository Structure

en/, zh/, ja/         Documentation content (en is source)
writing-guides/       Style guide, formatting guide, glossary
tools/translate/      Translation rules (zh/ja formatting guides, termbase) and utilities
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
