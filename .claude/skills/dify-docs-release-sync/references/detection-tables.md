# Detection Tables

Lookup tables for Phase 1.2 (Categorize PRs). For each changed source path, find the affected documentation target here.

## API Reference Detection (Deterministic)

The Service API reference is one spec per language: `{en,zh,ja}/api-reference/openapi_service.json`. Map changed source files to the spec's **tag groups** (the `tags` array in the spec). Which app types expose an operation is recorded in `tools/api-pipeline/memberships.json` — check it when assessing availability; there are no per-app-type spec files.

Source paths are under `api/` in the dify repo:

| Source path | Affected tag group(s) |
|---|---|
| `controllers/service_api/app/completion.py` | Chat Messages, Completion Messages |
| `controllers/service_api/app/message.py` | Chat Messages, Conversations, Feedback |
| `controllers/service_api/app/conversation.py` | Conversations |
| `controllers/service_api/app/workflow.py` | Workflow Runs |
| `controllers/service_api/app/workflow_events.py` | Workflow Runs |
| `controllers/service_api/app/audio.py` | Audio |
| `controllers/service_api/app/file.py`, `file_preview.py` | Files |
| `controllers/service_api/app/app.py`, `site.py` | Applications |
| `controllers/service_api/app/annotation.py` | Annotations |
| `controllers/service_api/app/human_input_form.py` | Human Input |
| `controllers/service_api/end_user/` | End Users |
| `controllers/service_api/workspace/` | Models |
| `controllers/service_api/dataset/dataset.py` | Knowledge Bases, Tags, Documents |
| `controllers/service_api/dataset/hit_testing.py` | Knowledge Bases |
| `controllers/service_api/dataset/document.py` | Documents |
| `controllers/service_api/dataset/segment.py` | Chunks |
| `controllers/service_api/dataset/metadata.py` | Metadata |
| `controllers/service_api/dataset/rag_pipeline/` | Knowledge Pipeline |
| `controllers/service_api/app/error.py` | Error responses in all app-side groups |
| `controllers/service_api/dataset/error.py` | Error responses in all dataset-side groups |
| `controllers/service_api/__init__.py`, `wraps.py`, `schema.py` | Entire spec (routing, auth, shared schemas) |
| `libs/external_api.py` | Entire spec (error envelope) |

Also check: Pydantic models and `fields/` serializers used by Service API controllers. If a PR modifies a model or serializer referenced by a Service API endpoint, that endpoint's tag group is affected.

A controller file not in this table means the table is stale, not that the change is out of scope: list `api/controllers/service_api/` at the upper ref, map the new file's routes to spec tag groups, and update this table.

## Help Documentation Detection (Heuristic)

Read the PR description for context. Map changed source paths to likely doc areas. `use-dify` content exists in two product copies (`en/cloud/...` and `en/self-host/...`); apply shared changes to both (audience-specific blocks — plan gating, env-var callouts, Enterprise tips — stay per-copy), then mirror zh/ja.

Which nodes live in dify vs graphon: follow the repo-split rule in the repo root `CLAUDE.md` (Key Rules); verify graphon behavior at the version pinned in `dify/api/pyproject.toml`, never graphon `main`.

| Repo | Source path pattern | Likely doc area |
|---|---|---|
| dify | `api/core/workflow/nodes/` (integration nodes) | `en/{cloud,self-host}/use-dify/nodes/` |
| dify | `api/core/rag/` | `en/{cloud,self-host}/use-dify/knowledge/` |
| dify | `api/core/tools/` | `en/{cloud,self-host}/use-dify/nodes/tools.mdx` or workflow tool node docs |
| dify | `api/core/agent/` | `en/{cloud,self-host}/use-dify/build/agent.mdx` |
| dify | `api/core/app/` | `en/{cloud,self-host}/use-dify/build/` |
| dify | `web/app/components/` | Match the component's feature area to the corresponding `en/{cloud,self-host}/use-dify/` page (e.g. `components/workflow/` → nodes docs, `components/datasets/` → knowledge docs). Pure styling/layout PRs: skip. |
| dify | `docker/.env.example`, `docker/envs/**/*.env.example`, `docker/docker-compose.yaml`, `docker/docker-compose-template.yaml`, `api/configs/` | `en/self-host/deploy/configuration/environments.mdx` (env var docs) |
| dify | `docker/README.md`, root `README.md`, any new, renamed, or removed file under `docker/` | `en/self-host/deploy/quick-start/docker-compose.mdx` and `en/self-host/deploy/quick-start/faqs.mdx` (deployment workflow docs) |
| graphon | `src/graphon/nodes/` (built-in nodes) | `en/{cloud,self-host}/use-dify/nodes/` |
| graphon | `src/graphon/model_runtime/` | `en/{cloud,self-host}/use-dify/workspace/model-providers.mdx` |
| graphon | `src/graphon/graph_engine/`, `src/graphon/runtime/` | workflow engine behavior, execution semantics |

Deployment files have been added upstream and then reverted within a single release window before. Before documenting a new `docker/` file, confirm it still exists at the upper ref (`git show <to>:docker/<file>` succeeds).

When checking dify PRs, also scan recent merges in `langgenius/graphon` for the same release window. A user-visible workflow change may ship as a graphon release plus a dify pin bump (look for changes to `api/pyproject.toml` and `api/uv.lock`).

## Environment Variable Detection (Deterministic)

Any file matching these patterns means env var documentation is affected:

| Source path | Impact |
|---|---|
| `docker/.env.example` | New vars, changed defaults, removed vars |
| `docker/envs/**/*.env.example` | Same — the split per-service env files |
| `api/configs/**/*.py` | Pydantic config models define backend vars |
| `web/docker/entrypoint.sh` | Frontend Docker-to-NEXT_PUBLIC mapping |
| `docker/docker-compose.yaml`, `docker/docker-compose-template.yaml` | Infrastructure/container vars |

When detected, the report should list which variables were added, removed, or had defaults changed, which config file(s) were modified, and priority (High if new/removed vars, Medium if default changes only).

## UI i18n Source Files

i18n source files: `web/i18n/{en-US,zh-Hans,ja-JP}/` (36 JSON files per language). Focus on: `common.json`, `app.json`, `workflow.json`, `dataset.json`, `dataset-creation.json`, `dataset-documents.json`. These contain the most documentation-relevant UI labels.
