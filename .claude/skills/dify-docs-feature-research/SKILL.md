---
name: dify-docs-feature-research
description: "Research a Dify feature before writing or optimizing documentation. Use when starting any doc task that requires understanding a feature's implementation, user pain points, or community feedback. Triggers: 'research this feature', 'investigate the code for', 'what do users say about', 'let's understand how X works before writing', or any documentation task where the current docs are being rewritten or significantly expanded."
---

# Dify Feature Research

Pre-writing research that combines codebase analysis with community feedback to ensure documentation is grounded in both technical reality and actual user needs.

## Before Starting

1. Ask the user which feature, node, or area to research.
2. Confirm which branch of the Dify codebase to investigate (default: `main`).
3. Check if the user has a specific doc page in mind for the rewrite.

**Codebase location**: The Dify codebase is typically available as an additional working directory. If not, ask the user for the path.

**Pull latest code** before investigating. In the Dify codebase directory:
```bash
git fetch origin && git checkout main && git pull origin main
```
If the user specified a different branch, substitute accordingly.

**GitHub repo**: `langgenius/dify`

## Research Process

Run Phase 1 and Phase 2 in parallel using subagents where possible.

### Phase 1: Codebase Investigation

Locate and read the source code for the feature. Cover all three layers:

**Backend implementation** — Find the core logic. For workflow nodes, check `api/dify_graph/nodes/<node_name>/`. Read:
- The main node class (execution logic, `_run()` method)
- Entity definitions (data models, enums, supported types)
- Any template or streaming logic

**Frontend UI** — Find the React components. For workflow nodes, check `web/app/components/workflow/nodes/<node_name>/`. Read:
- Panel component (what configuration options users see)
- Type definitions (data shape)
- Default values and validation rules

**API surface** — Trace how the feature's output reaches the API response. Check controllers, response converters, and serialization.

Produce a summary of:
- What the feature does (based on code, not existing docs)
- What configuration options exist
- What data types / values are supported
- How results are returned to the user (UI, API, streaming)
- Any notable edge cases or limitations visible in the code

Flag any behavior inferred from code rather than observed in the running product.

### Phase 2: Community Feedback

Search for user-reported problems and questions across these channels:

**GitHub Issues** — Run multiple searches with varied terms:
```bash
gh issue list --repo langgenius/dify --search "<feature name>" --limit 30
gh issue list --repo langgenius/dify --search "<alternative name>" --limit 30
gh search issues "<feature> <context>" --repo langgenius/dify --limit 20
```

**GitHub Discussions** — Search for related discussion topics:
```bash
gh api "repos/langgenius/dify/discussions?per_page=30" --jq '.[] | select(.title | test("<pattern>"; "i"))'
```

For each relevant issue or discussion, read the body and top comments to understand:
- What the user was trying to do
- What went wrong or was confusing
- Whether it's a bug, missing feature, or documentation gap

**Categorize findings** into:

| Category | Description |
|:---------|:------------|
| **Documentation gap** | User couldn't find information that should be documented |
| **Confusion** | User misunderstood behavior the docs should clarify |
| **Bug** | Product defect — note but don't document workarounds as features |
| **Feature request** | Missing capability — note but don't document as existing |

### Phase 3: Synthesize

Combine both phases into a structured research summary:

```
## Feature: [Name]

### How It Works (from code)
- [Key behaviors, configuration options, supported types]
- [API response structure]
- [Edge cases or limitations]
- [Unverified inferences — flagged for user testing]

### Current Documentation
- [What the existing page covers]
- [What it's missing]

### Community Pain Points
| Theme | Issues | Type | Doc impact |
|-------|--------|------|------------|
| ...   | #123   | gap  | Should document |

### Recommended Documentation Scope
- [What to add based on gaps]
- [What to clarify based on confusion]
- [What to explicitly omit and why (bugs, unreleased features)]
```

Present the summary to the user. Jointly decide what to include before starting the writing phase.

## Important

- This skill produces research only. Do not start writing documentation until the user reviews the findings and confirms the scope.
- Flag code-inferred behavior as unverified. Ask the user to test before documenting as fact.
- Distinguish bugs from documentation gaps. Documenting buggy behavior as intended causes more harm than leaving a gap.
- Note issue numbers for traceability. The user may want to reference them when prioritizing what to cover.
