#!/usr/bin/env python3
"""
GitBook to Mintlify格式转换脚本

将GitBook风格的Markdown组件转换为Mintlify MDX格式。
例如将 {% hint style="warning" %} xxx {% endhint %} 
转换为 <Warning>xxx</Warning>
"""

import re
import os

# 定义转换映射表
STYLE_MAPPING = {
    "info": "Info",
    "warning": "Warning",
    "danger": "Danger",
    "success": "Success",
    "note": "Note",
    "tip": "Tip",
    "caution": "Caution"
}

def convert_hints(content):
    """转换GitBook的hint组件为Mintlify组件"""
    # 使用正则表达式匹配所有hint块
    hint_pattern = r'{%\s*hint\s+style="([^"]*)"\s*%}(.*?){%\s*endhint\s*%}'
    
    def replace_hint(match):
        style = match.group(1)
        content = match.group(2).strip()
        
        # 获取对应的Mintlify组件名
        component = STYLE_MAPPING.get(style.lower(), "Info")
        
        # 处理多行内容
        if '\n' in content:
            # 保持缩进
            lines = content.split('\n')
            formatted_content = '\n'.join(lines)
            return f"<{component}>\n{formatted_content}\n</{component}>"
        else:
            # 单行内容
            return f"<{component}>{content}</{component}>"
    
    # 使用re.DOTALL使.能匹配所有字符包括换行符
    return re.sub(hint_pattern, replace_hint, content, flags=re.DOTALL)

def convert_tabs(content):
    """转换GitBook的tabs组件为Mintlify Tabs组件"""
    # 找到所有tabs块
    tabs_start_pattern = r'{%\s*tabs\s*%}'
    tabs_end_pattern = r'{%\s*endtabs\s*%}'
    tab_pattern = r'{%\s*tab title="([^"]*)"\s*%}(.*?){%\s*endtab\s*%}'
    
    # 先替换tab项
    def replace_tab(match):
        title = match.group(1)
        tab_content = match.group(2).strip()
        return f'<Tab title="{title}">\n{tab_content}\n</Tab>'
    
    content = re.sub(tab_pattern, replace_tab, content, flags=re.DOTALL)
    
    # 再替换整个tabs块
    content = re.sub(tabs_start_pattern, '<Tabs>', content)
    content = re.sub(tabs_end_pattern, '</Tabs>', content)
    
    return content

def convert_videos(content):
    """转换GitBook的视频embed为Mintlify video格式"""
    # 匹配多种可能的embed视频格式
    video_pattern1 = r'{%\s*embed\s+url="([^"]+)"\s*%}'
    video_pattern2 = r'{%\s*embed\s+url=[\"]([^\"]+)[\"]\s*%}'
    # 更宽松的模式，匹配各种可能的url格式
    video_pattern3 = r'{%\s*embed\s+url\s*=\s*["\']?([^"\'>}\s]+)["\']?\s*%}'
    
    def replace_video(match):
        url = match.group(1).strip()
        
        # 在转换后打印匹配到的视频链接
        print(f"  - 找到视频链接: {url}")
        
        # 生成简单的video标签格式
        return f'<video controls src="{url}" width="100%"></video>'
    
    # 先应用第一种模式
    content = re.sub(video_pattern1, replace_video, content)
    # 再应用第二种模式
    content = re.sub(video_pattern2, replace_video, content)
    # 最后应用更宽松的模式
    content = re.sub(video_pattern3, replace_video, content)
    
    return content

def convert_file(file_path):
    """转换指定文件中的GitBook组件为Mintlify格式"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 执行转换
        original_content = content  # 保存原始内容用于比较
        
        print(f"\n开始转换文件: {file_path}")
        
        # 检查文件中的特定模式
        hint_count = len(re.findall(r'{%\s*hint', content))
        tabs_count = len(re.findall(r'{%\s*tabs', content))
        embed_count = len(re.findall(r'{%\s*embed', content))
        
        print(f"  检测到: {hint_count} 个 hint 标签, {tabs_count} 个 tabs 标签, {embed_count} 个 embed 标签")
        
        # 应用转换
        content = convert_hints(content)
        content = convert_tabs(content)
        content = convert_videos(content)
        
        # 只有在内容有变化时才写入文件
        if content != original_content:
            # 备份原文件
            backup_path = f"{file_path}.bak"
            with open(backup_path, 'w', encoding='utf-8') as backup:
                backup.write(original_content)
            
            # 写入转换后的内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"✅ 文件已转换并备份: {file_path}")
        else:
            print(f"ℹ️ 文件未发生变化: {file_path}")
        
        return True
    
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        return False

def main():
    """主函数，处理用户输入的文件路径"""
    print("GitBook 到 Mintlify 格式转换工具")
    print("=" * 40)
    
    while True:
        file_path = input("\n请输入要转换的MD/MDX文件路径 (输入q退出): ").strip()
        
        if file_path.lower() == 'q':
            break
        
        if not os.path.exists(file_path):
            print(f"❌ 错误: 文件 '{file_path}' 不存在!")
            continue
        
        if os.path.isdir(file_path):
            print(f"❌ 错误: '{file_path}' 是目录，请输入文件路径!")
            continue
        
        if not file_path.endswith(('.md', '.mdx')):
            print(f"⚠️ 警告: 文件 '{file_path}' 不是Markdown或MDX文件。确定要继续吗? (y/n)")
            if input().lower() != 'y':
                continue
        
        convert_file(file_path)
    
    print("\n程序已退出。")

if __name__ == "__main__":
    main()
