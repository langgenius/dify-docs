# Dify Documentation Style Guide

## What a Good Page Does

A good page gives the reader what they came for, at the moment they arrive, in the fewest words that stay clear and accurate. Everything else in this guide serves that.

Picture the reader mid-task, with a question. The default sentence tells them what to do, where, and what happens: that is what they came for.

A fact earns its place because that reader would ask for it here, not because it is true, verified, or absent from the interface. A reason earns its place only where the reader would otherwise do the wrong thing; a reader who has just changed a setting does not need to be told why to check it. Where there is a real choice, say which way to lean and why, so they can decide for their own case.

Each section opens with the action, so the reader knows within a line whether this is the section they need. An abstract point rides on a concrete example. When an AI concept appears, say what problem it solves, because that is what a builder needs to use it well.

The page sounds like a person: sentences vary in length and shape because they follow the thought, and it reads aloud without stumbling. Its words are the product's, as the interface names them, never the code's or the team's. The patterns later in this guide say how; this section says what they are for.

Two failures look like finished writing and are not.

**Transcribed prose** restates a fact list in complete sentences. Every sentence is true, every sentence has the same shape, and none tells the reader what to do about anything. It happens when the writer drafts toward the research, every verified fact in order, instead of toward the reader. Its symptoms: a table kept to hold one fact because a template had a table there, a description of what a dialog shows, a reason attached to an instruction the reader would have followed anyway, a "why" sentence in front of the "do this" sentence. Ask of each sentence what the reader would do differently for having read it, and cut the ones with no answer.

**Dense prose** packs two or three ideas into one sentence, joined by "so", "which", or a participle, and runs a paragraph on past the point where the reader's question changed. Each sentence is defensible and the page is exhausting. A sentence carrying two separable ideas is two sentences, and a paragraph breaks where the topic turns.

### Two Examples

Two pages in this doc set show the register: `en/cloud/use-dify/build/new-agent/overview.mdx` for a concept page and `en/cloud/use-dify/build/new-agent/build.mdx` for a task page. Read the one in your page's genre before drafting. They calibrate the ear; this guide is the authority, and when a page and the guide disagree, the guide wins. The two examples below take one passage from each page and set it beside the facts it was written from and a version that merely states them.

**A concept.** The facts, as research produced them: an agent's role, prompt, model, skills, tools, and files are stored with the agent; a run's input is the chat message when the agent runs on its own and the node's instruction inside a workflow; the stored setup is used on every run; end users cannot change it.

Transcribed:

```mdx
## Configuration and Task

An agent has a configuration and a task. The configuration consists of the role, prompt, model, skills, tools, and files, and is stored with the agent. The task is the input for a run: the chat message when the agent runs on its own, or the instruction in the Agent node. The configuration is used for every run and cannot be changed by end users.
```

Written:

```mdx
## Capability and Task

An Agent separates what it *is* from what you ask it to *do*:

- **Its *capability* (think of it as the agent's soul) is who the agent is**.

  The role and prompt you write, the model it runs on, and the skills, Dify tools, and files you give it. You shape it once and keep refining it as you learn what the agent needs.

- **Its *task* is what you ask it to do on a given run**.

  When the agent works on its own, the task is the message you send it. When it works inside a workflow, the task is the instruction you give the node.

It's the same split as hiring someone: you choose a person for what they can do, then give them a specific task. Strong results need both: the right person for the job and a clear brief.
```

The second gives the reader a way to think, not a data model. The split gets names a builder will use, one analogy carries it, and the close tells them what a good result needs from them. The end-user fact, true and verified, is left for the task page, where the reader who would ask is.

**A task.** The facts: the **Agents** page has a **Create** button with two options, **Create from Blank** and **Import DSL file**; the create dialog has a required name and optional role and description; a new agent opens in **Configure**; a DSL import carries neither skills nor files.

Transcribed:

```mdx
## Create an Agent

The **Agents** page has a **Create** button with two options: **Create from Blank** and **Import DSL file**. **Create from Blank** opens a dialog with a name field, an optional role field, and an optional description field. After creation, the agent opens on the **Configure** tab. **Import DSL file** creates an agent from a DSL file. Skills and files are not included in the import.
```

Written:

```mdx
## Create an Agent

From **Agents**, click **Create** > **Create from Blank** and give the agent a name; optionally add a role such as *Research Assistant* and a description. Then you shape everything else in **Configure**.

To create an agent from a shared DSL file, choose **Import DSL file**. Skills and files aren't included, so add them after importing.
```

One sentence carries the whole action, its location, and where it lands. The dialog's fields are not described, because the reader is looking at them. The one fact kept from the import path is the one with a cost, and it arrives as the next thing to do. Both versions are correct; only the second is finished.

## Voice and Tone

Use **active voice** whenever natural and clear. Passive voice is acceptable when the actor is unknown or when it reads more naturally.

Be conversational but professional. Prefer everyday language over formal equivalents—"ask questions" over "submit queries". Write the way someone who knows the product explains it to a colleague: plainly, with the reason attached.

## Clarity and Conciseness

Express ideas clearly and concisely. Every sentence should add value. Cut unnecessary words without losing meaning.

Choose precision when it prevents confusion. A specific, descriptive term is better than a shorthand that assumes shared context with the reader.

A paragraph carries one idea. Mintlify's content column is narrow, so a paragraph that runs past a few lines renders as a block readers skip; break it where the reader's question changes, typically where setup turns to payoff or problem to solution. Shorten by leaving things out, never by packing more into each sentence.

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

**Promote traps.** When a fact contradicts what the interface implies (an API-started run labeled WebApp) or protects the reader's data or time (a download that expires), a short `<Info>` or `<Tip>` beats a buried sentence—even inside a list item.

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

Where a Community Edition capability ends and Dify Enterprise extends it, add a `<Tip>` at that point. It names a different product, not the reader's own, so it is not an audience restatement. Link **Contact sales** to the sales form for the page's language, never to the pricing page, the Enterprise docs, or a webapp. Do not add Enterprise mentions where CE isn't restricted, and no orphan headings for Enterprise-only features.

| Language | Sales form link |
|:---------|:----------------|
| en | `https://share-na2.hsforms.com/14-09ff5HS92Sh4m3f4yrcw40s9fk` |
| zh | `https://share-na2.hsforms.com/1O3Rajx4URXm88UzneXYpCw40s9fk` |
| ja | `https://share-na2.hsforms.com/176RpklY3TLeHo6qmuAdRKQ40s9fk` |

```mdx
<Tip>
  On Dify Enterprise, you can sign in with OAuth or SAML single sign-on instead of a password. [Contact sales](https://share-na2.hsforms.com/14-09ff5HS92Sh4m3f4yrcw40s9fk) to learn more.
</Tip>
```

## Patterns to Use

**Direct instructions.** Use the imperative for required actions: "Click **Generate** to create the output." Reserve "you can" for optional actions to signal choice. A capability the reader may not hold, granted at another permission level, is stated as a fact ("other members can hold it through a custom role"), not written as an instruction. When a task needs a role or permission the reader may not have, say so once, at the task's entry point, in an `<Info>` that names the role ("Creating and managing agents requires the Editor role or above."); don't repeat it per step, and don't add it where every reader of the page holds the permission.

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

**Repeating the UI.** Apply the moment-of-use test: if the interface shows the fact at the moment the reader acts—a button's next state, an unread marker, a notice that appears in context, a Retry label after a failure, the filename of a download—leave it out. Document what the interface cannot say at that moment: hidden affordances (hover-only actions), behavior connecting two screens, what a search field actually matches, and the system rules behind a label. Repeat a UI-visible fact only when it's especially consequential: data loss, permissions, or cost.

**Navigation hand-holding.** State where a surface lives once; don't re-explain routes to standard chrome (the avatar menu, **Settings**) or spell out a next step the restriction already implies ("ask an admin"). Location-first instructions cover the step being performed, not repeated wayfinding.

**Describing the documentation.** Don't narrate the page's own structure or the doc set like "This section covers". Readers want the product, not a tour of the page. Lead with what the user does or needs.

**Information noise.** If content doesn't provide value beyond what the reader already knows or can see, it hinders rather than helps. Before including a detail, ask: does the reader need this to accomplish their goal? If it repeats the UI (see above) or restates what the previous sentence implied, cut it.

**Sentences that add nothing.** Cut a sentence when the reader learns nothing from it: a "how it works" the "what it does" already implies, or a restatement of the line before. Keep a sentence that carries its own claim, however short; folding it into its neighbor trades a clear sentence for a crowded one.

**Repetitive structures.** Vary sentence patterns across related sections to avoid a mechanical feel.

**Narrating absent infrastructure.** Public text instructs; it never announces what internal automation or process does not exist ("there is no automatic translation pipeline", "we removed X"). Absence claims read as a confession and tell outsiders about operations they never asked about. State the positive behavior instead: "every change ships all three languages; translate in the same pass." Removal narratives belong in PR descriptions, not in READMEs, agent instructions, or docs.

**Vague cross-references.** Don't link to another page unless the reader gains something by clicking. If the current page already provides sufficient context, the link is noise. When linking, never write a bare "see [X]" — give the link a payoff: "see [X] for details" when the surrounding context already makes clear what those details are, or name what the reader will find ("see [X] for the full flag table") when it doesn't. Don't gate a link or section on who the reader is ("If you've used X, see…"); state the payoff so any reader can opt in.

