---
name: dify-ux-copy
description: Draft and review UX copy for Dify product interfaces, especially new features and designs. Verify the user's moment, then draft against the copy standards. Use for new UI wording and design-copy reviews. For historical copy changes or cross-repository impact checks, use dify-ux-copy-edit.
---

# UX Copy

<!-- Adapted from langgenius/dify-docs-registry@abd6343051fb1e789fb23b6eee40b8563213fa00, skills/dify-ux-copy/SKILL.md. Original review procedure and worked example retained; routing, shared-resource paths, repository discovery, and punctuation adapted for dify-docs. -->

Copy work fails in two ways: polishing a sentence whose framing is wrong for the moment, and wording a string without knowing where and when it actually appears. Verify the string's reality first, then write.

## Procedure

1. **Scope and route.** New-copy drafting and design reviews enter here. Historical copy changes and impact-only requests enter through [dify-ux-copy-edit](../dify-ux-copy-edit/SKILL.md). A string that exists only in design files (Figma), or is being drafted from a PRD, skips steps 3 to 5: label every claim about it `design-only, unverified trigger`, source the moment from the design frame and PRD, and queue re-verification for when code exists. Ask for missing product facts before drafting.
2. **Read now**: [UX Copy Standards](../../../writing-guides/ux-copy-standards.md); [Glossary](../../../writing-guides/glossary.md), including "UI Labels", which carries the key-resolution mechanics steps 3 and 4 use. Identify the product clone and target ref available to the task. Pin the ref per [Syncing the Dify codebase safely](../../../writing-guides/index.md#syncing-the-dify-codebase-safely), and name it, or the live build, with every observation below. For design-only work, record the PRD/design source instead.
3. **Trace the key.** Discover the locale directory at the pinned ref: `web/i18n/locales/` or `web/i18n/`. Search the English value there with `git grep -nF`, using a distinctive fragment with `{{interpolations}}` and markup tags stripped; a pasted zh/ja string is searched in its own locale tree first to find the key. No hit after the stem retry → grep the components for the literal; still nothing → print `UNTRACED: <string>` and stop for that string. Never conclude "hardcoded or server-sent" from a failed search alone.
4. **List every render site.** Search the key with `git grep -nF` in the product's frontend source at the pinned ref, retrying without the namespace prefix (`menus.apps` for `common.menus.apps`) per the glossary section. Record file:line for every place the value can reach the screen, following indirection (a prop or config entry carrying the key, like `labelKey`, counts; `__tests__` files do not). The wording is judged in ALL of them (standards rule 10).
5. **Verify the trigger.** For each render site, read the surrounding code: what condition or event shows the string (preemptive client check, server error mapping, state flag), which product states can hold at that time, and what sits on screen beside it, from code where readable, otherwise from the live product, labeled as such. The trigger defines the user's moment; a wording judged without it is a guess.
6. **Reconstruct the moment and draft.** Name the screen, the task the user is mid-way through, and the question they want answered; draft against the standards. Every proposed change cites the rule it enforces; a string that violates none is left alone.
7. **Report and STOP.** Print `UX-COPY REPORT: <traced>/<total> strings traced, <n> findings` and present the proposals for review. Report design-only drafts separately from code-traced strings.

## Rules (apply throughout)

- Live product and screenshots outrank code inference; internal identifiers (route constants, config values, table names) are not the public contract; different environments run different builds. Name which one an observation came from.
- Every claim carries its evidence level: code-verified (with ref), product-observed (with build/environment), or design-only.
- zh/ja strings reuse the exact on-screen labels of the buttons, badges, and toggles they reference. Trace those sibling keys too; never re-translate the concept freshly.
- Keep product clones read-only for this review: propose strings in the report, never edit the clone or its i18n files.
- A string embedding a docs URL: verify the target page exists on the live docs (shipped surfaces) or will exist at launch (pre-release).
- Never post to trackers, PRs, or product channels yourself.

## Worked example (traced 2026-08-26, dify@main)

- String (PM paste): "This workflow version is deployed, or being deployed, to one or more environments. …"
- Step 3: value search hits `web/i18n/en-US/workflow.json` → key `versionHistory.action.deleteDeployedVersionError`.
- Step 4: key grep (no prefix to drop here) → one render site, `web/app/components/workflow/panel/version-history-panel/index.tsx:144`; a `__tests__` hit is excluded.
- Step 5: trigger is a client-side pre-check on the Delete menu action, fires when `item.environments?.length`, before any API call; environment badges are visible on the version row at that moment.
- Step 6: moment = version history, deleting a version, asking "why can't I?". Draft: "This version is deployed to one or more environments. Undeploy it from every environment before deleting it." Comma-interruption cut (rule 1); "workflow version" dropped because the key also renders for Chatflow apps (rule 10); the zh action verb becomes 下线, the button's own label (rule 11).
