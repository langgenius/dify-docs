import httpx
import os
import sys
import asyncio
import aiofiles
import json
from pathlib import Path

# Load translation config
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

def load_translation_config():
    """Load language configuration"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

TRANSLATION_CONFIG = load_translation_config()

def build_docs_structure():
    """Build docs structure from config and hardcoded plugin-dev paths"""
    structure = {}

    # General docs from config
    if TRANSLATION_CONFIG and "languages" in TRANSLATION_CONFIG:
        general_help = {}
        for lang_code, lang_info in TRANSLATION_CONFIG["languages"].items():
            general_help[lang_info["name"]] = lang_info["directory"]
        structure["general_help"] = general_help
    else:
        # Fallback if config not available
        structure["general_help"] = {
            "English": "en",
            "Chinese": "zh",
            "Japanese": "ja"
        }

    # Versioned docs from config
    if TRANSLATION_CONFIG and "versioned_docs" in TRANSLATION_CONFIG:
        for version_key, version_paths in TRANSLATION_CONFIG["versioned_docs"].items():
            # Convert version key (e.g., "2-8-x") to structure key (e.g., "version_28x")
            structure_key = f"version_{version_key.replace('-', '')}"
            version_structure = {}

            # Map language codes to language names
            for lang_code, path in version_paths.items():
                if lang_code in TRANSLATION_CONFIG["languages"]:
                    lang_name = TRANSLATION_CONFIG["languages"][lang_code]["name"]
                    version_structure[lang_name] = path

            structure[structure_key] = version_structure
    else:
        # No versioned docs in config - skip rather than hardcode
        pass

    return structure

docs_structure = build_docs_structure()


async def translate_text(file_path, dify_api_key, original_language, target_language1, termbase_path=None, max_retries=5, the_doc_exist=None, diff_original=None):
    """
    Translate text using Dify API with termbase from `tools/translate/termbase_i18n.md`
    Includes retry logic with exponential backoff for handling API timeouts and gateway errors.

    Args:
        file_path: Path to the document to translate
        dify_api_key: Dify API key
        original_language: Source language name
        target_language1: Target language name
        termbase_path: Optional path to terminology database
        max_retries: Maximum number of retry attempts
        the_doc_exist: Optional existing translation (for modified files)
        diff_original: Optional git diff of the original file (for modified files)
    """
    if termbase_path is None:
        # Get project root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(script_dir))  # Two levels up
        termbase_path = os.path.join(base_dir, "tools", "translate", "termbase_i18n.md")

    url = "https://api.dify.ai/v1/workflows/run"

    termbase = await load_md_mdx(termbase_path)
    the_doc = await load_md_mdx(file_path)

    # Build inputs - always include base inputs
    inputs = {
        "original_language": original_language,
        "output_language1": target_language1,
        "the_doc": the_doc,
        "termbase": termbase
    }

    # Add optional inputs for modified files
    if the_doc_exist is not None:
        inputs["the_doc_exist"] = the_doc_exist
    if diff_original is not None:
        inputs["diff_original"] = diff_original

    payload = {
        "response_mode": "streaming",  # Use streaming to avoid gateway timeouts
        "user": "Dify",
        "inputs": inputs
    }

    headers = {
        "Authorization": "Bearer " + dify_api_key,
        "Content-Type": "application/json"
    }

    # Retry mechanism with exponential backoff
    for attempt in range(max_retries):
        try:
            # Add exponential backoff with jitter for retries
            if attempt > 0:
                # Exponential backoff: 30s, 60s, 120s, 240s, 300s with ±20% jitter
                # Modified files take 2-3 minutes, so we need longer waits
                import random
                base_delay = min(30 * (2 ** (attempt - 1)), 300)  # Cap at 300s (5 min)
                jitter = random.uniform(0.8, 1.2)
                delay = base_delay * jitter
                print(f"⏳ Retry attempt {attempt + 1}/{max_retries} after {delay:.1f}s delay...")
                await asyncio.sleep(delay)

            # Streaming mode: no gateway timeout issues
            # Set timeout to 600s (10 min) for the entire stream
            async with httpx.AsyncClient(timeout=600.0) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    # Check initial response status
                    if response.status_code != 200:
                        print(f"❌ HTTP Error: {response.status_code}")
                        error_text = await response.aread()
                        print(f"Response: {error_text.decode('utf-8')[:500]}")
                        if response.status_code in [502, 503, 504]:
                            if attempt < max_retries - 1:
                                print(f"Will retry... ({max_retries - attempt - 1} attempts remaining)")
                                continue
                        return ""

                    # Parse streaming response (Server-Sent Events format)
                    print(f"📥 Receiving streaming response...")
                    output1 = None
                    workflow_run_id = None
                    final_status = None

                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line or not line.startswith("data: "):
                            continue

                        try:
                            # Remove "data: " prefix and parse JSON
                            json_str = line[6:]  # Remove "data: "
                            event_data = json.loads(json_str)
                            event_type = event_data.get("event", "")

                            # Track workflow ID
                            if "workflow_run_id" in event_data:
                                workflow_run_id = event_data["workflow_run_id"]

                            # Handle different event types
                            if event_type == "workflow_started":
                                print(f"🔄 Workflow started: {workflow_run_id}")
                            elif event_type == "workflow_finished":
                                final_status = event_data.get("data", {}).get("status", "unknown")
                                print(f"🔄 Workflow finished with status: {final_status}")
                                # Extract output1 from final event
                                outputs = event_data.get("data", {}).get("outputs", {})
                                output1 = outputs.get("output1", "")
                            elif event_type == "node_started":
                                node_type = event_data.get("data", {}).get("node_type", "")
                                print(f"  ⚙️  Node started: {node_type}")
                            elif event_type == "error":
                                error_msg = event_data.get("message", "Unknown error")
                                print(f"❌ Workflow error: {error_msg}")
                                return ""
                        except json.JSONDecodeError as e:
                            # Skip invalid JSON lines
                            continue

            # Check final status and output
            if final_status == "failed":
                print(f"❌ Workflow execution failed")
                return ""

            if not output1:
                print(f"⚠️  Warning: No output1 found in workflow_finished event")
                if attempt < max_retries - 1:
                    print(f"Will retry... ({max_retries - attempt - 1} attempts remaining)")
                    continue
                return ""

            print(f"✅ Translation completed successfully (length: {len(output1)} chars)")
            return output1

        except httpx.ReadTimeout as e:
            print(f"⏱️  Stream timeout after 600s (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                print(f"Will retry... ({max_retries - attempt - 1} attempts remaining)")
            else:
                print(f"❌ All {max_retries} attempts failed due to timeout")
                return ""

        except httpx.ConnectTimeout as e:
            print(f"🔌 Connection timeout (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                print(f"❌ All {max_retries} attempts failed due to connection timeout")
                return ""

        except httpx.HTTPError as e:
            print(f"🌐 HTTP error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                print(f"❌ All {max_retries} attempts failed due to HTTP errors")
                return ""

        except Exception as e:
            print(f"❌ Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                print(f"❌ All {max_retries} attempts failed due to unexpected errors")
                return ""

    return ""


async def load_md_mdx(file_path):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
    return content


def determine_doc_type_and_language(file_path):
    """
    Determine document type and current language based on file path
    Returns (doc_type, current_language, language_name)
    """
    # Normalize path separators
    normalized_path = file_path.replace(os.sep, '/')
    
    # Collect all possible matches and find the longest one
    matches = []
    for doc_type, languages in docs_structure.items():
        for lang_name, lang_code in languages.items():
            # Normalize lang_code path separators too
            normalized_lang_code = lang_code.replace(os.sep, '/')
            if normalized_lang_code in normalized_path:
                matches.append((len(normalized_lang_code), doc_type, lang_code, lang_name))
    
    # Return the match with the longest lang_code (most specific)
    if matches:
        matches.sort(reverse=True)  # Sort by length descending
        _, doc_type, lang_code, lang_name = matches[0]
        return doc_type, lang_code, lang_name
    
    return None, None, None


def get_language_code_name_map(doc_type):
    """
    Get mapping from language code to language name
    """
    code_to_name = {}
    for lang_name, lang_code in docs_structure[doc_type].items():
        code_to_name[lang_code] = lang_name
    return code_to_name


def generate_target_path(file_path, current_lang_code, target_lang_code):
    """
    Generate target language file path
    """
    return file_path.replace(current_lang_code, target_lang_code)


async def save_translated_content(content, file_path):
    """
    Save translated content to file
    """
    try:
        print(f"Attempting to save to: {file_path}")
        print(f"Content length: {len(content)} characters")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save file
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(content)
        
        # Verify file was saved successfully
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✓ Translated content saved to {file_path} (size: {file_size} bytes)")
        else:
            print(f"✗ Failed to save file: {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {str(e)}")


async def translate_single_file(file_path, dify_api_key, current_lang_name, target_lang_code, target_lang_name, current_lang_code, semaphore):
    """
    Async translate single file (using semaphore to control concurrency)
    """
    async with semaphore:  # Control concurrency
        # Generate target file path
        target_file_path = generate_target_path(file_path, current_lang_code, target_lang_code)
        
        print(f"Source: {file_path}")
        print(f"Target: {target_file_path}")
        
        # Check if target file exists
        if os.path.exists(target_file_path):
            print(f"Target file already exists: {target_file_path}")
            return
        
        print(f"Translating from {current_lang_name} to {target_lang_name}...")
        
        try:
            # Call translation function
            translated_content = await translate_text(
                file_path, 
                dify_api_key, 
                current_lang_name, 
                target_lang_name
            )
            
            print(f"Translation result length: {len(translated_content)} characters")
            
            if translated_content and translated_content.strip():
                # Save translation result
                await save_translated_content(translated_content, target_file_path)
            else:
                print(f"Error: Translation failed for {target_lang_name} - empty or no content returned")
        except Exception as e:
            print(f"Error translating to {target_lang_name}: {str(e)}")
            import traceback
            traceback.print_exc()


async def main_async(file_path, dify_api_key=None):
    """
    Async main function
    """
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to load API key from .env file
    env_path = os.path.join(script_dir, '.env')
    if os.path.exists(env_path) and dify_api_key is None:
        try:
            # Import dotenv only when needed
            import importlib.util
            dotenv_spec = importlib.util.find_spec("dotenv")
            if dotenv_spec is not None:
                from dotenv import load_dotenv
                load_dotenv(env_path)
                dify_api_key = os.getenv('DIFY_API_KEY') or os.getenv('dify_api_key')
            else:
                raise ImportError
        except ImportError:
            # Manual parsing of .env file if dotenv is not available
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('DIFY_API_KEY=') or line.strip().startswith('dify_api_key='):
                        dify_api_key = line.strip().split('=', 1)[1].strip('"\'')
                        break
    
    if not dify_api_key:
        print("Error: DIFY_API_KEY not found. Please provide it as parameter or in .env file.")
        return
    
    # Determine document type and current language
    doc_type, current_lang_code, current_lang_name = determine_doc_type_and_language(file_path)
    
    if not doc_type:
        print(f"Error: Unable to determine document type and language for {file_path}")
        return
    
    print(f"Document type: {doc_type}, Current language: {current_lang_name} ({current_lang_code})")
    
    # Get all languages for current document type
    code_to_name = get_language_code_name_map(doc_type)
    
    # Create semaphore to limit concurrency (avoid excessive API pressure)
    semaphore = asyncio.Semaphore(2)
    
    # Create all translation tasks
    tasks = []
    for target_lang_code, target_lang_name in code_to_name.items():
        # Skip current language
        if target_lang_code == current_lang_code:
            continue
        
        task = translate_single_file(
            file_path, 
            dify_api_key, 
            current_lang_name, 
            target_lang_code, 
            target_lang_name, 
            current_lang_code,
            semaphore
        )
        tasks.append(task)
    
    # Execute all translation tasks
    if tasks:
        print("Running translations concurrently...")
        await asyncio.gather(*tasks)
        print("All translations completed!")
    else:
        print("No translations needed.")


def get_file_path_interactive():
    """
    Interactive file path input
    """
    while True:
        print("Please enter the file path to translate:")
        print("请输入要翻译的文件路径:")
        print("翻訳するファイルパスを入力してください:")
        file_path = input("File path / 文件路径 / ファイルパス: ").strip()
        
        if not file_path:
            print("File path cannot be empty. Please try again.")
            print("文件路径不能为空，请重新输入。")
            print("ファイルパスは空にできません。再度入力してください。")
            continue
            
        # Remove quotes if user copy-pasted with quotes
        file_path = file_path.strip('\'"')
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            print(f"文件不存在: {file_path}")
            print(f"ファイルが存在しません: {file_path}")
            print("Please check if the path is correct.")
            print("请检查路径是否正确。")
            print("パスが正しいか確認してください。")
            continue
            
        # Check if it's a file
        if not os.path.isfile(file_path):
            print(f"The specified path is not a file: {file_path}")
            print(f"指定的路径不是文件: {file_path}")
            print(f"指定されたパスはファイルではありません: {file_path}")
            continue
            
        # Check file extension
        if not (file_path.endswith('.md') or file_path.endswith('.mdx')):
            print(f"Warning: File is not .md or .mdx format: {file_path}")
            print(f"警告: 文件不是 .md 或 .mdx 格式: {file_path}")
            print(f"警告: ファイルは .md または .mdx 形式ではありません: {file_path}")
            confirm = input("Continue anyway? (y/n) / 是否继续? (y/n) / 続行しますか? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes', 'Y', 'YES']:
                continue
                
        return file_path


def load_local_api_key():
    """
    Load API key from local .env file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    if not os.path.exists(env_path):
        print(f"Error: .env file not found: {env_path}")
        print(f"错误: 未找到 .env 文件: {env_path}")
        print(f"エラー: .env ファイルが見つかりません: {env_path}")
        print("Please create .env file and add: DIFY_API_KEY=your_api_key")
        print("请在当前目录创建 .env 文件并添加: DIFY_API_KEY=your_api_key")
        print(".env ファイルを作成し、DIFY_API_KEY=your_api_key を追加してください")
        return None
    
    try:
        # Try using dotenv
        import importlib.util
        dotenv_spec = importlib.util.find_spec("dotenv")
        if dotenv_spec is not None:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            api_key = os.getenv('DIFY_API_KEY') or os.getenv('dify_api_key')
        else:
            # Manual parsing of .env file
            api_key = None
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('DIFY_API_KEY=') or line.startswith('dify_api_key='):
                        api_key = line.split('=', 1)[1].strip('"\'')
                        break
    except Exception as e:
        print(f"Error reading .env file: {e}")
        print(f"读取 .env 文件时出错: {e}")
        print(f".env ファイルの読み取りエラー: {e}")
        return None
    
    if not api_key:
        print("Error: DIFY_API_KEY not found in .env file")
        print("错误: 在 .env 文件中未找到 DIFY_API_KEY")
        print("エラー: .env ファイルに DIFY_API_KEY が見つかりません")
        print("Please ensure .env file contains: DIFY_API_KEY=your_api_key")
        print("请确保 .env 文件包含: DIFY_API_KEY=your_api_key")
        print(".env ファイルに DIFY_API_KEY=your_api_key が含まれていることを確認してください")
        return None
        
    print("✓ Successfully loaded local API key")
    print("✓ 成功加载本地 API key")
    print("✓ ローカル API キーの読み込みに成功しました")
    return api_key


def main(file_path, dify_api_key=None):
    """
    Sync wrapper function to run async main function
    """
    asyncio.run(main_async(file_path, dify_api_key))


if __name__ == "__main__":
    # If no parameters provided, enter interactive mode
    if len(sys.argv) == 1:
        print("=== Dify Documentation Translation Tool ===")
        print("=== Dify 文档翻译工具 ===")
        print("=== Dify ドキュメント翻訳ツール ===")
        print()
        
        # Interactive file path input
        file_path = get_file_path_interactive()
        
        # Load local API key
        dify_api_key = load_local_api_key()
        if not dify_api_key:
            sys.exit(1)
        
        print()
        print(f"Starting translation for file: {file_path}")
        print(f"开始翻译文件: {file_path}")
        print(f"ファイルの翻訳を開始: {file_path}")
        main(file_path, dify_api_key)
        
    # Command line argument mode
    elif len(sys.argv) >= 2:
        file_path = sys.argv[1]
        dify_api_key = None
        
        # Parse command line arguments
        for i, arg in enumerate(sys.argv[2:], 2):
            if dify_api_key is None:
                dify_api_key = arg
        
        main(file_path, dify_api_key)
    
    else:
        print("Usage: python main.py [file_path] [dify_api_key]")
        print("  No arguments: Enter interactive mode")
        print("  file_path: File path to translate")
        print("  dify_api_key: (Optional) Dify API key")
        sys.exit(1)



