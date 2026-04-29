# Intentionally Ignored Environment Variables

Variables listed here appear in Dify's `docker/.env.example` or `api/configs/`, but are deliberately **not** documented in `en/self-host/configuration/environments.mdx`. The verifier script reads this file and skips matching variables when comparing docs against `.env.example`.

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

## Experimental / internal

Feature flags for unfinished or staff-only features. Not yet meant for self-hosted tuning.

| Variable | Reason | Source |
|---|---|---|
| `EXPERIMENTAL_ENABLE_VINEXT` | Switches the web container to an experimental Vite-based server (`web/docker/entrypoint.sh`). Not a supported user-facing knob. | 1.14 sync audit, 2026-04-22 |

## Verifier false positives

The variable is documented in `environments.mdx` and supported by the backend, but the verifier reports it as missing from `.env.example` because the example entry is commented out.

| Variable | Reason | Source |
|---|---|---|
| `ALIYUN_CLOUDBOX_ID` | Commented-out `#ALIYUN_CLOUDBOX_ID=your-cloudbox-id` in `docker/.env.example`; backend field exists in `api/configs/middleware/storage/aliyun_oss_storage_config.py`. | 1.14 sync audit, 2026-04-22 |
