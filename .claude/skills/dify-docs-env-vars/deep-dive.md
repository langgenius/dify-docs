# Dify Environment Variables — Deep Dive Reference

This document records detailed code-traced explanations of each Dify environment variable. It serves as a long-term study reference and will be updated as new variables are analyzed.

---

## Common Variables

### CONSOLE_API_URL

**Default:** `""` (empty)

**What it actually does:** This is the address of Dify's backend API server. The code uses it in two main ways:

1. **OAuth login redirects** — When a user clicks "Log in with GitHub" or "Log in with Google," Dify tells GitHub/Google: "after the user approves, send them back to `{CONSOLE_API_URL}/console/api/oauth/authorize/github`." The same pattern is used for Notion integration, plugin OAuth, and MCP connections. There are ~22 places in the code that build callback URLs this way.

2. **Icon and file URLs** — The frontend loads plugin icons and file previews from URLs built on this base, like `{CONSOLE_API_URL}/console/api/workspaces/current/plugin/icon`.

3. **Cookie security** — The code checks whether this URL starts with `https` to decide whether to use secure cookies.

**If left empty:** For a simple local deployment behind Nginx on the same domain, it works — the frontend makes relative API calls. But any OAuth login (GitHub, Google, Notion) will break because OAuth providers require absolute callback URLs. Plugin icons may also fail to load.

**If set:** All OAuth flows and icon URLs work correctly.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (EndpointConfig)
- OAuth callbacks: `api/controllers/console/auth/oauth.py`
- Plugin OAuth: `api/controllers/console/workspace/tool_providers.py`, `trigger_providers.py`
- Icon URLs: `api/core/tools/tool_manager.py`, `api/services/tools/tools_transform_service.py`
- Cookie security: `api/libs/token.py`

---

### CONSOLE_WEB_URL

**Default:** `""` (empty)

**What it actually does:** This is the address of Dify's frontend web interface. The code uses it for:

1. **Email links** — Every email Dify sends contains links built from this URL: invitation activation links (`{CONSOLE_WEB_URL}/activate?token=...`), password reset links (`/reset-password`), login links (`/signin`), and dataset notification links (`/datasets`).

2. **OAuth completion redirects** — After an OAuth flow finishes on the backend, the server redirects the user's browser back to the frontend using `redirect(f"{CONSOLE_WEB_URL}/oauth-callback")` or `redirect(f"{CONSOLE_WEB_URL}/signin?message=...")`.

3. **CORS fallback** — If `CONSOLE_CORS_ALLOW_ORIGINS` is not set, the system uses this value as the allowed origin for cross-domain requests.

**If left empty:** Email links break (they'd look like `/signin` with no domain). OAuth login can't redirect back to the frontend. For local single-domain deployments behind Nginx, CORS may still work via the fallback, but emails are still broken.

**If set:** Emails contain clickable links, OAuth redirects work, and CORS is properly configured.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (EndpointConfig)
- Email links: `api/tasks/mail_invite_member_task.py`, `mail_register_task.py`, `mail_reset_password_task.py`
- OAuth redirects: `api/controllers/console/auth/oauth.py`, `data_source_oauth.py`
- Plugin/trigger OAuth: `api/controllers/console/workspace/tool_providers.py`, `trigger_providers.py`, `datasource_auth.py`
- CORS fallback: `api/configs/feature/__init__.py` (HttpConfig, via validation_alias)
- Scheduled tasks: `api/schedule/mail_clean_document_notify_task.py`

---

### SERVICE_API_URL

**Default:** `""` (empty)

**What it actually does:** This is the simplest one. It's used in exactly **2 places** in the backend, and both do the same thing:

```python
(dify_config.SERVICE_API_URL or request.host_url.rstrip("/")) + "/v1"
```

It provides the "API Base URL" shown to developers in the Dify console — the URL they copy-paste into their code when calling the Dify API (e.g., `https://api.example.com/v1`).

**If left empty:** Falls back to the current request's host URL. This works fine for single-domain setups — the frontend just uses whatever URL it's already talking to.

**If set:** Ensures all users see the same API base URL regardless of how they access the console (e.g., via IP vs domain name, or behind a load balancer).

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (EndpointConfig)
- App model: `api/models/model.py` (`api_base_url` property)
- Dataset endpoint: `api/controllers/console/datasets/datasets.py` (`DatasetApiBaseUrlApi`)

---

### APP_API_URL

**Default:** `""` (empty; Docker image defaults to `http://127.0.0.1:5001`)

**What it actually does:** This variable is **not used in the Python backend at all**. It's only used in the web frontend's Docker entrypoint script:

```bash
export NEXT_PUBLIC_PUBLIC_API_PREFIX=${APP_API_URL}/api
```

It tells the WebApp frontend (the published app interface, not the console) where the API server is.

**If left empty:** The frontend Docker image has a hardcoded fallback of `http://127.0.0.1:5001`.

**If set:** The WebApp frontend sends API requests to the specified address.

**Key code locations:**
- Docker entrypoint: `web/docker/entrypoint.sh`
- Dockerfile default: `web/Dockerfile`

---

### APP_WEB_URL

**Default:** `""` (empty)

**What it actually does:** This is the address of the WebApp frontend (where published apps live). It's used in **4 places**, all related to the **Human Input node** in workflows:

1. Building form URLs for workflow pause forms: `{APP_WEB_URL}/form/{token}`
2. Including those form URLs in notification emails sent to users
3. Displaying form links in the workflow run details
4. Testing delivery methods for human input

The `Site` model also uses it as the base URL for published apps, with a fallback to the current request URL.

**If left empty:** The `Site` model falls back to the current request URL for basic display. But form links in emails return `None` or are malformed — the Human Input email notification feature is broken.

**If set:** Human Input workflow forms work correctly, and email notifications contain valid links.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (EndpointConfig)
- Site base URL: `api/models/model.py` (`app_base_url` property on Site)
- Workflow form URLs: `api/controllers/console/app/workflow_run.py`
- Email delivery: `api/tasks/mail_human_input_delivery_task.py`
- Delivery test: `api/services/human_input_delivery_test_service.py`

---

### TRIGGER_URL

**Default:** `http://localhost:5001`

**What it actually does:** This is the externally reachable address where webhook and plugin triggers can reach Dify. The code uses it to build two types of endpoint URLs:

- Plugin triggers: `{TRIGGER_URL}/triggers/plugin/{endpoint_id}`
- Webhook triggers: `{TRIGGER_URL}/triggers/webhook/{webhook_id}`

These URLs are given to external systems so they know where to send events to invoke Dify workflows.

**If left empty or set to `localhost`:** Triggers only work locally. External systems can't reach your Dify instance.

**If set to a public URL:** External services can invoke your workflows via webhooks and plugin triggers.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (EndpointConfig)
- URL generation: `api/core/trigger/utils/endpoint.py`
- Trigger subscriptions: `api/services/trigger/trigger_subscription_builder_service.py`
- Trigger provider: `api/services/trigger/trigger_provider_service.py`

---

### FILES_URL

**Default:** `""` (empty; falls back to `CONSOLE_API_URL` via Pydantic alias)

**What it actually does:** This is the base URL for all file preview and download links. The code builds signed URLs like:

- `{FILES_URL}/files/tools/{file_id}?timestamp=X&nonce=Y&sign=Z`
- `{FILES_URL}/files/datasources/{file_id}?...`
- `{FILES_URL}/files/workspaces/{tenant_id}/webapp-logo`

These signed URLs are given to the frontend for displaying images/files, to multi-modal models as input, and to observability/tracing integrations (LangFuse, LangSmith, etc.).

**Fallback mechanism:** If `FILES_URL` is not set, Pydantic's `validation_alias=AliasChoices("FILES_URL", "CONSOLE_API_URL")` causes it to use `CONSOLE_API_URL` instead.

**If both are empty:** File previews, tool outputs, and workspace logos all fail to display.

**If set:** All file URLs resolve correctly. Required for file processing plugins.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (FileAccessConfig)
- Datasource files: `api/core/datasource/datasource_file_manager.py`
- Tool files: `api/core/tools/signature.py` (when `for_external=True`)
- Workspace logos: `api/services/workspace_service.py`, `api/controllers/web/site.py`
- Observability: `api/core/ops/langfuse_trace/`, `langsmith_trace/`, `opik_trace/`, etc.

---

### INTERNAL_FILES_URL

**Default:** `""` (empty; falls back to `FILES_URL`)

**What it actually does:** Same purpose as `FILES_URL`, but for communication **between services inside the Docker network**. Every usage in the code follows this pattern:

```python
base_url = dify_config.INTERNAL_FILES_URL or dify_config.FILES_URL
```

It's used when plugins, PDF extractors, or Word document processors need to access files. These internal services may not be able to reach the external `FILES_URL` (which might go through Nginx, a CDN, or a public domain that isn't routable from inside Docker).

**If left empty:** Falls back to `FILES_URL`. Works fine if internal services can reach the external URL.

**If set (e.g., `http://api:5001`):** Services communicate directly within Docker, avoiding external routing.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (FileAccessConfig)
- Tool files: `api/core/tools/tool_file_manager.py`, `api/core/tools/signature.py` (when `for_external=False`)
- Document extraction: `api/core/rag/extractor/pdf_extractor.py`, `word_extractor.py`
- Workflow runtime: `api/core/app/workflow/file_runtime.py`

---

### FILES_ACCESS_TIMEOUT

**Default:** `300` (seconds, i.e., 5 minutes)

**What it actually does:** Controls how long signed file URLs remain valid. Every file URL Dify generates includes a timestamp and HMAC signature. When the URL is accessed, the verification logic checks:

```python
current_time - timestamp <= FILES_ACCESS_TIMEOUT
```

If the URL is older than `FILES_ACCESS_TIMEOUT` seconds, it's rejected.

**If set to a larger value (e.g., 3600):** URLs stay valid longer, useful for long-running processes. Less protection against URL reuse/replay.

**If set to a smaller value (e.g., 60):** URLs expire faster, more secure but may break slow operations.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (FileAccessConfig)
- Verification: `api/core/datasource/datasource_file_manager.py`, `api/core/tools/tool_file_manager.py`, `api/core/tools/signature.py`
- Workflow runtime: `api/core/app/workflow/file_runtime.py`

---

## Server Configuration

### SECRET_KEY

**Default:** `change-this-to-a-random-secret` (pre-filled in .env.example; must be replaced for production)

**What it actually does:** This is the most critical security variable. It's used for four distinct purposes:

1. **Session cookie signing**—Flask uses it to sign browser session cookies, preventing forgery.
2. **JWT token signing**—All authentication tokens (login sessions) are signed with HS256 using this key. Both creation and verification depend on it.
3. **File URL signing**—Every file preview/download URL includes an HMAC-SHA256 signature derived from this key, making URLs tamper-proof and time-limited.
4. **OAuth credential encryption**—Third-party OAuth credentials (client_id, client_secret for plugin integrations) are encrypted with AES-256-CBC using a key derived from SECRET_KEY.

**If changed after deployment:**
- All users are immediately logged out (session cookies and JWT tokens become invalid)
- All existing file preview URLs break
- All encrypted OAuth credentials become undecryptable—plugin integrations stop working
- This is essentially a "reset everything" action

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (SecurityConfig)
- Flask session: `api/extensions/ext_set_secretkey.py`
- JWT: `api/libs/passport.py`
- File signing: `api/core/tools/signature.py`, `api/core/datasource/datasource_file_manager.py`
- OAuth encryption: `api/core/tools/utils/system_oauth_encryption.py`

---

### INIT_PASSWORD

**Default:** (empty)

**What it actually does:** An optional security gate for the initial admin account setup. It is NOT defined in the Pydantic config—it's read directly from the environment via `os.environ.get("INIT_PASSWORD")`.

When set, Dify requires this password to be entered at the `/install` page before the admin account can be created. The `@setup_required` decorator on API endpoints blocks all access until this validation passes.

When empty, the setup page is open without any password—anyone who can reach the `/install` URL can create the admin account.

**Only relevant during first-time setup.** Once the `DifySetup` database record exists (i.e., setup is complete), this variable has no further effect. Maximum length: 30 characters.

**Key code locations:**
- Validation: `api/controllers/console/init_validate.py`
- Setup gate: `api/controllers/console/wraps.py` (`@setup_required` decorator)

---

### DEBUG

**Default:** `false`

**What it actually does:** Enables verbose logging across many subsystems. When `true`:

1. **App startup timing**—logs how long each extension takes to initialize.
2. **Workflow debugging**—adds a `DebugLoggingLayer` to the GraphEngine that logs all node inputs and outputs.
3. **Tool execution details**—prints colored console output showing tool invocations, inputs, outputs (truncated to 1000 chars), and errors.
4. **LLM invocation logging**—logs the full prompt messages sent to models, streaming chunks as they arrive, and final responses with usage stats.
5. **Exception details**—various app generators log full stack traces on errors instead of silently failing.

This is primarily a developer/debugging tool. Not recommended for production due to the volume of output and potential exposure of sensitive data in logs.

**Key code locations:**
- Definition: `api/configs/deploy/__init__.py`
- Workflow debug: `api/core/workflow/workflow_entry.py`
- Tool callbacks: `api/core/callback_handler/agent_tool_callback_handler.py`
- LLM logging: `api/dify_graph/model_runtime/model_providers/__base/large_language_model.py`

---

### FLASK_DEBUG

**Default:** `false`

**What it actually does:** Defined in `.env.example` but **not actively used** in the Dify codebase. Flask's standard `FLASK_DEBUG` would enable Flask's auto-reloader and interactive debugger, but Dify doesn't leverage this mechanism—`DEBUG` is the primary control instead.

---

### ENABLE_REQUEST_LOGGING

**Default:** `false`

**What it actually does:** Registers Flask signal handlers that log HTTP request and response details. When enabled:

- **Always logs** a compact access line for every request: `{METHOD} {PATH} {STATUS_CODE} {DURATION_MS} {TRACE_ID}`
- **If LOG_LEVEL is also DEBUG**, additionally logs full request and response bodies as pretty-printed JSON.

Useful for debugging API issues, but can produce very large log volumes in production. The body logging only activates when both this variable AND DEBUG-level logging are enabled—enabling just this variable gives you the compact access log without the bodies.

**Key code locations:**
- Definition: `api/configs/deploy/__init__.py`
- Implementation: `api/extensions/ext_request_logging.py`

---

### DEPLOY_ENV

**Default:** `PRODUCTION`

**What it actually does:** Purely an **observability label**—it tags monitoring data but does NOT change any application behavior. Despite the `.env.example` comment about a "distinct color label on the front-end page," the backend code has no conditional logic based on this value.

It's sent to:
- **Sentry** as the `environment` tag for error grouping
- **OpenTelemetry** as the deployment environment resource attribute
- **HTTP response headers** as `X-Env` on every response

Setting it to `TESTING`, `STAGING`, or any custom value simply changes these labels. The frontend color label behavior, if it exists, is handled by the web frontend independently.

**Key code locations:**
- Definition: `api/configs/deploy/__init__.py`
- Sentry: `api/extensions/ext_sentry.py`
- OTEL: `api/extensions/ext_otel.py`
- Response header: `api/extensions/ext_app_metrics.py`

---

### MIGRATION_ENABLED

**Default:** `true`

**What it actually does:** Controls whether database schema migrations run automatically when the Docker container starts. This is handled in the Docker entrypoint script (not in Python config):

```bash
if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  flask upgrade-db
fi
```

When `true`, the container runs `flask upgrade-db` before starting the API server, ensuring the database schema matches the code version. This is essential during upgrades.

When `false`, migrations are skipped—useful if you want to run them manually or if a separate migration job handles them. For source code deployments (non-Docker), you always run migrations manually with `flask db upgrade`.

**Key code locations:**
- Docker entrypoint: `docker/docker-compose.yaml` and `api/docker/entrypoint.sh`

---

### CHECK_UPDATE_URL

**Default:** `https://updates.dify.ai`

**What it actually does:** The console has a version check feature that calls this URL with the current version. The remote endpoint returns information about newer versions (version number, release date, release notes, whether auto-update is possible).

If set to empty, the version check is skipped entirely—the console shows the current version but never indicates that updates are available. This is useful in air-gapped environments or if you don't want the system making external HTTP calls.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (UpdateConfig)
- Usage: `api/controllers/console/version.py`

---

### OPENAI_API_BASE

**Default:** `https://api.openai.com/v1`

**What it actually does:** This is a **legacy variable** that appears in `.env.example` but is **not actively used** in the current codebase. The modern implementation uses hosted service configurations (`HOSTED_OPENAI_API_BASE`, etc.) instead. It may still be picked up by the OpenAI Python SDK if present in the environment, but Dify's own code does not reference it.

---

### ACCESS_TOKEN_EXPIRE_MINUTES

**Default:** `60` (1 hour)

**What it actually does:** Controls how long a login session's access token remains valid. Dify uses JWT tokens stored in HTTP-only cookies. The access token has a short lifespan—when it expires, the browser automatically uses the refresh token to get a new one without requiring re-login.

**Key code locations:**
- JWT creation: `api/services/account_service.py`
- Cookie settings: `api/libs/token.py`
- WebApp tokens: `api/controllers/web/passport.py`

---

### REFRESH_TOKEN_EXPIRE_DAYS

**Default:** `30` (1 month)

**What it actually does:** Controls how long a user can stay logged in without re-entering credentials. The refresh token is stored in Redis with this TTL and as an HTTP-only cookie. When the access token expires (every 60 minutes by default), the refresh token is used to silently generate a new access token.

If the user doesn't visit for longer than this period, they'll need to log in again.

**Key code locations:**
- Token storage: `api/services/account_service.py`
- Cookie settings: `api/libs/token.py`

---

### APP_MAX_EXECUTION_TIME

**Default:** `1200` (20 minutes)

**What it actually does:** Sets the maximum time an app execution (chat completion, workflow run, etc.) can run before being forcefully terminated. The queue listener that streams results monitors elapsed time and publishes a stop event when this limit is reached.

This prevents runaway executions from consuming resources indefinitely—for example, a workflow with an infinite loop or an extremely slow LLM call.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (AppExecutionConfig)
- Enforcement: `api/core/app/apps/base_app_queue_manager.py`

---

### APP_DEFAULT_ACTIVE_REQUESTS

**Default:** `0` (unlimited)

**What it actually does:** Sets the default concurrent request limit per app. When an app doesn't have a custom `max_active_requests` setting configured in the UI, this value is used as the fallback.

If set to `5`, each app allows at most 5 simultaneous executions by default. New requests while the limit is reached are rejected. `0` means no limit.

Works together with `APP_MAX_ACTIVE_REQUESTS`—the effective limit is the smaller of the two non-zero values.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (AppExecutionConfig)
- Enforcement: `api/services/app_generate_service.py`

---

### APP_MAX_ACTIVE_REQUESTS

**Default:** `0` (unlimited)

**What it actually does:** Sets the global hard ceiling for concurrent requests across all apps. Even if an app's individual limit (or `APP_DEFAULT_ACTIVE_REQUESTS`) is higher, this value can never be exceeded.

Think of it as: `APP_DEFAULT_ACTIVE_REQUESTS` is the per-app default, and `APP_MAX_ACTIVE_REQUESTS` is the system-wide maximum that overrides everything.

**Key code locations:**
- Definition: `api/configs/feature/__init__.py` (AppExecutionConfig)
- Enforcement: `api/services/app_generate_service.py`

---

## Datasource Configuration

### ENABLE_WEBSITE_JINAREADER / ENABLE_WEBSITE_FIRECRAWL / ENABLE_WEBSITE_WATERCRAWL

**Defaults:** `true` / `true` / `true`

**What they actually do:** These are **frontend-only** feature flags. They control whether the corresponding web crawling service appears as an option in the dataset creation UI. The backend does not check these variables—it always supports all crawlers. Setting one to `false` simply hides that option from the UI.

**Key code locations:**
- Frontend config: `web/config/index.ts`, `web/env.ts`
- UI rendering: `web/app/components/datasets/create/website/index.tsx`

---

### NEXT_PUBLIC_ENABLE_SINGLE_DOLLAR_LATEX

**Default:** `false`

**What it actually does:** **Frontend-only.** Controls whether single dollar signs (`$...$`) trigger inline LaTeX rendering in chat responses. Disabled by default because single dollar signs commonly appear in regular text (prices, code), causing unintended math formatting. When enabled, both `$...$` (inline) and `$$...$$` (block) trigger LaTeX. When disabled, only double-dollar works.

**Key code locations:**
- Frontend: `web/env.ts`, `web/app/components/base/markdown/streamdown-wrapper.tsx`

---

## Database Configuration — Connection Pool

### SQLALCHEMY_MAX_OVERFLOW

**Default:** `10`

**What it actually does:** When all `SQLALCHEMY_POOL_SIZE` connections are in use, SQLAlchemy can create up to this many additional temporary connections. So with `pool_size=30` and `max_overflow=10`, up to 40 connections can exist simultaneously. These overflow connections are closed immediately after use (not returned to the pool). If even the overflow is exhausted, new requests wait up to `SQLALCHEMY_POOL_TIMEOUT` seconds.

---

### SQLALCHEMY_POOL_PRE_PING

**Default:** `false`

**What it actually does:** Before handing out a connection from the pool, sends a lightweight test query (`SELECT 1`) to verify the connection is still alive. If the connection is dead (e.g., database restarted, network blip), it's discarded and a fresh one is created. Adds a small amount of latency to every database operation, but prevents "connection lost" errors. Recommended for production deployments with long idle periods or unreliable networks.

---

### SQLALCHEMY_POOL_USE_LIFO

**Default:** `false` (FIFO)

**What it actually does:** Controls the order connections are reused from the pool. FIFO (default) rotates through all connections evenly—good for distributing load. LIFO reuses the most recently returned connection—keeps fewer connections "warm" and can reduce overhead when the pool is larger than typical demand.

---

### SQLALCHEMY_POOL_TIMEOUT

**Default:** `30` (seconds)

**What it actually does:** When a request needs a database connection but none are available (all `pool_size + max_overflow` connections are busy), it waits this many seconds. If no connection frees up in time, the request fails with a timeout error. This is a safety valve preventing requests from hanging indefinitely during database overload.

---

### PostgreSQL / MySQL Performance Tuning Variables

These are **not read by Dify's Python code**. They are passed as startup arguments to the database container in `docker-compose.yaml`. For example, `POSTGRES_SHARED_BUFFERS=128MB` becomes `postgres -c 'shared_buffers=128MB'`. They configure the database server itself, not the application.

---

## Redis Configuration

### REDIS_USE_CLUSTERS / REDIS_CLUSTERS / REDIS_CLUSTERS_PASSWORD

**What they actually do:** Enable Redis Cluster mode (as opposed to standalone or Sentinel mode). When `REDIS_USE_CLUSTERS=true`, Dify creates a `RedisCluster` client that connects to multiple Redis nodes for automatic sharding and high availability. `REDIS_CLUSTERS` is a comma-separated list of nodes (`host1:port1,host2:port2`). Cluster mode is mutually exclusive with Sentinel mode—you use one or the other.

**Key code locations:**
- Definition: `api/configs/middleware/cache/redis_config.py`
- Client creation: `api/extensions/ext_redis.py`

---

### REDIS_MAX_CONNECTIONS

**Default:** (empty; uses redis-py library default)

**What it actually does:** Limits the total number of connections in the Redis connection pool. Applied to standalone, Sentinel, and Cluster modes. When the pool is exhausted, new operations block waiting for a connection to free up. Leave unset to use the library default. Set this if you need to limit Redis connections to match your Redis server's `maxclients` setting.

---

### Redis SSL Variables

`REDIS_SSL_CERT_REQS`, `REDIS_SSL_CA_CERTS`, `REDIS_SSL_CERTFILE`, `REDIS_SSL_KEYFILE` only take effect when `REDIS_USE_SSL=true`. They configure TLS certificate verification and mutual TLS (mTLS) authentication:

- `CERT_REQS`: Level of verification (`CERT_NONE` = no verification, `CERT_REQUIRED` = full verification)
- `CA_CERTS`: Path to the CA certificate for verifying the server
- `CERTFILE` + `KEYFILE`: Client certificate and key for mutual TLS

These same SSL settings are also applied to the Celery broker when `BROKER_USE_SSL=true`.

---

## Celery Configuration

### CELERY_BACKEND

**Default:** `redis`

**What it actually does:** Controls where Celery stores task results after execution. Options: `redis` (stores in Redis, fast), `database` (stores in the main PostgreSQL/MySQL database). For most deployments, `redis` is the right choice.

---

### CELERY_TASK_ANNOTATIONS

**Default:** `null`

**What it actually does:** Applies runtime configuration to specific Celery tasks. Format is a JSON dictionary mapping task names to options like rate limits or time limits. Example: `{"tasks.add": {"rate_limit": "10/s"}}` limits that task to 10 executions per second. Most users don't need this.

---

### CELERY_SENTINEL_PASSWORD

**Default:** (empty)

**What it actually does:** Password for authenticating with Redis Sentinel nodes when using Sentinel mode for the Celery broker. This is separate from `REDIS_SENTINEL_PASSWORD`—they can differ if you use different Sentinel clusters for caching vs task queuing, though in practice they're usually the same value.

---

### BROKER_USE_SSL

**Default:** (auto-detected from URL scheme)

**What it actually does:** This is a computed property, not something you set directly. It returns `true` when `CELERY_BROKER_URL` starts with `rediss://` (note the double `s`). When true, the Redis SSL certificate settings are applied to the Celery broker connection.

---

## CORS Configuration

### COOKIE_DOMAIN / NEXT_PUBLIC_COOKIE_DOMAIN

**What they actually do:** These work together to enable cross-subdomain authentication.

By default (both empty), Dify uses `__Host-` prefixed cookies—the most secure option, but cookies are locked to a single domain. When your frontend and backend are on different subdomains (e.g., `console.example.com` and `api.example.com`), set both to the shared top-level domain (`example.com`) so authentication cookies can be shared across subdomains.

`COOKIE_DOMAIN` is used by the backend when setting cookies. `NEXT_PUBLIC_COOKIE_DOMAIN` is used by the frontend to know the cookie domain.

---

### NEXT_PUBLIC_BATCH_CONCURRENCY

**Default:** `5`

**What it actually does:** **Frontend-only.** Controls how many concurrent API calls the web UI makes during batch operations (e.g., bulk dataset indexing). Does not affect the backend.

---

## Datasource Configuration (continued)

### ENABLE_WEBSITE_JINAREADER / ENABLE_WEBSITE_FIRECRAWL / ENABLE_WEBSITE_WATERCRAWL

Already documented above.

### NEXT_PUBLIC_ENABLE_SINGLE_DOLLAR_LATEX

Already documented above.

---

## Database Configuration (continued)

### DB_TYPE

**Default:** `postgresql`

**What it actually does:** Controls the SQLAlchemy database driver. When set to `postgresql`, uses the `postgresql` driver. Any other value (`mysql`, `oceanbase`, `seekdb`) uses `mysql+pymysql`. Also affects connect_args: PostgreSQL gets `-c timezone=UTC` appended to force UTC timezone on all connections.

**Key code locations:**
- Definition and URI construction: `api/configs/middleware/__init__.py` (DatabaseConfig)

---

### DB_USERNAME

**Default:** `postgres`

**What it actually does:** Database username, URL-encoded into the SQLAlchemy connection URI. There is NO MySQL root-only restriction enforced in the code despite the `.env.example` comment—any valid MySQL user works.

---

### DB_PASSWORD

**Default:** `difyai123456`

**What it actually does:** Database password, URL-encoded into the connection URI to handle special characters like `@`, `:`, `%`.

---

### DB_HOST

**Default:** `db_postgres` (Docker service name) / `localhost` (code default)

**What it actually does:** Database server hostname, used directly in the SQLAlchemy connection URI.

---

### DB_PORT

**Default:** `5432` (always, regardless of DB_TYPE)

**What it actually does:** Database server port. Important: the default is hardcoded to 5432 (PostgreSQL). If you switch to MySQL, you MUST explicitly set `DB_PORT=3306`—there is no auto-detection based on DB_TYPE.

---

### DB_DATABASE

**Default:** `dify`

**What it actually does:** Database/schema name in the connection URI.

---

### SQLALCHEMY_POOL_SIZE

**Default:** `30`

**What it actually does:** Number of persistent connections SQLAlchemy keeps open in its pool. These connections are pre-created and held open, ready for immediate use. Increasing this allows more concurrent database operations but uses more database server resources.

---

### SQLALCHEMY_POOL_RECYCLE

**Default:** `3600` (1 hour)

**What it actually does:** Automatically closes and recreates connections that have been alive longer than this many seconds. Solves the problem of database servers silently dropping idle connections—without recycling, SQLAlchemy would try to use a dead connection and fail.

---

### SQLALCHEMY_ECHO

**Default:** `false`

**What it actually does:** When enabled, logs every SQL statement SQLAlchemy executes to the Python logger. Output includes the raw SQL with bound parameters. Generates massive log volume—for development/debugging only.

---

## Logging Configuration (continued)

### LOG_LEVEL

**Default:** `INFO`

**What it actually does:** Sets the root Python logger level via `logging.basicConfig(level=...)`. Controls the minimum severity that gets logged across all handlers (file + console). Levels from least to most severe: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

---

### LOG_OUTPUT_FORMAT

**Default:** `text`

**What it actually does:** Chooses between two log formatters. `text` produces human-readable lines with timestamp, level, thread, file:line, trace ID, and message. Supports timezone conversion via `LOG_TZ`. `json` produces structured JSON suitable for log aggregation tools (ELK, Datadog, etc.)—but does NOT support `LOG_TZ` (always UTC).

**Key code locations:**
- Formatter selection: `api/extensions/ext_logging.py`

---

### LOG_FILE

**Default:** (empty; console-only logging)

**What it actually does:** When set, enables file-based logging with automatic rotation via Python's `RotatingFileHandler`. The directory is created automatically if it doesn't exist. Also passed to Celery workers as `worker_logfile`. When empty, logs only go to console (stdout).

---

### LOG_FILE_MAX_SIZE

**Default:** `20` (MB)

**What it actually does:** Maximum size of a single log file before rotation. Converted to bytes internally (`value * 1024 * 1024`). When the active log file exceeds this size, it's renamed to `.1`, the previous `.1` becomes `.2`, etc.

---

### LOG_FILE_BACKUP_COUNT

**Default:** `5`

**What it actually does:** Number of rotated log files to keep. With default settings, you'll have at most 6 log files: the active file plus 5 backups (`.1` through `.5`). The oldest is deleted when a new rotation occurs.

---

### LOG_DATEFORMAT

**Default:** (empty; uses Python default `%Y-%m-%d %H:%M:%S`)

**What it actually does:** Timestamp format string for text-format logs. Uses Python's strftime codes. Only applies to text format—JSON format ignores this.

---

### LOG_TZ

**Default:** `UTC`

**What it actually does:** Timezone for log timestamps. Accepts pytz timezone strings (e.g., `America/New_York`, `Asia/Shanghai`). Only applies to text format logs—JSON format always uses UTC. Also sets Celery's internal timezone for task scheduling.

---

## Redis Configuration (continued)

### REDIS_HOST

**Default:** `localhost` (code) / `redis` (.env.example)

**What it actually does:** Redis server hostname. Only used in standalone mode—ignored when Sentinel or Cluster mode is enabled.

---

### REDIS_PORT

**Default:** `6379`

**What it actually does:** Redis server port. Only used in standalone mode.

---

### REDIS_USERNAME

**Default:** (empty)

**What it actually does:** Redis 6.0+ ACL username. Applies to all three modes (standalone, Sentinel, Cluster). When empty, uses Redis's default user.

---

### REDIS_PASSWORD

**Default:** `difyai123456`

**What it actually does:** Redis authentication password. Applies to standalone and Sentinel modes. For Cluster mode, use `REDIS_CLUSTERS_PASSWORD` instead.

---

### REDIS_DB

**Default:** `0`

**What it actually does:** Redis database number (0-15). Only applies to standalone and Sentinel modes (Cluster mode doesn't support database selection). Important: Celery broker parses its own database number from `CELERY_BROKER_URL`—make sure they don't collide. Default setup uses DB 0 for cache and DB 1 for Celery.

---

### REDIS_USE_SSL

**Default:** `false`

**What it actually does:** Changes the Redis connection class from plain `Connection` to `SSLConnection`. Also auto-detects in pub/sub URL building (changes scheme to `rediss://`). Does NOT automatically apply SSL to Sentinel protocol—Sentinel runs its own protocol.

---

### REDIS_USE_SENTINEL

**Default:** `false`

**What it actually does:** Switches from standalone to Sentinel mode. When enabled, `REDIS_HOST`/`REDIS_PORT` are ignored. Instead, Dify connects to the Sentinel nodes listed in `REDIS_SENTINELS`, asks them for the current master node for the service named `REDIS_SENTINEL_SERVICE_NAME`, and connects to that master. Failover is automatic—if the master goes down, Sentinel promotes a replica and Dify follows.

---

### REDIS_SENTINELS

**Default:** (empty)

**What it actually does:** Comma-separated list of Sentinel nodes, parsed by splitting on `,` then on `:` to get `[(host1, port1), (host2, port2), ...]`. These are the Sentinel instances, not the actual Redis servers.

---

### REDIS_SENTINEL_SERVICE_NAME

**Default:** (empty)

**What it actually does:** The logical service name that Sentinel monitors (configured in sentinel.conf as `sentinel monitor <name> ...`). Dify calls `sentinel.master_for(service_name)` to get the current master's address.

---

### REDIS_SENTINEL_USERNAME / REDIS_SENTINEL_PASSWORD

**Defaults:** (both empty)

**What they actually do:** Authentication for the Sentinel instances themselves—NOT for the Redis master/replica servers (those use `REDIS_USERNAME`/`REDIS_PASSWORD`). Sentinel nodes may require separate credentials.

---

### REDIS_SENTINEL_SOCKET_TIMEOUT

**Default:** `0.1` (seconds)

**What it actually does:** Socket timeout for communicating with Sentinel nodes. If too low, Sentinel health checks and master discovery may time out intermittently. Default 0.1s assumes fast local network. For cloud/WAN deployments, increase to 1.0-5.0s.

---

## Celery Configuration (continued)

### CELERY_BROKER_URL

Already documented above. Additional detail: the URL is parsed by Kombu's `parse_url()` to extract hostname, port, password, and database number. Supports both `redis://` and `rediss://` schemes.

---

### CELERY_USE_SENTINEL / CELERY_SENTINEL_MASTER_NAME / CELERY_SENTINEL_SOCKET_TIMEOUT

Already documented above. These form a cohesive unit: `CELERY_USE_SENTINEL` is the toggle, the other two provide the configuration. They configure `broker_transport_options` which Celery uses for Sentinel-aware broker connections.

---

## CORS Configuration (continued)

### WEB_API_CORS_ALLOW_ORIGINS

**Default:** `*`

**What it actually does:** Comma-separated string that gets split into a list. Applied to the Web API and Service API blueprints, covering public API endpoints (chat messages, embedded bots, authenticated API calls).

---

### CONSOLE_CORS_ALLOW_ORIGINS

**Default:** (empty; falls back to `CONSOLE_WEB_URL` via Pydantic AliasChoices)

**What it actually does:** Same format as above, but applied to the console API blueprint and FastOpenAPI endpoints. If not explicitly set, Pydantic's `AliasChoices("CONSOLE_CORS_ALLOW_ORIGINS", "CONSOLE_WEB_URL")` falls back to `CONSOLE_WEB_URL`—so for single-domain setups, you only need to set `CONSOLE_WEB_URL`.

---

## Container Startup Configuration (continued)

### DIFY_BIND_ADDRESS

**Default:** `0.0.0.0`

**What it actually does:** Network interface the API server binds to. `0.0.0.0` listens on all interfaces. Set to `127.0.0.1` to restrict to localhost only. Used in both Flask debug mode and Gunicorn production mode.

---

### DIFY_PORT

**Default:** `5001`

**What it actually does:** Port the API server listens on. Combined with `DIFY_BIND_ADDRESS` for the full socket binding in the entrypoint script.

---

### SERVER_WORKER_AMOUNT

**Default:** `1`

**What it actually does:** Number of Gunicorn worker processes. With gevent (default), each worker handles multiple concurrent connections via greenlets, so 1 is usually sufficient. For sync workers, Gunicorn docs recommend `(2 x CPU cores) + 1`.

---

### SERVER_WORKER_CLASS

**Default:** `gevent`

**What it actually does:** Gunicorn worker type. Gevent provides lightweight concurrency via greenlets. After gevent monkey-patches Python's standard library, a `post_patch()` hook patches psycopg2 (PostgreSQL driver) and gRPC for async compatibility. Changing this breaks these patches and requires removing gevent dependencies.

---

### SERVER_WORKER_CONNECTIONS

**Default:** `10`

**What it actually does:** Maximum concurrent connections per worker. Only applies to async workers (gevent). With default settings (1 worker, 10 connections), the server handles up to 10 concurrent requests. Increase for high-concurrency deployments.

---

### GUNICORN_TIMEOUT

**Default:** `360`

**What it actually does:** If a worker doesn't respond within this many seconds, Gunicorn kills and restarts it. The client request is lost. Set to 360 (6 minutes) to support long-lived SSE (Server-Sent Events) connections used for streaming LLM responses.

---

### CELERY_WORKER_CLASS

**Default:** (empty; defaults to `gevent`)

**What it actually does:** Worker type for Celery task processing. Same gevent patching requirements as `SERVER_WORKER_CLASS`. The entrypoint script checks `CELERY_WORKER_POOL` first, then `CELERY_WORKER_CLASS`, then falls back to `gevent`.

---

### CELERY_WORKER_AMOUNT

**Default:** (empty; defaults to `1`)

**What it actually does:** Number of Celery worker processes (concurrency level). Only used when autoscaling is disabled. Passed as the `-c` flag to Celery.

---

### CELERY_AUTO_SCALE / CELERY_MAX_WORKERS / CELERY_MIN_WORKERS

**Defaults:** `false` / (empty; defaults to CPU count) / (empty; defaults to 1)

**What they actually do:** When `CELERY_AUTO_SCALE=true`, Celery uses `--autoscale=MAX,MIN` instead of fixed concurrency. Celery monitors queue depth and spawns/kills workers dynamically between MIN and MAX. Useful for variable workloads with spiky task queues.

---

### API_TOOL_DEFAULT_CONNECT_TIMEOUT / API_TOOL_DEFAULT_READ_TIMEOUT

**Defaults:** `10` / `60`

**What they actually do:** Timeout values (in seconds) for HTTP requests made by API Tool nodes in workflows. Connect timeout controls how long to wait for establishing a TCP connection; read timeout controls how long to wait for the response. When exceeded, the tool invocation fails. Read directly via `os.getenv()` in `api/core/tools/custom_tool/tool.py`.

---

## Knowledge Configuration

### UPLOAD_FILE_SIZE_LIMIT

**Default:** `15` (MB)

**What it actually does:** Maximum file size for general document uploads (PDFs, Word docs, etc.). Enforced in `FileService.is_file_size_within_limit()`—users get a `FileTooLargeError` when exceeded. Does not apply to images, videos, or audio (they have separate limits).

### UPLOAD_FILE_BATCH_LIMIT

**Default:** `5`

**What it actually does:** Returned to the frontend as `batch_count_limit` in the upload config endpoint. Primarily a frontend hint for the file picker dialog, not strictly enforced server-side for individual batches.

### UPLOAD_FILE_EXTENSION_BLACKLIST

**Default:** (empty—all file types allowed)

**What it actually does:** Comma-separated list of blocked file extensions (lowercase, no dots). Enforced in `FileService.upload_file()`—raises `BlockedFileExtensionError`. Users see: "File extension '.exe' is not allowed for security reasons."

### SINGLE_CHUNK_ATTACHMENT_LIMIT

**Default:** `10`

**What it actually does:** Maximum number of images/files that can be embedded in a single knowledge base chunk (segment). A "chunk" is a segment of content in the knowledge base. When creating or editing a segment with more images than this limit, it raises a ValueError.

### IMAGE_FILE_BATCH_LIMIT

**Default:** `10`

**What it actually does:** Maximum images per upload batch. Returned to frontend in upload config. Different from `SINGLE_CHUNK_ATTACHMENT_LIMIT` which limits images per knowledge base segment.

### ATTACHMENT_IMAGE_FILE_SIZE_LIMIT

**Default:** `2` (MB)

**What it actually does:** Maximum size for images embedded in knowledge base content from external URLs. When Dify indexes a document with markdown images (`![alt](url)`), it fetches them. Images larger than this are skipped. Different from `UPLOAD_IMAGE_FILE_SIZE_LIMIT` (10 MB) which applies to direct image uploads via UI.

### ATTACHMENT_IMAGE_DOWNLOAD_TIMEOUT

**Default:** `60` (seconds)

**What it actually does:** Timeout for downloading images from external URLs during knowledge base indexing. Uses SSRF proxy for the request. If an external image server is slow or unresponsive, the download is abandoned after this timeout and the image is skipped.

### ETL_TYPE

**Default:** `dify`

**What it actually does:** Chooses the document extraction library. `dify` uses built-in extractors (supports txt, md, pdf, html, xlsx, docx, csv). `Unstructured` uses Unstructured.io (adds support for doc, msg, eml, ppt, pptx, xml, epub). The choice affects which file types appear as uploadable in the UI.

### UNSTRUCTURED_API_URL / UNSTRUCTURED_API_KEY

**Defaults:** both empty

**What they actually do:** Connection settings for Unstructured.io API. Only needed when `ETL_TYPE=Unstructured`. The URL is also checked to enable .ppt file support (old PowerPoint format only works with Unstructured).

### TOP_K_MAX_VALUE

**Default:** `10`

**What it actually does:** Maximum value users can set for the `top_k` parameter in knowledge base retrieval. Defined in `.env.example` and docker-compose but not yet in Python config classes.

---

## Model Configuration

### PROMPT_GENERATION_MAX_TOKENS / CODE_GENERATION_MAX_TOKENS

**Defaults:** `512` / `1024`

**What they actually do:** Defined in `.env.example` but not yet implemented in Python config. Intended to limit LLM output tokens when auto-generating prompts or code.

### PLUGIN_BASED_TOKEN_COUNTING_ENABLED

**Default:** `false`

**What it actually does:** When enabled, uses plugin-based token counting via PluginModelClient for accurate token usage tracking. When disabled, token counting returns 0 (faster, but cost/usage tracking is less accurate).

---

## Multi-modal Configuration

### MULTIMODAL_SEND_FORMAT

**Default:** `base64`

**What it actually does:** When sending files to multi-modal LLMs, `base64` embeds the file data directly in the request (more compatible, works offline, larger requests). `url` sends a signed URL for the model to fetch (faster, smaller requests, but requires FILES_URL to be externally accessible and the model must have internet access).

### UPLOAD_IMAGE_FILE_SIZE_LIMIT / UPLOAD_VIDEO_FILE_SIZE_LIMIT / UPLOAD_AUDIO_FILE_SIZE_LIMIT

**Defaults:** `10` / `100` / `50` (MB)

**What they actually do:** Maximum file sizes for direct uploads via UI, enforced in `FileService.is_file_size_within_limit()`. Each applies to its respective file type category (images: jpg/png/webp/gif/svg; videos: mp4/mov/mpeg/webm; audio: mp3/m4a/wav/amr/mpga).

---

## Sentry Configuration

### SENTRY_DSN vs API_SENTRY_DSN

`SENTRY_DSN` is the canonical variable used in the Python backend. `API_SENTRY_DSN` is a Docker-level alias that maps to it. They are effectively the same.

### WEB_SENTRY_DSN

Frontend-only (maps to `NEXT_PUBLIC_SENTRY_DSN` in the Next.js web app). Not used by the backend.

### PLUGIN_SENTRY_ENABLED / PLUGIN_SENTRY_DSN

Placeholder variables for future plugin daemon Sentry integration. Not yet implemented in Python code.

---

## Notion Integration

### NOTION_INTEGRATION_TYPE

**Default:** `public`

**What it actually does:** Selects between two Notion API authentication modes. `public` uses standard OAuth 2.0 (requires HTTPS for redirect URL, needs CLIENT_ID + CLIENT_SECRET). `internal` uses a direct integration token (works with HTTP, only needs NOTION_INTERNAL_SECRET). Use `internal` for local deployments since Notion's OAuth redirect URL requires HTTPS.

---

## Mail Configuration

### SMTP_USE_TLS vs SMTP_OPPORTUNISTIC_TLS

Three modes:
- **Implicit TLS** (`SMTP_USE_TLS=true`, `SMTP_OPPORTUNISTIC_TLS=false`): Uses `SMTP_SSL` on port 465. TLS from the start.
- **Explicit TLS/STARTTLS** (`SMTP_USE_TLS=true`, `SMTP_OPPORTUNISTIC_TLS=true`): Uses `SMTP` on port 587, then upgrades to TLS via STARTTLS command.
- **Plain** (`SMTP_USE_TLS=false`, `SMTP_OPPORTUNISTIC_TLS=false`): No encryption.
- `SMTP_USE_TLS=false` + `SMTP_OPPORTUNISTIC_TLS=true` is invalid and raises an error.

---

## Others Configuration

### CODE_EXECUTION_ENDPOINT / CODE_EXECUTION_API_KEY

The sandbox is a separate Go service that executes Python/JavaScript/Jinja2 code nodes. Dify sends POST requests to `{endpoint}/v1/sandbox/run` with the API key in `X-Api-Key` header. The sandbox runs code in isolation with configurable network access.

### WORKFLOW_MAX_EXECUTION_STEPS / WORKFLOW_MAX_EXECUTION_TIME / WORKFLOW_CALL_MAX_DEPTH

Enforced by `ExecutionLimitsLayer` in the graph engine. Steps counts every node execution. Time is wall-clock. Depth limits nested workflow-calls-workflow. Exceeding any of these terminates the workflow.

### MAX_VARIABLE_SIZE

**Default:** `204800` (200 KB)

Checked when creating variables: `if result.size > MAX_VARIABLE_SIZE` raises `VariableError`. Prevents memory attacks via extremely large variable values.

### HTTP_REQUEST_MAX_CONNECT_TIMEOUT / HTTP_REQUEST_MAX_READ_TIMEOUT / HTTP_REQUEST_MAX_WRITE_TIMEOUT

These are maximum ceilings. Users can set per-node timeouts in the workflow editor, but those values cannot exceed these limits.

### WEBHOOK_REQUEST_BODY_MAX_SIZE

Checked in webhook service's `_validate_content_length()`. Rejects payloads larger than this with `RequestEntityTooLarge`. Prevents webhook payload bombing.

### SSRF_PROXY_HTTP_URL / SSRF_PROXY_HTTPS_URL

All outbound HTTP requests from Dify (HTTP nodes, extension requests, image downloads) route through this SSRF proxy. The proxy (Squid) blocks requests to internal/private IP ranges, preventing Server-Side Request Forgery attacks.

### RESPECT_XFORWARD_HEADERS_ENABLED

When enabled, wraps the WSGI app with Flask's ProxyFix middleware, trusting X-Forwarded-For/Proto/Port headers. Only enable behind a single trusted reverse proxy—otherwise allows IP spoofing.

---

## Plugin Daemon Configuration

### PLUGIN_DAEMON_URL / PLUGIN_DAEMON_KEY

The plugin daemon is a separate process. All plugin operations (list, install, execute) flow as HTTP requests to this URL with the key in `X-Api-Key` header.

### PLUGIN_DIFY_INNER_API_KEY

The reverse direction: when the plugin daemon needs to call back to the Dify API (e.g., to access files or models), it authenticates with this key via `X-Inner-Api-Key` header. Must match between API and plugin daemon services.

### MARKETPLACE_ENABLED / MARKETPLACE_API_URL

When disabled, only locally installed plugins are available. When enabled, Dify fetches plugin manifests from the marketplace for browsing, installation, and auto-upgrade checking.

### FORCE_VERIFYING_SIGNATURE

When true, plugin packages must have valid signatures before installation. Prevents installing tampered or unsigned plugins.

### PIP_MIRROR_URL

Used by the plugin daemon (not the Python API) when installing plugin dependencies. Set to a local PyPI mirror for faster installs or air-gapped environments.

---

## OTLP / OpenTelemetry

### ENABLE_OTEL

Master switch. When enabled, instruments Flask with OpenTelemetry for distributed tracing and metrics.

### OTLP endpoint fallback chain

If `OTLP_TRACE_ENDPOINT` is set, use it. Otherwise, use `OTLP_BASE_ENDPOINT + "/v1/traces"`. Same pattern for metrics.

### OTEL_SAMPLING_RATE

**Default:** `0.1` (10%)

Probabilistic sampling: only 10% of traces are exported by default. Reduces overhead in high-traffic production environments.

---

## Scheduled Tasks

### ENABLE_CLEAN_EMBEDDING_CACHE_TASK

Deletes embedding cache records older than the configured retention period. Manages database size for the embeddings table.

### ENABLE_CLEAN_UNUSED_DATASETS_TASK

Disables documents in knowledge bases that haven't had activity within the retention period. Logs cleanup in `DatasetAutoDisableLog`.

### ENABLE_CLEAN_MESSAGES

Deletes conversation messages older than `SANDBOX_EXPIRED_RECORDS_RETENTION_DAYS`. If billing is enabled, only cleans sandbox-tier tenants.

### ENABLE_MAIL_CLEAN_DOCUMENT_NOTIFY_TASK

Sends email to workspace owners listing which knowledge bases had documents auto-disabled by the unused datasets cleanup task.

### ENABLE_DATASETS_QUEUE_MONITOR

Monitors the dataset processing queue length in Redis. Sends email alerts to `QUEUE_MONITOR_ALERT_EMAILS` when the backlog exceeds `QUEUE_MONITOR_THRESHOLD`.

### ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK

Fetches all plugin manifests from marketplace, compares with installed versions, and dispatches upgrade tasks according to each tenant's auto-upgrade schedule.

---

## Sandbox / Web Frontend / Nginx / Docker

### TEXT_GENERATION_TIMEOUT_MS

Frontend-only. Controls UI timeout for streaming text generation—pauses rendering if the stream exceeds this duration.

### SANDBOX_*

Configure the isolated code execution sandbox (a separate Go service). `SANDBOX_ENABLE_NETWORK` controls whether code can make outbound HTTP requests. `SANDBOX_WORKER_TIMEOUT` limits individual code execution time.

### COMPOSE_PROFILES

Docker Compose feature. Each service declares which profiles it belongs to. The value `${VECTOR_STORE:-weaviate},${DB_TYPE:-postgresql}` starts the correct database and vector store containers automatically based on your choices.

---

## File Storage Configuration

### STORAGE_TYPE

**Default:** `opendal`

**What it actually does:** The central dispatcher in `api/extensions/ext_storage.py` uses a match/case pattern to select and initialize the storage backend. 12 backend types are supported. The `opendal` type is the modern default—it wraps Apache OpenDAL which provides a unified interface to many storage services. The old `local` type is deprecated but still works—it internally uses `OpenDALStorage(scheme="fs")`, the same as opendal with filesystem scheme.

### OPENDAL_SCHEME / OPENDAL_FS_ROOT

**Defaults:** `fs` / `storage`

**What they actually do:** When `STORAGE_TYPE=opendal`, Dify scans environment variables matching `OPENDAL_<SCHEME>_*` and passes them as kwargs to the OpenDAL Operator. For example, with `OPENDAL_SCHEME=s3`, it scans for `OPENDAL_S3_ACCESS_KEY_ID`, `OPENDAL_S3_SECRET_ACCESS_KEY`, etc. Environment variables take precedence over `.env` file values.

For the default `fs` scheme, `OPENDAL_FS_ROOT` sets the local directory path. The directory is created automatically.

### S3_USE_AWS_MANAGED_IAM

**Default:** `false`

**What it actually does:** When `true`, creates a `boto3.Session()` without explicit credentials—boto3 auto-discovers credentials from EC2 instance metadata, ECS task roles, etc. When `false`, explicitly passes `S3_ACCESS_KEY` and `S3_SECRET_KEY` to the boto3 client.

### ARCHIVE_STORAGE_*

**What they actually do:** Separate S3-compatible storage for workflow run log archival. Used by the paid plan retention system to archive workflow runs older than 90 days to JSONL format. Tables archived include workflow_runs, workflow_node_executions, workflow_trigger_logs, etc. Requires `BILLING_ENABLED=true` and `ARCHIVE_STORAGE_ENABLED=true`. Different from main storage (which stores active files)—archive storage is write-once, read-rarely for compliance/audit.

### Provider credential variables

All provider-specific credential variables (S3_ENDPOINT, AZURE_BLOB_ACCOUNT_NAME, ALIYUN_OSS_ACCESS_KEY, etc.) are defined in Pydantic config classes under `api/configs/middleware/storage/` and flow directly to their respective client libraries (boto3, azure-storage-blob, oss2, etc.) during initialization in `api/extensions/storage/`.

---

## Vector Database Configuration

### VECTOR_STORE

**Default:** `weaviate` (from .env.example; code default is `None`)

**What it actually does:** The factory in `api/core/rag/datasource/vdb/vector_factory.py` uses a match/case pattern with `VectorType` enum to select and initialize the vector store backend. Supports 37+ backends with lazy imports. Falls back to the dataset's existing index type if the dataset already has one.

### VECTOR_INDEX_NAME_PREFIX

**Default:** `Vector_index`

**What it actually does:** Used in `Dataset.gen_collection_name_by_id()` to generate collection names: `{prefix}_{dataset_id}_Node`. Dataset ID hyphens are converted to underscores.

### WEAVIATE_GRPC_ENDPOINT

Separate gRPC endpoint for high-performance binary protocol communication alongside REST. Parses URL to extract host, port, and security scheme. Falls back to inferring from HTTP endpoint if not set. gRPC provides significantly better performance for batch operations.

### MILVUS_ENABLE_HYBRID_SEARCH

When enabled, creates a BM25 sparse index for full-text search alongside vector similarity search. Requires Milvus >= 2.5.0. If the collection was created without this flag, it must be recreated after enabling.

### ELASTICSEARCH_USE_CLOUD

Toggles between self-hosted mode (uses HOST/PORT/USERNAME/PASSWORD) and Elastic Cloud mode (uses CLOUD_URL/API_KEY). Different credential requirements and client initialization paths.

### OPENSEARCH_AUTH_METHOD

Two modes: `basic` (username/password via http_auth) and `aws_managed_iam` (SigV4 request signing via Boto3 credentials). The `aws_service` setting distinguishes between Elasticsearch Service (`es`) and OpenSearch Serverless (`aoss`).

### OCEANBASE_ENABLE_HYBRID_SEARCH

Similar to Milvus—enables fulltext index creation for BM25 queries alongside vector search. Requires OceanBase >= 4.3.5.1. Collections must be recreated after enabling.

---

## 1.14 Additions (traced 2026-04-22)

### REDIS_KEY_PREFIX

**Default:** `""` (empty)

**What it actually does:** Prepends a string namespace to every Redis key that Dify writes, so multiple Dify deployments can safely share one Redis server. When set to `staging:`, a `get("session_token:abc")` call becomes `GET staging:session_token:abc` on the wire.

The prefix is threaded through `RedisClientWrapper` in `api/extensions/ext_redis.py` via helpers in `api/extensions/redis_names.py` (`serialize_redis_name`, `serialize_redis_name_arg`, `serialize_redis_name_args`, `normalize_redis_key_prefix`). Every wrapper method — `get`, `set`, `setex`, `delete`, `incr`, `expire`, `exists`, `ttl`, `lock`, `hset`, `zadd`, and so on — prefixes its name argument before forwarding. `delete(*names)` and `exists(*names)` prefix every name.

Beyond direct key operations, the prefix is also applied to:

- **Pub/Sub channels** — `libs/broadcast_channel/redis/channel.py`, `sharded_channel.py`
- **Redis Streams** — `libs/broadcast_channel/redis/streams_channel.py`
- **Celery Redis transport** — applied as Celery's `global_keyprefix` transport option in `api/extensions/ext_celery.py`, so broker queues and result-backend keys follow the same namespace
- **DB migration locks** — `libs/db_migration_lock.py`

`normalize_redis_key_prefix()` strips whitespace; whitespace-only values are treated as empty (no prefixing).

**If left empty:** Keys are written unprefixed (backward-compatible with existing deployments). Correct choice when Dify has Redis to itself.

**If set:** Every key, channel, stream, and Celery artifact is namespaced. Existing data written without the prefix becomes invisible to the new client — plan a wipe or dual-run when switching.

**Key code locations:**
- Definition: `api/configs/middleware/cache/redis_config.py`
- Wrapper plumbing: `api/extensions/ext_redis.py`, `api/extensions/redis_names.py`
- Celery: `api/extensions/ext_celery.py`
- Broadcast channels: `api/libs/broadcast_channel/redis/{channel,sharded_channel,streams_channel}.py`
- Migration lock: `api/libs/db_migration_lock.py`

**Source:** PR #35139 (issue #35138), merged 2026-04-14.

---

### REDIS_RETRY_RETRIES / REDIS_RETRY_BACKOFF_BASE / REDIS_RETRY_BACKOFF_CAP

**Defaults:** `3`, `1.0`, `10.0`

**What they actually do:** `_get_retry_policy()` in `api/extensions/ext_redis.py` constructs a shared `redis.retry.Retry` object with `ExponentialWithJitterBackoff(base=BACKOFF_BASE, cap=BACKOFF_CAP)` and `retries=RETRIES`. The policy is attached to every standalone, Sentinel, and Cluster client (via `_get_connection_health_params()` / `_get_cluster_connection_health_params()`), and also to pub/sub clients built by `_create_pubsub_client()`.

When `redis-py` encounters transient failures (`ConnectionError`, `TimeoutError`, `socket.timeout`), it calls `Retry.call_with_retry()`, which sleeps `min(base * (2^attempt) + jitter, cap)` seconds between attempts, up to `retries` attempts. With the defaults, worst-case wait before surfacing the error is roughly `1s + 2s + 4s = 7s` plus jitter, capped at 10s per sleep.

**If left at default:** Most transient hiccups (master failover, brief DNS blip, half-open socket) are invisible to callers. Worst-case latency cost on a bad command is bounded.

**If `REDIS_RETRY_RETRIES=0`:** No retry; every transient error propagates immediately. Matches pre-1.14 behavior.

**If backoff values are raised:** Longer tails but more patience for slow failovers. Lowered: faster failure but less resilience.

**Key code locations:**
- Definition: `api/configs/middleware/cache/redis_config.py`
- Policy construction: `_get_retry_policy()` in `api/extensions/ext_redis.py`
- Applied via: `_get_connection_health_params()`, `_get_cluster_connection_health_params()`, `_get_base_redis_params()`, `_create_pubsub_client()`

**Source:** PR #34566 (issue #34557), merged 2026-04-09.

---

### REDIS_SOCKET_TIMEOUT / REDIS_SOCKET_CONNECT_TIMEOUT

**Defaults:** `5.0`, `5.0`

**What they actually do:** `socket_timeout` bounds how long each Redis command waits on a read/write on an already-established connection; `socket_connect_timeout` bounds how long the TCP handshake phase can take. Both are part of `RedisBaseParamsDict` in `_get_base_redis_params()` and flow into every client type — `redis.ConnectionPool`, `Sentinel.master_for()`, `RedisCluster`, and pub/sub clients all receive them.

Before PR #34566, the main backend clients built through `ConnectionPool(**redis_params)` / `sentinel.master_for(...)` / `RedisCluster.from_url(...)` used `redis-py`'s internal default (no socket timeout on standalone), which meant commands could block indefinitely on a silently-dropped connection.

**If left at default:** Stuck connections surface as timeouts after 5 seconds. Appropriate for most local or same-region deployments.

**If increased:** Necessary for cloud or WAN deployments where p99 network latency exceeds 5s under load. The existing `REDIS_SENTINEL_SOCKET_TIMEOUT` doc already notes this pattern for Sentinel; the same reasoning applies to the main client.

**Key code locations:**
- Definition: `api/configs/middleware/cache/redis_config.py`
- Used in: `_get_connection_health_params()`, `_get_cluster_connection_health_params()` in `api/extensions/ext_redis.py`

**Source:** PR #34566, merged 2026-04-09.

---

### REDIS_HEALTH_CHECK_INTERVAL

**Default:** `30` (seconds)

**What it actually does:** `redis-py`'s `Connection` class sends a PING on a connection if it has been idle longer than this many seconds before reusing it. Catches half-open sockets that the kernel hasn't noticed yet (e.g., after a NAT rebind or a silent LB timeout). Set to `0` to disable.

**Important asymmetry:** The parameter is passed only in `_get_connection_health_params()` (standalone + Sentinel). `_get_cluster_connection_health_params()` explicitly drops it — see the inline comment in `ext_redis.py`:

> "RedisCluster does not support `health_check_interval` as a constructor keyword (it is silently stripped by `cleanup_kwargs`), so it is excluded here. Only `retry`, `socket_timeout`, and `socket_connect_timeout` are passed through."

This is a known `redis-py` quirk. The doc row explicitly flags it so cluster users don't waste time tuning a no-op.

**If left at default:** Background PINGs every 30s on idle connections prevent stale-connection errors.

**If set to 0:** No background health checks. Saves a tiny bit of traffic; acceptable if load is high enough that every connection is used constantly.

**Key code locations:**
- Definition: `api/configs/middleware/cache/redis_config.py`
- Application: `_get_connection_health_params()` in `api/extensions/ext_redis.py`
- Cluster exclusion: `_get_cluster_connection_health_params()` in the same file

**Source:** PR #34566, merged 2026-04-09.

---

### BAIDU_VECTOR_DB_AUTO_BUILD_ROW_COUNT_INCREMENT / BAIDU_VECTOR_DB_AUTO_BUILD_ROW_COUNT_INCREMENT_RATIO

**Defaults:** `500`, `0.05`

**What they actually do:** Control when the Baidu Vector DB backend rebuilds its ANN index automatically. The Baidu SDK treats them as the "absolute row increase" and "relative row increase" thresholds; when either is exceeded, the index is rebuilt in the background.

Defined in `api/configs/middleware/vdb/baidu_vector_config.py` on `BaiduVectorDBConfig`; passed to the Baidu backend factory when initializing a collection. Only meaningful when `VECTOR_STORE=baidu`.

**If left at default:** Index rebuilds are triggered by 500 new rows OR a 5% increase, whichever happens first. Keeps search quality high for typical workloads.

**If raised:** Fewer rebuilds, lower CPU churn, but search quality degrades between rebuilds.

**If lowered:** More frequent rebuilds, higher background load, freshest index.

**Key code locations:**
- Definition: `api/configs/middleware/vdb/baidu_vector_config.py`
- Factory: `api/providers/vdb/vdb-baidu/src/dify_vdb_baidu/baidu_vector.py` (post 1.14 workspace refactor)

---

### BAIDU_VECTOR_DB_REBUILD_INDEX_TIMEOUT_IN_SECONDS

**Default:** `300`

**Code inconsistency to flag:** The Pydantic `Field` description in `baidu_vector_config.py` reads "default is 3600 seconds" but the actual `default=300`. `docker/.env.example` also uses 300. Document 300 (what users actually get); the description string is stale and should be flagged upstream.

**What it actually does:** Maximum wall-clock time the client waits for a Baidu VDB index rebuild before raising a timeout. 300 seconds (5 minutes) is adequate for small-to-medium collections; large collections (millions of rows) may need more.

**If it times out:** The client-side call fails, but the rebuild may still complete on the server. Re-querying after the rebuild succeeds typically resolves the error.

**Key code locations:**
- Definition: `api/configs/middleware/vdb/baidu_vector_config.py`

---

### COMPOSE_WORKER_HEALTHCHECK_DISABLED / _INTERVAL / _TIMEOUT

**Defaults:** `true`, `30s`, `30s`

**What they actually do:** Purely Docker Compose concerns. In `docker/docker-compose.yaml`, the `worker` service's `healthcheck:` block resolves to:

```yaml
test: ["CMD-SHELL", "celery -A celery_healthcheck.celery inspect ping"]
interval: ${COMPOSE_WORKER_HEALTHCHECK_INTERVAL:-30s}
timeout: ${COMPOSE_WORKER_HEALTHCHECK_TIMEOUT:-30s}
retries: 3
start_period: 60s
disable: ${COMPOSE_WORKER_HEALTHCHECK_DISABLED:-true}
```

`celery inspect ping` is a synchronous command that round-trips through the broker to ask every worker "are you alive?" and waits for replies. Under heavy load it can itself take significant time and contribute to broker contention, which is why the health check is **disabled by default**.

**If disabled (default):** Compose marks the worker container healthy based on process liveness only (PID 1 running). Lighter but won't detect a hung worker that's still alive at the process level.

**If enabled (`COMPOSE_WORKER_HEALTHCHECK_DISABLED=false`):** Compose runs `celery inspect ping` every `INTERVAL` with a `TIMEOUT` per attempt. Three consecutive failures mark the container unhealthy, which triggers Compose restart policies or orchestration reactions. Useful when operators have observed hung-worker incidents and the added broker traffic is acceptable.

`INTERVAL` and `TIMEOUT` accept Docker Compose duration strings (`30s`, `1m`, `1m30s`).

**Key code locations:**
- Definition: `docker/.env.example`, `docker/docker-compose.yaml`
- No Pydantic config; these are Compose-only, not read by Python code.

---

### ALLOW_INLINE_STYLES

**Default:** `false`

**What it actually does:** Frontend-only security toggle. `web/docker/entrypoint.sh` maps the operator-facing `ALLOW_INLINE_STYLES` (set in `docker/.env`) to `NEXT_PUBLIC_ALLOW_INLINE_STYLES` for the Next.js runtime:

```bash
export NEXT_PUBLIC_ALLOW_INLINE_STYLES=${ALLOW_INLINE_STYLES:-false}
```

The frontend's Markdown sanitizer reads `NEXT_PUBLIC_ALLOW_INLINE_STYLES` to decide whether to allow inline `style="..."` attributes and `<style>` tags in user-generated Markdown (chat responses, knowledge base content, and so on). Disabled by default because inline styles can be abused for phishing (e.g., hiding a malicious link behind a styled block that overlays trusted UI).

**If disabled (default):** Markdown rendering strips inline styles. User-authored content still renders, just without custom styling.

**If enabled:** Inline styles pass through. Enable only if your content pipeline is trusted and you need rich visual control from Markdown authors.

**Key code locations:**
- Mapping: `web/docker/entrypoint.sh`
- Default: `docker/.env.example` (root) and `web/.env.example` (source-code deployments)

---

### CELERY_WORKER_AMOUNT — default correction

The existing entry near line 937 describes behavior correctly, but the stated default ("1") no longer matches `docker/.env.example`, which sets `CELERY_WORKER_AMOUNT=4` (consumed by `docker-compose.yaml` via `${CELERY_WORKER_AMOUNT:-4}`). Docs updated to `4`.

**Why the change matters:** 4 is a better out-of-the-box baseline for a machine with a few cores; users with lighter workloads can still set it lower, and `CELERY_AUTO_SCALE=true` overrides it entirely.

---

### POSTGRES_MAX_CONNECTIONS — default correction

Covered in the "PostgreSQL / MySQL Performance Tuning Variables" section. `docker/.env.example` bumped the default from `100` to `200` upstream (`docker-compose.yaml` passes it as `-c max_connections=${POSTGRES_MAX_CONNECTIONS:-200}` to the Postgres container). The higher default is safer for Dify's multi-worker + Celery + async-task traffic shape; operators can still lower it on constrained hosts.
