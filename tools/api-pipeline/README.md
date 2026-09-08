# API Pipeline

Builds `{en,zh,ja}/api-reference/openapi_service.json` from Dify's generated Service API contract and language-specific documentation annotations. The contract comes from a pinned Dify commit; descriptions, examples, translated labels, and existing page URLs live in the overlays. Updates are manual and reviewed together in a PR.

## Layout

| File | Role |
|:-----|:-----|
| `upstream/service-openapi.json` | Unmodified Dify export for `/v1` |
| `upstream/source.json` | Source repository, full commit SHA, and snapshot checksum |
| `publication.json` | Explicitly excludes the root operation and five deprecated aliases, with reasons |
| `overlays/{en,zh,ja}.json` | Documentation annotations, including legacy operation IDs and Mintlify page metadata |
| `build_specs.py` | Import a snapshot, build the three specs, or capture reviewed annotations |
| `validate_specs.py` | OpenAPI 3.1 validation and media, parameter, and schema example validation |
| `merge_specs.py` | `wire` updates navigation and redirects; `check-coverage` checks overview links |
| `nav_labels.json`, `memberships.json` | Navigation labels/order and app-type availability |
| `lint_specs.py`, `parity_check.py` | Documentation lint, complete contract parity, and language-switcher URL parity |
| `coverage_matrix.py`, `swagger_diff.py` | Optional code/runtime comparison aids for manual audits |

The snapshots, overlays, tooling, and skill instructions are internal; `.mintignore` excludes `tools/` and `.claude/` from publication. Commit the generated language specs with their inputs.

## Update from Dify

Use a clean Dify checkout at the selected release tag or commit. Follow `writing-guides/index.md` for creating an isolated checkout; do not change an occupied working tree's branch. Set absolute paths below and record the checkout's full SHA:

```bash
export DOCS="$(git rev-parse --show-toplevel)"
DIFY_SOURCE=/absolute/path/to/dify-checkout
DIFY_REVISION=$(git -C "$DIFY_SOURCE" rev-parse HEAD)
DIFY_EXPORT=$(mktemp -d)
```

1. Export using that checkout's locked API dependency environment:

   ```bash
   uv run --project "$DIFY_SOURCE/api" --frozen python "$DIFY_SOURCE/api/dev/generate_swagger_specs.py" --output-dir "$DIFY_EXPORT"
   python3 "$DOCS/tools/api-pipeline/build_specs.py" import \
     --spec "$DIFY_EXPORT/service-openapi.json" --revision "$DIFY_REVISION"
   ```

   Import only `service-openapi.json`, not the console, web, or OpenAPI-platform export. `import` records the snapshot and its provenance; it does not update the published specs.

2. Review the raw snapshot diff against the previous version. Check changed routes, request/response schemas, constraints, status codes, and authentication against Dify. Review the existing overlay text and examples wherever behavior changed: a patch can still apply while its wording becomes stale.

3. Build, then edit the generated specs' descriptions, examples, and page metadata in all three languages:

   ```bash
   python3 "$DOCS/tools/api-pipeline/build_specs.py" build
   ```

   A removed annotation target fails the build. Update or remove the affected overlay entry after reviewing the source change. New operations also need translated summaries/tags and `x-mint` page metadata before the build can pass; see below.

4. After reviewing the three language files, capture their documentation changes and verify reproducibility:

   ```bash
   python3 "$DOCS/tools/api-pipeline/build_specs.py" capture
   python3 "$DOCS/tools/api-pipeline/build_specs.py" build --check
   ```

   `capture` rejects technical changes, including fields, types, `$ref`, `required`, `enum`, response statuses, and security. Fix those in Dify and export/import again. Do not delete response constraints or rewrite references for rendering. Capture saves annotations; it does not verify their meaning.

5. Run the checks below and review the generated pages. Commit the snapshot, provenance, overlays, three generated specs, and any navigation changes together.

## Documentation-only changes

With the existing snapshot, edit prose/examples in all three generated specs, run `capture`, then `build --check` and the checks below. Keep existing `operationId` values and `x-mint.href` URLs. Historical IDs may differ between languages; contract parity does not rename them.

Every published operation needs `x-mint.href = /{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}` and translated `x-mint.metadata.title`/`sidebarTitle`. Keep tag arrays aligned across languages. For new operations, add these annotations in each overlay, update `memberships.json`, `nav_labels.json` as needed, and the relevant app-type overview pages. Review `publication.json` when upstream adds or removes an excluded operation; exclusions must remain explicit and justified.

After adding/removing operations or changing labels, order, or availability, regenerate navigation with `wire`. Description-only changes do not need it. Shared endpoints appear once per language, with availability and mode-specific notes in their descriptions.

## Checks

```bash
python3 "$DOCS/tools/api-pipeline/build_specs.py" build --check
uvx --from openapi-spec-validator==0.9.0 python "$DOCS/tools/api-pipeline/validate_specs.py"
python3 "$DOCS/tools/api-pipeline/lint_specs.py"
python3 "$DOCS/tools/api-pipeline/parity_check.py"
python3 "$DOCS/tools/api-pipeline/merge_specs.py" wire --lang en zh ja
python3 "$DOCS/tools/api-pipeline/merge_specs.py" check-coverage --lang en zh ja
```

These commands exit nonzero on failure. Validation checks the raw snapshot and all three outputs; parity checks the complete technical contract and matching page URLs. The checks do not establish runtime behavior, translation accuracy, or the correctness of error triggers and streaming narratives: review those against the pinned code and inspect the rendered pages.

For a response with both JSON and SSE content, keep examples on both media types. Mintlify CLI 4.2.629 can replace the JSON examples with generated placeholders when the SSE media type has no example. A verified SSE excerpt avoids that rendering issue without changing the schema.

When changing the tooling, also run its regression tests:

```bash
uvx --from openapi-spec-validator==0.9.0 python -m unittest discover -s "$DOCS/tools/api-pipeline" -p 'test_*.py'
```
