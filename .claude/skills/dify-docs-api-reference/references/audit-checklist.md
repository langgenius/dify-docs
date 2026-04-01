# Audit Checklist (Per Endpoint)

Use this checklist when auditing or reviewing an OpenAPI spec against the Dify codebase.

## Pre-Audit

1. **Identify the spec's app type**: Determine which `AppMode` values this spec covers (see SKILL.md Spec Structure table). All subsequent checks are filtered through this app-type scope.
2. **Compare routes**: Check `api/controllers/service_api/__init__.py` for registered routes, then each controller file.

## Per-Endpoint Checks

3. **App-type scoping**: For shared controllers/models, only include fields, parameters, and errors relevant to this spec's app type. Trace code paths to confirm relevance.
4. **Missing endpoints**: Present in code but not in spec.
5. **Ghost endpoints**: Present in spec but not in code.
6. **Request schemas**: Verify params, types, required/optional, defaults, enums against every `Field()` argument.
7. **Hidden enums on request string fields**: For every `string` field without `enum`, trace through the service layer to check for `StrEnum` casts, `Literal` types, or validation against fixed lists. Do NOT trust the controller-level type annotation alone.
8. **Response schemas**: Verify fields, types, status codes. Check `return ..., <status>` and read response converters (they may flatten or inject fields).
9. **Error codes -- completeness**: All errors the endpoint raises are documented. Trace every `except` -> `raise` chain; read service methods to confirm they actually raise.
10. **Error codes -- correctness**: No phantom codes. Remove errors the controller does not raise.
11. **Error code names**: Must match `error_code` attribute (custom exceptions) or werkzeug generic name (`bad_request`, `not_found`). Never use Python class names or service exception names.
12. **Error messages**: Must match the `description` attribute or string argument. Copy from code verbatim.
13. **Example values**: Match actual code output (e.g., enum values returned by the code). No unresolved `{message}` placeholders.
14. **operationId convention**: Follows `{verb}{AppType}{Resource}` pattern for new endpoints; legacy IDs left as-is.
15. **Description quality**: Useful explanations, not just field-name labels.
16. **200/201 responses have examples**: Every JSON success response must have at least one `examples` entry with realistic values.
17. **No schema description duplication**: `$ref` response schemas must not have a top-level `description` (Mintlify shows both).
18. **Binary responses**: Use `content` with `format: binary` schema; details in response `description`.
19. **`oneOf` options have `title`**: Each option object needs a descriptive `title`. Parent schema has no `description`.
20. **`required` arrays on request schemas only**: Not on response schemas.
21. **`enum` on request schemas only**: Not on response schemas (Mintlify renders duplicate "Available options").
22. **Response array items have `properties`**: No bare `"type": "object"` -- Mintlify renders `object[]` with no expandable fields.
23. **Terminology consistency**: No synonym mixing within a tag (e.g., "segment" vs "chunk").
24. **Values backticked, number-unit spacing correct**: All literal values backticked; space between numbers and units.
25. **Endpoint ordering**: Follows CRUD lifecycle (POST create -> GET list/detail -> PUT/PATCH update -> DELETE).
26. **Tag naming**: Plural for countable resources, singular for uncountable nouns/abbreviations, Title Case.

## Two-Agent Workflow

- **Agent 1 (Fixer)**: Audits the spec and applies fixes using this checklist and all rules from SKILL.md.
- **Agent 2 (Reviewer)**: Reads the fixed spec and verifies compliance. Reports remaining issues WITHOUT making edits. If issues are found, fix and optionally re-run the reviewer.

Always validate JSON (`python -m json.tool`) after fixes.

## Cross-Spec Propagation

Shared endpoints (file upload, audio, feedback, app info, parameters, meta, site, end-user) appear in chat, chatflow, completion, and workflow specs. When a fix is applied to one spec, check all sibling specs for the same issue.

## Verification Rigor

**Every reported issue must be correct.** False positives erode trust and waste time.

1. **Trace the full path.** Don't stop at the controller. Follow errors through global handlers (`external_api.py`), check whether service methods actually raise.
2. **Check app-type relevance.** Don't flag `workflow_id` as missing from the chat spec.
3. **Verify every claim has evidence.** You must have read the actual code line. No speculative claims.
4. **Self-review before reporting.** Re-read each finding and ask:
   - "Did I read the actual code, or am I assuming?"
   - "Did I check global error handlers for bare `raise ValueError/Exception`?"
   - "Is this field/error relevant to THIS spec's app type?"
   - "Am I confusing the Python class name with the `error_code` attribute?"
   - "Did I check the service method body, or did I assume it raises?"
5. **When uncertain, investigate further.** Report fewer verified issues rather than many unverified ones. Mark uncertain items as "unverified -- needs manual check."

### Common False-Positive Patterns

- Assuming bare `ValueError` is a 500 (global handler converts to 400 `invalid_param`)
- Flagging shared-model fields as missing from a spec covering a different app type
- Assuming a service method raises when it's actually fire-and-forget
- Using the Python exception class name instead of the `error_code` attribute
- Inventing errors for code paths that don't exist under the spec's app mode
- Documenting an unreachable `except` clause (controller catches exception the service never raises for this endpoint)
- Adding `enum` to a genuinely dynamic/provider-specific string field (e.g., `voice`, `embedding_model_name`)
