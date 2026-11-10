# Dify Documentation Style Guide

## What a Good Page Does

A good page gives the reader what they came for, at the moment they arrive, in the fewest words that stay clear and accurate. Everything else in this guide serves that.

Picture the reader mid-task, with a question. The default sentence tells them what to do, where, and what happens: that is what they came for.

A fact earns its place because that reader would ask for it here, not because it is true, verified, absent from the interface, or reported once. A reason earns its place only where the reader would otherwise do the wrong thing; a reader who has just changed a setting does not need to be told why to check it. Where there is a real choice, say which way to lean and why, so they can decide for their own case.

The page follows the reader's order, not the product's: what they need first, then each step, with each fact at the step where they act on it. A page for several kinds of readers is written for the task they share, and one reader's case appears as an example, not as the frame.

Each section opens with the action, so the reader knows within a line whether this is the section they need. Within it, each sentence sits beside what it depends on: a condition where its situation arises, a pointer word after what it points to. An abstract point rides on a concrete example. When an AI concept appears, say what problem it solves, because that is what a builder needs to use it well.

The page sounds like a person: sentences vary in length and shape because they follow the thought, and it reads aloud without stumbling. Its words are the product's, as the interface names them, never the code's or the team's. A name the reader types or looks up, such as an environment variable or an error code, counts as the product's. The patterns later in this guide say how; this section says what they are for.

Two failures look like finished writing and are not.

**Transcribed prose** restates a fact list in complete sentences. Every sentence is true, every sentence has the same shape, and none tells the reader what to do about anything. It happens when the writer drafts toward the research, every verified fact in order, instead of toward the reader. Its symptoms: a table kept to hold one fact because a template had a table there, a description of what a dialog shows, a reason attached to an instruction the reader would have followed anyway, a "why" sentence in front of the "do this" sentence. Ask of each sentence what the reader would do differently for having read it, and cut the ones with no answer.

**Dense prose** packs two or three ideas into one sentence, joined by "so", "which", or a participle, and runs a paragraph on past the point where the reader's question changed. Each sentence is defensible and the page is exhausting. A sentence carrying two separable ideas is two sentences; ideas are separable when the reader can take each one alone, and the connecting word only shows where to look. A paragraph breaks where the topic turns.

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

## Organize and Present the Content

Getting the right content onto the right page comes first; the opening section is about that. A rule has one home, the page whose reader needs all of it. Other pages link there with a payoff and keep only what is specific to them, because a copied rule doubles the reading and the copies drift apart. A fact this page's reader acts on is specific to them when a sentence or two carries it: keep it here, since sending the reader away for a sentence costs more than repeating it.

The second job is to organize and present that content so the reader can use it. Each block takes the form that fits what the reader does with it, worked out from what they decide there and in what order, never from the order the facts were found or fixed in. Right content in the wrong form still fails: the reader holds every case in mind to find their own, or acts before reaching the sentence that would have stopped them.

A judgment the reader makes comes before the action it governs. A step that ends by telling some readers they shouldn't have started it is in the product's order, not theirs. Then choose the form by what the reader is doing:

| The reader | Form | Keep in mind |
|:--|:--|:--|
| Follows reasoning whose ideas connect | Paragraphs | Break where the reader's question changes; connected ideas don't become bullets (see **Excessive bullets**). |
| Finds their own case among several | A bulleted list, each item led in bold by the case as the reader recognizes it | Each reader fits exactly one item. |
| Carries out actions in a fixed order | A numbered list; `<Steps>` when each step carries its own code, images, or sub-steps | A short task stays a sentence or two (see **Progressive disclosure**). |
| Compares options, or looks up values, on the same points | A table | Every row answers the same columns; content that differs in kind from row to row is a list. |
| Follows one of several paths, each with its own steps, such as Docker or source code | `<Tabs>`, titled by the choice | The reader sees only the tab they open, so what every reader needs stays outside the tabs. |
| Copies the same operation for their language or tool | `<CodeGroup>` | Each variant does the same thing; different procedures are tabs. |
| Copies a command, a value, or a file | A code block | Put each command at the step where the reader runs it. |
| Meets something only some readers need, or a trap no reader may miss | A callout, typed per the [Formatting Guide](./formatting-guide.md#callouts) | See [Callouts](#callouts). |
| Needs it only in a specific situation: a troubleshooting entry, a FAQ, an optional deep dive | `<Accordion>`, or `<AccordionGroup>` for a set, titled by the symptom or question | The title lets the reader decide without opening it; never hide a step, a warning, or anything every reader needs. |
| May not know a term the page uses | A `<Tooltip>` on the term | It shows only on hover, so it holds a definition, never something the reader needs to act. |
| Looks up the fields of a request, a response, or a schema | `<ParamField>` or `<ResponseField>`, with `<Expandable>` for nested fields | Reference pages only; a guide page uses a table. |
| Needs to see a screen state words can't carry | An image in a `<Frame>`; side-by-side images in `<Columns>` | See [Images](#images): only when the text can't do it. |
| Needs to follow a flow or a relationship between parts | A Mermaid diagram | Same test as images: write the prose first, and add the diagram only where the prose can't carry it. |
| Finds their way around a directory layout | A `<Tree>` | Show only the folders and files the page talks about. |
| Chooses where to go next among several pages | `<Card>`s in a `<CardGroup>` or `<Columns>` | Each card says what the reader gets there; a single destination is a link in a sentence. |
| Recognizes a button shown only as an icon | An inline `<Icon>` beside the action | Only where the interface shows no label. |
| Sees what a plan or status gates | A `<Badge>` | See [Paid Feature Callouts](#paid-feature-callouts). |

The other Mintlify components serve the site itself or genres this doc set doesn't have: `<Banner>` (site-wide, configured in `docs.json`), `<Update>` (changelogs), `<Color>` (design systems), `<Panel>` and `<RequestExample>`/`<ResponseExample>` (the right sidebar), `<View>` (a page-wide language switch), `<Visibility>` (content per audience), `<Prompt>`, `<Tiles>`, and `<GitHub>` cards. Agree the first use of any of them with the docs team.

### Callouts

A section has a main line: what every reader needs, in the order they act on it. A callout sets other content apart from it, so the main line reads straight through and the reader who needs the rest finds it where it applies. Use one for either of two kinds of content, typed by its role:

- **Asides**: context only some readers need, an optional shortcut, a condition that applies to some deployments or plans, or a setting that enables what the section describes. Without a callout, an aside either interrupts the main line or gets cut from a page whose reader needed it.
- **Traps**: what no reader may miss. A limit the reader needs before acting goes at the start of the section; a fact that contradicts what the interface implies, such as an API-started run labeled WebApp, or one that protects the reader's data or time, such as a download that expires, goes where it applies, even inside a list item.

A step every reader takes, or a condition that decides which way the reader goes, is the main line and stays out of callouts. Callouts stacked one after another mean the main line around them needs reshaping.

### An Example

The first step of setting an environment variable on a self-hosted deployment, as first written (credentials abridged):

```mdx
Search `docker/envs/` for the variable's name. The `.defaults` file that defines it names its local file in the first comment. Edit that local file if it exists; otherwise, copy the `.defaults` file to that name first.

For example, settings shared by the API, workers, and scheduled tasks (Beat) are defined in `envs/core-services/api-worker.defaults`, so they go in `api-worker.env`.

<Info>
  If `docker/.env` also sets the variable, that value wins; see [Precedence](#precedence).
</Info>

If the search finds an `.env.example` template instead, such as `envs/security.env.example`, copy it to the same name without `.example`.

<Note>
  Skip `envs/middleware.env.example`: it belongs to the separate middleware stack for source-code development, and a Docker Compose deployment doesn't read it.
</Note>

Two kinds of settings go in `docker/.env` instead:

- **Settings Compose reads before it loads any service file**, such as `COMPOSE_PROFILES` and `VECTOR_STORE`.
- **Shared credentials**, so every service that uses one gets the same value, such as `PLUGIN_DAEMON_KEY`.
```

Reshaped:

```mdx
Set most variables in a local `.env` file under `docker/envs/`, and these two kinds in `docker/.env`:

- **Settings Compose reads before it loads any service file**, such as `COMPOSE_PROFILES` and `VECTOR_STORE`.
- **Shared credentials**, so every service that uses one gets the same value, such as `PLUGIN_DAEMON_KEY`.

For any other variable, search `docker/envs/` for its name, then act on what the search finds:

- **One `.defaults` file**: edit the local file named in its first comment. If that file doesn't exist yet, copy the `.defaults` file to that name first.
- **Several `.defaults` files**: edit the local file that every service using the variable loads; otherwise the services end up with different values.
- **An `.env.example` template**, such as `envs/security.env.example`: copy it to the same name without `.example`. Skip `envs/middleware.env.example`, which only the separate middleware stack for source-code development reads.

When `docker/.env` and a local file set the same variable, the `docker/.env` value wins, with the exceptions in [Precedence](#precedence).
```

The reader's first question is which file. The first version answered it for most readers, then told the rest in its last paragraph that the step wasn't for them. The reshaped step settles the two kinds that go in `docker/.env` first, then sorts everyone else by what their search finds, one item each. Both callouts held main-line content: the middleware file is one case's exception, so it joins that case, and precedence is the last thing a reader holding two values needs.

## Voice and Tone

Use **active voice** whenever natural and clear. Passive voice is acceptable when the actor is unknown, when who acts doesn't change what the reader does, or when it reads more naturally.

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

## Paid Feature Callouts

Each product copy has its own pattern. Plan badges appear only in the Cloud copy (`en/cloud/`). The Enterprise `<Tip>` appears on self-host pages, and on Cloud pages where Dify Enterprise goes beyond what Cloud offers. A Cloud page can carry both: badges for what a plan gates, the Tip for what only Enterprise adds.

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

### Enterprise Tip

Where a Community Edition or Cloud capability ends and Dify Enterprise extends it, add a `<Tip>` at that point. It names a different product, not the reader's own, so it is not an audience restatement. Link **Contact sales** to the sales form for the page's language, never to the pricing page, the Enterprise docs, or a webapp. Do not add Enterprise mentions where the reader's edition isn't restricted, and no orphan headings for Enterprise-only features.

On a Cloud page, add the Tip only where Enterprise does something no Cloud plan does, such as running an app in separate environments. Where a paid Cloud plan covers it, the plan badges are enough.

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

**Task-oriented headings.** "Import Your Data" instead of "Data Import Feature." The section under it answers that heading and stays on it.

**Location-first instructions.** When an operation involves a specific UI location, name the location before the action: "In the **Settings** panel, enable the toggle." This prevents users from completing an action in the wrong place.

**User outcomes over technical mechanisms.** Focus on what users achieve, not how the system works internally. "Answer follow-up questions coherently" (outcome) over "maintain conversational context across turns" (mechanism).

**Problem → solution structure.** Introduce features by stating the problem they solve, then the solution.

**Purpose-oriented descriptions.** Describe actions with their purpose: "Add comments to share ideas and discuss design decisions" is more useful than "Click the comment icon to add comments."

**Progressive disclosure.** Lead with the essential, add details as needed. Don't over-segment simple tasks into excessive steps.

**Natural transitions.** Connect ideas smoothly. Avoid mechanical connectors or repetitive sentence openers across a section.

**Parallel structure for dependencies.** Keep interdependent configurations in one sentence. Splitting implies sequential order or suggests one is more important.

**Decision-making information.** Provide applicable scenarios and trade-offs rather than prescribing specific configurations. Users have diverse needs; give them what they need to make informed choices.

**Adjustable parameter guidance.** When documenting parameters users can tune (thresholds, limits, intervals), describe the trade-off direction—not a recommended value. Tell users what happens when they go higher vs. lower so they can decide based on their own context. For example: "Higher thresholds return fewer, more relevant results; lower thresholds include broader matches."

**Switches and defaults.** Write a setting as the change the reader might make, not as its default. A switch that is off by default is written as when to turn it on and how ("To show readers which documents an answer came from, enable **Citations and Attributions**"); one that is on by default, as when to turn it off and how. The current state is visible where the switch is, so a sentence reporting it gives the reader nothing to do.

**Limits and quotas.** Match the claim to what the reader can change. A hardcoded product limit gets a plain number ("up to 50 MB") — on Cloud pages every limit reads this way, since readers there have no deployment configuration to change. On self-host pages, a deployment-configurable limit states the default and names the environment variable, linked to the environment variable reference ("up to 15 MB by default; adjust with `UPLOAD_FILE_SIZE_LIMIT`"); presenting a configurable default as a fixed rule breaks on any deployment that changed it.

**Genuine insight.** Add the "why" and "how it connects", not just a reorganization of information already visible in the product.

**Resolution, not just consequence.** When documenting a limitation, risky action, or failure mode, also tell the reader how to recover or avoid it. Stating what breaks without how to fix it leaves the user stuck. When the limitation already shows the way forward, as "can't be done from the CLI" points to the UI or a role limit points to an admin, it needs nothing added.

## Patterns to Avoid

**Excessive bullets.** Use bullet points only for genuinely discrete, enumerable items. When explaining concepts or processes, or when ideas connect, write in paragraphs. Don't fragment continuous reasoning into bullet lists.

**Passive voice overuse.** "The file is uploaded by the user" → "You upload the file."

**Feature-centric framing.** "This feature allows you to..." → "You can..." When an action is optional, "you can" is preferable; when it's required, use the imperative.

**Negative framing.** Say what something is, what happens, and what the reader does. "It's not X" plants the misreading it means to prevent, and a clause that grades the product, such as "with no `failure` to say why" or "an error that reads like an outage", tells the reader nothing to do. A consequence that costs the reader (data, quota, money, access) is still stated, plainly, with the action that avoids it.

**Feature names users don't see.** If a feature's official name doesn't appear in the product UI, don't use it as a sentence subject in body text. Describe what users do instead. "Collaboration lets workspace members edit..." → "You can edit the same workflow alongside your teammates..." Section headings and navigation labels can still use the name.

**Redundant phrases.** Cut "in order to", "it should be noted that", "please note that", and similar filler.

**Repeating context.** Don't restate conditions already established by the section heading or earlier prose. If a section is titled "Configure Webhooks", individual steps shouldn't keep saying "to configure webhooks." The first sentence after a heading should add new information, not paraphrase the heading. At the top of a page, the description under the title plays that heading's part, so the opening doesn't restate what the page is for.

**Repeating the UI.** Apply the moment-of-use test: if the interface shows the fact at the moment the reader acts—a button's next state, an unread marker, a notice that appears in context, a Retry label after a failure, the filename of a download—leave it out. Document what the interface cannot say at that moment: hidden affordances (hover-only actions), behavior connecting two screens, what a search field actually matches, and the system rules behind a label. Repeat a UI-visible fact only when it's especially consequential: data loss, permissions, or cost.

**Navigation hand-holding.** State where a surface lives once; don't re-explain routes to standard chrome (the avatar menu, **Settings**). Location-first instructions cover the step being performed, not repeated wayfinding.

**Describing the documentation.** Don't narrate the page's own structure or the doc set like "This section covers". Readers want the product, not a tour of the page. Lead with what the user does or needs.

**Information noise.** If content doesn't provide value beyond what the reader already knows or can see, it hinders rather than helps. Before including a detail, ask: does the reader need this to accomplish their goal? If it repeats the UI (see above) or restates what the previous sentence implied, cut it.

**Sentences that add nothing.** Cut a sentence when the reader learns nothing from it: a "how it works" the "what it does" already implies, or a restatement of the line before. Keep a sentence that carries its own claim, however short; folding it into its neighbor trades a clear sentence for a crowded one.

**Repetitive structures.** Vary sentence patterns across related sections to avoid a mechanical feel.

**Narrating absent infrastructure.** Public text instructs; it never announces what internal automation or process does not exist ("there is no automatic translation pipeline", "we removed X"). Absence claims read as a confession and tell outsiders about operations they never asked about. State the positive behavior instead: "every change ships all three languages in the same PR." Removal narratives belong in PR descriptions, not in READMEs, agent instructions, or docs.

**Vague cross-references.** Don't link to another page unless the reader gains something by clicking. If the current page already provides sufficient context, the link is noise. When linking, never write a bare "see [X]" — give the link a payoff: "see [X] for details" when the surrounding context already makes clear what those details are, or name what the reader will find ("see [X] for the full flag table") when it doesn't. Don't gate a link or section on who the reader is ("If you've used X, see…"); state the payoff so any reader can opt in.

The reader is the subject of the sentence and the page is what they open: "See [Manage Members] for how roles change." Never make the page the subject ("The Manage Members guide explains how roles change", "X says what to do"): a page that talks gives the reader nothing to do.

