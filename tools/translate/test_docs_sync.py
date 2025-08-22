#!/usr/bin/env python3
"""Test script for docs.json synchronization only"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sync_and_translate import DocsSynchronizer

def main():
    """Test docs.json sync without API calls"""
    # Initialize synchronizer with dummy API key 
    synchronizer = DocsSynchronizer("dummy-key")
    
    print("=== Testing docs.json Structure Synchronization ===")
    
    # Run only the docs.json sync
    results = synchronizer.sync_docs_json_structure()
    
    print("\n=== SYNC RESULTS ===")
    for log in results:
        print(f"  {log}")
    
    print("\n✓ Test completed")

if __name__ == "__main__":
    main()