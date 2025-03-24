#!/bin/bash

# Execute the language check script
if bash ./lang-check/git-diff.sh; then
    # Check passed, submission executed
    git commit -m "$*"
else
    # Check failed
    echo "Language check failed, commit aborted"
    exit 1
fi