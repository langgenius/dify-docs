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

## Language Policy

All code and documentation in **English** (international project).
