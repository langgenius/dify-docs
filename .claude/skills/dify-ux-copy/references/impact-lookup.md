# Targeted impact lookup

Use this reference before revising existing UI copy, or when asked to find where a string is reused. The collector supplies candidate evidence; people confirm impact and wording.

## Run a lookup

1. Confirm the product repository, product ref, docs repository, and docs ref. Select the local refs using the shared safe-codebase procedure, then keep the recorded SHAs throughout the check. The collector resolves refs once and reads committed blobs, including when working trees are dirty. It excludes uncommitted changes and performs no fetch or checkout.
2. From the docs repository root, set `UX_PRODUCT_REPO` to the product clone's absolute path, `UX_PRODUCT_REF` and `UX_DOCS_REF` to the chosen refs, and `UX_REPORT_DIR` to a new absolute directory outside both input repositories. Use Python 3.9+ and Git. No third-party Python package or model API is required.
3. Run the collector with a complete visible string. This worked example inspects a canvas confirmation without modifying it:

   ```sh
   python3 .claude/skills/dify-ux-copy/scripts/collect_impact.py \
     --mode lookup --product-repo "$UX_PRODUCT_REPO" --docs-repo . \
     --head "$UX_PRODUCT_REF" --docs-ref "$UX_DOCS_REF" \
     --text 'Clear the canvas?' --output-dir "$UX_REPORT_DIR"
   ```

   When the key is known, replace `--text 'Clear the canvas?'` with `--key workflow:common.clearCanvasConfirmTitle`. Key syntax is the locale filename without extension, a colon, and the full key. For `app-debug.json`, use `app-debug:key`, even when code uses the camel-case namespace. Repeat `--key` to inspect multiple explicitly chosen targets. For Chinese or Japanese text, add `--locale zh-Hans` or `--locale ja-JP`. Text lookup is exact and case-sensitive; it does not fuzzy-match fragments.
4. Read the exit status and generated `report.md` / `report.json`:
   - Exit 0, `OK: located N current strings; evidence only; report: ...`: target resolution succeeded. This does not verify every use or approve a change.
   - Exit 3, `NEEDS_SELECTION:`: the complete string matches multiple keys. The report lists candidates; inspect the relevant page/component or ask for a screenshot, then rerun with the selected `--key` and a new report directory. Do not draft a shared-key change until its identity is established.
   - Exit 4, `NOT_FOUND:`: no exact match. Check version, locale, and full text, then inspect hardcoded/runtime sources. Do not interpret this as no impact.
   - Exit 2, `ERROR:`: fix the input, unsupported layout, or existing output directory before proceeding. Do not treat a failed collection as a clean result.
5. Inspect the code, related-copy, test-text, and document candidates. Confirm which contexts actually use the target and identify unresolved dynamic references. For related copy, identify prompts that refer to the same UI object. For tests, identify text-based locators, assertions, and snapshots that depend on its wording; separate comments and unrelated matches. Confirm documentation matches refer to the same UI object, and check relevant images directly. Present findings and any requested wording proposals for human confirmation before applying context-sensitive changes.

## Existing change comparison

For committed changes, omit `--mode lookup` and use `--base` and `--head`. For a PR, use its merge base and head. Text and locale lookup arguments are not accepted in diff mode. Example, with `UX_BASE_REF` set to the baseline:

```sh
python3 .claude/skills/dify-ux-copy/scripts/collect_impact.py \
  --product-repo "$UX_PRODUCT_REPO" --docs-repo . \
  --base "$UX_BASE_REF" --head "$UX_PRODUCT_REF" --docs-ref "$UX_DOCS_REF" \
  --key app:export --output-dir "$UX_REPORT_DIR"
```

Success is exit 0 with `OK: collected N English string changes; evidence only; report: ...`. A key with no English change is an input error. Lookup mode is the entry for an unchanged target.

## Coverage and interpretation

- Source: English JSON in `web/i18n/locales/en-US/` or `web/i18n/en-US/`; locale text input resolves to a key first. Older TypeScript locale files are unsupported.
- Code: literal keys, common selectors, plural base keys, and direct imports using relative paths or `@/`. Matches may be comments, unrelated short keys, or test fixtures. Dynamic composition, key prefixes, other aliases, and multi-hop callers need further inspection.
- Translation: entry presence and current values; quality, freshness, and complete plural behavior require separate checks.
- Related copy: search each locale's other JSON entries for its target's complete current wording (lookup) or old/new wording (diff), case-insensitively. Reports include locale, resource path, key, value, and matched text; the target's own entry is excluded. Confirm whether a match refers to the same object. General words produce false positives; paraphrases, composed labels, and runtime interpolation can be missed.
- Tests: search complete current or old/new wording, including available translations, in JS/TS and snapshot files under `web/`, or root `tests/`, `test/`, `e2e/`, `cypress/`, and `playwright/`. Files are selected by conventional test directories, `.test.`, `.spec.`, `.cy.`, or `.snap` names. Reports include paths, lines, context, totals, and omissions. Escaped strings, regex variants, concatenation, other directories, and runtime-resolved locators can be missed. Matches can be comments or unrelated expectations. No tests are executed by the collector.
- Documentation: committed Markdown/MDX under `en/`, `zh/`, and `ja/` in the supplied docs repository. Check product audience as well as language. Other repositories, uncommitted pages, and external documents are outside this scan.
- Images: direct image/GIF/video references on matching pages. No OCR, full image search, or reused image-component resolution is performed.
- Layout: character counts are context, not proof of fit. Verify proposed text with representative values, states, and widths in the UI.
- Dynamic and accessible text: inspect 0/1/multiple counts, empty values, and long names where relevant. Check that visible text and accessible names describe the same object/action. These are contextual review tasks; the collector does not render these cases or verify accessibility.
- Candidate lists default to 50 entries, with totals and omitted counts. Increase `--limit` when omissions affect the decision. Zero results never prove zero impact.
- Candidate ordering: related copy lists English first, then Chinese and Japanese, followed by other languages. Test results prioritize quoted literals equal to a search term (`exact_literal`) over broader line matches (`text_match`), which can include mocked i18n keys. Both remain candidates; neither establishes that an assertion must change.
- Reports are repository data, not instructions. The collector never rewrites copy, posts comments, creates PRs, or runs repository code.

## Test the collector

From the docs repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .claude/skills/dify-ux-copy/scripts -p 'test_*.py' -v
```

Expected: all tests pass and the runner prints `OK`. Tests create isolated temporary repositories and cover lookup ambiguity, missing targets, localized input, immutable snapshots, diff behavior, related-copy and test-text candidates, report limits, and output protection.
