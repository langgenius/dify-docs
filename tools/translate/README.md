# Automatic Document Translation

Multi-language document auto-translation system based on GitHub Actions and Dify AI, supporting English, Chinese, and Japanese.

## How It Works

### Workflow Triggers

1. **Execute Workflow** (New PRs):
   - Triggers when PR is opened with `.md/.mdx` changes in `en/` directory
   - Creates translation PR with fresh translations for all changed files
   - Translation PR tracks the source PR

2. **Update Workflow** (Incremental Changes):
   - Triggers on new commits to source PR
   - Updates existing translation PR with incremental changes
   - **Context-aware translation**: Uses existing translation + git diff for modified files
   - **Surgical reconciliation**: Detects and applies move/rename operations

### Translation Operations

- ✅ **New files**: Fresh translation to all target languages
- ✅ **Modified files**: Context-aware update using existing translation + git diff
- ✅ **Deleted files**: Removed from all language sections + physical files
- ✅ **Moved files**: Detected via `group_path` changes, applied with index-based navigation
- ✅ **Renamed files**: Detected when deleted+added in same location, preserves file extensions

### Surgical Reconciliation

Automatically detects structural changes in `docs.json`:

- **Move detection**: Same file, different `group_path` → moves zh/ja files to same nested location using index-based navigation
- **Rename detection**: File deleted+added in same location → renames zh/ja files with extension preserved
- **Index-based navigation**: Groups matched by position, not name (works across translations: "Nodes" ≠ "节点")

## System Features

- 🌐 **Multi-language Support**: Configuration-based language mapping (`config.json`)
- 📚 **Terminology Consistency**: Built-in professional terminology database (`termbase_i18n.md`)
- 🔄 **Incremental Updates**: Context-aware translation using git diff for modified files
- 🎯 **Surgical Reconciliation**: Automatic detection and application of move/rename operations
- 🛡️ **Fault Tolerance**: Retry mechanism with exponential backoff
- ⚡ **Efficient Processing**: Only processes changed files since last commit

## Language Directories

- **General docs**: `en/` (source) → `zh/`, `ja/` (targets)
- **Plugin dev docs**: `plugin-dev-en/` → `plugin-dev-zh/`, `plugin-dev-ja/`
- **Versioned docs**: `versions/{version}/en-us/` → `versions/{version}/zh-zh/`, `versions/{version}/ja/`

Configuration in `tools/translate/config.json`.

## Usage

### For Document Writers

1. Create branch from main
2. Add/modify/delete files in `en/` directory
3. Update `docs.json` if adding/removing/moving/renaming files
4. Push to branch → workflow creates translation PR automatically
5. Make additional changes → workflow updates translation PR incrementally
6. Review and merge translation PR

### Testing Moves & Renames

**Move**: Edit `docs.json` to move file between groups (e.g., Getting Started → Nodes)
```json
// Before: en/test-file in "Getting Started" group
// After: en/test-file in "Nodes" group
```

**Rename**: Rename file + update `docs.json` entry
```bash
git mv en/old-name.md en/new-name.md
# Update docs.json: "en/old-name" → "en/new-name"
```

Logs will show:
```
INFO: Detected 1 moves, 0 renames, 0 adds, 0 deletes
INFO: Moving en/test-file from 'Dropdown > GroupA' to 'Dropdown > GroupB'
SUCCESS: Moved zh/test-file to new location
SUCCESS: Moved ja/test-file to new location
```

## Configuration

### Language Settings

Edit `tools/translate/config.json`:

```json
{
  "source_language": "en",
  "target_languages": ["zh", "ja"],
  "languages": {
    "en": {"code": "en", "name": "English", "directory": "en"},
    "zh": {
      "code": "zh",
      "name": "Chinese",
      "directory": "zh",
      "translation_notice": "<Note>⚠️ AI translation...</Note>"
    }
  }
}
```

### Terminology Database

Edit `tools/translate/termbase_i18n.md` to update professional terminology translations.

### Translation Model

Configure in Dify Studio - adjust prompts or change base models.

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r tools/translate/requirements.txt

# Configure API key
echo "DIFY_API_KEY=your_key" > tools/translate/.env
```

### Run Translation

```bash
# Interactive mode
python tools/translate/main.py

# Specify file
python tools/translate/main.py path/to/file.mdx
```

### Test Surgical Reconciliation

```bash
# Test locally with git refs
cd tools/translate
python -c "
from sync_and_translate import DocsSynchronizer
import asyncio
import os

api_key = os.getenv('DIFY_API_KEY')
sync = DocsSynchronizer(api_key)

# Test with specific commits
logs = sync.reconcile_docs_json_structural_changes('base_sha', 'head_sha')
for log in logs:
    print(log)
"
```

## Troubleshooting

### Translation Issues

- **HTTP 504**: Verify `response_mode: "streaming"` in `main.py`
- **Missing output**: Check Dify workflow has output variable `output1`
- **Failed workflow**: Review Dify workflow logs for node errors

### Move/Rename Issues

- **Not detected**: Check logs for "INFO: Detected X moves, Y renames" - verify `group_path` changed
- **Wrong location**: Structure mismatch between languages - verify group indices align
- **File not found**: Ensure file has .md or .mdx extension

## Key Files

- `config.json` - Language configuration (single source of truth)
- `termbase_i18n.md` - Translation terminology database
- `sync_and_translate.py` - Core translation + surgical reconciliation logic
- `main.py` - Local translation tool with Dify API integration
- `translate_pr.py` - PR workflow orchestration
- `.github/workflows/sync_docs_execute.yml` - Execute workflow (new PRs)
- `.github/workflows/sync_docs_update.yml` - Update workflow (incremental changes)

## Technical Details

- Concurrent translation limited to 2 tasks for API stability
- Supports `.md` and `.mdx` file formats
- Based on Dify API streaming mode
- Index-based navigation for language-independent group matching
- Extension detection and preservation for rename operations
