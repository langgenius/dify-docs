#!/usr/bin/env python3
"""
OpenAPI Translation Pipeline

Complete pipeline for translating OpenAPI JSON files:
Extract → Translate → Re-hydrate
"""

from .extractor import OpenAPIExtractor
from .translator import OpenAPITranslator
from .rehydrator import OpenAPIRehydrator
import os
from pathlib import Path
import tempfile


def translate_openapi_file(source_file: str, target_lang: str, output_file: str, dify_api_key: str = None) -> bool:
    """
    Complete pipeline to translate an OpenAPI JSON file.

    Pipeline stages:
    1. Extract: Pull all translatable fields into markdown
    2. Translate: Send to Dify API for translation
    3. Re-hydrate: Merge translations back into JSON structure

    Args:
        source_file: Path to source English OpenAPI JSON file
        target_lang: Target language code (cn, jp)
        output_file: Path to save translated JSON file
        dify_api_key: Optional Dify API key (if None, loads from env)

    Returns:
        True if successful, False otherwise
    """
    # Create temp directory for intermediate files
    temp_dir = tempfile.mkdtemp(prefix=f"openapi_translation_{os.path.basename(source_file)}_")

    try:
        print(f"\n{'='*60}")
        print(f"🌐 Translating OpenAPI: {os.path.basename(source_file)} → {target_lang}")
        print(f"{'='*60}\n")

        # Define temp file paths
        extraction_map_path = os.path.join(temp_dir, "extraction_map.json")
        markdown_path = os.path.join(temp_dir, "translation_input.md")
        translated_md_path = os.path.join(temp_dir, f"translation_output_{target_lang}.md")

        # Step 1: Extract translatable fields
        print(f"📤 Step 1/3: Extracting translatable fields from {source_file}...")
        extractor = OpenAPIExtractor(source_file)
        fields, markdown = extractor.extract()

        extractor.save_extraction_map(extraction_map_path)
        extractor.save_markdown(markdown_path, markdown)

        print(f"   ✓ Extracted {len(fields)} fields")
        print(f"   ✓ Saved extraction map: {extraction_map_path}")
        print(f"   ✓ Saved markdown for translation: {markdown_path}")

        # Step 2: Translate via Dify API
        print(f"\n🌐 Step 2/3: Translating to {target_lang}...")
        translator = OpenAPITranslator(markdown_path, target_lang, dify_api_key)
        translated_text = translator.translate()

        translator.save_translation(translated_md_path, translated_text)
        print(f"   ✓ Translation complete")
        print(f"   ✓ Saved translated markdown: {translated_md_path}")

        # Step 3: Re-hydrate JSON structure
        print(f"\n💧 Step 3/3: Re-hydrating JSON structure...")
        rehydrator = OpenAPIRehydrator(source_file, extraction_map_path)
        rehydrator.load_translation(translated_md_path)
        stats = rehydrator.rehydrate(output_file)

        print(f"   ✓ Created translated JSON: {output_file}")
        print(f"   📊 Stats: {stats['updated']}/{stats['total']} fields translated")

        if stats['missing'] > 0:
            print(f"   ⚠️  {stats['missing']} fields kept in English (missing translations)")

        print(f"\n{'='*60}")
        print(f"✅ Translation pipeline completed successfully!")
        print(f"   Source: {source_file}")
        print(f"   Output: {output_file}")
        print(f"   Language: {target_lang}")
        print(f"   Fields translated: {stats['updated']}/{stats['total']}")
        print(f"{'='*60}\n")

        return True

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Translation pipeline failed!")
        print(f"   Error: {str(e)}")
        print(f"{'='*60}\n")

        import traceback
        traceback.print_exc()

        return False

    finally:
        # Optional: Cleanup temp files
        # Uncomment to enable cleanup
        # import shutil
        # shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"🗂️  Temp files kept for debugging: {temp_dir}")


# Export main function
__all__ = ['translate_openapi_file', 'OpenAPIExtractor', 'OpenAPITranslator', 'OpenAPIRehydrator']
