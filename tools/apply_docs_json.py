import json
import os
from pathlib import Path
from collections import defaultdict

# --- Script Base Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

# --- Configuration ---
refresh = False  # Flag to control whether to clear existing dropdowns before processing
DOCS_JSON_PATH = BASE_DIR / "docs.json"  # Path to the main documentation structure JSON file

# --- Sync Configurations ---
# Define which dropdowns to sync between languages for each version
# Skip "Develop" dropdown as requested
SYNC_CONFIGS = [
    {
        "VERSION_CODE": "Latest",
        "BASE_PATHS": {
            "en": "en",
            "cn": "cn",
            "ja": "jp"
        },
        "DROPDOWNS_TO_SYNC": [
            {
                "en": {"name": "Documentation", "path": "documentation"},
                "cn": {"name": "文档", "path": "documentation"},
                "ja": {"name": "ドキュメント", "path": "documentation"}
            },
            {
                "en": {"name": "Self Hosting", "path": "self-hosting"},
                "cn": {"name": "自托管", "path": "self-hosting"},
                "ja": {"name": "セルフホスティング", "path": "self-hosting"}
            },
            {
                "en": {"name": "API Reference", "path": "api-reference", "type": "openapi"},
                "cn": {"name": "访问 API", "path": "", "type": "openapi"},
                "ja": {"name": "APIアクセス", "path": "", "type": "openapi"}
            }
        ]
    },
    {
        "VERSION_CODE": "3.3.x (Enterprise)",
        "BASE_PATHS": {
            "en": "versions/3-3-x/en",
            "cn": "versions/3-3-x/cn",
            "ja": "versions/3-3-x/jp"
        },
        "DROPDOWNS_TO_SYNC": []  # Add dropdowns for this version if needed
    },
    {
        "VERSION_CODE": "3.2.x (Enterprise)",
        "BASE_PATHS": {
            "en": "versions/3-2-x/en",
            "cn": "versions/3-2-x/cn",
            "ja": "versions/3-2-x/jp"
        },
        "DROPDOWNS_TO_SYNC": []  # Add dropdowns for this version if needed
    },
    {
        "VERSION_CODE": "3.0.x (Enterprise)",
        "BASE_PATHS": {
            "en": "versions/3-0-x/en",
            "cn": "versions/3-0-x/cn",
            "ja": "versions/3-0-x/jp"
        },
        "DROPDOWNS_TO_SYNC": []  # Add dropdowns for this version if needed
    }
]

# --- Helper Functions ---

CRITICAL_ISSUE_TYPES = {"Error", "Critical", "ConfigError", "SeriousWarning", "InternalError"}

def _log_issue(reports_list_for_commit_message: list, context: str, issue_type: str, message: str, details: str = ""):
    """
    Logs a detailed message to the console and adds a concise version to a list for commit messages
    if the issue_type is critical.
    """
    full_log_message = f"[{issue_type.upper()}] {context}: {message}"
    if details:
        full_log_message += f" Details: {details}"
    print(full_log_message)

    if issue_type in CRITICAL_ISSUE_TYPES:
        commit_msg_part = f"- {context}: [{issue_type}] {message}"
        reports_list_for_commit_message.append(commit_msg_part)


def load_docs_data_robust(path: Path, commit_message_reports_list: list) -> dict:
    """Load docs.json with error handling"""
    default_structure = {"navigation": {"versions": []}}
    try:
        if not path.exists():
            _log_issue(commit_message_reports_list, "GLOBAL", "Info", f"File '{path}' not found. Initializing with default structure.")
            return default_structure
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or \
               "navigation" not in data or not isinstance(data["navigation"], dict) or \
               "versions" not in data["navigation"] or not isinstance(data["navigation"]["versions"], list):
                _log_issue(commit_message_reports_list, "GLOBAL", "Error", f"Invalid structure in '{path}'. Using default.")
                return default_structure
            return data
    except json.JSONDecodeError as e:
        _log_issue(commit_message_reports_list, "GLOBAL", "Error", f"Failed to parse JSON: {e}")
        return default_structure
    except Exception as e:
        _log_issue(commit_message_reports_list, "GLOBAL", "Critical", f"Unexpected error: {e}")
        return default_structure


def save_docs_data_robust(path: Path, data: dict, commit_message_reports_list: list) -> bool:
    """Save docs.json with error handling"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        _log_issue(commit_message_reports_list, "GLOBAL", "Info", f"Successfully saved to '{path}'.")
        return True
    except Exception as e:
        _log_issue(commit_message_reports_list, "GLOBAL", "Critical", f"Failed to save: {e}")
        return False


def find_or_create_version(navigation_data: dict, version_code: str, commit_reports: list) -> dict:
    """Find or create a version in the navigation structure"""
    navigation_data.setdefault("versions", [])

    for version in navigation_data["versions"]:
        if version.get("version") == version_code:
            return version

    # Create new version
    new_version = {"version": version_code, "languages": []}
    navigation_data["versions"].append(new_version)
    _log_issue(commit_reports, version_code, "Info", f"Created new version '{version_code}'")
    return new_version


def find_or_create_language(version_data: dict, lang_code: str, commit_reports: list) -> dict:
    """Find or create a language in the version structure"""
    version_data.setdefault("languages", [])

    for language in version_data["languages"]:
        if language.get("language") == lang_code:
            return language

    # Create new language
    new_language = {"language": lang_code, "dropdowns": []}
    version_data["languages"].append(new_language)
    _log_issue(commit_reports, f"{version_data.get('version')}/{lang_code}", "Info", f"Created new language '{lang_code}'")
    return new_language


def find_or_create_dropdown(language_data: dict, dropdown_name: str, commit_reports: list) -> dict:
    """Find or create a dropdown in the language structure"""
    language_data.setdefault("dropdowns", [])

    for dropdown in language_data["dropdowns"]:
        if dropdown.get("dropdown") == dropdown_name:
            return dropdown

    # Create new dropdown
    new_dropdown = {"dropdown": dropdown_name}
    language_data["dropdowns"].append(new_dropdown)
    context = f"{language_data.get('language')}/{dropdown_name}"
    _log_issue(commit_reports, context, "Info", f"Created new dropdown '{dropdown_name}'")
    return new_dropdown


def extract_pages_from_structure(item, visited=None):
    """Recursively extract all page paths from a dropdown/group structure"""
    if visited is None:
        visited = set()

    # Avoid infinite recursion by tracking visited items
    item_id = id(item)
    if item_id in visited:
        return set()
    visited.add(item_id)

    pages = set()

    if isinstance(item, str):
        pages.add(item)
    elif isinstance(item, dict):
        # Handle 'pages' list
        if "pages" in item and isinstance(item["pages"], list):
            for page in item["pages"]:
                pages.update(extract_pages_from_structure(page, visited))
        # Handle 'groups' list
        if "groups" in item and isinstance(item["groups"], list):
            for group in item["groups"]:
                pages.update(extract_pages_from_structure(group, visited))
    elif isinstance(item, list):
        for sub_item in item:
            pages.update(extract_pages_from_structure(sub_item, visited))

    return pages


def discover_files_in_directory(base_path: Path, dropdown_path: str) -> set:
    """Discover all .mdx files in a directory and return their relative paths"""
    files = set()
    full_path = base_path / dropdown_path if dropdown_path else base_path

    if not full_path.exists():
        return files

    for mdx_file in full_path.rglob("*.mdx"):
        # Get relative path from base directory
        rel_path = mdx_file.relative_to(BASE_DIR)
        # Remove .mdx extension for the page path
        page_path = str(rel_path)[:-4]
        files.add(page_path)

    return files


def sync_dropdown_between_languages(
    version_config: dict,
    dropdown_config: dict,
    navigation_data: dict,
    commit_reports: list
):
    """Sync a specific dropdown between languages for a version"""
    version_code = version_config["VERSION_CODE"]
    base_paths = version_config["BASE_PATHS"]

    # Get English dropdown structure as source of truth
    version_nav = find_or_create_version(navigation_data, version_code, commit_reports)
    en_lang = find_or_create_language(version_nav, "en", commit_reports)
    en_dropdown_name = dropdown_config["en"]["name"]
    en_dropdown = None

    for dropdown in en_lang.get("dropdowns", []):
        if dropdown.get("dropdown") == en_dropdown_name:
            en_dropdown = dropdown
            break

    if not en_dropdown:
        _log_issue(commit_reports, f"{version_code}/en", "Warning",
                  f"English dropdown '{en_dropdown_name}' not found, skipping sync")
        return

    # Extract pages from English structure
    en_pages = extract_pages_from_structure(en_dropdown)

    # Skip if this is an OpenAPI type (handled differently)
    if dropdown_config["en"].get("type") == "openapi":
        _log_issue(commit_reports, f"{version_code}", "Info",
                  f"Skipping OpenAPI dropdown '{en_dropdown_name}'")
        return

    # Sync to other languages
    for lang_code in ["cn", "ja"]:
        if lang_code not in dropdown_config:
            continue

        lang_config = dropdown_config[lang_code]
        lang_dropdown_name = lang_config["name"]

        # Find or create language and dropdown
        lang_nav = find_or_create_language(version_nav, lang_code, commit_reports)
        lang_dropdown = find_or_create_dropdown(lang_nav, lang_dropdown_name, commit_reports)

        # For now, copy the entire structure from English and adjust paths
        # This ensures the navigation structure matches
        copy_dropdown_structure(en_dropdown, lang_dropdown, "en", lang_code, base_paths)

        _log_issue(commit_reports, f"{version_code}/{lang_code}/{lang_dropdown_name}",
                  "Info", f"Synced dropdown structure from English")


def copy_dropdown_structure(source_dropdown: dict, target_dropdown: dict,
                           source_lang: str, target_lang: str,
                           base_paths: dict):
    """Copy the structure from source dropdown to target, adjusting paths"""

    def adjust_path(path: str) -> str:
        """Adjust a page path from source language to target language"""
        # Replace source language path with target language path
        if path.startswith(f"{source_lang}/"):
            return path.replace(f"{source_lang}/", f"{base_paths[target_lang]}/", 1)
        elif path.startswith(base_paths[source_lang]):
            return path.replace(base_paths[source_lang], base_paths[target_lang], 1)
        return path

    def copy_structure(source_item):
        """Recursively copy and adjust structure"""
        if isinstance(source_item, str):
            return adjust_path(source_item)
        elif isinstance(source_item, dict):
            result = {}
            for key, value in source_item.items():
                if key in ["pages", "groups"]:
                    result[key] = [copy_structure(item) for item in value]
                elif key == "group" or key == "dropdown" or key == "tab":
                    result[key] = value  # Keep group names as is
                elif key == "icon":
                    result[key] = value  # Keep icons
                else:
                    result[key] = copy_structure(value)
            return result
        elif isinstance(source_item, list):
            return [copy_structure(item) for item in source_item]
        return source_item

    # Copy all keys from source to target, adjusting paths
    for key, value in source_dropdown.items():
        if key == "dropdown":
            continue  # Keep target dropdown name
        target_dropdown[key] = copy_structure(value)


def process_all_configs(configs: list, docs_json_path: Path) -> list[str]:
    """Process all sync configurations"""
    commit_reports = []

    # Load existing docs.json
    docs_data = load_docs_data_robust(docs_json_path, commit_reports)
    navigation_data = docs_data.setdefault("navigation", {})

    # Process each version configuration
    for version_config in configs:
        version_code = version_config["VERSION_CODE"]
        _log_issue(commit_reports, version_code, "Info", f"Processing version '{version_code}'")

        # Skip if no dropdowns to sync
        if not version_config.get("DROPDOWNS_TO_SYNC"):
            _log_issue(commit_reports, version_code, "Info", "No dropdowns configured for sync")
            continue

        # Sync each configured dropdown
        for dropdown_config in version_config["DROPDOWNS_TO_SYNC"]:
            sync_dropdown_between_languages(
                version_config,
                dropdown_config,
                navigation_data,
                commit_reports
            )

    # Save updated docs.json
    save_docs_data_robust(docs_json_path, docs_data, commit_reports)

    return commit_reports


def main_apply_docs_json() -> str:
    """Main function to sync documentation structure"""
    print(f"Script base directory: {BASE_DIR}")
    print(f"Docs JSON path: {DOCS_JSON_PATH}")
    print(f"Refresh mode: {refresh}")

    commit_message_parts = process_all_configs(SYNC_CONFIGS, DOCS_JSON_PATH)

    if not commit_message_parts:
        return "Documentation sync completed successfully"
    else:
        num_critical_issues = len([p for p in commit_message_parts if any(t in p for t in CRITICAL_ISSUE_TYPES)])
        if num_critical_issues > 0:
            return f"Documentation sync completed with {num_critical_issues} critical issue(s)"
        return "Documentation sync completed with warnings"


if __name__ == "__main__":
    result_message = main_apply_docs_json()
    print("\n--- Script Execution Result ---")
    print(result_message)