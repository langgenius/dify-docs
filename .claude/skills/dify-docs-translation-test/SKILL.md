---
name: dify-docs-translation-test
description: >
  Judge a zh or ja page as the owner of that edition would: a fresh agent
  reads it beside its English source against the language's formatting
  guide and the glossary, marks the sentences that fall short, and returns
  a ship verdict on the work of this round. Runs in the pipeline's Check
  stage after the editor test.
---

# Translation Test

The CJK linter measures mechanics. This test measures the translation: whether it says what the English says, in the language a native reader would write. It only measures anything if the judge has not seen the translating: a fresh sub-agent gets the translated page, its English source, the language's guide, and the glossary, and nothing else.

## Procedure

1. Agree the dispatch with the owner before sending anything: one judge per language per round is the usual shape, reading every page that round touched in that language; a page translated whole can have its own judge when the round is large. When no reviewer is in the session, state the dispatch in the report or PR description and proceed.
2. Dispatch the fresh sub-agent(s) (`subagent_type: general-purpose`) with the template below, filling `{LANG}` (Chinese or Japanese), `{GUIDE}` (`tools/translate/formatting-zh.md` or `tools/translate/formatting-ja.md`), `{GLOSSARY}` (`writing-guides/glossary.md`), `{SOURCE}` (the English page, absolute path), `{DRAFT}` (the translated page, absolute path), and `{CHANGED}` ("the whole page", or the sections and paragraphs this round changed). When one judge reads several pages, the page block (files 3 and 4 and the changed line) and the reply repeat per page, under the page's path. Put nothing else in the prompt.
3. Relay the report unedited. Then act on it as the editor test does: the verdict judges this round's work; "Ship with light edits" means fix the marked sentences, "Needs heavy edits" means retranslate the marked units whole from the English, "Needs retranslation" means a fresh translator takes the page from the English file on disk. A revised page goes to a new judge. Marks outside the change go to the owner as a list with a proposal for each.

## Dispatch prompt

```text
You are the editor of the {LANG} edition of a documentation set, reading a
translated page the way its owner would before deciding whether it can ship.

Read exactly these files, in this order:
1. {GUIDE}: the whole guide. Its translation-quality sections describe
   the failures you are looking for; the rest of the guide is context for
   them, and its formatting rules are checked elsewhere.
2. {GLOSSARY}: the terms and UI labels, with their {LANG} forms.

Then, for each page under review:
3. {SOURCE}: the English page. It is what the translation has to say.
4. {DRAFT}: the {LANG} page under review.
   This round changed: {CHANGED}. Read the whole page regardless; a
   sentence is judged in the context the page gives it.

Read nothing else and run no other command.

Mark every sentence that falls short, quoting it, with one tag each:
- meaning: says something the English does not, or drops something it
  does (a condition, a restriction, a qualifier such as "only")
- structure: carries the English clause structure or sentence order where
  a native writer would not
- register: a word in the wrong register for its context
- term: a general term whose {LANG} form is not the glossary's, or a UI
  label that does not correspond to the label the English page names
- tell: a translationese pattern the guide lists
- rule: breaks a translation rule the guide states and the tags above do
  not name (a standard phrase, a katakana convention, an app-type name);
  name the section

Then give one verdict on this round's work: Ship with light edits / Needs
heavy edits / Needs retranslation, with one sentence on what decided it.
Marks outside the change do not move the verdict; list them separately.

Do not check formatting, links, or facts beyond what the English page
says. Do not rewrite. Judge only whether a native reader would take this
page for one written in {LANG}.

Reply with exactly this, once per page, under the page's path:
- **Marked, in this change**: [quoted sentence — tag — five words on why; for rule, the section], one per line, or "none"
- **Marked, elsewhere on the page**: same form, or "none"
- **Best passage**: [the section that reads as written, in a phrase]
- **Verdict**: [one of the three, and the deciding sentence]
```
