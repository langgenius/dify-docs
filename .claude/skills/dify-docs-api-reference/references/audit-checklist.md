# Audit Checklist (Per Endpoint)

Use when auditing an existing spec against the Dify codebase. `spec-conventions.md` defines what "correct" looks like for each element; SKILL.md's "Verifying Against Code" defines the verification method. This file is the audit procedure plus the rules for not reporting false positives.

## Pre-Audit

1. **Identify which app types each operation serves** (its availability line and `tools/api-pipeline/memberships.json`). Every check is filtered through that app-type scope.
2. **Compare routes**: read `api/controllers/service_api/__init__.py` for registered routes, then each controller file. Note endpoints present in code but missing from the spec, and ghost endpoints present in the spec but not in code. **Match the exact route string** — hyphen and underscore variants of the same path are separate registrations and can differ in deprecation status.
3. **Pin the refs**: record the dify commit SHA and, for graph-engine behavior, the graphon version pinned in `dify/api/pyproject.toml`. Every finding cites file:line at those refs.

## Per-Endpoint Checks

Verify each against code, using `spec-conventions.md` as the definition of correct:

- **Path and method** match the route.
- **Request schema**: every parameter's type, required/optional, default, and enum against each `Field()` argument. For every `string` field without `enum`, trace the service layer for a hidden `StrEnum`/`Literal`/fixed-list validation before concluding none is needed.
- **Response schema**: fields, types, and status from the `return` statement; read response converters, which flatten or inject fields.
- **Error completeness**: every error the endpoint actually raises is documented. Trace each `except` to its `raise`; read service methods to confirm they raise. Include decorator-sourced errors: read the route's decorator stack (`wraps.py` auth, billing, rate-limit) — decorators fire before the body and genuinely differ between sibling endpoints.
- **Error correctness**: no phantom codes; names match the `error_code` attribute or the werkzeug generic, never the Python class name; messages copied verbatim.
- **Message provenance**: an example `message` must be the string constructed at the actual raise site, not the class-default `description` (raise sites usually override it) and not a log line. Watch for `BaseServiceError` subclasses that skip `super().__init__` — their wire message is the empty string; but check each class's own `__init__`, since sibling error hierarchies differ.
- **Availability ≠ mode guard**: a controller guard accepting an `AppMode` is necessary but not sufficient. Trace where the feature's toggle persists (which config store) and whether the service reads that store for this mode; for event-driven features, confirm the mode's runner actually emits the event. A UI toggle can exist with a dead API path.
- **Examples**: present on every 200/201 and every error response; values match actual code output; no unresolved `{message}` placeholders.
- **Formatting**: operationId, descriptions, schemas, tags, ordering, terminology, backticks, and number-unit spacing, all per `spec-conventions.md`.

## Batch-Audit Workflow

For audits spanning many endpoints, separate the roles and gate each stage:

1. **Auditors** (one per tag group, pinned refs): findings only, no edits; per-finding severity + file:line evidence + a "cannot confirm from code" list.
2. **Adversarial refuters** (one per group): independently re-trace every ERROR/WARN and try to REFUTE it; verdict CONFIRMED/REFUTED/UNCERTAIN with evidence. Only confirmed findings proceed. (In practice this kills real false positives — over-generalized class-hierarchy claims, sibling-endpoint assumptions.)
3. **Fix authors**: turn confirmed findings into patch scripts that assert every precondition (exact current text), are validated on a copy, and are applied serially — never direct parallel edits to one file.

Always validate JSON after fixes. Shared endpoints exist **once** in `openapi_service.json` with mode-aware descriptions — no cross-spec propagation. Propagate fixes across the three **language** specs instead: structural parity is enforced by `tools/api-pipeline/parity_check.py`; wire strings (`message`/`code` values, enum and example literals) stay verbatim English in zh/ja, and only human-language prose translates.

## Verification Rigor

**Every reported issue must be correct.** False positives erode trust and waste time.

1. **Trace the full path.** Don't stop at the controller; follow errors through the global handlers (`external_api.py`) and confirm service methods actually raise.
2. **Check app-type relevance.** Don't flag `workflow_id` as missing from the chat spec.
3. **Every claim needs evidence.** You must have read the actual code line. No speculation.
4. **Self-review before reporting.** For each finding, ask:
   - Did I read the actual code, or am I assuming?
   - Did I check the global handlers for a bare `raise ValueError/Exception`?
   - Is this field or error relevant to THIS spec's app type?
   - Am I confusing the Python class name with the `error_code` attribute?
   - Did I read the service method body, or assume it raises?
5. **When uncertain, investigate further.** Report fewer verified issues over many unverified ones; mark anything unconfirmed as "unverified, needs manual check."

### Common False Positives

- Assuming a bare `ValueError` is a 500 (the global handler converts it to 400 `invalid_param`).
- Flagging a shared-model field as missing from a spec covering a different app type.
- Assuming a service method raises when it is actually fire-and-forget.
- Using the Python exception class name instead of the `error_code` attribute.
- Inventing errors for code paths unreachable under the spec's app mode.
- Documenting an unreachable `except` (the controller catches an exception the service never raises here).
- Adding `enum` to a genuinely dynamic or provider-specific string field (e.g., `voice`, `embedding_model_name`).
- Assuming a sibling endpoint's decorator-sourced error (rate limit, billing) applies — decorator stacks differ per route.
- Treating a console/web blueprint's behavior as the `/v1` behavior; also, in-body checks duplicating what a decorator already enforced are dead code, not documentable errors.
- Over-generalizing message behavior across an error-class hierarchy (one class swallowing its message doesn't mean its siblings do — read each `__init__`).
- Expecting werkzeug's short phrase for generic errors; a bare `InternalServerError()` emits werkzeug's long default paragraph (see codebase-paths.md, "How error responses actually render").
