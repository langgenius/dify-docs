#!/usr/bin/env python3
"""
Translate and commit documentation changes to a translation PR.

This script consolidates the core translation logic used by both the
execute and update workflows. It handles:
- Branch setup (create new or checkout existing)
- Translation of documentation files
- English file removal
- Committing and pushing changes
- Creating/updating translation PRs
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sync_and_translate import DocsSynchronizer
from pr_analyzer import PRAnalyzer


class TranslationPRManager:
    """Manages the translation PR workflow."""

    def __init__(
        self,
        pr_number: int,
        head_sha: str,
        base_sha: str,
        is_incremental: bool,
        pr_title: Optional[str] = None,
        work_dir: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        self.pr_number = pr_number
        self.head_sha = head_sha
        self.base_sha = base_sha
        self.is_incremental = is_incremental
        self.pr_title = pr_title or "Documentation changes"
        self.work_dir = work_dir or "/tmp"
        self.api_key = api_key or os.environ.get("DIFY_API_KEY")

        self.sync_branch = f"docs-sync-pr-{pr_number}"
        self.repo_root = Path(__file__).parent.parent.parent

        # Load translation config
        config_path = self.repo_root / "tools/translate/config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.translation_config = json.load(f)

        self.source_language = self.translation_config.get("source_language", "en")
        self.target_languages = self.translation_config.get("target_languages", ["cn", "jp"])
        self.source_dir = self.translation_config["languages"][self.source_language]["directory"]

        # Load processing limits
        processing_limits = self.translation_config.get("processing_limits", {})
        self.max_files_per_run = processing_limits.get("max_files_per_run", 10)
        self.max_openapi_files_per_run = processing_limits.get("max_openapi_files_per_run", 5)

        # Get repository name dynamically
        self.repo_name = self.get_repository_name()

    def run_git(self, *args: str, check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a git command."""
        cmd = ["git", *args]
        return subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=capture_output,
            text=True,
            check=check
        )

    def run_gh(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        """Run a gh CLI command."""
        cmd = ["gh", *args]
        return subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=check
        )

    def get_repository_name(self) -> str:
        """Get the repository name dynamically from environment or git remote."""
        # Try GitHub Actions environment variable first
        repo_name = os.environ.get("GITHUB_REPOSITORY")
        if repo_name:
            return repo_name

        # Fall back to parsing git remote
        try:
            result = self.run_git("remote", "get-url", "origin", check=False)
            if result.returncode == 0 and result.stdout:
                remote_url = result.stdout.strip()
                # Parse formats: git@github.com:owner/repo.git or https://github.com/owner/repo.git
                if "github.com" in remote_url:
                    if remote_url.startswith("git@"):
                        # git@github.com:owner/repo.git
                        repo_part = remote_url.split(":", 1)[1]
                    else:
                        # https://github.com/owner/repo.git
                        repo_part = "/".join(remote_url.split("/")[-2:])
                    # Remove .git suffix if present
                    repo_name = repo_part.rstrip(".git")
                    return repo_name
        except Exception as e:
            print(f"⚠️  Warning: Could not detect repository name from git remote: {e}")

        # Final fallback
        return "unknown/repository"

    def check_branch_exists(self) -> bool:
        """Check if translation branch exists on remote."""
        result = self.run_git(
            "ls-remote", "--exit-code", "--heads", "origin", self.sync_branch,
            check=False
        )
        return result.returncode == 0

    def setup_translation_branch(self, branch_exists: bool) -> None:
        """Setup the translation branch (create or checkout existing)."""
        if branch_exists:
            print(f"✅ Fetching existing translation branch for incremental update: {self.sync_branch}")
            self.run_git("fetch", "origin", f"{self.sync_branch}:{self.sync_branch}")
            self.run_git("checkout", self.sync_branch)

            # For incremental updates, checkout English files from PR
            print(f"Checking out English files from {self.head_sha[:8]}...")
            self.run_git("checkout", self.head_sha, "--", f"{self.source_dir}/", check=False)
        else:
            print(f"🆕 Creating new translation branch: {self.sync_branch}")
            self.run_git("checkout", "-b", self.sync_branch)

            # Reset branch to main to avoid including English file changes from PR
            # Use --soft to keep working directory with PR files (needed for translation)
            self.run_git("reset", "--soft", "origin/main")
            # Unstage everything
            self.run_git("reset")

    async def run_translation(self) -> Dict:
        """Run the translation process using sync_and_translate logic."""
        if not self.api_key:
            print("❌ Error: DIFY_API_KEY not set")
            return {"translated": [], "failed": ["NO_API_KEY"], "skipped": []}

        # Load sync plan if available (from artifacts)
        sync_plan_path = Path(self.work_dir) / "sync_plan.json"
        if not sync_plan_path.exists():
            print(f"⚠️  Warning: No sync plan found at {sync_plan_path}")
            print("This is expected for update workflow - will analyze PR changes directly")
            return await self.run_translation_from_pr_analysis()

        with open(sync_plan_path) as f:
            sync_plan = json.load(f)

        return await self.run_translation_from_sync_plan(sync_plan)

    async def run_translation_from_pr_analysis(self) -> Dict:
        """Run translation by analyzing PR changes directly (used by update workflow)."""
        print(f"Analyzing PR changes: {self.base_sha[:8]}...{self.head_sha[:8]}")

        analyzer = PRAnalyzer(self.base_sha, self.head_sha)
        result = analyzer.categorize_pr()

        if result['type'] != 'english':
            print(f"PR type is {result['type']}, not english - skipping translation")
            return {"translated": [], "failed": [], "skipped": ["wrong_pr_type"]}

        # Get English files from PR analysis
        files_to_sync = result['files']['english']

        # Create a minimal sync plan
        sync_plan = {
            "files_to_sync": [{"path": f} for f in files_to_sync],
            "openapi_files_to_sync": [],
            "structure_changes": {"structure_changed": True},
            "metadata": {
                "base_sha": self.base_sha,
                "head_sha": self.head_sha
            }
        }

        return await self.run_translation_from_sync_plan(sync_plan)

    async def run_translation_from_sync_plan(self, sync_plan: Dict) -> Dict:
        """Run translation from a sync plan."""
        synchronizer = DocsSynchronizer(self.api_key)

        results = {
            "translated": [],
            "failed": [],
            "skipped": []
        }

        files_to_sync = sync_plan.get("files_to_sync", [])
        metadata = sync_plan.get("metadata", {})
        base_sha = metadata.get("base_sha", self.base_sha)
        head_sha = metadata.get("head_sha", self.head_sha)

        # Detect added vs modified files
        added_files, modified_files = self.detect_file_changes(base_sha, head_sha)

        print(f"Detected {len(added_files)} added files, {len(modified_files)} modified files")

        # Translate each file with configurable limit
        if len(files_to_sync) > self.max_files_per_run:
            print(f"⚠️  Warning: PR has {len(files_to_sync)} files to sync, limiting to {self.max_files_per_run} for safety")
            print(f"   (Adjust 'processing_limits.max_files_per_run' in config.json to change this limit)")

        for file_info in files_to_sync[:self.max_files_per_run]:
            file_path = file_info.get("path") if isinstance(file_info, dict) else file_info

            if file_path == "docs.json":
                results["skipped"].append(f"{file_path} (structure file)")
                continue

            if file_path.startswith("versions/"):
                results["skipped"].append(f"{file_path} (versioned docs)")
                continue

            if not (self.repo_root / file_path).exists():
                results["skipped"].append(f"{file_path} (not found)")
                continue

            is_modified = file_path in modified_files

            # Get diff for modified files
            diff_original = None
            if is_modified:
                diff_original = self.get_file_diff(base_sha, head_sha, file_path)

            # Translate to all target languages
            for target_lang in self.target_languages:
                target_dir = self.translation_config["languages"][target_lang]["directory"]
                target_path = file_path.replace(f"{self.source_dir}/", f"{target_dir}/")

                # Load existing translation for modified files
                the_doc_exist = None
                if is_modified:
                    target_full_path = self.repo_root / target_path
                    if target_full_path.exists():
                        with open(target_full_path, 'r', encoding='utf-8') as f:
                            the_doc_exist = f.read()

                try:
                    success = await synchronizer.translate_file_with_notice(
                        file_path,
                        target_path,
                        target_lang,
                        the_doc_exist=the_doc_exist,
                        diff_original=diff_original
                    )

                    if success:
                        change_type = "modified" if is_modified else "added"
                        results["translated"].append(f"{target_path} ({change_type})")
                    else:
                        results["failed"].append(target_path)
                except Exception as e:
                    print(f"❌ Error translating {file_path} to {target_lang}: {e}")
                    results["failed"].append(target_path)

        # Handle OpenAPI files if present
        openapi_files = sync_plan.get("openapi_files_to_sync", [])
        if openapi_files:
            await self.translate_openapi_files(openapi_files, results)

        # Sync docs.json structure
        if sync_plan.get("structure_changes", {}).get("structure_changed"):
            self.sync_docs_json_structure(synchronizer, added_files, base_sha, head_sha)

        return results

    def detect_file_changes(self, base_sha: str, head_sha: str) -> Tuple[List[str], List[str]]:
        """Detect added and modified files between two commits."""
        added_files = []
        modified_files = []

        try:
            result = self.run_git(
                "diff", "--name-status", "--diff-filter=AM",
                base_sha, head_sha
            )

            for line in result.stdout.strip().split('\n'):
                if line and '\t' in line:
                    status, file_path = line.split('\t', 1)
                    if status == 'A':
                        added_files.append(file_path)
                    elif status == 'M':
                        modified_files.append(file_path)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not detect file status: {e}")
            # Fallback: treat all as added

        return added_files, modified_files

    def get_file_diff(self, base_sha: str, head_sha: str, file_path: str) -> Optional[str]:
        """Get the diff for a specific file between two commits."""
        try:
            result = self.run_git("diff", base_sha, head_sha, "--", file_path)
            return result.stdout if result.stdout else None
        except subprocess.CalledProcessError:
            return None

    async def translate_openapi_files(self, openapi_files: List, results: Dict) -> None:
        """Translate OpenAPI JSON files."""
        from openapi import translate_openapi_file_async

        # Apply configurable limit with warning
        if len(openapi_files) > self.max_openapi_files_per_run:
            print(f"⚠️  Warning: PR has {len(openapi_files)} OpenAPI files, limiting to {self.max_openapi_files_per_run} for safety")
            print(f"   (Adjust 'processing_limits.max_openapi_files_per_run' in config.json to change this limit)")

        for file_info in openapi_files[:self.max_openapi_files_per_run]:
            file_path = file_info.get("path") if isinstance(file_info, dict) else file_info
            source_full_path = self.repo_root / file_path

            if not source_full_path.exists():
                results["skipped"].append(f"{file_path} (openapi not found)")
                continue

            for target_lang in self.target_languages:
                target_dir = self.translation_config["languages"][target_lang]["directory"]
                target_path = file_path.replace(f"{self.source_dir}/", f"{target_dir}/")
                target_full_path = self.repo_root / target_path

                target_full_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    success = await translate_openapi_file_async(
                        source_file=str(source_full_path),
                        target_lang=target_lang,
                        output_file=str(target_full_path),
                        dify_api_key=self.api_key
                    )

                    if success:
                        results["translated"].append(f"{target_path} (openapi)")
                    else:
                        results["failed"].append(target_path)
                except Exception as e:
                    print(f"❌ Error translating OpenAPI {file_path}: {e}")
                    results["failed"].append(target_path)

    def sync_docs_json_structure(
        self,
        synchronizer: DocsSynchronizer,
        added_files: List[str],
        base_sha: str,
        head_sha: str
    ) -> None:
        """Sync docs.json navigation structure."""
        print("Syncing docs.json structure...")

        # Get deleted files
        deleted_files = []
        try:
            result = self.run_git(
                "diff", "--name-status", "--diff-filter=D",
                base_sha, head_sha
            )

            for line in result.stdout.strip().split('\n'):
                if line and line.startswith('D\t'):
                    file_path = line.split('\t')[1]
                    if file_path.startswith(f"{self.source_dir}/"):
                        deleted_files.append(file_path)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not get deleted files: {e}")

        # Delete corresponding translation files
        if deleted_files:
            print(f"Deleting {len(deleted_files)} translation files...")
            for source_file in deleted_files:
                for target_lang in self.target_languages:
                    target_dir = self.translation_config["languages"][target_lang]["directory"]
                    target_file = source_file.replace(f"{self.source_dir}/", f"{target_dir}/")
                    target_path = self.repo_root / target_file

                    if target_path.exists():
                        target_path.unlink()
                        print(f"✓ Deleted {target_file}")

                        # Remove empty parent directories
                        parent = target_path.parent
                        while parent != self.repo_root:
                            try:
                                if not any(parent.iterdir()):
                                    parent.rmdir()
                                    print(f"✓ Removed empty directory {parent.relative_to(self.repo_root)}")
                                    parent = parent.parent
                                else:
                                    break
                            except (OSError, ValueError):
                                break

        # Sync docs.json incrementally
        sync_log = synchronizer.sync_docs_json_incremental(
            added_files=added_files,
            deleted_files=deleted_files
        )
        print("\n".join(sync_log))

    def remove_english_files(self) -> None:
        """Remove English source files from working directory before commit."""
        print("Removing English source files from working directory...")

        # Remove markdown and MDX files from English directory
        en_dir = self.repo_root / self.source_dir
        for pattern in ["*.md", "*.mdx"]:
            for file_path in en_dir.glob(f"**/{pattern}"):
                try:
                    file_path.unlink()
                    print(f"  Removed {file_path.relative_to(self.repo_root)}")
                except Exception as e:
                    print(f"  Warning: Could not remove {file_path}: {e}")

        # Unstage any English files that might have been staged
        self.run_git("reset", "HEAD", "--", f"{self.source_dir}/", check=False)

        print("✓ English source files removed")

    def commit_changes(self, branch_exists: bool) -> bool:
        """Commit translation changes."""
        # Setup git identity
        self.run_git("config", "user.name", "github-actions[bot]")
        self.run_git("config", "user.email", "github-actions[bot]@users.noreply.github.com")

        # Checkout translation branch again (in case we're in detached state)
        if branch_exists:
            self.run_git("fetch", "origin", self.sync_branch)
            # Try to checkout and merge remote changes instead of discarding them
            try:
                self.run_git("checkout", self.sync_branch)
                # Attempt fast-forward merge with remote
                merge_result = self.run_git("merge", f"origin/{self.sync_branch}", "--ff-only", check=False)
                if merge_result.returncode != 0:
                    print("⚠️  Cannot fast-forward merge. Translation branch has diverged.")
                    print("   This may indicate concurrent workflow runs or manual modifications.")
                    raise RuntimeError("Translation branch has diverged - concurrent modification detected")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error checking out translation branch: {e}")
                raise
        else:
            # Branch was already created in setup_translation_branch(), just checkout
            self.run_git("checkout", self.sync_branch)

        # Remove English files before staging
        self.remove_english_files()

        # Stage only translation files
        target_dirs = [self.translation_config["languages"][lang]["directory"]
                      for lang in self.target_languages]
        stage_paths = target_dirs + ["docs.json"]

        for path in stage_paths:
            self.run_git("add", path, check=False)

        # Check if there are changes to commit
        status_result = self.run_git("status", "--porcelain")
        if not status_result.stdout.strip():
            print("ℹ️  No changes to commit")
            return False

        # Create commit message
        if branch_exists:
            commit_msg = f"""🔄 Update translations for commit {self.head_sha[:8]}

Auto-generated translations for changes in commit {self.head_sha}.

Last-Processed-Commit: {self.head_sha}
Original-PR: #{self.pr_number}
Languages: Chinese (cn), Japanese (jp)

🤖 Generated with GitHub Actions"""
        else:
            commit_msg = f"""🌐 Initial translations for PR #{self.pr_number}

Auto-generated translations for documentation changes in PR #{self.pr_number}.

Last-Processed-Commit: {self.head_sha}
Original-PR: #{self.pr_number}
Languages: Chinese (cn), Japanese (jp)

🤖 Generated with GitHub Actions"""

        self.run_git("commit", "-m", commit_msg)
        print(f"✓ Committed changes to {self.sync_branch}")

        return True

    def push_changes(self) -> None:
        """Push changes to remote translation branch."""
        # Use --force-with-lease for safety - allows push only if remote hasn't changed
        # since we last fetched. This prevents accidental overwrites while being safer than --force.
        self.run_git("push", "--force-with-lease", "origin", self.sync_branch)
        print(f"✓ Pushed changes to origin/{self.sync_branch}")

    def create_or_update_pr(self, branch_exists: bool) -> Dict:
        """Create new translation PR or update existing one."""
        if not branch_exists:
            # Create new PR
            print("Creating new translation PR...")

            pr_body = f"""# 🌐 Auto-generated Translations

This PR contains automatically generated translations for the documentation changes in PR #{self.pr_number}.

## Original PR
**Title:** {self.pr_title}
**Link:** #{self.pr_number}

## What's included
- 🇨🇳 Chinese (cn) translations
- 🇯🇵 Japanese (jp) translations
- 📋 Updated navigation structure in docs.json

## Review Process
1. Review the generated translations for accuracy
2. Make any necessary adjustments
3. Merge this PR to apply the translations

## Links
- **Original English PR:** #{self.pr_number}
- **Translation branch:** `{self.sync_branch}`

---
🤖 This PR was created automatically by the documentation translation workflow."""

            result = self.run_gh(
                "pr", "create",
                "--base", "main",
                "--head", self.sync_branch,
                "--title", f"🌐 Auto-translations for PR #{self.pr_number}: {self.pr_title}",
                "--body", pr_body
            )

            pr_url = result.stdout.strip()
            pr_number = pr_url.split('/')[-1] if pr_url else None

            print(f"✅ Created translation PR: {pr_url}")

            return {
                "translation_pr_number": pr_number,
                "translation_pr_url": pr_url,
                "created": True
            }
        else:
            # Update existing PR with comment
            print("Finding existing translation PR...")

            result = self.run_gh(
                "pr", "list",
                "--search", f"head:{self.sync_branch}",
                "--json", "number",
                "--jq", ".[0].number",
                check=False
            )

            pr_number = result.stdout.strip()
            if not pr_number:
                print("⚠️  Could not find existing translation PR")
                return {
                    "created": False,
                    "translation_pr_number": None,
                    "translation_pr_url": None
                }

            # Add tracking comment
            comment = f"""<!-- Last-Processed-Commit: {self.head_sha} -->
🔄 **Updated for commit `{self.head_sha[:8]}`**

Latest source changes from PR #{self.pr_number} have been translated and committed.

**Source commit:** [`{self.head_sha[:8]}`](https://github.com/{self.repo_name}/commit/{self.head_sha})
**Original PR:** #{self.pr_number}"""

            self.run_gh("pr", "comment", pr_number, "--body", comment, check=False)

            pr_url = f"https://github.com/{self.repo_name}/pull/{pr_number}"

            print(f"✅ Updated translation PR #{pr_number}")

            return {
                "translation_pr_number": pr_number,
                "translation_pr_url": pr_url,
                "created": False
            }

    async def run(self) -> Dict:
        """Run the complete translation PR workflow."""
        try:
            # Check if branch exists
            branch_exists = self.check_branch_exists()
            print(f"Translation branch exists: {branch_exists}")

            # Setup translation branch
            self.setup_translation_branch(branch_exists)

            # Run translation
            translation_results = await self.run_translation()

            if translation_results["failed"]:
                print(f"⚠️  Some translations failed: {translation_results['failed']}")

            # Commit changes
            has_changes = self.commit_changes(branch_exists)

            if not has_changes:
                return {
                    "success": True,
                    "has_changes": False,
                    "translation_results": translation_results
                }

            # Push changes
            self.push_changes()

            # Create or update PR
            pr_info = self.create_or_update_pr(branch_exists)

            return {
                "success": True,
                "has_changes": True,
                "translation_results": translation_results,
                **pr_info
            }

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }


def main():
    parser = argparse.ArgumentParser(
        description="Translate and commit documentation changes to a translation PR"
    )
    parser.add_argument("--pr-number", type=int, required=True, help="Source PR number")
    parser.add_argument("--head-sha", required=True, help="HEAD commit SHA")
    parser.add_argument("--base-sha", required=True, help="Base commit SHA for comparison")
    parser.add_argument("--is-incremental", action="store_true", help="Whether this is an incremental update")
    parser.add_argument("--pr-title", help="Source PR title")
    parser.add_argument("--work-dir", default="/tmp", help="Working directory for artifacts")
    parser.add_argument("--api-key", help="Dify API key (defaults to DIFY_API_KEY env var)")

    args = parser.parse_args()

    manager = TranslationPRManager(
        pr_number=args.pr_number,
        head_sha=args.head_sha,
        base_sha=args.base_sha,
        is_incremental=args.is_incremental,
        pr_title=args.pr_title,
        work_dir=args.work_dir,
        api_key=args.api_key
    )

    result = asyncio.run(manager.run())

    # Output result as JSON for workflow parsing
    print("\n" + "="*80)
    print("RESULT_JSON:")
    print(json.dumps(result, indent=2))
    print("="*80)

    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
