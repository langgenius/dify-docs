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
        
        # Check English navigation section
        base_en = self.extract_language_navigation(base_docs, 'en')
        head_en = self.extract_language_navigation(head_docs, 'en')
        if base_en != head_en:
            changes['english_section'] = True
        
        # Check translation sections
        for lang in ['jp', 'cn']:
            base_lang = self.extract_language_navigation(base_docs, lang)
            head_lang = self.extract_language_navigation(head_docs, lang)
            if base_lang != head_lang:
                changes['translation_sections'] = True
                break
        
        return changes
    
    def categorize_files(self, files: List[str]) -> Dict[str, List[str]]:
        """Categorize changed files by type."""
        categories = {
            'english': [],
            'translation': [],
            'docs_json': [],
            'other': []
        }
        
        for file in files:
            if file == 'docs.json':
                categories['docs_json'].append(file)
            elif file.startswith('en/'):
                if file.endswith(('.md', '.mdx')):
                    categories['english'].append(file)
                else:
                    categories['other'].append(file)
            elif file.startswith(('jp/', 'cn/')):
                if file.endswith(('.md', '.mdx')):
                    categories['translation'].append(file)
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
        
        # Determine if there are English content changes
        has_english_files = len(file_categories['english']) > 0
        has_english_docs_changes = docs_json_changes['english_section']
        
        # Determine if there are translation changes
        has_translation_files = len(file_categories['translation']) > 0  
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