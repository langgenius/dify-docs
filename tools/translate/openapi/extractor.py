#!/usr/bin/env python3
"""
OpenAPI Field Extractor

Recursively extracts translatable fields (title, summary, description) from OpenAPI JSON files.
Generates a markdown file for translation and an extraction map for re-hydration.
"""

import json
from typing import List, Dict, Tuple
from pathlib import Path


class OpenAPIExtractor:
    """Extracts translatable fields from OpenAPI JSON structure."""

    def __init__(self, json_file_path: str, translatable_fields: List[str] = None):
        """
        Initialize the extractor.

        Args:
            json_file_path: Path to the source OpenAPI JSON file
            translatable_fields: List of field names to extract (default: title, summary, description)
        """
        self.source_path = json_file_path
        self.translatable_fields = translatable_fields or ["title", "summary", "description"]
        self.fields = []  # List of {id, path, value}

    def extract(self) -> Tuple[List[Dict], str]:
        """
        Extract all translatable fields from the JSON file.

        Returns:
            Tuple of (extraction_map list, markdown content string)
        """
        with open(self.source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Recursively walk and extract
        self._walk(data, path=[])

        # Generate markdown
        markdown = self._generate_markdown()

        return self.fields, markdown

    def _walk(self, obj, path: List):
        """
        Recursively walk JSON tree to find translatable fields.

        Args:
            obj: Current object (dict, list, or primitive)
            path: Current path as list of keys/indices
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = path + [key]

                # Check if this is a translatable field
                if key in self.translatable_fields and isinstance(value, str) and value.strip():
                    field_id = f"FIELD_{len(self.fields):04d}"
                    self.fields.append({
                        "id": field_id,
                        "path": current_path.copy(),
                        "value": value
                    })
                else:
                    # Recurse deeper
                    self._walk(value, current_path)

        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                current_path = path + [f"[{idx}]"]
                self._walk(item, current_path)

    def _generate_markdown(self) -> str:
        """
        Generate markdown content for translation.

        Format:
        ## FIELD_0000
        [PATH: info.title]
        Chat App API

        Returns:
            Markdown string ready for translation
        """
        lines = ["# OpenAPI Translation Input\n"]

        for field in self.fields:
            path_str = ".".join(str(p) for p in field["path"])
            lines.append(f"## {field['id']}")
            lines.append(f"[PATH: {path_str}]")
            lines.append(field["value"])
            lines.append("")  # blank line separator

        return "\n".join(lines)

    def save_extraction_map(self, output_path: str):
        """
        Save extraction metadata as JSON for later re-hydration.

        Args:
            output_path: Path to save the extraction map JSON file
        """
        extraction_data = {
            "source_file": str(self.source_path),
            "field_count": len(self.fields),
            "translatable_fields": self.translatable_fields,
            "fields": self.fields
        }

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)

    def save_markdown(self, output_path: str, markdown: str):
        """
        Save generated markdown to file.

        Args:
            output_path: Path to save the markdown file
            markdown: Markdown content string
        """
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
