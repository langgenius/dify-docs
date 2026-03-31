# Dify Documentation Translation System

A complete overview of the automated translation pipeline in the dify-docs repository. Covers the Python translation engine, GitHub Actions workflows, and the end-to-end flow from PR creation to translated documentation.

---

## Architecture

The system has two layers:

1. **Translation engine** (`tools/translate/`) — Python code that calls the Dify API to translate documents.
2. **Automation** (`.github/workflows/sync_docs_*.yml`) — GitHub Actions that trigger the engine automatically on PR events.

```
PR created/updated with changes in en/
        │
        ▼
   ┌─────────────┐
   │   Analyze    │  Detects what changed, generates a sync plan
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │   Route      │──→ New PR? ──→ Execute (creates translation PR)
   │              │──→ Existing translation PR? ──→ Update (incremental)
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  Cleanup     │  When original PR is closed/merged
   └─────────────┘
```

---

## Translation Engine (`tools/translate/`)

### `main.py` — Local CLI Tool

Entry point for manual, single-file translation. Useful for testing.

```bash
# Interactive mode
python main.py

# Translate a specific file
python main.py en/some-file.mdx

# With explicit API key
python main.py en/some-file.mdx app-xxx
```

- Calls Dify API in **streaming mode** (avoids HTTP 504 timeouts).
- Retry logic with exponential backoff: 30s, 60s, 120s, 240s, 300s.
- 600s timeout for streaming response.
- Concurrency limited to 2 simultaneous translations.

### `sync_and_translate.py` — Core Engine (~2,100 lines)

The main orchestrator. Handles the full translation lifecycle:

| Responsibility | How |
|:---------------|:----|
| Detect changes | Git diff between commits |
| Translate new files | Fresh translation of full content |
| Update modified files | Context-aware: sends existing translation + git diff to AI |
| Delete removed files | Removes target language files + docs.json entries |
| Sync docs.json | Inserts/removes entries at matching index positions |
| Surgical reconciliation | Auto-detects moves/renames in docs.json structure |

**Key class: `DocsSynchronizer`**

- Loads config from `config.json`.
- Translates files via Dify API with terminology database context.
- Inserts AI translation notice after frontmatter in each translated file.
- Syncs `docs.json` navigation structure across languages.

**Surgical reconciliation** detects when files are moved between sections or renamed in `docs.json`:

- Compares English section structure between base commit and HEAD.
- Detects **moves** (same file, different group path) and **renames** (deleted + added in same location).
- Applies identical operations to Chinese and Japanese using **index-based navigation** — groups are matched by position index, not by name. This works because "Nodes" in English is "节点" in Chinese and "ノード" in Japanese.

### `translate_pr.py` — PR Orchestration

Manages the translation branch lifecycle for GitHub workflow use:

- Creates `docs-sync-pr-{PR_NUMBER}` branch from `origin/main` (not from PR branch — this prevents stale state).
- Checks out only the files the PR actually changed.
- Merges `docs.json` structure: main's structure + branch's translations.
- Commits and pushes translated files.

**Stale PR handling:** When other PRs are merged to main before this PR processes, the translation branch is created from the latest main. Only this PR's changed files are checked out. This prevents reverting changes from other merged PRs.

### `pr_analyzer.py` — PR Analysis

Validates and categorizes PRs:

- Classifies PR as `source`, `translation`, or `none`.
- Rejects mixed PRs (both source and translation changes).
- Validates file paths (no directory traversal).
- Checks ignore list from config.
- Enforces file size limits (10MB).

### `json_formatter.py` — Format-Preserving JSON

Detects original JSON formatting (indent style, indent size, trailing newlines, key spacing) and rewrites `docs.json` maintaining the exact format. Prevents noisy diffs from formatting changes.

### `sync_by_path.py` — Utility for Specific Paths

Translate specific files or directories on demand:

```bash
python sync_by_path.py --file en/test.mdx --api-key app-xxx
python sync_by_path.py --dir en/guides/ --api-key app-xxx --dry-run
```

### `openapi/` — OpenAPI Translation Pipeline

Separate pipeline for OpenAPI specification files:

- `extractor.py` — Extracts translatable fields from OpenAPI JSON.
- `translator.py` — Translates field values via Dify API.
- `rehydrator.py` — Rebuilds OpenAPI JSON with translated values.

Translatable fields are defined in `config.json`: `title`, `summary`, `description`.

---

## Configuration

### `config.json` — Single Source of Truth

```json
{
  "source_language": "en",
  "target_languages": ["zh", "ja"],
  "languages": {
    "en": { "code": "en", "name": "English", "directory": "en" },
    "zh": { "code": "zh", "name": "Chinese", "directory": "zh", "translation_notice": "..." },
    "ja": { "code": "ja", "name": "Japanese", "directory": "ja", "translation_notice": "..." }
  },
  "max_files_per_run": 10,
  "max_openapi_files_per_run": 5
}
```

Also contains: versioned doc paths, ignore list, label translations, and translatable OpenAPI fields.

**Adding a new language:**

1. Add language code to `target_languages`.
2. Add language entry to `languages` with `code`, `name`, `directory`, `translation_notice`.
3. Create the directory structure.
4. Update workflow path filters in `.github/workflows/sync_docs_analyze.yml`.

### `termbase_i18n.md` — Terminology Database

A markdown file containing standardized translations for technical terms (Workflow, Agent, Knowledge Base, Node, Variable, etc.). Passed to the Dify API alongside each document to ensure consistent terminology across all translations.

### `.env` / `.env.example`

```
DIFY_API_KEY=your_dify_api_key_here
```

Required for local usage. In GitHub Actions, the key is stored as a repository secret.

---

## GitHub Actions Workflows

### `sync_docs_analyze.yml` — Analyze

**Trigger:** PR opened, updated, or reopened with changes to `en/`, `zh/`, `ja/`, or `docs.json`.

**What it does:**

1. Determines comparison range:
   - New PR: uses merge-base (where branch diverged from main).
   - Updated PR: uses `Last-Processed-Commit` from translation PR for incremental range.
2. Calls `pr_analyzer.py` to classify changes.
3. Validates file paths and sizes.
4. Generates sync plan via `SyncPlanGenerator`.
5. Uploads artifacts (1-day retention): `sync_plan.json`, `analysis.json`, `changed_files.txt`.

### `sync_docs_execute.yml` — Execute

**Trigger:** Analyze workflow succeeds (new PR, no existing translation PR).

**What it does:**

1. Downloads analysis artifacts from Analyze.
2. **Approval gate for fork PRs:**
   - Checks if PR author is OWNER, MEMBER, or COLLABORATOR.
   - If not: posts "pending approval" comment, skips translation.
   - If approved by maintainer: proceeds.
3. Calls `translate_pr.py` with PR number, head SHA, base SHA.
4. Creates `docs-sync-pr-{NUMBER}` branch with translated files.
5. Opens translation PR linking back to the source PR.
6. Comments on source PR with link to translation PR.

### `sync_docs_update.yml` — Update

**Trigger:** Analyze workflow succeeds (existing translation PR found).

**What it does:**

1. Finds existing translation PR/branch.
2. Reads `Last-Processed-Commit` from translation PR to determine incremental range.
3. Calls `translate_pr.py --is-incremental` — only translates files changed since last processing.
4. Context-aware: passes existing translation + git diff to AI for each modified file.
5. Pushes new commits to translation branch.
6. Comments on both PRs about the update.

### `sync_docs_cleanup.yml` — Cleanup

**Trigger:** Original PR closed (merged or abandoned).

**What it does:**

- If original PR was **merged**: leaves translation PR open (it can be merged independently).
- If original PR was **closed without merging**: closes the translation PR with an explanatory comment.

### `sync_docs_on_approval.yml` — Approval Gate

**Trigger:** PR review submitted with "Approved" state.

**What it does:**

1. Validates reviewer is OWNER, MEMBER, or COLLABORATOR.
2. Checks if this is a fork PR that needs the gate.
3. If translation PR already exists: posts info comment, skips.
4. Posts "Approval received" comment.
5. Re-runs the most recent Analyze workflow for this PR.
6. This triggers Execute, which now finds the approval and proceeds.

If the Analyze run is too old to re-run, it posts a comment suggesting the contributor push a small commit to trigger a fresh workflow.

---

## How a Translation Actually Happens

The Python code calls the Dify API endpoint (`https://api.dify.ai/v1/workflows/run`) in streaming mode with these inputs:

| Input | Value |
|:------|:------|
| `the_doc` | Full document content |
| `termbase` | Contents of `termbase_i18n.md` |
| `original_language` | "English" |
| `output_language1` | "Chinese" or "Japanese" |
| `the_doc_exist` | Existing translation (for modified files only) |
| `diff_original` | Git diff (for modified files only) |

The Dify workflow returns the translated content via the `output1` variable. The Python code then inserts a translation notice after the frontmatter.

**For new files:** Fresh full translation. Typically takes ~30–60 seconds per language.

**For modified files:** Context-aware update. The AI receives the current translation and only the diff, so it updates the relevant sections rather than retranslating from scratch. Typically takes ~2–3 minutes per language.

**Translation direction is always English → Chinese and English → Japanese.** Not Chinese → Japanese.

---

## End-to-End Flow

### Internal Maintainer PR

```
1. Maintainer creates PR with changes in en/
2. Analyze runs → generates sync plan
3. Execute runs → no approval gate → calls Dify API → creates translation PR
4. Translation PR (docs-sync-pr-{NUMBER}) is created automatically
5. If maintainer pushes more commits → Analyze → Update runs incrementally
6. Maintainer merges source PR → Cleanup leaves translation PR open
7. Maintainer reviews and merges translation PR
```

### External Contributor PR (Fork)

```
1. Contributor creates PR from fork with changes in en/
2. Analyze runs → generates sync plan
3. Execute runs → detects fork PR, author not trusted → posts "pending approval" comment
4. Maintainer reviews and approves the PR
5. On Approval workflow triggers → posts "Approval received" → re-runs Analyze
6. Execute runs again → finds approval → creates translation PR
7. Normal flow from here (same as internal)
```

---

## Safeguards

| Safeguard | Details |
|:----------|:--------|
| Streaming mode | Avoids HTTP 504 gateway timeouts on long translations |
| Retry with backoff | 30s, 60s, 120s, 240s, 300s intervals |
| Concurrency limit | Max 2 simultaneous translations |
| File processing limit | Max 10 docs + 5 OpenAPI files per run |
| File size limit | 10MB per file |
| Path validation | Rejects directory traversal attempts |
| Mixed PR rejection | PRs cannot contain both source and translation changes |
| Stale PR protection | Translation branch from main, only PR files checked out |
| Format preservation | JSON formatting detected and maintained |
| Approval gate | Fork PRs require OWNER/MEMBER/COLLABORATOR approval |

---

## Translation Testing Framework (`tools/translate-test-dify/`)

A/B testing framework for comparing translation quality between models or prompt variations:

```bash
cd tools/translate-test-dify
./setup.sh
source venv/bin/activate
python run_test.py spec.md
python compare.py results/<folder>/
```

Test specs define multiple API keys (different models/prompts) and test content. The framework runs the same content through each variant and generates comparison reports.

**Important:** Never commit `results/`, `mock_docs/`, or real API keys. Redact keys with `app-***` before committing.

---

## Key File Reference

| File | Purpose |
|:-----|:--------|
| `tools/translate/config.json` | Language config, processing limits, ignore list |
| `tools/translate/termbase_i18n.md` | Terminology database for consistent translations |
| `tools/translate/main.py` | Local CLI translation tool |
| `tools/translate/sync_and_translate.py` | Core translation + reconciliation engine |
| `tools/translate/translate_pr.py` | PR-level translation orchestration |
| `tools/translate/pr_analyzer.py` | PR change analysis and validation |
| `tools/translate/json_formatter.py` | Format-preserving JSON serialization |
| `tools/translate/sync_by_path.py` | Translate specific files/directories |
| `tools/translate/openapi/` | OpenAPI spec translation pipeline |
| `.github/workflows/sync_docs_analyze.yml` | PR analysis workflow |
| `.github/workflows/sync_docs_execute.yml` | Translation PR creation workflow |
| `.github/workflows/sync_docs_update.yml` | Incremental translation update workflow |
| `.github/workflows/sync_docs_cleanup.yml` | PR cleanup on close/merge |
| `.github/workflows/sync_docs_on_approval.yml` | Fork PR approval gate |
