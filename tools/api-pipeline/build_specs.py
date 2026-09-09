#!/usr/bin/env python3
"""Build translated Service API references from an upstream contract and annotations.

Only documentation annotations may differ from the generated contract. Request
and response fields, constraints, authentication, and references stay upstream.
"""

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = Path(__file__).resolve().parent
LANGUAGES = ("en", "zh", "ja")
METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
# Context matters: a schema description is prose, but a description key inside
# an enum/const/default value, OAuth scope map, or security requirement is data.
CHILDREN = {
    "document": {"paths": "path_item_map", "webhooks": "path_item_map", "components": "components"},
    "components": {"schemas": "schema_map", "parameters": "parameter_map", "responses": "response_map",
                   "headers": "header_map", "requestBodies": "request_body_map", "examples": "example_map",
                   "securitySchemes": "security_scheme_map", "links": "link_map", "callbacks": "callback_map",
                   "pathItems": "path_item_map"},
    "path_item": {**{method: "operation" for method in METHODS}, "parameters": "parameter_list"},
    "operation": {"parameters": "parameter_list", "requestBody": "request_body", "responses": "response_map",
                  "callbacks": "callback_map"},
    "response": {"content": "media_map", "headers": "header_map", "links": "link_map"},
    "request_body": {"content": "media_map"},
    "parameter": {"schema": "schema", "content": "media_map", "examples": "example_map"},
    "header": {"schema": "schema", "content": "media_map", "examples": "example_map"},
    "media": {"schema": "schema", "examples": "example_map", "encoding": "encoding_map"},
    "encoding": {"headers": "header_map"},
    "schema": {**{key: "schema_map" for key in ("properties", "patternProperties", "$defs", "definitions", "dependentSchemas")},
               **{key: "schema" for key in ("items", "additionalProperties", "unevaluatedProperties", "propertyNames", "not",
                                           "if", "then", "else", "contains", "additionalItems", "unevaluatedItems", "contentSchema")},
               **{key: "schema_list" for key in ("allOf", "anyOf", "oneOf", "prefixItems")}},
}
DOCUMENTATION_FIELDS = {
    "document": {"info", "servers", "tags", "externalDocs"},
    "operation": {"description", "summary", "externalDocs", "operationId", "tags", "x-mint"},
    "path_item": {"description", "summary"},
    "schema": {"description", "title", "example", "examples", "externalDocs"},
    "parameter": {"description", "example", "examples"},
    "header": {"description", "example", "examples"},
    "media": {"example", "examples"},
    "response": {"description"},
    "request_body": {"description"},
    "security_scheme": {"description"},
    "link": {"description"},
    "example": {"summary", "description", "value", "externalValue"},
}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def formatted(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(formatted(value), encoding="utf-8")


def pointer(parts):
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def parts_of(value):
    if not value.startswith("/"):
        raise ValueError(f"invalid annotation pointer: {value}")
    return [p.replace("~1", "/").replace("~0", "~") for p in value[1:].split("/")]


def object_role(parts):
    role = "document"
    for part in parts:
        if role.endswith("_map"):
            role = role.removesuffix("_map")
        elif role.endswith("_list") and str(part).isdigit():
            role = role.removesuffix("_list")
        elif role == "callback":
            role = "path_item"
        else:
            role = CHILDREN.get(role, {}).get(part, "literal")
    return role


def documentation_field(parts, key):
    return key in DOCUMENTATION_FIELDS.get(object_role(parts), set())


def contract(node, parts=()):
    """Remove presentation fields without removing properties named after them."""
    if isinstance(node, dict):
        return {k: contract(v, (*parts, k)) for k, v in node.items()
                if not documentation_field(parts, k)}
    if isinstance(node, list):
        return [contract(v, (*parts, str(i))) for i, v in enumerate(node)]
    return node


def annotation_changes(base, edited, parts=()):
    if isinstance(base, dict) and isinstance(edited, dict):
        for key in sorted(base.keys() | edited.keys()):
            location = (*parts, key)
            if documentation_field(parts, key):
                if key not in edited:
                    yield {"path": pointer(location), "remove": True}
                elif key not in base or base[key] != edited[key]:
                    yield {"path": pointer(location), "value": edited[key]}
            elif key not in base or key not in edited:
                raise ValueError(f"contract change at {pointer(location)}; fix the Dify source instead")
            else:
                yield from annotation_changes(base[key], edited[key], location)
    elif isinstance(base, list) and isinstance(edited, list) and len(base) == len(edited):
        for index, (left, right) in enumerate(zip(base, edited)):
            yield from annotation_changes(left, right, (*parts, str(index)))
    elif base != edited:
        raise ValueError(f"contract change at {pointer(parts)}; fix the Dify source instead")


def apply_annotations(base, overlay):
    result = copy.deepcopy(base)
    seen = set()
    for change in overlay["annotations"]:
        location = change["path"]
        parts = parts_of(location)
        if location in seen:
            raise ValueError(f"duplicate annotation: {location}")
        seen.add(location)
        if not documentation_field(parts[:-1], parts[-1]):
            raise ValueError(f"annotation would change the API contract: {location}")
        parent = result
        try:
            for part in parts[:-1]:
                parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError(f"annotation target no longer exists: {location}") from error
        if not isinstance(parent, dict):
            raise ValueError(f"annotation target is not an object: {location}")
        if change.get("remove"):
            if parts[-1] not in parent:
                raise ValueError(f"annotation removal target no longer exists: {location}")
            del parent[parts[-1]]
        else:
            parent[parts[-1]] = copy.deepcopy(change["value"])
    if contract(result) != contract(base):
        raise ValueError("annotations changed the API contract")
    return result


def operations(spec):
    for path, item in spec["paths"].items():
        for method, operation in item.items():
            if method in METHODS:
                yield f"{method.upper()} {path}", operation


def publication_base(pipeline=PIPELINE):
    upstream_dir = pipeline / "upstream"
    source = read_json(upstream_dir / "source.json")
    raw_path = upstream_dir / "service-openapi.json"
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    if source["sha256"] != digest:
        raise ValueError("upstream snapshot checksum differs from source.json; import it again")
    spec = read_json(raw_path)
    excluded = read_json(pipeline / "publication.json")["excluded_operations"]
    available = dict(operations(spec))
    for key, reason in excluded.items():
        if key not in available or not reason:
            raise ValueError(f"stale or unexplained publication exclusion: {key}")
    for path in list(spec["paths"]):
        for method in list(spec["paths"][path]):
            if f"{method.upper()} {path}" in excluded:
                del spec["paths"][path][method]
        if not any(m in METHODS for m in spec["paths"][path]):
            del spec["paths"][path]
    return spec


def check_publication(spec, lang):
    ids, hrefs = set(), set()
    for key, operation in operations(spec):
        operation_id = operation.get("operationId")
        mint = operation.get("x-mint", {})
        href = mint.get("href", "")
        if not operation_id or operation_id in ids:
            raise ValueError(f"{lang}: missing or duplicate operationId on {key}")
        if not href.startswith(f"/{lang}/api-reference/") or href in hrefs:
            raise ValueError(f"{lang}: missing or duplicate page URL on {key}")
        metadata = mint.get("metadata", {})
        if not metadata.get("title") or not metadata.get("sidebarTitle") or not operation.get("tags"):
            raise ValueError(f"{lang}: missing page labels on {key}")
        ids.add(operation_id)
        hrefs.add(href)


def build(args):
    base = publication_base()
    failed = []
    specs = {}
    # Validate all languages before writing any output.
    for lang in LANGUAGES:
        overlay = read_json(PIPELINE / "overlays" / f"{lang}.json")
        spec = apply_annotations(base, overlay)
        check_publication(spec, lang)
        specs[lang] = spec
    for lang, spec in specs.items():
        path = ROOT / lang / "api-reference" / "openapi_service.json"
        content = formatted(spec)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failed.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if failed:
        raise ValueError("generated specs are out of date: " + ", ".join(failed))
    print(f"{'checked' if args.check else 'built'} {len(specs)} languages, {len(dict(operations(base)))} operations each")


def capture(_args):
    base = publication_base()
    overlays = {}
    for lang in LANGUAGES:
        path = ROOT / lang / "api-reference" / "openapi_service.json"
        edited = read_json(path)
        check_publication(edited, lang)
        overlays[lang] = {"annotations": list(annotation_changes(base, edited))}
    for lang, overlay in overlays.items():
        write_json(PIPELINE / "overlays" / f"{lang}.json", overlay)
        print(f"captured {lang}: {len(overlay['annotations'])} annotations")


def import_source(args):
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        raise ValueError("--revision must be a full 40-character Dify commit SHA")
    data = args.spec.read_bytes()
    spec = json.loads(data)
    if spec.get("openapi") != "3.1.0" or not spec.get("paths"):
        raise ValueError("expected Dify's generated OpenAPI 3.1.0 Service API document")
    if not any(server.get("url") == "/v1" for server in spec.get("servers", [])):
        raise ValueError("expected service-openapi.json (/v1), not another Dify API surface")
    directory = PIPELINE / "upstream"
    directory.mkdir(parents=True, exist_ok=True)
    source = {"repository": "https://github.com/langgenius/dify", "revision": args.revision,
              "sha256": hashlib.sha256(data).hexdigest()}
    (directory / "service-openapi.json").write_bytes(data)
    write_json(directory / "source.json", source)
    print("imported upstream snapshot; review its diff and annotations before building")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("build", help="render the three language specs")
    command.add_argument("--check", action="store_true", help="fail if generated files differ")
    command.set_defaults(run=build)
    command = commands.add_parser("capture", help="save reviewed prose/example edits as annotations")
    command.set_defaults(run=capture)
    command = commands.add_parser("import", help="record an explicitly selected upstream export")
    command.add_argument("--spec", type=Path, required=True)
    command.add_argument("--revision", required=True, help="full Dify source commit SHA")
    command.set_defaults(run=import_source)
    args = parser.parse_args()
    try:
        args.run(args)
    except (ValueError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
