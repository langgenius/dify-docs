"""Unit tests for tools/translate/check-glossary-keys.py: run with `python3 -m unittest discover tools/tests`."""
import importlib.util
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "check_glossary_keys", Path(__file__).resolve().parent.parent / "translate" / "check-glossary-keys.py"
)
gk = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(gk)


class ResolvesTest(unittest.TestCase):
    def test_flat_and_nested_keys(self):
        self.assertTrue(gk.resolves({"menus.apps": "Studio"}, ["menus", "apps"]))
        self.assertTrue(gk.resolves({"menus": {"apps": "Studio"}}, ["menus", "apps"]))

    def test_a_descendant_does_not_count(self):
        self.assertFalse(gk.resolves({"menus.apps.title": "Studio"}, ["menus", "apps"]))


class SameKeyUnderTest(unittest.TestCase):
    def test_finds_the_key_after_a_namespace_split(self):
        every = {"common": {"operation.add": "Add"}, "navigation": {"menus.apps": "Studio"}}
        self.assertEqual(gk.same_key_under(every, "common.menus.apps"), ["navigation.menus.apps"])

    def test_a_removed_key_has_no_hint(self):
        self.assertEqual(gk.same_key_under({"common": {}, "navigation": {}}, "common.members.owner"), [])


if __name__ == "__main__":
    unittest.main()
