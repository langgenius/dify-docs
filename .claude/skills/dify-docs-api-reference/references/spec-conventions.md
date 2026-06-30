# Spec Conventions

The single source of truth for how every element of a Dify OpenAPI spec must be written. Load this when writing, editing, or auditing a spec. SKILL.md owns the workflow and code-verification method; this file owns the formatting and structural rules.

Every schema constraint, status code, error code, and example value here is subordinate to the code: transcribe `Field()` arguments verbatim and verify against the controller (see SKILL.md). These conventions govern *how to express* what the code dictates, never *what* it dictates.

## Endpoint Summaries

Imperative verb, Title Case, verb-object order (`Upload File`, not `File Upload`). Standard vocabulary:

| Verb | Method | When to use |
|------|--------|-------------|
| `Get` | GET | Single JSON resource by ID or fixed path |
| `List` | GET | Collection (paginated array) |
| `Download` | GET | Binary file content |
| `Create` | POST | New persistent resource |
| `Send` | POST | Message or request dispatch |
| `Submit` | POST | Feedback or input on existing resource |
| `Upload` | POST | File upload |
| `Convert` | POST | Format transformation |
| `Run` | POST | Execute workflow or process |
| `Stop` | POST | Halt running task |
| `Configure` | POST | Enable/disable setting |
| `Rename` | POST | Rename existing resource |
| `Update` | PUT/PATCH | Modify fields on existing resource |
| `Delete` | DELETE | Remove resource |

Do NOT use `Retrieve`; use `Get` or `List`.

## operationId

Pattern: `{verb}{AppType}{Resource}`.

| App Type | Prefix | Examples |
|----------|--------|---------|
| Chat | `Chat` | `createChatMessage`, `listChatConversations` |
| Chatflow | `Chatflow` | `createChatflowMessage` |
| Workflow | `Workflow` | `runWorkflow`, `getWorkflowLogs` |
| Completion | `Completion` | `createCompletionMessage` |
| Knowledge | *(none)* | `createDataset`, `listDocuments` |

**Legacy operationIds: do NOT rename.** Changing an operationId is a breaking change for SDK users. Apply this convention to new endpoints only.

## Descriptions

- **User-centric.** Name by what a developer wants to accomplish, not by what the code does (e.g., `Download`, not `Preview`, for an endpoint that serves raw file bytes).
- **Must add value.** `"Session identifier."` is a label, not a description. Write `"The \`user\` identifier provided in API requests."`
- **Terminology consistency.** All user-facing text within a spec uses one term per concept: "chunk" not "segment", "knowledge base" not "dataset". Code-derived names (paths, field names, schema names) stay as-is.
- **Nullable/conditional fields.** Explain when the field is present or `null`.
- **Backtick all values**: literal values, field names, code references.
- **Space between numbers and units**: `100 s`, `15 MB`, not `100s`, `15MB`.

### Endpoint vs parameter descriptions

| Field | Scope |
|---|---|
| Endpoint `description` | What the endpoint does, plus any whole-API surprise (cascading delete, long-poll duration). One sentence when possible. |
| Parameter `description` | Field meaning, valid values, deprecation, normalization, and when to use it vs an alternative. |

If the endpoint description explains a parameter, move it down.

❌ "Remove one or more tag bindings from a knowledge base. Provide tag IDs in `tag_ids`. The legacy `tag_id` field is still accepted for single-tag requests and is normalized into `tag_ids` server-side; supply at least one of the two."

✅ Endpoint: "Remove one or more tags from a knowledge base."
   `tag_ids`: "Tag IDs to unbind. Required unless the legacy `tag_id` is provided."
   `tag_id`: "Legacy single-tag form. Normalized into `tag_ids` server-side. Use `tag_ids` for new integrations."

### Cross-API links

When a description mentions another endpoint, link it: `/api-reference/{category}/{endpoint-name}` (kebab-case from the endpoint summary).

## Parameters

- Every parameter MUST have a `description`, and it must be specific (`"Available options."` is not acceptable).
- **Schema constraints match code exactly.** Transcribe `Field()` arguments verbatim; never round or "correct" (`Field(le=101)` → `"maximum": 101`, not 100).
- Mark `required` accurately from the code.
- **No `example` field on parameters**; use the request body `examples` instead.
- **Do NOT repeat schema metadata in descriptions.** If `default: 20` is in the schema, don't restate it in the description.
- **Do NOT repeat enum values in descriptions** unless explaining when to choose each one.
- **Request string fields**: use `enum` for known value sets. Trace string fields through the service layer for hidden enums (`StrEnum` cast, `Literal`, validation against a fixed list); if any exist, the spec MUST have `enum`. Exception: leave genuinely dynamic/provider-specific fields (e.g., `voice`, `embedding_model_name`) without `enum`.
- **Response fields**: do NOT use `enum`; Mintlify renders a duplicate "Available options" list. Explain the values in the `description` instead.

## Success Responses

- Only 200/201 as the primary response. For multiple modes (blocking/streaming), use markdown bullets in the 200 `description`.
- **Every 200/201 JSON response MUST have at least one `examples` entry** with realistic values.
- **Response body matches actual API output, not the Pydantic entity.** Response converters (e.g., `convert_blocking_full_response`) may flatten, restructure, or inject fields; read the converter.
- **Streaming endpoints**: verify the event-type `enum` against the events the task pipeline actually yields; every event type needs a corresponding discriminator mapping entry.
- **Binary/file responses**: use `content` with the right media type and `{ "type": "string", "format": "binary" }` (`audio/mpeg` for audio, `application/octet-stream` for generic files). Put details in the response `description`, not the endpoint description.
- **Schema description duplication**: when a response uses `$ref`, the referenced schema MUST NOT have a top-level `description`; Mintlify renders both.

## Error Responses

Each endpoint lists its specific error codes, grouped by HTTP status. Document only errors the endpoint actually raises (trace `except` → `raise` → exception class); never invent or carry over phantom codes.

### Deriving the error code name

| Exception kind | Code name | HTTP status |
|---|---|---|
| `BaseHTTPException` subclass (in `error.py`) | the `error_code` attribute | the `code` attribute |
| Werkzeug built-in (`BadRequest`, `NotFound`) | generic: `bad_request`, `not_found` | the exception's status |
| Custom werkzeug `HTTPException` subclass (NOT `BaseHTTPException`) | class name → snake_case (e.g., `FilenameNotExistsError` → `filename_not_exists_error`) | the exception's status |
| Bare `raise ValueError(...)` / unhandled | resolved by global handlers in `api/libs/external_api.py` (`ValueError` → 400 `invalid_param`, quota → 429 `too_many_requests`, `Exception` → 500) | per handler |

Never use the Python class name as the code when an `error_code` attribute exists. Error **messages** must be the exact string from the exception's `description` attribute or the werkzeug string argument.

### When NOT to add an error

- **Fire-and-forget methods**: if the service method returns `None` and never raises, document no error for it.
- **Unreachable `except`**: confirm the service method actually raises the caught exception for this endpoint before documenting it.
- **No custom handling**: if the controller only uses `@validate_app_token` with no `try/except`, the only error is 401 (global auth). Do NOT add an empty error section.

**Cloud-only errors still count.** The billing decorators in `wraps.py` raise `Forbidden` (403) and quota/rate-limit errors only on Dify Cloud (`BILLING_ENABLED`), but the specs document them anyway (as `forbidden`, `provider_quota_exceeded`, `rate_limit_error`). Keep them on the write endpoints they guard; do not drop them as self-host-irrelevant.

### Error format

- **No `$ref` schema** in error responses; omit `"schema"` entirely.
- `description` lists the error codes as markdown bullets with backticked names.
- **Examples required** for every error response (provides the Mintlify dropdown selector). No unresolved format placeholders like `{message}`; use realistic static text.

## Schemas

- **Prefer inline** over `$ref` for simple objects; use `$ref` only for genuinely reused or complex schemas.
- **Array items must define `properties`**; no bare `"type": "object"`, which Mintlify renders as `object[]` with no expandable fields.
- **`required` arrays on request schemas only**, never on response schemas.
- **`oneOf` options**: each option object needs a descriptive `title`; the parent schema (the `oneOf` wrapper) must NOT have a `description`.

## Examples

- **Realistic values only**: real-looking UUIDs, timestamps, text, metadata.
- **Verify values against code.** Enum-like fields must use values the code actually returns or accepts.
- Request and response examples must correspond.
- **Titles**: `"summary": "Request Example"` (single) or `"summary": "Request Example-Streaming mode"` (multiple). For error examples, use the error code as the summary.

## Tag Naming

Plural for countable resources (`Chats`, `Files`, `Conversations`); singular for uncountable nouns or abbreviations (`Feedback`, `TTS`); Title Case.

## Endpoint Ordering

CRUD lifecycle: POST create → GET list/detail → PUT/PATCH update → DELETE.

Exception: tags without a create operation (e.g., Conversations): GET list first; a non-create POST goes after the GETs but before PUT/DELETE.
