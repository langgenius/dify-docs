---
name: dify-docs-reader-test
description: >
  Post-writing verification from the reader's perspective. Invoke after
  completing any documentation task to simulate a real user reading the
  document for the first time.
---

# Reader Experience Test

## Purpose

Verify documentation from the reader's perspective. A clean-context agent reads the finished document as the target persona, with no access to source material, codebase, or prior conversation.

## How to Invoke

Dispatch a subagent with exactly two inputs:
1. The document content (the page just written or updated)
2. The reader persona description (from the writing skill being used)

Do NOT provide: source material, codebase access, prior conversation, or any context the reader wouldn't have.

## What the Test Agent Checks

- Can I accomplish the task described without prior knowledge?
- Are there steps that assume context not provided on this page?
- Are there terms used without explanation (and not in the glossary)?
- Is the information I need actually here, or do I have to guess?
- Do the code examples make sense on their own?
- After reading, do I know what to do next?

## What the Test Agent Does NOT Do

- Style or formatting review (that is the writer's job)
- Fact-check against the codebase (that is the writer's job)
- Rewrite anything—only report what was confusing

## Output Format

Structured feedback:
- **Got stuck at**: [section/step where understanding broke down]
- **Didn't understand**: [terms, concepts, or references that were unclear]
- **Missing context**: [assumptions the document makes that weren't established]
- **Verdict**: Clear / Minor gaps / Needs revision
