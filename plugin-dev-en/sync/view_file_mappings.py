#!/usr/bin/env python3
"""
简单的插件映射查看器
快速查看文件映射关系，支持在 VS Code 中点击打开
"""

import json
import os
from pathlib import Path

# ANSI 颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

# 新增符号常量
CHECK_MARK = f"{GREEN}✅{RESET}"
CROSS_MARK = f"{RED}❌{RESET}"
EMPTY_MARK = f"{YELLOW}❎{RESET}"

def load_mappings(json_file="plugin_mappings.json"):
    """加载映射文件"""
    # base_dir 是工作区根目录。脚本位于 <workspace_root>/plugin-dev-en/sync/script.py
    # 因此，base_dir 是脚本目录的父目录的父目录的父目录。
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    json_path = base_dir / "plugin-dev-en" / "sync" / json_file # 修正 JSON 文件路径
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{RED}错误: 找不到文件 {json_path}{RESET}")
        return None
    except json.JSONDecodeError:
        print(f"{RED}错误: JSON 文件格式错误{RESET}")
        return None

def calculate_statistics(mappings):
    """动态计算统计信息"""
    total = len(mappings)
    verified = sum(1 for m in mappings if m.get('verified', False))
    pending = total - verified
    
    # 额外统计
    plugin_only = sum(1 for m in mappings if m.get('plugin_path') and not m.get('dev_path'))
    dev_only = sum(1 for m in mappings if m.get('dev_path') and not m.get('plugin_path'))
    complete = sum(1 for m in mappings if m.get('plugin_path') and m.get('dev_path'))
    
    return {
        'total_mappings': total,
        'verified_count': verified,
        'pending_verification': pending,
        'plugin_only': plugin_only,
        'dev_only': dev_only,
        'complete_mappings': complete
    }

def show_mappings():
    """显示所有映射关系"""
    data = load_mappings()
    if not data:
        return
    
    mappings = data.get('mappings', [])
    stats = calculate_statistics(mappings)
    
    print(f"\n{BLUE}插件文档映射关系{RESET}")
    print(f"总计: {stats['total_mappings']} | "
          f"已验证: {GREEN}{stats['verified_count']}{RESET} | "
          f"待验证: {YELLOW}{stats['pending_verification']}{RESET}")
    print(f"完整映射: {stats['complete_mappings']} | "
          f"仅插件: {stats['plugin_only']} | "
          f"仅开发: {stats['dev_only']}")
    
    print("\n路径 | 验证 | 同步细节\n")
    
    separator_line1 = "-" * 56
    separator_line2 = "*" * 56
    
    for idx, mapping in enumerate(mappings, 1):
        plugin_path = mapping.get('plugin_path')
        dev_path = mapping.get('dev_path')
        verified = mapping.get('verified', False)
        sync_info = mapping.get('sync', '').strip()
        
        # 打印分隔符
        print(separator_line1)
        print(separator_line2)
        print(separator_line1)
        print() # 在分隔符后添加空行

        # 显示 Help 路径
        if plugin_path:
            print(f"Help: {plugin_path}")
        else:
            print(f"Help: {EMPTY_MARK}")
        
        # 显示 Dev 路径
        if dev_path:
            print(f"Dev: {dev_path}")
        else:
            print(f"Dev: {EMPTY_MARK}")
            
        # 显示 Verify 状态和 sync_info
        verify_symbol = CHECK_MARK if verified else CROSS_MARK
        print(f"Verify: {verify_symbol}")
        if sync_info:
            print(sync_info)
        # No "else" needed here as per example, empty sync_info means just the symbol

def main():
    """主函数"""
    show_mappings()
    
    print(f"\n{BLUE}提示:{RESET} 在 VS Code 中，你可以使用 Cmd+点击 路径来快速打开文件")
    print(f"{BLUE}命令:{RESET} python view_file_mappings.py")

if __name__ == "__main__":
    main()
