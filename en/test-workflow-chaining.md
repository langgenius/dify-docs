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
