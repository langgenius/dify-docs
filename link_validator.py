#!/usr/bin/env python3
import os
import re
import json
import sys
import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("link_validation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ANSI 颜色代码
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_docs_json(docs_json_path: str) -> dict:
    """加载 docs.json 文件并解析其中的路径信息"""
    try:
        with open(docs_json_path, 'r', encoding='utf-8') as f:
            docs_data = json.load(f)
        return docs_data
    except Exception as e:
        logger.error(f"加载 docs.json 时出错: {e}")
        raise

def extract_valid_paths(docs_data: dict) -> Set[str]:
    """从 docs.json 中提取所有有效的文档路径"""
    valid_paths = set()
    
    # 递归函数用于处理嵌套结构
    def extract_paths_from_object(obj):
        if isinstance(obj, dict):
            # 检查是否有页面路径
            if "pages" in obj:
                for page in obj["pages"]:
                    if isinstance(page, str) and not page.startswith(("http://", "https://")):
                        valid_paths.add(page)
                    elif isinstance(page, dict):
                        extract_paths_from_object(page)
            # 处理其他可能的字典键
            for key, value in obj.items():
                if key != "pages":  # 避免重复处理
                    extract_paths_from_object(value)
        elif isinstance(obj, list):
            # 处理列表中的每个元素
            for item in obj:
                extract_paths_from_object(item)
    
    # 开始提取
    extract_paths_from_object(docs_data)
    return valid_paths

def find_md_files(path: str) -> List[Path]:
    """查找指定路径下的所有 .md 和 .mdx 文件"""
    path_obj = Path(path)
    if path_obj.is_file() and (path_obj.suffix in ['.md', '.mdx']):
        return [path_obj]
    
    md_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                md_files.append(Path(os.path.join(root, file)))
    
    return md_files

def detect_file_language(file_path: Path) -> str:
    """根据文件路径检测语言"""
    path_str = str(file_path)
    if "/en/" in path_str:
        return "en"
    elif "/zh-hans/" in path_str:
        return "zh-hans"
    elif "/ja-jp/" in path_str:
        return "ja-jp"
    else:
        # 默认为英文
        return "en"

def check_link_exists(link: str, base_path: str, valid_paths: Set[str]) -> bool:
    """检查链接是否存在"""
    # 跳过锚点链接、邮件链接和外部链接
    if link.startswith(('#', 'mailto:', 'http://', 'https://')):
        return True
    
    # 处理以 / 开头的路径 (绝对路径)
    if link.startswith('/'):
        # 移除开头的 /
        clean_link = link[1:]
        
        # 检查在 valid_paths 中是否存在
        if clean_link in valid_paths:
            return True
        
        # 移除扩展名后检查
        link_without_ext, _ = os.path.splitext(clean_link)
        if link_without_ext in valid_paths:
            return True
        
        # 检查实际文件是否存在
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), clean_link)
        if os.path.exists(full_path):
            return True
        
        # 尝试添加 .mdx 或 .md 扩展名
        if os.path.exists(full_path + '.mdx') or os.path.exists(full_path + '.md'):
            return True
        
        return False
    
    # 处理相对路径
    base_dir = os.path.dirname(base_path)
    target_path = os.path.normpath(os.path.join(base_dir, link))
    
    # 检查文件是否存在
    if os.path.exists(target_path):
        return True
    
    # 移除扩展名
    target_without_ext, ext = os.path.splitext(target_path)
    
    # 尝试添加 .mdx 或 .md 扩展名
    if os.path.exists(target_without_ext + '.mdx') or os.path.exists(target_without_ext + '.md'):
        return True
    
    # 检查是否是目录
    if os.path.isdir(target_without_ext):
        # 检查目录中是否有 index.mdx 或 README.mdx
        if os.path.exists(os.path.join(target_without_ext, 'index.mdx')) or \
           os.path.exists(os.path.join(target_without_ext, 'index.md')) or \
           os.path.exists(os.path.join(target_without_ext, 'README.mdx')) or \
           os.path.exists(os.path.join(target_without_ext, 'README.md')):
            return True
    
    # 如果以上都不匹配，则检查在 valid_paths 中是否有相似路径
    rel_path = os.path.relpath(target_path, os.path.dirname(os.path.abspath(__file__)))
    rel_path = rel_path.replace('\\', '/')  # 统一路径分隔符
    
    if rel_path in valid_paths:
        return True
    
    # 移除扩展名再检查
    rel_path_without_ext, _ = os.path.splitext(rel_path)
    if rel_path_without_ext in valid_paths:
        return True
    
    return False

def find_line_number(content: str, link_text: str, link_url: str) -> int:
    """查找链接在文件中的行号"""
    lines = content.split('\n')
    # 先尝试精确匹配
    full_link = f"[{link_text}]({link_url})"
    
    for i, line in enumerate(lines, 1):
        if full_link in line:
            return i
    
    # 如果精确匹配失败，尝试使用正则表达式进行模糊匹配
    # 这可以处理链接包含特殊字符或包含属性的情况
    try:
        escaped_text = re.escape(link_text)
        escaped_url = re.escape(link_url)
        pattern = re.compile(f"\\[{escaped_text}\\]\\({escaped_url}")
        
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                return i
    except Exception:
        pass  # 如果正则表达式出错，忽略并继续
    
    # 如果以上方法都失败，尝试只匹配 URL
    try:
        for i, line in enumerate(lines, 1):
            if f"]({link_url})" in line or f"]({link_url} " in line:
                return i
    except Exception:
        pass
    
    return 0  # 如果找不到，返回 0

def validate_links_in_file(file_path: Path, valid_paths: Set[str], base_dir: str) -> List[Dict]:
    """验证文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"读取文件 {file_path} 时出错: {e}")
        return []
    
    # 提取当前文件的相对路径（相对于基础目录）
    relative_file_path = os.path.relpath(file_path, base_dir)
    
    # 找出所有 Markdown 链接
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)(\s+"[^"]*")?\)')
    matches = link_pattern.findall(content)
    
    invalid_links = []
    for match in matches:
        link_text, link_url, _ = match
        
        # 跳过锚点链接和邮件链接
        if link_url.startswith(('#', 'mailto:')):
            continue
        
        # 跳过外部链接
        if link_url.startswith(('http://', 'https://')):
            continue
        
        # 检查链接是否有效
        if not check_link_exists(link_url, str(file_path), valid_paths):
            line_number = find_line_number(content, link_text, link_url)
            invalid_links.append({
                "file": relative_file_path,
                "link_text": link_text,
                "link_url": link_url,
                "line_number": line_number
            })
    
    return invalid_links

def generate_report(all_invalid_links: List[Dict], total_files_processed: int, base_dir: str) -> str:
    """生成报告并保存到文件"""
    report_path = os.path.join(base_dir, "invalid_links_report.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 无效链接报告\n\n")
        f.write("生成时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        f.write("## 汇总\n\n")
        f.write(f"* 处理文件数: {total_files_processed}\n")
        f.write(f"* 发现无效链接数: {len(all_invalid_links)}\n\n")
        
        # 按文件分组
        files_groups = {}
        for link in all_invalid_links:
            if link['file'] not in files_groups:
                files_groups[link['file']] = []
            files_groups[link['file']].append(link)
        
        f.write("## 详细报告\n\n")
        
        for file, links in files_groups.items():
            f.write(f"### 文件: {file}\n\n")
            f.write("| 行号 | 链接文本 | 链接 URL |\n")
            f.write("|------|----------|----------|\n")
            for link in sorted(links, key=lambda x: x['line_number']):
                # 处理可能包含特殊字符的文本
                link_text = link['link_text'].replace('|', '\\|')
                link_url = link['link_url'].replace('|', '\\|')
                line_num = link['line_number'] if link['line_number'] > 0 else "未知"
                f.write(f"| {line_num} | {link_text} | {link_url} |\n")
            f.write("\n")
    
    return report_path

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_json_path = os.path.join(base_dir, 'docs.json')
    
    # 显示脚本标题
    print(f"\n{Colors.CYAN}{Colors.BOLD}===== Dify 文档链接验证工具 V2 ====={Colors.RESET}\n")
    
    # 加载 docs.json
    try:
        print(f"{Colors.BLUE}正在加载 docs.json...{Colors.RESET}")
        docs_data = load_docs_json(docs_json_path)
        valid_paths = extract_valid_paths(docs_data)
        print(f"{Colors.GREEN}从 docs.json 中提取了 {Colors.YELLOW}{len(valid_paths)}{Colors.GREEN} 个有效路径{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}加载 docs.json 时出错: {e}{Colors.RESET}")
        sys.exit(1)
    
    # 获取用户输入的路径
    path_input = input(f"{Colors.CYAN}请输入要验证的文件或目录路径（相对于当前目录）: {Colors.RESET}")
    target_path = os.path.join(base_dir, path_input)
    
    if not os.path.exists(target_path):
        print(f"{Colors.RED}路径不存在: {target_path}{Colors.RESET}")
        sys.exit(1)
    
    # 查找 Markdown 文件
    md_files = find_md_files(target_path)
    print(f"{Colors.GREEN}找到 {Colors.YELLOW}{len(md_files)}{Colors.GREEN} 个 Markdown 文件{Colors.RESET}")
    
    # 验证每个文件中的链接
    all_invalid_links = []
    total_files_processed = 0
    
    for file_path in md_files:
        total_files_processed += 1
        print(f"{Colors.BLUE}正在验证文件 ({total_files_processed}/{len(md_files)}): {Colors.YELLOW}{file_path}{Colors.RESET}")
        
        invalid_links = validate_links_in_file(file_path, valid_paths, base_dir)
        if invalid_links:
            print(f"{Colors.RED}发现 {len(invalid_links)} 个无效链接{Colors.RESET}")
            for link in invalid_links:
                line_num = link['line_number'] if link['line_number'] > 0 else "未知行"
                print(f"  {Colors.YELLOW}{line_num}: {Colors.RED}[{link['link_text']}]({link['link_url']}){Colors.RESET}")
            all_invalid_links.extend(invalid_links)
        else:
            print(f"{Colors.GREEN}所有链接验证通过{Colors.RESET}")
    
    # 显示总结
    print(f"\n{Colors.CYAN}{Colors.BOLD}===== 验证完成 ====={Colors.RESET}")
    print(f"{Colors.GREEN}共处理了 {Colors.YELLOW}{total_files_processed}{Colors.GREEN} 个文件{Colors.RESET}")
    
    if all_invalid_links:
        print(f"{Colors.RED}发现 {Colors.YELLOW}{len(all_invalid_links)}{Colors.RED} 个无效链接{Colors.RESET}")
        
        # 询问是否保存报告
        save_report = input(f"{Colors.CYAN}是否保存无效链接报告到文件? (y/n): {Colors.RESET}").lower() == 'y'
        if save_report:
            report_path = generate_report(all_invalid_links, total_files_processed, base_dir)
            print(f"{Colors.GREEN}报告已保存到: {Colors.YELLOW}{report_path}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}恭喜！所有链接验证通过{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}用户中断，程序退出{Colors.RESET}")
        sys.exit(0)
