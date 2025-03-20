#!/usr/bin/env python3
"""
多线程版GitBook链接检查器

此脚本使用多线程并行检查在线链接，大幅提高检查速度。
生成两个报告文件：
1. 包含所有链接的完整报告
2. 仅包含错误链接的报告
"""

import os
import re
import sys
import time
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from urllib.parse import urlparse

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    print("正在安装requests库...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    from requests.exceptions import RequestException

class LinkChecker:
    def __init__(self, summary_path, base_dir=None, verify_online=True, max_threads=10):
        """
        初始化链接检查器
        
        Args:
            summary_path: SUMMARY.md文件路径
            base_dir: 文档根目录，默认为SUMMARY.md所在目录
            verify_online: 是否验证在线链接
            max_threads: 最大线程数
        """
        self.summary_path = os.path.abspath(summary_path)
        self.base_dir = base_dir or os.path.dirname(self.summary_path)
        self.verify_online = verify_online
        self.max_threads = max_threads
        self.summary_links = []  # SUMMARY.md中的链接
        self.md_links = defaultdict(list)  # 每个文档中引用的链接
        self.processed_files = set()  # 已处理的文件
        self.summary_content = ""  # SUMMARY.md的内容
        self.invalid_links = []  # 存储所有无效链接
        
        # 图片文件扩展名
        self.image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.tiff', '.webp')
        
        # 在线链接缓存，避免重复检查
        self.online_link_cache = {}
        self.online_link_cache_lock = threading.Lock()  # 线程安全的缓存锁
        
        # 用于存储待检查的在线链接
        self.online_links_queue = queue.Queue()
        
        # 进度统计
        self.total_online_links = 0
        self.checked_online_links = 0
        self.progress_lock = threading.Lock()
    
    def is_image_link(self, link):
        """
        检查链接是否为图片链接
        
        Args:
            link: 链接路径
            
        Returns:
            is_image: 是否为图片链接
        """
        return link.lower().endswith(self.image_extensions)
    
    def check_online_link(self, url):
        """
        检查在线链接是否有效
        
        Args:
            url: 在线链接URL
            
        Returns:
            is_valid: 链接是否有效
        """
        # 如果已经检查过，直接返回缓存结果
        with self.online_link_cache_lock:
            if url in self.online_link_cache:
                return self.online_link_cache[url]
        
        if not self.verify_online:
            # 如果不验证在线链接，默认返回无效
            with self.online_link_cache_lock:
                self.online_link_cache[url] = False
            return False
        
        try:
            # 先尝试HEAD请求，速度更快
            response = requests.head(
                url, 
                timeout=5,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 GitBook-Link-Checker/1.0'}
            )
            
            if response.status_code < 400:
                # 状态码小于400，认为链接有效
                with self.online_link_cache_lock:
                    self.online_link_cache[url] = True
                return True
            
            # HEAD请求失败，尝试GET请求
            response = requests.get(
                url, 
                timeout=5,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 GitBook-Link-Checker/1.0'}
            )
            
            result = response.status_code < 400
            with self.online_link_cache_lock:
                self.online_link_cache[url] = result
            return result
            
        except RequestException:
            # 请求异常，链接无效
            with self.online_link_cache_lock:
                self.online_link_cache[url] = False
            return False
    
    def resolve_path(self, link, current_dir):
        """
        解析链接的实际路径
        
        Args:
            link: 链接路径
            current_dir: 当前文件所在目录
            
        Returns:
            resolved_path: 解析后的路径
            is_external: 是否为外部链接
            is_valid: 链接是否有效
        """
        if not link:
            return None, False, False
        
        # 处理锚点链接
        if '#' in link:
            link_part = link.split('#')[0]
            if not link_part:  # 如果只有锚点，没有路径部分
                return None, False, True  # 假设内部锚点是有效的
            link = link_part
        
        # 检查是否为图片链接
        if self.is_image_link(link):
            return None, False, True  # 跳过图片链接，并假设它们是有效的
        
        # 处理外部链接
        if link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            # 如果是http/https链接，加入待检查队列
            if link.startswith(('http://', 'https://')) and self.verify_online:
                # 将链接添加到待检查队列
                self.online_links_queue.put(link)
                with self.progress_lock:
                    self.total_online_links += 1
                
                # 暂时返回未知状态，后续会更新
                return link, True, None
            elif link.startswith(('http://', 'https://')) and not self.verify_online:
                # 如果不验证在线链接，标记为错误
                return link, True, False
            else:
                # mailto和tel链接默认有效
                return link, True, True
        
        # 处理绝对路径 (从文档根目录开始)
        if link.startswith('/'):
            resolved_path = os.path.normpath(os.path.join(self.base_dir, link.lstrip('/')))
        # 处理相对路径 (从当前文件所在目录开始)
        else:
            resolved_path = os.path.normpath(os.path.join(current_dir, link))
        
        # 处理目录链接
        if os.path.isdir(resolved_path):
            readme_path = os.path.join(resolved_path, 'README.md')
            if os.path.exists(readme_path):
                return readme_path, False, True
            index_path = os.path.join(resolved_path, 'index.md')
            if os.path.exists(index_path):
                return index_path, False, True
            # 如果没有README.md或index.md，保持原样
            return resolved_path, False, os.path.exists(resolved_path)
        
        # 处理不带扩展名的文件引用
        if not os.path.exists(resolved_path) and '.' not in os.path.basename(resolved_path):
            md_path = f"{resolved_path}.md"
            if os.path.exists(md_path):
                return md_path, False, True
        
        return resolved_path, False, os.path.exists(resolved_path)
    
    def online_link_worker(self):
        """工作线程：处理在线链接检查"""
        while True:
            try:
                # 从队列获取链接
                url = self.online_links_queue.get(block=False)
                
                # 检查链接
                is_valid = self.check_online_link(url)
                
                # 更新进度
                with self.progress_lock:
                    self.checked_online_links += 1
                    checked = self.checked_online_links
                    total = self.total_online_links
                
                # 显示进度
                print(f"在线链接检查进度: [{checked}/{total}] - {url} - {'✅' if is_valid else '❌'}")
                
                # 标记任务完成
                self.online_links_queue.task_done()
            except queue.Empty:
                # 队列为空，退出线程
                break
    
    def extract_sections_from_summary(self):
        """
        从SUMMARY.md提取所有章节信息
        
        Returns:
            sections: 章节列表
        """
        print(f"从 {self.summary_path} 提取章节信息...")
        
        try:
            with open(self.summary_path, 'r', encoding='utf-8') as file:
                self.summary_content = file.read()
        except Exception as e:
            print(f"读取文件时出错: {e}")
            sys.exit(1)
        
        # 提取所有章节标题
        sections = []
        section_pattern = r'^#+\s+(.*?)(?:\s+<a.*?>)?$'
        
        for line in self.summary_content.split('\n'):
            match = re.match(section_pattern, line)
            if match:
                section_title = match.group(1).strip()
                sections.append(section_title)
        
        return sections
    
    def extract_links_from_summary(self):
        """
        从SUMMARY.md提取所有链接及其层级结构
        
        Returns:
            links: 链接列表，每项包含链接信息和层级
        """
        print(f"从 {self.summary_path} 提取链接...")
        
        # 记录当前所在章节
        current_section = ""
        sections = self.extract_sections_from_summary()
        
        # 按行处理SUMMARY文件
        links = []
        
        for line in self.summary_content.split('\n'):
            # 检查是否是章节标题行
            section_match = re.match(r'^#+\s+(.*?)(?:\s+<a.*?>)?$', line)
            if section_match:
                current_section = section_match.group(1).strip()
                continue
            
            # 检查缩进级别
            indent_match = re.match(r'^(\s*)\*', line)
            if not indent_match:
                continue
            
            indent = indent_match.group(1)
            level = len(indent) // 2  # 假设每级缩进是2个空格
            
            # 提取链接
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if not link_match:
                continue
            
            text, link = link_match.groups()
            
            # 跳过只有锚点的链接
            if link.startswith('#'):
                continue
            
            # 解析实际文件路径
            file_path, is_external, is_valid = self.resolve_path(link, self.base_dir)
            
            # 添加链接
            link_info = {
                'text': text,
                'link': link,
                'file_path': file_path,
                'exists': is_valid,
                'level': level,
                'section': current_section,
                'is_external': is_external,
                'children': [],  # 用于存储子链接
                'source_file': 'SUMMARY.md'
            }
            
            links.append(link_info)
            
            # 如果链接无效，添加到无效链接列表
            if is_valid is False:  # 注意：is_valid可能为None（在线链接待检查）
                self.invalid_links.append(link_info)
        
        # 构建层级结构
        root_links = []
        level_stack = [None]  # 用于跟踪每个级别的最后一个链接
        
        for link in links:
            level = link['level']
            
            # 调整栈以匹配当前级别
            while len(level_stack) > level + 1:
                level_stack.pop()
            
            # 扩展栈以匹配当前级别
            while len(level_stack) < level + 1:
                level_stack.append(None)
            
            if level == 0:
                # 顶级链接
                root_links.append(link)
            else:
                # 子链接，添加到父链接的children列表中
                parent = level_stack[level - 1]
                if parent:
                    parent['children'].append(link)
            
            # 更新当前级别的最后一个链接
            level_stack[level] = link
        
        self.summary_links = root_links
        return links
    
    def extract_links_from_markdown(self, file_path):
        """
        从Markdown文件中提取链接
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            links: 提取的链接列表
        """
        if not file_path or file_path in self.processed_files:
            return []
            
        if not os.path.exists(file_path) or not file_path.endswith('.md'):
            return []
            
        self.processed_files.add(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return []
        
        # 提取链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        links = []
        current_dir = os.path.dirname(file_path)
        relative_source_path = os.path.relpath(file_path, self.base_dir)
        
        for text, link in matches:
            # 检查是否为图片链接
            if self.is_image_link(link):
                continue
            
            # 解析链接
            resolved_path, is_external, is_valid = self.resolve_path(link, current_dir)
            
            # 添加链接
            link_info = {
                'text': text,
                'link': link,
                'file_path': resolved_path,
                'exists': is_valid,
                'is_external': is_external,
                'source_file': relative_source_path
            }
            
            links.append(link_info)
            
            # 存储到字典中，以文件路径为键
            if file_path not in self.md_links:
                self.md_links[file_path] = []
            self.md_links[file_path].append(link_info)
            
            # 如果链接无效，添加到无效链接列表
            if is_valid is False:  # 注意：is_valid可能为None（在线链接待检查）
                self.invalid_links.append(link_info)
        
        return links
    
    def check_links(self):
        """
        递归检查所有链接
        """
        # 提取SUMMARY中的链接
        self.extract_links_from_summary()
        
        # 递归处理每个链接
        def process_link(link):
            if not link.get('is_external') and link.get('exists') and link.get('file_path') and link.get('file_path').endswith('.md'):
                try:
                    relative_path = os.path.relpath(link['file_path'], self.base_dir)
                    print(f"检查文件: {relative_path}")
                    self.extract_links_from_markdown(link['file_path'])
                except Exception as e:
                    print(f"处理文件 {link.get('file_path')} 时出错: {e}")
            
            # 递归处理子链接
            for child in link.get('children', []):
                process_link(child)
        
        # 处理所有顶级链接
        for link in self.summary_links:
            process_link(link)
        
        # 如果需要验证在线链接，启动多线程进行检查
        if self.verify_online and self.total_online_links > 0:
            self.check_online_links_with_threads()
            
            # 更新链接状态
            self.update_link_statuses()
    
    def check_online_links_with_threads(self):
        """使用多线程检查在线链接"""
        print(f"\n开始使用多线程检查在线链接，共有 {self.total_online_links} 个链接...")
        
        # 创建线程池
        num_threads = min(self.max_threads, self.total_online_links)
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 提交任务
            futures = [executor.submit(self.online_link_worker) for _ in range(num_threads)]
            
            # 等待队列任务完成
            self.online_links_queue.join()
            
            print(f"所有在线链接检查完成，共 {self.total_online_links} 个")
    
    def update_link_statuses(self):
        """根据检查结果更新链接状态"""
        # 更新所有链接的有效性状态
        def update_link(link):
            if link.get('is_external') and link.get('file_path') and link.get('file_path').startswith(('http://', 'https://')):
                with self.online_link_cache_lock:
                    is_valid = self.online_link_cache.get(link['file_path'], False)
                
                link['exists'] = is_valid
                
                # 如果链接无效，添加到无效链接列表
                if not is_valid and link not in self.invalid_links:
                    self.invalid_links.append(link)
            
            # 递归处理子链接
            for child in link.get('children', []):
                update_link(child)
        
        # 处理所有顶级链接
        for link in self.summary_links:
            update_link(link)
        
        # 更新文档链接字典
        for file_path, links in self.md_links.items():
            for link in links:
                if link.get('is_external') and link.get('file_path') and link.get('file_path').startswith(('http://', 'https://')):
                    with self.online_link_cache_lock:
                        is_valid = self.online_link_cache.get(link['file_path'], False)
                    
                    link['exists'] = is_valid
                    
                    # 如果链接无效，添加到无效链接列表
                    if not is_valid and link not in self.invalid_links:
                        self.invalid_links.append(link)
    
    def generate_reports(self, output_path):
        """
        生成两个报告：完整报告和错误链接报告
        
        Args:
            output_path: 完整报告输出文件路径
        """
        # 生成完整报告
        self.generate_full_report(output_path)
        
        # 生成错误链接报告
        error_report_path = output_path.replace('.md', '-error.md')
        if output_path == error_report_path:
            error_report_path = os.path.splitext(output_path)[0] + '-error.md'
        
        self.generate_error_report(error_report_path)
    
    def generate_full_report(self, output_path):
        """
        生成包含所有链接的完整报告
        
        Args:
            output_path: 输出文件路径
        """
        content = "# GitBook链接检查报告（完整版）\n\n"
        
        # 添加章节标题说明
        content += "本报告显示了GitBook文档中的所有链接及其引用的文档。每行的格式为：\n"
        content += "* [文档标题](文档链接) | [引用的文档1](链接1) | [引用的文档2](链接2) | ...\n\n"
        
        # 跟踪已处理的章节
        processed_sections = set()
        
        # 递归生成报告内容
        def generate_link_report(link, indent=""):
            nonlocal content
            
            # 检查是否有新章节
            if 'section' in link and link['section'] and link['section'] not in processed_sections:
                content += f"\n## {link['section']}\n\n"
                processed_sections.add(link['section'])
            
            # 生成主链接
            file_path = link.get('file_path')
            status = "✅" if link.get('exists', False) else "❌"
            
            # 基本链接信息
            content += f"{indent}* [{link['text']}]({link['link']}) {status}"
            
            # 添加该文档中引用的所有非图片链接
            if file_path and file_path in self.md_links and self.md_links[file_path]:
                referenced_links = self.md_links[file_path]
                
                # 遍历文档中引用的所有链接
                for ref_link in referenced_links:
                    # 跳过图片链接
                    if 'link' in ref_link and self.is_image_link(ref_link['link']):
                        continue
                    
                    ref_status = "✅" if ref_link.get('exists', False) else "❌"
                    content += f" | [{ref_link['text']}]({ref_link['link']}) {ref_status}"
            
            content += "\n"
            
            # 递归处理子链接
            for child in link.get('children', []):
                generate_link_report(child, indent + "  ")
        
        # 处理所有顶级链接
        for link in self.summary_links:
            generate_link_report(link)
        
        # 保存报告
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            print(f"完整报告已生成: {output_path}")
        except Exception as e:
            print(f"写入报告时出错: {e}")
    
    def generate_error_report(self, output_path):
        """
        生成仅包含错误链接的报告
        
        Args:
            output_path: 输出文件路径
        """
        if not self.invalid_links:
            print(f"没有发现无效链接，不生成错误报告")
            return
        
        content = "# GitBook链接检查报告（仅错误链接）\n\n"
        content += "本报告仅显示文档中的无效链接。每行的格式为：\n"
        content += "* [文档标题](文档链接) | [无效链接](链接路径) ❌\n\n"
        
        # 按源文件组织无效链接
        links_by_source = defaultdict(list)
        
        for link in self.invalid_links:
            source = link.get('source_file', 'Unknown')
            links_by_source[source].append(link)
        
        # 按源文件添加无效链接
        for source, links in sorted(links_by_source.items()):
            # 添加源文件标题
            content += f"## 来自 {source}\n\n"
            
            # 找到源文件在summary中的对应链接
            summary_link = None
            
            # 查找源文件对应的summary链接
            for link in self.extract_links_from_summary():
                if link.get('file_path') and os.path.relpath(link['file_path'], self.base_dir) == source:
                    summary_link = link
                    break
            
            # 如果是SUMMARY.md本身
            if source == 'SUMMARY.md':
                # 添加每个无效链接
                for link in links:
                    status = "❌"
                    content += f"* [{link['text']}]({link['link']}) {status}\n"
            else:
                # 如果找到了源文件对应的summary链接
                if summary_link:
                    # 显示源文件链接和其中的无效链接
                    source_status = "✅" if summary_link.get('exists', False) else "❌"
                    content += f"* [{summary_link['text']}]({summary_link['link']}) {source_status}"
                    
                    # 添加源文件中的无效链接
                    for link in links:
                        content += f" | [{link['text']}]({link['link']}) ❌"
                    
                    content += "\n\n"
                else:
                    # 没有找到源文件对应的summary链接，只显示无效链接
                    for link in links:
                        content += f"* 来自: {source} - [{link['text']}]({link['link']}) ❌\n"
                    
                    content += "\n"
        
        # 保存报告
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            print(f"错误报告已生成: {output_path}")
        except Exception as e:
            print(f"写入错误报告时出错: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("多线程版GitBook链接检查器")
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
    
    # 获取基础目录
    base_dir = os.path.dirname(os.path.abspath(summary_path))
    if len(sys.argv) > 2:
        base_dir = sys.argv[2]
    else:
        input_base_dir = input(f"请输入文档根目录 [默认: {base_dir}]: ").strip()
        if input_base_dir:
            base_dir = input_base_dir
    
    # 获取输出文件路径
    if len(sys.argv) > 3:
        output_path = sys.argv[3]
    else:
        default_output = os.path.join(base_dir, "link-check-report.md")
        output_path = input(f"请输入输出文件路径 [默认: {default_output}]: ").strip()
        if not output_path:
            output_path = default_output
    
    # 处理目录输出
    if os.path.isdir(output_path):
        output_path = os.path.join(output_path, "link-check-report.md")
    
    # 询问是否验证在线链接
    verify_online = input("是否验证在线链接? (y/n) [默认: n]: ").strip().lower() == 'y'
    
    max_threads = 10
    if verify_online:
        # 获取最大线程数
        try:
            max_threads = int(input(f"请输入最大线程数 [默认: 10]: ").strip() or "10")
            if max_threads < 1:
                max_threads = 10
                print(f"线程数必须大于0，已设置为默认值10")
        except ValueError:
            max_threads = 10
            print(f"输入无效，已设置为默认值10")
        
        print(f"将使用 {max_threads} 个线程并行检查在线链接")
    else:
        print("未验证的在线链接将被标记为错误，并添加到错误报告中")
    
    start_time = time.time()
    
    try:
        # 创建链接检查器并执行检查
        checker = LinkChecker(
            summary_path=summary_path,
            base_dir=base_dir,
            verify_online=verify_online,
            max_threads=max_threads
        )
        
        checker.check_links()
        checker.generate_reports(output_path)
        
        # 统计信息
        total_files = len(checker.processed_files)
        invalid_links = len(checker.invalid_links)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n统计信息:")
        print(f"- 检查的文件数: {total_files}")
        print(f"- 无效链接数: {invalid_links}")
        print(f"- 耗时: {elapsed_time:.2f} 秒")
        
        print("\n检查完成！")
    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()