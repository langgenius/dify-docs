---
title: Workflow Chaining Test
description: Testing secure workflow chaining between analyze and update workflows
---

# Workflow Chaining Test

This file tests the new secure workflow chaining implementation.

## Test Scenario

Testing that the update workflow:
1. Waits for analyze workflow to complete
2. Downloads validated artifacts from analyze workflow
3. Uses pre-validated sync_plan.json
4. Enforces all security checks from analyze workflow

## Expected Behavior

- Analyze workflow validates inputs with security checks
- Update workflow only runs after analyze succeeds
- Security validations cannot be bypassed
- Incremental updates work correctly with chained workflows

## Incremental Update Test

This section was added to test the workflow chaining on incremental updates.

### Security Validation Chain

When this change is pushed:
1. **Analyze Workflow** runs first (read-only permissions)
   - Validates file paths (no `../` traversal)
   - Checks file count limit (max 50 files)
   - Checks file size limit (10MB per file)
   - Creates validated `sync_plan.json` artifact
   - Uploads artifact for update workflow

2. **Update Workflow** waits for analyze completion
   - Triggered by `workflow_run` event
   - Downloads validated artifact from analyze workflow
   - Loads pre-validated `sync_plan.json`
   - Proceeds only if analyze succeeded
   - Uses validated inputs (no re-analysis)

### Security Guarantees

✅ All security checks enforced (cannot be bypassed)
✅ Proper separation: validation (read-only) → execution (write)
✅ Artifacts ensure validated inputs are used
✅ Defense in depth with sequential workflow execution
