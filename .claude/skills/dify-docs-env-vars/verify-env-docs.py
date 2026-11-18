#!/usr/bin/env python3
"""
Verify Dify environment variable documentation against the Docker env files.

Since Dify 1.19.0 the Docker deployment splits its settings across three kinds of file,
and the verifier gives each the role it plays in a stock installation (`docker/.env.example`
copied to `.env`, nothing else changed):

- `docker/.env.example`: copied to `.env`, so its active lines are stock values and win
  over everything below.
- `docker/envs/**/*.defaults`: loaded automatically. A line such as `FOO=${FOO-x}` keeps an
  earlier value and otherwise supplies `x`. A line that copies another setting
  (`WORKER_TIMEOUT=${SANDBOX_WORKER_TIMEOUT:-15}`, the "Container variable mappings") is not a
  setting of its own: the variable it copies from is recorded, with the fallback as its default.
- `docker/envs/**/*.env.example`: optional templates a stock installation does not create.
  Their variables are documentable, but none of their values is a default.

A commented line (`# FOO=bar`) in any of these files names a documentable variable but sets
nothing, so its value is never used as the default. A variable that only commented lines or
templates name has no default in these files; its default is the application's, which the
script does not resolve.

Usage:
    # Verify mode: docs vs the env files on disk (a directory is globbed recursively for
    # *.env.example and *.defaults)
    python3 verify-env-docs.py --env-example PATH [--env-example PATH ...] --compose DIR --docs PATH

    # Release diff mode: which vars were added/removed/changed between two refs, and
    # which NEW ones are still undocumented. Run this every release sync.
    python3 verify-env-docs.py --compare-rev OLD NEW --repo /path/to/dify [--docs PATH]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple


# --- Compose-style expansions ---------------------------------------------------------

_EXPANSION_BODY_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)(?:(:?[-?+])(.*))?\Z", re.S)
_REF_NAME_RE = re.compile(r"[A-Z][A-Z0-9_]*\Z")


def _closing_brace(text: str, start: int) -> int:
    """Index of the `}` closing the expansion whose body starts at `start`, or -1."""
    depth = 1
    i = start
    while i < len(text):
        if text.startswith("${", i):
            depth += 1
            i += 2
            continue
        if text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def iter_expansions(text: str) -> Iterator[Tuple[str, Optional[str], Optional[str]]]:
    """Yield (name, operator, operand) for every ${...} expansion in text, nested ones
    included. The operator is one of ":-", "-", ":?", "?", ":+", "+", or None for a bare
    ${NAME}. `$${...}` is compose's escape for a literal `$` (a shell variable inside a
    command) and is skipped, and so is a `${` that never closes, such as one in a comment."""
    i = 0
    while True:
        j = text.find("${", i)
        if j < 0:
            return
        i = j + 2  # keep scanning inside, so nested expansions are reported too
        if j > 0 and text[j - 1] == "$":
            continue
        end = _closing_brace(text, j + 2)
        if end < 0:
            continue
        m = _EXPANSION_BODY_RE.match(text[j + 2:end])
        if m:
            yield m.group(1), m.group(2), m.group(3)


def interpolate(value: str, env: Optional[Dict[str, str]] = None) -> str:
    """Resolve ${NAME}, ${NAME-x} and ${NAME:-x} the way Compose does, against `env`
    (the variables already set; anything absent is unset). `-` falls back only when the
    variable is unset, `:-` also when it is empty, and an unset bare ${NAME} is "".
    `+` and `:+` give their operand only when the variable is set; `?` and `:?` give the
    value or nothing. `$$` is a literal `$`."""
    env = env or {}
    out: List[str] = []
    i = 0
    while i < len(value):
        if value.startswith("$$", i):
            out.append("$")
            i += 2
            continue
        if not value.startswith("${", i):
            out.append(value[i])
            i += 1
            continue
        end = _closing_brace(value, i + 2)
        m = _EXPANSION_BODY_RE.match(value[i + 2:end]) if end >= 0 else None
        if not m:
            out.append(value[i:])
            break
        name, op, operand = m.group(1), m.group(2), m.group(3)
        is_set = name in env and not (op and op.startswith(":") and env[name] == "")
        if op in ("+", ":+"):
            out.append(interpolate(operand, env) if is_set else "")
        elif is_set:
            out.append(env[name])
        elif op in ("-", ":-"):
            out.append(interpolate(operand, env))
        i = end + 1
    return "".join(out)


def resolve_expansion(value: str) -> str:
    """The value a compose-style expression takes when nothing it refers to is set."""
    return interpolate(value.strip())


def collect_refs(text: str, found: Dict[str, str]) -> None:
    """Record every variable a ${...} expression in text refers to, with the value its
    fallback resolves to when nothing is set. Only `-` and `:-` operands are fallbacks;
    the other operators still name the variable. A name already recorded keeps its value
    unless that value is empty and this one is not."""
    for name, op, operand in iter_expansions(text):
        if not _REF_NAME_RE.match(name):
            continue
        value = resolve_expansion(operand) if op in ("-", ":-") and operand else ""
        if name not in found or (not found[name] and value):
            found[name] = value


# --- Env files ------------------------------------------------------------------------

ROLE_TEMPLATE = "optional template: names only"
ROLE_DEFAULTS = "tracked defaults"
ROLE_STOCK = "stock .env"
_ROLE_ORDER = {ROLE_TEMPLATE: 0, ROLE_DEFAULTS: 1, ROLE_STOCK: 2}


def env_file_role(name: str) -> Optional[str]:
    """The part a file plays in a stock installation, from its file name.
    `.env.example` is the one copied to `.env`; `*.defaults` load automatically;
    any other `*.env.example` is an optional template nobody has created."""
    if name == ".env.example":
        return ROLE_STOCK
    if name.endswith(".defaults"):
        return ROLE_DEFAULTS
    if name.endswith(".env.example"):
        return ROLE_TEMPLATE
    return None


def order_env_paths(paths: List[str]) -> List[str]:
    """Keep the env files among `paths` and put them in merge order: templates (which
    set nothing), then tracked defaults, then the stock `.env` last."""
    files = [p for p in paths if env_file_role(Path(p).name)]
    return sorted(files, key=lambda p: (_ROLE_ORDER[env_file_role(Path(p).name)], p))


_ACTIVE_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*)=(.*)$")
_COMMENTED_RE = re.compile(r"^#\s*([A-Z][A-Z0-9_]+)=(.*)$")
_VAR_NAME_RE = re.compile(r"[A-Z][A-Z0-9_]+\Z")


def classify_env_line(line: str) -> Optional[Tuple[str, str, str]]:
    """Return (kind, name, value) for an env-file line, or None for anything else.

    kind is "commented" for `# FOO=bar`, "mapping" for an active line whose value copies
    another setting (`TARGET=${SOURCE:-x}`, including composite values such as
    `-Xms${MIN:-512m}`), and "set" for the rest: a literal, or an expression that starts
    from the variable itself (`FOO=${FOO-x}`)."""
    s = line.strip()
    if not s:
        return None
    m = _COMMENTED_RE.match(s)
    if m:
        return "commented", m.group(1), m.group(2).strip()
    if s.startswith("#"):
        return None
    m = _ACTIVE_RE.match(s)
    if not m:
        return None
    name, value = m.group(1), m.group(2).strip()
    if "${" in value and not re.match(r"\$\{" + re.escape(name) + r"(?::?[-?+]|\})", value):
        return "mapping", name, value
    return "set", name, value


class EnvSurface:
    """What the env files say about each variable: whether it exists, and the value a
    stock installation runs with when the files set one."""

    def __init__(self) -> None:
        self.names: Dict[str, str] = {}               # variable -> the file that matters most
        self._rank: Dict[str, int] = {}               # role rank of that file
        self.stock: Dict[str, str] = {}               # active lines of the stock .env
        self.tracked: Dict[str, List[Tuple[str, str]]] = {}  # variable -> [(value, file)]
        self.fallbacks: Dict[str, str] = {}           # variable -> fallback of a ${...} ref
        self.mapped: Dict[str, List[Tuple[str, str]]] = {}   # container variable -> [(expr, file)]

    def _name(self, name: str, label: str, role: str) -> None:
        """Record a variable, pointing at the most authoritative file that names it."""
        rank = _ROLE_ORDER[role]
        if name not in self.names or rank > self._rank[name]:
            self.names[name] = label
            self._rank[name] = rank

    def add_text(self, lines, label: str, role: str) -> None:
        refs: Dict[str, str] = {}
        for line in lines:
            parsed = classify_env_line(line)
            if not parsed:
                continue
            kind, name, value = parsed
            is_var = bool(_VAR_NAME_RE.match(name))
            if kind == "commented":
                self._name(name, label, role)
                continue
            if role == ROLE_TEMPLATE:
                # Nothing in a template takes effect, but every variable it names exists.
                if is_var:
                    self._name(name, label, role)
                for ref in iter_expansions(value):
                    if _REF_NAME_RE.match(ref[0]):
                        self._name(ref[0], label, role)
                continue
            if kind == "mapping" and role == ROLE_DEFAULTS:
                # A container variable copied from another setting: the copied-from
                # variable is the setting, and the fallback is its default. The container
                # variable may be documented (setting it has no effect, so its row points
                # at the setting), but it is not a setting to require.
                collect_refs(value, refs)
                if is_var:
                    self.mapped.setdefault(name, []).append((value, label))
                continue
            collect_refs(value, refs)  # names nested inside the expression
            if not is_var:
                continue
            self._name(name, label, role)
            if role == ROLE_STOCK:
                self.stock[name] = value
            else:
                self.tracked.setdefault(name, []).append((value, label))
        for name, value in refs.items():
            self._name(name, label, role)
            if name not in self.fallbacks or (not self.fallbacks[name] and value):
                self.fallbacks[name] = value

    def add_compose(self, compose_vars: Dict[str, str]) -> List[str]:
        """Add compose ${VAR} references: names no env file has, and fallbacks for names
        without one. Returns the compose-only names."""
        only = sorted(n for n in compose_vars if n not in self.names)
        for name in only:
            self.names[name] = "compose"
            self._rank[name] = -1
        for name, value in compose_vars.items():
            if name not in self.fallbacks or (not self.fallbacks[name] and value):
                self.fallbacks[name] = value
        return only

    def stock_env(self) -> Dict[str, str]:
        return {n: interpolate(v) for n, v in self.stock.items()}

    def mapped_only(self) -> List[str]:
        """Container variables that only mapping lines set."""
        return sorted(n for n in self.mapped if n not in self.names)

    def defaults(self) -> Dict[str, Tuple[List[str], str]]:
        """variable -> (values, where from) for every variable the files give a default.

        The stock `.env` wins. Otherwise each tracked-defaults line is resolved against the
        stock `.env`; files may disagree because each service or vector store loads its own
        (`OCEANBASE_VECTOR_HOST` is `oceanbase` or `seekdb`), so every distinct value is kept.
        Otherwise the fallback of a ${...} reference applies, and for a container variable
        that only mapping lines set, the value those lines resolve to. Variables that only
        commented lines or templates name are absent: the files set no default for them."""
        env = self.stock_env()

        def resolved(lines: List[Tuple[str, str]]) -> Tuple[List[str], str]:
            values: List[str] = []
            where: List[str] = []
            for raw, label in lines:
                v = interpolate(raw, env)
                if v not in values:
                    values.append(v)
                if label not in where:
                    where.append(label)
            return values, ", ".join(where)

        out: Dict[str, Tuple[List[str], str]] = {}
        for name in self.names:
            if name in env:
                out[name] = ([env[name]], "stock .env")
            elif name in self.tracked:
                out[name] = resolved(self.tracked[name])
            elif name in self.fallbacks:
                out[name] = ([self.fallbacks[name]], "fallback of a ${...} reference")
        for name in self.mapped_only():
            out[name] = resolved(self.mapped[name])
        return out


def collect_env_files(sources: List[str]) -> List[Path]:
    """Resolve each source (file or directory) into env files, in merge order.
    A directory is globbed recursively for `*.env.example`, `.env.example` and `*.defaults`."""
    found: List[Path] = []
    seen = set()
    for source in sources:
        p = Path(source)
        if not p.exists():
            print(f"ERROR: env source not found: {source}", file=sys.stderr)
            sys.exit(1)
        candidates = [p]
        if p.is_dir():
            candidates = []
            for pattern in ("*.env.example", ".env.example", "*.defaults"):
                candidates.extend(sorted(p.rglob(pattern)))
        for f in candidates:
            if f not in seen and env_file_role(f.name):
                seen.add(f)
                found.append(f)
    by_text = {str(f): f for f in found}
    return [by_text[t] for t in order_env_paths(list(by_text))]


def parse_env_sources(sources: List[str]) -> Tuple[EnvSurface, List[Path]]:
    """Parse every env file reachable from the sources. Files are labelled by their path
    below the directory they share (`envs/core-services/api.defaults`)."""
    files = collect_env_files(sources)
    base = os.path.commonpath([str(f.parent) for f in files]) if files else ""
    surface = EnvSurface()
    for f in files:
        with open(f, encoding="utf-8") as fh:
            surface.add_text(fh, os.path.relpath(f, base), env_file_role(f.name))
    return surface, files


# --- Ignore list and docs -------------------------------------------------------------

def parse_ignored_vars(path: str) -> set:
    """Parse the ignored-vars markdown file and return the set of ignored names.

    Table rows beginning with a backticked variable name in the first cell register an
    ignore entry.
    The header row `| Variable | ...` is skipped naturally because it isn't backticked.
    """
    ignored = set()
    text = _read_ignored_text(path)
    for line in text.splitlines():
        match = re.match(r"^\|\s*`([A-Z][A-Z0-9_]+)`\s*\|", line)
        if match:
            ignored.add(match.group(1))
    return ignored


def _read_ignored_text(path: str) -> str:
    """Read the ignore list, falling back to the registry's committed copy.

    The registry clone is shared and often sits on another branch, so the file can be
    absent from its working tree while present on `origin/main`. Reading the committed
    copy keeps the ignore list from silently parsing as empty, which would report every
    ignored variable as missing documentation.
    """
    target = Path(path)
    if target.exists():
        return target.read_text(encoding="utf-8")
    for parent in target.parents:
        if (parent / ".git").exists():
            rel = target.relative_to(parent).as_posix()
            result = subprocess.run(
                ["git", "-C", str(parent), "show", f"origin/main:{rel}"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                print(f"(ignore list not in the working tree; read origin/main:{rel})")
                return result.stdout
            break
    # An empty ignore set would let a run end on ALL CHECKS PASSED by accident, so the
    # run is invalid rather than noisy: stop here instead of reporting against nothing.
    msg = (f"WARNING: ignore list not found at {path} and no committed copy could be read; "
           "the run is invalid. Set DIFY_DOCS_REGISTRY or pass --ignored.")
    print(msg)
    print(msg, file=sys.stderr)
    sys.exit(2)


def _doc_values(raw: str) -> str:
    """The default a table cell or Default: line states."""
    bt = re.match(r"^`(.*)`$", raw)
    if bt:
        return bt.group(1)
    if raw.startswith(("(", "（")):
        # (empty), (empty; falls back to...), (auto-generated), etc.
        # zh/ja pages write these with full-width parentheses: （空）
        return ""
    return raw


def parse_mdx_docs(path: str) -> Dict[str, str]:
    """Parse MDX documentation and extract documented defaults.

    Handles two formats:
    1. Table rows: | `VARIABLE` | `value` | description |
    2. Heading + Default line:
       ### VARIABLE
       Default: `value`
    """
    variables: Dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Format 1: Table rows — | `VAR_NAME` | `default` | description |
        table_match = re.match(
            r"^\|\s*`([A-Z][A-Z0-9_]+)`\s*\|\s*(.*?)\s*\|", line
        )
        if table_match:
            variables[table_match.group(1)] = _doc_values(table_match.group(2).strip())
            i += 1
            continue

        # Format 2: ### VARIABLE_NAME followed by Default: `value`
        heading_match = re.match(r"^###\s+([A-Z][A-Z0-9_]+)\s*$", line)
        if heading_match:
            name = heading_match.group(1)
            # Look ahead for "Default:" line within next 5 lines
            for j in range(1, 6):
                if i + j >= len(lines):
                    break
                next_line = lines[i + j].strip()
                if not next_line:
                    continue
                # en "Default:", zh "默认值：", ja "デフォルト値："
                default_match = re.match(r"^(?:Default|默认值|デフォルト値)\s*[:：]\s*(.+)", next_line)
                if default_match:
                    raw = default_match.group(1).strip()
                    # The first value is the Docker Compose one:
                    # Default: `true` on Docker Compose; `false` on source deployments
                    bt = re.match(r"^`([^`]*)`", raw)
                    variables[name] = bt.group(1) if bt else _doc_values(raw)
                    break
                # Stop if we hit content that's not the default line
                if next_line.startswith("#") or next_line.startswith("|"):
                    break
            i += 1
            continue

        i += 1

    return variables


PLACEHOLDER_PATTERNS = [
    "your-", "your_", "YOUR-", "YOUR_",
    "xxx", "difyai", "dify-sandbox",
    "sk-9f73s", "lYkiYYT6", "QaHbTe77",
    "testaccount", "testpassword", "difypassword",
    "gp-test.", "gp-ab",
    "instance-name",
    "WVF5YTha",
]

PLACEHOLDER_EXACT = {
    "dify", "password", "admin",
}

PLACEHOLDER_CONTAINS = [
    "your-object-storage",
    "xxx-vector",
]


def is_placeholder(value: str) -> bool:
    """Check if a value is a placeholder (not a real default)."""
    v = value.strip()
    if v in PLACEHOLDER_EXACT:
        return True
    for pattern in PLACEHOLDER_PATTERNS:
        if v.startswith(pattern):
            return True
    for pattern in PLACEHOLDER_CONTAINS:
        if pattern in v:
            return True
    return False


def normalize(value: str) -> str:
    """Normalize a value for comparison."""
    v = resolve_expansion(value).strip().strip('"').strip("'")
    # Normalize boolean representations
    if v.lower() in ("true", "yes", "1"):
        return "true"
    if v.lower() in ("false", "no", "0"):
        return "false"
    # Normalize empty
    if v in ("null", "None", "none", ""):
        return ""
    # Treat placeholder values as empty (they're not real defaults)
    if is_placeholder(v):
        return ""
    return v


def matches_default(doc_value: str, values: List[str]) -> bool:
    """A documented default matches when it states the stock value. Where the files that
    different services or vector stores load disagree, the cell must list every value,
    one per store (`oceanbase` / `seekdb`)."""
    expected = {normalize(v) for v in values}
    stated = {normalize(p) for p in re.split(r"`\s*/\s*`", doc_value)}
    return stated == expected


def _default_ignored_path() -> Path:
    """The ignore list lives in the private registry: its entries name unreleased work.
    Resolve $DIFY_DOCS_REGISTRY first, then a sibling clone of this repo. When neither
    is present the list parses as empty and every variable is reported, which is the
    safe direction."""
    registry = os.environ.get("DIFY_DOCS_REGISTRY")
    if registry:
        return Path(registry) / "guides" / "env-ignored-vars.md"
    docs_root = Path(__file__).resolve().parents[3]
    return docs_root.parent / "dify-docs-registry" / "guides" / "env-ignored-vars.md"


DEFAULT_IGNORED_PATH = _default_ignored_path()


# --- Compose files --------------------------------------------------------------------

def parse_compose_text(text: str) -> Dict[str, str]:
    """Collect ${VAR}, ${VAR-fallback} and ${VAR:-fallback} references from a compose file.

    A compose file can consume a variable that has no env-file entry at all; such a
    variable is invisible to every env-file-based check (EXPOSE_WEAVIATE_GRPC_PORT went
    unseen for eleven months this way). The value recorded is what the fallback resolves to
    when nothing is set.
    """
    found: Dict[str, str] = {}
    collect_refs(text, found)
    return found


def is_test_compose(name: str) -> bool:
    """docker/docker-compose.pytest.ports.yaml publishes vector-store ports for the
    integration tests; nothing a deployment reads. Skipped whether it arrives via a
    directory glob, an explicit path, or a git ref."""
    return "pytest" in name


def collect_compose_files(sources: List[str]) -> List[Path]:
    files: List[Path] = []
    for source in sources:
        p = Path(source)
        if not p.exists():
            print(f"ERROR: compose source not found: {source}", file=sys.stderr)
            sys.exit(1)
        candidates = [p]
        if p.is_dir():
            candidates = []
            for pattern in ("docker-compose*.yaml", "docker-compose*.yml"):
                candidates.extend(sorted(p.glob(pattern)))
        for f in candidates:
            if is_test_compose(f.name):
                print(f"(skipped {f.name}: test harness, not a deployment file)")
                continue
            files.append(f)
    return files


def _merge_compose(merged: Dict[str, str], found: Dict[str, str]) -> None:
    for name, value in found.items():
        if name not in merged or (not merged[name] and value):
            merged[name] = value


def parse_compose(sources: List[str]) -> Tuple[Dict[str, str], List[Path]]:
    files = collect_compose_files(sources)
    merged: Dict[str, str] = {}
    for f in files:
        _merge_compose(merged, parse_compose_text(f.read_text(encoding="utf-8")))
    return merged, files


# --- Git refs (--compare-rev) ---------------------------------------------------------

def _docker_paths_at_ref(repo: str, ref: str) -> List[str]:
    return subprocess.run(
        ["git", "-C", repo, "ls-tree", "-r", "--name-only", ref, "--", "docker/"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()


def _show(repo: str, ref: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, "show", f"{ref}:{path}"],
        capture_output=True, text=True, check=True,
    ).stdout


def compose_vars_at_ref(repo: str, ref: str, paths: List[str]) -> Dict[str, str]:
    """${VAR} references in docker/docker-compose*.y*ml at a git ref."""
    merged: Dict[str, str] = {}
    for path in paths:
        name = Path(path).name
        if not (name.startswith("docker-compose") and name.endswith((".yaml", ".yml"))):
            continue
        if is_test_compose(name):
            print(f"(skipped {name} at {ref}: test harness, not a deployment file)")
            continue
        _merge_compose(merged, parse_compose_text(_show(repo, ref, path)))
    return merged


def env_surface_at_ref(repo: str, ref: str) -> Tuple[EnvSurface, List[str]]:
    """The env surface at a git ref: every docker/ env file plus the compose references.
    Returns the surface and the compose-only names."""
    paths = _docker_paths_at_ref(repo, ref)
    surface = EnvSurface()
    for path in order_env_paths(paths):
        surface.add_text(_show(repo, ref, path).splitlines(), path, env_file_role(Path(path).name))
    compose_only = surface.add_compose(compose_vars_at_ref(repo, ref, paths))
    return surface, compose_only


NO_DEFAULT = "(no default in the env files)"


def _show_default(entry) -> str:
    if entry is None:
        return NO_DEFAULT
    return " | ".join(repr(v) for v in entry[0])


def default_changes(old: EnvSurface, new: EnvSurface) -> List[Tuple[str, str, str]]:
    """Variables present at both refs whose stock default changed, including a default
    that appeared or disappeared (a line commented out or uncommented)."""
    old_d, new_d = old.defaults(), new.defaults()
    changed = []
    for name in sorted(set(old.names) & set(new.names)):
        a, b = old_d.get(name), new_d.get(name)
        if a is None and b is None:
            continue
        if a is None or b is None or {normalize(v) for v in a[0]} != {normalize(v) for v in b[0]}:
            changed.append((name, _show_default(a), _show_default(b)))
    return changed


def run_compare_rev(repo: str, old_ref: str, new_ref: str, docs_path, ignored_path: str) -> int:
    """Report env vars added/removed/default-changed between two git refs.

    The release safety net: per-PR detection misses untagged PRs, so diff the whole
    env-file surface between the previous release and the target, and flag NEW
    vars that are still undocumented and not intentionally ignored.
    """
    try:
        old, _ = env_surface_at_ref(repo, old_ref)
        new, new_compose_only = env_surface_at_ref(repo, new_ref)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: git failed: {e.stderr.strip() or e}", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print("ERROR: git not found on PATH", file=sys.stderr)
        return 2

    added = sorted(set(new.names) - set(old.names))
    removed = sorted(set(old.names) - set(new.names))
    changed = default_changes(old, new)
    old_d, new_d = old.defaults(), new.defaults()

    print(f"=== ENV VAR DIFF {old_ref}..{new_ref} (.env.example, *.defaults and templates, "
          f"commented lines included, + compose ${{VAR}} refs) ===")
    print(f"NEW ({len(added)}):")
    for n in added:
        tag = "  (compose-only)" if n in new_compose_only else ""
        print(f"  + {n}={_show_default(new_d.get(n))}{tag}")
    print(f"REMOVED ({len(removed)}):")
    for n in removed:
        tag = "  (now only a container mapping)" if n in new.mapped else ""
        print(f"  - {n} (was {_show_default(old_d.get(n))}){tag}")
    print(f"DEFAULT CHANGED ({len(changed)}):")
    for n, a, b in changed:
        print(f"  ~ {n}: {a} -> {b}")

    if docs_path:
        doc_vars = parse_mdx_docs(docs_path)
        ignored = parse_ignored_vars(ignored_path)
        gaps = [n for n in added if n not in doc_vars and n not in ignored]
        print()
        print(f"=== NEW vars NOT documented and NOT in ignored-vars ({len(gaps)}) — TRIAGE ===")
        for n in gaps:
            print(f"  {n}={_show_default(new_d.get(n))}")
        print("(Document each, or add to env-ignored-vars.md with a reason. Never leave a")
        print(" new-this-release var as silent backlog.)")
    else:
        print("\n(Pass --docs to also flag which NEW vars are still undocumented.)")
    return 0


# --- Verify mode ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Verify env var documentation against Dify's Docker env files"
    )
    parser.add_argument(
        "--env-example",
        action="append",
        help=(
            "Path to an env file (`.env.example`, `*.env.example`, `*.defaults`) or a "
            "directory holding them, globbed recursively. May be repeated. Pass both "
            "`docker/.env.example` and `docker/envs/`."
        ),
    )
    parser.add_argument(
        "--compose",
        action="append",
        help=(
            "Path to a docker-compose*.y*ml file or a directory holding them (pass "
            "`<repo>/docker`). May be repeated. Variables a compose file consumes with "
            "no env-file entry are otherwise invisible to this check."
        ),
    )
    parser.add_argument(
        "--docs",
        help="Path to MDX documentation file (e.g., en/self-host/deploy/configuration/environments.mdx)",
    )
    parser.add_argument(
        "--compare-rev",
        nargs=2,
        metavar=("OLD", "NEW"),
        help=(
            "Release safety net: two git refs (previous release, target). Reports env "
            "vars added/removed/default-changed in the docker/ env files between them, and "
            "(with --docs) which NEW vars are still undocumented. Requires --repo."
        ),
    )
    parser.add_argument(
        "--repo",
        help="Path to the Dify code repo (required with --compare-rev).",
    )
    parser.add_argument(
        "--ignored",
        default=str(DEFAULT_IGNORED_PATH),
        help=f"Path to ignored-vars markdown file (default: {DEFAULT_IGNORED_PATH}).",
    )
    args = parser.parse_args()

    if args.compare_rev:
        if not args.repo:
            parser.error("--repo is required with --compare-rev")
        old_ref, new_ref = args.compare_rev
        return run_compare_rev(args.repo, old_ref, new_ref, args.docs, args.ignored)

    if not args.env_example or not args.docs:
        parser.error("--env-example and --docs are required (or use --compare-rev --repo)")

    if not Path(args.docs).exists():
        print(f"ERROR: Documentation not found at {args.docs}")
        sys.exit(1)

    surface, env_files = parse_env_sources(args.env_example)
    doc_vars = parse_mdx_docs(args.docs)
    ignored = parse_ignored_vars(args.ignored)

    print(f"Parsed {len(surface.names)} variables from {len(env_files)} env file(s), in merge order:")
    for f in env_files:
        print(f"  - {f}  [{env_file_role(f.name)}]")
    print(f"Parsed {len(doc_vars)} variables from documentation")
    print(f"Loaded {len(ignored)} ignored variables from {args.ignored}")
    print()

    compose_only: List[str] = []
    if args.compose:
        compose_vars, compose_files = parse_compose(args.compose)
        print(f"Parsed {len(compose_vars)} ${{VAR}} references from {len(compose_files)} compose file(s)")
        compose_only = surface.add_compose(compose_vars)
        if compose_only:
            print(f"=== IN COMPOSE BUT NOT IN ANY .env.example ({len(compose_only)}) ===")
            for name in compose_only:
                print(f"  {name} (compose fallback: {surface.fallbacks[name]!r})")
            print("(Only --compose sees these. Document each, or add it to env-ignored-vars.md with a reason.)")
            print()

    defaults = surface.defaults()
    names = set(surface.names)
    no_default = sorted((names & set(doc_vars)) - set(defaults) - ignored)
    print(f"{len(no_default)} documented variables have no default in the env files "
          "(commented lines or templates only); their page defaults are not compared.")
    container_rows = sorted(set(surface.mapped_only()) & set(doc_vars))
    if container_rows:
        print(f"{len(container_rows)} documented variables are container mappings, set through "
              f"another variable; each row must name it: {', '.join(container_rows)}")
    print()

    # --- Check 1: Variables in the env files but missing from docs ---
    missing_from_docs = sorted((names - set(doc_vars)) - ignored)
    if missing_from_docs:
        print(f"=== MISSING FROM DOCS ({len(missing_from_docs)}) ===")
        for name in missing_from_docs:
            entry = defaults.get(name)
            shown = " | ".join(entry[0]) if entry else "(no default)"
            print(f"  {name}={shown}  [{surface.names[name]}]")
        print()

    # --- Check 2: Variables in docs but not in any env file ---
    extra_in_docs = sorted((set(doc_vars) - names - set(surface.mapped_only())) - ignored)
    if extra_in_docs:
        print(f"=== IN DOCS BUT NOT IN ANY .env.example ({len(extra_in_docs)}) ===")
        for name in extra_in_docs:
            print(f"  {name} (doc default: {doc_vars[name]!r})")
        print()

    # --- Check 3: Default value mismatches ---
    # Ignored vars are excluded here too: the false-positives bucket covers
    # secret values that the docs deliberately describe instead of reproduce.
    common = sorted((set(defaults) & set(doc_vars)) - ignored)
    mismatches = []
    for name in common:
        values, where = defaults[name]
        if not matches_default(doc_vars[name], values):
            mismatches.append((name, values, where, doc_vars[name]))

    if mismatches:
        print(f"=== DEFAULT MISMATCHES ({len(mismatches)}) ===")
        for name, values, where, doc_val in mismatches:
            print(f"  {name}:")
            print(f"    stock default: {' | '.join(repr(v) for v in values)}  [{where}]")
            print(f"    documentation: {doc_val!r}")
        print()

    # --- Summary ---
    total_issues = len(missing_from_docs) + len(extra_in_docs) + len(mismatches)
    if total_issues == 0:
        print("ALL CHECKS PASSED — documentation matches .env.example")
    else:
        print(f"TOTAL ISSUES: {total_issues}")
        print(f"  Missing from docs: {len(missing_from_docs)}")
        print(f"  Extra in docs: {len(extra_in_docs)}")
        print(f"  Default mismatches: {len(mismatches)}")

    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
