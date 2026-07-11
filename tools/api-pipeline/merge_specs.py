#!/usr/bin/env python3
"""Service API docs.json wiring and coverage checks.

Since Phase 1 shipped, {lang}/api-reference/openapi_service.json is the
hand-maintained spec of record for each language: edit it directly. The
Phase-1 merge machinery (build/relink, resolutions.json, overrides/) that
produced it from the five per-app-type source specs is retired; recover it
from git history when Phase 2 rebuilds the spec from R&D's generated spec
plus docs-owned overlays.

Modes:
  wire            Regenerate the docs.json API menus (all languages ×
                  products) and the API redirects from the rendered specs,
                  nav_labels.json, and memberships.json.
  check-coverage  Fail if an app-type overview page misses a link to a
                  supported operation, per memberships.json.

Usage:
  export DOCS="$(git rev-parse --show-toplevel)"
  python3 "$DOCS/tools/api-pipeline/merge_specs.py" wire --lang en zh ja
  python3 "$DOCS/tools/api-pipeline/merge_specs.py" check-coverage --lang en zh ja

Env:
  DOCS  docs repo root (default: two levels above this file)
"""

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(os.environ.get("DOCS", Path(__file__).resolve().parents[2]))
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}


def iter_ops(spec: dict):
    """Yield (path, method, op) for every operation in a spec."""
    for path, item in spec.get("paths", {}).items():
        for method, op in item.items():
            if method in HTTP_METHODS:
                yield path, method, op


def load_memberships() -> dict:
    with open(Path(__file__).resolve().parent / "memberships.json", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Wire mode: docs.json navigation, redirects, and overview MDX pages
# ---------------------------------------------------------------------------


def load_nav_labels() -> dict:
    with open(Path(__file__).resolve().parent / "nav_labels.json", encoding="utf-8") as f:
        return json.load(f)


def nav_groups_for(lang: str, labels: dict) -> list:
    """The API menu's three groups: Guides, App APIs, Knowledge API.

    Guides lists the hand-maintained overview pages (guides_order). The two
    reference tiers group the merged spec's operations into tag subgroups,
    ordered and labeled per nav_labels.json, with per-tag op ordering
    overrides from op_order.
    """
    memberships = load_memberships()
    with open(REPO / lang / "api-reference" / "openapi_service.json", encoding="utf-8") as _fh:
        merged = json.load(_fh)
    with open(REPO / "en" / "api-reference" / "openapi_service.json", encoding="utf-8") as _fh:
        en_merged = json.load(_fh)
    if len(merged["tags"]) != len(en_merged["tags"]):
        raise ValueError(
            f"nav_groups_for({lang}): tag count mismatch: "
            f"{len(merged['tags'])} vs en {len(en_merged['tags'])}"
        )
    # en tag -> this language's tag label, via index alignment of the tags arrays
    tag_map = {e["name"]: l["name"] for e, l in zip(en_merged["tags"], merged["tags"])}
    ops_by_en_tag = {}
    mismatches = []
    for (path, method, op), (en_path, en_method, en_op) in zip(iter_ops(merged), iter_ops(en_merged)):
        if (path, method) != (en_path, en_method):
            mismatches.append(((path, method), (en_path, en_method)))
            continue
        ops_by_en_tag.setdefault(en_op["tags"][0], []).append(f"{method.upper()} {path}")
    if mismatches:
        raise ValueError(
            f"nav_groups_for({lang}): merged spec operation order diverges from en: {mismatches}"
        )
    for tag, order in labels.get("op_order", {}).items():
        if tag in ops_by_en_tag:
            ops_by_en_tag[tag] = [o for o in order if o in ops_by_en_tag[tag]] + \
                                 [o for o in ops_by_en_tag[tag] if o not in order]
    guides_pages = []
    for entry in labels["guides_layout"]:
        if "page" in entry:
            guides_pages.append(f"{lang}/{entry['page']}")
        else:
            sub = {"group": entry["labels"][lang],
                   "pages": [f"{lang}/{memberships['pages'][k]['page']}" for k in entry["apps"]]}
            if entry.get("expanded"):
                sub["expanded"] = True
            guides_pages.append(sub)
    guides = {"group": labels["guides_group"][lang], "pages": guides_pages}

    def tier(cfg):
        return {"group": cfg["labels"][lang], "pages": [
            {"group": tag_map[t], "openapi": f"{lang}/api-reference/openapi_service.json",
             "pages": ops_by_en_tag[t]} for t in cfg["tag_order_en"] if t in ops_by_en_tag]}

    return [guides, tier(labels["reference"]["app_apis"]), tier(labels["reference"]["knowledge_api"])]


def wire(langs):
    labels = load_nav_labels()
    docs_path = REPO / "docs.json"
    with open(docs_path, encoding="utf-8") as f:
        docs = json.load(f)

    for lang in langs:
        groups = nav_groups_for(lang, labels)
        lang_nav = next(l for l in docs["navigation"]["languages"] if l["language"] == lang)
        replaced = 0
        for prod in lang_nav.get("products", []):
            for tab in prod.get("tabs", []):
                for item in tab.get("menu", []):
                    if item.get("item") == "API":
                        item["groups"] = copy.deepcopy(groups)
                        replaced += 1
        print(f"[{lang}] replaced {replaced} API menus in docs.json")

    # Redirects. No per-endpoint API map: any legacy no-language-prefix
    # /api-reference/... link falls through to the English API home via the
    # catch-all. The only exceptions are the three knowledge-base links embedded
    # in the product UI, which keep a specific per-language target. Non-API
    # redirects are preserved untouched.
    existing = docs.get("redirects", [])
    api_kb = [
        {"source": "/api-reference/knowledge-bases/list-knowledge-bases",
         "destination": "/en/api-reference/guides/knowledge"},
        {"source": "/api-reference/知识库/获取知识库列表",
         "destination": "/zh/api-reference/guides/knowledge"},
        {"source": "/api-reference/データセット/ナレッジベースリストを取得",
         "destination": "/ja/api-reference/guides/knowledge"},
    ]
    # Catch-all last so the KB exceptions win (Mintlify matches sources in order).
    api_catchall = {"source": "/api-reference/:slug*",
                    "destination": "/en/api-reference/guides/get-started"}
    kept = [r for r in existing if "/api-reference/" not in r["source"]]
    docs["redirects"] = kept + api_kb + [api_catchall]
    print(f"redirects: {len(kept)} non-API + {len(api_kb)} KB + 1 catch-all")

    with open(docs_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {docs_path.relative_to(REPO)}")


def check_coverage(langs):
    memberships = load_memberships()
    failures = []
    for lang in langs:
        with open(REPO / lang / "api-reference" / "openapi_service.json", encoding="utf-8") as _fh:
            merged = json.load(_fh)
        hrefs = {f"{m.upper()} {p}": op["x-mint"]["href"]
                 for p, ms in merged["paths"].items() for m, op in ms.items()
                 if isinstance(op, dict) and "x-mint" in op}
        for key, cfg in memberships["pages"].items():
            page = REPO / lang / f"{cfg['page']}.mdx"
            if not page.exists():
                failures.append(f"{lang}/{key}: page missing"); continue
            text = page.read_text(encoding="utf-8")
            links = set(re.findall(r"\]\((/[a-z]{2}/api-reference/[^)#\s]+)", text))
            for op_key in cfg["ops"]:
                if hrefs[op_key] not in links:
                    failures.append(f"{lang}/{key}: missing link for {op_key} ({hrefs[op_key]})")
            for link in links - set(hrefs.values()):
                if not (link.endswith("/overview") or "/api-reference/guides/" in link):
                    failures.append(f"{lang}/{key}: link to unknown page {link}")
    for f in failures: print("COVERAGE:", f)
    print(f"coverage failures: {len(failures)}")
    sys.exit(1 if failures else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["wire", "check-coverage"])
    ap.add_argument("--lang", nargs="*", default=["en"])
    args = ap.parse_args()

    if args.mode == "wire":
        wire(args.lang)
    elif args.mode == "check-coverage":
        check_coverage(args.lang)


if __name__ == "__main__":
    main()
