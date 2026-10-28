# Documentation Task Guide

## Which Skill to Use

| Task | Skill |
|:-----|:------|
| Write or revise any documentation — guides, API specs, env vars, CLI pages, or anything else | dify-docs-write — loads the writing guides and the doc-type rule pack, then runs the stages from research to check |
| Prepare doc updates for a Dify release | Maintainers run the release-sync skill from the team's private registry; it diffs the codebase between two pinned version refs and hands execution to dify-docs-write |

Everything else (research, rule packs, checks) is loaded by these two — start here, not there.

## Post-Writing Verification

After completing a writing task, read the page back as its reader (the dify-docs-write skill's Check stage says how) and fix what you find; the checks below only catch what a reader would not. Then run them in order and apply the fixes before presenting the work, whether or not the writing went through dify-docs-write. The English is checked and final before zh and ja are translated, because an English change made after translation sends its sentences back through translation. Each, except the fact-check, is a self-contained skill.

| Step | Skill | Purpose |
|:-----|:------|:--------|
| 1 | a fact-check, dify-docs-editor-test, dify-docs-reader-test | On the English page, together, as `dify-docs-write` § Check (S7) describes: the fact-check checks this round's claims against the pinned code, the editor test judges the writing, and the reader test reads the page as a first-time reader. A unit changed by their findings goes back through the editor test and the fact-check before step 2. |
| 2 | dify-docs-format-check | Enforce formatting rules on changed files, routed by path: `formatting-guide.md` for `en/`, general + Chinese/Japanese-specific rules for `zh/` and `ja/`. |
| 3 | dify-docs-terminology-check | Verify terminology consistency against the glossary and codebase UI labels, in prose and in the UI strings shown in screenshots. |
| 4 | dify-docs-translation-test | On the zh and ja pages, once they are translated from the final English: a fresh agent judges each beside its English source against the language's formatting guide and the glossary, with the same form of marks and verdict; the API pack's specs use its parity check instead. |

Steps 2 and 3 audit the whole document, not just the diff, and run on the English before translation and on zh and ja after step 4. Step 2 also checks that the zh and ja pages carry the same sections and blocks as the English page, which passes only once the translations are in.

## Syncing the Dify codebase safely

Skills that verify behavior against the dify or graphon codebase read files at a pinned ref instead of switching branches. The clone may hold a feature branch or uncommitted work — never run `git checkout` or `git pull` in a tree you have not confirmed is clean.

The backend is split across two repos. Built-in workflow nodes, the graph engine, the runtime, and `model_runtime` live in `graphon`, version-pinned in `dify/api/pyproject.toml`; integration nodes (Agent, Knowledge, Datasource, Trigger), orchestration, RAG, and tools stay in `dify`. Verify against the graphon version dify pins, never graphon `main`. Code on a development branch may be in flux: when behavior is ambiguous there, ask rather than assume.

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
