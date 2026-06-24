---
name: dify-cli-docs
description: >
  Use when drafting or editing any page under `en/cli/` in dify-docs.
  Covers reader segments, the writing rules, content ownership, and
  codebase-verification rules for the Dify CLI (`difyctl`) doc set. Triggers:
  "draft a CLI page", "write difyctl docs", "edit a page in en/cli/".
---

# Dify CLI Documentation

## Before starting

Read `writing-guides/style-guide.md`, `formatting-guide.md`, `glossary.md`. For page structure, mirror an existing page of the same type. For the IA, see `docs.json`.

## Reader segments

`en/cli/` is CE + Cloud only (EE is separate), and launches CE-first (see Editions below).

- **CE and Cloud users** (default): have a Dify account, sign in with the browser device flow. Developers, DevOps, technical PMs; assume kubectl/gh familiarity. Explain Dify concepts by linking the main docs, never shell basics. One audience: don't split hairs over account type or token prefix in prose.
- **Integrate Your Agents** (a task section, not a persona): engineers wiring their own agent to call Dify apps as tools. Write for the human builder; engineering-deep. Disambiguate from building agents inside Dify Studio.
- SSO (`dfoe_`) is EE-only; its docs live in the EE repo, not here.

## Editions: CE-first and the Cloud badge

The CLI launches **CE-first**: the shipped docs are CE-only, with Cloud content added when Cloud supports the CLI. EE is a separate doc set (never add EE content here).

- **CE = one workspace.** No workspace switching, no `--workspace` / `-A` multi-workspace flags, no "another/every workspace" framing; `difyctl` runs against your single workspace.
- **Cloud-only content** (workspace switching and membership, and anything that needs more than one workspace) gets a `<Badge color="blue">Cloud</Badge>` on its heading or list item, then is removed for the CE release and saved to `~/Documents/Work/Projects/Dify CLI/deferred-cli-docs/cloud/` (snapshots + a restore README); restore it when Cloud ships. Mark with the badge; don't write a "Cloud only" sentence.
- **Host examples are self-hosted:** use `dify.example.com`, never `cloud.dify.ai`; the server edition shows `self_hosted`. (`auth login`'s real default is still `cloud.dify.ai`, so steer the reader to enter their host rather than stating the default.)
- `<Badge>` is not a standard Mintlify component and renders nowhere else in the repo yet; verify it before the Cloud restore.

## Writing rules

House overrides on top of the writing-guides. The non-obvious ones:

- **host vs server.** "host" = the connection target (`--host`, `hosts.yml`, `use host`, "Active host", "known hosts"). "server" = the backend as actor ("the server returns", "Network or server error") or its version ("client and server versions").
- **No "envelope" jargon.** Describe JSON plainly ("a `data` array with the paging fields `page`/`limit`/`total`/`has_more`"); error JSON is "a structured JSON object".
- **App types:** Chatbot, Chatflow, Agent, Workflow, Text Generator in prose; API mode names (`chat`, `advanced-chat`, ...) only inside literal output blocks.
- **Configurable values:** when a value is settable by flag, env var, and/or config, name the methods and make their precedence unambiguous, in prose or a numbered list, whichever is clearer (a list is often clearest for a multi-step chain). Clarity is the test, not a fixed phrase: avoid the chained "A overrides B, which overrides C" (the referent of "which" is unclear) and a bare "or" (hides the order). "Override" is fine with one clear referent ("the `--limit` flag overrides `DIFY_LIMIT`") or a named target ("overrides the resolution chain", linking the owner).
- **Openers stay general** over volatile lists (don't enumerate config keys in an opener); the table carries the specifics.
- **Cross-references:** make the command the actor ("Run `auth devices list` to see your sessions"), not "to do X, see [section]"; for an owned fact, link with a short payoff instead of re-explaining.
- **Placeholders:** app/workspace IDs are UUID-shaped (non-UUID fails validation); the reader's own identity is `<your-*>`; received values stay concrete. Never `<your-app-id>` in runnable code.
- **Never document `DIFY_TOKEN` or any non-interactive token as working auth** — the only path is the browser device flow.
- Backtick the typeable token, not the category word ("list commands such as `get app`"; never `list`).
- No version numbers in prose (the `version` page shows real output); no See Also; shipped reality only, except an in-flight Linear fix may be documented as expected behavior, verified before publish.

Also: task-oriented openers (lead with when/why you run it), front-load the key limitation, show real terminal output, ~3-4 line paragraphs, few semicolons, em dashes by judgment.

## Command Reference structure

One page per resource; each command an H2, task-phrased (never the literal command). Per-command order:

1. **Synopsis** (CLI notation `<required>` `[optional]` `...repeatable`) + a one-line description.
2. **`### Arguments`** — required wherever a positional arg exists, parallel to `### Flags`; note an arg's source ("`<app-id>` from `get app`").
3. **`### Flags`** — Flag / Type / Default / Description; a recurring flag gets its full description in every command that takes it.
4. **`### Examples`** — a verb-led caption + the command block. No result samples here.
5. **`### Output`** — what stdout and stderr get in each mode, success included. `-o` commands get a `| Format | What stdout gets |` table + captioned samples (exempt: `export`, `--json`-only). Describe failures, don't quote error strings.
6. **`### Exit Codes`** — link to Output Formats and Exit Codes for the full table.

Multi-command pages open with a one-line lead-in + a mini-index of anchor links; one-command pages get a plain sentence. Put a page-level "how it works" / owned section at the END, after the commands, but when a section is tightly coupled to one command (pause/resume belongs with run/resume), keep it beside that command rather than exiled to the bottom.

## Content ownership

Write each cross-cutting fact ONCE on its owner; link the anchor everywhere else. Never re-teach Dify platform concepts (one sentence + a link to the main docs).

| Content | Owner |
|---|---|
| Run dispatch across app types | Apps, "Run an App" |
| HITL pause/resume (exit 0 + `status:"paused"`) | Apps, "When a Workflow Pauses" |
| Workspace resolution chain | Workspaces |
| `-o` schemas, exit codes, stdout/stderr discipline | Output Formats and Exit Codes |
| Global flag inventory | Global Flags |
| Help forms and topics | help |
| Agent discovery (`help -o json`, `agentGuide`) | The Agent Contract |
| Sign-in and token storage | Authenticate |
| Env-var inventory | Environment Variables |
| Compat probe and range | version |

## Verification

Check behavior against the code, not the docs or in-CLI help (both drift). The CLI is `langgenius/dify` under `cli/` on `origin/main`: `git show origin/main:cli/<path>`. Never `feat/cli` or `cli/README.md`. Best source for exact strings and exit codes: the e2e suite `cli/test/e2e/suites/**`. Flags/args → `commands/<verb>/<resource>/index.ts`; codes → `errors/codes.ts`; env vars → `env/registry.ts`. Can't verify a claim? Skip it, soften it, or flag `{/* VERIFY: ... */}`.

For project context (known bugs, decisions, what's shipped vs planned), see the **Dify CLI** Linear project (team WTA).

After writing, run `writing-guides/index.md#post-writing-verification`, confirm anchors resolve and no owned fact is re-explained, and re-verify any behavior claim against `origin/main`.
