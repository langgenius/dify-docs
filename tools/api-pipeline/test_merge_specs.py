import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import merge_specs


class NavigationGenerationTest(unittest.TestCase):
    def test_existing_navigation_order_is_preserved_for_shared_operations(self) -> None:
        spec = {
            "tags": [{"name": "Documents"}],
            "paths": {
                "/a": {"get": {"tags": ["Documents"]}},
                "/b": {"get": {"tags": ["Documents"]}},
                "/new": {"get": {"tags": ["Documents"]}},
            },
        }
        labels = {
            "guides_layout": [],
            "guides_group": {"en": "Guides"},
            "op_order": {},
            "reference": {
                "app_apis": {
                    "labels": {"en": "App APIs"},
                    "tag_order_en": ["Documents"],
                },
                "knowledge_api": {
                    "labels": {"en": "Knowledge API"},
                    "tag_order_en": [],
                },
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            spec_path = repo / "en" / "api-reference" / "openapi_service.json"
            spec_path.parent.mkdir(parents=True)
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            with (
                patch.object(merge_specs, "REPO", repo),
                patch.object(merge_specs, "load_memberships", return_value={"pages": {}}),
            ):
                groups = merge_specs.nav_groups_for(
                    "en", labels, ["GET /b", "GET /a"]
                )

        self.assertEqual(
            groups[1]["pages"][0]["pages"],
            ["GET /b", "GET /a", "GET /new"],
        )

    def test_deprecated_compatibility_operations_are_not_added_to_navigation(self) -> None:
        spec = {
            "tags": [{"name": "Documents"}],
            "paths": {
                "/documents": {
                    "post": {"tags": ["Documents"]},
                },
                "/documents_legacy": {
                    "post": {"deprecated": True, "tags": ["Documents"]},
                },
            },
        }
        labels = {
            "guides_layout": [],
            "guides_group": {"en": "Guides"},
            "op_order": {},
            "reference": {
                "app_apis": {
                    "labels": {"en": "App APIs"},
                    "tag_order_en": ["Documents"],
                },
                "knowledge_api": {
                    "labels": {"en": "Knowledge API"},
                    "tag_order_en": [],
                },
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            spec_path = repo / "en" / "api-reference" / "openapi_service.json"
            spec_path.parent.mkdir(parents=True)
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            with (
                patch.object(merge_specs, "REPO", repo),
                patch.object(merge_specs, "load_memberships", return_value={"pages": {}}),
            ):
                groups = merge_specs.nav_groups_for("en", labels)

        pages = groups[1]["pages"][0]["pages"]
        self.assertEqual(pages, ["POST /documents"])


if __name__ == "__main__":
    unittest.main()
