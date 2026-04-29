---
name: dify-docs-feature-research
description: "Research a Dify feature before writing or optimizing documentation. Use when starting any doc task that requires understanding a feature's implementation, user pain points, or community feedback. Triggers: 'research this feature', 'investigate the code for', 'what do users say about', 'let's understand how X works before writing', or any documentation task where the current docs are being rewritten or significantly expanded."
---

# Dify Feature Research

Pre-writing research that combines codebase analysis with community feedback to ensure documentation is grounded in both technical reality and actual user needs.

## Before Starting

1. Ask the user which feature, node, or area to research.
2. Confirm which branch to investigate (default: `main` for both repos).
3. Check if the user has a specific doc page in mind for the rewrite.

**Codebase location**: Dify's backend logic is split across two repos.

| Repo | Local path (typical) | GitHub | Owns |
|:-----|:---------------------|:-------|:-----|
| dify | `~/Documents/Work/Dify Repo/dify` | `langgenius/dify` | API, web, orchestration, integration nodes (Agent, Knowledge, Datasource, Trigger), Celery tasks |
| graphon | `~/Documents/Work/Dify Repo/graphon` | `langgenius/graphon` | Graph engine, runtime, model_runtime, built-in workflow nodes, HTTP/file/protocols |

If either is missing as a working directory, ask the user for the path.

**Pull latest code** before investigating. Run in each repo directory:
```bash
git fetch origin && git checkout main && git pull origin main
```
If the user specified a different branch for either repo, substitute accordingly.

**Version pinning matters.** dify pins graphon to a specific version. Before reading graphon code, check the pinned version and verify against that tag, not graphon `main`:
```bash
grep '"graphon' ~/Documents/Work/Dify\ Repo/dify/api/pyproject.toml
# e.g. "graphon~=0.2.2" → check out v0.2.2 in graphon, not main
```
If you read graphon `main` and document behavior that ships only in an unreleased graphon version, the docs will not match what users see. When in doubt, ask the user whether to verify against the pinned version or graphon `main` (the latter is appropriate when documenting something the user knows is about to ship).

## Research Process

Run Phase 1 and Phase 2 in parallel using subagents where possible.

### Phase 1: Codebase Investigation

First decide which repo owns the backend implementation:

| Feature class | Repo | Path |
|:--------------|:-----|:-----|
| Built-in workflow nodes (LLM, Code, HTTP Request, If/Else, Loop, Iteration, Parameter Extractor, Document Extractor, List Operator, Variable Aggregator/Assigner, Question Classifier, Template Transform, Tool, Start/End/Answer, Human Input) | graphon | `src/graphon/nodes/<node_name>/` |
| Integration nodes (Agent, Knowledge Retrieval, Knowledge Index, Datasource, Trigger Plugin/Schedule/Webhook) | dify | `api/core/workflow/nodes/<node_name>/` |
| Graph engine, runtime state, variable pool, command channels, layers | graphon | `src/graphon/graph_engine/`, `src/graphon/runtime/` |
| Model runtime, model providers, LLM/embedding/rerank invocation | graphon | `src/graphon/model_runtime/` |
| Workflow orchestration in Flask routes and Celery tasks | dify | `api/controllers/`, `api/tasks/`, `api/services/` |
| RAG and knowledge retrieval logic | dify | `api/core/rag/` |
| Tool plugins | dify | `api/core/tools/` |

Then locate and read the source code, covering all three layers:

**Backend implementation** — Find the core logic in the repo identified above. Read:
- The main node class (execution logic, `_run()` method)
- Entity definitions (data models, enums, supported types)
- Any template or streaming logic

**Frontend UI** — Find the React components in the dify repo (the web frontend was not split out). For workflow nodes, check `web/app/components/workflow/nodes/<node_name>/`. Read:
- Panel component (what configuration options users see)
- Type definitions (data shape)
- Default values and validation rules

**API surface** — Trace how the feature's output reaches the API response. Check controllers, response converters, and serialization (all in dify).

Produce a summary of:
- What the feature does (based on code, not existing docs)
- What configuration options exist
- What data types / values are supported
- How results are returned to the user (UI, API, streaming)
- Any notable edge cases or limitations visible in the code

Flag any behavior inferred from code rather than observed in the running product.

### Phase 2: Community Feedback

Search for user-reported problems and questions across these channels:

**GitHub Issues** — Run multiple searches with varied terms. Always search dify; also search graphon when the feature is a built-in workflow node, the graph engine, runtime, or model_runtime:
```bash
gh issue list --repo langgenius/dify --search "<feature name>" --limit 30
gh issue list --repo langgenius/dify --search "<alternative name>" --limit 30
gh search issues "<feature> <context>" --repo langgenius/dify --limit 20

# For built-in nodes, engine, runtime, or model_runtime, also:
gh issue list --repo langgenius/graphon --search "<feature name>" --limit 30
gh search issues "<feature> <context>" --repo langgenius/graphon --limit 20
```

End users typically file in dify even for graphon-owned behavior; graphon's tracker tends to hold engineering-side reports. Check both to avoid missing pain points.

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
