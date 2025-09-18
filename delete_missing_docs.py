#!/usr/bin/env python3
"""
Script to delete documentation files listed in missing_docs.txt
with directory-by-directory approval and automatic empty directory cleanup
"""

import os
import re
from pathlib import Path
from typing import List, Set

def parse_missing_docs_file(file_path: Path) -> dict:
    """Parse the missing_docs.txt file and group files by directory"""
    files_by_directory = {}
    current_directory = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            # Skip empty lines and headers
            if not line or line.startswith('=') or line.startswith('Documentation files'):
                continue

            # Check if this is a directory header
            if line.startswith('## Directory:'):
                current_directory = line.replace('## Directory:', '').strip()
                if current_directory not in files_by_directory:
                    files_by_directory[current_directory] = []

            # Check if this is a file entry
            elif line.strip().startswith('- '):
                if current_directory is not None:
                    file_path = line.strip()[2:].strip()  # Remove "- " prefix
                    files_by_directory[current_directory].append(file_path)

    return files_by_directory

def delete_empty_directories(start_path: Path, root_path: Path):
    """Recursively delete empty directories up to the root path"""
    current = start_path

    while current != root_path and current.exists():
        try:
            # Check if directory is empty
            if current.is_dir() and not any(current.iterdir()):
                print(f"  Removing empty directory: {current}")
                current.rmdir()
                # Move up to parent directory
                current = current.parent
            else:
                # Directory not empty or doesn't exist, stop
                break
        except Exception as e:
            print(f"  Could not remove directory {current}: {e}")
            break

def confirm_action(prompt: str) -> bool:
    """Ask user for confirmation"""
    while True:
        response = input(f"{prompt} (y/n/q): ").lower().strip()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        elif response == 'q':
            print("\nQuitting...")
            exit(0)
        else:
            print("Please enter 'y' for yes, 'n' for no, or 'q' to quit")

def main():
    # Setup paths
    project_root = Path('/Users/guchenhe/Desktop/werk/projects/dify-docs')
    missing_docs_file = project_root / 'missing_docs.txt'

    if not missing_docs_file.exists():
        print(f"Error: {missing_docs_file} not found")
        print("Please run check_missing_docs.py first to generate the list")
        return

    # Parse the missing docs file
    print("Parsing missing_docs.txt...")
    files_by_directory = parse_missing_docs_file(missing_docs_file)

    if not files_by_directory:
        print("No files found to delete")
        return

    # Summary
    total_files = sum(len(files) for files in files_by_directory.values())
    print(f"\nFound {total_files} files in {len(files_by_directory)} directories to delete")
    print("\n" + "=" * 60)
    print("DELETION PROCESS")
    print("=" * 60)
    print("\nYou will be asked to approve deletion for each directory.")
    print("Options: y=yes, n=no (skip directory), q=quit")
    print("Empty directories will be automatically removed after file deletion.")
    print("\n" + "=" * 60)

    if not confirm_action("\nReady to start the deletion process?"):
        print("Deletion cancelled")
        return

    # Track statistics
    deleted_files = 0
    skipped_files = 0
    deleted_directories = set()

    # Process each directory
    for directory, files in sorted(files_by_directory.items()):
        print(f"\n{'='*60}")
        print(f"Directory: {directory}")
        print(f"Files to delete: {len(files)}")

        # Show first few files as preview
        preview_count = min(5, len(files))
        print("\nFiles preview:")
        for i, file in enumerate(files[:preview_count]):
            print(f"  - {file}")
        if len(files) > preview_count:
            print(f"  ... and {len(files) - preview_count} more files")

        # Ask for confirmation
        if not confirm_action(f"\nDelete all {len(files)} files in this directory?"):
            print(f"Skipping directory: {directory}")
            skipped_files += len(files)
            continue

        # Delete files in this directory
        print(f"\nDeleting files in {directory}...")
        directory_deleted_count = 0

        for file_path_str in files:
            file_path = project_root / file_path_str
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"  ✓ Deleted: {file_path_str}")
                    directory_deleted_count += 1
                    deleted_files += 1
                except Exception as e:
                    print(f"  ✗ Error deleting {file_path_str}: {e}")
                    skipped_files += 1
            else:
                print(f"  - File not found (already deleted?): {file_path_str}")
                skipped_files += 1

        print(f"  Deleted {directory_deleted_count} files from {directory}")

        # Clean up empty directories
        if directory_deleted_count > 0:
            dir_path = project_root / directory
            if dir_path.exists():
                print(f"\nChecking for empty directories to clean up...")
                delete_empty_directories(dir_path, project_root)

    # Final summary
    print(f"\n{'='*60}")
    print("DELETION COMPLETE")
    print(f"{'='*60}")
    print(f"Files deleted: {deleted_files}")
    print(f"Files skipped: {skipped_files}")
    print(f"Total files processed: {deleted_files + skipped_files}")

    # Option to delete the missing_docs.txt file itself
    if deleted_files > 0:
        print(f"\n{'='*60}")
        if confirm_action("\nDelete missing_docs.txt file as well?"):
            try:
                missing_docs_file.unlink()
                print("✓ Deleted missing_docs.txt")
            except Exception as e:
                print(f"✗ Error deleting missing_docs.txt: {e}")

    print("\nDone!")

if __name__ == "__main__":
    main()