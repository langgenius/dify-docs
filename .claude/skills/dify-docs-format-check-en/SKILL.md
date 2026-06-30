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

Verify English documentation against every rule in `writing-guides/formatting-guide.md`. Mechanical rules are enforced by a linter script (`check-format-en.py`); judgment-call rules are checked by reading the file.

## Before Starting

Audit the entire file, not just the diff. Default to files currently under review, detected via:

- `git diff --name-only` (unstaged changes in tracked files)
- `git diff --cached --name-only` (staged changes)
- Untracked files from `git status --porcelain` (lines starting with `??`)

Filter for `.mdx` and `.md` files under `en/`. If no files are detected, ask the user which files to check.

## Checks

### Part 1 — Deterministic (run the linter, paste the output)

Run the linter and paste its output into your report:

```bash
python3 .claude/skills/dify-docs-format-check-en/check-format-en.py <file> [<file> ...]
```

The script is the authoritative rule list. It prints one line per violation, grouped by file, as `line [rule-id] message`; the messages are self-describing, so do not re-summarize each rule. Rule IDs are prefixed by family: `F-` frontmatter, `H-` headings, `B-` bold/italic, `L-` lists, `C-` code, `Li-` links, `I-` images, `M-` Mintlify components, `U-` UI element references, `S-` spacing, `P-` punctuation.

Two IDs need context the message alone does not give:

- `H-ing-verb`: section-name gerunds (`Troubleshooting`, `Logging`, `Getting Started`, `Monitoring Data List`, etc.) are exempt via the `SKIP_ING_HEADINGS` constant in the script. If a flagged heading is a legitimate section concept, add it there.
- `I-alt-empty`: the script flags *every* empty alt as a prompt to confirm the image is genuinely decorative, not as a hard error.

### Part 2 — Judgment-call review (where your attention goes)

Part 1 is run-and-paste; this pass is where you actually read and reason. For each changed file, read it and look for:

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

Paste the script's raw output first, then append your judgment findings under each file. The script already groups by file and ends each file with either its violation lines or `✅ no deterministic issues found`; do not invent per-rule "clean" lines it never printed.

```
[script output, verbatim. Per file: "### {path}", then "line [rule-id] message"
lines, or "✅ no deterministic issues found", ending with "Total violations: {n}"]

### Judgment findings

**{path}**
- Line {n}: {description of issue} ({rule area})
- ...
```

If a file has no deterministic violations and no judgment findings, the script's `✅ no deterministic issues found` line stands on its own.

## Important

- Do NOT modify any files. This is a read-only audit.
- Report findings to the user for review.
- When the script flags a rule that looks like a false positive on inspection (e.g., an `-ing` verb that should have been in `SKIP_ING_HEADINGS`, or `_` that is a legitimate filename/identifier), surface it as a finding but note the ambiguity so the user can decide.
