import yaml  # pip install pyyaml
import re
import datetime
from pathlib import Path
import shutil


class Config:
    # --- Path Setup ---
    BASE_DIR = Path(__file__).resolve().parent.parent
    LANGUAGES = ["zh", "en", "ja"]  # Languages to process
    # Still useful for potential internal archiving if needed
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Directory Naming Templates ---
    # This is the directory we look for, operate within, and is the final name.
    LANG_DIR_TEMPLATE = "plugin_dev_{lang}"

    # Prefix for archiving a LANG_DIR_TEMPLATE if (for some external reason)
    # we wanted to back it up before processing. Not used in the main flow currently
    # but kept as a utility.
    ARCHIVE_LANG_DIR_PREFIX_TEMPLATE = "plugin_dev_{lang}_archive_pre_processing_"

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
    match = re.match(r"^\s*---\s*$(.*?)^---\s*$(.*)",
                     content, re.DOTALL | re.MULTILINE)
    if match:
        yaml_str = match.group(1).strip()
        markdown_content = match.group(2).strip()
        try:
            front_matter = yaml.safe_load(yaml_str)
            if front_matter is None:  # Handles empty YAML (--- \n ---)
                return {}, markdown_content
            return (
                front_matter if isinstance(front_matter, dict) else {}
            ), markdown_content
        except yaml.YAMLError as e:
            print(f"  [Error] YAML Parsing Failed: {e}")
            return None, content  # Indicate error
    else:
        return {}, content  # No front matter found


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
        warnings_messages.append(
            f"Unmapped primary type: '{primary}'. Using W={config.DEFAULT_W}")
    if detail is None:
        warnings_messages.append("Missing dimensions.type.detail")
    elif X == config.DEFAULT_X and primary in config.DETAIL_TYPE_MAPS:
        warnings_messages.append(
            f"Unmapped detail type: '{detail}' for primary '{primary}'. Using X={config.DEFAULT_X}")
    elif primary not in config.DETAIL_TYPE_MAPS and primary is not None:
        warnings_messages.append(
            f"No detail map defined for primary type: '{primary}'. Using X={config.DEFAULT_X}")
    if level is None:
        warnings_messages.append("Missing dimensions.level")
    elif Y == config.DEFAULT_Y:
        warnings_messages.append(
            f"Unmapped level: '{level}'. Using Y={config.DEFAULT_Y}")

    return P, W, X, Y, warnings_messages


def _generate_filename_parts(
    P: int, W: int, X: int, Y: int,
    front_matter: dict,
    original_filename_stem: str
) -> tuple[str | None, str, str, list[str]]:
    """Generates padded prefix, sanitized title, language suffix, and any warnings."""
    warnings_messages = []

    prefix_str = f"{P}{W}{X}{Y}"
    try:
        numeric_prefix = int(prefix_str)
        padded_prefix = f"{numeric_prefix:04d}"
    except ValueError:
        warnings_messages.append(
            f"Could not form numeric prefix from P={P},W={W},X={X},Y={Y}. Using '0000'.")
        padded_prefix = "0000"

    standard_title = front_matter.get("standard_title")
    title_part_to_use = standard_title
    if not title_part_to_use:
        warnings_messages.append(
            "Missing 'standard_title'. Using original filename stem as fallback.")
        title_part_to_use = original_filename_stem
    sanitized_title = sanitize_filename_part(title_part_to_use)

    lang_suffix = ""
    language_fm = front_matter.get("language")
    if language_fm:
        lang_code = str(language_fm).strip().lower()
        if lang_code:
            lang_suffix = f".{lang_code}"
        else:
            warnings_messages.append(
                "Empty 'language' field in frontmatter. Omitting language suffix.")
    else:
        warnings_messages.append(
            "Missing 'language' field in frontmatter. Omitting language suffix.")

    return padded_prefix, sanitized_title, lang_suffix, warnings_messages

# --- Core Processing Functions ---


def get_or_create_lang_dir(lang: str, config: Config) -> tuple[Path | None, bool]:
    """
    Identifies the language-specific directory. Creates it if it doesn't exist.
    This directory will be processed in-place.

    Returns:
        - Path | None: The path to the language directory, or None on critical error.
        - bool: True if the directory was newly created (was_absent), False otherwise.
    """
    lang_dir_name = config.LANG_DIR_TEMPLATE.format(lang=lang)
    lang_dir_path = config.BASE_DIR / lang_dir_name
    was_newly_created = False

    if lang_dir_path.exists():
        if not lang_dir_path.is_dir():
            print(
                f"[ERROR] Path '{lang_dir_path}' exists but is not a directory. Skipping language '{lang}'.")
            return None, False
        print(
            f"Using existing directory '{lang_dir_path.name}' for in-place processing of '{lang}'.")
    else:
        print(
            f"Directory '{lang_dir_path.name}' not found for language '{lang}'. Creating it.")
        try:
            # exist_ok=False to ensure it's new
            lang_dir_path.mkdir(parents=True, exist_ok=False)
            was_newly_created = True
            print(f"Created directory: '{lang_dir_path.name}' for '{lang}'.")
        except FileExistsError:  # Should not happen due to prior .exists() check, but for safety
            print(
                f"[ERROR] Directory '{lang_dir_path.name}' unexpectedly created by another process. Attempting to use it.")
            if not lang_dir_path.is_dir():  # Verify it's a dir
                print(
                    f"[ERROR] Path '{lang_dir_path}' is not a directory after attempted creation. Skipping language '{lang}'.")
                return None, False
            was_newly_created = False  # It existed.
        except OSError as e:
            print(
                f"[ERROR] Failed to create directory '{lang_dir_path}': {e}. Skipping language '{lang}'.")
            return None, False

    return lang_dir_path, was_newly_created

# This function is now a general utility, not directly tied to the old finalization flow.
# It could be used if a pre-processing archive step is desired.


def archive_existing_directory(path_to_archive: Path, archive_prefix_template: str, lang: str, timestamp: str) -> bool:
    """
    Archives the given directory if it exists.
    The archive_prefix_template should be like "plugin_dev_{lang}_archive_".
    Returns True if path is clear for use (was archived or didn't exist), False on error or if path is not a dir.
    """
    if path_to_archive.exists():
        if path_to_archive.is_dir():
            archive_base_name = archive_prefix_template.format(lang=lang)
            archive_dir_name = f"{archive_base_name}{timestamp}"
            archive_dir_path = path_to_archive.parent / archive_dir_name
            try:
                if archive_dir_path.exists():  # Safety: if target archive name exists, remove it.
                    print(
                        f"  [Warning] Archive destination '{archive_dir_path}' already exists. Removing it first to avoid error during move.")
                    shutil.rmtree(archive_dir_path)
                shutil.move(str(path_to_archive), str(archive_dir_path))
                print(
                    f"  Archived existing directory '{path_to_archive.name}' to '{archive_dir_path.name}'.")
                return True  # Path is now clear because original was moved
            except OSError as e:
                print(
                    f"  [Error] Failed to archive existing directory '{path_to_archive.name}' to '{archive_dir_path.name}': {e}")
                return False
        else:
            print(
                f"  [Error] Path '{path_to_archive}' exists but is not a directory. Cannot archive.")
            return False
    return True  # Path didn't exist, so it's clear


def process_single_mdx_file(
    mdx_filepath: Path,
    config: Config
) -> dict:
    """
    Processes a single MDX file: extracts metadata, generates new filename,
    and renames the file in place.
    Returns stats.
    """
    stats = {"status": "processed", "warnings": [], "error_message": None}
    display_path = mdx_filepath.name
    if mdx_filepath.parent != config.BASE_DIR:
        try:
            # Show relative path from the language directory's parent (BASE_DIR)
            display_path = mdx_filepath.relative_to(
                mdx_filepath.parent.parent).as_posix()
        except ValueError:
            display_path = mdx_filepath.relative_to(config.BASE_DIR).as_posix()

    file_warnings = []

    try:
        content = mdx_filepath.read_text(encoding="utf-8")
        front_matter, _ = extract_front_matter(content)

        if front_matter is None:
            stats["status"] = "error"
            stats["error_message"] = "YAML Error in file."
            print(f"\nProcessing: {display_path}")
            print(f"  [Skipping] {stats['error_message']}")
            return stats

        P, W, X, Y, pwxy_warnings = _calculate_pwxy_and_warnings(
            front_matter, config)
        file_warnings.extend(pwxy_warnings)

        padded_prefix, sanitized_title, lang_suffix, fname_warnings = _generate_filename_parts(
            P, W, X, Y, front_matter, mdx_filepath.stem
        )
        file_warnings.extend(fname_warnings)

        # padded_prefix has a fallback to "0000", so it should not be None
        new_filename = f"{padded_prefix}-{sanitized_title}{lang_suffix}.mdx"
        new_filepath = mdx_filepath.with_name(new_filename)

        if new_filepath == mdx_filepath:
            stats["status"] = "skipped_no_change"
        elif new_filepath.exists():
            stats["status"] = "skipped_target_exists"
            # Do not print here, summary will handle it. Let main loop print progress.
        else:
            try:
                mdx_filepath.rename(new_filepath)
            except Exception as rename_error:
                stats["status"] = "error"
                stats["error_message"] = f"Failed to rename file to '{new_filename}': {rename_error}"
                # Defer printing to main loop for consistency
                return stats

        stats["warnings"] = file_warnings
        # Only print details if there are warnings or an actual change/error for this file
        if file_warnings or (stats["status"] == "processed" and new_filepath != mdx_filepath) or stats["status"].startswith("error") or stats["status"] == "skipped_target_exists":
            print(
                f"\nProcessing: {display_path} -> {new_filename if new_filepath != mdx_filepath else '(no change)'}")
            for warning_msg in file_warnings:
                print(f"  [Warning] {warning_msg}")
            if stats["status"] == "skipped_target_exists":
                print(
                    f"  [Skipping] Target filename '{new_filename}' already exists in this directory.")
            if stats["error_message"]:
                print(f"  [Error] {stats['error_message']}")

    except FileNotFoundError:
        stats["status"] = "error"
        stats["error_message"] = f"File not found during processing: {mdx_filepath}"
        print(f"\nProcessing: {display_path}")
        print(f"  [Error] {stats['error_message']}")
    except Exception as e:
        stats["status"] = "error"
        stats["error_message"] = f"Unexpected error: {e}"
        print(f"\nProcessing: {display_path}")
        print(f"  [Error] Unexpected error processing file: {e}")
        import traceback
        traceback.print_exc()
    return stats


def run_processing_for_language(
    lang_dir_path: Path,
    config: Config
) -> dict:
    """Processes all MDX files in the lang_dir_path by renaming them in place."""
    print(f"Starting in-place processing for: {lang_dir_path.name}")

    lang_stats = {
        "processed_count": 0,
        "skipped_no_change_count": 0,
        "skipped_target_exists_count": 0,
        "error_count": 0,
        "warning_files_count": 0,
        "status": "OK",
        # For summary
        "dir_path_str": str(lang_dir_path.relative_to(config.BASE_DIR))
    }

    if not lang_dir_path.exists() or not lang_dir_path.is_dir():
        print(
            f"[Error] Language directory '{lang_dir_path.name}' does not exist or is not a directory.")
        lang_stats["status"] = "LANG_DIR_ERROR"
        return lang_stats

    # Sort for consistent processing order
    mdx_files = sorted(list(lang_dir_path.rglob("*.mdx")))
    total_files = len(mdx_files)
    print(f"Found {total_files} MDX files to process in '{lang_dir_path.name}'.")

    for i, mdx_filepath in enumerate(mdx_files):
        result = process_single_mdx_file(mdx_filepath, config)

        if result["status"] == "processed":
            lang_stats["processed_count"] += 1
        elif result["status"] == "skipped_no_change":
            lang_stats["skipped_no_change_count"] += 1
        elif result["status"] == "skipped_target_exists":
            lang_stats["skipped_target_exists_count"] += 1
        elif result["status"] == "error":
            lang_stats["error_count"] += 1

        if result["warnings"]:  # Count files with warnings regardless of status
            lang_stats["warning_files_count"] += 1

        if total_files > 0:
            progress = (i + 1) / total_files * 100
            print(
                f"Progress for {lang_dir_path.name}: {i+1}/{total_files} files ({progress:.1f}%) evaluated.", end="\r")

    if total_files > 0:
        print()  # Newline after progress bar

    print("-" * 20)
    print(f"Language Processing Summary ({lang_dir_path.name}):")
    print(
        f"  Successfully processed (renamed): {lang_stats['processed_count']}")
    # Clarified term
    print(
        f"  Checked (filename no change): {lang_stats['skipped_no_change_count']}")
    print(
        f"  Skipped (target filename exists): {lang_stats['skipped_target_exists_count']}")
    print(f"  Files with warnings: {lang_stats['warning_files_count']}")
    print(
        f"  Errors encountered during file processing: {lang_stats['error_count']}")
    print("-" * 20)

    if lang_stats["error_count"] > 0:
        lang_stats["status"] = "ERRORS_IN_PROCESSING"
    return lang_stats

# --- Main Orchestration ---


def main():
    config = Config()
    print(f"Base directory: {config.BASE_DIR}")
    print(f"Timestamp for this run: {config.TIMESTAMP}")

    overall_summary = {}
    # Store if the lang dir was newly created for cleanup decisions
    lang_dir_newly_created_flags = {}
    # Store the Path object of the language directory for each lang
    lang_dirs_map = {}

    for lang in config.LANGUAGES:
        print(f"\n{'='*10} Processing Language: {lang.upper()} {'='*10}")

        current_lang_dir, was_newly_created = get_or_create_lang_dir(
            lang, config)
        lang_dir_newly_created_flags[lang] = was_newly_created
        lang_dirs_map[lang] = current_lang_dir

        if not current_lang_dir:
            overall_summary[lang] = {
                "status": "SETUP_ERROR", "message": f"Failed to get or create language directory for {lang}."}
            continue

        # Optional: Add a pre-processing archive step if desired for non-Git backups
        # For example:
        # if current_lang_dir.exists() and any(current_lang_dir.iterdir()): # if dir exists and is not empty
        #     print(f"Attempting to archive '{current_lang_dir.name}' before processing...")
        #     if not archive_existing_directory(current_lang_dir, config.ARCHIVE_LANG_DIR_PREFIX_TEMPLATE, lang, config.TIMESTAMP):
        #         print(f"  [CRITICAL ERROR] Archiving failed. Skipping processing for {lang}.")
        #         overall_summary[lang] = {"status": "PRE_ARCHIVE_ERROR", "message": f"Failed to archive existing directory {current_lang_dir.name}."}
        #         continue
        #     # After archiving, the original path is gone, so we need to re-create it to process into
        #     current_lang_dir, was_newly_created = get_or_create_lang_dir(lang, config) # This will re-create it empty
        #     lang_dir_newly_created_flags[lang] = True # Mark as newly created for potential cleanup
        #     lang_dirs_map[lang] = current_lang_dir
        #     if not current_lang_dir:
        #         overall_summary[lang] = {"status": "SETUP_ERROR_POST_ARCHIVE", "message": f"Failed to re-create lang directory for {lang} after archiving."}
        #         continue

        lang_results = run_processing_for_language(current_lang_dir, config)
        overall_summary[lang] = lang_results

        # --- Finalization for this language (mainly cleanup) ---
        if current_lang_dir:  # Should always be true if we reached here
            # Processed, even if with errors
            if lang_results["status"] in ["OK", "ERRORS_IN_PROCESSING"]:
                # If the directory was newly created by this script AND it's still empty after processing
                # (e.g., no MDX files were found or created in it), then remove it.
                if was_newly_created and current_lang_dir.exists() and not any(current_lang_dir.iterdir()):
                    try:
                        current_lang_dir.rmdir()
                        print(
                            f"  Removed empty newly created language directory: {current_lang_dir.name}")
                        lang_dirs_map[lang] = None  # It's gone
                        lang_results["message"] = lang_results.get(
                            "message", "") + " Empty newly created directory removed."
                    except OSError as e:
                        print(
                            f"  Note: Could not remove empty newly created directory '{current_lang_dir.name}': {e}")
            # No renaming logic needed as we operate in-place.
            # The status messages in lang_results already indicate success/failure of content processing.

    print("\n\n" + "=" * 20 + " Overall Script Summary " + "=" * 20)
    for lang_code in config.LANGUAGES:
        summary = overall_summary.get(lang_code, {})
        lang_dir_path_obj = lang_dirs_map.get(lang_code)

        print(f"\nLanguage: {lang_code.upper()}")
        status = summary.get("status", "UNKNOWN")
        print(f"  Status: {status}")

        if "message" in summary:  # Print setup/archive messages
            print(f"  Message: {summary['message']}")

        if status not in ["SETUP_ERROR", "SETUP_ERROR_POST_ARCHIVE", "PRE_ARCHIVE_ERROR", "LANG_DIR_ERROR"]:
            print(f"  Directory: {summary.get('dir_path_str', 'N/A')}")
            print(
                f"  Processed (renamed): {summary.get('processed_count', 0)}")
            print(
                f"  Checked (no name change): {summary.get('skipped_no_change_count', 0)}")
            print(
                f"  Skipped (target exists): {summary.get('skipped_target_exists_count', 0)}")
            print(
                f"  Files with Warnings: {summary.get('warning_files_count', 0)}")
            print(
                f"  Errors during file processing: {summary.get('error_count', 0)}")

        if lang_dir_path_obj and lang_dir_path_obj.exists():
            print(f"  Final directory location: {lang_dir_path_obj.name}")
        # If it was new and now gone
        elif lang_dir_newly_created_flags.get(lang_code) and not lang_dir_path_obj:
            print("  Note: Empty newly created directory was removed as expected.")
        elif not lang_dir_path_obj and status != "SETUP_ERROR":  # If it wasn't a setup error but dir is None
            print(
                f"  Note: Language directory '{config.LANG_DIR_TEMPLATE.format(lang=lang_code)}' may have been archived or removed.")

    print("=" * (40 + len(" Overall Script Summary ")))
    print("\nScript finished. Please review changes and commit to Git if satisfied.")


if __name__ == "__main__":
    main()
