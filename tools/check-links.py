#!/usr/bin/env python3
"""Check for broken links in Dify documentation.

Usage:
    python3 tools/check-links.py --internal     # Check internal links (fast, no network)
    python3 tools/check-links.py --external     # Check external links (slow, network requests)
    python3 tools/check-links.py --all          # Check both
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_DIRS = ["en", "zh", "ja"]
DOCS_JSON = REPO_ROOT / "docs.json"

# Regex patterns
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r'href="([^"]+)"')
HTML_SRC_RE = re.compile(r'src="([^"]+)"')


def find_mdx_files() -> list[Path]:
    """Find all .md and .mdx files in doc directories."""
    files = []
    for d in DOC_DIRS:
        doc_dir = REPO_ROOT / d
        if doc_dir.exists():
            files.extend(doc_dir.rglob("*.md"))
            files.extend(doc_dir.rglob("*.mdx"))
    return sorted(files)


def extract_links(file_path: Path) -> list[tuple[int, str, str]]:
    """Extract all links from a file. Returns [(line_num, link_text, url)]."""
    links = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return links

    for i, line in enumerate(content.splitlines(), 1):
        # Markdown links [text](url)
        for match in MD_LINK_RE.finditer(line):
            text, url = match.group(1), match.group(2)
            links.append((i, text, url))
        # HTML href="url"
        for match in HTML_HREF_RE.finditer(line):
            url = match.group(1)
            if url not in [m.group(2) for m in MD_LINK_RE.finditer(line)]:
                links.append((i, "(html href)", url))
        # HTML src="url" (images)
        for match in HTML_SRC_RE.finditer(line):
            url = match.group(1)
            links.append((i, "(html src)", url))

    return links


def classify_link(url: str) -> str:
    """Classify a link as internal, external, anchor, or skip."""
    if url.startswith(("http://", "https://")):
        # Skip localhost/loopback URLs
        from urllib.parse import urlparse
        try:
            host = urlparse(url).hostname or ""
            if host in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
                return "skip"
        except Exception:
            pass
        return "external"
    if url.startswith("#"):
        return "anchor"
    if url.startswith("mailto:") or url.startswith("tel:"):
        return "skip"
    # Skip markdown syntax examples and placeholder URLs
    if url.startswith("image_url") or url.startswith("localhost") or url.startswith("127.0.0.1"):
        return "skip"
    # Flag relative paths as internal (they should be converted to absolute)
    if url.startswith("../") or url.startswith("./"):
        return "internal"
    if url.startswith("/") or not url.startswith((".", "{", "<")):
        return "internal"
    return "skip"


def resolve_internal_link(url: str, source_file: Path) -> bool:
    """Check if an internal link resolves to an existing file."""
    # Strip anchor
    url = url.split("#")[0]
    # Strip query params
    url = url.split("?")[0]

    if not url or url == "/":
        return True

    # Remove leading slash
    clean = url.lstrip("/")

    # Try exact path
    if (REPO_ROOT / clean).exists():
        return True

    # Try with common extensions
    for ext in [".mdx", ".md", ".json"]:
        if (REPO_ROOT / (clean + ext)).exists():
            return True

    # Try as directory with index
    for ext in [".mdx", ".md"]:
        if (REPO_ROOT / clean / ("index" + ext)).exists():
            return True

    return False


def check_docs_json() -> list[tuple[str, str]]:
    """Check that docs.json entries point to real files."""
    issues = []
    if not DOCS_JSON.exists():
        return [("docs.json", "File not found")]

    try:
        data = json.loads(DOCS_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return [("docs.json", f"Parse error: {e}")]

    def check_pages(pages: list, context: str = ""):
        if not isinstance(pages, list):
            return
        for item in pages:
            if isinstance(item, str):
                # Direct page reference
                path = item
                found = False
                for ext in ["", ".mdx", ".md"]:
                    if (REPO_ROOT / (path + ext)).exists():
                        found = True
                        break
                if not found:
                    issues.append(("docs.json", f"{context}Entry '{path}' — file not found"))
            elif isinstance(item, dict):
                # Group with pages
                group_name = item.get("group", "(unnamed)")
                sub_pages = item.get("pages", [])
                check_pages(sub_pages, f"{context}{group_name} > ")

    # Traverse the docs.json structure
    # Supports: navigation.languages[].versions[].dropdowns[].pages (Mintlify v2)
    # Also supports: tabs[].pages (legacy)
    nav = data.get("navigation", {})
    languages = nav.get("languages", [])
    if languages:
        for lang in languages:
            lang_code = lang.get("language", "?")
            for version in lang.get("versions", []):
                ver_name = version.get("version", "?")
                for dropdown in version.get("dropdowns", []):
                    dd_name = dropdown.get("dropdown", "(unnamed)")
                    check_pages(
                        dropdown.get("pages", []),
                        f"[{lang_code}/{ver_name}/{dd_name}] ",
                    )
    elif "tabs" in data:
        # Legacy flat structure
        for tab in data["tabs"]:
            tab_name = tab.get("tab", "(unnamed tab)")
            check_pages(tab.get("pages", []), f"[{tab_name}] ")

    return issues


def check_internal_links():
    """Check all internal links and docs.json entries."""
    files = find_mdx_files()
    broken = []
    total = 0

    for f in files:
        links = extract_links(f)
        for line_num, text, url in links:
            if classify_link(url) != "internal":
                continue
            total += 1
            if not resolve_internal_link(url, f):
                rel_path = f.relative_to(REPO_ROOT)
                broken.append((str(rel_path), line_num, url))

    # Check docs.json
    docs_json_issues = check_docs_json()

    # Report
    print(f"\n=== Internal Link Check ===")
    print(f"Files scanned: {len(files)}")
    print(f"Internal links checked: {total}")
    print(f"Broken links: {len(broken)}")
    print(f"docs.json issues: {len(docs_json_issues)}")

    if broken:
        print(f"\n--- Broken Internal Links ---\n")
        # Group by file
        by_file: dict[str, list] = {}
        for file_path, line_num, url in broken:
            by_file.setdefault(file_path, []).append((line_num, url))

        for file_path in sorted(by_file):
            print(f"  {file_path}:")
            for line_num, url in by_file[file_path]:
                print(f"    L{line_num}: {url}")

    if docs_json_issues:
        print(f"\n--- docs.json Issues ---\n")
        for source, issue in docs_json_issues:
            print(f"  {issue}")

    return len(broken) + len(docs_json_issues)


def check_external_links():
    """Check all external links for 404s."""
    files = find_mdx_files()
    urls_to_check: dict[str, list[tuple[str, int]]] = {}  # url -> [(file, line)]
    total = 0

    for f in files:
        links = extract_links(f)
        for line_num, text, url in links:
            if classify_link(url) != "external":
                continue
            total += 1
            rel_path = str(f.relative_to(REPO_ROOT))
            urls_to_check.setdefault(url, []).append((rel_path, line_num))

    unique_urls = list(urls_to_check.keys())
    print(f"\n=== External Link Check ===")
    print(f"Files scanned: {len(files)}")
    print(f"External links found: {total}")
    print(f"Unique URLs to check: {len(unique_urls)}")
    print(f"Checking...")

    broken = []
    skipped = 0

    for i, url in enumerate(unique_urls):
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{len(unique_urls)}")

        # Skip asset CDN URLs (usually reliable, many of them)
        if "assets-docs.dify.ai" in url:
            skipped += 1
            continue

        try:
            req = urllib.request.Request(
                url,
                method="HEAD",
                headers={"User-Agent": "Mozilla/5.0 (Dify-Docs-LinkChecker/1.0)"}
            )
            resp = urllib.request.urlopen(req, timeout=10)
            status = resp.getcode()
            if status >= 400:
                broken.append((url, f"HTTP {status}", urls_to_check[url]))
        except urllib.error.HTTPError as e:
            # Some sites block HEAD, try GET for 405
            if e.code == 405:
                try:
                    req = urllib.request.Request(
                        url,
                        method="GET",
                        headers={"User-Agent": "Mozilla/5.0 (Dify-Docs-LinkChecker/1.0)"}
                    )
                    resp = urllib.request.urlopen(req, timeout=10)
                except Exception:
                    broken.append((url, f"HTTP {e.code}", urls_to_check[url]))
            elif e.code == 403:
                # Many sites block automated requests — don't report as broken
                skipped += 1
            else:
                broken.append((url, f"HTTP {e.code}", urls_to_check[url]))
        except urllib.error.URLError as e:
            broken.append((url, f"URL error: {e.reason}", urls_to_check[url]))
        except Exception as e:
            broken.append((url, f"Error: {e}", urls_to_check[url]))

    print(f"\nBroken external links: {len(broken)}")
    print(f"Skipped (CDN/403): {skipped}")

    if broken:
        print(f"\n--- Broken External Links ---\n")
        for url, error, locations in broken:
            print(f"  {error}: {url}")
            for file_path, line_num in locations[:3]:
                print(f"    - {file_path}:L{line_num}")
            if len(locations) > 3:
                print(f"    ... and {len(locations) - 3} more")

    return len(broken)


def main():
    parser = argparse.ArgumentParser(description="Check links in Dify documentation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--internal", action="store_true", help="Check internal links only")
    group.add_argument("--external", action="store_true", help="Check external links only")
    group.add_argument("--all", action="store_true", help="Check both internal and external")
    args = parser.parse_args()

    exit_code = 0

    if args.internal or args.all:
        exit_code = check_internal_links()

    if args.external or args.all:
        exit_code += check_external_links()

    sys.exit(1 if exit_code > 0 else 0)


if __name__ == "__main__":
    main()
