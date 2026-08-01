# Backporting to release branches

Backports merged `main` changes onto long-term `release/*` branches as PRs.
Config lives in `.backportrc.json` and is shared by both methods below.

## Which branches are eligible

Docs on `main` use the layout introduced in `release/1.15.0` (per-audience
`en/{cloud,self-host}/use-dify/` trees). Automatic backports therefore target
`release/1.15.0` and later. On older branches (`release/1.14.*`) the same
pages live at different paths, so a cherry-pick cannot apply — landing a
change there means adapting it manually to that branch's layout in a PR
targeting the branch directly.

Before labeling, also confirm the content applies to that version: a change
to a feature that shipped after the branch's version has nothing to backport.

## Immediate (one PR)

Add a label `backport-to-release/<branch>` to the PR (before or after merge),
e.g. `backport-to-release/1.15.0`. On merge, the Backport workflow opens a
backport PR to that branch. Add multiple labels to fan out to several branches.
A clean cherry-pick opens the PR automatically; a conflict instead comments on
the source PR (finish it with the CLI below).

> The label must exist before you can apply it. When labeling for a new branch
> the first time, create the label (the labels box offers "Create new label").

If a backport depends on another change landing on the target branch first,
merge that prerequisite before the backport PR is created: a PR's checks run
against the merge ref computed when the PR opens, and re-running a failed
check replays that same ref. If the base moved after the PR opened, use
**Update branch** on the backport PR to trigger a fresh run.

## Local CLI (batch work and conflicts)

Authenticate with your existing `gh` login — its token already carries the
`repo` scope and org authorization:

```bash
npx backport --pr 792 --branch release/1.15.0 --githubToken "$(gh auth token)"
```

Without `gh`, put a token in `~/.backport/config.json` as
`{ "githubToken": "<token with repo scope>" }` — the key is `githubToken`.
The `BACKPORT_TOKEN` used by the workflow is a repository secret; it cannot
be read locally and is unrelated to CLI auth.

One edge: pushing a backport that touches `.github/workflows/` additionally
requires the `workflow` scope, which the default `gh` token does not carry —
grant it with `gh auth refresh -s workflow` if you hit that rejection.

Gather and select interactively (targets passed at runtime, so any
`release/*` works without editing config):

```bash
# By query, then arrow-key multi-select the PRs:
npx backport --pr-query "merged:>=2026-05-01 label:backport-pending" \
  --branch release/1.16.0 --branch release/1.15.0 --githubToken "$(gh auth token)"
# Or by path:
npx backport --path en/self-host/use-dify --branch release/1.15.0 --githubToken "$(gh auth token)"
```

## Finishing a conflicting backport

```bash
npx backport --pr <source-pr-number> --branch release/<branch> --githubToken "$(gh auth token)"
```

The CLI works in its own clone at `~/.backport/repositories/<org>/<repo>`,
not in the checkout you ran it from. When it pauses on conflicts: in a
second terminal, `cd` into that clone, resolve and `git add` the files
there, then return and press ENTER — the CLI commits, pushes, and opens
the PR.

## After merging

Confirm the change reached every labeled branch by probing content:

```bash
git fetch origin
git show origin/release/<branch>:<path> | grep "<distinctive marker>"
```

Squash-merged backports make `git log --grep` unreliable in both
directions — always check content, not commit messages.
