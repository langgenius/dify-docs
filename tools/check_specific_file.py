#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
针对特定文档的链接检查工具
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse

def is_external_link(link):
    """检查是否为外部链接"""
    parsed = urlparse(link)
    return bool(parsed.netloc) or link.startswith('http')

def load_valid_paths(docs_json_path):
    """从docs.json加载有效路径信息"""
    valid_paths = set()
    external_links = set()
    
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    
    def process_pages(items, prefix=""):
        """递归处理docs.json中的页面层级结构"""
        for item in items:
            if isinstance(item, dict):
                # 如果是字符串URL (用于外部链接)
                if isinstance(item.get('pages'), str):
                    if item['pages'].startswith('http'):
                        external_links.add(item['pages'])
                    else:
                        valid_paths.add(item['pages'])
                
                # 如果是字典或列表类型的pages
                if 'pages' in item and isinstance(item['pages'], (list, dict)):
                    process_pages(item['pages'], prefix)
                
                # 处理group情况下的pages
                if 'group' in item and 'pages' in item:
                    process_pages(item['pages'], prefix)
            elif isinstance(item, str):
                # 直接是文档路径
                if item.startswith('http'):
                    external_links.add(item)
                else:
                    valid_paths.add(item)
    
    # 处理navigation部分
    if 'navigation' in docs_data and 'languages' in docs_data['navigation']:
        for lang in docs_data['navigation']['languages']:
            if 'tabs' in lang:
                for tab in lang['tabs']:
                    if 'groups' in tab:
                        for group in tab['groups']:
                            if 'pages' in group:
                                process_pages(group['pages'])
    
    print(f"从docs.json中加载了 {len(valid_paths)} 个有效文档路径")
    return valid_paths, external_links

def extract_links_from_file(file_path):
    """从文件中提取链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    links = []
    
    # 提取Markdown链接 [text](url)
    md_links = re.findall(r'\[.+?\]\((.+?)\)', content)
    links.extend(md_links)
    
    # 提取HTML链接 href="url"
    html_links = re.findall(r'href=[\'"](.+?)[\'"]', content)
    links.extend(html_links)
    
    # 提取Card组件链接 href="url"
    card_links = re.findall(r'<Card.+?href=[\'"](.+?)[\'"]', content, re.DOTALL)
    links.extend(card_links)
    
    return links

def is_valid_internal_link(link, base_path, valid_paths):
    """检查内部链接是否有效"""
    # 去除锚点和查询参数
    link = link.split('#')[0].split('?')[0]
    
    # 跳过空链接
    if not link:
        return True
    
    # 如果是完整的路径
    if link in valid_paths:
        return True
    
    # 如果是相对路径，需要根据基础路径计算
    if base_path and not link.startswith('/'):
        # 获取基础目录
        base_dir = os.path.dirname(base_path)
        # 计算绝对路径
        if base_dir:
            abs_path = os.path.normpath(os.path.join(base_dir, link))
        else:
            abs_path = link
        
        # 替换Windows路径分隔符
        abs_path = abs_path.replace('\\', '/')
        
        # 检查是否在有效路径中
        return abs_path in valid_paths
    
    # 如果是以/开头的绝对路径
    if link.startswith('/'):
        # 去除开头的斜杠
        clean_link = link[1:]
        return clean_link in valid_paths
    
    return False

def main():
    # 配置
    docs_dir = '/Users/allen/Documents/dify-docs-mintlify'
    docs_json_path = '/Users/allen/Documents/dify-docs-mintlify/docs.json'
    target_file = '/Users/allen/Documents/dify-docs-mintlify/zh-hans/plugins/introduction.mdx'
    
    # 加载有效路径
    valid_paths, external_links = load_valid_paths(docs_json_path)
    
    # 获取相对路径
    rel_path = os.path.relpath(target_file, docs_dir)
    path_without_ext = os.path.splitext(rel_path)[0].replace('\\', '/')
    
    print(f"检查文件: {path_without_ext}")
    
    # 检查链接
    links = extract_links_from_file(target_file)
    broken_links = []
    
    for link in links:
        # 跳过外部链接和锚点链接
        if is_external_link(link) or link.startswith('#'):
            continue
        
        # 检查内部链接是否有效
        if not is_valid_internal_link(link, path_without_ext, valid_paths):
            broken_links.append(link)
    
    # 输出结果
    if not broken_links:
        print("\n✅ 所有链接检查完毕，未发现无效链接！")
    else:
        print("\n🔍 链接检查结果:")
        print("=" * 80)
        print(f"共发现 {len(broken_links)} 个无效链接")
        print("=" * 80)
        
        for link in broken_links:
            print(f"   ❌ 无效链接: {link}")

if __name__ == '__main__':
    main()
