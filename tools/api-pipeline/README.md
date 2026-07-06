# API Pipeline (Phase 1)

Consolidates the five per-app-type Service API specs into one `openapi_service.json` per language, and generates the docs.json wiring for it. Phase 2 swaps the input to R&D's code-generated spec plus docs-owned overlays; the merge, wiring, and check logic here carries over.

## Layout

| File | Role |
|:-----|:-----|
| `merge_specs.py` | The pipeline: `analyze`, `build`, `wire`, `relink`, `check-coverage` modes |
| `resolutions.json` | Explicit choice for every divergence between the five input specs |
| `overrides/strings.json` | Per-language strings injected by resolutions (mode notes, merged descriptions) |
| `overrides/chat-messages-sse.{en,zh,ja}.md` | Hand-merged mode-aware SSE documentation for `POST /chat-messages` |
| `nav_labels.json` | docs.json Guides order, two-tier reference config, per-group op ordering |
| `memberships.json` | App type → supported operations; drives availability lines, app-type pages, and the coverage lint |
| `lint_specs.py` | Example/schema, enum, link, and x-codeSamples lint (all specs) |
| `parity_check.py` | en/zh/ja structural parity |
| `coverage_matrix.py`, `swagger_diff.py`, `compose.swagger.yml` | Audit-era code-vs-spec tooling, kept for runtime verification |

## Usage

```bash
DOCS="$(git rev-parse --show-toplevel)"   # scripts default to repo root
python3 tools/api-pipeline/merge_specs.py analyze --lang en --report /tmp/overlap.md
python3 tools/api-pipeline/merge_specs.py build --lang en zh ja --report /tmp/reports
python3 tools/api-pipeline/merge_specs.py wire --lang en zh ja
python3 tools/api-pipeline/merge_specs.py relink --lang en zh ja
DOCS="$PWD" python3 tools/api-pipeline/lint_specs.py
DOCS="$PWD" python3 tools/api-pipeline/parity_check.py
```

- `build` refuses to run while any spec divergence lacks a `resolutions.json` entry; unresolved same-name components are namespaced per spec (rendering-preserving) and printed.
- `build --report` writes per-language render-diff reports: every operation whose fully-dereferenced rendering differs from its source spec, for review.
- `wire` regenerates the three-group API menu in docs.json (Guides / App APIs / Knowledge API, all languages × products) and the legacy-URL redirects (flattening chains). The per-app-type `overview.mdx` pages are hand-maintained content; `check-coverage` fails the build if a page misses a supported endpoint link.
- `relink` rewrites legacy `/api-reference/...` links in MDX bodies to the new language-prefixed URLs.

## URL scheme

Every operation carries `x-mint.href = /{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}`. The slug is English-derived in all languages so the language switcher can map pages across languages; sidebar labels stay localized via the translated `summary` fields. Legacy per-language URLs (`/api-reference/{tag}/{summary}`, CJK slugs included) redirect to the new pages via generated docs.json redirects.

## Inputs

The five per-app-type specs (`{lang}/api-reference/openapi_{chat,chatflow,workflow,completion,knowledge}.json`) are no longer referenced by docs.json but remain in the repo as the pipeline's input until Phase 2 replaces them with the upstream-generated spec.
