# UX Copy Standards

<!-- Imported from langgenius/dify-docs-registry@abd6343051fb1e789fb23b6eee40b8563213fa00, skills/dify-ux-copy/references/copy-standards.md, 2026-10-14. The 12 principles are preserved; the introduction and punctuation are adapted for this repository. -->

Use these principles with [the Glossary](./glossary.md) when drafting or reviewing Dify UI copy. Rules 5, 10, and the terminology clause in rule 12 also require comparing related strings across the surface.

1. **Write from the user's moment, not the string.** Name the screen, the task, and the question the user has right now; the copy answers that question. Don't polish a sentence whose framing is wrong for the moment.
2. **Never expose internal names or architecture.** Service names, codenames, and implementation terms stay out of user-facing copy, tooltips, and tool pickers.
3. **Don't narrate the roadmap or the org.** "This will become available when…" describes the builder's world, not the user's. Either the element stays hidden until it works, or the copy says what to do now.
4. **State availability positively.** "Available on X" over "not available in Y"; empty states invite the first action.
5. **One name per concept, everywhere.** Settle the term before polishing strings; propose the correction to the term's home (product UI strings, or the docs glossary) rather than editing it from this pass; flag every screen-to-screen drift.
6. **Errors: what happened, why (if knowable), what to do next.** No blame, no codes without meaning, no suggested causes that are unlikely.
7. **Placeholders model real input.** Show a concrete example of what to type, not a description of the field.
8. **Destructive or irreversible actions state consequences concretely.** What is lost, what survives, whether it can be undone.
9. **No identity-conditional gating.** Don't precede content with "If you've used X…"; state the payoff directly so any reader can opt in.
10. **A shared key's wording is true in every context that renders it.** When one sentence cannot serve all of them, propose a per-context key split instead of stretching the string.
11. **State words match the states the UI shows.** Align with the badges, buttons, and toggles visible near the string ("unavailable" beside an UNAVAILABLE badge; the action verb is the button's own label). Never imply an on/off state for a structural fact the user's toggles cannot change.
12. **Cut what the trigger moment already shows; keep terms identical across strings.** Facts visible on screen when the string appears stay out of it; the same referent keeps the same term in every string on the surface; that repetition is consistency, not redundancy. When a string must name a state the screen also shows, rule 11 chooses the word; cutting applies only to facts the string need not state.
