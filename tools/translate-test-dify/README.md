# Translation Testing Framework

A/B testing for Dify translation workflows. Primary user: **Claude Code**.

## Important

- **DO NOT commit test results** - `results/` is gitignored
- **DO NOT commit real API keys** - always redact with `app-***` before committing
- **DO NOT commit mock_docs/** - temporary files copied for testing

## Quick Start

```bash
# Setup (first time)
./setup.sh
source venv/bin/activate

# Run test
python run_test.py <spec.md>

# Compare results
python compare.py results/<folder>/
```

## Test Spec Format

```markdown
# Test Title

## keys
app-xxx
Description A

app-yyy
Description B

## test_content
(Inline content - Claude Code generates this for each test)

# OR reference existing file:
## test_file
en/guides/workflow/some-doc.md
```

## Workflow

1. User describes test scenario
2. Claude Code creates spec with `## test_content` tailored to the issue
3. Run: `source venv/bin/activate && python run_test.py spec.md`
4. Analyze: `python compare.py results/<folder>/`
5. **Redact API keys** with `app-***` before committing

## Example: Punctuation Test

```markdown
# Punctuation Test

## keys
app-***
Sonnet

app-***
Opus

## test_content
---
title: Test Doc
---

# Test

Sentence with commas, colons: semicolons; and more.

- Item one, comma
- Item two; semicolon
```

See `example-model-comparison.md` for a complete example.

## Files

| File | Purpose |
|------|---------|
| run_test.py | Test runner |
| compare.py | Generate comparison reports |
| example-model-comparison.md | Example test spec |
| results/ | Output (gitignored) |
| mock_docs/ | Temp test files (gitignored) |

## Testing Prompt Changes

Prompts are stored in `../translate/prompt/` (1.md, 2.md, 3.md).

### Prompt-to-Workflow Mapping

| File | Dify Workflow Node | Trigger |
|------|-------------------|---------|
| `1.md` | Template (1) | New doc (`the_doc` only) |
| `2.md` | Template (2) | Update (`the_doc` + `the_doc_exist`) |
| `3.md` | Template (3) | Update + diff (all three params) |

### Test All Scenarios

```bash
# Scenario 1: New document
cat > test.md << 'EOF'
# Test
## keys
app-YOUR_KEY
test
## target_languages
zh
## test_file
en/use-dify/getting-started/introduction.mdx
EOF
python run_test.py test.md

# Scenario 2: Add existing_file section
# Scenario 3: Add diff_content section

# Verify URL mapping
grep -o 'href="[^"]*"' results/*/variant_A/*.md | head -10
```

### Key Rule: URL Localization

All prompts must map internal links:
- `/en/` → `/zh/` or `/ja/`
- `plugin-dev-en/` → `plugin-dev-zh/` or `plugin-dev-ja/`

### API Parameters

```bash
curl -H "Authorization: Bearer $KEY" https://api.dify.ai/v1/parameters
```

Required: `original_language`, `output_language1`, `the_doc`, `termbase`
Optional: `the_doc_exist` (→ prompt 2), `diff_original` (→ prompt 3)

## Language Policy

All code and documentation in **English** (international project).
