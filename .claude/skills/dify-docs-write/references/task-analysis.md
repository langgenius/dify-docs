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

Rules: every task is a user objective passing the "I want to ___" test — never a feature description. Every question carries exactly one route. OPEN questions are never dropped; they go into the S4 report.

## Depths

**Full (R1 / R2 / R4)**

1. Build the task list from the S2 research; cluster by journey. Cross-check against S2's community pain themes: each theme maps to a task, or is listed as explicitly out of scope.
2. Question walk — per task, walk its steps in the product. At each step answer four fixed prompts; write "none" when a prompt yields nothing (the prompt must still be answered):
   - **prereqs**: what must exist or be true before starting?
   - **mid-task**: what does the reader wonder right here?
   - **overlooked**: what detail, skipped now, breaks something later?
   - **success**: how does the reader confirm it worked?
3. Evidence check: answer immediately whatever S2 already answered, citing the evidence. Everything else is OPEN.

**Delta (R5)**

List only the tasks the change affects. For each, state what changes: steps, prereqs, limits, or outcome. Apply the four prompts to the changed steps only.

**Three-question (R3)**

Answer inside the S4 report: who is the reader; what task are they mid-way through; what must this text answer to keep them moving.

## Routing tests

- **docs** — the answer changes what the reader does and is not visible in the UI at the moment of need. Apply the style guide's "Repeating the UI" filter: UI-discoverable mechanics stay out of pages unless especially consequential.
- **ui-finding** — the answer belongs at the moment of need (a label, placeholder, tooltip, empty state, or default). A UI→docs help link is justified only when the decision is consequential AND the answer does not fit in a sentence AND the reader can act on what they would read there.
- **product-gap** — no good answer exists in the product or the docs.

ui-finding and product-gap items go into the S4 and S8 reports for maintainers to route onward. Never compensate for them silently in docs prose.
