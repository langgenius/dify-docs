---
name: dify-docs-api-reference
description: >
  Use when editing, auditing, or creating OpenAPI specs for the Dify
  documentation repo. Applies to files in en/api-reference/. Covers
  formatting rules, error code conventions, example standards,
  operationId patterns.
---

# Dify API Reference Documentation

## Before Starting

Read these shared guides:

1. `writing-guides/style-guide.md`
2. `writing-guides/formatting-guide.md`
3. `writing-guides/glossary.md`

**When auditing**, also load:
- `references/audit-checklist.md`
- `references/common-mistakes.md`

**When tracing code paths**, also load:
- `references/codebase-paths.md`

## Reader Persona

Backend developers integrating Dify apps or knowledge bases into their own applications via REST APIs. Assume strong coding ability, familiarity with HTTP, authentication patterns, and JSON. Focus on precision: exact parameter types, required vs optional, error codes, and realistic examples. Don't explain what a REST API is.

## Code Fidelity (Non-Negotiable)

**Every detail in the spec MUST be verifiable against the codebase.** When the spec disagrees with the code, the spec is wrong.

### What must match the code exactly

- **Schema constraints**: `default`, `minimum`/`maximum`, `enum` must exactly match Pydantic `Field()` arguments. E.g., `le=101` -> `"maximum": 101` -- not 100.
- **Required/optional**: `Field(default=...)` = optional, no default = required; `FetchUserArg(required=True)` = required.
- **Error codes**: Only errors the endpoint actually raises. Trace `except` -> `raise` -> exception class -> `error_code` and `code` attributes. See [Error Responses](#error-responses).
- **Response status codes**: Must match the code's `return ..., <status>` value.
- **Response body fields**: Must match what the code actually returns. For streaming endpoints, verify the event type `enum` against actual events yielded by the task pipeline. Each event type must have a corresponding discriminator mapping entry.
- **Error messages**: Must match the exception's `description` attribute or the string passed to werkzeug exceptions.

### How to verify

1. Read the controller method.
2. For each parameter: find the Pydantic model or `request.args.get()`, note `Field()` arguments.
3. **Trace string fields beyond the controller.** The controller may declare `str`, but the service layer may cast to `StrEnum`, `Literal`, or validate against a fixed list. Common patterns: `SomeEnum(value)` cast, `Literal["a", "b"]` downstream, explicit `if field not in ALLOWED_VALUES` checks. If any exist, the spec MUST have `enum`.
4. For errors: trace `except` -> `raise` -> exception class -> `error_code` and `code` in `error.py`.
5. For responses: check `return` statement. **Important:** Response converters (e.g., `convert_blocking_full_response`) may flatten, restructure, or inject fields not present in the Pydantic entity. Always read the converter.
6. For service calls: read the service method to see what it returns or raises.

### Flagging suspected code bugs

The code is the source of truth, but the **code itself may have bugs**. When you encounter something irregular:

1. **Flag it explicitly** -- do NOT silently document the suspected bug.
2. **Show the evidence** -- quote the exact code line and explain why it looks wrong.
3. **Ask the user for a decision** -- (a) document as-is, or (b) treat as upstream bug.
4. **Never auto-correct** -- do not silently write the "correct" value when the code says otherwise.

Common code smells: off-by-one in `le`/`ge`, response body with 204, inconsistent error handling across similar endpoints, missing error handlers that sibling endpoints have, `required` mismatches.

### Professional judgment

You are a professional API documentation writer. Beyond code fidelity:
- **Challenge questionable decisions** with reasoning.
- **Suggest improvements** to API consistency or developer experience (clearly separated from required fixes).
- **Question conflicting instructions** -- push back with evidence.

## Spec Structure

| Spec File | App Type | `AppMode` values | Key Endpoints |
|-----------|----------|------------------|---------------|
| `openapi_chat.json` | Chat & Agent | `CHAT`, `AGENT_CHAT` | `/chat-messages`, conversations |
| `openapi_chatflow.json` | Chatflow | `ADVANCED_CHAT` | Same as chat, mode `advanced-chat` |
| `openapi_workflow.json` | Workflow | `WORKFLOW` | `/workflows/run`, workflow logs |
| `openapi_completion.json` | Completion | `COMPLETION` | `/completion-messages` |
| `openapi_knowledge.json` | Knowledge | *(N/A)* | datasets, documents, segments, metadata |

Shared endpoints (file upload, audio, feedback, app info, parameters, meta, site, end-user) appear in chat/chatflow/workflow/completion specs.

### App-Type Scoping (Critical)

The codebase uses shared controllers and Pydantic models across app modes. The **documentation separates** these into per-app-type specs. You MUST filter through the app type lens:

1. **Shared Pydantic models** -- only include fields relevant to this spec's app type.
2. **Shared error handlers** -- only include errors triggerable under this spec's app type.
3. **Internal-only fields** (e.g., `retriever_from`) -- omit from all specs.

**How to determine relevance:** Check the controller's `AppMode` guard. For fields: "does this field have any effect in this mode?" For errors: "can this error be triggered in this mode?" When in doubt, trace through `AppGenerateService.generate()`.

## Style Overrides

These rules are specific to API reference docs and override or extend the general style guide.

### Endpoint Summaries

Must start with an imperative verb. Title Case. Standard vocabulary:

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

**Do NOT use `Retrieve`** -- use `Get` or `List`. Verb-object order: `Upload File` not `File Upload`.

### operationId Convention

Pattern: `{verb}{AppType}{Resource}`

| App Type | Prefix | Examples |
|----------|--------|---------|
| Chat | `Chat` | `createChatMessage`, `listChatConversations` |
| Chatflow | `Chatflow` | `createChatflowMessage` |
| Workflow | `Workflow` | `runWorkflow`, `getWorkflowLogs` |
| Completion | `Completion` | `createCompletionMessage` |
| Knowledge | *(none)* | `createDataset`, `listDocuments` |

**Legacy operationIds**: Do NOT rename existing ones. Changing operationIds is a breaking change for SDK users. Apply this convention to **new endpoints only**.

### Descriptions

- **User-centric**: Write for developers, not the codebase. Name by what developers want to accomplish (e.g., "Download" not "Preview" for an endpoint serving raw file bytes).
- **Terminology consistency**: All user-facing text within a spec must use consistent terms. Code-derived names (paths, fields, schema names) stay as-is. Watch for: "segment" vs "chunk" (use "chunk"), "dataset" vs "knowledge base" (use "knowledge base").
- **Descriptions must add value**: `"Session identifier."` is a label, not a description. Instead: `"The \`user\` identifier provided in API requests."`.
- **Nullable/conditional fields**: Explain when present or `null`.

### Cross-API Links

When a description mentions another endpoint, add a markdown link.
Pattern: `/api-reference/{category}/{endpoint-name}` (kebab-case from endpoint summary).

## Parameters

- Every parameter MUST have a `description`.
- **Schema constraints must exactly match code.** Transcribe `Field()` arguments verbatim.
- Do NOT have `example` field on parameters.
- **Do NOT repeat schema metadata in descriptions.** If `default: 20` is in schema, don't repeat in description.
- **Do NOT repeat enum values in descriptions** unless explaining when to choose each value.
- Mark `required` accurately based on code.
- **Request fields**: Use `enum` for known value sets. Trace string fields through service layer for hidden enums.
- **Response fields**: Do NOT use `enum`. Explain values in `description` instead (Mintlify renders duplicate "Available options" list).
- **Backtick all values** in descriptions: literal values, field names, code references.
- **Space between numbers and units**: `100 s`, `15 MB` -- not `100s`, `15MB`.
- **Descriptions must be specific**: `"Available options."` is not acceptable.

## Responses

### Success Responses

Only 200/201 as the primary response. For multiple response modes (blocking/streaming), use markdown bullets in the 200 description.

**Every 200/201 JSON response MUST have at least one `examples` entry** with realistic values.

**Binary/file responses**: Use `content` with appropriate media type and `format: binary`. Use `audio/mpeg` for audio, `application/octet-stream` for generic files. Put details in response `description`, not endpoint description.

**Schema description duplication**: When using `$ref`, the schema definition MUST NOT have a top-level `description`. Mintlify renders both, causing duplication.

### Error Responses

Each endpoint MUST list its specific error codes, grouped by HTTP status.

#### Error Tracing Rules

1. **`BaseHTTPException` subclasses** (in `error.py`): Use `error_code` attribute as code name, `code` attribute as HTTP status.
2. **Werkzeug built-in exceptions** (`BadRequest`, `NotFound`): Use generic codes -- `bad_request`, `not_found`. NOT the service-layer exception name.
3. **Custom werkzeug `HTTPException` subclasses** (NOT `BaseHTTPException`): Global handler converts class name to snake_case via regex. E.g., `FilenameNotExistsError` -> `filename_not_exists_error`.
4. **Fire-and-forget methods**: If a service method never raises, do NOT invent error responses.
5. **No custom error handling**: If controller only uses `@validate_app_token` with no `try/except`, the only error is 401 (global auth). Do NOT add empty error sections.
6. **Error messages**: Use the exact string from the exception's `description` attribute or werkzeug string argument.

#### Error Format

- **No `$ref` schema** in error responses -- omit `"schema"` entirely.
- **Description** lists error codes as markdown bullets with backticked names.
- **Examples** required for every error response (provides Mintlify dropdown selector).

## Schemas

- **Prefer inline** over `$ref` for simple objects.
- Only use `$ref` for genuinely reused or complex schemas.
- **Array items must define `properties`** -- no bare `"type": "object"`.
- **`required` arrays on request schemas only** -- not response schemas.
- **`oneOf` options**: Each must have a `title` property. Parent schema must NOT have `description`.

## Examples

- **Realistic values only.** Real-looking UUIDs, timestamps, text, metadata.
- **Verify example values against code.** Enum-like fields must use values the code actually returns.
- Request and response examples must correspond.
- **Titles**: `"summary": "Request Example"` (single) or `"summary": "Request Example-Streaming mode"` (multiple). Error examples: use error code as summary.

## Tag Naming

- **Plural** for countable resources: `Chats`, `Files`, `Conversations`.
- **Singular** for uncountable nouns or abbreviations: `Feedback`, `TTS`.
- Title Case.

## Endpoint Ordering

**CRUD lifecycle**: POST create -> GET list/detail -> PUT/PATCH update -> DELETE.

Exception: Tags without a create operation (e.g., Conversations). GET list comes first; non-create POST placed after GETs but before PUT/DELETE.

## Post-Writing Verification

After completing the document:

1. Invoke `dify-docs-terminology-check` to verify terminology consistency against the glossary and codebase.
2. Invoke `dify-docs-reader-test` to verify it from the reader's perspective.
