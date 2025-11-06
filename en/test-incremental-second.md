---
title: Incremental Test - Second File
description: Testing incremental translation workflow with the second file
---

# Incremental Translation - Second File

This is the **second file** in our incremental translation test.

## Expected Behavior

When this commit is pushed:
1. Translation PR should be **updated** (not force-pushed)
2. Translation PR should have **2 commits total**
3. Second commit message should include the new `Last-Processed-Commit: <SHA>`
4. Only this file should be translated (first file should NOT be re-translated)

## Success Criteria

✅ Translation PR has 2 commits (not 1)
✅ Both commits have different SHAs
✅ Git history is preserved (no force-push)
