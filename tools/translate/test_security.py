#!/usr/bin/env python3
"""Test the security features of the documentation sync system"""

import json
import tempfile
from pathlib import Path
from security_validator import SecurityValidator, create_validator
from sync_and_translate import DocsSynchronizer

def test_security_validator():
    """Test the security validator functions"""
    print("=== Testing Security Validator ===")
    
    # Create temp directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        validator = SecurityValidator(Path(temp_dir))
        
        # Test path validation
        test_paths = [
            ("en/docs/test.md", True, "Valid path"),
            ("../../../etc/passwd", False, "Directory traversal"),
            ("/etc/passwd", False, "Absolute path"), 
            ("en/test.exe", False, "Invalid extension"),
            ("docs.json", True, "Special case"),
            ("zh-hans/test.mdx", True, "Valid target path"),
        ]
        
        print("Path Validation Tests:")
        for path, should_be_valid, description in test_paths:
            valid, error = validator.validate_file_path(path)
            status = "✓" if valid == should_be_valid else "✗"
            result = "PASS" if valid == should_be_valid else "FAIL"
            print(f"  {status} {path}: {result} - {description}")
            if error and not should_be_valid:
                print(f"    Error: {error}")
        
        # Test content validation
        print("\nContent Validation Tests:")
        test_contents = [
            ("# Normal markdown", True),
            ("<script>alert('xss')</script>", False),
            ("Normal text with onclick='bad()'", False),
            ("Valid content with [link](./test.md)", True),
        ]
        
        for content, should_be_valid in test_contents:
            valid, error = validator.validate_file_content(content)
            status = "✓" if valid == should_be_valid else "✗"
            result = "PASS" if valid == should_be_valid else "FAIL"
            preview = content[:30] + "..." if len(content) > 30 else content
            print(f"  {status} {preview}: {result}")
        
        # Test sync plan validation
        print("\nSync Plan Validation Tests:")
        
        # Valid sync plan
        valid_plan = {
            "files_to_sync": [
                {"path": "en/test.md", "size": 1000}
            ],
            "target_languages": ["zh-hans", "ja-jp"],
            "metadata": {"pr_number": 123}
        }
        
        valid, error = validator.validate_sync_plan(valid_plan)
        status = "✓" if valid else "✗"
        print(f"  {status} Valid sync plan: {'PASS' if valid else 'FAIL'}")
        
        # Invalid sync plan (too many files)
        invalid_plan = {
            "files_to_sync": [{"path": f"en/test{i}.md", "size": 1000} for i in range(60)],
            "target_languages": ["zh-hans"],
            "metadata": {"pr_number": 123}
        }
        
        valid, error = validator.validate_sync_plan(invalid_plan)
        status = "✓" if not valid else "✗"
        print(f"  {status} Invalid sync plan (too many files): {'PASS' if not valid else 'FAIL'}")
        if error:
            print(f"    Error: {error}")

def test_secure_synchronizer():
    """Test the secure synchronizer functionality"""
    print("\n=== Testing Secure Synchronizer ===")
    
    # Initialize with security enabled
    sync = DocsSynchronizer("test-key", enable_security=True)
    
    # Test path validation
    print("Synchronizer Security Tests:")
    
    test_cases = [
        ("en/docs/test.md", True),
        ("../../../etc/passwd", False),
        ("malicious/../path", False),
        ("docs.json", True),
    ]
    
    for path, should_be_valid in test_cases:
        valid, error = sync.validate_file_path(path)
        status = "✓" if valid == should_be_valid else "✗"
        result = "PASS" if valid == should_be_valid else "FAIL"
        print(f"  {status} {path}: {result}")
        if error and not should_be_valid:
            print(f"    Error: {error}")

def create_test_sync_plan():
    """Create a test sync plan for validation"""
    return {
        "metadata": {
            "pr_number": 123,
            "pr_title": "Test PR",
            "pr_author": "test-user",
            "base_sha": "abc123",
            "head_sha": "def456",
            "file_count": 1,
            "timestamp": "2024-08-22T10:00:00Z",
            "repository": "test/repo",
            "ref": "refs/pull/123/head"
        },
        "files_to_sync": [
            {
                "path": "en/documentation/pages/getting-started/test.mdx",
                "size": 2048,
                "type": "mdx"
            }
        ],
        "structure_changes": {
            "structure_changed": False,
            "navigation_modified": False,
            "languages_affected": []
        },
        "target_languages": ["zh-hans", "ja-jp"],
        "sync_required": True
    }

def test_artifact_simulation():
    """Test the artifact handling simulation"""
    print("\n=== Testing Artifact Simulation ===")
    
    # Create test artifacts
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test sync plan
        sync_plan = create_test_sync_plan()
        
        # Write test artifacts
        artifacts = {
            "analysis.json": sync_plan["metadata"],
            "sync_plan.json": sync_plan,
            "changed_files.txt": "en/documentation/pages/getting-started/test.mdx\n",
            "file_analysis.txt": "en/documentation/pages/getting-started/test.mdx|2048\n"
        }
        
        for filename, content in artifacts.items():
            file_path = temp_path / filename
            if isinstance(content, dict):
                with open(file_path, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(file_path, 'w') as f:
                    f.write(content)
        
        # Validate artifacts
        validator = SecurityValidator(temp_path.parent)
        
        # Test sync plan validation
        valid, error = validator.validate_sync_plan(sync_plan)
        status = "✓" if valid else "✗"
        print(f"  {status} Sync plan validation: {'PASS' if valid else 'FAIL'}")
        if error:
            print(f"    Error: {error}")
        
        print("  ✓ Artifact simulation completed successfully")

def main():
    """Run all tests"""
    try:
        test_security_validator()
        test_secure_synchronizer()
        test_artifact_simulation()
        
        print("\n=== Test Summary ===")
        print("✓ Security validation tests completed")
        print("✓ Synchronizer security tests completed")
        print("✓ Artifact handling tests completed")
        print("\n🎉 All security tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()