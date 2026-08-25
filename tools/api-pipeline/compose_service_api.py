#!/usr/bin/env python3
"""Compose localized Service API specs from Dify OpenAPI plus reviewed overlays.

The Dify-generated ``service-openapi.json`` is the base contract. Locale
overlays contain only the differences needed for documentation presentation,
localization, and published ``operationId`` compatibility. Wire-contract
fields are never captured from the rendered docs specs.

Each replace/remove action fingerprints the upstream value it was reviewed
against. An upstream change at an overlaid location therefore fails with a
conflict instead of being silently hidden. Unoverlaid upstream changes flow
into the composed document and make ``check`` report that the committed output
needs regeneration.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

LANGUAGES = ("en", "zh", "ja")
METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
OVERLAY_VERSION = 1
ABSENT = object()
PRESENTATION_KEYS = {
    "description",
    "example",
    "examples",
    "externalDocs",
    "summary",
    "title",
}
DOCS_EXTENSION_KEYS = {"x-codeSamples", "x-mint"}
NAMED_MAP_KEYS = {
    "$defs",
    "callbacks",
    "content",
    "definitions",
    "encoding",
    "headers",
    "mapping",
    "paths",
    "patternProperties",
    "properties",
    "responses",
    "schemas",
    "securitySchemes",
}
RAW_DATA_KEYS = {"const", "default", "enum"}
TOP_LEVEL_ORDER = (
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
)


def child_context(parent_context: str, key: str) -> str:
    if parent_context == "data":
        return "data"
    if parent_context == "named-map":
        return "object"
    if key in RAW_DATA_KEYS:
        return "data"
    if key in NAMED_MAP_KEYS:
        return "named-map"
    return "object"


class OverlayConflict(ValueError):
    """Raised when an overlay no longer matches its reviewed upstream value."""


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def escape_pointer_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def unescape_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def child_pointer(pointer: str, key: str) -> str:
    return f"{pointer}/{escape_pointer_token(key)}"


def guarded_action(
    action: dict[str, Any], context_guard: tuple[str, str] | None
) -> dict[str, Any]:
    if context_guard is not None:
        action["context_path"], action["context_sha256"] = context_guard
    return action


def diff_overlay(
    source: Any,
    target: Any,
    pointer: str = "",
    *,
    context_guard: tuple[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Return deterministic, preconditioned actions that turn source into target."""

    if isinstance(source, dict) and isinstance(target, dict):
        actions: list[dict[str, Any]] = []
        for key in sorted(set(source) | set(target)):
            path = child_pointer(pointer, key)
            if key not in source:
                actions.append(
                    guarded_action(
                        {"op": "add", "path": path, "value": target[key]},
                        context_guard,
                    )
                )
            elif key not in target:
                actions.append(
                    guarded_action(
                        {
                            "op": "remove",
                            "path": path,
                            "source_sha256": digest(source[key]),
                        },
                        context_guard,
                    )
                )
            else:
                actions.extend(
                    diff_overlay(
                        source[key],
                        target[key],
                        path,
                        context_guard=context_guard,
                    )
                )
        return actions

    if (
        isinstance(source, list)
        and isinstance(target, list)
        and len(source) == len(target)
    ):
        actions = []
        for index, (source_item, target_item) in enumerate(zip(source, target)):
            item_pointer = child_pointer(pointer, str(index))
            actions.extend(
                diff_overlay(
                    source_item,
                    target_item,
                    item_pointer,
                    context_guard=(item_pointer, digest(source_item)),
                )
            )
        return actions

    if source == target:
        return []
    return [
        guarded_action(
            {
                "op": "replace",
                "path": pointer,
                "source_sha256": digest(source),
                "value": target,
            },
            context_guard,
        )
    ]


def is_presentation_key(key: str, container: dict[str, Any] | None = None) -> bool:
    """Return whether a field may be owned by a locale overlay."""

    if key in PRESENTATION_KEYS or key in DOCS_EXTENSION_KEYS:
        return True
    is_operation = isinstance(container, dict) and isinstance(
        container.get("responses"), dict
    )
    return is_operation and key in {"operationId", "tags"}


def contract_shape(value: Any, *, context: str = "root") -> Any:
    """Return a value with locale-owned fields removed for safe list matching."""

    if isinstance(value, dict):
        return {
            key: contract_shape(
                child,
                context=child_context(context, key),
            )
            for key, child in sorted(value.items())
            if context == "named-map"
            or not (
                is_presentation_key(key, value)
                or (context == "root" and key == "tags")
            )
        }
    if isinstance(value, list):
        return [contract_shape(child, context=context) for child in value]
    return value


def merge_presentation(source: Any, target: Any, *, context: str = "root") -> Any:
    """Copy only target presentation fields onto the generated source.

    Dictionary structure always comes from Dify. Arrays are paired only when
    their presentation-free shapes match uniquely, which prevents a localized
    annotation from moving to a different ``oneOf`` branch after regeneration.
    """

    if isinstance(source, dict) and isinstance(target, dict):
        merged = copy.deepcopy(source)
        for key, target_child in target.items():
            if (
                context in {"object", "root"}
                and is_presentation_key(key, source)
            ) or (context == "root" and key == "tags"):
                merged[key] = copy.deepcopy(target_child)
            elif key in source:
                merged[key] = merge_presentation(
                    source[key],
                    target_child,
                    context=child_context(context, key),
                )
        for key in set(source) - set(target):
            if (
                context in {"object", "root"}
                and is_presentation_key(key, source)
            ) or (context == "root" and key == "tags"):
                del merged[key]
        return merged

    if isinstance(source, list) and isinstance(target, list):
        target_by_shape: dict[bytes, list[Any]] = {}
        for item in target:
            target_by_shape.setdefault(
                canonical_bytes(contract_shape(item, context=context)), []
            ).append(item)

        merged_items: list[Any] = []
        for item in source:
            matches = target_by_shape.get(
                canonical_bytes(contract_shape(item, context=context)), []
            )
            if len(matches) == 1:
                merged_items.append(
                    merge_presentation(item, matches[0], context=context)
                )
            else:
                merged_items.append(copy.deepcopy(item))
        return merged_items

    return copy.deepcopy(source)


def pointer_parent(document: Any, pointer: str) -> tuple[Any, str]:
    if not pointer.startswith("/"):
        raise OverlayConflict(f"overlay path must be an absolute JSON pointer: {pointer!r}")
    tokens = [unescape_pointer_token(token) for token in pointer[1:].split("/")]
    if not tokens or not tokens[-1]:
        raise OverlayConflict(f"overlay path must identify a child value: {pointer!r}")

    current = document
    for token in tokens[:-1]:
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise OverlayConflict(f"overlay parent does not exist: {pointer!r}")
    return current, tokens[-1]


def get_child(parent: Any, token: str) -> Any:
    if isinstance(parent, dict):
        return parent.get(token, ABSENT)
    if isinstance(parent, list) and token.isdigit():
        index = int(token)
        return parent[index] if index < len(parent) else ABSENT
    return ABSENT


def pointer_value(document: Any, pointer: str) -> Any:
    parent, token = pointer_parent(document, pointer)
    return get_child(parent, token)


def set_child(parent: Any, token: str, value: Any, *, add: bool) -> None:
    if isinstance(parent, dict):
        exists = token in parent
        if add and exists:
            raise OverlayConflict(f"add target already exists: {token!r}")
        if not add and not exists:
            raise OverlayConflict(f"replace target is absent: {token!r}")
        parent[token] = value
        return

    if isinstance(parent, list) and token.isdigit():
        index = int(token)
        if add:
            if index > len(parent):
                raise OverlayConflict(f"array add index is out of range: {index}")
            parent.insert(index, value)
        else:
            if index >= len(parent):
                raise OverlayConflict(f"array replace index is out of range: {index}")
            parent[index] = value
        return
    raise OverlayConflict(f"overlay target parent cannot contain {token!r}")


def remove_child(parent: Any, token: str) -> None:
    if isinstance(parent, dict) and token in parent:
        del parent[token]
        return
    if isinstance(parent, list) and token.isdigit() and int(token) < len(parent):
        del parent[int(token)]
        return
    raise OverlayConflict(f"remove target is absent: {token!r}")


def apply_overlay(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    if overlay.get("version") != OVERLAY_VERSION:
        raise OverlayConflict(
            f"unsupported overlay version {overlay.get('version')!r}; expected {OVERLAY_VERSION}"
        )
    actions = overlay.get("actions")
    if not isinstance(actions, list):
        raise OverlayConflict("overlay must contain an actions array")

    result = copy.deepcopy(base)
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            raise OverlayConflict(f"overlay action {index} must be an object")
        context_path = action.get("context_path")
        context_sha256 = action.get("context_sha256")
        if context_path is None and context_sha256 is None:
            continue
        if not isinstance(context_path, str) or not isinstance(context_sha256, str):
            raise OverlayConflict(
                f"overlay action {index} must provide string context_path/context_sha256"
            )
        context_value = pointer_value(base, context_path)
        if context_value is ABSENT or digest(context_value) != context_sha256:
            raise OverlayConflict(
                f"{context_path}: array item moved or changed upstream"
            )

    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            raise OverlayConflict(f"overlay action {index} must be an object")
        operation = action.get("op")
        pointer = action.get("path")
        if operation not in {"add", "remove", "replace"} or not isinstance(pointer, str):
            raise OverlayConflict(f"overlay action {index} has invalid op/path")

        parent, token = pointer_parent(result, pointer)
        current = get_child(parent, token)
        if operation == "add":
            if current is not ABSENT:
                raise OverlayConflict(f"{pointer}: add target already exists upstream")
            set_child(parent, token, copy.deepcopy(action.get("value")), add=True)
            continue

        if current is ABSENT:
            raise OverlayConflict(f"{pointer}: reviewed upstream value is now absent")
        expected = action.get("source_sha256")
        actual = digest(current)
        if not isinstance(expected, str) or actual != expected:
            raise OverlayConflict(
                f"{pointer}: upstream value changed (expected {expected!r}, found {actual})"
            )
        if operation == "remove":
            remove_child(parent, token)
        else:
            set_child(parent, token, copy.deepcopy(action.get("value")), add=False)

    if merge_presentation(base, result) != result:
        raise OverlayConflict("overlay contains a non-presentation contract change")
    return result


def iter_operations(spec: dict[str, Any]):
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method in METHODS and isinstance(operation, dict):
                yield path, method, operation


def validate_composed_spec(spec: dict[str, Any], language: str) -> list[str]:
    failures: list[str] = []
    expected_prefix = f"/{language}/api-reference/"
    for path, method, operation in iter_operations(spec):
        label = f"{method.upper()} {path}"
        if operation.get("deprecated") is True:
            continue
        tags = operation.get("tags")
        if not isinstance(tags, list) or not tags or tags == ["service_api"]:
            failures.append(f"{label}: missing docs navigation tag")
        href = (operation.get("x-mint") or {}).get("href")
        if not isinstance(href, str) or not href.startswith(expected_prefix):
            failures.append(f"{label}: missing localized x-mint.href")
        metadata = (operation.get("x-mint") or {}).get("metadata")
        if not isinstance(metadata, dict) or not all(
            isinstance(metadata.get(key), str) and metadata[key]
            for key in ("title", "sidebarTitle")
        ):
            failures.append(f"{label}: missing x-mint localized titles")
        if not isinstance(operation.get("summary"), str) or not operation["summary"]:
            failures.append(f"{label}: missing localized summary")
    return failures


def render_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def order_top_level(value: dict[str, Any]) -> dict[str, Any]:
    """Put onboarding metadata before the large paths and components maps."""

    ordered = {key: value[key] for key in TOP_LEVEL_ORDER if key in value}
    ordered.update({key: child for key, child in value.items() if key not in ordered})
    return ordered


def overlay_path(root: Path, language: str) -> Path:
    return root / "tools" / "api-pipeline" / "service_api_overlays" / f"{language}.json"


def spec_path(root: Path, language: str) -> Path:
    return root / language / "api-reference" / "openapi_service.json"


def capture(args: argparse.Namespace) -> int:
    base = load_json(args.upstream)
    for language in LANGUAGES:
        target = load_json(spec_path(args.docs_root, language))
        localized = merge_presentation(base, target)
        overlay = {
            "version": OVERLAY_VERSION,
            "language": language,
            "description": (
                "Reviewed locale overlay applied to Dify's generated Service API OpenAPI base. "
                "Replace/remove actions pin the upstream value with source_sha256."
            ),
            "actions": diff_overlay(base, localized),
        }
        path = overlay_path(args.docs_root, language)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_json(overlay), encoding="utf-8")
        print(f"captured {language}: {len(overlay['actions'])} actions -> {path}")
    return 0


def compose(args: argparse.Namespace) -> int:
    base = load_json(args.upstream)
    failed = False
    for language in LANGUAGES:
        path = overlay_path(args.docs_root, language)
        try:
            composed = order_top_level(apply_overlay(base, load_json(path)))
        except OverlayConflict as error:
            print(f"{language}: OVERLAY CONFLICT: {error}")
            failed = True
            continue

        validation_errors = validate_composed_spec(composed, language)
        if validation_errors:
            failed = True
            print(f"{language}: INVALID COMPOSED SPEC ({len(validation_errors)}):")
            for error in validation_errors:
                print(f"  - {error}")
            continue

        output = spec_path(args.docs_root, language)
        rendered = render_json(composed)
        if args.write:
            output.write_text(rendered, encoding="utf-8")
            print(f"{language}: wrote {output}")
        else:
            current = output.read_text(encoding="utf-8")
            if current != rendered:
                failed = True
                print(f"{language}: composed output differs from {output}")
            else:
                print(f"{language}: composed output is current")
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="dify-docs repository root",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture_parser = subparsers.add_parser(
        "capture", help="capture overlays from the current localized specs"
    )
    capture_parser.add_argument("upstream", type=Path)
    capture_parser.set_defaults(func=capture)

    compose_parser = subparsers.add_parser(
        "compose", help="compose and check or write the localized specs"
    )
    compose_parser.add_argument("upstream", type=Path)
    compose_parser.add_argument(
        "--write", action="store_true", help="write composed specs instead of checking"
    )
    compose_parser.set_defaults(func=compose)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
