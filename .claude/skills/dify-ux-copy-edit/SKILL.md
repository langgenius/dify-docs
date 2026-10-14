---
name: dify-ux-copy-edit
description: Investigate and revise existing Dify UI copy using an issue document, visible string, i18n key, or committed diff. Check reuse, translations, tests, and documentation impact before proposing changes. Use for historical copy fixes and impact-only checks; use dify-ux-copy for new-copy drafting and design reviews.
---

# UX Copy Revision and Impact Review

<!-- Extracted from the impact-review extension developed in dify-docs PR #1098. Contextual review principles derive from langgenius/dify-docs-registry@abd6343051fb1e789fb23b6eee40b8563213fa00, skills/dify-ux-copy/SKILL.md. -->

Verify where and when a string appears before proposing wording. A useful proposal answers the user's immediate question and remains accurate wherever the string is used.

## Procedure

1. **Scope the requested changes.** Read the supplied issue document and screenshots, or the individual string/key/diff. Identify the product, language, target items, and available PRD, design, code, or live environment. Keep the issue identifiers in the report so findings can be matched back to the document. Ask for an export when the document cannot be read. For new copy without an implementation, use [dify-ux-copy](../dify-ux-copy/SKILL.md). For a documentation page, use the repository's `dify-docs-write` pipeline.
2. **Read the shared sources.** Read [UX Copy Standards](../../../writing-guides/ux-copy-standards.md), the relevant [Glossary](../../../writing-guides/glossary.md) entries, and its “UI Labels” section. General terms define concepts; UI-label entries record observed interface text. Identify the product repository available to the task and record the commit or working-tree state being inspected. Follow [safe codebase inspection](../../../writing-guides/index.md#syncing-the-dify-codebase-safely) when fetching or reading another ref.
3. **Resolve the target before editing.** Read [Targeted impact lookup](references/impact-lookup.md) and run the bundled collector in `lookup` mode with a known key or the complete visible string. This needs one product snapshot, not a change or PR. For Chinese or Japanese input, select that locale. If multiple keys match, use the page, screenshot, or rendering component to identify the intended key; ask for that context when absent. Never select the first match by default. On no match, inspect other locales, hardcoded strings, and runtime composition; label unresolved targets `UNTRACED` and pause proposals for those targets until identified.
4. **Verify the collected impact candidates.** Read the report, then inspect code to establish where and when the target renders. Trace namespace-relative keys, selectors, props, configuration, shared components, and callers beyond the script's direct-import candidates. Separate verified render sites from text matches and unresolved dynamic usage. Review related-copy and test-text candidates: confirm whether other prompts reference the renamed object, and whether test locators, assertions, or snapshots depend on its wording. Text matches do not establish a dependency. Check the reported translation entries without inferring translation quality from presence. Confirm the documentation search scope with the documentation engineer; review candidate names, steps, help links, and images for references to the same UI object. Record required documentation updates and unverified images separately. For changes already committed, use the collector's `diff` mode and follow references beyond the PR diff.
5. **Verify the user's moment.** At each site, check which event or condition shows the string, which product states are possible, and the nearby labels and actions. Use available UI evidence to verify runtime behavior. For dynamic copy, check the complete rendered sentence with 0, 1, and multiple objects, empty values, and long names where applicable; record which cases were checked and which remain unverified. Review screenshots or a running interface at representative widths; text length alone cannot establish whether copy fits. Compare visible control text with its accessible name (`aria-label`, `aria-labelledby`, or visible text) so they describe the same action or object. Record unverified visual, state, or accessibility coverage explicitly.
6. **Draft when requested.** For an impact-only request, continue to the report. When wording is requested, state the screen, task, and immediate question, then propose copy with the relevant standard and evidence. Assess shared keys in every verified context. When contexts require different meanings, propose a key split. Trace referenced action labels in each locale, preserve interpolation and markup contracts, and leave wording that already meets the standard unchanged.
7. **Present findings for review.** Include the target key and original copy, affected locations with evidence, unresolved coverage, proposed wording when requested, and related-copy, test, translation, and documentation updates to consider. PM, design, and documentation collaborators confirm context-sensitive wording and impact; engineering supplies implementation facts. Print `UX-COPY REPORT: <traced>/<total> strings traced, <n> findings`, counting verified targets rather than script matches. For an impact-only request, report the evidence and stop. Implement only when requested and the relevant decisions are confirmed. After an authorized implementation, run the relevant tests using the repository's documented commands and report the command and result; distinguish expected wording updates from behavioral regressions instead of replacing assertions or snapshots blindly.

## Evidence and scope

- Name the commit, working-tree changes, design frame, or live build behind each observation. If evidence comes from different versions, report the mismatch.
- Label findings as code-verified, product-observed, or design-only. A code inference does not establish visual fit or observed runtime behavior.
- Keep user-facing wording grounded in product behavior. Verify consequences, permissions, and limits against the task's product evidence.
- Use the exact visible action labels when referencing nearby buttons, badges, or toggles, including in Chinese and Japanese.
- Verify linked help pages against the relevant docs environment or confirmed launch content.
- Keep research read-only. Implementation, PR comments, tracker updates, and channel messages require the corresponding user request.

## Example: a shared deletion message

Suppose a deletion-blocking message appears in both Workflow and Chatflow version histories, and verified code shows it before a delete request when the selected version is deployed. “This workflow version…” narrows the object incorrectly for one of those surfaces. “This version…” fits both. The recovery instruction must use the verified action label for removing the deployment. Verify both contexts and the action before proposing the final sentence.

## Using this skill in another agent

Keep access to the shared Glossary and UX Copy Standards when configuring this skill in another agent. Adapt resource paths to that host. Record the docs revision used for the task so a finding can be traced back to its rule source.
