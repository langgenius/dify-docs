#!/usr/bin/env python3
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

def load_docs_json(docs_json_path):
    """加载 docs.json 文件并解析其中的路径信息"""
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    return docs_data

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
    
    # 找出所有 Markdown 链接 - 支持带属性的链接
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)(\s+"[^"]*")?\)')
    matches = link_pattern.findall(content)
    
    changes = []
    for match in matches:
        link_text, link_url, link_attr = match
        
        # 修正link_attr（可能为空）
        link_attr = link_attr or ""
        
        # 跳过外部链接和已经格式化好的链接
        if link_url.startswith(('http://', 'https://', 'mailto:', '#')) or link_url.startswith('/en/'):
            continue
        
        # 处理 docs.dify.ai 链接
        if "docs.dify.ai" in link_url:
            # 从 docs.dify.ai 链接中提取路径部分
            docs_path = link_url.split("docs.dify.ai/")[-1] if "docs.dify.ai/" in link_url else ""
            
            if docs_path:
                # 查找最接近的有效路径
                matched_path = find_closest_path(docs_path, valid_paths)
                
                if matched_path:
                    # 构造新链接
                    new_link_url = f"/en/{matched_path}"
                    old_link = f"[{link_text}]({link_url}{link_attr})"
                    new_link = f"[{link_text}]({new_link_url}{link_attr})"
                    
                    changes.append({
                        "old_link": old_link, 
                        "new_link": new_link,
                        "match_type": "docs.dify.ai",
                        "match_path": matched_path
                    })
                else:
                    # 通用转换
                    new_link_url = f"/en/{docs_path}"
                    old_link = f"[{link_text}]({link_url}{link_attr})"
                    new_link = f"[{link_text}]({new_link_url}{link_attr})"
                    
                    changes.append({
                        "old_link": old_link, 
                        "new_link": new_link,
                        "match_type": "docs.dify.ai (generic)",
                        "match_path": None
                    })
        
        # 处理相对路径链接
        elif link_url.startswith(('../', './')) or not link_url.startswith('/'):
            # 计算目标文件的完整路径
            if link_url.startswith('./'):
                link_url = link_url[2:]  # 移除开头的 ./
            
            # 计算绝对路径
            target_path = os.path.normpath(os.path.join(file_dir, link_url))
            target_path = target_path.replace('\\', '/')  # 统一路径分隔符
            
            # 查找最接近的有效路径
            matched_path = find_closest_path(target_path, valid_paths)
            
            if matched_path:
                # 构造新链接
                new_link_url = f"/en/{matched_path}"
                old_link = f"[{link_text}]({link_url}{link_attr})"
                new_link = f"[{link_text}]({new_link_url}{link_attr})"
                
                changes.append({
                    "old_link": old_link, 
                    "new_link": new_link,
                    "match_type": "relative path",
                    "match_path": matched_path
                })
            else:
                # 检查是否是README.md类文件
                if os.path.basename(target_path) in ["README.md", "readme.md", "README", "readme"]:
                    # 对于README文件，使用其所在目录作为路径
                    dir_path = os.path.dirname(target_path)
                    if dir_path.startswith('en/'):
                        new_link_url = f"/{dir_path}"
                    else:
                        new_link_url = f"/en/{dir_path}"
                    
                    if new_link_url.endswith('/'):
                        new_link_url = new_link_url[:-1]
                else:
                    # 移除扩展名
                    target_without_ext, _ = os.path.splitext(target_path)
                    
                    # 避免en/前缀重复
                    if target_without_ext.startswith('en/'):
                        new_link_url = f"/{target_without_ext}"
                    else:
                        new_link_url = f"/en/{target_without_ext}"
                
                old_link = f"[{link_text}]({link_url}{link_attr})"
                new_link = f"[{link_text}]({new_link_url}{link_attr})"
                
                changes.append({
                    "old_link": old_link, 
                    "new_link": new_link,
                    "match_type": "relative path (generic)",
                    "match_path": None
                })
    
    return changes, content
