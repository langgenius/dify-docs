# Dify Documentation Formatting Guide

This document defines the formatting standards for Dify documentation. Contributors can load this guide into an AI assistant to automatically check and fix formatting issues during the writing process.

> **For AI assistants:** When a contributor asks you to review their documentation, check every rule in this guide and report violations with line-level references. When asked to fix formatting, apply all rules in a single pass.

---

## Frontmatter

Every MDX file must start with YAML frontmatter containing at least `title` and `description`:

```yaml
---
title: "Page Title"
description: "A concise summary of what this page covers"
---
```

- `title` is **required**. `description` is required for new pages; existing pages should be updated over time.
- `description` should not end with a period.
- `sidebarTitle` is optional. Add it when the title is too long for the sidebar, or when other pages in the same group follow a specific `sidebarTitle` convention.
- Use double quotes around values that contain special characters.
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

### Preferred Format (Frame Component)

```mdx
<Frame>
  ![LLM Node Overview](https://assets-docs.dify.ai/.../image.png)
</Frame>
```

- Use a `<Frame>` component wrapping `![]()` markdown syntax by default.
- Always include a descriptive `alt` attribute in **title case**.
- Only add a `caption` when the image's meaning is not clear from context—captions are visible to all readers, while alt text only displays if the image fails to load. Use **title case** for captions.

```mdx
<Frame caption="LLM Node Configuration Interface">
  ![LLM Node Configuration Interface](https://assets-docs.dify.ai/.../image.png)
</Frame>
```

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
- [ ] Images have `alt` attributes
- [ ] No double blank lines
- [ ] Em dashes and en dashes have no surrounding spaces
