---
name: dify-docs-reader-test
description: >
  Post-writing verification from the reader's perspective. Invoke after
  completing any documentation task to simulate a real user reading the
  document for the first time.
---

# Reader Experience Test

Verify a finished document by having a clean-context agent read it as the target reader, with no access to the source material, the codebase, or the writing conversation. The test only measures anything if the reader agent knows nothing you know: a subagent dispatched with the Agent tool starts with an empty context and knows only what its dispatch prompt says, so the steps below control exactly what that prompt contains.

## Procedure

1. **Get the persona.** Copy the reader persona verbatim from the writing skill used for the task: `dify-docs-guides` (Reader Personas, by document path), `dify-docs-env-vars` (Reader Persona), `dify-docs-api-reference` (Reader Persona), or `dify-cli-docs` (Reader segments). If the task used no writing skill with a persona, ask the user who the target reader is before dispatching.
2. **Dispatch one fresh subagent per document** with the Agent tool (`subagent_type: general-purpose`). Never run the test inline in the current conversation — this conversation contains the source context the reader must not have. The dispatch prompt is the template below verbatim, with two placeholders filled:
   - `{PATH}` — the absolute path to the finished document file. The input is the path, never pasted content: the test must run against the file on disk, not a possibly stale copy from the conversation.
   - `{PERSONA}` — the persona text from step 1, unmodified.
3. **Put nothing else in the dispatch prompt.** Each of these invalidates the test if included:
   - what the page covers, what changed, or why it was written
   - source material, code excerpts, codebase paths, or feature briefings
   - paths or links to other docs, the glossary, or the writing guides
   - your own summary of, concerns about, or questions about the draft
4. **Relay the subagent's report to the user unedited.** Add your own comments after it if needed, never merged into it.
5. **On a "Needs revision" verdict:** fix the document, then repeat from step 2 with a new subagent. Never send the revised document to the same subagent — it has context now and can no longer simulate a first-time reader. Repeat until the verdict is Clear or the user accepts the remaining gaps.

## Dispatch prompt template

```text
You are testing a documentation page by reading it as a first-time reader.

Read exactly one file: {PATH}

Do not read any other file, search the repository or the web, or run any
other command. Everything you may use is in that one file; if something
you need is missing, that is a finding to report, not a reason to look
elsewhere.

You are this reader:

{PERSONA}

Read the document once, top to bottom, as this person, and answer:

- Can I accomplish the task described without prior knowledge?
- Are there steps that assume context not provided on this page?
- Are there terms used without explanation?
- Is the information I need actually here, or do I have to guess?
- Do the code examples make sense on their own?
- After reading, do I know what to do next?

Do NOT review style or formatting, fact-check claims against any other
source, or rewrite anything. Only report where a first-time reader
struggles.

Reply with exactly this structure:

- **Got stuck at**: [section/step where understanding broke down, or "nowhere"]
- **Didn't understand**: [terms, concepts, or references that were unclear, or "nothing"]
- **Missing context**: [assumptions the document makes that weren't established, or "none"]
- **Verdict**: Clear / Minor gaps / Needs revision
```
