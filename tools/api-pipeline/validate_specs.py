#!/usr/bin/env python3
"""Validate OpenAPI documents and examples on media, parameters, and schemas.

Run with: uvx --from openapi-spec-validator==0.9.0 python tools/api-pipeline/validate_specs.py
"""

import json
from pathlib import Path
from urllib.parse import unquote

from jsonschema import Draft202012Validator
from openapi_spec_validator import OpenAPIV31SpecValidator
from referencing.exceptions import Unresolvable

from build_specs import object_role, parts_of, pointer

ROOT = Path(__file__).resolve().parents[2]


def objects(node, parts=()):
    """Visit typed OpenAPI/Schema objects, never enum/default/example data."""
    role = object_role(parts)
    if role == "literal":
        return
    if isinstance(node, dict):
        yield parts, role, node
        for key, value in node.items():
            yield from objects(value, (*parts, key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from objects(value, (*parts, str(index)))


def resolve_example(spec, example, location):
    """Resolve local Example Object references and retain their source pointer."""
    seen = set()
    while isinstance(example, dict) and "$ref" in example:
        ref = example["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise ValueError(f"cannot validate external example reference: {ref}")
        if ref in seen:
            raise ValueError(f"cyclic example reference: {ref}")
        seen.add(ref)
        location = tuple(parts_of(unquote(ref[1:])))
        example = spec
        try:
            for part in location:
                example = example[int(part)] if isinstance(example, list) else example[part]
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError(f"example reference does not exist: {ref}") from error
    if not isinstance(example, dict):
        raise ValueError("example reference must identify an Example Object")
    return example, location


def examples(spec, node, role, location):
    if "example" in node:
        yield (*location, "example"), node["example"]
    if role == "schema":
        for index, value in enumerate(node.get("examples", [])):
            yield (*location, "examples", str(index)), value
    else:
        for name, example in node.get("examples", {}).items():
            source = (*location, "examples", name)
            example, source = resolve_example(spec, example, source)
            if "value" in example:
                yield (*source, "value"), example["value"]
            elif "externalValue" in example:
                raise ValueError(f"cannot validate external example value at #{pointer(source)}; inline its value")


def validate_examples(spec):
    """Return the example count and failures, with pointers to editable values."""
    root_validator = Draft202012Validator(spec)
    count, errors = 0, []
    for location, role, node in objects(spec):
        if role == "schema":
            schema = node
        elif role == "media" or (role in {"parameter", "header"} and "schema" in node):
            schema = node.get("schema", {})
        else:
            continue
        # Evolving the validator preserves its document root for local $refs,
        # and also supports boolean schemas such as a media schema of false.
        validator = root_validator.evolve(schema=schema)
        try:
            for source, value in examples(spec, node, role, location):
                count += 1
                for error in validator.iter_errors(value):
                    instance_path = pointer(error.absolute_path)
                    errors.append(f"#{pointer(source)}{instance_path}: {error.message}")
        except (ValueError, Unresolvable) as error:
            errors.append(f"#{pointer(location)}: {error}")
    return count, errors


def validate(path):
    spec = json.loads(path.read_text(encoding="utf-8"))
    errors = [str(error) for error in OpenAPIV31SpecValidator(spec).iter_errors()]
    count = 0
    if not errors:
        count, errors = validate_examples(spec)
    print(f"{path.relative_to(ROOT)}: {count} examples, {len(errors)} errors")
    for error in errors:
        print(error)
    return len(errors)


def main():
    paths = [ROOT / "tools/api-pipeline/upstream/service-openapi.json"]
    paths += [ROOT / lang / "api-reference/openapi_service.json" for lang in ("en", "zh", "ja")]
    total = sum(validate(path) for path in paths)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
