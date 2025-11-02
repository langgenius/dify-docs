# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Dify documentation repository built with Mintlify, supporting multi-language documentation (English, Chinese, Japanese) with automatic translation capabilities powered by Dify AI workflows.

## Documentation Structure

### Content Organization
- **Format**: MDX files with YAML frontmatter (title, description required)
- **Languages**:
  - General docs: `en/`, `cn/`, `jp/`
  - Plugin dev docs: `plugin-dev-en/`, `plugin-dev-zh/`, `plugin-dev-ja/`
  - Versioned docs: `versions/{version}/{lang}/`
- **Configuration**: `docs.json` (navigation, theme, settings) - see [Mintlify docs.json schema](https://mintlify.com/docs.json)

### Translation System Architecture

AI-powered translation system that automatically translates English documentation to Chinese (cn) and Japanese (jp).

**Language Configuration** (`tools/translate/config.json`):
All language settings are centralized in a single config file. No code changes needed to add/modify languages.

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
      "translation_notice": "<Note>⚠️ AI translation notice...</Note>"
    }
  },
  "versioned_docs": {
    "3-2-x": {
      "en": "versions/3-2-x/en-us",
      "cn": "versions/3-2-x/zh-cn",
      "jp": "versions/3-2-x/jp"
    }
  }
}
```

**Adding a new language**: Edit `config.json` only (e.g., add Korean):
```json
{
  "target_languages": ["cn", "jp", "ko"],
  "languages": {
    "ko": {
      "code": "ko",
      "name": "Korean",
      "directory": "ko",
      "translation_notice": "<Note>...</Note>"
    }
  }
}
```

**Workflow**:
- Trigger: Push to non-main branches with `.md/.mdx` changes in source language directory
- Process: Dify API (streaming mode) with terminology database
- New files: ~30-60s per language | Modified files: ~2-3min per language (context-aware)
- Auto-inserts translation notices from config
- Incremental docs.json sync (only changed files, preserves structure)

**Key Files**: `sync_and_translate.py`, `.github/workflows/sync_docs_*.yml`, `config.json`

### Plugin Documentation Sync

Plugin development docs maintain cross-language file mappings in `plugin-dev-{lang}/sync/plugin_mappings.json`:
- Maps equivalent files across languages
- Tools: `sync_all_mdx_files_to_json.py`, `check_mapping_consistency.py`, `view_file_mappings.py`

## Development Commands

### Local Development
```bash
# Install Mintlify CLI
npm i -g mintlify

# Start local development server (from repo root where docs.json is)
mintlify dev
```

### Translation Tools

**Local translation** (for testing):
```bash
pip install -r tools/translate/requirements.txt
echo "DIFY_API_KEY=your_key" > tools/translate/.env
python tools/translate/main.py  # Interactive or pass file path
```

**Configuration**:
- Terminology: `tools/translate/termbase_i18n.md`
- Languages: `tools/translate/config.json`
- Model: Configure in Dify Studio

## Content Guidelines

See `AGENTS.md` for detailed writing standards. Key requirements:
- Every MDX file must have frontmatter with `title` and `description`
- Use relative paths for internal links (never absolute URLs)
- Test all code examples before publishing
- Second-person voice ("you")
- Language tags on all code blocks

**Git Rules**:
- NEVER use `--no-verify` or skip pre-commit hooks
- Create new branch for new work
- Commit frequently

## Navigation Structure (docs.json)

**Manual editing** (when auto-translation won't work):
- Only edit English (`en`) section when adding new pages
- Auto-translation workflow syncs to `cn`/`jp` sections automatically
- File position in navigation maintained across all languages
- Use label translations from `tools/translate/config.json` for new dropdowns

**Auto-sync behavior**:
- Added files: Fresh translation, inserted at same index position as English version
- Modified files: Context-aware translation update using existing translation + git diff
- Deleted files: Removed from all language sections, including physical files

## Testing & Debugging

**Test translation workflow**: Create test PR with branch name `test/{operation}-{scope}` (e.g., `test/add-single-doc`)
- Add: New file with docs.json entry
- Delete: Remove file and docs.json entry
- Update: Modify existing file

**Common issues**:
- **HTTP 504**: Verify `response_mode: "streaming"` in `main.py` (NOT `"blocking"`)
- **Missing output**: Check Dify workflow has output variable `output1`
- **Failed workflow**: Review Dify workflow logs for node errors

**Success log pattern**:
```
📥 Receiving streaming response...
🔄 Workflow started: {id}
🔄 Workflow finished with status: succeeded
✅ Translation completed successfully
```

## Key Paths

- `docs.json` - Navigation structure
- `tools/translate/config.json` - **Language configuration (single source of truth)**
- `tools/translate/termbase_i18n.md` - Translation terminology
- `tools/translate/sync_and_translate.py` - Core translation logic
- `.github/workflows/sync_docs_*.yml` - Auto-translation workflows
