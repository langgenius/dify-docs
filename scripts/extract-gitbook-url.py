#!/usr/bin/env python3
"""
改进的GitBook Summary链接提取器 (支持目录输出)

此脚本从SUMMARY.md文件中提取所有内容，
保留原始的目录结构和标题，
将链接转换为在线URL（不包含.md后缀）。
支持将输出文件放在指定目录中。
"""

import os
import re
import sys
import urllib.parse

def process_summary_file(summary_path, base_url):
    """
    处理SUMMARY.md文件，保留结构并转换链接
    
    Args:
        summary_path: SUMMARY.md文件的路径
        base_url: 基础URL
        
    Returns:
        processed_content: 处理后的内容
    """
    print(f"正在处理 {summary_path}...")
    
    try:
        with open(summary_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)
    
    # 确保base_url以/结尾
    if not base_url.endswith('/'):
        base_url += '/'
    
    # 处理每一行
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # 提取行中的Markdown链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, line)
        
        processed_line = line
        
        # 替换每个链接
        for text, link in matches:
            # 跳过锚点链接
            if link.startswith('#'):
                continue
            
            # 构建完整URL
            if not link.startswith(('http://', 'https://')):
                if link.startswith('/'):
                    link = link[1:]
                full_url = urllib.parse.urljoin(base_url, link)
            else:
                full_url = link
            
            # 移除.md后缀
            if full_url.endswith('.md'):
                full_url = full_url[:-3]
            
            # 替换链接
            original_link = f"[{text}]({link})"
            new_link = f"[{text}]({full_url})"
            processed_line = processed_line.replace(original_link, new_link)
        
        processed_lines.append(processed_line)
    
    return '\n'.join(processed_lines)


def save_to_markdown(content, output_path):
    """
    保存处理后的内容到Markdown文件
    
    Args:
        content: 处理后的内容
        output_path: 输出文件路径
    """
    # 检查路径是否是目录
    if os.path.isdir(output_path):
        # 如果是目录，在该目录中创建默认文件名
        output_file = os.path.join(output_path, "gitbook-urls.md")
    else:
        # 否则使用提供的路径
        output_file = output_path
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"已创建目录: {output_dir}")
        except Exception as e:
            print(f"创建目录时出错: {e}")
            sys.exit(1)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Markdown文件已生成: {output_file}")
    except Exception as e:
        print(f"写入文件时出错: {e}")
        sys.exit(1)


def add_header(content):
    """
    向内容添加标题和说明
    
    Args:
        content: 原始内容
        
    Returns:
        new_content: 添加标题和说明后的内容
    """
    header = "# GitBook文档链接\n\n"
    header += "以下是从SUMMARY.md提取的文档结构和链接：\n\n"
    
    return header + content


if __name__ == "__main__":
    print("=" * 60)
    print("改进的GitBook Summary链接提取器 (支持目录输出)")
    print("=" * 60)
    
    # 获取SUMMARY.md文件路径
    if len(sys.argv) > 1:
        summary_path = sys.argv[1]
    else:
        summary_path = input("请输入SUMMARY.md文件路径: ").strip()
        if not summary_path:
            summary_path = os.path.join(os.getcwd(), "SUMMARY.md")
            print(f"使用默认路径: {summary_path}")
    
    # 检查文件是否存在
    if not os.path.isfile(summary_path):
        print(f"错误: 文件 '{summary_path}' 不存在")
        sys.exit(1)
    
    # 获取基础URL
    if len(sys.argv) > 2:
        base_url = sys.argv[2]
    else:
        base_url = input("请输入文档基础URL: ").strip()
        if not base_url:
            base_url = "https://docs.example.com/"
            print(f"使用默认URL: {base_url}")
    
    # 获取输出文件路径或目录
    if len(sys.argv) > 3:
        output_path = sys.argv[3]
    else:
        default_output = os.path.join(os.path.dirname(summary_path), "gitbook-urls.md")
        output_path = input(f"请输入输出文件路径或目录 [默认: {default_output}]: ").strip()
        if not output_path:
            output_path = default_output
    
    # 处理文件内容
    processed_content = process_summary_file(summary_path, base_url)
    
    # 添加标题和说明
    final_content = add_header(processed_content)
    
    # 保存到Markdown文件
    save_to_markdown(final_content, output_path)
    
    print("\n处理完成！")