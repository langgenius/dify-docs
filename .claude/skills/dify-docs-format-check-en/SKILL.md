---
name: dify-docs-format-check-en
description: >
  Check formatting compliance in changed English documentation against
  writing-guides/formatting-guide.md. Use after finalizing a draft, or when
  the user says "check formatting", "format audit", "format check" on English
  content.
---

# English Formatting Check

## Purpose

Verify changed English documentation against every rule in `writing-guides/formatting-guide.md`. Mechanical rules are enforced by a linter script (`check-format-en.py`); judgment-call rules are checked by reading the file.

## Before Starting

Detect changed documentation files by combining:

- `git diff --name-only` (unstaged changes in tracked files)
- `git diff --cached --name-only` (staged changes)
- Untracked files from `git status --porcelain` (lines starting with `??`)

Filter for `.mdx` and `.md` files under `en/`. If no changed files are detected, ask the user which files to check.

## Checks

### Part 1 — Deterministic (run the linter)

Run the linter and capture its output:

```bash
python3 .claude/skills/dify-docs-format-check-en/check-format-en.py <file> [<file> ...]
```

The script checks these rules. Each violation includes the file path, line number, rule ID, severity, and a short message.

**Frontmatter**

- `F-title-missing` — file lacks `title` field.
- `F-desc-trailing-period` — `description` ends with a period.
- `F-quote-needed` — value contains `: ` (colon + space) but is not quoted.
- `F-quote-unnecessary` — value is quoted but contains no character that requires quoting.
- `F-single-quote` — value uses single quotes; should use double.
- `F-blank-after-fm` — no blank line between closing `---` and body.

**Headings**

- `H-trailing-hash` — heading ends with a trailing `#`.
- `H-blank-before` / `H-blank-after` — missing blank line adjacent to a heading.
- `H-skip-level` — jump in depth (e.g., H2 to H4 without H3).
- `H-ing-verb` — heading starts with a verb in `-ing` form where the base form should be used. The linter carries a curated verb list and strips leading numeric/parenthetical prefixes (`1.`, `(a)`, etc.) before detection. Section-name gerunds in a skip list are not flagged (`Troubleshooting`, `Logging`, `Getting Started`, `Monitoring Data List`, etc.). The skip list lives in the script constant `SKIP_TEXTS`.

**Bold and Italic**

- `B-trailing-colon-inside` — `**X:**` or `**X：**` patterns. Colon must be outside the bold markers.
- `B-underscore-italic` — `_italic_` style; must use `*italic*`.

**Lists**

- `L-asterisk-bullet` — `* ` used as a bullet; must use `- `.
- `L-blank-before` / `L-blank-after` — missing blank line around a list block.
- `L-nested-indent` — nested list item not indented by a multiple of 2 spaces.

**Code**

- `C-no-language` — fenced code block opens with ` ``` ` but no language tag.
- `C-blank-before` / `C-blank-after` — missing blank line around a fenced code block.

**Links**

- `Li-click-here` — link text is `click here`, `here`, or `Click here`.
- `Li-http-external` — external link uses `http://` rather than `https://`.
- `Li-internal-no-prefix` — internal link starts with a relative path or omits the language prefix (`/en/...`).

**Images**

- `I-raw-img-tag` — raw `<img>` element used instead of `<Frame>` + markdown.
- `I-alt-empty` — `![](...)` with no alt text on a non-decorative image. The script flags every empty alt as a prompt to confirm the image is truly decorative.
- `I-alt-too-long` — alt text exceeds 125 characters.
- `I-caption-alt-mismatch` — `<Frame caption="...">` value differs from the alt text of the enclosed markdown image.
- `I-filename-uppercase-ext` — filename ends with an uppercase extension (`.PNG`, `.JPG`).
- `I-filename-retina-suffix` — filename contains `@2x`, `@3x`, or similar.
- `I-filename-default-tool` — filename begins with `CleanShot`, `Screenshot`, `IMG_`, etc.
- `I-filename-non-kebab` — filename has underscores, spaces, uppercase letters, or non-ASCII characters.
- `I-filename-ing-verb` — filename begins with a verb in `-ing` form.

**Mintlify Components**

- `M-tab-no-title` — `<Tab>` without a `title` attribute.
- `M-component-blank-before` / `M-component-blank-after` — missing blank line around `<Info>`, `<Tip>`, `<Note>`, or `<Warning>`.

**UI Element References**

- `U-menu-arrow` — menu path uses `→`, `->`, or `=>` instead of `>`.

**Spacing**

- `S-double-blank` — two or more consecutive blank lines.
- `S-trailing-whitespace` — line ends with whitespace.

**Punctuation**

- `P-em-dash-spaces` — em dash `—` surrounded by spaces.
- `P-en-dash-spaces` — en dash `–` surrounded by spaces in a numeric range.
- `P-fullwidth-in-english` — full-width punctuation (`，。；：！？（）、`) adjacent to ASCII letters.

### Part 2 — Judgment-call review (LLM reads each file)

For each changed file, read it and look for:

**Headings**

- **Title case**: every heading uses proper title case. Major words capitalized; minor words (`a`, `and`, `the`, `of`, `in`, `on`, `to`, etc.) lowercase except at the start. Flag any heading that reads as sentence case, all-lowercase, or inconsistent.

**Bold and emphasis**

- **Bold for UI elements and key terms only.** Running-text emphasis should be italic or restructured. Flag bold that isn't a UI label, a menu path, a tab/field name, or a first-use key term.
- **Double quotation marks not used for emphasis.** Flag `"word"` patterns used emphatically (not as direct quotations or literal-phrase references).

**Lists**

- **Numbered lists only for sequential steps.** If items are not ordered steps, they should be unordered (dashes).
- **Descriptive-list pattern**: `- **Label**: description.` A list where each item introduces a labeled concept should use this pattern.
- **Period consistency**: items are either all complete sentences (period) or all fragments (no period). Flag mixed styles within a list.
- **Child content indentation**: when a list item has an expanded description, callout, or image, it must be indented two spaces under that item.

**Links**

- **Descriptive link text**. Flag link text that is vague (`this page`, `here`) even when it isn't `click here` exactly.

**Images**

- **Alt text in title case, describes what the image communicates** (not its appearance). "LLM Node Configuration Panel" is correct; "Screenshot of a form" is not.
- **Comparison images** (two or more images shown together for comparison) each need a caption. The linter cannot detect image adjacency; check by reading.
- **Decorative `alt=""`** should be used only for images that carry no information. Confirm that any empty alt flagged by the linter is truly decorative.
- **Image storage path** under `/images/<tier-1>/<tier-2>/...` follows the content-domain taxonomy in the guide.
- **Filenames are descriptive and specific** (`workflow-llm-node-parameters.png`, not `workflow-01.png` or `screenshot.png`).

**Tables**

- Left-aligned with `:---`; bold used in header row only when it aids clarity.
- Multi-line cells: prefer lists or components; fall back to `<br/><br/><br/><br/>` when a manual break is unavoidable.

**General**

- Content inside Mintlify components reads cleanly (bold, links, etc. work as expected inside `<Info>`, `<Note>`, etc.).

## Output Format

```
## English Formatting Check Results

### File: {path}

**Deterministic violations** ({n})
- Line {n} [{rule-id}]: {message}
- ...

**Judgment-call findings** ({n})
- Line {n}: {description of issue} — {rule area}
- ...

**Clean checks**
- ✅ Frontmatter valid
- ✅ No deterministic violations in {area}
```

Group by file. If a file has no issues in any area, report a single ✅ line for it.

## Important

- Do NOT modify any files. This is a read-only audit.
- Report findings to the user for review.
- When the script flags a rule that looks like a false positive on inspection (e.g., `-ing` verb that should have been in `SKIP_TEXTS`, or `_` that is a legitimate filename/identifier), surface it as a finding but note the ambiguity so the user can decide.
