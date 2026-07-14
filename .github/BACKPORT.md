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

## Batch (many PRs at once)

One-time local auth: create `~/.backport/config.json` with
`{ "accessToken": "<a GitHub token with repo scope>" }`.

Then gather and select interactively (targets passed at runtime, so any
`release/*` works without editing config):

```bash
# By query, then arrow-key multi-select the PRs:
npx backport --pr-query "merged:>=2026-05-01 label:backport-pending" \
  --branch release/1.16.0 --branch release/1.15.0
# Or by path / single PR:
npx backport --path en/self-host/use-dify --branch release/1.15.0
npx backport --pr 792 --branch release/1.15.0
```

## Finishing a conflicting backport

```bash
npx backport --pr <source-pr-number> --branch release/<branch>
# resolve the conflict when prompted; the CLI pushes and opens the PR
```
