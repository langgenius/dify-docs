#!/usr/bin/env python3
"""
文件映射一致性检查工具
对比 JSON 映射记录与实际文件情况，确保映射准确无误
"""

import json
import os
from pathlib import Path
from typing import Set, Dict

# ANSI 颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

class MappingValidator:
    def __init__(self, json_file: str = "plugin_mappings.json"):
        script_file_path = Path(os.path.abspath(__file__)).resolve()
        

        self.base_dir = script_file_path.parent.parent.parent
        
        self.json_file = script_file_path.parent / json_file
        
        # plugin_dir 是 <workspace_root>/en/plugins
        self.plugin_dir = self.base_dir / "en" / "plugins"
        
        # dev_dir 是 <workspace_root>/plugin_dev_en
        self.dev_dir = self.base_dir / "plugin_dev_en"
        
        self.mappings = []
        self.load_mappings()
    
    def load_mappings(self):
        """加载映射文件"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mappings = data.get('mappings', [])
        except FileNotFoundError:
            print(f"{RED}错误: 找不到文件 {self.json_file}{RESET}")
            self.mappings = []
        except json.JSONDecodeError:
            print(f"{RED}错误: JSON 文件格式错误{RESET}")
            self.mappings = []
    
    def count_mdx_files(self, directory: Path) -> int:
        """递归统计目录中的 .mdx 文件数量"""
        count = 0
        for file in directory.rglob('*.mdx'):
            count += 1
        return count
    
    def get_actual_file_paths(self, directory: Path) -> Set[str]:
        """获取目录中所有 .mdx 文件的相对路径"""
        files = set()
        for file in directory.rglob('*.mdx'):
            relative_path = str(file.relative_to(self.base_dir))
            files.add(relative_path)
        return files
    
    def calculate_mapping_stats(self) -> Dict:
        """计算映射统计"""
        total = len(self.mappings)
        plugin_only = sum(1 for m in self.mappings if m.get('plugin_path') and not m.get('dev_path'))
        dev_only = sum(1 for m in self.mappings if m.get('dev_path') and not m.get('plugin_path'))
        complete = sum(1 for m in self.mappings if m.get('plugin_path') and m.get('dev_path'))
        
        # 计算预期的文件数
        expected_plugin_files = total - dev_only  # 总数 - 仅开发 = 插件文件数
        expected_dev_files = total - plugin_only  # 总数 - 仅插件 = 开发文件数
        
        return {
            'total_mappings': total,
            'plugin_only': plugin_only,
            'dev_only': dev_only,
            'complete_mappings': complete,
            'expected_plugin_files': expected_plugin_files,
            'expected_dev_files': expected_dev_files
        }
    
    def validate(self):
        """执行验证"""
        print(f"\n{CYAN}=== 插件文档映射一致性检查工具 ==={RESET}")
        print(f"{CYAN}功能：对比 JSON 映射记录与实际文件，确保映射准确无遗漏{RESET}\n")
        
        # 统计实际文件数
        actual_plugin_count = self.count_mdx_files(self.plugin_dir)
        actual_dev_count = self.count_mdx_files(self.dev_dir)
        
        # 获取映射统计
        stats = self.calculate_mapping_stats()
        
        # 显示映射统计
        print(f"{BLUE}【JSON 映射统计情况】{RESET}")
        print(f"  总映射记录数: {stats['total_mappings']} 条")
        print(f"  完整映射（两边都有）: {stats['complete_mappings']} 条")
        print(f"  仅插件文档: {stats['plugin_only']} 条")
        print(f"  仅开发文档: {stats['dev_only']} 条\n")
        
        # 显示预期vs实际
        print(f"{BLUE}【运行时文件计数情况】{RESET}")
        print("  📁 插件文件夹 (en/plugins):")
        print(f"    JSON 映射预期: {stats['expected_plugin_files']} 个文件")
        print(f"    实际扫描结果: {actual_plugin_count} 个 .mdx 文件")
        if actual_plugin_count == stats['expected_plugin_files']:
            print(f"    状态: {GREEN}✓ 完全一致{RESET}")
        else:
            diff = actual_plugin_count - stats['expected_plugin_files']
            print(f"    状态: {RED}✗ 存在差异 (实际比预期{diff:+d}){RESET}")
        
        print("\n  📁 开发文件夹 (plugin_dev_en):")
        print(f"    JSON 映射预期: {stats['expected_dev_files']} 个文件")
        print(f"    实际扫描结果: {actual_dev_count} 个 .mdx 文件")
        if actual_dev_count == stats['expected_dev_files']:
            print(f"    状态: {GREEN}✓ 完全一致{RESET}")
        else:
            diff = actual_dev_count - stats['expected_dev_files']
            print(f"    状态: {RED}✗ 存在差异 (实际比预期{diff:+d}){RESET}")
        
        # 显示计算公式说明
        print(f"\n{BLUE}【预期文件数计算说明】{RESET}")
        print(f"  插件预期数 = 总映射数({stats['total_mappings']}) - 仅开发数({stats['dev_only']}) = {stats['expected_plugin_files']}")
        print(f"  开发预期数 = 总映射数({stats['total_mappings']}) - 仅插件数({stats['plugin_only']}) = {stats['expected_dev_files']}")
        
        # 如果有差异，找出具体文件
        if actual_plugin_count != stats['expected_plugin_files'] or actual_dev_count != stats['expected_dev_files']:
            self.find_discrepancies()
        else:
            print(f"\n{GREEN}✅ 检查完成：所有文件映射完全一致！{RESET}")
    
    def find_discrepancies(self):
        """找出映射和实际文件的差异"""
        print(f"\n{YELLOW}【差异详细分析】{RESET}\n")
        
        # 获取实际文件路径
        actual_plugin_files = self.get_actual_file_paths(self.plugin_dir)
        actual_dev_files = self.get_actual_file_paths(self.dev_dir)
        
        # 获取映射中的文件路径
        mapped_plugin_files = set(m['plugin_path'] for m in self.mappings if m.get('plugin_path'))
        mapped_dev_files = set(m['dev_path'] for m in self.mappings if m.get('dev_path'))
        
        # 找出未映射的文件
        unmapped_plugin_files = actual_plugin_files - mapped_plugin_files
        unmapped_dev_files = actual_dev_files - mapped_dev_files
        
        # 找出映射中但不存在的文件
        nonexistent_plugin_files = mapped_plugin_files - actual_plugin_files
        nonexistent_dev_files = mapped_dev_files - actual_dev_files
        
        has_issues = False
        
        if unmapped_plugin_files:
            has_issues = True
            print(f"{RED}❗ 实际存在但 JSON 中未记录的插件文件:{RESET}")
            for file in sorted(unmapped_plugin_files):
                print(f"  - {file}")
        
        if unmapped_dev_files:
            has_issues = True
            print(f"\n{RED}❗ 实际存在但 JSON 中未记录的开发文件:{RESET}")
            for file in sorted(unmapped_dev_files):
                print(f"  - {file}")
        
        if nonexistent_plugin_files:
            has_issues = True
            print(f"\n{RED}❗ JSON 中记录但实际不存在的插件文件:{RESET}")
            for file in sorted(nonexistent_plugin_files):
                print(f"  - {file}")
        
        if nonexistent_dev_files:
            has_issues = True
            print(f"\n{RED}❗ JSON 中记录但实际不存在的开发文件:{RESET}")
            for file in sorted(nonexistent_dev_files):
                print(f"  - {file}")
        
        if has_issues:
            print(f"\n{YELLOW}💡 建议：运行 sync_mdx_to_json.py 同步文件到映射{RESET}")
        else:
            print(f"{GREEN}未发现具体文件差异，检查完成{RESET}")

def main():
    """主函数"""
    validator = MappingValidator()
    validator.validate()

if __name__ == "__main__":
    main()
