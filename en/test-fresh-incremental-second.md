---
title: Fresh Incremental Test - Second File
description: Testing incremental translation with fixed workflow - second file
---

# Fresh Incremental Translation Test - Second File

This is the **second file** in our fresh incremental translation test.

## Expected Behavior

When this commit is pushed:
1. Translation PR #86 should be **updated** (not force-pushed)
2. Translation PR should have **2 commits total**
3. Second commit should include new `Last-Processed-Commit: <SHA>`
4. Second commit should ONLY contain:
   - `cn/test-fresh-incremental-second.md`
   - `jp/test-fresh-incremental-second.md`
   - `docs.json` (if navigation changed)
5. Second commit should NOT contain any `en/` files
6. First file should NOT be re-translated

## Success Criteria

✅ Translation PR has 2 commits (not 1)
✅ Both commits have different SHAs
✅ Git history is preserved (no force-push)
✅ No English source files in any commit
