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

# Language configurations
LANGUAGES = {
    "en": {
        "name": "English",
        "base_path": "en",
        "code": "en"
    },
    "cn": {
        "name": "Chinese",
        "base_path": "cn",
        "code": "cn"
    },
    "jp": {
        "name": "Japanese",
        "base_path": "jp",
        "code": "jp"
    }
}

TARGET_LANGUAGES = ["cn", "jp"]

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
        self.notices = self.load_notices()
    
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
                return json.load(f)
        return {
            "path_mappings": {
                "en": ["cn", "jp"]
            },
            "label_translations": {}
        }
    
    def load_notices(self) -> Dict[str, str]:
        """Load AI translation notice templates"""
        notices_path = SCRIPT_DIR / "notices.json"
        if notices_path.exists():
            with open(notices_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "cn": "> ⚠️ 本文档由 AI 自动翻译。如有任何不准确之处，请参考[英文原版]({en_path})。\n\n",
            "jp": "> ⚠️ このドキュメントはAIによって自動翻訳されています。不正確な部分がある場合は、[英語版]({en_path})を参照してください。\n\n"
        }
    
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
    
    def is_english_doc_file(self, file_path: str) -> bool:
        """Check if file is an English documentation file that should be synced"""
        return (file_path.startswith("en/") and 
                (file_path.endswith('.md') or file_path.endswith('.mdx')) and
                not file_path.startswith("en/api-reference/"))
    
    def convert_path_to_target_language(self, en_path: str, target_lang: str) -> str:
        """Convert English path to target language path"""
        if en_path.startswith("en/"):
            return en_path.replace("en/", f"{target_lang}/", 1)
        return en_path
    
    def get_relative_en_path_for_notice(self, target_path: str) -> str:
        """Get relative path to English version for AI notice"""
        # Convert cn/documentation/pages/getting-started/faq.md
        # to ../../en/documentation/pages/getting-started/faq.md
        if target_path.startswith("cn/"):
            en_path = target_path.replace("cn/", "en/", 1)
        elif target_path.startswith("jp/"):
            en_path = target_path.replace("jp/", "en/", 1)
        else:
            return ""

        # Count directory levels to create relative path
        target_dir_levels = len(Path(target_path).parent.parts)
        relative_prefix = "../" * target_dir_levels
        return relative_prefix + en_path
    
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

    async def translate_file_with_notice(self, en_file_path: str, target_file_path: str, target_lang: str) -> bool:
        """Translate a file and add AI notice at the top"""
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
            en_lang_name = LANGUAGES["en"]["name"]
            target_lang_name = LANGUAGES[target_lang]["name"]
            
            # Translate content
            translated_content = await translate_text(
                str(self.base_dir / en_file_path),
                self.dify_api_key,
                en_lang_name,
                target_lang_name
            )
            
            if not translated_content or not translated_content.strip():
                print(f"Warning: No translated content received for {en_file_path}")
                return False
            
            # Prepare AI notice
            en_relative_path = self.get_relative_en_path_for_notice(target_file_path)
            notice = self.notices.get(target_lang, "").format(en_path=en_relative_path)
            
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
                for target_lang in TARGET_LANGUAGES:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    # We'll translate these in the async part
                    operations_log.append(f"WILL_TRANSLATE: {file_path} -> {target_path}")
        
        # Handle deleted files
        for file_path in changes["deleted"]:
            if self.is_english_doc_file(file_path):
                for target_lang in TARGET_LANGUAGES:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    target_full_path = self.base_dir / target_path
                    if target_full_path.exists():
                        target_full_path.unlink()
                        operations_log.append(f"DELETED: {target_path}")
        
        # Handle renamed files  
        for old_path, new_path in changes["renamed"]:
            if self.is_english_doc_file(old_path) or self.is_english_doc_file(new_path):
                for target_lang in TARGET_LANGUAGES:
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
    
    async def translate_new_and_modified_files(self, changes: Dict[str, List[str]]) -> List[str]:
        """Translate new and modified files"""
        translation_log = []
        tasks = []
        
        # Collect translation tasks
        for file_path in changes["added"] + changes["modified"]:
            if self.is_english_doc_file(file_path):
                for target_lang in TARGET_LANGUAGES:
                    target_path = self.convert_path_to_target_language(file_path, target_lang)
                    task = self.translate_file_with_notice(file_path, target_path, target_lang)
                    tasks.append((task, file_path, target_path))
        
        # Handle renamed files that need translation
        for old_path, new_path in changes["renamed"]:
            if self.is_english_doc_file(new_path):
                for target_lang in TARGET_LANGUAGES:
                    target_path = self.convert_path_to_target_language(new_path, target_lang)
                    task = self.translate_file_with_notice(new_path, target_path, target_lang)
                    tasks.append((task, new_path, target_path))
        
        # Execute translations with concurrency control
        semaphore = asyncio.Semaphore(2)  # Limit concurrent translations
        
        async def bounded_translate(task, en_path, target_path):
            async with semaphore:
                success = await task
                return success, en_path, target_path
        
        # Run translations
        if tasks:
            print(f"Starting {len(tasks)} translation tasks...")
            results = await asyncio.gather(*[
                bounded_translate(task, en_path, target_path) 
                for task, en_path, target_path in tasks
            ], return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    translation_log.append(f"ERROR: {result}")
                else:
                    success, en_path, target_path = result
                    if success:
                        translation_log.append(f"TRANSLATED: {en_path} -> {target_path}")
                    else:
                        translation_log.append(f"FAILED: {en_path} -> {target_path}")
        
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
    
    def sync_docs_json_structure(self) -> List[str]:
        """Sync docs.json structure across languages - syncs ALL dropdowns"""
        sync_log = []

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
            zh_section = None
            ja_section = None

            for lang_data in languages_array:
                if lang_data.get("language") == "en":
                    en_section = lang_data
                elif lang_data.get("language") == "cn":
                    zh_section = lang_data
                elif lang_data.get("language") == "jp":
                    ja_section = lang_data

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
            for target_section, target_lang in [(zh_section, "cn"), (ja_section, "jp")]:
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
                        # Create new dropdown
                        target_dropdown = {
                            "dropdown": target_dropdown_name,
                            "icon": en_dropdown.get("icon", "book-open"),
                            "pages": []
                        }
                        target_section["dropdowns"].append(target_dropdown)
                        sync_log.append(f"INFO: Created new '{target_dropdown_name}' dropdown for {target_lang}")
                    else:
                        # Update existing dropdown
                        target_dropdown["dropdown"] = target_dropdown_name
                        if "icon" in en_dropdown:
                            target_dropdown["icon"] = en_dropdown["icon"]
                        # Remove old structure fields if they exist
                        if "groups" in target_dropdown:
                            del target_dropdown["groups"]
                        sync_log.append(f"INFO: Updated existing '{target_dropdown_name}' dropdown for {target_lang}")

                    # Sync the pages structure
                    if "pages" in en_dropdown:
                        existing_pages = target_dropdown.get("pages", [])
                        synced_pages = self.convert_pages_structure(
                            en_dropdown["pages"],
                            target_lang,
                            existing_pages
                        )
                        target_dropdown["pages"] = synced_pages
                        sync_log.append(f"INFO: Synced pages structure for '{target_dropdown_name}' ({target_lang})")

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
            
            # 2. Translate new and modified files
            results["translations"] = await self.translate_new_and_modified_files(changes)
            
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
                for target_lang in TARGET_LANGUAGES:
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