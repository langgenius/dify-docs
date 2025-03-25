#!/usr/bin/env python3
"""
Mintlify图片格式转换工具

这个脚本用于扫描dify-docs-mintlify目录中的所有.mdx文件，
并将<Frame>标签中的图片转换为标准Markdown格式。

转换前:
<Frame caption="示例标题">
  <img src="https://assets-docs.dify.ai/example.png" alt="示例" />
</Frame>

转换后:
![示例](https://assets-docs.dify.ai/example.png)
"""

import os
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional

# 颜色代码，用于美化终端输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 匹配Frame标签中的图片
FRAME_IMG_PATTERN = re.compile(r'<Frame(?:\s+caption="([^"]*)")?\s*>\s*<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*/?>\s*</Frame>', re.DOTALL)

def convert_frame_to_markdown(content: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    将Frame标签中的图片转换为Markdown格式
    
    Args:
        content: 文件内容
        
    Returns:
        Tuple[转换后的内容, 替换记录列表]
    """
    replacements = []
    
    def replace_frame(match):
        caption = match.group(1) or ""
        src = match.group(2)
        alt = match.group(3) or caption or ""
        
        # 原始内容
        original = match.group(0)
        
        # 转换为Markdown格式
        markdown = f"![{alt}]({src})"
        
        # 记录替换
        replacements.append((original, markdown))
        
        return markdown
    
    # 执行替换
    new_content = FRAME_IMG_PATTERN.sub(replace_frame, content)
    
    return new_content, replacements

def process_file(file_path: str, dry_run: bool = False) -> Tuple[int, List[Tuple[str, str]]]:
    """
    处理单个文件
    
    Args:
        file_path: 文件路径
        dry_run: 是否只预览修改而不实际写入
        
    Returns:
        Tuple[替换的数量, 替换记录列表]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换内容
        new_content, replacements = convert_frame_to_markdown(content)
        
        # 如果有修改且不是预览模式，写入文件
        if replacements and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return len(replacements), replacements
    except Exception as e:
        print(f"{Colors.FAIL}处理文件时出错 {file_path}: {e}{Colors.ENDC}")
        return 0, []

def scan_directory(dir_path: str, dry_run: bool = False, extensions: List[str] = ['.mdx']) -> Tuple[int, int, int]:
    """
    扫描目录并处理文件
    
    Args:
        dir_path: 目录路径
        dry_run: 是否只预览修改而不实际写入
        extensions: 要处理的文件扩展名列表
        
    Returns:
        Tuple[处理的文件数, 包含Frame的文件数, 替换的总数]
    """
    file_count = 0
    modified_file_count = 0
    total_replacements = 0
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                
                # 处理文件
                count, replacements = process_file(file_path, dry_run)
                
                file_count += 1
                if count > 0:
                    rel_path = os.path.relpath(file_path, dir_path)
                    print(f"\n{Colors.CYAN}文件: {rel_path}{Colors.ENDC}")
                    print(f"{Colors.GREEN}找到 {count} 个需要转换的图片{Colors.ENDC}")
                    
                    # 显示替换详情
                    for i, (original, markdown) in enumerate(replacements):
                        # 为了简洁，截断过长的内容
                        orig_short = original[:100] + "..." if len(original) > 100 else original
                        print(f"  {i+1}. {Colors.WARNING}{orig_short}{Colors.ENDC}")
                        print(f"     -> {Colors.GREEN}{markdown}{Colors.ENDC}")
                    
                    modified_file_count += 1
                    total_replacements += count
    
    return file_count, modified_file_count, total_replacements

def main():
    """主程序入口"""
    # 确定默认目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dir = os.path.dirname(script_dir)  # dify-docs-mintlify
    
    # 显示欢迎信息
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER} Mintlify图片格式转换工具 {Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    # 参数处理
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("\n使用方法:")
            print("  python convert_image_format.py [目录路径] [选项]")
            print("\n选项:")
            print("  --dry-run    仅预览修改，不实际写入")
            print("  --help, -h   显示此帮助信息")
            return
            
        if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
            target_dir = sys.argv[1]
        else:
            print(f"{Colors.FAIL}错误: 无效的目录路径: {sys.argv[1]}{Colors.ENDC}")
            return
    else:
        # 使用默认目录
        target_dir = default_dir
    
    # 检查是否为预览模式
    dry_run = '--dry-run' in sys.argv
    
    print(f"目标目录: {target_dir}")
    print(f"预览模式: {'是' if dry_run else '否'}\n")
    
    # 确认操作
    if not dry_run:
        response = input(f"{Colors.BOLD}这将修改所有.mdx文件中的图片格式。确认继续? (y/n): {Colors.ENDC}")
        if response.lower() != 'y':
            print(f"{Colors.BLUE}操作已取消{Colors.ENDC}")
            return
    
    # 开始处理
    start_time = time.time()
    file_count, modified_file_count, total_replacements = scan_directory(target_dir, dry_run)
    end_time = time.time()
    
    # 显示总结
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.GREEN}处理完成! 耗时: {end_time - start_time:.2f}秒{Colors.ENDC}")
    print(f"{Colors.GREEN}扫描了 {file_count} 个文件{Colors.ENDC}")
    print(f"{Colors.GREEN}修改了 {modified_file_count} 个文件中的 {total_replacements} 处图片格式{Colors.ENDC}")
    
    if dry_run:
        print(f"\n{Colors.BLUE}这是预览模式，没有实际写入修改。{Colors.ENDC}")
        print(f"{Colors.BLUE}如需实际应用修改，请去掉 --dry-run 选项重新运行脚本。{Colors.ENDC}")

if __name__ == "__main__":
    main()
