#!/usr/bin/env python3
"""
图片链接同步工具

这个脚本用于比较dify-docs和dify-docs-mintlify目录中的相同文件，
并将dify-docs中的图片链接(https://assets-docs.dify.ai/...)同步到
dify-docs-mintlify中的对应文件。

支持:
- 手动指定单个文件同步
- 整个目录扫描并自动查找对应文件
- 预览模式，只显示修改不实际写入
- 交互式确认模式
"""

import os
import re
import sys
import time
import difflib
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional

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

# 图片链接正则表达式 - 匹配以下格式的图片链接:
# 1. Markdown格式: ![alt text](https://assets-docs.dify.ai/...)
# 2. HTML格式: <img src="https://assets-docs.dify.ai/..." alt="..." />
# 3. Frame标签中的图片: <Frame>...<img src="https://assets-docs.dify.ai/..." />...</Frame>
# 4. 相对路径图片: ![alt](/zh-cn/user-guide/.gitbook/assets/...)

# Markdown格式图片
MD_IMG_PATTERN = re.compile(r'!\[(.*?)\]\((https?://[^)]+|/[^)]+)\)')

# HTML格式图片
HTML_IMG_PATTERN = re.compile(r'<img\s+src="([^"]+)"[^>]*>')

# 在线图床的URL特征
ASSETS_URL_PREFIX = 'https://assets-docs.dify.ai/'

# 相对路径特征
RELATIVE_PATH_PREFIX = '/zh-cn/user-guide/.gitbook/assets/'

def find_corresponding_file(source_file: str, source_dir: str, target_dir: str) -> Optional[str]:
    """查找源文件在目标目录中的对应文件"""
    # 获取相对路径
    rel_path = os.path.relpath(source_file, source_dir)
    
    # 语言路径映射 (zh_CN -> zh-hans)
    if rel_path.startswith('zh_CN/'):
        rel_path = 'zh-hans/' + rel_path[6:]
    elif rel_path.startswith('en_US/'):
        rel_path = 'en/' + rel_path[5:]
    
    # 文件扩展名映射 (.md -> .mdx)
    if rel_path.endswith('.md'):
        rel_path = rel_path[:-3] + '.mdx'
    
    # 处理其他可能的路径结构差异
    # 例如 guides/workflow/node/ -> guides/workflow/nodes/
    possible_paths = [
        rel_path,
        rel_path.replace('/node/', '/nodes/'),
        rel_path.replace('/nodes/', '/node/'),
    ]
    
    # 检查所有可能的路径
    for path in possible_paths:
        target_file = os.path.join(target_dir, path)
        if os.path.exists(target_file):
            return target_file
    
    # 尝试更进一步的模糊匹配
    if '/' in rel_path:
        base_dir = os.path.dirname(rel_path)
        file_name = os.path.basename(rel_path)
        
        # 在目标目录中查找可能的子目录
        for root, dirs, files in os.walk(os.path.join(target_dir, os.path.dirname(base_dir))):
            for file in files:
                if file == file_name or (file_name.endswith('.md') and file == file_name[:-3] + '.mdx'):
                    return os.path.join(root, file)
    
    return None

def extract_image_links(content: str) -> List[Tuple[str, str, str]]:
    """
    从内容中提取图片链接
    
    Returns:
        List of tuples (full_match, alt_text, image_url)
    """
    images = []
    
    # 提取Markdown格式图片
    for match in MD_IMG_PATTERN.finditer(content):
        full_match = match.group(0)
        alt_text = match.group(1)
        image_url = match.group(2)
        images.append((full_match, alt_text, image_url))
    
    # 提取HTML格式图片
    for match in HTML_IMG_PATTERN.finditer(content):
        full_match = match.group(0)
        image_url = match.group(1)
        # 从HTML标签中提取alt属性
        alt_match = re.search(r'alt="([^"]*)"', full_match)
        alt_text = alt_match.group(1) if alt_match else ""
        images.append((full_match, alt_text, image_url))
    
    return images

def generate_frame_replacement(old_content: str, new_image_url: str) -> str:
    """
    生成Frame标签的替换内容
    保留原始的Frame属性和图片的alt/width/height等属性
    """
    # 提取Frame标签
    frame_match = re.search(r'<Frame([^>]*)>(.*?)</Frame>', old_content, re.DOTALL)
    if not frame_match:
        return old_content
    
    frame_attrs = frame_match.group(1)
    inner_content = frame_match.group(2)
    
    # 提取图片标签属性
    img_match = re.search(r'<img([^>]*)>', inner_content)
    if not img_match:
        return old_content
    
    img_attrs = img_match.group(1)
    
    # 替换src属性
    new_img_attrs = re.sub(r'src="[^"]+"', f'src="{new_image_url}"', img_attrs)
    
    # 重建Frame标签
    new_content = f'<Frame{frame_attrs}>\n  <img{new_img_attrs} />\n</Frame>'
    return new_content

def sync_image_links(source_file: str, target_file: str, dry_run: bool = False) -> Tuple[int, List[Tuple[str, str]]]:
    """
    同步源文件和目标文件中的图片链接
    
    Args:
        source_file: 源文件路径
        target_file: 目标文件路径
        dry_run: 是否只预览修改而不实际写入
        
    Returns:
        (修改的链接数量, 替换的链接列表)
    """
    # 读取文件内容
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    with open(target_file, 'r', encoding='utf-8') as f:
        target_content = f.read()
    
    # 提取源文件中的图片链接
    source_images = extract_image_links(source_content)
    online_images = [(match, alt, url) for match, alt, url in source_images if url.startswith(ASSETS_URL_PREFIX)]
    
    if not online_images:
        return 0, []
    
    # 处理目标文件中的内容
    new_content = target_content
    modified_links = []
    
    # 处理Frame标签中的图片
    frame_pattern = re.compile(r'<Frame[^>]*>.*?<img\s+src="([^"]+)"[^>]*>.*?</Frame>', re.DOTALL)
    frame_matches = list(frame_pattern.finditer(target_content))
    
    # 处理每个在线图片链接
    for _, _, image_url in online_images:
        # 查找目标文件中可能的相对路径格式
        for match in frame_matches:
            frame_text = match.group(0)
            old_url = match.group(1)
            
            # 跳过已经是在线链接的图片
            if old_url.startswith(ASSETS_URL_PREFIX):
                continue
                
            # 如果是相对路径，替换为在线链接
            if old_url.startswith('/'):
                new_frame = generate_frame_replacement(frame_text, image_url)
                new_content = new_content.replace(frame_text, new_frame)
                modified_links.append((old_url, image_url))
    
    # 如果是预览模式，不写入修改
    if dry_run:
        return len(modified_links), modified_links
    
    # 如果内容有变化，写入新内容
    if new_content != target_content:
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return len(modified_links), modified_links

def process_file(source_file: str, source_dir: str, target_dir: str, dry_run: bool = False, auto_confirm: bool = False) -> Tuple[bool, int]:
    """
    处理单个文件
    
    Args:
        source_file: 源文件路径
        source_dir: 源目录路径
        target_dir: 目标目录路径
        dry_run: 是否只预览修改而不实际写入
        auto_confirm: 是否自动确认所有修改
        
    Returns:
        (是否成功处理, 修改的链接数量)
    """
    print(f"{Colors.HEADER}处理文件: {source_file}{Colors.ENDC}")
    
    # 查找对应文件
    target_file = find_corresponding_file(source_file, source_dir, target_dir)
    
    if not target_file:
        print(f"{Colors.FAIL}错误: 未找到对应的目标文件{Colors.ENDC}")
        return False, 0
    
    print(f"找到对应文件: {target_file}")
    
    # 同步图片链接
    try:
        modified_count, modified_links = sync_image_links(source_file, target_file, dry_run)
        
        if modified_count > 0:
            print(f"{Colors.GREEN}检测到 {modified_count} 个可以同步的图片链接:{Colors.ENDC}")
            for i, (old_url, new_url) in enumerate(modified_links):
                print(f"  {i+1}. {Colors.WARNING}{old_url}{Colors.ENDC} -> {Colors.GREEN}{new_url}{Colors.ENDC}")
            
            if not dry_run:
                if not auto_confirm:
                    response = input(f"{Colors.BOLD}是否应用这些修改? (y/n): {Colors.ENDC}")
                    if response.lower() != 'y':
                        print(f"{Colors.BLUE}已取消修改{Colors.ENDC}")
                        return True, 0
                
                print(f"{Colors.GREEN}已应用 {modified_count} 个修改{Colors.ENDC}")
            else:
                print(f"{Colors.BLUE}预览模式 - 未执行实际修改{Colors.ENDC}")
        else:
            print(f"{Colors.BLUE}没有需要同步的图片链接{Colors.ENDC}")
        
        return True, modified_count
    except Exception as e:
        print(f"{Colors.FAIL}处理文件时出错: {e}{Colors.ENDC}")
        return False, 0

def scan_directory(dir_path: str, source_dir: str, target_dir: str, dry_run: bool = False, auto_confirm: bool = False) -> Tuple[int, int]:
    """
    扫描目录并处理文件
    
    Args:
        dir_path: 要扫描的目录路径
        source_dir: 源目录路径
        target_dir: 目标目录路径
        dry_run: 是否只预览修改而不实际写入
        auto_confirm: 是否自动确认所有修改
        
    Returns:
        (处理的文件数量, 修改的链接总数)
    """
    processed_count = 0
    modified_count = 0
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 询问是否处理此文件
                if not auto_confirm:
                    response = input(f"{Colors.BOLD}是否处理文件 {file_path}? (y/n/q-退出): {Colors.ENDC}")
                    if response.lower() == 'n':
                        print(f"{Colors.BLUE}跳过此文件{Colors.ENDC}")
                        continue
                    elif response.lower() == 'q':
                        print(f"{Colors.BLUE}退出处理{Colors.ENDC}")
                        return processed_count, modified_count
                
                success, count = process_file(file_path, source_dir, target_dir, dry_run, auto_confirm)
                if success:
                    processed_count += 1
                    modified_count += count
    
    return processed_count, modified_count

def main():
    """主程序入口"""
    # 确定默认源目录和目标目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_target_dir = os.path.dirname(script_dir)  # dify-docs-mintlify
    default_source_dir = os.path.dirname(default_target_dir) + '/dify-docs'  # dify-docs
    
    # 显示欢迎信息
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER} Dify 文档图片链接同步工具 {Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"源目录: {default_source_dir}")
    print(f"目标目录: {default_target_dir}\n")
    
    # 确认目录
    if not os.path.isdir(default_source_dir):
        print(f"{Colors.FAIL}错误: 源目录不存在: {default_source_dir}{Colors.ENDC}")
        default_source_dir = input(f"{Colors.BOLD}请输入正确的源目录路径: {Colors.ENDC}")
    
    if not os.path.isdir(default_target_dir):
        print(f"{Colors.FAIL}错误: 目标目录不存在: {default_target_dir}{Colors.ENDC}")
        default_target_dir = input(f"{Colors.BOLD}请输入正确的目标目录路径: {Colors.ENDC}")
    
    # 交互式菜单
    while True:
        print(f"\n{Colors.BOLD}请选择操作模式:{Colors.ENDC}")
        print("1. 处理单个文件")
        print("2. 处理指定目录中的所有文件")
        print("3. 退出")
        
        choice = input(f"{Colors.BOLD}请输入选项 (1-3): {Colors.ENDC}")
        
        if choice == '1':
            # 处理单个文件
            source_file = input(f"{Colors.BOLD}请输入源文件路径 (相对于源目录): {Colors.ENDC}")
            source_file = os.path.join(default_source_dir, source_file)
            
            if not os.path.isfile(source_file):
                print(f"{Colors.FAIL}错误: 文件不存在: {source_file}{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            dry_run = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 处理文件
            start_time = time.time()
            success, modified_count = process_file(source_file, default_source_dir, default_target_dir, dry_run)
            end_time = time.time()
            
            if success:
                print(f"\n{Colors.GREEN}处理完成! 耗时: {end_time - start_time:.2f}秒{Colors.ENDC}")
                if not dry_run and modified_count > 0:
                    print(f"{Colors.GREEN}成功同步了 {modified_count} 个图片链接{Colors.ENDC}")
            
        elif choice == '2':
            # 处理目录
            dir_path = input(f"{Colors.BOLD}请输入要处理的源目录路径 (相对于源目录): {Colors.ENDC}")
            dir_path = os.path.join(default_source_dir, dir_path)
            
            if not os.path.isdir(dir_path):
                print(f"{Colors.FAIL}错误: 目录不存在: {dir_path}{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            dry_run = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 询问是否自动确认所有修改
            auto_confirm = input(f"{Colors.BOLD}是否自动确认所有修改? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 处理目录
            start_time = time.time()
            processed_count, modified_count = scan_directory(dir_path, default_source_dir, default_target_dir, dry_run, auto_confirm)
            end_time = time.time()
            
            print(f"\n{Colors.GREEN}处理完成! 耗时: {end_time - start_time:.2f}秒{Colors.ENDC}")
            print(f"{Colors.GREEN}共处理 {processed_count} 个文件，同步了 {modified_count} 个图片链接{Colors.ENDC}")
            
        elif choice == '3':
            # 退出
            print(f"{Colors.BLUE}感谢使用，再见!{Colors.ENDC}")
            break
            
        else:
            print(f"{Colors.WARNING}无效选项，请重试{Colors.ENDC}")

if __name__ == "__main__":
    main()
