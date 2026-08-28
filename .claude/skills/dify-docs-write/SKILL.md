---
name: dify-docs-write
description: >
  The entry point for writing or revising ANY documentation in this repo —
  user guides, deployment pages, plugin-dev pages, API specs, the env-var
  reference, CLI pages. Resolves the work type and doc type, then runs the
  eight-stage pipeline (intake → research → task analysis → scope gate →
  draft → translate → verify → close). Triggers: "write docs for X",
  "document X", "update this page", "fix/correct this doc",
  "rewrite/optimize X", "add a page for X".
---

# Docs Writing Pipeline

Every writing task runs the same eight stages. The work-type row sets each stage's depth; the doc-type rule pack supplies surface-specific procedures. A stage either runs and ends with its deliverable, or prints why not — never a silent skip:

- Skipped: `S<n>: N/A per <row>`
- Modified: `S<n> modified per <row or pack>: <how>`

## Step 1 — Route and load

1. Pick the work-type row. Test predicates in order; first match wins:

| Row | Work type | Entry predicate |
|---|---|---|
| R1 | Pre-release feature | The feature is in no shipped release (its code lives on a development branch or behind an unreleased tag) |
| R2 | New page | A target page does not exist yet |
| R3 | Correction | A named existing claim is wrong or outdated, and the fix adds or removes no sections |
| R4 | Rewrite / optimization | The task changes page structure (sections added, removed, or reordered; pages split or merged) |
| R5 | Update | Any other change to existing pages (shipped product change; new content within the existing structure) |

2. Pick the rule pack from the target path; most specific match wins. Rule packs are not entry points — this skill loads them:

| Target path | Rule pack |
|---|---|
| `en/self-host/deploy/configuration/environments.mdx` | `dify-docs-env-vars` |
| `en/{cloud,self-host}/use-dify/`, `en/self-host/deploy/`, `en/develop-plugin/` | `dify-docs-guides` |
| `{en,zh,ja}/api-reference/` | `dify-docs-api-reference` |
| `en/cli/` | `dify-cli-docs` |
| Dify-Enterprise-Docs `{lang}/{X.Y.x}/deploy/`, `{lang}/{X.Y.x}/administer/` | `ee-ops-docs` (in that repo, `.claude/skills/ee-ops-docs`) |
| Dify-Enterprise-Docs `{lang}/{X.Y.x}/use/`, `{lang}/{X.Y.x}/develop/plugins/` | `dify-docs-guides` |
| Dify-Enterprise-Docs `{lang}/{X.Y.x}/develop/api/` | `dify-docs-api-reference` |
| Dify-Enterprise-Docs `{lang}/{X.Y.x}/develop/cli/` | `dify-cli-docs` |
| any other path (e.g. `en/learn/`) | none — the writing guides alone govern |

Packs may live in the target repo, as `ee-ops-docs` does. When the target repo carries an `AGENTS.md`, its repo-wide rules (derivation transforms, version mechanics, gate command, PR conventions) apply on top of the pack.

3. Read now, before any other work: `writing-guides/style-guide.md`, `writing-guides/formatting-guide.md`, `writing-guides/glossary.md`; the rule pack's SKILL.md plus every reference it names; `references/task-analysis.md` in this skill. If the task includes zh or ja content, also `tools/translate/formatting-{zh,ja}.md`.

4. Print the route before starting S1: `ROUTE: row=<R#> pack=<name|none> pages=<paths>`.

Environment rules, binding at every stage:

- A claim whose pinned source is out of reach (missing clone or access) is marked `UNVERIFIED` in the scope report and the PR description, and stays out of the page — never written as fact.
- A stage that calls for a STOP when no reviewer is in the session puts its deliverable (scope report, outline) in the PR description instead; approval happens at review.

Depth at a glance (the imperatives live in the stage sections below):

| | S2 Research | S3 Task analysis | S4 Gate | S5 Draft |
|---|---|---|---|---|
| R1 pre-release | full, dev branch | full | STOP | outline gate + sections |
| R2 new page | full | full | STOP | outline gate + sections |
| R3 correction | claim only | three questions | report; STOP only if multi-page | single diff |
| R4 rewrite | full + re-verify carried claims | full | STOP | outline gate + sections |
| R5 update | targeted | delta | STOP | per-page diffs |

## S1 — Intake

1. Record the trigger (user request, issue, or release task) and the target pages. For any `use-dify` page, list BOTH audience copies' paths and scope shared vs per-copy changes (the guides pack's dual-copy rules).
2. Pin the code ref per `writing-guides/index.md` § "Syncing the Dify codebase safely" (R1: the development branch the user names). Every later claim cites this ref.
3. Deliverable — task header: `trigger | row | pack | pages | ref`.

## S2 — Research

1. By row:
   - R1, R2, R4: invoke `dify-docs-feature-research` at **full** depth. R4 additionally treats every claim carried over from the current page as unverified and re-checks it.
   - R5: invoke `dify-docs-feature-research` at **targeted** depth, scoped to the surfaces the change touches.
   - R3: do not invoke the module. Verify the disputed claim directly at the pinned ref (`git show`) and record `file:line` evidence.
2. Run every procedure the pack labels **S2 discovery** (e.g. the guides pack's env-var grep). Record each result, including "no match".
3. Universal rules: verify against code, never against existing docs; code presence ≠ working feature — behavior inferred from code is flagged unverified, reported at S4, and never written as fact.
4. Deliverable: the module's research summary, or the claim-verification note (R3), plus discovery results.

## S3 — Task analysis

1. Apply `references/task-analysis.md` at the row's depth: R1/R2/R4 **full**; R5 **delta**; R3 **three-question** (answers go inside the S4 report).
2. Deliverable: task list and routed question list with stable IDs (`T1…`, `Q1…`) per the reference's output schema.

## S4 — Scope gate

1. Report: every page and its planned changes; all unverified claims; the question routing (per Q: docs / ui-finding / product-gap); any pack procedures queued by S2 discovery.
2. STOP for approval. Two exceptions:
   - R3 touching a single page: print the report and proceed.
   - Arriving from an approved release-sync report: print `S4 satisfied upstream (release-sync report approved <date>)` and proceed.
3. Deliverable: the scope report.

## S5 — Draft

1. The pack's procedures govern structure and content. No pack → the writing guides alone.
2. R1/R2/R4, per page: outline gate first. Propose the sections; for each, what it includes AND deliberately excludes; and the rationale — each section cites a T/Q id, ordering follows the user journey, each exclusion states its reason. STOP for outline approval, then draft ONE section at a time, pausing for review after each.
3. R5: draft and present per-page diffs. R3: present the single diff.
4. Universal: uncertain content is omitted, never hedged — record each omission and what resolves it; frontmatter descriptions are written last; concept sections describe, task pages instruct, task lists state objectives. On any conflict, the writing guides win over this skill and over packs.
5. Deliverable: approved outlines and drafted sections, or diffs.

## S6 — Translate

1. Every English change ships `zh/` and `ja/` in the same pass, per `tools/translate/formatting-{zh,ja}.md` and the glossary. Packs may modify this stage (the API pack edits all three specs directly and gates on `parity_check`).
2. New pages: register navigation for all three languages in `docs.json` in the same PR.
3. Deliverable: three languages done + navigation registered (or the printed modification).

## S7 — Verify

1. Run the check chain per `writing-guides/index.md` § "Post-Writing Verification": `dify-docs-format-check` → `dify-docs-terminology-check` → `dify-docs-reader-test`. Fix findings and re-run until each reports clean.
2. Run every check the pack labels **S7 verifier**, gating on the success output each one names.
3. Universal: this stage closes EVERY writing execution — a draft or a direct modification alike — and its fixes are applied BEFORE the finished work is presented for review, never after. Writing that somehow bypassed this pipeline still owes S7 post-hoc: resolve the pack and read the guides per Step 1, run items 1–2, apply the fixes, then present. Process documents (design docs, plans, implementation docs) are exempt.
4. Deliverable: the printed check results.

## S8 — Close

1. Report: what changed; unresolved items and follow-ups; glossary additions for new terms (or "none"); affected sibling copies (the cloud/self-host dual-copy trees).
2. Deliverable: the closing report.
