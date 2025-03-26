#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Set
import time
import sys

# 颜色代码，用于终端输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(message):
    """输出信息日志"""
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} {message}")

def log_warning(message):
    """输出警告日志"""
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {message}")

def log_error(message):
    """输出错误日志"""
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")

def log_success(message):
    """输出成功日志"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} {message}")

def find_all_md_files(base_dir: str) -> List[Path]:
    """查找指定目录下的所有 .md 和 .mdx 文件"""
    md_files = []
    base_path = Path(base_dir)
    
    for ext in ["*.md", "*.mdx"]:
        md_files.extend(base_path.glob(f"**/{ext}"))
    
    return md_files

def extract_links(file_content: str) -> List[Tuple[str, str, str]]:
    """从文件内容中提取所有链接
    返回格式: [(完整匹配文本, 链接文本, 链接URL)]
    """
    links = []
    
    # 提取 Markdown 链接 [text](url)
    md_links = re.findall(r'\[(.*?)\]\((.*?)\)', file_content)
    for text, url in md_links:
        full_match = f"[{text}]({url})"
        links.append((full_match, text, url))
    
    # 提取 <a> 标签链接
    a_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>(.*?)<\/a>', file_content)
    for url, text in a_links:
        full_match = f'<a href="{url}">{text}</a>'
        links.append((full_match, text, url))
    
    # 提取 Mintlify Card 组件链接
    card_links = re.findall(r'<Card\s+title="([^"]*)"[^>]*\s+href="([^"]*)"[^>]*>(.*?)<\/Card>', file_content, re.DOTALL)
    for title, url, content in card_links:
        full_match = f'<Card title="{title}" href="{url}">{content}</Card>'
        links.append((full_match, title, url))
    
    return links

def check_link_extensions(links: List[Tuple[str, str, str]], 
                         file_path: Path, 
                         all_files: Dict[str, Path], 
                         base_dir: Path) -> List[Tuple[str, str, str, str]]:
    """检查链接是否包含不需要的扩展名
    返回格式: [(完整匹配文本, 链接文本, 原始URL, 修复后URL)]
    """
    issues = []
    
    for full_match, text, url in links:
        # 忽略外部链接和锚点链接
        if url.startswith(('http://', 'https://', '#', 'mailto:', 'tel:')):
            continue
        
        # 忽略以 / 开头的绝对路径
        if url.startswith('/'):
            continue
            
        # 检查链接是否包含 .md 或 .mdx 扩展名
        if url.endswith('.md') or url.endswith('.mdx'):
            # 计算修复后的 URL
            fixed_url = url.rsplit('.', 1)[0]
            issues.append((full_match, text, url, fixed_url))
    
    return issues

def fix_links(file_path: Path, issues: List[Tuple[str, str, str, str]], dry_run: bool = True) -> bool:
    """修复文件中的链接问题
    
    Args:
        file_path: 文件路径
        issues: 需要修复的问题列表 [(完整匹配文本, 链接文本, 原始URL, 修复后URL)]
        dry_run: 如果为 True，只显示将要进行的修改，不实际修改文件
        
    Returns:
        bool: 是否进行了修改
    """
    if not issues:
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = content
    
    # 遍历所有问题并修复
    for full_match, text, old_url, new_url in issues:
        if "Card" in full_match:
            # 修复 Card 组件链接
            old_pattern = f'href="{old_url}"'
            new_pattern = f'href="{new_url}"'
            modified_content = modified_content.replace(old_pattern, new_pattern)
        elif "<a" in full_match:
            # 修复 <a> 标签链接
            old_pattern = f'href="{old_url}"'
            new_pattern = f'href="{new_url}"'
            modified_content = modified_content.replace(old_pattern, new_pattern)
        else:
            # 修复 Markdown 链接
            old_pattern = f']({old_url})'
            new_pattern = f']({new_url})'
            modified_content = modified_content.replace(old_pattern, new_pattern)
    
    # 如果内容有变化，写回文件
    if modified_content != content and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        return True
    
    return not dry_run and modified_content != content

def process_file(file_path: Path, all_files: Dict[str, Path], base_dir: Path, args):
    """处理单个文件中的链接问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links(content)
        issues = check_link_extensions(links, file_path, all_files, base_dir)
        
        if issues:
            rel_path = file_path.relative_to(base_dir)
            print(f"\n{Colors.HEADER}{Colors.BOLD}检查文件: {rel_path}{Colors.ENDC}")
            
            for i, (full_match, text, old_url, new_url) in enumerate(issues, 1):
                print(f"  {i}. 发现问题: {Colors.WARNING}{old_url}{Colors.ENDC} -> {Colors.GREEN}{new_url}{Colors.ENDC}")
            
            # 询问用户是否修复
            if not args.auto_fix:
                choice = input(f"\n{Colors.BOLD}修复这些问题? (y/n/a/q): {Colors.ENDC}")
                if choice.lower() == 'q':  # q 代表退出脚本
                    log_info("用户请求退出脚本")
                    sys.exit(0)
                elif choice.lower() == 'a':  # a 代表全部修复，并设置 auto_fix 标志
                    args.auto_fix = True
                
                if choice.lower() not in ('y', 'a'):
                    log_info(f"跳过修复 {rel_path}")
                    return False
            
            # 修复问题
            fixed = fix_links(file_path, issues, dry_run=args.dry_run)
            
            if args.dry_run:
                log_info(f"已检测到 {len(issues)} 个需要修复的链接 (模拟运行，实际未修改)")
            elif fixed:
                log_success(f"已修复 {len(issues)} 个链接问题")
            
            # 如果不是自动修复模式，在每个文件处理完后暂停一下，让用户有时间查看结果
            if not args.auto_fix and fixed and not args.dry_run:
                input(f"\n{Colors.BOLD}已完成修复，按回车继续下一个文件...{Colors.ENDC}")
            
            return fixed
        
        return False
    
    except Exception as e:
        log_error(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='检查并修复文档中的链接问题')
    parser.add_argument('doc_path', nargs='?', help='文档根目录路径')
    parser.add_argument('--dry-run', action='store_true', help='只显示将要修改的内容，不实际修改文件')
    parser.add_argument('--auto-fix', action='store_true', help='自动修复所有问题，不询问')
    args = parser.parse_args()
    
    # 如果命令行未提供路径，则交互式询问
    if args.doc_path is None:
        doc_path = input(f"{Colors.BOLD}请输入文档根目录路径: {Colors.ENDC}")
        args.doc_path = doc_path.strip()
    
    base_dir = Path(args.doc_path)
    
    if not base_dir.exists() or not base_dir.is_dir():
        log_error(f"指定的目录 '{args.doc_path}' 不存在或不是一个目录")
        return 1
    
    # 添加确认步骤
    print(f"\n{Colors.BOLD}将要扫描的目录:{Colors.ENDC} {Colors.GREEN}{base_dir}{Colors.ENDC}")
    if args.dry_run:
        print(f"{Colors.BOLD}模式:{Colors.ENDC} {Colors.BLUE}仅检查，不修改文件{Colors.ENDC}")
    elif args.auto_fix:
        print(f"{Colors.BOLD}模式:{Colors.ENDC} {Colors.BLUE}自动修复所有问题{Colors.ENDC}")
    else:
        print(f"{Colors.BOLD}模式:{Colors.ENDC} {Colors.BLUE}交互式修复{Colors.ENDC}")
    
    confirm = input(f"\n{Colors.BOLD}确认开始扫描? (y/n): {Colors.ENDC}")
    if confirm.lower() != 'y':
        log_info("操作已取消")
        return 0
    
    log_info(f"开始扫描目录: {base_dir}")
    
    # 查找所有文档文件
    all_files_list = find_all_md_files(base_dir)
    log_info(f"共找到 {len(all_files_list)} 个文档文件")
    
    # 创建文件路径映射，用于链接验证
    all_files = {}
    for file_path in all_files_list:
        rel_path = file_path.relative_to(base_dir)
        all_files[str(rel_path)] = file_path
    
    # 处理所有文件
    fixed_count = 0
    total_files = len(all_files_list)
    
    try:
        for i, file_path in enumerate(all_files_list, 1):
            # 清空当前行并显示进度
            sys.stdout.write("\r" + " " * 80)  # 清空当前行
            sys.stdout.write(f"\r{Colors.BOLD}进度: {i}/{total_files} ({i/total_files*100:.1f}%){Colors.ENDC}")
            sys.stdout.flush()
            
            # 处理文件，如果有修复则增加计数
            if process_file(file_path, all_files, base_dir, args):
                fixed_count += 1
    except KeyboardInterrupt:
        print("\n")
        log_warning("用户中断了处理过程")
        # 继续执行后面的代码，显示已完成的统计信息
    
    print("\n")
    log_info(f"扫描完成，共处理 {total_files} 个文件")
    
    if args.dry_run:
        log_info(f"发现 {fixed_count} 个文件中有链接问题需要修复")
    else:
        log_success(f"已修复 {fixed_count} 个文件中的链接问题")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())