# Codebase Paths

Mapping of concepts to file paths in the Dify codebase and docs repo.

## Dify Docs Repo

| What | Path |
|------|------|
| OpenAPI specs | `en/api-reference/openapi_*.json` |
| Navigation config | `docs.json` |

## Dify Codebase

| What | Path |
|------|------|
| App controllers | `api/controllers/service_api/app/` |
| Dataset controllers | `api/controllers/service_api/dataset/` |
| App error definitions | `api/controllers/service_api/app/error.py` |
| Dataset error definitions | `api/controllers/service_api/dataset/error.py` |
| Auth/rate-limit wrapper | `api/controllers/service_api/wraps.py` |
| Global error handlers | `api/libs/external_api.py` |
| Route registration | `api/controllers/service_api/__init__.py` |

### Global Error Handlers

The handlers in `api/libs/external_api.py` are critical for error tracing:

- `ValueError` -> 400 `invalid_param`
- `AppInvokeQuotaExceededError` -> 429 `too_many_requests`
- Generic `Exception` -> 500

Always check these when tracing bare `raise ValueError(...)` or unhandled exceptions.

### Error Code Sources

| Error Type | Source |
|------------|--------|
| App-level errors | `api/controllers/service_api/app/error.py` |
| Knowledge errors | `api/controllers/service_api/dataset/error.py` |
| Auth/rate-limit | `api/controllers/service_api/wraps.py` |
| Global handlers | `api/libs/external_api.py` |
