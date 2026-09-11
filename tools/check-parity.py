#!/usr/bin/env python3
"""Check that a page's zh and ja twins carry the same structure as the English page.

Usage:
    python3 tools/check-parity.py --base origin/main <changed en/zh/ja pages...>
    python3 tools/check-parity.py --all

Each page is split into sections at its headings, and every section is
compared with the same section of the zh and ja pages: heading level, then
the paragraphs, list items, fenced code blocks, table rows, the sequence of
component names, and explicit anchor ids. Heading text is not compared,
because it is translated. The translation disclaimer at the top of a zh or ja
page is skipped. A zh or ja path is checked through its English twin.

With --base, the same comparison runs on the files at that ref, and only
mismatches that are not already there count: the corpus carries older drift,
and a round is judged on what it introduced. Pre-existing mismatches are
listed under their own heading. The ref is verified first; a page absent at
the ref is new, and all of its mismatches count. A page absent in all three
languages is a deletion and reports nothing; a translation that outlives its
English page is reported.

Ends with `PARITY OK: <n> pages` (exit 0) or `PARITY ISSUES: <n>` (exit 1).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # overridden by --repo
LANGS = ("en", "zh", "ja")
TWINS = ("zh", "ja")
DISCLAIMER = ("本文档由 AI 自动翻译", "このドキュメントは AI によって自動翻訳")

FM_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(.*?)\s*$")
CUSTOM_ID_RE = re.compile(r"\{#([\w-]+)\}")
TAG_ID_RE = re.compile(r"""\bid=["']([\w-]+)["']""")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}")
COMPONENT_RE = re.compile(r"^\s*<([A-Z][A-Za-z]*)\b")
INLINE_TAG_RE = re.compile(r"<([A-Z][A-Za-z]*)\b")
COMMENT_RE = re.compile(r"^\s*\{/\*.*\*/\}\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


class Section:
    def __init__(self, level: int, title: str = "") -> None:
        self.level = level
        self.title = title
        self.counts: Counter = Counter()
        self.components: list[str] = []
        self.anchors: list[str] = []


def sections_of(text: str) -> list[Section]:
    """Split a page into sections; the preamble is level 0."""
    text = FM_RE.sub("", text, count=1)
    out = [Section(0)]
    in_fence = in_para = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        cur = out[-1]
        if FENCE_RE.match(line):
            if not in_fence:
                cur.counts["code blocks"] += 1
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
            out.append(Section(len(h.group(1)), h.group(2)))
            m = CUSTOM_ID_RE.search(h.group(2))
            if m:
                out[-1].anchors.append(m.group(1))
            out[-1].components.extend(INLINE_TAG_RE.findall(h.group(2)))
            in_para = False
            continue
        if TABLE_ROW_RE.match(line):
            if not TABLE_SEP_RE.match(line):
                cur.counts["table rows"] += 1
            cur.components.extend(INLINE_TAG_RE.findall(line))
            cur.anchors.extend(TAG_ID_RE.findall(line))
            in_para = False
            continue
        if COMPONENT_RE.match(line):
            cur.components.extend(INLINE_TAG_RE.findall(line))
            cur.anchors.extend(TAG_ID_RE.findall(line))
            in_para = False
            continue
        cur.components.extend(INLINE_TAG_RE.findall(line))
        if line.lstrip().startswith("<"):
            cur.anchors.extend(TAG_ID_RE.findall(line))
            in_para = False
            continue
        if LIST_RE.match(line):
            cur.counts["list items"] += 1
            in_para = False
            continue
        cur.anchors.extend(CUSTOM_ID_RE.findall(line))
        if not in_para:
            cur.counts["paragraphs"] += 1
            in_para = True
    return out


def labels_for(en: list[Section]) -> list[str]:
    """Name each section by its English heading, so a mismatch keeps its name when
    a section is inserted or removed elsewhere on the page; the base comparison
    subtracts by these names. Repeated headings get a counter."""
    seen: Counter = Counter()
    out = []
    for sec in en:
        if sec.level == 0:
            out.append("preamble")
            continue
        title = re.sub(r"\s+", " ", CUSTOM_ID_RE.sub("", INLINE_TAG_RE.sub("", sec.title))).strip()[:60]
        seen[title] += 1
        out.append(f'section "{title}"' + (f" ({seen[title]})" if seen[title] > 1 else ""))
    return out


def compare_texts(rel_en: str, en_text: str, twins: dict[str, str | None]) -> list[str]:
    """Mismatch lines for one English page against its twins' texts (None = missing)."""
    issues: list[str] = []
    en = sections_of(en_text)
    names = labels_for(en)
    rest = rel_en.split("/", 1)[1]
    for lang in TWINS:
        trel = f"{lang}/{rest}"
        text = twins.get(lang)
        if text is None:
            issues.append(f"{trel}: missing twin")
            continue
        tw = sections_of(text)
        if len(tw) != len(en):
            issues.append(
                f"{trel}: {len(tw) - 1} headings, en {len(en) - 1}"
                " (sections compared in order as far as they align)"
            )
        for i, (a, b) in enumerate(zip(en, tw)):
            where = names[i]
            if a.level != b.level:
                issues.append(f"{trel}: {where}: heading level {b.level}, en {a.level}")
            for kind in sorted(set(a.counts) | set(b.counts)):
                if a.counts[kind] != b.counts[kind]:
                    issues.append(f"{trel}: {where}: {kind} {b.counts[kind]}, en {a.counts[kind]}")
            if a.components != b.components:
                issues.append(
                    f"{trel}: {where}: components {','.join(b.components) or 'none'}, "
                    f"en {','.join(a.components) or 'none'}"
                )
            if sorted(a.anchors) != sorted(b.anchors):
                issues.append(
                    f"{trel}: {where}: anchor ids {','.join(sorted(b.anchors)) or 'none'}, "
                    f"en {','.join(sorted(a.anchors)) or 'none'}"
                )
    return issues


def read_working(rel: str) -> str | None:
    p = REPO / rel
    return p.read_text(encoding="utf-8") if p.is_file() else None


def read_at(ref: str, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{ref}:{rel}"], capture_output=True, text=True
    )
    return proc.stdout if proc.returncode == 0 else None


def to_en(rel: str) -> str | None:
    parts = rel.split("/", 1)
    if len(parts) != 2 or parts[0] not in LANGS:
        return None
    return f"en/{parts[1]}"


def main() -> int:
    global REPO
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages", nargs="*", help="changed pages under en/, zh/, or ja/, relative to the repo root")
    ap.add_argument("--all", action="store_true", help="check every page under en/")
    ap.add_argument("--base", help="git ref; mismatches already present there are listed, not counted")
    ap.add_argument("--repo", type=Path, default=REPO, help="repo root (default: the script's repo)")
    args = ap.parse_args()
    REPO = args.repo.resolve()
    if args.base:
        ok = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--verify", "--quiet", f"{args.base}^{{commit}}"],
            capture_output=True, text=True,
        )
        if ok.returncode != 0:
            print(f"base ref not found in {REPO}: {args.base}", file=sys.stderr)
            return 2
        args.base = ok.stdout.strip()

    if args.all:
        pages = sorted(str(p.relative_to(REPO)) for p in (REPO / "en").rglob("*.md*"))
    else:
        pages = []
        for raw in args.pages:
            given = Path(raw)
            full = (given if given.is_absolute() else REPO / given).resolve()
            try:
                rel = str(full.relative_to(REPO))
            except ValueError:
                rel = ""
            en = to_en(rel)
            if not en or Path(en).suffix not in (".mdx", ".md"):
                print(f"not a page under en/, zh/, or ja/: {raw}", file=sys.stderr)
                return 2
            if en not in pages:
                pages.append(en)
    if not pages:
        print("no pages given; pass paths under en/, zh/, or ja/, or --all", file=sys.stderr)
        return 2

    new: list[str] = []
    old: list[str] = []
    for en in pages:
        en_text = read_working(en)
        rest = en.split("/", 1)[1]
        if en_text is None:
            # A page removed in all three languages is a synchronized deletion,
            # which the changed-file list will hand us; only a surviving twin
            # is a fault.
            for lang in TWINS:
                if read_working(f"{lang}/{rest}") is not None:
                    new.append(f"{lang}/{rest}: translation without an English page")
            continue
        now = compare_texts(en, en_text, {lang: read_working(f"{lang}/{rest}") for lang in TWINS})
        if args.base:
            base_en = read_at(args.base, en)
            before = (
                compare_texts(en, base_en, {lang: read_at(args.base, f"{lang}/{rest}") for lang in TWINS})
                if base_en is not None else []
            )
            seen = Counter(before)
            for line in now:
                if seen[line]:
                    seen[line] -= 1
                    old.append(line)
                else:
                    new.append(line)
        else:
            new.extend(now)

    for line in new:
        print(line)
    if old:
        print(f"pre-existing at {args.base[:12]} ({len(old)}):")
        for line in old:
            print(f"  {line}")
    if new:
        print(f"PARITY ISSUES: {len(new)}")
        return 1
    print(f"PARITY OK: {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
