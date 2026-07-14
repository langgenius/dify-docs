---
name: dify-docs-feature-research
description: "Research a Dify feature before writing or optimizing documentation. Use when starting any doc task that requires understanding a feature's implementation, user pain points, or community feedback. Triggers: 'research this feature', 'investigate the code for', 'what do users say about', 'let's understand how X works before writing', or any documentation task where the current docs are being rewritten or significantly expanded."
---

# Dify Feature Research

Pre-writing research that combines codebase analysis with community feedback to ensure documentation is grounded in both technical reality and actual user needs.

## Before Starting

1. Ask the user which feature, node, or area to research.
2. Confirm which dify ref to investigate (default: `main`). For graphon, the default is the version dify pins (step 6), never graphon `main`.
3. Check if the user has a specific doc page in mind for the rewrite.
4. Locate the repos: use the dify and graphon working directories configured for this session (`langgenius/dify` and `langgenius/graphon` on GitHub). If either is absent, ask the user for its path.
5. Sync and read code at the target ref by following "Syncing the Dify codebase safely" in `writing-guides/index.md`.
6. Resolve the graphon pin. dify pins graphon to an exact version; verify graphon behavior at that tag. From the dify repo root:
   ```bash
   grep '"graphon' api/pyproject.toml
   # e.g. "graphon==0.6.0" → read graphon at tag v0.6.0, not main
   ```
   Behavior read from graphon `main` may not exist in the version users run. Ask the user before researching graphon `main` (appropriate only when documenting something they know is about to ship).

## Research Process

Run Phase 1 and Phase 2 in parallel: dispatch one subagent per phase. If subagents are unavailable, run Phase 1 first, then Phase 2.

### Phase 1: Codebase Investigation

1. Decide which repo owns the backend implementation. Node ownership (which workflow nodes live in dify vs graphon) is maintained in one place: `.claude/skills/dify-docs-release-sync/references/detection-tables.md`. Read that file to route the feature; do not route from memory.
   - Human Input is split across both repos: graphon executes the node (`src/graphon/nodes/human_input/`), while dify owns the boundary, callback, and session-binding code (`api/core/workflow/nodes/human_input/`). Research both halves.
2. Locate the code:

| Layer | Repo | Path |
|:------|:-----|:-----|
| Workflow node backend | per ownership table (step 1) | graphon: `src/graphon/nodes/<node_name>/` or dify: `api/core/workflow/nodes/<node_name>/` |
| Graph engine, runtime state, variable pool, command channels, layers | graphon | `src/graphon/graph_engine/`, `src/graphon/runtime/` |
| Model runtime, model providers, LLM/embedding/rerank invocation | graphon | `src/graphon/model_runtime/` |
| Workflow orchestration in Flask routes and Celery tasks | dify | `api/controllers/`, `api/tasks/`, `api/services/` |
| RAG and knowledge retrieval logic | dify | `api/core/rag/` |
| Tool plugins | dify | `api/core/tools/` |
| Frontend UI (all features; the web app was never split out) | dify | `web/app/components/workflow/nodes/<node-name>/` (kebab-case) |

3. Read the backend implementation:
   - The main node class (execution logic, `_run()` method)
   - Entity definitions (data models, enums, supported types)
   - Any template or streaming logic
4. Read the frontend UI:
   - Panel component (what configuration options users see)
   - Type definitions (data shape)
   - Default values and validation rules
5. Trace the API surface: how the feature's output reaches the API response. Check controllers, response converters, and serialization (all in dify).
6. Produce a summary of:
   - What the feature does (based on code, not existing docs)
   - What configuration options exist
   - What data types / values are supported
   - How results are returned to the user (UI, API, streaming)
   - Any notable edge cases or limitations visible in the code
7. Flag inferred behavior per the rule in [Important](#important).

### Phase 2: Community Feedback

Search for user-reported problems and questions across these channels:

**GitHub Issues** — Run multiple searches with varied terms. Always search dify; also search graphon when the feature is a built-in workflow node, the graph engine, runtime, or model_runtime:

```bash
gh issue list --repo langgenius/dify --search "<feature name>" --limit 30      # e.g. "human input"
gh issue list --repo langgenius/dify --search "<alternative name>" --limit 30  # e.g. "HITL"
gh search issues "<feature> <context>" --repo langgenius/dify --limit 20       # e.g. "human input timeout"

# For built-in nodes, engine, runtime, or model_runtime, also:
gh issue list --repo langgenius/graphon --search "<feature name>" --limit 30
gh search issues "<feature> <context>" --repo langgenius/graphon --limit 20
```

End users typically file in dify even for graphon-owned behavior; graphon's tracker tends to hold engineering-side reports. Check both to avoid missing pain points.

**GitHub Discussions** — Search for related discussion topics. `<pattern>` is a case-insensitive regex, e.g. `"human ?input"`:

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

Present the summary to the user. STOP — do not start the writing phase until the user reviews the findings and confirms the scope.

## Important

- This skill produces research only. Do not start writing documentation until the user reviews the findings and confirms the scope.
- Flag code-inferred behavior as unverified. Ask the user to test before documenting as fact.
- Distinguish bugs from documentation gaps. Documenting buggy behavior as intended causes more harm than leaving a gap.
- Note issue numbers for traceability. The user may want to reference them when prioritizing what to cover.
