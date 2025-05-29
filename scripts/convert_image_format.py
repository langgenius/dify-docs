#!/usr/bin/env python3
"""
Mintlify图片格式转换工具

这个脚本用于扫描dify-docs目录中的所有.mdx文件，
并将<Frame>标签中的图片转换为标准Markdown格式或HTML格式。

支持以下转换:
1. 基本Frame转Markdown:
   <Frame caption="标题">
     <img src="https://example.com/image.png" alt="描述" />
   </Frame>
   
   转换为:
   ![描述](https://example.com/image.png)

2. 带自闭合标签的Frame:
   <Frame>
     <img src="https://example.com/image.png" alt="" / >
   </Frame>
   
   转换为:
   ![](https://example.com/image.png)

3. 带宽度的Frame转HTML:
   <Frame caption="标题" width="369">
     <img src="https://example.com/image.png" alt="描述" />
   </Frame>
   
   转换为:
   <img
   src="https://example.com/image.png"
   width="369"
   className="mx-auto"
   alt="描述"
   />
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

# 匹配Frame标签中的图片，处理多种情况:
# 1. 标准Frame标签: <Frame>...<img src="..." alt="..." />...</Frame>
# 2. 特殊结束的img标签: <Frame>...<img src="..." alt="" / >...</Frame>
# 3. 支持特殊字符和空格
FRAME_IMG_PATTERN = re.compile(
    r'<Frame(?:\s+caption="([^"]*)")?(?:\s+width="([^"]*)")?\s*>\s*'
    r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*(?:\/\s*>|\/ >|>\s*<\/img>)\s*'
    r'<\/Frame>', 
    re.DOTALL
)

# 另一种每行写一个属性的格式，更付特征，匹配如
# <img
# src="https://example.com/image.png"
# width="369"
# className="mx-auto"
# alt="metadata_field"
# />
HTML_IMG_PATTERN = re.compile(
    r'<img\s*\n\s*src="([^"]+)"\s*\n\s*(?:width="([^"]+)"\s*\n\s*)?(?:className="[^"]*"\s*\n\s*)?(?:alt="([^"]*)"\s*\n\s*)?\/>',
    re.DOTALL
)

def convert_frame_to_markdown(content: str) -> Tuple[str, List[Tuple[str, str, str]]]:
    """
    将Frame标签中的图片转换为Markdown或HTML格式
    
    Args:
        content: 文件内容
        
    Returns:
        Tuple[转换后的内容, 替换记录列表]
    """
    replacements = []
    
    def replace_frame(match):
        caption = match.group(1) or ""
        width = match.group(2)  # 可能为None
        src = match.group(3)
        alt = match.group(4) or caption or ""
        
        # 原始内容
        original = match.group(0)
        
        # 转换格式
        if width:
            # 带宽度的转为HTML格式
            new_format = "HTML"
            markdown = f"""<img
src="{src}"
width="{width}"
className="mx-auto"
alt="{alt}"
/>"""
        else:
            # 不带宽度的转为Markdown格式
            new_format = "Markdown"
            markdown = f"![{alt}]({src})"
        
        # 记录替换
        replacements.append((original, markdown, new_format))
        
        return markdown
    
    # 先处理Frame标签
    new_content = FRAME_IMG_PATTERN.sub(replace_frame, content)
    
    # 再处理HTML格式的img标签
    def replace_html_img(match):
        src = match.group(1)
        width = match.group(2)  # 可能为None
        alt = match.group(3) or ""
        
        # 原始内容
        original = match.group(0)
        
        # HTML格式的图片保持为HTML格式，但直接转为Markdown
        new_format = "Markdown"
        markdown = f"![{alt}]({src})"
        
        # 记录替换
        replacements.append((original, markdown, new_format))
        
        return markdown
    
    # 处理HTML格式的img标签
    final_content = HTML_IMG_PATTERN.sub(replace_html_img, new_content)
    
    return final_content, replacements

def process_file(file_path: str, dry_run: bool = False, debug: bool = False) -> Tuple[int, List[Tuple[str, str, str]]]:
    """
    处理单个文件
    
    Args:
        file_path: 文件路径
        dry_run: 是否只预览修改而不实际写入
        debug: 是否显示调试信息
        
    Returns:
        Tuple[替换的数量, 替换记录列表]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if debug:
            # 直接检查正则达式匹配
            frame_matches = FRAME_IMG_PATTERN.findall(content)
            html_matches = HTML_IMG_PATTERN.findall(content)
            
            print(f"\n{Colors.CYAN}匹配结果调试信息:{Colors.ENDC}")
            print(f"在文件 {file_path} 中找到:")
            print(f"- {len(frame_matches)} 个Frame标签中的图片")
            print(f"- {len(html_matches)} 个HTML格式的图片")
            
            # 打印Frame标签匹配
            for i, match in enumerate(frame_matches):
                caption, width, src, alt = match
                print(f"\n  Frame图片 {i+1}:")
                print(f"    caption: '{caption}'")
                print(f"    width: '{width}'")
                print(f"    src: '{src}'")
                print(f"    alt: '{alt}'")
                
                # 显示原始文本片段
                pattern_matches = list(FRAME_IMG_PATTERN.finditer(content))
                if i < len(pattern_matches):
                    orig_text = pattern_matches[i].group(0)
                    print(f"    原始文本: '{orig_text[:100]}...'")
            
            # 打印HTML图片匹配
            for i, match in enumerate(html_matches):
                src, width, alt = match
                print(f"\n  HTML图片 {i+1}:")
                print(f"    src: '{src}'")
                print(f"    width: '{width}'")
                print(f"    alt: '{alt}'")
                
                # 显示原始文本片段
                pattern_matches = list(HTML_IMG_PATTERN.finditer(content))
                if i < len(pattern_matches):
                    orig_text = pattern_matches[i].group(0)
                    print(f"    原始文本: '{orig_text[:100]}...'")
        
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

def scan_directory(dir_path: str, dry_run: bool = False, auto_confirm: bool = False, debug: bool = False, extensions: List[str] = ['.mdx']) -> Tuple[int, int, int, int]:
    """
    扫描目录并处理文件
    
    Args:
        dir_path: 目录路径
        dry_run: 是否只预览修改而不实际写入
        auto_confirm: 是否自动确认所有修改
        debug: 是否显示调试信息
        extensions: 要处理的文件扩展名列表
        
    Returns:
        Tuple[处理的文件数, 修改的文件数, 转为Markdown的数量, 转为HTML的数量]
    """
    file_count = 0
    modified_file_count = 0
    markdown_count = 0
    html_count = 0
    
    for root, dirs, files in os.walk(dir_path):
        # 跳过.git等特殊目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, dir_path)
                
                # 如果不是自动确认模式，则询问是否处理此文件
                if not auto_confirm:
                    print(f"\n{Colors.CYAN}文件 ({file_count+1}): {rel_path}{Colors.ENDC}")
                    response = input(f"{Colors.BOLD}是否处理此文件? (y/n/q-退出): {Colors.ENDC}")
                    if response.lower() == 'n':
                        print(f"{Colors.BLUE}跳过此文件{Colors.ENDC}")
                        file_count += 1
                        continue
                    elif response.lower() == 'q':
                        print(f"{Colors.BLUE}退出处理{Colors.ENDC}")
                        break
                
                # 处理文件
                count, replacements = process_file(file_path, dry_run, debug)
                
                file_count += 1
                if count > 0:
                    rel_path = os.path.relpath(file_path, dir_path)
                    print(f"\n{Colors.CYAN}文件: {rel_path}{Colors.ENDC}")
                    print(f"{Colors.GREEN}找到 {count} 个需要转换的图片{Colors.ENDC}")
                    
                    # 统计转换类型
                    md_count = sum(1 for _, _, fmt in replacements if fmt == "Markdown")
                    html_count = sum(1 for _, _, fmt in replacements if fmt == "HTML")
                    
                    # 显示替换详情
                    for i, (original, converted, format_type) in enumerate(replacements):
                        # 为了简洁，截断过长的内容
                        orig_short = original[:100] + "..." if len(original) > 100 else original
                        print(f"  {i+1}. {Colors.WARNING}[{format_type}] {orig_short}{Colors.ENDC}")
                        print(f"     -> {Colors.GREEN}{converted}{Colors.ENDC}")
                    
                    modified_file_count += 1
                    markdown_count += md_count
                    html_count += html_count
    
    return file_count, modified_file_count, markdown_count, html_count

def main():
    """主程序入口"""
    # 确定默认目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dir = os.path.dirname(script_dir)  # dify-docs
    
    # 显示欢迎信息
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER} Mintlify图片格式转换工具 {Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    # 交互式菜单
    while True:
        print(f"\n{Colors.BOLD}请选择操作模式:{Colors.ENDC}")
        print("1. 处理单个文件")
        print("2. 处理指定目录中的所有文件")
        print("3. 退出")
        
        choice = input(f"{Colors.BOLD}请输入选项 (1-3): {Colors.ENDC}")
        
        if choice == '1':
            # 处理单个文件
            file_path = input(f"{Colors.BOLD}请输入文件路径 (绝对或相对路径): {Colors.ENDC}")
            
            # 如果是相对路径，则基于默认目录
            if not os.path.isabs(file_path):
                file_path = os.path.join(default_dir, file_path)
            
            if not os.path.isfile(file_path):
                print(f"{Colors.FAIL}错误: 文件不存在: {file_path}{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            preview = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 询问是否显示调试信息
            debug = input(f"{Colors.BOLD}是否显示调试信息? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 处理文件
            start_time = time.time()
            count, replacements = process_file(file_path, preview, debug)
            end_time = time.time()
            
            if count > 0:
                # 统计转换类型
                md_count = sum(1 for _, _, fmt in replacements if fmt == "Markdown")
                html_count = sum(1 for _, _, fmt in replacements if fmt == "HTML")
                
                print(f"\n{Colors.GREEN}处理完成! 耗时: {end_time - start_time:.2f}秒{Colors.ENDC}")
                print(f"{Colors.GREEN}发现 {count} 个需要转换的图片:{Colors.ENDC}")
                print(f"{Colors.GREEN}- 转换为Markdown格式: {md_count}{Colors.ENDC}")
                print(f"{Colors.GREEN}- 转换为HTML格式: {html_count}{Colors.ENDC}")
                
                if preview:
                    print(f"\n{Colors.BLUE}这是预览模式，没有实际写入修改。{Colors.ENDC}")
            else:
                print(f"{Colors.BLUE}没有找到需要转换的图片{Colors.ENDC}")
            
        elif choice == '2':
            # 处理目录
            dir_path = input(f"{Colors.BOLD}请输入目录路径 (绝对或相对路径): {Colors.ENDC}")
            
            # 如果是相对路径，则基于默认目录
            if not os.path.isabs(dir_path):
                dir_path = os.path.join(default_dir, dir_path)
            
            if not os.path.isdir(dir_path):
                print(f"{Colors.FAIL}错误: 目录不存在: {dir_path}{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            preview = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 询问是否自动确认所有修改
            auto_confirm = input(f"{Colors.BOLD}是否自动确认所有修改? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 询问是否显示调试信息
            debug = input(f"{Colors.BOLD}是否显示调试信息? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 开始处理
            start_time = time.time()
            file_count, modified_file_count, markdown_count, html_count = scan_directory(dir_path, preview, auto_confirm=auto_confirm, debug=debug)
            end_time = time.time()
            
            # 显示总结
            print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
            print(f"{Colors.GREEN}处理完成! 耗时: {end_time - start_time:.2f}秒{Colors.ENDC}")
            print(f"{Colors.GREEN}扫描了 {file_count} 个文件{Colors.ENDC}")
            print(f"{Colors.GREEN}修改了 {modified_file_count} 个文件中的图片格式{Colors.ENDC}")
            print(f"{Colors.GREEN}- 转换为Markdown格式: {markdown_count}{Colors.ENDC}")
            print(f"{Colors.GREEN}- 转换为HTML格式: {html_count}{Colors.ENDC}")
            
            if preview:
                print(f"\n{Colors.BLUE}这是预览模式，没有实际写入修改。{Colors.ENDC}")
                
        elif choice == '3':
            # 退出
            print(f"{Colors.BLUE}感谢使用，再见!{Colors.ENDC}")
            break
            
        else:
            print(f"{Colors.WARNING}无效选项，请重试{Colors.ENDC}")

if __name__ == "__main__":
    main()
