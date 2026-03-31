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

- For existing features: verify against the `main` branch of the Dify codebase. The user will provide the codebase path or it will be configured as an additional working directory.
- For new features: the user may specify a development branch. Code may be in flux—when behavior is ambiguous, ask rather than assume.
- Trust the codebase over existing documentation. Existing docs may be outdated or inaccurate.

## Style Overrides

No overrides. Follow `writing-guides/style-guide.md` as written.

## Post-Writing Verification

After completing the document:

1. Invoke `dify-docs-terminology-check` to verify terminology consistency against the glossary and codebase.
2. Invoke `dify-docs-reader-test` to verify it from the reader's perspective.
