#!/usr/bin/env python3
"""Phase-1 Service API spec consolidation.

Merges the five per-app-type OpenAPI specs (chat, chatflow, workflow,
completion, knowledge) into one openapi_service.json per language.

Modes:
  build     Emit {lang}/api-reference/openapi_service.json for each language,
            applying resolutions.json to divergent operations. Refuses to
            build while any divergence is unresolved.

Usage:
  python3 merge_specs.py build [--lang en zh ja]

Env:
  DOCS  docs repo root (default: two levels above this file)

This script is Phase 2's pipeline skeleton: the input today is our five
hand-maintained specs; in Phase 2 it becomes R&D's generated spec plus
docs-owned overlays. Keep the merge logic input-agnostic where possible.
"""

import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(os.environ.get("DOCS", Path(__file__).resolve().parents[2]))
SPEC_NAMES = ["chat", "chatflow", "workflow", "completion", "knowledge"]
LANGS = ["en", "zh", "ja"]
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
RESOLUTIONS = Path(__file__).resolve().parent / "resolutions.json"

# Merged-spec metadata. Everything else is carried over from the inputs.
MERGED_INFO = {
    "en": {
        "title": "Dify Service API",
        "description": "REST API for Dify applications and knowledge bases. Application endpoints authenticate with an app API key; knowledge endpoints authenticate with a dataset API key.",
    },
    "zh": {
        "title": "Dify 服务 API",
        "description": "用于 Dify 应用与知识库的 REST API。应用类接口使用应用 API 密钥认证，知识库类接口使用知识库 API 密钥认证。",
    },
    "ja": {
        "title": "Dify サービス API",
        "description": "Dify アプリケーションとナレッジベースのための REST API です。アプリケーション系エンドポイントはアプリの API キーで、ナレッジ系エンドポイントはナレッジベースの API キーで認証します。",
    },
}


def load_spec(lang: str, name: str) -> dict:
    path = REPO / lang / "api-reference" / f"openapi_{name}.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def iter_ops(spec: dict):
    """Yield (path, method, op) for every operation in a spec."""
    for path, item in spec.get("paths", {}).items():
        for method, op in item.items():
            if method in HTTP_METHODS:
                yield path, method, op


def json_diff(a, b, pointer=""):
    """Recursive diff returning a list of (pointer, a_value, b_value)."""
    if type(a) is not type(b):
        return [(pointer or "/", a, b)]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            pa, pb = a.get(k, "<absent>"), b.get(k, "<absent>")
            if k not in a or k not in b:
                out.append((f"{pointer}/{k}", pa, pb))
            elif pa != pb:
                out.extend(json_diff(pa, pb, f"{pointer}/{k}"))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [(f"{pointer}/<len {len(a)} vs {len(b)}>", a, b)]
        out = []
        for i, (xa, xb) in enumerate(zip(a, b)):
            if xa != xb:
                out.extend(json_diff(xa, xb, f"{pointer}/{i}"))
        return out
    return [(pointer or "/", a, b)] if a != b else []


# ---------------------------------------------------------------------------
# Build mode
# ---------------------------------------------------------------------------

import copy
import re

OVERRIDES_DIR = Path(__file__).resolve().parent / "overrides"

# Prefix used when a colliding component must keep per-spec variants.
NAMESPACE_PREFIX = {
    "chat": "Chat",
    "chatflow": "Chatflow",
    "workflow": "Workflow",
    "completion": "Completion",
    "knowledge": "Knowledge",
}


def kebab(text: str) -> str:
    """Mintlify-style URL slug: lowercase Latin, spaces to hyphens.

    Non-ASCII characters (CJK text and full-width punctuation) are kept
    verbatim — observed behavior of the existing zh/ja page URLs, e.g.
    /api-reference/文档/获取文档嵌入状态（进度）.
    """
    out = text.strip().lower()
    out = re.sub(r"\s+", "-", out)
    out = re.sub(r"[!-,.-/:-@\[-`{-~]", "", out)  # ASCII punctuation except '-'
    out = re.sub(r"-{2,}", "-", out).strip("-")
    return out


def load_resolutions() -> dict:
    with open(RESOLUTIONS, encoding="utf-8") as f:
        return json.load(f)


def link_rewriter(linkmap: dict, prefixed: bool = False):
    """String-rewrite function for legacy /api-reference/... URLs.

    Single-pass substitution: longest alternatives first, and skip URLs that
    already carry a language prefix (re.sub never rescans its own output).
    With prefixed=True the keys carry explicit /{lang}/ prefixes themselves,
    so the language-prefix guard is dropped.
    """
    keys = sorted(linkmap, key=len, reverse=True)
    guard = "" if prefixed else r"(?<!/en)(?<!/zh)(?<!/ja)"
    pattern = re.compile(
        guard + r"(" + "|".join(re.escape(k) for k in keys) + r")"
    )

    def fix(s: str) -> str:
        if "/api-reference/" not in s:
            return s
        return pattern.sub(lambda mo: linkmap[mo.group(1)], s)

    return fix


def load_strings(lang: str) -> dict:
    with open(OVERRIDES_DIR / "strings.json", encoding="utf-8") as f:
        return json.load(f)[lang]


def load_memberships() -> dict:
    with open(Path(__file__).resolve().parent / "memberships.json", encoding="utf-8") as f:
        return json.load(f)


def walk_strings(node, fn):
    """Apply fn to every string value in a JSON tree, in place."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                node[k] = fn(v)
            else:
                walk_strings(v, fn)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                node[i] = fn(v)
            else:
                walk_strings(v, fn)


class Merger:
    def __init__(self, lang: str, resolutions: dict, en_slugs: dict):
        self.lang = lang
        self.res = resolutions
        self.en_slugs = en_slugs  # (path, method) -> "tag-slug/summary-slug"
        self.specs = {name: load_spec(lang, name) for name in SPEC_NAMES}
        self.render_changes = []  # (op/component, spec, rule)
        self.namespaced = []  # renames applied by the fixed-point pass
        self.errors = []
        self.tag_alignment = self._build_tag_alignment()
        self.op_availability = self._build_op_availability()

    def _build_tag_alignment(self) -> dict:
        """Map every tag name as it appears in this language's specs to its
        en tag name, by index-zipping each spec's en tags with its
        this-language tags (identity when self.lang == "en").
        """
        alignment = {}
        for name in SPEC_NAMES:
            en_tags = [t["name"] for t in load_spec("en", name)["tags"]]
            lang_tags = [t["name"] for t in self.specs[name].get("tags", [])]
            if len(en_tags) != len(lang_tags):
                self.errors.append(
                    f"tag alignment length mismatch in {name}: "
                    f"en={len(en_tags)} {self.lang}={len(lang_tags)}"
                )
                continue
            for en_name, lang_name in zip(en_tags, lang_tags):
                if lang_name in alignment and alignment[lang_name] != en_name:
                    self.errors.append(
                        f"tag alignment conflict in {name}: {lang_name!r} maps to "
                        f"both {alignment[lang_name]!r} and {en_name!r}"
                    )
                    continue
                alignment[lang_name] = en_name
        return alignment

    def _build_op_availability(self) -> dict:
        """{"METHOD /path": [availability names, in guides_order order]}.

        Built from memberships.json: for each app-type page in
        nav_labels.json's guides_order, non-empty availability_labels for
        this language contribute their names to every op that page lists.
        App types with empty availability_labels (e.g. Knowledge, which
        isn't an app-type page) contribute nothing.
        """
        guides_order = load_nav_labels()["guides_order"]
        pages = load_memberships()["pages"]
        availability = {}
        for name in guides_order:
            names = pages[name]["availability_labels"].get(self.lang, [])
            if not names:
                continue
            for op_key in pages[name]["ops"]:
                availability.setdefault(op_key, []).extend(names)
        return availability

    def availability_line(self, op_key):
        names = self.op_availability.get(op_key)
        if not names:
            return None
        joiner = ", " if self.lang == "en" else "、"
        return self.strings["availability_prefix"].replace("{list}", joiner.join(names))

    # -- canonical operation table (language-independent decisions) --------

    def op_occurrences(self):
        ops = {}
        for name in SPEC_NAMES:
            for path, method, op in iter_ops(self.specs[name]):
                ops.setdefault((path, method), []).append(name)
        return ops

    def lang_tag_name(self, tag: str) -> str:
        """Map a tag as it appears in this language's specs to its final name."""
        en_name = self.tag_alignment.get(tag, tag)
        return self.res.get("tag_renames", {}).get(en_name, {}).get(self.lang, tag)

    def canonical_meta(self, key):
        """(operationId, tags) for the merged op, from resolutions or first spec."""
        op_res = self.res["operations"].get(f"{key[1].upper()} {key[0]}", {})
        first = self.op_order[key][0]
        first_op = self.specs[first]["paths"][key[0]][key[1]]
        opid_source = op_res.get("operationId_from", first)
        tags_source = op_res.get("tags_from", first)
        opid = self.specs[opid_source]["paths"][key[0]][key[1]].get("operationId")
        tags = self.specs[tags_source]["paths"][key[0]][key[1]].get("tags")
        return opid, tags, first_op

    # -- link canonicalization ---------------------------------------------

    def build_linkmap(self):
        """Map every old /api-reference/... URL (this lang + en) to the new URL."""
        linkmap = {}
        for lang in {self.lang, "en"}:
            for name in SPEC_NAMES:
                spec = self.specs[name] if lang == self.lang else load_spec(lang, name)
                for path, method, op in iter_ops(spec):
                    tag = (op.get("tags") or [""])[0]
                    old = f"/api-reference/{kebab(tag)}/{kebab(op.get('summary', ''))}"
                    new = f"/{self.lang}/api-reference/{self.en_slugs[(path, method)]}"
                    if old in linkmap and linkmap[old] != new:
                        self.errors.append(f"link collision: {old} -> {linkmap[old]} vs {new}")
                    linkmap[old] = new
        return linkmap

    def canonicalize_links(self):
        fix = link_rewriter(self.build_linkmap())

        for name in SPEC_NAMES:
            walk_strings(self.specs[name], fix)

        # Any surviving unprefixed /api-reference/ link is a dangling target.
        dangling = re.compile(r"\(/api-reference/[^)]*\)")
        for name in SPEC_NAMES:
            found = dangling.findall(json.dumps(self.specs[name], ensure_ascii=False))
            for hit in set(found):
                self.errors.append(f"{name}: unmapped cross-link {hit}")

    # -- component unification ---------------------------------------------

    def unify_components(self):
        """Resolve collisions; namespace genuinely divergent components."""
        comp_res = self.res["components"]

        # Phase 1: snapshot chosen contents from pristine (pre-overwrite) specs.
        chosen_contents = {}
        for res_key, rule in comp_res.items():
            kind, comp_name = res_key.split("/", 1)
            source = rule.get("content_from") or rule.get("pick") or rule.get("custom_from")
            chosen = None
            if rule.get("superset") == "chunk-chat-event":
                chosen = self.superset_chunk_chat_event()
            elif rule.get("superset") == "chat-request":
                chosen = self.superset_chat_request()
            elif source:
                if ":" in source:
                    src_spec, src_ref = source.split(":", 1)
                    src_kind, src_name = src_ref.split("/", 1)
                else:
                    src_spec, src_kind, src_name = source, kind, comp_name
                chosen = copy.deepcopy(self.specs[src_spec]["components"][src_kind][src_name])
            if chosen is not None:
                for ptr, string_key in rule.get("set_strings", {}).items():
                    self.set_pointer(chosen, ptr, self.strings[string_key])
            chosen_contents[res_key] = chosen

        # Phase 2: overwrite variants and apply renames.
        for res_key, rule in comp_res.items():
            kind, comp_name = res_key.split("/", 1)
            chosen = chosen_contents[res_key]
            for name in SPEC_NAMES:
                comps = self.specs[name].get("components", {}).get(kind, {})
                if comp_name not in comps:
                    continue
                if chosen is not None:
                    if canon(comps[comp_name]) != canon(chosen):
                        self.note_change(f"components/{kind}/{comp_name}", name, rule)
                    comps[comp_name] = copy.deepcopy(chosen)
                new_name = rule.get("rename_to")
                if new_name:
                    comps[new_name] = comps.pop(comp_name)
                    self.rewrite_refs(self.specs[name], kind, comp_name, new_name)

        # Phase 3: fixed-point namespacing for remaining divergence.
        for _ in range(10):
            collisions = self.find_collisions()
            progressed = False
            for kind, comp_name, variants in collisions:
                keep = variants[0]  # first occurrence keeps the name
                for spec_name in variants[1:]:
                    if canon(self.get_comp(spec_name, kind, comp_name)) == canon(
                        self.get_comp(keep, kind, comp_name)
                    ):
                        continue
                    new_name = NAMESPACE_PREFIX[spec_name] + comp_name
                    comps = self.specs[spec_name]["components"][kind]
                    if new_name in comps:
                        self.errors.append(f"rename target exists: {new_name}")
                        continue
                    comps[new_name] = comps.pop(comp_name)
                    self.rewrite_refs(self.specs[spec_name], kind, comp_name, new_name)
                    self.namespaced.append(f"{kind}/{comp_name} ({spec_name}) -> {new_name}")
                    progressed = True
            if not collisions:
                return
            if not progressed:
                self.errors.append(f"unresolved collisions without progress: {collisions}")
                return
        self.errors.append("component namespacing did not converge")

    def get_comp(self, spec_name, kind, comp_name):
        return self.specs[spec_name]["components"][kind][comp_name]

    def find_collisions(self):
        seen = {}
        out = []
        for name in SPEC_NAMES:
            for kind, entries in self.specs[name].get("components", {}).items():
                for comp_name, comp in entries.items():
                    seen.setdefault((kind, comp_name), []).append((name, canon(comp)))
        for (kind, comp_name), occ in seen.items():
            if len({c for _, c in occ}) > 1:
                out.append((kind, comp_name, [n for n, _ in occ]))
        return out

    def rewrite_refs(self, spec, kind, old, new):
        old_ref = f"#/components/{kind}/{old}"
        new_ref = f"#/components/{kind}/{new}"

        def fix(s: str) -> str:
            return new_ref if s == old_ref else s

        walk_strings(spec, fix)

    # -- superset builders (POST /chat-messages and the events endpoint) ----

    def superset_chunk_chat_event(self):
        chat = copy.deepcopy(self.get_comp("chat", "schemas", "ChunkChatEvent"))
        cf = self.get_comp("chatflow", "schemas", "ChunkChatEvent")
        enum = list(cf["properties"]["event"]["enum"])
        for extra, anchor in (("agent_message", "message"), ("agent_thought", "agent_message")):
            if extra not in enum:
                enum.insert(enum.index(anchor) + 1, extra)
        merged = copy.deepcopy(cf)
        merged["properties"]["event"]["enum"] = enum
        merged["discriminator"]["mapping"] = {
            **chat["discriminator"]["mapping"],
            **cf["discriminator"]["mapping"],
        }
        return merged

    def superset_chat_request(self):
        cf = copy.deepcopy(self.get_comp("chatflow", "schemas", "ChatRequest"))
        chat = self.get_comp("chat", "schemas", "ChatRequest")
        cf["properties"]["response_mode"]["description"] = (
            chat["properties"]["response_mode"]["description"]
            + " "
            + self.strings["response_mode_new_agent_note"]
        )
        cf["properties"]["files"]["description"] += " " + self.strings["files_new_agent_note"]
        wf_id = cf["properties"]["workflow_id"]
        wf_id["description"] = self.strings["workflow_id_mode_note"] + " " + wf_id["description"]
        return cf

    def superset_chat_messages(self):
        """Single mode-aware POST /chat-messages from the chat + chatflow variants."""
        chat = self.specs["chat"]["paths"]["/chat-messages"]["post"]
        cf = self.specs["chatflow"]["paths"]["/chat-messages"]["post"]
        op = copy.deepcopy(cf)  # error responses are supersets of chat's
        op["description"] = self.strings["chat_messages_description"]
        json200 = op["responses"]["200"]["content"]["application/json"]
        json200["examples"] = copy.deepcopy(chat["responses"]["200"]["content"]["application/json"]["examples"])
        sse = op["responses"]["200"]["content"]["text/event-stream"]
        sse["schema"]["description"] = (OVERRIDES_DIR / f"chat-messages-sse.{self.lang}.md").read_text(encoding="utf-8").strip()
        chat_sse_examples = chat["responses"]["200"]["content"]["text/event-stream"]["examples"]
        merged_examples = {}
        for key, value in sse["examples"].items():
            merged_examples[key] = value
            if key == "streamingResponseBasic":
                merged_examples["streamingResponseAgent"] = copy.deepcopy(chat_sse_examples["streamingResponseAgent"])
        sse["examples"] = merged_examples
        # New Agent mode: verified against 7a4252b3de (streaming-only; agent
        # binding errors surface as 400 invalid_param).
        r400 = op["responses"]["400"]
        r400["description"] += "\n" + self.strings["chat_messages_400_new_agent_bullets"]
        r400["content"]["application/json"]["examples"].update({
            "new_agent_streaming_only": {
                "summary": "bad_request",
                "value": {"code": "bad_request", "message": "Agent App only supports streaming response mode.", "status": 400},
            },
            "new_agent_not_bound": {
                "summary": "invalid_param",
                "value": {"code": "invalid_param", "message": "Agent App has no bound Agent", "status": 400},
            },
            "new_agent_not_published": {
                "summary": "agent_not_published",
                "value": {"code": "agent_not_published", "message": "Agent has not been published. Please publish the Agent before using the API.", "status": 400},
            },
        })
        return op

    def superset_events(self):
        """Single mode-aware GET /workflow/{workflow_run_id}/events."""
        wf = self.specs["workflow"]["paths"]["/workflow/{workflow_run_id}/events"]["get"]
        cf = self.specs["chatflow"]["paths"]["/workflow/{workflow_run_id}/events"]["get"]
        op = copy.deepcopy(wf)  # workflow's wording is mode-neutral
        sse = op["responses"]["200"]["content"]["text/event-stream"]
        sse["schema"]["description"] = self.strings["events_stream_format_note"]
        sse["examples"]["resumedRun"]["summary"] = self.strings["events_example_workflow_summary"]
        cf_example = cf["responses"]["200"]["content"]["text/event-stream"]["examples"]["resumedRun"]
        merged = copy.deepcopy(cf_example)
        merged["summary"] = self.strings["events_example_chatflow_summary"]
        sse["examples"]["resumedRunChatflow"] = merged
        return op

    # -- op merge ------------------------------------------------------------

    def merge_ops(self):
        merged_paths = {}
        op_res_map = self.res["operations"]
        occurrences = self.op_occurrences()
        self.op_order = occurrences
        for name in SPEC_NAMES:
            for path, item in self.specs[name]["paths"].items():
                for method, op in item.items():
                    if method not in HTTP_METHODS:
                        self.errors.append(f"{name}: non-operation key {path}.{method}")
                        continue
                    key = (path, method)
                    if path in merged_paths and method in merged_paths[path]:
                        continue  # already merged at first occurrence
                    res = op_res_map.get(f"{method.upper()} {path}", {})
                    specs_with = occurrences[key]
                    if len(specs_with) == 1:
                        merged = copy.deepcopy(op)
                    elif res.get("superset") == "chat-messages":
                        merged = self.superset_chat_messages()
                    elif res.get("superset") == "events":
                        merged = self.superset_events()
                    elif "pick" in res:
                        merged = copy.deepcopy(
                            self.specs[res["pick"]]["paths"][path][method]
                        )
                        for ptr, string_key in res.get("set_strings", {}).items():
                            self.set_pointer(merged, ptr, self.strings[string_key])
                        for ptr, val in res.get("set_json", {}).items():
                            self.set_pointer(merged, ptr, val)
                    else:
                        # default: all occurrences must match apart from
                        # operationId and tags
                        variants = set()
                        for sname in specs_with:
                            v = copy.deepcopy(self.specs[sname]["paths"][path][method])
                            v.pop("operationId", None)
                            v.pop("tags", None)
                            variants.add(canon(v))
                        if len(variants) > 1:
                            self.errors.append(
                                f"unresolved divergence: {method.upper()} {path} in {specs_with}"
                            )
                            continue
                        merged = copy.deepcopy(op)
                    opid, tags, _ = self.canonical_meta(key)
                    merged["operationId"] = opid
                    merged["tags"] = [self.lang_tag_name(t) for t in tags]
                    line = self.availability_line(f"{method.upper()} {path}")
                    if line:
                        merged["description"] = line + "\n\n" + merged.get("description", "")
                    merged.setdefault("x-mint", {})["href"] = (
                        f"/{self.lang}/api-reference/{self.en_slugs[key]}"
                    )
                    # A custom href makes Mintlify derive the nav label from the
                    # English URL slug instead of the (translated) summary. Pin
                    # the sidebar label and page title to the summary so zh/ja
                    # operations render in their own language.
                    if merged.get("summary"):
                        merged["x-mint"].setdefault("metadata", {}).update(
                            {"title": merged["summary"], "sidebarTitle": merged["summary"]}
                        )
                    merged_paths.setdefault(path, {})[method] = merged
        return merged_paths

    # -- assembly ------------------------------------------------------------

    def note_change(self, target, spec, rule):
        self.render_changes.append((target, spec, json.dumps(rule, ensure_ascii=False)[:120]))

    def set_pointer(self, obj, pointer, value):
        parts = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/") if p]
        for part in parts[:-1]:
            obj = obj[int(part)] if isinstance(obj, list) else obj[part]
        last = parts[-1]
        if isinstance(obj, list):
            obj[int(last)] = value
        else:
            obj[last] = value

    def merged_tags(self, paths):
        """Union of tag objects; divergent descriptions default to first occurrence.

        resolutions.json 'tags' entries (keyed by the tag name in this
        language's specs) can pick a later spec's variant instead.

        Names are then remapped through tag_renames, and any tag object
        whose final name isn't carried by at least one merged op is dropped
        (e.g. the "Chatflows" tag, whose ops all merge under other tags).
        """
        tag_res = self.res["tags"]
        seen = {}
        order = []
        for name in SPEC_NAMES:
            for t in self.specs[name].get("tags", []):
                if t["name"] not in seen:
                    seen[t["name"]] = t
                    order.append(t["name"])
                elif canon(seen[t["name"]]) != canon(t):
                    pick = tag_res.get(t["name"], {}).get("pick")
                    if pick == name:
                        seen[t["name"]] = t
                    else:
                        self.note_change(f"tags/{t['name']}", name, {"default": "first occurrence"})
        used = {tag for item in paths.values() for op in item.values() for tag in op["tags"]}
        tags = []
        for n in order:
            tag = copy.deepcopy(seen[n])
            tag["name"] = self.lang_tag_name(n)
            if tag["name"] in used:
                tags.append(tag)
        return tags

    def build(self):
        self.strings = load_strings(self.lang)
        self.canonicalize_links()
        self.pristine = copy.deepcopy(self.specs)
        self.op_order = self.op_occurrences()
        self.unify_components()
        paths = self.merge_ops()
        components = {}
        for name in SPEC_NAMES:
            for kind, entries in self.specs[name].get("components", {}).items():
                bucket = components.setdefault(kind, {})
                for comp_name, comp in entries.items():
                    if comp_name in bucket and canon(bucket[comp_name]) != canon(comp):
                        self.errors.append(f"residual collision {kind}/{comp_name} from {name}")
                    bucket.setdefault(comp_name, comp)
        tags = self.merged_tags(paths)
        base = self.specs["chat"]
        servers = copy.deepcopy(base["servers"])
        servers[0]["description"] = self.strings["server_description"]
        merged = {
            "openapi": base["openapi"],
            "info": {**MERGED_INFO[self.lang], "version": "1.0.0"},
            "servers": servers,
            "security": base["security"],
            "tags": tags,
            "paths": paths,
            "components": components,
        }
        # Every cross-reference must carry a language prefix by now.
        stale = re.findall(r"\(/api-reference/[^)]*\)", json.dumps(merged, ensure_ascii=False))
        for hit in sorted(set(stale)):
            self.errors.append(f"unprefixed cross-link in merged spec: {hit}")
        if self.errors:
            for e in self.errors:
                print(f"ERROR [{self.lang}]: {e}")
            sys.exit(1)
        return merged


def resolve_tree(node, components, stack=frozenset()):
    """Dereference $refs recursively so trees compare by rendered content."""
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str) and node["$ref"].startswith("#/components/"):
            ref = node["$ref"]
            if ref in stack:
                return "<recursion>"
            _, _, kind, name = ref.split("/")
            target = components.get(kind, {}).get(name)
            if target is None:
                return f"<dangling:{ref}>"
            resolved = resolve_tree(target, components, stack | {ref})
            extra = {k: v for k, v in node.items() if k != "$ref"}
            if extra and isinstance(resolved, dict):
                resolved = {**resolved, **resolve_tree(extra, components, stack)}
            return resolved
        return {k: resolve_tree(v, components, stack) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve_tree(v, components, stack) for v in node]
    return node


def verify_rendering(merger, merged, report_lines):
    """Diff every op's dereferenced tree: merged spec vs each source spec."""
    p = report_lines.append
    for name in SPEC_NAMES:
        spec = merger.pristine[name]
        comps = spec.get("components", {})
        for path, method, op in iter_ops(spec):
            merged_op = merged["paths"][path][method]
            a = copy.deepcopy(op)
            b = copy.deepcopy(merged_op)
            for v in (a, b):
                v.pop("operationId", None)
                v.pop("tags", None)
                v.pop("x-mint", None)
            line = merger.availability_line(f"{method.upper()} {path}")
            if line and isinstance(b.get("description"), str) and b["description"].startswith(line):
                b["description"] = b["description"][len(line):].lstrip("\n")
            diffs = json_diff(
                resolve_tree(a, comps), resolve_tree(b, merged["components"])
            )
            if diffs:
                p(f"### {method.upper()} {path} (vs {name}): {len(diffs)} pointers")
                for ptr, va, vb in diffs:
                    p(f"- `{ptr}`")
                    p(f"    - {name}: {canon(va)[:180]}")
                    p(f"    - merged: {canon(vb)[:180]}")


def compute_en_slugs(resolutions: dict) -> dict:
    """Canonical language-independent URL slugs from the en specs."""
    specs = {name: load_spec("en", name) for name in SPEC_NAMES}
    slugs, seen = {}, {}
    ops = {}
    for name in SPEC_NAMES:
        for path, method, op in iter_ops(specs[name]):
            ops.setdefault((path, method), []).append((name, op))
    renames = resolutions.get("tag_renames", {})
    for key, occ in ops.items():
        res = resolutions["operations"].get(f"{key[1].upper()} {key[0]}", {})
        tags_source = res.get("tags_from", occ[0][0])
        op = dict(occ)[tags_source]
        tag_en = renames.get(op["tags"][0], {}).get("en", op["tags"][0])
        slug = f"{kebab(tag_en)}/{kebab(op['summary'])}"
        if slug in seen and seen[slug] != key:
            sys.exit(f"slug collision: {slug} for {seen[slug]} and {key}")
        seen[slug] = key
        slugs[key] = slug
    return slugs


def build_all(langs, report_dir: Path | None = None):
    resolutions = load_resolutions()
    en_slugs = compute_en_slugs(resolutions)
    for lang in langs:
        merger = Merger(lang, resolutions, en_slugs)
        merged = merger.build()
        out = REPO / lang / "api-reference" / "openapi_service.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
            f.write("\n")
        if report_dir:
            lines = [f"# Rendered-content changes — {lang}", ""]
            verify_rendering(merger, merged, lines)
            report = report_dir / f"render_diff_{lang}.md"
            report.write_text("\n".join(lines), encoding="utf-8")
            print(f"[{lang}] render diff report: {report}")
        n_ops = sum(1 for _ in iter_ops(merged))
        print(f"[{lang}] wrote {out.relative_to(REPO)}: {n_ops} operations, "
              f"{sum(len(v) for v in merged['components'].values())} components")
        for entry in merger.namespaced:
            print(f"  namespaced: {entry}")
        for target, spec, rule in merger.render_changes:
            print(f"  render change: {target} (from {spec}) rule={rule}")


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
    merged = json.load(open(REPO / lang / "api-reference" / "openapi_service.json", encoding="utf-8"))
    en_merged = json.load(open(REPO / "en" / "api-reference" / "openapi_service.json", encoding="utf-8"))
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


def relink(langs):
    """Rewrite legacy /api-reference/... links in MDX bodies to the new URLs.

    Links in a page map to that page's own language, so readers stay in it.
    Language-prefixed URLs written under earlier slug schemes (before a tag
    rename in resolutions.json) are remapped to the current slugs as well.
    """
    resolutions = load_resolutions()
    en_slugs = compute_en_slugs(resolutions)
    pre_rename = {k: v for k, v in resolutions.items() if k != "tag_renames"}
    old_en_slugs = compute_en_slugs(pre_rename)
    for lang in langs:
        linkmap = {}
        for src_lang in {lang, "en"}:
            for name in SPEC_NAMES:
                spec = load_spec(src_lang, name)
                for path, method, op in iter_ops(spec):
                    tag = (op.get("tags") or [""])[0]
                    old = f"/api-reference/{kebab(tag)}/{kebab(op.get('summary', ''))}"
                    linkmap[old] = f"/{lang}/api-reference/{en_slugs[(path, method)]}"
        prefixed_map = {
            f"/{lang}/api-reference/{old_en_slugs[key]}":
                f"/{lang}/api-reference/{slug}"
            for key, slug in en_slugs.items()
            if old_en_slugs[key] != slug
        }
        fix = link_rewriter(linkmap)
        fix_prefixed = link_rewriter(prefixed_map, prefixed=True) if prefixed_map else (lambda s: s)
        changed = 0
        for mdx in sorted((REPO / lang).rglob("*.mdx")):
            text = mdx.read_text(encoding="utf-8")
            if "/api-reference/" not in text:
                continue
            new_text = fix_prefixed(fix(text))
            if new_text != text:
                mdx.write_text(new_text, encoding="utf-8")
                changed += 1
        print(f"[{lang}] relinked {changed} MDX files")


def check_coverage(langs):
    memberships = load_memberships()
    failures = []
    for lang in langs:
        merged = json.load(open(REPO / lang / "api-reference" / "openapi_service.json", encoding="utf-8"))
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
    ap.add_argument("mode", choices=["build", "wire", "relink", "check-coverage"])
    ap.add_argument("--lang", nargs="*", default=["en"])
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args()

    if args.mode == "build":
        build_all(args.lang, args.report)
    elif args.mode == "wire":
        wire(args.lang)
    elif args.mode == "relink":
        relink(args.lang)
    elif args.mode == "check-coverage":
        check_coverage(args.lang)


if __name__ == "__main__":
    main()
