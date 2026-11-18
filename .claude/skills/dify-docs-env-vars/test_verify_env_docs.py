"""Tests for verify-env-docs.py: run with `python3 .claude/skills/dify-docs-env-vars/test_verify_env_docs.py`."""

import contextlib
import io
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("verify-env-docs.py")
V = runpy.run_path(str(SCRIPT))


def surface_of(*files):
    """Build an EnvSurface from (file name, text) pairs, merged in the script's order."""
    surface = V["EnvSurface"]()
    by_name = dict(files)
    for name in V["order_env_paths"](list(by_name)):
        surface.add_text(by_name[name].splitlines(), name, V["env_file_role"](Path(name).name))
    return surface


class ExpansionTest(unittest.TestCase):
    def test_colon_less_and_colon_forms_resolve_to_their_fallback(self):
        interpolate = V["interpolate"]
        self.assertEqual(interpolate("${NEXT_PUBLIC_ENABLE_AGENT_V2-true}"), "true")
        self.assertEqual(interpolate("${GUNICORN_TIMEOUT:-360}"), "360")
        self.assertEqual(interpolate("${WEB_SENTRY_DSN}"), "")

    def test_dash_keeps_an_empty_value_and_colon_dash_replaces_it(self):
        interpolate = V["interpolate"]
        self.assertEqual(interpolate("${CELERY_WORKER_AMOUNT-4}", {"CELERY_WORKER_AMOUNT": ""}), "")
        self.assertEqual(interpolate("${CELERY_WORKER_AMOUNT:-4}", {"CELERY_WORKER_AMOUNT": ""}), "4")
        self.assertEqual(interpolate("${CELERY_WORKER_AMOUNT-4}", {"CELERY_WORKER_AMOUNT": "8"}), "8")

    def test_nested_and_embedded_expansions(self):
        interpolate = V["interpolate"]
        self.assertEqual(interpolate("${A:-${B:-${C:-}}}"), "")
        self.assertEqual(interpolate("${A:-${B:-http://plugin_daemon:5002}}"), "http://plugin_daemon:5002")
        self.assertEqual(
            interpolate("${CELERY_BROKER_URL:-redis://:${REDIS_PASSWORD:-pw}@${REDIS_HOST:-redis}:${REDIS_PORT:-6379}/1}",
                        {"REDIS_HOST": "cache"}),
            "redis://:pw@cache:6379/1",
        )

    def test_compose_refs_include_colon_less_and_deeply_nested_names(self):
        refs = V["parse_compose_text"](
            "      KNOWLEDGE_BACKGROUND_EXECUTION: ${KNOWLEDGE_BACKGROUND_EXECUTION-}\n"
            "      DIFY_AGENT_E2B_API_KEY: ${DIFY_AGENT_E2B_API_KEY:-${E2B_API_KEY:-${E2B_API_TOKEN:-}}}\n"
            "      PORT: ${EXPOSE_NGINX_PORT:-80}\n"
            '      command: FLAG_FILE="$${DIR}/.init_permissions"\n'
        )
        self.assertEqual(refs["KNOWLEDGE_BACKGROUND_EXECUTION"], "")
        for name in ("DIFY_AGENT_E2B_API_KEY", "E2B_API_KEY", "E2B_API_TOKEN"):
            self.assertIn(name, refs)
        self.assertEqual(refs["EXPOSE_NGINX_PORT"], "80")
        self.assertNotIn("DIR", refs)

    def test_an_unclosed_brace_does_not_hide_later_references(self):
        refs = V["parse_compose_text"]("a: ${A:-1}\n# use ${UNCLOSED to configure\nb: ${B:-2}\n")
        self.assertEqual(refs, {"A": "1", "B": "2"})

    def test_required_and_alternate_operators(self):
        interpolate = V["interpolate"]
        refs = V["parse_compose_text"]("x: ${REQUIRED_TOKEN:?set it}\ny: ${OPT:+--flag}\n")
        self.assertEqual(refs, {"REQUIRED_TOKEN": "", "OPT": ""})
        self.assertEqual(interpolate("${OPT:+--flag}"), "")
        self.assertEqual(interpolate("${OPT:+--flag}", {"OPT": "1"}), "--flag")
        self.assertEqual(interpolate("${REQUIRED_TOKEN:?set it}", {"REQUIRED_TOKEN": "t"}), "t")
        self.assertEqual(V["classify_env_line"]("FOO=${FOO:?required}")[0], "set")

    def test_double_dollar_is_a_literal_dollar(self):
        self.assertEqual(V["interpolate"]("$${A:-x}"), "${A:-x}")


class LineTest(unittest.TestCase):
    def test_line_kinds(self):
        classify = V["classify_env_line"]
        self.assertEqual(classify("# ENABLE_OAUTH_BEARER=false"), ("commented", "ENABLE_OAUTH_BEARER", "false"))
        self.assertEqual(classify("#FOO=bar")[0], "commented")
        self.assertEqual(classify("TRIGGER_URL=${TRIGGER_URL-http://localhost}")[0], "set")
        self.assertEqual(classify("PDF_RENDER_DPI=350")[0], "set")
        self.assertEqual(classify("WORKER_TIMEOUT=${SANDBOX_WORKER_TIMEOUT:-15}")[0], "mapping")
        self.assertEqual(classify("OPENSEARCH_JAVA_OPTS=-Xms${OPENSEARCH_JAVA_OPTS_MIN:-512m}")[0], "mapping")
        self.assertEqual(classify("bootstrap.memory_lock=${OPENSEARCH_BOOTSTRAP_MEMORY_LOCK:-true}")[0], "mapping")
        self.assertIsNone(classify("# Remove accidental empty overrides (especially CELERY_WORKER_AMOUNT=)."))
        self.assertIsNone(classify(""))


class SurfaceTest(unittest.TestCase):
    def test_commented_line_names_a_variable_but_sets_no_default(self):
        s = surface_of(("envs/api-worker.defaults", "# ENABLE_OAUTH_BEARER=false\n"))
        self.assertIn("ENABLE_OAUTH_BEARER", s.names)
        self.assertNotIn("ENABLE_OAUTH_BEARER", s.defaults())

    def test_template_values_are_names_only(self):
        s = surface_of(("envs/security.env.example", "SECRET_KEY=sk-example\n# INIT_PASSWORD=\n"))
        self.assertEqual(set(s.names), {"SECRET_KEY", "INIT_PASSWORD"})
        self.assertEqual(s.defaults(), {})

    def test_mapping_records_the_source_not_the_container_variable(self):
        s = surface_of(("envs/sandbox.defaults", "WORKER_TIMEOUT=${SANDBOX_WORKER_TIMEOUT:-15}\n"))
        self.assertIn("SANDBOX_WORKER_TIMEOUT", s.names)
        self.assertNotIn("WORKER_TIMEOUT", s.names)
        defaults = s.defaults()
        self.assertEqual(defaults["SANDBOX_WORKER_TIMEOUT"][0], ["15"])
        # The container variable may be documented; its value is the mapping's.
        self.assertEqual(s.mapped_only(), ["WORKER_TIMEOUT"])
        self.assertEqual(defaults["WORKER_TIMEOUT"][0], ["15"])

    def test_mapping_value_never_competes_with_the_variables_own_default(self):
        s = surface_of(
            ("envs/db-postgres.defaults", "DB_DATABASE=${DB_DATABASE-dify}\n"),
            ("envs/plugin-daemon.defaults", "DB_DATABASE=${DB_PLUGIN_DATABASE:-dify_plugin}\n"),
        )
        self.assertEqual(s.defaults()["DB_DATABASE"][0], ["dify"])
        self.assertEqual(s.defaults()["DB_PLUGIN_DATABASE"][0], ["dify_plugin"])
        self.assertEqual(s.mapped_only(), [])

    def test_merge_order_stock_env_then_defaults_then_reference_fallbacks(self):
        s = surface_of(
            (".env.example", "COMPOSE_PROFILES=weaviate,postgresql\nREDIS_HOST=cache\n"),
            ("envs/api.defaults",
             "REDIS_HOST=${REDIS_HOST-redis}\n"
             "CELERY_BROKER_URL=${CELERY_BROKER_URL:-redis://:${REDIS_PASSWORD:-pw}@${REDIS_HOST:-redis}:6379/1}\n"),
            ("envs/redis.defaults", "REDIS_PASSWORD=${REDIS_PASSWORD:-difyai123456}\n"),
            ("envs/security.env.example", "REDIS_PASSWORD=from-template\n"),
        )
        d = s.defaults()
        self.assertEqual(d["REDIS_HOST"], (["cache"], "stock .env"))
        # A defaults line is resolved against the stock .env, not against other defaults files.
        self.assertEqual(d["CELERY_BROKER_URL"][0], ["redis://:pw@cache:6379/1"])
        # The tracked line beats the fallback nested in another expression and the template.
        self.assertEqual(d["REDIS_PASSWORD"][0], ["difyai123456"])

    def test_defaults_that_differ_by_vector_store_are_all_kept(self):
        s = surface_of(
            ("envs/vectorstores/oceanbase.defaults", "OCEANBASE_VECTOR_HOST=${OCEANBASE_VECTOR_HOST-oceanbase}\n"),
            ("envs/vectorstores/seekdb.defaults", "OCEANBASE_VECTOR_HOST=${OCEANBASE_VECTOR_HOST-seekdb}\n"),
        )
        values = s.defaults()["OCEANBASE_VECTOR_HOST"][0]
        self.assertEqual(sorted(values), ["oceanbase", "seekdb"])
        matches = V["matches_default"]
        self.assertTrue(matches("oceanbase` / `seekdb", values))
        self.assertTrue(matches("seekdb` / `oceanbase", values))
        # A row that names only one store is wrong for the other.
        self.assertFalse(matches("seekdb", values))
        self.assertFalse(matches("localhost", values))
        self.assertTrue(matches("dify", ["dify"]))
        self.assertFalse(matches("dify` / `other", ["dify"]))

    def test_missing_variables_point_at_the_most_authoritative_file(self):
        s = surface_of(
            ("envs/knowledge-fs-worker.env.example", "# KNOWLEDGE_FS_BACKGROUND_WORKER_ENABLED=true\n"),
            ("envs/api-worker.defaults", "# KNOWLEDGE_FS_BACKGROUND_WORKER_ENABLED=true\n"),
        )
        self.assertEqual(s.names["KNOWLEDGE_FS_BACKGROUND_WORKER_ENABLED"], "envs/api-worker.defaults")

    def test_compose_reference_supplies_names_and_fallbacks_only_where_missing(self):
        s = surface_of(("envs/api.defaults", "# VECTOR_STORE=weaviate\nNGINX_PORT=${NGINX_PORT-80}\n"))
        only = s.add_compose({"VECTOR_STORE": "weaviate", "NGINX_PORT": "8080", "EXPOSE_NGINX_PORT": "80"})
        self.assertEqual(only, ["EXPOSE_NGINX_PORT"])
        d = s.defaults()
        self.assertEqual(d["VECTOR_STORE"][0], ["weaviate"])
        self.assertEqual(d["NGINX_PORT"][0], ["80"])

    def test_paths_at_a_ref_are_filtered_and_put_in_merge_order(self):
        paths = [
            "docker/envs/core-services/api.defaults",
            "docker/.env.example",
            "docker/docker-compose.yaml",
            "docker/envs/security.env.example",
            "docker/README.md",
            "docker/envs/vectorstores/weaviate.defaults",
            "docker/envs/middleware.env.example",
        ]
        self.assertEqual(V["order_env_paths"](paths), [
            "docker/envs/middleware.env.example",
            "docker/envs/security.env.example",
            "docker/envs/core-services/api.defaults",
            "docker/envs/vectorstores/weaviate.defaults",
            "docker/.env.example",
        ])

    def test_commenting_out_a_default_is_a_default_change(self):
        old = surface_of((".env.example", "ENABLE_OAUTH_BEARER=false\nLOG_LEVEL=INFO\n"))
        new = surface_of(
            (".env.example", "COMPOSE_PROFILES=weaviate\n"),
            ("envs/api-worker.defaults", "# ENABLE_OAUTH_BEARER=false\nLOG_LEVEL=${LOG_LEVEL-INFO}\n"),
        )
        self.assertEqual(V["default_changes"](old, new), [
            ("ENABLE_OAUTH_BEARER", "'false'", V["NO_DEFAULT"]),
        ])


class DocsParseTest(unittest.TestCase):
    def test_default_line_takes_the_first_value_and_cells_keep_alternatives(self):
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / "page.mdx"
            page.write_text(
                "### RESPECT_XFORWARD_HEADERS_ENABLED\n\n"
                "Default: `true` on Docker Compose; `false` on source deployments\n\n"
                "| `OCEANBASE_VECTOR_HOST` | `oceanbase` / `seekdb` | Host. |\n"
                "| `DIFY_AGENT_REDIS_URL` | (empty; derives from `REDIS_PASSWORD`) | Redis. |\n",
                encoding="utf-8",
            )
            docs = V["parse_mdx_docs"](str(page))
        self.assertEqual(docs["RESPECT_XFORWARD_HEADERS_ENABLED"], "true")
        self.assertEqual(docs["OCEANBASE_VECTOR_HOST"], "oceanbase` / `seekdb")
        self.assertEqual(docs["DIFY_AGENT_REDIS_URL"], "")


DOCS = """\
| Variable | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Log level. |
| `ENABLE_OAUTH_BEARER` | `true` | Bearer tokens. |
| `SANDBOX_WORKER_TIMEOUT` | `15` | Code run limit. |
| `WORKER_TIMEOUT` | `15` | Container variable; set `SANDBOX_WORKER_TIMEOUT` instead. |
| `SECRET_KEY` | (pre-filled; must be replaced) | Signing key. |
"""


class CommandTest(unittest.TestCase):
    """The printed contract: success line, TOTAL ISSUES, exit codes."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        docker = self.dir / "docker"
        (docker / "envs").mkdir(parents=True)
        (docker / ".env.example").write_text("COMPOSE_PROFILES=weaviate\n")
        (docker / "envs" / "api-worker.defaults").write_text(
            "LOG_LEVEL=${LOG_LEVEL-INFO}\n# ENABLE_OAUTH_BEARER=false\n")
        (docker / "envs" / "sandbox.defaults").write_text("WORKER_TIMEOUT=${SANDBOX_WORKER_TIMEOUT:-15}\n")
        (docker / "envs" / "security.env.example").write_text("SECRET_KEY=sk-example\n")
        (docker / "docker-compose.yaml").write_text("x: ${COMPOSE_PROFILES:-weaviate}\n")
        self.docs = self.dir / "page.mdx"
        self.ignored = self.dir / "ignored.md"
        self.ignored.write_text("| `COMPOSE_PROFILES` | Compose selector | test |\n")
        self.docker = docker

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_verify(self, docs_text):
        self.docs.write_text(docs_text)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--env-example", str(self.docker / ".env.example"),
             "--env-example", str(self.docker / "envs"), "--compose", str(self.docker),
             "--docs", str(self.docs), "--ignored", str(self.ignored)],
            capture_output=True, text=True,
        )

    def test_clean_page_passes(self):
        result = self.run_verify(DOCS)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.strip().splitlines()[-1],
                         "ALL CHECKS PASSED — documentation matches .env.example")
        # ENABLE_OAUTH_BEARER (commented) and SECRET_KEY (template only) have no default.
        self.assertIn("2 documented variables have no default in the env files", result.stdout)
        self.assertIn("1 documented variables are container mappings", result.stdout)
        self.assertIn(f"{self.docker / '.env.example'}  [stock .env]", result.stdout)

    def test_container_mapping_row_is_compared_with_the_mapping(self):
        result = self.run_verify(DOCS.replace("| `WORKER_TIMEOUT` | `15` |", "| `WORKER_TIMEOUT` | `30` |"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("  Default mismatches: 1", result.stdout)

    def test_mismatch_and_extra_are_counted(self):
        result = self.run_verify(DOCS.replace("`INFO`", "`DEBUG`") + "| `WORKER_COUNT` | `1` | Gone. |\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("TOTAL ISSUES: 2", result.stdout)
        self.assertIn("  Extra in docs: 1", result.stdout)
        self.assertIn("  Default mismatches: 1", result.stdout)

    def test_missing_ignore_list_stops_with_exit_2(self):
        self.ignored.unlink()
        result = self.run_verify(DOCS)
        self.assertEqual(result.returncode, 2)
        self.assertIn("WARNING: ignore list not found", result.stdout)
        self.assertNotIn("TOTAL ISSUES", result.stdout)


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class CompareRevTest(unittest.TestCase):
    def test_reads_defaults_files_and_commented_lines_at_both_refs(self):
        repo = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, repo)

        def git(*args):
            subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

        def commit(files, tag):
            for rel, text in files.items():
                path = repo / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            git("add", "-A")
            git("-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", tag)
            git("tag", tag)

        git("init", "-q")
        commit({"docker/.env.example": "ENABLE_OAUTH_BEARER=false\nLOG_LEVEL=INFO\nOLD_FLAG=1\nSENTRY_DSN=\n"}, "old")
        (repo / "docker/.env.example").write_text("COMPOSE_PROFILES=weaviate\n")
        commit({"docker/envs/api-worker.defaults":
                "LOG_LEVEL=${LOG_LEVEL-INFO}\n# ENABLE_OAUTH_BEARER=false\n# NEW_FLAG=true\n"
                "SENTRY_DSN=${API_SENTRY_DSN:-}\n"}, "new")

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = V["run_compare_rev"](str(repo), "old", "new", None, "unused")
        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("NEW (3):", text)  # API_SENTRY_DSN, COMPOSE_PROFILES, NEW_FLAG
        self.assertIn("  + NEW_FLAG=(no default in the env files)", text)
        self.assertIn("REMOVED (2):\n  - OLD_FLAG (was '1')\n"
                      "  - SENTRY_DSN (was '')  (now only a container mapping)", text)
        self.assertIn("DEFAULT CHANGED (1):\n  ~ ENABLE_OAUTH_BEARER: 'false' -> (no default in the env files)", text)


if __name__ == "__main__":
    unittest.main()
