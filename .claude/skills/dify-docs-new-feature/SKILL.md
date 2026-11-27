---
name: dify-docs-new-feature
description: Additions to the dify-docs-write pipeline for documenting a feature that has not shipped yet, while its spec, design, and code still disagree. Adds source intake with a trust order, parallel research lanes with a reconcile report, sorting of open questions, information-architecture options, per-page translation, and re-verification on a test build. Triggers: "document this unreleased feature", "write docs for [feature]" when the feature is in no release.
---

# Documenting an Unreleased Feature

An unreleased feature is documented while its spec, design, and code disagree with each other and its scope still moves. Run the pipeline in `.claude/skills/dify-docs-write/SKILL.md` with the additions below layered onto its stages. This skill only adds or, where marked, modifies: the pipeline's stages and gates all apply. For a change to a feature that has already shipped, run the pipeline alone.

**Reading:** this file fully, then the pipeline skill, which names each stage's reading.

## S1 additions: source intake

1. Collect every source and date each one: the spec or PRD, the UI design file (Figma, for example), the tracker's issues and milestones for the feature, the code branch or pull request, design docs inside the code repository, and the docs of the feature this one replaces or extends. Ask the owner for any you cannot reach.
2. Build the source table (source | date | authoritative for) and set the trust order. Normally: code at a pinned ref > design and traceability docs in the repository > the UI design file > the spec. The newest evidence you can verify wins. Record each source's stale claims as you find them.
3. Sweep the code branch for design docs first (`docs/`, `*/docs/`, READMEs, traceability matrices): they are usually fresher than the spec and far cheaper than reading code.
4. Read the tracker before the code: issue titles reveal the architecture and what was cut, and milestones reveal the dates the docs must meet. Read each issue's comment thread as well as its description, because engineers record behavioral constraints there that the description omits (what a control blocks while it is on, what a migration skips). Record each such remark as a lead to verify at the pinned ref, never as a fact.
5. Pin the ref at a fixed commit of the development branch and read it as `writing-guides/index.md` § "Syncing the Dify codebase safely" describes. Every claim records the ref it was verified against. Never research a moving branch tip.
6. Start the project's research record now, before any research: the source table, then findings, decisions, open questions, and the fill-in list (each thing the pages still owe, with the event that will resolve it). Keep it where the owner says, outside the docs repository, and never commit it. Update it at the end of every pipeline stage, so a new session can continue from the record alone.

## S2 additions: parallel lanes and reconcile

7. Instead of a single feature-research run, dispatch read-only research agents in parallel, one per lane. Scale the lanes to the feature; four is typical. Where the host has no sub-agents, run the lanes one after another.

| Lane | Reads | Reports |
|:--|:--|:--|
| Backend and service | new service code and its in-repo docs | domain model, states, limits, flags |
| Platform integration | routes, permissions, config, migrations | what UI and API callers can do; how it's gated |
| Frontend and contract | UI code, API contract, e2e specs, i18n | what UI exists against what's promised; string inventory |
| Community | the predecessor feature's issues and discussions | pain themes, framed as tasks, with issue numbers |

8. Every lane brief requires: file-path evidence for every claim, explicit "inferred, unverified" flags, a status for each concept (present, renamed from X, removed, deferred), and the pinned ref from step 5.
9. While the lanes run, map the UI design file's structure (sections, then screens, then states) before taking screenshots, and screenshot only the screens that raise questions.
10. Reconcile into four deliverables:
    - a concept table: spec term, current name, status, evidence
    - a corrections list: where each older source is wrong
    - a surface-state table: spec, design, backend, and shipped UI side by side, each with its age
    - a gate ledger: for each surface that can ship, where its availability switch lives (a frontend gate or flag with its file path, a backend enum or route, a Helm or Compose value if any) and what "on" looks like, at the pinned ref. Gate state at drafting time is not an availability verdict, because development may simply be unfinished; the ledger exists so release time can assert it cheaply.
11. Report to the owner and stop. This is an extra gate before the pipeline's S3: no task analysis, information architecture, or drafting until the corrections are reviewed.

## S3 additions: sorting open questions

12. Run the pipeline's task analysis at full depth as written, building the question list jointly with the owner: walk each journey asking "what does the user wonder at this moment?", merge in the owner's own questions, and answer at once whatever the evidence already answers.
13. Sort every open question into exactly one bucket:
    - **ask the developers now**: draft the questions for the owner to send, and never contact anyone yourself
    - **verify on a test build**: write that checklist now, before the build exists
    - **docs commitment**: onto the fill-in list

## S4 addition: information architecture options

14. Propose information architecture (IA) options with their concrete impact on the reader and their page counts, and recommend one. The S4 stop covers this choice. Prefer permanent slugs, URLs that survive the feature's future, over transitional ones.

## S5 addition: links from the UI

15. At S5 entry, before any section is drafted, record every docs URL the feature's UI embeds and confirm each has a target page that will exist at launch. A link with no target at launch goes to the owner as a UI finding.

## S6 modification: per-page translation

16. Translate per page, never per section: the pipeline's English freeze happens page by page as each page's English stabilizes, and the translation test runs once per page as it is translated.

## S7 additions: test build

17. When a test build exists, run the checklist from step 13, resolve the fill-in list, and re-verify every claim inferred from code that reached a draft. A flag observed on in a test build is evidence about that build only, because test environments often force flags on. Never state availability from a test build: record each flag's source and default in the gate ledger, so the release's docs can be checked against that release's defaults.
18. Anything you run on your own machine to research the feature (a CLI, a local build, a package manager, a runtime) runs isolated from its first command, version and help probes included: an empty environment, a fake `HOME`, and its own config folder. The `dify-cli-docs` pack's "Live tests (S2)" section shows the pattern for `difyctl`. Report any call that ran outside it with the exact paths it touched, and offer cleanup instead of doing it unasked.

## S8 addition: close-out

19. Resolve the fill-in list, or carry each remaining item with the event that will resolve it. The pipeline's S8 covers glossary additions and the closing report.
