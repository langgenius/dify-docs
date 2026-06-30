# Detection Tables

Lookup tables for Phase 1.2 (Categorize PRs). For each changed source path, find the affected documentation target here.

## API Reference Detection (Deterministic)

Any file matching these patterns means the corresponding spec is affected:

| Source path | Affected spec(s) |
|---|---|
| `controllers/service_api/app/chat.py` | chat, chatflow |
| `controllers/service_api/app/completion.py` | completion |
| `controllers/service_api/app/workflow.py` | workflow, chatflow |
| `controllers/service_api/app/audio.py`, `file.py`, `site.py`, `app.py` | all 4 app specs |
| `controllers/service_api/app/message.py` | chat, chatflow, completion |
| `controllers/service_api/app/conversation.py` | chat, chatflow |
| `controllers/service_api/app/annotation.py` | chat, chatflow |
| `controllers/service_api/dataset/` | knowledge |
| `controllers/service_api/app/error.py` | all 4 app specs |
| `controllers/service_api/dataset/error.py` | knowledge |
| `controllers/service_api/wraps.py` | all 5 specs |
| `controllers/service_api/__init__.py` | all 5 specs (route changes) |
| `libs/external_api.py` | all 5 specs |

Also check: Pydantic models and `fields/` serializers used by Service API controllers. If a PR modifies a model or serializer referenced by a Service API endpoint, that spec is affected.

## Help Documentation Detection (Heuristic)

Read the PR description for context. Map changed source paths to likely doc areas. `use-dify` content exists in two product copies (`en/cloud/...` and `en/self-host/...`); apply changes to both, then mirror zh/ja:

| Repo | Source path pattern | Likely doc area |
|---|---|---|
| dify | `api/core/workflow/nodes/` (integration nodes only: agent, knowledge, datasource, trigger) | `en/{cloud,self-host}/use-dify/nodes/` |
| dify | `api/core/rag/` | `en/{cloud,self-host}/use-dify/knowledge/` |
| dify | `api/core/tools/` | `en/{cloud,self-host}/use-dify/nodes/tools.mdx` or workflow tool node docs |
| dify | `api/core/agent/` | `en/{cloud,self-host}/use-dify/build/agent.mdx` |
| dify | `api/core/app/` | `en/{cloud,self-host}/use-dify/build/` |
| dify | `web/app/components/` | UI-related docs (check PR description for specifics) |
| dify | `docker/.env.example`, `docker/docker-compose.yaml`, `docker/docker-compose-template.yaml`, `api/configs/` | `en/self-host/deploy/configuration/environments.mdx` (env var docs) |
| dify | `docker/README.md`, `docker/dify-compose*`, `docker/.env.default`, root `README.md`, any new file under `docker/` | `en/self-host/deploy/quick-start/docker-compose.mdx` and `en/self-host/deploy/quick-start/faqs.mdx` (deployment workflow docs) |
| graphon | `src/graphon/nodes/` (built-in nodes: llm, code, http_request, if_else, loop, iteration, parameter_extractor, document_extractor, list_operator, variable_aggregator/assigner, question_classifier, template_transform, tool, start/end/answer, human_input) | `en/{cloud,self-host}/use-dify/nodes/` |
| graphon | `src/graphon/model_runtime/` | `en/{cloud,self-host}/use-dify/workspace/model-providers.mdx` |
| graphon | `src/graphon/graph_engine/`, `src/graphon/runtime/` | workflow engine behavior, execution semantics |

When checking dify PRs, also scan recent merges in `langgenius/graphon` for the same release window. A user-visible workflow change may ship as a graphon release plus a dify pin bump (look for changes to `api/pyproject.toml` and `api/uv.lock`).

## Environment Variable Detection (Deterministic)

Any file matching these patterns means env var documentation is affected:

| Source path | Impact |
|---|---|
| `docker/.env.example` | New vars, changed defaults, removed vars |
| `api/configs/**/*.py` | Pydantic config models define backend vars |
| `web/docker/entrypoint.sh` | Frontend Docker-to-NEXT_PUBLIC mapping |
| `docker-compose.yaml` | Infrastructure/container vars |

When detected, the report should list which variables were added, removed, or had defaults changed, which config file(s) were modified, and priority (High if new/removed vars, Medium if default changes only).

## UI i18n Source Files

i18n source files: `web/i18n/{en-US,zh-Hans,ja-JP}/` (~30 JSON files each, ~4,875 keys total). Focus on: `common.json`, `app.json`, `workflow.json`, `dataset.json`, `dataset-creation.json`, `dataset-documents.json`. These contain the most documentation-relevant UI labels.
