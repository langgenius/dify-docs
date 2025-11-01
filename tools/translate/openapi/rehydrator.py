#!/usr/bin/env python3
"""
OpenAPI Re-hydrator

Merges translated text back into the original JSON structure using extraction map.
"""

import json
import re
from typing import Dict, List
from pathlib import Path


class OpenAPIRehydrator:
    """Re-hydrates OpenAPI JSON with translated text."""

    def __init__(self, original_json_path: str, extraction_map_path: str):
        """
        Initialize the re-hydrator.

        Args:
            original_json_path: Path to the original English JSON file
            extraction_map_path: Path to the extraction map JSON created during extraction
        """
        self.original_json_path = original_json_path
        self.extraction_map_path = extraction_map_path
        self.translation_map = {}  # field_id -> translated_text

    def load_translation(self, translated_md_path: str):
        """
        Parse translated markdown into field_id -> text mapping.

        Args:
            translated_md_path: Path to the translated markdown file

        Expected format:
        ## FIELD_0000
        [PATH: info.title]
        Translated text here

        ## FIELD_0001
        [PATH: info.description]
        Translated description here
        """
        with open(translated_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by field markers
        sections = re.split(r'\n## (FIELD_\d+)\n', content)

        # Process sections (pattern: text, field_id, section_content, field_id, section_content, ...)
        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break

            field_id = sections[i]
            section_content = sections[i + 1]

            # Extract translated text after [PATH: ...] line
            lines = section_content.split('\n')
            path_line_found = False
            translated_text_lines = []

            for line in lines:
                if line.startswith('[PATH:'):
                    path_line_found = True
                    continue
                if path_line_found and line.strip():
                    translated_text_lines.append(line)

            # Join lines and strip whitespace
            translated_text = '\n'.join(translated_text_lines).strip()

            if translated_text:
                self.translation_map[field_id] = translated_text

        print(f"📝 Parsed {len(self.translation_map)} translated fields from markdown")

    def rehydrate(self, output_path: str) -> Dict[str, int]:
        """
        Create translated JSON file by merging translations into original structure.

        Args:
            output_path: Path to save the translated JSON file

        Returns:
            Statistics dict with keys: updated, missing, total
        """
        # Load original JSON
        with open(self.original_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load extraction map
        with open(self.extraction_map_path, 'r', encoding='utf-8') as f:
            extraction_map = json.load(f)

        # Apply translations
        fields_updated = 0
        fields_missing = []

        for field_info in extraction_map['fields']:
            field_id = field_info['id']
            path = field_info['path']
            original_value = field_info['value']

            # Get translated text
            translated_text = self.translation_map.get(field_id)

            if translated_text:
                # Navigate and update
                try:
                    self._set_nested_value(data, path, translated_text)
                    fields_updated += 1
                except Exception as e:
                    print(f"⚠️  Error setting {field_id} at path {path}: {e}")
                    fields_missing.append(field_id)
            else:
                # Fallback to English
                fields_missing.append(field_id)
                print(f"⚠️  Missing translation for {field_id} (path: {'.'.join(str(p) for p in path)})")
                print(f"    Keeping English: {original_value[:80]}...")

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save translated JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        stats = {
            "updated": fields_updated,
            "missing": len(fields_missing),
            "total": len(extraction_map['fields'])
        }

        print(f"✅ Re-hydration complete: {fields_updated}/{stats['total']} fields updated")
        if fields_missing:
            print(f"⚠️  {len(fields_missing)} fields kept in English")

        return stats

    def _set_nested_value(self, obj, path: List, value: str):
        """
        Navigate JSON path and set value.

        Args:
            obj: Root JSON object
            path: List of keys/indices representing the path
            value: Value to set

        Example path: ['paths', '/chat-messages', 'post', 'summary']
        Example path with array: ['servers', '[0]', 'description']
        """
        current = obj

        # Navigate to parent
        for key in path[:-1]:
            if isinstance(key, str) and key.startswith('[') and key.endswith(']'):
                # Array index
                idx = int(key[1:-1])
                current = current[idx]
            else:
                current = current[key]

        # Set final value
        final_key = path[-1]
        if isinstance(final_key, str) and final_key.startswith('[') and final_key.endswith(']'):
            # Array index
            idx = int(final_key[1:-1])
            current[idx] = value
        else:
            current[final_key] = value
