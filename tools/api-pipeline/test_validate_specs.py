"""Regression checks for examples attached to real OpenAPI and Schema nodes."""

import unittest

from validate_specs import validate_examples


def document(*, schemas=None, media=None, components=None):
    return {
        "openapi": "3.1.0",
        "info": {"title": "Example API", "version": "1"},
        "components": {"schemas": schemas or {}, **(components or {})},
        "paths": {"/items": {"post": {
            "responses": {"200": {"description": "Success", "content": {
                "application/json": media or {},
            }}},
        }}},
    }


class ExampleValidationTests(unittest.TestCase):
    def test_rejects_inline_property_example_with_wrong_type(self):
        spec = document(media={"schema": {"type": "object", "properties": {
            "data": {"type": "string", "example": {"must": "be a JSON string"}},
        }}})
        count, errors = validate_examples(spec)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("/schema/properties/data/example:", errors[0])
        self.assertIn("not of type 'string'", errors[0])

    def test_validates_component_examples_and_referenced_media_schema(self):
        spec = document(
            schemas={"Item": {"type": "object", "properties": {
                "examples": {"type": "string", "examples": [4, "valid"]},
            }}},
            media={"schema": {"$ref": "#/components/schemas/Item"},
                   "example": {"examples": 9}},
        )
        count, errors = validate_examples(spec)
        self.assertEqual(count, 3)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("#/components/schemas/Item/properties/examples/examples/0:" in e for e in errors))
        self.assertTrue(any("/content/application~1json/example/examples:" in e for e in errors))

    def test_checks_referenced_response_request_body_and_example_objects(self):
        spec = document(components={
            "examples": {"bad/value": {"value": "not an integer"}},
            "responses": {"Shared": {"description": "Shared response", "content": {
                "application/json": {"schema": {"type": "integer"}, "examples": {
                    "sample": {"$ref": "#/components/examples/bad~1value"},
                }},
            }}},
            "requestBodies": {"SharedBody": {"content": {
                "application/json": {"schema": {"type": "boolean"}, "example": "not a boolean"},
            }}},
        })
        operation = spec["paths"]["/items"]["post"]
        operation["responses"]["200"] = {"$ref": "#/components/responses/Shared"}
        operation["requestBody"] = {"$ref": "#/components/requestBodies/SharedBody"}
        count, errors = validate_examples(spec)
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("#/components/examples/bad~1value/value:" in e for e in errors))
        self.assertTrue(any("#/components/requestBodies/SharedBody/content/application~1json/example:" in e
                            for e in errors))

    def test_does_not_treat_keyword_named_literal_data_as_schema(self):
        value = {"type": "integer", "examples": ["literal"], "properties": {
            "nested": {"type": "integer", "example": "literal"},
        }}
        spec = document(schemas={"Item": {"type": "object", "const": value, "enum": [value],
                                           "default": value, "example": value}})
        self.assertEqual(validate_examples(spec), (1, []))

    def test_boolean_media_schemas_are_validated(self):
        spec = document(media={"schema": False, "example": "rejected"})
        count, errors = validate_examples(spec)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("False schema does not allow", errors[0])
        spec["paths"]["/items"]["post"]["responses"]["200"]["content"]["application/json"]["schema"] = True
        self.assertEqual(validate_examples(spec), (1, []))

    def test_parameter_and_header_examples_use_their_schema(self):
        spec = document(components={
            "parameters": {"description": {"name": "query", "in": "query", "schema": {"type": "integer"},
                                               "examples": {"bad": {"value": "text"}}}},
            "headers": {"title": {"schema": {"type": "integer"}, "example": False}},
        })
        count, errors = validate_examples(spec)
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("#/components/parameters/description/examples/bad/value:" in e for e in errors))
        self.assertTrue(any("#/components/headers/title/example:" in e for e in errors))

    def test_unresolvable_or_external_examples_fail_instead_of_being_skipped(self):
        for example in (
            {"$ref": "#/components/examples/missing"},
            {"$ref": "https://example.com/example.json"},
            {"externalValue": "https://example.com/example.json"},
        ):
            with self.subTest(example=example):
                spec = document(media={"schema": {"type": "integer"}, "examples": {"bad": example}})
                count, errors = validate_examples(spec)
                self.assertEqual(count, 0)
                self.assertEqual(len(errors), 1)

    def test_cyclic_example_reference_fails_instead_of_looping(self):
        spec = document(
            components={"examples": {"loop": {"$ref": "#/components/examples/loop"}}},
            media={"schema": {"type": "integer"}, "examples": {
                "bad": {"$ref": "#/components/examples/loop"},
            }},
        )
        count, errors = validate_examples(spec)
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("cyclic example reference", errors[0])


if __name__ == "__main__":
    unittest.main()
