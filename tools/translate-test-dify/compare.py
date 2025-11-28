#!/usr/bin/env python3
"""
Translation Comparison Utility
Usage: python compare.py <results_folder>
"""

import sys
import json
import difflib
from pathlib import Path
from datetime import datetime


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def save_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


def get_metrics(content: str) -> dict:
    lines = content.split("\n")
    return {"chars": len(content), "lines": len(lines), "words": len(content.split())}


def similarity(t1: str, t2: str) -> float:
    if not t1 or not t2:
        return 0.0
    return difflib.SequenceMatcher(None, t1, t2).ratio()


def excerpt(content: str, max_lines: int = 20) -> str:
    lines = content.split("\n")
    result = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        result += f"\n... ({len(lines) - max_lines} more lines)"
    return result


def generate_md_report(config: dict, variants: dict, translations: dict) -> str:
    lines = [
        f"# Comparison Report",
        f"**Test:** {config.get('test_name', 'Unknown')}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Variants:** {', '.join(variants.keys())}",
        "",
        "## Variants",
        "| Variant | Description |",
        "|---------|-------------|"
    ]
    for name, cfg in variants.items():
        lines.append(f"| {name} | {cfg.get('description', '')} |")
    lines.append("")

    for lang, var_contents in translations.items():
        lines.append(f"## {lang.upper()}")
        lines.append("")
        lines.append("| Variant | Chars | Lines |")
        lines.append("|---------|-------|-------|")
        for var, content in var_contents.items():
            if content:
                m = get_metrics(content)
                lines.append(f"| {var} | {m['chars']} | {m['lines']} |")
            else:
                lines.append(f"| {var} | - | - |")
        lines.append("")

        vars_list = list(var_contents.keys())
        if len(vars_list) >= 2:
            v1, v2 = vars_list[0], vars_list[1]
            sim = similarity(var_contents.get(v1, ""), var_contents.get(v2, ""))
            lines.append(f"Similarity ({v1} vs {v2}): **{sim:.1%}**")
            lines.append("")

        for var, content in var_contents.items():
            if content:
                lines.append(f"<details><summary>{var}</summary>\n\n```\n{excerpt(content, 25)}\n```\n</details>")
        lines.append("")

    return "\n".join(lines)


def generate_txt_report(config: dict, variants: dict, translations: dict) -> str:
    lines = [
        "=" * 50,
        "COMPARISON SUMMARY",
        "=" * 50,
        f"Test: {config.get('test_name', 'Unknown')}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Variants:"
    ]
    for name, cfg in variants.items():
        lines.append(f"  {name}: {cfg.get('description', '')}")
    lines.append("")

    for lang, var_contents in translations.items():
        lines.append(f"{lang.upper()}:")
        for var, content in var_contents.items():
            if content:
                m = get_metrics(content)
                lines.append(f"  {var}: {m['chars']} chars, {m['lines']} lines")
            else:
                lines.append(f"  {var}: FAILED")

        vars_list = list(var_contents.keys())
        if len(vars_list) >= 2:
            v1, v2 = vars_list[0], vars_list[1]
            sim = similarity(var_contents.get(v1, ""), var_contents.get(v2, ""))
            lines.append(f"  Similarity: {sim:.1%}")
        lines.append("")

    return "\n".join(lines)


def compare_results(result_dir: str):
    result_path = Path(result_dir)
    if not result_path.exists():
        print(f"Error: {result_dir} not found")
        sys.exit(1)

    config_path = result_path / "config.json"
    if not config_path.exists():
        print(f"Error: config.json not found")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    variants = config.get("variants", {})
    target_languages = config.get("target_languages", ["cn"])

    print(f"Comparing: {result_path.name}")
    print(f"Variants: {', '.join(variants.keys())}")

    # Find translation files in variant folders
    translations = {}  # {lang: {variant: content}}
    for lang in target_languages:
        translations[lang] = {}
        for var in variants:
            var_dir = result_path / f"variant_{var}"
            if var_dir.exists():
                # Find any *_{lang}.md file
                for f in var_dir.glob(f"*_{lang}.md"):
                    content = load_file(f)
                    translations[lang][var] = content
                    if content:
                        print(f"  Loaded: {f.relative_to(result_path)}")
                    break

    md_report = generate_md_report(config, variants, translations)
    txt_report = generate_txt_report(config, variants, translations)

    save_file(result_path / "comparison.md", md_report)
    save_file(result_path / "comparison.txt", txt_report)

    print(f"\nGenerated: comparison.md, comparison.txt")


def main():
    if len(sys.argv) < 2:
        print("Usage: python compare.py <results_folder>")
        sys.exit(1)
    compare_results(sys.argv[1])


if __name__ == "__main__":
    main()
