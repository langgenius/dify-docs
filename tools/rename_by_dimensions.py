import os
import yaml # pip install pyyaml
import re
import datetime
from pathlib import Path
import shutil

class Config:
    # --- Path Setup ---
    BASE_DIR = Path(__file__).resolve().parent.parent
    LANGUAGES = ["zh", "en", "ja"]  # Languages to process
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Directory Naming Templates ---
    # Original directory for a language, e.g., "plugin_dev_zh"
    # This will be renamed to become the source for processing.
    ORIGINAL_LANG_DIR_TEMPLATE = "plugin_dev_{lang}"

    # Name template for the source directory after renaming the original.
    # e.g., "plugin_dev_zh_20231027_103000"
    SOURCE_DIR_FROM_ORIGINAL_TEMPLATE = "plugin_dev_{lang}_{timestamp}"

    # Name template for an empty source if the original lang dir doesn't exist.
    # e.g., "plugin_dev_zh_empty_source_20231027_103000"
    EMPTY_SOURCE_DIR_TEMPLATE = "plugin_dev_{lang}_empty_source_{timestamp}"

    # Name template for the final output directory (will be newly created).
    # e.g., "plugin_dev_zh"
    TARGET_DIR_TEMPLATE = "plugin_dev_{lang}"

    # Prefix for archiving the TARGET_DIR if it unexpectedly exists before creation.
    # e.g., "plugin_dev_zh_processed_archive_"
    # Note: TARGET_DIR should ideally be empty or non-existent after source dir renaming.
    # This archive is a safety net.
    ARCHIVE_TARGET_PREFIX_TEMPLATE = "plugin_dev_{lang}_archive_"

    # --- PWXY Mappings ---
    PRIMARY_TYPE_MAP = {
        "conceptual": 1,
        "implementation": 2,
        "operational": 3,
        "reference": 4,
    }
    DEFAULT_W = 0
    DETAIL_TYPE_MAPS = {
        "conceptual": {"introduction": 1, "principles": 2, "architecture": 3},
        "implementation": {"basic": 1, "standard": 2, "high": 3, "advanced": 4},
        "operational": {"setup": 1, "deployment": 2, "maintenance": 3},
        "reference": {"core": 1, "configuration": 2, "examples": 3},
    }
    DEFAULT_X = 0
    LEVEL_MAP = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
    }
    DEFAULT_Y = 0
    PRIORITY_NORMAL = 0
    PRIORITY_HIGH = 9
    PRIORITY_ADVANCED_LEVEL_KEY = "advanced"
    PRIORITY_IMPLEMENTATION_PRIMARY_KEY = "implementation"
    PRIORITY_IMPLEMENTATION_DETAIL_KEYS = {"high", "advanced"}

# --- Helper Functions ---

def extract_front_matter(content: str):
    match = re.match(r"^\s*---\s*$(.*?)^---\s*$(.*)", content, re.DOTALL | re.MULTILINE)
    if match:
        yaml_str = match.group(1).strip()
        markdown_content = match.group(2).strip()
        try:
            front_matter = yaml.safe_load(yaml_str)
            if front_matter is None: # Handles empty YAML (--- \n ---)
                return {}, markdown_content
            return (
                front_matter if isinstance(front_matter, dict) else {}
            ), markdown_content
        except yaml.YAMLError as e:
            print(f"  [Error] YAML Parsing Failed: {e}")
            return None, content # Indicate error
    else:
        return {}, content # No front matter found

def sanitize_filename_part(part: str) -> str:
    if not isinstance(part, str):
        part = str(part)
    part = part.lower()
    part = part.replace("&", "and").replace("@", "at")
    part = re.sub(r"\s+", "-", part)
    part = re.sub(r"[^\w\-]+", "", part)
    part = part.strip(".-_")
    return part or "untitled"

def _calculate_pwxy_and_warnings(front_matter: dict, config: Config) -> tuple[int, int, int, int, list[str]]:
    """Calculates P, W, X, Y values and generates warnings for missing/unmapped data."""
    warnings_messages = []
    dimensions = front_matter.get("dimensions", {})
    type_info = dimensions.get("type", {})
    primary = type_info.get("primary")
    detail = type_info.get("detail")
    level = dimensions.get("level")

    P = config.PRIORITY_NORMAL
    if level == config.PRIORITY_ADVANCED_LEVEL_KEY:
        P = config.PRIORITY_HIGH
    if (
        primary == config.PRIORITY_IMPLEMENTATION_PRIMARY_KEY
        and detail in config.PRIORITY_IMPLEMENTATION_DETAIL_KEYS
    ):
        P = config.PRIORITY_HIGH

    W = config.PRIMARY_TYPE_MAP.get(primary, config.DEFAULT_W)
    primary_detail_map = config.DETAIL_TYPE_MAPS.get(primary, {})
    X = primary_detail_map.get(detail, config.DEFAULT_X)
    Y = config.LEVEL_MAP.get(level, config.DEFAULT_Y)

    if primary is None:
        warnings_messages.append("Missing dimensions.type.primary")
    elif W == config.DEFAULT_W:
        warnings_messages.append(f"Unmapped primary type: '{primary}'. Using W={config.DEFAULT_W}")
    if detail is None:
        warnings_messages.append("Missing dimensions.type.detail")
    elif X == config.DEFAULT_X and primary in config.DETAIL_TYPE_MAPS:
        warnings_messages.append(f"Unmapped detail type: '{detail}' for primary '{primary}'. Using X={config.DEFAULT_X}")
    elif primary not in config.DETAIL_TYPE_MAPS and primary is not None:
        warnings_messages.append(f"No detail map defined for primary type: '{primary}'. Using X={config.DEFAULT_X}")
    if level is None:
        warnings_messages.append("Missing dimensions.level")
    elif Y == config.DEFAULT_Y:
        warnings_messages.append(f"Unmapped level: '{level}'. Using Y={config.DEFAULT_Y}")

    return P, W, X, Y, warnings_messages

def _generate_filename_parts(
    P: int, W: int, X: int, Y: int,
    front_matter: dict,
    original_filename_stem: str
) -> tuple[str | None, str, str, list[str]]:
    """Generates padded prefix, sanitized title, language suffix, and any warnings."""
    warnings_messages = []

    # Padded Prefix
    prefix_str = f"{P}{W}{X}{Y}"
    try:
        numeric_prefix = int(prefix_str)
        padded_prefix = f"{numeric_prefix:04d}"
    except ValueError:
        # This case should ideally not happen if P,W,X,Y are always numeric
        warnings_messages.append(f"Could not form numeric prefix from P={P},W={W},X={X},Y={Y}. Using '0000'.")
        padded_prefix = "0000" # Fallback, but indicates an issue

    # Sanitized Title
    standard_title = front_matter.get("standard_title")
    title_part_to_use = standard_title
    if not title_part_to_use:
        warnings_messages.append("Missing 'standard_title'. Using original filename stem as fallback.")
        title_part_to_use = original_filename_stem
    sanitized_title = sanitize_filename_part(title_part_to_use)

    # Language Suffix
    lang_suffix = ""
    language_fm = front_matter.get("language") # Language from frontmatter
    if language_fm:
        lang_code = str(language_fm).strip().lower()
        if lang_code:
            lang_suffix = f".{lang_code}"
        else:
            warnings_messages.append("Empty 'language' field in frontmatter. Omitting language suffix.")
    else:
        warnings_messages.append("Missing 'language' field in frontmatter. Omitting language suffix.")

    return padded_prefix, sanitized_title, lang_suffix, warnings_messages

# --- Core Processing Functions ---

def setup_paths_for_lang(lang: str, config: Config) -> tuple[Path | None, Path | None]:
    """
    Sets up source and target paths for a given language.
    Renames original lang_dir to be the source_dir for processing.
    Returns (source_dir_path, target_dir_path) or (None, None) on critical error.
    """
    original_lang_dir_name = config.ORIGINAL_LANG_DIR_TEMPLATE.format(lang=lang)
    original_lang_dir_path = config.BASE_DIR / original_lang_dir_name

    target_dir_name = config.TARGET_DIR_TEMPLATE.format(lang=lang)
    target_dir_path = config.BASE_DIR / target_dir_name

    source_dir_path: Path
    source_dir_created_empty = False

    if original_lang_dir_path.exists():
        if not original_lang_dir_path.is_dir():
            print(f"[ERROR] Path '{original_lang_dir_path}' exists but is not a directory. Skipping language '{lang}'.")
            return None, None

        source_dir_name = config.SOURCE_DIR_FROM_ORIGINAL_TEMPLATE.format(lang=lang, timestamp=config.TIMESTAMP)
        source_dir_path = config.BASE_DIR / source_dir_name
        try:
            # Ensure no conflict if a previous timestamped dir exists (unlikely but possible)
            if source_dir_path.exists():
                 print(f"[WARNING] Timestamped source dir '{source_dir_path}' already exists. This might be from a rapid re-run or manual creation. Trying to use it.")
            else:
                 original_lang_dir_path.rename(source_dir_path)
            print(f"Using '{source_dir_path}' (renamed from '{original_lang_dir_path}') as source for '{lang}'.")
        except OSError as e:
            print(f"[ERROR] Failed to rename '{original_lang_dir_path}' to '{source_dir_path}': {e}. Skipping language '{lang}'.")
            return None, None
    else:
        print(f"Warning: Original directory '{original_lang_dir_path}' not found for language '{lang}'.")
        source_dir_name = config.EMPTY_SOURCE_DIR_TEMPLATE.format(lang=lang, timestamp=config.TIMESTAMP)
        source_dir_path = config.BASE_DIR / source_dir_name
        source_dir_path.mkdir(parents=True, exist_ok=True)
        source_dir_created_empty = True
        print(f"Created empty source directory: '{source_dir_path}' for '{lang}'.")

    return source_dir_path, target_dir_path, source_dir_created_empty, source_dir_name


def archive_and_create_target_dir(target_dir_path: Path, archive_prefix: str, timestamp: str) -> bool:
    """
    Archives the target directory if it exists, then creates a new empty target directory.
    Returns True on success, False on failure.
    """
    if target_dir_path.exists():
        if target_dir_path.is_dir():
            archive_dir_name = f"{archive_prefix}{timestamp}"
            archive_dir_path = target_dir_path.parent / archive_dir_name
            try:
                # shutil.move is more robust for renaming across different filesystems (though unlikely here)
                # and can overwrite if archive_dir_path somehow exists (very unlikely)
                if archive_dir_path.exists():
                    print(f"  [Warning] Archive destination '{archive_dir_path}' already exists. Removing it first.")
                    shutil.rmtree(archive_dir_path) # Or handle differently
                shutil.move(str(target_dir_path), str(archive_dir_path))
                print(f"  Archived existing target directory to: {archive_dir_path}")
            except OSError as e:
                print(f"  [Error] Failed to archive existing target dir '{target_dir_path}': {e}")
                print("  Aborting for this language to prevent data loss.")
                return False
        else:
            print(f"  [Error] Target path '{target_dir_path}' exists but is not a file/directory. Please remove/rename manually.")
            print("  Aborting for this language.")
            return False
    try:
        target_dir_path.mkdir(parents=True, exist_ok=False) # Should not exist now
        print(f"  Created new target directory: {target_dir_path}")
        return True
    except OSError as e:
        print(f"  [Error] Failed to create target directory '{target_dir_path}': {e}")
        print("  Aborting for this language.")
        return False


def process_single_mdx_file(
    mdx_filepath: Path,
    target_dir: Path,
    config: Config
) -> dict:
    """
    Processes a single MDX file: extracts metadata for new filename,
    and copies the original file content to the new location.
    Returns stats.
    """
    stats = {"status": "processed", "warnings": [], "error_message": None}
    relative_path = mdx_filepath.relative_to(config.BASE_DIR).as_posix()
    file_warnings = []

    try:
        content = mdx_filepath.read_text(encoding="utf-8")
        front_matter, _ = extract_front_matter(content) # markdown_content not needed for re-writing

        if front_matter is None: # YAML parsing error from extract_front_matter
            stats["status"] = "error"
            stats["error_message"] = "YAML Error in file."
            print(f"\nProcessing: {relative_path}")
            print(f"  [Skipping] {stats['error_message']}")
            return stats

        # Calculate PWXY and related warnings
        P, W, X, Y, pwxy_warnings = _calculate_pwxy_and_warnings(front_matter, config)
        file_warnings.extend(pwxy_warnings)

        # Generate filename parts and related warnings
        padded_prefix, sanitized_title, lang_suffix, fname_warnings = _generate_filename_parts(
            P, W, X, Y, front_matter, mdx_filepath.stem
        )
        file_warnings.extend(fname_warnings)

        if padded_prefix is None: # Critical error in prefix generation
             stats["status"] = "error"
             stats["error_message"] = "Could not form numeric prefix."
             print(f"\nProcessing: {relative_path}")
             print(f"  [Error] {stats['error_message']} P={P},W={W},X={X},Y={Y}. Skipping.")
             return stats

        new_filename = f"{padded_prefix}-{sanitized_title}{lang_suffix}.mdx"
        target_filepath = target_dir / new_filename

        if target_filepath.exists():
            stats["status"] = "skipped_exists"
            print(f"\nProcessing: {relative_path}")
            print(f"  [Skipping] Target file already exists: {new_filename}")
            return stats

        # Copy original file instead of rewriting content
        try:
            shutil.copy2(mdx_filepath, target_filepath) # copy2 preserves metadata
        except Exception as copy_error:
            stats["status"] = "error"
            stats["error_message"] = f"Failed to copy file: {copy_error}"
            print(f"\nProcessing: {relative_path}")
            print(f"  [Error] {stats['error_message']}")
            return stats

        stats["warnings"] = file_warnings
        if file_warnings:
            print(f"\nProcessing: {relative_path} -> {new_filename}")
            for warning_msg in file_warnings:
                print(f"  [Warning] {warning_msg}")
        # No print needed for successful processing without warnings unless verbose mode

    except FileNotFoundError:
        stats["status"] = "error"
        stats["error_message"] = f"File not found during processing: {mdx_filepath}"
        print(f"\nProcessing: {relative_path}")
        print(f"  [Error] {stats['error_message']}")
    except Exception as e:
        stats["status"] = "error"
        stats["error_message"] = f"Unexpected error: {e}"
        print(f"\nProcessing: {relative_path}")
        print(f"  [Error] Unexpected error processing file: {e}")
        import traceback
        traceback.print_exc()
    return stats


def run_processing_for_language(
    source_dir: Path,
    target_dir: Path,
    archive_prefix: str,
    config: Config
) -> dict:
    """Processes all MDX files in the source_dir and outputs them to target_dir."""
    print(f"Starting processing for source: {source_dir}")
    print(f"Target directory: {target_dir}")

    lang_stats = {
        "processed_count": 0,
        "skipped_count": 0,
        "error_count": 0,
        "warning_files_count": 0, # Files with at least one warning
        "status": "OK"
    }

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"[Error] Source directory '{source_dir}' does not exist or is not a directory.")
        lang_stats["status"] = "SOURCE_DIR_ERROR"
        return lang_stats

    # Archive existing target directory (if any) and create a new one
    if not archive_and_create_target_dir(target_dir, archive_prefix, config.TIMESTAMP):
        lang_stats["status"] = "TARGET_DIR_SETUP_ERROR"
        return lang_stats # Abort if target dir setup fails

    mdx_files = list(source_dir.rglob("*.mdx"))
    total_files = len(mdx_files)
    print(f"Found {total_files} MDX files to process in '{source_dir}'.")

    if not mdx_files and source_dir.name.startswith(config.ORIGINAL_LANG_DIR_TEMPLATE.format(lang="")[:-1]): # Heuristic check if it was an original dir
        pass # It's fine for an original directory to be empty.

    for i, mdx_filepath in enumerate(mdx_files):
        result = process_single_mdx_file(mdx_filepath, target_dir, config)

        if result["status"] == "processed":
            lang_stats["processed_count"] += 1
            if result["warnings"]:
                lang_stats["warning_files_count"] +=1
        elif result["status"] == "skipped_exists":
            lang_stats["skipped_count"] += 1
        elif result["status"] == "error":
            lang_stats["error_count"] += 1
        
        if (i + 1) % 10 == 0 or (i + 1) == total_files:
            if total_files > 0 : # Avoid division by zero for empty source
                 print(f"Progress: {i+1}/{total_files} files evaluated.", end="\r")

    print("\n" + "-" * 20) # Newline after progress
    print(f"Language Processing Summary ({source_dir.name}):")
    print(f"  Successfully processed: {lang_stats['processed_count']}")
    print(f"  Skipped (target exists): {lang_stats['skipped_count']}")
    print(f"  Files with warnings: {lang_stats['warning_files_count']}")
    print(f"  Errors encountered: {lang_stats['error_count']}")
    print("-" * 20)
    return lang_stats

# --- Main Orchestration ---

def main():
    config = Config()
    print(f"Base directory: {config.BASE_DIR}")
    print(f"Timestamp for this run: {config.TIMESTAMP}")

    overall_summary = {}

    for lang in config.LANGUAGES:
        print(f"\n{'='*10} Processing Language: {lang.upper()} {'='*10}")

        source_dir_path, target_dir_path, source_created_empty, source_actual_name = setup_paths_for_lang(lang, config)

        if not source_dir_path or not target_dir_path:
            overall_summary[lang] = {"status": "SETUP_ERROR", "message": f"Failed to setup paths for {lang}."}
            continue # Skip to next language

        archive_prefix_for_lang = config.ARCHIVE_TARGET_PREFIX_TEMPLATE.format(lang=lang)
        lang_results = run_processing_for_language(source_dir_path, target_dir_path, archive_prefix_for_lang, config)
        overall_summary[lang] = lang_results

        # Clean up empty source directory if it was created for this run
        if source_created_empty:
            try:
                # Check if it's truly empty (no files processed into it by mistake)
                if not any(source_dir_path.iterdir()):
                    source_dir_path.rmdir()
                    print(f"Removed temporary empty source directory: {source_dir_path}")
                else:
                    print(f"Note: Temporary empty source '{source_dir_path}' was not empty. Not removed.")
            except OSError as e:
                print(f"Note: Could not remove temporary empty source directory '{source_dir_path}': {e}")
    
    print("\n\n" + "=" * 20 + " Overall Summary " + "=" * 20)
    for lang, summary in overall_summary.items():
        print(f"\nLanguage: {lang.upper()}")
        if summary.get("status") == "OK":
            print(f"  Status: OK")
            print(f"  Processed: {summary.get('processed_count', 0)}")
            print(f"  Skipped: {summary.get('skipped_count', 0)}")
            print(f"  Files with Warnings: {summary.get('warning_files_count', 0)}")
            print(f"  Errors: {summary.get('error_count', 0)}")
        else:
            print(f"  Status: {summary.get('status', 'UNKNOWN_ERROR')}")
            if "message" in summary:
                print(f"  Message: {summary['message']}")
    print("=" * (40 + len(" Overall Summary ")))


if __name__ == "__main__":
    main()