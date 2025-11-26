"""
Format-preserving JSON serialization utilities.

This module detects and preserves the exact formatting of existing JSON files,
allowing surgical edits without reformatting the entire file.
"""

import json
import re
from typing import Any, Dict, Optional, Tuple
from pathlib import Path


class JSONFormat:
    """Detected JSON formatting style"""

    def __init__(self):
        self.indent_char = ' '  # ' ' or '\t'
        self.indent_size = 4  # Number of indent chars per level
        self.indent_pattern = 'consistent'  # 'consistent' or 'mixed'
        self.indent_increments = [4]  # List of space counts per level
        self.trailing_newline = True
        self.key_spacing = True  # Space after colon: "key": value vs "key":value

    def __repr__(self):
        return (f"JSONFormat(char={repr(self.indent_char)}, "
                f"size={self.indent_size}, pattern={self.indent_pattern}, "
                f"increments={self.indent_increments})")


def detect_json_format(file_path: str) -> JSONFormat:
    """
    Detect the formatting style of an existing JSON file.

    Analyzes indentation pattern, whitespace, and structural formatting
    to enable format-preserving edits.
    """
    fmt = JSONFormat()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Check trailing newline
    fmt.trailing_newline = content.endswith('\n')

    # Detect indent character and pattern by tracking absolute indent levels
    indent_levels = {}  # Maps absolute space count to frequency

    for line_num, line in enumerate(lines[:300]):  # Sample first 300 lines
        if not line.strip() or line.strip().startswith('//'):
            continue

        # Count leading whitespace
        stripped = line.lstrip(' \t')
        if not stripped:
            continue

        spaces = len(line) - len(stripped)
        tabs = line[:spaces].count('\t')

        # Detect tab vs space
        if tabs > 0:
            fmt.indent_char = '\t'
            indent_count = tabs
        else:
            indent_count = spaces

        if indent_count > 0:
            indent_levels[indent_count] = indent_levels.get(indent_count, 0) + 1

    if not indent_levels:
        # Fallback to default
        return fmt

    # Sort indent levels to build the actual progression
    sorted_levels = sorted(indent_levels.keys())

    # Build increment pattern from actual levels seen
    increments = []
    if sorted_levels:
        prev_level = 0
        for level in sorted_levels:
            increment = level - prev_level
            increments.append(increment)
            prev_level = level

    # Check if consistent (all increments the same)
    unique_increments = list(set(increments))

    if len(unique_increments) == 1:
        fmt.indent_pattern = 'consistent'
        fmt.indent_size = unique_increments[0]
        fmt.indent_increments = [unique_increments[0]]
    else:
        fmt.indent_pattern = 'mixed'
        fmt.indent_increments = increments

    # Detect key spacing (": " vs ":")
    colon_samples = [line for line in lines[:100] if '":' in line]
    if colon_samples:
        with_space = sum(1 for line in colon_samples if '": ' in line)
        fmt.key_spacing = with_space > len(colon_samples) // 2

    return fmt


def get_indent_for_level(fmt: JSONFormat, level: int) -> str:
    """
    Get the indent string for a specific nesting level.
    Handles both consistent and mixed indent patterns.
    """
    if level == 0:
        return ''

    if fmt.indent_pattern == 'consistent':
        count = fmt.indent_size * level
    else:
        # For mixed patterns, sum up increments up to this level
        # increments[0] is the increment from level 0 to level 1
        # increments[1] is the increment from level 1 to level 2, etc.
        count = 0
        for i in range(level):
            if i < len(fmt.indent_increments):
                count += fmt.indent_increments[i]
            else:
                # If we run out of recorded increments, use the last one
                count += fmt.indent_increments[-1] if fmt.indent_increments else 2

    return fmt.indent_char * count


def format_preserving_json_dump(data: Any, fmt: JSONFormat, level: int = 0) -> str:
    """
    Serialize JSON data while preserving the detected formatting style.

    This custom serializer respects:
    - Detected indent pattern (consistent vs mixed)
    - Space vs tab indentation
    - Key spacing preferences
    - Trailing newline conventions

    Note: level indicates the nesting depth of the current structure's opening brace.
    """
    indent = get_indent_for_level(fmt, level)
    child_indent = get_indent_for_level(fmt, level + 1)
    colon = ': ' if fmt.key_spacing else ':'

    if isinstance(data, dict):
        if not data:
            return '{}'

        lines = ['{']
        items = list(data.items())

        for i, (key, value) in enumerate(items):
            is_last = (i == len(items) - 1)
            # Serialize child values at the same structural level (they'll handle their own nesting)
            serialized_value = format_preserving_json_dump(value, fmt, level + 1)

            # Check if value is multiline
            if '\n' in serialized_value:
                # Multiline value (object or array) - needs special handling
                value_lines = serialized_value.split('\n')
                comma = '' if is_last else ','
                # First line goes on same line as key
                lines.append(f'{child_indent}"{key}"{colon}{value_lines[0]}')
                # Remaining lines keep their indentation
                for vline in value_lines[1:-1]:
                    lines.append(vline)
                # Last line gets the comma
                lines.append(value_lines[-1] + comma)
            else:
                # Single line value
                comma = '' if is_last else ','
                lines.append(f'{child_indent}"{key}"{colon}{serialized_value}{comma}')

        lines.append(f'{indent}}}')
        return '\n'.join(lines)

    elif isinstance(data, list):
        if not data:
            return '[]'

        lines = ['[']

        for i, item in enumerate(data):
            is_last = (i == len(data) - 1)
            serialized_item = format_preserving_json_dump(item, fmt, level + 1)

            # Check if item is multiline
            if '\n' in serialized_item:
                # Multiline item needs proper indentation
                item_lines = serialized_item.split('\n')
                comma = '' if is_last else ','
                # First line gets child indent
                lines.append(f'{child_indent}{item_lines[0]}')
                # Remaining lines keep their indentation
                for iline in item_lines[1:-1]:
                    lines.append(iline)
                # Last line gets the comma
                lines.append(item_lines[-1] + comma)
            else:
                # Single line item
                comma = '' if is_last else ','
                lines.append(f'{child_indent}{serialized_item}{comma}')

        lines.append(f'{indent}]')
        return '\n'.join(lines)

    elif isinstance(data, str):
        # Escape special characters
        escaped = json.dumps(data, ensure_ascii=False)
        return escaped

    elif isinstance(data, bool):
        return 'true' if data else 'false'

    elif data is None:
        return 'null'

    elif isinstance(data, (int, float)):
        return str(data)

    else:
        # Fallback to standard JSON serialization
        return json.dumps(data, ensure_ascii=False)


def save_json_with_preserved_format(file_path: str, data: Dict[str, Any],
                                   reference_file: Optional[str] = None) -> bool:
    """
    Save JSON data to file while preserving the original formatting style.

    Args:
        file_path: Path to JSON file to write
        data: Dictionary to serialize
        reference_file: Optional path to reference file for format detection.
                       If not provided, uses file_path for detection.

    Returns:
        True if successful, False otherwise
    """
    try:
        # Detect format from reference file or existing target file
        format_source = reference_file if reference_file else file_path

        if Path(format_source).exists():
            fmt = detect_json_format(format_source)
        else:
            # Use sensible defaults for new files
            fmt = JSONFormat()
            fmt.indent_size = 4
            fmt.indent_pattern = 'consistent'

        # Serialize with preserved format
        content = format_preserving_json_dump(data, fmt, level=0)

        # Add trailing newline if detected in original
        if fmt.trailing_newline and not content.endswith('\n'):
            content += '\n'

        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"Error saving JSON with preserved format: {e}")
        return False


def validate_format_preservation(original_path: str, new_path: str) -> Dict[str, Any]:
    """
    Validate that formatting was preserved between two JSON files.

    Returns a report with:
    - matching: bool (whether formats match)
    - differences: list of detected differences
    - original_format: detected format from original
    - new_format: detected format from new file
    """
    original_fmt = detect_json_format(original_path)
    new_fmt = detect_json_format(new_path)

    differences = []

    if original_fmt.indent_char != new_fmt.indent_char:
        differences.append(f"Indent char: {repr(original_fmt.indent_char)} → {repr(new_fmt.indent_char)}")

    if original_fmt.indent_pattern != new_fmt.indent_pattern:
        differences.append(f"Indent pattern: {original_fmt.indent_pattern} → {new_fmt.indent_pattern}")

    if original_fmt.indent_size != new_fmt.indent_size:
        differences.append(f"Indent size: {original_fmt.indent_size} → {new_fmt.indent_size}")

    if original_fmt.trailing_newline != new_fmt.trailing_newline:
        differences.append(f"Trailing newline: {original_fmt.trailing_newline} → {new_fmt.trailing_newline}")

    return {
        'matching': len(differences) == 0,
        'differences': differences,
        'original_format': original_fmt,
        'new_format': new_fmt
    }
