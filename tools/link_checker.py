#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
链接检查工具：检查文档中的内部链接是否有效

这个脚本用于扫描Mintlify文档中的内部链接，并验证它们是否正确指向存在的文档。
支持相对路径链接和绝对路径链接。
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

class LinkChecker:
    def __init__(self, docs_dir, docs_json_path, base_lang="zh-hans"):
        self.docs_dir = Path(docs_dir)
        self.docs_json_path = Path(docs_json_path)
        self.base_lang = base_lang
        self.valid_paths = set()
        self.external_links = set()
        self.documents = {}
        self.broken_links = defaultdict(list)
        
        # 加载docs.json文件以获取有效路径
        self._load_docs_json()
        # 获取所有文档文件
        self._load_documents()
    
    def _load_docs_json(self):
        """从docs.json加载有效路径信息"""
        with open(self.docs_json_path, 'r', encoding='utf-8') as f:
            docs_data = json.load(f)
        
        def process_pages(items, prefix=""):
            """递归处理docs.json中的页面层级结构"""
            for item in items:
                if isinstance(item, dict):
                    # 如果是字符串URL (用于外部链接)
                    if isinstance(item.get('pages'), str):
                        if item['pages'].startswith('http'):
                            self.external_links.add(item['pages'])
                        else:
                            self.valid_paths.add(item['pages'])
                    
                    # 如果是字典或列表类型的pages
                    if 'pages' in item and isinstance(item['pages'], (list, dict)):
                        process_pages(item['pages'], prefix)
                    
                    # 处理group情况下的pages
                    if 'group' in item and 'pages' in item:
                        process_pages(item['pages'], prefix)
                elif isinstance(item, str):
                    # 直接是文档路径
                    if item.startswith('http'):
                        self.external_links.add(item)
                    else:
                        self.valid_paths.add(item)
        
        # 处理navigation部分
        if 'navigation' in docs_data and 'languages' in docs_data['navigation']:
            for lang in docs_data['navigation']['languages']:
                if 'tabs' in lang:
                    for tab in lang['tabs']:
                        if 'groups' in tab:
                            for group in tab['groups']:
                                if 'pages' in group:
                                    process_pages(group['pages'])
        
        print(f"从docs.json中加载了 {len(self.valid_paths)} 个有效文档路径")
    
    def _load_documents(self):
        """加载文档目录下的所有.mdx和.md文件"""
        for ext in ['.mdx', '.md']:
            for file_path in self.docs_dir.glob(f'**/*{ext}'):
                rel_path = file_path.relative_to(self.docs_dir)
                path_str = str(rel_path).replace('\\', '/')
                # 移除扩展名以匹配docs.json中的路径
                path_without_ext = os.path.splitext(path_str)[0]
                self.documents[path_without_ext] = file_path
                
                # 也添加到有效路径集合中
                self.valid_paths.add(path_without_ext)
        
        print(f"扫描到 {len(self.documents)} 个文档文件")
    
    def _is_external_link(self, link):
        """检查是否为外部链接"""
        parsed = urlparse(link)
        return bool(parsed.netloc) or link.startswith('http')
    
    def _is_valid_internal_link(self, link, base_path=None):
        """检查内部链接是否有效"""
        # 去除锚点和查询参数
        link = link.split('#')[0].split('?')[0]
        
        # 跳过空链接
        if not link:
            return True
        
        # 如果是完整的路径
        if link in self.valid_paths:
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
            return abs_path in self.valid_paths
        
        # 如果是以/开头的绝对路径
        if link.startswith('/'):
            # 去除开头的斜杠
            clean_link = link[1:]
            return clean_link in self.valid_paths
        
        return False
    
    def extract_links_from_file(self, file_path):
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
    
    def check_links(self, specific_file=None):
        """检查所有文档中的链接"""
        if specific_file:
            # 只检查特定文件
            if os.path.exists(specific_file):
                rel_path = os.path.relpath(specific_file, self.docs_dir)
                path_without_ext = os.path.splitext(rel_path)[0].replace('\\', '/')
                self._check_file_links(specific_file, path_without_ext)
            else:
                print(f"错误: 文件 {specific_file} 不存在")
        else:
            # 检查所有文档
            for path_without_ext, file_path in self.documents.items():
                self._check_file_links(file_path, path_without_ext)
        
        # 输出结果
        self._print_results()
    
    def _check_file_links(self, file_path, doc_path):
        """检查单个文件中的链接"""
        links = self.extract_links_from_file(file_path)
        
        for link in links:
            # 跳过外部链接和锚点链接
            if self._is_external_link(link) or link.startswith('#'):
                continue
            
            # 检查内部链接是否有效
            if not self._is_valid_internal_link(link, doc_path):
                self.broken_links[doc_path].append(link)
    
    def _print_results(self):
        """打印检查结果"""
        if not self.broken_links:
            print("✅ 所有链接检查完毕，未发现无效链接！")
            return
        
        print("\n🔍 链接检查结果:")
        print("=" * 80)
        
        total_broken = sum(len(links) for links in self.broken_links.values())
        print(f"共发现 {total_broken} 个无效链接，分布在 {len(self.broken_links)} 个文档中")
        print("=" * 80)
        
        for doc, links in self.broken_links.items():
            print(f"\n📄 文档: {doc}")
            for link in links:
                print(f"   ❌ 无效链接: {link}")
        
        print("\n" + "=" * 80)

def main():
    parser = argparse.ArgumentParser(description='检查Mintlify文档中的内部链接')
    parser.add_argument('--docs-dir', type=str, required=True, help='文档根目录路径')
    parser.add_argument('--docs-json', type=str, required=True, help='docs.json文件路径')
    parser.add_argument('--file', type=str, help='要检查的特定文件路径（可选）')
    parser.add_argument('--lang', type=str, default='zh-hans', help='基础语言（默认: zh-hans）')
    
    args = parser.parse_args()
    
    checker = LinkChecker(args.docs_dir, args.docs_json, args.lang)
    checker.check_links(args.file)

if __name__ == '__main__':
    main()
