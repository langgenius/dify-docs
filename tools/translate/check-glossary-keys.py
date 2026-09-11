#!/usr/bin/env python3
"""Check that every i18n key cited in the glossary still exists in the Dify web UI strings.

Usage:
    python3 tools/translate/check-glossary-keys.py --dify <path-to-dify-clone> [--ref origin/main]
    DIFY_REPO=<path> python3 tools/translate/check-glossary-keys.py

Reads every "i18n Key" cell in writing-guides/glossary.md, resolves each key
against web/i18n/en-US/<namespace>.json at the given ref (read with
`git show`, never a checkout), and lists the keys that no longer resolve. A
glossary row whose key is dead is not evidence for the label it carries:
the label may have moved to another key, or left the product.

Prints `DEAD: <key>  (glossary.md:<line>, <section>)` per dead key and ends
with `GLOSSARY KEYS OK: <n> resolve at <ref>` or
`GLOSSARY KEYS: <n> checked, <m> dead at <ref>`. Dead rows are a report for
a glossary fix, not a failed audit, so the exit code is 0 either way unless
--strict is given.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
GLOSSARY = REPO / "writing-guides" / "glossary.md"
KEY_RE = re.compile(r"\b[a-z][A-Za-z0-9-]*(?:\.[A-Za-z0-9_-]+)+\b")


def git_show(dify: Path, ref: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(dify), "show", f"{ref}:{path}"], capture_output=True, text=True
    )
    return proc.stdout if proc.returncode == 0 else None


def resolves(data: dict, parts: list[str]) -> bool:
    """True if the dotted path exists, nested or as a flattened key. A descendant
    of the path does not count: the cited key must itself exist."""
    node = data
    for i, part in enumerate(parts):
        if isinstance(node, dict) and part in node:
            node = node[part]
            continue
        return isinstance(node, dict) and ".".join(parts[i:]) in node
    return True


def glossary_keys() -> list[tuple[int, str, str]]:
    """Yield (line number, section, key) for every key cell under an 'i18n Key' column."""
    out: list[tuple[int, str, str]] = []
    section = ""
    key_col = None
    for n, line in enumerate(GLOSSARY.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            key_col = None
            continue
        if not line.startswith("|"):
            key_col = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if key_col is None:
            if "i18n Key" in cells:
                key_col = cells.index("i18n Key")
            continue
        if all(set(c) <= set(":- ") for c in cells):
            continue
        if key_col < len(cells):
            for key in KEY_RE.findall(cells[key_col].replace("`", " ")):
                out.append((n, section, key))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dify", type=Path, default=os.environ.get("DIFY_REPO"), help="path to the dify clone (or set DIFY_REPO)")
    ap.add_argument("--ref", default="origin/main", help="ref to read the i18n files at (default origin/main)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any key is dead (default: report and exit 0)")
    args = ap.parse_args()
    if not args.dify or not (Path(args.dify) / ".git").exists():
        print("dify clone not found: pass --dify <path> or set DIFY_REPO", file=sys.stderr)
        return 2
    dify = Path(args.dify)
    sha = subprocess.run(["git", "-C", str(dify), "rev-parse", "--short=12", args.ref], capture_output=True, text=True)
    if sha.returncode != 0:
        print(f"ref {args.ref!r} not found in {dify}", file=sys.stderr)
        return 2
    short = sha.stdout.strip()
    ref_label = short if args.ref.startswith(short) else f"{args.ref} ({short})"
    pinned = subprocess.run(["git", "-C", str(dify), "rev-parse", args.ref], capture_output=True, text=True).stdout.strip()
    files: dict[str, dict | None] = {}
    dead: list[tuple[int, str, str]] = []
    keys = glossary_keys()
    for n, section, key in keys:
        ns, *parts = key.split(".")
        if ns not in files:
            # Namespaces are cited as the code writes them (appLog) or as the
            # file is named (app-log); the file is always kebab-case.
            fname = re.sub(r"(?<!^)(?=[A-Z])", "-", ns).lower()
            raw = git_show(dify, pinned, f"web/i18n/en-US/{fname}.json")
            files[ns] = json.loads(raw) if raw else None
        data = files[ns]
        if data is None or not resolves(data, parts):
            dead.append((n, section, key))
    for n, section, key in dead:
        print(f"DEAD: {key}  (glossary.md:{n}, {section})")
    if dead:
        print(f"GLOSSARY KEYS: {len(keys)} checked, {len(dead)} dead at {ref_label}")
        return 1 if args.strict else 0
    print(f"GLOSSARY KEYS OK: {len(keys)} resolve at {ref_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
