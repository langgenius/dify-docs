---
title: Fresh Incremental Test - First File
description: Testing incremental translation with fixed workflow - first file
---

# Fresh Incremental Translation Test - First File

This is the **first file** in our fresh incremental translation test with the English file removal fix.

## Expected Behavior

When this PR is created:
1. Translation PR should be created
2. This file should be translated to `cn/` and `jp/`
3. Translation commit should ONLY contain:
   - `cn/test-fresh-incremental-first.md`
   - `jp/test-fresh-incremental-first.md`
   - `docs.json`
4. Translation commit should NOT contain any `en/` files
5. Commit message should include `Last-Processed-Commit: <SHA>`

## Next Step

After the translation PR is created, we'll push a **second file** to verify incremental updates work correctly.
