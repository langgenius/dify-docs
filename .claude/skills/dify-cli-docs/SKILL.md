---
name: dify-cli-docs
description: >
  Rule pack for the Dify CLI (`difyctl`) doc set: en/cli/ and the Enterprise
  develop/cli/ trees. Readers, source of truth, house style, page shape, and
  content ownership. Loaded by dify-docs-write.
---

# Dify CLI Documentation

Not an entry point: `dify-docs-write` loads this pack for `en/cli/` pages and the Enterprise `develop/cli/` trees.

## Readers

Developers, DevOps engineers, and technical PMs who have a Dify account and sign in through the browser device flow. They know their shell and tools like kubectl and gh, so never explain shell basics. They may not know Dify's concepts: one sentence and a link to the main docs, never a re-teach. The "Integrate Your Agents" section is for engineers wiring their own agent to call Dify apps as tools; write for that builder, at engineering depth, and keep it distinct from building agents inside Dify Studio. SSO sign-in (`dfoe_` tokens) is Enterprise-only and is documented only in the Enterprise trees.

## Source of truth (S2)

Every behavior claim is verified in `cli/` on `langgenius/dify` `origin/main`, read at the pinned SHA per `writing-guides/index.md` § "Syncing the Dify codebase safely", and the report records that SHA. Not `feat/cli`, not `cli/README.md`, not the CLI's own help text: all three drift from what shipped. Where to look:

- exact strings and exit codes: the e2e suite `cli/test/e2e/suites/**`
- flags and args: `cli/src/commands/<verb>/<resource>/index.ts` (verb-only commands in `cli/src/commands/<verb>/index.ts`)
- error codes: `cli/src/errors/codes.ts`
- env vars: `cli/src/env/registry.ts`

A claim you cannot verify is left out or marked `{/* VERIFY: … */}`, never softened into a fact. For project context (known bugs, what is shipped versus planned), ask the user.

## Three rules that protect users

- The only documented way to authenticate is the browser device flow. `DIFY_TOKEN` and other non-interactive tokens are never shown as working auth, because readers copy auth examples into scripts.
- Runnable examples never contain `<your-app-id>`: app and workspace IDs are UUID-shaped, because a non-UUID fails validation and the reader's first attempt errors. The reader's own identity is `<your-*>`; values they received stay concrete.
- The `en/cli/` doc set launched CE-first. Cloud-only content, which is anything that needs more than one workspace (workspace switching and membership, `--workspace`, `-A`), carries `<Badge color="blue">Cloud</Badge>` on its heading or list item rather than a "Cloud only" sentence; CE prose has one workspace and no "another workspace" framing.
- Host examples use `dify.example.com`, never `cloud.dify.ai`, and since `auth login` defaults to `cloud.dify.ai`, steer the reader to enter their host rather than stating the default. If a CE release requires removing Cloud-only sections, list the exact sections and stop for approval, then remove them in a dedicated commit so git history can restore them. The Enterprise trees have multiple workspaces, so these edition rules do not apply there.

## House style

A command section opens with when and why you would run it, front-loads its key limitation, and shows real terminal output, because a reader scanning for their case decides in the first line whether to stay. The vocabulary and conventions this doc set has settled on:

- **host vs server.** "host" is the connection target (`--host`, `hosts.yml`, `use host`, "Active host", "known hosts"); "server" is the backend acting ("the server returns", "Network or server error") or its version ("client and server versions").
- **JSON, described plainly.** "A `data` array with the paging fields `page`/`limit`/`total`/`has_more`"; error JSON is "a structured JSON object". Never "envelope".
- **App types** as the product names them: Chatbot, Chatflow, Agent, Workflow, Text Generator. API mode names (`chat`, `advanced-chat`, …) only inside literal output.
- **Configurable values.** When a value can be set by flag, env var, and config, say which wins in a way that leaves no doubt; a numbered list often reads clearest for a chain. A chained "A overrides B, which overrides C" leaves the referent of "which" unclear, and a bare "or" hides the order. "Override" is fine with one clear referent ("the `--limit` flag overrides `DIFY_LIMIT`") or a named, linked target.
- **Openers stay general** over volatile lists; the table carries the specifics, so a new config key changes one row rather than the opener.
- **Cross-references** make the command the actor ("Run `auth devices list` to see your sessions"), and an owned fact is linked with a short payoff instead of re-explained.
- **Backtick the typeable token**, not the category word ("list commands such as `get app`").
- **No version numbers in prose** (the `version` page shows real output), no "See Also" sections, and shipped reality only, except a fix the user confirms is in flight, verified before publish.

## Page shape

A command reference page covers one resource, one H2 per command, headings phrased as the task ("List Your Apps", never the literal command). Read a sibling page (`en/cli/reference/apps.mdx`; for a task page, `en/cli/common-tasks.mdx`) for the shape before writing, and match it where the content is alike.

Within a command, the reader's questions come in this order, and the sections follow it:

1. What do I type: the synopsis in `<required>` `[optional]` `...repeatable` notation, plus one line on when you would reach for it.
2. What do the positional arguments mean and where do I get them: `### Arguments`, noting the source ("`<app-id>` from `get app`").
3. What flags exist: `### Flags`, a table with Flag, Type, Default, Description. A recurring flag is described in full each time, because readers land mid-page.
4. What does an invocation look like: `### Examples`, a verb-led caption and the command block, no result samples.
5. What comes back: `### Output`, stdout and stderr per mode, success included. `-o` commands get a `| Format | What stdout gets |` table with captioned samples (except `export` and `--json`-only commands). Describe failures rather than quoting error strings.
6. What the exit codes mean: `### Exit Codes`, linking Output Formats and Exit Codes for the full table.

A section that would carry a single fact becomes a sentence instead; the shape serves the reader, not the reverse.

Multi-command pages open with a one-line lead-in and an index of anchor links; a one-command page opens with a plain sentence. Page-level material (how the resource works, shared concepts) goes after the commands, unless it belongs beside one command (pause and resume stay with run), in which case it stays there.

## Content ownership

Each cross-cutting fact lives on one page; everywhere else links it with a short payoff.

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

## Checks (S7)

After the pipeline's own checks: `python3 tools/check-links.py --internal` must print `Broken links: 0` and `Broken anchors: 0` (a `<Badge>` in a heading joins the anchor slug, so `## Switch Your Workspace <Badge color="blue">Cloud</Badge>` is `#switch-your-workspace-cloud`); and confirm against the ownership table that no owned fact is re-explained on the changed page.
