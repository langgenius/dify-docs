import unittest

from contract_alignment import (
    METHODS,
    compare_specs as _compare_specs,
    validate_declared_schema_dialect,
)


def compare_specs(upstream: dict, documented: dict):
    """Compare focused fixtures under the contract's current OpenAPI dialect."""

    return _compare_specs(
        {"openapi": "3.1.0", **upstream},
        {"openapi": "3.1.0", **documented},
    )


def response_schema_spec(schema: object) -> dict:
    return {
        "paths": {
            "/items": {
                "get": {
                    "operationId": "get_items",
                    "responses": {
                        "200": {"content": {"application/json": {"schema": schema}}}
                    },
                }
            }
        }
    }


class ContractAlignmentMethodCoverageTest(unittest.TestCase):
    def test_all_openapi_operation_methods_are_compared(self) -> None:
        for method in METHODS:
            with self.subTest(method=method):
                upstream = {
                    "paths": {
                        "/health": {
                            method: {
                                "operationId": f"{method}_health",
                                "responses": {"200": {}},
                            }
                        }
                    }
                }

                hard_errors, differences, counts = compare_specs(
                    upstream, {"paths": {}}
                )

                self.assertEqual(
                    hard_errors,
                    [f"missing documented operation: {method.upper()} /health"],
                )
                self.assertEqual(differences, {})
                self.assertEqual(counts, {})

    def test_supported_methods_match_openapi_operation_fields(self) -> None:
        self.assertEqual(
            set(METHODS),
            {"delete", "get", "head", "options", "patch", "post", "put", "trace"},
        )


class ContractAlignmentWireSemanticsTest(unittest.TestCase):
    def test_operation_id_compatibility_override_preserves_public_sdk_name(self) -> None:
        upstream = response_schema_spec({"type": "object"})
        documented = response_schema_spec({"type": "object"})
        upstream["paths"]["/items"]["get"]["operationId"] = "generated_items"
        documented["paths"]["/items"]["get"]["operationId"] = "getItems"

        self.assertEqual(
            _compare_specs(
                {"openapi": "3.1.0", **upstream},
                {"openapi": "3.1.0", **documented},
                {"GET /items": "getItems"},
            ),
            ([], {}, {}),
        )

    def test_operation_id_compatibility_override_mismatch_is_a_hard_error(self) -> None:
        spec = response_schema_spec({"type": "object"})

        hard_errors, differences, counts = _compare_specs(
            {"openapi": "3.1.0", **spec},
            {"openapi": "3.1.0", **spec},
            {"GET /items": "getItems"},
        )

        self.assertEqual(
            hard_errors,
            [
                "operationId compatibility override mismatch: GET /items: "
                "expected='getItems', documented='get_items'"
            ],
        )
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_stale_operation_id_compatibility_override_is_a_hard_error(self) -> None:
        spec = response_schema_spec({"type": "object"})

        hard_errors, _, _ = _compare_specs(
            {"openapi": "3.1.0", **spec},
            {"openapi": "3.1.0", **spec},
            {"GET /missing": "getMissing"},
        )

        self.assertEqual(
            hard_errors,
            ["stale operationId compatibility override: GET /missing"],
        )

    def test_openapi_version_mismatch_is_a_hard_error(self) -> None:
        hard_errors, differences, counts = compare_specs(
            {"openapi": "3.1.0", "paths": {}},
            {"openapi": "3.0.1", "paths": {}},
        )

        self.assertEqual(
            hard_errors,
            ["OpenAPI version mismatch: upstream=3.1.0, documented=3.0.1"],
        )
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_missing_or_invalid_openapi_version_is_a_hard_error(self) -> None:
        operation = {
            "paths": {
                "/health": {
                    "get": {
                        "operationId": "get_health",
                        "responses": {"200": {}},
                    }
                }
            }
        }
        cases = (
            (
                {**operation},
                {**operation, "openapi": "3.1.0"},
                [
                    "upstream OpenAPI version must be a non-empty string: None",
                    "OpenAPI version mismatch: upstream=None, documented=3.1.0",
                ],
            ),
            (
                {**operation, "openapi": "3.1.0"},
                {**operation, "openapi": 31},
                [
                    "documented OpenAPI version must be a non-empty string: 31",
                    "OpenAPI version mismatch: upstream=3.1.0, documented=31",
                ],
            ),
            (
                {**operation},
                {**operation},
                [
                    "upstream OpenAPI version must be a non-empty string: None",
                    "documented OpenAPI version must be a non-empty string: None",
                ],
            ),
        )

        for upstream, documented, expected_errors in cases:
            with self.subTest(
                upstream=upstream.get("openapi"), documented=documented.get("openapi")
            ):
                hard_errors, differences, counts = _compare_specs(upstream, documented)

                self.assertEqual(hard_errors, expected_errors)
                self.assertEqual(differences, {})
                self.assertEqual(counts, {})

    def test_openapi_30_rejects_json_schema_2020_12_keywords(self) -> None:
        spec = {
            "openapi": "3.0.1",
            "components": {
                "schemas": {
                    "Invalid": {
                        "type": "object",
                        "properties": {
                            "kind": {"const": "fixed"},
                            "value": {"type": "null"},
                            "labels": {
                                "type": "object",
                                "propertyNames": {"type": "string"},
                            },
                        },
                    }
                }
            },
        }

        failures = validate_declared_schema_dialect(spec)

        self.assertEqual(len(failures), 3)
        self.assertTrue(any("'const'" in failure for failure in failures))
        self.assertTrue(any("type 'null'" in failure for failure in failures))
        self.assertTrue(any("'propertyNames'" in failure for failure in failures))

    def test_openapi_30_nullable_and_single_value_enum_are_valid(self) -> None:
        spec = {
            "openapi": "3.0.1",
            "components": {
                "schemas": {
                    "Valid": {
                        "type": "object",
                        "properties": {
                            "kind": {"type": "string", "enum": ["fixed"]},
                            "value": {"type": "string", "nullable": True},
                        },
                    }
                }
            },
        }

        self.assertEqual(validate_declared_schema_dialect(spec), [])

    def test_openapi_30_rejects_unsupported_conditional_and_content_keywords(
        self,
    ) -> None:
        cases = {
            "if": {"if": {"required": ["kind"]}},
            "then": {"then": {"required": ["value"]}},
            "else": {"else": {"required": ["fallback"]}},
            "contains": {"type": "array", "contains": {"type": "string"}},
            "unevaluatedItems": {"type": "array", "unevaluatedItems": False},
            "contentSchema": {"type": "string", "contentSchema": {"type": "object"}},
        }

        for keyword, schema in cases.items():
            with self.subTest(keyword=keyword):
                spec = {
                    "openapi": "3.0.3",
                    "components": {"schemas": {"Invalid": schema}},
                }

                failures = validate_declared_schema_dialect(spec)

                self.assertTrue(
                    any(repr(keyword) in failure for failure in failures), failures
                )

    def test_openapi_30_rejects_array_type_syntax(self) -> None:
        spec = {
            "openapi": "3.0.3",
            "components": {
                "schemas": {
                    "Invalid": {"type": ["string", "null"]},
                }
            },
        }

        failures = validate_declared_schema_dialect(spec)

        self.assertEqual(len(failures), 1)
        self.assertIn("array 'type'", failures[0])

    def test_openapi_31_rejects_openapi_30_nullable_and_boolean_exclusive_bounds(
        self,
    ) -> None:
        spec = {
            "openapi": "3.1.0",
            "components": {
                "schemas": {
                    "Invalid": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string", "nullable": True},
                            "score": {
                                "type": "number",
                                "exclusiveMinimum": True,
                                "minimum": 0,
                            },
                        },
                    }
                }
            },
        }

        failures = validate_declared_schema_dialect(spec)

        self.assertEqual(len(failures), 2)
        self.assertTrue(any("'nullable'" in failure for failure in failures))
        self.assertTrue(any("'exclusiveMinimum'" in failure for failure in failures))

    def test_openapi_31_json_schema_null_is_valid(self) -> None:
        spec = {
            "openapi": "3.1.0",
            "components": {
                "schemas": {
                    "Valid": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "null"},
                        ]
                    }
                }
            },
        }

        self.assertEqual(validate_declared_schema_dialect(spec), [])

    def test_recursive_reference_target_identity_is_preserved(self) -> None:
        def recursive_spec(*, target: str) -> dict:
            return {
                "components": {
                    "schemas": {
                        "A": {
                            "type": "object",
                            "properties": {"next": {"$ref": "#/components/schemas/B"}},
                        },
                        "B": {
                            "type": "object",
                            "properties": {"next": {"$ref": target}},
                        },
                    }
                },
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {"$ref": "#/components/schemas/A"}
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
            }

        hard_errors, differences, counts = compare_specs(
            recursive_spec(target="#/components/schemas/A"),
            recursive_spec(target="#/components/schemas/B"),
        )

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences),
            {"response-schema | GET /items | 200 | application/json"},
        )
        self.assertEqual(counts, {"response-schema": 1})

    def test_schema_keyword_names_are_valid_property_names(self) -> None:
        for version, property_name in (("3.0.3", "const"), ("3.1.0", "nullable")):
            with self.subTest(version=version, property_name=property_name):
                spec = {
                    "openapi": version,
                    "components": {
                        "schemas": {
                            "Valid": {
                                "type": "object",
                                "properties": {property_name: {"type": "string"}},
                            }
                        }
                    },
                }

                self.assertEqual(validate_declared_schema_dialect(spec), [])

    def test_presentation_payloads_are_not_inspected_as_schemas(self) -> None:
        spec = {
            "openapi": "3.1.0",
            "components": {
                "schemas": {
                    "Valid": {
                        "type": "object",
                        "default": {"nullable": True},
                        "examples": [{"nullable": True}],
                    }
                }
            },
        }

        self.assertEqual(validate_declared_schema_dialect(spec), [])

    def test_reusable_response_schemas_are_validated(self) -> None:
        spec = {
            "openapi": "3.1.0",
            "components": {
                "responses": {
                    "Invalid": {
                        "description": "Invalid reusable response",
                        "content": {
                            "application/json": {
                                "schema": {"type": "string", "nullable": True}
                            }
                        },
                    }
                }
            },
        }

        failures = validate_declared_schema_dialect(spec)

        self.assertEqual(len(failures), 1)
        self.assertIn("components.responses", failures[0])

    def test_security_scheme_names_and_descriptions_are_presentation(self) -> None:
        def spec(scheme_name: str, description: str) -> dict:
            return {
                "security": [{scheme_name: []}],
                "components": {
                    "securitySchemes": {
                        scheme_name: {
                            "type": "http",
                            "scheme": "bearer",
                            "bearerFormat": "API_KEY",
                            "description": description,
                        }
                    }
                },
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {"200": {}},
                        }
                    }
                },
            }

        self.assertEqual(
            compare_specs(
                spec("Bearer", "Generated guidance"),
                spec("ApiKeyAuth", "Localized guidance"),
            ),
            ([], {}, {}),
        )

    def test_missing_authentication_is_a_hard_error(self) -> None:
        upstream = {
            "security": [{"Bearer": []}],
            "components": {
                "securitySchemes": {
                    "Bearer": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "API_KEY",
                    }
                }
            },
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {"200": {}},
                    }
                }
            },
        }
        documented = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {"200": {}},
                    }
                }
            }
        }

        hard_errors, differences, counts = compare_specs(upstream, documented)

        self.assertEqual(hard_errors, ["security contract mismatch: GET /items"])
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_operation_security_override_is_compared(self) -> None:
        def spec(public: bool) -> dict:
            operation = {
                "operationId": "get_items",
                "responses": {"200": {}},
            }
            if public:
                operation["security"] = []
            return {
                "security": [{"Bearer": []}],
                "components": {
                    "securitySchemes": {"Bearer": {"type": "http", "scheme": "bearer"}}
                },
                "paths": {"/items": {"get": operation}},
            }

        hard_errors, differences, counts = compare_specs(spec(False), spec(True))

        self.assertEqual(hard_errors, ["security contract mismatch: GET /items"])
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_missing_callback_is_a_hard_error(self) -> None:
        upstream = response_schema_spec({"type": "object"})
        documented = response_schema_spec({"type": "object"})
        upstream["paths"]["/items"]["get"]["callbacks"] = {
            "description": {
                "{$request.body#/callback_url}": {
                    "post": {
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["item_id"],
                                        "properties": {
                                            "item_id": {"type": "string"}
                                        },
                                    }
                                }
                            }
                        },
                        "responses": {"204": {"description": "Accepted"}},
                    }
                }
            }
        }

        hard_errors, differences, counts = compare_specs(upstream, documented)

        self.assertEqual(hard_errors, ["callback contract mismatch: GET /items"])
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_callback_schema_mismatch_is_a_hard_error(self) -> None:
        def spec(item_type: str) -> dict:
            value = response_schema_spec({"type": "object"})
            value["paths"]["/items"]["get"]["callbacks"] = {
                "itemReady": {
                    "{$request.body#/callback_url}": {
                        "post": {
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "item_id": {"type": item_type}
                                            },
                                        }
                                    }
                                }
                            },
                            "responses": {"204": {}},
                        }
                    }
                }
            }
            return value

        hard_errors, differences, counts = compare_specs(
            spec("string"), spec("integer")
        )

        self.assertEqual(hard_errors, ["callback contract mismatch: GET /items"])
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_callback_presentation_fields_are_ignored(self) -> None:
        def spec(description: str) -> dict:
            value = response_schema_spec({"type": "object"})
            value["paths"]["/items"]["get"]["callbacks"] = {
                "itemReady": {
                    "{$request.body#/callback_url}": {
                        "post": {
                            "description": description,
                            "responses": {
                                "204": {"description": f"{description} response"}
                            },
                        }
                    }
                }
            }
            return value

        self.assertEqual(
            compare_specs(spec("Generated"), spec("Documented")),
            ([], {}, {}),
        )

    def test_parameter_serialization_mismatch_is_a_hard_error(self) -> None:
        base_parameter = {
            "name": "ids",
            "in": "query",
            "schema": {"type": "array", "items": {"type": "string"}},
            "style": "form",
        }
        upstream = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "parameters": [{**base_parameter, "explode": True}],
                        "responses": {"200": {}},
                    }
                }
            }
        }
        documented = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "parameters": [{**base_parameter, "explode": False}],
                        "responses": {"200": {}},
                    }
                }
            }
        }

        hard_errors, differences, counts = compare_specs(upstream, documented)

        self.assertEqual(hard_errors, ["parameter contract mismatch: GET /items"])
        self.assertEqual(differences, {})
        self.assertEqual(counts, {})

    def test_explicit_parameter_serialization_defaults_are_equivalent(self) -> None:
        parameter = {
            "name": "ids",
            "in": "query",
            "schema": {"type": "array", "items": {"type": "string"}},
        }
        upstream = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "parameters": [{**parameter, "style": "form", "explode": True}],
                        "responses": {"200": {}},
                    }
                }
            }
        }
        documented = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "parameters": [parameter],
                        "responses": {"200": {}},
                    }
                }
            }
        }

        self.assertEqual(compare_specs(upstream, documented), ([], {}, {}))

    def test_multipart_encoding_mismatch_is_fingerprinted(self) -> None:
        request_schema = {
            "type": "object",
            "properties": {"ids": {"type": "array", "items": {"type": "string"}}},
        }

        def spec(explode: bool) -> dict:
            return {
                "paths": {
                    "/upload": {
                        "post": {
                            "operationId": "upload",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": request_schema,
                                        "encoding": {
                                            "ids": {"style": "form", "explode": explode}
                                        },
                                    }
                                }
                            },
                            "responses": {"204": {}},
                        }
                    }
                }
            }

        hard_errors, differences, counts = compare_specs(spec(True), spec(False))

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences), {"request-encoding | POST /upload | multipart/form-data"}
        )
        self.assertEqual(counts, {"request-encoding": 1})

    def test_multipart_encoding_preserves_presentation_named_fields(self) -> None:
        request_schema = {
            "type": "object",
            "properties": {
                "description": {"type": "array", "items": {"type": "string"}},
                "title": {"type": "array", "items": {"type": "string"}},
            },
        }

        def spec(field_name: str, explode: bool) -> dict:
            return {
                "paths": {
                    "/upload": {
                        "post": {
                            "operationId": "upload",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": request_schema,
                                        "encoding": {
                                            field_name: {
                                                "style": "form",
                                                "explode": explode,
                                            }
                                        },
                                    }
                                }
                            },
                            "responses": {"204": {}},
                        }
                    }
                }
            }

        for field_name in ("description", "title"):
            with self.subTest(field_name=field_name):
                hard_errors, differences, counts = compare_specs(
                    spec(field_name, True), spec(field_name, False)
                )

                self.assertEqual(hard_errors, [])
                self.assertEqual(
                    set(differences),
                    {"request-encoding | POST /upload | multipart/form-data"},
                )
                self.assertEqual(counts, {"request-encoding": 1})

    def test_property_names_does_not_overwrite_explicit_property_schemas(self) -> None:
        def spec(property_type: str) -> dict:
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "propertyNames": {"enum": ["value"]},
                                                "properties": {
                                                    "value": {"type": property_type}
                                                },
                                            }
                                        }
                                    }
                                }
                            },
                        }
                    }
                }
            }

        hard_errors, differences, counts = compare_specs(
            spec("string"), spec("integer")
        )

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences),
            {"response-schema | GET /items | 200 | application/json"},
        )
        self.assertEqual(counts, {"response-schema": 1})

    def test_property_names_preserves_additional_properties_schema(self) -> None:
        def finite_map(value_type: str) -> dict:
            return {
                "type": "object",
                "propertyNames": {"enum": ["value"]},
                "additionalProperties": {"type": value_type},
            }

        hard_errors, differences, counts = compare_specs(
            response_schema_spec(finite_map("string")),
            response_schema_spec(finite_map("integer")),
        )

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences),
            {"response-schema | GET /items | 200 | application/json"},
        )
        self.assertEqual(counts, {"response-schema": 1})
        self.assertEqual(
            compare_specs(
                response_schema_spec(finite_map("string")),
                response_schema_spec(
                    {
                        "type": "object",
                        "properties": {"value": {"type": "string"}},
                        "additionalProperties": False,
                    }
                ),
            ),
            ([], {}, {}),
        )

    def test_property_names_respects_false_additional_properties(self) -> None:
        self.assertEqual(
            compare_specs(
                response_schema_spec(
                    {
                        "type": "object",
                        "propertyNames": {"enum": ["value"]},
                        "additionalProperties": False,
                    }
                ),
                response_schema_spec(
                    {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    }
                ),
            ),
            ([], {}, {}),
        )

    def test_property_names_discards_explicit_properties_outside_enum(self) -> None:
        self.assertEqual(
            compare_specs(
                response_schema_spec(
                    {
                        "type": "object",
                        "propertyNames": {"enum": ["allowed"]},
                        "properties": {
                            "allowed": {"type": "string"},
                            "forbidden": {"type": "integer"},
                        },
                    }
                ),
                response_schema_spec(
                    {
                        "type": "object",
                        "properties": {"allowed": {"type": "string"}},
                        "additionalProperties": False,
                    }
                ),
            ),
            ([], {}, {}),
        )

    def test_property_names_with_patterns_remains_unexpanded(self) -> None:
        def patterned(value_type: str) -> dict:
            return {
                "type": "object",
                "propertyNames": {"enum": ["value"]},
                "patternProperties": {"^value$": {"type": value_type}},
                "additionalProperties": False,
            }

        hard_errors, differences, counts = compare_specs(
            response_schema_spec(patterned("string")),
            response_schema_spec(patterned("integer")),
        )

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences),
            {"response-schema | GET /items | 200 | application/json"},
        )
        self.assertEqual(counts, {"response-schema": 1})

    def test_openapi_31_type_array_order_is_not_semantic(self) -> None:
        self.assertEqual(
            compare_specs(
                response_schema_spec({"type": ["string", "null"]}),
                response_schema_spec({"type": ["null", "string"]}),
            ),
            ([], {}, {}),
        )

    def test_dependent_required_array_order_is_not_semantic(self) -> None:
        self.assertEqual(
            compare_specs(
                response_schema_spec(
                    {
                        "type": "object",
                        "dependentRequired": {"value": ["first", "second"]},
                    }
                ),
                response_schema_spec(
                    {
                        "type": "object",
                        "dependentRequired": {"value": ["second", "first"]},
                    }
                ),
            ),
            ([], {}, {}),
        )

    def test_json_instance_data_preserves_presentation_named_fields(self) -> None:
        def spec(keyword: str, marker: str) -> dict:
            value: object = {
                "description": marker,
                "title": f"{marker}-title",
                "x-custom": {"description": marker},
            }
            if keyword == "enum":
                value = [value]
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {"schema": {keyword: value}}
                                    }
                                }
                            },
                        }
                    }
                }
            }

        for keyword in ("const", "default", "enum"):
            with self.subTest(keyword=keyword):
                hard_errors, differences, counts = compare_specs(
                    spec(keyword, "upstream"), spec(keyword, "documented")
                )

                self.assertEqual(hard_errors, [])
                self.assertEqual(
                    set(differences),
                    {"response-schema | GET /items | 200 | application/json"},
                )
                self.assertEqual(counts, {"response-schema": 1})

    def test_schema_presentation_fields_remain_ignored(self) -> None:
        def spec(description: str) -> dict:
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "string",
                                                "description": description,
                                                "title": description,
                                                "x-mint": {"note": description},
                                            }
                                        }
                                    }
                                }
                            },
                        }
                    }
                }
            }

        self.assertEqual(
            compare_specs(spec("generated"), spec("localized")),
            ([], {}, {}),
        )

    def test_unknown_vendor_extension_remains_part_of_schema_contract(self) -> None:
        upstream = response_schema_spec(
            {"type": "string", "x-wire-contract": {"mode": "generated"}}
        )
        documented = response_schema_spec(
            {"type": "string", "x-wire-contract": {"mode": "documented"}}
        )

        hard_errors, differences, counts = compare_specs(upstream, documented)

        self.assertEqual(hard_errors, [])
        self.assertEqual(
            set(differences),
            {"response-schema | GET /items | 200 | application/json"},
        )
        self.assertEqual(counts, {"response-schema": 1})

    def test_unmatched_response_status_payload_changes_change_fingerprint(
        self,
    ) -> None:
        documented = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {"200": {}},
                    }
                }
            }
        }

        def upstream(enum_value: str) -> dict:
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {},
                                "418": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "string",
                                                "enum": [enum_value],
                                            }
                                        }
                                    }
                                },
                            },
                        }
                    }
                }
            }

        first = compare_specs(upstream("A"), documented)
        changed = compare_specs(upstream("B"), documented)
        key = "response-status | GET /items"
        self.assertEqual(set(first[1]), {key})
        self.assertNotEqual(first[1], changed[1])

    def test_unmatched_response_media_payload_changes_change_fingerprint(self) -> None:
        def spec(*, include_problem: bool, enum_value: str = "") -> dict:
            content = {"application/json": {"schema": {"type": "string"}}}
            if include_problem:
                content["application/problem+json"] = {
                    "schema": {"type": "string", "enum": [enum_value]}
                }
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {"200": {"content": content}},
                        }
                    }
                }
            }

        documented = spec(include_problem=False)
        first = compare_specs(spec(include_problem=True, enum_value="A"), documented)
        changed = compare_specs(spec(include_problem=True, enum_value="B"), documented)
        key = "response-media | GET /items | 200"
        self.assertEqual(set(first[1]), {key})
        self.assertNotEqual(first[1], changed[1])

    def test_response_header_mismatch_is_fingerprinted(self) -> None:
        upstream = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {
                            "200": {
                                "headers": {
                                    "X-RateLimit": {"schema": {"type": "integer"}}
                                }
                            }
                        },
                    }
                }
            }
        }
        documented = {
            "paths": {
                "/items": {
                    "get": {"operationId": "get_items", "responses": {"200": {}}}
                }
            }
        }

        hard_errors, differences, counts = compare_specs(upstream, documented)

        self.assertEqual(hard_errors, [])
        self.assertEqual(set(differences), {"response-header | GET /items | 200"})
        self.assertEqual(counts, {"response-header": 1})

    def test_response_header_names_are_case_insensitive(self) -> None:
        def spec(name: str) -> dict:
            return {
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "headers": {name: {"schema": {"type": "integer"}}}
                                }
                            },
                        }
                    }
                }
            }

        self.assertEqual(
            compare_specs(spec("X-RateLimit"), spec("x-ratelimit")), ([], {}, {})
        )

    def test_referenced_schema_sibling_mismatches_are_fingerprinted(self) -> None:
        def spec(sibling: dict) -> dict:
            return {
                "openapi": "3.1.0",
                "components": {
                    "schemas": {
                        "Kind": {"type": "string", "enum": ["primary", "secondary"]},
                    }
                },
                "paths": {
                    "/items": {
                        "get": {
                            "operationId": "get_items",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Kind",
                                                **sibling,
                                            }
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
            }

        cases = (
            ({"default": "primary"}, {"default": "secondary"}),
            ({"deprecated": True}, {"deprecated": False}),
            ({"readOnly": True}, {"readOnly": False}),
            ({"writeOnly": True}, {"writeOnly": False}),
        )
        for upstream_sibling, documented_sibling in cases:
            with self.subTest(sibling=next(iter(upstream_sibling))):
                hard_errors, differences, counts = compare_specs(
                    spec(upstream_sibling), spec(documented_sibling)
                )

                self.assertEqual(hard_errors, [])
                self.assertEqual(
                    set(differences),
                    {"response-schema | GET /items | 200 | application/json"},
                )
                self.assertEqual(counts, {"response-schema": 1})

    def test_referenced_schema_siblings_match_equivalent_inline_schema(self) -> None:
        upstream = {
            "openapi": "3.1.0",
            "components": {
                "schemas": {
                    "Kind": {"type": "string", "enum": ["primary", "secondary"]},
                }
            },
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Kind",
                                            "default": "primary",
                                            "readOnly": True,
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            },
        }
        documented = {
            "openapi": "3.1.0",
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "get_items",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "string",
                                            "enum": ["primary", "secondary"],
                                            "default": "primary",
                                            "readOnly": True,
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            },
        }

        self.assertEqual(compare_specs(upstream, documented), ([], {}, {}))

    def test_unrestricted_json_union_preserves_null_default_annotation(self) -> None:
        unrestricted_json = {
            "anyOf": [
                {"additionalProperties": True, "type": "object"},
                {"items": {}, "type": "array"},
                {"type": "boolean"},
                {"type": "integer"},
                {"type": "null"},
                {"type": "number"},
                {"type": "string"},
            ],
            "default": None,
        }

        self.assertEqual(
            compare_specs(
                response_schema_spec(unrestricted_json),
                response_schema_spec({"default": None}),
            ),
            ([], {}, {}),
        )


if __name__ == "__main__":
    unittest.main()
