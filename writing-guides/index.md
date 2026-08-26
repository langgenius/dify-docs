# Documentation Task Guide

## Which Skill to Use

| Task | Skill |
|:-----|:------|
| Write or revise any documentation — guides, API specs, env vars, CLI pages, or anything else | dify-docs-write — resolves the work type, loads the doc-type rule pack, and runs the stage pipeline |
| Prepare doc updates for a Dify release | dify-docs-release-sync — diffs the codebase between two pinned version refs, then hands execution to dify-docs-write |

Everything else (research, rule packs, checks) is loaded by these two — start here, not there.

## Post-Writing Verification

After completing a writing task, run these checks in order and apply the fixes before presenting the work for review — this holds even for writing that did not run through dify-docs-write (the full obligation lives in its S7 stage). Each is a self-contained skill.

| Step | Skill | Purpose |
|:-----|:------|:--------|
| 1 | dify-docs-format-check | Enforce formatting rules on changed files, routed by path: `formatting-guide.md` for `en/`, general + Chinese/Japanese-specific rules for `zh/` and `ja/`. |
| 2 | dify-docs-terminology-check | Verify terminology consistency against the glossary and codebase UI labels, in prose and in the UI strings screenshots display. |
| 3 | dify-docs-reader-test | Read each page from a first-time reader's perspective and flag comprehension gaps. |

Steps 1 and 2 cover all three languages and audit the whole document, not just the diff. Step 3 is always the last step because it depends on the others passing.

## Syncing the Dify codebase safely

Skills that verify behavior against the dify or graphon codebase read files at a pinned ref instead of switching branches. The clone may hold a feature branch or uncommitted work — never run `git checkout` or `git pull` in a tree you have not confirmed is clean.

1. In the codebase clone, fetch and pin the ref:

   ```bash
   git fetch --tags origin
   REF=$(git rev-parse origin/main)  # or the tag / dev branch the user names
   ```

2. Read files at the pinned ref with `git show`. Build the revspec in its own variable, with braces around the ref — in zsh (the macOS default shell), an unbraced `$REF:<path>` — inline or in an assignment — triggers csh-style modifier expansion (`:a` means absolute-path, so `$REF:api/…` expands to `<cwd><ref>pi/…`), handing git a mangled argument while a piped command still exits 0 with empty output. Other shells mangle differently; the braced form is safe everywhere:

   ```bash
   REVSPEC="${REF}:api/pyproject.toml"
   git show "$REVSPEC"
   ```

   Never read an empty result as "unchanged" or "file absent". If the output is empty, confirm the path exists at the ref (`git ls-tree "$REF" -- <path>`) before concluding anything.

3. If the task truly needs a full checkout (e.g., running a script over the whole tree), use a detached worktree, which leaves the clone untouched:

   ```bash
   git worktree add --detach ../dify-verify "$REF"
   # work in ../dify-verify, then:
   git worktree remove ../dify-verify
   ```

Record the SHA you verified against (`$REF`) in your report.

## Reference Files

- **style-guide.md** — Voice, tone, writing patterns, callout usage
- **formatting-guide.md** — MDX formatting, Mintlify components, headings, lists, code
- **glossary.md** — Standardized terminology with Chinese and Japanese translations
