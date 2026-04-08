---
name: dify-docs-env-vars
description: >
  Use when writing, rewriting, or auditing environment variable documentation
  for Dify self-hosted deployment. Applies to
  en/self-host/configuration/environments.mdx. Covers the full process from
  codebase tracing to user-facing descriptions.
---

# Dify Environment Variable Documentation

## Before Starting

Read these shared guides:

1. `writing-guides/style-guide.md`
2. `writing-guides/formatting-guide.md`
3. `writing-guides/glossary.md`

## Four-Step Process

**Pull the latest Dify code** before tracing. In the Dify codebase directory:
```bash
git fetch origin && git checkout main && git pull origin main
```

**This process applies to every variable without exception.** Do not skip variables because they seem "obvious" — every variable must be traced, explained, and described.

### Step 1: Trace the Variable in the Codebase

**Agent granularity**: When using subagents for tracing, assign 3–5 related variables per agent.

**Tracing depth depends on variable type:**

- **Python config variables** (defined in `api/configs/`): Full tracing — find definition, all usage locations, and behavior when empty vs set.
- **Frontend variables** (mapped in `web/docker/entrypoint.sh`): Trace from `entrypoint.sh` to find the Docker-to-`NEXT_PUBLIC_*` mapping, verify the default in both `docker/.env.example` and `web/.env.example`, and check whether the variable is also used in Python code (dual-purpose). For Next.js-only variables (UI knobs like `MAX_TOOLS_NUM`), light verification is sufficient.
- **Docker/container service variables** (only in `docker-compose.yaml`): Light verification — grep to confirm the variable is not used in Python code, then document from `.env.example` comments.
- **Plugin daemon variables** (`PLUGIN_*` not in `api/configs/`): Document from `.env.example` comments.

**For full tracing**, search the Dify codebase:

1. **Find the definition** in `api/configs/` — note the Pydantic field type, default, description, and any `validation_alias` (fallback) settings.
2. **Find every usage** — grep for both the env var name and the Python attribute (e.g., `dify_config.VARIABLE_NAME`). Read surrounding code to understand what each usage does.
3. **Determine behavior when empty vs set** — trace fallback chains and identify what features break.

### Step 2: Write a Plain-Language Explanation

Write an explanation covering:

- What the variable actually does (in practical terms, not code terms)
- Specific features that depend on it (name them)
- What happens if left empty (what breaks, what falls back)
- What happens if set (what works)
- Key code locations (file paths, no line numbers — they shift)

Save to `deep-dive.md` (in this skill directory) under the appropriate section heading.

### Step 3: Write the User-Facing Description

Transform the explanation into a concise documentation description. The description must:

- **Lead with the practical impact**, not the technical mechanism
- **Name the features** that require this variable (e.g., "Required for the Human Input node" not "used for frontend references")
- **Explain what breaks** if misconfigured (e.g., "If empty, email links will be broken")
- **Mention fallback behavior** if the variable has one (e.g., "falls back to `CONSOLE_API_URL`")
- **Include relationships** with other variables when relevant
- **End with an example value** for non-obvious variables

### Step 4: Confirm with Reviewer

Present the proposed description to the user for review before editing the documentation file.

## Document Structure

The env var doc is organized into three sections following `docker/.env.example` section order:

1. **Backend (API + Worker)** — Python API server and Celery worker variables.
2. **Frontend (Web)** — Next.js frontend variables. Uses `<Tabs>` to show Docker and source code variable names.
3. **Infrastructure (Docker Compose / AWS AMI Only)** — database, Redis, Nginx, and other container variables. Not applicable to source code deployments.

**When to use tables**: Groups of related, straightforward variables (connection settings, credentials, tuning knobs).

**When to use individual headings**: Important variables needing explanation — typically enum-type selectors (`STORAGE_TYPE`, `VECTOR_STORE`) or variables where the "why" matters (`SECRET_KEY`, `FILES_URL`).

**When to use tabs**: Frontend section variables where Docker and source code deployments use different variable names. Tabs cannot be placed inside table cells, so all tabbed variables require individual headings.

**When to use accordions**: Provider-specific configuration (storage backends, vector databases, mail providers) — users only need one provider.

## Reader Persona

Same audience as `en/self-host/` documentation (see `dify-docs-guides` skill): DevOps engineers and system administrators deploying Dify. Assume strong infrastructure knowledge.

**Additional context for env var docs:** Readers are actively configuring a deployment. They need to know what each variable does, when to change it, and what breaks if they get it wrong. They are not reading linearly—they are scanning for a specific variable.

## Style Overrides

Rules specific to env var docs (override or extend the shared style guide):

- Use `(empty)` for empty-string defaults, not `""` or blank
- For empty defaults with a fallback: `(empty; falls back to X)` or `(empty; defaults to X)`
- Never include real or example secret keys — GitHub push protection blocks `sk-*` patterns. Use descriptions like `(pre-filled in .env.example; must be replaced for production)`

**Consistency over variety in reference tables.** The general style guide says to vary sentence patterns. In reference tables, consistency aids scanning. Use predictable patterns for connection credentials (hostname, port, username, password) across providers. Vary descriptions only when variables genuinely differ in behavior or purpose.

**Variable descriptions should be self-contained.** The general style guide says not to restate the heading. Variable descriptions must state what the variable does—even if the name partially implies it. Not all variable names are self-explanatory, and users may arrive at a description via search without seeing the surrounding section context.

**Include actionable technical mechanisms.** The general style guide favors user outcomes over technical mechanisms. For env var docs, include technical mechanisms that help users configure, troubleshoot, or understand trade-offs—algorithm names, encoding behavior, fallback chains, version requirements. Exclude mechanisms that only describe code architecture—factory patterns, lazy imports, class names—unless understanding them is necessary for configuration.

- **Keep**: "URL-encoded in the connection string, so `@`, `:`, `%` are safe to use", "HMAC-SHA256", "Requires Milvus >= 2.5.0", "Falls back to `CONSOLE_API_URL`"
- **Remove**: "Dify's storage dispatcher lazily imports the selected backend", "Sends POST to /v1/sandbox/run with X-Api-Key header"

**No specific recommended values for tuning parameters.** For numeric tuning parameters without clear boundaries (connection pool sizes, worker counts, timeouts, buffer sizes), do not prescribe values. Describe the symptom that indicates the value needs changing: "If you experience connection rejections under load, try increasing this value." Exception: when a value has a well-established recommendation (e.g., PostgreSQL `shared_buffers` = 25% of RAM), include it with a reference link.

## Description Anti-Patterns

| Anti-Pattern | Better |
|---|---|
| "Used for frontend references" | "Required for the Human Input node — form links in email notifications are built from this URL" |
| "The backend URL of the console API" | "Set this if you use OAuth login (GitHub, Google) or Notion integration — these features need an absolute callback URL" |
| "Upload file size limit, default 15" | "Maximum file size in MB for uploads" |
| Restating the code comment verbatim | Explaining when you'd change it and what happens if you don't |

## Verification

Run after completing any documentation change:

```bash
python3 .claude/skills/dify-docs-env-vars/verify-env-docs.py \
  --env-example <path-to-docker/.env.example> \
  --docs <path-to-environments.mdx>
```

The script reports:
- **Missing from docs**: Variables in `.env.example` not yet documented (address over time)
- **Extra in docs**: Variables documented but not in `.env.example` (verify manually)
- **Default mismatches**: Documented defaults that don't match `.env.example` — **must be zero before work is complete**

Use `.env.example` defaults (what Docker Compose users actually get), not Pydantic code defaults.

## Post-Writing Verification

After completing the document:

1. Invoke `dify-docs-terminology-check` to verify terminology consistency against the glossary and codebase.
2. Invoke `dify-docs-reader-test` to verify it from the reader's perspective.
