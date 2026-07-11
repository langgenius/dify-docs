"""Mechanical lint for Dify OpenAPI specs: examples vs schemas, enum coverage, links, x-codeSamples guard."""

import json
import os
import re
import sys
from collections import defaultdict

DOCS = os.environ["DOCS"]
issues = defaultdict(list)  # file -> [msg]


def slug(s):
    out = s.strip().lower()
    out = re.sub(r"\s+", "-", out)
    return out


def resolve(schema, spec, depth=0):
    if depth > 12 or not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        node = spec
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node.get(part, {})
        return resolve(node, spec, depth + 1)
    return schema


CHECKS = {"examples": 0, "links": 0}

def check_example(example, schema, spec, where, f, path=""):
    if not path:
        CHECKS["examples"] += 1
    schema = resolve(schema, spec)
    if not isinstance(schema, dict):
        return
    for comb in ("oneOf", "anyOf", "allOf"):
        if comb in schema:
            return  # combinators: skip deep validation, too noisy to arbitrate mechanically
    stype = schema.get("type")
    if isinstance(example, dict) and (stype in (None, "object")) and "properties" in schema:
        props = schema["properties"]
        addl = schema.get("additionalProperties", True)
        for k, v in example.items():
            if k not in props:
                if addl is False or isinstance(addl, dict) is False and addl is not True:
                    issues[f].append(f"{where}: example key `{k}{path}` not in schema properties")
                elif addl is True and not isinstance(schema.get("additionalProperties"), dict):
                    issues[f].append(f"{where}: example key `{k}{path}` undeclared in schema")
            else:
                check_example(v, props[k], spec, where, f, path=f".{k}")
        for r in schema.get("required", []):
            if r not in example:
                issues[f].append(f"{where}: required key `{r}` missing from example{path or ''}")
    elif isinstance(example, list) and "items" in schema:
        for i, item in enumerate(example[:5]):
            check_example(item, schema["items"], spec, where, f, path=f"[{i}]")
    elif "enum" in schema and example is not None:
        if example not in schema["enum"]:
            issues[f].append(f"{where}: example value {example!r}{path} not in enum {schema['enum']}")


def iter_examples(media):
    if "example" in media:
        yield "(example)", media["example"]
    for name, ex in media.get("examples", {}).items():
        if isinstance(ex, dict) and "value" in ex:
            yield name, ex["value"]


def collect_enum_usage(node, used, spec, depth=0):
    """Record enum values seen anywhere in examples."""
    if depth > 15:
        return
    if isinstance(node, dict):
        for v in node.values():
            collect_enum_usage(v, used, spec, depth + 1)
    elif isinstance(node, list):
        for v in node:
            collect_enum_usage(v, used, spec, depth + 1)
    elif isinstance(node, (str, int, bool)):
        used.add(node)


SPEC_FILES = [f"{DOCS}/{lang}/api-reference/openapi_service.json" for lang in ("en", "zh", "ja")]
missing = [f for f in SPEC_FILES if not os.path.exists(f)]
if missing:
    for f in missing:
        print(f"MISSING FILE: {f.replace(DOCS + '/', '')}")
    sys.exit(1)

for f in SPEC_FILES:
    rel = f.replace(DOCS + "/", "")
    spec = json.load(open(f))
    lang = rel.split("/")[0]

    # Build valid page slugs for this language
    valid_pages = set()
    for g in [f"{DOCS}/{lang}/api-reference/openapi_service.json"]:
        s2 = json.load(open(g))
        for p, ms in s2["paths"].items():
            for m, op in ms.items():
                if not isinstance(op, dict) or "summary" not in op:
                    continue
                for t in op.get("tags", ["default"]):
                    valid_pages.add(f"/api-reference/{slug(t)}/{slug(op['summary'])}")
                href = (op.get("x-mint") or {}).get("href")
                if href:
                    valid_pages.add(href.split("#")[0])

    all_example_values = set()
    all_enums = []  # (where, enum values)

    for p, ms in spec["paths"].items():
        for m, op in ms.items():
            if not isinstance(op, dict):
                continue
            where = f"{m.upper()} {p}"

            # request body examples vs schema
            for ctype, media in (op.get("requestBody", {}).get("content", {}) or {}).items():
                schema = media.get("schema", {})
                for name, ex in iter_examples(media):
                    check_example(ex, schema, spec, f"{where} req[{name}]", rel)
                    collect_enum_usage(ex, all_example_values, spec)

            # response examples vs schema
            for code, resp in (op.get("responses", {}) or {}).items():
                for ctype, media in (resp.get("content", {}) or {}).items():
                    schema = media.get("schema", {})
                    for name, ex in iter_examples(media):
                        check_example(ex, schema, spec, f"{where} resp{code}[{name}]", rel)
                        collect_enum_usage(ex, all_example_values, spec)

            # param examples + collect enums; x-codeSamples guard
            req_query = []
            for prm in op.get("parameters", []) or []:
                sch = resolve(prm.get("schema", {}), spec)
                if isinstance(sch, dict) and "enum" in sch:
                    all_enums.append((f"{where} param `{prm['name']}`", sch["enum"]))
                if prm.get("in") == "query" and prm.get("required"):
                    req_query.append(prm["name"])
            if req_query and m.lower() == "get" and not op.get("x-codeSamples"):
                issues[rel].append(f"{where}: required query {req_query} but no x-codeSamples override")

            # link targets in descriptions
            desc = op.get("description", "") or ""
            for link in re.findall(r"\]\((/[^)\s]+)\)", desc):
                CHECKS["links"] += 1
                if link.startswith("/api-reference/") or re.match(r"^/(en|zh|ja)/api-reference/", link):
                    base = link.split("#")[0]
                    if base not in valid_pages:
                        # MDX guide pages live under api-reference/ too
                        target = f"{DOCS}{base}"
                        if not (os.path.exists(target + ".mdx") or os.path.exists(target + ".md")):
                            issues[rel].append(f"{where}: broken link target {link}")
                else:
                    if not re.match(r"^/(en|zh|ja)/", link):
                        issues[rel].append(f"{where}: non-API link without language prefix: {link}")
                    else:
                        target = f"{DOCS}{link.split('#')[0]}"
                        if not (os.path.exists(target + ".mdx") or os.path.exists(target + ".md")):
                            issues[rel].append(f"{where}: broken doc link {link}")

    # enum coverage: every enum value in schemas seen in at least one example (warning-level)
    def walk_schemas(node, ctx, depth=0):
        if depth > 15 or not isinstance(node, dict):
            return
        if "enum" in node and isinstance(node["enum"], list):
            missing = [v for v in node["enum"] if v not in all_example_values]
            if missing and len(missing) < len(node["enum"]):  # fully-unused enums too noisy; report partial
                issues[rel].append(f"enum partially unexercised in examples ({ctx}): missing {missing}")
        for k, v in node.items():
            if isinstance(v, dict):
                walk_schemas(v, ctx if len(ctx) > 60 else f"{ctx}.{k}", depth + 1)
            elif isinstance(v, list):
                for it in v:
                    walk_schemas(it, ctx, depth + 1) if isinstance(it, dict) else None

    # keep enum sweep opt-in via env (noisy)
    if os.environ.get("ENUM_SWEEP"):
        walk_schemas(spec.get("components", {}).get("schemas", {}), "components", 0)

total = sum(len(v) for v in issues.values())
print(f"checked: {CHECKS}")
print(f"TOTAL ISSUES: {total}\n")
for f in sorted(issues):
    print(f"### {f} ({len(issues[f])})")
    seen = set()
    for msg in issues[f]:
        if msg in seen:
            continue
        seen.add(msg)
        print("  -", msg)
    print()
