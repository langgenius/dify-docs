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
            # 指向项目根目录
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.json_file = self.base_dir / "plugin_dev_en" / \
            "sync" / json_file  # 修正 JSON 文件路径
        self.plugin_dir = self.base_dir / "en" / "plugins"  # 指向英文插件目录
        self.dev_dir = self.base_dir / "plugin_dev_en"  # 指向英文开发目录
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

    def get_base_filename(self, filepath: str) -> str:
        """从文件路径中提取基本名称，移除扩展名和常见的语言代码。"""
        name = os.path.basename(filepath)
        # 顺序很重要：先匹配更具体的（如 .en.mdx），再匹配通用的（如 .mdx）
        if name.endswith('.en.mdx'):
            return name[:-7]
        elif name.endswith('.zh.mdx'):  # 保留以处理多语言情况
            return name[:-7]
        elif name.endswith('.ja.mdx'):  # 保留以处理多语言情况
            return name[:-7]
        elif name.endswith('.mdx'):  # 通用 .mdx
            return name[:-4]
        return os.path.splitext(name)[0]  # 备选方案：返回不含最后一个扩展名的名称

    def _find_match_in_set(self, source_file_path: str, target_file_set: Set[str]) -> str | None:
        """通过比较基本名称，在目标集合中查找源文件的匹配项。"""
        source_base = self.get_base_filename(source_file_path)
        for target_file in target_file_set:
            if self.get_base_filename(target_file) == source_base:
                return target_file
        return None

    def find_matching_mapping(self, path: str) -> Dict | None:
        """查找与给定路径匹配的映射"""
        for mapping in self.mappings:
            if mapping['plugin_path'] == path or mapping['dev_path'] == path:
                return mapping
        return None

    def sync_files(self):
        """同步文件到映射, 包括添加新文件、移除不存在的文件关联、并尝试链接对应文件。"""
        actual_plugin_files = self.get_mdx_files(self.plugin_dir)
        actual_dev_files = self.get_mdx_files(self.dev_dir)

        made_changes = False

        # 步骤 1: 从现有映射中修剪不存在的文件路径
        valid_mappings = []
        for mapping in self.mappings:
            plugin_path = mapping.get('plugin_path')
            dev_path = mapping.get('dev_path')

            original_plugin_path_for_log = plugin_path
            original_dev_path_for_log = dev_path

            path_changed_in_mapping = False
            if plugin_path and plugin_path not in actual_plugin_files:
                print(f"信息：插件文件 '{plugin_path}' 在映射中但实际不存在，将从该映射中移除。")
                mapping['plugin_path'] = None
                made_changes = True
                path_changed_in_mapping = True

            if dev_path and dev_path not in actual_dev_files:
                print(f"信息：开发文件 '{dev_path}' 在映射中但实际不存在，将从该映射中移除。")
                mapping['dev_path'] = None
                made_changes = True
                path_changed_in_mapping = True

            # 如果映射仍然至少有一个有效路径，则保留它
            if mapping.get('plugin_path') or mapping.get('dev_path'):
                valid_mappings.append(mapping)
            elif path_changed_in_mapping:  # 因修剪而变为空
                print(
                    f"信息：移除了一个空的映射条目 (原插件: {original_plugin_path_for_log}, 原开发: {original_dev_path_for_log})。")
                # made_changes 已在路径被设为 None 时置为 true

        self.mappings = valid_mappings

        # 步骤 2: 识别修剪后映射中当前代表的所有文件
        mapped_plugin_paths = {m['plugin_path']
                               for m in self.mappings if m.get('plugin_path')}
        mapped_dev_paths = {m['dev_path']
                            for m in self.mappings if m.get('dev_path')}

        # 步骤 3: 添加/链接新的插件文件
        for p_file in actual_plugin_files:
            if p_file not in mapped_plugin_paths:  # 这个插件文件不在任何映射的 plugin_path 中
                made_changes = True
                corresponding_dev_file = self._find_match_in_set(
                    p_file, actual_dev_files)
                linked_to_existing_dev_mapping = False

                if corresponding_dev_file:
                    for m in self.mappings:  # 寻找一个只有dev路径且匹配的现有映射
                        if m.get('dev_path') == corresponding_dev_file and not m.get('plugin_path'):
                            m['plugin_path'] = p_file
                            print(
                                f"链接新插件文件到现有开发映射: {p_file} -> {corresponding_dev_file}")
                            mapped_plugin_paths.add(p_file)
                            linked_to_existing_dev_mapping = True
                            break

                if not linked_to_existing_dev_mapping:
                    new_mapping_entry = {
                        'plugin_path': p_file, 'dev_path': None, 'verified': False}
                    if corresponding_dev_file and corresponding_dev_file not in mapped_dev_paths:
                        # 如果对应的dev文件也存在且尚未被映射，则一起加入新条目
                        new_mapping_entry['dev_path'] = corresponding_dev_file
                        mapped_dev_paths.add(corresponding_dev_file)
                        print(
                            f"添加新映射 (插件与新开发链接): {p_file} <-> {corresponding_dev_file}")
                    else:
                        print(f"添加新映射 (仅插件): {p_file}")
                    self.mappings.append(new_mapping_entry)
                    mapped_plugin_paths.add(p_file)

        # 步骤 4: 添加/链接新的开发文件 (那些在步骤3中未被链接的)
        for d_file in actual_dev_files:
            if d_file not in mapped_dev_paths:  # 这个开发文件不在任何映射的 dev_path 中
                made_changes = True
                corresponding_plugin_file = self._find_match_in_set(
                    d_file, actual_plugin_files)
                linked_to_existing_plugin_mapping = False

                if corresponding_plugin_file:  # 对应的插件文件存在
                    for m in self.mappings:  # 寻找一个只有plugin路径且匹配的现有映射
                        if m.get('plugin_path') == corresponding_plugin_file and not m.get('dev_path'):
                            m['dev_path'] = d_file
                            print(
                                f"链接新开发文件到现有插件映射: {corresponding_plugin_file} <- {d_file}")
                            mapped_dev_paths.add(d_file)
                            linked_to_existing_plugin_mapping = True
                            break

                if not linked_to_existing_plugin_mapping:
                    # 如果没有找到可链接的仅插件映射，则添加为新的仅开发映射
                    print(f"添加新映射 (仅开发): {d_file}")
                    self.mappings.append(
                        {'plugin_path': None, 'dev_path': d_file, 'verified': False})
                    mapped_dev_paths.add(d_file)  # 确保它现在被认为是已映射

        # 步骤 5: 清理重复项
        initial_len = len(self.mappings)
        self.remove_duplicates()  # 原位修改 self.mappings
        if len(self.mappings) != initial_len:
            print(f"信息：移除了 {initial_len - len(self.mappings)} 个重复映射。")
            made_changes = True

        # 步骤 6: 如果有更改则保存
        if made_changes:
            self.save_mappings()
            print("\\n映射已同步并保存。")
        else:
            print("\\n映射文件无需更新。")

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
