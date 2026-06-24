#!/usr/bin/env python3
"""
Verify Dify environment variable documentation against .env.example sources.

Parses one or more env-example files plus the docs MDX, extracts variable names
and defaults, and reports discrepancies.

After Dify PR #31586, env vars were split across `docker/.env.example` and
`docker/envs/**/*.env.example`. The verifier accepts either a single file or
a directory; passing a directory globs `**/*.env.example` recursively.

Usage:
    # Verify mode: docs vs current .env.example
    python3 verify-env-docs.py --env-example PATH [--env-example PATH ...] --docs PATH

    # Release diff mode: which vars were added/removed/changed between two refs, and
    # which NEW ones are still undocumented. Run this every release sync.
    python3 verify-env-docs.py --compare-rev OLD NEW --repo /path/to/dify [--docs PATH]

`--env-example` may be repeated and may point to either a file or a directory.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_env_lines(lines) -> dict[str, str]:
    """Parse env-example text lines and return {VARIABLE_NAME: default_value}.

    Only uncommented `VAR=value` lines are captured (commented `#VAR=...` defaults
    cannot be parsed reliably, matching the verifier's documented behavior).
    """
    variables = {}
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue
        # Match VARIABLE=value (value can be empty)
        match = re.match(r"^([A-Z][A-Z0-9_]+)=(.*)", line)
        if match:
            variables[match.group(1)] = match.group(2).strip()
    return variables


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a single env-example file and return {VARIABLE_NAME: default_value}."""
    with open(path, encoding="utf-8") as f:
        return parse_env_lines(f)


# Env files for deployment modes that intentionally diverge from the standard
# full-stack Docker deployment that environments.mdx documents. middleware.env.example
# targets the "middleware-only / app-on-host" dev compose, where services are reached
# via host.docker.internal instead of their compose service names. Its values must not
# be treated as authoritative (they cause false-positive default mismatches, e.g.
# PLUGIN_DAEMON_URL, ENDPOINT_URL_TEMPLATE, LOGSTORE_DUAL_WRITE_ENABLED), so it is loaded
# at LOWEST precedence: its variable names still count for the missing/extra checks
# (some vars, e.g. SSRF_SANDBOX_PROXY_*, are only listed there), but every other source
# overrides its values.
LOW_PRECEDENCE_ENV_BASENAMES = {"middleware.env.example"}


def collect_env_files(sources: list[str]) -> list[Path]:
    """Resolve each source (file or directory) into env-example files, in merge
    precedence order (lowest first, highest last, since callers merge later-wins).

    Order: LOW_PRECEDENCE_ENV_BASENAMES first (present for name checks, never
    authoritative for values), then the other directory-globbed files, then
    explicitly-listed files last — so the canonical `docker/.env.example` has the
    final say on conflicts (it is what a Docker Compose user actually gets).
    """
    low_precedence: list[Path] = []
    dir_files: list[Path] = []
    explicit_files: list[Path] = []
    seen: set[Path] = set()
    for source in sources:
        p = Path(source)
        if not p.exists():
            print(f"ERROR: env source not found: {source}", file=sys.stderr)
            sys.exit(1)
        if p.is_dir():
            # `*.env.example` plus the bare `.env.example` filename.
            for pattern in ("*.env.example", ".env.example"):
                for f in sorted(p.rglob(pattern)):
                    if f in seen:
                        continue
                    seen.add(f)
                    if f.name in LOW_PRECEDENCE_ENV_BASENAMES:
                        low_precedence.append(f)
                    else:
                        dir_files.append(f)
        elif p not in seen:
            explicit_files.append(p)
            seen.add(p)
    return low_precedence + dir_files + explicit_files


def parse_env_example(sources: list[str]) -> tuple[dict[str, str], list[Path]]:
    """Parse all env-example files reachable from the given sources.

    Files are merged later-wins. collect_env_files orders them so directory-globbed
    files come first and explicitly-listed files (the canonical docker/.env.example)
    come last, giving the primary file the final say on conflicts. Returns the merged
    variable map plus the list of files actually parsed (for diagnostics).
    """
    files = collect_env_files(sources)
    merged: dict[str, str] = {}
    for f in files:
        merged.update(parse_env_file(f))
    return merged, files


def parse_ignored_vars(path: str) -> set[str]:
    """Parse the ignored-vars markdown file and return the set of ignored names.

    Table rows beginning with `| \`VARIABLE_NAME\` |` register an ignore entry.
    The header row `| Variable | ...` is skipped naturally because it isn't backticked.
    """
    ignored: set[str] = set()
    if not Path(path).exists():
        return ignored
    with open(path, encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\|\s*`([A-Z][A-Z0-9_]+)`\s*\|", line)
            if match:
                ignored.add(match.group(1))
    return ignored


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


DEFAULT_IGNORED_PATH = Path(__file__).parent / "ignored-vars.md"


def _env_example_paths_at_ref(repo: str, ref: str) -> list[str]:
    """List docker/ *.env.example paths tracked at a git ref, in merge-precedence
    order (lowest first, canonical docker/.env.example last)."""
    out = subprocess.run(
        ["git", "-C", repo, "ls-tree", "-r", "--name-only", ref, "--", "docker/"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    files = [p for p in out if p.endswith(".env.example")]

    def precedence(path: str) -> tuple[int, str]:
        if Path(path).name in LOW_PRECEDENCE_ENV_BASENAMES:
            return (0, path)  # lowest precedence (e.g. middleware.env.example)
        if path == "docker/.env.example":
            return (2, path)  # canonical file has the final say
        return (1, path)

    return sorted(files, key=precedence)


def env_vars_at_ref(repo: str, ref: str) -> dict[str, str]:
    """Return the merged {VAR: default} from all docker/ *.env.example files at a git ref."""
    merged: dict[str, str] = {}
    for path in _env_example_paths_at_ref(repo, ref):
        content = subprocess.run(
            ["git", "-C", repo, "show", f"{ref}:{path}"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        merged.update(parse_env_lines(content))
    return merged


def run_compare_rev(repo: str, old_ref: str, new_ref: str, docs_path, ignored_path: str) -> int:
    """Report env vars added/removed/default-changed between two git refs.

    The release safety net: per-PR detection misses untagged PRs, so diff the whole
    .env.example var set between the previous release and the target, and flag NEW
    vars that are still undocumented and not intentionally ignored.
    """
    try:
        old_vars = env_vars_at_ref(repo, old_ref)
        new_vars = env_vars_at_ref(repo, new_ref)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: git failed: {e.stderr.strip() or e}", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print("ERROR: git not found on PATH", file=sys.stderr)
        return 2

    added = sorted(set(new_vars) - set(old_vars))
    removed = sorted(set(old_vars) - set(new_vars))
    changed = sorted(
        n for n in (set(new_vars) & set(old_vars))
        if normalize(old_vars[n]) != normalize(new_vars[n])
    )

    print(f"=== ENV VAR DIFF {old_ref}..{new_ref} (uncommented .env.example vars) ===")
    print(f"NEW ({len(added)}):")
    for n in added:
        print(f"  + {n}={new_vars[n]}")
    print(f"REMOVED ({len(removed)}):")
    for n in removed:
        print(f"  - {n} (was {old_vars[n]!r})")
    print(f"DEFAULT CHANGED ({len(changed)}):")
    for n in changed:
        print(f"  ~ {n}: {old_vars[n]!r} -> {new_vars[n]!r}")

    if docs_path:
        doc_vars = parse_mdx_docs(docs_path)
        ignored = parse_ignored_vars(ignored_path)
        gaps = [n for n in added if n not in doc_vars and n not in ignored]
        print()
        print(f"=== NEW vars NOT documented and NOT in ignored-vars ({len(gaps)}) — TRIAGE ===")
        for n in gaps:
            print(f"  {n}={new_vars[n]}")
        print("(Document each, or add to ignored-vars.md with a reason. Never leave a")
        print(" new-this-release var as silent backlog.)")
    else:
        print("\n(Pass --docs to also flag which NEW vars are still undocumented.)")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Verify env var documentation against .env.example"
    )
    parser.add_argument(
        "--env-example",
        action="append",
        help=(
            "Path to a .env.example file or to a directory containing them. "
            "May be repeated. When given a directory, the verifier globs "
            "**/*.env.example recursively. Pass both `docker/.env.example` and "
            "`docker/envs/` to capture the post-PR-#31586 layout."
        ),
    )
    parser.add_argument(
        "--docs",
        help="Path to MDX documentation file (e.g., en/self-host/deploy/configuration/environments.mdx)",
    )
    parser.add_argument(
        "--compare-rev",
        nargs=2,
        metavar=("OLD", "NEW"),
        help=(
            "Release safety net: two git refs (previous release, target). Reports env "
            "vars added/removed/default-changed in .env.example between them, and (with "
            "--docs) which NEW vars are still undocumented. Requires --repo."
        ),
    )
    parser.add_argument(
        "--repo",
        help="Path to the Dify code repo (required with --compare-rev).",
    )
    parser.add_argument(
        "--ignored",
        default=str(DEFAULT_IGNORED_PATH),
        help=f"Path to ignored-vars markdown file (default: {DEFAULT_IGNORED_PATH}).",
    )
    args = parser.parse_args()

    if args.compare_rev:
        if not args.repo:
            parser.error("--repo is required with --compare-rev")
        old_ref, new_ref = args.compare_rev
        return run_compare_rev(args.repo, old_ref, new_ref, args.docs, args.ignored)

    if not args.env_example or not args.docs:
        parser.error("--env-example and --docs are required (or use --compare-rev --repo)")

    if not Path(args.docs).exists():
        print(f"ERROR: Documentation not found at {args.docs}")
        sys.exit(1)

    env_vars, env_files = parse_env_example(args.env_example)
    doc_vars = parse_mdx_docs(args.docs)
    ignored = parse_ignored_vars(args.ignored)

    print(f"Parsed {len(env_vars)} variables from {len(env_files)} env-example file(s):")
    for f in env_files:
        print(f"  - {f}")
    print(f"Parsed {len(doc_vars)} variables from documentation")
    print(f"Loaded {len(ignored)} ignored variables from {args.ignored}")
    print()

    # --- Check 1: Variables in .env.example but missing from docs ---
    missing_from_docs = sorted(
        (set(env_vars.keys()) - set(doc_vars.keys())) - ignored
    )
    if missing_from_docs:
        print(f"=== MISSING FROM DOCS ({len(missing_from_docs)}) ===")
        for name in missing_from_docs:
            print(f"  {name}={env_vars[name]}")
        print()

    # --- Check 2: Variables in docs but not in any env-example source ---
    extra_in_docs = sorted(
        (set(doc_vars.keys()) - set(env_vars.keys())) - ignored
    )
    if extra_in_docs:
        print(f"=== IN DOCS BUT NOT IN ANY .env.example ({len(extra_in_docs)}) ===")
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
