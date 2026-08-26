#!/usr/bin/env python3
"""Align localized Service API specs with Dify's generated wire contract.

This is the migration-stage aligner. It starts from Dify's generated
``service-openapi.json`` and carries over documentation presentation fields
from the existing English, Chinese, and Japanese specs. Routes, methods,
parameters, request and response schemas, status codes, authentication,
deprecation flags, and operation IDs always come from Dify.

The later overlay stage will replace this migration workflow. Until then,
running the command without ``--write`` checks that committed specs are the
deterministic result of the alignment.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

LANGUAGES = ("en", "zh", "ja")
HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
PRESENTATION_KEYS = {
    "description",
    "example",
    "examples",
    "externalDocs",
    "summary",
    "title",
    "x-codeSamples",
    "x-mint",
}

DEPRECATED_ALIAS_PRESENTATION = {
    "en": {
        "summary": "Deprecated Compatibility Endpoint",
        "description": "Deprecated compatibility endpoint. Use the equivalent hyphenated endpoint instead.",
    },
    "zh": {
        "summary": "已弃用的兼容端点",
        "description": "用于兼容旧版调用的已弃用端点。请改用对应的连字符路径。",
    },
    "ja": {
        "summary": "非推奨の互換エンドポイント",
        "description": "旧バージョンとの互換性のための非推奨エンドポイントです。対応するハイフン区切りのパスを使用してください。",
    },
}

RESPONSE_DESCRIPTION_FALLBACKS = {
    "zh": {
        "2": "请求成功。",
        "400": "请求参数无效。",
        "401": "身份验证失败：API 令牌无效。",
        "403": "没有访问此资源的权限。",
        "404": "找不到请求的资源。",
        "409": "请求与资源当前状态冲突。",
        "429": "请求过于频繁。",
        "5": "服务器无法完成请求。",
        "default": "请求失败。",
    },
    "ja": {
        "2": "リクエストが成功しました。",
        "400": "リクエストパラメーターが無効です。",
        "401": "認証に失敗しました。API トークンが無効です。",
        "403": "このリソースにアクセスする権限がありません。",
        "404": "リクエストされたリソースが見つかりません。",
        "409": "リクエストがリソースの現在の状態と競合しています。",
        "429": "リクエストが多すぎます。",
        "5": "サーバーはリクエストを完了できませんでした。",
        "default": "リクエストに失敗しました。",
    },
}
FALLBACK_TRANSLATIONS = {
    translation
    for language_fallbacks in RESPONSE_DESCRIPTION_FALLBACKS.values()
    for translation in language_fallbacks.values()
}

API_LINK_RE = re.compile(r"(?<!/(?:en|zh|ja))(/api-reference/)")
LOCALIZED_API_LINK_RE = re.compile(r"/(?:en|zh|ja)/api-reference/")
DEPRECATED_ALIAS_PATHS = {
    "/datasets/{dataset_id}/document/create_by_file",
    "/datasets/{dataset_id}/document/create_by_text",
    "/datasets/{dataset_id}/documents/{document_id}/update_by_file",
    "/datasets/{dataset_id}/documents/{document_id}/update_by_text",
    "/datasets/{dataset_id}/hit-testing",
}
CANONICAL_DEPRECATED_PATH = "/datasets/{dataset_id}/documents/{document_id}/update-by-file"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def render_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def item_identity(value: Any) -> tuple[Any, ...] | None:
    if not isinstance(value, dict):
        return None
    if isinstance(value.get("$ref"), str):
        return ("ref", value["$ref"])
    if isinstance(value.get("name"), str) and isinstance(value.get("in"), str):
        return ("parameter", value["in"], value["name"])
    if isinstance(value.get("type"), str) and isinstance(value.get("format"), str):
        return ("schema", value["type"], value["format"])
    if isinstance(value.get("type"), str):
        return ("schema", value["type"])
    return None


def is_presentation_field(key: str, parent_path: tuple[Any, ...]) -> bool:
    """Return whether a key is OpenAPI presentation rather than user data."""

    # Under a JSON Schema `properties` object these names are API fields, not
    # OpenAPI annotations (for example, a response field named `summary`).
    return key in PRESENTATION_KEYS and (not parent_path or parent_path[-1] != "properties")


def is_operation_tags(key: str, parent_path: tuple[Any, ...]) -> bool:
    """Return whether a `tags` key belongs to an OpenAPI operation."""

    return (
        key == "tags"
        and len(parent_path) == 3
        and parent_path[0] == "paths"
        and parent_path[2] in HTTP_METHODS
    )


def merge_presentation(generated: Any, current: Any, *, path: tuple[Any, ...] = ()) -> Any:
    """Copy documentation-only fields while retaining generated structure."""

    if isinstance(generated, dict) and isinstance(current, dict):
        result = {}
        for key, current_value in current.items():
            if is_presentation_field(key, path) or is_operation_tags(key, path):
                result[key] = copy.deepcopy(current_value)
            elif key in generated:
                result[key] = merge_presentation(
                    generated[key],
                    current_value,
                    path=path + (key,),
                )
        for key, generated_value in generated.items():
            if key not in result:
                result[key] = copy.deepcopy(generated_value)
        return result

    if isinstance(generated, list) and isinstance(current, list):
        current_by_identity: dict[tuple[Any, ...], list[Any]] = defaultdict(list)
        for item in current:
            identity = item_identity(item)
            if identity is not None:
                current_by_identity[identity].append(item)

        result = []
        for index, generated_item in enumerate(generated):
            identity = item_identity(generated_item)
            matches = current_by_identity.get(identity, []) if identity is not None else []
            if len(matches) == 1:
                current_item = matches[0]
            elif len(generated) == len(current):
                current_item = current[index]
            else:
                current_item = None
            result.append(
                merge_presentation(
                    generated_item,
                    current_item,
                    path=path + (index,),
                )
                if current_item is not None
                else copy.deepcopy(generated_item)
            )
        return result

    return copy.deepcopy(generated)


def resolve_local_ref(root: dict[str, Any], ref: str) -> tuple[Any, tuple[str, ...]]:
    """Resolve a local JSON pointer and return its value and path."""

    if not ref.startswith("#/"):
        raise ValueError(f"only local references are supported: {ref}")
    path = tuple(part.replace("~1", "/").replace("~0", "~") for part in ref[2:].split("/"))
    value: Any = root
    for part in path:
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"unresolvable local reference: {ref}")
        value = value[part]
    return value, path


def schema_match_score(generated: Any, current: Any, generated_root: dict[str, Any]) -> int:
    """Score how likely two schema branches describe the same value."""

    if not isinstance(generated, dict) or not isinstance(current, dict):
        return 0
    if isinstance(generated.get("$ref"), str):
        generated, _ = resolve_local_ref(generated_root, generated["$ref"])
        if not isinstance(generated, dict):
            return 0

    score = 0
    generated_type = generated.get("type")
    current_type = current.get("type")
    if generated_type == current_type and generated_type is not None:
        score += 4
    generated_properties = generated.get("properties")
    current_properties = current.get("properties")
    if isinstance(generated_properties, dict) and isinstance(current_properties, dict):
        shared = set(generated_properties) & set(current_properties)
        score += len(shared) * 10
        if set(generated_properties) == set(current_properties):
            score += 5
    if "items" in generated and "items" in current:
        score += 3
    generated_enum = generated.get("enum")
    current_enum = current.get("enum")
    if isinstance(generated_enum, list) and isinstance(current_enum, list):
        score += len(set(generated_enum) & set(current_enum)) * 2
    return score


def carry_referenced_presentation(
    generated_root: dict[str, Any],
    current_root: dict[str, Any],
    aligned_root: dict[str, Any],
) -> None:
    """Carry docs fields when generated schemas move behind local references.

    ``merge_presentation`` handles fields that stay at the same JSON path. This
    pass handles structural extraction performed by Pydantic/OpenAPI, such as
    an inline response object becoming ``$ref: ...DocumentResponse``. It only
    applies an old value when every matching source location agrees, so a
    shared component never inherits endpoint-specific prose by accident.
    """

    candidates: dict[tuple[tuple[Any, ...], str], list[Any]] = defaultdict(list)
    active_refs: set[tuple[str, str | None]] = set()

    def collect_presentation(current: dict[str, Any], aligned_path: tuple[Any, ...]) -> None:
        for key in PRESENTATION_KEYS:
            if key in current and is_presentation_field(key, aligned_path):
                candidates[(aligned_path, key)].append(copy.deepcopy(current[key]))

    def best_variant(variants: list[Any], current: dict[str, Any]) -> tuple[int, Any] | None:
        scored = [
            (schema_match_score(variant, current, generated_root), index, variant)
            for index, variant in enumerate(variants)
            if not (isinstance(variant, dict) and variant.get("type") == "null")
        ]
        if not scored:
            return None
        scored.sort(key=lambda item: (-item[0], item[1]))
        if scored[0][0] == 0 and len(scored) > 1:
            return None
        return scored[0][1], scored[0][2]

    def walk(
        generated: Any,
        current: Any,
        aligned: Any,
        aligned_path: tuple[Any, ...],
        *,
        remapped: bool = False,
        copy_here: bool = True,
    ) -> None:
        if isinstance(generated, dict) and isinstance(current, dict) and isinstance(aligned, dict):
            generated_ref = generated.get("$ref")
            current_ref = current.get("$ref")
            if isinstance(generated_ref, str):
                # Identical references are already merged at their component
                # definitions by merge_presentation; following them again can
                # misplace presentation from a nullable wrapper onto a branch.
                if generated_ref == current_ref:
                    return
                ref_pair = (generated_ref, current_ref if isinstance(current_ref, str) else None)
                if ref_pair in active_refs:
                    return
                generated_target, target_path = resolve_local_ref(generated_root, generated_ref)
                aligned_target, _ = resolve_local_ref(aligned_root, generated_ref)
                if isinstance(current_ref, str):
                    current_target, _ = resolve_local_ref(current_root, current_ref)
                    target_copy_here = True
                else:
                    current_target = current
                    # Presentation on an inline schema stays beside the new
                    # $ref; only its children move into the component.
                    target_copy_here = False
                active_refs.add(ref_pair)
                walk(
                    generated_target,
                    current_target,
                    aligned_target,
                    target_path,
                    remapped=True,
                    copy_here=target_copy_here,
                )
                active_refs.remove(ref_pair)
                return

            if isinstance(current_ref, str):
                current_target, _ = resolve_local_ref(current_root, current_ref)
                walk(
                    generated,
                    current_target,
                    aligned,
                    aligned_path,
                    remapped=True,
                    copy_here=True,
                )
                return

            if remapped and copy_here:
                collect_presentation(current, aligned_path)

            # OpenAPI 3.1 commonly wraps an old nullable schema in anyOf with
            # a null branch. Follow the structurally matching non-null branch.
            for union_key in ("anyOf", "oneOf"):
                generated_variants = generated.get(union_key)
                if isinstance(generated_variants, list) and union_key not in current:
                    match = best_variant(generated_variants, current)
                    if match is not None:
                        index, generated_variant = match
                        aligned_variants = aligned.get(union_key)
                        if isinstance(aligned_variants, list) and index < len(aligned_variants):
                            walk(
                                generated_variant,
                                current,
                                aligned_variants[index],
                                aligned_path + (union_key, index),
                                remapped=True,
                                copy_here=False,
                            )
                            return

            for key in generated:
                if key not in current or key not in aligned:
                    continue
                walk(
                    generated[key],
                    current[key],
                    aligned[key],
                    aligned_path + (key,),
                    remapped=remapped,
                )
            return

        if isinstance(generated, list) and isinstance(current, list) and isinstance(aligned, list):
            unused = set(range(len(current)))
            for generated_index, generated_item in enumerate(generated):
                if generated_index >= len(aligned):
                    break
                ranked = sorted(
                    (
                        schema_match_score(generated_item, current[index], generated_root),
                        index,
                    )
                    for index in unused
                )
                if not ranked:
                    continue
                score, current_index = ranked[-1]
                if score == 0:
                    current_index = generated_index if generated_index in unused else min(unused)
                unused.remove(current_index)
                walk(
                    generated_item,
                    current[current_index],
                    aligned[generated_index],
                    aligned_path + (generated_index,),
                    remapped=remapped,
                )

    walk(generated_root, current_root, aligned_root, ())

    for (path, key), values in candidates.items():
        unique = {json.dumps(value, ensure_ascii=False, sort_keys=True) for value in values}
        if len(unique) != 1:
            continue
        target: Any = aligned_root
        for part in path:
            if isinstance(part, int):
                if not isinstance(target, list) or part >= len(target):
                    target = None
                    break
            elif not isinstance(target, dict) or part not in target:
                target = None
                break
            target = target[part]
        if isinstance(target, dict) and key not in target:
            target[key] = values[0]


def iter_operations(spec: dict[str, Any]):
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise TypeError("OpenAPI paths must be an object")
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method in HTTP_METHODS and isinstance(operation, dict):
                yield path, method, operation


def build_translation_memory(
    english: Any,
    localized: Any,
    *,
    key: str | None = None,
    result: dict[str, set[str]] | None = None,
) -> dict[str, set[str]]:
    """Collect existing prose translations at structurally matching locations."""

    result = defaultdict(set) if result is None else result
    if isinstance(english, dict) and isinstance(localized, dict):
        for child_key in set(english) & set(localized):
            build_translation_memory(
                english[child_key],
                localized[child_key],
                key=child_key,
                result=result,
            )
    elif isinstance(english, list) and isinstance(localized, list):
        for english_item, localized_item in zip(english, localized):
            build_translation_memory(english_item, localized_item, key=key, result=result)
    elif (
        key in {"description", "summary", "title"}
        and isinstance(english, str)
        and isinstance(localized, str)
        and english != localized
        and localized not in FALLBACK_TRANSLATIONS
    ):
        result[english].add(localized)
    return result


def apply_translation_memory(english: Any, localized: Any, memory: dict[str, set[str]], *, key: str | None = None) -> Any:
    """Fill newly generated prose from unambiguous existing translations."""

    if isinstance(english, dict) and isinstance(localized, dict):
        result = copy.deepcopy(localized)
        for child_key in set(english) & set(localized):
            result[child_key] = apply_translation_memory(
                english[child_key],
                localized[child_key],
                memory,
                key=child_key,
            )
        return result
    if isinstance(english, list) and isinstance(localized, list) and len(english) == len(localized):
        return [
            apply_translation_memory(english_item, localized_item, memory, key=key)
            for english_item, localized_item in zip(english, localized)
        ]
    if (
        key in {"description", "summary", "title"}
        and isinstance(english, str)
        and localized == english
        and len(memory.get(english, set())) == 1
    ):
        return next(iter(memory[english]))
    return copy.deepcopy(localized)


def prefer_aligned_memory(
    initial: dict[str, set[str]],
    aligned: dict[str, set[str]],
) -> dict[str, set[str]]:
    """Prefer a unique translation visible in the generated document shape."""

    result = {english: set(translations) for english, translations in initial.items()}
    for english, translations in aligned.items():
        if len(translations) == 1:
            result[english] = set(translations)
        elif english not in result:
            result[english] = set(translations)
    return result


def collect_equal_presentation(english: Any, localized: Any, *, key: str | None = None) -> set[str]:
    """Return presentation strings already intentionally shared by a locale."""

    result: set[str] = set()
    if isinstance(english, dict) and isinstance(localized, dict):
        for child_key in set(english) & set(localized):
            result.update(collect_equal_presentation(english[child_key], localized[child_key], key=child_key))
    elif isinstance(english, list) and isinstance(localized, list):
        for english_item, localized_item in zip(english, localized):
            result.update(collect_equal_presentation(english_item, localized_item, key=key))
    elif (
        key in {"description", "summary", "title"}
        and isinstance(english, str)
        and canonical_presentation(english) == canonical_presentation(localized)
    ):
        result.add(canonical_presentation(english))
    return result


def canonical_presentation(value: str) -> str:
    """Ignore locale prefixes when comparing otherwise identical prose."""

    return LOCALIZED_API_LINK_RE.sub("/api-reference/", value)


def response_description_fallback(language: str, status: str) -> str:
    fallbacks = RESPONSE_DESCRIPTION_FALLBACKS[language]
    if status in fallbacks:
        return fallbacks[status]
    if status.startswith("2"):
        return fallbacks["2"]
    if status.startswith("5"):
        return fallbacks["5"]
    return fallbacks["default"]


def remove_new_untranslated_presentation(
    english: Any,
    localized: Any,
    allowed_equal: set[str],
    language: str,
    *,
    path: tuple[Any, ...] = (),
) -> Any:
    """Avoid introducing raw English prose into zh/ja during migration.

    Existing shared technical labels remain intact. Newly generated optional
    presentation fields are omitted until the overlay owns them. OpenAPI
    response descriptions are required, so new ones receive a localized
    status-level fallback instead.
    """

    if isinstance(english, dict) and isinstance(localized, dict):
        result = copy.deepcopy(localized)
        for key in list(result):
            if key not in english:
                continue
            english_value = english[key]
            localized_value = result[key]
            if (
                key in {"description", "summary", "title"}
                and isinstance(english_value, str)
                and isinstance(localized_value, str)
                and canonical_presentation(localized_value) == canonical_presentation(english_value)
                and canonical_presentation(english_value) not in allowed_equal
            ):
                is_response_description = (
                    key == "description"
                    and len(path) >= 2
                    and path[-2] == "responses"
                    and isinstance(path[-1], str)
                )
                if is_response_description:
                    result[key] = response_description_fallback(language, path[-1])
                else:
                    del result[key]
                continue
            result[key] = remove_new_untranslated_presentation(
                english_value,
                localized_value,
                allowed_equal,
                language,
                path=path + (key,),
            )
        return result
    if isinstance(english, list) and isinstance(localized, list):
        return [
            remove_new_untranslated_presentation(
                english_item,
                localized_item,
                allowed_equal,
                language,
                path=path + (index,),
            )
            for index, (english_item, localized_item) in enumerate(zip(english, localized))
        ]
    return copy.deepcopy(localized)


def prefix_internal_api_links(value: Any, language: str, *, key: str | None = None) -> Any:
    """Add the locale prefix to bare internal API reference links."""

    if isinstance(value, dict):
        return {
            child_key: prefix_internal_api_links(child, language, key=child_key)
            for child_key, child in value.items()
        }
    if isinstance(value, list):
        return [prefix_internal_api_links(child, language, key=key) for child in value]
    if key in PRESENTATION_KEYS and isinstance(value, str):
        return API_LINK_RE.sub(f"/{language}/api-reference/", value)
    return copy.deepcopy(value)


def localize_unmatched_tags(
    aligned: dict[str, Any],
    english_current: dict[str, Any],
    localized_current: dict[str, Any],
) -> None:
    english_tags = [tag.get("name") for tag in english_current.get("tags", []) if isinstance(tag, dict)]
    localized_tags = [tag.get("name") for tag in localized_current.get("tags", []) if isinstance(tag, dict)]
    tag_map = {
        english: localized
        for english, localized in zip(english_tags, localized_tags)
        if isinstance(english, str) and isinstance(localized, str)
    }
    for _, _, operation in iter_operations(aligned):
        tags = operation.get("tags")
        if isinstance(tags, list):
            operation["tags"] = [tag_map.get(tag, tag) for tag in tags]


def apply_deprecated_alias_presentation(spec: dict[str, Any], language: str) -> None:
    presentation = DEPRECATED_ALIAS_PRESENTATION[language]
    for path, _, operation in iter_operations(spec):
        if operation.get("deprecated") is not True:
            continue
        if path in DEPRECATED_ALIAS_PATHS:
            operation.pop("x-mint", None)
            operation["summary"] = presentation["summary"]
            operation["description"] = presentation["description"]
        elif path == CANONICAL_DEPRECATED_PATH:
            operation["x-mint"] = {
                "href": f"/{language}/api-reference/documents/update-document-by-file",
                "metadata": {
                    "title": operation["summary"],
                    "sidebarTitle": operation["summary"],
                },
            }


def align_language(
    generated: dict[str, Any],
    current: dict[str, Any],
    language: str,
) -> dict[str, Any]:
    aligned = merge_presentation(generated, current)
    carry_referenced_presentation(generated, current, aligned)

    # JSON object order is not part of the wire contract, but it controls the
    # generated sidebar order. Keep the reviewed docs order, retain the
    # generated root path first, and append other generated-only paths.
    generated_paths = aligned.get("paths", {})
    current_paths = current.get("paths", {})
    if isinstance(generated_paths, dict) and isinstance(current_paths, dict):
        path_order = (
            (["/"] if "/" in generated_paths and "/" not in current_paths else [])
            + [path for path in current_paths if path in generated_paths]
            + [
                path
                for path in generated_paths
                if path not in current_paths and path != "/"
            ]
        )
        ordered_paths = {}
        for path in path_order:
            path_item = generated_paths[path]
            current_path_item = current_paths.get(path)
            if isinstance(path_item, dict) and isinstance(current_path_item, dict):
                item_order = (
                    [key for key in current_path_item if key in path_item]
                    + [key for key in path_item if key not in current_path_item]
                )
                path_item = {key: path_item[key] for key in item_order}
            ordered_paths[path] = path_item
        aligned["paths"] = ordered_paths

    # These top-level values control the published docs experience rather than
    # the request/response wire contract.
    for key in ("info", "servers", "tags"):
        if key in current:
            aligned[key] = copy.deepcopy(current[key])

    generated_schemes = aligned.get("components", {}).get("securitySchemes", {})
    current_schemes = current.get("components", {}).get("securitySchemes", {})
    if isinstance(generated_schemes, dict) and isinstance(current_schemes, dict):
        current_descriptions = [
            scheme.get("description")
            for scheme in current_schemes.values()
            if isinstance(scheme, dict) and isinstance(scheme.get("description"), str)
        ]
        if len(current_descriptions) == 1:
            for scheme in generated_schemes.values():
                if isinstance(scheme, dict):
                    scheme["description"] = current_descriptions[0]

    apply_deprecated_alias_presentation(aligned, language)
    return aligned


def wire_shape(value: Any, *, path: tuple[Any, ...] = ()) -> Any:
    """Remove presentation fields before comparing generated ownership."""

    if isinstance(value, dict):
        return {
            key: wire_shape(child, path=path + (key,))
            for key, child in value.items()
            if not is_presentation_field(key, path)
            and not (
                key == "tags"
                and len(path) == 3
                and path[0] == "paths"
                and path[2] in HTTP_METHODS
            )
        }
    if isinstance(value, list):
        return [wire_shape(child, path=path + (index,)) for index, child in enumerate(value)]
    return value


def validate_alignment(generated: dict[str, Any], aligned: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    generated_ops = {(path, method): operation for path, method, operation in iter_operations(generated)}
    aligned_ops = {(path, method): operation for path, method, operation in iter_operations(aligned)}
    if set(generated_ops) != set(aligned_ops):
        failures.append("operation inventory differs from generated contract")

    for key in sorted(set(generated_ops) & set(aligned_ops)):
        generated_operation = generated_ops[key]
        aligned_operation = aligned_ops[key]
        for field in ("deprecated", "operationId", "parameters", "requestBody", "security"):
            if wire_shape(generated_operation.get(field)) != wire_shape(aligned_operation.get(field)):
                failures.append(f"{key[1].upper()} {key[0]}: generated {field} changed")
        generated_responses = generated_operation.get("responses") or {}
        aligned_responses = aligned_operation.get("responses") or {}
        if set(generated_responses) != set(aligned_responses):
            failures.append(f"{key[1].upper()} {key[0]}: response statuses changed")
        elif wire_shape(generated_responses) != wire_shape(aligned_responses):
            failures.append(f"{key[1].upper()} {key[0]}: response contract changed")

    if generated.get("openapi") != aligned.get("openapi"):
        failures.append("OpenAPI version differs from generated contract")
    if generated.get("security") != aligned.get("security"):
        failures.append("top-level security differs from generated contract")
    if wire_shape(generated.get("paths"), path=("paths",)) != wire_shape(
        aligned.get("paths"), path=("paths",)
    ):
        failures.append("generated path contract changed")
    if wire_shape(generated.get("components")) != wire_shape(aligned.get("components")):
        failures.append("generated component contract changed")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generated", type=Path, help="Dify-generated service-openapi.json")
    parser.add_argument("--docs-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--presentation-root",
        type=Path,
        help="optional source root for the pre-alignment locale presentation",
    )
    parser.add_argument("--write", action="store_true", help="write aligned locale specs")
    args = parser.parse_args()

    generated = load_json(args.generated)
    presentation_root = args.presentation_root or args.docs_root
    current = {
        language: load_json(presentation_root / language / "api-reference" / "openapi_service.json")
        for language in LANGUAGES
    }
    memories = {
        language: build_translation_memory(current["en"], current[language])
        for language in ("zh", "ja")
    }
    allowed_equal = {
        language: collect_equal_presentation(current["en"], current[language])
        for language in ("zh", "ja")
    }

    aligned = {
        language: align_language(generated, current[language], language)
        for language in LANGUAGES
    }
    for language in ("zh", "ja"):
        for _ in range(5):
            aligned_memory = build_translation_memory(aligned["en"], aligned[language])
            memory = prefer_aligned_memory(memories[language], aligned_memory)
            translated = apply_translation_memory(aligned["en"], aligned[language], memory)
            if translated == aligned[language]:
                break
            aligned[language] = translated
        localize_unmatched_tags(aligned[language], current["en"], current[language])
        aligned[language] = remove_new_untranslated_presentation(
            aligned["en"],
            aligned[language],
            allowed_equal[language],
            language,
        )

    aligned = {
        language: prefix_internal_api_links(spec, language)
        for language, spec in aligned.items()
    }

    failed = False
    for language in LANGUAGES:
        failures = validate_alignment(generated, aligned[language])
        if failures:
            failed = True
            print(f"{language}: alignment failures ({len(failures)})")
            for failure in failures:
                print(f"  - {failure}")
            continue

        output = args.docs_root / language / "api-reference" / "openapi_service.json"
        rendered = render_json(aligned[language])
        if args.write:
            output.write_text(rendered, encoding="utf-8")
            print(f"{language}: wrote {output}")
        elif output.read_text(encoding="utf-8") != rendered:
            failed = True
            print(f"{language}: aligned output differs from {output}")
        else:
            print(f"{language}: aligned output is current")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
