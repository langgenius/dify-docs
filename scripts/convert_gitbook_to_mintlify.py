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
    """转换GitBook的视频embed为Mintlify iframe格式"""
    # 匹配embed视频格式
    video_pattern = r'{%\s*embed\s+url="([^"]+)"\s*%}'
    
    def replace_video(match):
        url = match.group(1).strip()
        
        # 生成Mintlify iframe格式
        return f'<iframe\n  src="{url}"\n  width="100%"\n  height="315"\n  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\n  allowFullScreen\