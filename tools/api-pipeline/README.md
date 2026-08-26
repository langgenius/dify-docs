# API Pipeline

Tooling for the Service API reference. During the generated-contract migration, Dify's generated `service-openapi.json` owns the wire contract in `{lang}/api-reference/openapi_service.json`; the locale files continue to own presentation fields. Overlay extraction follows after the generated and documented contracts are aligned.

## Layout

| File | Role |
|:-----|:-----|
| `merge_specs.py` | `wire` (docs.json API menus + redirects) and `check-coverage` modes |
| `nav_labels.json` | Guides layout, two-tier reference config, per-group op ordering |
| `memberships.json` | App type → supported operations; drives the app-type overview pages and the coverage check |
| `lint_specs.py` | Example/schema, enum, link, and x-codeSamples lint |
| `parity_check.py` | en/zh/ja structural parity (ops, params, responses, samples) |
| `align_service_api.py` | Migration-stage alignment from Dify's generated contract while preserving locale presentation |
| `service_api_source.json` | Reviewed Dify commit and generated Service API digest |
| `coverage_matrix.py`, `swagger_diff.py` | Code-vs-spec audit tooling, for runtime verification (read `openapi_service.json`) |

## Usage

```bash
export DOCS="$(git rev-parse --show-toplevel)"
python3 "$DOCS/tools/api-pipeline/merge_specs.py" wire --lang en zh ja
python3 "$DOCS/tools/api-pipeline/merge_specs.py" check-coverage --lang en zh ja
python3 "$DOCS/tools/api-pipeline/lint_specs.py"
python3 "$DOCS/tools/api-pipeline/parity_check.py"
```

parity_check.py and check-coverage exit nonzero on failure; lint_specs.py exits nonzero only on missing files — gate on its printed `TOTAL ISSUES` count.

## Align with Dify

Generate `service-openapi.json` from the exact Dify commit recorded in `service_api_source.json`. Then align all three locale specs:

```bash
python3 "$DOCS/tools/api-pipeline/align_service_api.py" /path/to/service-openapi.json --write
python3 "$DOCS/tools/api-pipeline/align_service_api.py" /path/to/service-openapi.json
```

For the initial migration, `--presentation-root` can point to a checkout of
the pre-alignment docs so presentation follows schemas that the generator
moved behind `$ref` components. Subsequent runs use the committed locale specs.

The aligner takes paths, methods, parameters, schemas, status codes, authentication, deprecation flags, and operation IDs from Dify. It preserves localized prose, examples, operation tags and ordering, `x-mint`, `x-codeSamples`, top-level navigation tags, and the absolute server template used by the Mintlify playground. Existing JSON object keys retain their reviewed order, with generated-only keys appended, to keep contract updates diff-friendly.

## Editing the spec

- Edit all three languages; `parity_check` enforces structural parity with en.
- Every published operation carries `x-mint.href = /{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}` (English slugs in every language, so the language switcher can map pages) and `x-mint.metadata.title`/`sidebarTitle` = the translated summary (without them, the custom href makes Mintlify label the sidebar from the English slug). Generated operations without `x-mint` remain in the wire contract but are excluded from the documentation navigation.
- The `tags` arrays must stay index-aligned across languages; `wire` maps translated tag labels by position and fails on a mismatch.
- Shared endpoints exist once, with availability lines and mode notes in the description; there is no cross-spec propagation anymore.
- After adding, removing, retitling, or reordering operations: update `memberships.json` (and the app-type overview pages) if availability changed, then run `wire`, `check-coverage`, and the lints. Description-only edits need no `wire`.

## URL scheme

`/{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}`. Legacy URLs are covered by wire-generated redirects: a catch-all to the English API home plus three knowledge-base exceptions embedded in the product UI.
