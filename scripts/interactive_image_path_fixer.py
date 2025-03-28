#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交互式图片路径修复工具

该脚本可以交互式地查找并修复 .mdx 文件中的相对图片路径，
将它们替换为原始 dify-docs 仓库中对应的在线 URL。

每次找到一个问题时，会显示详细信息并等待用户确认后再进行修改。

目录映射关系:
    dify-docs-mintlify -> dify-docs
    zh-hans -> zh_CN
    en -> en
    ja-jp -> jp
"""

import os
import re
import sys
from pathlib import Path
import argparse
from colorama import init, Fore, Style
import difflib

# 初始化 colorama
init(autoreset=True)

# 查找图片的正则表达式
MD_IMAGE_RE = re.compile(r'!\[(.*?)\]\(((?!https?://|/).+?\.(png|jpe?g|gif|svg))\)')
HTML_IMAGE_RE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+\.(png|jpe?g|gif|svg))["\'][^>]*>')
FRAME_IMAGE_RE = re.compile(r'<img\s+[^>]*src=["\'](/[^"\']+\.(png|jpe?g|gif|svg))["\'][^>]*>')

# 查找在线URL的正则表达式
MD_ONLINE_URL_RE = re.compile(r'!\[[^\]]*\]\((https://[^\s\)]+\.(png|jpe?g|gif|svg|jpeg))\)')
HTML_ONLINE_URL_RE = re.compile(r'<img[^>]*src=["\'](https://[^\s"\']+\.(png|jpe?g|gif|svg|jpeg))["\'][^>]*>')

# 语言目录映射
LANGUAGE_MAPPING = {
    'zh-hans': 'zh_CN',
    'en': 'en',
    'ja-jp': 'jp'
}

REVERSE_LANGUAGE_MAPPING = {v: k for k, v in LANGUAGE_MAPPING.items()}

def find_relative_images(file_path):
    """
    在 .mdx 文件中查找所有相对路径的图片。
    返回一个包含 (匹配文本, 图片路径, 行号, 位置) 的列表
    """
    relative_images = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查 Markdown 图片语法
    for match in MD_IMAGE_RE.finditer(content):
        image_path = match.group(2)
        if not image_path.startswith(('http://', 'https://', '/')):
            # 记录行号和位置
            line_no = content[:match.start()].count('\n') + 1
            position = match.start()
            relative_images.append((match.group(0), image_path, line_no, position))
    
    # 检查 HTML img 标签
    for match in HTML_IMAGE_RE.finditer(content):
        image_path = match.group(1)
        if not image_path.startswith(('http://', 'https://', '/')):
            line_no = content[:match.start()].count('\n') + 1
            position = match.start()
            relative_images.append((match.group(0), image_path, line_no, position))
    
    # 检查 Frame 组件中的相对路径
    for match in FRAME_IMAGE_RE.finditer(content):
        image_path = match.group(1)
        # 如 /ja-jp/img/... 或 /en-us/img/... 或 /zh-cn/... 这样的路径
        if image_path.startswith('/'):
            line_no = content[:match.start()].count('\n') + 1
            position = match.start()
            relative_images.append((match.group(0), image_path, line_no, position))
    
    # 按位置排序，确保按照文档中的顺序处理
    relative_images.sort(key=lambda x: x[3])
    
    # 返回时去掉位置信息
    return [(match, path, line) for match, path, line, _ in relative_images]

def parse_md_file_for_urls(file_path):
    """仔细解析Markdown文件以提取在线URL和它们的位置"""
    urls = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 查找图片URLs
        for i, line in enumerate(lines):
            # 查找Markdown风格的图片
            for match in MD_ONLINE_URL_RE.finditer(line):
                url = match.group(1)
                position = sum(len(l) + 1 for l in lines[:i]) + match.start()
                urls.append((url, i+1, position))
            
            # 查找HTML风格的图片
            for match in HTML_ONLINE_URL_RE.finditer(line):
                url = match.group(1)
                position = sum(len(l) + 1 for l in lines[:i]) + match.start()
                urls.append((url, i+1, position))
        
        # 按文档中的位置排序
        urls.sort(key=lambda x: x[2])
        
        return urls
    except Exception as e:
        print(f"{Fore.RED}读取文件 {file_path} 时出错: {e}")
        return []

def find_corresponding_file(mintlify_file, mintlify_base, dify_base):
    """查找 dify-docs 仓库中对应的文件"""
    
    # 获取从 mintlify_base 到文件的相对路径
    rel_path = os.path.relpath(mintlify_file, mintlify_base)
    
    # 提取语言文件夹（路径的第一个组件）
    parts = rel_path.split(os.sep)
    if len(parts) > 0 and parts[0] in LANGUAGE_MAPPING:
        lang_folder = parts[0]
        mapped_lang = LANGUAGE_MAPPING[lang_folder]
        parts[0] = mapped_lang
        
        # 用映射后的语言重建路径
        rel_path = os.path.join(*parts)
    
    # 将扩展名从 .mdx 改为 .md
    if rel_path.endswith('.mdx'):
        rel_path = rel_path[:-4] + '.md'
    
    # 构建在 dify-docs 中的完整路径
    dify_file = os.path.join(dify_base, rel_path)
    
    return dify_file if os.path.exists(dify_file) else None

def extract_img_basename(path):
    """从图片路径中提取基本文件名"""
    # 处理常规和语言前缀路径
    # 如 /ja-jp/img/jp-env-variable.png 或 /en-us/img/image.png
    if path.startswith('/'):
        parts = path.split('/')
        if len(parts) > 1:
            return parts[-1]  # 获取最后一部分（文件名）
    return os.path.basename(path)

def get_file_extension(path):
    """获取文件扩展名"""
    basename = extract_img_basename(path)
    if '.' in basename:
        return basename.split('.')[-1].lower()
    return None

def debug_print_file_comparison(mintlify_file, dify_file):
    """打印两个文件的内容对比，用于调试"""
    print(f"\n{Fore.CYAN}======= 文件内容对比 =======")
    
    # 读取mintlify文件内容
    try:
        with open(mintlify_file, 'r', encoding='utf-8') as f:
            mintlify_content = f.read()
            print(f"\n{Fore.GREEN}Mintlify文件({mintlify_file}):")
            print(mintlify_content[:500] + "..." if len(mintlify_content) > 500 else mintlify_content)
    except Exception as e:
        print(f"{Fore.RED}读取 {mintlify_file} 错误: {e}")
    
    # 读取dify文件内容
    try:
        with open(dify_file, 'r', encoding='utf-8') as f:
            dify_content = f.read()
            print(f"\n{Fore.YELLOW}Dify文件({dify_file}):")
            print(dify_content[:500] + "..." if len(dify_content) > 500 else dify_content)
    except Exception as e:
        print(f"{Fore.RED}读取 {dify_file} 错误: {e}")
    
    # 提取并比较图片URLs
    mintlify_images = find_relative_images(mintlify_file)
    dify_urls = parse_md_file_for_urls(dify_file)
    
    print(f"\n{Fore.CYAN}Mintlify图片({len(mintlify_images)}):")
    for i, (_, img_path, _) in enumerate(mintlify_images):
        print(f"{i+1}. {img_path}")
    
    print(f"\n{Fore.CYAN}Dify URLs({len(dify_urls)}):")
    for i, (url, _, _) in enumerate(dify_urls):
        print(f"{i+1}. {url}")

def match_images_precisely(mintlify_images, dify_file):
    """精确匹配图片，按照文档位置和上下文"""
    results = []
    dify_urls = parse_md_file_for_urls(dify_file)
    
    # 按照位置对应匹配图片和URL
    for i, (match_text, img_path, line_no) in enumerate(mintlify_images):
        img_ext = get_file_extension(img_path)
        
        # 检查是否有足够的URLs
        if i < len(dify_urls):
            # 检查扩展名是否匹配
            url_ext = get_file_extension(dify_urls[i][0])
            if img_ext and url_ext and img_ext.lower() == url_ext.lower():
                results.append((match_text, img_path, line_no, dify_urls[i][0], dify_file))
            else:
                # 尝试在剩余URL中找到匹配的扩展名
                found_match = False
                for j, (url, _, _) in enumerate(dify_urls):
                    if j != i:  # 避免重复使用当前位置
                        j_ext = get_file_extension(url)
                        if img_ext and j_ext and img_ext.lower() == j_ext.lower():
                            results.append((match_text, img_path, line_no, url, dify_file))
                            found_match = True
                            break
                
                if not found_match:
                    results.append((match_text, img_path, line_no, None, None))
        else:
            results.append((match_text, img_path, line_no, None, None))
    
    return results

def get_all_content_after_image(content, image_path):
    """获取图片后的所有文本内容"""
    # 查找相对路径的位置
    index = content.find(image_path)
    if index == -1:
        return ""
    
    # 返回图片后的所有内容
    return content[index + len(image_path):]

def match_images_by_name_and_context(mintlify_file, dify_file):
    """通过图片名称和上下文匹配图片"""
    try:
        # 读取文件内容
        with open(mintlify_file, 'r', encoding='utf-8') as f:
            mintlify_content = f.read()
        
        with open(dify_file, 'r', encoding='utf-8') as f:
            dify_content = f.read()
        
        # 获取mintlify文件中的相对图片
        mintlify_images = find_relative_images(mintlify_file)
        
        # 提取dify文件中的在线URLs
        dify_urls = parse_md_file_for_urls(dify_file)
        
        # 按顺序匹配每个图片
        results = []
        for match_text, img_path, line_no in mintlify_images:
            # 提取图片名称和后缀
            img_base = extract_img_basename(img_path)
            img_ext = get_file_extension(img_path)
            
            # 获取图片在mintlify文件中的实际位置
            img_index = mintlify_content.find(img_path)
            if img_index == -1:
                img_index = mintlify_content.find(match_text)
            
            # 获取图片后的文本上下文（用于更精确的匹配）
            after_text = mintlify_content[img_index + len(match_text):img_index + len(match_text) + 200]
            after_text = re.sub(r'[\n\r\s]+', ' ', after_text).strip()
            
            # 尝试通过图片在文档中的位置和顺序匹配
            # 首先，确定当前图片是这种类型的第几个图片
            same_ext_images = [i for i, (_, p, _) in enumerate(mintlify_images) 
                              if get_file_extension(p) == img_ext]
            current_index = same_ext_images.index(mintlify_images.index((match_text, img_path, line_no)))
            
            # 获取对应索引的相同类型URL
            same_ext_urls = [(i, u) for i, (u, _, _) in enumerate(dify_urls) 
                            if get_file_extension(u) == img_ext]
            
            if current_index < len(same_ext_urls):
                # 按顺序匹配
                url_index, url = same_ext_urls[current_index]
                results.append((match_text, img_path, line_no, url, dify_file))
            else:
                # 如果顺序匹配失败，尝试上下文相似度匹配
                best_match = None
                best_score = 0
                
                for _, (url, url_line, _) in enumerate(dify_urls):
                    # 检查扩展名是否匹配
                    url_ext = get_file_extension(url)
                    if img_ext != url_ext:
                        continue
                    
                    # 获取URL在dify文件中的实际位置
                    url_index = dify_content.find(url)
                    
                    # 获取URL后的文本上下文
                    url_after_text = dify_content[url_index + len(url):url_index + len(url) + 200]
                    url_after_text = re.sub(r'[\n\r\s]+', ' ', url_after_text).strip()
                    
                    # 计算上下文相似度
                    matcher = difflib.SequenceMatcher(None, after_text, url_after_text)
                    score = matcher.ratio()
                    
                    if score > best_score:
                        best_score = score
                        best_match = url
                
                if best_match:
                    results.append((match_text, img_path, line_no, best_match, dify_file))
                else:
                    results.append((match_text, img_path, line_no, None, None))
        
        return results
    
    except Exception as e:
        print(f"{Fore.RED}匹配图片时出错: {e}")
        return []

def find_matching_image_url(mintlify_file, dify_file, img_path, order_index=0):
    """查找匹配的图片URL，考虑多种策略"""
    # 策略1: 按顺序匹配
    # 策略2: 按扩展名匹配
    # 策略3: 按上下文匹配
    
    try:
        # 获取图片扩展名
        img_ext = get_file_extension(img_path)
        if not img_ext:
            return None
        
        # 解析dify文件中的URLs
        urls = parse_md_file_for_urls(dify_file)
        
        # 按顺序和扩展名匹配
        # 找出所有扩展名匹配的URLs
        matching_urls = []
        for url, _, _ in urls:
            url_ext = get_file_extension(url)
            if url_ext == img_ext:
                matching_urls.append(url)
        
        # 如果没有匹配的URL，返回None
        if not matching_urls:
            return None
        
        # 如果图片序号在有效范围内，按序号匹配
        if order_index < len(matching_urls):
            return matching_urls[order_index]
        
        # 否则返回第一个匹配的URL
        return matching_urls[0]
    
    except Exception as e:
        print(f"{Fore.RED}查找匹配URL时出错: {e}")
        return None

def validate_content_alignment(mintlify_file, dify_file, img_path, url, check_text_length=200):
    """验证内容对齐情况，确保图片周围的内容相似"""
    try:
        with open(mintlify_file, 'r', encoding='utf-8') as f:
            mintlify_content = f.read()
        
        with open(dify_file, 'r', encoding='utf-8') as f:
            dify_content = f.read()
        
        # 在原始文件中找到图片位置
        img_index = mintlify_content.find(img_path)
        if img_index == -1:
            return False
        
        # 在目标文件中找到URL位置
        url_index = dify_content.find(url)
        if url_index == -1:
            return False
        
        # 获取图片后的文本
        img_after = mintlify_content[img_index + len(img_path):img_index + len(img_path) + check_text_length]
        img_after = re.sub(r'[\n\r\s]+', ' ', img_after).strip()
        
        # 获取URL后的文本
        url_after = dify_content[url_index + len(url):url_index + len(url) + check_text_length]
        url_after = re.sub(r'[\n\r\s]+', ' ', url_after).strip()
        
        # 计算相似度
        matcher = difflib.SequenceMatcher(None, img_after, url_after)
        ratio = matcher.ratio()
        
        # 返回相似度是否超过阈值
        return ratio > 0.5
    
    except Exception as e:
        print(f"{Fore.RED}验证内容对齐时出错: {e}")
        return False

def replace_image_in_file(file_path, match_text, online_url):
    """在文件中将单个相对图片路径替换为在线 URL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        if '<img' in match_text and 'src=' in match_text:
            # 对于 HTML img 标签
            new_text = re.sub(r'src=["\'][^"\']+["\']', f'src="{online_url}"', match_text)
            new_content = new_content.replace(match_text, new_text)
        elif match_text.startswith('!['):
            # 对于 Markdown 图片语法
            alt_text = re.search(r'!\[(.*?)\]', match_text).group(1)
            new_text = f'![{alt_text}]({online_url})'
            new_content = new_content.replace(match_text, new_text)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"{Fore.RED}处理文件 {file_path} 时出错: {e}")
        return False

def get_user_choice(prompt):
    """获取用户选择"""
    valid_choices = {
        'y': f"{Fore.GREEN}(y)是",
        'n': f"{Fore.RED}(n)否",
        's': f"{Fore.YELLOW}(s)跳过文件",
        'd': f"{Fore.BLUE}(d)显示文件内容进行对比",
        'q': f"{Fore.MAGENTA}(q)退出程序"
    }
    
    options = " / ".join(valid_choices.values())
    full_prompt = f"{prompt} {options}: "
    
    while True:
        choice = input(full_prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"{Fore.RED}无效选择，请重试。")

def interactive_fix(file_path, mintlify_base, dify_base):
    """交互式修复文件中的相对图片路径"""
    # 查找对应的 dify 文件
    dify_file = find_corresponding_file(file_path, mintlify_base, dify_base)
    if not dify_file or not os.path.exists(dify_file):
        print(f"{Fore.YELLOW}警告: 未找到对应的 dify 文件: {dify_file}")
        return 0, 0
    
    # 获取mintlify中的所有相对图片
    mintlify_images = find_relative_images(file_path)
    if not mintlify_images:
        print(f"{Fore.YELLOW}没有找到需要处理的相对路径图片")
        return 0, 0
    
    print(f"{Fore.CYAN}找到 {len(mintlify_images)} 个相对路径图片")
    print(f"{Fore.CYAN}对应的 dify 文件: {dify_file}")
    
    # 解析dify文件中的URLs
    dify_urls = parse_md_file_for_urls(dify_file)
    print(f"{Fore.CYAN}在dify文件中找到 {len(dify_urls)} 个在线URL")
    
    fixed = 0
    skipped = 0
    
    for i, (match_text, img_path, line_no) in enumerate(mintlify_images):
        # 获取图片扩展名
        img_ext = get_file_extension(img_path)
        
        # 找出当前类型的第几个图片
        same_ext_count = sum(1 for _, p, _ in mintlify_images[:i] if get_file_extension(p) == img_ext)
        
        # 尝试查找匹配的URL
        online_url = find_matching_image_url(file_path, dify_file, img_path, same_ext_count)
        
        if online_url:
            print("\n" + "="*80)
            print(f"{Fore.GREEN}文件: {file_path}")
            print(f"{Fore.YELLOW}发现相对图片路径: {img_path}")
            print(f"{Fore.RED}原始文本: {match_text}")
            print(f"{Fore.BLUE}找到在线 URL: {online_url}")
            print(f"{Fore.CYAN}来源文件: {dify_file}")
            print(f"{Fore.CYAN}图片序号: 第 {i+1} 个 (总共 {len(mintlify_images)} 个)")
            print(f"{Fore.CYAN}同类型图片序号: 第 {same_ext_count+1} 个 {img_ext} 图片")
            
            # 验证内容对齐情况
            is_aligned = validate_content_alignment(file_path, dify_file, img_path, online_url)
            if not is_aligned:
                print(f"{Fore.YELLOW}警告: 图片周围的内容可能不一致，请仔细检查")
            
            choice = get_user_choice("是否替换?")
            
            if choice == 'y':
                success = replace_image_in_file(file_path, match_text, online_url)
                if success:
                    print(f"{Fore.GREEN}成功将相对路径替换为在线 URL")
                    fixed += 1
                else:
                    print(f"{Fore.RED}替换相对路径失败")
                    skipped += 1
            elif choice == 'n':
                print(f"{Fore.YELLOW}跳过此替换")
                skipped += 1
            elif choice == 's':
                print(f"{Fore.YELLOW}跳过此文件")
                skipped += len(mintlify_images) - i
                break
            elif choice == 'd':
                print(f"{Fore.BLUE}显示文件内容进行对比")
                debug_print_file_comparison(file_path, dify_file)
                # 重新询问是否替换
                choice = get_user_choice("是否替换?")
                if choice == 'y':
                    success = replace_image_in_file(file_path, match_text, online_url)
                    if success:
                        print(f"{Fore.GREEN}成功将相对路径替换为在线 URL")
                        fixed += 1
                    else:
                        print(f"{Fore.RED}替换相对路径失败")
                        skipped += 1
                elif choice == 'n':
                    print(f"{Fore.YELLOW}跳过此替换")
                    skipped += 1
                elif choice == 's':
                    print(f"{Fore.YELLOW}跳过此文件")
                    skipped += len(mintlify_images) - i
                    break
                elif choice == 'q':
                    print(f"{Fore.MAGENTA}正在退出...")
                    return fixed, skipped
            elif choice == 'q':
                print(f"{Fore.MAGENTA}正在退出...")
                return fixed, skipped
        else:
            print("\n" + "="*80)
            print(f"{Fore.GREEN}文件: {file_path}")
            print(f"{Fore.YELLOW}发现相对图片路径: {img_path}")
            print(f"{Fore.RED}原始文本: {match_text}")
            print(f"{Fore.RED}未找到匹配的在线 URL (确保文件格式相同)")
            print(f"{Fore.CYAN}对应的 dify 文件: {dify_file}")
            print(f"{Fore.CYAN}图片序号: 第 {i+1} 个 (总共 {len(mintlify_images)} 个)")
            
            choice = get_user_choice("是否跳过?")
            
            if choice == 'y':
                skipped += 1
            elif choice == 's':
                print(f"{Fore.YELLOW}跳过此文件")
                skipped += len(mintlify_images) - i
                break
            elif choice == 'd':
                print(f"{Fore.BLUE}显示文件内容进行对比")
                debug_print_file_comparison(file_path, dify_file)
                # 重新询问是否跳过
                choice = get_user_choice("是否跳过?")
                if choice == 'y':
                    skipped += 1
                elif choice == 's':
                    print(f"{Fore.YELLOW}跳过此文件")
                    skipped += len(mintlify_images) - i
                    break
                elif choice == 'q':
                    print(f"{Fore.MAGENTA}正在退出...")
                    return fixed, skipped
            elif choice == 'q':
                print(f"{Fore.MAGENTA}正在退出...")
                return fixed, skipped
    
    return fixed, skipped

def main():
    parser = argparse.ArgumentParser(description='交互式修复 MDX 文件中的相对图片路径')
    parser.add_argument('--mintlify-dir', default='/Users/allen/Documents/dify-docs-mintlify', 
                        help='dify-docs-mintlify 目录路径')
    parser.add_argument('--dify-dir', default='/Users/allen/Documents/dify-docs', 
                        help='dify-docs 目录路径')
    parser.add_argument('--file', help='处理特定文件')
    parser.add_argument('--debug', action='store_true', help='开启调试模式')
    args = parser.parse_args()
    
    mintlify_base = args.mintlify_dir
    dify_base = args.dify_dir
    
    # 验证目录
    if not os.path.isdir(mintlify_base):
        print(f"{Fore.RED}错误: {mintlify_base} 不是有效目录")
        return 1
    if not os.path.isdir(dify_base):
        print(f"{Fore.RED}错误: {dify_base} 不是有效目录")
        return 1
    
    total_fixed = 0
    total_skipped = 0
    
    # 如果提供了特定文件则处理该文件
    if args.file:
        if not os.path.isfile(args.file):
            print(f"{Fore.RED}错误: {args.file} 不是有效文件")
            return 1
        
        print(f"{Fore.CYAN}正在处理 {args.file}...")
        
        # 如果开启调试模式，打印更多信息
        if args.debug:
            dify_file = find_corresponding_file(args.file, mintlify_base, dify_base)
            if dify_file:
                debug_print_file_comparison(args.file, dify_file)
        
        fixed, skipped = interactive_fix(args.file, mintlify_base, dify_base)
        total_fixed += fixed
        total_skipped += skipped
    
    # 处理所有 MDX 文件
    else:
        for lang in LANGUAGE_MAPPING.keys():
            lang_dir = os.path.join(mintlify_base, lang)
            if not os.path.isdir(lang_dir):
                print(f"{Fore.YELLOW}警告: 未找到语言目录 {lang_dir}")
                continue
            
            print(f"{Fore.CYAN}正在扫描 {lang_dir}...")
            for root, _, files in os.walk(lang_dir):
                for file in files:
                    if file.endswith('.mdx'):
                        file_path = os.path.join(root, file)
                        fixed, skipped = interactive_fix(file_path, mintlify_base, dify_base)
                        total_fixed += fixed
                        total_skipped += skipped
    
    # 总结
    print("\n" + "="*80)
    print(f"{Fore.GREEN}总结:")
    print(f"{Fore.GREEN}成功修复: {total_fixed} 个")
    print(f"{Fore.YELLOW}跳过: {total_skipped} 个")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
