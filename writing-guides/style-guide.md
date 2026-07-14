# Dify Documentation Style Guide

## Voice and Tone

Use **active voice** whenever natural and clear. Passive voice is acceptable when the actor is unknown or when it reads more naturally.

Be conversational but professional. Prefer everyday language over formal equivalents—"ask questions" over "submit queries". Avoid robotic, AI-sounding phrasing.

## Clarity and Conciseness

Express ideas clearly and concisely. Every sentence should add value. Cut unnecessary words without losing meaning.

Choose precision when it prevents confusion. A specific, descriptive term is better than a shorthand that assumes shared context with the reader.

Keep every paragraph to four rendered lines or fewer (roughly 50 words). On Mintlify's content width, anything longer renders as a dense block that readers skip. When a paragraph runs long, split it at a natural boundary, typically where the topic shifts from setup to payoff, or from problem to solution.

## Images

An image should clarify something text cannot, not decorate the page. Documentation readers are trying to accomplish a task, and every visual element competes with the text for their attention. Images that repeat what the prose already says dilute the content rather than reinforce it.

Before adding an image, ask three questions in order:

1. Can the reader understand this section without it?
2. If not, can rewording or restructuring the prose solve the problem?
3. Is the image the only way to convey this information?

Only add the image when the answer to the first two is no and the answer to the third is yes. Screenshots of obvious UI, decorative banners, and illustrations that restate the heading all belong in the cut column.

When an image is warranted:

- Prefer highlight marks (fills, color overlays) over bounding boxes to draw attention. Boxes pile up and age poorly; highlights integrate with the screenshot.
- Crop tightly to the relevant area. A full-window screenshot where only a panel matters is visual noise.

For the mechanics of image syntax, alt text, captions, and storage, see the [Formatting Guide](./formatting-guide.md#images).

## Callout Usage

Place critical limitations at the start of a section when users need them before taking action, not only at the end.

**Avoid overuse.** Too many callouts dilute their importance and interrupt reading flow. When a section accumulates multiple callouts, restructure into flowing paragraphs with inline bold text instead. Reserve callout visual weight for genuinely critical information.

## Paid Feature Callouts

Each product copy has its own pattern. Plan badges appear only in the Cloud copy (`en/cloud/`); Enterprise mentions appear only on self-host pages, as a `<Tip>`. Never both patterns in one copy.

### Cloud pages: plan badges

- `<Badge color="blue">Professional</Badge>`
- `<Badge color="blue">Team</Badge>`

Pick one of three placements based on the scope of the gated feature.

**1. Whole section is the paid feature.** Place the badges inline with the section heading. No additional callout needed.

```mdx
## Spread Requests Across Keys with Load Balancing <Badge color="blue">Professional</Badge> <Badge color="blue">Team</Badge>
```

**2. Paid feature is one item within a section that also covers standard features.** Place the `<Info>` callout AFTER the target paragraph (not before, where it would be ambiguous). State the subject explicitly.

```mdx
Add one chunk or batch-add several. For documents chunked in Parent-child mode, both parent and child chunks can be added.

<Info>
Adding chunks is available on <Badge color="blue">Professional</Badge> and <Badge color="blue">Team</Badge>. [Learn more](https://dify.ai/pricing).
</Info>
```

**3. Paid feature mentioned in body prose alongside standard features.** Use inline badges directly in the sentence.

```mdx
Unlimited log retention is available on <Badge color="blue">Professional</Badge> and <Badge color="blue">Team</Badge> for the duration of the active subscription. [Learn more](https://dify.ai/pricing).
```

### Self-host pages: Enterprise Tip

Where a Community Edition capability ends and Dify Enterprise extends it, add a `<Tip>` at that point. It names a different product, not the reader's own, so it is not an audience restatement. Link to contact sales, never to the pricing page or the Enterprise docs. Do not add Enterprise mentions where CE isn't restricted, and no orphan headings for Enterprise-only features.

```mdx
<Tip>
  On Dify Enterprise, you can sign in with OAuth or SAML single sign-on instead of a password. [Contact sales](https://udify.app/chat/QuwcpW1oBNcfeL55) to learn more.
</Tip>
```

## Patterns to Use

**Direct instructions.** Use the imperative for required actions: "Click **Generate** to create the output." Reserve "you can" for optional actions to signal choice.

**Task-oriented headings.** "Import Your Data" instead of "Data Import Feature."

**Location-first instructions.** When an operation involves a specific UI location, name the location before the action: "In the **Settings** panel, enable the toggle." This prevents users from completing an action in the wrong place.

**User outcomes over technical mechanisms.** Focus on what users achieve, not how the system works internally. "Answer follow-up questions coherently" (outcome) over "maintain conversational context across turns" (mechanism).

**Problem → solution structure.** Introduce features by stating the problem they solve, then the solution.

**Purpose-oriented descriptions.** Describe actions with their purpose: "Add comments to share ideas and discuss design decisions" is more useful than "Click the comment icon to add comments."

**Progressive disclosure.** Lead with the essential, add details as needed. Don't over-segment simple tasks into excessive steps.

**Natural transitions.** Connect ideas smoothly. Avoid mechanical connectors or repetitive sentence openers across a section.

**Parallel structure for dependencies.** Keep interdependent configurations in one sentence. Splitting implies sequential order or suggests one is more important.

**Decision-making information.** Provide applicable scenarios and trade-offs rather than prescribing specific configurations. Users have diverse needs; give them what they need to make informed choices.

**Adjustable parameter guidance.** When documenting parameters users can tune (thresholds, limits, intervals), describe the trade-off direction—not a recommended value. Tell users what happens when they go higher vs. lower so they can decide based on their own context. For example: "Higher thresholds return fewer, more relevant results; lower thresholds include broader matches."

**Limits and quotas.** Match the claim to what the reader can change. A hardcoded product limit gets a plain number ("up to 50 MB") — on Cloud pages every limit reads this way, since readers there have no deployment configuration to change. On self-host pages, a deployment-configurable limit states the default and names the environment variable, linked to the environment variable reference ("up to 15 MB by default; adjust with `UPLOAD_FILE_SIZE_LIMIT`"); presenting a configurable default as a fixed rule breaks on any deployment that changed it.

**Genuine insight.** Add the "why" and "how it connects", not just a reorganization of information already visible in the product.

**Resolution, not just consequence.** When documenting a limitation, risky action, or failure mode, also tell the reader how to recover or avoid it. Stating what breaks without how to fix it leaves the user stuck.

## Patterns to Avoid

**Excessive bullets.** Use bullet points only for genuinely discrete, enumerable items. When explaining concepts or processes, or when ideas connect, write in paragraphs. Don't fragment continuous reasoning into bullet lists.

**Passive voice overuse.** "The file is uploaded by the user" → "You upload the file."

**Feature-centric framing.** "This feature allows you to..." → "You can..." When an action is optional, "you can" is preferable; when it's required, use the imperative.

**Feature names users don't see.** If a feature's official name doesn't appear in the product UI, don't use it as a sentence subject in body text. Describe what users do instead. "Collaboration lets workspace members edit..." → "You can edit the same workflow alongside your teammates..." Section headings and navigation labels can still use the name.

**Redundant phrases.** Cut "in order to", "it should be noted that", "please note that", and similar filler.

**Repeating context.** Don't restate conditions already established by the section heading or earlier prose. If a section is titled "Configure Webhooks", individual steps shouldn't keep saying "to configure webhooks." The first sentence after a heading should add new information, not paraphrase the heading.

**Repeating the UI.** Don't describe interface elements users can see directly—default values, field labels, button names. Documentation provides context and rationale not visible in the UI.

**Describing the documentation.** Don't narrate the page's own structure or the doc set like "This section covers". Readers want the product, not a tour of the page. Lead with what the user does or needs.

**Information noise.** If content doesn't provide value beyond what the reader already knows or can see, it hinders rather than helps. Before including a detail, ask: does the reader need this to accomplish their goal? If the UI already communicates it, or it restates what the previous sentence implied, cut it.

**Unnecessary second sentences.** When two sentences can be merged into one without losing readability, combine them. If the "how it works" can be folded into the "what it does," a separate sentence is noise. Apply case-by-case—don't sacrifice clarity for brevity.

**Repetitive structures.** Vary sentence patterns across related sections to avoid a mechanical feel.

**Vague cross-references.** Don't link to another page unless the reader gains something by clicking. If the current page already provides sufficient context, the link is noise. When linking, "see X for details" is fine if the surrounding context already makes clear what those details are. Only add a specific description when the context alone doesn't convey what the reader will find—otherwise the description itself becomes redundant.

**Over-simplification.** Don't sacrifice clarity for brevity. Choose precision when a specific term prevents confusion, even if it's longer.
