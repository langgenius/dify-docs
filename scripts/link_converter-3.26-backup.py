
#!/usr/bin/env python3
import os
import re
import json
import sys
from pathlib import Path

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
                extract_paths_from_object(value)
        elif isinstance(obj, list):
            # 处理列表中的每个元素
            for item in obj:
                extract_paths_from_object(item)
    
    # 开始提取
    extract_paths_from_object(docs_data)
    return valid_paths

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
                
                changes.append((old_link, new_link))
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
                
                changes.append((old_link, new_link))
        
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
                
                changes.append((old_link, new_link))
            else:
                # 没有找到匹配路径，使用通用转换规则
                parts = docs_path.split('/')
                if len(parts) >= 2:
                    # 假设 docs.dify.ai 链接对应于 en/ 目录下的内容
                    new_link_url = f"/en/{docs_path}"
                    
                    old_link = f"[{link_text}]({link_url})"
                    new_link = f"[{link_text}]({new_link_url})"
                    
                    changes.append((old_link, new_link))
    
    return changes, content

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_json_path = os.path.join(base_dir, 'docs.json')
    
    # 加载 docs.json
    try:
        docs_data = load_docs_json(docs_json_path)
        valid_paths = extract_valid_paths(docs_data)
        print(f"从 docs.json 中提取了 {len(valid_paths)} 个有效路径")
    except Exception as e:
        print(f"加载 docs.json 时出错: {e}")
        sys.exit(1)
    
    # 获取用户输入的路径
    path_input = input("请输入要处理的文件或目录路径（相对于当前目录）: ")
    target_path = os.path.join(base_dir, path_input)
    
    if not os.path.exists(target_path):
        print(f"路径不存在: {target_path}")
        sys.exit(1)
    
    # 查找 Markdown 文件
    md_files = find_md_files(target_path)
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    # 处理每个文件
    for file_path in md_files:
        print(f"\n处理文件: {file_path}")
        
        changes, content = convert_links_in_file(file_path, valid_paths, base_dir)
        
        if not changes:
            print("未发现需要修改的链接")
            continue
        
        print("发现以下需要修改的链接:")
        for i, (old_link, new_link) in enumerate(changes, 1):
            print(f"{i}. {old_link} -> {new_link}")
        
        confirm = input("确认进行修改? (y/n): ")
        if confirm.lower() == 'y':
            # 进行替换
            modified_content = content
            for old_link, new_link in changes:
                modified_content = modified_content.replace(old_link, new_link)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            print(f"文件已更新: {file_path}")
        else:
            print("跳过此文件")

if __name__ == "__main__":
    main()
