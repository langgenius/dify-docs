---
name: dify-docs-env-vars
description: >
  Use when writing, rewriting, or auditing environment variable documentation
  for Dify self-hosted deployment. Applies to
  en/self-host/deploy/configuration/environments.mdx. Covers the full process from
  codebase tracing to user-facing descriptions.
---

# Dify Environment Variable Documentation

Work through the steps in order. **Every variable goes through steps 4–7 without exception** — do not skip a variable because it seems "obvious".

## Step 1: Read first

1. `writing-guides/style-guide.md`
2. `writing-guides/formatting-guide.md`
3. `writing-guides/glossary.md`
4. `references/style-overrides.md` (in this skill directory) — env-var-specific style rules and description anti-patterns

## Step 2: Sync the Dify codebase

Follow `writing-guides/index.md` section "Syncing the Dify codebase safely". Never run `git checkout` or `git pull` in the Dify working tree. Record the tag or SHA you verify against; cite it in your step 7 report.

## Step 3 (release sync only): Diff the var set between releases

Run this before any tracing. Per-PR detection misses vars from untagged PRs, and the verifier's Missing-from-docs list hides genuinely new vars inside old backlog.

```bash
python3 .claude/skills/dify-docs-env-vars/verify-env-docs.py \
  --compare-rev <last-release-tag> <target-release-tag> \
  --repo <path-to-dify-repo> \
  --docs en/self-host/deploy/configuration/environments.mdx
```

Pin exact tags or SHAs (e.g., `--compare-rev 1.14.1 1.15.0`), never a branch name. The script prints the vars **added / removed / default-changed** between the refs, then `=== NEW vars NOT documented and NOT in ignored-vars (<n>) — TRIAGE ===`, and exits 0. Every triage var must end the task either documented or in `ignored-vars.md` with a reason — never as silent backlog.

## Step 4: Trace each variable in the codebase

When using subagents for tracing, assign 3–5 related variables per agent. Tracing depth depends on variable type:

| Variable type | Depth |
|---|---|
| Python config vars (defined in `api/configs/`) | Full trace (below). |
| Frontend vars (mapped in `web/docker/entrypoint.sh`) | Trace the Docker-to-`NEXT_PUBLIC_*` mapping in `entrypoint.sh`; verify the default in both `docker/.env.example` and `web/.env.example`; run `grep -rn "<VAR_NAME>" <path-to-dify-repo>/api/` — any match means the var is dual-purpose and needs a full trace. |
| Docker/container service vars (only in `docker-compose.yaml`) | `grep -rn "<VAR_NAME>" <path-to-dify-repo>/api/` must return no matches; then document from `.env.example` comments. |
| Plugin daemon vars (`PLUGIN_*` not in `api/configs/`) | Document from `.env.example` comments. |

Full trace:

1. Find the definition in `api/configs/` — Pydantic field type, default, description, and any `validation_alias` (fallback) settings.
2. Find every usage — grep both the env var name and the Python attribute (`dify_config.VARIABLE_NAME`); read the surrounding code.
3. Determine behavior when empty vs set — trace fallback chains; identify what breaks.

## Step 5: Write a plain-language explanation

Cover: what the variable does in practical terms; the specific features that depend on it (name them); what happens if left empty; what happens if set; key code file paths (no line numbers — they shift). This explanation goes into your step 7 report.

## Step 6: Write the user-facing description

- Lead with the practical impact, not the technical mechanism
- Name the features that require the variable (e.g., "Required for the Human Input node")
- Explain what breaks if misconfigured (e.g., "If empty, email links will be broken")
- Mention fallback behavior if any (e.g., "falls back to `CONSOLE_API_URL`")
- Include relationships with other variables when relevant
- Apply every rule in `references/style-overrides.md`

## Step 7: Report and STOP

Present to the user: the plain-language explanations, the proposed descriptions, and the codebase ref from step 2. **STOP — do not edit any documentation file until the user approves.**

## Step 8: Edit the documentation

Edit `en/self-host/deploy/configuration/environments.mdx` following [Document Structure](#document-structure). Update the `zh/` and `ja/` copies in the same pass, per `tools/translate/formatting-zh.md`, `tools/translate/formatting-ja.md`, and `writing-guides/glossary.md`.

## Step 9: Run the verifier

The canonical command scans BOTH env sources — never pass only one:

```bash
python3 .claude/skills/dify-docs-env-vars/verify-env-docs.py \
  --env-example <path-to-dify-repo>/docker/.env.example \
  --env-example <path-to-dify-repo>/docker/envs \
  --docs en/self-host/deploy/configuration/environments.mdx
```

`--env-example` is repeatable; a directory argument is globbed `**/*.env.example` recursively. The script first prints the list of files it parsed — confirm it shows `docker/.env.example` plus the files under `docker/envs/`. A single-source run under-scans and produces false "extra in docs" results.

Output contract: on a fully clean doc the last line is `ALL CHECKS PASSED — documentation matches .env.example` and the script exits 0; otherwise it prints `TOTAL ISSUES: <n>` with per-category counts and exits 1.

Pass bar for every task: **Extra in docs: 0** and **Default mismatches: 0**. **Missing from docs** is standing backlog and may stay nonzero, but no variable you touched may appear in it, and every step 3 triage var must be resolved.

## Step 10: Update `ignored-vars.md` if needed

The verifier filters out variables listed in `ignored-vars.md` (in this skill directory). When you:

- Remove a variable from the docs as Cloud-only → add it under **Cloud-only (SaaS)**.
- Skip documenting an experimental or internal flag → add it under **Experimental / internal**.
- Document a supported variable whose `.env.example` entry is commented out (`#FOO=bar`) → add it under **Verifier false positives**. This bucket is **only** for vars present in `.env.example` in commented form; see [Source of Truth](#source-of-truth) for vars absent entirely.

Every entry must include a source reference (PR, commit, or audit date).

## Step 11: Post-writing checks

Run the checks listed in `writing-guides/index.md#post-writing-verification`.

## Source of Truth

After Dify PR #31586, the supported self-host knob surface is split across:

- `docker/.env.example` — essential startup values
- `docker/envs/**/*.env.example` — categorized optional vars (core-services, databases, infrastructure, security, vectorstores, middleware)

The verifier reads both — always use the canonical step 9 command, which passes both sources.

| Var location | Action |
|---|---|
| In any `.env.example` file, uncommented | Document. |
| In any `.env.example` file, commented (`#FOO=bar`) | Document; add to **Verifier false positives** in `ignored-vars.md` (the verifier can't parse defaults from comments). |
| Only in `api/configs/` Pydantic, not in any `.env.example` | **Don't document.** Upstream-deferred; file a PR adding it to the appropriate `.env.example` file first. |
| Removed from `.env.example` because the code no longer reads it | **Remove from docs.** Documenting unreferenced vars implies they still take effect. Discoverability for upgraders belongs in upstream Dify release notes, not this docs site. |

**The verifier's "extra in docs" signal is not an escape hatch. Never suppress it for Pydantic-only vars via `ignored-vars.md`.**

## Document Structure

The doc groups variables by subsystem, broadly following the `docker/.env.example` and `docker/envs/**` layout (Common Variables, Server Configuration, Web Frontend Service, Database Service, and so on). Match an existing `##` section for a new variable; don't invent one. If a variable genuinely fits no section, raise it with the user rather than guessing.

| Element | Use for |
|---|---|
| Tables | Groups of related, straightforward variables (connection settings, credentials, tuning knobs). |
| Individual headings | Important variables needing explanation — enum-type selectors (`STORAGE_TYPE`, `VECTOR_STORE`) or variables where the "why" matters (`SECRET_KEY`, `FILES_URL`). |
| Tabs | Frontend variables where Docker and source deployments use different names. Tabs cannot sit inside table cells, so tabbed variables need individual headings. |
| Accordions | Provider-specific configuration (storage backends, vector databases, mail providers) — users only need one provider. |

## Reader Persona

Same audience as `en/self-host/deploy/` documentation (see the `dify-docs-guides` skill): DevOps engineers and system administrators deploying Dify. Assume strong infrastructure knowledge. Readers are actively configuring a deployment and scanning for a specific variable, not reading linearly. They need to know what each variable does, when to change it, and what breaks if they get it wrong.
