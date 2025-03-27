#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MDX文档链接验证脚本
检查当前目录中所有.mdx文件中的相对链接是否有效
"""

import os
import re
import sys
from pathlib import Path
from tabulate import tabulate
import glob

def extract_links(file_path):
    """提取文件中的所有链接，返回链接及其所在行号"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
    
    image_pattern = r'!\[.*?\]\((.*?)\)'  # 匹配图片 ![alt](src)
    link_pattern = r'(?<!!)\[.*?\]\((.*?)\)'  # 匹配普通链接 [text](href)，但排除图片链接
    
    issues = []
    
    for line_num, line in enumerate(content, 1):
        # 提取图片链接
        for match in re.finditer(image_pattern, line):
            link = match.group(1)
            if not link.startswith(('http://', 'https://')):
                issues.append({
                    'file': str(file_path),
                    'line': line_num,
                    'link': link,
                    'type': '图片',
                    'issue': '相对路径图片链接' 
                })
        
        # 提取普通链接
        for match in re.finditer(link_pattern, line):
            link = match.group(1)
            # 只检查相对链接
            if not link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                issues.append({
                    'file': str(file_path),
                    'line': line_num,
                    'link': link,
                    'type': '文档',
                    'issue': '需验证的文档链接'
                })
    
    return issues

def validate_doc_link(link, root_dir):
    """验证文档链接是否有效"""
    # 移除查询参数和锚点
    link = link.split('#')[0].split('?')[0]
    
    # 如果是空链接，认为是有效的
    if not link:
        return True
    
    # 处理相对路径
    link_path = link.lstrip('/')
    
    # 如果没有扩展名，尝试添加.mdx
    if not os.path.splitext(link_path)[1]:
        link_path = f"{link_path}.mdx"
    
    # 检查文件是否存在
    target_path = os.path.join(root_dir, link_path)
    return os.path.exists(target_path)

def main():
    current_dir = os.getcwd()
    mdx_files = glob.glob('**/*.mdx', recursive=True)
    
    if not mdx_files:
        output = "当前目录及子目录中未找到.mdx文件"
        print(output)
        with open('out_put.md', 'w', encoding='utf-8') as f:
            f.write(output)
        return
    
    all_issues = []
    
    # 收集所有可能的文档路径，用于验证链接
    doc_paths = set()
    for mdx_file in mdx_files:
        # 添加完整路径
        doc_paths.add(mdx_file)
        # 添加不带扩展名的路径
        without_ext = os.path.splitext(mdx_file)[0]
        doc_paths.add(without_ext)
    
    for mdx_file in mdx_files:
        file_path = Path(mdx_file)
        issues = extract_links(file_path)
        
        # 验证文档链接
        for issue in issues:
            if issue['type'] == '文档':
                link = issue['link']
                # 处理相对路径
                if link.startswith('/'):
                    is_valid = validate_doc_link(link, current_dir)
                    if not is_valid:
                        issue['issue'] = '无效的文档链接'
                    else:
                        continue  # 跳过有效链接
                else:
                    # 相对于当前文件的链接
                    base_dir = file_path.parent
                    target = (base_dir / link).resolve()
                    target_rel = os.path.relpath(target, current_dir)
                    
                    if not target.exists() and not target.with_suffix('.mdx').exists():
                        issue['issue'] = '无效的文档链接'
                    else:
                        continue  # 跳过有效链接
            
            all_issues.append(issue)
    
    if all_issues:
        # 按文件名和行号排序
        all_issues.sort(key=lambda x: (x['file'], x['line']))
        
        # 准备表格数据
        table_data = [[
            issue['file'], 
            issue['line'], 
            issue['type'], 
            issue['link'], 
            issue['issue']
        ] for issue in all_issues]
        
        headers = ['文件', '行号', '类型', '链接', '问题']
        output = tabulate(table_data, headers=headers, tablefmt='grid')
        output += f"\n\n总共发现 {len(all_issues)} 个需要检查的链接问题"
        
        # 打印到控制台
        print(output)
        
        # 保存到文件
        with open('out_put.md', 'w', encoding='utf-8') as f:
            f.write("# MDX文档链接检查结果\n\n")
            
            # 添加Markdown格式的表格
            md_table = "| " + " | ".join(headers) + " |\n"
            md_table += "| " + " | ".join(["---" for _ in headers]) + " |\n"
            
            for row in table_data:
                md_table += "| " + " | ".join(map(str, row)) + " |\n"
            
            f.write(md_table)
            f.write(f"\n总共发现 {len(all_issues)} 个需要检查的链接问题\n")
        
        print(f"\n结果已保存到 out_put.md 文件中")
    else:
        output = "未发现链接问题"
        print(output)
        with open('out_put.md', 'w', encoding='utf-8') as f:
            f.write("# MDX文档链接检查结果\n\n")
            f.write(output)
        print("\n结果已保存到 out_put.md 文件中")

if __name__ == "__main__":
    main()
