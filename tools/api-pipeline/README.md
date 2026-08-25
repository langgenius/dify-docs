# API Pipeline

Tooling for the Service API reference. Dify's generated `service-openapi.json` is the base contract. Reviewed locale overlays add only localized prose, examples, Mintlify metadata, and published operation ID compatibility to produce `{lang}/api-reference/openapi_service.json`.

The composed language specs remain the human-readable authoring surface. After editing them, recapture the overlays from the reviewed Dify ref. CI rebuilds the specs from Dify plus those overlays and rejects stale output or an upstream change hidden under an overlay.

## Layout

| File | Role |
|:-----|:-----|
| `merge_specs.py` | `wire` (docs.json API menus + redirects) and `check-coverage` modes |
| `nav_labels.json` | Guides layout, two-tier reference config, per-group op ordering |
| `memberships.json` | App type → supported operations; drives the app-type overview pages and the coverage check |
| `lint_specs.py` | Example/schema, enum, link, and x-codeSamples lint |
| `parity_check.py` | en/zh/ja structural parity (ops, params, responses, samples) |
| `compose_service_api.py` | Captures and applies preconditioned locale overlays over Dify's generated contract |
| `service_api_overlays/{en,zh,ja}.json` | Generated locale overlays; every replace/remove action fingerprints its reviewed upstream value |
| `contract_alignment.py` | Generated-vs-composed wire-contract gate |
| `operation_id_overrides.json` | Compatibility overlay for operation IDs already published as SDK method names |
| `dify_ref.json` | Reviewed Dify commit and generated Service API spec digest used by CI |
| `coverage_matrix.py`, `swagger_diff.py` | Code-vs-spec audit tooling, for runtime verification (read `openapi_service.json`) |

## Usage

```bash
export DOCS="$(git rev-parse --show-toplevel)"
python3 "$DOCS/tools/api-pipeline/merge_specs.py" wire --lang en zh ja
python3 "$DOCS/tools/api-pipeline/merge_specs.py" check-coverage --lang en zh ja
python3 "$DOCS/tools/api-pipeline/lint_specs.py"
python3 "$DOCS/tools/api-pipeline/parity_check.py"
python3 -m unittest discover -s "$DOCS/tools/api-pipeline" -p 'test_*.py'
```

Every command exits nonzero when its checks fail. `lint_specs.py` also prints a `TOTAL ISSUES` summary for local diagnosis.

## Contract alignment

Generate the Service API spec from the exact Dify commit recorded in `dify_ref.json`, then compare it with all three localized docs specs. Use a clean detached worktree so uncommitted application changes cannot affect the result:

```bash
export DIFY_REPO=/path/to/dify
export DOCS="$(git rev-parse --show-toplevel)"
export DIFY_REF="$(python3 -c 'import json; print(json.load(open("tools/api-pipeline/dify_ref.json"))["ref"])')"
export DIFY="$(mktemp -d)/dify"
export GENERATED_DIR="$(mktemp -d)"
git -C "$DIFY_REPO" worktree add --detach "$DIFY" "$DIFY_REF"
uv run --project "$DIFY/api" "$DIFY/api/dev/generate_swagger_specs.py" --output-dir "$GENERATED_DIR"
python3 "$DOCS/tools/api-pipeline/compose_service_api.py" compose "$GENERATED_DIR/service-openapi.json"
python3 "$DOCS/tools/api-pipeline/contract_alignment.py" "$GENERATED_DIR/service-openapi.json"
git -C "$DIFY_REPO" worktree remove "$DIFY"
```

`compose_service_api.py compose` starts from the generated JSON and applies each locale overlay. An overlay action that replaces or removes an upstream value carries its SHA-256 fingerprint. If Dify changes that value, composition stops with a conflict. Changes outside overlay paths flow into the composed result and make the committed specs fail the current-output check. Every non-deprecated operation must also have localized Mintlify navigation metadata.

`compose_service_api.py capture` deliberately copies only presentation fields (`summary`, `description`, examples, documentation extensions, operation tags, and published `operationId` values). It never captures routes, parameters, request or response schemas, media types, headers, status codes, security, or deprecation flags from the rendered docs. Editing those fields in a localized output cannot override Dify's generated contract; the next compose restores the generated values.

The locale overlays also relocate Dify's generated `info.externalDocs` metadata to the OpenAPI 3.1 top-level `externalDocs` field. This presentation-only normalization keeps the composed document valid for Mintlify without changing the wire contract.

The alignment gate requires zero wire-contract differences: matching OpenAPI versions, exact public path/method coverage, matching deprecation flags, and semantically equivalent effective authentication requirements, parameters, request encodings, request media types, response headers, schemas, and statuses. It also validates schemas against the declared OpenAPI dialect: 3.0 specs cannot use keywords or array-form types outside the OpenAPI 3.0 Schema Object subset, while 3.1 specs cannot use the legacy `nullable` keyword or boolean exclusive bounds. Descriptions, examples, enum ordering, `x-mint`, and `x-codeSamples` are presentation and localization data; any other vendor extension remains part of the compared contract.

Previously published operation IDs are a compatibility contract because generated SDKs expose them as method names. `operation_id_overrides.json` preserves those IDs while new operations follow the generated contract.

If the generated JSON does not describe runtime behavior correctly, fix the code-side OpenAPI annotations in Dify and regenerate. Do not encode a wire-contract correction in a locale overlay.

`.github/workflows/check_service_api.yml` runs unit tests, example/link lint, localization parity, coverage, deterministic generation, composition, and contract alignment for every relevant pull request. The reviewed pin comes only from `dify_ref.json`. A daily scheduled run checks Dify `main`, and `repository_dispatch` or manual runs can supply another ref, so later upstream contract changes cannot remain invisible behind the pin.

### Update the localized specs

After reviewing a new Dify ref, compose the current overlays against it:

```bash
python3 "$DOCS/tools/api-pipeline/compose_service_api.py" compose "$GENERATED_DIR/service-openapi.json" --write
```

Unrelated upstream additions flow into the output. If the new contract touches an overlaid presentation value, review that location and update the localized spec deliberately. New operations require localized summaries, descriptions, tags, examples, and `x-mint` metadata before validation passes.

After editing the three composed specs, capture a new reviewed overlay set, then immediately rebuild and run the gates:

```bash
python3 "$DOCS/tools/api-pipeline/compose_service_api.py" capture "$GENERATED_DIR/service-openapi.json"
python3 "$DOCS/tools/api-pipeline/compose_service_api.py" compose "$GENERATED_DIR/service-openapi.json"
python3 "$DOCS/tools/api-pipeline/contract_alignment.py" "$GENERATED_DIR/service-openapi.json"
python3 "$DOCS/tools/api-pipeline/parity_check.py"
python3 "$DOCS/tools/api-pipeline/lint_specs.py"
```

## Editing the spec

- Edit all three composed language specs, then recapture their overlays; `parity_check` enforces structural parity with en.
- Every operation carries `x-mint.href = /{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}` (English slugs in every language, so the language switcher can map pages) and `x-mint.metadata.title`/`sidebarTitle` = the translated summary (without them, the custom href makes Mintlify label the sidebar from the English slug). Set all of these when adding an operation.
- The `tags` arrays must stay index-aligned across languages; `wire` maps translated tag labels by position and fails on a mismatch.
- Shared endpoints exist once, with availability lines and mode notes in the description; there is no cross-spec propagation anymore.
- After adding, removing, retitling, or reordering operations: update `memberships.json` (and the app-type overview pages) if availability changed, then run `wire`, `check-coverage`, and the lints. Description-only edits need no `wire`.

## URL scheme

`/{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}`. Legacy URLs are covered by wire-generated redirects: a catch-all to the English API home plus three knowledge-base exceptions embedded in the product UI.
