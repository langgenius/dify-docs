#!/usr/bin/env python3
"""Test script for FAQ translation only"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(__file__))

from sync_and_translate import DocsSynchronizer

async def main():
    """Test FAQ translation only"""
    if len(sys.argv) < 2:
        print("Usage: python test_faq_only.py <dify_api_key>")
        sys.exit(1)
    
    dify_api_key = sys.argv[1]
    synchronizer = DocsSynchronizer(dify_api_key)
    
    print("=== Testing FAQ File Translation ===")
    
    # Test translating just the FAQ file
    faq_file = "en/documentation/pages/getting-started/faq.mdx"
    
    try:
        # Test Chinese translation
        print(f"\nTranslating {faq_file} to Chinese...")
        zh_result = await synchronizer.translate_file_with_notice(
            faq_file,
            "zh-hans/documentation/pages/getting-started/faq.mdx", 
            "zh-hans"
        )
        print(f"Chinese result: {zh_result}")
        
        # Test Japanese translation  
        print(f"\nTranslating {faq_file} to Japanese...")
        ja_result = await synchronizer.translate_file_with_notice(
            faq_file,
            "ja-jp/documentation/pages/getting-started/faq.mdx",
            "ja-jp"
        )
        print(f"Japanese result: {ja_result}")
        
        # Test docs.json sync
        print(f"\nTesting docs.json structure sync...")
        sync_results = synchronizer.sync_docs_json_structure()
        for result in sync_results:
            print(f"  {result}")
        
        print("\n✓ FAQ test completed")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())