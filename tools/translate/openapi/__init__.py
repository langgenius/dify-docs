"""OpenAPI translation utilities.

Extract translatable fields from an OpenAPI JSON file into markdown, and re-hydrate translated markdown back into the JSON structure. The translation of the extracted markdown is produced by the writer (typically with an AI agent) following the rules in `tools/translate/`.
"""

from .extractor import OpenAPIExtractor
from .rehydrator import OpenAPIRehydrator

__all__ = ["OpenAPIExtractor", "OpenAPIRehydrator"]
