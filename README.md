# Dify Documentation

Official documentation for [Dify](https://dify.ai), available in English, Chinese, and Japanese.

## Table of Contents

- [Contributing](#contributing)
- [Viewing Previous Versions](#viewing-previous-versions)

---

## Contributing

We welcome contributions! Submit changes in **all three languages**: English (`en/`, the source), Chinese (`zh/`), and Japanese (`ja/`). If you work with an AI agent (Claude Code, Cursor, etc.), it can produce the translations — point it at `tools/translate/formatting-zh.md`, `tools/translate/formatting-ja.md`, and `writing-guides/glossary.md`, the same rules our own agents follow.

### Quick Start

1. Fork and clone the repository.
2. Create a branch, make your changes, and open a pull request against `main`.
3. Your PR will be reviewed by a maintainer, translations included — the docs team may adjust zh/ja wording during review.

### Repository Structure

```
dify-docs/
├── en/              # English documentation (source language)
├── zh/              # Chinese translations (submitted with each change)
├── ja/              # Japanese translations (submitted with each change)
├── writing-guides/  # Style guide, formatting guide, glossary
├── .claude/skills/  # Claude Code documentation skills
├── tools/translate/ # Translation rules and utilities
├── docs.json        # Navigation structure
```

- English is the source: make the change in `en/` first, then mirror it to `zh/` and `ja/` in the same PR. Keep the translation Note at the top of zh/ja pages.
- If you add or move a page, update all three language sections of `docs.json`.

### File Format

Documentation files use MDX with required YAML frontmatter:

```mdx
---
title: Your Page Title
description: A brief description of the page content.
---

Page content here...
```

### Commit and PR Conventions

Commits and PR titles follow the same format: `{type}: {description}`

- Lowercase, imperative mood ("add", not "added" or "adds").
- No trailing period.
- Under 72 characters.

| Type | When | Example |
|:-----|:-----|:--------|
| `docs` | New or updated content | `docs: add workflow node configuration guide` |
| `fix` | Typos, broken links, incorrect info | `fix: correct broken link in knowledge base page` |
| `feat` | Tooling or structural changes | `feat: add search index to knowledge section` |
| `refactor` | Reorganization without content changes | `refactor: restructure knowledge base section` |
| `translate` | Translation additions or updates | `translate: update Japanese workflow pages` |
| `style` | Formatting-only changes | `style: fix heading levels in plugin guide` |
| `chore` | Dependencies, config | `chore: bump mintlify to 4.0.710` |

For non-obvious changes, add a body after a blank line explaining why:

```
fix: switch API response mode to streaming

Blocking mode was causing HTTP 504 timeouts on large pages.
```

### Local Preview

```bash
npm i -g mintlify
mintlify dev
```

This starts a local development server at `http://localhost:3000`.

### Setup

To enable the pre-commit hook (auto-regenerates the terminology database when you commit glossary changes):

```bash
git config core.hooksPath .githooks
```

### Formatting Standards

We maintain a formatting guide in [`writing-guides/formatting-guide.md`](writing-guides/formatting-guide.md). If you use an AI-powered editor or assistant (Cursor, Claude Code, Copilot, etc.), you can point it to that file to check your work before submitting.

### AI-Assisted Contributing

This repository includes Claude Code skills in `.claude/skills/` that provide writing assistance for different documentation types. If you use Claude Code, these skills are available automatically after cloning.

### Guidelines

- **One topic per PR.** Don't combine unrelated changes.
- **All three languages.** Every content change updates `en/`, `zh/`, and `ja/` together; agent-produced translations are welcome when they follow the rules in `tools/translate/`.
- **Update navigation.** If you add a new page, add it to the English section of `docs.json`.
- **Test locally.** Run `mintlify dev` to verify your changes render correctly before opening a PR.
- **No secrets.** Never commit API keys, credentials, or `.env` files.

---

## Viewing Previous Versions

Our published documentation site only hosts the latest version of Dify. To view docs for an earlier release, check out the matching `release/*` branch and preview it locally with the Mintlify CLI.

```bash
git clone https://github.com/langgenius/dify-docs.git
cd dify-docs
git checkout release/1.14.x   # replace with the version you want
npm i -g mintlify
mintlify dev
```

This serves the historical docs at `http://localhost:3000`. See the [branches list](https://github.com/langgenius/dify-docs/branches/all?query=release) for available `release/*` versions.
