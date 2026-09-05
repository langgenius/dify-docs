---
name: dify-docs-write
description: >
  The entry point for writing or revising any documentation in this repo:
  user guides, deployment pages, plugin-dev pages, API specs, the env-var
  reference, CLI pages. Triggers: "write docs for X", "document X",
  "update this page", "fix/correct this doc", "rewrite/optimize X",
  "add a page for X".
---

# Writing Dify Documentation

The deliverable is a page a reader can use: accurate against the shipped product, written for the moment they arrive with, in the fewest words that stay clear. The standard is the style guide, above all its opening section, "What a Good Page Does"; the two reference pages it names calibrate register beside it. The checks catch what a reader pass can miss; passing them is a floor, not the standard.

Each stage below names what it reads. Read at the stage, not before: the drafting turn should hold the bar and the facts, not the check procedures.

## Route

Pick the rule pack from the target path (most specific match wins). When the target repo carries an `AGENTS.md`, its repo-wide rules apply on top. The pack carries what is specific to its surface. When they disagree, the guides win, over this skill too.

| Target path | Rule pack |
|---|---|
| `en/self-host/deploy/configuration/environments.mdx` | `dify-docs-env-vars` |
| `en/{cloud,self-host}/use-dify/`, `en/self-host/deploy/`, `en/develop-plugin/` | `dify-docs-guides` |
| `{en,zh,ja}/api-reference/` | `dify-docs-api-reference` |
| `en/cli/` | `dify-cli-docs` |
| `Dify-Enterprise-Docs/{lang}/{X.Y.x}/deploy/`, `…/administer/` | `ee-ops-docs` (in that repo) |
| `Dify-Enterprise-Docs/{lang}/{X.Y.x}/use/`, `…/develop/plugins/` | `dify-docs-guides` |
| `Dify-Enterprise-Docs/{lang}/{X.Y.x}/develop/api/` | `dify-docs-api-reference` |
| `Dify-Enterprise-Docs/{lang}/{X.Y.x}/develop/cli/` | `dify-cli-docs` |
| any other path | none; the writing guides govern |

Read now: `writing-guides/style-guide.md`; the pack's reader and vocabulary sections; the glossary rows for the surfaces in scope (`writing-guides/glossary.md`, by UI label, not the whole file).

## Understand before you write (S1–S3)

Read now: `writing-guides/index.md` § "Syncing the Dify codebase safely"; the pack's procedures labeled S2; `references/task-analysis.md`.

Pin the code ref first (for a pre-release feature, the development branch the user names) and verify every claim there. Existing docs are not evidence, because pages go stale, so a rewrite re-checks everything it keeps. Code presence is not a working feature either: behavior inferred from code rather than confirmed is reported as unverified and stays off the page, and so is a claim whose source you cannot reach, marked `UNVERIFIED` in the scope report and the PR description. The depth follows the job. A correction verifies the one disputed claim and records the evidence. An update runs `dify-docs-feature-research` at targeted depth on the surfaces the change touches. A new page, a rewrite, or a pre-release feature runs `dify-docs-feature-research` in full, and a rewrite re-verifies every claim carried over. Run the pack's S2 discovery and record each result, including "no match".

Write the research down as the drafter will need it: product vocabulary only, facts grouped by the reader's questions rather than by UI field, a "visible in the UI at the moment of use" list of what not to state, the actor named for every action, and no timing claims. Apply the reader test to the facts themselves: a fact enters the summary because the reader would ask for it here, and a fact that is merely true, or merely verified, goes on the "not on this page" list beside the unverified ones. The drafter mirrors the shape and vocabulary of what it is handed, and treats every fact on the summary as one to state, so the summary is where most of the leaving-out happens.

Then work out who arrives at this page and what they are trying to do, with `references/task-analysis.md`. Tasks come from the reader's own journeys through the product, not from the issue text or the code trace. For each task, note what they need before starting, what they will wonder mid-way, what they will overlook, and how they will know it worked. What the interface shows at that moment stays out; what it cannot show goes in. A question the docs cannot answer (a UI gap, a product gap) is reported, never papered over in prose.

For a `use-dify` page, both audience copies are in scope: shared improvements land in both, audience-specific blocks stay per copy (the guides pack has the rules).

## Agree the scope (S4)

Before drafting, report the pages and what will change on each, the research summary itself, the unverified claims, and the questions you are routing elsewhere, then stop for approval. Silent scope drift is the failure this guards against, and the summary is shown so the owner can strike facts a reader would not ask for before a drafter states them. A single-page correction, or a task arriving from an already-approved release-sync report, proceeds without the stop. When the scope offers a structural choice, give each option's reader impact and size before asking for a decision. A port into another tree is scoped from the feature's full footprint in the source tree (the union of its source PRs' file lists, a link sweep, and a name sweep), never from the target tree or a parked branch, and every footprint file gets an include, adapt, or exclude line. When no reviewer is in the session, put the report in the PR description and continue; the approval happens at PR review.

## Write (S5)

Read now: the pack's procedures labeled S5 and the references they name (page shape, conventions, style overrides). Then, last before the first sentence: the whole style guide, whose opening section "What a Good Page Does" is the standard and whose later sections carry the rules only a drafter can apply (plan badges, the Enterprise tip, how limits are phrased, location-first instructions); `references/drafting-turn.md`; and the reference page in the page's genre, `en/cloud/use-dify/build/new-agent/overview.mdx` for a concept page or `build.mdx` for a task page. A reference page (a CLI command, an API group, a node) takes `build.mdx` plus the pack's page shape: the pack decides the sections, tables, and conventions of its document type, and the sample decides only how the sentences inside them sound. The two pages calibrate register; the style guide is the authority when they differ.

For a new page or a rewrite, propose the outline first: the sections in the reader's order, and for each the reader question it answers. Exclusions need no defense; an inclusion that answers no question is the thing to defend. Stop for approval of the outline (the no-reviewer rule under Agree the scope applies), then hand the drafting to a fresh agent.

The session that did the research never drafts: its context is full of code vocabulary, tool output, and its own history, and the prose takes that register.

The drafter gets the filled-in reader block at the top of its turn, the research summary, the whole style guide, `references/drafting-turn.md`, the reference page in its genre, and the pack's page-shape and drafting sections, and nothing else. It names the judgment each section owes its reader, writes toward that rather than toward the fact list, drafts the page whole so the sections carry a through-line, and reads it back once before returning it.

Review the whole draft, then sort the corrections by one question: does this change what a unit is for, or only what a sentence says? A fact, a label, a link, a number, or a word: edit it directly. A sentence or paragraph reworked with its idea unchanged: rewrite that unit whole and read it back against the standard. A changed idea, a section or more, or the second round of corrections on the same unit: hand the draft, the corrections, the standard, and the reference page to a fresh drafter and run the editor test after, because by then this session holds the old framing and the discussion about it, and patches accumulate into prose written in three different contexts.

Uncertain content is left out and recorded, never hedged. Concept sections describe, task pages instruct. Frontmatter descriptions are written last, from the finished page.

## Translate (S6)

Read now: `tools/translate/formatting-zh.md`, `tools/translate/formatting-ja.md`, and the glossary.

Every English change ships `zh/` and `ja/` in the same pass. A new page is registered in all three navigation sections of `docs.json` in the same PR. The API pack edits its three specs directly and gates on its parity check.

Translate from the English file on disk as it stands, not from the draft in the conversation. After a review round, diff the English file and carry every changed sentence, structural edits included, into zh and ja; a stated sync is intent, not verified state, and a deletion of content you drafted is confirmed with the owner before it is mirrored. A page that already exists translated in a sibling tree is copied and adjusted (links, the disclaimer backlink, the audience-specific fragment), never re-translated. When the owner deletes from one translation, mirror the deletion in the other.

## Check (S7)

Read now: `writing-guides/formatting-guide.md`; the pack's procedures labeled S7.

1. Read it back per `references/drafting-turn.md` and fix what you find; a fault found once is swept across the page before it counts as fixed. Then run `dify-docs-editor-test` on the English page: a fresh agent reads the draft against the standard, the reference page, and the pack's page shape, and returns sentence-level marks and a verdict. The zh and ja pages are judged by the translation guides, not by this test. "Needs rewrite" means the unit is rewritten whole, not patched.
2. Run `dify-docs-format-check`, then `dify-docs-terminology-check`, then the pack's S7 verifiers, fixing and re-running until each is clean. A clean run is not a finished page.
3. Run `dify-docs-reader-test` last, on the finished page.

This applies to every edit, including a one-line correction made without the rest of this pipeline: check the work before presenting it. Process documents (plans, design notes) are exempt. If you skip or change a stage, say so and why.

## Close (S8)

Read now, if the page has a sibling copy in the other audience tree or an Enterprise version: that copy, for the propagation proposal.

Report what changed, what stays open (unverified claims, routed questions, follow-ups), any glossary additions, any pack reference or guide the work showed to be stale, and the sibling copies affected.
