---
name: dify-docs-editor-test
description: >
  Judge a finished draft as the docs owner would: a fresh agent reads it
  against the style guide and the reference page in its genre, marks the
  sentences that fall short, and returns a ship verdict on the work of this
  round. Runs in the pipeline's Check stage before any linter.
---

# Editor Test

The linters measure mechanics. This test measures the writing, and it only measures anything if the judge has not seen the research: a fresh sub-agent gets the draft, the style guide, the reference page, and the shape the page's type follows, and nothing else.

## Procedure

1. Agree the dispatch with the owner before sending anything: how many judges, and what each reads. A page written or rewritten whole gets its own judge, unless several pages were drafted as one topic and the marks need the cross-page view, in which case one judge reads the set. A round that changed parts of pages sends the touched pages to one judge, each with its changed sections named, or to several judges split by topic when the set is large. Pages of different genres go to different judges, because the reference page differs. One judge per page is a choice, not the default. When no reviewer is in the session, state the dispatch in the report or PR description and proceed.
2. Dispatch the fresh sub-agent(s) (`subagent_type: general-purpose`) with the template below, filling `{DRAFT}` (absolute path), `{STANDARD}` (the style guide's path), `{EXEMPLAR}` (the reference page in the draft's genre: `en/cloud/use-dify/build/new-agent/overview.mdx` for a concept page, `en/cloud/use-dify/build/new-agent/build.mdx` for a task page or a reference), `{SHAPE}` (the pack's page-shape or conventions section for this document type: the CLI pack's "Page shape", the API pack's `references/spec-conventions.md`, the env-var pack's document structure; for a page with no pack, the line reads "none"), and `{CHANGED}` ("the whole page", or the sections and paragraphs this round changed, named as the reader would find them). When one judge reads several pages, the page block (files 3 and 4 and the changed line) and the reply repeat per page, under the page's path. The shape file keeps the judge from marking a required table or synopsis as a fault; the language inside the structure is still judged. Put nothing else in the prompt: no fact sheet, no research, no account of what changed beyond that line, no concerns of your own.
3. Relay the report unedited. Then act on it. The verdict judges this round's work. "Ship with light edits": fix the marked sentences. "Needs heavy edits": rewrite the marked units whole, from their job. "Needs rewrite": hand the draft and the marks to a fresh drafter, as the pipeline's Write stage does for a changed idea. After either rewrite, dispatch a new judge; never send a revised draft to the same one. Marks outside the change are the page's standing debt: report them to the owner as a list with a proposal for each (fix in this round, or a follow-up), and touch none of them without that decision, because on a release branch a page's debt is not this round's scope.

## Dispatch prompt

```text
You are the editor of a documentation set, reading a draft the way its owner
would before deciding whether it can ship.

Read exactly these files, in this order:
1. {STANDARD}: the whole style guide. Its opening section, "What a Good
   Page Does", is the standard; the sections after it are the rules a
   page also has to meet.
2. {EXEMPLAR}: a page the owner wrote. It calibrates register and judgment
   about what to leave out; the standard in file 1 is the authority. Do not
   copy it; measure against it.
Then, for each page under review:
3. {SHAPE}: the conventions this kind of page follows (its sections, tables,
   synopsis blocks). A structure the conventions require is not a fault;
   judge the sentences inside it. If this line reads "none", skip it.
4. {DRAFT}: the page under review.
   This round changed: {CHANGED}. Read the whole page regardless: a
   sentence is judged in the context the page gives it, and a change is
   judged by whether it fits the page it landed in.

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
- rule: breaks a rule in a later section of the style guide; name the section

Then give one verdict on this round's work: Ship with light edits / Needs
heavy edits / Needs rewrite, with one sentence on what decided it. Marks
outside the change do not move the verdict; list them separately.

Do not check facts, formatting, links, or terminology. Do not rewrite. Judge
only whether this is writing the owner would put their name to.

Reply with exactly this, once per page, under the page's path:
- **Marked, in this change**: [quoted sentence — tag — five words on why; for rule, the section], one per line, or "none"
- **Marked, elsewhere on the page**: same form, or "none"
- **Best passage**: [the section that meets the bar, in a phrase]
- **Verdict**: [one of the three, and the deciding sentence]
```
