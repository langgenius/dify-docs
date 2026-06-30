# Report Template

Skeleton for the Phase 2 doc sync report. Fill in the comparison refs, counts, and per-track tables, then present to the user and STOP.

```markdown
# Doc Sync Report: [from] -> [to]

## Summary
- **Comparison**: `<from>..<to>` (X commits, Y PRs)
- **API reference impact**: Y PRs -> Z spec files (A already documented, B need updates)
- **Help documentation impact**: W PRs -> V doc pages (C already documented, D need updates)
- **Environment variable impact**: E PRs -> F variables (G already documented, H need updates)
- **UI i18n changes**: I PRs -> J glossary entries affected
- **No doc impact**: N PRs

## API Reference Changes

### openapi_chat.json / openapi_chatflow.json

| PR | Title | Change Type | Details | Doc Status |
|---|---|---|---|---|
| #1234 | Add streaming retry | New parameter | `retry_count` on `/chat-messages` | Not yet documented |
| #1235 | Fix error handling | Error codes | New `rate_limit_exceeded` on `/chat-messages` | Already documented |

### openapi_knowledge.json
| PR | Title | Change Type | Details | Doc Status |
|---|---|---|---|---|
| #1240 | Add metadata filter | New parameter | `metadata_filter` on list segments | Not yet documented |

## Help Documentation Changes

| PR | Title | Affected Doc(s) | Priority | Change Needed | Doc Status |
|---|---|---|---|---|---|
| #1250 | Add semantic chunking | `knowledge/chunking.mdx` | High | New chunking option must be added | Not yet documented |
| #1251 | New HTTP node timeout | `workflow/nodes/http.mdx` | Low | Timeout config not covered | Already documented |

## Environment Variable Changes

| PR | Title | Variables | Change Type | Priority | Doc Status |
|---|---|---|---|---|---|
| #1270 | Add Redis sentinel | `REDIS_SENTINEL_*` (3 new) | New variables | High | Not yet documented |
| #1271 | Change default log level | `LOG_LEVEL` default INFO->WARNING | Default change | Medium | Already documented |

## UI i18n Changes (Glossary Impact)

| PR | Key | Old Value | New Value | Glossary Status |
|---|---|---|---|---|
| #1280 | `dataset.indexMethod` | Index Method | Indexing Method | Exists — update needed |
| #1281 | `workflow.nodeGroup` | (new) | Node Group | Candidate for addition |

## No Documentation Impact

| PR | Title | Reason |
|---|---|---|
| #1260 | Refactor internal cache | Internal only |
| #1261 | Update CI pipeline | Infrastructure |
```
