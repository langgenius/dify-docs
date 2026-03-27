# Dify Documentation Style Guide

## Voice and Tone

Use **active voice** whenever natural and clear. Passive voice is acceptable when the actor is unknown or when it reads more naturally.

Be conversational but professional. Prefer everyday language over formal equivalents—"ask questions" over "submit queries". Avoid robotic, AI-sounding phrasing.

This documentation serves both developers and non-technical users. Write to be accessible to both.

## Clarity and Conciseness

Express ideas clearly and concisely. Every sentence should add value. Cut unnecessary words without losing meaning, but don't sacrifice readability for minimalism—the goal is the shortest version that still reads naturally.

Choose precision when it prevents confusion. A specific, descriptive term is better than a shorthand that assumes shared context with the reader.

When a heading already states the topic, the first sentence should add new information—not restate the heading.

## Formatting Principles

Use **Title Case** for all headings.

Prefer prose over bullet points when explaining concepts or processes. Use bullet points only for genuinely discrete, enumerable items. Write in paragraphs when ideas connect.

Use tabs (not numbered lists) when presenting parallel options users choose between. Numbered lists imply sequence; tabs signal alternatives.

## Callout Usage

- **Info**: General informational content—helpful context, version-specific or deployment-specific details
- **Tip**: Helpful suggestions or shortcuts
- **Note**: Important information that requires attention—missing it could lead to potential complications
- **Warning**: Actions that could cause errors or data loss

Place critical limitations at the start of a section when users need them before taking action, not only at the end.

**Avoid overuse.** Too many callouts dilute their importance and interrupt reading flow. When a section accumulates multiple callouts, restructure into flowing paragraphs with inline bold text instead. Reserve callout visual weight for genuinely critical information.

These are principles, not absolute rules. Apply them when they improve clarity; use editorial judgment when they don't.

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

**Genuine insight.** Add the "why" and "how it connects", not just a reorganization of information already visible in the product.

## Patterns to Avoid

**Excessive bullets.** Don't fragment continuous reasoning into bullet lists. If the items connect, use prose.

**Passive voice overuse.** "The file is uploaded by the user" → "You upload the file."

**Feature-centric framing.** "This feature allows you to..." → "You can..." When an action is optional, "you can" is preferable; when it's required, use the imperative.

**Redundant phrases.** Cut "in order to", "it should be noted that", "please note that", and similar filler.

**Repeating context.** Don't restate the scenario conditions established by the section heading or earlier prose. If a section is titled "Configure Webhooks", individual steps shouldn't keep saying "to configure webhooks."

**Repeating the UI.** Don't describe interface elements users can see directly—default values, field labels, button names. Documentation provides context and rationale not visible in the UI.

**Repetitive structures.** Vary sentence patterns across related sections to avoid a mechanical feel.

**Over-simplification.** Don't sacrifice clarity for brevity. Choose precision when a specific term prevents confusion, even if it's longer.
