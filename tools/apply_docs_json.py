import json
import os
import re
from collections import defaultdict

# --- 配置 ---
refresh = True  # 如果为 True，将清空指定版本的 tabs
DOCS_JSON_PATH = 'docs.json'

# --- 简体中文配置（docs_config） ---
PLUGIN_DEV_ZH = {
    "DOCS_DIR": "plugin_dev_zh",  # 插件开发文档目录
    "LANGUAGE_CODE": "简体中文",  # 注意：虽然变量名是 LANGUAGE_CODE，但会部署为 docs.json 中的 'version' 值。
    "FILE_EXTENSION": ".zh.mdx",
    "TARGET_TAB_NAME": "插件开发",  # 新增：目标 Tab 名称
    "FILENAME_PATTERN": re.compile(r'^(\d{4})-(.*?)\.zh\.mdx$'),  # 新增：文件名匹配模式
    "PWX_TO_GROUP_MAP": {
        # --- PWX 到 Group 名称的映射 (统一到 "插件开发" Tab) ---
        # (P, W, X) -> (tab_name, group_name, nested_group_name)
        # Tab: 插件开发
        #   Group: 概念与入门
        ('0', '1', '1'): ("插件开发", "概念与入门", "概览"),
        ('0', '1', '3'): ("插件开发", "概念与入门", None),
        #   Group: 开发实践
        ('0', '2', '1'): ("插件开发", "开发实践", "快速开始"),
        ('0', '2', '2'): ("插件开发", "开发实践", "开发 Dify 插件"),
        #   Group: 贡献与发布
        ('0', '3', '1'): ("插件开发", "贡献与发布", "行为准则与规范"),
        ('0', '3', '2'): ("插件开发", "贡献与发布", "发布与上架"),
        ('0', '3', '3'): ("插件开发", "贡献与发布", "常见问题解答"),
        #   Group: 实践案例与示例
        ('0', '4', '3'): ("插件开发", "实践案例与示例", "开发示例"),
        #   Group: 高级开发
        ('9', '2', '2'): ("插件开发", "高级开发", "Extension 与 Agent"),
        ('9', '2', '3'): ("插件开发", "高级开发", "Extension 与 Agent"),
        ('9', '4', '3'): ("插件开发", "高级开发", "Extension 与 Agent"),
        ('9', '2', '4'): ("插件开发", "高级开发", "反向调用"),
        #   Group: Reference & Specifications
        ('0', '4', '1'): ("插件开发", "Reference & Specifications", "核心规范与功能"),
    },
    "DESIRED_GROUP_ORDER": [
        "概念与入门",
        "开发实践",
        "贡献与发布",
        "实践案例与示例",
        "高级开发",
        "Reference & Specifications"  # 确保这个在最后
    ]
}

# --- English Configuration ---
PLUGIN_DEV_EN = {
    "DOCS_DIR": "plugin_dev_en",  # Plugin development documentation directory
    "LANGUAGE_CODE": "English",  # Note: Although the variable name is LANGUAGE_CODE, it will be deployed as the 'version' value in docs.json.
    "FILE_EXTENSION": ".en.mdx",
    "TARGET_TAB_NAME": "Plugin Development",
    "FILENAME_PATTERN": re.compile(r'^(\d{4})-(.*?)\.en\.mdx$'),
    "PWX_TO_GROUP_MAP": {
        # --- PWX to Group Name Mapping (Unified under the "Plugin Development" Tab) ---
        # (P, W, X) -> (tab_name, group_name, nested_group_name)
        # Tab: Plugin Development
        #   Group: Concepts & Getting Started
        ('0', '1', '1'): ("Plugin Development", "Concepts & Getting Started", "Overview"),
        ('0', '1', '3'): ("Plugin Development", "Concepts & Getting Started", None),
        #   Group: Development Practices
        ('0', '2', '1'): ("Plugin Development", "Development Practices", "Quick Start"),
        ('0', '2', '2'): ("Plugin Development", "Development Practices", "Developing Dify Plugins"),
        #   Group: Contribution & Publishing
        ('0', '3', '1'): ("Plugin Development", "Contribution & Publishing", "Code of Conduct & Standards"),
        ('0', '3', '2'): ("Plugin Development", "Contribution & Publishing", "Publishing & Listing"),
        ('0', '3', '3'): ("Plugin Development", "Contribution & Publishing", "FAQ"),
        #   Group: Examples & Use Cases
        ('0', '4', '3'): ("Plugin Development", "Examples & Use Cases", "Development Examples"),
        #   Group: Advanced Development
        ('9', '2', '2'): ("Plugin Development", "Advanced Development", "Extension & Agent"),
        ('9', '2', '3'): ("Plugin Development", "Advanced Development", "Extension & Agent"),
        ('9', '4', '3'): ("Plugin Development", "Advanced Development", "Extension & Agent"),
        ('9', '2', '4'): ("Plugin Development", "Advanced Development", "Reverse Calling"),
        #   Group: Reference & Specifications
        ('0', '4', '1'): ("Plugin Development", "Reference & Specifications", "Core Specifications & Features"),
    },
    "DESIRED_GROUP_ORDER": [
        "Concepts & Getting Started",
        "Development Practices",
        "Contribution & Publishing",
        "Examples & Use Cases",
        "Advanced Development",
        "Reference & Specifications"  # Ensure this is last
    ]
}

# --- 日本語設定 (Japanese Configuration) ---
PLUGIN_DEV_JA = {
    "DOCS_DIR": "plugin_dev_ja",  # プラグイン開発ドキュメントディレクトリ
    "LANGUAGE_CODE": "日本語",  #注意：変数名は LANGUAGE_CODE ですが、docs.json の 'version' 値としてデプロイされます。
    "FILE_EXTENSION": ".ja.mdx",
    "TARGET_TAB_NAME": "プラグイン開発", # 対象タブ名
    "FILENAME_PATTERN": re.compile(r'^(\d{4})-(.*?)\.ja\.mdx$'), # ファイル名照合パターン
    "PWX_TO_GROUP_MAP": {
        # --- PWX からグループ名へのマッピング（「プラグイン開発」タブに統一）---
        # (P, W, X) -> (tab_name, group_name, nested_group_name)
        # Tab: プラグイン開発
        #   Group: 概念と概要
        ('0', '1', '1'): ("プラグイン開発", "概念と概要", "概要"),
        ('0', '1', '3'): ("プラグイン開発", "概念と概要", None),
        #   Group: 開発実践
        ('0', '2', '1'): ("プラグイン開発", "開発実践", "クイックスタート"),
        ('0', '2', '2'): ("プラグイン開発", "開発実践", "Difyプラグインの開発"),
        #   Group: 貢献と公開
        ('0', '3', '1'): ("プラグイン開発", "貢献と公開", "行動規範と基準"),
        ('0', '3', '2'): ("プラグイン開発", "貢献と公開", "公開と掲載"),
        ('0', '3', '3'): ("プラグイン開発", "貢献と公開", "よくある質問 (FAQ)"),
        #   Group: 実践例とユースケース
        ('0', '4', '3'): ("プラグイン開発", "実践例とユースケース", "開発例"),
        #   Group: 高度な開発
        ('9', '2', '2'): ("プラグイン開発", "高度な開発", "Extension と Agent"),
        ('9', '2', '3'): ("プラグイン開発", "高度な開発", "Extension と Agent"),
        ('9', '4', '3'): ("プラグイン開発", "高度な開発", "Extension と Agent"),
        ('9', '2', '4'): ("プラグイン開発", "高度な開発", "リバースコール"), # Reverse Calling
        #   Group: リファレンスと仕様
        ('0', '4', '1'): ("プラグイン開発", "リファレンスと仕様", "コア仕様と機能"),
    },
    "DESIRED_GROUP_ORDER": [
        "概念と概要",
        "開発実践",
        "貢献と公開",
        "実践例とユースケース",
        "高度な開発",
        "リファレンスと仕様"  # これが最後になるように確認
    ]
}


# --- 辅助函数 ---

def clear_tabs_if_refresh(navigation_data, version_code, target_tab_name, do_refresh):
    """如果 do_refresh 为 True，则查找指定版本和目标 Tab，并清空其 groups 列表"""
    if not do_refresh:
        return False  # 未执行清空

    if not navigation_data or 'versions' not in navigation_data:
        print("警告: 'navigation.versions' 未找到，无法清空 tabs。")
        return False

    version_found = False
    tab_found_and_cleared = False
    for version_nav in navigation_data.get('versions', []):
        if version_nav.get('version') == version_code:
            version_found = True
            target_tab = None
            if 'tabs' in version_nav and isinstance(version_nav['tabs'], list):
                for tab in version_nav['tabs']:
                    if isinstance(tab, dict) and tab.get('tab') == target_tab_name:
                        target_tab = tab
                        break

            if target_tab:
                if 'groups' in target_tab:
                    target_tab['groups'] = []
                    print(f"信息: 已清空版本 '{version_code}' 下 Tab '{target_tab_name}' 的 groups (因为 refresh=True)。")
                    tab_found_and_cleared = True
                else:
                    # 如果 'groups' 不存在，也视为一种“清空”状态，或者可以创建一个空的
                    target_tab['groups'] = []
                    print(f"信息: 版本 '{version_code}' 下 Tab '{target_tab_name}' 没有 'groups' 键，已确保其为空列表 (因为 refresh=True)。")
                    tab_found_and_cleared = True
            else:
                print(f"警告: 在版本 '{version_code}' 中未找到目标 Tab '{target_tab_name}'，无法清空其 groups。")
            break # 找到版本后即可退出循环

    if not version_found:
        print(f"警告: 未找到版本 '{version_code}'，无法清空任何 Tab。")
        return False

    return tab_found_and_cleared


def get_page_path(filename, docs_config):  # docs_config 参数保留，但 FILE_EXTENSION 不再用于此处的后缀移除
    """从 mdx 文件名获取 mintlify 页面路径 (固定去掉末尾 .mdx 后缀)"""
    docs_dir = docs_config["DOCS_DIR"]
    # 固定移除末尾的 .mdx，以保留 .zh 或 .en 等语言标识
    if filename.endswith('.mdx'):
        base_filename = filename[:-len('.mdx')]
    else:
        # 如果不以 .mdx 结尾，则引发错误，因为这是预期格式
        raise ValueError(f"错误: 文件名 '{filename}' 不以 '.mdx' 结尾，无法处理。")

    return os.path.join(docs_dir, base_filename)


def extract_existing_pages(navigation_data, version_code, target_tab_name):
    """递归提取指定版本和目标 Tab 下所有已存在的页面路径"""
    existing_pages = set()
    target_version_nav = None
    target_tab_nav = None # 新增：用于存储找到的目标 Tab 对象

    if not navigation_data or 'versions' not in navigation_data:
        print("警告: 'navigation.versions' 未找到")
        return existing_pages, None, None # 返回三个值

    # 查找目标版本
    for version_nav in navigation_data.get('versions', []):
        if version_nav.get('version') == version_code:
            target_version_nav = version_nav
            break

    if not target_version_nav:
        print(f"警告: 版本 '{version_code}' 在 docs.json 中未找到")
        return existing_pages, None, None # 返回三个值

    # 在目标版本中查找目标 Tab
    if 'tabs' in target_version_nav and isinstance(target_version_nav['tabs'], list):
        for tab in target_version_nav['tabs']:
            if isinstance(tab, dict) and tab.get('tab') == target_tab_name:
                target_tab_nav = tab # 存储找到的 Tab 对象
                # 仅从目标 Tab 中提取页面
                for group in tab.get('groups', []):
                    if isinstance(group, dict):
                        _recursive_extract(group, existing_pages)
                break # 找到目标 Tab 后即可退出循环
    else: # 'tabs' might not exist or not be a list
        target_version_nav['tabs'] = []


    if not target_tab_nav:
         print(f"警告: 在版本 '{version_code}' 中未找到 Tab '{target_tab_name}'，无法提取现有页面。")
         # 即使 Tab 不存在，也返回版本导航对象，以便后续可能创建 Tab
         return existing_pages, target_version_nav, None

    # 返回提取到的页面、版本导航对象和目标 Tab 对象
    return existing_pages, target_version_nav, target_tab_nav


def _recursive_extract(group_item, pages_set):
    """递归辅助函数"""
    # Ensure group_item is a dictionary before proceeding
    if not isinstance(group_item, dict):
        return

    if 'pages' in group_item and isinstance(group_item['pages'], list):
        for page in group_item['pages']:
            if isinstance(page, str):
                pages_set.add(page)
            elif isinstance(page, dict) and 'group' in page:
                # Recurse into nested groups
                _recursive_extract(page, pages_set)


def remove_obsolete_pages(target_tab_data, pages_to_remove):
    """递归地从目标 Tab 的 groups 结构中移除失效页面路径。
       注意：此函数直接修改传入的 target_tab_data 字典。
    """
    if not isinstance(target_tab_data, dict) or 'groups' not in target_tab_data:
        # 如果输入不是预期的 Tab 结构，则直接返回
        return

    groups = target_tab_data.get('groups', [])
    if not isinstance(groups, list):
        # 如果 groups 不是列表，也无法处理
        return

    # 使用索引迭代以安全地移除项
    i = 0
    while i < len(groups):
        group_item = groups[i]
        if isinstance(group_item, dict):
            # 递归处理 group 内部的 pages
            _remove_obsolete_from_group(group_item, pages_to_remove)
            # 如果处理后 group 的 pages 为空（且没有嵌套 group），可以选择移除该 group
            # 当前逻辑：保留空 group 结构
            if not group_item.get('pages'):
                 print(f"信息: Group '{group_item.get('group')}' 清理后为空，已保留结构。")
            i += 1
        else:
            # 如果 groups 列表中包含非字典项（不符合预期），则跳过
            i += 1

def _remove_obsolete_from_group(group_dict, pages_to_remove):
    """辅助函数，递归处理单个 group 或 nested group 内的 pages"""
    if not isinstance(group_dict, dict) or 'pages' not in group_dict:
        return

    pages = group_dict.get('pages', [])
    if not isinstance(pages, list):
        return

    new_pages = []
    for page_item in pages:
        if isinstance(page_item, str):
            if page_item not in pages_to_remove:
                new_pages.append(page_item)
            else:
                print(f"    - {page_item} (从 Group '{group_dict.get('group')}' 移除)")
        elif isinstance(page_item, dict) and 'group' in page_item:
            # 递归处理嵌套的 group
            _remove_obsolete_from_group(page_item, pages_to_remove)
            # 保留嵌套 group 结构，即使它变空
            if page_item or page_item.get('pages'): # 检查字典是否为空或 pages 是否存在
                 new_pages.append(page_item)
            else:
                 print(f"信息: 嵌套 Group '{page_item.get('group')}' 清理后为空，已保留结构。")
                 new_pages.append(page_item) # 仍然添加空的嵌套组结构
        else:
            # 保留无法识别的项
            new_pages.append(page_item)
    group_dict['pages'] = new_pages


def find_or_create_target_group(target_version_nav, tab_name, group_name, nested_group_name):
    # 注意：target_version_nav 是特定版本对象，例如 {"version": "简体中文", "tabs": [...]}
    target_tab = None
    # Ensure 'tabs' exists and is a list
    if 'tabs' not in target_version_nav or not isinstance(target_version_nav['tabs'], list):
        target_version_nav['tabs'] = []

    for tab in target_version_nav['tabs']:
        if isinstance(tab, dict) and tab.get('tab') == tab_name:
            target_tab = tab
            break
    if target_tab is None:
        target_tab = {'tab': tab_name, 'groups': []}
        target_version_nav['tabs'].append(target_tab)

    target_group = None
    # Ensure 'groups' exists and is a list
    if 'groups' not in target_tab or not isinstance(target_tab['groups'], list):
        target_tab['groups'] = []

    for group in target_tab['groups']:
        if isinstance(group, dict) and group.get('group') == group_name:
            target_group = group
            break
    if target_group is None:
        target_group = {'group': group_name, 'pages': []}
        target_tab['groups'].append(target_group)

    # Ensure 'pages' exists in the target_group and is a list
    if 'pages' not in target_group or not isinstance(target_group['pages'], list):
        target_group['pages'] = []

    # Default container is the top-level group's pages list
    target_pages_container = target_group['pages']

    if nested_group_name:
        target_nested_group = None
        # Find existing nested group
        for item in target_group['pages']:
            if isinstance(item, dict) and item.get('group') == nested_group_name:
                target_nested_group = item
                # Ensure pages list exists in nested group
                target_pages_container = target_nested_group.setdefault(
                    'pages', [])
                # Ensure it's actually a list after setdefault
                if not isinstance(target_pages_container, list):
                    target_nested_group['pages'] = []
                    target_pages_container = target_nested_group['pages']
                break
        # If not found, create it
        if target_nested_group is None:
            target_nested_group = {'group': nested_group_name, 'pages': []}
            # Check if target_group['pages'] is already the container we want to add to
            # This logic assumes nested groups are *always* dicts within the parent's 'pages' list
            target_group['pages'].append(target_nested_group)
            target_pages_container = target_nested_group['pages']

    # Final check before returning
    if not isinstance(target_pages_container, list):
        # 这表示内部逻辑错误，应该引发异常
        raise RuntimeError(
            f"内部错误: 无法为 Tab='{tab_name}', Group='{group_name}', Nested='{nested_group_name}' 获取有效的 pages 列表。")

    return target_pages_container

# --- 主逻辑 ---


def get_group_sort_key(group_dict, docs_config):
    """为排序提供 key，根据 DESIRED_GROUP_ORDER 返回索引，未知组放在最后"""
    group_name = group_dict.get('group', '')
    desired_order = docs_config["DESIRED_GROUP_ORDER"]
    try:
        return desired_order.index(group_name)
    except ValueError:
        return len(desired_order)  # 将未在列表中的组排在最后


def main(docs_config, navigation_data):  # navigation_data: 传入内存中的 navigation 字典供直接修改
    """处理单个文档配置，并直接修改传入的 navigation_data"""
    print(f"\n--- 开始处理版本: {docs_config['LANGUAGE_CODE']} / Tab: {docs_config['TARGET_TAB_NAME']} ---")

    # 从 docs_config 获取配置值
    language_code = docs_config["LANGUAGE_CODE"]
    docs_dir = docs_config["DOCS_DIR"]
    file_extension = docs_config["FILE_EXTENSION"]
    pwx_to_group_map = docs_config["PWX_TO_GROUP_MAP"]
    filename_pattern = docs_config["FILENAME_PATTERN"]  # 使用配置中的 pattern
    target_tab_name = docs_config["TARGET_TAB_NAME"]  # 使用配置中的 tab name

    # 1. 清理或准备版本导航 (不再加载 JSON，直接使用传入的 navigation_data)
    navigation = navigation_data  # 使用传入的 navigation 对象进行操作

    # 使用 language_code 和 target_tab_name 清理目标 Tab
    was_refreshed = clear_tabs_if_refresh(navigation, language_code, target_tab_name, refresh)
    if was_refreshed:
        print(f"继续执行 Tab '{target_tab_name}' 的后续页面提取和添加操作...")

    # 2. 提取目标 Tab 的现有页面或创建版本/Tab 导航
    existing_pages, target_version_nav, target_tab_nav = extract_existing_pages(
        navigation, language_code, target_tab_name)

    if target_version_nav is None:
        print(f"信息：在导航数据中未找到版本 '{language_code}'，将创建。")
        if 'versions' not in navigation:  # 确保 versions 列表存在
            navigation['versions'] = []
        target_version_nav = {"version": language_code, "tabs": []}
        navigation['versions'].append(target_version_nav)
        existing_pages = set()
        target_tab_nav = None # 版本是新建的，Tab 肯定不存在

    # 如果目标 Tab 不存在，需要创建它
    if target_tab_nav is None:
        print(f"信息: 在版本 '{language_code}' 中未找到 Tab '{target_tab_name}'，将创建。")
        target_tab_nav = {'tab': target_tab_name, 'groups': []}
        # 确保 target_version_nav['tabs'] 是列表
        if 'tabs' not in target_version_nav or not isinstance(target_version_nav['tabs'], list):
            target_version_nav['tabs'] = []
        target_version_nav['tabs'].append(target_tab_nav)
        existing_pages = set() # 新 Tab 没有现有页面

    print(f"找到 {len(existing_pages)} 个已存在的页面 (版本: '{language_code}', Tab: '{target_tab_name}')。")

    # 3. 扫描文件系统 (这部分不变，扫描目录下的所有匹配文件)
    filesystem_pages = set()
    valid_files = []
    if not os.path.isdir(docs_dir):
        # 如果目录不存在，则无法继续处理此配置，引发错误
        raise FileNotFoundError(f"错误: 配置 '{language_code}' 的文档目录 '{docs_dir}' 不存在。")
    else:
        for filename in os.listdir(docs_dir):
            # 使用配置中的 filename_pattern
            if filename.endswith(file_extension) and filename_pattern.match(filename):
                try: # 添加 try-except 块以捕获 get_page_path 可能引发的 ValueError
                    page_path = get_page_path(filename, docs_config)
                    filesystem_pages.add(page_path)
                    valid_files.append(filename)
                except ValueError as e:
                    # 从 get_page_path 捕获到错误，打印并继续处理其他文件，或重新引发以停止
                    print(f"错误处理文件 '{filename}': {e}。将跳过此文件。")
                    # 如果希望停止整个过程，取消注释下一行:
                    # raise e
        print(f"在 '{docs_dir}' 找到 {len(filesystem_pages)} 个有效的文档文件。")


    # 4. 计算差异 (相对于目标 Tab 的 existing_pages)
    new_files_paths = filesystem_pages - existing_pages
    removed_files_paths = existing_pages - filesystem_pages

    print(f"新增文件数 (相对于 Tab '{target_tab_name}'): {len(new_files_paths)}")
    print(f"移除文件数 (相对于 Tab '{target_tab_name}'): {len(removed_files_paths)}")

    # 5. 移除失效页面 (仅从目标 Tab 移除)
    if removed_files_paths and target_tab_nav: # 确保目标 Tab 存在
        print(f"正在从 Tab '{target_tab_name}' 移除失效页面...")
        remove_obsolete_pages(target_tab_nav, removed_files_paths) # 直接传入目标 Tab 对象
        print(f"已处理从 Tab '{target_tab_name}' 移除: {removed_files_paths}")
    elif removed_files_paths:
        print(f"警告: 存在失效页面 {removed_files_paths}，但未找到目标 Tab '{target_tab_name}' 进行移除。")


    # 6. 添加新页面 (逻辑不变，但 find_or_create_target_group 会确保添加到正确的 Tab 和 Group)
    if new_files_paths:
        print(f"正在向 Tab '{target_tab_name}' 添加新页面...")
        new_files_sorted = sorted(
            [f for f in valid_files if get_page_path(f, docs_config) in new_files_paths])

        groups_to_add = defaultdict(list)
        for filename in new_files_sorted:
            match = filename_pattern.match(filename)  # 使用配置中的 pattern
            if match:
                pwxy = match.group(1)
                if len(pwxy) >= 3:
                    p, w, x = pwxy[0], pwxy[1], pwxy[2]
                    try: # 包裹 get_page_path 调用
                        page_path = get_page_path(filename, docs_config)
                    except ValueError as e:
                         print(f"错误处理文件 '{filename}' (添加阶段): {e}。将跳过此文件。")
                         continue # 跳过这个文件

                    group_key = (p, w, x)
                    if group_key in pwx_to_group_map:
                        map_result = pwx_to_group_map[group_key]
                        current_tab_name_from_map = map_result[0]
                        # 强制使用配置的目标 Tab 名称
                        if current_tab_name_from_map != target_tab_name:
                             print(f"警告: 文件 '{filename}' 根据 PWX 映射到 Tab '{current_tab_name_from_map}'，但当前配置强制处理 Tab '{target_tab_name}'。将添加到 '{target_tab_name}'。")
                        # 始终使用配置中定义的 target_tab_name
                        tab_name_to_use = target_tab_name

                        if len(map_result) == 3:
                            _, group_name, nested_group_name = map_result
                        else: # 兼容旧格式或只有两项的情况
                            if len(map_result) >= 2:
                                _, group_name = map_result[:2] # 取前两项
                            else:
                                # 处理 map_result 项数不足的情况
                                print(f"错误: PWX_TO_GROUP_MAP 中键 '{group_key}' 的值 '{map_result}' 格式不正确，至少需要两项。跳过文件 '{filename}'。")
                                continue
                            nested_group_name = None # 假设没有嵌套组

                        groups_to_add[(tab_name_to_use, group_name, nested_group_name)].append(
                            page_path)
                    else:
                        print(
                            f"警告: 文件 '{filename}' 的 PWX 前缀 ('{p}', '{w}', '{x}') 在 PWX_TO_GROUP_MAP 中没有找到映射，将跳过添加。")
                else:
                    # 数字前缀不足3位是文件名格式错误，应引发异常
                    raise ValueError(
                        f"错误: 文件 '{filename}' 的数字前缀 '{pwxy}' 不足3位，无法解析 PWX。")

        for (tab_name, group_name, nested_group_name), pages_to_append in groups_to_add.items():
             # 确保只添加到目标 Tab 下 (此检查现在是多余的，因为上面强制使用了 target_tab_name)
            # if tab_name == target_tab_name:
            print(
                f"  添加到 Tab='{tab_name}', Group='{group_name}', Nested='{nested_group_name or '[无]'}' : {len(pages_to_append)} 个页面")
            # find_or_create_target_group 现在需要 target_version_nav 来定位或创建 Tab
            target_pages_list = find_or_create_target_group(
                target_version_nav, tab_name, group_name, nested_group_name) # tab_name 此时应等于 target_tab_name

            if isinstance(target_pages_list, list):
                for new_page in pages_to_append:
                    if new_page not in target_pages_list:
                        target_pages_list.append(new_page)
                        print(f"    + {new_page}")
            else:
                # find_or_create_target_group 内部出错时会抛出 RuntimeError
                # 这里可以加日志，但理论上不应到达
                 print(f"错误: 未能为 Tab='{tab_name}', Group='{group_name}', Nested='{nested_group_name}' 获取有效的 pages 列表进行添加。")
            # else: # 这个 else 分支现在不会被触发
            #     print(f"信息: 跳过向非目标 Tab '{tab_name}' 添加页面 (目标 Tab: '{target_tab_name}')。")


    # <-- 排序 Group (仅排序目标 Tab 内的 Group) -->
    print(f"正在排序 Tab '{target_tab_name}' 内的 Group...")
    if target_tab_nav and 'groups' in target_tab_nav: # 确保目标 Tab 和 groups 存在
        groups_list = [g for g in target_tab_nav['groups'] if isinstance(g, dict)]
        groups_list.sort(key=lambda g: get_group_sort_key(g, docs_config))
        target_tab_nav['groups'] = groups_list
        print(f"  已对 Tab '{target_tab_name}' 中的 Group 进行排序。")
    elif target_tab_nav:
         print(f"  Tab '{target_tab_name}' 中没有 'groups' 或为空，无需排序。")
    else:
         print(f"  未找到 Tab '{target_tab_name}'，无法排序 Group。")


    # 不再返回 docs_data，因为直接修改了传入的 navigation_data
    print(f"--- 完成处理版本: {docs_config['LANGUAGE_CODE']} / Tab: {docs_config['TARGET_TAB_NAME']} ---")


def load_docs_data(path):
    """加载 JSON 文件，处理文件不存在和格式错误的情况"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"信息: {path} 未找到，将创建新的结构。")
        return {"navigation": {"versions": []}} # 返回初始结构
    except json.JSONDecodeError as e:
        # 引发更具体的错误，而不是返回 None
        raise json.JSONDecodeError(f"错误: {path} 格式错误。无法继续。- {e.msg}", e.doc, e.pos)

def save_docs_data(path, data):
    """保存 JSON 数据到文件"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\n成功更新 {path}，包含所有已处理的版本。")
        # 不再需要返回 True/False，因为异常会处理失败情况
    except IOError as e:
        # 引发 IO 错误
        raise IOError(f"错误: 无法写入 {path} - {e}")
    except Exception as e:
        # 引发其他未知错误
        raise Exception(f"写入 {path} 时发生未知错误: {e}")

def process_configurations(configs, docs_path):
    """加载数据，处理所有有效配置，然后保存数据"""
    # 1. 加载初始数据
    try:
        current_docs_data = load_docs_data(docs_path)
    except json.JSONDecodeError as e:
        print(e) # 打印加载错误信息
        return # 加载失败则退出
    # current_docs_data 不会是 None，因为 load_docs_data 要么返回数据要么引发异常

    # 2. 确保基本结构存在
    navigation_data = current_docs_data.setdefault('navigation', {}) # 获取 navigation 字典
    navigation_data.setdefault('versions', [])

    # 3. 筛选有效配置
    valid_configs = []
    for config in configs:
        required_keys = ["DOCS_DIR", "LANGUAGE_CODE", "FILE_EXTENSION",
                         "PWX_TO_GROUP_MAP", "DESIRED_GROUP_ORDER",
                         "TARGET_TAB_NAME", "FILENAME_PATTERN"]
        if all(k in config for k in required_keys):
             # 可选：检查 PWX_TO_GROUP_MAP 和 DESIRED_GROUP_ORDER 是否为空
             # 并且检查 FILENAME_PATTERN 是否是编译后的正则表达式对象
             if (config.get("PWX_TO_GROUP_MAP") and
                 config.get("DESIRED_GROUP_ORDER") and
                 isinstance(config.get("FILENAME_PATTERN"), re.Pattern)):
                 valid_configs.append(config)
             else:
                 reason = []
                 if not config.get("PWX_TO_GROUP_MAP"): reason.append("PWX_TO_GROUP_MAP 为空或不存在")
                 if not config.get("DESIRED_GROUP_ORDER"): reason.append("DESIRED_GROUP_ORDER 为空或不存在")
                 if not isinstance(config.get("FILENAME_PATTERN"), re.Pattern): reason.append("FILENAME_PATTERN 不是有效的正则表达式对象")
                 print(f"警告: 配置 {config.get('LANGUAGE_CODE', '未知')} 无效 ({'; '.join(reason)})，跳过处理。")
        else:
             missing_keys = [k for k in required_keys if k not in config]
             print(f"警告: 配置 {config.get('LANGUAGE_CODE', '未知')} 不完整 (缺少: {', '.join(missing_keys)})，跳过处理。")

    # 4. 处理有效配置
    if not valid_configs:
         print("没有有效的配置可供处理。")
    else:
        try: # 包裹所有配置的处理过程
            for config in valid_configs:
                # 将 navigation_data 传递给 main 函数进行修改
                main(config, navigation_data) # main 函数会直接修改这个 navigation_data 字典

            # 5. 所有配置处理完毕后，统一写回文件
            save_docs_data(docs_path, current_docs_data)
        except (FileNotFoundError, ValueError, RuntimeError, IOError, Exception) as e:
             # 捕获 main 或 save_docs_data 中可能引发的已知错误
             print(f"\n处理过程中发生错误: {e}")
             print("操作已终止，文件可能未完全更新。")
             # 根据需要，可以在这里决定是否尝试保存部分结果或直接退出

if __name__ == "__main__":
    # 定义要处理的配置列表
    CONFIGS_TO_PROCESS = [
        PLUGIN_DEV_ZH,
        PLUGIN_DEV_EN,
        PLUGIN_DEV_JA,
    ]

    # 调用主处理函数
    process_configurations(CONFIGS_TO_PROCESS, DOCS_JSON_PATH)