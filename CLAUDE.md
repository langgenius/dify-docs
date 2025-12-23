# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dify documentation repository built with Mintlify, supporting multi-language documentation (English, Chinese, Japanese) with AI-powered automatic translation via Dify workflows.

## Documentation Structure

- **Format**: MDX files with YAML frontmatter (`title` and `description` required)
- **Languages**: `en/`, `cn/`, `jp/` (source: en)
- **Configuration**: `docs.json` (navigation structure) - [Mintlify schema](https://mintlify.com/docs.json)

## Translation System

### Language Configuration

All language settings in `tools/translate/config.json` (single source of truth):

```json
{
  "source_language": "en",
  "target_languages": ["cn", "jp"],
  "languages": {
    "en": {"code": "en", "name": "English", "directory": "en"},
    "cn": {
      "code": "cn",
      "name": "Chinese",
      "directory": "cn",
      "translation_notice": "<Note>⚠️ AI translation...</Note>"
    }
  }
}
```

**Adding new language**: Edit config.json only - add to `target_languages` and `languages` object with required fields.

### Workflow

- **Trigger**: Push to non-main branches with `.md/.mdx` changes in `en/`
- **Process**: Dify API streaming mode with terminology database (`termbase_i18n.md`)
- **Timing**: New files ~30-60s/lang | Modified files ~2-3min/lang (context-aware with git diff)
- **Auto-operations**: Translation notices, incremental docs.json sync

### Surgical Reconciliation (Move & Rename)

**Purpose**: Detect and apply structural changes (moves, renames) from English section to cn/jp automatically.

**How it works**:
1. Compares English section between base commit and HEAD
2. Detects **moves** (same file, different `group_path`) and **renames** (deleted+added in same location)
3. Applies identical operations to cn/jp using **index-based navigation**

**Index-based navigation**:
- Groups matched by position index, not name (works across translations: "Nodes" ≠ "节点")
- Location tracked as `group_indices: [0, 1]` (parent group index 0, child index 1)
- Navigates nested structures regardless of translated group names

**Rename specifics**:
- Detects file extension (.md, .mdx) from physical file
- Preserves extension when renaming cn/jp files
- Updates docs.json entries (stored without extensions)

### Navigation Sync Behavior

**Manual editing**: Only edit English (`en`) section in docs.json - workflow syncs to cn/jp automatically.

**Auto-sync operations**:
- **Added files**: Fresh translation, inserted at same index position as English
- **Modified files**: Context-aware update using existing translation + git diff
- **Deleted files**: Removed from all language sections + physical files
- **Moved files**: Detected via `group_path` changes, cn/jp relocated using index-based navigation
- **Renamed files**: Detected when deleted+added in same location, physical files renamed with extension preserved

### First-Time Contributor Approval Flow

For PRs from forks by contributors who are not OWNER/MEMBER/COLLABORATOR:

1. **PR opened** → Analyze workflow runs → Execute workflow checks for approval
2. **No approval found** → Execute skips translation, posts "pending approval" comment
3. **Maintainer approves PR** → `sync_docs_on_approval.yml` triggers automatically
4. **"Approval received" comment posted** → Analyze workflow re-runs with fresh artifacts
5. **Execute workflow runs** → Finds approval → Creates translation PR

**Approval requirements**:
- Reviewer must have OWNER, MEMBER, or COLLABORATOR association
- Approval triggers immediate translation (no additional push needed)
- Each approval posts a new comment preserving the timeline

**Edge cases**:
- If translation PR already exists when approval happens → info comment posted, no re-run
- If Analyze run is too old to re-run → error comment with instructions to push a small commit
- Internal PRs (same repo, not fork) → no approval gate, auto-translates immediately

**Manual trigger**: If approval flow fails, maintainers can manually trigger via Actions → Execute Documentation Sync → Run workflow (enter PR number)

## Development Commands

```bash
# Local preview
npm i -g mintlify
mintlify dev

# Local translation testing
pip install -r tools/translate/requirements.txt
echo "DIFY_API_KEY=your_key" > tools/translate/.env
python tools/translate/main.py
```

**Configuration**:
- Terminology: `tools/translate/termbase_i18n.md`
- Languages: `tools/translate/config.json`
- Model: Configure in Dify Studio

**Git Rules**:
- NEVER use `--no-verify` or skip hooks
- Create new branch for each feature/fix
- Commit frequently with descriptive messages

## Testing & Debugging

### Test Translation Workflow

Create test PR with branch name `test/{operation}-{scope}`:

- **Add**: New file + docs.json entry
- **Delete**: Remove file + docs.json entry
- **Update**: Modify existing file content
- **Move**: Move file between groups in docs.json (e.g., Getting Started → Nodes)
- **Rename**: Rename file + update docs.json entry (tests extension preservation)

### Common Issues

**Translation failures**:
- **HTTP 504**: Verify `response_mode: "streaming"` in `main.py` (NOT `"blocking"`)
- **Missing output**: Check Dify workflow has output variable `output1`
- **Failed workflow**: Review Dify workflow logs for node errors

**Move/Rename issues**:
- **Not detected**: Check logs for "INFO: Detected X moves, Y renames" - if 0 when expecting changes, verify `group_path` actually changed between commits
- **Wrong location**: Structure mismatch between languages - verify group indices align (same nested structure)
- **File not found**: Extension detection failed - ensure file has .md or .mdx extension

**Success log pattern**:
```
INFO: Detected 1 moves, 0 renames, 0 adds, 0 deletes
INFO: Moving en/test-file from 'Dropdown > GroupA' to 'Dropdown > GroupB'
SUCCESS: Moved cn/test-file to new location
SUCCESS: Moved jp/test-file to new location
```

**Approval flow issues** (first-time contributors):
- **Translation not starting after approval**: Check Actions tab for `Retrigger Sync on Approval` workflow status
- **"Could not automatically start translation"**: Analyze run too old - push a small commit to trigger fresh workflow
- **Approval from non-maintainer**: Only OWNER/MEMBER/COLLABORATOR approvals unlock the gate
- **Multiple "pending approval" comments**: Normal - each commit triggers Execute which posts if no approval found

## Translation A/B Testing

For comparing translation quality between models or prompt variations:

```bash
cd tools/translate-test-dify
./setup.sh
source venv/bin/activate
python run_test.py <spec.md>
python compare.py results/<folder>/
```

**Important**:
- Never commit `results/`, `mock_docs/`, or real API keys
- Always redact keys with `app-***` before committing
- See `tools/translate-test-dify/README.md` for details

## Key Paths

- `docs.json` - Navigation structure
- `tools/translate/config.json` - Language configuration (single source of truth)
- `tools/translate/termbase_i18n.md` - Translation terminology database
- `tools/translate/sync_and_translate.py` - Core translation + surgical reconciliation logic
- `tools/translate-test-dify/` - Translation A/B testing framework
- `.github/workflows/sync_docs_analyze.yml` - Analyzes PR changes, uploads artifacts
- `.github/workflows/sync_docs_execute.yml` - Creates translation PRs (triggered by Analyze)
- `.github/workflows/sync_docs_update.yml` - Updates existing translation PRs
- `.github/workflows/sync_docs_cleanup.yml` - Cleans up sync PRs when original PR closes
- `.github/workflows/sync_docs_on_approval.yml` - Retriggers translation on maintainer approval
