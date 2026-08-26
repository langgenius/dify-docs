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

ROOT_PRESENTATION = {
    "en": {
        "summary": "Get API Information",
        "description": "Returns the public Service API version and server version without requiring an API key.",
        "tag": "Applications",
        "example_summary": "Response Example",
    },
    "zh": {
        "summary": "获取 API 信息",
        "description": "无需 API 密钥即可获取服务 API 版本和服务器版本。",
        "tag": "应用配置",
        "example_summary": "响应示例",
    },
    "ja": {
        "summary": "API 情報の取得",
        "description": "API キーを使用せずに、サービス API とサーバーのバージョンを取得します。",
        "tag": "アプリケーション設定",
        "example_summary": "レスポンス例",
    },
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


def merge_presentation(generated: Any, current: Any) -> Any:
    """Copy documentation-only fields while retaining generated structure."""

    if isinstance(generated, dict) and isinstance(current, dict):
        result = {}
        for key, current_value in current.items():
            if key in PRESENTATION_KEYS or key == "tags":
                result[key] = copy.deepcopy(current_value)
            elif key in generated:
                result[key] = merge_presentation(generated[key], current_value)
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
                merge_presentation(generated_item, current_item)
                if current_item is not None
                else copy.deepcopy(generated_item)
            )
        return result

    return copy.deepcopy(generated)


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


def apply_root_presentation(spec: dict[str, Any], language: str) -> None:
    operation = spec["paths"]["/"]["get"]
    presentation = ROOT_PRESENTATION[language]
    operation["summary"] = presentation["summary"]
    operation["description"] = presentation["description"]
    operation["tags"] = [presentation["tag"]]
    operation["x-mint"] = {
        "href": f"/{language}/api-reference/applications/get-api-information",
        "metadata": {
            "title": presentation["summary"],
            "sidebarTitle": presentation["summary"],
        },
    }
    media = operation["responses"]["200"]["content"]["application/json"]
    media["examples"] = {
        "response": {
            "summary": presentation["example_summary"],
            "value": {
                "welcome": "Dify OpenAPI",
                "api_version": "v1",
                "server_version": "1.17.0",
            },
        }
    }


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

    # JSON object order is not part of the wire contract, but it controls the
    # generated sidebar order. Keep the reviewed docs order, prepend the new
    # public API-information endpoint, and append other generated-only paths.
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

    apply_root_presentation(aligned, language)
    apply_deprecated_alias_presentation(aligned, language)
    return aligned


def wire_shape(value: Any, *, path: tuple[Any, ...] = ()) -> Any:
    """Remove presentation fields before comparing generated ownership."""

    if isinstance(value, dict):
        return {
            key: wire_shape(child, path=path + (key,))
            for key, child in value.items()
            if key not in PRESENTATION_KEYS
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
    parser.add_argument("--write", action="store_true", help="write aligned locale specs")
    args = parser.parse_args()

    generated = load_json(args.generated)
    current = {
        language: load_json(args.docs_root / language / "api-reference" / "openapi_service.json")
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
