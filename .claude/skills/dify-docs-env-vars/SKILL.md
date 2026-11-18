---
name: dify-docs-env-vars
description: >
  Rule pack for the environment variable reference —
  en/self-host/deploy/configuration/environments.mdx. Carries the tracing
  procedure, description rules, verifier, and document structure. Loaded by
  dify-docs-write; not an entry point.
---

# Dify Environment Variable Documentation

Not an entry point — run under `dify-docs-write`; the procedure below implements its stages for `en/self-host/deploy/configuration/environments.mdx`. Read `references/style-overrides.md` (in this skill directory — env-var-specific style rules and description anti-patterns) together with this pack. Use the ref pinned at S1.

## Procedure (S2 → S5)

Work through in order. **Every variable goes through the trace, explanation, task-analysis, report, and description steps without exception** — do not skip a variable because it seems "obvious".

### Step 1 (S2): Trace each variable in the codebase

When using subagents for tracing, assign 3–5 related variables per agent. Tracing depth depends on variable type:

| Variable type | Depth |
|---|---|
| Python config vars (defined in `api/configs/`) | Full trace (below). |
| Frontend vars (mapped in `web/docker/entrypoint.sh`) | Trace the Docker-to-`NEXT_PUBLIC_*` mapping in `entrypoint.sh`; verify the default in both `docker/envs/core-services/web.defaults` and `web/.env.example`; run `grep -rn "<VAR_NAME>" <path-to-dify-repo>/api/` — any match means the var is dual-purpose and needs a full trace. |
| Docker/container service vars (only in `docker-compose.yaml`) | `grep -rn "<VAR_NAME>" <path-to-dify-repo>/api/` must return no matches; then document from the comments in the service's `.defaults` file. |
| Plugin daemon vars (`PLUGIN_*` not in `api/configs/`) | Document from the comments in `docker/envs/core-services/plugin-daemon.defaults`. |

Full trace:

1. Find the definition in `api/configs/` — Pydantic field type, default, description, and any `validation_alias` (fallback) settings.
2. Find every usage — grep both the env var name and the Python attribute (`dify_config.VARIABLE_NAME`); read the surrounding code.
3. Determine behavior when empty vs set — trace fallback chains; identify what breaks.

### Step 2 (S2): Write a plain-language explanation

Cover: what the variable does in practical terms; the specific features that depend on it (name them); what happens if left empty; what happens if set; key code file paths (no line numbers — they shift).

### Step 3 (S3): Find the operator's task

For every variable a change adds or alters, run the pipeline's task analysis at the depth that change sets. The operator arrives with a goal rather than a variable name, so the lead text and rows must answer what the goal needs: prerequisites, which file a setting takes effect in, how to confirm it works. For a single variable the walk is usually short: Step 2 already covers what breaks when it is empty or wrong, which leaves what to set up first and how to confirm it took effect. A group that sets up something new, such as a runtime backend or an exporter, needs the whole walk.

### Step 4 (S4 contribution): Report

The S4 scope report presents: the plain-language explanations, the task analysis, and the pinned ref. The pipeline's S4 gate applies.

### Step 5 (S5): Write the user-facing description

- Lead with the practical impact, not the technical mechanism
- Name the features that require the variable (e.g., "Required for the Human Input node")
- Explain what breaks if misconfigured (e.g., "If empty, email links will be broken")
- Mention fallback behavior if any (e.g., "falls back to `CONSOLE_API_URL`")
- Include relationships with other variables when relevant
- Apply every rule in `references/style-overrides.md`

### Step 6 (S5): Edit the documentation

Edit `en/self-host/deploy/configuration/environments.mdx` following [Document Structure](#document-structure). The `zh/` and `ja/` copies follow at the pipeline's S6, after the owner freezes the English.

## S7 verifiers

### Run the verifier

The canonical command scans the root template and the `envs/` tree together; a run that leaves out either one under-scans and reports false "extra in docs" results:

```bash
python3 .claude/skills/dify-docs-env-vars/verify-env-docs.py \
  --env-example <path-to-dify-repo>/docker/.env.example \
  --env-example <path-to-dify-repo>/docker/envs \
  --compose <path-to-dify-repo>/docker \
  --docs en/self-host/deploy/configuration/environments.mdx
```

`--env-example` is repeatable, and a directory argument is searched recursively for `*.env.example` and `*.defaults`. The script first lists the files it parsed in merge order, each with the part it plays in a stock installation (see [Source of Truth](#source-of-truth)): confirm the list includes the `.defaults` files under `docker/envs/` and ends with `docker/.env.example` marked `[stock .env]`.

`--compose` reads the `${VAR}` references in `docker/docker-compose*.y*ml`, the colon-less `${VAR-x}` form included. A variable a compose file consumes with no env-file entry is invisible to every other check — `EXPOSE_WEAVIATE_GRPC_PORT` went undocumented for eleven months that way — so the script lists them under `=== IN COMPOSE BUT NOT IN ANY .env.example (<n>) ===` and treats them as source variables from then on. `--compare-rev` reads the compose files at both refs on its own. The `docker-compose.pytest.*.yaml` files are skipped in both modes, and each skip is printed: they serve only the integration tests, and no deployment reads them.

Before its checks, the script prints two notes that the [Source of Truth](#source-of-truth) table acts on: how many documented variables no env file gives a default, and which documented variables are container mappings.

Output contract: on a fully clean doc the last line is `ALL CHECKS PASSED — documentation matches .env.example` and the script exits 0; otherwise it prints `TOTAL ISSUES: <n>` with per-category counts and exits 1. After changing the script, run `python3 .claude/skills/dify-docs-env-vars/test_verify_env_docs.py`; it must end with `OK`.

**Cadence.** The full command above is the baseline audit. A release pass runs `--compare-rev`, which diffs every env file between two refs, commented lines included, plus the compose references, so a clean baseline stays clean incrementally. A line commented out or uncommented between the refs shows under `DEFAULT CHANGED`, because it moves the default between the env files and the application. A variable listed under `REMOVED` with `(now only a container mapping)` keeps its row, which then names the variable it copies from. Re-run the full command whenever this script, the ignore list's location, or the env-file layout changes, and after any pass that touched more than a handful of variables; it must end on `ALL CHECKS PASSED` or every remaining line must be accounted for in the ignore list. Run it against the `zh` and `ja` pages too — the parser understands `默认值：`, `デフォルト値：` and `（空）`, so their counts are as meaningful as English's.

Pass bar for every task: the full command ends on `ALL CHECKS PASSED`, or every remaining line is accounted for in the ignore list with a reason. **Missing from docs** is never standing backlog: every variable it lists is documented or ignored before the task ends. If the script prints `WARNING: ignore list not found`, it stops with exit status 2 and prints no counts: fix the path and re-run.

### Update the ignore list if needed

The verifier filters out variables listed in the registry's `guides/env-ignored-vars.md`. That list stays in the private registry because its entries name unreleased work. The verifier finds it through `$DIFY_DOCS_REGISTRY` or a sibling clone of this repo; pass `--ignored PATH` to point somewhere else. When you:

- Remove a variable from the docs as Cloud-only → add it under **Cloud-only (SaaS)**.
- Skip documenting an experimental or internal flag → add it under **Experimental / internal**.
- Document a variable the verifier still misreports, such as a secret the env files pre-fill and the row describes instead of reproducing → add it under **Verifier false positives**. A commented line needs no entry, since the verifier reads it. Never use this bucket for a variable absent from the env files; see [Source of Truth](#source-of-truth).

Every entry must include a source reference (PR, commit, or audit date).

## Source of Truth

Since Dify 1.19.0, the supported self-host settings live in three kinds of file, and each plays a different part in a stock installation:

- `docker/.env.example` is the minimal template a stock installation copies to `.env`. Its active lines win over every file below.
- `docker/envs/**/*.defaults` hold the tracked defaults, which Compose loads into the services that name them. A line such as `FOO=${FOO-x}` supplies `x` unless `docker/.env` or the service's optional copy, such as `envs/core-services/api-worker.env`, sets `FOO`. The lines under a **Container variable mappings** comment copy another setting into the name a container reads (`WORKER_TIMEOUT=${SANDBOX_WORKER_TIMEOUT:-15}`): the setting is the variable they copy from.
- `docker/envs/**/*.env.example` are optional templates, such as `security.env.example`, that a stock installation never creates.

In any of these files, a commented line (`# FOO=bar`) still names a supported setting. The verifier reads all three kinds, commented lines included, so always use the canonical command above.

| Var location | Action |
|---|---|
| Active in `docker/.env.example` or a `.defaults` file, other than a container mapping | Document. |
| Commented (`# FOO=bar`) in any of these files, or only in an optional template | Document, and trace the default by hand: unless a `${...}` fallback supplies it, it is the application's, which the verifier can't compare. |
| Only as a container variable under **Container variable mappings** | Document the variable it copies from. A row for the container variable itself must name that variable, because setting the container variable has no effect. |
| Only in `api/configs/` Pydantic, not in any of these files | **Don't document.** Upstream-deferred; file a PR adding it to the appropriate env file first. |
| In the env files and still parsed, but upstream-deprecated with a replacement | Keep the row; lead the description with the deprecation and the replacement: "Deprecated; use `X`." Deprecated means still parsed — a removed var never gets a Deprecated label. |
| Removed from the env files because the code no longer reads it | **Remove from docs — no tombstone rows** (a documented row implies the var still takes effect). If a successor variable replaced it, add one clause to the successor's description so the old names stay findable via search: "Replaces the former `EDITION`, ignored from 1.17.0 onward." With no successor, remove without trace; upgrader discoverability belongs in upstream Dify release notes. |

**The default a row states** is the value a stock Docker Compose installation runs with: `docker/.env.example` copied to `.env` and nothing else changed. Resolve it in the order the page's Precedence section gives, down to the application default when no loaded file sets the variable. A commented line (`# FOO=false`) and a value in an optional file that a stock installation doesn't create set nothing, so neither is the default: `ENABLE_OAUTH_BEARER` was documented as `false` from such a line while stock installations ran with the application default, `true`. A vector store's `.defaults` file loads once `VECTOR_STORE` selects that store, so its values are the defaults for that store's rows; where two stores' files disagree, as `OCEANBASE_VECTOR_HOST` does for OceanBase and seekdb, the row names both. A value a `.defaults` line builds from another setting is the default too: the row states the value a stock installation gets and names the setting it comes from, as in `redis://:difyai123456@redis:6379/2` (built from `REDIS_PASSWORD`).

**The verifier's "extra in docs" signal is not an escape hatch. Never suppress it for Pydantic-only vars via `env-ignored-vars.md`.**

## Document Structure

The doc groups variables by subsystem, broadly following the `docker/.env.example` and `docker/envs/**` layout (Common Variables, Server Configuration, Web Frontend Service, Database Service, and so on). Match an existing `##` section for a new variable; don't invent one. If a variable genuinely fits no section, raise it with the user rather than guessing.

| Element | Use for |
|---|---|
| Tables | Groups of related, straightforward variables (connection settings, credentials, tuning knobs). |
| Individual headings | Important variables needing explanation — enum-type selectors (`STORAGE_TYPE`, `VECTOR_STORE`) or variables where the "why" matters (`SECRET_KEY`, `FILES_URL`). |
| Tabs | Frontend variables where Docker and source deployments use different names. Tabs cannot sit inside table cells, so tabbed variables need individual headings. |
| Accordions | Provider-specific configuration (storage backends, vector databases, mail providers) — users only need one provider. |

## Reader Persona

Same audience as `en/self-host/deploy/` documentation (see the `dify-docs-guides` pack): DevOps engineers and system administrators deploying Dify. Assume strong infrastructure knowledge. Readers arrive two ways, neither reading linearly: scanning for a specific variable while configuring a deployment, or setting up something new, such as a runtime backend or an exporter, and looking for everything it needs. They need to know what each variable does, when to change it, and what breaks if they get it wrong.
