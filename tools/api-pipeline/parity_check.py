"""Check the complete API contract and language-switcher URLs across languages."""

import json
import os
import sys
from pathlib import Path

from build_specs import contract, operations

DOCS = Path(os.environ.get("DOCS", Path(__file__).resolve().parents[2]))


def load(lang):
    return json.loads((DOCS / lang / "api-reference" / "openapi_service.json").read_text())


def differences(left, right, path=""):
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(left.keys() | right.keys()):
            if key not in left or key not in right:
                yield f"{path}/{key}: missing or extra key"
            else:
                yield from differences(left[key], right[key], f"{path}/{key}")
    elif isinstance(left, list) and isinstance(right, list) and len(left) == len(right):
        for i, (a, b) in enumerate(zip(left, right)):
            yield from differences(a, b, f"{path}/{i}")
    elif left != right:
        yield f"{path}: {left!r} != {right!r}"


def main():
    total = 0
    try:
        english = load("en")
        for lang in ("zh", "ja"):
            translated = load(lang)
            issues = list(differences(contract(english), contract(translated)))
            en_ops, translated_ops = dict(operations(english)), dict(operations(translated))
            for key in en_ops.keys() & translated_ops.keys():
                expected = en_ops[key].get("x-mint", {}).get("href", "").replace("/en/", f"/{lang}/", 1)
                actual = translated_ops[key].get("x-mint", {}).get("href")
                if expected != actual:
                    issues.append(f"{key}: language-switcher URL differs: {expected!r} != {actual!r}")
            for issue in issues:
                print(f"{lang}: {issue}")
            total += len(issues)
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}")
        total += 1
    print(f"TOTAL PARITY ISSUES: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
