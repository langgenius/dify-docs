#!/usr/bin/env python3
"""
Documentation Auto-Sync System
Synchronizes English documentation structure and content to Chinese and Japanese versions.
With enhanced security for handling external PRs.
"""

import json
import os
import sys
import asyncio
import shutil
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
import subprocess
import tempfile

# Import the existing translation function
from main import translate_text, load_md_mdx

# Import format-preserving JSON serialization
from json_formatter import save_json_with_preserved_format

# Import OpenAPI translation pipeline
from openapi import translate_openapi_file, translate_openapi_file_async

# Import security validator
try:
    from security_validator import SecurityValidator, create_validator
except ImportError:
    # Fallback if security module not available
    SecurityValidator = None
    create_validator = None

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent.parent
DOCS_JSON_PATH = BASE_DIR / "docs.json"

class DocsSynchronizer:
    def __init__(self, dify_api_key: str, enable_security: bool = False):
        self.dify_api_key = dify_api_key
        self.base_dir = BASE_DIR
        self.docs_json_path = DOCS_JSON_PATH
        self.enable_security = enable_security
        
        # Initialize security validator if enabled
        self.validator = None
        if enable_security and create_validator:
            self.validator = create_validator(self.base_dir)
        self.config = self.load_config()
    
    def validate_file_path(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate file path for security if security is enabled"""
        if not self.enable_security or not self.validator:
            return True, None
        
        return self.validator.validate_file_path(file_path)
    
    def validate_sync_plan(self, sync_plan: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate synchronization plan for security if security is enabled"""
        if not self.enable_security or not self.validator:
            return True, None
        
        return self.validator.validate_sync_plan(sync_plan)
    
    def sanitize_path(self, file_path: str) -> Optional[str]:
        """Sanitize file path if security is enabled"""
        if not self.enable_security or not self.validator:
            return file_path
        
        return self.validator.sanitize_path(file_path)
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration file with language mappings"""
        config_path = SCRIPT_DIR / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Validate required fields
            required = ["source_language", "target_languages", "languages"]
            for field in required:
                if field not in config:
                    raise ValueError(f"Missing required field in config.json: {field}")

            # Validate all referenced languages exist
            all_langs = [config["source_language"]] + config["target_languages"]
            for lang in all_langs:
                if lang not in config["languages"]:
                    raise ValueError(f"Language '{lang}' referenced but not defined in languages")

            # Validate target languages have translation_notice
            for lang in config["target_languages"]:
                if "translation_notice" not in config["languages"][lang]:
                    raise ValueError(f"Target language '{lang}' missing translation_notice")

            return config

        raise FileNotFoundError(f"Config file not found: {config_path}")

    @property
    def source_language(self) -> str:
        """Get source language code from config"""
        return self.config["source_language"]

    @property
    def target_languages(self) -> List[str]:
        """Get list of target language codes from config"""
        return self.config["target_languages"]

    def get_language_info(self, lang_code: str) -> Dict[str, Any]:
        """Get full language information for a language code"""
        return self.config["languages"].get(lang_code, {})

    def get_language_name(self, lang_code: str) -> str:
        """Get human-readable language name (e.g., 'English', 'Chinese')"""
        return self.get_language_info(lang_code).get("name", "")

    def get_language_directory(self, lang_code: str) -> str:
        """Get directory path for a language (e.g., 'en', 'cn')"""
        return self.get_language_info(lang_code).get("directory", lang_code)

    def get_translation_notice(self, lang_code: str) -> str:
        """Get AI translation notice template for a target language"""
        return self.get_language_info(lang_code).get("translation_notice", "")

    def get_changed_files(self, since_commit: str = "HEAD~1") -> Dict[str, List[str]]:
        """Get changed files using git diff"""
        try:
            # Get file changes
            result = subprocess.run([
                "git", "diff", "--name-status", since_commit, "HEAD"
            ], capture_output=True, text=True, cwd=self.base_dir)

            changes = {
                "added": [],
                "modified": [],
                "deleted": [],
                "renamed": []
            }

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                parts = line.split('\t')
                status = parts[0]

                if status == 'A':
                    changes["added"].append(parts[1])
                elif status == 'M':
                    changes["modified"].append(parts[1])
                elif status == 'D':
                    changes["deleted"].append(parts[1])
                elif status.startswith('R'):
                    changes["renamed"].append((parts[1], parts[2]))

            return changes
        except subprocess.CalledProcessError as e:
            print(f"Error getting git changes: {e}")
            return {"added": [], "modified": [], "deleted": [], "renamed": []}

    def get_file_diff(self, file_path: str, since_commit: str = "HEAD~1") -> Optional[str]:
        """Get git diff for a specific file"""
        try:
            result = subprocess.run([
                "git", "diff", since_commit, "HEAD", "--", file_path
            ], capture_output=True, text=True, cwd=self.base_dir)

            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Warning: Could not get diff for {file_path}")
                return None
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff for {file_path}: {e}")
            return None
    
    def is_english_doc_file(self, file_path: str) -> bool:
        """Check if file is a source language documentation file that should be synced"""
        source_dir = self.get_language_directory(self.source_language)
        return (file_path.startswith(f"{source_dir}/") and
                (file_path.endswith('.md') or file_path.endswith('.mdx')) and
                not file_path.startswith(f"{source_dir}/api-reference/"))
    
    def convert_path_to_target_language(self, source_path: str, target_lang: str) -> str:
        """Convert source language path to target language path"""
        source_dir = self.get_language_directory(self.source_language)
        target_dir = self.get_language_directory(target_lang)
        if source_path.startswith(f"{source_dir}/"):
            return source_path.replace(f"{source_dir}/", f"{target_dir}/", 1)
        return source_path
    
    def get_relative_source_path_for_notice(self, target_path: str) -> str:
        """Get absolute path to source language version for AI notice (without file extension)"""
        source_dir = self.get_language_directory(self.source_language)

        # Find which target language directory this path is in
        for target_lang in self.target_languages:
            target_dir = self.get_language_directory(target_lang)
            if target_path.startswith(f"{target_dir}/"):
                # Replace target dir with source dir
                source_path = target_path.replace(f"{target_dir}/", f"{source_dir}/", 1)
                # Remove file extension (.md or .mdx)
                source_path = source_path.rsplit('.', 1)[0] if '.' in source_path else source_path
                # Return absolute path starting with /
                return f"/{source_path}"

        return ""
    
    def _build_notice_removal_pattern(self) -> str:
        """Build regex pattern to match any translation notice from config templates."""
        # Collect all translation notice templates from target languages
        notice_templates = []
        for lang in self.target_languages:
            template = self.get_translation_notice(lang)
            if template:
                # Escape regex special chars, but replace {source_path} with a wildcard
                # First, escape the template for regex
                escaped = re.escape(template.strip())
                # Replace escaped placeholder with pattern that matches any path
                escaped = escaped.replace(r'\{source_path\}', r'[^\]]+')
                notice_templates.append(escaped)

        # Build pattern that matches any of the templates, followed by optional whitespace/newlines
        if notice_templates:
            return '(?:' + '|'.join(notice_templates) + r')\s*\n*'
        return ''

    def insert_notice_under_title(self, content: str, notice: str) -> str:
        """Insert notice after frontmatter or first heading to keep it under the doc title."""
        if not notice.strip():
            return content

        if not content:
            return notice

        bom_prefix = ""
        if content.startswith("\ufeff"):
            bom_prefix = "\ufeff"
            content = content[len("\ufeff"):]

        # Remove any existing translation notice to prevent duplicates
        # Pattern dynamically built from config templates
        existing_notice_pattern = self._build_notice_removal_pattern()
        if existing_notice_pattern:
            content = re.sub(existing_notice_pattern, '', content, flags=re.DOTALL)

        notice_block = notice if notice.endswith("\n") else f"{notice}\n"

        frontmatter_match = re.match(r"^(---\s*\n.*?\n---\s*\n?)", content, flags=re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            remainder = content[frontmatter_match.end():].lstrip("\n")

            final = frontmatter
            if not final.endswith("\n"):
                final += "\n"
            final += notice_block
            if remainder:
                final += remainder
            return bom_prefix + final

        heading_match = re.search(r"(?m)^(#{1,6}\s+.+)$", content)
        if heading_match:
            line_start = heading_match.start()
            line_end = content.find("\n", line_start)
            if line_end == -1:
                line_end = len(content)
            else:
                line_end += 1

            heading_section = content[:line_end]
            remainder = content[line_end:].lstrip("\n")

            final = heading_section
            if not final.endswith("\n"):
                final += "\n"
            final += notice_block
            if remainder:
                final += remainder
            return bom_prefix + final

        return bom_prefix + notice_block + content.lstrip("\n")

    async def translate_file_with_notice(self, en_file_path: str, target_file_path: str, target_lang: str,
                                        the_doc_exist: Optional[str] = None, diff_original: Optional[str] = None) -> bool:
        """Translate a file and add AI notice at the top

        Args:
            en_file_path: English source file path
            target_file_path: Target translation file path
            target_lang: Target language code (cn, jp)
            the_doc_exist: Optional existing translation content (for modified files)
            diff_original: Optional git diff of original file (for modified files)
        """
        try:
            # Security validation
            if self.enable_security:
                # Validate source path
                valid, error = self.validate_file_path(en_file_path)
                if not valid:
                    print(f"Security error - invalid source path {en_file_path}: {error}")
                    return False

                # Validate target path
                valid, error = self.validate_file_path(target_file_path)
                if not valid:
                    print(f"Security error - invalid target path {target_file_path}: {error}")
                    return False

                # Sanitize paths
                en_file_path = self.sanitize_path(en_file_path) or en_file_path
                target_file_path = self.sanitize_path(target_file_path) or target_file_path

            print(f"Translating {en_file_path} to {target_file_path}")

            # Ensure target directory exists
            target_dir = Path(self.base_dir / target_file_path).parent
            target_dir.mkdir(parents=True, exist_ok=True)

            # Get language names for translation API
            source_lang_name = self.get_language_name(self.source_language)
            target_lang_name = self.get_language_name(target_lang)

            # Translate content
            translated_content = await translate_text(
                str(self.base_dir / en_file_path),
                self.dify_api_key,
                source_lang_name,
                target_lang_name,
                the_doc_exist=the_doc_exist,
                diff_original=diff_original
            )

            if not translated_content or not translated_content.strip():
                print(f"Warning: No translated content received for {en_file_path}")
                return False

            # Prepare AI notice
            source_relative_path = self.get_relative_source_path_for_notice(target_file_path)
            notice = self.get_translation_notice(target_lang).format(source_path=source_relative_path)

            # Combine notice and translated content
            final_content = self.insert_notice_under_title(translated_content, notice)

            # Write to target file
            with open(self.base_dir / target_file_path, 'w', encoding='utf-8') as f:
                f.write(final_content)

            print(f"✓ Successfully created {target_file_path}")
            return True

        except Exception as e:
            print(f"Error translating {en_file_path} to {target_file_path}: {e}")
            return False
    
    def sync_file_operations(self, changes: Dict[str, List[str]]) -> List[str]:
        """Sync file operations to target languages"""
        operations_log = []
        
        # Handle added files
        for file_path in changes["added"]:
            if self.is_english_doc_file(file_path):
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    # We'll translate these in the async part
                    operations_log.append(f"WILL_TRANSLATE: {file_path} -> {target_path}")

        # Handle deleted files
        for file_path in changes["deleted"]:
            if self.is_english_doc_file(file_path):
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    target_full_path = self.base_dir / target_path
                    if target_full_path.exists():
                        target_full_path.unlink()
                        operations_log.append(f"DELETED: {target_path}")
        
        # Handle renamed files
        for old_path, new_path in changes["renamed"]:
            if self.is_english_doc_file(old_path) or self.is_english_doc_file(new_path):
                for target_lang in self.target_languages:
                    old_target = self.convert_path_to_target_language(old_path, target_lang)
                    new_target = self.convert_path_to_target_language(new_path, target_lang)
                    
                    old_full_path = self.base_dir / old_target
                    new_full_path = self.base_dir / new_target
                    
                    if old_full_path.exists():
                        # Ensure target directory exists
                        new_full_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(old_full_path), str(new_full_path))
                        operations_log.append(f"RENAMED: {old_target} -> {new_target}")
        
        return operations_log
    
    async def translate_new_and_modified_files(self, changes: Dict[str, List[str]], since_commit: str = "HEAD~1") -> List[str]:
        """Translate new and modified files

        Args:
            changes: Dictionary with 'added', 'modified', 'deleted', 'renamed' file lists
            since_commit: Git commit to compare against for diffs
        """
        translation_log = []
        tasks = []

        # Handle added files (no existing translation)
        for file_path in changes["added"]:
            if self.is_english_doc_file(file_path):
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    # New files - no existing translation or diff needed
                    task = self.translate_file_with_notice(file_path, target_path, target_lang)
                    tasks.append((task, file_path, target_path, "added"))

        # Handle modified files (may have existing translation)
        for file_path in changes["modified"]:
            if self.is_english_doc_file(file_path):
                # Get diff for this file
                diff_original = self.get_file_diff(file_path, since_commit)

                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    target_full_path = self.base_dir / target_path

                    # Check if target translation exists
                    the_doc_exist = None
                    if target_full_path.exists():
                        try:
                            with open(target_full_path, 'r', encoding='utf-8') as f:
                                the_doc_exist = f.read()
                            print(f"Found existing translation for {target_path} ({len(the_doc_exist)} chars)")
                        except Exception as e:
                            print(f"Warning: Could not read existing translation {target_path}: {e}")
                            the_doc_exist = None

                    # Modified files - pass existing translation and diff if available
                    task = self.translate_file_with_notice(
                        file_path,
                        target_path,
                        target_lang,
                        the_doc_exist=the_doc_exist,
                        diff_original=diff_original
                    )
                    tasks.append((task, file_path, target_path, "modified"))

        # Handle renamed files that need translation
        for old_path, new_path in changes["renamed"]:
            if self.is_english_doc_file(new_path):
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(new_path, target_lang)
                    # Renamed files treated as new
                    task = self.translate_file_with_notice(new_path, target_path, target_lang)
                    tasks.append((task, new_path, target_path, "renamed"))

        # Execute translations with concurrency control
        semaphore = asyncio.Semaphore(2)  # Limit concurrent translations

        async def bounded_translate(task, en_path, target_path, change_type):
            async with semaphore:
                success = await task
                return success, en_path, target_path, change_type

        # Run translations
        if tasks:
            print(f"Starting {len(tasks)} translation tasks...")
            results = await asyncio.gather(*[
                bounded_translate(task, en_path, target_path, change_type)
                for task, en_path, target_path, change_type in tasks
            ], return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    translation_log.append(f"ERROR: {result}")
                else:
                    success, en_path, target_path, change_type = result
                    if success:
                        translation_log.append(f"TRANSLATED ({change_type}): {en_path} -> {target_path}")
                    else:
                        translation_log.append(f"FAILED ({change_type}): {en_path} -> {target_path}")

        return translation_log
    
    def load_docs_json(self) -> Dict[str, Any]:
        """Load docs.json file"""
        try:
            with open(self.docs_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading docs.json: {e}")
            return {}
    
    def save_docs_json(self, data: Dict[str, Any]) -> bool:
        """Save docs.json file while preserving original formatting"""
        try:
            # Use format-preserving serialization
            # Pass the same file as both target and reference since we're overwriting
            success = save_json_with_preserved_format(
                self.docs_json_path,
                data,
                reference_file=self.docs_json_path
            )
            if success:
                print("✓ Saved docs.json with preserved formatting")
            return success
        except Exception as e:
            print(f"Error saving docs.json: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def extract_english_structure_changes(self, changes: Dict[str, List[str]]) -> bool:
        """Check if docs.json was modified"""
        return "docs.json" in changes["modified"] or "docs.json" in changes["added"]
    
    def get_dropdown_translation(self, en_dropdown_name: str, target_lang: str) -> str:
        """
        Get translated dropdown name from config.json label_translations.
        Falls back to English name if not found.
        """
        label_translations = self.config.get("label_translations", {})
        if en_dropdown_name in label_translations:
            translation = label_translations[en_dropdown_name].get(target_lang)
            if translation:
                return translation
        # Fallback to English name
        return en_dropdown_name

    def get_basic_label_translation(self, en_label: str, target_lang: str) -> str:
        """Get basic translation for common labels"""
        basic_translations = {
            "cn": {
                "Getting Started": "快速开始",
                "Documentation": "文档",
                "Build": "构建",
                "Debug": "调试",
                "Publish": "发布",
                "Monitor": "监控",
                "Knowledge": "知识库",
                "Workspace": "工作区",
                "Tutorials": "教程",
                "FAQ": "常见问题",
                "Introduction": "介绍",
                "Quick Start": "快速开始",
                "Key Concepts": "核心概念"
            },
            "jp": {
                "Getting Started": "はじめに",
                "Documentation": "ドキュメント",
                "Build": "ビルド",
                "Debug": "デバッグ",
                "Publish": "公開",
                "Monitor": "モニタリング",
                "Knowledge": "ナレッジベース",
                "Workspace": "ワークスペース",
                "Tutorials": "チュートリアル",
                "FAQ": "よくある質問",
                "Introduction": "紹介",
                "Quick Start": "クイックスタート",
                "Key Concepts": "主要概念"
            }
        }

        return basic_translations.get(target_lang, {}).get(en_label, en_label)
    
    def find_file_in_dropdown_structure(self, file_path: str, dropdown: Dict) -> Optional[List[str]]:
        """
        Find a file path in a dropdown's pages structure or groups with openapi fields.
        Returns the path to the item as a list of keys/indices, or None if not found.
        Example: ["pages", 0, "pages", 2] means dropdown["pages"][0]["pages"][2] == file_path
        Example: ["groups", 1, "openapi"] means dropdown["groups"][1]["openapi"] == file_path

        Note: docs.json stores paths without file extensions, so we strip them for comparison.
        """
        # Strip file extension for comparison (docs.json doesn't include .md/.mdx extensions)
        file_path_no_ext = re.sub(r'\.(mdx?|md)$', '', file_path)

        def search_pages(pages: List, current_path: List) -> Optional[List[str]]:
            for i, item in enumerate(pages):
                if isinstance(item, str):
                    # Compare without extensions
                    item_no_ext = re.sub(r'\.(mdx?|md)$', '', item)
                    if item_no_ext == file_path_no_ext:
                        return current_path + [i]
                elif isinstance(item, dict) and "pages" in item:
                    result = search_pages(item["pages"], current_path + [i, "pages"])
                    if result:
                        return result
            return None

        # Search in pages array (markdown files)
        if "pages" in dropdown:
            result = search_pages(dropdown["pages"], ["pages"])
            if result:
                return result

        # Search in groups array (OpenAPI files)
        if "groups" in dropdown:
            groups = dropdown["groups"]
            for i, group in enumerate(groups):
                if isinstance(group, dict) and "openapi" in group:
                    # Compare OpenAPI file paths (no extension stripping needed for .json)
                    if group["openapi"] == file_path:
                        return ["groups", i, "openapi"]

        return None

    def find_dropdown_containing_file(self, file_path: str, lang_section: Dict) -> Optional[Tuple[str, List[str]]]:
        """
        Find which dropdown contains a specific file path.
        Returns (dropdown_name, path_to_file) or None if not found.
        """
        dropdowns = lang_section.get("dropdowns", [])
        for dropdown in dropdowns:
            dropdown_name = dropdown.get("dropdown", "")
            file_location = self.find_file_in_dropdown_structure(file_path, dropdown)
            if file_location:
                return (dropdown_name, file_location)
        return None

    def add_page_to_structure(self, pages: List, page_path: str, reference_structure: List = None) -> bool:
        """
        Add a page to a pages array, attempting to maintain position relative to reference structure.
        Returns True if added, False if already exists.

        Note: Strips file extensions before adding (docs.json doesn't include .md/.mdx extensions).
        """
        # Strip file extension (docs.json doesn't include extensions)
        page_path_no_ext = re.sub(r'\.(mdx?|md)$', '', page_path)

        # First pass: check if page already exists anywhere in the structure
        def page_exists(pages_to_check):
            for item in pages_to_check:
                if isinstance(item, str):
                    item_no_ext = re.sub(r'\.(mdx?|md)$', '', item)
                    if item_no_ext == page_path_no_ext:
                        return True
                elif isinstance(item, dict) and "pages" in item:
                    if page_exists(item["pages"]):
                        return True
            return False

        if page_exists(pages):
            return False

        # Page doesn't exist - add it to the top level (without extension)
        pages.append(page_path_no_ext)
        return True

    def _add_openapi_group(self, target_dropdown: Dict, openapi_path: str, file_location: List, en_dropdown: Dict) -> bool:
        """
        Add an OpenAPI group to target dropdown.
        file_location is like ["groups", 1, "openapi"]

        Args:
            target_dropdown: Target language dropdown structure
            openapi_path: Path to OpenAPI file (e.g., "cn/api-reference/openapi_test.json")
            file_location: Location path like ["groups", 1, "openapi"]
            en_dropdown: English dropdown structure for reference

        Returns:
            True if added, False if already exists
        """
        if len(file_location) < 3 or file_location[0] != "groups" or file_location[2] != "openapi":
            return False

        group_index = file_location[1]

        # Ensure groups array exists
        if "groups" not in target_dropdown:
            target_dropdown["groups"] = []

        # Check if this OpenAPI file already exists in target
        for group in target_dropdown.get("groups", []):
            if isinstance(group, dict) and group.get("openapi") == openapi_path:
                return False  # Already exists

        # Get the English group structure
        en_groups = en_dropdown.get("groups", [])
        if group_index >= len(en_groups):
            return False

        en_group = en_groups[group_index]

        # Create the target group with the same structure but translated path
        target_group = {
            "group": en_group.get("group", ""),  # Keep English group name for now (could translate later)
            "openapi": openapi_path
        }

        # Ensure we have enough slots in target groups
        while len(target_dropdown["groups"]) <= group_index:
            target_dropdown["groups"].append(None)

        # Insert at the same index position
        if target_dropdown["groups"][group_index] is None:
            target_dropdown["groups"][group_index] = target_group
        else:
            # Index already occupied, append instead
            target_dropdown["groups"].append(target_group)

        return True

    def add_page_at_location(self, target_dropdown: Dict, page_path: str, file_location: List, en_dropdown: Dict) -> bool:
        """
        Add a page to target dropdown at the same nested location as in English dropdown.
        Uses the file_location path to navigate to the correct nested group.

        Args:
            target_dropdown: Target language dropdown structure
            page_path: Path of the file to add (e.g., "cn/documentation/pages/..." or "cn/api-reference/openapi_test.json")
            file_location: Location path from find_file_in_dropdown_structure
                         (e.g., ["pages", 0, "pages", 0, "pages", 3] or ["groups", 1, "openapi"])
            en_dropdown: English dropdown structure for reference

        Returns:
            True if added, False if already exists
        """
        # Handle OpenAPI groups structure (e.g., ["groups", 1, "openapi"])
        if file_location and file_location[0] == "groups":
            return self._add_openapi_group(target_dropdown, page_path, file_location, en_dropdown)

        # Strip file extension (docs.json doesn't include extensions)
        page_path_no_ext = re.sub(r'\.(mdx?|md)$', '', page_path)

        # Check if page already exists anywhere in target
        def page_exists(pages_to_check):
            if not pages_to_check:
                return False
            for item in pages_to_check:
                if isinstance(item, str):
                    item_no_ext = re.sub(r'\.(mdx?|md)$', '', item)
                    if item_no_ext == page_path_no_ext:
                        return True
                elif isinstance(item, dict) and "pages" in item:
                    if page_exists(item["pages"]):
                        return True
            return False

        if "pages" in target_dropdown and page_exists(target_dropdown["pages"]):
            return False

        # Navigate to the correct nested location
        # file_location is like ["pages", 0, "pages", 0, "pages", 3]
        # We navigate through the path, creating groups as needed

        current_target = target_dropdown
        current_en = en_dropdown

        # Process path in pairs: "pages" key, then index
        i = 0
        while i < len(file_location) - 1:  # Stop before final element (insertion point)
            key = file_location[i]

            if key == "pages":
                # Ensure pages array exists
                if "pages" not in current_target:
                    current_target["pages"] = []

                # Check if next element is an index
                if i + 1 < len(file_location):
                    next_elem = file_location[i + 1]

                    if isinstance(next_elem, int):
                        # Navigate to group at this index
                        idx = next_elem

                        # Get corresponding English item
                        en_pages = current_en.get("pages", [])
                        if idx < len(en_pages):
                            en_item = en_pages[idx]

                            # If English item is a group, ensure target has matching group
                            if isinstance(en_item, dict) and "pages" in en_item:
                                # Ensure target has items up to this index (only for groups we'll navigate through)
                                while len(current_target["pages"]) <= idx:
                                    current_target["pages"].append(None)
                                target_item = current_target["pages"][idx]

                                if not isinstance(target_item, dict) or "pages" not in target_item:
                                    # Create group structure (preserve existing group name if present)
                                    if isinstance(target_item, dict) and "group" in target_item:
                                        existing_group = target_item["group"]
                                    else:
                                        existing_group = en_item.get("group", "")

                                    current_target["pages"][idx] = {
                                        "group": existing_group,
                                        "pages": target_item.get("pages", []) if isinstance(target_item, dict) else []
                                    }
                                    if "icon" in en_item:
                                        current_target["pages"][idx]["icon"] = en_item["icon"]

                                # Navigate into this group
                                current_target = current_target["pages"][idx]
                                current_en = en_item
                                i += 2  # Skip "pages" and index
                                continue

            i += 1

        # Add the page at the final location
        if "pages" not in current_target:
            current_target["pages"] = []

        # Get the insertion index from file_location (last element)
        # file_location is like ["pages", 1] or ["pages", 0, "pages", 3]
        # The last element is the index where the file should be inserted
        if file_location and isinstance(file_location[-1], int):
            insert_index = file_location[-1]
            # Insert at the same index position as in English structure
            # If index is beyond current length, append to end
            if insert_index <= len(current_target["pages"]):
                current_target["pages"].insert(insert_index, page_path_no_ext)
            else:
                current_target["pages"].append(page_path_no_ext)
        else:
            # Fallback: append if we can't determine index
            current_target["pages"].append(page_path_no_ext)

        return True

    def remove_page_from_structure(self, pages: List, page_path: str) -> bool:
        """
        Remove a page from a pages array recursively.
        Returns True if removed, False if not found.

        Note: Strips file extensions for comparison (docs.json doesn't include .md/.mdx extensions).
        """
        # Strip file extension for comparison
        page_path_no_ext = re.sub(r'\.(mdx?|md)$', '', page_path)

        for i, item in enumerate(pages):
            if isinstance(item, str):
                item_no_ext = re.sub(r'\.(mdx?|md)$', '', item)
                if item_no_ext == page_path_no_ext:
                    pages.pop(i)
                    return True
            elif isinstance(item, dict) and "pages" in item:
                if self.remove_page_from_structure(item["pages"], page_path):
                    # Clean up empty groups
                    if not item["pages"]:
                        pages.pop(i)
                    return True
        return False

    def extract_file_locations(self, section_data) -> Dict[str, Dict]:
        """
        Extract all file paths and their locations in the navigation structure.
        Returns dict mapping file path to location metadata including group indices for language-independent navigation.
        """
        locations = {}

        if not section_data or "dropdowns" not in section_data:
            return locations

        def traverse_structure(pages, dropdown_name, dropdown_idx, group_path, group_indices, path_prefix=""):
            """Recursively traverse pages structure to extract file locations."""
            for idx, item in enumerate(pages):
                if isinstance(item, str):
                    # Direct page reference
                    locations[item] = {
                        "dropdown": dropdown_name,
                        "dropdown_idx": dropdown_idx,
                        "group_path": group_path,  # Full group path for logging/debugging
                        "group_indices": group_indices.copy(),  # Index-based path for language-independent navigation
                        "page_index": idx,  # Position within parent pages array
                        "path": f"{path_prefix}[{idx}]",
                        "type": "page"
                    }
                elif isinstance(item, dict):
                    if "pages" in item:
                        # Nested group
                        group_name = item.get("group", item.get("label", ""))
                        new_group_path = f"{group_path} > {group_name}" if group_path else group_name
                        new_group_indices = group_indices + [idx]  # Track the index of this group
                        traverse_structure(
                            item["pages"],
                            dropdown_name,
                            dropdown_idx,
                            new_group_path,
                            new_group_indices,
                            f"{path_prefix}[{idx}].pages"
                        )

        for dropdown_idx, dropdown in enumerate(section_data.get("dropdowns", [])):
            dropdown_name = dropdown.get("dropdown", "")

            # Check pages array
            if "pages" in dropdown:
                traverse_structure(dropdown["pages"], dropdown_name, dropdown_idx, dropdown_name, [], "pages")

        return locations

    def reconcile_docs_json_structural_changes(
        self,
        base_sha: str,
        head_sha: str,
        skip_rename_detection: bool = False
    ) -> List[str]:
        """
        Detect and apply specific structural changes (moves) from English section.
        Compares base vs head English sections and applies only those changes to cn/jp.

        Args:
            base_sha: Base commit SHA
            head_sha: Head commit SHA
            skip_rename_detection: If True, skip the broken rename detection logic
                                   (renames should be handled by git-based detection instead)
        """
        reconcile_log = []

        try:
            # Get docs.json from both commits
            import subprocess

            base_docs_result = subprocess.run(
                ["git", "show", f"{base_sha}:docs.json"],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.base_dir
            )
            base_docs = json.loads(base_docs_result.stdout)

            head_docs_result = subprocess.run(
                ["git", "show", f"{head_sha}:docs.json"],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.base_dir
            )
            head_docs = json.loads(head_docs_result.stdout)

            # Extract English sections
            def get_english_section(docs_data):
                nav = docs_data.get("navigation", {})
                if "versions" in nav and nav["versions"]:
                    languages = nav["versions"][0].get("languages", [])
                else:
                    languages = nav.get("languages", [])

                for lang in languages:
                    if lang.get("language") == self.source_language:
                        return lang
                return None

            base_en = get_english_section(base_docs)
            head_en = get_english_section(head_docs)

            if not base_en or not head_en:
                reconcile_log.append("ERROR: Could not find English sections for comparison")
                return reconcile_log

            # Extract file locations from both versions
            base_locations = self.extract_file_locations(base_en)
            head_locations = self.extract_file_locations(head_en)

            base_files = set(base_locations.keys())
            head_files = set(head_locations.keys())

            # Detect operations
            added = head_files - base_files
            deleted = base_files - head_files
            possibly_moved = base_files & head_files

            # Check for actual moves (same file, different location)
            moved_files = []
            for file_path in possibly_moved:
                base_loc = base_locations[file_path]
                head_loc = head_locations[file_path]

                # Check if location changed (use group_path for accurate comparison)
                if base_loc["group_path"] != head_loc["group_path"]:
                    moved_files.append({
                        "file": file_path,
                        "from": base_loc,
                        "to": head_loc
                    })

            # Detect renames: files that were deleted and added might be renames
            # NOTE: This heuristic-based rename detection is BROKEN and causes false positives.
            # It can incorrectly treat "delete file A + add unrelated file B" as a rename.
            # Use git-based rename detection (--find-renames=100%) instead.
            renamed_files = []

            if not skip_rename_detection:
                # DEPRECATED: This logic is kept for backward compatibility but should not be used
                reconcile_log.append("WARNING: Using deprecated heuristic-based rename detection")
                deleted_normalized = {}
                added_normalized = {}

                source_dir = self.get_language_directory(self.source_language)
                source_prefix = f"^{source_dir}/"

                for deleted_file in deleted:
                    # Normalize: {source_dir}/foo/bar.md -> foo/bar.md
                    normalized = re.sub(source_prefix, '', deleted_file)
                    deleted_normalized[normalized] = deleted_file

                for added_file in added:
                    # Normalize: {source_dir}/foo/baz.md -> foo/baz.md
                    normalized = re.sub(source_prefix, '', added_file)
                    added_normalized[normalized] = added_file

                # Check for renames: different paths but same location
                # This is a simple heuristic - if added and deleted have different normalized paths
                # but appear in similar locations, treat as rename
                for del_norm, del_file in deleted_normalized.items():
                    for add_norm, add_file in added_normalized.items():
                        if del_norm != add_norm:
                            # Different paths - potential rename
                            del_loc = base_locations[del_file]
                            add_loc = head_locations[add_file]

                            # If they're in the same location group, it's likely a rename
                            if del_loc["group_path"] == add_loc["group_path"]:
                                renamed_files.append({
                                    "from_file": del_file,
                                    "to_file": add_file,
                                    "location": add_loc
                                })
                                # Remove from added/deleted to avoid processing twice
                                added.discard(add_file)
                                deleted.discard(del_file)
                                break

            if not moved_files and not added and not deleted and not renamed_files:
                reconcile_log.append("INFO: No structural changes detected")
                return reconcile_log

            reconcile_log.append(f"INFO: Detected {len(moved_files)} moves, {len(renamed_files)} renames, {len(added)} adds, {len(deleted)} deletes")

            # Load current docs.json
            docs_data = self.load_docs_json()
            if not docs_data:
                reconcile_log.append("ERROR: Could not load docs.json")
                return reconcile_log

            changes_made = False

            # Apply moves to cn/jp sections
            for move_op in moved_files:
                en_file = move_op["file"]
                from_loc = move_op["from"]
                to_loc = move_op["to"]

                reconcile_log.append(f"INFO: Moving {en_file} from '{from_loc['group_path']}' to '{to_loc['group_path']}'")

                # Apply to each target language
                for target_lang in self.target_languages:
                    target_file = self.convert_path_to_target_language(en_file, target_lang)

                    # Remove from old location
                    removed = self.remove_file_from_navigation(docs_data, target_file, target_lang)

                    if removed:
                        # Add to new location
                        added = self.add_file_to_navigation(docs_data, target_file, target_lang, to_loc)

                        if added:
                            reconcile_log.append(f"SUCCESS: Moved {target_file} to new location")
                            changes_made = True
                        else:
                            reconcile_log.append(f"WARNING: Could not add {target_file} to new location")
                    else:
                        reconcile_log.append(f"WARNING: Could not remove {target_file} from old location")

            # Apply renames to cn/jp sections
            for rename_op in renamed_files:
                from_file = rename_op["from_file"]
                to_file = rename_op["to_file"]
                location = rename_op["location"]

                reconcile_log.append(f"INFO: Renaming {from_file} to {to_file}")

                # Apply to each target language
                for target_lang in self.target_languages:
                    old_target_file = self.convert_path_to_target_language(from_file, target_lang)
                    new_target_file = self.convert_path_to_target_language(to_file, target_lang)

                    # Find the actual file with extension (docs.json entries don't have extensions)
                    old_file_path = None
                    file_extension = None

                    # Try common extensions
                    for ext in ['.md', '.mdx', '']:
                        test_path = self.base_dir / f"{old_target_file}{ext}"
                        if test_path.exists():
                            old_file_path = test_path
                            file_extension = ext
                            break

                    if old_file_path and old_file_path.exists():
                        # Create new file path with same extension
                        new_file_path = self.base_dir / f"{new_target_file}{file_extension}"

                        # Create parent directories if needed
                        new_file_path.parent.mkdir(parents=True, exist_ok=True)

                        # Rename the file
                        old_file_path.rename(new_file_path)
                        reconcile_log.append(f"SUCCESS: Renamed file {old_target_file}{file_extension} to {new_target_file}{file_extension}")

                        # Update docs.json: remove old entry, add new entry
                        removed = self.remove_file_from_navigation(docs_data, old_target_file, target_lang)
                        if removed:
                            added = self.add_file_to_navigation(docs_data, new_target_file, target_lang, location)
                            if added:
                                reconcile_log.append(f"SUCCESS: Updated docs.json for {target_lang} rename")
                                changes_made = True
                            else:
                                reconcile_log.append(f"WARNING: Could not add {new_target_file} to docs.json")
                        else:
                            reconcile_log.append(f"WARNING: Could not remove {old_target_file} from docs.json")
                    else:
                        reconcile_log.append(f"WARNING: File {old_target_file} not found for rename (tried .md, .mdx, and no extension)")

            # Apply deletes to cn/jp sections
            for en_file in deleted:
                reconcile_log.append(f"INFO: Deleting {en_file}")

                # Apply to each target language
                for target_lang in self.target_languages:
                    target_file = self.convert_path_to_target_language(en_file, target_lang)

                    # Remove from docs.json navigation
                    removed = self.remove_file_from_navigation(docs_data, target_file, target_lang)

                    if removed:
                        reconcile_log.append(f"SUCCESS: Removed {target_file} from docs.json")
                        changes_made = True

                        # Delete physical file
                        for ext in ['.md', '.mdx', '']:
                            file_path = self.base_dir / f"{target_file}{ext}"
                            if file_path.exists():
                                file_path.unlink()
                                reconcile_log.append(f"SUCCESS: Deleted physical file {target_file}{ext}")
                                break
                    else:
                        reconcile_log.append(f"WARNING: Could not remove {target_file} from docs.json")

            # Save updated docs.json
            if changes_made:
                self.save_docs_json(docs_data)
                reconcile_log.append("SUCCESS: Applied structural changes to docs.json")

            return reconcile_log

        except Exception as e:
            reconcile_log.append(f"ERROR: Failed to reconcile structural changes: {e}")
            return reconcile_log

    def remove_file_from_navigation(self, docs_data: Dict, file_path: str, target_lang: str) -> bool:
        """Remove a file from target language navigation structure."""
        nav = docs_data.get("navigation", {})

        # Find target language section
        if "versions" in nav and nav["versions"]:
            languages = nav["versions"][0].get("languages", [])
        else:
            languages = nav.get("languages", [])

        target_section = None
        for lang in languages:
            if lang.get("language") == target_lang:
                target_section = lang
                break

        if not target_section:
            return False

        # Remove from dropdowns
        for dropdown in target_section.get("dropdowns", []):
            if "pages" in dropdown:
                if self.remove_page_from_structure(dropdown["pages"], file_path):
                    return True

        return False

    def add_file_to_navigation(self, docs_data: Dict, file_path: str, target_lang: str, location_info: Dict) -> bool:
        """Add a file to target language navigation at specified location using index-based navigation."""
        nav = docs_data.get("navigation", {})

        # Find target language section
        if "versions" in nav and nav["versions"]:
            languages = nav["versions"][0].get("languages", [])
        else:
            languages = nav.get("languages", [])

        target_section = None
        for lang in languages:
            if lang.get("language") == target_lang:
                target_section = lang
                break

        if not target_section:
            return False

        # Find target dropdown by index
        dropdown_idx = location_info["dropdown_idx"]
        dropdowns = target_section.get("dropdowns", [])

        if dropdown_idx >= len(dropdowns):
            return False

        target_dropdown = dropdowns[dropdown_idx]

        # Start from dropdown's pages
        if "pages" not in target_dropdown:
            target_dropdown["pages"] = []

        current_pages = target_dropdown["pages"]

        # Navigate through nested groups using indices (language-independent)
        group_indices = location_info.get("group_indices", [])

        for group_idx in group_indices:
            # Navigate to the group at this index
            if group_idx >= len(current_pages):
                # Index out of bounds - structure mismatch between languages
                return False

            item = current_pages[group_idx]

            if isinstance(item, dict) and "pages" in item:
                # Navigate into this group
                if "pages" not in item:
                    item["pages"] = []
                current_pages = item["pages"]
            else:
                # Expected a group but found something else - structure mismatch
                return False

        # Add file to the target location if not already present
        if file_path not in str(current_pages):
            # Insert at the same position as in the source language
            page_index = location_info.get("page_index", len(current_pages))

            # Ensure index is within bounds (append if beyond end)
            if page_index > len(current_pages):
                page_index = len(current_pages)

            current_pages.insert(page_index, file_path)
            return True

        return False

    def _handle_rename(self, old_en_path: str, new_en_path: str) -> Tuple[List[str], List[str]]:
        """
        Handle file rename operation for target languages.

        If the old translation file exists, rename it and update docs.json.
        If it doesn't exist, return the new path for fresh translation.

        Args:
            old_en_path: Old English file path (e.g., "en/docs/old.mdx")
            new_en_path: New English file path (e.g., "en/docs/new.mdx")

        Returns:
            Tuple of (log_messages, files_needing_translation)
            files_needing_translation contains new paths that need fresh translation
        """
        log = []
        files_needing_translation = []

        log.append(f"INFO: Processing rename {old_en_path} -> {new_en_path}")

        # Load docs.json to get location info and update entries
        docs_data = self.load_docs_json()
        if not docs_data:
            log.append("ERROR: Could not load docs.json for rename operation")
            return log, files_needing_translation

        # Get English section to find the location of the new file
        nav = docs_data.get("navigation", {})
        if "versions" in nav and nav["versions"]:
            languages = nav["versions"][0].get("languages", [])
        else:
            languages = nav.get("languages", [])

        en_section = None
        for lang in languages:
            if lang.get("language") == self.source_language:
                en_section = lang
                break

        if not en_section:
            log.append("ERROR: Could not find English section in docs.json")
            return log, files_needing_translation

        # Extract file location from English section (use new path since English already renamed)
        file_locations = self.extract_file_locations(en_section)
        location = file_locations.get(new_en_path)

        if not location:
            log.append(f"WARNING: Could not find location for {new_en_path} in English section")
            # Continue without updating docs.json entries
            location = None

        docs_changed = False

        for target_lang in self.target_languages:
            old_target = self.convert_path_to_target_language(old_en_path, target_lang)
            new_target = self.convert_path_to_target_language(new_en_path, target_lang)

            # Find old file with extension (.md, .mdx, or no extension)
            old_file_path = None
            file_extension = None
            for ext in ['.md', '.mdx', '']:
                test_path = self.base_dir / f"{old_target}{ext}"
                if test_path.exists():
                    old_file_path = test_path
                    file_extension = ext
                    break

            if old_file_path and old_file_path.exists():
                # Old file exists - rename it
                new_file_path = self.base_dir / f"{new_target}{file_extension}"

                # Create parent directories if needed
                new_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Rename the physical file
                old_file_path.rename(new_file_path)
                log.append(f"SUCCESS: Renamed {old_target}{file_extension} -> {new_target}{file_extension}")

                # Update docs.json entry if we have location info
                if location:
                    # Remove old entry
                    removed = self.remove_file_from_navigation(docs_data, old_target, target_lang)
                    if removed:
                        # Add new entry at same location
                        added = self.add_file_to_navigation(docs_data, new_target, target_lang, location)
                        if added:
                            log.append(f"SUCCESS: Updated docs.json entry {old_target} -> {new_target} for {target_lang}")
                            docs_changed = True
                        else:
                            log.append(f"WARNING: Could not add {new_target} to docs.json for {target_lang}")
                    else:
                        log.append(f"WARNING: Could not remove {old_target} from docs.json for {target_lang}")
            else:
                # Old file not found - need fresh translation
                log.append(f"INFO: Old file {old_target} not found, will generate new translation")
                files_needing_translation.append(new_en_path)

        # Save docs.json if we made changes
        if docs_changed:
            self.save_docs_json(docs_data)
            log.append("SUCCESS: Saved updated docs.json with rename entries")

        return log, files_needing_translation

    def sync_docs_json_incremental(
        self,
        added_files: List[str] = None,
        deleted_files: List[str] = None,
        renamed_files: List[Tuple[str, str]] = None,
        base_sha: str = None,
        head_sha: str = None
    ) -> List[str]:
        """
        Incrementally sync docs.json structure - only processes changed files.
        Preserves existing dropdown names and only updates affected pages.
        """
        sync_log = []
        added_files = added_files or []
        deleted_files = deleted_files or []
        renamed_files = renamed_files or []

        # Process renames first (before adds/deletes)
        # Renamed files that couldn't be renamed will be added to added_files for fresh translation
        for old_path, new_path in renamed_files:
            if old_path.startswith(f"{self.get_language_directory(self.source_language)}/"):
                rename_log, files_to_translate = self._handle_rename(old_path, new_path)
                sync_log.extend(rename_log)

                # If any translations need to be generated (old file didn't exist), add to added_files
                if new_path in files_to_translate:
                    if new_path not in added_files:
                        added_files.append(new_path)
                        sync_log.append(f"INFO: Added {new_path} to translation queue (old translation not found)")

        # Check for structural changes (moves only, not renames since we handled those)
        if base_sha and head_sha:
            sync_log.append("INFO: Checking for structural changes (moves)...")
            reconcile_log = self.reconcile_docs_json_structural_changes(
                base_sha, head_sha,
                skip_rename_detection=True  # Skip broken rename detection - we handle renames properly above
            )
            sync_log.extend(reconcile_log)

        # If no file adds/deletes after rename processing, we're done
        if not added_files and not deleted_files:
            sync_log.append("INFO: No file adds/deletes to sync")
            return sync_log

        try:
            docs_data = self.load_docs_json()
            if not docs_data or "navigation" not in docs_data:
                sync_log.append("ERROR: Invalid docs.json structure")
                return sync_log

            navigation = docs_data["navigation"]

            # Handle both direct languages and versions structure
            languages_array = None
            if "languages" in navigation and isinstance(navigation["languages"], list):
                languages_array = navigation["languages"]
            elif "versions" in navigation and len(navigation["versions"]) > 0:
                if "languages" in navigation["versions"][0]:
                    languages_array = navigation["versions"][0]["languages"]

            if not languages_array:
                sync_log.append("ERROR: No languages found in navigation")
                return sync_log

            # Find language sections
            en_section = None
            target_sections = {}

            for lang_data in languages_array:
                if lang_data.get("language") == self.source_language:
                    en_section = lang_data
                elif lang_data.get("language") in self.target_languages:
                    target_sections[lang_data.get("language")] = lang_data

            if not en_section:
                sync_log.append("ERROR: English section not found")
                return sync_log

            sync_log.append(f"INFO: Processing {len(added_files)} added, {len(deleted_files)} deleted files")

            # Process added files
            for en_file in added_files:
                if not en_file.startswith("en/"):
                    continue

                # Find which dropdown contains this file in English section
                result = self.find_dropdown_containing_file(en_file, en_section)
                if not result:
                    sync_log.append(f"WARNING: Could not find {en_file} in English navigation")
                    continue

                en_dropdown_name, file_location = result
                sync_log.append(f"INFO: Found {en_file} in '{en_dropdown_name}' dropdown at location {file_location}")

                # Get the English dropdown for reference
                en_dropdown = None
                en_dropdown_index = -1
                for i, dropdown in enumerate(en_section.get("dropdowns", [])):
                    if dropdown.get("dropdown") == en_dropdown_name:
                        en_dropdown = dropdown
                        en_dropdown_index = i
                        break

                if not en_dropdown:
                    sync_log.append(f"WARNING: Could not find English dropdown '{en_dropdown_name}'")
                    continue

                # Add to each target language
                for target_lang, target_section in target_sections.items():
                    target_file = self.convert_path_to_target_language(en_file, target_lang)

                    # Find or create corresponding dropdown
                    target_dropdown = None
                    target_dropdown_name = None

                    # Strategy: Try to find the dropdown by matching index position first,
                    # then by translated name. This preserves correct dropdown associations.
                    target_dropdowns = target_section.get("dropdowns", [])

                    # Try to use same index in target language (assuming dropdowns are in same order)
                    if en_dropdown_index >= 0 and en_dropdown_index < len(target_dropdowns):
                        target_dropdown = target_dropdowns[en_dropdown_index]
                        target_dropdown_name = target_dropdown.get("dropdown", "")

                    # If index-based match failed, try matching by translated name
                    if not target_dropdown:
                        translated_name = self.get_dropdown_translation(en_dropdown_name, target_lang)
                        for dropdown in target_dropdowns:
                            if dropdown.get("dropdown") == translated_name:
                                target_dropdown = dropdown
                                target_dropdown_name = translated_name
                                break

                    # If still not found, create new dropdown
                    if not target_dropdown:
                        translated_name = self.get_dropdown_translation(en_dropdown_name, target_lang)

                        target_dropdown = {
                            "dropdown": translated_name,
                            "icon": en_dropdown.get("icon", "book-open"),
                            "pages": []
                        }
                        target_section.setdefault("dropdowns", [])
                        target_section["dropdowns"].append(target_dropdown)
                        target_dropdown_name = translated_name
                        sync_log.append(f"INFO: Created new dropdown '{translated_name}' for {target_lang}")

                    # Add the page to the dropdown at the correct nested location
                    if "pages" not in target_dropdown:
                        target_dropdown["pages"] = []

                    # Use the new method that preserves group structure
                    added = self.add_page_at_location(target_dropdown, target_file, file_location, en_dropdown)
                    if added:
                        sync_log.append(f"INFO: Added {target_file} to '{target_dropdown_name}' at nested location ({target_lang})")
                    else:
                        sync_log.append(f"INFO: {target_file} already exists in '{target_dropdown_name}' ({target_lang})")

            # Process deleted files
            for en_file in deleted_files:
                if not en_file.startswith("en/"):
                    continue

                sync_log.append(f"INFO: Processing deletion of {en_file}")

                # Remove from each target language (cn, jp)
                for target_lang, target_section in target_sections.items():
                    target_file = self.convert_path_to_target_language(en_file, target_lang)
                    sync_log.append(f"INFO: Attempting to remove {target_file} from {target_lang} section")

                    # Find and remove from all dropdowns
                    removed = False
                    dropdowns = target_section.get("dropdowns", [])
                    sync_log.append(f"INFO: Searching through {len(dropdowns)} dropdowns in {target_lang} section")

                    for idx, dropdown in enumerate(dropdowns):
                        dropdown_name = dropdown.get("dropdown", "")
                        sync_log.append(f"INFO: Checking dropdown {idx + 1}/{len(dropdowns)}: '{dropdown_name}'")

                        # Check pages array for markdown files
                        if "pages" in dropdown:
                            if self.remove_page_from_structure(dropdown["pages"], target_file):
                                sync_log.append(f"SUCCESS: Removed {target_file} from '{dropdown_name}' ({target_lang})")
                                removed = True
                                break

                        # Check groups array for OpenAPI files
                        if "groups" in dropdown:
                            groups = dropdown["groups"]
                            for i, group in enumerate(groups):
                                if isinstance(group, dict) and group.get("openapi") == target_file:
                                    groups.pop(i)
                                    sync_log.append(f"SUCCESS: Removed OpenAPI {target_file} from '{dropdown_name}' ({target_lang})")
                                    removed = True
                                    break
                            if removed:
                                break

                        if "pages" not in dropdown and "groups" not in dropdown:
                            sync_log.append(f"INFO: Dropdown '{dropdown_name}' has no pages or groups array")

                    if not removed:
                        sync_log.append(f"WARNING: Could not find {target_file} in {target_lang} navigation - file may not exist in navigation")

            # Save the updated docs.json
            if self.save_docs_json(docs_data):
                sync_log.append("INFO: Updated docs.json with incremental changes")
            else:
                sync_log.append("ERROR: Failed to save updated docs.json")

        except Exception as e:
            sync_log.append(f"ERROR: Exception in incremental sync: {e}")
            import traceback
            sync_log.append(f"TRACE: {traceback.format_exc()}")

        return sync_log

    def sync_docs_json_structure(self) -> List[str]:
        """
        DEPRECATED: Full sync of docs.json structure across languages.
        This method syncs ALL dropdowns and is only kept for backward compatibility.
        Use sync_docs_json_incremental() for new code.
        """
        sync_log = []
        sync_log.append("WARNING: Using deprecated full sync method")

        try:
            docs_data = self.load_docs_json()
            if not docs_data or "navigation" not in docs_data:
                sync_log.append("ERROR: Invalid docs.json structure")
                return sync_log

            navigation = docs_data["navigation"]

            # Handle both direct languages and versions structure
            languages_array = None
            if "languages" in navigation and isinstance(navigation["languages"], list):
                languages_array = navigation["languages"]
            elif "versions" in navigation and len(navigation["versions"]) > 0:
                if "languages" in navigation["versions"][0]:
                    languages_array = navigation["versions"][0]["languages"]

            if not languages_array:
                sync_log.append("ERROR: No languages found in navigation")
                return sync_log

            # Find language sections
            en_section = None
            target_sections = {}

            for lang_data in languages_array:
                if lang_data.get("language") == self.source_language:
                    en_section = lang_data
                elif lang_data.get("language") in self.target_languages:
                    target_sections[lang_data.get("language")] = lang_data

            if not en_section:
                sync_log.append("ERROR: English section not found")
                return sync_log

            # Get all English dropdowns
            en_dropdowns = en_section.get("dropdowns", [])
            if not en_dropdowns:
                sync_log.append("INFO: No dropdowns found in English section")
                return sync_log

            sync_log.append(f"INFO: Found {len(en_dropdowns)} English dropdowns to sync")

            # Sync each English dropdown to target languages
            for target_lang, target_section in target_sections.items():
                if not target_section:
                    sync_log.append(f"WARNING: {target_lang} section not found")
                    continue

                # Ensure dropdowns array exists
                target_section.setdefault("dropdowns", [])

                # Process each English dropdown
                for en_dropdown in en_dropdowns:
                    en_dropdown_name = en_dropdown.get("dropdown", "")
                    if not en_dropdown_name:
                        continue

                    # Get translated dropdown name from config.json
                    target_dropdown_name = self.get_dropdown_translation(en_dropdown_name, target_lang)

                    # Find existing dropdown in target language by translated name
                    target_dropdown = None
                    dropdown_index = -1
                    for i, dropdown in enumerate(target_section["dropdowns"]):
                        if dropdown.get("dropdown") == target_dropdown_name:
                            target_dropdown = dropdown
                            dropdown_index = i
                            break

                    if not target_dropdown:
                        # Create new dropdown - SET translated name
                        target_dropdown = {
                            "dropdown": target_dropdown_name,
                            "icon": en_dropdown.get("icon", "book-open"),
                            "pages": []
                        }
                        target_section["dropdowns"].append(target_dropdown)
                        sync_log.append(f"INFO: Created new '{target_dropdown_name}' dropdown for {target_lang}")
                    else:
                        # Update existing dropdown - PRESERVE existing name, only update icon
                        # Do NOT overwrite target_dropdown["dropdown"] to preserve existing translations
                        if "icon" in en_dropdown:
                            target_dropdown["icon"] = en_dropdown["icon"]
                        # Remove old structure fields if they exist
                        if "groups" in target_dropdown:
                            del target_dropdown["groups"]
                        sync_log.append(f"INFO: Updated existing '{target_dropdown.get('dropdown')}' dropdown for {target_lang}")

                    # Sync the pages structure
                    if "pages" in en_dropdown:
                        existing_pages = target_dropdown.get("pages", [])
                        synced_pages = self.convert_pages_structure(
                            en_dropdown["pages"],
                            target_lang,
                            existing_pages
                        )
                        target_dropdown["pages"] = synced_pages
                        sync_log.append(f"INFO: Synced pages structure for '{target_dropdown.get('dropdown')}' ({target_lang})")

            # Save the updated docs.json
            if self.save_docs_json(docs_data):
                sync_log.append("INFO: Updated docs.json with synced structure")
            else:
                sync_log.append("ERROR: Failed to save updated docs.json")

        except Exception as e:
            sync_log.append(f"ERROR: Exception in docs.json sync: {e}")
            import traceback
            sync_log.append(f"TRACE: {traceback.format_exc()}")

        return sync_log
    
    def extract_page_paths(self, structure, normalize_lang=True):
        """
        Extract all page paths from a structure recursively.
        Returns a set of normalized paths (without language prefix) for comparison.
        """
        paths = set()

        if not structure:
            return paths

        for item in structure:
            if isinstance(item, str):
                # Normalize path by removing language prefix
                if normalize_lang:
                    normalized = re.sub(r'^(en|cn|jp)/', '', item)
                    paths.add(normalized)
                else:
                    paths.add(item)
            elif isinstance(item, dict) and "pages" in item:
                # Recursively extract from nested pages
                nested_paths = self.extract_page_paths(item["pages"], normalize_lang)
                paths.update(nested_paths)

        return paths

    def find_matching_group(self, en_group_item, existing_structure, target_lang):
        """
        Find a matching group in existing structure based on page content.
        Groups match if they contain the same normalized page paths.
        """
        if not existing_structure or not isinstance(en_group_item, dict):
            return None

        if "pages" not in en_group_item:
            return None

        # Extract normalized paths from English group
        en_paths = self.extract_page_paths(en_group_item["pages"], normalize_lang=True)

        if not en_paths:
            return None

        # Search through existing structure for matching group
        for existing_item in existing_structure:
            if isinstance(existing_item, dict) and "pages" in existing_item:
                existing_paths = self.extract_page_paths(existing_item["pages"], normalize_lang=True)

                # Groups match if they have identical page sets
                if en_paths == existing_paths:
                    return existing_item

        return None

    def convert_pages_structure(self, pages_structure, target_lang: str, existing_structure=None):
        """
        Recursively convert English page paths to target language paths.
        Uses content-based matching to preserve existing group translations.
        Groups are matched by their page content, not by position.
        """
        if not pages_structure:
            return []

        converted = []
        for item in pages_structure:
            if isinstance(item, str):
                # Convert path: en/documentation/pages/... -> target_lang/documentation/pages/...
                if item.startswith("en/"):
                    converted_path = item.replace("en/", f"{target_lang}/", 1)
                    converted.append(converted_path)
                else:
                    converted.append(item)
            elif isinstance(item, dict):
                converted_item = {}

                # For groups, use content-based matching instead of index-based
                existing_match = None
                if "group" in item and existing_structure:
                    existing_match = self.find_matching_group(item, existing_structure, target_lang)

                for key, value in item.items():
                    if key == "pages" and isinstance(value, list):
                        # Recursively convert nested pages
                        # Pass existing nested structure if we found a matching group
                        existing_nested = None
                        if existing_match and "pages" in existing_match:
                            existing_nested = existing_match["pages"]

                        converted_item[key] = self.convert_pages_structure(
                            value,
                            target_lang,
                            existing_nested
                        )
                    elif key == "group":
                        # Preserve existing human-translated group name if we found a match
                        if existing_match and "group" in existing_match:
                            # Use existing translated group name from matched group
                            converted_item[key] = existing_match["group"]
                        else:
                            # New group or no match - use basic translation
                            translated_group = self.get_basic_label_translation(value, target_lang)
                            converted_item[key] = translated_group
                    else:
                        converted_item[key] = value
                converted.append(converted_item)
            else:
                converted.append(item)

        return converted
    
    async def run_sync(self, since_commit: str = "HEAD~1") -> Dict[str, List[str]]:
        """Run the complete synchronization process"""
        print("=== Starting Documentation Synchronization ===")

        # Get file changes
        changes = self.get_changed_files(since_commit)
        print(f"Detected changes: {changes}")

        results = {
            "file_operations": [],
            "translations": [],
            "structure_sync": [],
            "errors": []
        }

        try:
            # 1. Sync file operations (delete, rename)
            results["file_operations"] = self.sync_file_operations(changes)

            # 2. Translate new and modified files (pass since_commit for diffs)
            results["translations"] = await self.translate_new_and_modified_files(changes, since_commit)

            # 3. Sync docs.json structure if needed
            if self.extract_english_structure_changes(changes):
                results["structure_sync"] = self.sync_docs_json_structure()

        except Exception as e:
            results["errors"].append(f"CRITICAL: {e}")
            print(f"Critical error during sync: {e}")

        print("=== Synchronization Complete ===")
        return results
    
    async def secure_sync_from_plan(self, sync_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute synchronization from a validated sync plan (for external PRs)
        """
        print("=== Starting Secure Documentation Synchronization ===")
        
        # Validate sync plan
        if self.enable_security:
            valid, error = self.validate_sync_plan(sync_plan)
            if not valid:
                return {"errors": [f"Invalid sync plan: {error}"]}
        
        results = {
            "translated": [],
            "failed": [],
            "skipped": [],
            "structure_synced": False,
            "errors": []
        }
        
        try:
            # Process files from sync plan
            files_to_sync = sync_plan.get("files_to_sync", [])
            
            # Limit number of files for security
            max_files = 10 if self.enable_security else len(files_to_sync)
            files_to_process = files_to_sync[:max_files]
            
            for file_info in files_to_process:
                file_path = file_info.get("path")
                if not file_path:
                    continue
                
                # Additional security validation per file
                if self.enable_security:
                    valid, error = self.validate_file_path(file_path)
                    if not valid:
                        results["errors"].append(f"Invalid file path {file_path}: {error}")
                        continue
                
                print(f"Processing: {file_path}")
                
                # Check if source file exists
                if not (self.base_dir / file_path).exists():
                    results["skipped"].append(file_path)
                    continue

                # Translate to target languages
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    try:
                        success = await self.translate_file_with_notice(
                            file_path, target_path, target_lang
                        )
                        if success:
                            results["translated"].append(target_path)
                        else:
                            results["failed"].append(target_path)
                    except Exception as e:
                        print(f"Error translating {file_path} to {target_lang}: {e}")
                        results["failed"].append(target_path)

            # Process OpenAPI JSON files
            openapi_files_to_sync = sync_plan.get("openapi_files_to_sync", [])

            # Limit number of OpenAPI files for security
            max_openapi_files = 5 if self.enable_security else len(openapi_files_to_sync)
            openapi_files_to_process = openapi_files_to_sync[:max_openapi_files]

            for file_info in openapi_files_to_process:
                file_path = file_info.get("path")
                if not file_path:
                    continue

                # Additional security validation per file
                if self.enable_security:
                    valid, error = self.validate_file_path(file_path)
                    if not valid:
                        results["errors"].append(f"Invalid OpenAPI file path {file_path}: {error}")
                        continue

                print(f"Processing OpenAPI: {file_path}")

                # Check if source file exists
                source_full_path = self.base_dir / file_path
                if not source_full_path.exists():
                    results["skipped"].append(file_path)
                    continue

                # Translate to target languages
                for target_lang in self.target_languages:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    target_full_path = self.base_dir / target_path

                    try:
                        # Ensure target directory exists
                        target_full_path.parent.mkdir(parents=True, exist_ok=True)

                        # Run OpenAPI translation pipeline (use async version)
                        success = await translate_openapi_file_async(
                            source_file=str(source_full_path),
                            target_lang=target_lang,
                            output_file=str(target_full_path),
                            dify_api_key=self.dify_api_key
                        )

                        if success:
                            results["translated"].append(target_path)
                            print(f"✅ Successfully translated OpenAPI: {file_path} → {target_path}")
                        else:
                            results["failed"].append(target_path)
                            print(f"❌ Failed to translate OpenAPI: {file_path} → {target_path}")

                    except Exception as e:
                        print(f"Error translating OpenAPI {file_path} to {target_lang}: {e}")
                        results["failed"].append(target_path)

            # Handle structure changes
            structure_changes = sync_plan.get("structure_changes", {})
            if structure_changes.get("structure_changed"):
                print("Syncing documentation structure...")
                try:
                    sync_log = self.sync_docs_json_structure()
                    results["structure_synced"] = True
                    print("Structure sync completed")
                except Exception as e:
                    results["errors"].append(f"Structure sync failed: {e}")
            
        except Exception as e:
            results["errors"].append(f"Critical error: {e}")
        
        print("=== Secure Synchronization Complete ===")
        return results

async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python sync_and_translate.py <dify_api_key> [since_commit]")
        print("  since_commit: Git commit to compare against (default: HEAD~1)")
        sys.exit(1)
    
    dify_api_key = sys.argv[1]
    since_commit = sys.argv[2] if len(sys.argv) > 2 else "HEAD~1"
    
    # Initialize synchronizer
    synchronizer = DocsSynchronizer(dify_api_key)
    
    # Run synchronization
    results = await synchronizer.run_sync(since_commit)
    
    # Print results
    print("\n=== SYNCHRONIZATION RESULTS ===")
    for category, logs in results.items():
        if logs:
            print(f"\n{category.upper()}:")
            for log in logs:
                print(f"  {log}")
    
    # Return appropriate exit code
    if results["errors"]:
        sys.exit(1)
    else:
        print("\n✓ Synchronization completed successfully")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())