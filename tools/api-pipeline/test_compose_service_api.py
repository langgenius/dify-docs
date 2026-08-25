import unittest

from compose_service_api import (
    OverlayConflict,
    apply_overlay,
    digest,
    diff_overlay,
    merge_presentation,
    order_top_level,
)


class ComposeServiceApiTest(unittest.TestCase):
    def test_order_top_level_puts_onboarding_before_contract_maps(self):
        source = {
            "components": {},
            "info": {"title": "API"},
            "openapi": "3.1.0",
            "paths": {},
            "x-extra": True,
        }

        ordered = order_top_level(source)

        self.assertEqual(
            list(ordered),
            ["openapi", "info", "paths", "components", "x-extra"],
        )

    def test_overlay_round_trip(self):
        source = {
            "openapi": "3.1.0",
            "paths": {"/items": {"get": {"summary": "Generated"}}},
            "components": {"schemas": {"Item": {"type": "object"}}},
        }
        target = {
            "openapi": "3.1.0",
            "paths": {
                "/items": {
                    "get": {
                        "summary": "List Items",
                        "x-mint": {"href": "/en/api-reference/items/list-items"},
                    }
                }
            },
            "components": {
                "schemas": {
                    "Item": {
                        "type": "object",
                        "description": "An item.",
                    }
                }
            },
        }
        overlay = {"version": 1, "actions": diff_overlay(source, target)}
        self.assertEqual(apply_overlay(source, overlay), target)

    def test_overlay_can_relocate_external_docs_to_valid_top_level(self):
        source = {
            "openapi": "3.1.0",
            "info": {
                "title": "API",
                "version": "1.0",
                "externalDocs": {"url": "/generated-location"},
            },
        }
        target = {
            "openapi": "3.1.0",
            "info": {"title": "API", "version": "1.0"},
            "externalDocs": {"url": "/guides/get-started"},
        }

        overlay = {"version": 1, "actions": diff_overlay(source, target)}

        self.assertEqual(apply_overlay(source, overlay), target)

    def test_upstream_change_at_replace_path_conflicts(self):
        source = {"info": {"title": "Generated"}}
        target = {"info": {"title": "Localized"}}
        overlay = {"version": 1, "actions": diff_overlay(source, target)}

        with self.assertRaisesRegex(OverlayConflict, "upstream value changed"):
            apply_overlay({"info": {"title": "Changed upstream"}}, overlay)

    def test_unoverlaid_upstream_addition_flows_through(self):
        source = {"paths": {}, "info": {"title": "Generated"}}
        target = {"paths": {}, "info": {"title": "Localized"}}
        overlay = {"version": 1, "actions": diff_overlay(source, target)}
        changed_source = {
            "paths": {"/new": {"get": {"summary": "New"}}},
            "info": {"title": "Generated"},
        }

        composed = apply_overlay(changed_source, overlay)

        self.assertIn("/new", composed["paths"])
        self.assertEqual(composed["info"]["title"], "Localized")

    def test_upstream_addition_at_docs_only_path_conflicts(self):
        source = {"paths": {}}
        target = {"paths": {"/docs-only": {"get": {}}}}
        overlay = {"version": 1, "actions": diff_overlay(source, target)}

        with self.assertRaisesRegex(OverlayConflict, "already exists upstream"):
            apply_overlay({"paths": {"/docs-only": {"get": {}}}}, overlay)

    def test_capture_keeps_generated_wire_contract(self):
        source = {
            "paths": {
                "/items": {
                    "get": {
                        "summary": "Generated",
                        "operationId": "generated_items",
                        "responses": {"200": {}, "404": {}},
                    }
                }
            }
        }
        target = {
            "paths": {
                "/items": {
                    "get": {
                        "summary": "Localized",
                        "operationId": "published_items",
                        "responses": {"200": {}, "503": {}},
                        "x-mint": {"href": "/en/api-reference/items"},
                    }
                }
            }
        }

        localized = merge_presentation(source, target)

        self.assertEqual(localized["paths"]["/items"]["get"]["summary"], "Localized")
        self.assertEqual(
            localized["paths"]["/items"]["get"]["operationId"],
            "published_items",
        )
        self.assertEqual(
            set(localized["paths"]["/items"]["get"]["responses"]),
            {"200", "404"},
        )
        self.assertIn("x-mint", localized["paths"]["/items"]["get"])

    def test_array_annotations_follow_matching_contract_shape(self):
        source = {
            "oneOf": [
                {"type": "string", "description": "Generated string"},
                {"type": "integer", "description": "Generated integer"},
            ]
        }
        target = {
            "oneOf": [
                {"type": "integer", "description": "Localized integer"},
                {"type": "string", "description": "Localized string"},
            ]
        }

        localized = merge_presentation(source, target)

        self.assertEqual(localized["oneOf"][0]["description"], "Localized string")
        self.assertEqual(localized["oneOf"][1]["description"], "Localized integer")

    def test_schema_property_names_and_default_data_are_not_presentation(self):
        source = {
            "properties": {
                "summary": {"type": "string", "default": {"description": "wire"}},
                "tags": {"items": {"type": "string"}, "type": "array"},
            }
        }
        target = {
            "properties": {
                "summary": {
                    "type": "integer",
                    "default": {"description": "localized"},
                },
                "tags": {"items": {"type": "integer"}, "type": "array"},
            }
        }

        self.assertEqual(merge_presentation(source, target), source)

    def test_component_schema_names_are_not_presentation(self):
        source = {
            "components": {
                "schemas": {
                    "summary": {"type": "string"},
                    "description": {"type": "boolean"},
                }
            }
        }
        target = {
            "components": {
                "schemas": {
                    "summary": {"type": "integer"},
                    "description": {"type": "number"},
                }
            }
        }

        self.assertEqual(merge_presentation(source, target), source)

    def test_non_docs_vendor_extension_is_not_captured(self):
        source = {"type": "string", "x-wire-contract": {"mode": "generated"}}
        target = {"type": "string", "x-wire-contract": {"mode": "documented"}}

        self.assertEqual(merge_presentation(source, target), source)

    def test_list_diff_records_only_changed_presentation_leaf(self):
        source = {
            "parameters": [
                {
                    "in": "query",
                    "name": "limit",
                    "required": True,
                    "schema": {"minimum": 1, "type": "integer"},
                }
            ]
        }
        target = {
            "parameters": [
                {
                    "description": "Maximum results.",
                    "in": "query",
                    "name": "limit",
                    "required": True,
                    "schema": {"minimum": 1, "type": "integer"},
                }
            ]
        }

        self.assertEqual(
            diff_overlay(source, target),
            [
                {
                    "context_path": "/parameters/0",
                    "context_sha256": digest(source["parameters"][0]),
                    "op": "add",
                    "path": "/parameters/0/description",
                    "value": "Maximum results.",
                }
            ],
        )

    def test_array_reorder_conflicts_before_annotations_can_move(self):
        source = {
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
            ]
        }
        target = {
            "oneOf": [
                {"type": "string", "description": "String docs"},
                {"type": "integer", "description": "Integer docs"},
            ]
        }
        overlay = {"version": 1, "actions": diff_overlay(source, target)}
        reordered = {
            "oneOf": [
                {"type": "integer"},
                {"type": "string"},
            ]
        }

        with self.assertRaisesRegex(OverlayConflict, "array item moved"):
            apply_overlay(reordered, overlay)

    def test_handwritten_wire_contract_action_is_rejected(self):
        source = {"servers": [{"url": "https://api.example.com/v1"}]}
        overlay = {
            "version": 1,
            "actions": [
                {
                    "op": "replace",
                    "path": "/servers/0/url",
                    "source_sha256": digest("https://api.example.com/v1"),
                    "value": "https://attacker.example/v1",
                }
            ],
        }

        with self.assertRaisesRegex(OverlayConflict, "non-presentation"):
            apply_overlay(source, overlay)

    def test_top_level_tags_are_presentation(self):
        source = {"tags": [{"name": "service_api"}], "paths": {}}
        target = {"tags": [{"name": "Applications"}], "paths": {}}

        self.assertEqual(merge_presentation(source, target)["tags"], target["tags"])

    def test_capture_can_remove_generated_presentation_field(self):
        source = {"description": "Generated description", "type": "string"}
        target = {"type": "string"}

        localized = merge_presentation(source, target)
        overlay = {"version": 1, "actions": diff_overlay(source, localized)}

        self.assertEqual(localized, target)
        self.assertEqual(apply_overlay(source, overlay), target)
        self.assertEqual(
            overlay["actions"],
            [
                {
                    "op": "remove",
                    "path": "/description",
                    "source_sha256": digest("Generated description"),
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
