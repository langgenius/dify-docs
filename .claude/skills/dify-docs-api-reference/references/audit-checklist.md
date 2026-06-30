# Audit Checklist (Per Endpoint)

Use when auditing an existing spec against the Dify codebase. `spec-conventions.md` defines what "correct" looks like for each element; SKILL.md's "Verifying Against Code" defines the verification method. This file is the audit procedure plus the rules for not reporting false positives.

## Pre-Audit

1. **Identify the spec's app type** (SKILL.md Spec Structure). Every check is filtered through this app-type scope.
2. **Compare routes**: read `api/controllers/service_api/__init__.py` for registered routes, then each controller file. Note endpoints present in code but missing from the spec, and ghost endpoints present in the spec but not in code.

## Per-Endpoint Checks

Verify each against code, using `spec-conventions.md` as the definition of correct:

- **Path and method** match the route.
- **Request schema**: every parameter's type, required/optional, default, and enum against each `Field()` argument. For every `string` field without `enum`, trace the service layer for a hidden `StrEnum`/`Literal`/fixed-list validation before concluding none is needed.
- **Response schema**: fields, types, and status from the `return` statement; read response converters, which flatten or inject fields.
- **Error completeness**: every error the endpoint actually raises is documented. Trace each `except` to its `raise`; read service methods to confirm they raise.
- **Error correctness**: no phantom codes; names match the `error_code` attribute or the werkzeug generic, never the Python class name; messages copied verbatim.
- **Examples**: present on every 200/201 and every error response; values match actual code output; no unresolved `{message}` placeholders.
- **Formatting**: operationId, descriptions, schemas, tags, ordering, terminology, backticks, and number-unit spacing, all per `spec-conventions.md`.

## Two-Agent Workflow

- **Agent 1 (Fixer)**: audits and applies fixes using this checklist, `spec-conventions.md`, and SKILL.md.
- **Agent 2 (Reviewer)**: reads the fixed spec, verifies compliance, and reports remaining issues WITHOUT editing. Fix and optionally re-run the reviewer.

Always validate JSON (`python -m json.tool`) after fixes. Shared endpoints exist in the chat, chatflow, completion, and workflow specs; propagate every fix to all siblings.

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
