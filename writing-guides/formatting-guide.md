# Dify Documentation Formatting Guide

This document defines the formatting standards for Dify documentation. Contributors can load this guide into an AI assistant to automatically check and fix formatting issues during the writing process.

> **For AI assistants:** When a contributor asks you to review their documentation, check every rule in this guide and report violations with line-level references. When asked to fix formatting, apply all rules in a single pass.

---

## Frontmatter

Every MDX file must start with YAML frontmatter containing at least `title` and `description`:

```yaml
---
title: Page Title
description: A concise summary of what this page covers
---
```

- `title` is **required**. `description` is required for new pages; existing pages should be updated over time.
- `description` should not end with a period.
- `sidebarTitle` is optional. Add it when the title is too long for the sidebar, or when other pages in the same group follow a specific `sidebarTitle` convention.
- Leave values unquoted by default. Wrap a value in double quotes only when it contains a colon followed by a space, for example `title: "Step 1: Create Knowledge Pipeline"`. Without the quotes, YAML will misread everything after the colon.
- Leave one blank line after the closing `---` before the document body.

---

## Headings

- Use **title case**: `## Model Selection and Parameters`, not `## Model selection and parameters`.
- Page titles and section titles starting with a verb should use the base form (imperative), not the "-ing" form: `## Create a Workflow`, not `## Creating a Workflow`.
- Use H2 (`##`) for major sections, H3 (`###`) for subsections, H4 (`####`) for deeper subsections.
- Do not skip heading levels (e.g., don't jump from H2 to H4).
- One blank line before and after each heading.
- Do not add a trailing `#` to headings.

---

## Bold and Italic

### Bold (`**text**`)

Use bold for:

- **UI elements**: button names, menu items, tab labels, field names.
  - Example: `Click **Save and Authorize** to confirm.`
- **Key terms** when first introduced or when emphasis is critical.

Do not use bold for general emphasis in running text. If everything is bold, nothing stands out.

Do not include trailing punctuation (colons, commas, periods) inside bold markup. Write `**Upload Method**:` not `**Upload Method:**`.

### Italic (`*text*`)

- Always use single asterisks (`*text*`), never underscores (`_text_`).
- Use sparingly — for semantic emphasis, alternative phrasings, or example values.
  - Example: `Both plugin triggers and webhook triggers make your workflow *event-driven*.`

### Quotation Marks

- Do not use double quotation marks for emphasis. Use italics instead.
- Use double quotation marks for direct quotations and for referring to literal words or phrases when backticks are not more appropriate.

---

## Lists

- Use dashes (`-`) for unordered lists, not asterisks (`*`).
- Use numbered lists (`1.`, `2.`, `3.`) only for sequential steps.
- Leave a blank line before the first list item and after the last.
- For descriptive lists, use the **bold label + colon** pattern:

```markdown
- **Delivery method**: How the request form reaches recipients.
- **Form content**: What information recipients will see.
```

- End list items with a period when they are complete sentences or clauses. Omit periods for short phrases or fragments.
- Nested lists: indent with 2 spaces.
- If an expanded description, callout, or image belongs to a specific list item rather than the main body text, indent it with two spaces below that item to ensure correct rendering.

---

## Code

### Inline Code

Use backticks for:

- Variable names: `` `{{variable_name}}` ``
- File paths and extensions: `` `.env` ``, `` `docker-compose.yml` ``
- Configuration values: `` `streaming` ``, `` `true` ``
- Special characters and delimiters: `` `\n\n` ``
- Exact strings a user must type or match: `` `yes` ``, `` `DELETE` ``

Do not use backticks for product names, UI labels, or general English words.

### Code Blocks

- Always specify a language tag: `` ```python ``, `` ```bash ``, `` ```json ``, `` ```text ``.
- Use `` ```text `` for plain text, prompts, or output that isn't code.
- One blank line before and after the code block.
- No indentation inside code blocks (start at column 0).

---

## Links

### Internal Links

- Use absolute paths from the language root: `[Link text](/en/path/to/page)`
- Include anchor references when linking to a specific section: `[Retrieval Settings](/en/use-dify/knowledge/create-knowledge/setting-indexing-methods#setting-the-retrieval-setting)`
- Use descriptive link text. Never use "click here" or "here" as link text.

### External Links

- Use full URLs: `[Dify Marketplace](https://marketplace.dify.ai/)`
- Ensure all external links are HTTPS.

---

## Images

For editorial guidance on whether to include an image at all, see the [Style Guide](./style-guide.md#images). The rules below cover mechanics only.

### Syntax

Use a `<Frame>` component wrapping a markdown image. This gives responsive sizing, consistent visual styling, and proper caption support. Do not use raw `<img>` tags.

```mdx
<Frame>
  ![LLM Node Overview](/images/use-dify/workflow/llm-node-overview.png)
</Frame>
```

### Alt Text

Every image must have descriptive alt text. Alt text is read by screen readers and shown when an image fails to load.

- Use **Title Case**, matching the convention for headings and UI element references.
- Describe what the image communicates in context, not its visual appearance. "LLM Node Configuration Panel" is better than "Screenshot of a form with dropdowns."
- Keep alt text under 125 characters. Screen readers truncate beyond that length.
- Use `alt=""` (empty) for purely decorative images that carry no information. This is rare in documentation.

### Captions

Captions are visible to every reader; alt text is a fallback for screen readers and broken-image cases. They differ in visibility, but they describe the same image, so they should say the same thing.

- Required when two or more images are presented together for comparison. Each image in the set needs a caption identifying what it shows, so readers can tell the images apart without inferring from context.
- Optional elsewhere.
- Use **Title Case** for captions.
- **When a Frame has a caption, the alt text must match the caption exactly.** If you cannot think of a reason the two should differ, they should be identical.

```mdx
<Frame caption="Correct: Highlight Used for Emphasis">
  ![Correct: Highlight Used for Emphasis](/images/shared/emphasis-highlight.png)
</Frame>

<Frame caption="Incorrect: Bounding Box Used for Emphasis">
  ![Incorrect: Bounding Box Used for Emphasis](/images/shared/emphasis-box.png)
</Frame>
```

### Storage

All new images go in `/images/`, organized by **content domain**, not by where the image is referenced from. A content domain is a stable topical area that outlives nav reshuffles and physical folder refactors.

### Tier 1: top-level dropdown

Matches the four top-level dropdowns in `docs.json`, plus `shared/` for cross-section assets:

- `images/use-dify/`
- `images/develop-plugin/`
- `images/self-host/`
- `images/api-reference/`
- `images/shared/`

### Tier 2: content domain

A **closed list** of topical subfolders within each tier-1 section. Contributors choose from this list. Adding a new tier-2 folder requires a writing team discussion; do not create ad-hoc folders.

**`images/use-dify/`**

- `get-started/` — introductions, concepts, onboarding visuals
- `workflow/` — workflow and chatflow authoring, nodes (including agent nodes), debug
- `basic-app/` — agent apps, chatbot apps, completion apps, and other non-workflow app types
- `knowledge/` — knowledge bases, documents, retrieval, indexing
- `monitor/` — monitoring dashboards, logs, analytics
- `publish/` — publishing apps, WebApp chrome, API access, conversation features
- `tutorial/` — step-by-step guides, multi-lesson series
- `workspace/` — team settings, credentials, model providers, billing

**`images/develop-plugin/`**

- `get-started/`
- `dev-guide/` — plugin development walkthroughs
- `specs/` — schemas, manifests, specifications
- `publish/` — marketplace listing and release

**`images/self-host/`** and **`images/api-reference/`**

Flat within the tier-1 folder for now. Tier-2 will be added when content volume justifies it.

### Tier 3: per-tutorial subfolders and rare promotions

Tier-3 subfolders apply in two cases.

**Tutorials always get their own tier-3 subfolder, regardless of image count.** Each tutorial is a self-contained unit, and its images do not mix with images from other tutorials. For multi-lesson series like Workflow 101, each lesson is its own tier-3 subfolder.

- `images/use-dify/tutorial/simple-chatbot/` — single-page tutorial, one folder
- `images/use-dify/tutorial/workflow-101-lesson-01/` — multi-lesson series, one folder per lesson

**Other tier-2 folders may earn a tier-3 promotion** when they accumulate roughly 30 or more images AND the excess is a self-contained sub-area. For smaller sub-areas, use a filename prefix instead of a new folder. For example, `workflow/trigger-schedule-config.png` rather than `workflow/trigger/schedule-config.png` when there are only a handful of trigger images.

Promotions to tier-3 require updating every reference to every image in the affected sub-area, across `en/`, `zh/`, and `ja/`. Use the migration tooling at `tools/image-migration/` if it exists, or script the rename pass to keep references in sync.

### When a folder path provides context, do not repeat it in filenames

When an image lives inside a descriptive subfolder, the filename should not duplicate the folder's context. Inside `images/use-dify/tutorial/workflow-101-lesson-02/`, the file is `start-node.png`, not `workflow-101-lesson-02-start-node.png`. The folder path already says what lesson and series the image belongs to.

This applies most strongly to tier-3 tutorial folders where the folder name encodes the tutorial identity. In tier-2 folders where the subfolder is a broad domain like `workflow/`, filenames may still need a domain-specific prefix for grep-friendliness.

### Legacy CDN images

Do not commit new images from external CDNs to the repo. Existing CDN-hosted images (`assets-docs.dify.ai`) remain as legacy; all new images are local.

### Naming

Format: `[descriptive-name].[extension]`, optionally with a module prefix and a two-digit sequence suffix.

- **kebab-case, lowercase, ASCII only.** No underscores, spaces, Chinese characters, parentheses, or special characters (`@`, `&`, and so on).
- **Lowercase file extensions.** `.png`, not `.PNG`. `.jpg`, not `.JPG`.
- **No retina suffixes in filenames.** Strip `@2x`, `@3x`, and similar designators. They describe display metadata, not content. The file may still be a 2x asset; the filename does not need to advertise it.
- **Descriptive and specific.** `workflow-llm-node-parameters.png` beats `workflow-01.png` or `screenshot.png`.
- **Base-form verbs.** `configure-load-balance`, not `configuring-load-balance`. Matches the heading convention.
- **Module prefix is optional** when the subfolder already provides scope. Use a prefix when the filename alone would be ambiguous out of context, or when you want grep-friendly grouping within a subfolder.
- **Numeric suffix only for genuine sequences.** Use `01`, `02`, `03` (zero-padded to two digits) only when multiple images share the same module and description and need ordering. Zero-padding ensures natural sort order. Do not use numeric suffixes as a shortcut for lazy naming.

Examples:

- ✅ `images/use-dify/workflow/llm-node-overview.png`
- ✅ `images/use-dify/workflow/llm-configure-parameters-01.png`
- ✅ `images/use-dify/tutorial/workflow-101-lesson-02/start-node.png`
- ✅ `images/develop-plugin/publish/marketplace-submit-form.png`
- ❌ `images/use-dify/workflow/llm_node_overview.png` (underscores)
- ❌ `images/use-dify/workflow/CleanShot2025-07-07at07.28.04@2x.png` (default tool name, retina suffix, special characters)
- ❌ `images/use-dify/workflow/llm-node-overview.PNG` (uppercase extension)
- ❌ `images/use-dify/workflow/screenshot-01.png` (not descriptive)

Rename default tool outputs (`CleanShot*`, `Screenshot*`, `IMG_*`) before committing.

### File Format and Size

- **PNG** for UI screenshots.
- **SVG** for icons, logos, and diagrams.
- **MP4 or WebP** for motion. Avoid GIF for static images; use GIF only when you need autoplay in contexts that do not support video.
- Avoid JPEG for documentation screenshots. JPEG compression artifacts degrade UI detail.
- Capture screenshots at **2x resolution** (Retina) so they render sharply on high-DPI displays.
- Compress before committing (TinyPNG, squoosh, or equivalent). Target under 500 KB per image where feasible.

---

## Mintlify Components

### Info, Tip, Note, Warning

Use these for callouts instead of italics or raw text. Each serves a different purpose:

| Component | When to use |
|:----------|:------------|
| `<Info>` | General informational content—helpful context, version-specific or deployment-specific details |
| `<Tip>` | Helpful suggestions or shortcuts |
| `<Note>` | Important information that requires attention—missing it could lead to potential complications |
| `<Warning>` | Actions that could cause errors or data loss |

Format:

```mdx
<Info>
Configure at least one model provider in **System Settings** > **Model Providers** before using LLM nodes.
</Info>
```

- One blank line before and after the component.
- Content inside can include bold, links, and other inline formatting.

### Tabs

Use for presenting alternatives (e.g., different methods, OS-specific instructions):

```mdx
<Tabs>
  <Tab title="Visual Editor">
    Content for this tab.
  </Tab>
  <Tab title="JSON Schema">
    Content for this tab.
  </Tab>
</Tabs>
```

- Each `<Tab>` must have a `title` attribute.

### Steps

Use for sequential procedures:

````mdx
<Steps>
  <Step title="Clone Dify">
    Clone the source code to your local machine.

    ```bash
    git clone https://github.com/langgenius/dify.git
    ```
  </Step>
  <Step title="Start Dify">
    Navigate to the docker directory and start the containers.
  </Step>
</Steps>
````

### Accordion

Use for optional or supplementary content:

```mdx
<Accordion title="What is a webhook?">
  A webhook allows one system to automatically send real-time data to another system.
</Accordion>
```

### CodeGroup

Use for showing multiple code variants of the same operation:

````mdx
<CodeGroup>
  ```bash Docker Compose V2
  docker compose up -d
  ```
  ```bash Docker Compose V1
  docker-compose up -d
  ```
</CodeGroup>
````

---

## Tables

- Left-align columns by default using `:---`.
- Use bold for header row content only when it adds clarity.
- For multi-line content within cells, prefer lists or components. When manual line breaks are needed, use `<br/><br/><br/><br/>` between lines.
- Mintlify components (`<Info>`, `<Note>`) can be embedded within table cells when necessary.

```markdown
| Setting       | Description                              |
|:--------------|:-----------------------------------------|
| **Name**      | Identifies the knowledge base.           |
| **Description** | Indicates the knowledge base's purpose.|
```

---

## UI Element References

| Element type | Format | Example |
|:-------------|:-------|:--------|
| Buttons | Bold | `**Save and Authorize**` |
| Menu paths | Bold with arrow | `**System Settings** > **Model Providers**` |
| Tab/section names | Bold | `**Quick Settings**` |
| Field names | Bold | `**Temperature**` |
| Status indicators | Bold | `**Edited**`, `**Healthy**` |

- Use the arrow character `>` (not `→`, `->`, or `=>`) for menu paths.

---

## Spacing

- **One blank line** between paragraphs, before/after headings, before/after components, before/after code blocks.
- **No double blank lines** anywhere in the file.
- Do not leave trailing whitespace at the end of lines.

---

## Punctuation

- **Em dashes**: No spaces around em dashes — write `word—word`, not `word — word`.
- **En dashes**: No spaces around en dashes in ranges — write `2–4`, not `2 – 4`.

---

## Quick Checklist

Before submitting, verify:

- [ ] Frontmatter has both `title` and `description`
- [ ] Headings use title case; verb-leading titles use imperative form
- [ ] Headings follow the correct hierarchy (H2 → H3 → H4)
- [ ] Bold is used for UI elements and key terms
- [ ] Italics use `*asterisks*`, not `_underscores_`
- [ ] Lists use dashes (`-`), not asterisks (`*`)
- [ ] Code blocks have language tags
- [ ] Internal links use absolute paths (`/en/...`)
- [ ] Images use `<Frame>` wrapping markdown `![]()`; alt text is in title case and under 125 characters
- [ ] Image files are stored under the correct `images/<section>/` subfolder
- [ ] Image filenames use kebab-case, are descriptive, and contain no default tool names
- [ ] Comparison images (two or more shown together) each have a caption
- [ ] No double blank lines
- [ ] Em dashes and en dashes have no surrounding spaces
