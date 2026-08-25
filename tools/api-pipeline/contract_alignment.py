"""Check the docs Service API contract against the code-generated OpenAPI spec.

The generated spec owns the wire contract. The localized docs specs may add
presentation fields (descriptions, examples, x-mint, and x-codeSamples), but
must not silently drift in routes, parameter serialization, request media
encodings, response headers, or body schemas. Existing public operation IDs are
preserved through a compatibility overlay because generated SDKs use them as
method names. Every other wire-contract difference fails.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

METHODS = ("delete", "get", "head", "options", "patch", "post", "put", "trace")
LANGUAGES = ("en", "zh", "ja")
PRESENTATION_KEYS = {
    "description",
    "example",
    "examples",
    "externalDocs",
    "summary",
    "title",
}
DOCS_EXTENSION_KEYS = {"x-codeSamples", "x-mint"}
ORDER_INSENSITIVE_ARRAY_KEYS = {
    "allOf",
    "anyOf",
    "enum",
    "oneOf",
    "required",
    "type",
}
OPENAPI_30_UNSUPPORTED_SCHEMA_KEYS = {
    "$anchor",
    "$comment",
    "$defs",
    "$dynamicAnchor",
    "$dynamicRef",
    "$id",
    "$schema",
    "const",
    "contains",
    "contentEncoding",
    "contentMediaType",
    "contentSchema",
    "dependentRequired",
    "dependentSchemas",
    "else",
    "examples",
    "if",
    "maxContains",
    "minContains",
    "patternProperties",
    "prefixItems",
    "propertyNames",
    "then",
    "unevaluatedItems",
    "unevaluatedProperties",
}
SCHEMA_MAP_KEYWORDS = {
    "$defs",
    "definitions",
    "dependentSchemas",
    "patternProperties",
    "properties",
}
SCHEMA_ARRAY_KEYWORDS = {"allOf", "anyOf", "oneOf", "prefixItems"}
SCHEMA_SINGLE_KEYWORDS = {
    "additionalItems",
    "additionalProperties",
    "contains",
    "contentSchema",
    "else",
    "if",
    "items",
    "not",
    "propertyNames",
    "then",
    "unevaluatedItems",
    "unevaluatedProperties",
}
NAMED_OBJECT_MAP_KEYS = SCHEMA_MAP_KEYWORDS | {
    "callbacks",
    "content",
    "dependentRequired",
    "encoding",
    "headers",
    "mapping",
}
RAW_INSTANCE_KEYS = {"const", "default"}


def normalization_context(key: str) -> str:
    """Return how a value's object keys should be interpreted while normalizing."""

    if key == "enum":
        return "enum"
    if key in RAW_INSTANCE_KEYS:
        return "data"
    if key in NAMED_OBJECT_MAP_KEYS:
        return "named-map"
    return "object"


@dataclass(frozen=True)
class Operation:
    path: str
    method: str
    path_item: dict[str, Any]
    data: dict[str, Any]

    @property
    def label(self) -> str:
        return f"{self.method.upper()} {self.path}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def operations(spec: dict[str, Any]) -> dict[tuple[str, str], Operation]:
    result: dict[tuple[str, str], Operation] = {}
    for path, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for method in METHODS:
            data = path_item.get(method)
            if isinstance(data, dict):
                result[(path, method)] = Operation(path, method, path_item, data)
    return result


def resolve_ref(spec: dict[str, Any], ref: str) -> Any:
    if not ref.startswith("#/"):
        return {"$ref": ref}
    value: Any = spec
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[token]
    return value


def _schema_roots(spec: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    schemas = (spec.get("components") or {}).get("schemas") or {}
    if isinstance(schemas, dict):
        for name, schema in schemas.items():
            yield f"components.schemas.{name}", schema

    def walk(value: Any, path: str) -> Iterable[tuple[str, Any]]:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                if key == "schema":
                    yield child_path, child
                elif key in {"example", "examples"}:
                    continue
                else:
                    yield from walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                yield from walk(child, f"{path}[{index}]")

    yield from walk(spec.get("paths") or {}, "paths")
    components = spec.get("components") or {}
    if isinstance(components, dict):
        for section, value in components.items():
            if section in {"schemas", "securitySchemes"}:
                continue
            yield from walk(value, f"components.{section}")


def validate_declared_schema_dialect(spec: dict[str, Any]) -> list[str]:
    """Reject schema keywords whose meaning conflicts with the declared dialect."""

    version = spec.get("openapi")
    if not isinstance(version, str):
        return []

    failures: list[str] = []

    def inspect(value: Any, path: str) -> None:
        if not isinstance(value, dict):
            return

        if version.startswith("3.0"):
            if value.get("type") == "null":
                failures.append(f"OpenAPI {version} schema uses type 'null': {path}")
            elif isinstance(value.get("type"), list):
                failures.append(
                    f"OpenAPI {version} schema uses an array 'type'; OpenAPI 3.0 requires a single string: {path}"
                )
            for key in sorted(OPENAPI_30_UNSUPPORTED_SCHEMA_KEYS & set(value)):
                failures.append(
                    f"OpenAPI {version} schema uses unsupported keyword {key!r}: {path}"
                )
        elif version.startswith("3.1"):
            if "nullable" in value:
                failures.append(
                    f"OpenAPI {version} schema uses unsupported keyword 'nullable': {path}"
                )
            for key in ("exclusiveMaximum", "exclusiveMinimum"):
                if isinstance(value.get(key), bool):
                    failures.append(
                        f"OpenAPI {version} schema uses boolean {key!r}; JSON Schema 2020-12 requires a number: {path}"
                    )

        for keyword in SCHEMA_MAP_KEYWORDS:
            children = value.get(keyword)
            if not isinstance(children, dict):
                continue
            for name, child in children.items():
                inspect(child, f"{path}.{keyword}.{name}")

        for keyword in SCHEMA_ARRAY_KEYWORDS:
            children = value.get(keyword)
            if not isinstance(children, list):
                continue
            for index, child in enumerate(children):
                inspect(child, f"{path}.{keyword}[{index}]")

        for keyword in SCHEMA_SINGLE_KEYWORDS:
            child = value.get(keyword)
            if isinstance(child, list):
                for index, item in enumerate(child):
                    inspect(item, f"{path}.{keyword}[{index}]")
            else:
                inspect(child, f"{path}.{keyword}")

    for path, schema in _schema_roots(spec):
        inspect(schema, path)
    return failures


def nullable_schema(
    non_null: Any, *, has_default: bool, default: Any = None
) -> dict[str, Any]:
    if (
        isinstance(non_null, dict)
        and set(non_null) == {"anyOf"}
        and isinstance(non_null["anyOf"], list)
    ):
        candidates = list(non_null["anyOf"])
    else:
        candidates = [non_null]
    null_schema = {"type": "null"}
    if null_schema not in candidates:
        candidates.append(null_schema)
    candidates.sort(key=canonical_json)
    result: dict[str, Any] = {"anyOf": candidates}
    if has_default:
        result["default"] = default
    return result


def finite_property_names(
    value: Any,
    spec: dict[str, Any],
    *,
    stack: tuple[str, ...] = (),
) -> tuple[str, ...] | None:
    """Return a provably complete finite set accepted by propertyNames.

    A propertyNames schema can contain arbitrary JSON Schema constraints. Only
    an enum of unique strings, plus non-validating annotations and an optional
    redundant ``type: string``, is safe to expand into explicit properties.
    """

    if not isinstance(value, dict):
        return None

    ref = value.get("$ref")
    if isinstance(ref, str):
        semantic_siblings = {
            key
            for key in value
            if key != "$ref"
            and key not in PRESENTATION_KEYS
            and key != "$comment"
            and key not in DOCS_EXTENSION_KEYS
        }
        if semantic_siblings or ref in stack:
            return None
        target = resolve_ref(spec, ref)
        if target == {"$ref": ref}:
            return None
        return finite_property_names(target, spec, stack=(*stack, ref))

    semantic_keys = {
        key
        for key in value
        if key not in PRESENTATION_KEYS
        and key != "$comment"
        and key not in DOCS_EXTENSION_KEYS
    }
    if not semantic_keys <= {"enum", "type"}:
        return None
    if "type" in value and value["type"] != "string":
        return None

    names = value.get("enum")
    if (
        not isinstance(names, list)
        or not all(isinstance(name, str) for name in names)
        or len(names) != len(set(names))
    ):
        return None
    return tuple(names)


def expand_finite_property_names(
    value: dict[str, Any], spec: dict[str, Any]
) -> dict[str, Any] | None:
    """Expand a finite propertyNames enum without changing object semantics.

    ``additionalProperties`` constrains names not covered by ``properties`` or
    ``patternProperties``. For every permitted name, carry that value schema
    into the explicit property. Non-empty patterns and constraining
    ``unevaluatedProperties`` make the equivalent expansion non-local, so they
    deliberately remain unexpanded.
    """

    if value.get("type") != "object":
        return None
    names = finite_property_names(value.get("propertyNames"), spec)
    if names is None:
        return None

    properties_value = value.get("properties", {})
    if not isinstance(properties_value, dict):
        return None

    patterns = value.get("patternProperties", {})
    if not isinstance(patterns, dict) or patterns:
        return None

    unevaluated = value.get("unevaluatedProperties", True)
    if unevaluated not in (True, {}):
        return None

    additional = value.get("additionalProperties", True)
    if not isinstance(additional, (bool, dict)):
        return None

    properties: dict[str, Any] = {}
    for name in names:
        if name in properties_value:
            properties[name] = properties_value[name]
        elif additional is not False:
            properties[name] = {} if additional is True else additional

    expanded = dict(value)
    expanded.pop("propertyNames")
    expanded.pop("patternProperties", None)
    expanded.pop("unevaluatedProperties", None)
    expanded["properties"] = properties
    expanded["additionalProperties"] = False
    return expanded


def normalize(
    value: Any,
    spec: dict[str, Any],
    *,
    stack: tuple[str, ...] = (),
    key: str = "",
    context: str | None = None,
) -> Any:
    context = context or normalization_context(key)

    # Defaults, const values, and enum members are JSON instances, not schema
    # objects. Their keys are application data even when they happen to be
    # named ``description``, ``title``, or ``x-*``.
    if context == "data":
        if isinstance(value, dict):
            return {
                child_key: normalize(
                    child_value,
                    spec,
                    stack=stack,
                    key=child_key,
                    context="data",
                )
                for child_key, child_value in sorted(value.items())
            }
        if isinstance(value, list):
            return [
                normalize(item, spec, stack=stack, key=key, context="data")
                for item in value
            ]
        return value

    # Enum order is not significant, but array-valued enum members retain
    # their own element order as ordinary JSON instances.
    if context == "enum":
        if not isinstance(value, list):
            return normalize(value, spec, stack=stack, key=key, context="data")
        items = [
            normalize(item, spec, stack=stack, key=key, context="data")
            for item in value
        ]
        items.sort(key=canonical_json)
        return items

    # Maps such as Schema Object ``properties`` and Media Type Object
    # ``encoding`` use arbitrary application-defined names. Preserve every
    # map key, while normalizing each mapped OpenAPI/Schema object normally.
    if context == "named-map":
        if not isinstance(value, dict):
            return value
        child_context = "dependent-required" if key == "dependentRequired" else "object"
        return {
            child_key: normalize(
                child_value,
                spec,
                stack=stack,
                key=child_key,
                context=child_context,
            )
            for child_key, child_value in sorted(value.items())
        }

    if context == "dependent-required":
        normalized = normalize(value, spec, stack=stack, key=key, context="data")
        if isinstance(normalized, list):
            normalized.sort(key=canonical_json)
        return normalized

    if isinstance(value, dict):
        # JSON Schema's empty schema and boolean true are equivalent. OpenAPI
        # 3.0 commonly emits the former while OpenAPI 3.1 permits the latter.
        if key == "additionalProperties" and not value:
            return True

        ref = value.get("$ref")
        if isinstance(ref, str):
            if ref in stack:
                # Preserve which ancestor the recursive edge targets. A plain
                # boolean makes A -> B -> A indistinguishable from A -> B -> B.
                return {"$recursive": stack.index(ref)}
            target = resolve_ref(spec, ref)
            if target == {"$ref": ref}:
                return target
            siblings = {
                k: v
                for k, v in value.items()
                if k != "$ref"
                and k not in PRESENTATION_KEYS
                and k not in DOCS_EXTENSION_KEYS
            }
            resolved = normalize(
                target,
                spec,
                stack=(*stack, ref),
                key=key,
                context="object",
            )
            nullable = siblings.pop("nullable", None)
            default = siblings.pop("default", None) if "default" in siblings else None
            has_default = "default" in value
            deprecated = (
                siblings.pop("deprecated", None) if "deprecated" in siblings else None
            )
            has_deprecated = "deprecated" in value
            read_only = (
                siblings.pop("readOnly", None) if "readOnly" in siblings else None
            )
            has_read_only = "readOnly" in value
            write_only = (
                siblings.pop("writeOnly", None) if "writeOnly" in siblings else None
            )
            has_write_only = "writeOnly" in value
            if nullable is True:
                non_null: Any = resolved
                if siblings:
                    non_null = {
                        "resolved": resolved,
                        "siblings": normalize(
                            siblings,
                            spec,
                            stack=stack,
                            key=key,
                            context="object",
                        ),
                    }
                result = nullable_schema(
                    non_null,
                    has_default=has_default,
                    default=normalize(
                        default,
                        spec,
                        stack=stack,
                        key="default",
                        context="data",
                    ),
                )
                if has_deprecated:
                    result["deprecated"] = deprecated
                if has_read_only:
                    result["readOnly"] = read_only
                if has_write_only:
                    result["writeOnly"] = write_only
                return result
            if not siblings and not (
                has_default or has_deprecated or has_read_only or has_write_only
            ):
                return resolved
            if not siblings:
                result = (
                    dict(resolved)
                    if isinstance(resolved, dict)
                    else {"resolved": resolved}
                )
            else:
                result = {
                    "resolved": resolved,
                    "siblings": normalize(
                        siblings,
                        spec,
                        stack=stack,
                        key=key,
                        context="object",
                    ),
                }
            if has_default:
                result["default"] = normalize(
                    default,
                    spec,
                    stack=stack,
                    key="default",
                    context="data",
                )
            if has_deprecated:
                result["deprecated"] = deprecated
            if has_read_only:
                result["readOnly"] = read_only
            if has_write_only:
                result["writeOnly"] = write_only
            return result

        # A finite propertyNames enum can be compared with an equivalent set
        # of explicit properties, provided all value constraints can be
        # carried across without guessing.
        expanded_property_names = expand_finite_property_names(value, spec)
        if expanded_property_names is not None:
            value = expanded_property_names

        # Compare OpenAPI 3.0 nullable schemas with their OpenAPI 3.1 JSON
        # Schema representation. Keep a missing nullable flag meaningful: an
        # optional property and a property accepting an explicit null are not
        # the same wire contract.
        if value.get("nullable") is True:
            non_null = {
                child_key: child_value
                for child_key, child_value in value.items()
                if child_key != "nullable"
            }
            has_default = "default" in non_null
            default = non_null.pop("default", None)
            has_deprecated = "deprecated" in non_null
            deprecated = non_null.pop("deprecated", None)
            has_read_only = "readOnly" in non_null
            read_only = non_null.pop("readOnly", None)
            has_write_only = "writeOnly" in non_null
            write_only = non_null.pop("writeOnly", None)
            enum = non_null.get("enum")
            if enum == [None]:
                result = {"type": "null"}
                if has_default:
                    result["default"] = normalize(
                        default,
                        spec,
                        stack=stack,
                        key="default",
                        context="data",
                    )
                if has_deprecated:
                    result["deprecated"] = deprecated
                if has_read_only:
                    result["readOnly"] = read_only
                if has_write_only:
                    result["writeOnly"] = write_only
                return result
            if isinstance(enum, list) and None in enum:
                non_null["enum"] = [item for item in enum if item is not None]
            normalized_non_null = normalize(
                non_null,
                spec,
                stack=stack,
                key=key,
                context="object",
            )
            result = nullable_schema(
                normalized_non_null,
                has_default=has_default,
                default=normalize(
                    default,
                    spec,
                    stack=stack,
                    key="default",
                    context="data",
                ),
            )
            if has_deprecated:
                result["deprecated"] = deprecated
            if has_read_only:
                result["readOnly"] = read_only
            if has_write_only:
                result["writeOnly"] = write_only
            return result

        normalized: dict[str, Any] = {}
        for child_key in sorted(value):
            if child_key in PRESENTATION_KEYS or child_key in DOCS_EXTENSION_KEYS:
                continue
            normalized[child_key] = normalize(
                value[child_key],
                spec,
                stack=stack,
                key=child_key,
                context=normalization_context(child_key),
            )
        # OpenAPI 3.0 represents a fixed value as a single-value enum, while
        # JSON Schema/OpenAPI 3.1 can use const directly.
        enum = normalized.get("enum")
        if "const" not in normalized and isinstance(enum, list) and len(enum) == 1:
            normalized["const"] = enum[0]
            del normalized["enum"]
        # Pydantic may spell unconstrained JSON either as an empty schema or as
        # an explicit union of every JSON value kind. Treat those spellings as
        # the same contract so component de-duplication cannot create drift.
        unrestricted_json = {
            canonical_json({"additionalProperties": True, "type": "object"}),
            canonical_json({"items": {}, "type": "array"}),
            canonical_json({"type": "boolean"}),
            canonical_json({"type": "integer"}),
            canonical_json({"type": "null"}),
            canonical_json({"type": "number"}),
            canonical_json({"type": "string"}),
        }
        unrestricted_json_without_integer = unrestricted_json - {
            canonical_json({"type": "integer"})
        }
        candidates = normalized.get("anyOf")
        if isinstance(candidates, list):
            flattened: list[Any] = []
            for candidate in candidates:
                if (
                    isinstance(candidate, dict)
                    and set(candidate) == {"anyOf"}
                    and isinstance(candidate["anyOf"], list)
                ):
                    flattened.extend(candidate["anyOf"])
                else:
                    flattened.append(candidate)
            unique = {canonical_json(candidate): candidate for candidate in flattened}
            if any(
                isinstance(candidate, dict) and candidate.get("type") == "number"
                for candidate in unique.values()
            ):
                unique = {
                    encoded: candidate
                    for encoded, candidate in unique.items()
                    if not (
                        isinstance(candidate, dict)
                        and candidate.get("type") == "integer"
                    )
                }
            candidates = sorted(unique.values(), key=canonical_json)
            normalized["anyOf"] = candidates
        if (
            isinstance(candidates, list)
            and {canonical_json(candidate) for candidate in candidates}
            in (unrestricted_json, unrestricted_json_without_integer)
        ):
            # Collapse only the validation portion. JSON Schema annotations
            # such as ``default: null`` remain meaningful on an otherwise
            # unrestricted value and must survive normalization.
            del normalized["anyOf"]
            if not normalized:
                return True if key == "additionalProperties" else {}
        return normalized

    if isinstance(value, list):
        items = [
            normalize(item, spec, stack=stack, key=key, context="object")
            for item in value
        ]
        if key in ORDER_INSENSITIVE_ARRAY_KEYS:
            items.sort(key=canonical_json)
        return items

    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest_pair(upstream: Any, documented: Any) -> str:
    payload = canonical_json({"upstream": upstream, "documented": documented}).encode()
    return hashlib.sha256(payload).hexdigest()[:20]


def parameter_contract(
    parameter: dict[str, Any], spec: dict[str, Any], *, location: str
) -> dict[str, Any]:
    """Return the wire-relevant portion of an OpenAPI Parameter or Header object."""

    default_style = "form" if location in {"cookie", "query"} else "simple"
    style = parameter["style"] if "style" in parameter else default_style
    result: dict[str, Any] = {
        "deprecated": parameter.get("deprecated", False),
        "explode": parameter["explode"] if "explode" in parameter else style == "form",
        "required": parameter.get("required", False),
        "style": style,
    }
    if location == "query":
        result["allowEmptyValue"] = parameter.get("allowEmptyValue", False)
        result["allowReserved"] = parameter.get("allowReserved", False)
    if "schema" in parameter:
        result["schema"] = normalize(parameter["schema"], spec, key="schema")
    if "content" in parameter:
        result["content"] = normalize(parameter["content"], spec, key="content")
    return result


def operation_parameters(operation: Operation, spec: dict[str, Any]) -> dict[str, Any]:
    parameters: list[Any] = []
    parameters.extend(operation.path_item.get("parameters") or [])
    parameters.extend(operation.data.get("parameters") or [])
    result: dict[str, Any] = {}
    for parameter in parameters:
        if not isinstance(parameter, dict):
            continue
        if "$ref" in parameter:
            parameter = resolve_ref(spec, parameter["$ref"])
        location = parameter.get("in")
        name = parameter.get("name")
        if location not in {"cookie", "header", "path", "query"} or not isinstance(
            name, str
        ):
            continue
        result[f"{location}:{name}"] = parameter_contract(
            parameter, spec, location=location
        )
    return result


def security_scheme_contract(scheme: dict[str, Any]) -> dict[str, Any]:
    """Return the authentication-relevant portion of an OpenAPI security scheme."""

    scheme_type = scheme.get("type")
    result: dict[str, Any] = {"type": scheme_type}
    if scheme_type == "apiKey":
        result.update({"in": scheme.get("in"), "name": scheme.get("name")})
    elif scheme_type == "http":
        result["scheme"] = str(scheme.get("scheme", "")).lower()
        if "bearerFormat" in scheme:
            result["bearerFormat"] = scheme["bearerFormat"]
    elif scheme_type == "oauth2":
        flows: dict[str, Any] = {}
        for flow_name, flow in (scheme.get("flows") or {}).items():
            if not isinstance(flow_name, str) or not isinstance(flow, dict):
                continue
            flow_contract = {
                key: flow[key]
                for key in ("authorizationUrl", "refreshUrl", "tokenUrl")
                if key in flow
            }
            scopes = flow.get("scopes")
            if isinstance(scopes, dict):
                # Scope descriptions are presentation; scope names define the
                # permissions a security requirement may request.
                flow_contract["scopes"] = sorted(str(scope) for scope in scopes)
            flows[flow_name] = flow_contract
        result["flows"] = flows
    elif scheme_type == "openIdConnect":
        result["openIdConnectUrl"] = scheme.get("openIdConnectUrl")
    return result


def effective_security_contract(
    operation: Operation, spec: dict[str, Any]
) -> list[Any]:
    """Resolve global/operation security requirements without depending on scheme names."""

    requirements = operation.data.get("security", spec.get("security", []))
    if not isinstance(requirements, list):
        return [{"invalid": normalize(requirements, spec, key="security")}]

    schemes = (spec.get("components") or {}).get("securitySchemes") or {}
    normalized_requirements: list[Any] = []
    for requirement in requirements:
        if not isinstance(requirement, dict):
            normalized_requirements.append(
                {"invalid": normalize(requirement, spec, key="security")}
            )
            continue
        normalized_requirement: list[dict[str, Any]] = []
        for scheme_name, scopes in requirement.items():
            scheme = schemes.get(scheme_name) if isinstance(schemes, dict) else None
            if isinstance(scheme, dict) and "$ref" in scheme:
                scheme = resolve_ref(spec, scheme["$ref"])
            scheme_contract = (
                security_scheme_contract(scheme)
                if isinstance(scheme, dict)
                else {"missing_security_scheme": str(scheme_name)}
            )
            normalized_requirement.append(
                {
                    "scheme": scheme_contract,
                    "scopes": sorted(str(scope) for scope in scopes)
                    if isinstance(scopes, list)
                    else scopes,
                }
            )
        normalized_requirement.sort(key=canonical_json)
        normalized_requirements.append(normalized_requirement)
    normalized_requirements.sort(key=canonical_json)
    return normalized_requirements


def request_body(
    operation: Operation, spec: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    body = operation.data.get("requestBody")
    if not isinstance(body, dict):
        return False, {}
    if "$ref" in body:
        body = resolve_ref(spec, body["$ref"])
    content = body.get("content") or {}
    media_contracts = {
        media_type: {
            "encoding": normalize(media.get("encoding", {}), spec, key="encoding"),
            "schema": normalize(media.get("schema"), spec, key="schema"),
        }
        for media_type, media in content.items()
        if isinstance(media, dict)
    }
    return bool(body.get("required")), media_contracts


def callbacks(operation: Operation, spec: dict[str, Any]) -> Any:
    """Return the normalized callback contract for an operation."""

    return normalize(operation.data.get("callbacks", {}), spec, key="callbacks")


def response_headers(response: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, header in (response.get("headers") or {}).items():
        if not isinstance(name, str) or not isinstance(header, dict):
            continue
        if "$ref" in header:
            header = resolve_ref(spec, header["$ref"])
        if not isinstance(header, dict):
            continue
        # HTTP field names are case-insensitive, so casing alone is not drift.
        result[name.lower()] = parameter_contract(header, spec, location="header")
    return result


def responses(operation: Operation, spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for status, response in (operation.data.get("responses") or {}).items():
        if not isinstance(response, dict):
            continue
        if "$ref" in response:
            response = resolve_ref(spec, response["$ref"])
        content = response.get("content") or {}
        result[str(status)] = {
            "content": {
                media_type: normalize(media, spec, key="media")
                for media_type, media in content.items()
                if isinstance(media, dict)
            },
            "headers": response_headers(response, spec),
        }
    return result


def add_difference(
    differences: dict[str, str], key: str, upstream: Any, documented: Any
) -> None:
    if upstream != documented:
        differences[key] = digest_pair(upstream, documented)


def compare_specs(
    upstream: dict[str, Any],
    documented: dict[str, Any],
    operation_id_overrides: dict[str, str] | None = None,
) -> tuple[list[str], dict[str, str], dict[str, int]]:
    hard_errors = [
        f"upstream {failure}" for failure in validate_declared_schema_dialect(upstream)
    ]
    hard_errors.extend(validate_declared_schema_dialect(documented))
    upstream_version = upstream.get("openapi")
    documented_version = documented.get("openapi")
    if not isinstance(upstream_version, str) or not upstream_version:
        hard_errors.append(
            f"upstream OpenAPI version must be a non-empty string: {upstream_version!r}"
        )
    if not isinstance(documented_version, str) or not documented_version:
        hard_errors.append(
            f"documented OpenAPI version must be a non-empty string: {documented_version!r}"
        )
    if upstream_version != documented_version:
        hard_errors.append(
            f"OpenAPI version mismatch: upstream={upstream_version}, documented={documented_version}"
        )
    differences: dict[str, str] = {}

    upstream_ops = operations(upstream)
    documented_ops = operations(documented)
    operation_id_overrides = operation_id_overrides or {}

    for key in sorted(set(upstream_ops) - set(documented_ops)):
        hard_errors.append(f"missing documented operation: {upstream_ops[key].label}")
    for key in sorted(set(documented_ops) - set(upstream_ops)):
        hard_errors.append(f"docs-only operation: {documented_ops[key].label}")

    shared_labels = {
        upstream_ops[key].label for key in set(upstream_ops) & set(documented_ops)
    }
    for label in sorted(set(operation_id_overrides) - shared_labels):
        hard_errors.append(f"stale operationId compatibility override: {label}")

    for key in sorted(set(upstream_ops) & set(documented_ops)):
        source = upstream_ops[key]
        docs = documented_ops[key]

        source_params = operation_parameters(source, upstream)
        docs_params = operation_parameters(docs, documented)
        if source_params != docs_params:
            hard_errors.append(f"parameter contract mismatch: {source.label}")

        source_deprecated = bool(source.data.get("deprecated"))
        docs_deprecated = bool(docs.data.get("deprecated"))
        if source_deprecated != docs_deprecated:
            hard_errors.append(f"deprecated flag mismatch: {source.label}")

        source_security = effective_security_contract(source, upstream)
        docs_security = effective_security_contract(docs, documented)
        if source_security != docs_security:
            hard_errors.append(f"security contract mismatch: {source.label}")

        source_callbacks = callbacks(source, upstream)
        docs_callbacks = callbacks(docs, documented)
        if source_callbacks != docs_callbacks:
            hard_errors.append(f"callback contract mismatch: {source.label}")

        source_required, source_request = request_body(source, upstream)
        docs_required, docs_request = request_body(docs, documented)
        if set(source_request) != set(docs_request):
            hard_errors.append(f"request media-type mismatch: {source.label}")
        add_difference(
            differences,
            f"request-required | {source.label}",
            source_required,
            docs_required,
        )
        for media_type in sorted(set(source_request) & set(docs_request)):
            add_difference(
                differences,
                f"request-schema | {source.label} | {media_type}",
                source_request[media_type]["schema"],
                docs_request[media_type]["schema"],
            )
            add_difference(
                differences,
                f"request-encoding | {source.label} | {media_type}",
                source_request[media_type]["encoding"],
                docs_request[media_type]["encoding"],
            )

        source_responses = responses(source, upstream)
        docs_responses = responses(docs, documented)
        source_only_statuses = sorted(set(source_responses) - set(docs_responses))
        docs_only_statuses = sorted(set(docs_responses) - set(source_responses))
        add_difference(
            differences,
            f"response-status | {source.label}",
            {
                "statuses": sorted(source_responses),
                "unmatched": {
                    status: source_responses[status] for status in source_only_statuses
                },
            },
            {
                "statuses": sorted(docs_responses),
                "unmatched": {
                    status: docs_responses[status] for status in docs_only_statuses
                },
            },
        )
        for status in sorted(set(source_responses) & set(docs_responses)):
            source_response = source_responses[status]
            docs_response = docs_responses[status]
            add_difference(
                differences,
                f"response-header | {source.label} | {status}",
                source_response["headers"],
                docs_response["headers"],
            )
            source_content = source_response["content"]
            docs_content = docs_response["content"]
            source_only_media = sorted(set(source_content) - set(docs_content))
            docs_only_media = sorted(set(docs_content) - set(source_content))
            add_difference(
                differences,
                f"response-media | {source.label} | {status}",
                {
                    "media_types": sorted(source_content),
                    "unmatched": {
                        media_type: source_content[media_type]
                        for media_type in source_only_media
                    },
                },
                {
                    "media_types": sorted(docs_content),
                    "unmatched": {
                        media_type: docs_content[media_type]
                        for media_type in docs_only_media
                    },
                },
            )
            for media_type in sorted(set(source_content) & set(docs_content)):
                add_difference(
                    differences,
                    f"response-schema | {source.label} | {status} | {media_type}",
                    source_content[media_type],
                    docs_content[media_type],
                )

        if source.label in operation_id_overrides:
            expected_operation_id = operation_id_overrides[source.label]
            if docs.data.get("operationId") != expected_operation_id:
                hard_errors.append(
                    "operationId compatibility override mismatch: "
                    f"{source.label}: expected={expected_operation_id!r}, "
                    f"documented={docs.data.get('operationId')!r}"
                )
        else:
            add_difference(
                differences,
                f"operation-id | {source.label}",
                source.data.get("operationId"),
                docs.data.get("operationId"),
            )

    counts: dict[str, int] = {}
    for difference in differences:
        category = difference.split(" | ", 1)[0]
        counts[category] = counts.get(category, 0) + 1
    return hard_errors, differences, counts


def print_items(title: str, items: Iterable[str]) -> None:
    items = list(items)
    if not items:
        return
    print(f"\n{title} ({len(items)}):")
    for item in items:
        print(f"  - {item}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "upstream", type=Path, help="code-generated service-openapi.json"
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="dify-docs repository root",
    )
    parser.add_argument(
        "--operation-id-overrides",
        type=Path,
        default=Path(__file__).with_name("operation_id_overrides.json"),
        help="compatibility overlay for previously published operation IDs",
    )
    parser.add_argument(
        "--print-differences",
        action="store_true",
        help="print the current English wire-difference keys and fingerprints, then exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    upstream = load_json(args.upstream)
    operation_id_manifest = load_json(args.operation_id_overrides)
    operation_id_overrides = operation_id_manifest.get("operations")
    if not isinstance(operation_id_overrides, dict) or not all(
        isinstance(label, str) and isinstance(operation_id, str) and operation_id
        for label, operation_id in (operation_id_overrides or {}).items()
    ):
        raise TypeError(
            f"{args.operation_id_overrides} must contain a string-to-string operations object"
        )
    results: dict[str, tuple[list[str], dict[str, str], dict[str, int]]] = {}
    for language in LANGUAGES:
        docs_path = args.docs_root / language / "api-reference" / "openapi_service.json"
        results[language] = compare_specs(
            upstream,
            load_json(docs_path),
            operation_id_overrides,
        )

    if args.print_differences:
        print(json.dumps(results["en"][1], ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    failed = False
    for language in LANGUAGES:
        hard_errors, differences, counts = results[language]
        print(
            f"{language}: {len(operations(upstream))} operations; "
            f"hard errors={len(hard_errors)}; "
            f"wire differences={len(differences)}"
        )
        if counts:
            print(
                "  "
                + ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
            )
        print_items(f"{language} hard errors", hard_errors)
        print_items(f"{language} wire differences", differences)
        failed = failed or bool(hard_errors or differences)

    if failed:
        print("\nCONTRACT ALIGNMENT: FAILED")
        return 1
    print("\nCONTRACT ALIGNMENT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
