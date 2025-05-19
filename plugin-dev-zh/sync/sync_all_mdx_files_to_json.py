#!/usr/bin/env python3
"""
同步 MDX 文件到映射
确保所有 mdx 文件都在 JSON 映射中，并去除 metadata
"""

import json
import os
from pathlib import Path
from typing import Set, Dict


class MdxSyncManager:
    def __init__(self, json_file: str = "plugin_mappings.json"):
        self.base_dir = Path(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Corrected base_dir to project root
        self.json_file = self.base_dir / "plugin-dev-zh" / "sync" / json_file  # Corrected json_file path
        self.plugin_dir = self.base_dir / "zh-hans" / "plugins"
        self.dev_dir = self.base_dir / "plugin-dev-zh"
        self.mappings = []
        self.load_mappings()

    def load_mappings(self):
        """加载现有映射"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 只加载 mappings，忽略 metadata
                self.mappings = data.get('mappings', [])
        except FileNotFoundError:
            print(f"创建新的映射文件: {self.json_file}")
            self.mappings = []
        except json.JSONDecodeError:
            print("JSON 文件格式错误，创建新文件")
            self.mappings = []

    def save_mappings(self):
        """保存映射（不包含 metadata）"""
        # 只保存 mappings，不保存 metadata
        data = {
            'mappings': self.mappings
        }
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_mdx_files(self, directory: Path) -> Set[str]:
        """获取目录中所有 mdx 文件的相对路径"""
        mdx_files = set()
        for file in directory.rglob('*.mdx'):
            relative_path = str(file.relative_to(self.base_dir))
            mdx_files.add(relative_path)
        return mdx_files

    def get_existing_paths(self) -> Dict[str, Dict]:
        """获取现有映射中的所有路径"""
        existing = {}
        for mapping in self.mappings:
            if mapping['plugin_path']:
                existing[mapping['plugin_path']] = mapping
            if mapping['dev_path']:
                existing[mapping['dev_path']] = mapping
        return existing

    def find_matching_mapping(self, path: str) -> Dict:
        """查找与给定路径匹配的映射"""
        for mapping in self.mappings:
            if mapping['plugin_path'] == path or mapping['dev_path'] == path:
                return mapping
        return None

    def sync_files(self):
        """同步文件到映射"""
        # 获取所有 mdx 文件
        plugin_files = self.get_mdx_files(self.plugin_dir)
        dev_files = self.get_mdx_files(self.dev_dir)

        # 获取现有映射中的路径
        existing_paths = self.get_existing_paths()

        added_count = 0

        # 处理 plugin 文件夹中的文件
        for plugin_file in plugin_files:
            if plugin_file not in existing_paths:
                # 查找是否已经在某个映射的 dev_path 中
                existing_mapping = self.find_matching_mapping(plugin_file)
                if not existing_mapping:
                    # 创建新映射
                    new_mapping = {
                        'plugin_path': plugin_file,
                        'dev_path': None,
                        'verified': False
                    }
                    self.mappings.append(new_mapping)
                    added_count += 1
                    print(f"添加新映射: {plugin_file}")

        # 处理 dev 文件夹中的文件
        for dev_file in dev_files:
            if dev_file not in existing_paths:
                # 查找是否已经在某个映射的 plugin_path 中
                existing_mapping = self.find_matching_mapping(dev_file)
                if not existing_mapping:
                    # 尝试找到可能对应的 plugin 文件
                    matching_plugin = self.find_potential_match(
                        dev_file, plugin_files)
                    if matching_plugin:
                        # 更新现有映射
                        for mapping in self.mappings:
                            if mapping['plugin_path'] == matching_plugin and not mapping['dev_path']:
                                mapping['dev_path'] = dev_file
                                print(f"更新映射: {matching_plugin} <- {dev_file}")
                                break
                    else:
                        # 创建新映射
                        new_mapping = {
                            'plugin_path': None,
                            'dev_path': dev_file,
                            'verified': False
                        }
                        self.mappings.append(new_mapping)
                        added_count += 1
                        print(f"添加新映射: {dev_file}")

        # 清理重复项
        self.remove_duplicates()

        if added_count > 0:
            self.save_mappings()
            print(f"\n已添加 {added_count} 个新映射")
        else:
            print("\n所有文件都已在映射中")

    def find_potential_match(self, dev_file: str, plugin_files: Set[str]) -> str:
        """尝试找到可能匹配的 plugin 文件"""
        # 提取文件名（去除路径和语言后缀）
        dev_filename = os.path.basename(dev_file)
        if dev_filename.endswith('.mdx'):
            base_name = dev_filename[:-7]  # 去除 .mdx
        else:
            base_name = dev_filename[:-4]  # 去除 .mdx

        # 查找相似的 plugin 文件
        for plugin_file in plugin_files:
            plugin_filename = os.path.basename(plugin_file)
            if base_name in plugin_filename:
                return plugin_file

        return None

    def remove_duplicates(self):
        """去除重复的映射"""
        unique_mappings = []
        seen = set()

        for mapping in self.mappings:
            # 创建唯一键
            key = (mapping.get('plugin_path'), mapping.get('dev_path'))
            if key not in seen:
                seen.add(key)
                unique_mappings.append(mapping)

        self.mappings = unique_mappings

    def show_status(self):
        """显示当前状态"""
        plugin_count = sum(1 for m in self.mappings if m['plugin_path'])
        dev_count = sum(1 for m in self.mappings if m['dev_path'])
        both_count = sum(
            1 for m in self.mappings if m['plugin_path'] and m['dev_path'])

        print("\n当前映射状态:")
        print(f"总映射数: {len(self.mappings)}")
        print(f"Plugin 文件: {plugin_count}")
        print(f"Dev 文件: {dev_count}")
        print(f"完整映射: {both_count}")


def main():
    """主函数"""
    manager = MdxSyncManager()

    print("开始同步 MDX 文件到映射...")
    manager.sync_files()
    manager.show_status()

    print("\n同步完成！")


if __name__ == "__main__":
    main()
