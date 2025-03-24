#!/usr/bin/env python3
"""
本地GitBook Markdown文件链接检查工具

此脚本会:
1. 从SUMMARY.md提取所有文档链接
2. 解析每个本地Markdown文件
3. 提取并验证文件中的内部链接
4. 生成链接检查报告
"""

import os
import re
import sys
import csv
from datetime import datetime
from urllib.parse import urlparse, urljoin

# 尝试导入依赖，如果不存在则自动安装
try:
    from bs4 import BeautifulSoup
    import markdown
except ImportError:
    print("正在安装必要依赖...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "markdown"])
    from bs4 import BeautifulSoup
    import markdown


class GitbookLocalChecker:
    """GitBook本地文件链接检查工具"""
    
    def __init__(self, summary_path, base_dir=None, remove_md=True):
        """
        初始化链接检查器
        
        Args:
            summary_path: SUMMARY.md文件路径
            base_dir: 文档根目录，默认为SUMMARY.md所在目录
            remove_md: 是否移除.md后缀
        """
        self.summary_path = os.path.abspath(summary_path)
        self.base_dir = base_dir or os.path.dirname(self.summary_path)
        self.remove_md = remove_md
        self.all_links = []
        self.all_md_files = []
        self.invalid_links = []
        
        # 记录解析过的文件，避免重复处理
        self.processed_files = set()
    
    def extract_summary_links(self):
        """从SUMMARY.md提取所有Markdown文件链接"""
        print(f"正在从 {self.summary_path} 提取文档链接...")
        
        with open(self.summary_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 使用正则表达式提取链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        links = []
        for i, (text, link) in enumerate(matches, 1):
            # 排除锚点链接
            if not link.startswith('#') and link.endswith('.md'):
                # 计算本地文件路径
                local_path = os.path.normpath(os.path.join(self.base_dir, link))
                
                links.append({
                    'id': i,
                    'text': text,
                    'link': link,
                    'local_path': local_path,
                    'exists': os.path.exists(local_path),
                    'type': 'summary_link',
                    'source_file': 'SUMMARY.md'
                })
                
                # 将文件添加到待处理列表
                if os.path.exists(local_path):
                    self.all_md_files.append(local_path)
        
        print(f"找到 {len(links)} 个文档链接，{len(self.all_md_files)} 个本地Markdown文件")
        self.all_links.extend(links)
        return links
    
    def process_md_file(self, file_path):
        """处理单个Markdown文件，提取其中的链接"""
        # 如果文件已处理，跳过
        if file_path in self.processed_files:
            return []
        
        self.processed_files.add(file_path)
        relative_path = os.path.relpath(file_path, self.base_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 提取所有链接
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, content)
            
            links = []
            for text, link in matches:
                # 排除外部链接和锚点链接
                if link.startswith(('http://', 'https://', '#')):
                    continue
                
                # 解析相对路径
                if link.startswith('/'):
                    # 从根目录计算
                    target_path = os.path.normpath(os.path.join(self.base_dir, link.lstrip('/')))
                else:
                    # 从当前文件所在目录计算
                    target_path = os.path.normpath(os.path.join(os.path.dirname(file_path), link))
                
                # 如果链接没有扩展名但指向目录，添加README.md
                if not os.path.splitext(target_path)[1]:
                    if os.path.isdir(target_path):
                        target_path = os.path.join(target_path, 'README.md')
                    else:
                        # 可能是不带扩展名的文件引用，添加.md
                        target_path += '.md'
                
                # 检查链接是否有效
                exists = os.path.exists(target_path)
                
                link_info = {
                    'text': text,
                    'link': link,
                    'local_path': target_path,
                    'target_file': os.path.basename(target_path),
                    'exists': exists,
                    'type': 'internal_link',
                    'source_file': relative_path
                }
                
                links.append(link_info)
                
                # 如果链接无效，添加到无效链接列表
                if not exists:
                    self.invalid_links.append(link_info)
                # 如果是有效的Markdown文件且尚未处理，添加到待处理列表
                elif target_path.endswith('.md') and target_path not in self.processed_files:
                    self.all_md_files.append(target_path)
            
            return links
            
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            return []
    
    def process_all_files(self):
        """处理所有Markdown文件"""
        print("开始处理所有Markdown文件...")
        
        # 先提取SUMMARY.md中的链接
        self.extract_summary_links()
        
        # 处理所有Markdown文件
        files_to_process = list(self.all_md_files)  # 创建副本，因为处理过程中会添加新文件
        processed_count = 0
        
        for file_path in files_to_process:
            if file_path not in self.processed_files:
                relative_path = os.path.relpath(file_path, self.base_dir)
                print(f"处理文件: {relative_path}")
                
                links = self.process_md_file(file_path)
                self.all_links.extend(links)
                
                processed_count += 1
                
                # 如果发现新文件，可能需要处理它们
                new_files = [f for f in self.all_md_files if f not in files_to_process and f not in self.processed_files]
                files_to_process.extend(new_files)
        
        print(f"已处理 {processed_count} 个Markdown文件")
        print(f"共找到 {len(self.all_links)} 个链接，其中 {len(self.invalid_links)} 个无效")
    
    def generate_markdown_report(self, output_path):
        """生成Markdown格式的报告"""
        print(f"正在生成报告: {output_path}")
        
        content = f"""# GitBook本地链接检查报告

## 摘要
- 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 处理文件数: {len(self.processed_files)}
- 总链接数: {len(self.all_links)}
- 无效链接数: {len(self.invalid_links)}

## 无效链接列表
"""
        
        # 按源文件分组显示无效链接
        grouped_links = {}
        for link in self.invalid_links:
            source = link['source_file']
            if source not in grouped_links:
                grouped_links[source] = []
            grouped_links[source].append(link)
        
        for source, links in sorted(grouped_links.items()):
            content += f"\n### 文件: {source}\n"
            for link in links:
                content += f"- [{link['text']}]({link['link']}) -> {link['local_path']} (无效)\n"
        
        # 添加所有文件的链接统计
        content += "\n## 文件链接统计\n"
        file_stats = {}
        for link in self.all_links:
            source = link['source_file']
            if source not in file_stats:
                file_stats[source] = {'total': 0, 'invalid': 0}
            file_stats[source]['total'] += 1
            if not link['exists']:
                file_stats[source]['invalid'] += 1
        
        for source, stats in sorted(file_stats.items()):
            content += f"- {source}: 共 {stats['total']} 个链接，{stats['invalid']} 个无效\n"
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"报告已生成: {output_path}")
    
    def generate_csv_report(self, output_path):
        """生成CSV格式的报告"""
        print(f"正在生成CSV报告: {output_path}")
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['source_file', 'text', 'link', 'local_path', 'exists', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for link in self.all_links:
                writer.writerow({
                    'source_file': link['source_file'],
                    'text': link['text'],
                    'link': link['link'],
                    'local_path': link['local_path'],
                    'exists': link['exists'],
                    'type': link['type']
                })
        
        print(f"CSV报告已生成: {output_path}")


def get_input_with_default(prompt, default=None):
    """获取用户输入，如果为空则使用默认值"""
    if default:
        user_input = input(f"{prompt} [{default}]: ")
        return user_input if user_input.strip() else default
    else:
        return input(f"{prompt}: ")


def get_yes_no_input(prompt, default="y"):
    """获取用户是/否输入"""
    valid_responses = {
        'y': True, 'yes': True, '是': True, 
        'n': False, 'no': False, '否': False
    }
    
    if default.lower() in ['y', 'yes', '是']:
        prompt = f"{prompt} [Y/n]: "
        default_value = True
    else:
        prompt = f"{prompt} [y/N]: "
        default_value = False
    
    user_input = input(prompt).lower()
    
    if not user_input:
        return default_value
    
    return valid_responses.get(user_input, default_value)


def main():
    """主函数，交互式获取输入"""
    print("=" * 60)
    print("本地GitBook Markdown文件链接检查工具")
    print("=" * 60)
    
    # 获取SUMMARY.md文件路径
    while True:
        summary_path = get_input_with_default(
            "请输入SUMMARY.md文件路径", 
            os.path.join(os.getcwd(), "SUMMARY.md")
        )
        
        # 检查文件是否存在
        if os.path.isfile(summary_path):
            break
        else:
            print(f"错误: 文件 '{summary_path}' 不存在")
    
    # 获取文档根目录
    default_base_dir = os.path.dirname(os.path.abspath(summary_path))
    base_dir = get_input_with_default(
        "请输入文档根目录(包含所有Markdown文件的目录)", 
        default_base_dir
    )
    
    # 获取输出目录
    output_dir = get_input_with_default(
        "请输入输出目录", 
        os.path.dirname(summary_path) or os.getcwd()
    )
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件路径
    report_path = os.path.join(output_dir, "gitbook-links-report.md")
    csv_path = os.path.join(output_dir, "gitbook-links-report.csv")
    
    # 询问是否移除.md后缀
    remove_md = get_yes_no_input("是否移除链接中的.md后缀", "y")
    
    try:
        # 创建检查器实例
        checker = GitbookLocalChecker(
            summary_path=summary_path,
            base_dir=base_dir,
            remove_md=remove_md
        )
        
        # 处理所有文件
        checker.process_all_files()
        
        # 生成报告
        checker.generate_markdown_report(report_path)
        checker.generate_csv_report(csv_path)
        
        print("\n检查完成！")
        print(f"Markdown报告: {report_path}")
        print(f"CSV报告: {csv_path}")
        
        # 显示摘要
        print(f"\n摘要:")
        print(f"- 处理文件数: {len(checker.processed_files)}")
        print(f"- 总链接数: {len(checker.all_links)}")
        print(f"- 无效链接数: {len(checker.invalid_links)}")
        
        if checker.invalid_links:
            print("\n无效链接示例:")
            for i, link in enumerate(checker.invalid_links[:5], 1):
                print(f"{i}. 文件 '{link['source_file']}' 中 [{link['text']}]({link['link']}) -> {link['local_path']} (无效)")
            
            if len(checker.invalid_links) > 5:
                print(f"... 以及其他 {len(checker.invalid_links) - 5} 个无效链接")
        
    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()