#!/usr/bin/env python3
"""
Verify Dify environment variable documentation against .env.example.

Parses both files, extracts variable names and defaults, and reports
discrepancies between what the documentation says and what .env.example defines.

Usage:
    python3 verify-env-docs.py [--env-example PATH] [--docs PATH]

Both arguments are required (no defaults).
"""

import argparse
import re
import sys
from pathlib import Path


def parse_env_example(path: str) -> dict[str, str]:
    """Parse .env.example and return {VARIABLE_NAME: default_value}."""
    variables = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Match VARIABLE=value (value can be empty)
            match = re.match(r"^([A-Z][A-Z0-9_]+)=(.*)", line)
            if match:
                name = match.group(1)
                value = match.group(2).strip()
                variables[name] = value
    return variables


def parse_mdx_docs(path: str) -> dict[str, str]:
    """Parse MDX documentation and extract documented defaults.

    Handles two formats:
    1. Table rows: | `VARIABLE` | `value` | description |
    2. Heading + Default line:
       ### VARIABLE
       Default: `value`
    """
    variables = {}
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Format 1: Table rows — | `VAR_NAME` | `default` | description |
        table_match = re.match(
            r"^\|\s*`([A-Z][A-Z0-9_]+)`\s*\|\s*(.*?)\s*\|", line
        )
        if table_match:
            name = table_match.group(1)
            default_cell = table_match.group(2).strip()
            # Extract value from backticks if present
            backtick_match = re.match(r"^`(.*)`$", default_cell)
            if backtick_match:
                variables[name] = backtick_match.group(1)
            elif default_cell.startswith("("):
                # (empty), (empty; falls back to...), (auto-generated), etc.
                variables[name] = ""
            else:
                variables[name] = default_cell
            i += 1
            continue

        # Format 2: ### VARIABLE_NAME followed by Default: `value`
        heading_match = re.match(r"^###\s+([A-Z][A-Z0-9_]+)\s*$", line)
        if heading_match:
            name = heading_match.group(1)
            # Look ahead for "Default:" line within next 5 lines
            for j in range(1, 6):
                if i + j >= len(lines):
                    break
                next_line = lines[i + j].strip()
                if not next_line:
                    continue
                default_match = re.match(r"^Default:\s*(.+)", next_line)
                if default_match:
                    raw = default_match.group(1).strip()
                    # Extract from backticks
                    bt = re.match(r"^`(.*)`", raw)
                    if bt:
                        variables[name] = bt.group(1)
                    elif raw.startswith("("):
                        variables[name] = ""
                    else:
                        variables[name] = raw
                    break
                # Stop if we hit content that's not the default line
                if next_line.startswith("#") or next_line.startswith("|"):
                    break
            i += 1
            continue

        i += 1

    return variables


PLACEHOLDER_PATTERNS = [
    "your-", "your_", "YOUR-", "YOUR_",
    "xxx", "difyai", "dify-sandbox",
    "sk-9f73s", "lYkiYYT6", "QaHbTe77",
    "testaccount", "testpassword", "difypassword",
    "gp-test.", "gp-ab",
    "instance-name",
    "WVF5YTha",
]

PLACEHOLDER_EXACT = {
    "dify", "password", "admin",
}

PLACEHOLDER_CONTAINS = [
    "your-object-storage",
    "xxx-vector",
]


def is_placeholder(value: str) -> bool:
    """Check if a value is a placeholder (not a real default)."""
    v = value.strip()
    if v in PLACEHOLDER_EXACT:
        return True
    for pattern in PLACEHOLDER_PATTERNS:
        if v.startswith(pattern):
            return True
    for pattern in PLACEHOLDER_CONTAINS:
        if pattern in v:
            return True
    return False


def normalize(value: str) -> str:
    """Normalize a value for comparison."""
    v = value.strip().strip('"').strip("'")
    # Normalize boolean representations
    if v.lower() in ("true", "yes", "1"):
        return "true"
    if v.lower() in ("false", "no", "0"):
        return "false"
    # Normalize empty
    if v in ("null", "None", "none", ""):
        return ""
    # Treat placeholder values as empty (they're not real defaults)
    if is_placeholder(v):
        return ""
    return v


def main():
    parser = argparse.ArgumentParser(
        description="Verify env var documentation against .env.example"
    )
    parser.add_argument(
        "--env-example",
        required=True,
        help="Path to .env.example file (e.g., /path/to/dify/docker/.env.example)",
    )
    parser.add_argument(
        "--docs",
        required=True,
        help="Path to MDX documentation file (e.g., en/self-host/configuration/environments.mdx)",
    )
    args = parser.parse_args()

    if not Path(args.env_example).exists():
        print(f"ERROR: .env.example not found at {args.env_example}")
        sys.exit(1)
    if not Path(args.docs).exists():
        print(f"ERROR: Documentation not found at {args.docs}")
        sys.exit(1)

    env_vars = parse_env_example(args.env_example)
    doc_vars = parse_mdx_docs(args.docs)

    print(f"Parsed {len(env_vars)} variables from .env.example")
    print(f"Parsed {len(doc_vars)} variables from documentation")
    print()

    # --- Check 1: Variables in .env.example but missing from docs ---
    missing_from_docs = sorted(set(env_vars.keys()) - set(doc_vars.keys()))
    if missing_from_docs:
        print(f"=== MISSING FROM DOCS ({len(missing_from_docs)}) ===")
        for name in missing_from_docs:
            print(f"  {name}={env_vars[name]}")
        print()

    # --- Check 2: Variables in docs but not in .env.example ---
    extra_in_docs = sorted(set(doc_vars.keys()) - set(env_vars.keys()))
    if extra_in_docs:
        print(f"=== IN DOCS BUT NOT IN .env.example ({len(extra_in_docs)}) ===")
        for name in extra_in_docs:
            print(f"  {name} (doc default: {doc_vars[name]!r})")
        print()

    # --- Check 3: Default value mismatches ---
    common = sorted(set(env_vars.keys()) & set(doc_vars.keys()))
    mismatches = []
    for name in common:
        env_val = normalize(env_vars[name])
        doc_val = normalize(doc_vars[name])
        if env_val != doc_val:
            mismatches.append((name, env_vars[name], doc_vars[name]))

    if mismatches:
        print(f"=== DEFAULT MISMATCHES ({len(mismatches)}) ===")
        for name, env_val, doc_val in mismatches:
            print(f"  {name}:")
            print(f"    .env.example: {env_val!r}")
            print(f"    documentation: {doc_val!r}")
        print()

    # --- Summary ---
    total_issues = len(missing_from_docs) + len(extra_in_docs) + len(mismatches)
    if total_issues == 0:
        print("ALL CHECKS PASSED — documentation matches .env.example")
    else:
        print(f"TOTAL ISSUES: {total_issues}")
        print(f"  Missing from docs: {len(missing_from_docs)}")
        print(f"  Extra in docs: {len(extra_in_docs)}")
        print(f"  Default mismatches: {len(mismatches)}")

    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
