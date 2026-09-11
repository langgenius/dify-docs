#!/usr/bin/env python3
"""Check that a page's zh and ja twins carry the same structure as the English page.

Usage:
    python3 tools/check-parity.py en/cloud/use-dify/build/agent.mdx ...
    python3 tools/check-parity.py --all

Each English page is split into sections at its headings, and every section
is compared with the same section of the zh and ja pages: heading level,
then the number of paragraphs, list items, fenced code blocks, tables,
Mintlify components, tabs, and explicit anchor ids. Heading text is not
compared, because it is translated. The translation disclaimer at the top of
a zh or ja page is skipped.

Prints one line per mismatch and ends with `PARITY OK: <n> pages` (exit 0) or
`PARITY ISSUES: <n>` (exit 1).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # overridden by --repo
TWINS = ("zh", "ja")
DISCLAIMER = ("本文档由 AI 自动翻译", "このドキュメントは AI によって自動翻訳")

FM_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CUSTOM_ID_RE = re.compile(r"\{#([\w-]+)\}")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}")
COMPONENT_RE = re.compile(r"^\s*<([A-Z][A-Za-z]*)\b")
TAB_RE = re.compile(r"^\s*<Tab\b")
COMMENT_RE = re.compile(r"^\s*\{/\*.*\*/\}\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def section_counts(text: str) -> list[tuple[int, Counter]]:
    """Return one (heading level, counts) per section; the preamble is level 0."""
    text = FM_RE.sub("", text, count=1)
    sections: list[tuple[int, Counter]] = [(0, Counter())]
    in_fence = False
    in_para = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        c = sections[-1][1]
        if FENCE_RE.match(line):
            if not in_fence:
                c["code blocks"] += 1
            in_fence = not in_fence
            in_para = False
            continue
        if in_fence:
            continue
        if not line.strip():
            in_para = False
            continue
        if any(m in line for m in DISCLAIMER) or COMMENT_RE.match(line):
            continue
        h = HEADING_RE.match(line)
        if h:
            sections.append((len(h.group(1)), Counter()))
            if CUSTOM_ID_RE.search(h.group(2)):
                sections[-1][1]["anchor ids"] += 1
            in_para = False
            continue
        if TABLE_ROW_RE.match(line):
            if not TABLE_SEP_RE.match(line):
                c["table rows"] += 1
            in_para = False
            continue
        if COMPONENT_RE.match(line):
            if TAB_RE.match(line):
                c["tabs"] += 1
            else:
                c["components"] += 1
            in_para = False
            continue
        if line.lstrip().startswith("</"):
            in_para = False
            continue
        if LIST_RE.match(line):
            c["list items"] += 1
            in_para = False
            continue
        if CUSTOM_ID_RE.search(line):
            c["anchor ids"] += 1
        if not in_para:
            c["paragraphs"] += 1
            in_para = True
    return sections


def compare(en_path: Path) -> list[str]:
    rel = en_path.relative_to(REPO)
    issues: list[str] = []
    en_sections = section_counts(en_path.read_text(encoding="utf-8"))
    for lang in TWINS:
        twin = REPO / lang / Path(*rel.parts[1:])
        if not twin.is_file():
            issues.append(f"{lang}/{'/'.join(rel.parts[1:])}: missing twin")
            continue
        tw_sections = section_counts(twin.read_text(encoding="utf-8"))
        trel = twin.relative_to(REPO)
        if len(tw_sections) != len(en_sections):
            issues.append(
                f"{trel}: {len(tw_sections) - 1} headings, en {len(en_sections) - 1}"
                " (sections not compared until the headings match)"
            )
            continue
        for i, ((en_lvl, en_c), (tw_lvl, tw_c)) in enumerate(zip(en_sections, tw_sections)):
            where = "preamble" if i == 0 else f"section {i}"
            if en_lvl != tw_lvl:
                issues.append(f"{trel}: {where}: heading level {tw_lvl}, en {en_lvl}")
            for kind in sorted(set(en_c) | set(tw_c)):
                if en_c[kind] != tw_c[kind]:
                    issues.append(f"{trel}: {where}: {kind} {tw_c[kind]}, en {en_c[kind]}")
    return issues


def main() -> int:
    global REPO
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="English pages (en/...mdx), relative to the repo root")
    ap.add_argument("--all", action="store_true", help="check every page under en/")
    ap.add_argument("--repo", type=Path, default=REPO, help="repo root (default: the script's repo)")
    args = ap.parse_args()
    REPO = args.repo.resolve()
    if args.all:
        pages = sorted((REPO / "en").rglob("*.mdx"))
    else:
        pages = [(REPO / p).resolve() for p in args.pages]
    pages = [p for p in pages if p.is_file() and p.suffix == ".mdx" and (REPO / "en") in p.parents]
    if not pages:
        print("no English pages given; pass en/...mdx paths or --all", file=sys.stderr)
        return 2
    issues: list[str] = []
    for p in pages:
        issues.extend(compare(p))
    for line in issues:
        print(line)
    if issues:
        print(f"PARITY ISSUES: {len(issues)}")
        return 1
    print(f"PARITY OK: {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
