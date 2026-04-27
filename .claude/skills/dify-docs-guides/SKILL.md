---
name: dify-docs-guides
description: >
  Use when writing, improving, or reviewing Dify user guide documentation.
  Covers pages in en/use-dify/, en/develop-plugin/, and en/self-host/.
  Triggers: "write docs for [feature]", "improve this page",
  "review this documentation section".
---

# Dify Documentation Guides

## Before Starting

Read these files before beginning any documentation task:

1. `writing-guides/style-guide.md` — voice, tone, writing patterns
2. `writing-guides/formatting-guide.md` — MDX formatting, Mintlify components
3. `writing-guides/glossary.md` — standardized terminology

When optimizing Chinese or Japanese translations, also read:
- `tools/translate/formatting-zh.md` or `tools/translate/formatting-ja.md`

## Reader Personas

Adjust tone and assumed knowledge based on the document path:

### en/use-dify/
Product users building AI applications on Dify. Mix of developers and non-technical users. Assume basic AI familiarity but not infrastructure or deep coding knowledge. Explain technical concepts when they appear. Prioritize task completion and outcomes.

### en/self-host/
DevOps engineers and system administrators deploying Dify. Assume strong infrastructure knowledge (Docker, databases, networking, environment variables). Be precise with technical details. Don't over-explain standard operations.

### en/develop-plugin/
Developers building custom Dify plugins. Assume strong Python skills and familiarity with Dify's core concepts. Focus on API contracts, extension points, and code patterns. Code examples are essential.

## Collaboration Model

This is a team effort. The user brings documentation expertise and user empathy; Claude brings AI domain knowledge and broader technical perspective. Actively leverage this dynamic rather than passively executing writing tasks.

**Explain the "why" behind AI concepts.** When an AI concept comes up, explain why it's designed this way and what problem it solves—not just what it does. For example, if asked why a tool role appears in conversation history, explain from the LLM API mechanism level.

**Help judge design decisions.** When the user questions a product design: assess whether it's common in the AI field, clarify if it's Dify-specific or industry standard, and offer perspective on how users might understand it.

**Provide analogies and concrete scenarios.** When concepts are abstract, use specific scenarios rather than technical jargon. Help the user understand "why users need this feature" from a practical standpoint.

**Analyze wording from user cognition perspective.** When the user is unsure about phrasing, consider: Can users understand this term? Is it accurate in the AI context? Is there a term closer to the user's mental model?

**Proactively flag issues.** If a design seems unusual, a concept may have been misunderstood, or a term is inaccurate in the AI domain—speak up directly rather than waiting to be asked.

## Verifying Feature Behavior

- Pull the latest code before verifying. In the Dify codebase directory, run `git fetch origin && git checkout main && git pull origin main`. If the user specifies a different branch, substitute accordingly.
- For existing features: verify against the `main` branch of the Dify codebase. The user will provide the codebase path or it will be configured as an additional working directory.
- For new features: the user may specify a development branch. Code may be in flux—when behavior is ambiguous, ask rather than assume.
- Trust the codebase over existing documentation. Existing docs may be outdated or inaccurate.
- **Code presence ≠ working feature.** A code path existing does not guarantee the feature functions end to end. When behavior is inferred from code analysis rather than observed in the running product, flag it as unverified and ask the user to test before documenting it as fact.

## Environment Variables in User Guides

When a feature is gated by or configured through environment variables (feature toggles, endpoints, self-host-only switches, worker classes), coordinate with the reference doc instead of duplicating it.

### Investigate first

During feature research, check whether the feature has related environment variables:

- Grep `docker/.env.example`, `api/configs/`, and the feature's PR for any `ENABLE_*`, `*_URL`, worker, or socket settings tied to the feature.
- Note which variables are mandatory vs. optional, and what their defaults are.

If the feature has related variables, use the `dify-docs-env-vars` skill to update `en/self-host/configuration/environments.mdx` in the same session. The reference doc is the single source of truth for variable semantics.

### Division of responsibility

- **Environment Variable Reference** (`en/self-host/configuration/environments.mdx`): exhaustive. Every variable gets a description covering purpose, defaults, interactions, and failure modes. Maintained via the `dify-docs-env-vars` skill.
- **User Guide**: functional only. Name the mandatory variables and the values to set, then link to the reference. Do not re-explain the mechanism (WebSocket paths, worker classes, scheme rules, fallback behavior). Those details live in the reference.

### How to present in the User Guide

User Guides serve both SaaS (Dify Cloud) and self-hosted readers. Place self-host-only configuration in a callout rather than a dedicated H2 section. The callout surfaces the information clearly for self-hosters while letting SaaS readers skip past it without breaking the flow of the guide.

Choose the callout type by what the variables do:

- **`<Note>`** — when the variables are **mandatory** for the feature to work. Without them, self-hosters will not be able to use the feature at all. Example: `ENABLE_COLLABORATION_MODE` gates the entire collaboration feature.
- **`<Info>`** — when the variables only **customize** existing behavior (tuning a default, switching backends, adjusting an endpoint). The feature works without them; these are optional knobs.

Pattern (substitute `<Note>` or `<Info>` per the rule above):

```mdx
<Note>
On self-hosted deployments, [feature] is turned off by default. Enable it by setting:

- `VAR_NAME` = `value`
- ...

See [Environment Variables](/en/self-host/configuration/environments#var_name) for details.
</Note>
```

Do not promote self-host config to an H2 section. Giving deployment-specific content equal weight with product-facing content clutters the guide for SaaS readers, who are the majority of the audience.

### What to exclude from the User Guide

- Default values already covered in the reference.
- The "why" behind each variable: worker types, proxy paths, scheme rules, fallback behavior.
- Custom-domain examples, deployment-specific mechanics, or variable interactions.
- Anything a reader could find by clicking through to the reference.

## Style Overrides

No overrides. Follow `writing-guides/style-guide.md` as written.

## Post-Writing Verification

After completing the document, run the post-writing checks listed in `writing-guides/index.md#post-writing-verification`.
