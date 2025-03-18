#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("md-to-mdx")

class MarkdownToMDXConverter:
    def __init__(self):
        self.conversion_count = 0
        self.error_count = 0
        self.base_output_dir = None
    
    def process_directory(self, input_dir, output_dir=None, recursive=True):
        """处理指定目录中的所有Markdown文件"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            logger.error(f"输入目录不存在: {input_dir}")
            return
        
        if self.base_output_dir is None and output_dir:
            self.base_output_dir = Path(output_dir)
            self.base_input_dir = input_path
            self.base_output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建基础输出目录: {self.base_output_dir}")
        
        for file in input_path.glob("*.md"):
            if self.base_output_dir:
                rel_path = file.parent.relative_to(self.base_input_dir) if file.parent != self.base_input_dir else Path('')
                target_dir = self.base_output_dir / rel_path
                target_dir.mkdir(parents=True, exist_ok=True)
                self._process_file(file, target_dir)
            else:
                self._process_file(file, file.parent)
        
        if recursive:
            for subdir in [d for d in input_path.iterdir() if d.is_dir()]:
                if subdir.name == "output" or subdir.name.startswith('.'):
                    continue
                self.process_directory(subdir, output_dir, recursive)
    
    def _process_file(self, file_path, output_dir):
        """处理单个Markdown文件"""
        try:
            logger.info(f"处理文件: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = self._fix_broken_text(content)
            content = self._convert_images(content)
            content = self._convert_hints(content)
            converted_content = self.convert_content(content)
            
            output_file = output_dir / (file_path.stem + ".mdx")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            
            logger.info(f"转换完成: {output_file}")
            self.conversion_count += 1
                
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            self.error_count += 1
    
    def _fix_broken_text(self, content):
        """修复文本中的割裂问题，特别是在代码块周围"""
        broken_code_pattern = re.compile(r'```([a-zA-Z]*)\r?\n(.*?)\r?\n```([a-zA-Z]*)', re.DOTALL)
        content = broken_code_pattern.sub(r'```\1\n\2\n```', content)
        return content
    
    def _convert_images(self, content):
        """转换HTML图片格式为Markdown或MDX格式"""
        
        # 转换没有标题的 <figure><img> 结构
        img_pattern_no_caption = re.compile(r'<figure>\s*<img src="([^"]+)" alt="([^"]*)">\s*<figcaption></figcaption>\s*</figure>', re.DOTALL)
        content = img_pattern_no_caption.sub(r'![](\1)', content)
        
        # 转换带标题的 <figure><img> 结构
        img_pattern_with_caption = re.compile(r'<figure>\s*<img src="([^"]+)" alt="([^"]*)">\s*<figcaption><p>(.*?)</p></figcaption>\s*</figure>', re.DOTALL)
        def img_replacer(match):
            img_src = match.group(1)
            alt_text = match.group(3).strip()
            return f'![{alt_text}]({img_src})'
        content = img_pattern_with_caption.sub(img_replacer, content)
        
        return content
    
    def _convert_hints(self, content):
        """转换 hint 提示框"""
        hint_pattern = re.compile(r'{%\s*hint\s*style="info"\s*%}\s*{%\s*endhint\s*%}', re.DOTALL)
        content = hint_pattern.sub(r'<Info>\n</Info>', content)
        return content
    
    def convert_content(self, content):
        """将Gitbook Markdown内容转换为Mintlify MDX格式"""
        h1_pattern = re.compile(r'^#\s+(.+?)$', re.MULTILINE)
        match = h1_pattern.search(content)
        if match:
            title = match.group(1).strip()
            content = h1_pattern.sub(f'---\ntitle: {title}\n---\n', content, count=1)
        return content
    
    def get_statistics(self):
        """返回处理统计信息"""
        return {
            "conversion_count": self.conversion_count,
            "error_count": self.error_count
        }

def main():
    print("=" * 60)
    print("Gitbook Markdown 转 Mintlify MDX 转换工具")
    print("=" * 60)
    
    input_path_str = input("请输入源文件或目录路径: ")
    input_path = Path(input_path_str)
    
    if not input_path.exists():
        print(f"错误: 路径 '{input_path_str}' 不存在!")
        return
    
    recursive = False
    if input_path.is_dir():
        recursive_input = input("是否递归处理所有子目录? (y/n): ").lower()
        recursive = recursive_input in ('y', 'yes')
    
    if input_path.is_file():
        output_dir = input_path.parent / "output"
    else:
        output_dir = input_path / "output"
    
    converter = MarkdownToMDXConverter()
    
    if input_path.is_file() and input_path.suffix.lower() == '.md':
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录已创建: {output_dir}")
        converter._process_file(input_path, output_dir)
    elif input_path.is_dir():
        converter.process_directory(input_path, output_dir, recursive)
    else:
        logger.error(f"无效的输入路径: {input_path_str}")
        print(f"错误: '{input_path_str}' 不是有效的Markdown文件或目录!")
        return
    
    stats = converter.get_statistics()
    print("=" * 60)
    print(f"转换完成! 成功转换: {stats['conversion_count']}个文件, 错误: {stats['error_count']}个文件")
    print(f"转换结果已保存至: {output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
