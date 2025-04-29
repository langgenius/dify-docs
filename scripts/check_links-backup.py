#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Checker for Markdown/MDX files

This script checks both online links and relative file paths in markdown files.
It verifies that online links are accessible and that relative paths exist in the filesystem.
"""

import re
import requests
import os
from pathlib import Path
import concurrent.futures
import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

class LinkChecker:
    def __init__(self, base_dir, timeout=10, max_workers=10):
        self.base_dir = Path(base_dir)
        self.timeout = timeout
        self.max_workers = max_workers
        self.results = {"valid": [], "invalid": [], "skipped": []}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def extract_links_from_markdown(self, file_path):
        """Extract all links from a Markdown/MDX file, with line and column info"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        link_infos = []
        # Markdown links [text](url)
        for match in re.finditer(r'\[.*?\]\((.*?)\)', content):
            url = match.group(1)
            start = match.start(1)
            line = content.count('\n', 0, start) + 1
            col = start - content.rfind('\n', 0, start)
            link_infos.append((url, line, col))
        # HTML links <a href="url">
        for match in re.finditer(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', content):
            url = match.group(1)
            start = match.start(1)
            line = content.count('\n', 0, start) + 1
            col = start - content.rfind('\n', 0, start)
            link_infos.append((url, line, col))
        return link_infos
    
    def is_external_link(self, url):
        """Check if a link is an external URL"""
        return url.startswith(('http://', 'https://', 'ftp://'))
    
    def is_anchor_link(self, url):
        """Check if a link is a page anchor"""
        return url.startswith('#')
    
    def is_mail_link(self, url):
        """Check if a link is a mailto link"""
        return url.startswith('mailto:')
    
    def check_online_link(self, link):
        """Check if an online link is accessible"""
        try:
            response = requests.head(link, allow_redirects=True, timeout=self.timeout, headers=self.headers)
            
            # If HEAD request fails, try GET request
            if response.status_code >= 400:
                response = requests.get(link, timeout=self.timeout, headers=self.headers)
            
            if response.status_code < 400:
                return (link, True, f"HTTP {response.status_code}")
            else:
                return (link, False, f"HTTP {response.status_code}")
        except requests.exceptions.Timeout:
            return (link, False, "Timeout")
        except requests.exceptions.ConnectionError:
            return (link, False, "Connection Error")
        except Exception as e:
            return (link, False, str(e))
    
    def check_local_path(self, link, file_path):
        """Check if a local file path exists"""
        try:
            current_file_dir = Path(file_path).parent
            
            # Handle different types of relative paths
            if link.startswith('/'):
                # Path relative to the base directory (remove leading '/')
                target_path = self.base_dir / link.lstrip('/')
            else:
                # Path relative to the current file
                target_path = (current_file_dir / link).resolve()
            
            # Handle paths without extensions (try adding .mdx or .md)
            if not os.path.splitext(link)[1]:
                # Path has no extension, try adding .mdx or .md
                if target_path.with_suffix('.mdx').exists():
                    return (link, True, str(target_path.with_suffix('.mdx')))
                elif target_path.with_suffix('.md').exists():
                    return (link, True, str(target_path.with_suffix('.md')))
                else:
                    # Check if the directory exists
                    if target_path.exists() and target_path.is_dir():
                        # Check for index.mdx or index.md in the directory
                        if (target_path / 'index.mdx').exists():
                            return (link, True, str(target_path / 'index.mdx'))
                        elif (target_path / 'index.md').exists():
                            return (link, True, str(target_path / 'index.md'))
            
            # Check if the path exists directly
            if target_path.exists():
                return (link, True, str(target_path))
            else:
                return (link, False, f"File not found: {target_path}")
                
        except Exception as e:
            return (link, False, str(e))
    
    def check_link(self, link, file_path):
        """Check a link based on its type"""
        if self.is_external_link(link):
            return self.check_online_link(link)
        elif self.is_anchor_link(link) or self.is_mail_link(link):
            return (link, None, "Skipped (anchor or mail link)")
        else:
            return self.check_local_path(link, file_path)
    
    def check_links_in_file(self, file_path):
        """Check all links in a file, with line/col info"""
        link_infos = self.extract_links_from_markdown(file_path)
        print(f"Found {len(link_infos)} links in {file_path}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_info = {executor.submit(self.check_link, url, file_path): (url, line, col) for url, line, col in link_infos}
            for future in concurrent.futures.as_completed(future_to_info):
                url, line, col = future_to_info[future]
                link, is_valid, status = future.result()
                if is_valid is None:
                    self.results["skipped"].append((link, status, file_path, line, col))
                elif is_valid:
                    self.results["valid"].append((link, status, file_path, line, col))
                else:
                    self.results["invalid"].append((link, status, file_path, line, col))
    
    def print_report(self):
        """Print a colored report of the link check results, with file/line info for invalid links"""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}LINK CHECKER REPORT{Style.RESET_ALL}")
        print("="*60)
        print(f"\n{Fore.GREEN}✅ Valid Links ({len(self.results['valid'])}):{Style.RESET_ALL}")
        for link, status, file_path, line, col in self.results["valid"]:
            print(f"  - {link} -> {status} ({file_path}:{line}:{col})")
        print(f"\n{Fore.RED}❌ Invalid Links ({len(self.results['invalid'])}):{Style.RESET_ALL}")
        for link, status, file_path, line, col in self.results["invalid"]:
            # Cursor/VSCode 终端友好格式
            print(f"{file_path}:{line}:{col}: {Fore.RED}无效链接: {link} -> {status}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}⏩ Skipped Links ({len(self.results['skipped'])}):{Style.RESET_ALL}")
        for link, reason, file_path, line, col in self.results["skipped"]:
            print(f"  - {link} ({reason}) ({file_path}:{line}:{col})")
        print("\n" + "-"*60)
        print(f"{Fore.CYAN}SUMMARY:{Style.RESET_ALL}")
        print(f"Total links: {len(self.results['valid']) + len(self.results['invalid']) + len(self.results['skipped'])}")
        print(f"{Fore.GREEN}Valid: {len(self.results['valid'])}{Style.RESET_ALL}")
        print(f"{Fore.RED}Invalid: {len(self.results['invalid'])}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Skipped: {len(self.results['skipped'])}{Style.RESET_ALL}")
        print("-"*60)
    
    def check_links_in_directory(self, directory, file_pattern="*.md*"):
        """Check links in all markdown files in a directory (md/mdx)"""
        mdx_files = list(Path(directory).glob(f"**/{file_pattern}"))
        print(f"Found {len(mdx_files)} {file_pattern} files in {directory}")
        for file_path in mdx_files:
            print(f"\nChecking {file_path}...")
            self.check_links_in_file(file_path)

def main():
    parser = argparse.ArgumentParser(description='Check links in markdown files')
    parser.add_argument('path', nargs='?', default=None, help='Path to the markdown file or directory to check')
    parser.add_argument('--base-dir', help='Base directory for resolving relative paths (default: parent dir of the file)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout for HTTP requests in seconds (default: 10)')
    parser.add_argument('--workers', type=int, default=10, help='Number of worker threads (default: 10)')
    parser.add_argument('--pattern', default="*.mdx", help='File pattern to match when checking directories (default: *.mdx)')
    
    args = parser.parse_args()
    
    # 新增：如果没有传入 path，则提示输入
    if not args.path:
        args.path = input("请输入要检查的文件或目录路径: ").strip()
    
    file_path = Path(args.path)
    if not file_path.exists():
        print(f"{Fore.RED}Error: Path '{args.path}' does not exist{Style.RESET_ALL}")
        return 1
    
    # If base_dir is not specified, use parent of parent directory (for typical docs structure)
    if args.base_dir:
        base_dir = args.base_dir
    elif file_path.is_file():
        base_dir = file_path.parent.parent
    else:
        base_dir = file_path
    
    checker = LinkChecker(
        base_dir=base_dir,
        timeout=args.timeout,
        max_workers=args.workers
    )
    
    print(f"Base directory: {base_dir}")
    
    if file_path.is_file():
        print(f"Checking links in file: {file_path}")
        checker.check_links_in_file(file_path)
    else:
        print(f"Checking links in directory: {file_path}")
        checker.check_links_in_directory(file_path, args.pattern)
    
    checker.print_report()
    
    # Return non-zero exit code if invalid links were found
    return 1 if checker.results["invalid"] else 0

if __name__ == "__main__":
    sys.exit(main())
