import copy
import unittest

from align_service_api import (
    apply_deprecated_alias_presentation,
    align_language,
    merge_presentation,
    prefix_internal_api_links,
    remove_new_untranslated_presentation,
    validate_alignment,
)


class AlignServiceApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.generated = {
            "openapi": "3.1.0",
            "info": {"title": "Generated", "version": "1"},
            "servers": [{"url": "/v1"}],
            "security": [{"Bearer": []}],
            "tags": [{"name": "service_api"}],
            "paths": {
                "/": {
                    "get": {
                        "operationId": "get_index_api",
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {"application/json": {"schema": {"type": "object"}}},
                            }
                        },
                        "security": [],
                        "summary": "Generated root",
                        "tags": ["service_api"],
                    }
                },
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {"200": {"description": "Success"}, "401": {"description": "Unauthorized"}},
                        "summary": "Generated summary",
                        "tags": ["service_api"],
                    }
                },
            },
            "components": {
                "securitySchemes": {
                    "Bearer": {"type": "http", "scheme": "bearer", "description": "Generated auth"}
                }
            },
        }
        self.current = {
            "openapi": "3.0.1",
            "info": {"title": "Dify Service API", "version": "1.0.0"},
            "servers": [{"url": "https://{api_base_url}"}],
            "security": [{"ApiKeyAuth": []}],
            "tags": [{"name": "Applications"}],
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "listItems",
                        "description": "Curated description.",
                        "responses": {"200": {"description": "Curated success"}},
                        "summary": "List Items",
                        "tags": ["Applications"],
                        "x-mint": {"href": "/en/api-reference/applications/list-items"},
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "ApiKeyAuth": {"type": "http", "scheme": "bearer", "description": "Curated auth"}
                }
            },
        }

    def test_generated_wire_fields_and_operation_ids_win(self) -> None:
        aligned = align_language(copy.deepcopy(self.generated), self.current, "en")
        operation = aligned["paths"]["/items"]["get"]
        self.assertEqual(operation["operationId"], "get_items")
        self.assertEqual(set(operation["responses"]), {"200", "401"})
        self.assertEqual(aligned["security"], [{"Bearer": []}])
        self.assertEqual(validate_alignment(self.generated, aligned), [])

    def test_documentation_presentation_and_server_are_preserved(self) -> None:
        aligned = align_language(copy.deepcopy(self.generated), self.current, "en")
        operation = aligned["paths"]["/items"]["get"]
        self.assertEqual(operation["summary"], "List Items")
        self.assertEqual(operation["description"], "Curated description.")
        self.assertEqual(operation["tags"], ["Applications"])
        self.assertEqual(operation["x-mint"]["href"], "/en/api-reference/applications/list-items")
        self.assertEqual(aligned["servers"], self.current["servers"])
        self.assertEqual(aligned["components"]["securitySchemes"]["Bearer"]["description"], "Curated auth")

    def test_existing_key_order_is_stable_and_new_keys_are_appended(self) -> None:
        generated = {"type": "object", "new": True, "description": "Generated"}
        current = {"description": "Curated", "type": "object"}
        aligned = merge_presentation(generated, current)
        self.assertEqual(list(aligned), ["description", "type", "new"])

    def test_root_operation_receives_docs_metadata(self) -> None:
        aligned = align_language(copy.deepcopy(self.generated), self.current, "en")
        operation = aligned["paths"]["/"]["get"]
        self.assertEqual(operation["summary"], "Get API Information")
        self.assertEqual(operation["tags"], ["Applications"])
        self.assertEqual(operation["x-mint"]["href"], "/en/api-reference/applications/get-api-information")
        example = operation["responses"]["200"]["content"]["application/json"]["examples"]["response"]["value"]
        self.assertEqual(example["api_version"], "v1")
        self.assertEqual(example["server_version"], "1.17.0")

    def test_new_untranslated_prose_is_removed_but_response_description_is_localized(self) -> None:
        english = {
            "description": "New schema prose.",
            "responses": {"401": {"description": "Unauthorized - invalid API token"}},
        }
        localized = copy.deepcopy(english)
        cleaned = remove_new_untranslated_presentation(english, localized, set(), "zh")
        self.assertNotIn("description", cleaned)
        self.assertEqual(cleaned["responses"]["401"]["description"], "身份验证失败：API 令牌无效。")

    def test_internal_api_links_receive_locale_prefix(self) -> None:
        value = {
            "description": "See [Upload File](/api-reference/files/upload-file).",
            "x-mint": {"href": "/en/api-reference/files/upload-file"},
        }
        localized = prefix_internal_api_links(value, "en")
        self.assertIn("](/en/api-reference/files/upload-file)", localized["description"])
        self.assertEqual(localized["x-mint"]["href"], "/en/api-reference/files/upload-file")

    def test_deprecated_aliases_are_hidden_but_canonical_page_remains_linkable(self) -> None:
        spec = {
            "paths": {
                "/datasets/{dataset_id}/document/create_by_file": {
                    "post": {"deprecated": True, "summary": "Alias", "x-mint": {"href": "/alias"}}
                },
                "/datasets/{dataset_id}/documents/{document_id}/update-by-file": {
                    "post": {"deprecated": True, "summary": "Update Document by File"}
                },
            }
        }
        apply_deprecated_alias_presentation(spec, "en")
        alias = spec["paths"]["/datasets/{dataset_id}/document/create_by_file"]["post"]
        canonical = spec["paths"]["/datasets/{dataset_id}/documents/{document_id}/update-by-file"]["post"]
        self.assertNotIn("x-mint", alias)
        self.assertEqual(
            canonical["x-mint"]["href"],
            "/en/api-reference/documents/update-document-by-file",
        )

    def test_component_wire_changes_fail_validation(self) -> None:
        aligned = align_language(copy.deepcopy(self.generated), self.current, "en")
        aligned["components"]["securitySchemes"]["Bearer"]["scheme"] = "basic"
        self.assertIn("generated component contract changed", validate_alignment(self.generated, aligned))

    def test_schema_property_named_tags_is_wire_owned(self) -> None:
        generated = copy.deepcopy(self.generated)
        generated["components"]["schemas"] = {
            "Item": {"type": "object", "properties": {"tags": {"type": "array"}}}
        }
        aligned = align_language(copy.deepcopy(generated), self.current, "en")
        aligned["components"]["schemas"]["Item"]["properties"]["tags"]["type"] = "string"
        self.assertIn("generated component contract changed", validate_alignment(generated, aligned))


if __name__ == "__main__":
    unittest.main()
