#!/usr/bin/env python3
"""
文档迁移助手

这个脚本用于辅助 gitbook 文档(dify-docs)迁移至 mintlify（dify-docs-mintlify）
主要功能包括：
1. 图片路径替换：从原始文档查找并替换为在线图片链接
2. 文档引用路径替换：将相对路径替换为绝对路径
3. 支持交互式确认每个修改

使用方法:
python doc_migration_helper.py <目标文件路径>
例如:
python doc_migration_helper.py /Users/allen/Documents/dify-docs-mintlify/zh-hans/guides/workflow/nodes/parameter-extractor.mdx
"""

import os
import re
import sys
import json
from pathlib import Path

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DocMigrationHelper:
    def __init__(self, target_file, source_dir="/Users/allen/Documents/dify-docs", 
                 mintlify_dir="/Users/allen/Documents/dify-docs-mintlify"):
        """
        初始化文档迁移助手
        
        Args:
            target_file: 要处理的目标文件路径
            source_dir: 源文档目录路径
            mintlify_dir: mintlify文档目录路径
        """
        self.target_file = target_file
        self.source_dir = source_dir
        self.mintlify_dir = mintlify_dir
        
        # 获取docs.json内容用于路径映射
        self.docs_config = self._load_docs_config()
        
        # 解析目标文件的相对路径
        self.rel_path = os.path.relpath(target_file, mintlify_dir)
        
        # 推断对应的源文件路径
        self.source_file = self._infer_source_file_path()
        
        # 图片映射缓存
        self.image_url_cache = {}
    
    def _load_docs_config(self):
        """加载docs.json配置文件"""
        try:
            docs_config_path = os.path.join(self.mintlify_dir, "docs.json")
            with open(docs_config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"{Colors.RED}无法加载docs.json: {e}{Colors.ENDC}")
            return {}
    
    def _infer_source_file_path(self):
        """推断源文件路径"""
        # 从mintlify路径推断原始文档中对应的路径
        parts = self.rel_path.split(os.sep)
        
        # 处理语言差异 (zh-hans -> zh_CN)
        if parts[0] == "zh-hans":
            lang_dir = "zh_CN"
        elif parts[0] == "en":
            lang_dir = "en_US"
        else:
            lang_dir = parts[0]
        
        # 实际目标文件名称
        target_basename = os.path.basename(self.target_file)
        if target_basename.endswith(".mdx"):
            target_basename = target_basename[:-4]
        
        # 收集可能的路径
        potential_paths = []
        
        # 处理文件扩展名 (.mdx -> .md)
        rest_path = os.path.join(*parts[1:])
        if rest_path.endswith(".mdx"):
            rest_path = rest_path[:-4] + ".md"
        
        # 1. 直接对应路径
        direct_path = os.path.join(self.source_dir, lang_dir, rest_path)
        potential_paths.append(direct_path)
        
        # 2. 处理节点路径差异 (nodes -> node)
        node_path = direct_path.replace("nodes", "node")
        if node_path != direct_path:
            potential_paths.append(node_path)
        
        # 3. 可能添加了 guides 前缀
        guides_path = os.path.join(self.source_dir, lang_dir, "guides", rest_path)
        if guides_path != direct_path:
            potential_paths.append(guides_path)
            # 也考虑 guides 和 node 的组合
            guides_node_path = guides_path.replace("nodes", "node")
            if guides_node_path != guides_path:
                potential_paths.append(guides_node_path)
        
        # 4. 如果是工作流节点文件，尝试特定目录
        if "workflow" in rest_path and "nodes" in rest_path:
            workflow_node_path = os.path.join(self.source_dir, lang_dir, "guides", "workflow", "node", target_basename + ".md")
            potential_paths.append(workflow_node_path)
        
        # 先检查所有可能的直接匹配路径
        for path in potential_paths:
            if os.path.exists(path):
                print(f"{Colors.GREEN}找到源文件: {path}{Colors.ENDC}")
                return path
        
        # 如果上面的匹配都失败，尝试一些含有繁体/简体变体的目录
        if "workflow" in rest_path and "nodes" in rest_path:
            # 尝试搜索node目录
            node_dir = os.path.join(self.source_dir, lang_dir, "guides", "workflow", "node")
            if os.path.exists(node_dir):
                # 对比文件名，考虑字符替换（如 - 和 _）
                target_name_variants = [
                    target_basename,
                    target_basename.replace("-", "_"),
                    target_basename.replace("_", "-")
                ]
                
                for file in os.listdir(node_dir):
                    if file.endswith(".md"):
                        file_basename = os.path.splitext(file)[0]
                        # 尝试各种变体
                        for variant in target_name_variants:
                            if file_basename == variant:
                                found_path = os.path.join(node_dir, file)
                                print(f"{Colors.GREEN}找到匹配的源文件: {found_path}{Colors.ENDC}")
                                return found_path
        
        # 如果仍然找不到，尝试搜索整个文档目录
        print(f"{Colors.YELLOW}尝试搜索整个文档目录...{Colors.ENDC}")
        found_files = []
        
        for root, _, files in os.walk(os.path.join(self.source_dir, lang_dir)):
            for file in files:
                if file.endswith(".md"):
                    file_basename = os.path.splitext(file)[0]
                    # 比较文件名的各种变体
                    if (file_basename == target_basename or 
                        file_basename == target_basename.replace("-", "_") or 
                        file_basename == target_basename.replace("_", "-")):
                        found_files.append(os.path.join(root, file))
        
        if found_files:
            # 如果找到多个文件，选择路径最相似的
            if len(found_files) > 1:
                best_match = None
                best_score = -1
                current_parts = rest_path.split(os.sep)
                
                for file_path in found_files:
                    rel_path = os.path.relpath(file_path, self.source_dir)
                    rel_parts = rel_path.split(os.sep)
                    # 计算路径部分的重叠数量
                    score = sum(1 for a, b in zip(current_parts, rel_parts) if a == b or a.replace("nodes", "node") == b)
                    if score > best_score:
                        best_score = score
                        best_match = file_path
                
                print(f"{Colors.GREEN}找到最匹配的源文件: {best_match}{Colors.ENDC}")
                return best_match
            else:
                print(f"{Colors.GREEN}找到源文件: {found_files[0]}{Colors.ENDC}")
                return found_files[0]
        
        print(f"{Colors.YELLOW}无法找到对应的源文件{Colors.ENDC}")
        return None
    
    def get_corresponding_image_url(self, local_path):
        """
        根据本地图片路径找到对应的在线URL
        
        Args:
            local_path: 本地图片路径，例如 /zh-cn/user-guide/.gitbook/assets/image (66).png
            
        Returns:
            online_url: 在线图片URL
        """
        # 如果已经缓存过，直接返回
        if local_path in self.image_url_cache:
            return self.image_url_cache[local_path]
        
        # 获取本地图片文件名和图片序号
        local_img_name = os.path.basename(local_path)
        img_number_match = re.search(r'\((\d+)\)', local_img_name)
        img_number = img_number_match.group(1) if img_number_match else None
        
        # 直接尝试根据目标文件路径推断对应的源文件
        if not self.source_file:
            print(f"{Colors.YELLOW}无法找到对应的源文件，尝试查找相关文件...{Colors.ENDC}")
            # 尝试从目标文件名推断源文件名
            target_basename = os.path.basename(self.target_file).replace('.mdx', '')
            
            # 构建可能的源文件路径
            parts = self.rel_path.split(os.sep)
            if parts[0] == "zh-hans":
                lang_dir = "zh_CN"
            elif parts[0] == "en":
                lang_dir = "en_US"
            else:
                lang_dir = parts[0]
            
            # 尝试在guides/workflow/node目录下查找
            possible_source_dir = os.path.join(self.source_dir, lang_dir, "guides", "workflow", "node")
            if os.path.exists(possible_source_dir):
                for file in os.listdir(possible_source_dir):
                    if file.endswith(".md") and file.startswith(target_basename.replace("-", "_")):
                        self.source_file = os.path.join(possible_source_dir, file)
                        print(f"{Colors.GREEN}找到可能的源文件: {self.source_file}{Colors.ENDC}")
                        break
        
        # 如果找不到源文件，尝试在整个文档中搜索图片
        if not self.source_file or not os.path.exists(self.source_file):
            print(f"{Colors.YELLOW}尝试在整个文档中搜索图片...{Colors.ENDC}")
            # 搜索整个源目录中的所有.md文件
            all_md_files = []
            for root, _, files in os.walk(os.path.join(self.source_dir, "zh_CN")):
                for file in files:
                    if file.endswith(".md"):
                        all_md_files.append(os.path.join(root, file))
            
            # 在所有文件中搜索图片URL
            for md_file in all_md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 查找图片序号匹配
                    if img_number:
                        # 查找包含特定序号的图片
                        url_matches = re.findall(r'!\[.*?\]\((https://assets-docs\.dify\.ai/[^)]+)\)', content)
                        for url in url_matches:
                            # 如果URL包含图片名字的关键部分，可能是匹配项
                            if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".gif"):
                                self.image_url_cache[local_path] = url
                                print(f"{Colors.GREEN}在文件 {md_file} 中找到可能匹配的图片URL: {url}{Colors.ENDC}")
                                return url
                except Exception as e:
                    continue
            
            # 如果找不到，返回构造的URL
            # 默认路径构造
            if parts[0] == "zh-hans":
                constructed_url = f"https://assets-docs.dify.ai/dify-enterprise-mintlify/zh_CN/guides/workflow/node/{img_number}.png"
                print(f"{Colors.YELLOW}未找到匹配图片，构造URL: {constructed_url}{Colors.ENDC}")
                return constructed_url
            return None
        
        # 读取源文件内容
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                source_content = f.read()
            
            # 在源文件中查找图片链接
            online_urls = re.findall(r'!\[.*?\]\((https://assets-docs\.dify\.ai/[^)]+)\)', source_content)
            
            # 首先尝试基于图片序号匹配
            if img_number:
                for url in online_urls:
                    # 检查URL是否包含相同序号或相似模式
                    if f"{img_number}.png" in url or f"{img_number})" in url:
                        self.image_url_cache[local_path] = url
                        return url
            
            # 然后尝试文件名匹配
            for url in online_urls:
                url_basename = os.path.basename(url)
                # 精确匹配
                if url_basename == local_img_name:
                    self.image_url_cache[local_path] = url
                    return url
                
                # 尝试模糊匹配（移除数字和特殊字符后比较）
                clean_local = re.sub(r'[^a-zA-Z]', '', local_img_name)
                clean_url = re.sub(r'[^a-zA-Z]', '', url_basename)
                
                if clean_local and clean_url and clean_local == clean_url:
                    self.image_url_cache[local_path] = url
                    return url
            
            # 查找Frame组件中的图片
            frame_urls = re.findall(r'<Frame[^>]*>.*?<img[^>]*src="(https://assets-docs\.dify\.ai/[^"]+)".*?</Frame>', 
                                  source_content, re.DOTALL)
            
            for url in frame_urls:
                url_basename = os.path.basename(url)
                if url_basename == local_img_name or re.sub(r'[^a-zA-Z]', '', url_basename) == re.sub(r'[^a-zA-Z]', '', local_img_name):
                    self.image_url_cache[local_path] = url
                    return url
            
            # 如果在源文件中找不到匹配的URL，尝试在相关文件中查找
            related_files = []
            source_dir = os.path.dirname(self.source_file)
            for file in os.listdir(source_dir):
                if file.endswith(".md") and file != os.path.basename(self.source_file):
                    related_files.append(os.path.join(source_dir, file))
            
            for related_file in related_files:
                try:
                    with open(related_file, 'r', encoding='utf-8') as f:
                        related_content = f.read()
                    
                    related_urls = re.findall(r'!\[.*?\]\((https://assets-docs\.dify\.ai/[^)]+)\)', related_content)
                    for url in related_urls:
                        if img_number and (f"{img_number}.png" in url or f"{img_number})" in url):
                            self.image_url_cache[local_path] = url
                            print(f"{Colors.GREEN}在相关文件 {related_file} 中找到匹配图片: {url}{Colors.ENDC}")
                            return url
                except Exception as e:
                    continue
            
            # 最后尝试根据目录结构构造URL
            relative_source_path = os.path.relpath(self.source_file, self.source_dir)
            dir_parts = os.path.dirname(relative_source_path).split(os.sep)
            
            if img_number and len(dir_parts) >= 2:
                # 使用目录结构构造可能的URL
                if dir_parts[0] == "zh_CN":
                    constructed_url = f"https://assets-docs.dify.ai/dify-enterprise-mintlify/{dir_parts[0]}/{'/'.join(dir_parts[1:])}/{img_number}.png"
                    print(f"{Colors.YELLOW}未找到匹配图片，构造URL: {constructed_url}{Colors.ENDC}")
                    return constructed_url
            
            return None
            
        except Exception as e:
            print(f"{Colors.RED}读取源文件时出错: {e}{Colors.ENDC}")
            return None
    
    def get_absolute_doc_path(self, relative_path):
        """
        将相对文档路径转换为绝对路径
        
        Args:
            relative_path: 相对路径，例如 ./iteration.md 或 http-request.md
            
        Returns:
            absolute_path: 绝对路径，例如 /zh-hans/guides/workflow/nodes/iteration
        """
        # 如果已经是绝对路径，直接返回
        if relative_path.startswith('/'):
            return relative_path
            
        # 如果是外部链接，直接返回
        if relative_path.startswith(('http://', 'https://')):
            return relative_path
        
        # 提取锁点信息（如果有的话）
        fragment = ""
        if '#' in relative_path:
            relative_path, fragment = relative_path.split('#', 1)
            fragment = f'#{fragment}'
            
        # 移除.md或.mdx扩展名
        if relative_path.endswith(('.md', '.mdx')):
            extension = '.md' if relative_path.endswith('.md') else '.mdx'
            relative_path = relative_path[:-len(extension)]
        
        # 获取当前文件的语言前缀（例如 zh-hans）
        lang_prefix = self.rel_path.split(os.sep)[0]
        
        # 处理相对路径
        current_dir = os.path.dirname(self.rel_path)
        current_dir_parts = current_dir.split(os.sep)
        
        # 根据不同类型的相对路径进行处理
        if relative_path.startswith('./'):
            # ./file.md 形式
            relative_path = relative_path[2:]
            full_path = os.path.normpath(os.path.join(current_dir, relative_path))
        elif relative_path.startswith('../'):
            # ../file.md 形式
            full_path = os.path.normpath(os.path.join(current_dir, relative_path))
        else:
            # 简单名称 file.md 形式
            # 首先检查是否在同一目录下
            basename = os.path.basename(relative_path)
            same_level_path = os.path.normpath(os.path.join(current_dir, basename))
            
            # 检查实际文件是否存在
            if os.path.exists(os.path.join(self.mintlify_dir, same_level_path + '.mdx')):
                full_path = same_level_path
            else:
                # 如果是节点文件，通常在 /nodes/ 目录下
                # 查找是否在当前语言的 workflow/nodes 目录下
                if "workflow" in current_dir and ("node" in current_dir or "nodes" in current_dir):
                    # 构造可能的节点路径
                    possible_path = f"{lang_prefix}/guides/workflow/nodes/{basename}"
                    if os.path.exists(os.path.join(self.mintlify_dir, possible_path + '.mdx')):
                        full_path = possible_path
                    else:
                        # 如果不存在，使用默认的同级目录路径
                        full_path = same_level_path
                        print(f"{Colors.YELLOW}警告: 无法找到文件 {possible_path}.mdx，使用默认路径{Colors.ENDC}")
                else:
                    # 尝试搜索整个 mintlify 目录
                    matches = []
                    for root, _, files in os.walk(os.path.join(self.mintlify_dir, lang_prefix)):
                        for file in files:
                            if file == f"{basename}.mdx" or file == f"{basename}.md":
                                rel_file_path = os.path.relpath(os.path.join(root, file), self.mintlify_dir)
                                # 移除扩展名
                                rel_file_path = os.path.splitext(rel_file_path)[0]
                                matches.append(rel_file_path)
                    
                    if matches:
                        # 如果找到多个匹配，选择与当前目录最相似的
                        if len(matches) > 1:
                            best_match = None
                            best_score = -1
                            
                            for match in matches:
                                match_parts = match.split(os.sep)
                                # 计算路径部分的重叠数量
                                score = sum(1 for a, b in zip(current_dir_parts, match_parts[1:]) if a == b)
                                if score > best_score:
                                    best_score = score
                                    best_match = match
                            
                            full_path = best_match
                        else:
                            full_path = matches[0]
                    else:
                        # 如果找不到匹配的文件，使用默认的同级目录路径
                        full_path = same_level_path
                        print(f"{Colors.YELLOW}警告: 无法找到文件 {basename}.mdx，使用默认路径{Colors.ENDC}")
        
        # 确保路径以 / 开头
        if not full_path.startswith('/'):
            full_path = '/' + full_path
            
        # 添加锁点（如果有的话）
        return full_path + fragment
    
    def process_file(self):
        """处理文件，替换图片路径和文档引用路径"""
        try:
            # 读取目标文件内容
            with open(self.target_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 存储修改项
            changes = []
            
            # 1. 查找并替换Markdown格式图片
            # ![alt text](/zh-cn/user-guide/.gitbook/assets/image.png)
            md_img_pattern = re.compile(r'!\[([^\]]*)\]\((/[^)]+)\)')
            for match in md_img_pattern.finditer(content):
                alt_text = match.group(1)
                local_path = match.group(2)
                full_match = match.group(0)
                
                # 获取对应的在线URL
                online_url = self.get_corresponding_image_url(local_path)
                if online_url:
                    new_text = f'![{alt_text}]({online_url})'
                    changes.append((full_match, new_text, '图片链接'))
            
            # 2. 查找并替换Frame组件中的图片
            frame_img_pattern = re.compile(r'(<Frame[^>]*>[\s\S]*?<img[^>]*src=")(/[^"]+)("[^>]*>[\s\S]*?</Frame>)')
            for match in frame_img_pattern.finditer(content):
                prefix = match.group(1)
                local_path = match.group(2)
                suffix = match.group(3)
                full_match = match.group(0)
                
                # 获取对应的在线URL
                online_url = self.get_corresponding_image_url(local_path)
                if online_url:
                    new_text = f'{prefix}{online_url}{suffix}'
                    changes.append((full_match, new_text, 'Frame组件图片'))
            
            # 3. 查找并替换文档引用链接
            # [link text](./path/to/file.md) 或 [link text](path/to/file.md)
            doc_link_pattern = re.compile(r'\[([^\]]+)\]\((\./[^)]+\.md(?:#[^)]*)?|\.\./[^)]+\.md(?:#[^)]*)?|[^)]+\.md(?:#[^)]*)?)\)')
            for match in doc_link_pattern.finditer(content):
                link_text = match.group(1)
                rel_path = match.group(2)
                full_match = match.group(0)
                
                # 检查是否包含锚点
                fragment = ""
                if '#' in rel_path:
                    rel_path, fragment = rel_path.split('#', 1)
                    fragment = f'#{fragment}'
                
                # 获取绝对路径
                abs_path = self.get_absolute_doc_path(rel_path)
                if abs_path:
                    new_text = f'[{link_text}]({abs_path}{fragment})'
                    changes.append((full_match, new_text, '文档链接'))
            
            # 如果没有需要修改的内容
            if not changes:
                print(f"{Colors.GREEN}文件不需要修改{Colors.ENDC}")
                return True
            
            # 显示找到的修改项
            print(f"\n{Colors.BLUE}找到 {len(changes)} 个需要修改的内容:{Colors.ENDC}")
            for i, (old, new, change_type) in enumerate(changes):
                print(f"{Colors.CYAN}修改 {i+1} ({change_type}):{Colors.ENDC}")
                print(f"  - 原始内容: {Colors.YELLOW}{old[:100]}{'...' if len(old) > 100 else ''}{Colors.ENDC}")
                print(f"  - 新内容: {Colors.GREEN}{new[:100]}{'...' if len(new) > 100 else ''}{Colors.ENDC}")
                print()
            
            # 询问是否执行修改
            selected_changes = []
            response = input(f"{Colors.BOLD}是否应用这些修改? (y/n/部分修改输入数字如1,3,5): {Colors.ENDC}")
            
            if response.lower() == 'n':
                print(f"{Colors.BLUE}已取消修改{Colors.ENDC}")
                return False
            elif response.lower() == 'y':
                selected_changes = changes
            else:
                try:
                    # 解析用户选择的修改索引
                    indices = [int(i.strip()) - 1 for i in response.split(',')]
                    selected_changes = [changes[i] for i in indices if 0 <= i < len(changes)]
                    if not selected_changes:
                        print(f"{Colors.YELLOW}未选择任何有效修改，操作取消{Colors.ENDC}")
                        return False
                except:
                    print(f"{Colors.YELLOW}输入格式有误，操作取消{Colors.ENDC}")
                    return False
            
            # 应用修改
            modified_content = content
            for old, new, _ in selected_changes:
                modified_content = modified_content.replace(old, new)
            
            # 写入文件
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"{Colors.GREEN}成功应用 {len(selected_changes)} 个修改到文件{Colors.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}处理文件时出错: {e}{Colors.ENDC}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} <目标文件路径>")
        print(f"例如: {sys.argv[0]} /Users/allen/Documents/dify-docs-mintlify/zh-hans/guides/workflow/nodes/parameter-extractor.mdx")
        return
    
    # 获取目标文件路径
    target_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.isfile(target_file):
        print(f"{Colors.RED}文件不存在: {target_file}{Colors.ENDC}")
        return
    
    # 初始化并处理文件
    helper = DocMigrationHelper(target_file)
    
    print(f"{Colors.HEADER}开始处理文件: {target_file}{Colors.ENDC}")
    print(f"对应的源文件: {helper.source_file or '未找到'}")
    
    helper.process_file()

if __name__ == "__main__":
    main()
