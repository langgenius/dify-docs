import httpx
import os
import sys
import asyncio
import aiofiles

docs_structure = {
    "general_help": {
        "English": "en",
        "Chinese": "zh-hans",
        "Japanese": "ja-jp"
    },
    "plugin_dev": {
        "English": "plugin-dev-en",
        "Chinese": "plugin-dev-zh",
        "Japanese": "plugin-dev-ja"
    },
    "version_28x": {
        "English": "versions/2-8-x/en-us",
        "Chinese": "versions/2-8-x/zh-cn",
        "Japanese": "versions/2-8-x/ja-jp"
    },
    "version_30x": {
        "English": "versions/3-0-x/en-us",
        "Chinese": "versions/3-0-x/zh-cn",
        "Japanese": "versions/3-0-x/ja-jp"
    },
    "version_31x": {
        "English": "versions/3-1-x/en-us",
        "Chinese": "versions/3-1-x/zh-cn",
        "Japanese": "versions/3-1-x/ja-jp"
    }
}


async def translate_text(file_path, dify_api_key, original_language, target_language1, termbase_path=None, max_retries=3):
    """
    Translate text using Dify API with termbase from `tools/translate/termbase_i18n.md`
    """
    if termbase_path is None:
        # Get project root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(script_dir))  # Two levels up
        termbase_path = os.path.join(base_dir, "tools", "translate", "termbase_i18n.md")
    
    url = "https://api.dify.ai/v1/workflows/run"

    termbase = await load_md_mdx(termbase_path)
    the_doc = await load_md_mdx(file_path)
    payload = {
        "response_mode": "blocking",
        "user": "Dify",
        "inputs": {
            "original_language": original_language,
            "output_language1": target_language1,
            "the_doc": the_doc,
            "termbase": termbase
        }
    }

    headers = {
        "Authorization": "Bearer " + dify_api_key,
        "Content-Type": "application/json"
    }

    # Retry mechanism
    for attempt in range(max_retries):
        try:
            # Add delay to avoid concurrent pressure
            if attempt > 0:
                delay = attempt * 2  # Incremental delay: 2s, 4s, 6s
                print(f"Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(delay)

            async with httpx.AsyncClient(timeout=120.0) as client:  # Increase timeout to 120 seconds
                response = await client.post(url, json=payload, headers=headers)

            # Check HTTP status code
            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                if attempt == max_retries - 1:  # Last attempt
                    return ""
                continue

            try:
                response_data = response.json()
                print(f"API Response: {response_data}")  # Debug info
                
                # Extract output1
                output1 = response_data.get("data", {}).get("outputs", {}).get("output1", "")
                if not output1:
                    print("Warning: No output1 found in response")
                    print(f"Full response: {response_data}")
                return output1
            except Exception as e:
                print(f"Error parsing response: {e}")
                print(f"Response text: {response.text}")
                if attempt == max_retries - 1:  # Last attempt
                    return ""
                continue
                
        except httpx.ReadTimeout as e:
            print(f"Request timeout (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:  # Last attempt
                print(f"All {max_retries} attempts failed due to timeout")
                return ""
        except Exception as e:
            print(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:  # Last attempt
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



