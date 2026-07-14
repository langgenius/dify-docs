# Env Var Docs — Style Overrides and Anti-Patterns

Rules specific to env var documentation. They override or extend the shared style guide.

## Formatting rules

- Use `(empty)` for empty-string defaults, not `""` or blank.
- For empty defaults with a fallback: `(empty; falls back to X)` or `(empty; defaults to X)`.
- Never include real or example secret keys — GitHub push protection blocks `sk-*` patterns. Use descriptions like `(pre-filled in .env.example; must be replaced for production)`.
- Add an `Example:` line only when the default is empty (it shows what to set); omit it for concrete defaults, which already show the format (e.g., `TRIGGER_URL`, `SERVER_CONSOLE_API_URL`).

## Style-guide overrides

**Consistency over variety in reference tables.** The general style guide says to vary sentence patterns. In reference tables, consistency aids scanning. Use predictable patterns for connection credentials (hostname, port, username, password) across providers. Vary descriptions only when variables genuinely differ in behavior or purpose.

**Variable descriptions should be self-contained.** The general style guide says not to restate the heading. Variable descriptions must state what the variable does — even if the name partially implies it. Not all variable names are self-explanatory, and users may arrive at a description via search without seeing the surrounding section context.

**Include actionable technical mechanisms.** The general style guide favors user outcomes over technical mechanisms. For env var docs, include technical mechanisms that help users configure, troubleshoot, or understand trade-offs: algorithm names, encoding behavior, fallback chains, version requirements. Exclude mechanisms that only describe code architecture (factory patterns, lazy imports, class names) unless understanding them is necessary for configuration.

- **Keep**: "URL-encoded in the connection string, so `@`, `:`, `%` are safe to use", "HMAC-SHA256", "Requires Milvus >= 2.5.0", "Falls back to `CONSOLE_API_URL`"
- **Remove**: "Dify's storage dispatcher lazily imports the selected backend", "Sends POST to /v1/sandbox/run with X-Api-Key header"

**No specific recommended values for tuning parameters.** For numeric tuning parameters without clear boundaries (connection pool sizes, worker counts, timeouts, buffer sizes), do not prescribe values. Describe the symptom that indicates the value needs changing: "If you experience connection rejections under load, try increasing this value." Exception: when a value has a well-established recommendation (e.g., PostgreSQL `shared_buffers` = 25% of RAM), include it with a reference link.

## Description anti-patterns

| Anti-pattern | Better |
|---|---|
| "Used for frontend references" | "Required for the Human Input node — form links in email notifications are built from this URL" |
| "The backend URL of the console API" | "Set this if you use OAuth login (GitHub, Google) or Notion integration — these features need an absolute callback URL" |
| "Upload file size limit, default 15" | "Maximum file size in MB for uploads" |
| Restating the code comment verbatim | Explaining when you'd change it and what happens if you don't |
