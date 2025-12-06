#!/usr/bin/env python3
"""
Translation A/B Testing Runner
Usage: python run_test.py <spec.md> [--dry-run]

Test spec format:
  ## keys
  app-xxx
  Description A

  ## test_content
  (inline content to translate)

  OR

  ## test_file
  path/to/file.md
"""

import httpx
import os
import sys
import asyncio
import json
import re
import random
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR / "results"
TERMBASE_PATH = SCRIPT_DIR.parent / "translate" / "termbase_i18n.md"
DIFY_API_URL = "https://api.dify.ai/v1/workflows/run"
LANGUAGE_NAMES = {"cn": "Chinese", "jp": "Japanese", "en": "English"}


def load_env_file():
    env_path = SCRIPT_DIR / ".env"
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip("'\"")


def parse_markdown_spec(file_path: Path) -> dict:
    """Parse markdown test spec"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    config = {
        "test_name": file_path.stem,
        "target_languages": ["cn"],
        "test_content": None,
        "test_file": None,
        "existing_file": None,  # For update scenario
        "diff_content": None,   # For update with diff scenario
        "variants": {}
    }

    # Title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        config["test_name"] = re.sub(r'[^a-zA-Z0-9]+', '_', title_match.group(1)).lower().strip('_')

    # Keys
    keys_match = re.search(r'##\s*keys\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if keys_match:
        lines = [l.strip() for l in keys_match.group(1).strip().split('\n') if l.strip()]
        variant_names = iter('ABCDEFGHIJ')
        i = 0
        while i < len(lines):
            if lines[i].startswith('app-') and not lines[i].startswith('app-***'):
                api_key = lines[i]
                description = lines[i + 1] if i + 1 < len(lines) and not lines[i + 1].startswith('app-') else ""
                if description:
                    i += 1
                config["variants"][next(variant_names)] = {"api_key": api_key, "description": description}
            i += 1

    # Target languages
    lang_match = re.search(r'##\s*target_languages\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if lang_match:
        langs = [l.strip() for l in lang_match.group(1).strip().split('\n') if l.strip() and not l.startswith('#')]
        if langs:
            config["target_languages"] = langs

    # Inline test content
    content_match = re.search(r'##\s*test_content\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if content_match:
        config["test_content"] = content_match.group(1).strip()

    # Test file path
    file_match = re.search(r'##\s*test_file\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if file_match:
        config["test_file"] = file_match.group(1).strip().split('\n')[0].strip()

    # Existing translation file (for update scenarios)
    existing_match = re.search(r'##\s*existing_file\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if existing_match:
        config["existing_file"] = existing_match.group(1).strip().split('\n')[0].strip()

    # Diff content (for update with diff scenarios)
    diff_match = re.search(r'##\s*diff_content\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if diff_match:
        config["diff_content"] = diff_match.group(1).strip()

    return config


def is_markdown_spec(file_path: Path) -> bool:
    if file_path.suffix in ['.md', '.mdx']:
        with open(file_path, "r", encoding="utf-8") as f:
            return bool(re.search(r'##\s*keys', f.read(), re.IGNORECASE))
    return False


async def load_file(file_path: Path) -> str:
    import aiofiles
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        return await f.read()


async def save_file(file_path: Path, content: str):
    import aiofiles
    file_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(content)


async def translate_text(content: str, api_key: str, target_language: str, termbase: str,
                         the_doc_exist: str = None, diff_original: str = None, max_retries: int = 3) -> str:
    inputs = {
        "original_language": "English",
        "output_language1": target_language,
        "the_doc": content,
        "termbase": termbase
    }
    # Add optional params for update scenarios (triggers different prompts in Dify)
    if the_doc_exist is not None:
        inputs["the_doc_exist"] = the_doc_exist
    if diff_original is not None:
        inputs["diff_original"] = diff_original

    payload = {
        "response_mode": "streaming",
        "user": "TranslationTest",
        "inputs": inputs
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = min(30 * (2 ** (attempt - 1)), 300) * random.uniform(0.8, 1.2)
                print(f"    Retry {attempt + 1}/{max_retries}...")
                await asyncio.sleep(delay)

            async with httpx.AsyncClient(timeout=600.0) as client:
                async with client.stream("POST", DIFY_API_URL, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        print(f"    HTTP {response.status_code}")
                        if response.status_code in [502, 503, 504] and attempt < max_retries - 1:
                            continue
                        return ""

                    output1 = None
                    async for line in response.aiter_lines():
                        if line.strip().startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if data.get("event") == "workflow_finished":
                                    output1 = data.get("data", {}).get("outputs", {}).get("output1", "")
                                elif data.get("event") == "error":
                                    print(f"    Error: {data.get('message')}")
                                    return ""
                            except json.JSONDecodeError:
                                continue

            if output1:
                return output1
            if attempt < max_retries - 1:
                continue
            return ""

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.HTTPError) as e:
            print(f"    {type(e).__name__}")
            if attempt >= max_retries - 1:
                return ""

    return ""


async def run_test(config_path: str, dry_run: bool = False):
    load_env_file()

    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: {config_path} not found")
        sys.exit(1)

    if not is_markdown_spec(config_file):
        print(f"Error: Not a valid test spec (needs ## keys section)")
        sys.exit(1)

    print(f"Parsing: {config_path}")
    config = parse_markdown_spec(config_file)

    test_name = config.get("test_name", "test")
    target_languages = config.get("target_languages", ["cn"])
    variants = config.get("variants", {})
    test_content = config.get("test_content")
    test_file = config.get("test_file")
    existing_file = config.get("existing_file")
    diff_content = config.get("diff_content")

    if not variants:
        print("Error: No valid API keys found")
        sys.exit(1)

    # Get test content
    if test_content:
        doc_content = test_content
        doc_name = "inline"
    elif test_file:
        test_file_path = Path(test_file)
        if not test_file_path.is_absolute():
            test_file_path = SCRIPT_DIR.parent.parent / test_file
        if not test_file_path.exists():
            print(f"Error: Test file not found: {test_file}")
            sys.exit(1)
        doc_content = await load_file(test_file_path)
        doc_name = test_file_path.stem
    else:
        print("Error: Need ## test_content or ## test_file section")
        sys.exit(1)

    # Load existing translation (optional - for update scenarios)
    existing_content = None
    if existing_file:
        existing_path = Path(existing_file)
        if not existing_path.is_absolute():
            existing_path = SCRIPT_DIR.parent.parent / existing_file
        if existing_path.exists():
            existing_content = await load_file(existing_path)
            print(f"Loaded existing translation: {existing_file} ({len(existing_content)} chars)")
        else:
            print(f"Warning: existing_file not found: {existing_file}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = RESULTS_DIR / f"{timestamp}_{test_name}"

    if not dry_run:
        result_dir.mkdir(parents=True, exist_ok=True)
        with open(result_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        # Save source content
        with open(result_dir / f"source_{doc_name}.md", "w", encoding="utf-8") as f:
            f.write(doc_content)

    termbase = await load_file(TERMBASE_PATH) if TERMBASE_PATH.exists() else ""

    # Determine test mode
    if existing_content and diff_content:
        test_mode = "update+diff (prompt 3)"
    elif existing_content:
        test_mode = "update (prompt 2)"
    else:
        test_mode = "new (prompt 1)"

    print(f"\n{'='*50}")
    print(f"Test: {test_name}")
    print(f"Mode: {test_mode}")
    print(f"Variants: {', '.join(variants.keys())}")
    print(f"Languages: {', '.join(target_languages)}")
    print(f"Content: {doc_name} ({len(doc_content)} chars)")
    if existing_content:
        print(f"Existing: {len(existing_content)} chars")
    if diff_content:
        print(f"Diff: {len(diff_content)} chars")
    print(f"{'='*50}\n")

    all_results = {}
    for var_name, var_config in variants.items():
        api_key = var_config.get("api_key")
        desc = var_config.get("description", "")
        print(f"{var_name}: {desc}")

        if dry_run:
            print("  DRY RUN")
            continue

        var_dir = result_dir / f"variant_{var_name}"
        var_dir.mkdir(parents=True, exist_ok=True)

        results = {}
        for lang in target_languages:
            lang_name = LANGUAGE_NAMES.get(lang, lang)
            print(f"  → {lang_name}...", end=" ", flush=True)

            translated = await translate_text(doc_content, api_key, lang_name, termbase,
                                             the_doc_exist=existing_content, diff_original=diff_content)
            if translated:
                out_file = var_dir / f"{doc_name}_{lang}.md"
                await save_file(out_file, translated)
                print(f"OK ({len(translated)} chars)")
                results[lang] = {"status": "ok", "chars": len(translated)}
            else:
                print("FAIL")
                results[lang] = {"status": "fail"}

        all_results[var_name] = results

    if not dry_run:
        with open(result_dir / "results.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\nResults: {result_dir}")
        print(f"Run: python compare.py {result_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_test.py <spec.md> [--dry-run]")
        sys.exit(1)
    asyncio.run(run_test(sys.argv[1], "--dry-run" in sys.argv))


if __name__ == "__main__":
    main()
