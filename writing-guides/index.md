# Documentation Task Guide

## Which Skill to Use

| Task | Skill | Paths | References |
|:-----|:------|:------|:-----------|
| Research a feature before writing | dify-docs-feature-research | — | Dify codebase, GitHub Issues |
| Write or improve a user guide | dify-docs-guides | `en/use-dify/`, `en/develop-plugin/`, `en/self-host/` | style-guide, formatting-guide, glossary |
| Write or audit API reference specs | dify-docs-api-reference | `en/api-reference/` | style-guide, formatting-guide, glossary |
| Write or audit env var docs | dify-docs-env-vars | `en/self-host/configuration/environments.mdx` | style-guide, formatting-guide, glossary |

When paths overlap, the most specific match takes precedence.

## Without a Skill

If no skill matches your task (e.g., fixing a typo, updating navigation), follow the style guide and formatting guide directly.

## Post-Writing Verification

After completing a writing task, run these checks in order. Each is a self-contained skill.

| Step | Skill | Purpose |
|:-----|:------|:--------|
| 1 | dify-docs-format-check-en | Enforce `formatting-guide.md` rules (frontmatter, headings, lists, code, images, spacing) on English content. |
| 2 | dify-docs-format-check-cjk | Enforce general + Chinese/Japanese-specific formatting rules on `zh/` and `ja/` content. Run after translations are generated. |
| 3 | dify-docs-terminology-check | Verify terminology consistency against the glossary and codebase UI labels. |
| 4 | dify-docs-reader-test | Read each page from a first-time reader's perspective and flag comprehension gaps. |

Steps 1 and 3 apply to any English doc change. Step 2 applies after the zh/ja translations are produced. Step 4 is always the last step because it depends on the others passing.

## Reference Files

- **style-guide.md** — Voice, tone, writing patterns, callout usage
- **formatting-guide.md** — MDX formatting, Mintlify components, headings, lists, code
- **glossary.md** — Standardized terminology with Chinese and Japanese translations
