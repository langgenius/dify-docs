---
name: dify-docs-api-reference
description: >
  Use when editing, auditing, or creating OpenAPI specs in the Dify docs
  repo (en/api-reference/openapi_*.json), or on any task touching API
  endpoint parameters, responses, error codes, status codes, or examples.
---

# Dify API Reference Documentation

OpenAPI specs for developers integrating Dify over REST. **The code is the source of truth: when the spec disagrees with the code, the spec is wrong.** Every detail you write must be traceable to a controller, model, or converter in the Dify codebase.

## Workflow

Work through these in order. Steps 1, 3, 4, and 5 are non-negotiable.

Editing or creating a spec runs all five steps. Auditing an existing spec is steps 1 and 3 applied systematically from `references/audit-checklist.md`; the independent subagent audit in step 5 is required only when you have written or substantially changed an endpoint.

1. **Set up and scope.** Read the shared guides (`writing-guides/style-guide.md`, `formatting-guide.md`, `glossary.md`). Confirm the Dify codebase is on the ref you mean to verify against: the latest `main` by default (`git fetch origin`, then fast-forward only if the working tree is clean), or a dev branch if the user names one. Do not force a checkout over a dirty or feature working tree. Identify which spec you are in and its app type from [Spec Structure](#spec-structure); every later check is filtered through that app-type lens (see [App-Type Scoping](#app-type-scoping)).
2. **Write or edit to the conventions.** Apply `references/spec-conventions.md` for every element: summaries, operationId, descriptions, parameters, responses, error format, schemas, examples, tags, ordering. That file is the single source for formatting rules; do not reinvent them here.
3. **Verify every detail against the code.** Nothing ships unverified (see [Verifying Against Code](#verifying-against-code)). Use `references/codebase-paths.md` to locate controllers, error definitions, and global handlers.
4. **Flag suspected code bugs; never silently document them** (see [Flagging Suspected Bugs](#flagging-suspected-bugs)).
5. **Run post-writing verification** (see [Post-Writing Verification](#post-writing-verification)): the post-writing checks always, plus the independent subagent audit for new or substantially-changed endpoints.

## Reader Persona

Backend developers integrating Dify apps or knowledge bases via REST. Strong coding ability; familiar with HTTP, authentication patterns, and JSON. Be precise about parameter types, required vs optional, error codes, and realistic examples. Do not explain what a REST API is.

## Spec Structure

You edit five per-app-type **source** specs; `tools/api-pipeline/merge_specs.py` merges them into one rendered `openapi_service.json` per language. Edit the sources — never the rendered spec.

Source specs (`{en,zh,ja}/api-reference/openapi_*.json`), one per app type:

| Spec File | App Type | `AppMode` values | Key Endpoints |
|-----------|----------|------------------|---------------|
| `openapi_chat.json` | Chat & Agent | `CHAT`, `AGENT_CHAT` | `/chat-messages`, conversations |
| `openapi_chatflow.json` | Chatflow | `ADVANCED_CHAT` | Same as chat, mode `advanced-chat` |
| `openapi_workflow.json` | Workflow | `WORKFLOW` | `/workflows/run`, workflow logs |
| `openapi_completion.json` | Completion | `COMPLETION` | `/completion-messages` |
| `openapi_knowledge.json` | Knowledge | *(N/A)* | datasets, documents, segments, metadata |

Shared endpoints (file upload, audio, feedback, app info, parameters, meta, site, end-user) appear in the chat, chatflow, workflow, and completion specs. A fix to one usually applies to all four, so propagate it. zh/ja translations live in their own source specs and merge the same way.

After editing a source spec, run `build --lang en zh ja` then `wire` to regenerate `openapi_service.json`, the docs.json API nav, and redirects, then `check-coverage`. The build stamps one English-slug `x-mint.href` (language-switcher parity) and an `x-mint.metadata.sidebarTitle` (the summary, so translated operations keep their language in the sidebar) per operation.

### App-Type Scoping

The codebase shares controllers and Pydantic models across app modes; the docs split them into per-app-type specs. Filter everything through the app type of the spec you are in:

- **Shared models**: include only fields that have an effect in this mode.
- **Shared error handlers**: include only errors triggerable in this mode.
- **Internal-only fields** (e.g., `retriever_from`): omit from all specs.

To judge relevance, check the controller's `AppMode` guard; when in doubt, trace through `AppGenerateService.generate()`. For example, `workflow_id` belongs in chatflow, not chat.

## Verifying Against Code

Every detail in the spec MUST be verifiable against the codebase.

**What must match exactly:**

- **Schema constraints** (`default`, `minimum`/`maximum`, `enum`): the Pydantic `Field()` arguments, verbatim.
- **Required/optional**: `Field(default=...)` is optional; no default is required; `FetchUserArg(required=True)` is required.
- **Response status codes**: the code's `return ..., <status>`.
- **Response body fields**: what the code actually returns after converters.
- **Error codes and messages**: only errors the endpoint raises, with names and `description` strings traced to the exception.

**How to verify:**

1. **Identify the correct controller.** These specs are the Service API (`servers` base ends in `/v1`; `controllers/service_api/`). The same route name often also exists on the `web` or `console` blueprint with a different path, auth model, and required params (e.g., a required `user`); match the blueprint whose base URL matches `servers`, not the first controller you find.
2. Read the controller method.
3. For each parameter, find the Pydantic model or `request.args.get()` and note the `Field()` arguments.
4. **Trace string fields beyond the controller.** A controller `str` may be cast to `StrEnum`/`Literal` or validated against a fixed list downstream; if so, the spec needs `enum`.
5. For errors, trace `except` to `raise` to the exception class and its `error_code`/`code` in `error.py`, and through the global handlers in `api/libs/external_api.py`.
6. For responses, read the `return` statement AND any response converter (they flatten, restructure, or inject fields).
7. For service calls, read the service method to see what it actually returns or raises.

## Flagging Suspected Bugs

The code is the source of truth, but the code itself can have bugs. When something looks irregular (off-by-one in `le`/`ge`, a body on a 204, error handling that differs from sibling endpoints, a `required` mismatch):

1. **Flag it explicitly.** Never silently document the suspected bug.
2. **Show the evidence.** Quote the exact line and explain why it looks wrong.
3. **Ask the user to decide**: document as-is, or treat as an upstream bug.
4. **Never auto-correct.** Do not write the "correct" value when the code says otherwise.

Beyond fidelity, act as a professional API writer: challenge questionable decisions with reasoning, suggest developer-experience improvements (kept clearly separate from required fixes), and push back on conflicting instructions with evidence.

## Post-Writing Verification

Run the post-writing checks in `writing-guides/index.md#post-writing-verification`, then the two passes below.

### Independent code audit (required for new or substantially-changed endpoints)

Spec errors hide in plausible-looking JSON. Dispatch a subagent to audit the spec against the code, and instruct it not to trust your draft. The brief MUST:

- Pin the verification refs: the exact dify tag/branch. Add the graphon version pinned in `dify/api/pyproject.toml` only when the endpoint's behavior runs through the graph engine (workflow execution and its streaming events); it does not apply to the Knowledge spec or to controller, parameter, or error checks, which live in `dify`.
- Require the agent to load this skill and its `references/` (spec-conventions, audit-checklist, codebase-paths).
- **Identify the correct controller** (Service API at `/v1`, `controllers/service_api/`), not a same-named `web`/`console` route with different auth or params; see [Verifying Against Code](#verifying-against-code).
- Per endpoint: check path/method, every parameter (required/optional/type), response status and body fields, and each error code traced `exception` to `handler`, all against code. Return a per-endpoint verdict with `file:symbol` evidence, plus a separate list of what code alone cannot confirm.
- Trace opaque request fields (ids, tokens, file references) to where they are resolved and validated, not just the controller. Capture ownership and cross-request rules, such as an `upload_file_id` whose owning `user` must match the submit's.
- If the endpoint also appears in the in-product API templates (`web/app/components/develop/template/template_*.mdx`), diff the spec against them; they document the same endpoints and surface divergence and upstream fixes.

Treat the audit as authoritative over your draft; reconcile every discrepancy before claiming done.

### Example and schema consistency

A quick mechanical pass, independent of the audit:

- Every key in a request or response example appears in the corresponding schema, and every documented field appears in at least one example.
- Every documented enum value and `oneOf` branch is exercised by at least one example.
