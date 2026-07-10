# Codebase Paths

Mapping of concepts to file paths in the Dify codebase and docs repo.

## Dify Docs Repo

| What | Path |
|------|------|
| OpenAPI specs (spec of record) | `{en,zh,ja}/api-reference/openapi_service.json` |
| Navigation config | `docs.json` |

## Dify Codebase

| What | Path |
|------|------|
| App controllers | `api/controllers/service_api/app/` |
| Dataset controllers | `api/controllers/service_api/dataset/` |
| App error definitions | `api/controllers/service_api/app/error.py` |
| Dataset error definitions | `api/controllers/service_api/dataset/error.py` |
| Shared file errors | `api/controllers/common/errors.py` |
| Auth/rate-limit wrappers | `api/controllers/service_api/wraps.py` |
| Global error handlers | `api/libs/external_api.py` |
| `BaseHTTPException` | `api/libs/exception.py` |
| Route registration | `api/controllers/service_api/__init__.py` |
| Provider identifiers (`GenericProviderID`) | `api/models/provider_ids.py` |
| File extension lists | `api/constants/__init__.py` |
| Upload limits, feature flags | `api/configs/feature/__init__.py` |
| In-product API templates | `web/app/components/develop/template/template_*.mdx` |

### How error responses actually render

Dify pins a flask-restx fork; its `handle_error` ends with `data = getattr(e, "data", default_data)`, which decides everything:

| Exception | Wire `code` | Wire `message` |
|---|---|---|
| `BaseHTTPException` subclass (`.data` set in `api/libs/exception.py`) | its `error_code` | its `description` (class default, or the constructor argument when passed) |
| Plain werkzeug / custom `HTTPException` without `.data` | `snake_case(type(e).__name__)` via `handle_http_exception` | `e.description` — a bare `InternalServerError()` emits werkzeug's long default paragraph, never "Internal server error." |
| Bare `ValueError` (pydantic `ValidationError` included) | 400 `invalid_param` | `str(e)` |
| `AppInvokeQuotaExceededError` | 429 `too_many_requests` | `str(e)` |
| Unhandled `Exception` | 500 | werkzeug default |

### AppMode ↔ app-type names

| `AppMode` | Docs name |
|---|---|
| `CHAT` | Chatbot |
| `AGENT_CHAT` | Agent |
| `ADVANCED_CHAT` | Chatflow |
| `AGENT` | New Agent |
| `WORKFLOW` | Workflow |
| `COMPLETION` | Text Generator |

`AGENT` vs `AGENT_CHAT` is the recurring trap — double-check it in both directions on every availability claim.

### wraps.py decorator semantics

- `validate_app_token(FetchUserArg(...))`: sets where `user` comes from (JSON/FORM/QUERY) and whether it's required; a missing required `user` → 400 `invalid_param` "Arg user must be provided."
- `validate_dataset_token`: fires before every dataset controller body — 404 "Dataset not found." and 403 "Dataset api access is not enabled."; authenticates as the tenant **owner** (per-dataset permission checks pass). In-body dataset-existence fallbacks after it are dead code.
- Billing/rate-limit decorators are **per-route**: read each route's decorator stack; sibling endpoints genuinely differ.

### Error Code Sources

| Error Type | Source |
|------------|--------|
| App-level errors | `api/controllers/service_api/app/error.py` |
| Knowledge errors | `api/controllers/service_api/dataset/error.py` |
| Auth/rate-limit | `api/controllers/service_api/wraps.py` |
| Global handlers | `api/libs/external_api.py` |
