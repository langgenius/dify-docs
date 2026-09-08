"""Regression checks for keeping documentation overlays out of API contracts."""

import copy
import unittest

from build_specs import annotation_changes, apply_annotations, contract, check_publication


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.base = {
            "openapi": "3.1.0",
            "paths": {"/items": {"post": {
                "operationId": "create_item",
                "summary": "Create item",
                "requestBody": {"content": {"application/json": {"schema": {
                    "type": "object",
                    "required": ["description"],
                    "properties": {
                        "description": {"type": "string", "description": "Item description"},
                        "content": {"type": "string", "description": "Item content"},
                        "properties": {"type": "object", "properties": {
                            "title": {"type": "string", "description": "A title"}}},
                    },
                }}}},
                "responses": {"200": {"description": "Success"}},
            }}},
        }

    def test_capture_and_build_prose_examples_and_legacy_urls(self):
        edited = copy.deepcopy(self.base)
        op = edited["paths"]["/items"]["post"]
        op["summary"] = "Create Item"
        op["operationId"] = "createItem"
        op["tags"] = ["Items"]
        op["x-mint"] = {"href": "/en/api-reference/items/create-item", "metadata": {
            "title": "Create Item", "sidebarTitle": "Create Item"}}
        media = op["requestBody"]["content"]["application/json"]
        media["examples"] = {"item": {"value": {"description": "A sample", "title": "Literal data"}}}
        media["schema"]["properties"]["content"]["description"] = "Updated content description"
        overlay = {"annotations": list(annotation_changes(self.base, edited))}
        self.assertEqual(apply_annotations(self.base, overlay), edited)
        self.assertEqual(contract(edited), contract(self.base))
        check_publication(edited, "en")

    def test_capture_rejects_changes_to_property_named_description(self):
        edited = copy.deepcopy(self.base)
        schema = edited["paths"]["/items"]["post"]["requestBody"]["content"]["application/json"]["schema"]
        schema["properties"]["description"]["type"] = "integer"
        with self.assertRaisesRegex(ValueError, "contract change"):
            list(annotation_changes(self.base, edited))

    def test_capture_rejects_required_and_enum_changes(self):
        for key, value in (("required", []), ("enum", ["invented"])):
            with self.subTest(key=key):
                edited = copy.deepcopy(self.base)
                schema = edited["paths"]["/items"]["post"]["requestBody"]["content"]["application/json"]["schema"]
                schema[key] = value
                with self.assertRaisesRegex(ValueError, "contract change"):
                    list(annotation_changes(self.base, edited))

    def test_build_rejects_forged_property_replacement(self):
        overlay = {"annotations": [{"path": "/paths/~1items/post/requestBody/content/application~1json/schema/properties/description",
                                     "value": {"type": "integer"}}]}
        with self.assertRaisesRegex(ValueError, "API contract"):
            apply_annotations(self.base, overlay)

    def test_build_rejects_orphan_and_duplicate_annotations(self):
        for changes in (
            [{"path": "/paths/~1removed/get/description", "value": "Gone"}],
            [{"path": "/paths/~1items/post/description", "value": "Twice"}] * 2,
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                apply_annotations(self.base, {"annotations": changes})

    def test_keyword_named_properties_remain_part_of_contract(self):
        schema = contract(self.base)["paths"]["/items"]["post"]["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(schema["properties"]["description"], {"type": "string"})
        self.assertEqual(schema["properties"]["content"], {"type": "string"})
        self.assertEqual(schema["properties"]["properties"]["properties"]["title"], {"type": "string"})

    def test_literal_values_cannot_be_changed_as_documentation(self):
        cases = [
            ({"components": {"schemas": {"Item": {"enum": [{"description": "allowed"}]}}}},
             "/components/schemas/Item/enum/0/description", "different"),
            ({"components": {"schemas": {"Item": {"const": {"title": "fixed"}}}}},
             "/components/schemas/Item/const/title", "different"),
            ({"components": {"schemas": {"Item": {"default": {"description": "default"}}}}},
             "/components/schemas/Item/default/description", "different"),
            ({"security": [{"description": ["read"]}]}, "/security/0/description", ["write"]),
            ({"components": {"schemas": {"Item": {"dependentRequired": {"description": ["id"]}}}}},
             "/components/schemas/Item/dependentRequired/description", []),
            ({"components": {"schemas": {"Item": {"discriminator": {"mapping": {"title": "#/A"}}}}}},
             "/components/schemas/Item/discriminator/mapping/title", "#/B"),
            ({"components": {"parameters": {"description": {"name": "q", "in": "query"}}}},
             "/components/parameters/description", {"name": "q", "in": "header"}),
        ]
        for base, location, value in cases:
            with self.subTest(location=location):
                edited = copy.deepcopy(base)
                parts = location[1:].split("/")
                parent = edited
                for part in parts[:-1]:
                    parent = parent[int(part)] if isinstance(parent, list) else parent[part]
                parent[parts[-1]] = value
                self.assertNotEqual(contract(base), contract(edited))
                with self.assertRaisesRegex(ValueError, "contract change"):
                    list(annotation_changes(base, edited))
                with self.assertRaisesRegex(ValueError, "API contract"):
                    apply_annotations(base, {"annotations": [{"path": location, "value": value}]})

    def test_named_components_and_nested_schemas_still_allow_prose(self):
        base = {"components": {
            "parameters": {"description": {"name": "q", "in": "query", "description": "Query"}},
            "schemas": {"Item": {"dependentSchemas": {"title": {"description": "Rule"}}}},
        }}
        overlay = {"annotations": [
            {"path": "/components/parameters/description/description", "value": "Search query"},
            {"path": "/components/schemas/Item/dependentSchemas/title/description", "value": "New rule"},
        ]}
        edited = apply_annotations(base, overlay)
        self.assertEqual(contract(base), contract(edited))
        self.assertEqual(list(annotation_changes(base, edited)), overlay["annotations"])


if __name__ == "__main__":
    unittest.main()
