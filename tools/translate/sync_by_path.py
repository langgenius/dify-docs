#!/usr/bin/env python3
"""
Enhanced sync script with path-based translation and additional flags.

Usage:
    # Translate specific file
    python sync_by_path.py --file en/use-dify/nodes/llm.mdx --api-key app-xxx

    # Translate entire directory
    python sync_by_path.py --dir en/develop-plugin --api-key app-xxx

    # Dry run (show what would be translated)
    python sync_by_path.py --file en/test.mdx --api-key app-xxx --dry-run

    # Skip docs.json sync
    python sync_by_path.py --dir en/use-dify/nodes --api-key app-xxx --no-docs-sync

    # Force overwrite without prompting
    python sync_by_path.py --file en/test.mdx --api-key app-xxx --force

    # Read API key from .env
    python sync_by_path.py --file en/test.mdx
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Import from existing sync script
from sync_and_translate import DocsSynchronizer

async def sync_by_paths(
    api_key: str,
    files: Optional[List[str]] = None,
    directory: Optional[str] = None,
    dry_run: bool = False,
    sync_docs_json: bool = True,
    delete_mode: bool = False,
    force: bool = False
) -> Dict[str, List[str]]:
    """
    Sync translation by specific files or directory

    Args:
        api_key: Dify API key
        files: List of specific file paths to translate
        directory: Directory to translate all files from
        dry_run: If True, only show what would be done
        sync_docs_json: If True, sync docs.json structure
        delete_mode: If True, delete translated files and remove from docs.json
        force: If True, overwrite existing files without prompting
    """
    results = {
        "translated": [],
        "skipped": [],
        "errors": [],
        "docs_json_synced": False
    }

    # Initialize synchronizer
    synchronizer = DocsSynchronizer(api_key)
    base_dir = synchronizer.base_dir

    # Collect files to translate
    files_to_translate = []

    if files:
        files_to_translate.extend(files)

    if directory:
        # Find all .md/.mdx files in directory
        dir_path = base_dir / directory
        if not dir_path.exists():
            results["errors"].append(f"Directory not found: {directory}")
            return results

        for ext in ['.md', '.mdx']:
            files_to_translate.extend([
                str(p.relative_to(base_dir))
                for p in dir_path.rglob(f'*{ext}')
            ])

    if not files_to_translate:
        results["errors"].append("No files specified")
        return results

    # Filter to only source language files
    source_dir = synchronizer.get_language_directory(synchronizer.source_language)
    files_to_translate = [
        f for f in files_to_translate
        if f.startswith(f"{source_dir}/")
    ]

    if not files_to_translate:
        results["errors"].append(f"No {source_dir}/ files found")
        return results

    print(f"Found {len(files_to_translate)} file(s):")
    for f in files_to_translate:
        print(f"  • {f}")

    if dry_run:
        if delete_mode:
            print("\n[DRY RUN] Would DELETE translations:")
            for source_file in files_to_translate:
                for target_lang in synchronizer.target_languages:
                    target_file = synchronizer.convert_path_to_target_language(
                        source_file, target_lang
                    )
                    print(f"  • {target_file}")

            if sync_docs_json:
                print("\n[DRY RUN] Would modify docs.json:")
                preview_docs_json_changes(
                    synchronizer, files_to_translate, delete_mode=True
                )
        else:
            print("\n[DRY RUN] Would translate to:")
            for source_file in files_to_translate:
                for target_lang in synchronizer.target_languages:
                    target_file = synchronizer.convert_path_to_target_language(
                        source_file, target_lang
                    )
                    print(f"  • {source_file} → {target_file}")

            if sync_docs_json:
                print("\n[DRY RUN] Would modify docs.json:")
                preview_docs_json_changes(
                    synchronizer, files_to_translate, delete_mode=False
                )
            else:
                print("\n[DRY RUN] Would skip docs.json sync (--no-docs-sync)")

        return results

    # Delete or translate files
    if delete_mode:
        print("\nDeleting translations...")
        for source_file in files_to_translate:
            # Delete translated files
            for target_lang in synchronizer.target_languages:
                target_file = synchronizer.convert_path_to_target_language(
                    source_file, target_lang
                )
                target_path = base_dir / target_file

                if target_path.exists():
                    try:
                        target_path.unlink()
                        results["translated"].append(f"DELETED: {target_file}")
                        print(f"✓ Deleted {target_file}")
                    except Exception as e:
                        results["errors"].append(f"Error deleting {target_file}: {e}")
                else:
                    results["skipped"].append(f"{target_file} (not found)")
    else:
        print("\nStarting translation...")
        overwrite_preference = None  # Track user's preference: 'all' or 'skip_all'

        for source_file in files_to_translate:
            source_path = base_dir / source_file

            if not source_path.exists():
                results["skipped"].append(f"{source_file} (not found)")
                continue

            # Translate to each target language
            for target_lang in synchronizer.target_languages:
                target_file = synchronizer.convert_path_to_target_language(
                    source_file, target_lang
                )
                target_path = base_dir / target_file

                # Track if file is being updated or created
                is_update = target_path.exists()

                # Check if target file exists and prompt for overwrite if needed
                if is_update and not force:
                    # Use saved preference if user chose 'all' or 'skip_all'
                    if overwrite_preference == 'all':
                        should_overwrite = True
                    elif overwrite_preference == 'skip_all':
                        results["skipped"].append(f"{target_file} (user skipped)")
                        print(f"⊘ Skipped {target_file}")
                        continue
                    else:
                        # Prompt user for this specific file
                        response = prompt_overwrite(target_file)
                        if response == 'all':
                            overwrite_preference = 'all'
                            should_overwrite = True
                        elif response == 'skip_all':
                            overwrite_preference = 'skip_all'
                            results["skipped"].append(f"{target_file} (user skipped)")
                            print(f"⊘ Skipped {target_file}")
                            continue
                        elif response == 'yes':
                            should_overwrite = True
                        else:  # 'no'
                            results["skipped"].append(f"{target_file} (user skipped)")
                            print(f"⊘ Skipped {target_file}")
                            continue

                try:
                    # Prepare context for incremental translation if updating existing file
                    the_doc_exist = None
                    diff_original = None

                    if is_update:
                        # Read existing translation for context-aware update
                        try:
                            with open(target_path, 'r', encoding='utf-8') as f:
                                the_doc_exist = f.read()
                            print(f"  📝 Using incremental update (existing translation: {len(the_doc_exist)} chars)")
                        except Exception as e:
                            print(f"  ⚠️  Could not read existing translation: {e}")

                        # Try to get git diff for additional context (optional)
                        try:
                            diff_original = synchronizer.get_file_diff(source_file, "HEAD~1")
                            if diff_original:
                                print(f"  📊 Using git diff for context ({len(diff_original)} chars)")
                        except Exception:
                            # Git diff is optional - not all files may be in git yet
                            pass

                    print(f"Translating {source_file} → {target_file}...")
                    success = await synchronizer.translate_file_with_notice(
                        source_file,
                        target_file,
                        target_lang,
                        the_doc_exist=the_doc_exist,
                        diff_original=diff_original
                    )

                    if success:
                        results["translated"].append(target_file)
                        print(f"✓ {'Updated' if is_update else 'Created'} {target_file}")
                    else:
                        results["errors"].append(f"Failed: {source_file} → {target_file}")

                except Exception as e:
                    results["errors"].append(f"Error translating {source_file}: {e}")

    # Sync docs.json if requested
    if sync_docs_json:
        print("\nSyncing docs.json structure...")
        try:
            # Use the incremental sync method
            if delete_mode:
                sync_log = synchronizer.sync_docs_json_incremental(
                    added_files=[],
                    deleted_files=files_to_translate,
                    renamed_files=[]
                )
            else:
                sync_log = synchronizer.sync_docs_json_incremental(
                    added_files=files_to_translate,
                    deleted_files=[],
                    renamed_files=[]
                )

            if sync_log:
                print("Docs.json sync results:")
                for log in sync_log:
                    print(f"  {log}")
                results["docs_json_synced"] = True
            else:
                print("No docs.json updates needed")

        except Exception as e:
            results["errors"].append(f"Error syncing docs.json: {e}")
    else:
        print("\nSkipping docs.json sync (--no-docs-sync)")

    return results


def _get_group_path_from_location(file_location: List, target_section: Dict, dropdown_name: str, translated_dropdown_name: str = None) -> str:
    """
    Get a human-readable group path from file_location.

    Args:
        file_location: Location like ["groups", 0, "pages", 1]
        target_section: Target language section data
        dropdown_name: Name of the dropdown (source language)
        translated_dropdown_name: Translated name of the dropdown (for target language lookup)

    Returns:
        String like "Group: 'Getting Started'" or "pages" if no groups
    """
    if not file_location or not target_section:
        return "pages"

    # Find the dropdown using translated name if provided
    search_name = translated_dropdown_name if translated_dropdown_name else dropdown_name
    dropdowns = target_section.get("dropdowns", [])
    target_dropdown = None
    for dropdown in dropdowns:
        if dropdown.get("dropdown") == search_name:
            target_dropdown = dropdown
            break

    if not target_dropdown:
        return "pages"

    # Navigate through file_location to find group names
    group_names = []
    current = target_dropdown

    i = 0
    while i < len(file_location) - 1:  # Stop before final index
        key = file_location[i]

        if key == "groups" and i + 1 < len(file_location):
            idx = file_location[i + 1]
            groups = current.get("groups", [])
            if isinstance(idx, int) and idx < len(groups):
                group = groups[idx]
                if isinstance(group, dict):
                    group_names.append(group.get("group", f"group[{idx}]"))
                    # Navigate into nested pages if present
                    if "pages" in group:
                        current = group
            i += 2
        elif key == "pages" and i + 1 < len(file_location):
            idx = file_location[i + 1]
            pages = current.get("pages", [])
            if isinstance(idx, int) and idx < len(pages):
                item = pages[idx]
                if isinstance(item, dict) and "group" in item:
                    group_names.append(item.get("group", f"pages[{idx}]"))
                    current = item
            i += 2
        else:
            i += 1

    if group_names:
        return "Group: '" + "' > '".join(group_names) + "'"

    return "pages"


def _show_diff_preview(
    target_section: Dict,
    dropdown_name: str,
    file_location: List,
    changes: List[Dict],
    delete_mode: bool,
    translated_dropdown_name: str = None
) -> None:
    """
    Show git diff-style preview of changes to a pages array.

    Args:
        target_section: Target language section data
        dropdown_name: Name of the dropdown (source language)
        file_location: Location like ["groups", 0, "pages", 1]
        changes: List of changes with 'action' and 'file'
        delete_mode: If True, showing deletions; otherwise additions
        translated_dropdown_name: Translated name of the dropdown (for target language lookup)
    """
    # Find the dropdown using translated name if provided
    search_name = translated_dropdown_name if translated_dropdown_name else dropdown_name
    dropdowns = target_section.get("dropdowns", [])
    target_dropdown = None
    for dropdown in dropdowns:
        if dropdown.get("dropdown") == search_name:
            target_dropdown = dropdown
            break

    if not target_dropdown:
        print("      @@ (dropdown not found in target) @@")
        for change in changes:
            action = "-" if delete_mode else "+"
            print(f"      {action} {change['file']}")
        return

    # Navigate to the pages array using file_location
    current_pages = None
    current = target_dropdown

    # Build location string for display
    location_parts = []

    i = 0
    while i < len(file_location) - 1:  # Stop before final index
        key = file_location[i]

        if key == "groups" and i + 1 < len(file_location):
            idx = file_location[i + 1]
            location_parts.append(f"groups[{idx}]")
            groups = current.get("groups", [])
            if isinstance(idx, int) and idx < len(groups):
                current = groups[idx]
            i += 2
        elif key == "pages":
            location_parts.append("pages")
            if i + 1 < len(file_location):
                idx = file_location[i + 1]
                pages = current.get("pages", [])
                if isinstance(idx, int) and idx < len(pages):
                    item = pages[idx]
                    if isinstance(item, dict):
                        current = item
                    i += 2
                else:
                    # We've reached the final pages array
                    current_pages = pages
                    i += 1
            else:
                # Last element is "pages" key
                current_pages = current.get("pages", [])
                i += 1
        else:
            i += 1

    # Get the insertion index (last element of file_location)
    insert_idx = file_location[-1] if file_location and isinstance(file_location[-1], int) else None

    # If we haven't found pages yet, try getting from current
    if current_pages is None:
        current_pages = current.get("pages", []) if isinstance(current, dict) else []

    # Show the diff header
    location_str = ".".join(location_parts) if location_parts else "pages"
    print(f"    @@ {location_str} @@")

    # Collect all indices we need to show
    context_size = 2
    indices_to_show = set()

    if insert_idx is not None:
        # Show context around insertion point
        for i in range(max(0, insert_idx - context_size),
                      min(len(current_pages) + 1, insert_idx + context_size + 1)):
            indices_to_show.add(i)

    # For deletions, find where each file exists
    if delete_mode:
        for change in changes:
            file_path = change['file']
            for i, page in enumerate(current_pages):
                if isinstance(page, str) and page == file_path:
                    # Show context around this deletion
                    for ctx_i in range(max(0, i - context_size),
                                      min(len(current_pages), i + context_size + 1)):
                        indices_to_show.add(ctx_i)
                    break

    # Sort indices for display
    sorted_indices = sorted(indices_to_show)

    # Show the pages with changes
    if not delete_mode and insert_idx is not None:
        # Additions - show with consecutive indices
        for i in sorted_indices:
            if i == insert_idx:
                # Show all additions at consecutive positions starting from insert_idx
                for idx, change in enumerate(changes):
                    print(f"      + [{insert_idx + idx}] \"{change['file']}\"")
            elif i < len(current_pages):
                # Show existing pages
                page = current_pages[i]
                display_idx = i if i < insert_idx else i + len(changes)
                if isinstance(page, str):
                    print(f"        [{display_idx}] \"{page}\"")
                else:
                    print(f"        [{display_idx}] {page}")
    else:
        # Deletions or no specific insert index
        deletion_files = {change['file'] for change in changes}

        for i in sorted_indices:
            if i < len(current_pages):
                page = current_pages[i]
                if isinstance(page, str):
                    if page in deletion_files:
                        print(f"      - [{i}] \"{page}\"")
                    else:
                        print(f"        [{i}] \"{page}\"")
                else:
                    print(f"        [{i}] {page}")

    print()  # Blank line after each diff section


def preview_docs_json_changes(
    synchronizer,
    files: List[str],
    delete_mode: bool = False
) -> None:
    """
    Preview what changes would be made to docs.json without actually modifying it

    Args:
        synchronizer: DocsSynchronizer instance
        files: List of source files to add/delete
        delete_mode: If True, preview deletions; otherwise additions
    """
    try:
        docs_data = synchronizer.load_docs_json()
        if not docs_data or "navigation" not in docs_data:
            print("  ⚠️  Could not load docs.json")
            return

        navigation = docs_data["navigation"]

        # Get languages array
        languages_array = None
        if "languages" in navigation and isinstance(navigation["languages"], list):
            languages_array = navigation["languages"]
        elif "versions" in navigation and len(navigation["versions"]) > 0:
            if "languages" in navigation["versions"][0]:
                languages_array = navigation["versions"][0]["languages"]

        if not languages_array:
            print("  ⚠️  No languages found in docs.json")
            return

        # Find source section
        source_section = None
        for lang_data in languages_array:
            if lang_data.get("language") == synchronizer.source_language:
                source_section = lang_data
                break

        if not source_section:
            print("  ⚠️  Source language section not found")
            return

        # Find target language sections
        target_sections = {}
        for lang_data in languages_array:
            if lang_data.get("language") in synchronizer.target_languages:
                target_sections[lang_data.get("language")] = lang_data

        # Preview changes for each file
        changes_by_lang_location = {}  # Organize by lang > dropdown > group path
        for target_lang in synchronizer.target_languages:
            changes_by_lang_location[target_lang] = {}

        for source_file in files:
            # Strip extension for search (docs.json stores paths without extensions)
            source_file_no_ext = source_file.rstrip('.mdx').rstrip('.md')

            # Find dropdown and location
            result = synchronizer.find_dropdown_containing_file(source_file_no_ext, source_section)

            if not result:
                print(f"  ⚠️  {source_file} not found in source docs.json")
                continue

            dropdown_name, file_location = result

            # Get target file paths and preview changes
            for target_lang in synchronizer.target_languages:
                target_file = synchronizer.convert_path_to_target_language(
                    source_file, target_lang
                )
                target_file_no_ext = target_file.rstrip('.mdx').rstrip('.md')

                # Translate dropdown name for target language
                translated_dropdown = synchronizer.get_dropdown_translation(dropdown_name, target_lang)

                # Get group path for organization
                group_path_str = _get_group_path_from_location(
                    file_location,
                    target_sections.get(target_lang),
                    dropdown_name,
                    translated_dropdown
                )

                # Organize by dropdown and group path
                if dropdown_name not in changes_by_lang_location[target_lang]:
                    changes_by_lang_location[target_lang][dropdown_name] = {}

                if group_path_str not in changes_by_lang_location[target_lang][dropdown_name]:
                    changes_by_lang_location[target_lang][dropdown_name][group_path_str] = {
                        'location': file_location,
                        'translated_dropdown': translated_dropdown,
                        'changes': []
                    }

                changes_by_lang_location[target_lang][dropdown_name][group_path_str]['changes'].append({
                    'action': 'REMOVE' if delete_mode else 'ADD',
                    'file': target_file_no_ext,
                })

        # Print git diff-style preview
        for lang, dropdowns in changes_by_lang_location.items():
            if dropdowns:
                print(f"\n  Language: {lang}")

                for dropdown_name, groups in dropdowns.items():
                    for group_path_str, data in groups.items():
                        file_location = data['location']
                        translated_dropdown = data['translated_dropdown']
                        changes = data['changes']

                        # Get the target section and navigate to pages array
                        target_section = target_sections.get(lang)
                        if not target_section:
                            continue

                        # Show diff-style output
                        print(f"    Dropdown: '{dropdown_name}' > {group_path_str}")
                        print(f"    ")

                        _show_diff_preview(
                            target_section,
                            dropdown_name,
                            file_location,
                            changes,
                            delete_mode,
                            translated_dropdown
                        )

    except Exception as e:
        print(f"  ⚠️  Error previewing docs.json changes: {e}")


def prompt_overwrite(file_path: str) -> str:
    """
    Prompt user for confirmation to overwrite an existing file.

    Args:
        file_path: Path to the file that already exists

    Returns:
        One of: 'yes', 'no', 'all', 'skip_all'
    """
    while True:
        response = input(f"File {file_path} already exists. Overwrite? [y/n/all/skip_all]: ").strip().lower()
        if response in ['y', 'yes']:
            return 'yes'
        elif response in ['n', 'no']:
            return 'no'
        elif response in ['a', 'all']:
            return 'all'
        elif response in ['s', 'skip', 'skip_all', 'skip all']:
            return 'skip_all'
        else:
            print("Invalid input. Please enter 'y' (yes), 'n' (no), 'all' (overwrite all), or 'skip_all' (skip all).")


def load_api_key_from_env() -> Optional[str]:
    """Load API key from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('DIFY_API_KEY=') or line.startswith('dify_api_key='):
                    return line.split('=', 1)[1].strip()
    return None


async def main():
    parser = argparse.ArgumentParser(
        description='Translate documentation files by path',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate a single file
  %(prog)s --file en/use-dify/nodes/llm.mdx --api-key app-xxx

  # Translate entire directory
  %(prog)s --dir en/develop-plugin --api-key app-xxx

  # Multiple files
  %(prog)s --file en/file1.mdx --file en/file2.mdx --api-key app-xxx

  # Dry run
  %(prog)s --file en/test.mdx --dry-run

  # Skip docs.json sync
  %(prog)s --dir en/use-dify/nodes --no-docs-sync

  # Delete translations
  %(prog)s --file en/old-file.mdx --delete

  # Force overwrite without prompting
  %(prog)s --file en/test.mdx --force

  # Read API key from .env (no --api-key needed)
  %(prog)s --file en/test.mdx
        """
    )

    # Input options
    parser.add_argument(
        '--file', '-f',
        action='append',
        dest='files',
        help='Specific file to translate (can be used multiple times)'
    )
    parser.add_argument(
        '--dir', '-d',
        dest='directory',
        help='Directory to translate all files from'
    )

    # Configuration options
    parser.add_argument(
        '--api-key',
        help='Dify API key (or set in .env file)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually translating'
    )
    parser.add_argument(
        '--no-docs-sync',
        action='store_true',
        help='Skip docs.json structure synchronization'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete translated files and remove from docs.json (instead of translating)'
    )
    parser.add_argument(
        '--force', '-y',
        action='store_true',
        help='Overwrite existing files without prompting'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.files and not args.directory:
        parser.error("Must specify either --file or --dir")

    # Get API key
    api_key = args.api_key
    if not api_key:
        api_key = load_api_key_from_env()

    if not api_key and not args.dry_run:
        parser.error("API key required (use --api-key or set in .env file)")

    # Run sync
    results = await sync_by_paths(
        api_key=api_key or "dummy",  # Use dummy for dry run
        files=args.files,
        directory=args.directory,
        dry_run=args.dry_run,
        sync_docs_json=not args.no_docs_sync,
        delete_mode=args.delete,
        force=args.force
    )

    # Print results
    print("\n=== RESULTS ===")
    if results["translated"]:
        print(f"\n✓ Translated {len(results['translated'])} file(s):")
        for f in results["translated"]:
            print(f"  • {f}")

    if results["skipped"]:
        print(f"\n⚠ Skipped {len(results['skipped'])} file(s):")
        for f in results["skipped"]:
            print(f"  • {f}")

    if results["docs_json_synced"]:
        print("\n✓ Docs.json structure synced")

    if results["errors"]:
        print(f"\n✗ Errors ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✓ Success!")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
