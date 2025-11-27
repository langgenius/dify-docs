#!/usr/bin/env python3
"""
PR Analyzer for Documentation Translation Workflow

This utility analyzes pull request changes to categorize them and validate
they follow the proper workflow requirements for English vs translation content.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

class PRAnalyzer:
    """Analyzes PR changes to categorize and validate translation workflow requirements."""
    
    def __init__(self, base_sha: str, head_sha: str, repo_root: Optional[str] = None):
        self.base_sha = base_sha
        self.head_sha = head_sha
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent.parent
        self.docs_json_path = self.repo_root / "docs.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load translation configuration."""
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files between base and head commits."""
        try:
            result = subprocess.run([
                "git", "diff", "--name-only", self.base_sha, self.head_sha
            ], capture_output=True, text=True, check=True, cwd=self.repo_root)
            
            files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            return files
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}")
            return []
    
    def get_docs_json_at_sha(self, sha: str) -> Optional[Dict]:
        """Get docs.json content at a specific commit."""
        try:
            result = subprocess.run([
                "git", "show", f"{sha}:docs.json"
            ], capture_output=True, text=True, check=True, cwd=self.repo_root)
            
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"Error loading docs.json at {sha}: {e}")
            return None
    
    def extract_language_navigation(self, docs_data: Dict, language: str) -> Optional[Dict]:
        """Extract navigation structure for a specific language from docs.json."""
        if not docs_data or 'navigation' not in docs_data:
            return None

        navigation = docs_data['navigation']

        # Handle both direct languages and versions structure
        if 'languages' in navigation:
            languages = navigation['languages']
        elif 'versions' in navigation and len(navigation['versions']) > 0:
            languages = navigation['versions'][0].get('languages', [])
        else:
            return None

        for lang_data in languages:
            if lang_data.get('language') == language:
                return lang_data

        return None
    
    def analyze_docs_json_changes(self) -> Dict[str, bool]:
        """Analyze which language sections changed in docs.json."""
        base_docs = self.get_docs_json_at_sha(self.base_sha)
        head_docs = self.get_docs_json_at_sha(self.head_sha)
        
        changes = {
            'english_section': False,
            'translation_sections': False,
            'any_docs_json_changes': False
        }
        
        if not base_docs or not head_docs:
            return changes
        
        # Check if docs.json changed at all
        if base_docs != head_docs:
            changes['any_docs_json_changes'] = True
        
        # Check source language navigation section
        source_lang = self.config['source_language']
        base_en = self.extract_language_navigation(base_docs, source_lang)
        head_en = self.extract_language_navigation(head_docs, source_lang)
        if base_en != head_en:
            changes['english_section'] = True
        
        # Check translation sections
        for lang in self.config['target_languages']:
            base_lang = self.extract_language_navigation(base_docs, lang)
            head_lang = self.extract_language_navigation(head_docs, lang)
            if base_lang != head_lang:
                changes['translation_sections'] = True
                break
        
        return changes
    
    def is_openapi_file(self, file_path: str) -> bool:
        """Check if file matches OpenAPI patterns from config."""
        openapi_config = self.config.get('openapi', {})

        if not openapi_config.get('enabled', False):
            return False

        patterns = openapi_config.get('file_patterns', [])
        directories = openapi_config.get('directories', [])

        # Check if in allowed directory
        path_parts = Path(file_path).parts
        if len(path_parts) < 3:  # e.g., en/api-reference/file.json
            return False

        dir_name = path_parts[1]  # Get directory after language code
        if dir_name not in directories:
            return False

        # Check if matches any pattern
        file_name = Path(file_path).name
        for pattern in patterns:
            if self._match_pattern(file_name, pattern):
                return True

        return False

    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Simple glob-like pattern matching."""
        regex = pattern.replace('*', '.*').replace('?', '.')
        return bool(re.match(f'^{regex}$', filename))

    def categorize_files(self, files: List[str]) -> Dict[str, List[str]]:
        """Categorize changed files by type."""
        categories = {
            'english': [],
            'english_openapi': [],      # NEW category
            'translation': [],
            'translation_openapi': [],  # NEW category
            'docs_json': [],
            'other': []
        }

        for file in files:
            if file == 'docs.json':
                categories['docs_json'].append(file)
            elif file.startswith('en/'):
                if file.endswith(('.md', '.mdx')):
                    categories['english'].append(file)
                elif self.is_openapi_file(file):  # NEW
                    categories['english_openapi'].append(file)
                else:
                    categories['other'].append(file)
            elif file.startswith(('ja/', 'zh/')):
                if file.endswith(('.md', '.mdx')):
                    categories['translation'].append(file)
                elif self.is_openapi_file(file):  # NEW
                    categories['translation_openapi'].append(file)
                else:
                    categories['other'].append(file)
            else:
                categories['other'].append(file)

        return categories
    
    def categorize_pr(self) -> Dict[str, any]:
        """Categorize the PR based on changed files and docs.json sections."""
        changed_files = self.get_changed_files()
        if not changed_files:
            return {
                'type': 'none',
                'should_skip': True,
                'error': None,
                'files': {'english': [], 'translation': [], 'docs_json': [], 'other': []},
                'docs_json_changes': {'english_section': False, 'translation_sections': False, 'any_docs_json_changes': False}
            }
        
        file_categories = self.categorize_files(changed_files)
        docs_json_changes = self.analyze_docs_json_changes()

        # Determine if there are English content changes (including OpenAPI)
        has_english_files = len(file_categories['english']) > 0 or len(file_categories['english_openapi']) > 0
        has_english_docs_changes = docs_json_changes['english_section']

        # Determine if there are translation changes (including OpenAPI)
        has_translation_files = len(file_categories['translation']) > 0 or len(file_categories['translation_openapi']) > 0
        has_translation_docs_changes = docs_json_changes['translation_sections']
        
        # Filter out non-documentation changes from consideration
        relevant_english_changes = has_english_files or has_english_docs_changes
        relevant_translation_changes = has_translation_files or has_translation_docs_changes
        
        # Categorize PR type
        if relevant_english_changes and relevant_translation_changes:
            pr_type = 'mixed'
            should_skip = False
            error = self.generate_mixed_pr_error(file_categories, docs_json_changes)
        elif relevant_english_changes:
            pr_type = 'english'
            should_skip = False
            error = None
        elif relevant_translation_changes:
            pr_type = 'translation'
            should_skip = True
            error = None
        else:
            pr_type = 'none'
            should_skip = True
            error = None
        
        return {
            'type': pr_type,
            'should_skip': should_skip,
            'error': error,
            'files': file_categories,
            'docs_json_changes': docs_json_changes
        }
    
    def generate_mixed_pr_error(self, file_categories: Dict[str, List[str]], docs_json_changes: Dict[str, bool]) -> str:
        """Generate comprehensive error message for mixed PRs."""
        
        def format_file_list(files: List[str], max_files: int = 10) -> str:
            if not files:
                return "   - (none)"
            
            formatted = []
            for file in files[:max_files]:
                formatted.append(f"   - `{file}`")
            
            if len(files) > max_files:
                formatted.append(f"   - ... and {len(files) - max_files} more")
            
            return '\n'.join(formatted)
        
        def format_docs_json_changes(changes: Dict[str, bool]) -> str:
            parts = []
            if changes['english_section']:
                parts.append("   - ✅ English navigation section")
            if changes['translation_sections']:
                parts.append("   - ✅ Translation navigation sections (jp, cn)")
            if not parts:
                parts.append("   - (no navigation changes)")
            return '\n'.join(parts)
        
        error_msg = f"""❌ **Mixed Content PR Detected**

This PR contains changes to both English content and translations, which violates our automated workflow requirements.

**🔧 Required Action: Separate into Two PRs**

Please create two separate pull requests:

### 1️⃣ **English Content PR** 
Create a PR containing only:
- Changes to `en/` files  
- Changes to English navigation in `docs.json`
- This will trigger automatic translation generation

### 2️⃣ **Translation Improvement PR**
Create a PR containing only:
- Changes to `jp/` and `cn/` files
- Changes to translation navigation sections in `docs.json`
- This will go through direct review (no automation)

---

**📋 Files Detected in This PR:**

**📝 English Content Files ({len(file_categories['english'])} files):**
{format_file_list(file_categories['english'])}

**🌐 Translation Files ({len(file_categories['translation'])} files):**
{format_file_list(file_categories['translation'])}

**📋 docs.json Navigation Changes:**
{format_docs_json_changes(docs_json_changes)}

---

**💡 Why This Separation is Required:**

- **Proper Review Process**: English content and translations have different review requirements
- **Automation Conflicts**: Mixed PRs break the automated translation workflow  
- **Independent Merging**: Content and translations can be merged independently
- **Clear History**: Maintains clean git history for content vs translation changes

**🤖 What Happens Next:**

1. **English PR**: Will automatically generate translations and create a linked translation PR
2. **Translation PR**: Will go through standard review process
3. **Both PRs**: Can be reviewed and merged independently

Please separate your changes and resubmit as two focused PRs. Thank you! 🙏"""

        return error_msg


class SyncPlanGenerator:
    """
    Generates sync_plan.json with identical logic for both execute and update workflows.

    Extracts the sync plan generation logic from the analyze workflow to ensure
    both workflows use the same file filtering and structure change detection.
    """

    def __init__(self, base_sha: str, head_sha: str, repo_root: Optional[str] = None):
        self.base_sha = base_sha
        self.head_sha = head_sha
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent.parent
        self.analyzer = PRAnalyzer(base_sha, head_sha, repo_root)
        self.config = self.analyzer.config

    def get_changed_files_with_status(self) -> List[Tuple[str, str]]:
        """
        Get list of changed files with their status (A=added, M=modified, D=deleted, etc).

        Returns list of tuples: [(status, filepath), ...]
        Only returns A (added) and M (modified) files for translation.
        Filters out files that don't exist at head_sha (handles add-then-delete scenario).
        """
        try:
            result = subprocess.run([
                "git", "diff", "--name-status", "--diff-filter=AM",
                self.base_sha, self.head_sha
            ], capture_output=True, text=True, check=True, cwd=self.repo_root)

            files_with_status = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('\t', 1)
                    if len(parts) == 2:
                        status, filepath = parts[0], parts[1]

                        # Verify file exists at head_sha (handles add-then-delete scenario)
                        if self._file_exists_at_commit(filepath, self.head_sha):
                            files_with_status.append((status, filepath))
                        else:
                            print(f"Skipping {filepath}: added then deleted in same PR")

            return files_with_status
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files with status: {e}")
            return []

    def _file_exists_at_commit(self, filepath: str, commit_sha: str) -> bool:
        """Check if a file exists at a specific commit."""
        try:
            subprocess.run([
                "git", "cat-file", "-e", f"{commit_sha}:{filepath}"
            ], capture_output=True, check=True, cwd=self.repo_root)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes."""
        full_path = self.repo_root / filepath
        try:
            return full_path.stat().st_size if full_path.exists() else 0
        except:
            return 0

    def is_openapi_file(self, filepath: str) -> bool:
        """Check if file matches OpenAPI JSON pattern."""
        openapi_config = self.config.get("openapi", {})
        if not openapi_config.get("enabled", False):
            return False

        file_patterns = openapi_config.get("file_patterns", ["openapi*.json"])
        directories = openapi_config.get("directories", ["api-reference"])

        # Check if file is in allowed directories
        if not any(f"/{dir}/" in filepath or filepath.startswith(f"{dir}/") for dir in directories):
            return False

        # Check if filename matches patterns
        filename = Path(filepath).name
        for pattern in file_patterns:
            regex = pattern.replace('*', '.*').replace('?', '.')
            if re.match(f'^{regex}$', filename):
                return True

        return False

    def generate_sync_plan(self) -> Dict:
        """
        Generate sync plan with identical logic to analyze workflow.

        Returns sync_plan dict with:
        - metadata: PR context and commit info
        - files_to_sync: English markdown files (A/M only)
        - openapi_files_to_sync: English OpenAPI JSON files (A/M only)
        - structure_changes: docs.json change analysis
        - target_languages: Languages to translate to
        - sync_required: Whether any sync is needed
        """
        # Get changed files with status
        files_with_status = self.get_changed_files_with_status()

        # Categorize files for translation
        files_to_sync = []
        openapi_files_to_sync = []
        docs_json_changed = False

        for status, filepath in files_with_status:
            # Check for docs.json
            if filepath == 'docs.json':
                docs_json_changed = True
                continue

            # Process English markdown files
            if filepath.startswith('en/') and filepath.endswith(('.md', '.mdx')):
                file_size = self.get_file_size(filepath)
                file_type = 'mdx' if filepath.endswith('.mdx') else 'md'
                files_to_sync.append({
                    "path": filepath,
                    "size": file_size,
                    "type": file_type,
                    "status": status
                })

            # Process English OpenAPI JSON files
            elif filepath.startswith('en/') and self.is_openapi_file(filepath):
                file_size = self.get_file_size(filepath)
                openapi_files_to_sync.append({
                    "path": filepath,
                    "size": file_size,
                    "type": "openapi_json",
                    "status": status
                })

        # Analyze docs.json changes (if changed)
        if docs_json_changed:
            docs_changes = self.analyzer.analyze_docs_json_changes()
            structure_changes = {
                "structure_changed": docs_changes["any_docs_json_changes"],
                "navigation_modified": docs_changes["english_section"],
                "languages_affected": self.config["target_languages"] if docs_changes["english_section"] else []
            }
        else:
            structure_changes = {
                "structure_changed": False,
                "navigation_modified": False,
                "languages_affected": []
            }

        # Create metadata
        metadata = {
            "base_sha": self.base_sha,
            "head_sha": self.head_sha,
            "comparison": f"{self.base_sha[:8]}...{self.head_sha[:8]}"
        }

        # Build sync plan
        sync_plan = {
            "metadata": metadata,
            "files_to_sync": files_to_sync,
            "openapi_files_to_sync": openapi_files_to_sync,
            "structure_changes": structure_changes,
            "target_languages": self.config["target_languages"],
            "sync_required": len(files_to_sync) > 0 or len(openapi_files_to_sync) > 0 or structure_changes.get("structure_changed", False)
        }

        return sync_plan


def main():
    """Main entry point for command line usage."""
    if len(sys.argv) != 3:
        print("Usage: python pr_analyzer.py <base_sha> <head_sha>")
        sys.exit(1)
    
    base_sha = sys.argv[1]
    head_sha = sys.argv[2]
    
    analyzer = PRAnalyzer(base_sha, head_sha)
    result = analyzer.categorize_pr()
    
    # Output results for GitHub Actions
    print(f"pr_type={result['type']}")
    print(f"should_skip={str(result['should_skip']).lower()}")
    
    if result['error']:
        print(f"error_message={result['error']}")
        sys.exit(1)
    
    # Output additional details
    files = result['files']
    docs_changes = result['docs_json_changes']
    
    print(f"english_files_count={len(files['english'])}")
    print(f"translation_files_count={len(files['translation'])}")
    print(f"docs_json_english_changes={str(docs_changes['english_section']).lower()}")
    print(f"docs_json_translation_changes={str(docs_changes['translation_sections']).lower()}")
    print(f"any_docs_json_changes={str(docs_changes['any_docs_json_changes']).lower()}")

if __name__ == "__main__":
    main()