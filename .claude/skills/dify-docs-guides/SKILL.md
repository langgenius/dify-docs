---
name: dify-docs-guides
description: >
  Use when writing, improving, or reviewing Dify user guide documentation.
  Covers pages in en/{cloud,self-host}/use-dify/, en/develop-plugin/, and en/self-host/deploy/.
  Triggers: "write docs for [feature]", "improve this page",
  "review this documentation section".
---

# Dify Documentation Guides

Follow the numbered workflow in order. Do not skip steps.

## Step 1 — Read the guides

Read all three files before drafting or editing anything:

1. `writing-guides/style-guide.md` — voice, tone, writing patterns. No overrides: it applies as written.
2. `writing-guides/formatting-guide.md` — MDX formatting, Mintlify components.
3. `writing-guides/glossary.md` — standardized terminology.

If the task includes Chinese or Japanese content, also read `tools/translate/formatting-zh.md` or `tools/translate/formatting-ja.md` before writing that language.

## Step 2 — Research and verify

1. Identify the target page(s) and match each to its reader persona (see Reader Personas below). `use-dify` pages exist as two product copies — `en/cloud/use-dify/` and `en/self-host/use-dify/` — with no shared pages and no cross-audience navigation. When the page exists in both, scope both: shared-content improvements land in both copies in the same pass; audience-specific blocks (plan gating, env-var callouts, Enterprise tips) stay per-copy.
2. For a new feature page, or a rewrite that changes what the doc claims about behavior (not just wording), invoke the `dify-docs-feature-research` skill first and complete its research gate.
3. Verify feature behavior against the Dify codebase, never against existing docs — existing docs may be outdated or wrong. Work in the Dify codebase directory configured for this session; if none is configured, ask the user for the path. Sync it per `writing-guides/index.md` section "Syncing the Dify codebase safely". For new features, use the development branch the user names; when code in flux is ambiguous, ask rather than assume.
4. When rewriting an existing page, treat every carried-over claim as unverified: re-check permissions, defaults, option lists, navigation paths, and behavior against the code before keeping them. The most common failure mode is faithfully reproducing an outdated section.
5. Code presence ≠ working feature. If behavior is inferred from code rather than observed in the running product, mark it unverified and ask the user to test before documenting it as fact.
6. Check for feature-related environment variables. In the Dify codebase, run:

   ```bash
   grep -rn "<FEATURE_KEYWORD>" docker/.env.example docker/envs/ api/configs/
   ```

   Use the feature's name as it would appear in a variable (e.g. `COLLABORATION`); try 2–3 keyword variants before concluding. No matches → the feature has no env-var surface; skip the env-var guidance in Step 4. Matches → record each variable as mandatory or optional plus its default, and invoke the `dify-docs-env-vars` skill in the same session to update `en/self-host/deploy/configuration/environments.mdx` — that reference is the single source of truth for variable semantics.

## Step 3 — Report scope, then STOP

If the task touches more than one page, or restructures a section (adds, moves, renames, or deletes pages or headings), report before editing:

- the full path of every page you will touch
- for each page, what changes and why
- every claim from Step 2 you could not verify in code

**STOP — do not edit any file until the user approves.** A single-page edit with no restructuring may proceed directly to Step 4, but any unverified claims must still be reported to the user, never written as fact.

## Step 4 — Draft

1. Write for the persona of the page's path (see Reader Personas below).
2. Never restate the page's own audience. Everyone on a self-host page is self-hosted and everyone on a cloud page is on Dify Cloud, so "On self-hosted deployments, …" and "On Dify Cloud, …" are banned on their own pages. Audience qualifiers are legitimate only on the audience-neutral trees (`en/learn/`, `en/api-reference/`, `en/cli/`, `en/develop-plugin/`), where they genuinely disambiguate. Two carve-outs are deliberate and stay: naming a different product (the `<Tip>` surfacing Dify Enterprise where a CE capability ends — see "Paid Feature Callouts" in the style guide), and a comparative-advantage claim, where the qualifier marks something this product has that the other lacks ("On Dify Cloud, many popular trigger plugins are pre-configured" — the point is the perk, not the scope). Scoping restatement is banned; advantage framing is not.
3. If Step 2.6 found related environment variables, present them per Environment Variables in User Guides below.

## Step 5 — Translate

Every English change ships all three languages. Update `zh/` and `ja/` in the same pass per `tools/translate/formatting-{zh,ja}.md` and `writing-guides/glossary.md`.

## Step 6 — Run the check chain

Invoke these skills in order (the chain is defined in `writing-guides/index.md` section "Post-Writing Verification"). Do not restate their rules or hand-roll their checks — invoke them:

1. `dify-docs-format-check`
2. `dify-docs-terminology-check`
3. `dify-docs-reader-test`

Fix what they flag and re-run until each reports clean, then report the results to the user.

## Reader Personas

Adjust tone and assumed knowledge by document path. This is the master copy of these personas; other skills point here.

| Path | Readers | Assume | Prioritize |
|:-----|:--------|:-------|:-----------|
| `en/cloud/use-dify/` | Dify Cloud app builders; mix of developers and non-technical users | Basic AI familiarity; no infrastructure or deep coding knowledge — there is no deployment to operate | Task completion and outcomes; explain technical concepts when they appear |
| `en/self-host/use-dify/` | App builders whose team self-hosts Dify | Basic AI familiarity; no deep coding knowledge. Their deployment exists, so env vars are fine to mention — but the reader is a builder, not the operator | Task completion and outcomes; explain technical concepts when they appear; keep deployment mechanics one click away in the env reference |
| `en/self-host/deploy/` | DevOps engineers and system administrators | Strong infrastructure knowledge: Docker, databases, networking, environment variables | Precise technical detail; don't over-explain standard operations |
| `en/develop-plugin/` | Developers building custom Dify plugins | Strong Python skills; familiarity with Dify's core concepts | API contracts, extension points, code patterns; code examples are essential |

## Collaboration Model

The user brings documentation expertise and user empathy; you bring AI domain knowledge. Apply it actively:

- Explain why an AI concept is designed the way it is and what problem it solves, not just what it does (e.g., explain a tool role in conversation history at the LLM API mechanism level).
- When the user questions a product design, say whether it is Dify-specific or an industry norm, and how users are likely to understand it.
- Replace abstract explanations with concrete scenarios that show why a user needs the feature.
- When the user is unsure about phrasing, judge it from the reader's side: is the term understandable, accurate in the AI context, and close to the user's mental model?
- Flag unusual designs, likely misunderstood concepts, and inaccurate AI-domain terms unprompted.

## Environment Variables in User Guides

Applies when Step 2.6 found related variables. The two product copies fork — never mix the patterns:

- **Self-host copy** (`en/self-host/use-dify/`): name the mandatory variables and the values to set in a callout (rules below), and link to the reference. `environments.mdx` (maintained via `dify-docs-env-vars`) owns everything else: defaults, mechanisms (worker classes, proxy paths, scheme rules, fallbacks), interactions, and failure modes.
- **Cloud copy** (`en/cloud/use-dify/`): never any env-var content. A feature that is simply on in Dify Cloud gets nothing; a plan-limited feature gets the plan-gating pattern (`<Badge color="blue">Professional</Badge> and <Badge color="blue">Team</Badge>` in prose with a [Learn more](https://dify.ai/pricing) link — see "Paid Feature Callouts" in the style guide).

In the self-host copy:

1. Place the configuration in a callout, never a dedicated H2 section. Configuration enablement is an aside to the page's task flow, and the defaults and mechanics live one click away in the env reference.
2. Pick the callout type: `<Note>` when the variables are mandatory (the feature does not work at all without them); `<Info>` when they only customize behavior that already works.
3. Use this pattern — open with the feature state, never an audience qualifier (Step 4.2):

   ```mdx
   <Note>
   [Feature] is off by default. Enable it by setting:

   - `VAR_NAME` = `value`

   See [Environment Variables](/en/self-host/deploy/configuration/environments#var_name) for details.
   </Note>
   ```

4. Exclude from the user guide: default values, the "why" behind each variable, deployment-specific mechanics, and variable interactions — anything the reader finds one click into the reference.
