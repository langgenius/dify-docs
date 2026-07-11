# API Pipeline

Tooling for the Service API reference. `{lang}/api-reference/openapi_service.json` is the hand-maintained spec of record per language: edit it directly. The Phase-1 merge machinery (`build`/`relink` modes, `resolutions.json`, `overrides/`) that consolidated the five legacy per-app-type specs is retired; recover it from git history when Phase 2 rebuilds the spec from R&D's generated spec plus docs-owned overlays.

## Layout

| File | Role |
|:-----|:-----|
| `merge_specs.py` | `wire` (docs.json API menus + redirects) and `check-coverage` modes |
| `nav_labels.json` | Guides layout, two-tier reference config, per-group op ordering |
| `memberships.json` | App type → supported operations; drives the app-type overview pages and the coverage check |
| `lint_specs.py` | Example/schema, enum, link, and x-codeSamples lint |
| `parity_check.py` | en/zh/ja structural parity (ops, params, responses, samples) |
| `coverage_matrix.py`, `swagger_diff.py` | Code-vs-spec audit tooling, for runtime verification (read `openapi_service.json`) |

## Usage

```bash
export DOCS="$(git rev-parse --show-toplevel)"
python3 "$DOCS/tools/api-pipeline/merge_specs.py" wire --lang en zh ja
python3 "$DOCS/tools/api-pipeline/merge_specs.py" check-coverage --lang en zh ja
python3 "$DOCS/tools/api-pipeline/lint_specs.py"
python3 "$DOCS/tools/api-pipeline/parity_check.py"
```

All checks exit nonzero on failure.

## Editing the spec

- Edit all three languages; `parity_check` enforces structural parity with en.
- Every operation carries `x-mint.href = /{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}` (English slugs in every language, so the language switcher can map pages) and `x-mint.metadata.title`/`sidebarTitle` = the translated summary (without them, the custom href makes Mintlify label the sidebar from the English slug). Set all of these when adding an operation.
- The `tags` arrays must stay index-aligned across languages; `wire` maps translated tag labels by position and fails on a mismatch.
- Shared endpoints exist once, with availability lines and mode notes in the description; there is no cross-spec propagation anymore.
- After adding, removing, retitling, or reordering operations: update `memberships.json` (and the app-type overview pages) if availability changed, then run `wire`, `check-coverage`, and the lints. Description-only edits need no `wire`.

## URL scheme

`/{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}`. Legacy URLs are covered by wire-generated redirects: a catch-all to the English API home plus three knowledge-base exceptions embedded in the product UI.
