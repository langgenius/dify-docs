#!/usr/bin/env python3
"""
交互式Markdown链接修复工具

这个脚本用于交互式地修复Markdown文件中的相对路径引用，将它们转换为
从根目录开始的绝对路径格式（如 /zh-hans/xxx），以符合Mintlify文档要求。
脚本支持处理单个文件或指定目录内的所有.mdx文件。

特点:
- 交互式操作，精确可控
- 提供修改预览
- 支持单文件或目录处理
- 将相对路径转换为绝对路径
- 支持锚点保留
- 移除文件扩展名
"""

import os
import re
import sys
from pathlib import Path
import glob

# 正则表达式来匹配Markdown链接引用，支持.md和.mdx文件
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+\.(md|mdx))(?:#([^)]*))?(\))')
REL_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)/][^)]+)(?:#([^)]*))?(\))')  # 匹配不以/开头的相对路径

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
    

def find_file_in_project(root_dir, rel_path, current_file_dir):
    """
    根据相对路径在项目中查找实际文件
    
    Args:
        root_dir: 项目根目录
        rel_path: 相对路径引用
        current_file_dir: 当前文件所在目录
        
    Returns:
        找到的文件绝对路径，或None如果未找到
    """
    # 移除扩展名，稍后会添加回.mdx
    if rel_path.endswith(('.md', '.mdx')):
        extension = '.md' if rel_path.endswith('.md') else '.mdx'
        rel_path = rel_path[:-len(extension)]
    
    # 如果是以../或./开头的相对路径
    if rel_path.startswith(('./','../')):
        # 计算实际路径
        actual_path = os.path.normpath(os.path.join(current_file_dir, rel_path))
        
        # 尝试匹配.mdx文件
        matches = glob.glob(f"{actual_path}.mdx")
        if matches:
            return matches[0]
            
        # 尝试匹配.md文件
        matches = glob.glob(f"{actual_path}.md")
        if matches:
            return matches[0]
    
    # 尝试在项目中搜索匹配的文件名
    basename = os.path.basename(rel_path)
    # 搜索所有.mdx文件
    mdx_matches = []
    md_matches = []
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.mdx') and os.path.splitext(file)[0] == basename:
                mdx_matches.append(os.path.join(root, file))
            elif file.endswith('.md') and os.path.splitext(file)[0] == basename:
                md_matches.append(os.path.join(root, file))
    
    # 优先使用.mdx文件
    if mdx_matches:
        return mdx_matches[0]
    elif md_matches:
        return md_matches[0]
    
    return None

def get_absolute_path(file_path, root_dir):
    """
    获取相对于项目根目录的绝对路径
    
    Args:
        file_path: 文件的完整路径
        root_dir: 项目根目录
        
    Returns:
        /zh-hans/xxx 格式的绝对路径
    """
    # 获取相对于根目录的路径
    rel_path = os.path.relpath(file_path, root_dir)
    # 移除扩展名
    rel_path = os.path.splitext(rel_path)[0]
    # 添加前导斜杠
    abs_path = f"/{rel_path}"
    
    return abs_path

def process_file(file_path, root_dir, dry_run=False, auto_confirm=False):
    """
    处理单个Markdown文件中的链接引用
    
    Args:
        file_path: 要处理的文件路径
        root_dir: 项目根目录
        dry_run: 是否只预览修改，不实际写入
        auto_confirm: 是否自动确认所有修改
        
    Returns:
        修改的链接数量
    """
    print(f"\n{Colors.HEADER}处理文件:{Colors.ENDC} {file_path}")
    
    # 获取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"{Colors.FAIL}错误: 无法读取文件 - {e}{Colors.ENDC}")
        return 0
    
    # 当前文件所在目录
    current_file_dir = os.path.dirname(file_path)
    
    # 存储所有要修改的内容
    changes = []
    
    # 查找带有.md或.mdx后缀的链接
    for m in MD_LINK_PATTERN.finditer(content):
        link_text = m.group(1)
        link_path = m.group(2)
        fragment = m.group(4) or ""  # 锚点可能不存在
        full_match = m.group(0)
        
        # 跳过外部链接
        if link_path.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
            continue
        
        # 查找实际文件
        actual_file = find_file_in_project(root_dir, link_path, current_file_dir)
        if actual_file:
            # 转换为绝对路径
            abs_path = get_absolute_path(actual_file, root_dir)
            fragment_text = f"#{fragment}" if fragment else ""
            new_link = f"[{link_text}]({abs_path}{fragment_text})"
            changes.append((full_match, new_link, actual_file))
    
    # 查找其他相对路径链接（不带.md或.mdx后缀）
    for m in REL_LINK_PATTERN.finditer(content):
        link_text = m.group(1)
        link_path = m.group(2)
        fragment = m.group(3) or ""  # 锚点可能不存在
        full_match = m.group(0)
        
        # 跳过已经是绝对路径的链接
        if link_path.startswith('/'):
            continue
            
        # 跳过外部链接
        if link_path.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
            continue
        
        # 查找实际文件
        actual_file = find_file_in_project(root_dir, link_path, current_file_dir)
        if actual_file:
            # 转换为绝对路径
            abs_path = get_absolute_path(actual_file, root_dir)
            fragment_text = f"#{fragment}" if fragment else ""
            new_link = f"[{link_text}]({abs_path}{fragment_text})"
            changes.append((full_match, new_link, actual_file))
    
    # 如果没有找到需要修改的链接
    if not changes:
        print(f"{Colors.GREEN}没有找到需要修改的链接{Colors.ENDC}")
        return 0
    
    # 显示找到的修改
    print(f"\n{Colors.BLUE}找到 {len(changes)} 个需要修改的链接:{Colors.ENDC}")
    for i, (old, new, target) in enumerate(changes):
        print(f"{Colors.CYAN}修改 {i+1}:{Colors.ENDC}")
        print(f"  - 原始链接: {Colors.WARNING}{old}{Colors.ENDC}")
        print(f"  - 新链接: {Colors.GREEN}{new}{Colors.ENDC}")
        print(f"  - 目标文件: {os.path.relpath(target, root_dir)}\n")
    
    # 如果是预览模式，返回
    if dry_run:
        print(f"{Colors.BLUE}预览模式 - 未执行实际修改{Colors.ENDC}")
        return len(changes)
    
    # 确认修改
    if not auto_confirm:
        response = input(f"{Colors.BOLD}是否应用这些修改? (y/n/部分修改输入数字如1,3,5): {Colors.ENDC}")
        
        if response.lower() == 'n':
            print(f"{Colors.BLUE}已取消修改{Colors.ENDC}")
            return 0
        elif response.lower() == 'y':
            selected_changes = changes
        else:
            try:
                # 解析用户选择的修改索引
                indices = [int(i.strip()) - 1 for i in response.split(',')]
                selected_changes = [changes[i] for i in indices if 0 <= i < len(changes)]
                if not selected_changes:
                    print(f"{Colors.WARNING}未选择任何有效修改，操作取消{Colors.ENDC}")
                    return 0
            except:
                print(f"{Colors.WARNING}输入格式有误，操作取消{Colors.ENDC}")
                return 0
    else:
        selected_changes = changes
    
    # 应用修改
    modified_content = content
    for old, new, _ in selected_changes:
        modified_content = modified_content.replace(old, new)
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"{Colors.GREEN}成功应用 {len(selected_changes)} 个修改到文件{Colors.ENDC}")
        return len(selected_changes)
    except Exception as e:
        print(f"{Colors.FAIL}错误: 无法写入文件 - {e}{Colors.ENDC}")
        return 0

def scan_directory(dir_path, root_dir, dry_run=False, auto_confirm=False):
    """
    扫描目录中的所有.mdx文件
    
    Args:
        dir_path: 要扫描的目录路径
        root_dir: 项目根目录
        dry_run: 是否只预览修改
        auto_confirm: 是否自动确认所有修改
        
    Returns:
        处理的文件数量，修改的链接总数
    """
    file_count = 0
    total_changes = 0
    
    print(f"{Colors.HEADER}扫描目录: {dir_path}{Colors.ENDC}")
    
    # 获取所有.mdx文件
    mdx_files = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.mdx'):
                mdx_files.append(os.path.join(root, file))
    
    if not mdx_files:
        print(f"{Colors.WARNING}在目录中未找到.mdx文件{Colors.ENDC}")
        return 0, 0
    
    print(f"{Colors.BLUE}找到 {len(mdx_files)} 个.mdx文件{Colors.ENDC}")
    
    # 处理每个文件
    for file_path in mdx_files:
        # 显示文件的相对路径
        rel_path = os.path.relpath(file_path, root_dir)
        print(f"\n{Colors.BOLD}处理文件 ({file_count+1}/{len(mdx_files)}): {rel_path}{Colors.ENDC}")
        
        # 询问是否处理此文件
        if not auto_confirm:
            response = input(f"{Colors.BOLD}是否处理此文件? (y/n/q-退出): {Colors.ENDC}")
            if response.lower() == 'n':
                print(f"{Colors.BLUE}跳过此文件{Colors.ENDC}")
                continue
            elif response.lower() == 'q':
                print(f"{Colors.BLUE}退出处理{Colors.ENDC}")
                break
        
        # 处理文件
        changes = process_file(file_path, root_dir, dry_run, auto_confirm)
        if changes > 0:
            file_count += 1
            total_changes += changes
    
    return file_count, total_changes

def main():
    """主程序入口"""
    # 确定项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # 脚本在scripts目录下，上一级是项目根目录
    
    # 显示欢迎信息
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER} Mintlify文档链接修复工具 {Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"项目根目录: {project_root}\n")
    
    # 交互式菜单
    while True:
        print(f"\n{Colors.BOLD}请选择操作模式:{Colors.ENDC}")
        print("1. 处理单个文件")
        print("2. 处理指定目录中的所有.mdx文件")
        print("3. 退出")
        
        choice = input(f"{Colors.BOLD}请输入选项 (1-3): {Colors.ENDC}")
        
        if choice == '1':
            # 处理单个文件
            file_path = input(f"{Colors.BOLD}请输入文件路径 (相对于项目根目录): {Colors.ENDC}")
            file_path = os.path.join(project_root, file_path)
            
            if not os.path.isfile(file_path):
                print(f"{Colors.FAIL}错误: 文件不存在{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            dry_run = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 处理文件
            changes = process_file(file_path, project_root, dry_run)
            
            print(f"\n{Colors.GREEN}处理完成! 共发现 {changes} 个需要修改的链接{Colors.ENDC}")
            
        elif choice == '2':
            # 处理目录
            dir_path = input(f"{Colors.BOLD}请输入目录路径 (相对于项目根目录): {Colors.ENDC}")
            dir_path = os.path.join(project_root, dir_path)
            
            if not os.path.isdir(dir_path):
                print(f"{Colors.FAIL}错误: 目录不存在{Colors.ENDC}")
                continue
            
            # 询问是否只预览修改
            dry_run = input(f"{Colors.BOLD}是否只预览修改而不实际写入? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 询问是否自动确认所有修改
            auto_confirm = input(f"{Colors.BOLD}是否自动确认所有修改? (y/n): {Colors.ENDC}").lower() == 'y'
            
            # 处理目录
            file_count, total_changes = scan_directory(dir_path, project_root, dry_run, auto_confirm)
            
            print(f"\n{Colors.GREEN}处理完成! 共处理 {file_count} 个文件，修改了 {total_changes} 个链接{Colors.ENDC}")
            
        elif choice == '3':
            # 退出
            print(f"{Colors.BLUE}感谢使用，再见!{Colors.ENDC}")
            break
            
        else:
            print(f"{Colors.WARNING}无效选项，请重试{Colors.ENDC}")

if __name__ == "__main__":
    main()
