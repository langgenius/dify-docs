#!/usr/bin/env python3
"""Check for broken links in Dify documentation.

Usage:
    python3 tools/check-links.py --internal     # Check internal links (fast, no network)
    python3 tools/check-links.py --external     # Check external links (slow, network requests)
    python3 tools/check-links.py --all          # Check both
    python3 tools/check-links.py --external --report out.json   # JSON summary for CI
"""

from __future__ import annotations

import argparse
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_DIRS = ["en", "zh", "ja"]
DOCS_JSON = REPO_ROOT / "docs.json"

# Regex patterns
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r'href="([^"]+)"')
HTML_SRC_RE = re.compile(r'src="([^"]+)"')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
CUSTOM_ID_RE = re.compile(r"\{#([\w-]+)\}")
HTML_ID_RE = re.compile(r"""<a\s+[^>]*\bid=["']([\w-]+)["']""", re.IGNORECASE)
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
# Mintlify components that generate an anchor. An explicit `id` attribute
# replaces the default title-derived anchor (per the Tabs docs, `id` defaults
# to the title), so a tag is matched whole and its attributes decide.
TAB_COMPONENT_RE = re.compile(r"""<(?:Tab|Accordion)\b[^>]*>""", re.IGNORECASE)
ATTR_TITLE_RE = re.compile(r"""\btitle=["']([^"']+)["']""", re.IGNORECASE)
ATTR_ID_RE = re.compile(r"""\bid=["']([\w-]+)["']""", re.IGNORECASE)

# Per-file anchor cache: file path -> set of valid anchor slugs
_anchor_cache: dict[Path, set[str]] = {}


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
        try:
            host = urllib.parse.urlparse(url).hostname or ""
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


def resolve_internal_link(url: str, source_file: Path) -> Path | None:
    """Resolve an internal link to a file path. Returns None if unresolved.

    Absolute links (`/foo/bar`) resolve against the repo root.
    Relative links (`./foo`, `../bar`) resolve against source_file's
    parent directory.

    Returns REPO_ROOT for the bare root URL "/" (treated as valid but
    has no associated file for anchor lookup).
    """
    # Strip anchor and query
    url = url.split("#")[0].split("?")[0]

    if not url or url == "/":
        return REPO_ROOT

    if url.startswith("./") or url.startswith("../"):
        base = source_file.parent
        clean = url
    else:
        base = REPO_ROOT
        clean = url.lstrip("/")

    # Try exact path
    candidate = (base / clean).resolve()
    if candidate.exists():
        return candidate

    # Try with common extensions
    for ext in [".mdx", ".md", ".json"]:
        candidate = (base / (clean + ext)).resolve()
        if candidate.exists():
            return candidate

    # Try as directory with index
    for ext in [".mdx", ".md"]:
        candidate = (base / clean / ("index" + ext)).resolve()
        if candidate.exists():
            return candidate

    return None


def slugify(text: str) -> str:
    """Convert heading text to a Mintlify-style anchor slug.

    Lowercase, strip ASCII punctuation and markdown markers, turn
    whitespace into hyphens, collapse and trim. Non-ASCII characters (CJK
    text and full-width punctuation like "：") are kept, matching Mintlify,
    so an English heading's ASCII ":" is dropped while a zh/ja heading's
    "：" is preserved.
    """
    s = text.lower().strip()
    # Strip JSX/HTML tags but keep their inner text. Mintlify renders a
    # heading's components and includes their text in the anchor, e.g.
    # `## Switch Your Workspace <Badge color="blue">Cloud</Badge>` ->
    # `#switch-your-workspace-cloud`. Dropping the tag markup (not the
    # "Cloud" text) avoids mangling the attributes into the slug.
    s = re.sub(r"<[^>]+>", "", s)
    # Strip inline markdown formatting markers (backticks and asterisks).
    # Underscores are preserved — they appear in identifier headings like
    # `retrieval_setting` and Mintlify keeps them in the slug.
    s = re.sub(r"[`*]", "", s)
    # Strip Pandoc/kramdown custom-id syntax if embedded in heading text
    s = CUSTOM_ID_RE.sub("", s)
    # Strip ASCII punctuation only; the negated class keeps every non-ASCII
    # char (CJK text and full-width punctuation like "："), which Mintlify
    # preserves in the slug.
    s = re.sub(r"[^\w\s\u0080-\U0010ffff-]", "", s, flags=re.UNICODE)
    # Whitespace → hyphen
    s = re.sub(r"\s+", "-", s)
    # Collapse hyphens, trim
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def extract_anchors(file_path: Path) -> set[str]:
    """Extract the set of valid anchor slugs in a file (cached)."""
    if file_path in _anchor_cache:
        return _anchor_cache[file_path]

    anchors: set[str] = set()
    if not file_path.is_file():
        _anchor_cache[file_path] = anchors
        return anchors

    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        _anchor_cache[file_path] = anchors
        return anchors

    # Strip fenced code blocks so `# comment` lines aren't picked up as headings
    content = CODE_FENCE_RE.sub("", content)

    counts: dict[str, int] = {}
    for match in HEADING_RE.finditer(content):
        text = match.group(2)
        custom = CUSTOM_ID_RE.search(text)
        if custom:
            anchors.add(custom.group(1))
            continue
        slug = slugify(text)
        if not slug:
            continue
        if slug not in counts:
            counts[slug] = 1
            anchors.add(slug)
        else:
            anchors.add(f"{slug}-{counts[slug]}")
            counts[slug] += 1

    # Standalone <a id="..."> anchors
    for match in HTML_ID_RE.finditer(content):
        anchors.add(match.group(1))

    # Mintlify Tab/Accordion components also produce anchors: an explicit
    # id attribute wins; otherwise the title text is slugified.
    for match in TAB_COMPONENT_RE.finditer(content):
        tag = match.group(0)
        id_attr = ATTR_ID_RE.search(tag)
        if id_attr:
            anchors.add(id_attr.group(1))
            continue
        title_attr = ATTR_TITLE_RE.search(tag)
        if title_attr:
            slug = slugify(title_attr.group(1))
            if slug:
                anchors.add(slug)

    _anchor_cache[file_path] = anchors
    return anchors


def anchor_check_skipped(url: str, resolved: Path) -> bool:
    """Whether to skip anchor validation for a resolved target.

    Skip API reference pages (anchors derived from OpenAPI spec, not the
    file itself) and any non-MDX/MD target.
    """
    if "/api-reference/" in url:
        return True
    if resolved == REPO_ROOT:
        return True
    if resolved.suffix.lower() not in (".mdx", ".md"):
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
    """Check all internal links, anchors, and docs.json entries."""
    files = find_mdx_files()
    broken: list[tuple[str, int, str]] = []
    broken_anchors: list[tuple[str, int, str]] = []
    skipped_anchors = 0
    total = 0
    anchor_total = 0

    for f in files:
        links = extract_links(f)
        for line_num, text, url in links:
            cls = classify_link(url)

            # Same-page anchor: validate against the source file's anchors
            if cls == "anchor":
                anchor = url.lstrip("#").split("?")[0]
                if not anchor:
                    continue
                anchor_total += 1
                if anchor not in extract_anchors(f):
                    rel_path = str(f.relative_to(REPO_ROOT))
                    broken_anchors.append((rel_path, line_num, url))
                continue

            if cls != "internal":
                continue

            # API reference pages are auto-generated by Mintlify from the
            # OpenAPI specs and follow the /api-reference/<tag>/<endpoint>
            # convention without a language prefix; there is no filesystem
            # path to resolve. Skip both existence and anchor validation
            # for these (consistent with anchor_check_skipped).
            if "/api-reference/" in url:
                continue

            total += 1

            resolved = resolve_internal_link(url, f)
            rel_path = str(f.relative_to(REPO_ROOT))
            if resolved is None:
                broken.append((rel_path, line_num, url))
                continue

            # If the URL has an anchor, validate it against the resolved file
            if "#" in url:
                anchor = url.split("#", 1)[1].split("?")[0]
                if not anchor:
                    continue
                if anchor_check_skipped(url, resolved):
                    skipped_anchors += 1
                    continue
                anchor_total += 1
                if anchor not in extract_anchors(resolved):
                    broken_anchors.append((rel_path, line_num, url))

    # Check docs.json
    docs_json_issues = check_docs_json()

    # Report
    print(f"\n=== Internal Link Check ===")
    print(f"Files scanned: {len(files)}")
    print(f"Internal links checked: {total}")
    print(f"Anchors checked: {anchor_total}")
    print(f"Anchors skipped (non-MDX targets): {skipped_anchors}")
    print(f"Broken links: {len(broken)}")
    print(f"Broken anchors: {len(broken_anchors)}")
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

    if broken_anchors:
        print(f"\n--- Broken Anchors ---\n")
        by_file_a: dict[str, list] = {}
        for file_path, line_num, url in broken_anchors:
            by_file_a.setdefault(file_path, []).append((line_num, url))

        for file_path in sorted(by_file_a):
            print(f"  {file_path}:")
            for line_num, url in by_file_a[file_path]:
                print(f"    L{line_num}: {url}")

    if docs_json_issues:
        print(f"\n--- docs.json Issues ---\n")
        for source, issue in docs_json_issues:
            print(f"  {issue}")

    return len(broken) + len(broken_anchors) + len(docs_json_issues)


# Hosts the external check never requests. Placeholders never resolve;
# support.huaweicloud.com answers automated requests with a bot-verification
# page (HTTP 404) that browsers never see, so a genuine 404 there is
# indistinguishable and stays hidden — re-check those links by hand.
SKIP_HOSTS = {
    "assets-docs.dify.ai",   # CDN, blocks HEAD
    "volcengine.com",        # geo-restricted
    "twitter.com",
    "x.com",
    "support.huaweicloud.com",
    "your-dify-host",        # placeholder in the embedding page
}

# Statuses that mean "try again", not "the page is gone". GitHub answers
# bursts of HEAD requests with 503; a retry a few seconds later returns 200.
TRANSIENT_STATUSES = {408, 425, 429, 502, 503, 504}
RETRY_DELAYS = (3, 8)  # seconds between the first, second and third attempt
TRANSIENT_ERRORS = (ConnectionResetError, ConnectionAbortedError, http.client.HTTPException)
USER_AGENT = "Mozilla/5.0 (Dify-Docs-LinkChecker/1.0)"


def skip_host(url: str) -> bool:
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return False
    return any(host == d or host.endswith("." + d) for d in SKIP_HOSTS)


def fetch_status(url: str) -> tuple[str, str]:
    """Return ("ok" | "skipped" | "broken", detail) for one URL.

    HEAD first, GET when the host rejects HEAD (405). Transient statuses and
    timeouts are retried with a pause; 403 counts as skipped because many
    hosts block automated requests without the page being gone.
    """
    def attempt(method: str) -> tuple[str, str]:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
        return ("ok", "") if status < 400 else ("broken", f"HTTP {status}")

    method = "HEAD"
    last: tuple[str, str] = ("broken", "no attempt")
    attempts = 0
    while attempts <= len(RETRY_DELAYS):
        if attempts:
            time.sleep(RETRY_DELAYS[attempts - 1])
        attempts += 1
        try:
            return attempt(method)
        except urllib.error.HTTPError as e:
            if e.code == 405 and method == "HEAD":
                # The host rejects HEAD: switch to GET right away, without
                # spending an attempt or a pause on it.
                method = "GET"
                attempts -= 1
                continue
            if e.code == 403:
                return ("skipped", "HTTP 403")
            last = ("broken", f"HTTP {e.code}")
            if e.code not in TRANSIENT_STATUSES:
                return last
            method = "GET"  # some hosts only rate-limit HEAD
        except urllib.error.URLError as e:
            last = ("broken", f"URL error: {e.reason}")
            if not isinstance(e.reason, (TimeoutError, TRANSIENT_ERRORS)) and "timed out" not in str(e.reason):
                return last
        except TimeoutError as e:
            last = ("broken", f"Timeout: {e}")
        except TRANSIENT_ERRORS as e:
            # A host that hangs up on a burst instead of answering 503.
            last = ("broken", f"Error: {e}")
        except Exception as e:
            return ("broken", f"Error: {e}")
    return last


def is_transient(error: str) -> bool:
    """Whether a recorded error is the kind a later attempt may clear."""
    if error.startswith("HTTP "):
        try:
            return int(error.split()[1]) in TRANSIENT_STATUSES
        except ValueError:
            return False
    return error.startswith(("Timeout", "Error:")) or "timed out" in error


def check_external_links(report_path: Path | None = None):
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

        if skip_host(url):
            skipped += 1
            continue

        # Encode non-ASCII characters in URL path, preserving existing percent-escapes
        try:
            parsed = urllib.parse.urlparse(url)
            encoded_url = urllib.parse.urlunparse(parsed._replace(
                path=urllib.parse.quote(parsed.path, safe="/:@!$&'()*+,;=-._~%")
            ))
        except Exception:
            encoded_url = url

        verdict, detail = fetch_status(encoded_url)
        if verdict == "skipped":
            skipped += 1
        elif verdict == "broken":
            broken.append((url, detail, urls_to_check[url]))

    # Second pass: the sweep itself puts minutes between the first and this
    # attempt, which is what clears a host's rate limit when 11 seconds of
    # inline retries did not. Hard failures (404, DNS) are not re-checked.
    deferred = [(url, err, locs) for url, err, locs in broken if is_transient(err)]
    if deferred:
        print(f"  Re-checking {len(deferred)} transient failure(s) after the sweep...")
        broken = [b for b in broken if not is_transient(b[1])]
        for url, _err, locs in deferred:
            verdict, detail = fetch_status(url)
            if verdict == "skipped":
                skipped += 1
            elif verdict == "broken":
                broken.append((url, detail, locs))

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

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps({
            "checked": len(unique_urls) - skipped,
            "skipped": skipped,
            "broken": [
                {"url": url, "error": error,
                 "locations": [f"{f}:L{n}" for f, n in locations]}
                for url, error, locations in broken
            ],
        }, indent=2), encoding="utf-8")

    return len(broken)


def main():
    parser = argparse.ArgumentParser(description="Check links in Dify documentation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--internal", action="store_true", help="Check internal links only")
    group.add_argument("--external", action="store_true", help="Check external links only")
    group.add_argument("--all", action="store_true", help="Check both internal and external")
    parser.add_argument("--report", type=Path, metavar="FILE",
                        help="Write the external-link result as JSON to FILE (for CI notifications)")
    args = parser.parse_args()
    if args.report and not (args.external or args.all):
        parser.error("--report only applies to --external or --all")

    exit_code = 0

    if args.internal or args.all:
        exit_code = check_internal_links()

    if args.external or args.all:
        exit_code += check_external_links(args.report)

    sys.exit(1 if exit_code > 0 else 0)


if __name__ == "__main__":
    main()
