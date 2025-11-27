#!/usr/bin/env python3
"""
OpenAPI Translator

Coordinates translation of OpenAPI markdown via Dify API.
Wraps the existing translation infrastructure for OpenAPI-specific needs.
"""

import httpx
import asyncio
import json
import os
from pathlib import Path


class OpenAPITranslator:
    """Manages translation of OpenAPI markdown via Dify API."""

    def __init__(self, markdown_path: str, target_lang: str, dify_api_key: str = None):
        """
        Initialize the translator.

        Args:
            markdown_path: Path to the markdown file to translate
            target_lang: Target language code (zh, ja)
            dify_api_key: Dify API key (if None, loads from env)
        """
        self.markdown_path = markdown_path
        self.target_lang = target_lang
        self.dify_api_key = dify_api_key or self._load_api_key()

        # Load termbase
        self.termbase_path = Path(__file__).parent.parent / "termbase_i18n.md"

        # Load config for language mappings
        self.config = self._load_config()

    def _load_config(self):
        """Load translation configuration from config.json"""
        config_path = Path(__file__).parent.parent / "config.json"
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")

        # Fallback to empty config
        return {}

    def _load_api_key(self) -> str:
        """Load Dify API key from environment or .env file."""
        # Try environment variable first (case-insensitive)
        api_key = os.getenv("DIFY_API_KEY") or os.getenv("dify_api_key")
        if api_key:
            return api_key

        # Try .env file (support both uppercase and lowercase)
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("DIFY_API_KEY=") or line.startswith("dify_api_key="):
                        return line.split("=", 1)[1].strip()

        raise ValueError("DIFY_API_KEY (or dify_api_key) not found in environment or .env file")

    async def translate_async(self, max_retries: int = 5) -> str:
        """
        Translate the markdown file via Dify API (async version).

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            Translated markdown text
        """
        # Read markdown content
        with open(self.markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Read termbase
        termbase = ""
        if self.termbase_path.exists():
            with open(self.termbase_path, 'r', encoding='utf-8') as f:
                termbase = f.read()

        # Get target language name from config
        target_language_name = self.target_lang
        if self.config and 'languages' in self.config:
            lang_info = self.config['languages'].get(self.target_lang, {})
            target_language_name = lang_info.get('name', self.target_lang)
        else:
            # Fallback mapping if config not available
            fallback_map = {"zh": "Chinese", "ja": "Japanese"}
            target_language_name = fallback_map.get(self.target_lang, self.target_lang)

        # Prepare API payload
        url = "https://api.dify.ai/v1/workflows/run"

        inputs = {
            "original_language": "English",
            "output_language1": target_language_name,
            "the_doc": content,
            "termbase": termbase
        }

        payload = {
            "response_mode": "streaming",  # Critical: avoid gateway timeouts
            "user": "OpenAPI-Translator",
            "inputs": inputs
        }

        headers = {
            "Authorization": f"Bearer {self.dify_api_key}",
            "Content-Type": "application/json"
        }

        # Retry mechanism with exponential backoff
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    import random
                    base_delay = min(30 * (2 ** (attempt - 1)), 300)  # Cap at 5 min
                    jitter = random.uniform(0.8, 1.2)
                    delay = base_delay * jitter
                    print(f"⏳ Retry attempt {attempt + 1}/{max_retries} after {delay:.1f}s delay...")
                    await asyncio.sleep(delay)

                # Stream the response (timeout: 10 minutes)
                async with httpx.AsyncClient(timeout=600.0) as client:
                    async with client.stream("POST", url, json=payload, headers=headers) as response:
                        # Check initial status
                        if response.status_code != 200:
                            print(f"❌ HTTP Error: {response.status_code}")
                            error_text = await response.aread()
                            print(f"Response: {error_text.decode('utf-8')[:500]}")
                            if response.status_code in [502, 503, 504]:
                                if attempt < max_retries - 1:
                                    print(f"Will retry... ({max_retries - attempt - 1} attempts remaining)")
                                    continue
                            raise Exception(f"HTTP {response.status_code}")

                        # Parse streaming response (SSE format)
                        print(f"📥 Receiving streaming response...")
                        output1 = None
                        workflow_run_id = None
                        final_status = None

                        async for line in response.aiter_lines():
                            line = line.strip()
                            if not line or not line.startswith("data: "):
                                continue

                            try:
                                json_str = line[6:]  # Remove "data: " prefix
                                event_data = json.loads(json_str)
                                event_type = event_data.get("event", "")

                                if "workflow_run_id" in event_data:
                                    workflow_run_id = event_data["workflow_run_id"]

                                if event_type == "workflow_started":
                                    print(f"🔄 Workflow started: {workflow_run_id}")
                                elif event_type == "workflow_finished":
                                    final_status = event_data.get("data", {}).get("status", "unknown")
                                    print(f"🔄 Workflow finished with status: {final_status}")
                                    outputs = event_data.get("data", {}).get("outputs", {})
                                    output1 = outputs.get("output1", "")
                                elif event_type == "node_started":
                                    node_type = event_data.get("data", {}).get("node_type", "")
                                    print(f"  ⚙️  Node started: {node_type}")
                                elif event_type == "error":
                                    error_msg = event_data.get("message", "Unknown error")
                                    print(f"❌ Workflow error: {error_msg}")
                                    raise Exception(f"Workflow error: {error_msg}")
                            except json.JSONDecodeError:
                                continue

                # Check final status
                if final_status == "failed":
                    print(f"❌ Workflow execution failed")
                    if attempt < max_retries - 1:
                        continue
                    raise Exception("Workflow execution failed")

                if not output1:
                    print(f"⚠️  Warning: No output1 found in workflow_finished event")
                    if attempt < max_retries - 1:
                        print(f"Will retry... ({max_retries - attempt - 1} attempts remaining)")
                        continue
                    raise Exception("No output received from workflow")

                print(f"✅ Translation completed successfully (length: {len(output1)} chars)")
                return output1

            except httpx.ReadTimeout:
                print(f"⏱️  Stream timeout after 600s (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    raise Exception(f"All {max_retries} attempts failed due to timeout")

            except httpx.ConnectTimeout as e:
                print(f"🔌 Connection timeout (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"All {max_retries} attempts failed due to connection timeout")

            except httpx.HTTPError as e:
                print(f"🌐 HTTP error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"All {max_retries} attempts failed due to HTTP errors")

            except Exception as e:
                if "Workflow" in str(e) or "HTTP" in str(e):
                    if attempt < max_retries - 1:
                        continue
                print(f"❌ Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise

        raise Exception(f"Translation failed after {max_retries} attempts")

    def translate(self, max_retries: int = 5) -> str:
        """
        Translate the markdown file via Dify API (sync wrapper).

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            Translated markdown text
        """
        return asyncio.run(self.translate_async(max_retries=max_retries))

    def save_translation(self, output_path: str, translated_text: str):
        """
        Save translated markdown to file.

        Args:
            output_path: Path to save the translated markdown
            translated_text: Translated markdown content
        """
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_text)
