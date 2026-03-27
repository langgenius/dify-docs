# Common Mistakes

Quick-reference table of frequent spec issues. Each row is a distinct mistake pattern -- fix column shows what to do.

| # | Mistake | Fix |
|---|---------|-----|
| 1 | Schema constraint doesn't match code (`Field(le=101)` -> spec says 100) | Transcribe `Field()` arguments exactly. Do not round or "correct." |
| 2 | `example` field on parameters | Remove. Use request body `examples` instead. |
| 3 | Missing error codes on endpoint | Trace controller `except` -> `raise` chain. Add all raised errors. |
| 4 | Phantom error codes not raised by controller | Remove. Only document errors with a traceable raise path. |
| 5 | Error code uses exception class name instead of `error_code` | Use the `error_code` attribute from `error.py`, not the Python class name. |
| 6 | Werkzeug exception -> wrong error code | `BadRequest` -> `bad_request`, `NotFound` -> `not_found`. Never use service-layer exception name. |
| 7 | `$ref` to ErrorResponse in error responses | Remove schema. Use description + examples only (avoids Mintlify rendering issue). |
| 8 | Error response missing `description` or `examples` | Every error response needs backticked code in `description` AND example objects. |
| 9 | Invented error for fire-and-forget method | Read the service method body. If it returns `None` and never raises, no error response. |
| 10 | Error from unreachable `except` clause documented | Verify the service method actually raises the caught exception for this endpoint. |
| 11 | Field/error from wrong app type included | Filter by spec's `AppMode`. E.g., `workflow_id` belongs in chatflow, not chat. |
| 12 | Internal-only field exposed in spec | Fields like `retriever_from` are internal. Omit from all specs. |
| 13 | Request string field missing `enum` -- controller says `str` but service casts to Enum | Trace through service layer. If cast to `StrEnum`, `Literal`, or validated against list, add `enum`. |
| 14 | `enum` on response schema field | Remove. Mintlify renders duplicate "Available options." Explain values in `description` instead. |
| 15 | Values listed in request description but no `enum` | Add `enum` to request schema when specific values are known. |
| 16 | Request schema missing `required` array | Add based on Pydantic model non-optional fields. |
| 17 | `required` array on response schema | Remove. Only request schemas should have `required` arrays. |
| 18 | Response array items with bare `"type": "object"` | Define `properties` on array items. Mintlify shows `object[]` with no expandable fields otherwise. |
| 19 | Deeply nested `$ref` for simple objects | Inline the properties directly. |
| 20 | `oneOf` options show "Option 1", "Option 2" | Add `"title"` to each `oneOf` option object. |
| 21 | Parent description on `oneOf` wrapper | Remove. Describe only the parent array/property that references the wrapper. |
| 22 | 200 response missing examples | Every JSON 200/201 response must have at least one `examples` entry. |
| 23 | Schema has `description` AND response has `description` | Remove `description` from referenced schema. Mintlify shows both. |
| 24 | Binary response missing `format: binary` | Use `content` with media type + `{ "type": "string", "format": "binary" }`. Details in response `description`. |
| 25 | Response schema matches Pydantic entity, not actual API output | Response converters can flatten or inject fields. Read the converter method. |
| 26 | Streaming event enum missing event types | Cross-reference against task pipeline event yields. Every event type needs a discriminator mapping entry. |
| 27 | Unresolved `{message}` placeholder in example | Replace format placeholders with realistic static text. |
| 28 | Fix applied to one spec but not siblings | Shared endpoints exist in chat/chatflow/completion/workflow specs. Propagate fixes. |
| 29 | Mixed synonyms for same concept | Pick one user-facing term per concept (e.g., "chunk" not "segment"). Code-derived names stay as-is. |
| 30 | Mentioning another API without a link | Add markdown link: `[API Name](/api-reference/category/endpoint)`. |
