"""Diff the code-generated flask-restx swagger against the documented en specs.

Disagreements are flags for Tier 1 investigation, not verdicts: the restx doc
decorators are themselves hand-maintained.
"""

import glob
import json
import os
import re
import urllib.request
from collections import defaultdict

DOCS = os.environ["DOCS"]
SWAGGER_URL = os.environ.get("SWAGGER_URL", "http://localhost:15001/v1/swagger.json")


def blank(p):
    return re.sub(r"\{[^}]+\}", "{}", p)


swagger = json.load(urllib.request.urlopen(SWAGGER_URL, timeout=20))
print(f"swagger version: {swagger.get('swagger') or swagger.get('openapi')}, paths: {len(swagger['paths'])}")

code_ops = {}
for p, ms in swagger["paths"].items():
    for m, op in ms.items():
        if m not in ("get", "post", "put", "patch", "delete"):
            continue
        params = {}
        for prm in op.get("parameters", []) or []:
            if prm.get("in") in ("query", "path"):
                params[(prm["name"], prm["in"])] = bool(prm.get("required"))
        code_ops[(blank(p), m)] = {
            "path": p,
            "params": params,
            "responses": set((op.get("responses") or {}).keys()),
            "deprecated": bool(op.get("deprecated")),
        }

spec_ops = {}
for f in sorted(glob.glob(f"{DOCS}/en/api-reference/openapi_*.json")):
    spec = json.load(open(f))
    name = f.split("/")[-1]
    for p, ms in spec["paths"].items():
        for m, op in ms.items():
            if m not in ("get", "post", "put", "patch", "delete"):
                continue
            params = {}
            for prm in op.get("parameters", []) or []:
                if prm.get("in") in ("query", "path"):
                    params[(prm["name"], prm["in"])] = bool(prm.get("required"))
            key = (blank(p), m)
            e = spec_ops.setdefault(key, {"path": p, "params": {}, "responses": set(), "specs": []})
            e["params"].update(params)
            e["responses"] |= set((op.get("responses") or {}).keys())
            e["specs"].append(name)

shared = sorted(set(code_ops) & set(spec_ops))
print(f"shared operations: {len(shared)}\n")

n = 0
for key in shared:
    c, s = code_ops[key], spec_ops[key]
    msgs = []
    c_q = {name for (name, loc) in c["params"] if loc == "query"}
    s_q = {name for (name, loc) in s["params"] if loc == "query"}
    only_code = c_q - s_q
    only_spec = s_q - c_q
    if only_code:
        msgs.append(f"query params in code-swagger but not documented: {sorted(only_code)}")
    if only_spec:
        msgs.append(f"query params documented but not in code-swagger: {sorted(only_spec)}")
    for pk in sorted(set(c["params"]) & set(s["params"])):
        if c["params"][pk] != s["params"][pk]:
            msgs.append(f"required mismatch on {pk}: code={c['params'][pk]} spec={s['params'][pk]}")
    resp_only_spec = {r for r in s["responses"] if r not in c["responses"] and r != "default"}
    resp_only_code = {r for r in c["responses"] if r not in s["responses"] and r != "default"}
    if resp_only_code:
        msgs.append(f"status codes in code-swagger not documented: {sorted(resp_only_code)}")
    if resp_only_spec:
        msgs.append(f"status codes documented, absent from code-swagger: {sorted(resp_only_spec)}")
    if msgs:
        n += len(msgs)
        print(f"== {key[1].upper()} {s['path']}   ({', '.join(sorted(set(s['specs'])))})")
        for msg in msgs:
            print("   -", msg)

print(f"\nTOTAL FLAGS: {n}")
