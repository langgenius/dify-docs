# Mintlify documentation

This file provides guidance when working with the Dify documentation repository.

## Project Overview

Dify documentation repository built with Mintlify, supporting multi-language documentation (English, Chinese, Japanese) with AI-powered automatic translation via Dify workflows.

## Working relationship
- You can push back on ideas-this can lead to better documentation. Cite sources and explain your reasoning when you do so
- ALWAYS ask for clarification rather than making assumptions
- NEVER lie, guess, or make up anything

## Project context
- Format: MDX files with YAML frontmatter
- Config: docs.json for navigation, theme, settings
- Components: Mintlify components

## Documentation Structure

- **Format**: MDX files with YAML frontmatter (`title` and `description` required)
- **Languages**: `en/`, `zh/`, `ja/` (source: en)
- **Configuration**: `docs.json` (navigation structure) - [Mintlify schema](https://mintlify.com/docs.json)

## Content strategy
- Document just enough for user success - not too much, not too little
- Prioritize accuracy and usability
- Make content evergreen when possible
- Search for existing content before adding anything new. Avoid duplication unless it is done for a strategic reason
- Check existing patterns for consistency
- Start by making the smallest reasonable changes

## Frontmatter requirements for pages
- title: Clear, descriptive page title
- description: Concise summary for SEO/navigation

## Writing standards
- Second-person voice ("you")
- Prerequisites at start of procedural content
- Test all code examples before publishing
- Match style and formatting of existing pages
- Include both basic and advanced use cases
- Language tags on all code blocks
- Alt text on all images
- Relative paths for internal links

## Translation System

### Language Configuration

All language settings in `tools/translate/config.json` (single source of truth):

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
    },
    "ja": {
      "code": "ja",
      "name": "Japanese",
      "directory": "ja",
      "translation_notice": "<Note>⚠️ AI translation...</Note>"
    }
  }
}
```

**Adding new language**: Edit config.json only - add to `target_languages` and `languages` object with required fields (`code`, `name`, `directory`, `translation_notice`).

### Workflow

- **Trigger**: Push to non-main branches with `.md/.mdx` changes in `en/`
- **Process**: Dify API streaming mode with terminology database (`termbase_i18n.md`)
- **Timing**: New files ~30-60s/lang | Modified files ~2-3min/lang (context-aware with git diff)
- **Auto-operations**: Translation notices, incremental docs.json sync

### Surgical Reconciliation (Move & Rename)

**Purpose**: Detect and apply structural changes (moves, renames) from English section to zh/ja automatically.

**How it works**:
1. Compares English section between base commit and HEAD
2. Detects **moves** (same file, different `group_path`) and **renames** (deleted+added in same location)
3. Applies identical operations to zh/ja using **index-based navigation**

**Index-based navigation**:
- Groups matched by position index, not name (works across translations: "Nodes" ≠ "节点")
- Location tracked as `group_indices: [0, 1]` (parent group index 0, child index 1)
- Navigates nested structures regardless of translated group names

**Rename specifics**:
- Detects file extension (.md, .mdx) from physical file
- Preserves extension when renaming zh/ja files
- Updates docs.json entries (stored without extensions)

### Navigation Sync Behavior

**Manual editing**: Only edit English (`en`) section in docs.json - workflow syncs to zh/ja automatically.

**Auto-sync operations**:
- **Added files**: Fresh translation, inserted at same index position as English
- **Modified files**: Context-aware update using existing translation + git diff
- **Deleted files**: Removed from all language sections + physical files
- **Moved files**: Detected via `group_path` changes, zh/ja relocated using index-based navigation
- **Renamed files**: Detected when deleted+added in same location, physical files renamed with extension preserved

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

## Git workflow
- NEVER use `--no-verify` or skip hooks
- Ask how to handle uncommitted changes before starting
- Create new branch for each feature/fix
- Commit frequently throughout development
- NEVER skip or disable pre-commit hooks

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
SUCCESS: Moved zh/test-file to new location
SUCCESS: Moved ja/test-file to new location
```

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
- `.github/workflows/sync_docs_*.yml` - Auto-translation workflow triggers

## Do not
- Skip frontmatter on any MDX file
- Use absolute URLs for internal links
- Include untested code examples
- Make assumptions - always ask for clarification
