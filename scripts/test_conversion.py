#!/usr/bin/env python3
"""
测试脚本，用于测试图片格式转换
"""

import re
from typing import Tuple, List

# 匹配Frame标签中的图片
FRAME_IMG_PATTERN = re.compile(
    r'<Frame(?:\s+caption="([^"]*)")?(?:\s+width="([^"]*)")?\s*>\s*'
    r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*(?:\/\s*>|\/ >|>\s*<\/img>)\s*'
    r'<\/Frame>', 
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
    
    # 执行替换
    new_content = FRAME_IMG_PATTERN.sub(replace_frame, content)
    
    return new_content, replacements

# 测试
test_file = "/Users/allen/Documents/dify-docs-mintlify/zh-hans/guides/workflow/nodes/ifelse.mdx"

# 读取文件
with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 测试匹配
matches = FRAME_IMG_PATTERN.findall(content)
print(f"找到 {len(matches)} 个匹配")

# 打印匹配详情
for i, match in enumerate(matches):
    caption, width, src, alt = match
    print(f"Match {i+1}:")
    print(f"  caption: '{caption}'")
    print(f"  width: '{width}'")
    print(f"  src: '{src}'")
    print(f"  alt: '{alt}'")

# 测试转换
new_content, replacements = convert_frame_to_markdown(content)

# 打印替换详情
print(f"\n找到 {len(replacements)} 个需要替换的内容")
for i, (original, new, format_type) in enumerate(replacements):
    print(f"替换 {i+1} ({format_type}):")
    print(f"原始: {original[:100]}...")
    print(f"新的: {new}")
    print()

# 如果找到替换内容，则写入文件
if replacements:
    print("替换后的内容示例:")
    # 显示部分替换后的内容
    for line in new_content.split('\n')[:20]:
        print(line)
