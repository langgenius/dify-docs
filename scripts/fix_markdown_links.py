#!/usr/bin/env python3
"""
This script automatically fixes relative path references in Markdown files.
It searches for links to .md and .mdx files and replaces them with the correct format
for Mintlify documentation, changing links like [text](file.md) or [text](file.mdx) to [text](./file).

使用方法：
1. 在命令行中运行： python fix_markdown_links.py [directory]
2. 如果不提供目录参数，将使用当前工作目录

脚本会递归扫描目录中的所有.md和.mdx文件，并自动修正链接路径：
- 移除.md和.mdx文件后缀
- 为同级目录文件引用添加./前缀
- 正确处理相对路径和锚点
"""

import os
import re
import sys
import time
from pathlib import Path

# 开始计时
start_time = time.time()

# 正则表达式来匹配Markdown链接引用，支持.md和.mdx文件
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+\.(md|mdx))(?:#[^)]*)?\)')

# 是否应该处理这个文件的配置
def should_process_file(file_path):
    """检查指定文件是否应该处理"""
    # 使用绝对路径
    abs_path = os.path.abspath(file_path)
    
    # 跳过特定目录，如.git目录
    if any(segment.startswith('.') and segment != '..' for segment in abs_path.split(os.sep)):
        if '.git' in abs_path.split(os.sep):
            return False
    
    return True

def is_valid_path(path):
    """检查给定的路径是否有效（不包含无效字符）"""
    return not any(char in path for char in ['<', '>', ':', '"', '|', '?', '*'])

def fix_md_links(content, source_path, root_dir):
    """
    修复内容中的Markdown链接
    
    Args:
        content (str): 文件内容
        source_path (Path): 源文件路径
        root_dir (Path): 项目根目录路径
        
    Returns:
        str: 修改后的内容
        int: 修改的链接数量
    """
    changes = 0
    source_dir = source_path.parent
    
    def replace_link(match):
        nonlocal changes
        
        link_text = match.group(1)
        link_path = match.group(2)
        fragment = ''
        
        # 检查是否有锚点（#section）
        if '#' in link_path:
            link_path, fragment = link_path.split('#', 1)
            fragment = f'#{fragment}'
        
        # 跳过外部链接
        if link_path.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
            return match.group(0)
        
        # 如果链接路径无效，保留原样
        if not is_valid_path(link_path):
            print(f"  警告: 在 {source_path} 中发现无效链接路径: {link_path}")
            return match.group(0)
        
        # 移除.md或.mdx后缀
        if link_path.endswith(('.md', '.mdx')):
            # 获取文件后缀
            extension = '.md' if link_path.endswith('.md') else '.mdx'
            # 移除后缀
            link_path = link_path[:-len(extension)]
        
        # 解析链接路径
        if link_path.startswith('/'):
            # 绝对路径（从项目根开始）
            abs_target_path = root_dir / link_path.lstrip('/')
            rel_path = os.path.relpath(abs_target_path, source_dir)
        elif link_path.startswith(('./', '../')):
            # 已经是相对路径
            rel_path = link_path
        else:
            # 同级目录，添加./前缀
            rel_path = f'./{link_path}'
        
        # 构建新的链接
        new_link = f'[{link_text}]({rel_path}{fragment})'
        
        if new_link != match.group(0):
            changes += 1
            print(f"  修改: {match.group(0)} -> {new_link}")
        
        return new_link
    
    # 替换所有匹配的链接
    new_content = MD_LINK_PATTERN.sub(replace_link, content)
    
    return new_content, changes



def scan_directory(dir_path, root_dir, extensions=['.mdx', '.md']):
    """扫描目录及其子目录中的Markdown文件"""
    file_count = 0
    modified_count = 0
    total_links_modified = 0
    
    for root, dirs, files in os.walk(dir_path):
        # 跳过.git等特殊目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                
                # 检查文件是否应该处理
                if not should_process_file(file_path):
                    continue
                
                try:
                    # 记录当前修改计数
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    original_links = MD_LINK_PATTERN.findall(content)
                    
                    if not original_links:
                        # 没有需要处理的链接，跳过
                        continue
                    
                    # 附加路径显示为相对根目录的路径
                    rel_file_path = os.path.relpath(file_path, str(root_dir))
                    print(f"处理文件: {rel_file_path} (有 {len(original_links)} 个链接)")
                    
                    # 处理文件
                    try:
                        new_content, changes = fix_md_links(content, Path(file_path), root_dir)
                        
                        if changes > 0:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"  已修改 {changes} 个链接")
                            total_links_modified += changes
                            modified_count += 1
                        else:
                            print("  无需修改的链接")
                    except Exception as e:
                        print(f"  处理文件时出错: {e}")
                    
                    file_count += 1
                except Exception as e:
                    print(f"  跳过文件 {file_path}: {e}")
    
    return file_count, modified_count, total_links_modified

def main():
    """程序入口点"""
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        # 默认使用当前工作目录作为根目录
        root_dir = os.getcwd()
    
    root_dir = Path(root_dir)
    print(f"开始处理目录: {root_dir}")
    print("-" * 50)
    
    file_count, modified_count, total_links_modified = scan_directory(root_dir, root_dir)
    
    # 计算运行时间
    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 50)
    print(f"\n处理完成!")
    print(f"共处理 {file_count} 个文件，修改了 {modified_count} 个文件中的 {total_links_modified} 个链接引用")
    print(f"总耗时: {duration:.2f} 秒")
    
    if modified_count > 0:
        print("\n修改的文件中的链接现在符合Mintlify格式要求:")
        print("  - 移除了.md和.mdx文件后缀")
        print("  - 为同级目录文件引用添加了./前缀")
        print("  - 保留了锚点引用")
    else:
        print("\n没有发现需要修改的文件")

if __name__ == "__main__":
    main()
