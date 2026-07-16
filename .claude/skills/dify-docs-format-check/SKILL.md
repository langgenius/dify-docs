---
name: dify-docs-format-check
description: >
  Check formatting compliance in changed documentation against
  writing-guides/formatting-guide.md and tools/translate/formatting-{zh,ja}.md.
  Routes by path: en/ files get the English linter and rules; zh/ and ja/
  files get the CJK linter and rules. Use after finalizing a draft or a
  translation batch, or when the user says "check formatting", "format
  check", "format audit", or "check CJK formatting".
---

# Formatting Check (en / zh / ja)

Read-only audit of documentation formatting. Mechanical rules are enforced by two linter scripts in this skill directory; judgment-call rules are checked by reading each file. Route by path:

| Files under | Linter | Judgment digest |
|:------------|:-------|:----------------|
| `en/` | `check-format-en.py` | Step 4 (English) |
| `zh/` | `check-format-cjk.py` | Step 5 (CJK shared + Chinese) |
| `ja/` | `check-format-cjk.py` | Step 5 (CJK shared + Japanese) |

## Procedure

1. **Read the rule sources** for the languages in scope. The digests in steps 4-5 are summaries of these files; wherever a digest and its source disagree, the source file wins.
   - `writing-guides/formatting-guide.md` — all languages
   - `tools/translate/formatting-zh.md` — when any `zh/` file is in scope
   - `tools/translate/formatting-ja.md` — when any `ja/` file is in scope

2. **Detect the files to audit.** Audit entire files, not just diffs. Default to the files currently under review:

   ```bash
   git diff --name-only; git diff --cached --name-only; git status --porcelain | grep '^??'
   ```

   Keep `.mdx`/`.md` files under `en/`, `zh/`, or `ja/`. If none are detected, ask the user which files to check. Translations ship as a zh/ja pair from one English source, so when both changed, audit both in the same session.

3. **Run the linter for each path group and paste its output verbatim** into your report:

   ```bash
   python3 .claude/skills/dify-docs-format-check/check-format-en.py <en files...>
   python3 .claude/skills/dify-docs-format-check/check-format-cjk.py <zh and ja files...>
   ```

   Success signal: each run prints one block per file and ends with `Total violations: {n}`; exit code is 0 when n = 0, 1 otherwise. A file passed to the wrong script is skipped with a stderr note (`skip (non-en)` / `skip (non-zh/ja)`); `check-format-cjk.py` selects the zh or ja rule set from the file path.

   The scripts are the authoritative deterministic rule list. Violation lines print as `line [rule-id] message` and the messages are self-describing, so do not re-summarize each rule. Rule-ID families: `F-` frontmatter, `H-` headings, `B-` bold/italic, `L-` lists, `C-` code, `Li-` links, `I-` images, `M-` Mintlify components, `U-` UI element references (en only), `S-` spacing, `P-` punctuation, `CJK-` both CJK languages, `ZH-` Chinese only, `JA-` Japanese only.

   Four IDs need context the message alone does not give:

   - `H-ing-verb` (en): section-name gerunds (`Troubleshooting`, `Logging`, `Getting Started`, etc.) are exempt via the `SKIP_ING_HEADINGS` constant in `check-format-en.py`. If a flagged heading is a legitimate section concept, propose the addition to `SKIP_ING_HEADINGS` in your report — do not edit the script.
   - `I-alt-empty` (en): flags every empty alt as a prompt to confirm the image is genuinely decorative, not as a hard error.
   - `CJK-disclaimer-missing`: the script looks for the translation disclaimer only within the ~10 lines below the frontmatter, so a disclaimer placed lower in the file still trips it.
   - `CJK-cross-lang-link`: `/en/...` links are flagged everywhere except on the disclaimer line, which is allowed to point at the English source.

4. **Judgment review — `en/` files.** Digest of `writing-guides/formatting-guide.md` (section names in parentheses; the guide wins on conflict). Read each file and check:

   - **Headings** (§Headings): proper title case — major words capitalized, minor words (`a`, `and`, `the`, `of`, `in`, `on`, `to`, etc.) lowercase except at the start. Flag sentence case, all-lowercase, or inconsistency.
   - **Bold and emphasis** (§Bold and Italic, §Quotation Marks): bold only for UI elements, menu paths, tab/field names, and first-use key terms; running-text emphasis is italic or restructured. Flag `"word"` used emphatically rather than as a quotation or literal-phrase reference.
   - **Lists** (§Lists): numbered lists only for sequential steps, otherwise dashes; labeled-concept items use `- **Label**: description.`; items are all sentences (period) or all fragments (no period), never mixed; child content (description, callout, image) indented two spaces under its item.
   - **Links** (§Links): descriptive link text — flag vague text (`this page`, `here`) even when it isn't `click here` exactly.
   - **Images** (§Images: Alt Text, Captions, Storage, Naming): alt text in title case describing what the image communicates ("LLM Node Configuration Panel", not "Screenshot of a form"); comparison images shown together each need a caption (the linter cannot detect adjacency); `alt=""` only for genuinely decorative images; storage path follows the `/images/<tier-1>/<tier-2>/...` taxonomy; filenames descriptive and specific (`workflow-llm-node-parameters.png`, not `screenshot.png`).
   - **Tables** (§Tables): left-aligned with `:---`; bold in header row only when it aids clarity; multi-line cells prefer lists or components, falling back to `<br/>` only when a manual break is unavoidable.
   - **Mintlify components** (§Mintlify Components): content inside `<Info>`, `<Note>`, etc. reads cleanly (bold, links work as expected).

5. **Judgment review — `zh/` and `ja/` files.** Digest of `tools/translate/formatting-zh.md` and `tools/translate/formatting-ja.md` (those files win on conflict). The two findings the linter misses most often are **translated anchor slugs** and **`{{placeholder}}` variables left unchanged** in otherwise-translated prompts. Read each file and check:

   - **Translatable elements** (§Translatable Elements, both files): Tab titles (`<Tab title="...">`), Frame captions, and image alt text translated; bold UI labels translated; natural-language prompt examples inside code blocks translated with variable placeholders (`{{variable_name}}`) left unchanged.
   - **Anchors** (§Cross-Reference Anchors, both files): `[text](#anchor)` and `[text](/path#anchor)` use the translated heading slug — the heading `## 响应` produces `#响应`, not `#response`.
   - **Chinese style** (`formatting-zh.md`): enumeration comma `、` for parallel items within a sentence (§Enumeration Comma); ellipsis `……` used correctly and not combined with `等` in one phrase (§Ellipsis); Arabic numerals for technical content (`3 种`, not `三种`) with idiomatic expressions as the judgment call (§Numbers); translationese — redundant `你的`, unnecessary `会`, `当...时` wrappers, `能够` for `能`, `可以` where `可` suffices (§Translation Quality → Patterns to Eliminate).
   - **Japanese style** (`formatting-ja.md`): `です/ます` maintained in body text (§Writing Style, §Honorifics); headings are noun phrases, not sentences (§Headings); short loanwords (3 morae or fewer) keep the trailing `ー`, longer ones drop it, and established compounds (ワークフロー, ナレッジベース) match the glossary (§Katakana Conventions); middle dot `・` only where readability needs it, none inside established compounds (§Middle Dot); translationese — redundant `あなたの`, `〜することができます` for `〜できます`, `〜とき/〜場合` wrappers, stacked `の` (§Translation Quality → Patterns to Eliminate).

6. **Report.** Paste the raw linter output first, then append judgment findings per file:

   ```
   [linter output, verbatim — per file: "### {path}" (the cjk script adds
   " ({lang})"), then "line [rule-id] message" lines or "✅ no deterministic
   issues found", each run ending with "Total violations: {n}"]

   ### Judgment findings

   **{path}**
   - Line {n}: {description of issue} ({rule area})
   ```

   The scripts report only violations; do not invent per-rule "clean" lines they never printed. A file with no violations and no judgment findings needs nothing beyond its `✅ no deterministic issues found` line.

## Important

- Do NOT modify any files. This is a read-only audit: report findings, including any proposed `SKIP_ING_HEADINGS` additions, for the user to review and apply.
- When a flagged item is clearly intentional on inspection (an `-ing` heading that belongs in `SKIP_ING_HEADINGS`, a `_` in a legitimate filename or identifier, a half-width comma inside a Latin acronym, a mainland quotation mark quoted from an external source), surface it but note the ambiguity so the user can decide.
- Glossary and UI-label wording verification is `dify-docs-terminology-check`'s job — do not check terms against the glossary or codebase i18n files here. When a finding overlaps terminology, note it and point the user at that skill.
- The Japanese sentence-length and style-mix checks (`JA-sentence-too-long`, `JA-style-mix`) are heuristic: they flag candidates for human review, not definitive violations.
