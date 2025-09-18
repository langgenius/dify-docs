#!/usr/bin/env python3
"""
Script to find documentation files that are not included in docs.json
"""

import json
import os
from pathlib import Path

def extract_pages_from_docs_json(docs_data):
    """Recursively extract all page file paths from docs.json structure"""
    pages = set()

    def extract_from_item(item):
        if isinstance(item, dict):
            # Check for 'page' key (file reference)
            if 'page' in item:
                # Normalize path - remove leading slash if present
                page_path = item['page'].lstrip('/')
                pages.add(page_path)

            # Check all keys for nested structures
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    extract_from_item(value)

        elif isinstance(item, list):
            for sub_item in item:
                if isinstance(sub_item, str):
                    # Direct page reference as string
                    pages.add(sub_item.lstrip('/'))
                else:
                    extract_from_item(sub_item)

        elif isinstance(item, str):
            # Direct page reference
            pages.add(item.lstrip('/'))

    # Start extraction from root
    extract_from_item(docs_data)

    return pages

def find_all_doc_files(root_path):
    """Find all .md and .mdx files in the repository"""
    doc_files = set()

    # Walk through the directory tree
    for root, dirs, files in os.walk(root_path):
        # Skip hidden directories and common non-doc directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'dist', 'build']]

        for file in files:
            if file.endswith(('.md', '.mdx')):
                # Get relative path from root
                full_path = Path(root) / file
                rel_path = full_path.relative_to(root_path)
                doc_files.add(str(rel_path))

    return doc_files

def main():
    # Get the project root
    project_root = Path('/Users/guchenhe/Desktop/werk/projects/dify-docs')

    # Read docs.json
    docs_json_path = project_root / 'docs.json'

    if not docs_json_path.exists():
        print(f"Error: docs.json not found at {docs_json_path}")
        return

    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)

    # Extract pages from docs.json
    print("Extracting pages from docs.json...")
    included_pages = extract_pages_from_docs_json(docs_data)

    # Add .mdx extension if not present (docs.json might not include extensions)
    included_pages_with_ext = set()
    for page in included_pages:
        if not page.endswith(('.md', '.mdx')):
            included_pages_with_ext.add(f"{page}.mdx")
            included_pages_with_ext.add(f"{page}.md")
        else:
            included_pages_with_ext.add(page)

    # Find all doc files
    print("Finding all documentation files in the repository...")
    all_doc_files = find_all_doc_files(project_root)

    # Find files not included
    missing_files = []
    for doc_file in sorted(all_doc_files):
        # Check if file is included (with or without extension variations)
        doc_file_no_ext = str(Path(doc_file).with_suffix(''))

        is_included = (
            doc_file in included_pages or
            doc_file in included_pages_with_ext or
            doc_file_no_ext in included_pages or
            doc_file.replace('.md', '') in included_pages or
            doc_file.replace('.mdx', '') in included_pages
        )

        if not is_included:
            missing_files.append(doc_file)

    # Write results to file
    output_file = project_root / 'missing_docs.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Documentation files not included in docs.json:\n")
        f.write("=" * 50 + "\n\n")

        if missing_files:
            # Group by directory for better readability
            by_directory = {}
            for file in missing_files:
                directory = str(Path(file).parent)
                if directory not in by_directory:
                    by_directory[directory] = []
                by_directory[directory].append(file)

            for directory in sorted(by_directory.keys()):
                f.write(f"\n## Directory: {directory}\n")
                for file in sorted(by_directory[directory]):
                    f.write(f"  - {file}\n")

            f.write(f"\n\nTotal missing files: {len(missing_files)}\n")
        else:
            f.write("All documentation files are included in docs.json!\n")

    # Print summary
    print(f"\nSummary:")
    print(f"- Total documentation files found: {len(all_doc_files)}")
    print(f"- Files referenced in docs.json: {len(included_pages)}")
    print(f"- Files NOT in docs.json: {len(missing_files)}")
    print(f"\nResults written to: {output_file}")

    if missing_files:
        print(f"\nFirst 10 missing files:")
        for file in missing_files[:10]:
            print(f"  - {file}")
        if len(missing_files) > 10:
            print(f"  ... and {len(missing_files) - 10} more")

if __name__ == "__main__":
    main()