---
name: dify-docs-guides
description: >
  Rule pack for Dify user-guide pages — en/{cloud,self-host}/use-dify/,
  en/develop-plugin/, and en/self-host/deploy/. Carries the reader personas
  (master copy), audience-voice rules, dual-copy discipline, and env-var
  presentation patterns. Loaded by dify-docs-write; not an entry point.
---

# User Guide Rules

Not an entry point — run under `dify-docs-write`; this pack's rules and procedures implement its stages for user-guide pages.

## Scoping rules (S1)

Match each target page to its reader persona (see Reader Personas below). `use-dify` pages exist as two product copies — `en/cloud/use-dify/` and `en/self-host/use-dify/` — with no shared pages and no cross-audience navigation. When the page exists in both, scope both: shared-content improvements land in both copies in the same pass; audience-specific blocks (plan gating, env-var callouts, Enterprise tips) stay per-copy. Exception — work on a `release/<version>` branch edits only the self-host copy, still in all three languages; what it excludes is the cloud copy, which follows Cloud's own release lane (see the dify-docs-release-sync skill § Docs Branch).

## S2 discovery — environment variables

Check for feature-related environment variables. In the Dify codebase, run:

```bash
grep -rn "<FEATURE_KEYWORD>" docker/.env.example docker/envs/ api/configs/
```

Use the feature's name as it would appear in a variable (e.g. `COLLABORATION`); try 2–3 keyword variants before concluding. No matches → the feature has no env-var surface; skip the env-var guidance below. Matches → record each variable as mandatory or optional plus its default, and queue the `dify-docs-env-vars` pack's procedure in the S4 scope report, to update `en/self-host/deploy/configuration/environments.mdx` in the same session — that reference is the single source of truth for variable semantics.

## Drafting rules (S5)

1. Write for the persona of the page's path (see Reader Personas below).
2. Never restate the page's own audience. Everyone on a self-host page is self-hosted and everyone on a cloud page is on Dify Cloud, so "On self-hosted deployments, …" and "On Dify Cloud, …" are banned on their own pages. Audience qualifiers are legitimate only on the audience-neutral trees (`en/learn/`, `en/api-reference/`, `en/cli/`, `en/develop-plugin/`), where they genuinely disambiguate. Two carve-outs are deliberate and stay: naming a different product (the `<Tip>` surfacing Dify Enterprise where a CE capability ends — see "Paid Feature Callouts" in the style guide), and a comparative-advantage claim, where the qualifier marks something this product has that the other lacks ("On Dify Cloud, many popular trigger integrations are pre-configured" — the point is the perk, not the scope). Scoping restatement is banned; advantage framing is not.
3. If S2 discovery found related environment variables, present them per Environment Variables in User Guides below.

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

Applies when S2 discovery found related variables. The two product copies fork — never mix the patterns:

- **Self-host copy** (`en/self-host/use-dify/`): name the mandatory variables and the values to set in a callout (rules below), and link to the reference. `environments.mdx` (maintained via the `dify-docs-env-vars` pack) owns everything else: defaults, mechanisms (worker classes, proxy paths, scheme rules, fallbacks), interactions, and failure modes.
- **Cloud copy** (`en/cloud/use-dify/`): never any env-var content. A feature that is simply on in Dify Cloud gets nothing; a plan-limited feature gets the plan-gating pattern (`<Badge color="blue">Professional</Badge> and <Badge color="blue">Team</Badge>` in prose with a [Learn more](https://dify.ai/pricing) link — see "Paid Feature Callouts" in the style guide).

In the self-host copy:

1. Place the configuration in a callout, never a dedicated H2 section. Configuration enablement is an aside to the page's task flow, and the defaults and mechanics live one click away in the env reference.
2. Pick the callout type: `<Note>` when the variables are mandatory (the feature does not work at all without them); `<Info>` when they only customize behavior that already works.
3. Use this pattern — open with the feature state, never an audience qualifier (Drafting rule 2):

   ```mdx
   <Note>
   [Feature] is off by default. Enable it by setting:

   - `VAR_NAME` = `value`

   See [Environment Variables](/en/self-host/deploy/configuration/environments#var_name) for details.
   </Note>
   ```

4. Exclude from the user guide: default values, the "why" behind each variable, deployment-specific mechanics, and variable interactions — anything the reader finds one click into the reference.
