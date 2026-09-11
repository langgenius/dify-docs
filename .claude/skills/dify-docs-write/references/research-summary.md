# The Research Summary (S3)

The summary is what the drafter writes from, so its shape becomes the page's shape and its frame decides what the drafter does with a fact. It opens with its contract, groups facts under the question each section answers, and closes with what the page does not carry.

## The shape

```md
# Facts: [the page], verified at [repo, ref]

Every fact in a question-headed section is verified. Add no product fact
that is not on this sheet, and do not state every fact that is: a fact
goes on the page because the reader would ask for it at that section. The
closing lists hold what stays off the page, unverified claims included. Facts marked "background" are
here so you understand the product; the reader would not ask for them, so
they stay off the page.

## The writing task
[The page, its place in the nav, what it links to, and which sections are
being written.]

## Reader
[The persona, what they were just doing, and what they need next. The
reader block at the top of the drafting turn is filled from this.]

## [Section]: [the question the reader brings to it, in their words]
- [A fact that answers it, in product vocabulary, with the actor named and no claim about how long anything takes.]
- background: [a fact the drafter needs to understand the product.]

## Vocabulary
[The product's words, and the UI labels, bold when named as controls.]

## Visible in the UI at the moment of use: do not describe
- [What the screen shows when the reader is there, minus what is consequential enough to repeat: data loss, permissions, cost.]

## Not on this page
- [Owned by another page, with the link. Not true. Internal. Unverified, recorded here so it is reported and never stated.]
```

The session that did the research owns the two closing lists: what another page carries and what the screen shows are decisions about the doc set and the product, made with both in view. The drafter owns the rest, sentence by sentence: whether this reader, at this section, would ask for this fact. That judgment needs room, so the summary reaches the drafter slightly fuller than the page will be. A summary trimmed to exactly the page is an outline with facts, and it gets transcribed.

## One section, and the prose it became

A section of the summary for a page about testing a knowledge base:

```md
## Bad cases: the right chunk didn't come back, or came back too low. What do I do?
- From a run in Retrieval Test, click **Make bad case** and pick the reason: **Retrieval miss** (the chunk did not come back at all) or **Low score** (it came back ranked too low).
- A retrieval miss: first check how the document was processed (Review Processed Documents page); if it looks fine, widen the search with a deeper retrieval depth, a higher Top K, or a lower score threshold.
- A low score: a different rerank model, since the rerank model assigns the scores.
- Cases wait in **Quality** > **Bad cases**. **Replay** reruns the question with the current settings; **Promote** turns a case that now passes into a golden question and closes it; **Ignore** closes a case you will not fix.
- Bad cases also open on their own when a query from an app returns nothing.
- background: the knowledge base's reasoning model judges whether an app's empty result was a genuine miss before opening the case, and tags the case as coming from a workflow.
- background: one open bad case per query; a second for the same query is refused.
```

What the drafter wrote from it:

> When the right chunk is missing or ranked too low, click **Make bad case** under the run's results and pick the reason. Each points to a different fix:
>
> - **Retrieval miss**: the chunk didn't come back at all. First check how the document was processed in [Review Processed Documents](...). If it looks fine, widen the search with a deeper [retrieval depth](#retrieval-depth), a higher **Top K**, or a lower **Score Threshold** under [Retrieval Settings](#retrieval-settings).
> - **Low score**: the chunk came back but ranked too low. The rerank model assigns the scores, so try a different rerank model.
>
> Cases wait in **Quality** > **Bad cases**. After a fix, click **Replay** to rerun the question with the current settings. If the result is now right, click **Promote** to turn the case into a golden question and close it. **Ignore** closes a case you won't fix.
>
> Bad cases also open on their own when a question from one of your apps comes back with nothing, so check the list once your apps are live, not only while you're testing.

The two background facts stayed off the page. The fix for each reason went in whole, because that is the judgment the reader came for. The last bullet became a sentence with the reader's next move, which the summary did not state and did not need to: the product fact is the sheet's to verify, and what the reader does with it is the drafter's to say.
