---
title: Incremental Test - First File
description: Testing incremental translation workflow with the first file
---

# Incremental Translation - First File

This is the **first file** in our incremental translation test.

## Expected Behavior

When this PR is created:
1. Translation PR should be created
2. This file should be translated to `cn/` and `jp/`
3. Commit message should include `Last-Processed-Commit: <SHA>`

## Next Step

After the translation PR is created, we'll push a **second file** to verify incremental updates work correctly.
