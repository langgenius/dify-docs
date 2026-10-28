"""Unit tests for tools/check-links.py: run with `python3 -m unittest discover tools/tests`."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "check_links", Path(__file__).resolve().parent.parent / "check-links.py"
)
check_links = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(check_links)


def anchors_of(content: str) -> set[str]:
    with tempfile.TemporaryDirectory() as d:
        page = Path(d) / "page.mdx"
        page.write_text(content, encoding="utf-8")
        return check_links.extract_anchors(page)


class SlugifyTest(unittest.TestCase):
    def test_keeps_slash_and_ampersand(self):
        self.assertEqual(check_links.slugify("OTLP / OpenTelemetry Configuration"), "otlp-/-opentelemetry-configuration")
        self.assertEqual(check_links.slugify("OTLP / OpenTelemetry 配置"), "otlp-/-opentelemetry-配置")
        self.assertEqual(check_links.slugify("ModelProvider & Tool Position Configuration"), "modelprovider-&-tool-position-configuration")

    def test_still_strips_other_ascii_punctuation(self):
        self.assertEqual(check_links.slugify("Agent (New)"), "agent-new")
        self.assertEqual(check_links.slugify("Step 1: Install"), "step-1-install")

    def test_keeps_full_width_punctuation(self):
        self.assertEqual(check_links.slugify("步骤一：安装"), "步骤一：安装")


class HeadingAnchorTest(unittest.TestCase):
    def test_indented_heading_inside_tab(self):
        content = '<Tabs>\n  <Tab title="New Agent" id="new-agent">\n\n  ## Declare Its Outputs\n\n  </Tab>\n</Tabs>\n'
        self.assertIn("declare-its-outputs", anchors_of(content))

    def test_indented_code_comment_is_not_a_heading(self):
        content = '<Tab title="Shell">\n\n  ```bash\n  # Install the CLI\n  ```\n\n</Tab>\n'
        self.assertNotIn("install-the-cli", anchors_of(content))

    def test_top_level_heading_with_slash(self):
        self.assertIn("otlp-/-opentelemetry-configuration", anchors_of("### OTLP / OpenTelemetry Configuration\n"))


class ComponentAnchorTest(unittest.TestCase):
    def test_accordion_titles_follow_their_own_rule(self):
        content = (
            '<Accordion title="OceanBase / seekdb">\nx\n</Accordion>\n'
            '<Accordion title="Form & Workflow Apps">\nx\n</Accordion>\n'
        )
        anchors = anchors_of(content)
        self.assertIn("oceanbase-seekdb", anchors)
        self.assertIn("form-and-workflow-apps", anchors)
        self.assertNotIn("oceanbase-/-seekdb", anchors)

    def test_tab_titles_keep_the_old_stripping(self):
        self.assertIn("macos-linux", anchors_of('<Tabs>\n<Tab title="macOS / Linux">\nx\n</Tab>\n</Tabs>\n'))

    def test_explicit_id_wins(self):
        self.assertEqual(anchors_of('<Tab title="New Agent" id="new-agent">\nx\n</Tab>\n'), {"new-agent"})


class HeadingLinkTest(unittest.TestCase):
    def test_link_in_heading_contributes_its_text(self):
        self.assertEqual(
            check_links.slugify("1. [Register/Login](https://app.arize.com/auth/join) to Arize"),
            "1-register/login-to-arize",
        )


class InternalLinkTest(unittest.TestCase):
    def test_missing_anchor_is_still_reported(self):
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / "page.mdx"
            page.write_text("## Real Heading\n\nSee [x](#real-heading) and [y](#no-such-heading).\n", encoding="utf-8")
            anchors = check_links.extract_anchors(page)
            targets = [url[1:] for _, _, url in check_links.extract_links(page) if url.startswith("#")]
            self.assertEqual([t for t in targets if t not in anchors], ["no-such-heading"])


if __name__ == "__main__":
    unittest.main()
