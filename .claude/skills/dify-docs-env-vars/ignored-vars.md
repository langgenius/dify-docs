# Intentionally Ignored Environment Variables

Variables listed here appear in Dify's `docker/.env.example` or `api/configs/`, but are deliberately **not** documented in `en/self-host/deploy/configuration/environments.mdx`. The verifier script reads this file and skips matching variables when comparing docs against `.env.example`.

## When to update this list

Add an entry when you:

- Remove a variable from the docs because it only applies to Dify Cloud.
- Skip documenting a new variable because it's experimental, internal, or not user-tunable.
- Identify a verifier false positive (e.g., the variable is commented-out in `.env.example` but documented because the code supports it).

Remove an entry when the reason no longer holds (e.g., an experimental flag graduates to a stable, user-facing feature).

Every entry requires: variable name, category, reason, and a source reference (commit, PR, or issue). This enforces traceability so later maintainers can audit the decision.

## Format

The verifier parses the tables below. A line is treated as an ignore entry when it matches `| \`VARIABLE_NAME\` | ...`. Additional columns are informational.

---

## Cloud-only (SaaS)

Meaningful only on the hosted Dify Cloud deployment; self-hosted users cannot use or benefit from them. Removing these from the self-host docs prevents confusion.

| Variable | Reason | Source |
|---|---|---|
| `ENABLE_WEBSITE_JINAREADER` | Cloud UI feature flag for Jina Reader crawler. | PR #721, commit 9248032 |
| `ENABLE_WEBSITE_FIRECRAWL` | Cloud UI feature flag for Firecrawl. | PR #721, commit 9248032 |
| `ENABLE_WEBSITE_WATERCRAWL` | Cloud UI feature flag for WaterCrawl. | PR #721, commit 9248032 |
| `NEXT_PUBLIC_ENABLE_SINGLE_DOLLAR_LATEX` | Cloud-specific UI toggle. | PR #721, commit 9248032 |
| `TIDB_API_URL` | TiDB Cloud control plane. | PR #721, commit 9248032 |
| `TIDB_IAM_API_URL` | TiDB Cloud IAM control plane. | PR #721, commit 9248032 |
| `TIDB_PRIVATE_KEY` | TiDB Cloud credential. | PR #721, commit 9248032 |
| `TIDB_PUBLIC_KEY` | TiDB Cloud credential. | PR #721, commit 9248032 |
| `TIDB_PROJECT_ID` | TiDB Cloud project reference. | PR #721, commit 9248032 |
| `TIDB_REGION` | TiDB Cloud region. | PR #721, commit 9248032 |
| `TIDB_SPEND_LIMIT` | TiDB Cloud billing guard. | PR #721, commit 9248032 |
| `TIDB_ON_QDRANT_URL` | Hybrid TiDB-Qdrant Cloud-only backend. | PR #721, commit 9248032 |
| `TIDB_ON_QDRANT_API_KEY` | Hybrid TiDB-Qdrant Cloud-only backend. | PR #721, commit 9248032 |
| `TIDB_ON_QDRANT_CLIENT_TIMEOUT` | Hybrid TiDB-Qdrant Cloud-only backend. | PR #721, commit 9248032 |
| `TIDB_ON_QDRANT_GRPC_ENABLED` | Hybrid TiDB-Qdrant Cloud-only backend. | PR #721, commit 9248032 |
| `TIDB_ON_QDRANT_GRPC_PORT` | Hybrid TiDB-Qdrant Cloud-only backend. | PR #721, commit 9248032 |
| `CREATE_TIDB_SERVICE_JOB_ENABLED` | Cloud-side TiDB pre-provisioning job. | PR #721, commit 9248032 |
| `AMPLITUDE_API_KEY` | Cloud product analytics integration. | PR #721, commit 9248032 |
| `COOKIEYES_SITE_KEY` | CookieYes consent-banner key for Dify Cloud analytics. The frontend boundary requires the system-features `deployment_edition` to be `CLOUD` plus the Cloud console host (`web/app/components/base/analytics-consent/request-boundary.ts`); dify PR #39408 explicitly excludes self-hosted deployments. Companion to `AMPLITUDE_API_KEY`. | dify #39408, 1.16.1 sync audit 2026-07-23, re-verified after #40142 2026-08-11 |
| `ENABLE_TRIAL_APP` | Cloud trial-app runs on Explore. The server gate (`api/services/recommended_app_service.py`) requires `DEPLOYMENT_EDITION=CLOUD`, so the flag is inert on self-host: `can_trial` is always false and the `/trial-apps/*` endpoints 403. | dify #39562, 1.16.1 sync audit 2026-07-27, re-verified after #40142 2026-08-11 |
| `ENABLE_EXPLORE_BANNER` | Marketing banner carousel on the Explore page. Banner content comes from the `exporle_banners` DB table (sic—the table name is misspelled upstream, `api/models/model.py`), which has no CE management UI or seed data—enabling the flag on self-host renders nothing. | dify #39543, 1.16.1 sync audit 2026-07-27 |
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile server-side secret for the email-code sign-in challenge. The only verification call site (`api/controllers/console/auth/login.py`) runs inside a `DEPLOYMENT_EDITION == CLOUD` gate, and the sign-in page renders the widget only when `deployment_edition` is `CLOUD` (`web/app/signin/components/mail-and-code-auth.tsx`)—inert on CE. | dify #40494, 1.16.2 sync 2026-08-12 |
| `TURNSTILE_ALLOWED_HOSTNAMES` | Hostname allowlist for the same Cloud-only Turnstile verification; unused on CE for the same reason as `TURNSTILE_SECRET_KEY`. | dify #40494, 1.16.2 sync 2026-08-12 |
| `TURNSTILE_SITE_KEY` | Frontend site key for the same Cloud-only Turnstile challenge; the sign-in widget renders only when `deployment_edition` is `CLOUD`. Companion to `TURNSTILE_SECRET_KEY`. | dify #40569, 1.16.2 delta sweep 2026-08-17 |
| `KNOWLEDGE_UPLOAD_FILE_SIZE_LIMIT_FOR_PAID_PLAN` | Raised knowledge-upload size cap for paid Cloud plans. `FeatureService.get_knowledge_file_size_limit` (`api/services/feature_service.py`) returns plain `UPLOAD_FILE_SIZE_LIMIT` unless `DEPLOYMENT_EDITION == CLOUD` and the tenant's billing plan is Professional or Team. | dify #39967, 1.16.2 sync 2026-08-12 |
| `TIDB_ON_QDRANT_ESTIMATED_STORAGE_LIMITS_MB` | Per-Cloud-plan storage admission limits for the TiDB-on-Qdrant backend; `api/services/vector_space_admission_service.py` exits early unless `DEPLOYMENT_EDITION == CLOUD` and the dataset's vector store is TiDB on Qdrant. Joins the existing `TIDB_ON_QDRANT_*` rows. | dify #39967, 1.16.2 sync 2026-08-12 |
| `SANDBOX_EXPIRED_RECORDS_CLEAN_GRACEFUL_PERIOD` | Grace period for Cloud's expired-subscription record cleanup. Both consumers gate on `DEPLOYMENT_EDITION == CLOUD`: `create_message_clean_policy` returns `BillingDisabledPolicy` otherwise, and `WorkflowRunCleanup._filter_free_tenants` returns every tenant without plan checks—inert on CE. Previously documented; row removed 2026-08-12. The sibling `SANDBOX_EXPIRED_RECORDS_*` vars stay documented (consumed unconditionally by the cleanup tasks). | dify #40142 follow-up, DC-186 review 2026-08-12 |

## Experimental / internal

Feature flags for unfinished or staff-only features. Not yet meant for self-hosted tuning.

| Variable | Reason | Source |
|---|---|---|
| `EXPERIMENTAL_ENABLE_VINEXT` | Switches the web container to an experimental Vite-based server (`web/docker/entrypoint.sh`). Not a supported user-facing knob. | 1.14 sync audit, 2026-04-22 |
| `KNOWLEDGE_FS_ENABLED` | Feature flag for the unreleased New Knowledge (KnowledgeFS) Console bridge. Default false; every proxy route 404s and the frontend hides the UI while off (`api/controllers/console/knowledge_fs_proxy.py`). Document the group and drop these five entries when the feature ships enabled. | dify #39158/#39314, 1.16.1 sync audit 2026-07-23 |
| `KNOWLEDGE_FS_BASE_URL` | Connection setting for the flag-off KnowledgeFS bridge; inert unless `KNOWLEDGE_FS_ENABLED=true`. | dify #39158/#39314, 1.16.1 sync audit 2026-07-23 |
| `KNOWLEDGE_FS_JWT_SECRET` | Service-JWT signing secret for the flag-off KnowledgeFS bridge; inert unless enabled. | dify #39158/#39314, 1.16.1 sync audit 2026-07-23 |
| `KNOWLEDGE_FS_TIMEOUT_SECONDS` | Request timeout for the flag-off KnowledgeFS bridge; inert unless enabled. | dify #39158/#39314, 1.16.1 sync audit 2026-07-23 |
| `KNOWLEDGE_FS_SSE_READ_TIMEOUT_SECONDS` | SSE idle-read timeout for the flag-off KnowledgeFS bridge; inert unless enabled. | dify #39158/#39314, 1.16.1 sync audit 2026-07-23 |
| `ENABLE_STEP_BY_STEP_TOUR` | Staged-rollout onboarding tour (home/studio/knowledge/integration guides). Flag-off, and eligibility additionally requires `STEP_BY_STEP_TOUR_ROLLOUT_STARTED_AT`, which is Pydantic-only (`api/services/step_by_step_tour_service.py` `is_eligible`)—the tour cannot be turned on from the docker env alone. Revisit when it ships enabled. | dify #38785/#39399, 1.16.1 sync audit 2026-07-27 |

## Enterprise-only

Switches for the Dify Enterprise control plane. Inert at their defaults on Community Edition; enabling them without the Enterprise services makes the deployment call APIs that don't exist. Enterprise deployments configure them through the EE Helm chart, not this file.

| Variable | Reason | Source |
|---|---|---|
| `RBAC_ENABLED` | Routes permission checks to the EE inner RBAC API (`rbac_permission_required` in `api/controllers/common/wraps.py` is an explicit no-op when false). On CE there is no RBAC service to answer the checks. | dify #39543, 1.16.1 sync audit 2026-07-27 |
| `ENABLE_LICENSE_EXPIRY_NOTICE` | Toggles the console's license-expiry countdown badge. `FeatureService.get_license` returns the default license model on non-ENTERPRISE editions before the var is ever read, and the badge renders only when license status is `expiring`—a status CE never has. Inert on CE. | dify #39972/#40128, 1.16.2 sync 2026-08-12 |

## Verifier false positives

The variable is documented in `environments.mdx`, but the verifier misreports it: either the example entry is commented out (reported as missing), or the example pre-fills a secret value that the docs deliberately describe instead of reproduce (reported as a default mismatch).

| Variable | Reason | Source |
|---|---|---|
| `ALIYUN_CLOUDBOX_ID` | Commented-out `#ALIYUN_CLOUDBOX_ID=your-cloudbox-id` in `docker/.env.example`; backend field exists in `api/configs/middleware/storage/aliyun_oss_storage_config.py`. | 1.14 sync audit, 2026-04-22 |
| `DIFY_AGENT_SERVER_SECRET_KEY` | Documented with a descriptive default; `.env.example` pre-fills a development key that the docs must not reproduce (no real or example secret values in docs). | feat/agent-v2 audit, 2026-07-09 |
| `DIFY_AGENT_API_TOKEN` | Documented with a descriptive default; `.env.example` pre-fills a development bearer token that the docs describe instead of reproduce (same rule as `DIFY_AGENT_SERVER_SECRET_KEY`). | dify #39544/#39622, 1.16.1 sync audit 2026-07-27 |
