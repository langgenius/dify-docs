---
name: dify-docs-editor-test
description: >
  Judge a finished draft as the docs owner would: a fresh agent reads it
  against the style guide's standard and the reference page in its genre,
  marks the sentences that fall short, and returns a ship verdict. Runs in the
  pipeline's Check stage before any linter.
---

# Editor Test

The linters measure mechanics. This test measures the writing, and it only measures anything if the judge has not seen the research: a fresh sub-agent gets the draft, the standard, the reference page, and the shape the page's type follows, and nothing else.

## Procedure

1. Dispatch one fresh sub-agent per page (`subagent_type: general-purpose`) with the template below, filling `{DRAFT}` (absolute path), `{STANDARD}` (the style guide's path; the agent reads only its opening section), `{EXEMPLAR}` (the reference page in the draft's genre: `en/cloud/use-dify/build/new-agent/overview.mdx` for a concept page, `build.mdx` for a task page or a reference), and `{SHAPE}` (the pack's page-shape or conventions section for this document type: the CLI pack's "Page shape", the API pack's `references/spec-conventions.md`, the env-var pack's document structure; for a page with no pack, the line reads "none"). The shape file keeps the judge from marking a required table or synopsis as a fault; the language inside the structure is still judged. Put nothing else in the prompt: no fact sheet, no research, no account of what changed, no concerns of your own.
2. Relay the report unedited. Then act on it. "Ship with light edits": fix the marked sentences. "Needs heavy edits": rewrite the marked units whole, from their job. "Needs rewrite": hand the draft and the marks to a fresh drafter, the pipeline's third tier. After either rewrite, dispatch a new judge; never send a revised draft to the same one.

## Dispatch prompt

```text
You are the editor of a documentation set, reading a draft the way its owner
would before deciding whether it can ship.

Read exactly these files, in this order:
1. {STANDARD}: read only the section titled "What a Good Page Does".
2. {EXEMPLAR}: a page the owner wrote. It calibrates register and judgment
   about what to leave out; the standard in file 1 is the authority. Do not
   copy it; measure against it.
3. {SHAPE}: the conventions this kind of page follows (its sections, tables,
   synopsis blocks). A structure the conventions require is not a fault;
   judge the sentences inside it. If this line reads "none", skip it.
4. {DRAFT}: the page under review.

Read nothing else and run no other command.

Mark every sentence in the draft that falls short of the bar, quoting it,
with one tag each:
- transcribed: a fact stated with no reader who would ask for it here
- reason: a why-clause on an instruction the reader would have followed anyway
- interface: describes what the reader can see on screen at that moment
- dense: two separable ideas in one sentence, or a paragraph that runs past
  the point where the reader's question changed
- vocabulary: a word from the code, the spec, or the team, not the product
- missing: a place the reader needed a judgment (what to choose, what to
  avoid, what happens if they get it wrong) and got a description

Then give one verdict: Ship with light edits / Needs heavy edits / Needs
rewrite, with one sentence on what decided it.

Do not check facts, formatting, links, or terminology. Do not rewrite. Judge
only whether this is writing the owner would put their name to.

Reply with exactly:
- **Marked**: [quoted sentence — tag — five words on why], one per line, or "none"
- **Best passage**: [the section that meets the bar, in a phrase]
- **Verdict**: [one of the three, and the deciding sentence]
```
