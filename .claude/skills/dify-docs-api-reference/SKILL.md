---
name: dify-docs-api-reference
description: >
  Rule pack for the Service API specs
  ({en,zh,ja}/api-reference/openapi_service.json): spec conventions,
  app-type scoping, code-verification rules, and the audit machinery.
  Writing and editing run under dify-docs-write; the standalone audit of an
  existing spec ("audit the API spec") runs directly from this pack.
---

# Dify API Reference Documentation

OpenAPI specs for developers integrating Dify over REST. **The code is the source of truth: when the spec disagrees with the code, the spec is wrong.** Every detail you write must be traceable to a controller, model, or converter in the Dify codebase.

Not an entry point for writing — editing or creating specs runs under `dify-docs-write`; the procedures below implement its stages for the Service API specs.

**Standalone audit** (read-only, own trigger — no pipeline needed): auditing an existing spec is the app-type lens (procedure 1 below) plus [Verifying Against Code](#verifying-against-code) applied systematically from `references/audit-checklist.md`.

## Procedures by stage

All four are non-negotiable.

1. **S1 — scope.** Identify which app types the operation serves from the AppMode table in `references/codebase-paths.md`; every later check is filtered through that app-type lens (see [App-Type Scoping](#app-type-scoping)). Read code at the ref pinned in S1 per `writing-guides/index.md` § "Syncing the Dify codebase safely"; never `git checkout` or `git pull` in a tree you have not confirmed is clean.
2. **S5 — write or edit to the conventions.** Apply `references/spec-conventions.md` for every element: summaries, operationId, descriptions, parameters, responses, error format, schemas, examples, tags, ordering. That file is the single source for formatting rules; do not reinvent them here. `S6 modified per pack`: all three language specs are edited directly in the same pass (see [Spec Structure](#spec-structure)); `parity_check` replaces a separate translate step.
3. **S2/S7 — verify every detail against the code.** Nothing ships unverified (see [Verifying Against Code](#verifying-against-code)). Use `references/codebase-paths.md` to locate controllers, error definitions, and global handlers. Flag suspected code bugs; never silently document them (see [Flagging Suspected Bugs](#flagging-suspected-bugs)).
4. **S7 verifiers** (after the spine's check chain): the independent subagent audit — required for new or **substantially changed** endpoints — and the example/schema consistency pass (both under [S7 Verifiers](#s7-verifiers)). **Substantially changed** = any change to paths, methods, parameters, schema fields or constraints, status codes, error codes, example values, or availability; only pure prose rewording (summaries, descriptions, translations) is exempt.

## Reader Persona

Backend developers integrating Dify apps or knowledge bases via REST. Strong coding ability; familiar with HTTP, authentication patterns, and JSON. Be precise about parameter types, required vs optional, error codes, and realistic examples. Do not explain what a REST API is.

## Spec Structure

Dify's generated `service-openapi.json` is the base contract. The three `{en,zh,ja}/api-reference/openapi_service.json` files are composed authoring outputs: edit presentation fields in all three languages, then recapture their reviewed overlays with `compose_service_api.py capture`. Capture ignores wire-contract edits, so paths, parameters, schemas, statuses, security, and deprecation always come from Dify. The composer applies the locale overlays back to the Dify base, and `parity_check` enforces structural parity with en. Never update an overlay fingerprint without rechecking the affected endpoint against runtime.

App types map to `AppMode` values. The one mapping table (docs names, spec groups, key endpoints, and the modes the Service API does not cover) is `references/codebase-paths.md` § "AppMode ↔ app-type names" — use it, never memory.

Shared endpoints (file upload, audio, feedback, app info, parameters, meta, site, end-user) appear **once**, with an availability line and per-mode notes in the description — a fix applies in one place, no propagation. `tools/api-pipeline/memberships.json` records which app types support each operation and drives the app-type overview pages plus `check-coverage`.

Every operation carries `x-mint.href` (`/{lang}/api-reference/{en-tag-kebab}/{en-summary-kebab}` — English slugs in all languages for language-switcher parity) and `x-mint.metadata.title`/`sidebarTitle` (the translated summary; without them the sidebar shows the English slug). Set all of these when adding an operation, and keep the `tags` arrays index-aligned across languages.

After any spec edit, recapture and verify the locale overlays per `tools/api-pipeline/README.md`. After structural edits (adding, removing, retitling, or reordering operations, or changing availability), also update `memberships.json` and the app-type overview pages, then run `wire`, `check-coverage`, `lint_specs`, and `parity_check`. Description-only edits need no `wire`.

### App-Type Scoping

The codebase shares controllers and Pydantic models across app modes; the merged spec documents each shared endpoint once, mode-aware. Filter every claim through the app types the operation actually serves (its availability line and `memberships.json`):

- **Shared models**: include only fields that have an effect in at least one supported mode; mark mode-specific fields in a mode note.
- **Shared error handlers**: include only errors triggerable in a supported mode.
- **Internal-only fields** (e.g., `retriever_from`): omit from the spec.

To judge relevance, check the controller's `AppMode` guard; when in doubt, trace through `AppGenerateService.generate()`. For example, `workflow_id` matters in chatflow mode, not chat.

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

## S7 Verifiers

### Independent code audit (required for new or substantially-changed endpoints)

Spec errors hide in plausible-looking JSON. Dispatch a subagent to audit the spec against the code, and instruct it not to trust your draft. The brief MUST:

- Pin the verification refs: the exact dify tag/branch. Add the graphon version pinned in `dify/api/pyproject.toml` only when the endpoint's behavior runs through the graph engine (workflow execution and its streaming events); it does not apply to the Knowledge spec or to controller, parameter, or error checks, which live in `dify`.
- Require the agent to load this skill and its `references/` (spec-conventions, audit-checklist, codebase-paths).
- **Identify the correct controller** (Service API at `/v1`, `controllers/service_api/`), not a same-named `web`/`console` route with different auth or params; see [Verifying Against Code](#verifying-against-code).
- Per endpoint: check path/method, every parameter (required/optional/type), response status and body fields, and each error code traced `exception` to `handler`, all against code. Return a per-endpoint verdict with `file:symbol` evidence, plus a separate list of what code alone cannot confirm.
- Trace opaque request fields (ids, tokens, file references) to where they are resolved and validated, not just the controller. Capture ownership and cross-request rules, such as an `upload_file_id` whose owning `user` must match the submit's.
- If the endpoint also appears in the in-product API templates (`web/app/components/develop/template/template_*.mdx`), diff the spec against them. Treat divergence as a signal to re-check the code, not as authority: the templates have been found stale (wrong limits, renamed error codes) — the code decides, and template drift is worth flagging upstream.

Treat the audit as authoritative over your draft; reconcile every discrepancy before claiming done.

### Example and schema consistency

A quick mechanical pass, independent of the audit:

- Every key in a request or response example appears in the corresponding schema, and every documented field appears in at least one example.
- Every documented enum value and `oneOf` branch is exercised by at least one example.
