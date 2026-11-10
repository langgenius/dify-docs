---
name: dify-cli-docs
description: >
  Rule pack for the Dify CLI (`difyctl`) doc set: en/cli/ and the Enterprise
  develop/cli/ trees. Readers, vocabulary, source of truth, rules that protect
  readers, house style, page shape, and content ownership. Loaded by
  dify-docs-write.
---

# Dify CLI Documentation

Not an entry point: `dify-docs-write` loads this pack for `en/cli/` pages and the Enterprise `develop/cli/` trees.

## Readers

This file governs `en/cli/`, which documents `difyctl` from Dify 1.18.0 on, and any Enterprise version folder whose release is built on Dify 1.18.0 or later, even while its pages are still the older ones copied from the previous folder. An Enterprise version folder whose release is built on an earlier Dify version follows `references/v1.md` instead, Readers included.

The reader works with Dify apps from a terminal and hands the same work to a coding agent, a script, or a CI job. Others arrive without handing anything over: someone upgrading scripts from the CLI before Dify 1.18.0, an admin who turns the CLI on and keeps a team's builds in step with the server, and someone deciding whether `difyctl` fits. They know their shell and tools like kubectl and gh, so never explain shell basics. They know Studio and the console, including who can do what and where settings live, so a page names a console setting and moves on rather than walking through it. The docs are for these people: a coding agent learns the CLI from the `difyctl` skill and `help`, so a page where the agent does the work gives the person a simple mental model and only what changes their actions, and leaves whatever the agent asks or shows in the moment to the agent. Code that calls a single app belongs to the Service API, not to these pages. SSO sign-in (`dfoe_` tokens) is Enterprise-only and is documented only in the Enterprise trees.

## Vocabulary

- "server" is both the connection target (`--server`, `DIFY_SERVER`) and the backend acting ("the server returns"). "host" keeps only its network sense (a proxy's `NO_PROXY` list) and appears otherwise only inside quoted CLI messages.
- Name the assistant "coding agent" and the CLI's skill "the `difyctl` skill" at first mention in a section, because Dify has an Agent app type and workspace skills. After that, "your agent" reads clearly, and "skill" on its own means a workspace skill.
- App types as the product names them: Workflow, Chatflow, Chatbot, Text Generator, and legacy Agent, cased as the glossary's Legacy Agent row says. Mode names such as `advanced_chat` appear only in command words, the `<mode>` placeholder, and the Run Apps mode table.
- Builds are named by Dify release ("the 1.18.0 build"), never by a CLI version.

## Source of truth (S2)

Business commands come from the server, not from `cli/`. Each route in `api/controllers/openapi/*.py` declares an `@endpoint` with its op id, summary, effect, requirements, and the Pydantic models that become its flags, and `_catalog.py` serves them as the catalog `difyctl` turns into commands. So an op's flags, requirements, and refusals are verified in `api/controllers/openapi/`, with `auth/requirements.py` for who may call it, and `difyctl help <command>` against a server at the same release prints the same descriptor. `cli/` holds the rest:

- local commands (`login`, `logout`, `use workspace`, `install skills`, config, cache, `version`): `cli/src/commands/`; `help`: `cli/src/plugins/commands/`
- environment variables: the `DIFY_*` set in `cli/src/plugins/env/index.ts`; the others where they're read, such as `cli/src/net/proxy.ts`, `cli/src/sys/io/color.ts`, `cli/src/sys/index.ts`, and `cli/src/store/manager.ts`; installer variables: `cli/scripts/install-cli.sh` and `cli/scripts/install.ps1`
- error codes and their exit codes: `cli/src/errors/codes.ts`; message strings: at each throw site
- tests that pin strings and behavior: the colocated `*.test.ts` files and the mock server in `cli/test/fixtures/dify-mock/`

Read everything at the Dify release the pages describe (its tag), or at the branch the user names for work ahead of a release, per `writing-guides/index.md` § "Syncing the Dify codebase safely", and record that SHA. `cli/README.md` drifts from what shipped, so it is not a source. The `difyctl` skill (`skills/difyctl/`) ships inside the build, so a page agrees with it or says nothing on that point; where the skill is wrong for the release, the page states what the code does and the gap goes to the user. A claim you cannot verify is left out or marked `{/* VERIFY: … */}`, never softened into a fact. For project context (known bugs, what is shipped versus planned), ask the user.

## Live tests (S2)

A test that runs `difyctl` against a real server is isolated from its first command, `version` and `help` included: run every call as `env -i PATH=/usr/bin:/bin HOME=<scratch>/home DIFY_CONFIG_DIR=<scratch>/cfg <full path to difyctl> …`, sign in only with `login --no-keyring`, and report any call made outside that. The fake home keeps the run out of the tester's own config, cache, and keychain. Isolation doesn't cover the server side: signing in as an account ends that account's other sign-ins on the machine, so test with an account the tester isn't using, or expect to sign them back in.

## Reader tasks (S3)

Run the pipeline's task analysis, at the depth the change sets, for each command or concept a change adds or alters. CLI readers arrive with a job rather than a command name: sign in on a server or in a container, run an app from a script, let a coding agent drive the CLI, recover from an exit code. The questions on the way to that job decide what a page says beyond the CLI's own help: what to set up first, how to confirm it worked, what to do when it fails. They go into the S4 scope report.

## Content ownership (S3, S7)

Each cross-cutting fact lives on one page. The research summary applies this table to the page: what the page owns, it states in full; anything else it needs, it states in one line, only where the reader needs it to act, and links the owner. The Upgrade page restates old-to-new facts as migration steps; that is its job, not a second home.

| Content | Owner |
|---|---|
| Where `difyctl` installs from; the first sign-in, `--insecure`, and its approval checks; the two server switches; the version rule | Get Started |
| Setting up a coding agent and the `difyctl` skill | Get Started § Set Up Your Coding Agent |
| Which app types run, and how each one runs | Run Apps § Find Your Apps |
| Human Input pause and resume | Run Apps § Answer a Human Input Form |
| What an update import does; DSL files versus app packages | Create and Update Apps from DSL Files |
| A job's sign-in through `DIFY_TOKEN` | Use `difyctl` in CI and Automation |
| Sign-in lifetime, sessions, signing out, where the token lives and the config folder per OS | Manage Your Sign-In |
| Switching workspaces, and what overrides a switch | Manage Your Sign-In § Switch Your Workspace |
| Updating the build, reinstalling the `difyctl` skill, refreshing the command list | Update or Uninstall |
| `help`, `--help`, effect labels, `--input`; `difyctl` never asks before running a command | Find and Run Commands |
| Every command and what it requires | Command Index |
| Environment and installer variables, and which workspace setting wins; the files `difyctl` keeps | Configuration |
| Where output goes, `--json`, and `--verbose`; run results; error codes, exit codes, retries, rate limits | Results, Errors, and Exit Codes |
| The crossing from the CLI before Dify 1.18.0 | Upgrade Across Dify 1.18.0 |

An error's fix lives in one Troubleshooting table: Get Started's for sign-in errors, Run Apps' for run errors, and Results' for errors any command can raise. Another page names the error in one line and links that row. An error that is a normal branch of a task, such as `draft_changed` on an update import, is handled in the task itself.

## Rules that protect readers (S5)

- **Sign-in.** An interactive sign-in is `difyctl login --server <url>` approved by a person in a browser, also when a script starts it with `--no-wait` and finishes it with `--resume`. A job with no person present sets `DIFY_SERVER` and `DIFY_TOKEN`, plus `DIFY_WORKSPACE_ID` when a command needs a workspace; the token is one a person signed in for or, once the doc set documents them, a personal access token. Examples read the token from the CI system's secrets or the environment, never as a literal, because readers copy auth examples into scripts as they are. Other tokens, such as the ones the **Access Tokens** settings page creates, stay off every page until the doc set documents them.
- **IDs in examples.** Runnable examples use UUID-shaped app, workspace, and run IDs, because a non-UUID fails validation and the reader's first attempt errors. Values the reader received, such as a form token, stay concrete.
- **Server addresses.** Examples use `https://dify.example.com`. `https://cloud.dify.ai` is named for Dify Cloud readers only where they enter the address (the sign-in step and its troubleshooting fix), never as the example value; `login` has no default server, so the page tells readers to pass the address they open Dify at.
- **Editions.** One `{lang}/cli/` set serves Dify Cloud and self-hosted servers. A fact true on both is stated neutrally; a fact true only on a self-hosted server, such as a server switch, says "on a self-hosted server". Content written for Dify Cloud readers, such as switching workspaces and agent knowledge bases, carries `<Badge color="blue">Cloud</Badge>` even where a self-hosted server could offer it; content a self-hosted server alone has, such as workspace skills, carries `<Badge color="blue">Self-Hosted</Badge>`. A badge on a heading keeps the default size; inline it is `size="sm"`. A sentence that already names Dify Cloud carries no badge.

## House style (S5)

A section opens with when and why you would do it and front-loads its key limitation, because a reader scanning for their case decides in the first line whether to stay. The conventions this doc set has settled on:

- **Commands.** Every command in a code block is a full `difyctl` command, with `#` comments as captions; an environment assignment or `$(…)` around it is fine. In prose, write the full command where the sentence tells the reader to type it, usually at a section's first mention ("Run `difyctl get console_app`"), and the bare name when naming it in passing, in tables, and later in the section. The command is the actor in a cross-reference ("Run `difyctl get account session` to see your sessions"). Backtick the typeable token, not the category word.
- **JSON.** Name results by field path (`outputs`, `run_id`, `error.message`), trim samples with `…`, and show checks as `jq -e` expressions. Never "envelope".
- **Precedence.** When a value can come from a flag, a variable, and a saved setting, say which wins so it leaves no doubt: "`--workspace-id` wins over `DIFY_WORKSPACE_ID`". A chained "A overrides B, which overrides C" hides the referent of "which"; a numbered list reads clearest for a longer chain.
- **Volatile lists.** Openers stay general and the table carries the specifics, so a new variable or command changes one row rather than the opener.
- **Shipped reality.** Describe what the release does; a fix in flight appears only when the user confirms it and it is verified before publish. No "See Also" sections. Name a Dify release only where it changes what the reader does, such as the version rule or the 1.18.0 crossing.

## Page shape (S5)

The set has five kinds of page, and a kind doesn't do another kind's job. Read the sibling of the page's kind before writing and match it where the content is alike:

- **Start** (Overview, Get Started): route the reader and end at a first working command.
- **Job** (Run Apps; Create and Update Apps from DSL Files for a `<Steps>` sequence; Build Apps, where the coding agent does the job): open with a Tip that the reader can hand the page to their coding agent. H2s are tasks ("Run a Workflow"): one to three sentences, a `bash` block, and a Note only where the reader would hit a trap.
- **Context** (Use `difyctl` in CI and Automation): an H2 per path or decision, why before how, and one complete worked example.
- **Manage** (Manage Your Sign-In; Update or Uninstall): keep `difyctl` working over time, an H2 per thing the reader maintains.
- **Reference** (Find and Run Commands; Command Index; Configuration; Results, Errors, and Exit Codes): lead each H2 with a table where its content is a set of like items, with columns from the sibling: `| Command | What it does | Requires |`, `| Variable | Description |`, `| Exit code | Means | Error codes |`.

Upgrade Across Dify 1.18.0 stands alone. A page that owns a Troubleshooting table ends with `## Troubleshooting` (`| Message | What to do |`). No page carries per-command Arguments or Flags sections: flags come from the server, and `difyctl help <command>` shows them for the reader's own server, so a page names a flag only where its task needs one. Describe failures rather than quoting error strings, except in a Troubleshooting table, where the message is how the reader finds the row.

## Checks (S7)

In each check pass, after the format and terminology checks: `python3 tools/check-links.py --internal` must print `Broken links: 0` and `Broken anchors: 0`. A `<Badge>` in a heading joins the anchor slug (`## Agent Knowledge Bases <Badge color="blue">Cloud</Badge>` is `#agent-knowledge-bases-cloud`) unless the heading carries an explicit `{#id}`. Then confirm against the Content ownership table that no owned fact is re-explained on the changed page.
