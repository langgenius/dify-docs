#!/usr/bin/env python3
"""
Security validation utilities for documentation synchronization.
Provides input validation, path sanitization, and security checks.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
import hashlib
import hmac

class SecurityValidator:
    """Validates and sanitizes inputs for documentation synchronization"""

    # Security constants
    MAX_FILE_SIZE_MB = 10
    MAX_FILES_PER_SYNC = 50
    MAX_PATH_LENGTH = 255
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10  # 10MB

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.md', '.mdx', '.json'}

    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r'\.\.',  # Directory traversal
        r'^/',     # Absolute paths
        r'^~',     # Home directory
        r'\$\{',   # Variable expansion
        r'`',      # Command substitution
        r'<script', # Script tags
        r'javascript:', # JavaScript protocol
        r'data:text/html', # Data URLs with HTML
    ]

    def __init__(self, base_dir: Path, config_path: Optional[Path] = None):
        """
        Initialize the security validator.

        Args:
            base_dir: The base directory for all operations
            config_path: Optional path to config.json (defaults to tools/translate/config.json)
        """
        self.base_dir = Path(base_dir).resolve()

        # Load configuration for dynamic language directories
        self.config = self._load_config(config_path)

        # Build allowed directories dynamically from config
        self.allowed_base_dirs = self._build_allowed_dirs()
        self.valid_languages = self._build_valid_languages()

    def _load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """Load translation configuration from config.json"""
        if config_path is None:
            # Default to tools/translate/config.json relative to base_dir
            config_path = self.base_dir / "tools" / "translate" / "config.json"

        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")

        # Fallback to empty config
        return {}

    def _build_allowed_dirs(self) -> Set[str]:
        """Build set of allowed base directories from config"""
        allowed = set()

        if 'languages' in self.config:
            for lang_code, lang_info in self.config['languages'].items():
                if 'directory' in lang_info:
                    allowed.add(lang_info['directory'])

        # Fallback if config is empty
        if not allowed:
            allowed = {'en', 'zh', 'ja'}

        return allowed

    def _build_valid_languages(self) -> Set[str]:
        """Build set of valid target language codes from config"""
        if 'target_languages' in self.config:
            return set(self.config['target_languages'])

        # Fallback if config is empty
        return {'zh', 'ja'}
    
    def validate_file_path(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a file path for security issues.
        
        Args:
            file_path: The file path to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check path length
        if len(file_path) > self.MAX_PATH_LENGTH:
            return False, f"Path too long: {len(file_path)} > {self.MAX_PATH_LENGTH}"
        
        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE):
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Parse path
        path = Path(file_path)
        
        # Check for absolute path
        if path.is_absolute():
            return False, "Absolute paths not allowed"
        
        # Check file extension
        if path.suffix not in self.ALLOWED_EXTENSIONS:
            return False, f"File extension not allowed: {path.suffix}"
        
        # Check if path starts with allowed directory
        parts = path.parts
        if not parts:
            return False, "Empty path"

        if parts[0] not in self.allowed_base_dirs and not file_path == 'docs.json':
            return False, f"Path must start with allowed directory: {self.allowed_base_dirs}"
        
        # Resolve and check if path stays within base directory
        try:
            full_path = (self.base_dir / path).resolve()
            if not full_path.is_relative_to(self.base_dir):
                return False, "Path escapes base directory"
        except (ValueError, RuntimeError) as e:
            return False, f"Invalid path: {e}"
        
        return True, None
    
    def validate_file_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file content for security issues.
        
        Args:
            content: The file content to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check content length
        if len(content) > self.MAX_CONTENT_LENGTH:
            return False, f"Content too large: {len(content)} > {self.MAX_CONTENT_LENGTH}"
        
        # Check for script injections in content
        dangerous_content_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'on\w+\s*=\s*["\']',  # Event handlers
            r'javascript:',  # JavaScript protocol
            r'data:text/html',  # Data URLs with HTML
        ]
        
        for pattern in dangerous_content_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return False, f"Dangerous content pattern detected"
        
        return True, None
    
    def validate_json_structure(self, json_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate JSON structure for security issues.
        
        Args:
            json_data: The JSON data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        def check_value(value: Any, depth: int = 0) -> Optional[str]:
            """Recursively check JSON values"""
            if depth > 10:
                return "JSON nesting too deep"
            
            if isinstance(value, str):
                # Check for dangerous patterns in string values
                for pattern in self.DANGEROUS_PATTERNS:
                    if re.search(pattern, value, re.IGNORECASE):
                        return f"Dangerous pattern in JSON value: {pattern}"
            elif isinstance(value, dict):
                for k, v in value.items():
                    if not isinstance(k, str):
                        return "Non-string key in JSON"
                    error = check_value(v, depth + 1)
                    if error:
                        return error
            elif isinstance(value, list):
                for item in value:
                    error = check_value(item, depth + 1)
                    if error:
                        return error
            
            return None
        
        error = check_value(json_data)
        if error:
            return False, error
        
        return True, None
    
    def validate_sync_plan(self, sync_plan: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a synchronization plan.
        
        Args:
            sync_plan: The sync plan to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        required_fields = ['files_to_sync', 'target_languages', 'metadata']
        for field in required_fields:
            if field not in sync_plan:
                return False, f"Missing required field: {field}"
        
        # Validate file count
        files = sync_plan.get('files_to_sync', [])
        if len(files) > self.MAX_FILES_PER_SYNC:
            return False, f"Too many files: {len(files)} > {self.MAX_FILES_PER_SYNC}"
        
        # Validate each file
        for file_info in files:
            if not isinstance(file_info, dict):
                return False, "Invalid file info structure"
            
            file_path = file_info.get('path')
            if not file_path:
                return False, "File path missing in sync plan"
            
            valid, error = self.validate_file_path(file_path)
            if not valid:
                return False, f"Invalid file path in sync plan: {error}"
            
            # Validate file size if present
            if 'size' in file_info:
                max_size = self.MAX_FILE_SIZE_MB * 1024 * 1024
                if file_info['size'] > max_size:
                    return False, f"File too large: {file_path}"
        
        # Validate target languages
        target_langs = sync_plan.get('target_languages', [])
        for lang in target_langs:
            if lang not in self.valid_languages:
                return False, f"Invalid target language: {lang}"
        
        return True, None
    
    def sanitize_path(self, file_path: str) -> Optional[str]:
        """
        Sanitize a file path by removing dangerous elements.
        
        Args:
            file_path: The file path to sanitize
            
        Returns:
            Sanitized path or None if path cannot be sanitized
        """
        # Remove leading/trailing whitespace
        file_path = file_path.strip()
        
        # Remove any null bytes
        file_path = file_path.replace('\x00', '')
        
        # Normalize path separators
        file_path = file_path.replace('\\', '/')
        
        # Remove double slashes
        while '//' in file_path:
            file_path = file_path.replace('//', '/')
        
        # Validate the sanitized path
        valid, _ = self.validate_file_path(file_path)
        if not valid:
            return None
        
        return file_path
    
    def create_safe_temp_dir(self) -> Path:
        """
        Create a safe temporary directory for operations.
        
        Returns:
            Path to the temporary directory
        """
        import tempfile
        import secrets
        
        # Create temp dir with random suffix
        suffix = secrets.token_hex(8)
        temp_dir = Path(tempfile.mkdtemp(suffix=f'-sync-{suffix}'))
        
        # Set restrictive permissions (Unix only)
        try:
            os.chmod(temp_dir, 0o700)
        except:
            pass  # Windows doesn't support chmod
        
        return temp_dir
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA-256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hex digest of the file hash
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def verify_artifact_integrity(self, artifact_data: bytes, expected_hash: Optional[str] = None) -> bool:
        """
        Verify the integrity of an artifact.
        
        Args:
            artifact_data: The artifact data
            expected_hash: Optional expected hash
            
        Returns:
            True if artifact is valid
        """
        if expected_hash:
            actual_hash = hashlib.sha256(artifact_data).hexdigest()
            return hmac.compare_digest(actual_hash, expected_hash)
        
        # Basic validation if no hash provided
        return len(artifact_data) < self.MAX_CONTENT_LENGTH
    
    def is_trusted_contributor(self, username: str, trusted_list: List[str] = None) -> bool:
        """
        Check if a user is a trusted contributor.
        
        Args:
            username: GitHub username
            trusted_list: Optional list of trusted usernames
            
        Returns:
            True if user is trusted
        """
        if not trusted_list:
            # Default trusted contributors (should be configured)
            trusted_list = []
        
        return username in trusted_list
    
    def rate_limit_check(self, identifier: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
        """
        Simple rate limiting check (would need persistent storage in production).
        
        Args:
            identifier: Unique identifier (e.g., PR number)
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            True if within rate limit
        """
        # This is a placeholder - in production, you'd use Redis or similar
        # For now, always return True
        return True


def create_validator(base_dir: Optional[Path] = None) -> SecurityValidator:
    """
    Create a security validator instance.
    
    Args:
        base_dir: Optional base directory (defaults to script parent)
        
    Returns:
        SecurityValidator instance
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent.parent
    
    return SecurityValidator(base_dir)


# Example usage and tests
if __name__ == "__main__":
    validator = create_validator()
    
    # Test path validation
    test_paths = [
        "en/docs/test.md",  # Valid
        "../../../etc/passwd",  # Invalid - directory traversal
        "/etc/passwd",  # Invalid - absolute path
        "en/test.exe",  # Invalid - wrong extension
        "zh/docs/test.mdx",  # Valid
        "docs.json",  # Valid - special case
    ]
    
    print("Path Validation Tests:")
    for path in test_paths:
        valid, error = validator.validate_file_path(path)
        status = "✓" if valid else "✗"
        print(f"  {status} {path}: {error if error else 'Valid'}")
    
    print("\nContent Validation Tests:")
    test_contents = [
        "# Normal markdown content",  # Valid
        "<script>alert('xss')</script>",  # Invalid - script tag
        "Normal text with onclick='alert()'",  # Invalid - event handler
    ]
    
    for content in test_contents:
        valid, error = validator.validate_file_content(content)
        status = "✓" if valid else "✗"
        preview = content[:30] + "..." if len(content) > 30 else content
        print(f"  {status} {preview}: {error if error else 'Valid'}")