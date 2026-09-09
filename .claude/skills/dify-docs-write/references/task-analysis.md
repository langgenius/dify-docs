# Task Analysis & Reader Questions (S3)

The pre-draft half of reader empathy: establish what readers are trying to do and what they will wonder, before any prose exists. (`dify-docs-reader-test` is the post-draft half.)

## Output schema (every depth)

```
## Tasks
- T1 [journey: set up | build | maintain | verify | consume]: I want to <objective>
## Questions
- Q1 (T1): <what the reader wonders or overlooks> — answer: <one sentence + evidence, or OPEN>
  route: docs → <page/section> | ui-finding | product-gap
```

A task is something the reader wants to do, phrased so "I want to ___" reads naturally, and it comes from the persona's own journeys through the product. Research findings, issue text, and briefing bullets tell you what is in scope and supply evidence; they don't tell you what readers are trying to do, because an issue bullet is a directive and a reader is not. A task you can't walk as concrete product steps isn't a task. Every question gets one route, and OPEN questions go into the scope report rather than being dropped.

## Depths

**Full (new page, rewrite, pre-release feature)**

1. Build the task list from the persona's journeys, with the S2 research as evidence; cluster by journey. Cross-check against S2's community pain themes: each theme maps to a task, or is listed as explicitly out of scope.
2. Question walk — per task, walk its steps in the product and, at each step, look for four things:
   - **prereqs**: what must exist or be true before starting?
   - **mid-task**: what does the reader wonder right here?
   - **overlooked**: what detail, skipped now, breaks something later?
   - **success**: how does the reader confirm it worked?
3. Evidence check: answer immediately whatever S2 already answered, citing the evidence. Everything else is OPEN.

**Delta (update)**

List only the tasks the change affects. For each, state what changes: steps, prereqs, limits, or outcome. Apply the four prompts to the changed steps only.

**Three-question (correction)**

Answer inside the S4 report: who is the reader; what task are they mid-way through; what must this text answer to keep them moving.

## Routing tests

- **docs** — the answer changes what the reader does and is not visible in the UI at the moment of need. Apply the style guide's "Repeating the UI" filter: UI-discoverable mechanics stay out of pages unless especially consequential.
- **ui-finding** — the answer belongs at the moment of need (a label, placeholder, tooltip, empty state, or default). A UI→docs help link is justified only when the decision is consequential AND the answer does not fit in a sentence AND the reader can act on what they would read there.
- **product-gap** — no good answer exists in the product or the docs.

ui-finding and product-gap items go into the S4 and S8 reports for maintainers to route onward. Never compensate for them silently in docs prose.
