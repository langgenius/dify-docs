def load_docs_json(docs_json_path):
    """加载 docs.json 文件并解析其中的路径信息"""
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    return docs_data#!/usr/bin/env python3
import os
import re
import json
import sys
import difflib
from pathlib import Path

# ANSI 颜色代码
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def extract_valid_paths(docs_data):
    """从 docs.json 中提取所有有效的文档路径"""
    valid_paths = set()
    
    # 递归函数用于处理嵌套结构
    def extract_paths_from_object(obj):
        if isinstance(obj, dict):
            # 检查是否有页面路径
            if "pages" in obj:
                for page in obj["pages"]:
                    if isinstance(page, str) and not page.startswith("http"):
                        valid_paths.add(page)
                    elif isinstance(page, dict):
                        extract_paths_from_object(page)
            # 处理其他可能的字典键
            for key, value in obj.items():
                if key != "pages":  # 避免重复处理
                    extract_paths_from_object(value)
        elif isinstance(obj, list):
            # 处理列表中的每个元素
            for item in obj:
                extract_paths_from_object(item)
    
    # 开始提取
    extract_paths_from_object(docs_data)
    return valid_paths

def find_closest_path(target_path, valid_paths):
    """查找最接近的有效路径"""
    # 移除扩展名
    target_without_ext, _ = os.path.splitext(target_path)
    
    # 检查精确匹配
    for path in valid_paths:
        path_without_ext, _ = os.path.splitext(path)
        if path_without_ext == target_without_ext or path == target_without_ext:
            return path
    
    # 如果没有精确匹配，查找最相似的路径
    best_match = None
    best_score = 0
    
    for path in valid_paths:
        # 计算路径的相似度
        score = difflib.SequenceMatcher(None, target_without_ext, path).ratio()
        
        # 特别检查路径的末尾部分（文件名）是否匹配
        target_parts = target_without_ext.split('/')
        path_parts = path.split('/')
        
        if len(target_parts) > 0 and len(path_parts) > 0:
            if target_parts[-1] == path_parts[-1]:
                score += 0.3  # 增加匹配度
        
        if score > best_score:
            best_score = score
            best_match = path
    
    # 如果相似度足够高，返回最佳匹配
    if best_score > 0.6:  # 阈值可以调整
        return best_match
    
    # 寻找包含目标路径末尾部分的路径
    if len(target_parts) > 0:
        for path in valid_paths:
            if target_parts[-1] in path.split('/'):
                return path
    
    return None

def find_md_files(path):
    """查找指定路径下的所有 .md 和 .mdx 文件"""
    path_obj = Path(path)
    if path_obj.is_file() and (path_obj.suffix in ['.md', '.mdx']):
        return [path_obj]
    
    md_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                md_files.append(Path(os.path.join(root, file)))
    
    return md_files

def convert_links_in_file(file_path, valid_paths, base_dir):
    """转换文件中的链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取当前文件的相对路径（相对于基础目录）
    relative_file_path = os.path.relpath(file_path, base_dir)
    file_dir = os.path.dirname(relative_file_path)
    
    # 找出所有 Markdown 链接
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    links = link_pattern.findall(content)
    
    changes = []
    for link_text, link_url in links:
        # 跳过外部链接
        if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        
        # 跳过已经以 /en/ 开头的链接
        if link_url.startswith('/en/'):
            continue
        
        # 处理相对路径链接
        if link_url.startswith(('../', './')) or not link_url.startswith('/') and not link_url.startswith('http'):
            # 计算绝对路径
            if link_url.startswith('./'):
                link_url = link_url[2:]  # 移除开头的 ./
            
            # 计算目标文件的完整路径
            target_path = os.path.normpath(os.path.join(file_dir, link_url))
            
            # 提取不包含扩展名的路径（docs.json 中通常不包含扩展名）
            target_without_ext, _ = os.path.splitext(target_path)
            
            # 防止路径重复
            if target_without_ext.startswith('en/'):
                clean_target = target_without_ext
            else:
                clean_target = target_without_ext
            
            # 查找匹配的有效路径
            matching_path = None
            for valid_path in valid_paths:
                valid_without_ext, _ = os.path.splitext(valid_path)
                if valid_without_ext == clean_target or valid_path == clean_target:
                    matching_path = valid_path
                    break
            
            if matching_path:
                # 找到匹配的路径，转换为以 /en/ 开头的绝对路径
                if not matching_path.startswith('/'):
                    if matching_path.startswith('en/'):
                        new_link_url = f"/{matching_path}"
                    else:
                        new_link_url = f"/en/{matching_path}"
                else:
                    new_link_url = matching_path
                
                old_link = f"[{link_text}]({link_url})"
                new_link = f"[{link_text}]({new_link_url})"
                
                changes.append((old_link, new_link, link_url, new_link_url))
            else:
                # 没有找到匹配路径，使用通用转换规则
                # 去掉可能的文件扩展名
                clean_target, _ = os.path.splitext(target_path)
                if clean_target.startswith('en/'):
                    new_link_url = f"/{clean_target}"
                else:
                    new_link_url = f"/en/{clean_target}"
                
                old_link = f"[{link_text}]({link_url})"
                new_link = f"[{link_text}]({new_link_url})"
                
                changes.append((old_link, new_link, link_url, new_link_url))
        
        # 处理 docs.dify.ai 链接
        elif "docs.dify.ai" in link_url:
            # 从 docs.dify.ai 链接中提取路径部分
            docs_path = link_url.split("docs.dify.ai/")[-1]
            
            # 查找匹配的有效路径
            matching_path = None
            for valid_path in valid_paths:
                if valid_path.endswith(docs_path) or docs_path in valid_path:
                    matching_path = valid_path
                    break
            
            if matching_path:
                # 找到匹配的路径，转换为以 /en/ 开头的绝对路径
                if not matching_path.startswith('/'):
                    if matching_path.startswith('en/'):
                        new_link_url = f"/{matching_path}"
                    else:
                        new_link_url = f"/en/{matching_path}"
                else:
                    new_link_url = matching_path
                
                old_link = f"[{link_text}]({link_url})"
                new_link = f"[{link_text}]({new_link_url})"
                
                changes.append((old_link, new_link, link_url, new_link_url))
            else:
                # 没有找到匹配路径，使用通用转换规则
                parts = docs_path.split('/')
                if len(parts) >= 2:
                    # 假设 docs.dify.ai 链接对应于 en/ 目录下的内容
                    new_link_url = f"/en/{docs_path}"
                    
                    old_link = f"[{link_text}]({link_url})"
                    new_link = f"[{link_text}]({new_link_url})"
                    
                    changes.append((old_link, new_link, link_url, new_link_url))
    
    return changes, content

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_json_path = os.path.join(base_dir, 'docs.json')
    
    # 显示脚本标题
    print(f"\n{Colors.CYAN}{Colors.BOLD}===== Dify 文档链接转换工具 ====={Colors.RESET}\n")
    
    # 加载 docs.json
    try:
        docs_data = load_docs_json(docs_json_path)
        valid_paths = extract_valid_paths(docs_data)
        print(f"{Colors.GREEN}从 docs.json 中提取了 {Colors.YELLOW}{len(valid_paths)}{Colors.GREEN} 个有效路径{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}加载 docs.json 时出错: {e}{Colors.RESET}")
        sys.exit(1)
    
    # 获取用户输入的路径
    path_input = input(f"{Colors.CYAN}请输入要处理的文件或目录路径（相对于当前目录）: {Colors.RESET}")
    target_path = os.path.join(base_dir, path_input)
    
    if not os.path.exists(target_path):
        print(f"{Colors.RED}路径不存在: {target_path}{Colors.RESET}")
        sys.exit(1)
    
    # 查找 Markdown 文件
    md_files = find_md_files(target_path)
    print(f"{Colors.GREEN}找到 {Colors.YELLOW}{len(md_files)}{Colors.GREEN} 个 Markdown 文件{Colors.RESET}")
    
    # 处理每个文件
    total_changed = 0
    total_files_changed = 0
    
    for file_path in md_files:
        print(f"\n{Colors.BLUE}{Colors.BOLD}处理文件: {Colors.RESET}{Colors.YELLOW}{file_path}{Colors.RESET}")
        
        changes, content = convert_links_in_file(file_path, valid_paths, base_dir)
        
        if not changes:
            print(f"{Colors.GREEN}未发现需要修改的链接{Colors.RESET}")
            continue
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}发现以下需要修改的链接:{Colors.RESET}")
        for i, (old_link, new_link, old_url, new_url) in enumerate(changes, 1):
            # 提取链接文本
            link_text_match = re.match(r'\[([^\]]+)\]', old_link)
            link_text = link_text_match.group(1) if link_text_match else ""
            print(f"{Colors.YELLOW}{i}. {Colors.RESET}{old_link} -> {new_link}")
        
        confirm = input(f"\n{Colors.CYAN}确认进行修改? (y/n): {Colors.RESET}")
        if confirm.lower() == 'y':
            # 进行替换
            modified_content = content
            for old_link, new_link, _, _ in changes:
                modified_content = modified_content.replace(old_link, new_link)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            total_changed += len(changes)
            total_files_changed += 1
            print(f"{Colors.GREEN}文件已更新: {file_path}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}跳过此文件{Colors.RESET}")
    
    # 显示总结
    print(f"\n{Colors.CYAN}{Colors.BOLD}===== 转换完成 ====={Colors.RESET}")
    print(f"{Colors.GREEN}共修改了 {Colors.YELLOW}{total_files_changed}{Colors.GREEN} 个文件，{Colors.YELLOW}{total_changed}{Colors.GREEN} 个链接{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}用户中断，程序退出{Colors.RESET}")
        sys.exit(0)
