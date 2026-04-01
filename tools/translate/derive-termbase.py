#!/usr/bin/env python3
"""Derive termbase_i18n.md from writing-guides/glossary.md.

Reads the rich glossary (with Notes and i18n Key columns),
strips them, and writes the lean termbase for the translation pipeline.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GLOSSARY_PATH = REPO_ROOT / "writing-guides" / "glossary.md"
TERMBASE_PATH = Path(__file__).resolve().parent / "termbase_i18n.md"

STATIC_FOOTER = """
## General Guidelines

Technical accuracy, English identifiers preserved, markdown formatting
maintained, professional tone.
"""

# H2 sections to skip entirely (non-term content)
SKIP_SECTIONS: list[str] = []


def parse_glossary(glossary_text: str) -> list[tuple[str, list[tuple[str, list[list[str]]]]]]:
    """Parse glossary into top-level sections of (h2_heading, [(h3_heading, rows)]).

    Each row is [English, Chinese, Japanese] with Notes/i18n Key stripped.
    """
    top_sections = []
    current_h2 = None
    current_h3 = None
    current_rows = []
    h3_groups = []
    header_seen = False

    def flush_h3():
        nonlocal current_h3, current_rows
        if current_h3 and current_rows:
            h3_groups.append((current_h3, current_rows))
        current_h3 = None
        current_rows = []

    def flush_h2():
        nonlocal current_h2, h3_groups
        flush_h3()
        if current_h2 and current_h2 not in SKIP_SECTIONS and h3_groups:
            top_sections.append((current_h2, list(h3_groups)))
        current_h2 = None
        h3_groups = []

    for line in glossary_text.splitlines():
        # Detect H2 headings
        h2_match = re.match(r"^## (.+)", line)
        if h2_match and not line.startswith("### "):
            flush_h2()
            current_h2 = h2_match.group(1).strip()
            header_seen = False
            continue

        # Detect H3 headings
        h3_match = re.match(r"^### (.+)", line)
        if h3_match:
            flush_h3()
            current_h3 = h3_match.group(1).strip()
            header_seen = False
            continue

        # Skip sections we don't want
        if current_h2 and current_h2 in SKIP_SECTIONS:
            continue

        # Detect table rows
        if line.startswith("|"):
            if not header_seen:
                if re.match(r"\|[\s:]-", line):
                    header_seen = True
                continue
            if re.match(r"\|[\s:]-", line):
                continue

            cells = [c.strip() for c in line.split("|")[1:-1]]

            if len(cells) >= 3:
                english = cells[0]
                chinese = cells[1]
                japanese = cells[2]

                # Strip (UI) suffix from column values
                english = re.sub(r"\s*\(UI\)\s*$", "", english)

                current_rows.append([english, chinese, japanese])

    flush_h2()
    return top_sections


def generate_termbase(top_sections: list[tuple[str, list[tuple[str, list[list[str]]]]]]) -> str:
    """Generate lean termbase markdown from parsed sections."""
    lines = ["# Terminology Database", ""]

    for h2_heading, h3_groups in top_sections:
        lines.append(f"## {h2_heading}")
        lines.append("")
        for h3_heading, rows in h3_groups:
            lines.append(f"### {h3_heading}")
            lines.append("")
            lines.append("| English | Chinese | Japanese |")
            lines.append("|:--------|:--------|:---------|")
            for english, chinese, japanese in rows:
                lines.append(f"| {english} | {chinese} | {japanese} |")
            lines.append("")

    lines.append(STATIC_FOOTER.strip())
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Derive termbase_i18n.md from glossary.md"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if termbase is in sync (exit 1 if not). Does not write.",
    )
    args = parser.parse_args()

    if not GLOSSARY_PATH.exists():
        print(f"Error: glossary not found at {GLOSSARY_PATH}", file=sys.stderr)
        sys.exit(1)

    glossary_text = GLOSSARY_PATH.read_text(encoding="utf-8")
    top_sections = parse_glossary(glossary_text)
    generated = generate_termbase(top_sections)

    if args.check:
        if not TERMBASE_PATH.exists():
            print(f"Error: termbase not found at {TERMBASE_PATH}", file=sys.stderr)
            sys.exit(1)
        current = TERMBASE_PATH.read_text(encoding="utf-8")
        if current != generated:
            print(
                "termbase_i18n.md is out of sync with glossary.md.\n"
                "Run `python3 tools/translate/derive-termbase.py` and commit the result.",
                file=sys.stderr,
            )
            sys.exit(1)
        print("termbase_i18n.md is in sync with glossary.md.")
        sys.exit(0)

    TERMBASE_PATH.write_text(generated, encoding="utf-8")
    print(f"Generated {TERMBASE_PATH}")


if __name__ == "__main__":
    main()
