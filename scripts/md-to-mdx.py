#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
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
    def __init__(self, backup=True, in_place=False):
        self.backup = backup
        self.in_place = in_place
        self.conversion_count = 0
        self.error_count = 0
        self.base_output_dir = None
    
    def process_directory(self, input_dir, output_dir=None, recursive=True):
        """处理指定目录中的所有Markdown文件"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            logger.error(f"输入目录不存在: {input_dir}")
            return
        
        # 保存基础输出目录，用于构建子目录输出路径
        if not self.in_place and self.base_output_dir is None and output_dir:
            self.base_output_dir = Path(output_dir)
            self.base_input_dir = input_path
            self.base_output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建基础输出目录: {self.base_output_dir}")
        
        # 处理当前目录中的所有.md和.mdx文件
        for file in list(input_path.glob("*.md")) + list(input_path.glob("*.mdx")):
            if self.in_place:
                # 在原位置处理
                self._process_file(file, file.parent, delete_original=True)
            else:
                # 计算相对于基础输入目录的路径
                if self.base_output_dir:
                    rel_path = file.parent.relative_to(self.base_input_dir) if file.parent != self.base_input_dir else Path('')
                    target_dir = self.base_output_dir / rel_path
                    target_dir.mkdir(parents=True, exist_ok=True)
                    self._process_file(file, target_dir)
                else:
                    # 如果没有基础输出目录，则就地处理
                    self._process_file(file, file.parent)
        
        # 如果需要递归处理子目录
        if recursive:
            for subdir in [d for d in input_path.iterdir() if d.is_dir()]:
                # 跳过output目录，避免重复处理
                if subdir.name == "output" or subdir.name.startswith('.'):
                    continue
                
                self.process_directory(subdir, output_dir, recursive)
    
    def _process_file(self, file_path, output_dir, delete_original=False):
        """处理单个Markdown文件"""
        try:
            logger.info(f"处理文件: {file_path}")
            
            # 备份原始文件（如果需要）
            if self.backup:
                backup_file = str(file_path) + ".bak"
                if not os.path.exists(backup_file):
                    shutil.copy2(file_path, backup_file)
                    logger.info(f"已创建备份: {backup_file}")
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 执行转换
            converted_content = self.convert_content(content)
            
            # 确定输出文件路径
            output_file = output_dir / (file_path.stem + ".mdx")
            
            # 写入转换后的内容
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            
            logger.info(f"转换完成: {output_file}")
            self.conversion_count += 1
            
            # 如果需要，删除原始文件
            if delete_original:
                try:
                    os.remove(file_path)
                    logger.info(f"已删除源文件: {file_path}")
                except Exception as e:
                    logger.error(f"删除源文件 {file_path} 失败: {str(e)}")
                
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            self.error_count += 1
    
    def convert_content(self, content):
        """将Gitbook Markdown内容转换为Mintlify MDX格式"""
        
        # 1. 转换文档开头的h1元素为frontmatter
        h1_pattern = re.compile(r'^#\s+(.+?)$', re.MULTILINE)
        match = h1_pattern.search(content)
        if match:
            title = match.group(1).strip()
            content = h1_pattern.sub(f'---\ntitle: {title}\n---\n', content, count=1)
        
        # 2. 转换hint提示框
        hint_pattern = re.compile(
            r'{%\s*hint\s+style="(\w+)"\s*%}(.*?){%\s*endhint\s*%}', 
            re.DOTALL
        )
        
        def hint_replacer(match):
            style = match.group(1)
            text = match.group(2).strip()
            component_name = style.capitalize() if style != "info" else "Info"
            return f'<{component_name}>\n{text}\n</{component_name}>'
        
        content = hint_pattern.sub(hint_replacer, content)
        
        # 3. 转换卡片链接
        card_pattern = re.compile(
            r'{%\s*content-ref\s+url="([^"]+)"\s*%}\s*\[([^\]]+)\]\(([^)]+)\)\s*{%\s*endcontent-ref\s*%}',
            re.DOTALL
        )
        
        def card_replacer(match):
            url = match.group(1)
            title = match.group(2)
            return f'<Card title="{title}" icon="link" href="{url}">\n  {title}\n</Card>'
        
        content = card_pattern.sub(card_replacer, content)
        
        # 4. 转换并排图片样式
        # 寻找连续的图片并转换为并排布局
        img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)\s*!\[(.*?)\]\((.*?)\)', re.DOTALL)
        
        def img_side_replacer(match):
            alt1 = match.group(1) or "Image 1"
            src1 = match.group(2)
            alt2 = match.group(3) or "Image 2"
            src2 = match.group(4)
            
            return f'''<div class="image-side-by-side">
  <figure>
    <img src="{src1}" alt="{alt1}" />
  </figure>
  <figure>
    <img src="{src2}" alt="{alt2}" />
  </figure>
</div>'''
        
        content = img_pattern.sub(img_side_replacer, content)
        
        # 5. 转换Frame包装的图片
        frame_pattern = re.compile(r'<Frame>\s*<img\s+src="([^"]+)"\s+alt="([^"]+)"\s*/>\s*</Frame>', re.DOTALL)
        
        def frame_replacer(match):
            src = match.group(1)
            alt = match.group(2)
            return f'![{alt}]({src})'
        
        content = frame_pattern.sub(frame_replacer, content)
        
        # 5.1 转换<figure><img>格式的带有宽度和figcaption的图片为特定格式
        figure_img_width_caption_pattern = re.compile(r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="(\d+)"\s*/?>\s*<figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption>\s*</figure>', re.DOTALL)
        
        def figure_img_width_caption_replacer(match):
            src = match.group(1)
            alt = match.group(2) or ""
            width = match.group(3)
            caption = match.group(4).strip()
            
            # 如果有caption，将其添加到alt中
            if caption:
                alt = caption
            
            return f'''<img
src="{src}"
width="{width}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = figure_img_width_caption_pattern.sub(figure_img_width_caption_replacer, content)
        
        # 5.2 转换<figure><img>格式的带有宽度但没有figcaption的图片
        figure_img_width_pattern = re.compile(r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="(\d+)"\s*/?>\s*</figure>', re.DOTALL)
        
        def figure_img_width_replacer(match):
            src = match.group(1)
            alt = match.group(2) or ""
            width = match.group(3)
            
            return f'''<img
src="{src}"
width="{width}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = figure_img_width_pattern.sub(figure_img_width_replacer, content)
        
        # 5.3 转换<figure><img>格式的没有宽度但有figcaption的图片
        figure_img_caption_pattern = re.compile(r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/?>\s*<figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption>\s*</figure>', re.DOTALL)
        
        def figure_img_caption_replacer(match):
            src = match.group(1)
            alt = match.group(2) or ""
            caption = match.group(3).strip()
            
            # 如果有caption，将其添加到alt中
            if caption:
                alt = caption
            
            return f'''<img
src="{src}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = figure_img_caption_pattern.sub(figure_img_caption_replacer, content)
        
        # 5.4 处理没有figcaption和宽度的<figure><img>标签
        figure_img_no_caption_pattern = re.compile(r'<figure>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/?>\s*</figure>', re.DOTALL)
        
        def figure_img_no_caption_replacer(match):
            src = match.group(1)
            alt = match.group(2) or ""
            
            return f'''<img
src="{src}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = figure_img_no_caption_pattern.sub(figure_img_no_caption_replacer, content)
        
        # 6. 转换Tabs组件
        # 先匹配整个tabs块
        tabs_pattern = re.compile(
            r'{%\s*tabs\s*%}(.*?){%\s*endtabs\s*%}',
            re.DOTALL
        )
        
        def tabs_replacer(match):
            tabs_content = match.group(1)
            # 匹配每个tab
            tab_pattern = re.compile(
                r'{%\s*tab\s+title="([^"]+)"\s*%}(.*?){%\s*endtab\s*%}',
                re.DOTALL
            )
            
            # 构建新的Tabs组件
            tabs_start = "<Tabs>"
            tabs_items = []
            
            for tab_match in tab_pattern.finditer(tabs_content):
                title = tab_match.group(1)
                content = tab_match.group(2).strip()
                tabs_items.append(f'  <Tab title="{title}">\n    {content}\n  </Tab>')
            
            tabs_end = "</Tabs>"
            
            return tabs_start + "\n" + "\n".join(tabs_items) + "\n" + tabs_end
        
        content = tabs_pattern.sub(tabs_replacer, content)
        
        # 7. 处理有限制大小的独立img标签
        img_size_pattern = re.compile(r'<img\s+src="([^"]+)"\s+width="(\d+)"(?:\s+alt="([^"]*)")?\s*/>', re.DOTALL)
        
        def img_size_replacer(match):
            src = match.group(1)
            width = match.group(2)
            alt = match.group(3) if match.group(3) else ""
            
            return f'''<img
src="{src}"
width="{width}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = img_size_pattern.sub(img_size_replacer, content)
        
        # 7.1 处理各种形式的独立<img>标签
        standalone_img_pattern = re.compile(r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?[^>]*>', re.DOTALL)
        
        def standalone_img_replacer(match):
            src = match.group(1)
            alt = match.group(2) if match.group(2) else ""
            
            return f'''<img
src="{src}"
className="mx-auto"
alt="{alt}"
/>'''
        
        content = standalone_img_pattern.sub(standalone_img_replacer, content)
        
        # 8. 将markdown表格转换为MDX表格格式
        # 使用正则表达式匹配markdown表格
        table_pattern = re.compile(r'(\|.*\|\n\|[-:\s|]*\|\n(?:\|.*\|\n)+)', re.MULTILINE)
        
        def table_replacer(match):
            md_table = match.group(1)
            lines = md_table.strip().split('\n')
            
            # 提取表头和表体
            header_row = lines[0]
            header_cells = [cell.strip() for cell in header_row.split('|')[1:-1]]
            
            # 忽略分隔行
            body_rows = lines[2:]
            body_cells_rows = []
            for row in body_rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                body_cells_rows.append(cells)
            
            # 按照要求的格式构建MDX表格
            mdx_table = "<table>\n  <thead>\n    <tr>\n"
            
            # 添加表头
            for cell in header_cells:
                mdx_table += f"      <th>{cell}</th>\n"
            
            mdx_table += "    </tr>\n  </thead>\n  <tbody>\n"
            
            # 添加表体
            for row_cells in body_cells_rows:
                mdx_table += "    <tr>\n"
                for cell in row_cells:
                    # 先转换Markdown链接为HTML链接
                    # 匹配 [text](url) 格式
                    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
                    cell = link_pattern.sub(r'<a href="\2">\1</a>', cell)
                    
                    # 替换<br>标签为</p><p>，实现正确的段落分隔
                    # 先处理<br>标签（可能有不同形式：<br>, <br/>, <br />）
                    br_pattern = re.compile(r'<br\s*/?>')
                    
                    # 处理单元格中的<p>和<br>标签
                    if '<p>' in cell or br_pattern.search(cell):
                        # 如果已有<p>标签但包含<br>，替换<br>为</p><p>
                        if '<p>' in cell and br_pattern.search(cell):
                            cell = br_pattern.sub(r'</p>\n        <p>', cell)
                            # 清理末尾的空<br>标签
                            cell = re.sub(r'<br\s*/?>(\s*</p>)', r'\1', cell)
                        # 如果没有<p>标签但有<br>，用<p>标签包装每个段落
                        elif br_pattern.search(cell) and not '<p>' in cell:
                            paragraphs = br_pattern.split(cell)
                            cell = '<p>' + '</p>\n        <p>'.join([p.strip() for p in paragraphs if p.strip()]) + '</p>'
                    
                        # 确保缩进正确
                        mdx_table += f"      <td>\n        {cell}\n      </td>\n"
                    else:
                        # 普通文本单元格
                        mdx_table += f"      <td>{cell}</td>\n"
                mdx_table += "    </tr>\n"
            
            mdx_table += "  </tbody>\n</table>"
            
            return mdx_table
        
        content = table_pattern.sub(table_replacer, content)
        
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
    
    # 通过交互方式获取输入路径
    input_path_str = input("请输入源文件或目录路径: ")
    input_path = Path(input_path_str)
    
    if not input_path.exists():
        print(f"错误: 路径 '{input_path_str}' 不存在!")
        return
    
    # 询问是否递归处理子目录
    recursive = False
    if input_path.is_dir():
        recursive_input = input("是否递归处理所有子目录? (y/n): ").lower()
        recursive = recursive_input in ('y', 'yes')
    
    # 询问是否创建备份
    backup_input = input("是否创建备份文件? (y/n, 默认:y): ").lower()
    create_backup = backup_input in ('', 'y', 'yes')
    
    # 询问是否原地转换并删除源文件
    in_place_input = input("是否在原地转换并删除源文件? (y/n, 默认:n): ").lower()
    in_place = in_place_input in ('y', 'yes')
    
    # 确定输出目录
    output_dir = None
    if not in_place:
        if input_path.is_file():
            output_dir = input_path.parent / "output"
        else:
            output_dir = input_path / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录已创建: {output_dir}")
    
    # 创建转换器并处理文件
    converter = MarkdownToMDXConverter(backup=create_backup, in_place=in_place)
    
    if input_path.is_file() and input_path.suffix.lower() == '.md':
        # 处理单个文件
        if in_place:
            converter._process_file(input_path, input_path.parent, delete_original=True)
        else:
            converter._process_file(input_path, output_dir)
    elif input_path.is_dir():
        # 处理目录
        converter.process_directory(input_path, output_dir, recursive)
    else:
        logger.error(f"无效的输入路径: {input_path_str}")
        print(f"错误: '{input_path_str}' 不是有效的Markdown文件或目录!")
        return
    
    # 打印统计信息
    stats = converter.get_statistics()
    print("=" * 60)
    print(f"转换完成! 成功转换: {stats['conversion_count']}个文件, 错误: {stats['error_count']}个文件")
    if not in_place and output_dir:
        print(f"转换结果已保存至: {output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()